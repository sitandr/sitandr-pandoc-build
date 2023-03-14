import panflute as pf
import json

begin_environments = json.load(open(os.environ['SPB'] + r"\filters\latex_begins.json", encoding='utf8'))

def figure_insert(elem, doc):
    if not (type(elem) == pf.Para and type(elem.content[0]) == pf.Str):
        return
    
    head = elem.content[0].text.strip()

    if not (head[1:-1] in begin_environments
        and head[0] == "!" and head[-1] == ":"):
        return
    ...
   
def main(doc=None):
    return pf.run_filter(figure_insert, doc=doc)

if __name__ == "__main__":
    main()
