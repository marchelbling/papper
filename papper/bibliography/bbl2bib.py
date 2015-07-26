# -*- coding: utf-8 -*-

import os
import re
import json
import requests

from . import bibliography


def bbl_to_bib(path):
    context = {}
    # 1. list all files
    context['filenames'] = list_all_files(path, extensions=('tex', 'bbl'))
    # 2. split content from bibliography
    context['bbl'] = reduce(lambda x, y: x + y,
                            map(parse_bibliography, context['filenames']))
    # 3. split bibliography
    context['bibitems'] = split_bibitems(context['bbl'])
    # 4. resolve reference
    context['bibliography'] = map(resolve, context['bibitems'])
    print(context['bibliography'])
    # 5. return formatted bibtex bibliography
    return '\n'.join(context['bibliography'])


def concatenate_dict_values(dictionaries):
    """
    >>> h = {'a': 'foo', 'b': 'bar'}
    >>> g = {'a': 'baz', 'c': 'buz'}
    >>> concatenate_dict_values([h, g])
    {'a': 'foo\\nbaz', 'c': 'buz', 'b': 'bar'}
    """
    keys = set().union(*dictionaries)
    return {key: '\n'.join(filter(None, [dictionary.get(key, '')
                                         for dictionary in dictionaries]))
            for key in keys}


def extract(string, begin, end):
    """
    >>> extract('foo', '[', ']')
    ('', 'foo')
    >>> extract('[foo[]', '[', ']')
    ('foo[', '')
    >>> extract('[foo]]', '[', ']')
    ('foo', ']')
    >>> extract('bar[foo]baz', '[', ']')
    ('foo', 'bar baz')
    """
    # it would be more robust to check parentheses count
    begin_index = string.find(begin)
    end_index = string.find(end)
    if begin_index != -1 and end_index != -1:
        return (string[begin_index + 1:end_index],
                ' '.join((string[:begin_index], string[end_index+1:])).strip())
    else:
        return ('', string)


def list_all_files(path, discard=None, extensions=None):
    filenames = []
    path = os.path.abspath(path)
    for root, _, files in os.walk(path, topdown=True):
        filenames.extend(map(lambda x: os.path.join(root, x), files))

    if discard is not None:
        discard = set(discard)
        filenames = filter(lambda x: x not in discard, filenames)

    if extensions:
        filenames = filter(lambda x: any(map(x.endswith, extensions)),
                           filenames)

    return filenames


def parse_bibliography(filename):
    references = []

    def find_pattern(string, pattern):
        position = string.find(pattern)
        return position if position != -1 else None

    def is_inlined_bbl(line):
        return (find_pattern(line, r'\input{') is not None and
                find_pattern(line, r'.bbl}') is not None) or \
            find_pattern(line, r'\bibliography{')

    def bbl_file(line):
        folder = os.path.dirname(filename)
        bbl = line.split('{', 1)[1].split('}', 1)[0]
        if not os.path.isabs(bbl):
            bbl = os.path.join(folder, bbl)
        bbl += '.bbl'
        return bbl if os.path.exists(bbl) else None

    def default_bbl():
        return os.path.splitext(filename)[0] + '.bbl'

    def is_biblio_begin(line):
        return find_pattern(line, r'\begin{thebibliography}') is not None

    def is_biblio_end(line):
        return find_pattern(line, r'\end{thebibliography}') is not None

    def is_bib(line):
        return not is_biblio_begin(line) and not is_biblio_end(line)

    def is_comment(line):
        return line.startswith('%')

    def parse_inline_biblio(line):
        bbl = bbl_file(line) or default_bbl()
        try:
            with open(bbl, 'r') as external_bbl:
                bbl_lines = filter(is_bib,
                                   external_bbl.readlines())
        except IOError:
            print("Error while trying to read '{}'".format(bbl))
            bbl_lines = ''
        return '\n'.join(bbl_lines)

    with open(filename, 'r') as data:
        biblio = False

        for line in data:
            if is_biblio_begin(line):
                biblio = True
                continue
            elif is_biblio_end(line):
                biblio = False
                continue
            elif is_comment(line):
                continue

            if is_inlined_bbl(line):
                references.append(parse_inline_biblio(line))
            elif bibliography:
                references.append(line)

    return '\n'.join(references)


