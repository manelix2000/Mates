#!/usr/bin/env python3
"""Genera shapes-perimeter-area.json amb 25 exercicis de perímetre i àrea.

Inclou figures bàsiques (quadrat, rectangle, triangle rectangle, trapezi, cercle)
i figures compostes per 2 figures bàsiques. Cada exercici té gràfic a l'enunciat
(destacant la incògnita) i gràfic final a la resolució (amb tots els valors).

SVG usa Y cap avall. Totes les coordenades del gràfic estan en aquest sistema.
"""
import json
import math
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "app" / "public" / "topics" / "shapes-perimeter-area.json"


# ------------------------- Helpers numèrics / format -------------------------
def fmt(x, nd=2):
    r = round(x, nd)
    if abs(r - round(r)) < 1e-9:
        return f"{int(round(r))}"
    s = f"{r:.{nd}f}".rstrip("0").rstrip(".")
    return s


def fmt_cm(x):
    return f"${fmt(x)}\\ \\text{{cm}}$"


def fmt_cm2(x):
    return f"${fmt(x)}\\ \\text{{cm}}^2$"


def qid(i):
    return f"shape-{i:03d}"


# ------------------------- Helpers gràfic -------------------------
def polygon(points, dashed=False, filled=True, highlight=False):
    s = {"type": "polygon", "points": [[round(p[0], 3), round(p[1], 3)] for p in points]}
    if dashed:
        s["dashed"] = True
    if filled:
        s["filled"] = True
    if highlight:
        s["highlight"] = True
    return s


def circle(cx, cy, r, dashed=False, filled=True, highlight=False):
    s = {"type": "circle", "center": [round(cx, 3), round(cy, 3)], "r": round(r, 3)}
    if dashed:
        s["dashed"] = True
    if filled:
        s["filled"] = True
    if highlight:
        s["highlight"] = True
    return s


def arc(cx, cy, r, fromDeg, toDeg, closed=False, dashed=False, filled=True, highlight=False):
    s = {
        "type": "arc",
        "center": [round(cx, 3), round(cy, 3)],
        "r": round(r, 3),
        "fromDeg": fromDeg,
        "toDeg": toDeg,
    }
    if closed:
        s["closed"] = True
    if dashed:
        s["dashed"] = True
    if filled:
        s["filled"] = True
    if highlight:
        s["highlight"] = True
    return s


def line(p0, p1, dashed=False, highlight=False):
    s = {"type": "line", "from": [round(p0[0], 3), round(p0[1], 3)], "to": [round(p1[0], 3), round(p1[1], 3)]}
    if dashed:
        s["dashed"] = True
    if highlight:
        s["highlight"] = True
    return s


def label(x, y, text, anchor="middle", color="default", bold=False):
    l = {"at": [round(x, 3), round(y, 3)], "text": text, "anchor": anchor}
    if color != "default":
        l["color"] = color
    if bold:
        l["bold"] = True
    return l


def shape_graphic(viewBox, shapes, labels=None):
    g = {"kind": "shape-plot", "viewBox": [round(v, 3) for v in viewBox], "shapes": shapes}
    if labels:
        g["labels"] = labels
    return g


def make_opts(correct, wrong, pos):
    opts = list(wrong)
    opts.insert(pos, correct)
    return opts[:4], pos


def build_question(i, statement, g_enun, g_res, options, correct_idx, res_steps_pre):
    res = list(res_steps_pre) + [{"kind": "graphic", "graphic": g_res}]
    return {
        "id": qid(i),
        "statement": statement,
        "graphic": g_enun,
        "options": options,
        "correct": correct_idx,
        "resolution": res,
    }


# ------------------------- Generadors de figures bàsiques -------------------------
# Totes les funcions reben mides en "unitats lògiques" (normalment les mateixes que cm
# per a figures petites, o escalades). Retornen (viewBox, shapes_sin_highlight, shapes_highlight_set, labels_base).


def shapes_square(side, origin=(10, 10), highlight=False):
    x, y = origin
    pts = [(x, y), (x + side, y), (x + side, y + side), (x, y + side)]
    return [polygon(pts, highlight=highlight)], (x, y, side, side)


def shapes_rectangle(w, h, origin=(10, 10), highlight=False):
    x, y = origin
    pts = [(x, y), (x + w, y), (x + w, y + h), (x, y + h)]
    return [polygon(pts, highlight=highlight)], (x, y, w, h)


def shapes_right_triangle(b, h, origin=(10, 10), highlight=False):
    x, y = origin
    # Catet horitzontal b a baix, catet vertical h al costat esquerre, angle recte a baix-esquerra.
    pts = [(x, y + h), (x + b, y + h), (x, y)]
    return [polygon(pts, highlight=highlight)], (x, y, b, h)


def shapes_trapezoid(B, b, h, origin=(10, 10), highlight=False, isosceles=True):
    x, y = origin
    if isosceles:
        off = (B - b) / 2
        pts = [(x, y + h), (x + B, y + h), (x + off + b, y), (x + off, y)]
    else:
        # Trapezi rectangle: base gran abaix, base petita dalt alineada a l'esquerra.
        pts = [(x, y + h), (x + B, y + h), (x + b, y), (x, y)]
    return [polygon(pts, highlight=highlight)], (x, y, B, h)


def shapes_circle(r, center=(40, 40), highlight=False):
    cx, cy = center
    return [circle(cx, cy, r, highlight=highlight)], (cx - r, cy - r, 2 * r, 2 * r)


# ------------------------- Enrotllat per a viewBox amb padding -------------------------
def viewBox_from(xywh, pad=12):
    x, y, w, h = xywh
    return (x - pad, y - pad, w + 2 * pad, h + 2 * pad)


# ====================================================================================
# Generació de les 25 preguntes
# ====================================================================================
questions = []


# ---------- 1. Quadrat — perímetre ----------
def q1():
    s = 6
    shapes, box = shapes_square(s, (20, 20), highlight=True)
    labels = [
        label(20 + s / 2, 20 - 4, f"{s} cm"),
    ]
    g_enun = shape_graphic(viewBox_from(box), shapes, labels + [label(20 + s / 2, 20 + s / 2, "P = ?", color="highlight", bold=True)])
    g_res = shape_graphic(
        viewBox_from(box), shapes,
        labels + [label(20 + s / 2, 20 + s / 2, "P = 24 cm", color="highlight", bold=True)]
    )
    P = 4 * s
    correct = fmt_cm(P)
    wrong = [fmt_cm2(s * s), fmt_cm(2 * s), fmt_cm(3 * s)]
    opts, ci = make_opts(correct, wrong, 2)
    return build_question(
        1,
        f"Calcula el perímetre d'un quadrat de costat {s} cm.",
        g_enun, g_res, opts, ci,
        [
            {"kind": "text", "text": "El perímetre d'un quadrat és la suma dels seus 4 costats iguals."},
            {"kind": "math", "tex": rf"P = 4 \cdot {s} = {P}\ \text{{cm}}"},
        ],
    )


questions.append(q1())


