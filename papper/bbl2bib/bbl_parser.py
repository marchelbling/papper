# -*- coding: utf-8 -*-

import os
from .document import Document


class BBLParser(object):
    @staticmethod
    def parse(path):
        folder = os.path.dirname(path)
        document, references = [], []

        def find_pattern(string, pattern):
            position = string.find(pattern)
            return position if position != -1 else None

        def inlined_bbl(line):
            return find_pattern(line, r'\input{') is not None and \
                   find_pattern(line, r'.bbl}') is not None

        def bbl_file(line):
            return os.path.join(folder,
                                line.split('{', 1)[1].split('}', 1)[0])

        def is_begin(line):
            return find_pattern(line, r'\begin{thebibliography}') is not None

        def is_end(line):
            return find_pattern(line, r'\end{thebibliography}') is not None

        def is_bib(line):
            return not is_begin(line) and not is_end(line)

        with open(path, 'r') as data:
            bibliography = False

            for line in data:
                if is_begin(line):
                    bibliography = True
                elif is_end(line) is not None:
                    bibliography = False

                if inlined_bbl(line):
                    try:
                        with open(bbl_file(line), 'r') as external_bbl:
                            bbl_lines = filter(is_bib,
                                               external_bbl.readlines())
                            references.append('\n'.join(bbl_lines))
                    except IOError:
                        print("Error while trying to read '{}'"
                              .format(bbl_file(line)))
                elif bibliography:
                    references.append(line)
                else:
                    document.append(line)

        return Document(content='\n'.join(document),
                        bbl='\n'.join(references))
