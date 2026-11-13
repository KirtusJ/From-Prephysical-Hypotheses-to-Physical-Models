"""Draw the one-page program-scope figure as matching vector PDF and SVG.

Run with Python from any working directory. Use --output to select a new output directory; otherwise the outputs go
in Rebuilt_Program_Diagram next to this source directory. ReportLab and matplotlib are the only dependencies.
All positions and line wrapping are shared between the PDF and SVG renderers.
The SVG embeds its fonts and does not require a network connection.
"""
from __future__ import annotations

import argparse
import base64
import html
from pathlib import Path

from matplotlib import font_manager
from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import A4, landscape
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas


OUT = Path(__file__).resolve().parent.parent
STEM = "Program_Questions_Models_and_Physical_Correspondence"
WIDTH, HEIGHT = landscape(A4)
MARGIN = 28.0
CONTENT = WIDTH - 2 * MARGIN
FONT_FILES = {
    "Body": Path(font_manager.findfont(font_manager.FontProperties(family="DejaVu Sans"))),
    "Bold": Path(font_manager.findfont(font_manager.FontProperties(family="DejaVu Sans", weight="bold"))),
}
for name, path in FONT_FILES.items():
    pdfmetrics.registerFont(TTFont("Scope" + name, str(path)))

INK = "#172b3a"
MUTED = "#435568"
BLUE = "#245a7b"
AMBER = "#91601c"
RULE = "#c6d0d8"
PALE = "#f5f8fa"
WARM = "#fcf8ef"
WHITE = "#ffffff"
scene: list[dict] = []
checks: list[dict] = []


def rect(x, y, w, h, fill=WHITE, stroke=RULE, radius=4, sw=0.7):
    scene.append(dict(kind="rect", x=x, y=y, w=w, h=h, fill=fill, stroke=stroke, radius=radius, sw=sw))


def line(x1, y1, x2, y2, color=RULE, sw=0.7):
    scene.append(dict(kind="line", x1=x1, y1=y1, x2=x2, y2=y2, color=color, sw=sw))


def wrap(text, width, size, face="Body"):
    result = []
    for paragraph in text.split("\n"):
        current = ""
        for word in paragraph.split():
            trial = current + (" " if current else "") + word
            if current and pdfmetrics.stringWidth(trial, "Scope" + face, size) > width:
                result.append(current)
                current = word
            else:
                current = trial
        result.append(current)
    return result


def text(x, y, w, value, size=9.5, face="Body", color=INK, leading=None, max_height=None):
    leading = leading or size * 1.22
    lines = wrap(value, w, size, face)
    ascent = pdfmetrics.getAscent("Scope" + face) * size / 1000
    descent = abs(pdfmetrics.getDescent("Scope" + face)) * size / 1000
    used = ascent + descent + (len(lines) - 1) * leading
    if max_height is not None and used > max_height + 0.1:
        raise ValueError(f"Text exceeds its box: {value!r}: {used:.2f} > {max_height:.2f}")
    for index, value_line in enumerate(lines):
        width = pdfmetrics.stringWidth(value_line, "Scope" + face, size)
        if width > w + 0.1:
            raise ValueError(f"Unbreakable line exceeds width: {value_line!r}")
        text_y = y + ascent + index * leading
        scene.append(dict(kind="text", x=x, text_y=text_y, value=value_line, face=face, size=size, color=color))
        checks.append(dict(text=value_line, x=x, y=y + index * leading, width=width, bottom=text_y + descent))
    return used


def arrow(x1, x2, y):
    line(x1, y, x2 - 4.5, y, BLUE, 1.1)
    scene.append(dict(kind="polygon", points=[(x2, y), (x2 - 5.5, y - 3.1), (x2 - 5.5, y + 3.1)], fill=BLUE))