# ---------- 2. Quadrat — àrea ----------
def q2():
    s = 9
    shapes, box = shapes_square(s, (20, 20), highlight=True)
    labels_base = [label(20 + s / 2, 20 - 4, f"{s} cm")]
    g_enun = shape_graphic(viewBox_from(box), shapes, labels_base + [label(20 + s / 2, 20 + s / 2, "A = ?", color="highlight", bold=True)])
    A = s * s
    labels_res = labels_base + [label(20 + s / 2, 20 + s / 2, f"A = {A} cm²", color="highlight", bold=True)]
    g_res = shape_graphic(viewBox_from(box), shapes, labels_res)
    correct = fmt_cm2(A)
    wrong = [fmt_cm(4 * s), fmt_cm2(2 * s), fmt_cm2(4 * s)]
    opts, ci = make_opts(correct, wrong, 0)
    return build_question(
        2,
        f"Calcula l'àrea d'un quadrat de costat {s} cm.",
        g_enun, g_res, opts, ci,
        [
            {"kind": "text", "text": "L'àrea d'un quadrat és el costat multiplicat per ell mateix."},
            {"kind": "math", "tex": rf"A = {s}^2 = {A}\ \text{{cm}}^2"},
        ],
    )


questions.append(q2())


# ---------- 3. Rectangle — perímetre ----------
def q3():
    w, h = 10, 5
    shapes, box = shapes_rectangle(w, h, (15, 15), highlight=True)
    labels_base = [
        label(15 + w / 2, 15 - 4, f"{w} cm"),
        label(15 - 6, 15 + h / 2, f"{h} cm", anchor="middle"),
    ]
    g_enun = shape_graphic(viewBox_from(box), shapes, labels_base + [label(15 + w / 2, 15 + h / 2, "P = ?", color="highlight", bold=True)])
    P = 2 * (w + h)
    g_res = shape_graphic(viewBox_from(box), shapes, labels_base + [label(15 + w / 2, 15 + h / 2, f"P = {P} cm", color="highlight", bold=True)])
    correct = fmt_cm(P)
    wrong = [fmt_cm2(w * h), fmt_cm(w + h), fmt_cm(4 * w)]
    opts, ci = make_opts(correct, wrong, 3)
    return build_question(
        3,
        f"Calcula el perímetre d'un rectangle de base {w} cm i altura {h} cm.",
        g_enun, g_res, opts, ci,
        [
            {"kind": "text", "text": "El perímetre d'un rectangle és 2 vegades la base més 2 vegades l'altura."},
            {"kind": "math", "tex": rf"P = 2\cdot{w} + 2\cdot{h} = {P}\ \text{{cm}}"},
        ],
    )


questions.append(q3())


# ---------- 4. Rectangle — àrea ----------
def q4():
    w, h = 12, 7
    shapes, box = shapes_rectangle(w, h, (15, 15), highlight=True)
    labels_base = [
        label(15 + w / 2, 15 - 4, f"{w} cm"),
        label(15 - 6, 15 + h / 2, f"{h} cm"),
    ]
    g_enun = shape_graphic(viewBox_from(box), shapes, labels_base + [label(15 + w / 2, 15 + h / 2, "A = ?", color="highlight", bold=True)])
    A = w * h
    g_res = shape_graphic(viewBox_from(box), shapes, labels_base + [label(15 + w / 2, 15 + h / 2, f"A = {A} cm²", color="highlight", bold=True)])
    correct = fmt_cm2(A)
    wrong = [fmt_cm(2 * (w + h)), fmt_cm2(w + h), fmt_cm2(2 * w * h)]
    opts, ci = make_opts(correct, wrong, 1)
    return build_question(
        4,
        f"Calcula l'àrea d'un rectangle de base {w} cm i altura {h} cm.",
        g_enun, g_res, opts, ci,
        [
            {"kind": "text", "text": "L'àrea d'un rectangle és la base per l'altura."},
            {"kind": "math", "tex": rf"A = {w} \cdot {h} = {A}\ \text{{cm}}^2"},
        ],
    )


questions.append(q4())


# ---------- 5. Rectangle — àrea (altres mesures) ----------
def q5():
    w, h = 15, 4
    shapes, box = shapes_rectangle(w, h, (10, 15), highlight=True)
    labels_base = [
        label(10 + w / 2, 15 - 4, f"{w} cm"),
        label(10 - 6, 15 + h / 2, f"{h} cm"),
    ]
    g_enun = shape_graphic(viewBox_from(box), shapes, labels_base + [label(10 + w / 2, 15 + h / 2, "A = ?", color="highlight", bold=True)])
    A = w * h
    g_res = shape_graphic(viewBox_from(box), shapes, labels_base + [label(10 + w / 2, 15 + h / 2, f"A = {A} cm²", color="highlight", bold=True)])
    correct = fmt_cm2(A)
    wrong = [fmt_cm(2 * (w + h)), fmt_cm2(w + h), fmt_cm2(w * h / 2)]
    opts, ci = make_opts(correct, wrong, 2)
    return build_question(
        5,
        f"Un rectangle té {w} cm de base i {h} cm d'altura. Calcula la seva àrea.",
        g_enun, g_res, opts, ci,
        [
            {"kind": "math", "tex": rf"A = b \cdot h = {w} \cdot {h} = {A}\ \text{{cm}}^2"},
        ],
    )


questions.append(q5())


# ---------- 6. Triangle rectangle — perímetre ----------
def q6():
    b, h = 12, 5
    hyp = math.hypot(b, h)  # 13
    shapes, box = shapes_right_triangle(b, h, (15, 15), highlight=True)
    labels_base = [
        label(15 + b / 2, 15 + h + 4, f"{b} cm"),
        label(15 - 6, 15 + h / 2, f"{h} cm"),
        label(15 + b / 2 + 1, 15 + h / 2 - 2, f"{fmt(hyp)} cm"),
    ]
    g_enun = shape_graphic(viewBox_from(box), shapes, labels_base + [label(15 + b / 3, 15 + h * 0.7, "P = ?", color="highlight", bold=True)])
    P = b + h + hyp
    g_res = shape_graphic(viewBox_from(box), shapes, labels_base + [label(15 + b / 3, 15 + h * 0.7, f"P = {fmt(P)} cm", color="highlight", bold=True)])
    correct = fmt_cm(P)
    wrong = [fmt_cm2(b * h / 2), fmt_cm(b + h), fmt_cm(2 * (b + h))]
    opts, ci = make_opts(correct, wrong, 3)
    return build_question(
        6,
        f"Calcula el perímetre d'un triangle rectangle amb catets de {b} cm i {h} cm.",
        g_enun, g_res, opts, ci,
        [
            {"kind": "text", "text": "Primer trobem la hipotenusa amb el teorema de Pitàgores."},
            {"kind": "math", "tex": rf"\text{{hip}} = \sqrt{{{b}^2 + {h}^2}} = \sqrt{{{b * b + h * h}}} = {fmt(hyp)}\ \text{{cm}}"},
            {"kind": "math", "tex": rf"P = {b} + {h} + {fmt(hyp)} = {fmt(P)}\ \text{{cm}}"},
        ],
    )


questions.append(q6())


