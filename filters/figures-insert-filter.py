import panflute as pf

def convert_percents(percents: str) -> float:
    if percents[-1] != "%":
        return float(percents)
    return float(percents[:-1])/100

def figure_insert(elem, doc):
    if (type(elem) == pf.Para and type(elem.content[0]) == pf.Str
        and elem.content[0].text == '!SUBFIGURES:'):
        para = elem
        res = r'\begin{figure}\centering'
        
        default_width = 0.33
        name = ''
        for elem in para.content:
            if type(elem) == pf.Image:
                if elem.url:
                    
                    width = elem.attributes.get('width')
                    width = width if width else default_width
                    
                    res += r'''\begin{subfigure}{%s\linewidth}
                               \includegraphics[width=\linewidth]{%s}
                               \caption{%s}
                               \end{subfigure}'''%(width, elem.url.replace("%20", " "), pf.stringify(elem))
                else:
                    if elem.attributes.get('width'): default_width = convert_percents(elem.attributes.get('width'))
                    if pf.stringify(elem): name = pf.stringify(elem)

            elif type(elem) == pf.Str:
                if elem.text == '|':
                    res += r'\hfill'

        return pf.RawBlock(res + (r'\caption{%s}'%name if name else '') + r'\end{figure}',
                           format = 'tex')
   
def main(doc=None):
    return pf.run_filter(figure_insert, doc=doc)

if __name__ == "__main__":
    main()
