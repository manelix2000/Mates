#!/usr/bin/env python3
"""Genera applied-right-triangles.json amb 25 problemes aplicats de trigonometria."""
import json
import math
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "app" / "public" / "topics" / "applied-right-triangles.json"


def fmt(x, nd=2):
    r = round(x, nd)
    if abs(r - round(r)) < 1e-9:
        return f"{int(round(r))}"
    return f"{r:.{nd}f}".rstrip("0").rstrip(".")


def fmt_m(x):
    return f"${fmt(x)}\\ \\text{{m}}$"


def fmt_deg(x):
    return f"${fmt(x, 1)}°$"


def qid(i):
    return f"trig-{i:03d}"


def graphic(angle_deg, labels, highlight, vtx=None):
    g = {"kind": "applied-triangle", "angleDeg": float(angle_deg), "labels": labels, "highlight": highlight}
    if vtx:
        g["vertexLabels"] = vtx
    return g


def build_question(i, statement, angle_deg, labels_q, labels_res, highlight_q, vertex_labels, options, correct_idx, resolution_steps):
    return {
        "id": qid(i),
        "statement": statement,
        "graphic": graphic(angle_deg, labels_q, highlight_q, vertex_labels),
        "options": options,
        "correct": correct_idx,
        "resolution": resolution_steps + [{"kind": "graphic", "graphic": graphic(angle_deg, labels_res, [], vertex_labels)}],
    }


def make_opts(correct, wrong, pos):
    opts = list(wrong)
    opts.insert(pos, correct)
    return opts[:4], pos


questions = []

# 1. Pal bandera inclinat (hipotenusa, pedir altura)
angle = 60
L = 8
h = L * math.sin(math.radians(angle))
statement = "Un pal d'una bandera de 8 m de longitud està recolzat formant un angle de 60° amb el terra. A quina alçada arriba l'extrem superior del pal?"
correct = fmt_m(h)
wrong = [fmt_m(L * math.cos(math.radians(angle))), fmt_m(L * math.tan(math.radians(angle))), fmt_m(L / math.sin(math.radians(angle)))]
opts, ci = make_opts(correct, wrong, 1)
res = [
    {"kind": "text", "text": "La hipotenusa és el pal (8 m) i l'alçada és el catet oposat a l'angle de 60°."},
    {"kind": "math", "tex": r"\sin(60°) = \dfrac{\text{alçada}}{\text{pal}}"},
    {"kind": "math", "tex": r"\text{alçada} = 8 \cdot \sin(60°) = 4\sqrt{3} \approx " + fmt(h) + r"\ \text{m}"},
]
questions.append(build_question(
    1, statement, angle,
    {"hypotenuse": "8 m", "opposite": "?", "angle": "60°"},
    {"hypotenuse": "8 m", "opposite": fmt(h) + " m", "angle": "60°"},
    ["opposite"], {"acuteAngle": "terra", "top": "extrem"}, opts, ci, res,
))

# 2. Escala — alçada
angle = 70
L = 5
h = L * math.sin(math.radians(angle))
statement = "Una escala de 5 m està recolzada contra una paret formant un angle de 70° amb el terra. Fins a quina alçada de la paret arriba l'escala?"
correct = fmt_m(h)
wrong = [fmt_m(L * math.cos(math.radians(angle))), fmt_m(L * math.tan(math.radians(angle))), fmt_m(L / math.sin(math.radians(angle)))]
opts, ci = make_opts(correct, wrong, 2)
res = [
    {"kind": "text", "text": "L'escala és la hipotenusa (5 m). L'alçada que busquem és el catet oposat a l'angle de 70°."},
    {"kind": "math", "tex": r"\sin(70°) = \dfrac{\text{alçada}}{5}"},
    {"kind": "math", "tex": r"\text{alçada} = 5 \cdot \sin(70°) \approx 5 \cdot 0{,}9397 \approx " + fmt(h) + r"\ \text{m}"},
]
questions.append(build_question(
    2, statement, angle,
    {"hypotenuse": "5 m", "opposite": "?", "angle": "70°"},
    {"hypotenuse": "5 m", "opposite": fmt(h) + " m", "angle": "70°"},
    ["opposite"], {"acuteAngle": "terra", "rightAngle": "peu", "top": "alt"}, opts, ci, res,
))

