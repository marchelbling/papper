# -*- coding: utf-8 -*-

import argparse
import os
from bbl2bib import bbl_to_bib


def parse_bibliography_options():
    parser = argparse.ArgumentParser(description='Process bibliography:'
                                                 ' convert bbl to bibtex'
                                                 ' format')
    parser.add_argument('input', type=str, default='',
                        help='Path to folder to be processed')

    options = parser.parse_known_args()[0]
    if os.path.isfile(options.input):
        options.input = os.path.dirname(options.input)
    return options


def cli():
    options = parse_bibliography_options()
    bbl_to_bib(options.input)
