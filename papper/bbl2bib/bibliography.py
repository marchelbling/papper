# -*- coding: utf-8 -*-

from .reference import Reference
from .utils import unlatexify


class Bibliography(object):
    def __init__(self, bbl):
        self.bibitems = Bibliography.split_bibitem(bbl)
        self.references = []

    def process(self):
        self.references = map(lambda item: Reference(label=item[0],
                                                     bibitem=item[1]).bibtex,
                              self.bibitems)
        with open('/tmp/biblio.bib', 'w') as output:
            output.write('\n\n'.join(self.references))

    @staticmethod
    def split_bibitem(bbl):
        def extract_substring_in(string, begin, end):
            # it would be more robust to check parentheses count
            begin_index = string.find(begin)
            end_index = string.find(end)
            substring = string[begin_index + 1:end_index]
            return substring, string.replace(begin + substring + end, '', 1)

        # split each bibitem
        bibitems = bbl.split(r'\bibitem')
        # removes leading/trailing spaces
        bibitems = map(lambda item: item.strip(), bibitems)
        # filter empty reference
        bibitems = filter(None, bibitems)
        # filter citation name
        bibitems = map(lambda ref: extract_substring_in(ref, '[', ']')[1],
                       bibitems)
        # split reference alias and reference info
        bibitems = map(lambda ref: extract_substring_in(ref, '{', '}'),
                       bibitems)
        return map(unlatexify, bibitems)
