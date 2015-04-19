# -*- coding: utf-8 -*-
import re
import requests
import json


class Reference(object):
    def __init__(self, label, bibitem):
        self.label = label
        self.reference = Reference.resolve(bibitem)

    def set_label(self):
        labelify = re.compile('{.*?,')
        self.reference = labelify.sub(self.reference,
                                      '{' + self.label + ',', 1)

    @staticmethod
    def resolve(bibitem):
        # Let’s be naive:
        # http://labs.crossref.org/resolving-citations-we-dont-need-no-stinkin-parser/
        dois = Reference.query_dois({
            'q': '+'.join(bibitem.strip().split()),
            'sort': 'score'
        })
        if not dois:
            return Reference.parse()

        crossref = dois[0]
        return Reference.resolve_doi(crossref['doi']) or \
            Reference.crossref_to_bibtex(crossref)

    @staticmethod
    def query_dois(filters):
        response = requests.get('http://search.labs.crossref.org/dois',
                                params=filters)
        if not response.ok:
            return []
        return json.loads(response.content)

    @staticmethod
    def resolve_doi(doi):
        headers = {
            'Accept': 'application/x-bibtex'
        }
        response = requests.get(doi, headers=headers)
        if not response.ok:
            return None
        return response.content

    @staticmethod
    def crossref_to_bibtex(self, doi):
        raise NotImplementedError

    @staticmethod
    def parse(label, bibitem):
        raise NotImplementedError