# 3. Escala — distància base
angle = 65
L = 6
d = L * math.cos(math.radians(angle))
h = L * math.sin(math.radians(angle))
statement = "Una escala de 6 m està recolzada en una paret formant un angle de 65° amb el terra. A quina distància del peu de la paret s'ha posat la base de l'escala?"
correct = fmt_m(d)
wrong = [fmt_m(h), fmt_m(L * math.tan(math.radians(angle))), fmt_m(L / math.cos(math.radians(angle)))]
opts, ci = make_opts(correct, wrong, 0)
res = [
    {"kind": "text", "text": "L'escala és la hipotenusa (6 m). La distància al peu de la paret és el catet contigu a l'angle de 65°."},
    {"kind": "math", "tex": r"\cos(65°) = \dfrac{\text{distància}}{6}"},
    {"kind": "math", "tex": r"\text{distància} = 6 \cdot \cos(65°) \approx 6 \cdot 0{,}4226 \approx " + fmt(d) + r"\ \text{m}"},
]
questions.append(build_question(
    3, statement, angle,
    {"hypotenuse": "6 m", "adjacent": "?", "angle": "65°"},
    {"hypotenuse": "6 m", "adjacent": fmt(d) + " m", "angle": "65°"},
    ["adjacent"], {"acuteAngle": "peu escala", "rightAngle": "paret", "top": "alt"}, opts, ci, res,
))

# 4. Tirolina (hipotenusa, pedir Δh)
angle = 25
L = 120
h = L * math.sin(math.radians(angle))
statement = "Una tirolina té 120 m de cable i baixa amb un pendent que forma un angle de 25° amb l'horitzontal. Quina és la diferència d'alçada entre el punt de sortida i el d'arribada?"
correct = fmt_m(h)
wrong = [fmt_m(L * math.cos(math.radians(angle))), fmt_m(L * math.tan(math.radians(angle))), fmt_m(L / math.sin(math.radians(angle)))]
opts, ci = make_opts(correct, wrong, 3)
res = [
    {"kind": "text", "text": "El cable és la hipotenusa (120 m). La diferència d'alçada és el catet oposat a l'angle de 25°."},
    {"kind": "math", "tex": r"\sin(25°) = \dfrac{\Delta h}{120}"},
    {"kind": "math", "tex": r"\Delta h = 120 \cdot \sin(25°) \approx 120 \cdot 0{,}4226 \approx " + fmt(h) + r"\ \text{m}"},
]
questions.append(build_question(
    4, statement, angle,
    {"hypotenuse": "120 m", "opposite": "?", "angle": "25°"},
    {"hypotenuse": "120 m", "opposite": fmt(h) + " m", "angle": "25°"},
    ["opposite"], {"acuteAngle": "arribada", "top": "sortida"}, opts, ci, res,
))

# 5. Teleféric — distància horitzontal
angle = 40
L = 300
d = L * math.cos(math.radians(angle))
h = L * math.sin(math.radians(angle))
statement = "Un teleféric puja amb un cable de 300 m de longitud que forma un angle de 40° amb l'horitzontal. Quina distància horitzontal es recorre?"
correct = fmt_m(d)
wrong = [fmt_m(h), fmt_m(L * math.tan(math.radians(angle))), fmt_m(L / math.cos(math.radians(angle)))]
opts, ci = make_opts(correct, wrong, 1)
res = [
    {"kind": "text", "text": "El cable és la hipotenusa (300 m). La distància horitzontal és el catet contigu a l'angle de 40°."},
    {"kind": "math", "tex": r"\cos(40°) = \dfrac{\text{horitzontal}}{300}"},
    {"kind": "math", "tex": r"\text{horitzontal} = 300 \cdot \cos(40°) \approx 300 \cdot 0{,}7660 \approx " + fmt(d) + r"\ \text{m}"},
]
questions.append(build_question(
    5, statement, angle,
    {"hypotenuse": "300 m", "adjacent": "?", "angle": "40°"},
    {"hypotenuse": "300 m", "adjacent": fmt(d) + " m", "angle": "40°"},
    ["adjacent"], {"acuteAngle": "base", "top": "cim"}, opts, ci, res,
))

# 6. Arbre i ombra
angle = 35
d = 12
h = d * math.tan(math.radians(angle))
L = d / math.cos(math.radians(angle))
statement = "Un arbre projecta una ombra de 12 m quan els raigs del sol formen un angle de 35° amb el terra. Quina és l'alçada de l'arbre?"
correct = fmt_m(h)
wrong = [fmt_m(d * math.sin(math.radians(angle))), fmt_m(d / math.tan(math.radians(angle))), fmt_m(L)]
opts, ci = make_opts(correct, wrong, 0)
res = [
    {"kind": "text", "text": "L'ombra (12 m) és el catet contigu a l'angle de 35°. Evitem la tangent: primer trobem la hipotenusa amb el cosinus i després l'alçada amb el sinus."},
    {"kind": "math", "tex": r"\cos(35°) = \dfrac{12}{L} \;\Rightarrow\; L = \dfrac{12}{\cos(35°)} \approx \dfrac{12}{0{,}8192} \approx 14{,}65\ \text{m}"},
    {"kind": "math", "tex": r"\text{arbre} = L \cdot \sin(35°) \approx 14{,}65 \cdot 0{,}5736 \approx " + fmt(h) + r"\ \text{m}"},
]
questions.append(build_question(
    6, statement, angle,
    {"adjacent": "12 m", "opposite": "?", "angle": "35°"},
    {"adjacent": "12 m", "opposite": fmt(h) + " m", "angle": "35°"},
    ["opposite"], {"acuteAngle": "sol", "rightAngle": "peu arbre", "top": "cim arbre"}, opts, ci, res,
))

