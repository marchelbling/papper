# -*- coding: utf-8 -*-

""" cli interface for bbl2bib """
__version__ = "0.0.1"

import argparse
from .bbl_parser import BBLParser


def parse_options():
    parser = argparse.ArgumentParser(description='Convert BBL into bib file.')
    parser.add_argument('input', type=str, default='', help='latex or bbl file to read')
    return parser.parse_args()


def main():
    options = parse_options()
    BBLParser(options.input)
