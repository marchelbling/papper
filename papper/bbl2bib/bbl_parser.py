# -*- coding: utf-8 -*-

import os
from .utils import list_all_files
from .bibliography import Bibliography


class BBLParser(object):
    r"""Extract bbl lines and return a Bibliography
    """
    @staticmethod
    def parse(path, output=None):
        if output is None:
            output = path if os.path.isdir(path) else os.path.dirname(path)
            output = os.path.join(output, 'ppr_biblio.bib')
        filenames = []
        if os.path.isdir(path):
            filenames = list_all_files(path, extensions=('.bbl', '.tex'))
        elif os.path.isfile(path):
            filenames = [path]

        bbl = []
        for filename in filenames:
            with open(filename, 'r') as fp:
                bbl.extend(BBLParser.parse_content(fp))
        return Bibliography('\n'.join(bbl)).format(output)

    @staticmethod
    def parse_content(fp):
        def find_pattern(string, pattern):
            position = string.find(pattern)
            return position if position != -1 else None

        def is_biblio_begin(line):
            return find_pattern(line, r'\begin{thebibliography}') is not None

        def is_biblio_end(line):
            return find_pattern(line, r'\end{thebibliography}') is not None

        bibliography = False
        references = []

        for line in fp:
            if is_biblio_begin(line):
                bibliography = True
            elif is_biblio_end(line):
                bibliography = False
            elif bibliography:
                references.append(line)
        return references