def build_scene():
    text(MARGIN, 22, CONTENT, "From Prephysical Hypotheses to Physical Models", 20.0, "Bold")
    text(MARGIN, 49, CONTENT, "Program questions, mathematical models and physical correspondence", 12.0, color=MUTED)
    line(MARGIN, 71, WIDTH - MARGIN, 71, RULE, 0.8)

    text(MARGIN, 82, CONTENT, "RESEARCH QUESTIONS", 9.1, "Bold", BLUE)
    gap = 12
    card_w = (CONTENT - 2 * gap) / 3
    questions = [
        ("Specify", "What primitives, relations and equivalences can be defined without assuming the physical structure being sought?"),
        ("Derive and challenge", "Which conclusions follow from stated assumptions, and which proposed implications fail?"),
        ("Discriminate", "Which observations distinguish candidate models when calibration and uncertainty are included?"),
    ]
    for i, (title, body) in enumerate(questions):
        x = MARGIN + i * (card_w + gap)
        rect(x, 98, card_w, 65, PALE)
        text(x + 11, 107, card_w - 22, title, 10.6, "Bold")
        text(x + 11, 124, card_w - 22, body, 9.1, max_height=34)

    text(MARGIN, 176, CONTENT, "PARALLEL MATHEMATICAL APPROACHES", 9.1, "Bold", BLUE)
    text(MARGIN + 300, 176, CONTENT - 300, "Each row retains its own assumptions and scope.", 8.6, color=MUTED)
    c1, c2, c3 = MARGIN + 11, 211, 532
    w1, w2, w3 = 151, 282, WIDTH - MARGIN - 11 - 532
    text(c1, 192, w1, "APPROACH", 7.7, "Bold", MUTED)
    text(c2, 192, w2, "MATHEMATICAL SETTING", 7.7, "Bold", MUTED)
    text(c3, 192, w3, "STATEMENTS AND LIMITS", 7.7, "Bold", MUTED)
    rows = [
        ("Signed-sector signal proposal", "ONE EXPLORATORY OPTION", "Proposed sectors and a relation, without assigned physical frequency. Mathematical types remain to be specified.", "Geometry and a continuum are proposed targets. The sketch supplies no construction or observation law.", False),
        ("Finite relational models", "CONDITIONAL MATHEMATICS", "Finite positive-arity signature; nonempty finite structures; ordinary homomorphisms and homomorphic equivalence.", "Each equivalence class has a core unique up to isomorphism. Quotienting can discard multiplicity.", True),
        ("State/effect and instrument models", "MATHEMATICAL REPRESENTATIONS", "Hilbert spaces, completely positive maps or stochastic kernels are mathematical choices with explicit observation rules.", "Conditional output laws, instrument bounds and comparison models. Physical realization needs separate warrant.", False),
        ("Identification and information", "EXPERIMENT-RELATIVE ANALYSIS", "Declared model class, experiment menu and outcome-law map; separate resource and statistical contracts.", "Identified properties are constant on observation fibers. Information and testing bounds keep their extra premises.", True),
        ("Analytic and effective models", "MODEL-SPECIFIC ANALYSIS", "Chosen operators, transfer kernels, interaction laws and limiting regimes.", "Spectral, entropy and continuum estimates retain their analytic hypotheses and unresolved extensions.", False),
    ]
    start, row_h, row_gap = 207, 47, 4
    for i, (title, status, premises, result, implication) in enumerate(rows):
        y = start + i * (row_h + row_gap)
        rect(MARGIN, y, CONTENT, row_h, WARM if i == 0 else WHITE)
        title_h = text(c1, y + 7, w1, title, 9.3, "Bold", max_height=24)
        text(c1, y + 10 + title_h, w1, status, 6.25, "Bold", AMBER if i == 0 else MUTED, max_height=10)
        text(c2, y + 7, w2, premises, 9.0, max_height=row_h - 13)
        text(c3, y + 7, w3, result, 9.0, max_height=row_h - 13)
        if implication:
            arrow(503, 520, y + row_h / 2)

    panel_y = 474
    rect(MARGIN, panel_y, CONTENT, 75, PALE, BLUE, sw=0.8)
    text(MARGIN + 11, panel_y + 9, CONTENT - 22,
         "PHYSICAL CORRESPONDENCE: WHAT WOULD WARRANT A PHYSICAL INTERPRETATION?", 9.0, "Bold", BLUE)
    obligations = [
        ("Map the representation", "Relate mathematical states, transformations and effects to preparations, controls and observations."),
        ("Justify physical quantities", "Supply units, clocks, energy, geometry and composition where those physical claims are made."),
        ("Test discriminating predictions", "State alternatives, calibration and uncertainty; obtain observations that distinguish the proposed models."),
    ]
    for i, (title, body) in enumerate(obligations):
        x = MARGIN + 11 + i * (card_w + gap)
        text(x, panel_y + 28, card_w - 22, title, 9.1, "Bold")
        text(x, panel_y + 43, card_w - 22, body, 8.5, max_height=25)

    text(MARGIN, 559, CONTENT,
         "Arrows mark conditional mathematical implications. Grouping indicates a research topic, not causal propagation or physical emergence.",
         8.2, color=MUTED, max_height=13)
    text(MARGIN, 575, CONTENT,
         "The figure organizes selected research lines; it does not assert one completed physical theory or a unique ontology.",
         8.2, color=MUTED, max_height=13)

    for item in checks:
        assert item["x"] >= MARGIN - 0.1
        assert item["x"] + item["width"] <= WIDTH - MARGIN + 0.1
        assert item["y"] >= 0 and item["bottom"] <= HEIGHT - 7


