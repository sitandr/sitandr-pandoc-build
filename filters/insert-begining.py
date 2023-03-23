import panflute as pf
import json
import os

begin_environments = json.load(open(os.environ['SPB'] + r"\filters\latex_begins.json", encoding='utf8'))

def block_iterator(elem):
    """Replaces

!<env>:
<…>
:!

with \begin{…}…\end{…} (multiline)"""
    inside = []
    
    for par_num in range(len(elem.content)):
        par = elem.content[par_num]
        # pf.debug("NEXT_PAR:", pf.stringify(par), inside, type(par))

        if check_string_at(par, 0):
            env = get_env(par.content[0].text)
            if env:
                par.content[0] = pf.RawInline(f"\\begin{{{env}}}", "latex")
                inside.append(env)

            elem.content[par_num] = par

        if check_string_at(par, -1):            
            if par.content[-1].text.strip() == ":!":
                if not inside:
                    pf.debug("WARNING: no actual environment at :!")
                    continue
                env = inside.pop()
                par.content[-1] = pf.RawInline(f"\\end{{{env}}}", "latex")
                
                elem.content[par_num] = par

    return elem
        

def str_iterator(block):
    """Replaces !<env>:<…>:! with \begin{…}…\end{…} (inline)"""

    inside = False
    for par_num in range(len(elem.content)):
        par = elem.content[par_num]
        pf.debug("NEXT_PAR:", pf.stringify(par), inside)


def get_env(text):
    head = text.strip()
    #pf.debug(head)

    if not (head[0] == "!" and head[-1] == ":"):
        return
    
    #if not(head[1:-1] in begin_environments):
    #    pf.debug("Invalid environment: " + head[1:-1])
    #    return
    
    return head[1:-1].lower()#begin_environments[head[1:-1]]


def check_string_at(par, i=0):
    return (isinstance(par, pf.Block)
            and hasattr(par, "content")
            and type(par.content[i]) == pf.Str)


def replace_blocks(elem, doc):
    if (isinstance(elem, pf.Doc)
        or isinstance(elem, pf.BlockQuote)
        or isinstance(elem, pf.Definition)
        or isinstance(elem, pf.Div)
        or isinstance(elem, pf.Note)
        or isinstance(elem, pf.ListItem)):
        return block_iterator(elem)

    
   
def main(doc=None):
    return pf.run_filter(replace_blocks, doc=doc)

if __name__ == "__main__":
    main()
