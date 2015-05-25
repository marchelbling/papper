# -*- coding: utf-8 -*-
import re
import requests
import json


class Reference(object):
    def __init__(self, label, bibitem):
        self.label = label
        self.reference = self.resolve(bibitem)

    @property
    def bibtex(self):
        labelify = re.compile('{.*?,')
        return labelify.sub(self.reference,
                            '{' + self.label + ',', 1)

    def resolve(self, bibitem):
        # Let’s be naive:
        # http://labs.crossref.org/resolving-citations-we-dont-need-no-stinkin-parser/
        dois = self.query_dois({
            'q': '+'.join(bibitem.strip().split()),
            'sort': 'score'
        })
        if not dois:
            return self.parse()

        crossref = dois[0]
        return self.resolve_doi(crossref['doi']) or \
            self.crossref_to_bibtex(crossref)

    def query_dois(self, filters):
        response = requests.get('http://search.labs.crossref.org/dois',
                                params=filters)
        if not response.ok:
            return []
        return json.loads(response.content)

    def resolve_doi(self, doi):
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

    def parse(self):
        return 'Missing data for {}'.format(self.label)
        raise NotImplementedError
