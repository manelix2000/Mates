#!/usr/bin/env python3
"""Genera volumes.json amb 25 exercicis de càlcul de volums.

Figures: prisma (rectangular i triangular), cilindre, piràmide (base quadrada
i triangular), con i esfera.  Cada exercici té gràfic esquemàtic 2D a
l'enunciat i a la resolució, amb les cotes rellevants.

Distribució:
  q1-q5   Prisma (3 rectangular, 2 triangular)
  q6-q10  Cilindre
  q11-q15 Piràmide (3 base quadrada, 2 base triangular)
  q16-q20 Con
  q21-q25 Esfera
"""
import json
import math
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "app" / "public" / "topics" / "volumes.json"


# ──────────────────────────── Helpers numèrics ────────────────────────────
def fmt(x, nd=2):
    r = round(x, nd)
    if abs(r - round(r)) < 1e-9:
        return f"{int(round(r))}"
    s = f"{r:.{nd}f}".rstrip("0").rstrip(".")
    return s


def fmt_cm3(x):
    return f"${fmt(x)}\\ \\text{{cm}}^3$"


def fmt_pi(coeff):
    """Retorna per ex. '$120\\pi\\ \\text{cm}^3$'."""
    c = fmt(coeff)
    return f"${c}\\pi\\ \\text{{cm}}^3$"


def qid(i):
    return f"vol-{i:03d}"


# ──────────────────────────── Helpers gràfic ────────────────────────────
def polygon(points, dashed=False, filled=True, highlight=False):
    s = {"type": "polygon", "points": [[round(p[0], 3), round(p[1], 3)] for p in points]}
    if dashed: s["dashed"] = True
    if filled: s["filled"] = True
    if highlight: s["highlight"] = True
    return s


def circle_shape(cx, cy, r, dashed=False, filled=True, highlight=False):
    s = {"type": "circle", "center": [round(cx, 3), round(cy, 3)], "r": round(r, 3)}
    if dashed: s["dashed"] = True
    if filled: s["filled"] = True
    if highlight: s["highlight"] = True
    return s


def arc(cx, cy, r, fromDeg, toDeg, closed=False, dashed=False, filled=True, highlight=False):
    s = {
        "type": "arc",
        "center": [round(cx, 3), round(cy, 3)],
        "r": round(r, 3),
        "fromDeg": fromDeg,
        "toDeg": toDeg,
    }
    if closed: s["closed"] = True
    if dashed: s["dashed"] = True
    if filled: s["filled"] = True
    if highlight: s["highlight"] = True
    return s


def line(p0, p1, dashed=False, highlight=False):
    s = {"type": "line",
         "from": [round(p0[0], 3), round(p0[1], 3)],
         "to": [round(p1[0], 3), round(p1[1], 3)]}
    if dashed: s["dashed"] = True
    if highlight: s["highlight"] = True
    return s


def label(x, y, text, anchor="middle", color="default", bold=False):
    l = {"at": [round(x, 3), round(y, 3)], "text": text, "anchor": anchor}
    if color != "default": l["color"] = color
    if bold: l["bold"] = True
    return l


def shape_graphic(viewBox, shapes, labels=None):
    g = {"kind": "shape-plot", "viewBox": [round(v, 3) for v in viewBox], "shapes": shapes}
    if labels: g["labels"] = labels
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


# ──────────────────────────── Dibuix 2D de figures 3D ────────────────────
# Totes generen una representació esquemàtica en 2D (vista lateral o
# 3/4) suficient per mostrar les cotes.  Coordenades SVG (Y cap avall).

def draw_rect_prism(w, d, h, ox=10, oy=10, show_dims=True,
                    w_label=None, d_label=None, h_label=None,
                    vol_label=None, highlight=False):
    """Prisma rectangular en projecció paral·lela senzilla.

    Dibuixa la cara frontal (w×h) i la cara lateral (d×h) amb profunditat
    representada en diagonal.
    """
    dx = d * 0.5
    dy = d * 0.4
    # Cara frontal (rectangle)
    f = [(ox, oy + dy + h), (ox + w, oy + dy + h),
         (ox + w, oy + dy), (ox, oy + dy)]
    # Cara superior
    t = [(ox, oy + dy), (ox + dx, oy), (ox + w + dx, oy), (ox + w, oy + dy)]
    # Cara lateral dreta
    r = [(ox + w, oy + dy), (ox + w + dx, oy),
         (ox + w + dx, oy + h), (ox + w, oy + dy + h)]

    shapes = [
        polygon(f, filled=True, highlight=highlight),
        polygon(t, filled=True, highlight=highlight),
        polygon(r, filled=True, highlight=highlight),
    ]
    labels = []
    pad = 1.5
    if show_dims:
        if w_label:
            labels.append(label(ox + w / 2, oy + dy + h + pad, w_label))
        if h_label:
            labels.append(label(ox - pad, oy + dy + h / 2, h_label, anchor="end"))
        if d_label:
            labels.append(label(ox + dx / 2 - pad * 0.5, oy + dy / 2 - pad * 0.3, d_label, anchor="end"))
    if vol_label:
        labels.append(label(ox + w / 2 + dx / 2, oy + dy + h / 2,
                            vol_label, color="highlight", bold=True))

    vb = (ox - 3, oy - 2, w + dx + 6, h + dy + 6)
    return shapes, labels, vb


def draw_triangular_prism(base, tri_h, depth, ox=10, oy=10, show_dims=True,
                          b_label=None, th_label=None, d_label=None,
                          vol_label=None, highlight=False):
    """Prisma triangular (base triangle rectangle) en vista 3/4."""
    dx = depth * 0.45
    dy = depth * 0.35
    # Triangle frontal (base horitz, vèrtex amunt)
    ft = [(ox, oy + dy + tri_h), (ox + base, oy + dy + tri_h),
          (ox + base / 2, oy + dy)]
    # Triangle posterior
    bt = [(ox + dx, oy + tri_h), (ox + base + dx, oy + tri_h),
          (ox + base / 2 + dx, oy)]
    shapes = [
        polygon(bt, filled=True, highlight=highlight, dashed=True),
        polygon(ft, filled=True, highlight=highlight),
        # arestes laterals
    ]
    # Arestes que connecten els dos triangles
    shapes.append(line((ox, oy + dy + tri_h), (ox + dx, oy + tri_h), dashed=True))
    shapes.append(line((ox + base, oy + dy + tri_h), (ox + base + dx, oy + tri_h)))
    shapes.append(line((ox + base / 2, oy + dy), (ox + base / 2 + dx, oy)))

    labels = []
    pad = 1.5
    if show_dims:
        if b_label:
            labels.append(label(ox + base / 2, oy + dy + tri_h + pad, b_label))
        if th_label:
            labels.append(label(ox - pad, oy + dy + tri_h / 2, th_label, anchor="end"))
        if d_label:
            labels.append(label(ox + base + dx / 2 + pad * 0.5, oy + tri_h / 2 + dy / 2, d_label, anchor="start"))
    if vol_label:
        labels.append(label(ox + base / 2 + dx / 3, oy + dy + tri_h * 0.6,
                            vol_label, color="highlight", bold=True))

    vb = (ox - 4, oy - 2, base + dx + 8, tri_h + dy + 5)
    return shapes, labels, vb


