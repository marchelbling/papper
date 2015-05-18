# -*- coding: utf-8 -*-
import requests
import json


class Reference(object):
    def __init__(self, label, bibitem):
        self.label = label
        self.bibtex = Reference.resolve(label, bibitem)

    @staticmethod
    def resolve(label, bibitem):
        # Let’s be naive:
        # http://labs.crossref.org/resolving-citations-we-dont-need-no-stinkin-parser/
        dois = Reference.query_dois({
            'q': '+'.join(bibitem.strip().split()),
            'sort': 'score'
        })
        if not dois:
            return Reference.parse()
        reference = Reference.resolve_doi(dois[0]['doi'])
        if reference:
            return Reference.set_label(label, reference)
        else:
            return Reference.reference_to_bibtex(dois[0])

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
    def set_label(label, reference):
        return ''.join([reference.split('{', 1)[0],
                        '{', label, ',',
                        reference.split(',', 1)[1]])

    def reference_to_bibtex(self, doi):
        raise NotImplementedError

    @staticmethod
    def parse(label, bibitem):
        raise NotImplementedError