# ---------- 7. Triangle rectangle — àrea ----------
def q7():
    b, h = 8, 6
    shapes, box = shapes_right_triangle(b, h, (15, 15), highlight=True)
    labels_base = [
        label(15 + b / 2, 15 + h + 4, f"{b} cm"),
        label(15 - 6, 15 + h / 2, f"{h} cm"),
    ]
    g_enun = shape_graphic(viewBox_from(box), shapes, labels_base + [label(15 + b / 3, 15 + h * 0.7, "A = ?", color="highlight", bold=True)])
    A = b * h / 2
    g_res = shape_graphic(viewBox_from(box), shapes, labels_base + [label(15 + b / 3, 15 + h * 0.7, f"A = {fmt(A)} cm²", color="highlight", bold=True)])
    correct = fmt_cm2(A)
    wrong = [fmt_cm2(b * h), fmt_cm(b + h), fmt_cm2(b + h)]
    opts, ci = make_opts(correct, wrong, 1)
    return build_question(
        7,
        f"Calcula l'àrea d'un triangle rectangle amb catets de {b} cm i {h} cm.",
        g_enun, g_res, opts, ci,
        [
            {"kind": "text", "text": "En un triangle rectangle, els dos catets són la base i l'altura."},
            {"kind": "math", "tex": rf"A = \dfrac{{b \cdot h}}{{2}} = \dfrac{{{b} \cdot {h}}}{{2}} = {fmt(A)}\ \text{{cm}}^2"},
        ],
    )


questions.append(q7())


# ---------- 8. Triangle rectangle — àrea ----------
def q8():
    b, h = 9, 12
    shapes, box = shapes_right_triangle(b, h, (15, 15), highlight=True)
    labels_base = [
        label(15 + b / 2, 15 + h + 4, f"{b} cm"),
        label(15 - 6, 15 + h / 2, f"{h} cm"),
    ]
    g_enun = shape_graphic(viewBox_from(box), shapes, labels_base + [label(15 + b / 3, 15 + h * 0.7, "A = ?", color="highlight", bold=True)])
    A = b * h / 2
    g_res = shape_graphic(viewBox_from(box), shapes, labels_base + [label(15 + b / 3, 15 + h * 0.7, f"A = {fmt(A)} cm²", color="highlight", bold=True)])
    correct = fmt_cm2(A)
    wrong = [fmt_cm2(b * h), fmt_cm(b + h + 15), fmt_cm2(b + h)]
    opts, ci = make_opts(correct, wrong, 2)
    return build_question(
        8,
        f"Un triangle rectangle té catets de {b} cm i {h} cm. Calcula la seva àrea.",
        g_enun, g_res, opts, ci,
        [
            {"kind": "math", "tex": rf"A = \dfrac{{b \cdot h}}{{2}} = \dfrac{{{b} \cdot {h}}}{{2}} = {fmt(A)}\ \text{{cm}}^2"},
        ],
    )


questions.append(q8())


# ---------- 9. Trapezi rectangle — àrea ----------
def q9():
    B, b, h = 10, 6, 5
    shapes, box = shapes_trapezoid(B, b, h, (15, 15), highlight=True, isosceles=False)
    labels_base = [
        label(15 + B / 2, 15 + h + 4, f"B = {B} cm"),
        label(15 + b / 2, 15 - 4, f"b = {b} cm"),
        label(15 - 6, 15 + h / 2, f"h = {h} cm"),
    ]
    A = (B + b) * h / 2
    g_enun = shape_graphic(viewBox_from(box), shapes, labels_base + [label(15 + B / 2, 15 + h / 2, "A = ?", color="highlight", bold=True)])
    g_res = shape_graphic(viewBox_from(box), shapes, labels_base + [label(15 + B / 2, 15 + h / 2, f"A = {fmt(A)} cm²", color="highlight", bold=True)])
    correct = fmt_cm2(A)
    wrong = [fmt_cm2((B + b) * h), fmt_cm2(B * b), fmt_cm(B + b + 2 * h)]
    opts, ci = make_opts(correct, wrong, 0)
    return build_question(
        9,
        f"Calcula l'àrea d'un trapezi rectangle amb base gran B = {B} cm, base petita b = {b} cm i altura h = {h} cm.",
        g_enun, g_res, opts, ci,
        [
            {"kind": "math", "tex": rf"A = \dfrac{{(B+b)\cdot h}}{{2}} = \dfrac{{({B}+{b})\cdot {h}}}{{2}} = {fmt(A)}\ \text{{cm}}^2"},
        ],
    )


questions.append(q9())


# ---------- 10. Trapezi isòsceles — àrea ----------
def q10():
    B, b, h = 14, 8, 5
    shapes, box = shapes_trapezoid(B, b, h, (10, 15), highlight=True, isosceles=True)
    labels_base = [
        label(10 + B / 2, 15 + h + 4, f"B = {B} cm"),
        label(10 + B / 2, 15 - 4, f"b = {b} cm"),
        label(10 - 6, 15 + h / 2, f"h = {h} cm"),
    ]
    A = (B + b) * h / 2
    g_enun = shape_graphic(viewBox_from(box), shapes, labels_base + [label(10 + B / 2, 15 + h / 2, "A = ?", color="highlight", bold=True)])
    g_res = shape_graphic(viewBox_from(box), shapes, labels_base + [label(10 + B / 2, 15 + h / 2, f"A = {fmt(A)} cm²", color="highlight", bold=True)])
    correct = fmt_cm2(A)
    wrong = [fmt_cm2((B + b) * h), fmt_cm2(B * b), fmt_cm2(B * h)]
    opts, ci = make_opts(correct, wrong, 2)
    return build_question(
        10,
        f"Calcula l'àrea d'un trapezi isòsceles amb bases de {B} cm i {b} cm i altura de {h} cm.",
        g_enun, g_res, opts, ci,
        [
            {"kind": "text", "text": "L'àrea d'un trapezi és la semi-suma de les bases per l'altura."},
            {"kind": "math", "tex": rf"A = \dfrac{{(B+b)\cdot h}}{{2}} = \dfrac{{({B}+{b})\cdot {h}}}{{2}} = {fmt(A)}\ \text{{cm}}^2"},
        ],
    )


questions.append(q10())


# ---------- 11. Trapezi — perímetre ----------
def q11():
    B, b, h = 12, 6, 4
    # Trapezi isòsceles: costat oblic = sqrt(((B-b)/2)^2 + h^2) = sqrt(9+16) = 5
    lateral = math.hypot((B - b) / 2, h)  # 5
    shapes, box = shapes_trapezoid(B, b, h, (10, 15), highlight=True, isosceles=True)
    labels_base = [
        label(10 + B / 2, 15 + h + 4, f"{B} cm"),
        label(10 + B / 2, 15 - 4, f"{b} cm"),
        label(10 + (B - b) / 4 - 3, 15 + h / 2, f"{fmt(lateral)} cm", anchor="end"),
        label(10 + B - (B - b) / 4 + 3, 15 + h / 2, f"{fmt(lateral)} cm", anchor="start"),
    ]
    P = B + b + 2 * lateral
    g_enun = shape_graphic(viewBox_from(box), shapes, labels_base + [label(10 + B / 2, 15 + h / 2, "P = ?", color="highlight", bold=True)])
    g_res = shape_graphic(viewBox_from(box), shapes, labels_base + [label(10 + B / 2, 15 + h / 2, f"P = {fmt(P)} cm", color="highlight", bold=True)])
    correct = fmt_cm(P)
    wrong = [fmt_cm2((B + b) * h / 2), fmt_cm(B + b), fmt_cm(B + b + lateral)]
    opts, ci = make_opts(correct, wrong, 1)
    return build_question(
        11,
        f"Un trapezi isòsceles té bases de {B} cm i {b} cm, i els costats oblics mesuren {fmt(lateral)} cm cadascun. Calcula'n el perímetre.",
        g_enun, g_res, opts, ci,
        [
            {"kind": "text", "text": "El perímetre és la suma dels 4 costats."},
            {"kind": "math", "tex": rf"P = {B} + {b} + 2\cdot{fmt(lateral)} = {fmt(P)}\ \text{{cm}}"},
        ],
    )