# 7. Edifici amb angle elevació (adjacent conocido, pedir altura)
angle = 52
d = 40
h = d * math.tan(math.radians(angle))
statement = "Des d'un punt del terra, l'angle d'elevació fins al cim d'un edifici és de 52°. Si el punt està a 40 m de la base de l'edifici, quina alçada té l'edifici?"
correct = fmt_m(h)
wrong = [fmt_m(d * math.sin(math.radians(angle))), fmt_m(d / math.tan(math.radians(angle))), fmt_m(d * math.cos(math.radians(angle)))]
opts, ci = make_opts(correct, wrong, 1)
res = [
    {"kind": "text", "text": "La distància al peu (40 m) és el catet contigu a l'angle. Trobem primer la hipotenusa (línia de visió) amb el cosinus i després l'alçada amb el sinus."},
    {"kind": "math", "tex": r"\cos(52°) = \dfrac{40}{L} \;\Rightarrow\; L = \dfrac{40}{\cos(52°)} \approx \dfrac{40}{0{,}6157} \approx 64{,}97\ \text{m}"},
    {"kind": "math", "tex": r"h = L \cdot \sin(52°) \approx 64{,}97 \cdot 0{,}7880 \approx " + fmt(h) + r"\ \text{m}"},
]
questions.append(build_question(
    7, statement, angle,
    {"adjacent": "40 m", "opposite": "?", "angle": "52°"},
    {"adjacent": "40 m", "opposite": fmt(h) + " m", "angle": "52°"},
    ["opposite"], {"acuteAngle": "observador", "rightAngle": "base", "top": "cim"}, opts, ci, res,
))

# 8. Rampa — longitud (opposite conegut, pedir hipotenusa)
angle = 15
h = 1.2
L = h / math.sin(math.radians(angle))
d = h / math.tan(math.radians(angle))
statement = "Una rampa d'accés salva un desnivell d'1,2 m amb una inclinació de 15° respecte a l'horitzontal. Quina longitud té la rampa?"
correct = fmt_m(L)
wrong = [fmt_m(h * math.sin(math.radians(angle))), fmt_m(d), fmt_m(h / math.cos(math.radians(angle)))]
opts, ci = make_opts(correct, wrong, 2)
res = [
    {"kind": "text", "text": "El desnivell (1,2 m) és el catet oposat a l'angle de 15°. La longitud de la rampa és la hipotenusa."},
    {"kind": "math", "tex": r"\sin(15°) = \dfrac{1{,}2}{L}"},
    {"kind": "math", "tex": r"L = \dfrac{1{,}2}{\sin(15°)} \approx \dfrac{1{,}2}{0{,}2588} \approx " + fmt(L) + r"\ \text{m}"},
]
questions.append(build_question(
    8, statement, angle,
    {"opposite": "1,2 m", "hypotenuse": "?", "angle": "15°"},
    {"opposite": "1,2 m", "hypotenuse": fmt(L) + " m", "angle": "15°"},
    ["hypotenuse"], {"acuteAngle": "inici", "rightAngle": "peu", "top": "final"}, opts, ci, res,
))

# 9. Estel/cometa
angle = 50
h = 25
L = h / math.sin(math.radians(angle))
d = h / math.tan(math.radians(angle))
statement = "Una persona fa volar un estel que està a 25 m d'alçada. El fil forma un angle de 50° amb el terra. Quina és la longitud del fil (suposant que està tens i recte)?"
correct = fmt_m(L)
wrong = [fmt_m(h * math.sin(math.radians(angle))), fmt_m(d), fmt_m(h * math.cos(math.radians(angle)))]
opts, ci = make_opts(correct, wrong, 3)
res = [
    {"kind": "text", "text": "L'alçada (25 m) és el catet oposat a l'angle de 50°. El fil és la hipotenusa."},
    {"kind": "math", "tex": r"\sin(50°) = \dfrac{25}{L}"},
    {"kind": "math", "tex": r"L = \dfrac{25}{\sin(50°)} \approx \dfrac{25}{0{,}7660} \approx " + fmt(L) + r"\ \text{m}"},
]
questions.append(build_question(
    9, statement, angle,
    {"opposite": "25 m", "hypotenuse": "?", "angle": "50°"},
    {"opposite": "25 m", "hypotenuse": fmt(L) + " m", "angle": "50°"},
    ["hypotenuse"], {"acuteAngle": "persona", "top": "estel"}, opts, ci, res,
))

