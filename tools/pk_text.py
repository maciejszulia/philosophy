#!/usr/bin/env python3
"""Plain prose of README.md for pklint: no maths, links, images or the bibliography.

Usage: python3 tools/pk_text.py README.md > /tmp/text.txt
       then, in the polszczyzna-kontrolowana repository: python3 -m src.pklint /tmp/text.txt
"""
import re, sys
s = open(sys.argv[1], encoding="utf-8").read()
s = re.sub(r"## Źródła\n.*?(?=\n## )", "\n", s, flags=re.S)          # bibliography: foreign titles
s = re.sub(r"## Spis treści\n.*?(?=\n## )", "\n", s, flags=re.S)      # table of contents repeats the headings
s = re.sub(r"\$\$.*?\$\$", " X ", s, flags=re.S)
s = re.sub(r"\$[^$\n]*\$", "X", s)
s = re.sub(r"!\[[^\]]*\]\([^)]*\)", "", s)
s = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", s)
out = []
for line in s.split("\n"):
    line = line.rstrip()
    if re.match(r"^\|[-| ]+\|$", line):
        continue
    if line.startswith("|"):
        out += [c.strip() for c in line.strip("|").split("|")]         # each table cell is its own block
        continue
    line = re.sub(r"^#+\s*(\d+\.\s*)?", "", line)
    line = re.sub(r"^>\s*", "", line)
    line = re.sub(r"^(?:[-*]|\d+\.)\s+", "", line)
    out.append(line.replace("**", ""))
print("\n\n".join(out))