questions.append(q11())


# ---------- 12. Cercle — perímetre (longitud) ----------
def q12():
    r = 5
    shapes, box = shapes_circle(r, (30, 30), highlight=True)
    # Marcar radi
    radius_line = [line((30, 30), (30 + r, 30), dashed=True)]
    labels_base = [
        label(30 + r / 2, 30 - 3, f"r = {r} cm"),
    ]
    P = 2 * math.pi * r
    g_enun = shape_graphic(viewBox_from(box), shapes + radius_line, labels_base + [label(30, 30 + r + 6, "P = ?", color="highlight", bold=True)])
    g_res = shape_graphic(viewBox_from(box), shapes + radius_line, labels_base + [label(30, 30 + r + 6, f"P = {fmt(P)} cm", color="highlight", bold=True)])
    correct = fmt_cm(P)
    wrong = [fmt_cm(math.pi * r), fmt_cm2(math.pi * r * r), fmt_cm(4 * r)]
    opts, ci = make_opts(correct, wrong, 0)
    return build_question(
        12,
        f"Calcula la longitud (perímetre) d'un cercle de radi {r} cm. Utilitza π ≈ 3,14.",
        g_enun, g_res, opts, ci,
        [
            {"kind": "text", "text": "La longitud d'una circumferència és 2π per el radi."},
            {"kind": "math", "tex": rf"P = 2\pi r = 2\pi \cdot {r} = 10\pi \approx {fmt(P)}\ \text{{cm}}"},
        ],
    )


questions.append(q12())


# ---------- 13. Cercle — àrea ----------
def q13():
    r = 3
    shapes, box = shapes_circle(r, (25, 25), highlight=True)
    radius_line = [line((25, 25), (25 + r, 25), dashed=True)]
    labels_base = [label(25 + r / 2, 25 - 2, f"r = {r} cm")]
    A = math.pi * r * r
    g_enun = shape_graphic(viewBox_from(box), shapes + radius_line, labels_base + [label(25, 25 + r + 4, "A = ?", color="highlight", bold=True)])
    g_res = shape_graphic(viewBox_from(box), shapes + radius_line, labels_base + [label(25, 25 + r + 4, f"A = {fmt(A)} cm²", color="highlight", bold=True)])
    correct = fmt_cm2(A)
    wrong = [fmt_cm(2 * math.pi * r), fmt_cm2(2 * math.pi * r), fmt_cm2(math.pi * r)]
    opts, ci = make_opts(correct, wrong, 3)
    return build_question(
        13,
        f"Calcula l'àrea d'un cercle de radi {r} cm. Utilitza π ≈ 3,14.",
        g_enun, g_res, opts, ci,
        [
            {"kind": "math", "tex": rf"A = \pi r^2 = \pi \cdot {r}^2 = 9\pi \approx {fmt(A)}\ \text{{cm}}^2"},
        ],
    )


questions.append(q13())


# ---------- 14. Cercle — àrea a partir del diàmetre ----------
def q14():
    d = 12
    r = d / 2
    shapes, box = shapes_circle(r, (30, 30), highlight=True)
    diameter = [line((30 - r, 30), (30 + r, 30), dashed=True)]
    labels_base = [label(30, 30 - 2, f"d = {d} cm")]
    A = math.pi * r * r
    g_enun = shape_graphic(viewBox_from(box), shapes + diameter, labels_base + [label(30, 30 + r + 6, "A = ?", color="highlight", bold=True)])
    g_res = shape_graphic(viewBox_from(box), shapes + diameter, labels_base + [label(30, 30 + r + 6, f"A = {fmt(A)} cm²", color="highlight", bold=True)])
    correct = fmt_cm2(A)
    # Distractor clàssic: utilitzar d com si fos r → A = π·d² = 144π ≈ 452,39
    wrong = [fmt_cm2(math.pi * d * d), fmt_cm(math.pi * d), fmt_cm2(2 * math.pi * r)]
    opts, ci = make_opts(correct, wrong, 1)
    return build_question(
        14,
        f"Un cercle té diàmetre {d} cm. Calcula la seva àrea (π ≈ 3,14).",
        g_enun, g_res, opts, ci,
        [
            {"kind": "text", "text": "Primer obtenim el radi dividint el diàmetre entre 2."},
            {"kind": "math", "tex": rf"r = \dfrac{{{d}}}{{2}} = {fmt(r)}\ \text{{cm}}"},
            {"kind": "math", "tex": rf"A = \pi r^2 = \pi \cdot {fmt(r)}^2 = 36\pi \approx {fmt(A)}\ \text{{cm}}^2"},
        ],
    )


questions.append(q14())


# ====================================================================================
# Figures compostes (2 figures bàsiques)
# ====================================================================================


# ---------- 15. Rectangle + semicercle (àrea) — estadi/pista ----------
def q15():
    w, h = 12, 8
    r = h / 2
    ox, oy = 10, 15
    # Rectangle
    rect = polygon([(ox, oy), (ox + w, oy), (ox + w, oy + h), (ox, oy + h)])
    # Semicercle a la dreta: centre a (ox+w, oy+h/2), de -90° (dalt) a 90° (baix), tancat
    semi = arc(ox + w, oy + h / 2, r, -90, 90, closed=True)
    # Línia discontínua de separació
    sep = line((ox + w, oy), (ox + w, oy + h), dashed=True)
    shapes = [rect, semi, sep]
    box = (ox, oy, w + r, h)
    labels_base = [
        label(ox + w / 2, oy - 4, f"{w} cm"),
        label(ox - 6, oy + h / 2, f"{h} cm"),
        label(ox + w + r / 2 + 1, oy + h / 2 - 3, f"r = {fmt(r)} cm"),
    ]
    A_rect = w * h
    A_semi = math.pi * r * r / 2
    A = A_rect + A_semi
    g_enun = shape_graphic(viewBox_from(box, pad=16), shapes, labels_base + [label(ox + w / 2, oy + h / 2, "A = ?", color="highlight", bold=True)])
    g_res = shape_graphic(viewBox_from(box, pad=16), shapes, labels_base + [label(ox + w / 2, oy + h / 2, f"A = {fmt(A)} cm²", color="highlight", bold=True)])
    correct = fmt_cm2(A)
    wrong = [fmt_cm2(A_rect + math.pi * r * r), fmt_cm2(A_rect), fmt_cm2(A_rect + math.pi * h * h / 2)]
    opts, ci = make_opts(correct, wrong, 2)
    return build_question(
        15,
        f"La figura és un rectangle de {w} cm per {h} cm amb un semicercle afegit al costat dret (diàmetre = {h} cm). Calcula l'àrea total.",
        g_enun, g_res, opts, ci,
        [
            {"kind": "text", "text": "Descomposem la figura en un rectangle i un semicercle."},
            {"kind": "math", "tex": rf"A_{{\text{{rect}}}} = {w} \cdot {h} = {A_rect}\ \text{{cm}}^2"},
            {"kind": "math", "tex": rf"A_{{\text{{semi}}}} = \dfrac{{\pi r^2}}{{2}} = \dfrac{{\pi \cdot {fmt(r)}^2}}{{2}} = 8\pi \approx {fmt(A_semi)}\ \text{{cm}}^2"},
            {"kind": "math", "tex": rf"A = A_{{\text{{rect}}}} + A_{{\text{{semi}}}} \approx {fmt(A)}\ \text{{cm}}^2"},
        ],
    )


