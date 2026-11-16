"""Read the supplied authors' figure and compare its numeric panel with exact walks."""
from argparse import ArgumentParser
from fractions import Fraction as F
from functools import lru_cache
from hashlib import sha256
from pathlib import Path
from runpy import run_path
import json

from PIL import Image
import fitz

walk = run_path(str(Path(__file__).with_name("check_cycle_cover.py")))
require = walk["require"]
PNG_SHA = "9a285bad1a8b4cae1dc907abde00f95e074fdc320126cc7e41258d3765fc1d6e"
PDF_SHA = "4d04148c6afc41fa67c3288e47f79121ea915de7d4c3a675f9354558bbb7bc8b"
TOP, BOTTOM = 1237, 1969


def cell(image, panel, tick, site):
    left = {"numeric": 73, "experiment": 496}[panel]
    # Source PNG, zero-based pixels. Pitch in both directions is 36.75 px.
    x = left + ((2*site+1)*147)//8
    y = 1235 + ((2*tick+1)*147)//8
    colors = {image.getpixel((x+dx, y+dy)) for dx in (-5, 0, 5) for dy in (-5, 0, 5)}
    require(len(colors) == 1, "cell center crosses a boundary")
    return colors.pop()


def legend_reader(image):
    entries = tuple(image.getpixel((885, y)) for y in range(TOP, BOTTOM+1))
    require(entries == tuple(image.getpixel((890, y)) for y in range(TOP, BOTTOM+1)),
            "legend column mismatch")

    @lru_cache(None)
    def read(rgb, slack):
        distances = [max(abs(a-b) for a, b in zip(rgb, color)) for color in entries]
        threshold = min(distances) + slack
        matches = [i for i, delta in enumerate(distances) if delta <= threshold]
        span = BOTTOM-TOP
        return F(span-max(matches), span), F(span-min(matches), span)
    return read


def pdf_symmetry(pdf_path):
    """Use the original indexed image bytes. Equal indices imply equal colors."""
    with fitz.open(pdf_path) as doc:
        page = doc[7]
        panels = sorted({(info["bbox"][0], info["xref"]) for info in page.get_image_info(xrefs=True)
                         if 360 < info["bbox"][1] < 370})
        require(len(panels) == 2, "journal panel count")
        colors = []
        for _, xref in panels:
            require(doc.xref_get_key(xref, "Width")[1] == "308" and
                    doc.xref_get_key(xref, "Height")[1] == "614", "journal panel dimensions")
            data = doc.xref_stream(xref)
            require(len(data) == 308*614, "journal indexed pixel count")
            row = (2*3+1)*614//40
            pair = [data[row*308 + (2*m+1)*308//20] for m in (1, 3)]
            colors.append(pair)
        require(colors == [[8, 8], [10, 11]], "journal round-three pixel indices")
    return colors


def main():
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("figure_png", type=Path)
    parser.add_argument("journal_pdf", type=Path)
    args = parser.parse_args()
    for path, expected in ((args.figure_png, PNG_SHA), (args.journal_pdf, PDF_SHA)):
        require(sha256(path.read_bytes()).hexdigest() == expected, "different source bytes")
    phase_input = walk["launch"](10, 0)
    phase_input[0] = [(1, 0), (0, 1)]
    first = walk["step"](phase_input, "Hprime")
    require(sum(walk["probability"](a, 1) for a in first[1])/2 == 1 and
            sum(walk["probability"](a, 1) for a in first[9])/2 == 0, "phase control")
    indices = pdf_symmetry(args.journal_pdf)
    with Image.open(args.figure_png) as image:
        require(image.size == (1003, 2040) and image.mode == "RGB", "source raster layout")
        read = legend_reader(image)
        sharp = [walk["launch"](10, rail) for rail in (0, 1)]
        diagonal = walk["launch"](10, 0)
        diagonal[0] = [(1, 0), (1, 0)]  # Divide intensities by two below.
        counts = {str(slack): [0, 0, 0] for slack in (2, 4, 8)}
        misses = []
        prediction = {}
        for t in range(20):
            for m in range(10):
                displacement = (m-2) % 10
                probs = [sum(walk["probability"](a, t) for a in s[displacement]) for s in sharp]
                pure = sum(walk["probability"](a, t) for a in diagonal[displacement])/2
                require(pure == sum(probs)/2, "diagonal input versus equal incoherent mixture")
                if (m-t) % 2:
                    require(all(p == 0 for p in probs), "parity control")
                    continue
                if (t, m) in ((3,1), (3,3), (7,7)):
                    prediction[f"{t},{m}"] = [str(p) for p in probs+[pure]]
                rgb = cell(image, "numeric", t, m)
                for slack in (2, 4, 8):
                    low, high = read(rgb, slack)
                    for j, p in enumerate(probs+[pure]):
                        counts[str(slack)][j] += low <= p <= high
                    if slack == 4 and not low <= pure <= high:
                        misses.append([t, m])
            sharp = [walk["step"](s, "Hprime") for s in sharp]
            diagonal = walk["step"](diagonal, "Hprime")
        require(prediction == {"3,1": ["1/8","5/8","3/8"], "3,3": ["5/8","1/8","3/8"],
                               "7,7": ["29/64"]*3}, "distinguishing and nondistinguishing cells")
        require(counts == {"2":[44,44,87], "4":[46,46,95], "8":[49,49,100]}, "panel counts")
        require(misses == [[6,0],[6,6],[7,5],[7,9],[19,7]], "preserve discrepant cells")
        readings = {}
        for t, m in ((3,1), (3,3), (7,7)):
            pair = {}
            for panel in ("numeric", "experiment"):
                rgb = cell(image, panel, t, m)
                low, high = read(rgb, 4)
                pair[panel] = dict(rgb=rgb, legend_range=[str(low), str(high)])
            readings[f"{t},{m}"] = pair
    print(json.dumps(dict(journal_round_three_indices=indices, predictions_R_L_diagonal=prediction,
                          png_samples=readings, matching_accessible_cells=counts,
                          diagonal_misses_at_slack_four=misses), indent=2))


if __name__ == "__main__":
    main()
