import panflute as pf
import json

replacement = json.load(open(r"C:\Tools\pandoc-sitandr-build\filters\unicode_math.json", encoding='utf8'))

def replace_math(elem, doc):
    if isinstance(elem, pf.Math):
        for key in replacement.keys():
            elem.text = elem.text.replace(key, replacement[key]+' ')

    return elem


def main(doc=None):
    return pf.run_filter(replace_math, doc=doc)

if __name__ == "__main__":
    main()