questions.append(q15())


# ---------- 16. Rectangle + semicercle damunt (àrea) ----------
def q16():
    w, h = 10, 6
    r = w / 2
    ox, oy = 15, 20
    rect = polygon([(ox, oy), (ox + w, oy), (ox + w, oy + h), (ox, oy + h)])
    # Semicercle damunt: centre (ox+w/2, oy), de 180° a 360° (per dalt, és a dir Y negatiu)
    semi = arc(ox + w / 2, oy, r, 180, 360, closed=True)
    sep = line((ox, oy), (ox + w, oy), dashed=True)
    shapes = [rect, semi, sep]
    box = (ox, oy - r, w, h + r)
    labels_base = [
        label(ox + w / 2, oy + h + 4, f"{w} cm"),
        label(ox - 6, oy + h / 2, f"{h} cm"),
        label(ox + w / 2 + 1, oy - r / 2 - 2, f"r = {fmt(r)} cm"),
    ]
    A_rect = w * h
    A_semi = math.pi * r * r / 2
    A = A_rect + A_semi
    g_enun = shape_graphic(viewBox_from(box, pad=14), shapes, labels_base + [label(ox + w / 2, oy + h / 2, "A = ?", color="highlight", bold=True)])
    g_res = shape_graphic(viewBox_from(box, pad=14), shapes, labels_base + [label(ox + w / 2, oy + h / 2, f"A = {fmt(A)} cm²", color="highlight", bold=True)])
    correct = fmt_cm2(A)
    wrong = [fmt_cm2(A_rect + math.pi * r * r), fmt_cm2(A_rect), fmt_cm(2 * (w + h) + math.pi * r)]
    opts, ci = make_opts(correct, wrong, 0)
    return build_question(
        16,
        f"Una finestra té forma de rectangle de {w} cm per {h} cm rematat per un semicercle a la part superior (diàmetre = {w} cm). Calcula l'àrea.",
        g_enun, g_res, opts, ci,
        [
            {"kind": "math", "tex": rf"A_{{\text{{rect}}}} = {w} \cdot {h} = {A_rect}\ \text{{cm}}^2"},
            {"kind": "math", "tex": rf"A_{{\text{{semi}}}} = \dfrac{{\pi \cdot {fmt(r)}^2}}{{2}} = \dfrac{{25\pi}}{{2}} \approx {fmt(A_semi)}\ \text{{cm}}^2"},
            {"kind": "math", "tex": rf"A = {A_rect} + {fmt(A_semi)} \approx {fmt(A)}\ \text{{cm}}^2"},
        ],
    )


questions.append(q16())


# ---------- 17. Quadrat + triangle rectangle damunt (teulada de casa) (àrea) ----------
def q17():
    s = 8  # costat quadrat
    b_t = 8  # base triangle = costat quadrat
    h_t = 5  # altura triangle
    ox, oy = 15, 15
    sq = polygon([(ox, oy + h_t), (ox + s, oy + h_t), (ox + s, oy + h_t + s), (ox, oy + h_t + s)])
    # Triangle damunt: vèrtex a la dreta-dalt (triangle rectangle amb catet horitzontal = s i catet vertical = h_t)
    tri = polygon([(ox, oy + h_t), (ox + s, oy + h_t), (ox + s, oy)])
    sep = line((ox, oy + h_t), (ox + s, oy + h_t), dashed=True)
    shapes = [sq, tri, sep]
    box = (ox, oy, s, s + h_t)
    labels_base = [
        label(ox + s / 2, oy + h_t + s + 4, f"{s} cm"),
        label(ox - 6, oy + h_t + s / 2, f"{s} cm"),
        label(ox + s + 4, oy + h_t / 2, f"{h_t} cm", anchor="start"),
    ]
    A_sq = s * s
    A_tri = b_t * h_t / 2
    A = A_sq + A_tri
    g_enun = shape_graphic(viewBox_from(box, pad=16), shapes, labels_base + [label(ox + s / 2, oy + h_t + s / 2, "A = ?", color="highlight", bold=True)])
    g_res = shape_graphic(viewBox_from(box, pad=16), shapes, labels_base + [label(ox + s / 2, oy + h_t + s / 2, f"A = {fmt(A)} cm²", color="highlight", bold=True)])
    correct = fmt_cm2(A)
    wrong = [fmt_cm2(A_sq + b_t * h_t), fmt_cm2(A_sq), fmt_cm(4 * s + b_t + h_t)]
    opts, ci = make_opts(correct, wrong, 3)
    return build_question(
        17,
        f"La figura és un quadrat de costat {s} cm amb un triangle rectangle a sobre (catets de {s} cm i {h_t} cm). Calcula l'àrea total.",
        g_enun, g_res, opts, ci,
        [
            {"kind": "math", "tex": rf"A_{{\text{{quad}}}} = {s}^2 = {A_sq}\ \text{{cm}}^2"},
            {"kind": "math", "tex": rf"A_{{\text{{tri}}}} = \dfrac{{{b_t}\cdot {h_t}}}{{2}} = {fmt(A_tri)}\ \text{{cm}}^2"},
            {"kind": "math", "tex": rf"A = {A_sq} + {fmt(A_tri)} = {fmt(A)}\ \text{{cm}}^2"},
        ],
    )


questions.append(q17())


# ---------- 18. Rectangle + triangle rectangle a la dreta (àrea) ----------
def q18():
    w, h = 10, 6
    bt, ht = 5, 6  # triangle rectangle amb catet vertical = h
    ox, oy = 10, 15
    rect = polygon([(ox, oy), (ox + w, oy), (ox + w, oy + h), (ox, oy + h)])
    # Triangle a la dreta: catet vertical alineat amb el costat dret del rectangle, catet horitzontal cap a la dreta
    tri = polygon([(ox + w, oy), (ox + w + bt, oy + h), (ox + w, oy + h)])
    sep = line((ox + w, oy), (ox + w, oy + h), dashed=True)
    shapes = [rect, tri, sep]
    box = (ox, oy, w + bt, h)
    labels_base = [
        label(ox + w / 2, oy - 4, f"{w} cm"),
        label(ox - 6, oy + h / 2, f"{h} cm"),
        label(ox + w + bt / 2 + 1, oy + h + 4, f"{bt} cm"),
    ]
    A_rect = w * h
    A_tri = bt * ht / 2
    A = A_rect + A_tri
    g_enun = shape_graphic(viewBox_from(box, pad=14), shapes, labels_base + [label(ox + w / 2, oy + h / 2, "A = ?", color="highlight", bold=True)])
    g_res = shape_graphic(viewBox_from(box, pad=14), shapes, labels_base + [label(ox + w / 2, oy + h / 2, f"A = {fmt(A)} cm²", color="highlight", bold=True)])
    correct = fmt_cm2(A)
    wrong = [fmt_cm2(A_rect + bt * ht), fmt_cm2(A_rect), fmt_cm2(2 * (w + h))]
    opts, ci = make_opts(correct, wrong, 1)
    return build_question(
        18,
        f"La figura està formada per un rectangle de {w} cm × {h} cm i un triangle rectangle a la dreta amb catets de {bt} cm i {h} cm. Calcula l'àrea total.",
        g_enun, g_res, opts, ci,
        [
            {"kind": "math", "tex": rf"A_{{\text{{rect}}}} = {w} \cdot {h} = {A_rect}\ \text{{cm}}^2"},
            {"kind": "math", "tex": rf"A_{{\text{{tri}}}} = \dfrac{{{bt}\cdot {ht}}}{{2}} = {fmt(A_tri)}\ \text{{cm}}^2"},
            {"kind": "math", "tex": rf"A = {A_rect} + {fmt(A_tri)} = {fmt(A)}\ \text{{cm}}^2"},
        ],
    )


