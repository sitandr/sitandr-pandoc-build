import sys
import panflute as pf
import csv, tabulate


def figure_insert(elem, doc):
    if (type(elem) == pf.Para and type(elem.content[0]) == pf.Str
        and elem.content[0].text == '{table:' and pf.stringify(elem).strip()[-1] == '}'):
        para = elem
        
        file = open(pf.stringify(elem).strip()[len('{table:'):-1].strip(),
                    encoding = 'utf-8')

        csv_f = list(csv.reader(file, delimiter = ';'))
        for i in csv_f:
            for j in range(len(i)):
                i[j] = i[j].replace('\n', ' ')
                
        string = tabulate.tabulate(csv_f, headers="firstrow", tablefmt = "github")

        return pf.convert_text(string)

def main(doc=None):
    return pf.run_filter(figure_insert, doc=doc)

if __name__ == "__main__":
    main()
