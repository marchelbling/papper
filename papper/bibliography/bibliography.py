def one(args):
    """
    >>> one([True, False])
    True
    >>> one([True, True])
    False
    >>> one([False, False])
    False
    >>> one([0, 1, []])
    True
    >>> one([0, 1, [], [0]])
    False
    """
    return len(filter(None, args)) == 1


class Or(object):
    """
    >>> _or = Or('foo', 'bar')
    >>> _or.inside({'foo': 'foo', 'baz': 'baz'})
    'foo'
    >>> _or.inside({'foo': 'foo', 'bar': 'baz'})
    'foo'
    >>> _or.inside({'buz': 'buz', 'baz': 'baz'})
    Traceback (most recent call last):
    ...
    AssertionError: Or(('foo', 'bar')) not found in {'buz': 'buz', 'baz': 'baz'}
    """
    def __init__(self, *args):
        self.fields = args

    def inside(self, entries):
        content = map(entries.get, self.fields)
        assert any(content), "Or({}) not found in {}".format(self.fields, entries)
        return filter(None, content)[0]


class Xor(object):
    """
    >>> xor = Xor('foo', 'bar')
    >>> xor.inside({'foo': 'foo', 'baz': 'baz'})
    'foo'
    >>> xor.inside({'foo': 'foo', 'bar': 'bar'})
    Traceback (most recent call last):
    ...
    AssertionError: Xor(('foo', 'bar')) not found in {'foo': 'foo', 'bar': 'bar'}
    >>> xor.inside({'buz': 'buz', 'baz': 'baz'})
    Traceback (most recent call last):
    ...
    AssertionError: Xor(('foo', 'bar')) not found in {'buz': 'buz', 'baz': 'baz'}
    """
    def __init__(self, *args):
        self.fields = args

    def inside(self, entries):
        content = map(entries.get, self.fields)
        assert one(content), "Xor({}) not found in {}".format(self.fields, entries)
        return filter(None, content)[0]


# from http://nwalsh.com/tex/texhelp/bibtx-7.html
class Entry(object):
    """
    >>> entry = Entry(json={
    ...     'author': 'foo',
    ...     'title': 'bar',
    ...     'pages': '05--17',
    ...     'title': 'foo',
    ...     'publisher': 'baz',
    ...     'year': 2013})
    >>> entry['author']
    'foo'
    >>> entry[Xor('author', 'editor')]
    'foo'
    >>> entry[Or('author', 'title', 'note')]
    'foo'
    >>> entry.is_valid()
    True
    >>> article = Article(json=entry.entries)
    >>> article.is_valid()
    False
    >>> article.entries['journal'] = 'paywall'
    >>> article.is_valid()
    True
    >>> print article.to_bibtex()
    """
    spec = {
        'required': [],
        'optional': [],
        'format': ''
    }

    def __init__(self, **kwargs):
        self.entries = kwargs['json'] if kwargs.get('json') \
            else self.from_bibtex(kwargs['bibtex'])

    @staticmethod
    def _format_bibtex_entry(key, value):
        return '\n\t{key} = {{{value}}}'.format(key=key, value=value) if value else ''

    @property
    def _spec(self):
        return self.__class__.spec

    def _format_bibtex_required(self):
        bibtex_entry = Entry._format_bibtex_entry
        return ','.join(map(lambda key: bibtex_entry(key, self[key]),
                            self._spec['required']))

    def _format_bibtex_optional(self):
        bibtex_entry = Entry._format_bibtex_entry
        return ','.join(filter(None,
                               map(lambda key: bibtex_entry(key, self[key]),
                                   self._spec['optional'])))

    def is_valid(self):
        return all(self[key] for key in self.__class__.spec['required'])

    def to_bibtex(self, label=None):
        required = self._format_bibtex_required()
        optional = self._format_bibtex_optional()
        sep = ',' if required and optional else ''
        return self._spec['format'].format(label=label,
                                           required=required,
                                           sep=sep,
                                           optional=optional)

    def __getitem__(self, key):
        try:
            if isinstance(key, (Xor, Or)):
                return key.inside(self.entries)
            else:
                return self.entries[key]
        except KeyError:
            return None


class Article(Entry):
    spec = {
        'type': 'article',
        'required': ['author', 'title', 'journal', 'year'],
        'optional': ['volume', 'number', 'pages', 'month', 'note', 'type'],
        'format': '@ARTICLE{{{label},'
                  ' {required}{sep}{optional}'
                  '}}'
    }