questions.append(q18())


# ---------- 19. Figura en L (dos rectangles) ----------
def q19():
    # Rectangle gran 10×7 al qual li treiem un rectangle 6×4 del cantó superior dret.
    # Ho descomposem com: rectangle 10×3 (baix) + rectangle 4×4 (dalt-esquerra)
    ox, oy = 10, 15
    W, H = 10, 7
    w2, h2 = 6, 4  # mossegada superior dreta
    # Polígon en L (6 vèrtexs) — SVG Y cap avall: oy és la línia superior
    pts = [
        (ox, oy),                # superior-esquerra
        (ox + (W - w2), oy),     # punt on comença la mossegada
        (ox + (W - w2), oy + h2),# baixa pel costat de la mossegada
        (ox + W, oy + h2),       # cap a la dreta (part del damunt de la part baixa)
        (ox + W, oy + H),        # cantonada inferior dreta
        (ox, oy + H),            # cantonada inferior esquerra
    ]
    l_shape = polygon(pts)
    # Línia discontínua per indicar la descomposició en 2 rectangles:
    # rectangle baix: (ox, oy + h2) — (ox + W, oy + H) i rectangle dalt: (ox, oy) — (ox + (W - w2), oy + h2)
    sep = line((ox, oy + h2), (ox + (W - w2), oy + h2), dashed=True)
    shapes = [l_shape, sep]
    box = (ox, oy, W, H)
    labels_base = [
        label(ox + (W - w2) / 2, oy - 4, f"{W - w2} cm"),
        label(ox + W / 2, oy + H + 4, f"{W} cm"),
        label(ox - 6, oy + H / 2, f"{H} cm"),
        label(ox + (W - w2) + w2 / 2, oy + h2 - 3, f"{w2} cm"),
        label(ox + W + 4, oy + h2 / 2, f"{h2} cm", anchor="start"),
    ]
    A1 = W * (H - h2)  # rectangle baix
    A2 = (W - w2) * h2  # rectangle dalt esquerra
    A = A1 + A2
    g_enun = shape_graphic(viewBox_from(box, pad=16), shapes, labels_base + [label(ox + (W - w2) / 2, oy + H / 2, "A = ?", color="highlight", bold=True)])
    g_res = shape_graphic(viewBox_from(box, pad=16), shapes, labels_base + [label(ox + (W - w2) / 2, oy + H / 2 + 2, f"A = {fmt(A)} cm²", color="highlight", bold=True)])
    correct = fmt_cm2(A)
    wrong = [fmt_cm2(W * H), fmt_cm2(W * H - w2 * h2 * 2), fmt_cm(2 * (W + H))]
    opts, ci = make_opts(correct, wrong, 2)
    return build_question(
        19,
        "La figura té forma de L. Descomposa-la en dos rectangles i calcula l'àrea total.",
        g_enun, g_res, opts, ci,
        [
            {"kind": "text", "text": "Dividim la L en un rectangle inferior (10 × 3) i un rectangle superior esquerre (4 × 4)."},
            {"kind": "math", "tex": rf"A_1 = {W} \cdot {H - h2} = {A1}\ \text{{cm}}^2"},
            {"kind": "math", "tex": rf"A_2 = {W - w2} \cdot {h2} = {A2}\ \text{{cm}}^2"},
            {"kind": "math", "tex": rf"A = A_1 + A_2 = {A}\ \text{{cm}}^2"},
        ],
    )


questions.append(q19())


# ---------- 20. Rectangle amb cercle buit (àrea) ----------
def q20():
    w, h = 14, 10
    r = 3
    ox, oy = 10, 15
    rect = polygon([(ox, oy), (ox + w, oy), (ox + w, oy + h), (ox, oy + h)])
    cx, cy = ox + w / 2, oy + h / 2
    circ = circle(cx, cy, r, filled=True)
    shapes = [rect, circ]
    box = (ox, oy, w, h)
    labels_base = [
        label(ox + w / 2, oy - 4, f"{w} cm"),
        label(ox - 6, oy + h / 2, f"{h} cm"),
        label(cx + r / 2 + 1, cy - 2, f"r = {r} cm"),
    ]
    A_rect = w * h
    A_circ = math.pi * r * r
    A = A_rect - A_circ
    g_enun = shape_graphic(viewBox_from(box, pad=14), shapes, labels_base + [label(ox + w * 0.22, oy + h * 0.25, "A = ?", color="highlight", bold=True)])
    g_res = shape_graphic(viewBox_from(box, pad=14), shapes, labels_base + [label(ox + w * 0.22, oy + h * 0.25, f"A = {fmt(A)} cm²", color="highlight", bold=True)])
    correct = fmt_cm2(A)
    wrong = [fmt_cm2(A_rect + A_circ), fmt_cm2(A_rect), fmt_cm2(A_rect - 2 * math.pi * r)]
    opts, ci = make_opts(correct, wrong, 3)
    return build_question(
        20,
        f"Una placa rectangular de {w} cm × {h} cm té un forat circular de radi {r} cm al centre. Calcula l'àrea de la placa restant (π ≈ 3,14).",
        g_enun, g_res, opts, ci,
        [
            {"kind": "math", "tex": rf"A_{{\text{{rect}}}} = {w} \cdot {h} = {A_rect}\ \text{{cm}}^2"},
            {"kind": "math", "tex": rf"A_{{\text{{cercle}}}} = \pi r^2 = 9\pi \approx {fmt(A_circ)}\ \text{{cm}}^2"},
            {"kind": "math", "tex": rf"A = A_{{\text{{rect}}}} - A_{{\text{{cercle}}}} \approx {fmt(A)}\ \text{{cm}}^2"},
        ],
    )


questions.append(q20())


