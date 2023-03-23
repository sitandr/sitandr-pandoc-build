import panflute as pf

def replace_blocks_with_tex(elem, doc):
    if isinstance(elem, pf.Div) and len(elem.classes) == 1:
        env = elem.classes[0]
        # pf.debug(env)
        return [pf.RawBlock(f"\\begin{{{env}}}", 'latex'),
                *elem.content,
                pf.RawBlock(f"\\end{{{env}}}", 'latex')]

def replace_blocks_with_caps(elem, doc):
    if isinstance(elem, pf.Div) and len(elem.classes) == 1:
        env = elem.classes[0]
        # pf.debug(env)
        return [pf.Plain(pf.Str(f"!{env.upper()}:\n\n")),
                *elem.content,
                pf.Plain(pf.Str(f":!\n\n"))]

def replace_block(elem, doc):
    if doc.format == 'latex':
        return replace_blocks_with_tex(elem, doc)
    return replace_blocks_with_caps(elem, doc)

def main(doc=None):
    return pf.run_filter(replace_block, doc=doc)

if __name__ == "__main__":
    main()