class Book(Entry):
    spec = {
        'type': 'book',
        'required': [Xor('author', 'editor'), 'title', 'publisher',
                     'year'],
        'optional': ['volume', 'series', 'address', 'edition', 'month', 'note',
                     'type'],
        'format': '@BOOK{{{label},'
                  ' {required}{sep}{optional}'
                  '}}'
    }


class Booklet(Entry):
    spec = {
        'type': 'booklet',
        'required': ['title'],
        'optional': ['author', 'howpublished', 'address', 'month', 'year',
                     'note', 'type'],
        'format': '@BOOKLET{{{label},'
                  ' {required}{sep}{optional}'
                  '}}'
    }


class Conference(Entry):
    spec = {
        'type': 'conference',
        'required': ['author', 'title', 'booktitle', 'year'],
        'optional': ['editor', 'pages', 'organization', 'publisher', 'address',
                     'month', 'note', 'type'],
        'format': '@CONFERENCE{{{label},'
                  ' {required}{sep}{optional}'
                  '}}'
    }


class InBook(Entry):
    spec = {
        'type': 'inbook',
        'required': ['author', 'title', 'booktitle', 'year'],
        'required': [Xor('author', 'editor'), 'title',
                     Or('chapter', 'pages'), 'publisher', 'year'],
        'optional': ['volume', 'series', 'address', 'edition', 'month', 'note',
                     'type'],
        'format': '@INBOOK{{{label},'
                  ' {required}{sep}{optional}'
                  '}}'
    }


class InCollection(Entry):
    spec = {
        'type': 'incollection',
        'required': ['author', 'title', 'booktitle', 'year'],
        'optional': ['editor', 'pages', 'organization', 'publisher', 'address',
                     'month', 'note', 'type'],
        'format': '@INCOLLECTION{{{label},'
                  ' {required}{sep}{optional}'
                  '}}'
    }


class InProceedings(Entry):
    spec = {
        'type': 'inproceedings',
        'required': ['author', 'title', 'booktitle', 'year'],
        'optional': ['editor', 'pages', 'organization', 'publisher', 'address',
                     'month', 'note', 'type'],
        'format': '@INPROCEEDINGS{{{label},'
                  ' {required}{sep}{optional}'
                  '}}'
    }


class Manual(Entry):
    spec = {
        'type': 'manual',
        'required': ['title'],
        'optional': ['author', 'organization', 'address', 'edition', 'month',
                     'year', 'note', 'type'],
        'format': '@MANUAL{{{label},'
                  ' {required}{sep}{optional}'
                  '}}'
    }


class MasterThesis(Entry):
    spec = {
        'type': 'masterthesis',
        'required': ['author', 'title', 'school', 'year'],
        'optional': ['address', 'month', 'note', 'type'],
        'format': '@MASTERSTHESIS{{{label},'
                  ' {required}{sep}{optional}'
                  '}}'
    }


class Misc(Entry):
    spec = {
        'type': 'misc',
        'required': [],
        'optional': ['author', 'title', 'howpublished', 'month', 'year',
                     'note', 'type'],
        'format': '@MISC{{{label},'
                  ' {required}{sep}{optional}'
                  '}}'
    }


class PhdThesis(Entry):
    spec = {
        'type': 'phdthesis',
        'required': ['author', 'title', 'school', 'year'],
        'optional': ['address', 'month', 'note', 'type'],
        'format': '@PHDTHESIS{{{label},'
                  ' {required}{sep}{optional}'
                  '}}'
    }


class Proceedings(Entry):
    spec = {
        'type': 'proceedings',
        'required': ['title', 'year'],
        'optional': ['editor', 'publisher', 'organization', 'address', 'month',
                     'note', 'type'],
        'format': '@PROCEEDINGS{{{label},'
                  ' {required}{sep}{optional}'
                  '}}'
    }


class TechReport(Entry):
    spec = {
        'type': 'techreport',
        'required': ['author', 'title', 'institution', 'year'],
        'optional': ['type', 'number', 'address', 'month', 'note', 'type'],
        'format': '@TECHREPORT{{{label},'
                  ' {required}{sep}{optional}'
                  '}}'
    }


class Unpublished(Entry):
    spec = {
        'type': 'unpublished',
        'required': ['author', 'title', 'note'],
        'optional': ['month', 'year', 'type'],
        'format': '@UNPUBLISHED{{{label},'
                  ' {required}{sep}{optional}'
                  '}}'
    }


class Bibtex(object):
    entries = [Article, Book, Booklet, Conference, InBook, InCollection,
               InProceedings, Manual, MasterThesis, Misc, PhdThesis,
               Proceedings, TechReport, Unpublished]

    def __init__(self, **kwargs):
        pass