# 10. Cable antena
angle = 55
h = 18
L = h / math.sin(math.radians(angle))
d = h / math.tan(math.radians(angle))
statement = "Un cable tensor subjecta una antena pel seu extrem superior, situat a 18 m d'alçada. El cable arriba al terra formant un angle de 55° amb l'horitzontal. Quina és la longitud del cable?"
correct = fmt_m(L)
wrong = [fmt_m(d), fmt_m(h * math.sin(math.radians(angle))), fmt_m(h / math.cos(math.radians(angle)))]
opts, ci = make_opts(correct, wrong, 0)
res = [
    {"kind": "text", "text": "L'alçada de l'antena (18 m) és el catet oposat a l'angle i el cable és la hipotenusa."},
    {"kind": "math", "tex": r"\sin(55°) = \dfrac{18}{L}"},
    {"kind": "math", "tex": r"L = \dfrac{18}{\sin(55°)} \approx \dfrac{18}{0{,}8192} \approx " + fmt(L) + r"\ \text{m}"},
]
questions.append(build_question(
    10, statement, angle,
    {"opposite": "18 m", "hypotenuse": "?", "angle": "55°"},
    {"opposite": "18 m", "hypotenuse": fmt(L) + " m", "angle": "55°"},
    ["hypotenuse"], {"acuteAngle": "ancoratge", "rightAngle": "peu antena", "top": "cim antena"}, opts, ci, res,
))

# 11. Far (opposite, pedir adjacent)
angle = 8
h = 45
d = h / math.tan(math.radians(angle))
L = h / math.sin(math.radians(angle))
statement = "Des d'un vaixell, s'observa el capdamunt d'un far a 45 m d'alçada amb un angle d'elevació de 8°. A quina distància horitzontal es troba el vaixell del far?"
correct = fmt_m(d)
wrong = [fmt_m(L), fmt_m(h * math.tan(math.radians(angle))), fmt_m(h * math.cos(math.radians(angle)))]
opts, ci = make_opts(correct, wrong, 1)
res = [
    {"kind": "text", "text": "L'alçada del far (45 m) és el catet oposat a l'angle de 8°. Trobem primer la línia de visió (hipotenusa) amb el sinus i després la distància horitzontal amb el cosinus."},
    {"kind": "math", "tex": r"\sin(8°) = \dfrac{45}{L} \;\Rightarrow\; L = \dfrac{45}{\sin(8°)} \approx \dfrac{45}{0{,}1392} \approx 323{,}31\ \text{m}"},
    {"kind": "math", "tex": r"d = L \cdot \cos(8°) \approx 323{,}31 \cdot 0{,}9903 \approx " + fmt(d) + r"\ \text{m}"},
]
questions.append(build_question(
    11, statement, angle,
    {"opposite": "45 m", "adjacent": "?", "angle": "8°"},
    {"opposite": "45 m", "adjacent": fmt(d) + " m", "angle": "8°"},
    ["adjacent"], {"acuteAngle": "vaixell", "rightAngle": "peu far", "top": "far"}, opts, ci, res,
))

# 12. Avió
angle = 12
d = 5000
h = d * math.tan(math.radians(angle))
statement = "Un avió segueix una trajectòria d'enlairament amb un angle constant de 12°. Quan ha recorregut 5000 m en horitzontal, a quina alçada es troba?"
correct = fmt_m(h)
wrong = [fmt_m(d * math.sin(math.radians(angle))), fmt_m(d / math.tan(math.radians(angle))), fmt_m(d / math.cos(math.radians(angle)))]
opts, ci = make_opts(correct, wrong, 2)
res = [
    {"kind": "text", "text": "La distància horitzontal (5000 m) és el catet contigu a l'angle de 12°. Trobem primer la trajectòria (hipotenusa) amb el cosinus i després l'alçada amb el sinus."},
    {"kind": "math", "tex": r"\cos(12°) = \dfrac{5000}{L} \;\Rightarrow\; L = \dfrac{5000}{\cos(12°)} \approx \dfrac{5000}{0{,}9781} \approx 5111{,}87\ \text{m}"},
    {"kind": "math", "tex": r"h = L \cdot \sin(12°) \approx 5111{,}87 \cdot 0{,}2079 \approx " + fmt(h) + r"\ \text{m}"},
]
questions.append(build_question(
    12, statement, angle,
    {"adjacent": "5000 m", "opposite": "?", "angle": "12°"},
    {"adjacent": "5000 m", "opposite": fmt(h) + " m", "angle": "12°"},
    ["opposite"], {"acuteAngle": "pista", "top": "avió"}, opts, ci, res,
))