# ---------- 21. Trapezi + rectangle (àrea) ----------
def q21():
    # Trapezi isòsceles a dalt + rectangle a baix
    B, b, ht = 12, 6, 4  # trapezi: B=12, b=6, h=4
    wr, hr = 12, 5  # rectangle (mateixa base)
    ox, oy = 10, 15
    # Trapezi ocupa y ∈ [oy, oy+ht]
    off = (B - b) / 2
    trap = polygon([
        (ox, oy + ht), (ox + B, oy + ht), (ox + off + b, oy), (ox + off, oy)
    ])
    # Rectangle a baix: y ∈ [oy+ht, oy+ht+hr]
    rect = polygon([(ox, oy + ht), (ox + wr, oy + ht), (ox + wr, oy + ht + hr), (ox, oy + ht + hr)])
    sep = line((ox, oy + ht), (ox + B, oy + ht), dashed=True)
    shapes = [trap, rect, sep]
    box = (ox, oy, B, ht + hr)
    labels_base = [
        label(ox + B / 2, oy - 4, f"{b} cm"),
        label(ox + B / 2, oy + ht + hr + 4, f"{wr} cm"),
        label(ox - 6, oy + ht / 2, f"{ht} cm"),
        label(ox + B + 4, oy + ht + hr / 2, f"{hr} cm", anchor="start"),
    ]
    A_trap = (B + b) * ht / 2
    A_rect = wr * hr
    A = A_trap + A_rect
    g_enun = shape_graphic(viewBox_from(box, pad=14), shapes, labels_base + [label(ox + B / 2, oy + ht + hr / 2, "A = ?", color="highlight", bold=True)])
    g_res = shape_graphic(viewBox_from(box, pad=14), shapes, labels_base + [label(ox + B / 2, oy + ht + hr / 2, f"A = {fmt(A)} cm²", color="highlight", bold=True)])
    correct = fmt_cm2(A)
    wrong = [fmt_cm2(A_trap * 2 + A_rect), fmt_cm2(B * (ht + hr)), fmt_cm2(A_rect)]
    opts, ci = make_opts(correct, wrong, 2)
    return build_question(
        21,
        f"La figura està formada per un trapezi isòsceles (bases {B} cm i {b} cm, altura {ht} cm) damunt d'un rectangle de {wr} cm × {hr} cm. Calcula l'àrea total.",
        g_enun, g_res, opts, ci,
        [
            {"kind": "math", "tex": rf"A_{{\text{{trap}}}} = \dfrac{{({B}+{b})\cdot {ht}}}{{2}} = {fmt(A_trap)}\ \text{{cm}}^2"},
            {"kind": "math", "tex": rf"A_{{\text{{rect}}}} = {wr} \cdot {hr} = {A_rect}\ \text{{cm}}^2"},
            {"kind": "math", "tex": rf"A = {fmt(A_trap)} + {A_rect} = {fmt(A)}\ \text{{cm}}^2"},
        ],
    )


questions.append(q21())


# ---------- 22. Rectangle + semicercle (perímetre) ----------
def q22():
    w, h = 12, 8
    r = h / 2
    ox, oy = 10, 15
    rect_top = line((ox, oy), (ox + w, oy))
    rect_bottom = line((ox, oy + h), (ox + w, oy + h))
    rect_left = line((ox, oy), (ox, oy + h))
    semi = arc(ox + w, oy + h / 2, r, -90, 90, closed=False, filled=False)
    # Afegim un polígon del contorn total per tenir un fill (ompliment visual) amb un path compost
    # Com que `arc` només fa un path obert aquí, usem un polígon aproximat només per color de fons
    bg = polygon([(ox, oy), (ox + w, oy), (ox + w, oy + h), (ox, oy + h)], filled=True)
    # Per al semicercle tancat (per l'ompliment) es dibuixa també com arc tancat sense highlight
    semi_fill = arc(ox + w, oy + h / 2, r, -90, 90, closed=True, filled=True)
    shapes = [bg, semi_fill, rect_top, rect_bottom, rect_left, semi]
    box = (ox, oy, w + r, h)
    labels_base = [
        label(ox + w / 2, oy - 4, f"{w} cm"),
        label(ox - 6, oy + h / 2, f"{h} cm"),
        label(ox + w + r / 2 + 1, oy + h / 2 - 3, f"r = {fmt(r)} cm"),
    ]
    P = w + h + w + math.pi * r  # 2 costats horitzontals de w, el costat esquerre h, i el semicercle π·r
    g_enun = shape_graphic(viewBox_from(box, pad=16), shapes, labels_base + [label(ox + w / 2, oy + h / 2, "P = ?", color="highlight", bold=True)])
    g_res = shape_graphic(viewBox_from(box, pad=16), shapes, labels_base + [label(ox + w / 2, oy + h / 2, f"P = {fmt(P)} cm", color="highlight", bold=True)])
    correct = fmt_cm(P)
    wrong = [fmt_cm(2 * (w + h) + 2 * math.pi * r), fmt_cm(2 * w + h + 2 * math.pi * r), fmt_cm2(w * h + math.pi * r * r / 2)]
    opts, ci = make_opts(correct, wrong, 1)
    return build_question(
        22,
        f"La figura és un rectangle de {w} cm × {h} cm amb un semicercle al costat dret (diàmetre = {h} cm). Calcula'n el perímetre (π ≈ 3,14).",
        g_enun, g_res, opts, ci,
        [
            {"kind": "text", "text": "El perímetre inclou 3 costats del rectangle (no el de la dreta, que el substitueix el semicercle) més l'arc del semicercle."},
            {"kind": "math", "tex": rf"P = {w} + {h} + {w} + \pi r = {2 * w + h} + \pi \cdot {fmt(r)} \approx {fmt(P)}\ \text{{cm}}"},
        ],
    )


questions.append(q22())


# ---------- 23. Quadrat + semicercle damunt (àrea) ----------
def q23():
    s = 10
    r = s / 2
    ox, oy = 15, 20
    sq = polygon([(ox, oy), (ox + s, oy), (ox + s, oy + s), (ox, oy + s)])
    semi = arc(ox + s / 2, oy, r, 180, 360, closed=True)
    sep = line((ox, oy), (ox + s, oy), dashed=True)
    shapes = [sq, semi, sep]
    box = (ox, oy - r, s, s + r)
    labels_base = [
        label(ox + s / 2, oy + s + 4, f"{s} cm"),
        label(ox - 6, oy + s / 2, f"{s} cm"),
        label(ox + s / 2 + 1, oy - r / 2 - 2, f"r = {fmt(r)} cm"),
    ]
    A_sq = s * s
    A_semi = math.pi * r * r / 2
    A = A_sq + A_semi
    g_enun = shape_graphic(viewBox_from(box, pad=14), shapes, labels_base + [label(ox + s / 2, oy + s / 2, "A = ?", color="highlight", bold=True)])
    g_res = shape_graphic(viewBox_from(box, pad=14), shapes, labels_base + [label(ox + s / 2, oy + s / 2, f"A = {fmt(A)} cm²", color="highlight", bold=True)])
    correct = fmt_cm2(A)
    wrong = [fmt_cm2(A_sq + math.pi * r * r), fmt_cm2(A_sq), fmt_cm2(A_sq + math.pi * s * s / 2)]
    opts, ci = make_opts(correct, wrong, 1)
    return build_question(
        23,
        f"Un tapís té forma d'un quadrat de {s} cm de costat amb un semicercle a la part superior (diàmetre = {s} cm). Calcula'n l'àrea total (π ≈ 3,14).",
        g_enun, g_res, opts, ci,
        [
            {"kind": "math", "tex": rf"A_{{\text{{quad}}}} = {s}^2 = {A_sq}\ \text{{cm}}^2"},
            {"kind": "math", "tex": rf"A_{{\text{{semi}}}} = \dfrac{{\pi \cdot {fmt(r)}^2}}{{2}} = \dfrac{{25\pi}}{{2}} \approx {fmt(A_semi)}\ \text{{cm}}^2"},
            {"kind": "math", "tex": rf"A = {A_sq} + {fmt(A_semi)} \approx {fmt(A)}\ \text{{cm}}^2"},
        ],
    )


questions.append(q23())