def draw_cylinder(r, h, ox=30, oy=10, show_dims=True,
                  r_label=None, h_label=None, d_label=None,
                  vol_label=None, highlight=False):
    """Cilindre: dues el·lipses + costats."""
    cx = ox
    ry = r * 0.3  # compressió vertical per perspectiva
    # El·lipse superior (arc complet via dos arcs)
    shapes = [
        # Cos: rectangle + el·lipses
        polygon([(cx - r, oy + ry), (cx + r, oy + ry),
                 (cx + r, oy + h + ry), (cx - r, oy + h + ry)],
                filled=True, highlight=highlight),
        # El·lipse inferior (visible)
        arc(cx, oy + h + ry, r, 0, 180, dashed=False, filled=False, highlight=highlight),
        arc(cx, oy + h + ry, r, 180, 360, dashed=True, filled=False, highlight=highlight),
        # El·lipse superior
        arc(cx, oy + ry, r, 0, 180, dashed=False, filled=False, highlight=highlight),
        arc(cx, oy + ry, r, 180, 360, dashed=False, filled=False, highlight=highlight),
    ]
    # Línies laterals
    shapes.append(line((cx - r, oy + ry), (cx - r, oy + h + ry)))
    shapes.append(line((cx + r, oy + ry), (cx + r, oy + h + ry)))

    labels = []
    pad = 1.5
    if show_dims:
        if r_label:
            # Radi dibuixat a la part superior
            shapes.append(line((cx, oy + ry), (cx + r, oy + ry), dashed=True))
            labels.append(label(cx + r / 2, oy + ry - pad, r_label))
        if d_label:
            shapes.append(line((cx - r, oy + ry), (cx + r, oy + ry), dashed=True))
            labels.append(label(cx, oy + ry - pad, d_label))
        if h_label:
            labels.append(label(cx - r - pad, oy + ry + h / 2, h_label, anchor="end"))
    if vol_label:
        labels.append(label(cx, oy + ry + h / 2, vol_label, color="highlight", bold=True))

    vb = (cx - r - 4, oy - 2, 2 * r + 8, h + 2 * ry + 5)
    return shapes, labels, vb


def draw_pyramid(base, h, ox=10, oy=10, show_dims=True,
                 b_label=None, h_label=None,
                 vol_label=None, highlight=False):
    """Piràmide de base quadrada: vista frontal (triangle) amb base representada."""
    dx = base * 0.3
    dy = base * 0.2
    # Base (romboide per representar el quadrat en perspectiva)
    bl = (ox, oy + h + dy)
    br = (ox + base, oy + h + dy)
    tr = (ox + base + dx, oy + h)
    tl = (ox + dx, oy + h)
    apex = (ox + base / 2 + dx / 2, oy)

    shapes = [
        # Cara frontal (triangle)
        polygon([bl, br, apex], filled=True, highlight=highlight),
        # Cara lateral dreta
        polygon([br, tr, apex], filled=True, highlight=highlight),
        # Base
        polygon([bl, br, tr, tl], filled=True, highlight=highlight, dashed=True),
        # Aresta posterior esquerra (dashed)
        line(tl, apex, dashed=True),
    ]
    # Altura (dashed, des del vèrtex fins al centre de la base)
    bcx = (bl[0] + br[0] + tr[0] + tl[0]) / 4
    bcy = (bl[1] + br[1] + tr[1] + tl[1]) / 4
    shapes.append(line(apex, (bcx, bcy), dashed=True, highlight=True))

    labels = []
    pad = 1.5
    if show_dims:
        if b_label:
            labels.append(label(ox + base / 2, oy + h + dy + pad, b_label))
        if h_label:
            labels.append(label(bcx + pad, (oy + bcy) / 2 + pad, h_label, anchor="start", color="highlight"))
    if vol_label:
        labels.append(label(ox + base / 2 + dx / 3, oy + h * 0.55,
                            vol_label, color="highlight", bold=True))

    vb = (ox - 3, oy - 2, base + dx + 6, h + dy + 5)
    return shapes, labels, vb


def draw_tri_pyramid(base, tri_h_base, h, ox=10, oy=10, show_dims=True,
                     b_label=None, bh_label=None, h_label=None,
                     vol_label=None, highlight=False):
    """Piràmide de base triangular: vista frontal simplificada."""
    dx = base * 0.25
    dy = base * 0.18
    # Triangle base (representat en perspectiva)
    bl = (ox, oy + h + dy)
    br = (ox + base, oy + h + dy)
    bt = (ox + base / 2 + dx, oy + h)
    apex = (ox + base / 2 + dx / 2, oy)

    shapes = [
        # Base (triangle en perspectiva)
        polygon([bl, br, bt], filled=True, highlight=highlight, dashed=True),
        # Cares laterals
        polygon([bl, br, apex], filled=True, highlight=highlight),
        polygon([br, bt, apex], filled=True, highlight=highlight),
        # Aresta posterior
        line(bl, bt, dashed=True),
        line(bt, apex, dashed=True),
    ]
    # Altura
    bcx = (bl[0] + br[0] + bt[0]) / 3
    bcy = (bl[1] + br[1] + bt[1]) / 3
    shapes.append(line(apex, (bcx, bcy), dashed=True, highlight=True))

    labels = []
    pad = 1.5
    if show_dims:
        if b_label:
            labels.append(label(ox + base / 2, oy + h + dy + pad, b_label))
        if bh_label:
            labels.append(label(ox - pad, oy + h + dy / 2, bh_label, anchor="end"))
        if h_label:
            labels.append(label(bcx + pad, (oy + bcy) / 2 + pad, h_label, anchor="start", color="highlight"))
    if vol_label:
        labels.append(label(ox + base / 2 + dx / 3, oy + h * 0.55,
                            vol_label, color="highlight", bold=True))

    vb = (ox - 4, oy - 2, base + dx + 8, h + dy + 5)
    return shapes, labels, vb