# 13. Tobogán
angle = 45
L = 4
h = L * math.sin(math.radians(angle))
statement = "Un tobogán d'un parc infantil fa 4 m de llarg i està inclinat 45° respecte al terra. Quina alçada té el punt més alt del tobogán?"
correct = fmt_m(h)
wrong = [fmt_m(L), fmt_m(L / 2), fmt_m(L / math.sin(math.radians(angle)))]
opts, ci = make_opts(correct, wrong, 3)
res = [
    {"kind": "text", "text": "El tobogán és la hipotenusa (4 m). L'alçada és el catet oposat a l'angle de 45°."},
    {"kind": "math", "tex": r"\sin(45°) = \dfrac{h}{4}"},
    {"kind": "math", "tex": r"h = 4 \cdot \sin(45°) = 2\sqrt{2} \approx " + fmt(h) + r"\ \text{m}"},
]
questions.append(build_question(
    13, statement, angle,
    {"hypotenuse": "4 m", "opposite": "?", "angle": "45°"},
    {"hypotenuse": "4 m", "opposite": fmt(h) + " m", "angle": "45°"},
    ["opposite"], {"acuteAngle": "peu", "top": "dalt"}, opts, ci, res,
))

# 14. Rampa camió
angle = 20
L = 3
h = L * math.sin(math.radians(angle))
statement = "La rampa de càrrega d'un camió fa 3 m de llarg i està inclinada 20°. Quina és l'alçada del remolc des del terra?"
correct = fmt_m(h)
wrong = [fmt_m(L * math.cos(math.radians(angle))), fmt_m(L * math.tan(math.radians(angle))), fmt_m(L / math.sin(math.radians(angle)))]
opts, ci = make_opts(correct, wrong, 0)
res = [
    {"kind": "text", "text": "La rampa és la hipotenusa (3 m). L'alçada del remolc és el catet oposat a l'angle de 20°."},
    {"kind": "math", "tex": r"\sin(20°) = \dfrac{h}{3}"},
    {"kind": "math", "tex": r"h = 3 \cdot \sin(20°) \approx 3 \cdot 0{,}3420 \approx " + fmt(h) + r"\ \text{m}"},
]
questions.append(build_question(
    14, statement, angle,
    {"hypotenuse": "3 m", "opposite": "?", "angle": "20°"},
    {"hypotenuse": "3 m", "opposite": fmt(h) + " m", "angle": "20°"},
    ["opposite"], {"acuteAngle": "terra", "top": "remolc"}, opts, ci, res,
))

# 15. Funicular
angle = 30
L = 200
d = L * math.cos(math.radians(angle))
h = L * math.sin(math.radians(angle))
statement = "Un funicular recorre 200 m sobre un pendent de 30°. Quina distància horitzontal avança?"
correct = fmt_m(d)
wrong = [fmt_m(h), fmt_m(L * math.tan(math.radians(angle))), fmt_m(L / math.cos(math.radians(angle)))]
opts, ci = make_opts(correct, wrong, 1)
res = [
    {"kind": "text", "text": "La via del funicular és la hipotenusa (200 m). La distància horitzontal és el catet contigu a l'angle."},
    {"kind": "math", "tex": r"\cos(30°) = \dfrac{d}{200}"},
    {"kind": "math", "tex": r"d = 200 \cdot \cos(30°) = 100\sqrt{3} \approx " + fmt(d) + r"\ \text{m}"},
]
questions.append(build_question(
    15, statement, angle,
    {"hypotenuse": "200 m", "adjacent": "?", "angle": "30°"},
    {"hypotenuse": "200 m", "adjacent": fmt(d) + " m", "angle": "30°"},
    ["adjacent"], {"acuteAngle": "base", "top": "cim"}, opts, ci, res,
))

# 16. Rampa — angle (arcsin)
h = 1.5
L = 10
angle = math.degrees(math.asin(h / L))
statement = "Una rampa fa 10 m de llarg i salva un desnivell d'1,5 m. Quin angle forma la rampa amb l'horitzontal?"
correct = fmt_deg(angle)
wrong = [fmt_deg(math.degrees(math.acos(h / L))), fmt_deg(math.degrees(math.atan(h / L))), fmt_deg(math.degrees(math.atan(L / h)))]
opts, ci = make_opts(correct, wrong, 2)
res = [
    {"kind": "text", "text": "Coneixem el catet oposat (1,5 m) i la hipotenusa (10 m). Utilitzem el sinus."},
    {"kind": "math", "tex": r"\sin(\alpha) = \dfrac{1{,}5}{10} = 0{,}15"},
    {"kind": "math", "tex": r"\alpha = \arcsin(0{,}15) \approx " + fmt(angle, 1) + r"°"},
]
questions.append(build_question(
    16, statement, angle,
    {"opposite": "1,5 m", "hypotenuse": "10 m", "angle": "?"},
    {"opposite": "1,5 m", "hypotenuse": "10 m", "angle": fmt(angle, 1) + "°"},
    [], {"acuteAngle": "inici", "top": "final"}, opts, ci, res,
))

