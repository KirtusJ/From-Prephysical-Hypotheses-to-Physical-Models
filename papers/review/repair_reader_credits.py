"""Rebuild the current reader credits from the preceding published reader blobs.

Requires PyMuPDF 2.1 and git. The two pinned font files come from DejaVu
Serif (Matplotlib's distribution) and Latin Modern Roman (TeX Live).
The input commit already contains the seven mathematical font-map repairs.
"""
import argparse
import csv
import hashlib
import json
from pathlib import Path
import subprocess

import pymupdf


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
FONTS = {
    "DejaVuSerif.ttf": "107244956e9962b9e96faccdc551825e0ae0898ae13737133e1b921a2fd35ffa",
    "lmroman10-regular.otf": "1aa18cfefa58132c52ce5de70db1fd1154201c19cd2b2cdaffba4906a33e6852",
}


def checked_font(path):
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    if FONTS[path.name] != digest:
        raise ValueError(f"Unexpected font bytes: {path.name}")
    return pymupdf.Font(fontfile=str(path))


def draw_paragraph(page, edit, font):
    box = pymupdf.Rect(edit["area"])
    x, baseline = edit["at"]
    size = edit["size"]
    available = box.x1 - x
    words = edit["text"].split()
    lines = []
    current = ""
    for word in words:
        trial = f"{current} {word}".strip()
        if current and font.text_length(trial, fontsize=size) > available:
            lines.append(current)
            current = word
        else:
            current = trial
    lines.append(current)

    writer = pymupdf.TextWriter(page.rect)
    bottom = baseline + (len(lines) - 1) * edit["leading"] - size * font.descender
    if bottom > box.y1 + 1.5:
        raise ValueError(f"Paragraph extends outside its declared region on page {page.number+1} ({bottom:.2f} > {box.y1:.2f}): {lines}")
    for line in lines:
        writer.append((x, baseline), line, font=font, fontsize=size)
        baseline += edit["leading"]
    writer.write_text(page, color=(0, 0, 0))


def build(source, output, edits, fonts):
    with pymupdf.open(stream=source, filetype="pdf") as doc:
        for edit in edits:
            page = doc[edit["page"] - 1]
            region = pymupdf.Rect(edit["area"])
            if any(region.intersects(link["from"]) for link in page.get_links()):
                raise ValueError(f"Link intersects the declared region on {output.name}, page {page.number+1}")
            if edit["kind"] == "title addition":
                if page.get_textbox(region).strip():
                    raise ValueError(f"Title addition would cover existing text on {output.name}")
            else:
                page.add_redact_annot(region, fill=False, cross_out=False)
                page.apply_redactions(images=0, graphics=0, text=0)
            draw_paragraph(page, edit, fonts[edit["font"]])
        # Unreferenced originals must not survive in the revised reader.
        doc.save(output, garbage=2, deflate=True, no_new_id=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dejavu", required=True, type=Path)
    parser.add_argument("--latin-modern", required=True, type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    fonts = {p.name: checked_font(p) for p in (args.dejavu, args.latin_modern)}
    spec = json.loads((HERE / "reader_credits.json").read_text(encoding="utf-8"))
    with (HERE.parent / "catalog.csv").open(encoding="utf-8-sig", newline="") as file:
        published = {row["id"]: row["file"] for row in csv.DictReader(file)}
    args.output.mkdir(parents=True, exist_ok=True)
    for paper, record in spec["readers"].items():
        path = f"papers/{paper}.pdf"
        source = subprocess.check_output(["git", "show", f'{spec["source_commit"]}:{path}'], cwd=ROOT)
        if hashlib.sha256(source).hexdigest() != record["input_sha256"]:
            raise ValueError(f"Original reader hash mismatch: {path}")
        filename = published[paper]
        if not filename or Path(filename).name != filename:
            raise ValueError(f"Unexpected catalog filename for {paper}: {filename}")
        build(source, args.output / filename, record["edits"], fonts)


if __name__ == "__main__":
    main()