# ---------- 24. Triangle rectangle + rectangle (perímetre) ----------
def q24():
    # Rectangle a baix amb un triangle rectangle damunt; el catet horitzontal del triangle és
    # part de la base superior del rectangle. Per simplificar: el triangle cobreix tota la part
    # superior del rectangle, formant una "fletxa" vertical (rectangle + triangle agut damunt).
    # Millor: triangle rectangle a la dreta tocant el rectangle (fitxa que puja).
    w, h = 9, 6
    bt, ht = 9, 4  # triangle rectangle damunt, catet horitzontal = w
    ox, oy = 10, 15
    rect = polygon([(ox, oy + ht), (ox + w, oy + ht), (ox + w, oy + ht + h), (ox, oy + ht + h)])
    # Triangle rectangle damunt: angle recte a l'esquerra-baix; catets = bt (horitzontal) i ht (vertical).
    tri = polygon([(ox, oy + ht), (ox + bt, oy + ht), (ox, oy)])
    sep = line((ox, oy + ht), (ox + w, oy + ht), dashed=True)
    shapes = [rect, tri, sep]
    box = (ox, oy, w, h + ht)
    hyp_tri = math.hypot(bt, ht)  # hipotenusa del triangle
    labels_base = [
        label(ox + w / 2, oy + ht + h + 4, f"{w} cm"),
        label(ox - 6, oy + ht + h / 2, f"{h} cm"),
        label(ox - 6, oy + ht / 2, f"{ht} cm"),
        label(ox + bt / 2 + 2, oy + ht / 2 - 3, f"{fmt(hyp_tri)} cm", color="muted"),
    ]
    # Perímetre del contorn extern = base rectangle + costat dret rectangle + dalt rectangle (coincideix amb catet horitzontal del triangle)… compte:
    # El contorn extern és: baix (w) + dret rectangle (h) + dalt triangle: del cantó superior dret del rectangle pugem per l'hipotenusa fins al vèrtex agut del triangle? No.
    # Repensem la figura: Triangle rectangle damunt amb catet horitzontal = w coincidint amb el costat superior del rectangle, i catet vertical a l'esquerra (ht). Llavors el vèrtex agut del triangle és a la esquerra-dalt (ox, oy).
    # Contorn extern: (ox, oy+ht+h) → (ox+w, oy+ht+h) [base inf rectangle, w] →
    #                (ox+w, oy+ht) [costat dret rectangle, h] →
    #                (ox, oy) [hipotenusa triangle, hyp_tri] →
    #                (ox, oy+ht+h) [costat esquerre rectangle + catet esquerre triangle, h+ht]
    P = w + h + hyp_tri + (h + ht)
    g_enun = shape_graphic(viewBox_from(box, pad=14), shapes, labels_base + [label(ox + w / 2, oy + ht + h / 2, "P = ?", color="highlight", bold=True)])
    g_res = shape_graphic(viewBox_from(box, pad=14), shapes, labels_base + [label(ox + w / 2, oy + ht + h / 2, f"P = {fmt(P)} cm", color="highlight", bold=True)])
    correct = fmt_cm(P)
    wrong = [fmt_cm(2 * (w + h) + bt + ht), fmt_cm(w + h + bt + ht), fmt_cm2(w * h + bt * ht / 2)]
    opts, ci = make_opts(correct, wrong, 3)
    return build_question(
        24,
        f"La figura està formada per un rectangle de {w} cm × {h} cm amb un triangle rectangle al damunt (catets de {bt} cm i {ht} cm). Calcula el perímetre (contorn exterior).",
        g_enun, g_res, opts, ci,
        [
            {"kind": "text", "text": "Primer calculem la hipotenusa del triangle amb Pitàgores."},
            {"kind": "math", "tex": rf"\text{{hip}} = \sqrt{{{bt}^2 + {ht}^2}} = \sqrt{{{bt * bt + ht * ht}}} = {fmt(hyp_tri)}\ \text{{cm}}"},
            {"kind": "text", "text": "El contorn exterior recorre: base del rectangle, costat dret, hipotenusa del triangle i costat esquerre (rectangle + triangle)."},
            {"kind": "math", "tex": rf"P = {w} + {h} + {fmt(hyp_tri)} + ({h} + {ht}) = {fmt(P)}\ \text{{cm}}"},
        ],
    )


questions.append(q24())


# ---------- 25. Figura en T (dos rectangles) (àrea) ----------
def q25():
    # Rectangle horitzontal a dalt (ample) + rectangle vertical sota centrat (estret)
    Wt, Ht = 12, 3   # rectangle horitzontal (dalt)
    Wv, Hv = 4, 7    # rectangle vertical (baix, centrat)
    ox, oy = 10, 15  # cantonada superior esquerra del rect horitzontal
    top = polygon([(ox, oy), (ox + Wt, oy), (ox + Wt, oy + Ht), (ox, oy + Ht)])
    # rectangle vertical centrat respecte al horitzontal: comença a ox + (Wt - Wv)/2
    vx = ox + (Wt - Wv) / 2
    vy = oy + Ht
    bot = polygon([(vx, vy), (vx + Wv, vy), (vx + Wv, vy + Hv), (vx, vy + Hv)])
    sep = line((vx, vy), (vx + Wv, vy), dashed=True)
    shapes = [top, bot, sep]
    box = (ox, oy, Wt, Ht + Hv)
    labels_base = [
        label(ox + Wt / 2, oy - 4, f"{Wt} cm"),
        label(ox - 6, oy + Ht / 2, f"{Ht} cm"),
        label(vx + Wv / 2, vy + Hv + 4, f"{Wv} cm"),
        label(vx + Wv + 4, vy + Hv / 2, f"{Hv} cm", anchor="start"),
    ]
    A_top = Wt * Ht
    A_bot = Wv * Hv
    A = A_top + A_bot
    g_enun = shape_graphic(viewBox_from(box, pad=14), shapes, labels_base + [label(ox + Wt / 2, oy + Ht / 2, "A = ?", color="highlight", bold=True)])
    g_res = shape_graphic(viewBox_from(box, pad=14), shapes, labels_base + [label(ox + Wt / 2, oy + Ht / 2, f"A = {fmt(A)} cm²", color="highlight", bold=True)])
    correct = fmt_cm2(A)
    wrong = [fmt_cm2(Wt * (Ht + Hv)), fmt_cm2(A_top), fmt_cm(2 * (Wt + Ht) + 2 * (Wv + Hv))]
    opts, ci = make_opts(correct, wrong, 0)
    return build_question(
        25,
        f"La figura té forma de T: un rectangle horitzontal superior de {Wt} cm × {Ht} cm i un rectangle vertical inferior de {Wv} cm × {Hv} cm, centrat sota del primer. Calcula l'àrea total.",
        g_enun, g_res, opts, ci,
        [
            {"kind": "math", "tex": rf"A_1 = {Wt} \cdot {Ht} = {A_top}\ \text{{cm}}^2"},
            {"kind": "math", "tex": rf"A_2 = {Wv} \cdot {Hv} = {A_bot}\ \text{{cm}}^2"},
            {"kind": "math", "tex": rf"A = {A_top} + {A_bot} = {A}\ \text{{cm}}^2"},
        ],
    )


questions.append(q25())


# ====================================================================================
# Validacions bàsiques
# ====================================================================================
assert len(questions) == 25, f"Esperem 25 preguntes, hi ha {len(questions)}"
for q in questions:
    assert len(q["options"]) == 4, f"{q['id']}: ha de tenir 4 opcions"
    assert len(set(q["options"])) == 4, f"{q['id']}: opcions duplicades: {q['options']}"
    assert 0 <= q["correct"] < 4, f"{q['id']}: índex correcte fora de rang"


topic = {
    "id": "shapes-perimeter-area",
    "name": "Perímetres i àrees de figures planes",
    "description": "Càlcul de perímetres i àrees de figures bàsiques i compostes.",
    "questions": questions,
}

OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(json.dumps(topic, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(f"Escrit {OUT} amb {len(questions)} preguntes.")