# 17. Edifici — arctan
h = 30
d = 40
angle = math.degrees(math.atan(h / d))
L = math.sqrt(h * h + d * d)
statement = "Un edifici de 30 m d'alçada s'observa des d'un punt situat a 40 m de la seva base. Quin és l'angle d'elevació des del punt fins al cim de l'edifici?"
correct = fmt_deg(angle)
wrong = [fmt_deg(math.degrees(math.atan(d / h))), fmt_deg(math.degrees(math.asin(h / d))), fmt_deg(90 - angle + 5)]
opts, ci = make_opts(correct, wrong, 0)
res = [
    {"kind": "text", "text": "Coneixem els dos catets (30 m i 40 m). Trobem primer la hipotenusa amb el teorema de Pitàgores i després l'angle amb el sinus."},
    {"kind": "math", "tex": r"L = \sqrt{30^2 + 40^2} = \sqrt{900 + 1600} = \sqrt{2500} = 50\ \text{m}"},
    {"kind": "math", "tex": r"\sin(\alpha) = \dfrac{30}{50} = 0{,}6 \;\Rightarrow\; \alpha = \arcsin(0{,}6) \approx " + fmt(angle, 1) + r"°"},
]
questions.append(build_question(
    17, statement, angle,
    {"opposite": "30 m", "adjacent": "40 m", "angle": "?"},
    {"opposite": "30 m", "adjacent": "40 m", "angle": fmt(angle, 1) + "°"},
    [], {"acuteAngle": "observador", "top": "cim"}, opts, ci, res,
))

# 18. Escala — arccos
L = 4
d = 1.5
angle = math.degrees(math.acos(d / L))
statement = "Una escala de 4 m recolzada a una paret té el peu a 1,5 m de la paret. Quin angle forma l'escala amb el terra?"
correct = fmt_deg(angle)
wrong = [fmt_deg(math.degrees(math.asin(d / L))), fmt_deg(math.degrees(math.atan(d / L))), fmt_deg(90 - angle + 10)]
opts, ci = make_opts(correct, wrong, 3)
res = [
    {"kind": "text", "text": "Coneixem el catet contigu (1,5 m) i la hipotenusa (4 m). Utilitzem el cosinus."},
    {"kind": "math", "tex": r"\cos(\alpha) = \dfrac{1{,}5}{4} = 0{,}375"},
    {"kind": "math", "tex": r"\alpha = \arccos(0{,}375) \approx " + fmt(angle, 1) + r"°"},
]
questions.append(build_question(
    18, statement, angle,
    {"adjacent": "1,5 m", "hypotenuse": "4 m", "angle": "?"},
    {"adjacent": "1,5 m", "hypotenuse": "4 m", "angle": fmt(angle, 1) + "°"},
    [], {"acuteAngle": "terra", "rightAngle": "paret"}, opts, ci, res,
))

# 19. Pendent 8% — arctan
tan_val = 0.08
angle = math.degrees(math.atan(tan_val))
statement = "Un tram de carretera té un pendent del 8%, que significa que per cada 100 m en horitzontal puja 8 m. Quin angle forma aquest tram amb l'horitzontal?"
correct = fmt_deg(angle)
wrong = [fmt_deg(8), fmt_deg(math.degrees(math.atan(tan_val * 10))), fmt_deg(45)]
opts, ci = make_opts(correct, wrong, 1)
res = [
    {"kind": "text", "text": "Un 8% de pendent vol dir 8 m d'alçada per cada 100 m en horitzontal. Trobem primer la hipotenusa amb Pitàgores i després l'angle amb el sinus."},
    {"kind": "math", "tex": r"L = \sqrt{100^2 + 8^2} = \sqrt{10000 + 64} = \sqrt{10064} \approx 100{,}32\ \text{m}"},
    {"kind": "math", "tex": r"\sin(\alpha) = \dfrac{8}{100{,}32} \approx 0{,}0797 \;\Rightarrow\; \alpha = \arcsin(0{,}0797) \approx " + fmt(angle, 1) + r"°"},
]
questions.append(build_question(
    19, statement, angle,
    {"opposite": "8 m", "adjacent": "100 m", "angle": "?"},
    {"opposite": "8 m", "adjacent": "100 m", "angle": fmt(angle, 1) + "°"},
    [], {"acuteAngle": "inici", "top": "puja"}, opts, ci, res,
))

