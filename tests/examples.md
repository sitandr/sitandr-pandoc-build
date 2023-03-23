

```bash
pandoc --from latex  _.tex --to markdown-smart+hard_line_breaks -o _.md --filter ../filters/div-converter.py --filter ../filters/math-replace.py
```

```bash
pandoc --from markdown-auto_identifiers+fenced_divs  _.md --to latex-auto_identifiers -o _2.tex --filter ../filters/div-converter.py --filter ../filters/insert-begining.py ../filters/math-replace.py --top-level-division chapter
```

