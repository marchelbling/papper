# -*- coding: utf-8 -*-

import os
from .bibliography import Bibliography


class BBLParser(object):
    r"""Extract bbl lines and return a Bibliography
    """
    @staticmethod
    def parse(path):
        references = []

        def find_pattern(string, pattern):
            position = string.find(pattern)
            return position if position != -1 else None

        def is_external_bbl(line):
            return (find_pattern(line, r'\input{') is not None and
                    find_pattern(line, r'.bbl}') is not None) or \
                find_pattern(line, r'\bibliography{')

        def bbl_file(line):
            folder = os.path.dirname(path)
            bbl = line.split('{', 1)[1].split('}', 1)[0]
            if not os.path.isabs(bbl):
                bbl = os.path.join(folder, bbl)
            bbl += '.bbl'
            return bbl if os.path.exists(bbl) else None

        def default_bbl():
            return os.path.splitext(path)[0] + '.bbl'

        def is_biblio_begin(line):
            return find_pattern(line, r'\begin{thebibliography}') is not None

        def is_biblio_end(line):
            return find_pattern(line, r'\end{thebibliography}') is not None

        def is_biblio_tag(line):
            return not is_biblio_begin(line) and not is_biblio_end(line)

        def parse_external_biblio(line):
            bbl = bbl_file(line) or default_bbl()
            try:
                with open(bbl, 'r') as external_bbl:
                    bbl_lines = filter(is_biblio_tag,
                                       external_bbl.readlines())
            except IOError:
                print("Error while trying to read '{}'".format(bbl))
                bbl_lines = ''
            return '\n'.join(bbl_lines)

        with open(path, 'r') as data:
            bibliography = False

            for line in data:
                if is_biblio_begin(line):
                    bibliography = True
                elif is_biblio_end(line) is not None:
                    bibliography = False

                if is_external_bbl(line):
                    references.append(parse_external_biblio(line))
                elif bibliography:
                    references.append(line)

        return Bibliography('\n'.join(references))