# 20. Cable tensor — arcsin
h = 12
L = 20
angle = math.degrees(math.asin(h / L))
statement = "Un cable tensor de 20 m subjecta el capdamunt d'un pal situat a 12 m d'alçada. Quin angle forma el cable amb el terra?"
correct = fmt_deg(angle)
wrong = [fmt_deg(math.degrees(math.acos(h / L))), fmt_deg(math.degrees(math.atan(h / L))), fmt_deg(90 - angle + 5)]
opts, ci = make_opts(correct, wrong, 0)
res = [
    {"kind": "text", "text": "L'alçada (12 m) és el catet oposat i el cable (20 m) és la hipotenusa. Utilitzem el sinus."},
    {"kind": "math", "tex": r"\sin(\alpha) = \dfrac{12}{20} = 0{,}6"},
    {"kind": "math", "tex": r"\alpha = \arcsin(0{,}6) \approx " + fmt(angle, 1) + r"°"},
]
questions.append(build_question(
    20, statement, angle,
    {"opposite": "12 m", "hypotenuse": "20 m", "angle": "?"},
    {"opposite": "12 m", "hypotenuse": "20 m", "angle": fmt(angle, 1) + "°"},
    [], {"acuteAngle": "ancoratge", "rightAngle": "peu pal", "top": "cim pal"}, opts, ci, res,
))

# 21. Depressió
angle = 28
h = 60
d = h / math.tan(math.radians(angle))
statement = "Des d'una torre de vigilància de 60 m d'alçada, un vigilant observa un cotxe amb un angle de depressió de 28°. A quina distància horitzontal del peu de la torre es troba el cotxe?"
correct = fmt_m(d)
wrong = [fmt_m(h * math.tan(math.radians(angle))), fmt_m(h / math.sin(math.radians(angle))), fmt_m(h * math.cos(math.radians(angle)))]
opts, ci = make_opts(correct, wrong, 2)
res = [
    {"kind": "text", "text": "L'angle de depressió des de dalt coincideix amb l'angle d'elevació des del cotxe (angles alterns). L'alçada de la torre (60 m) és el catet oposat a 28°. Trobem primer la línia de visió amb el sinus i després la distància horitzontal amb el cosinus."},
    {"kind": "math", "tex": r"\sin(28°) = \dfrac{60}{L} \;\Rightarrow\; L = \dfrac{60}{\sin(28°)} \approx \dfrac{60}{0{,}4695} \approx 127{,}80\ \text{m}"},
    {"kind": "math", "tex": r"d = L \cdot \cos(28°) \approx 127{,}80 \cdot 0{,}8829 \approx " + fmt(d) + r"\ \text{m}"},
]
questions.append(build_question(
    21, statement, angle,
    {"opposite": "60 m", "adjacent": "?", "angle": "28°"},
    {"opposite": "60 m", "adjacent": fmt(d) + " m", "angle": "28°"},
    ["adjacent"], {"acuteAngle": "cotxe", "rightAngle": "peu torre", "top": "vigilant"}, opts, ci, res,
))

# 22. Pal bandera (exemple usuari)
angle = 60
h = 5
L = h / math.sin(math.radians(angle))
d = h / math.tan(math.radians(angle))
statement = "La bandera d'una ambaixada està hissada en un pal que forma un angle de 60° amb el terra. Si l'extrem del pal està a 5 m d'alçada, calcula la longitud del pal."
correct = fmt_m(L)
wrong = [fmt_m(h * math.sin(math.radians(angle))), fmt_m(h), fmt_m(d)]
opts, ci = make_opts(correct, wrong, 1)
res = [
    {"kind": "text", "text": "L'alçada (5 m) és el catet oposat a l'angle de 60°. La longitud del pal és la hipotenusa."},
    {"kind": "math", "tex": r"\sin(60°) = \dfrac{5}{L}"},
    {"kind": "math", "tex": r"L = \dfrac{5}{\sin(60°)} = \dfrac{5}{\frac{\sqrt{3}}{2}} = \dfrac{10\sqrt{3}}{3} \approx " + fmt(L) + r"\ \text{m}"},
]
questions.append(build_question(
    22, statement, angle,
    {"opposite": "5 m", "hypotenuse": "?", "angle": "60°"},
    {"opposite": "5 m", "hypotenuse": fmt(L) + " m", "angle": "60°"},
    ["hypotenuse"], {"acuteAngle": "base", "rightAngle": "terra", "top": "extrem"}, opts, ci, res,
))

