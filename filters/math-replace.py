import panflute as pf
import json
import os

replacement = json.load(open(os.environ['SPB'] + r"\filters\unicode_math.json", encoding='utf8'))


def replace_unicode_with_math(elem, doc):
    if isinstance(elem, pf.Math):
        for key in replacement:
            elem.text = elem.text.replace(key, replacement[key]+' ')

    return elem

def replace_single_expr(text, expr, rep):
    ind = 0
    while True:
        i = text.find(expr, ind)
        if i == -1:
            return text
        if len(text) > i+len(expr) and text[i+len(expr)].isalpha():
            ind += 1
            continue
        text = text[:i] + rep + text[i+len(expr):]
        ind = i + len(rep)

def replace_math_with_unicode(elem, doc):
    if isinstance(elem, pf.Math):
        for key in replacement:
            if not replacement[key].isalpha():
                elem.text = replace_single_expr(elem.text,
                                                replacement[key], key)
    return elem


def replace_math(elem, doc):
    if doc.format == "markdown":
        return replace_math_with_unicode(elem, doc)
    return replace_unicode_with_math(elem, doc)


def main(doc=None):
    return pf.run_filter(replace_math, doc=doc)


if __name__ == "__main__":
    main()
