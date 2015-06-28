# -*- coding: utf-8 -*-

from .bibliography import Bibliography


class Document(object):
    def __init__(self, content, bbl):
        self.content = content
        self.bibliography = Bibliography(bbl).process()

    def format(self):
        pass