# 23. Cinta transportadora
angle = 22
L = 8
d = L * math.cos(math.radians(angle))
h = L * math.sin(math.radians(angle))
statement = "Una cinta transportadora de 8 m fa un angle de 22° amb el terra. Quina distància horitzontal cobreix?"
correct = fmt_m(d)
wrong = [fmt_m(h), fmt_m(L * math.tan(math.radians(angle))), fmt_m(L / math.cos(math.radians(angle)))]
opts, ci = make_opts(correct, wrong, 0)
res = [
    {"kind": "text", "text": "La cinta és la hipotenusa (8 m). La distància horitzontal és el catet contigu a l'angle."},
    {"kind": "math", "tex": r"\cos(22°) = \dfrac{d}{8}"},
    {"kind": "math", "tex": r"d = 8 \cdot \cos(22°) \approx 8 \cdot 0{,}9272 \approx " + fmt(d) + r"\ \text{m}"},
]
questions.append(build_question(
    23, statement, angle,
    {"hypotenuse": "8 m", "adjacent": "?", "angle": "22°"},
    {"hypotenuse": "8 m", "adjacent": fmt(d) + " m", "angle": "22°"},
    ["adjacent"], {"acuteAngle": "entrada", "top": "sortida"}, opts, ci, res,
))

# 24. Muntanya — arctan
h = 750
d = 1200
angle = math.degrees(math.atan(h / d))
statement = "Una muntanya té 750 m d'alçada. Un excursionista es troba a 1200 m en horitzontal del centre de la muntanya. Amb quin angle d'elevació veu el cim?"
correct = fmt_deg(angle)
wrong = [fmt_deg(math.degrees(math.atan(d / h))), fmt_deg(math.degrees(math.asin(h / d))), fmt_deg(45)]
opts, ci = make_opts(correct, wrong, 1)
res = [
    {"kind": "text", "text": "Coneixem els dos catets: l'alçada de la muntanya (750 m) i la distància horitzontal (1200 m). Trobem primer la línia de visió amb Pitàgores i després l'angle amb el sinus."},
    {"kind": "math", "tex": r"L = \sqrt{1200^2 + 750^2} = \sqrt{1\,440\,000 + 562\,500} = \sqrt{2\,002\,500} \approx 1414{,}96\ \text{m}"},
    {"kind": "math", "tex": r"\sin(\alpha) = \dfrac{750}{1414{,}96} \approx 0{,}5301 \;\Rightarrow\; \alpha = \arcsin(0{,}5301) \approx " + fmt(angle, 1) + r"°"},
]
questions.append(build_question(
    24, statement, angle,
    {"opposite": "750 m", "adjacent": "1200 m", "angle": "?"},
    {"opposite": "750 m", "adjacent": "1200 m", "angle": fmt(angle, 1) + "°"},
    [], {"acuteAngle": "excursionista", "top": "cim"}, opts, ci, res,
))

# 25. Globus aerostàtic
angle = 38
h = 90
L = h / math.sin(math.radians(angle))
d = h / math.tan(math.radians(angle))
statement = "Un globus aerostàtic està lligat al terra per una corda tensa. El globus es troba a 90 m d'alçada i la corda forma un angle de 38° amb el terra. Quina és la longitud de la corda?"
correct = fmt_m(L)
wrong = [fmt_m(d), fmt_m(h * math.sin(math.radians(angle))), fmt_m(h / math.cos(math.radians(angle)))]
opts, ci = make_opts(correct, wrong, 3)
res = [
    {"kind": "text", "text": "L'alçada (90 m) és el catet oposat a l'angle de 38° i la corda és la hipotenusa."},
    {"kind": "math", "tex": r"\sin(38°) = \dfrac{90}{L}"},
    {"kind": "math", "tex": r"L = \dfrac{90}{\sin(38°)} \approx \dfrac{90}{0{,}6157} \approx " + fmt(L) + r"\ \text{m}"},
]
questions.append(build_question(
    25, statement, angle,
    {"opposite": "90 m", "hypotenuse": "?", "angle": "38°"},
    {"opposite": "90 m", "hypotenuse": fmt(L) + " m", "angle": "38°"},
    ["hypotenuse"], {"acuteAngle": "ancoratge", "top": "globus"}, opts, ci, res,
))

assert len(questions) == 25

# Verifica que no hi hagi opcions duplicades dins d'una pregunta
for q in questions:
    assert len(set(q["options"])) == 4, f"Duplicats a {q['id']}: {q['options']}"
    assert 0 <= q["correct"] < 4

topic = {
    "id": "applied-right-triangles",
    "name": "Problemes de triangles rectangles",
    "description": "Problemes aplicats de trigonometria (pals, escales, rampes, ombres, angles d'elevació i depressió).",
    "questions": questions,
}

OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(json.dumps(topic, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"Escrit {OUT} amb {len(questions)} preguntes")
