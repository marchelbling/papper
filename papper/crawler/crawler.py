import requests
import time
import os


DATA_DIR = os.environ.get('DATA_PATH', '/data/')
ARXIV_XML_DIR = os.path.join(DATA_DIR, 'arxiv', 'xml')
REQUEST_DELAY = 21


def wait(delay):
    def decorator(method):
        def clocked(self, *args, **kwargs):
            if self.clock:
                elapsed = time.time() - self.clock
                if elapsed < delay:
                    time.sleep(delay - elapsed)
            result = method(self, *args, **kwargs)
            self.clock = time.time()
            return result
        return clocked
    return decorator


class ArxivCrawler(object):
    @staticmethod
    def get_last_cursor():
        xmls = filter(lambda x: os.path.splitext(x)[-1] == '.xml',
                      filter(lambda x: os.path.isfile(os.path.join(ARXIV_XML_DIR, x)),
                             os.listdir(ARXIV_XML_DIR)))
        return os.path.splitext(sorted(xmls)[-1])[0].split('_')[-1] if xmls else None

    @staticmethod
    def base_url():
        return 'http://export.arxiv.org/oai2?verb=ListRecords'

    def __init__(self):
        self.cursor = ArxivCrawler.get_last_cursor() or '0001'
        self.token = None
        self.clock = None

    @property
    def url(self):
        if self.token is None:
            return ArxivCrawler.base_url() + '&metadataPrefix=arXivRaw'
        else:
            return ArxivCrawler.base_url() + '&resumptionToken={}'.format(self.resumption_token)

    @property
    def resumption_token(self):
        return '{}|{}'.format(self.token, self.cursor)

    def update(self, string):
        begin = '<resumptionToken'
        end = '</resumptionToken'
        try:
            self.token, cursor = string[string.find(begin):string.rfind(end)]\
                                 .split('>')[1]\
                                 .split('|')
            self.cursor = max(int(self.cursor), int(cursor))
        except ValueError:
            self.cursor = None

    @wait(REQUEST_DELAY)
    def fetch(self):
        print('Fetching {}'.format(self.url))
        return requests.get(self.url)

    def crawl(self):
        while self.cursor:
            response = self.fetch()
            if response.status_code == 200:
                self.dump_xml(response.content)
                self.update(response.content)
            else:
                print(response.content)
                return

    def dump_xml(self, xml):
        filename = 'arxiv_{}.xml'.format(self.cursor)
        with open(os.path.join(ARXIV_XML_DIR, filename), 'w') as output:
            output.write(xml)


if __name__ == '__main__':
    ArxivCrawler().crawl()
