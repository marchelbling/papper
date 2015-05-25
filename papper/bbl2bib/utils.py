# -*- coding: utf-8 -*-

import os


def safe_decode_string(value):
    try:
        return value.decode('utf8').encode('utf8')
    except UnicodeError:
        try:
            return value.decode('latin1').encode('utf8')
        except UnicodeError:
            return value.decode('utf8', errors='replace').encode('utf8')


def list_all_files(path, extensions=None):
    filenames = []
    path = os.path.abspath(path)
    for root, _, files in os.walk(safe_decode_string(path), topdown=True):
        filenames.extend(map(lambda x: os.path.join(root, safe_decode_string(x)), files))

    if extensions is not None:
        filenames = filter(lambda x: os.path.splitext(x)[-1] in extensions,
                           filenames)

    return filenames


def unlatexify(line):
    # see http://arxiv.org/help/prep#author
    return line.replace('\\"A', "Ä")\
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
