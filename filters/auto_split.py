import panflute as pf


def needs_to_split(text: str) -> bool:
    deep = 0
    escaped = False
    for i in range(len(text)):
        char = text[i]
        #print(char, deep, escaped)
        if not escaped:
            if char == '{':
                deep += 1
            elif char == '}':
                deep -= 1
            elif char == '\\':
                escaped = True
        else:
            if char == '\\' and deep == 0:
                return True
            if text[i:].startswith("begin"):
                if not text[i+len("begin")].isalpha():
                    deep += 1
            elif text[i:].startswith("end"):
                if not text[i+len("end")].isalpha():
                    deep -= 1
            escaped = False
    return False


def replace_math(elem, doc):
    if isinstance(elem, pf.Math):
        if needs_to_split(elem.text):
            elem.text = '\\begin{split}' + elem.text + '\\end{split}'
    return elem


def main(doc=None):
    return pf.run_filter(replace_math, doc=doc)


if __name__ == "__main__":
    main()
