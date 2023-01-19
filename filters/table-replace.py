import sys

_from_ = sys.argv[1]
_middle_ = sys.argv[2]

import csv, tabulate

s = open(_from_, encoding = 'utf-8', errors= 'ignore').read()
while True:
    to = s.find('{table:')
    if to == -1:
          break
    end = s[to + 1:].find('}') + 1
    #print(to, end, s[to-10:to + end+10])
    file = open(s[to + 8: to + end], encoding = 'utf-8')
    #print(file.read())
    csv_f = list(csv.reader(file, delimiter = ';'))
    for i in csv_f:
        for j in range(len(i)):
            i[j] = i[j].replace('\n', ' ')
            
    string = tabulate.tabulate(csv_f, headers="firstrow", tablefmt = "github")
    #print(string)
    s = s[:to] + string + s[to + end + 1:]

open(_middle_, 'w', encoding = 'utf-8').write(s)