def draw_cone(r, h, ox=30, oy=10, show_dims=True,
              r_label=None, h_label=None,
              vol_label=None, highlight=False):
    """Con: triangle + el·lipse a la base."""
    cx = ox
    ry = r * 0.25
    apex = (cx, oy)

    shapes = [
        # Cos (triangle)
        polygon([(cx - r, oy + h), (cx + r, oy + h), apex],
                filled=True, highlight=highlight),
        # Base el·líptica (meitat visible + meitat dashed)
        arc(cx, oy + h, r, 0, 180, filled=False, highlight=highlight),
        arc(cx, oy + h, r, 180, 360, dashed=True, filled=False, highlight=highlight),
    ]
    # Altura
    shapes.append(line(apex, (cx, oy + h), dashed=True, highlight=True))
    # Radi
    if show_dims and r_label:
        shapes.append(line((cx, oy + h), (cx + r, oy + h), dashed=True))

    labels = []
    pad = 1.5
    if show_dims:
        if r_label:
            labels.append(label(cx + r / 2, oy + h + pad + ry, r_label))
        if h_label:
            labels.append(label(cx + pad, oy + h / 2, h_label, anchor="start", color="highlight"))
    if vol_label:
        labels.append(label(cx, oy + h * 0.5, vol_label, color="highlight", bold=True))

    vb = (cx - r - 3, oy - 2, 2 * r + 6, h + ry + 5)
    return shapes, labels, vb


def draw_sphere(r, ox=30, oy=30, show_dims=True,
                r_label=None, vol_label=None, highlight=False):
    """Esfera: cercle + el·lipse horitzontal (equador)."""
    cx, cy = ox, oy
    shapes = [
        circle_shape(cx, cy, r, filled=True, highlight=highlight),
        # Equador (meitat visible + meitat dashed)
        arc(cx, cy, r, 0, 180, dashed=True, filled=False),
        arc(cx, cy, r, 180, 360, filled=False),
    ]
    # Radi
    if show_dims and r_label:
        shapes.append(line((cx, cy), (cx + r, cy), highlight=True))
        labels = [label(cx + r / 2, cy - r * 0.15, r_label)]
    else:
        labels = []

    if vol_label:
        labels.append(label(cx, cy + r * 0.45, vol_label, color="highlight", bold=True))

    vb = (cx - r - 3, cy - r - 3, 2 * r + 6, 2 * r + 6)
    return shapes, labels, vb


# ──────────────────────────── Preguntes ──────────────────────────────────
questions = []

PI = math.pi

# ====================== PRISMA (q1-q5) ======================

def q1():
    # Prisma rectangular senzill
    w, d, h = 8, 5, 4
    V = w * d * h
    s_e, l_e, vb = draw_rect_prism(w, d, h, w_label=f"{w} cm", d_label=f"{d} cm", h_label=f"{h} cm")
    s_r, l_r, vb_r = draw_rect_prism(w, d, h, w_label=f"{w} cm", d_label=f"{d} cm", h_label=f"{h} cm",
                                      vol_label=f"V = {V} cm³")
    g_e = shape_graphic(vb, s_e, l_e)
    g_r = shape_graphic(vb_r, s_r, l_r)
    correct = fmt_cm3(V)
    wrong = [fmt_cm3(w * d + w * h + d * h),  # confondre amb meitat de l'àrea total
             fmt_cm3(w * d * h * 2),           # duplicar
             fmt_cm3(w * h * d / 2)]           # dividir per 2
    opts, ci = make_opts(correct, wrong, 0)
    return build_question(1,
        f"Calcula el volum d'un prisma rectangular de {w} cm × {d} cm × {h} cm.",
        g_e, g_r, opts, ci,
        [{"kind": "text", "text": "El volum d'un prisma rectangular és:"},
         {"kind": "math", "tex": r"V = \text{llarg} \times \text{ample} \times \text{alt}"},
         {"kind": "math", "tex": rf"V = {w} \times {d} \times {h} = {V}\ \text{{cm}}^3"}])


def q2():
    # Prisma rectangular – nombres més grans
    w, d, h = 12, 6, 10
    V = w * d * h
    s_e, l_e, vb = draw_rect_prism(w, d, h, w_label=f"{w} cm", d_label=f"{d} cm", h_label=f"{h} cm")
    s_r, l_r, vb_r = draw_rect_prism(w, d, h, w_label=f"{w} cm", d_label=f"{d} cm", h_label=f"{h} cm",
                                      vol_label=f"V = {V} cm³")
    g_e = shape_graphic(vb, s_e, l_e)
    g_r = shape_graphic(vb_r, s_r, l_r)
    correct = fmt_cm3(V)
    wrong = [fmt_cm3(2 * (w * d + w * h + d * h)),  # àrea total
             fmt_cm3(w + d + h),                      # suma
             fmt_cm3(w * d * h / 3)]                  # dividir per 3
    opts, ci = make_opts(correct, wrong, 1)
    return build_question(2,
        f"Calcula el volum d'un prisma rectangular de {w} cm × {d} cm × {h} cm.",
        g_e, g_r, opts, ci,
        [{"kind": "text", "text": "El volum d'un prisma rectangular és:"},
         {"kind": "math", "tex": r"V = l \times a \times h"},
         {"kind": "math", "tex": rf"V = {w} \times {d} \times {h} = {V}\ \text{{cm}}^3"}])


def q3():
    # Cub
    a = 7
    V = a ** 3
    s_e, l_e, vb = draw_rect_prism(a, a, a, w_label=f"{a} cm", d_label=f"{a} cm", h_label=f"{a} cm")
    s_r, l_r, vb_r = draw_rect_prism(a, a, a, w_label=f"{a} cm", d_label=f"{a} cm", h_label=f"{a} cm",
                                      vol_label=f"V = {V} cm³")
    g_e = shape_graphic(vb, s_e, l_e)
    g_r = shape_graphic(vb_r, s_r, l_r)
    correct = fmt_cm3(V)
    wrong = [fmt_cm3(6 * a ** 2),   # àrea total
             fmt_cm3(a ** 2),        # quadrat de l'aresta
             fmt_cm3(3 * a)]         # 3 × aresta
    opts, ci = make_opts(correct, wrong, 2)
    return build_question(3,
        f"Calcula el volum d'un cub d'aresta {a} cm.",
        g_e, g_r, opts, ci,
        [{"kind": "text", "text": "El volum d'un cub és:"},
         {"kind": "math", "tex": r"V = a^3"},
         {"kind": "math", "tex": rf"V = {a}^3 = {V}\ \text{{cm}}^3"}])


