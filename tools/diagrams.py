#!/usr/bin/env python3
"""Draw the two diagrams of the text with the generator from the claude-code-skills repository.

Usage: python3 tools/diagrams.py [directory of render_diagrams.py]
Default directory: ../claude-code-skills/tools next to this repository.
"""
import os, sys
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
sys.path.insert(0, sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, "..", "claude-code-skills", "tools"))
import render_diagrams as rd

node = rd.node
_route = rd.route


def route(a, b, na, nb):
    if nb["col"] < na["col"] and nb["row"] == na["row"]:      # same row, right to left
        y = a[1] + a[3] / 2
        return [(a[0], y), (b[0] + b[2], y)]
    return _route(a, b, na, nb)


rd.route = route
DIAGRAMS = {
    "causal-chain": {
        "title": ["Każde ogniwo wynika z poprzedniego ogniwa.",
                  "Oba zakończenia ogniwa 6 dają ten sam wynik."],
        "cols": 4,
        "nodes": [
            node("n1", 0, 0, ["1. Problem", "ludzkość rozwiązuje", "problem"]),
            node("n2", 1, 0, ["2. Stan spokoju", "rośnie w miejscu", "rozwiązania"]),
            node("n3", 2, 0, ["3. Nowe problemy", "powstają w innym", "miejscu (teza 2)"]),
            node("n4", 3, 0, ["4. System", "rozwiązuje problemy", "za człowieka"]),
            node("n5", 0, 1, ["5. Człowiek", "traci problemy ciekawe", "i zdolność działania", "bez systemu"]),
            node("n6a", 1, 1, ["6a. Awaria systemu", "człowiek bez zdolności", "działania"]),
            node("n6b", 1, 2, ["6b. Perfekcja systemu", "człowiek bez różnic"]),
            node("end", 2, 1, ["Wynik", "ludzkość ginie"], "accent", rows=2),
        ],
        "edges": [("n1", "n2"), ("n2", "n3"), ("n3", "n4"), ("n4", "n5"), ("n5", "n6a"), ("n5", "n6b"),
                  ("n6a", "end"), ("n6b", "end")],
    },
    "active-system": {
        "title": ["Układ aktywny żyje w obrocie między stanem niespokoju a stanem spokoju.",
                  "Wola otwiera problem, uwaga zamyka problem, odpowiedzialność zaczyna nowy obrót."],
        "cols": 4,
        "nodes": [
            node("wola", 0, 0, ["Wola", "wybiera 1 problem"], "accent"),
            node("nies", 1, 0, ["Stan niespokoju", "problem jest otwarty"]),
            node("uwaga", 2, 0, ["Uwaga", "kieruje energię", "na problem"], "accent"),
            node("spok", 3, 0, ["Stan spokoju", "problem jest zamknięty"]),
            node("odp", 3, 1, ["Odpowiedzialność", "przyjmuje skutki", "rozwiązania"], "accent"),
            node("nowe", 0, 1, ["Nowe problemy", "skutki rozwiązania", "(teza 2)"]),
        ],
        "edges": [("wola", "nies"), ("nies", "uwaga"), ("uwaga", "spok"), ("spok", "odp"), ("odp", "nowe"),
                  ("nowe", "wola")],
    },
}
out = os.path.join(ROOT, "docs", "diagrams")
os.makedirs(out, exist_ok=True)
for name, d in DIAGRAMS.items():
    open(os.path.join(out, name + ".svg"), "w", encoding="utf-8").write(rd.render(name, d))
print("ok", list(DIAGRAMS))
