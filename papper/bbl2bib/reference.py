import requests
import json


class Reference(object):
    def __init__(self, label, bibitem):
        self.label = label
        self.bibitem = bibitem
        self.reference = self.resolve()

    def resolve(self):
        # Let’s be naive:
        # http://labs.crossref.org/resolving-citations-we-dont-need-no-stinkin-parser/
        dois = self.query_dois({
            'q': '+'.join(self.bibitem.strip().split()),
            'sort': 'score'
        })
        if not dois:
            return self.parse()
        reference = self.resolve_doi(dois[0]['doi'])
        if reference:
            return self.set_label(reference)
        else:
            return self.doi_to_bibtex(dois[0])

    def query_dois(self, filters):
        response = requests.get('http://search.labs.crossref.org/dois',
                                params=filters)
        if not response.ok:
            return []
        return json.loads(response.content)

    def resolve_doi(self, doi):
        # That’s already pretty cool. But if you extract the DOI from the above and use DOI content negotiation to query the the DOI like this:
        # $ curl -LH "Accept: application/x-bibtex" http://dx.doi.org/10.5555/12345678
        # You get the following result in BibTex:
        headers = {
            'Accept': 'application/x-bibtex'
        }
        response = requests.get(doi, headers=headers)
        if not response.ok:
            return None
        return response.content

    def set_label(self, reference):
        return ''.join([reference.split('{', 1)[0],
                        self.label,
                        reference.split(',', 1)[1]])

    def doi_to_bibtex(self, doi):
        raise NotImplementedError

    def parse(self):
        raise NotImplementedError
