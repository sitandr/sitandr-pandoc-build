import panflute as pf
# import json
# import os

replacement = ['pmatrix', 'matrix', 'cases']


def replace(text, key):
    while (start := text.find('\\' + key)) > -1:
        l = len(key) + 1
        if start == -1:
            continue

        brace_start = None
        deep = 0
        escaped = False
        for i in range(start + l, len(text)):
            char = text[i]
            if not escaped:
                if char == '{':
                    if not brace_start:
                        brace_start = i
                    deep += 1
                elif char == '}':
                    deep -= 1
                    if deep == 0:
                        break
                elif char == '\\':
                    escaped = True
            else:
                escaped = False
        text = text[:start] + f'\\begin{{{key}}}' \
               + text[brace_start + 1: i] + f'\\end{{{key}}}' \
               + text[i + 1:]
    return text


def replace_math(elem, doc):
    if isinstance(elem, pf.Math):
        for key in replacement:
            elem.text = replace(elem.text, key)
    return elem


def main(doc=None):
    return pf.run_filter(replace_math, doc=doc)


if __name__ == "__main__":
    main()