def split_bibitems(bbl):
    """
    >>> split_bibitems('\\\\bibitem{foo1} bar1 \\n\\\\bibitem{foo2} bar2')
    [{'raw': 'bar1', 'label': 'foo1'}, {'raw': 'bar2', 'label': 'foo2'}]
    """

    # split each bibitem
    bibitems = bbl.split(r'\bibitem')
    # removes leading/trailing spaces
    bibitems = map(lambda item: item.strip(), bibitems)
    # filter empty reference
    bibitems = filter(None, bibitems)
    # filter reference alias and citation
    bibitems = map(lambda ref: extract(ref, '{', '}'), bibitems)
    return [{'label': bibitem[0], 'raw': bibitem[1].strip()}
            for bibitem in bibitems]


def unlatexify(content):
    # see http://arxiv.org/help/prep#author
    blocks = re.compile('\\\\newblock')
    blanks = re.compile('\s+')
    strip = lambda regexp, string: regexp.sub(' ', string)

    return strip(blanks, strip(blocks, content))\
        .replace('\\"A', "Ä")\
        .replace('\\"a', "ä")\
        .replace("\\'A", "Á")\
        .replace("\\'a", "á")\
        .replace("\\.A", "Ȧ")\
        .replace("\\.a", "ȧ")\
        .replace("\\=A", "Ā")\
        .replace("\\=a", "ā")\
        .replace("\\^A", "Â")\
        .replace("\\^a", "â")\
        .replace("\\`A", "À")\
        .replace("\\`a", "à")\
        .replace("\\k{A}", "Ą")\
        .replace("\\k{a}", "ą")\
        .replace("\\r{A}", "Å")\
        .replace("\\r{a}", "å")\
        .replace("\\u{A}", "Ă")\
        .replace("\\u{a}", "ă")\
        .replace("\\v{A}", "Ǎ")\
        .replace("\\v{a}", "ǎ")\
        .replace("\\~A", "Ã")\
        .replace("\\~a", "ã")\
        .replace("\\'C", "Ć")\
        .replace("\\'c", "ć")\
        .replace("\\.C", "Ċ")\
        .replace("\\.c", "ċ")\
        .replace("\\^C", "Ĉ")\
        .replace("\\^c", "ĉ")\
        .replace("\\c{C}", "Ç")\
        .replace("\\c{c}", "ç")\
        .replace("\\v{C}", "Č")\
        .replace("\\v{c}", "č")\
        .replace("\\v{D}", "Ď")\
        .replace("\\v{d}", "ď")\
        .replace('\\"E', "Ë")\
        .replace('\\"e', "ë")\
        .replace("\\'E", "É")\
        .replace("\\'e", "é")\
        .replace("\\.E", "Ė")\
        .replace("\\.e", "ė")\
        .replace("\\=E", "Ē")\
        .replace("\\=e", "ē")\
        .replace("\\^E", "Ê")\
        .replace("\\^e", "ê")\
        .replace("\\`E", "È")\
        .replace("\\`e", "è")\
        .replace("\\c{E}", "Ȩ")\
        .replace("\\c{e}", "ȩ")\
        .replace("\\k{E}", "Ę")\
        .replace("\\k{e}", "ę")\
        .replace("\\u{E}", "Ĕ")\
        .replace("\\u{e}", "ĕ")\
        .replace("\\v{E}", "Ě")\
        .replace("\\v{e}", "ě")\
        .replace("\\.G", "Ġ")\
        .replace("\\.g", "ġ")\
        .replace("\\^G", "Ĝ")\
        .replace("\\^g", "ĝ")\
        .replace("\\c{G}", "Ģ")\
        .replace("\\c{g}", "ģ")\
        .replace("\\u{G}", "Ğ")\
        .replace("\\u{g}", "ğ")\
        .replace("\\v{G}", "Ǧ")\
        .replace("\\v{g}", "ǧ")\
        .replace("\\^H", "Ĥ")\
        .replace("\\^h", "ĥ")\
        .replace("\\v{H}", "Ȟ")\
        .replace("\\v{h}", "ȟ")\
        .replace('\\"I', "Ï")\
        .replace('\\"i', "ï")\
        .replace("\\'I", "Í")\
        .replace("\\'i", "í")\
        .replace("\\.I", "İ")\
        .replace("\\=I", "Ī")\
        .replace("\\=i", "ī")\
        .replace("\\^I", "Î")\
        .replace("\\^i", "î")\
        .replace("\\`I", "Ì")\
        .replace("\\`i", "ì")\
        .replace("\\k{I}", "Į")\
        .replace("\\k{i}", "į")\
        .replace("\\u{I}", "Ĭ")\
        .replace("\\u{i}", "ĭ")\
        .replace("\\v{I}", "Ǐ")\
        .replace("\\v{i}", "ǐ")\
        .replace("\\~I", "Ĩ")\
        .replace("\\~i", "ĩ")\
        .replace("\\^J", "Ĵ")\
        .replace("\\^j", "ĵ")\
        .replace("\\c{K}", "Ķ")\
        .replace("\\c{k}", "ķ")\
        .replace("\\v{K}", "Ǩ")\
        .replace("\\v{k}", "ǩ")\
        .replace("\\'L", "Ĺ")\
        .replace("\\'l", "ĺ")\
        .replace("\\c{L}", "Ļ")\
        .replace("\\c{l}", "ļ")\
        .replace("\\v{L}", "Ľ")\
        .replace("\\v{l}", "ľ")\
        .replace("\\'N", "Ń")\
        .replace("\\'n", "ń")\
        .replace("\\c{N}", "Ņ")\
        .replace("\\c{n}", "ņ")\
        .replace("\\v{N}", "Ň")\
        .replace("\\v{n}", "ň")\
        .replace("\\~N", "Ñ")\
        .replace("\\~n", "ñ")\
        .replace('\\"O', "Ö")\
        .replace('\\"o', "ö")\
        .replace("\\'O", "Ó")\
        .replace("\\'o", "ó")\
        .replace("\\.O", "Ȯ")\
        .replace("\\.o", "ȯ")\
        .replace("\\=O", "Ō")\
        .replace("\\=o", "ō")\
        .replace("\\^O", "Ô")\
        .replace("\\^o", "ô")\
        .replace("\\`O", "Ò")\
        .replace("\\`o", "ò")\
        .replace("\\H{O}", "Ő")\
        .replace("\\H{o}", "ő")\
        .replace("\\k{O}", "Ǫ")\
        .replace("\\k{o}", "ǫ")\
        .replace("\\u{O}", "Ŏ")\
        .replace("\\u{o}", "ŏ")\
        .replace("\\v{O}", "Ǒ")\
        .replace("\\v{o}", "ǒ")\
        .replace("\\~O", "Õ")\
        .replace("\\~o", "õ")\
        .replace("\\'R", "Ŕ")\
        .replace("\\'r", "ŕ")\
        .replace("\\c{R}", "Ŗ")\
        .replace("\\c{r}", "ŗ")\
        .replace("\\v{R}", "Ř")\
        .replace("\\v{r}", "ř")\
        .replace("\\'S", "Ś")\
        .replace("\\'s", "ś")\
        .replace("\\^S", "Ŝ")\
        .replace("\\^s", "ŝ")\
        .replace("\\c{S}", "Ş")\
        .replace("\\c{s}", "ş")\
        .replace("\\v{S}", "Š")\
        .replace("\\v{s}", "š")\
        .replace("\\c{T}", "Ţ")\
        .replace("\\c{t}", "ţ")\
        .replace("\\v{T}", "Ť")\
        .replace("\\v{t}", "ť")\
        .replace('\\"U', "Ü")\
        .replace('\\"u', "ü")\
        .replace("\\'U", "Ú")\
        .replace("\\'u", "ú")\
        .replace("\\=U", "Ū")\
        .replace("\\=u", "ū")\
        .replace("\\^U", "Û")\
        .replace("\\^u", "û")\
        .replace("\\`U", "Ù")\
        .replace("\\`u", "ù")\
        .replace("\\H{U}", "Ű")\
        .replace("\\H{u}", "ű")\
        .replace("\\k{U}", "Ų")\
        .replace("\\k{u}", "ų")\
        .replace("\\r{U}", "Ů")\
        .replace("\\r{u}", "ů")\
        .replace("\\u{U}", "Ŭ")\
        .replace("\\u{u}", "ŭ")\
        .replace("\\v{U}", "Ǔ")\
        .replace("\\v{u}", "ǔ")\
        .replace("\\~U", "Ũ")\
        .replace("\\~u", "ũ")\
        .replace("\\^W", "Ŵ")\
        .replace("\\^w", "ŵ")\
        .replace('\\"Y', "Ÿ")\
        .replace('\\"y', "ÿ")\
        .replace("\\'Y", "Ý")\
        .replace("\\'y", "ý")\
        .replace("\\=Y", "Ȳ")\
        .replace("\\=y", "ȳ")\
        .replace("\\^Y", "Ŷ")\
        .replace("\\^y", "ŷ")\
        .replace("\\'Z", "Ź")\
        .replace("\\'z", "ź")\
        .replace("\\.Z", "Ż")\
        .replace("\\.z", "ż")\
        .replace("\\v{Z}", "Ž")\
        .replace("\\v{z}", "ž")\
        .replace("{\\aa}", "å")\
        .replace("{\\AA}", "Å")\
        .replace("{\\ae}", "æ")\
        .replace("{\\AE}", "Æ")\
        .replace("{\\DH}", "Ð")\
        .replace("{\\dh}", "ð")\
        .replace("{\\dj}", "đ")\
        .replace("{\\DJ}", "Đ")\
        .replace("{\\eth}", "ð")\
        .replace("{\\ETH}", "Ð")\
        .replace("{\\i}", "ı")\
        .replace("{\\I}", "ł")\
        .replace("{\\L}", "Ł")\
        .replace("{\\ng}", "ŋ")\
        .replace("{\\NG}", "Ŋ")\
        .replace("{\\O}", "Ø")\
        .replace("{\\o}", "ø")\
        .replace("{\\oe}", "œ")\
        .replace("{\\OE}", "Œ")\
        .replace("{\\ss}", "ß")\
        .replace("{\\th}", "þ")\
        .replace("{\\TH}", "Þ")\
        .replace("~", " ")\
        .replace("\mbox{.}", "")


def crossref(reference):
    def query_dois(filters):
        response = requests.get('http://search.labs.crossref.org/dois',
                                params=filters)
        return json.loads(response.content) if response.ok else None

    def resolve_doi(doi):
        headers = {'Accept': 'application/x-bibtex'}
        response = requests.get(doi, headers=headers)
        return response.content if response.ok else None

    # http://labs.crossref.org/resolving-citations-we-dont-need-no-stinkin-parser
    candidates = query_dois({
        'q': '+'.join(reference.strip().split()),
        'sort': 'score'
    })

    return resolve_doi(candidates[0]['doi']) if candidates else None


def parse(reference):
    # FIXME: we should parse reference to label each reference fields
    return bibliography.Misc(json={'note': unlatexify(reference)}).to_bibtex()


def set_label(reference, label):
    """
    >>> set_label('@misc{bar, title = "toto"}', 'foo')
    '@misc{foo, title = "toto"}'
    """
    return ''.join([reference.split('{', 1)[0],
                    '{', label, ',',
                    reference.split(',', 1)[1]])


def resolve(reference):
    resolved = crossref(reference['raw']) or parse(reference['raw'])
    return set_label(resolved, reference['label'])