def q4():
    # Prisma triangular
    b, th, d = 6, 8, 10
    A_base = b * th / 2
    V = A_base * d
    s_e, l_e, vb = draw_triangular_prism(b, th, d,
        b_label=f"{b} cm", th_label=f"{th} cm", d_label=f"{d} cm")
    s_r, l_r, vb_r = draw_triangular_prism(b, th, d,
        b_label=f"{b} cm", th_label=f"{th} cm", d_label=f"{d} cm",
        vol_label=f"V = {int(V)} cm³")
    g_e = shape_graphic(vb, s_e, l_e)
    g_r = shape_graphic(vb_r, s_r, l_r)
    correct = fmt_cm3(V)
    wrong = [fmt_cm3(b * th * d),         # oblidar dividir per 2
             fmt_cm3(b * th * d / 3),     # dividir per 3
             fmt_cm3(b * d)]              # oblidar l'altura del triangle
    opts, ci = make_opts(correct, wrong, 0)
    return build_question(4,
        f"Calcula el volum d'un prisma triangular amb base triangular de base {b} cm i altura {th} cm, i profunditat {d} cm.",
        g_e, g_r, opts, ci,
        [{"kind": "text", "text": "L'àrea de la base triangular és:"},
         {"kind": "math", "tex": rf"A_{{base}} = \frac{{{b} \times {th}}}{{2}} = {int(A_base)}\ \text{{cm}}^2"},
         {"kind": "text", "text": "El volum del prisma és:"},
         {"kind": "math", "tex": rf"V = A_{{base}} \times \text{{profunditat}} = {int(A_base)} \times {d} = {int(V)}\ \text{{cm}}^3"}])


def q5():
    # Prisma triangular 2
    b, th, d = 10, 6, 15
    A_base = b * th / 2
    V = A_base * d
    s_e, l_e, vb = draw_triangular_prism(b, th, d,
        b_label=f"{b} cm", th_label=f"{th} cm", d_label=f"{d} cm")
    s_r, l_r, vb_r = draw_triangular_prism(b, th, d,
        b_label=f"{b} cm", th_label=f"{th} cm", d_label=f"{d} cm",
        vol_label=f"V = {int(V)} cm³")
    g_e = shape_graphic(vb, s_e, l_e)
    g_r = shape_graphic(vb_r, s_r, l_r)
    correct = fmt_cm3(V)
    wrong = [fmt_cm3(b * th * d),         # oblidar dividir per 2
             fmt_cm3(b * th / 2),         # oblidar profunditat
             fmt_cm3(b * d * th / 3)]     # dividir per 3
    opts, ci = make_opts(correct, wrong, 3)
    return build_question(5,
        f"Calcula el volum d'un prisma triangular amb base triangular de base {b} cm i altura {th} cm, i profunditat {d} cm.",
        g_e, g_r, opts, ci,
        [{"kind": "text", "text": "L'àrea de la base triangular és:"},
         {"kind": "math", "tex": rf"A_{{base}} = \frac{{{b} \times {th}}}{{2}} = {int(A_base)}\ \text{{cm}}^2"},
         {"kind": "text", "text": "El volum del prisma és:"},
         {"kind": "math", "tex": rf"V = A_{{base}} \times \text{{prof.}} = {int(A_base)} \times {d} = {int(V)}\ \text{{cm}}^3"}])


# ====================== CILINDRE (q6-q10) ======================

def q6():
    r, h = 5, 10
    V = round(PI * r ** 2 * h, 2)
    coeff = r ** 2 * h  # 250
    s_e, l_e, vb = draw_cylinder(r, h, r_label=f"{r} cm", h_label=f"{h} cm")
    s_r, l_r, vb_r = draw_cylinder(r, h, r_label=f"{r} cm", h_label=f"{h} cm",
                                    vol_label=f"V = {coeff}π cm³")
    g_e = shape_graphic(vb, s_e, l_e)
    g_r = shape_graphic(vb_r, s_r, l_r)
    correct = fmt_pi(coeff)
    wrong = [fmt_pi(2 * r * h),           # àrea lateral sense π extra
             fmt_pi(r * h),               # oblidar elevar al quadrat
             fmt_cm3(round(V, 2))]        # valor decimal (no en forma π)
    # Assegurem opcions úniques
    opts, ci = make_opts(correct, wrong, 1)
    return build_question(6,
        f"Calcula el volum d'un cilindre de radi {r} cm i altura {h} cm. Expressa el resultat en funció de $\\pi$.",
        g_e, g_r, opts, ci,
        [{"kind": "text", "text": "El volum d'un cilindre és:"},
         {"kind": "math", "tex": r"V = \pi r^2 h"},
         {"kind": "math", "tex": rf"V = \pi \cdot {r}^2 \cdot {h} = {coeff}\pi\ \text{{cm}}^3"}])


def q7():
    r, h = 3, 14
    coeff = r ** 2 * h  # 126
    s_e, l_e, vb = draw_cylinder(r, h, r_label=f"{r} cm", h_label=f"{h} cm")
    s_r, l_r, vb_r = draw_cylinder(r, h, r_label=f"{r} cm", h_label=f"{h} cm",
                                    vol_label=f"V = {coeff}π cm³")
    g_e = shape_graphic(vb, s_e, l_e)
    g_r = shape_graphic(vb_r, s_r, l_r)
    correct = fmt_pi(coeff)
    wrong = [fmt_pi(r * h),                       # oblidar r²
             fmt_pi(2 * r * h + 2 * r ** 2),      # àrea total
             fmt_pi(2 * r ** 2 * h)]               # duplicar
    opts, ci = make_opts(correct, wrong, 0)
    return build_question(7,
        f"Calcula el volum d'un cilindre de radi {r} cm i altura {h} cm. Expressa el resultat en funció de $\\pi$.",
        g_e, g_r, opts, ci,
        [{"kind": "text", "text": "El volum d'un cilindre és:"},
         {"kind": "math", "tex": r"V = \pi r^2 h"},
         {"kind": "math", "tex": rf"V = \pi \cdot {r}^2 \cdot {h} = {coeff}\pi\ \text{{cm}}^3"}])


def q8():
    # Donat diàmetre
    d, h = 12, 7
    r = d / 2
    coeff = r ** 2 * h  # 252
    s_e, l_e, vb = draw_cylinder(r, h, d_label=f"d = {d} cm", h_label=f"{h} cm")
    s_r, l_r, vb_r = draw_cylinder(r, h, r_label=f"r = {int(r)} cm", h_label=f"{h} cm",
                                    vol_label=f"V = {int(coeff)}π cm³")
    g_e = shape_graphic(vb, s_e, l_e)
    g_r = shape_graphic(vb_r, s_r, l_r)
    correct = fmt_pi(int(coeff))
    wrong = [fmt_pi(d ** 2 * h),                  # usar diàmetre com a radi
             fmt_pi(int(r * h)),                   # oblidar r²
             fmt_pi(int(r ** 2 * h / 3))]          # fórmula del con
    opts, ci = make_opts(correct, wrong, 2)
    return build_question(8,
        f"Calcula el volum d'un cilindre de diàmetre {d} cm i altura {h} cm. Expressa el resultat en funció de $\\pi$.",
        g_e, g_r, opts, ci,
        [{"kind": "text", "text": "Primer trobem el radi:"},
         {"kind": "math", "tex": rf"r = \frac{{d}}{{2}} = \frac{{{d}}}{{2}} = {int(r)}\ \text{{cm}}"},
         {"kind": "text", "text": "El volum del cilindre és:"},
         {"kind": "math", "tex": r"V = \pi r^2 h"},
         {"kind": "math", "tex": rf"V = \pi \cdot {int(r)}^2 \cdot {h} = {int(coeff)}\pi\ \text{{cm}}^3"}])