def render_pdf(path):
    cv = canvas.Canvas(str(path), pagesize=(WIDTH, HEIGHT), pageCompression=1)
    cv.setAuthor("Kirtus Justus")
    cv.setTitle("Program Questions, Mathematical Models and Physical Correspondence")
    cv.setSubject("Scope of From Prephysical Hypotheses to Physical Models")
    for obj in scene:
        kind = obj["kind"]
        if kind == "rect":
            cv.setFillColor(HexColor(obj["fill"]))
            cv.setStrokeColor(HexColor(obj["stroke"]))
            cv.setLineWidth(obj["sw"])
            cv.roundRect(obj["x"], HEIGHT - obj["y"] - obj["h"], obj["w"], obj["h"], obj["radius"], fill=1, stroke=1)
        elif kind == "line":
            cv.setStrokeColor(HexColor(obj["color"]))
            cv.setLineWidth(obj["sw"])
            cv.line(obj["x1"], HEIGHT - obj["y1"], obj["x2"], HEIGHT - obj["y2"])
        elif kind == "polygon":
            cv.setFillColor(HexColor(obj["fill"]))
            p = cv.beginPath()
            for i, (x, y) in enumerate(obj["points"]):
                (p.moveTo if i == 0 else p.lineTo)(x, HEIGHT - y)
            p.close()
            cv.drawPath(p, fill=1, stroke=0)
        elif kind == "text":
            cv.setFillColor(HexColor(obj["color"]))
            cv.setFont("Scope" + obj["face"], obj["size"])
            cv.drawString(obj["x"], HEIGHT - obj["text_y"], obj["value"])
    cv.showPage()
    cv.save()


def render_svg(path):
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH:.4f}pt" height="{HEIGHT:.4f}pt" viewBox="0 0 {WIDTH:.4f} {HEIGHT:.4f}" role="img">',
             '<title>Program questions, mathematical models and physical correspondence</title>',
             '<desc>Three research questions, five parallel mathematical approaches, and separate requirements for physical interpretation. Two arrows mark conditional mathematical implications.</desc>',
             '<defs><style>']
    for face, fpath in FONT_FILES.items():
        encoded = base64.b64encode(fpath.read_bytes()).decode("ascii")
        weight = 700 if face == "Bold" else 400
        parts.append(f"@font-face {{font-family:'ScopeSans';src:url(data:font/ttf;base64,{encoded}) format('truetype');font-weight:{weight};font-style:normal;}}")
    parts.append('</style></defs>')
    parts.append(f'<rect width="{WIDTH}" height="{HEIGHT}" fill="white"/>')
    for obj in scene:
        kind = obj["kind"]
        if kind == "rect":
            parts.append(f'<rect x="{obj["x"]}" y="{obj["y"]}" width="{obj["w"]}" height="{obj["h"]}" rx="{obj["radius"]}" fill="{obj["fill"]}" stroke="{obj["stroke"]}" stroke-width="{obj["sw"]}"/>')
        elif kind == "line":
            parts.append(f'<line x1="{obj["x1"]}" y1="{obj["y1"]}" x2="{obj["x2"]}" y2="{obj["y2"]}" stroke="{obj["color"]}" stroke-width="{obj["sw"]}"/>')
        elif kind == "polygon":
            pts = " ".join(f"{x},{y}" for x, y in obj["points"])
            parts.append(f'<polygon points="{pts}" fill="{obj["fill"]}"/>')
        elif kind == "text":
            weight = 700 if obj["face"] == "Bold" else 400
            parts.append(f'<text x="{obj["x"]}" y="{obj["text_y"]}" font-family="ScopeSans, DejaVu Sans, sans-serif" font-weight="{weight}" font-size="{obj["size"]}" fill="{obj["color"]}" xml:space="preserve">{html.escape(obj["value"])}</text>')
    parts.append('</svg>')
    path.write_text("\n".join(parts) + "\n", encoding="utf-8")


def main():
    global OUT
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=OUT / "Rebuilt_Program_Diagram")
    args = parser.parse_args()
    OUT = args.output.resolve()
    if OUT.exists():
        raise FileExistsError("Choose a new output directory.")
    OUT.mkdir(parents=True, exist_ok=False)
    build_scene()
    render_pdf(OUT / (STEM + ".pdf"))
    render_svg(OUT / (STEM + ".svg"))
    print(f"Wrote one landscape A4 page; {len(checks)} fitted text lines; two conditional implication arrows.")
    print(OUT / (STEM + ".pdf"))
    print(OUT / (STEM + ".svg"))


if __name__ == "__main__":
    main()
