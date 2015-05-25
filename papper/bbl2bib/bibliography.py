# -*- coding: utf-8 -*-

from .reference import Reference
from .utils import unlatexify


class Bibliography(object):
    def __init__(self, bbl):
        self.references = [Reference(label=item[0], bibitem=item[1])
                           for item in Bibliography.split_bibitem(bbl)]

    def format(self, path):
        with open(path, 'w') as output:
            output.write('\n\n'.join(map(lambda reference: reference.bibtex,
                                         self.references)))

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
        # remove latex char sequences
        bibitems = map(unlatexify, bibitems)
        # filter citation name
        bibitems = map(lambda ref: extract_substring_in(ref, '[', ']')[1],
                       bibitems)
        # split reference alias and reference info
        return map(lambda ref: extract_substring_in(ref, '{', '}'),
                   bibitems)