def q9():
    r, h = 4, 9
    coeff = r ** 2 * h  # 144
    V = round(PI * coeff, 2)
    s_e, l_e, vb = draw_cylinder(r, h, r_label=f"{r} cm", h_label=f"{h} cm")
    s_r, l_r, vb_r = draw_cylinder(r, h, r_label=f"{r} cm", h_label=f"{h} cm",
                                    vol_label=f"V ≈ {fmt(V)} cm³")
    g_e = shape_graphic(vb, s_e, l_e)
    g_r = shape_graphic(vb_r, s_r, l_r)
    correct = fmt_cm3(V)
    wrong = [fmt_cm3(round(PI * r * h, 2)),              # oblidar r²
             fmt_cm3(round(PI * r ** 2 * h / 3, 2)),     # fórmula del con
             fmt_cm3(round(2 * PI * r * h, 2))]           # àrea lateral
    opts, ci = make_opts(correct, wrong, 1)
    return build_question(9,
        f"Calcula el volum d'un cilindre de radi {r} cm i altura {h} cm. Arrodoneix a les centèsimes.",
        g_e, g_r, opts, ci,
        [{"kind": "text", "text": "El volum d'un cilindre és:"},
         {"kind": "math", "tex": r"V = \pi r^2 h"},
         {"kind": "math", "tex": rf"V = \pi \cdot {r}^2 \cdot {h} = {coeff}\pi \approx {fmt(V)}\ \text{{cm}}^3"}])


