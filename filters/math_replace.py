import panflute as pf

replacement = {'−': '-',
               '≪': '\ll',
               '≫': '\gg',
               ' ': ' ',
               ' ': ' ',
               '≔': ':=',
               }

def replace_math(elem, doc):
    if isinstance(elem, pf.Math):
        for key in replacement.keys():
            elem.text = elem.text.replace(key, replacement[key])

    return elem


def main(doc=None):
    return pf.run_filter(replace_math, doc=doc)

if __name__ == "__main__":
    main()