# -*- coding: utf-8 -*-

""" papper cli """

import argparse
from .bibliography import cli as bibliography_cli


def parse_papper_options():
    parser = argparse.ArgumentParser(description='Process bibliography:'
                                                 ' convert bbl to bibtex'
                                                 ' format')
    parser.add_argument('bib', default=False, action='store_true',
                        help='Convert bbl format to bibtex')
    return parser.parse_known_args()[0]


def papper_cli():
    options = parse_papper_options()

    if options.bib:
        bibliography_cli()


if __name__ == '__main__':
    papper_cli()