def q10():
    r, h = 7, 5
    coeff = r ** 2 * h  # 245
    s_e, l_e, vb = draw_cylinder(r, h, r_label=f"{r} cm", h_label=f"{h} cm")
    s_r, l_r, vb_r = draw_cylinder(r, h, r_label=f"{r} cm", h_label=f"{h} cm",
                                    vol_label=f"V = {coeff}π cm³")
    g_e = shape_graphic(vb, s_e, l_e)
    g_r = shape_graphic(vb_r, s_r, l_r)
    correct = fmt_pi(coeff)
    wrong = [fmt_pi(r * h),                       # oblidar r²
             fmt_pi(2 * r ** 2 + 2 * r * h),      # àrea total
             fmt_pi(coeff // 3)]                   # fórmula del con
    opts, ci = make_opts(correct, wrong, 3)
    return build_question(10,
        f"Calcula el volum d'un cilindre de radi {r} cm i altura {h} cm. Expressa el resultat en funció de $\\pi$.",
        g_e, g_r, opts, ci,
        [{"kind": "text", "text": "El volum d'un cilindre és:"},
         {"kind": "math", "tex": r"V = \pi r^2 h"},
         {"kind": "math", "tex": rf"V = \pi \cdot {r}^2 \cdot {h} = {coeff}\pi\ \text{{cm}}^3"}])


# ====================== PIRÀMIDE (q11-q15) ======================

def q11():
    # Piràmide base quadrada
    b, h = 6, 9
    V = b ** 2 * h / 3
    s_e, l_e, vb = draw_pyramid(b, h, b_label=f"{b} cm", h_label=f"{h} cm")
    s_r, l_r, vb_r = draw_pyramid(b, h, b_label=f"{b} cm", h_label=f"{h} cm",
                                    vol_label=f"V = {int(V)} cm³")
    g_e = shape_graphic(vb, s_e, l_e)
    g_r = shape_graphic(vb_r, s_r, l_r)
    correct = fmt_cm3(V)
    wrong = [fmt_cm3(b ** 2 * h),          # oblidar dividir per 3
             fmt_cm3(b * h / 3),           # base lineal
             fmt_cm3(b ** 2 * h / 2)]      # dividir per 2
    opts, ci = make_opts(correct, wrong, 0)
    return build_question(11,
        f"Calcula el volum d'una piràmide de base quadrada de costat {b} cm i altura {h} cm.",
        g_e, g_r, opts, ci,
        [{"kind": "text", "text": "El volum d'una piràmide és:"},
         {"kind": "math", "tex": r"V = \frac{1}{3} \cdot A_{base} \cdot h"},
         {"kind": "text", "text": f"L'àrea de la base quadrada és ${b}^2 = {b**2}\\ \\text{{cm}}^2$."},
         {"kind": "math", "tex": rf"V = \frac{{1}}{{3}} \cdot {b**2} \cdot {h} = {int(V)}\ \text{{cm}}^3"}])


def q12():
    b, h = 10, 12
    V = b ** 2 * h / 3
    s_e, l_e, vb = draw_pyramid(b, h, b_label=f"{b} cm", h_label=f"{h} cm")
    s_r, l_r, vb_r = draw_pyramid(b, h, b_label=f"{b} cm", h_label=f"{h} cm",
                                    vol_label=f"V = {int(V)} cm³")
    g_e = shape_graphic(vb, s_e, l_e)
    g_r = shape_graphic(vb_r, s_r, l_r)
    correct = fmt_cm3(V)
    wrong = [fmt_cm3(b ** 2 * h),          # oblidar /3
             fmt_cm3(b ** 2 * h / 2),      # dividir per 2
             fmt_cm3(4 * b * h / 3)]       # perimetre × h / 3
    opts, ci = make_opts(correct, wrong, 2)
    return build_question(12,
        f"Calcula el volum d'una piràmide de base quadrada de costat {b} cm i altura {h} cm.",
        g_e, g_r, opts, ci,
        [{"kind": "text", "text": "El volum d'una piràmide és:"},
         {"kind": "math", "tex": r"V = \frac{1}{3} \cdot A_{base} \cdot h"},
         {"kind": "text", "text": f"L'àrea de la base quadrada és ${b}^2 = {b**2}\\ \\text{{cm}}^2$."},
         {"kind": "math", "tex": rf"V = \frac{{1}}{{3}} \cdot {b**2} \cdot {h} = {int(V)}\ \text{{cm}}^3"}])


def q13():
    b, h = 8, 15
    V = b ** 2 * h / 3
    s_e, l_e, vb = draw_pyramid(b, h, b_label=f"{b} cm", h_label=f"{h} cm")
    s_r, l_r, vb_r = draw_pyramid(b, h, b_label=f"{b} cm", h_label=f"{h} cm",
                                    vol_label=f"V = {int(V)} cm³")
    g_e = shape_graphic(vb, s_e, l_e)
    g_r = shape_graphic(vb_r, s_r, l_r)
    correct = fmt_cm3(V)
    wrong = [fmt_cm3(b ** 2 * h),           # oblidar /3
             fmt_cm3(b * h),                # base lineal × h
             fmt_cm3(b ** 2 * h / 6)]       # dividir per 6
    opts, ci = make_opts(correct, wrong, 1)
    return build_question(13,
        f"Calcula el volum d'una piràmide de base quadrada de costat {b} cm i altura {h} cm.",
        g_e, g_r, opts, ci,
        [{"kind": "text", "text": "El volum d'una piràmide és:"},
         {"kind": "math", "tex": r"V = \frac{1}{3} \cdot A_{base} \cdot h"},
         {"kind": "math", "tex": rf"A_{{base}} = {b}^2 = {b**2}\ \text{{cm}}^2"},
         {"kind": "math", "tex": rf"V = \frac{{1}}{{3}} \cdot {b**2} \cdot {h} = {int(V)}\ \text{{cm}}^3"}])


def q14():
    # Piràmide base triangular
    bt, bh, h = 6, 8, 12
    A_base = bt * bh / 2
    V = A_base * h / 3
    s_e, l_e, vb = draw_tri_pyramid(bt, bh, h, b_label=f"{bt} cm", bh_label=f"{bh} cm", h_label=f"{h} cm")
    s_r, l_r, vb_r = draw_tri_pyramid(bt, bh, h, b_label=f"{bt} cm", bh_label=f"{bh} cm", h_label=f"{h} cm",
                                       vol_label=f"V = {int(V)} cm³")
    g_e = shape_graphic(vb, s_e, l_e)
    g_r = shape_graphic(vb_r, s_r, l_r)
    correct = fmt_cm3(V)
    wrong = [fmt_cm3(bt * bh * h / 3),      # oblidar /2 a la base
             fmt_cm3(A_base * h),            # oblidar /3
             fmt_cm3(bt * bh * h)]           # oblidar /2 i /3
    opts, ci = make_opts(correct, wrong, 3)
    return build_question(14,
        f"Calcula el volum d'una piràmide de base triangular (base {bt} cm, altura del triangle {bh} cm) i altura de la piràmide {h} cm.",
        g_e, g_r, opts, ci,
        [{"kind": "text", "text": "L'àrea de la base triangular és:"},
         {"kind": "math", "tex": rf"A_{{base}} = \frac{{{bt} \times {bh}}}{{2}} = {int(A_base)}\ \text{{cm}}^2"},
         {"kind": "text", "text": "El volum de la piràmide és:"},
         {"kind": "math", "tex": r"V = \frac{1}{3} \cdot A_{base} \cdot h"},
         {"kind": "math", "tex": rf"V = \frac{{1}}{{3}} \cdot {int(A_base)} \cdot {h} = {int(V)}\ \text{{cm}}^3"}])


def q15():
    # Piràmide base triangular 2
    bt, bh, h = 10, 5, 9
    A_base = bt * bh / 2
    V = A_base * h / 3
    s_e, l_e, vb = draw_tri_pyramid(bt, bh, h, b_label=f"{bt} cm", bh_label=f"{bh} cm", h_label=f"{h} cm")
    s_r, l_r, vb_r = draw_tri_pyramid(bt, bh, h, b_label=f"{bt} cm", bh_label=f"{bh} cm", h_label=f"{h} cm",
                                       vol_label=f"V = {int(V)} cm³")
    g_e = shape_graphic(vb, s_e, l_e)
    g_r = shape_graphic(vb_r, s_r, l_r)
    correct = fmt_cm3(V)
    wrong = [fmt_cm3(bt * bh * h / 3),    # oblidar /2 a la base
             fmt_cm3(A_base * h),          # oblidar /3
             fmt_cm3(bt * bh * h)]         # oblidar /2 i /3
    opts, ci = make_opts(correct, wrong, 0)
    return build_question(15,
        f"Calcula el volum d'una piràmide de base triangular (base {bt} cm, altura del triangle {bh} cm) i altura de la piràmide {h} cm.",
        g_e, g_r, opts, ci,
        [{"kind": "text", "text": "L'àrea de la base triangular és:"},
         {"kind": "math", "tex": rf"A_{{base}} = \frac{{{bt} \times {bh}}}{{2}} = {int(A_base)}\ \text{{cm}}^2"},
         {"kind": "text", "text": "El volum de la piràmide és:"},
         {"kind": "math", "tex": r"V = \frac{1}{3} \cdot A_{base} \cdot h"},
         {"kind": "math", "tex": rf"V = \frac{{1}}{{3}} \cdot {int(A_base)} \cdot {h} = {int(V)}\ \text{{cm}}^3"}])


# ====================== CON (q16-q20) ======================

def q16():
    r, h = 4, 9
    coeff = r ** 2 * h  # 144
    V_coeff = coeff / 3  # 48
    s_e, l_e, vb = draw_cone(r, h, r_label=f"{r} cm", h_label=f"{h} cm")
    s_r, l_r, vb_r = draw_cone(r, h, r_label=f"{r} cm", h_label=f"{h} cm",
                                vol_label=f"V = {int(V_coeff)}π cm³")
    g_e = shape_graphic(vb, s_e, l_e)
    g_r = shape_graphic(vb_r, s_r, l_r)
    correct = fmt_pi(int(V_coeff))
    wrong = [fmt_pi(coeff),                   # oblidar /3 (fórmula del cilindre)
             fmt_pi(r * h),                   # oblidar r² i /3
             fmt_pi(int(coeff / 2))]          # dividir per 2
    opts, ci = make_opts(correct, wrong, 0)
    return build_question(16,
        f"Calcula el volum d'un con de radi {r} cm i altura {h} cm. Expressa el resultat en funció de $\\pi$.",
        g_e, g_r, opts, ci,
        [{"kind": "text", "text": "El volum d'un con és:"},
         {"kind": "math", "tex": r"V = \frac{1}{3} \pi r^2 h"},
         {"kind": "math", "tex": rf"V = \frac{{1}}{{3}} \cdot \pi \cdot {r}^2 \cdot {h} = {int(V_coeff)}\pi\ \text{{cm}}^3"}])


def q17():
    r, h = 6, 10
    coeff = r ** 2 * h
    V_coeff = coeff / 3  # 120
    s_e, l_e, vb = draw_cone(r, h, r_label=f"{r} cm", h_label=f"{h} cm")
    s_r, l_r, vb_r = draw_cone(r, h, r_label=f"{r} cm", h_label=f"{h} cm",
                                vol_label=f"V = {int(V_coeff)}π cm³")
    g_e = shape_graphic(vb, s_e, l_e)
    g_r = shape_graphic(vb_r, s_r, l_r)
    correct = fmt_pi(int(V_coeff))
    wrong = [fmt_pi(coeff),              # cilindre
             fmt_pi(int(V_coeff * 2)),   # ×2
             fmt_pi(r * h)]              # r×h
    opts, ci = make_opts(correct, wrong, 1)
    return build_question(17,
        f"Calcula el volum d'un con de radi {r} cm i altura {h} cm. Expressa el resultat en funció de $\\pi$.",
        g_e, g_r, opts, ci,
        [{"kind": "text", "text": "El volum d'un con és:"},
         {"kind": "math", "tex": r"V = \frac{1}{3} \pi r^2 h"},
         {"kind": "math", "tex": rf"V = \frac{{1}}{{3}} \cdot \pi \cdot {r}^2 \cdot {h} = {int(V_coeff)}\pi\ \text{{cm}}^3"}])


def q18():
    # Donat diàmetre
    d, h = 10, 12
    r = d / 2
    coeff = r ** 2 * h
    V_coeff = coeff / 3  # 100
    s_e, l_e, vb = draw_cone(r, h, r_label=f"d = {d} cm", h_label=f"{h} cm")
    s_r, l_r, vb_r = draw_cone(r, h, r_label=f"r = {int(r)} cm", h_label=f"{h} cm",
                                vol_label=f"V = {int(V_coeff)}π cm³")
    g_e = shape_graphic(vb, s_e, l_e)
    g_r = shape_graphic(vb_r, s_r, l_r)
    correct = fmt_pi(int(V_coeff))
    wrong = [fmt_pi(int(d ** 2 * h / 3)),    # usar diàmetre com a radi
             fmt_pi(int(coeff)),              # fórmula del cilindre
             fmt_pi(int(r * h))]              # oblidar r²
    opts, ci = make_opts(correct, wrong, 2)
    return build_question(18,
        f"Calcula el volum d'un con de diàmetre {d} cm i altura {h} cm. Expressa el resultat en funció de $\\pi$.",
        g_e, g_r, opts, ci,
        [{"kind": "text", "text": "Primer trobem el radi:"},
         {"kind": "math", "tex": rf"r = \frac{{d}}{{2}} = \frac{{{d}}}{{2}} = {int(r)}\ \text{{cm}}"},
         {"kind": "text", "text": "El volum del con és:"},
         {"kind": "math", "tex": r"V = \frac{1}{3} \pi r^2 h"},
         {"kind": "math", "tex": rf"V = \frac{{1}}{{3}} \cdot \pi \cdot {int(r)}^2 \cdot {h} = {int(V_coeff)}\pi\ \text{{cm}}^3"}])


def q19():
    r, h = 3, 8
    coeff = r ** 2 * h  # 72
    V_coeff = coeff / 3  # 24
    V = round(PI * V_coeff, 2)
    s_e, l_e, vb = draw_cone(r, h, r_label=f"{r} cm", h_label=f"{h} cm")
    s_r, l_r, vb_r = draw_cone(r, h, r_label=f"{r} cm", h_label=f"{h} cm",
                                vol_label=f"V ≈ {fmt(V)} cm³")
    g_e = shape_graphic(vb, s_e, l_e)
    g_r = shape_graphic(vb_r, s_r, l_r)
    correct = fmt_cm3(V)
    wrong = [fmt_cm3(round(PI * coeff, 2)),          # cilindre (sense /3)
             fmt_cm3(round(PI * r ** 2 * h / 2, 2)),  # /2 en lloc de /3
             fmt_cm3(round(2 * PI * r * h, 2))]        # àrea lateral
    opts, ci = make_opts(correct, wrong, 3)
    return build_question(19,
        f"Calcula el volum d'un con de radi {r} cm i altura {h} cm. Arrodoneix a les centèsimes.",
        g_e, g_r, opts, ci,
        [{"kind": "text", "text": "El volum d'un con és:"},
         {"kind": "math", "tex": r"V = \frac{1}{3} \pi r^2 h"},
         {"kind": "math", "tex": rf"V = \frac{{1}}{{3}} \cdot \pi \cdot {r}^2 \cdot {h} = {int(V_coeff)}\pi \approx {fmt(V)}\ \text{{cm}}^3"}])


def q20():
    r, h = 5, 15
    coeff = r ** 2 * h  # 375
    V_coeff = coeff / 3  # 125
    s_e, l_e, vb = draw_cone(r, h, r_label=f"{r} cm", h_label=f"{h} cm")
    s_r, l_r, vb_r = draw_cone(r, h, r_label=f"{r} cm", h_label=f"{h} cm",
                                vol_label=f"V = {int(V_coeff)}π cm³")
    g_e = shape_graphic(vb, s_e, l_e)
    g_r = shape_graphic(vb_r, s_r, l_r)
    correct = fmt_pi(int(V_coeff))
    wrong = [fmt_pi(coeff),                        # cilindre
             fmt_pi(int(V_coeff * 4 / 3)),         # confondre amb esfera
             fmt_pi(r * h)]                         # r×h
    opts, ci = make_opts(correct, wrong, 0)
    return build_question(20,
        f"Calcula el volum d'un con de radi {r} cm i altura {h} cm. Expressa el resultat en funció de $\\pi$.",
        g_e, g_r, opts, ci,
        [{"kind": "text", "text": "El volum d'un con és:"},
         {"kind": "math", "tex": r"V = \frac{1}{3} \pi r^2 h"},
         {"kind": "math", "tex": rf"V = \frac{{1}}{{3}} \cdot \pi \cdot {r}^2 \cdot {h} = {int(V_coeff)}\pi\ \text{{cm}}^3"}])


# ====================== ESFERA (q21-q25) ======================

def q21():
    r = 6
    coeff = 4 * r ** 3 / 3  # 288
    s_e, l_e, vb = draw_sphere(r, r_label=f"{r} cm")
    s_r, l_r, vb_r = draw_sphere(r, r_label=f"{r} cm", vol_label=f"V = {int(coeff)}π cm³")
    g_e = shape_graphic(vb, s_e, l_e)
    g_r = shape_graphic(vb_r, s_r, l_r)
    correct = fmt_pi(int(coeff))
    wrong = [fmt_pi(4 * r ** 2),                  # àrea superficial (sense /1)
             fmt_pi(r ** 3),                       # oblidar 4/3
             fmt_pi(int(4 * r ** 3))]              # oblidar /3
    opts, ci = make_opts(correct, wrong, 1)
    return build_question(21,
        f"Calcula el volum d'una esfera de radi {r} cm. Expressa el resultat en funció de $\\pi$.",
        g_e, g_r, opts, ci,
        [{"kind": "text", "text": "El volum d'una esfera és:"},
         {"kind": "math", "tex": r"V = \frac{4}{3} \pi r^3"},
         {"kind": "math", "tex": rf"V = \frac{{4}}{{3}} \cdot \pi \cdot {r}^3 = {int(coeff)}\pi\ \text{{cm}}^3"}])


def q22():
    r = 9
    coeff = 4 * r ** 3 / 3  # 972
    s_e, l_e, vb = draw_sphere(r, r_label=f"{r} cm")
    s_r, l_r, vb_r = draw_sphere(r, r_label=f"{r} cm", vol_label=f"V = {int(coeff)}π cm³")
    g_e = shape_graphic(vb, s_e, l_e)
    g_r = shape_graphic(vb_r, s_r, l_r)
    correct = fmt_pi(int(coeff))
    wrong = [fmt_pi(4 * r ** 2),            # àrea superficial
             fmt_pi(int(r ** 3 / 3)),        # oblidar el 4
             fmt_pi(int(4 * r ** 3))]        # oblidar /3
    opts, ci = make_opts(correct, wrong, 0)
    return build_question(22,
        f"Calcula el volum d'una esfera de radi {r} cm. Expressa el resultat en funció de $\\pi$.",
        g_e, g_r, opts, ci,
        [{"kind": "text", "text": "El volum d'una esfera és:"},
         {"kind": "math", "tex": r"V = \frac{4}{3} \pi r^3"},
         {"kind": "math", "tex": rf"V = \frac{{4}}{{3}} \cdot \pi \cdot {r}^3 = {int(coeff)}\pi\ \text{{cm}}^3"}])


def q23():
    # Donat diàmetre
    d = 14
    r = d / 2
    coeff = 4 * r ** 3 / 3  # 457.333...
    coeff_frac = f"\\frac{{{4 * int(r ** 3)}}}{{{3}}}"
    V = round(4 / 3 * PI * r ** 3, 2)
    s_e, l_e, vb = draw_sphere(r, r_label=f"d = {d} cm")
    s_r, l_r, vb_r = draw_sphere(r, r_label=f"r = {int(r)} cm", vol_label=f"V ≈ {fmt(V)} cm³")
    g_e = shape_graphic(vb, s_e, l_e)
    g_r = shape_graphic(vb_r, s_r, l_r)
    correct = fmt_cm3(V)
    wrong = [fmt_cm3(round(4 / 3 * PI * d ** 3, 2)),    # usar diàmetre com a radi
             fmt_cm3(round(PI * r ** 3, 2)),              # oblidar 4/3
             fmt_cm3(round(4 * PI * r ** 2, 2))]          # àrea superficial
    opts, ci = make_opts(correct, wrong, 2)
    return build_question(23,
        f"Calcula el volum d'una esfera de diàmetre {d} cm. Arrodoneix a les centèsimes.",
        g_e, g_r, opts, ci,
        [{"kind": "text", "text": "Primer trobem el radi:"},
         {"kind": "math", "tex": rf"r = \frac{{d}}{{2}} = \frac{{{d}}}{{2}} = {int(r)}\ \text{{cm}}"},
         {"kind": "text", "text": "El volum de l'esfera és:"},
         {"kind": "math", "tex": r"V = \frac{4}{3} \pi r^3"},
         {"kind": "math", "tex": rf"V = \frac{{4}}{{3}} \cdot \pi \cdot {int(r)}^3 = {coeff_frac}\pi \approx {fmt(V)}\ \text{{cm}}^3"}])


def q24():
    r = 3
    coeff = 4 * r ** 3 / 3  # 36
    V = round(PI * coeff, 2)
    s_e, l_e, vb = draw_sphere(r, r_label=f"{r} cm")
    s_r, l_r, vb_r = draw_sphere(r, r_label=f"{r} cm", vol_label=f"V ≈ {fmt(V)} cm³")
    g_e = shape_graphic(vb, s_e, l_e)
    g_r = shape_graphic(vb_r, s_r, l_r)
    correct = fmt_cm3(V)
    wrong = [fmt_cm3(round(PI * r ** 3, 2)),           # oblidar 4/3
             fmt_cm3(round(4 / 3 * PI * r ** 2, 2)),   # r² en lloc de r³
             fmt_cm3(round(4 * PI * r ** 3, 2))]       # oblidar /3
    opts, ci = make_opts(correct, wrong, 3)
    return build_question(24,
        f"Calcula el volum d'una esfera de radi {r} cm. Arrodoneix a les centèsimes.",
        g_e, g_r, opts, ci,
        [{"kind": "text", "text": "El volum d'una esfera és:"},
         {"kind": "math", "tex": r"V = \frac{4}{3} \pi r^3"},
         {"kind": "math", "tex": rf"V = \frac{{4}}{{3}} \cdot \pi \cdot {r}^3 = {int(coeff)}\pi \approx {fmt(V)}\ \text{{cm}}^3"}])


def q25():
    r = 10
    coeff = 4 * r ** 3 / 3  # 1333.33...
    coeff_frac = f"\\frac{{{4 * r ** 3}}}{{{3}}}"
    s_e, l_e, vb = draw_sphere(r, r_label=f"{r} cm")
    s_r, l_r, vb_r = draw_sphere(r, r_label=f"{r} cm",
                                  vol_label=f"V = {coeff_frac}π cm³")
    g_e = shape_graphic(vb, s_e, l_e)
    g_r = shape_graphic(vb_r, s_r, l_r)
    correct = f"$\\frac{{{4 * r ** 3}}}{{3}}\\pi\\ \\text{{cm}}^3$"
    wrong = [fmt_pi(4 * r ** 2),                     # àrea superficial
             fmt_pi(r ** 3),                          # oblidar 4/3
             fmt_pi(4 * r ** 3)]                      # oblidar /3
    opts, ci = make_opts(correct, wrong, 1)
    return build_question(25,
        f"Calcula el volum d'una esfera de radi {r} cm. Expressa el resultat en funció de $\\pi$.",
        g_e, g_r, opts, ci,
        [{"kind": "text", "text": "El volum d'una esfera és:"},
         {"kind": "math", "tex": r"V = \frac{4}{3} \pi r^3"},
         {"kind": "math", "tex": rf"V = \frac{{4}}{{3}} \cdot \pi \cdot {r}^3 = \frac{{{4 * r ** 3}}}{{3}}\pi\ \text{{cm}}^3"}])


# ──────────────────────────── Genera ────────────────────────────────────
for fn in [q1, q2, q3, q4, q5, q6, q7, q8, q9, q10,
           q11, q12, q13, q14, q15, q16, q17, q18, q19, q20,
           q21, q22, q23, q24, q25]:
    questions.append(fn())


# ──────────────────────────── Validacions ────────────────────────────────
assert len(questions) == 25, f"Esperem 25 preguntes, hi ha {len(questions)}"
for q in questions:
    assert len(q["options"]) == 4, f"{q['id']}: ha de tenir 4 opcions"
    assert len(set(q["options"])) == 4, f"{q['id']}: opcions duplicades: {q['options']}"
    assert 0 <= q["correct"] < 4, f"{q['id']}: índex correcte fora de rang"


topic = {
    "id": "volumes",
    "name": "Volums de cossos geomètrics",
    "description": "Càlcul de volums de prismes, cilindres, piràmides, cons i esferes.",
    "questions": questions,
}

OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(json.dumps(topic, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(f"Escrit {OUT} amb {len(questions)} preguntes.")
