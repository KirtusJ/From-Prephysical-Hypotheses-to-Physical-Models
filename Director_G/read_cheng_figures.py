"""Extract the two named vector panels from the authors' versioned arXiv sources."""

import argparse
import csv
import hashlib
from pathlib import Path
import tarfile

import pymupdf


HERE = Path(__file__).resolve().parent


def drawings(archive, member, expected_hash):
    with tarfile.open(archive) as source:
        data = source.extractfile(member).read()
    if hashlib.sha256(data).hexdigest() != expected_hash:
        raise ValueError(f"Unexpected source figure: {member}")
    with pymupdf.open(stream=data, filetype="pdf") as pdf:
        return pdf[0].get_drawings()


def centers(path, bottom_clipped):
    boxes = [item[1] for item in path["items"] if item[0] == "re"]
    assert len(boxes) == 21
    # Both panels use equal square markers. Recover the center from the visible
    # top edge in Fig. 4(a), or bottom edge in Fig. 6(d) (opposite axis clipping).
    half = boxes[5].height / 2
    assert abs(half - 2.58) < 0.001
    if bottom_clipped:
        return [box.y0 + half for box in boxes]
    return [box.y1 - half for box in boxes]


def cap_heights(paths, x, grid_step):
    caps = []
    for path in paths:
        r = path["rect"]
        if r.width > 1 and r.height == 0 and abs((r.x0 + r.x1) / 2 - x) < grid_step / 4:
            caps.append(r.y0)
    assert len(caps) in (0, 2)
    return sorted(caps) if caps else [None, None]


def axis(draw, axis_index, maximum):
    a = draw[axis_index]["rect"]
    return lambda y: "" if y is None else f"{maximum * (a.y1 - y) / a.height:.6f}"


def histogram(path):
    d = drawings(path, "fig4a.pdf", "866a4b7124f4df6a729a07dc04d2819f9bad91ad4faa0c3da554db4227409158")
    scale = axis(d, 22, 0.5)
    x0, spacing = d[0]["rect"].x0, d[0]["rect"].width / 20
    black = centers(d[189], True)
    gray = centers(d[108], True)
    bars = {}
    for item in d[68:108]:
        rect = item["rect"]
        index = round(((rect.x0 + rect.x1) / 2 - x0) / spacing)
        bars[index, item["color"]] = rect.y0
    yield ["x", "black", "black_cap_low", "black_cap_high", "gray", "gray_cap_low", "gray_cap_high", "theory_stack_top", "theory_blue_top"]
    for i in range(21):
        x = x0 + i * spacing
        b_hi, b_lo = cap_heights(d[190:270], x, spacing)
        g_hi, g_lo = cap_heights(d[109:189], x, spacing)
        base = d[0]["rect"].y0
        # Zero-height endpoint bars can be absent from one of the two paints.
        blue = bars.get((i, (0, 0, 1)), base)
        top = bars.get((i, (1, 0, 0)), blue)
        yield [2 * i - 20, *map(scale, (black[i], b_lo, b_hi, gray[i], g_lo, g_hi, top, blue))]


def concentration(path):
    d = drawings(path, "fig6d.pdf", "fb2b3836958f8b001b4de88e0ccb2d2d94e8fef619336db268fc8daadbf925a1")
    scale = axis(d, 12, 1)
    points = centers(d[26], False)
    line = d[24]["items"]
    assert len(line) == 20 and all(seg[0] == "l" for seg in line)
    numerical = [line[0][1]] + [seg[2] for seg in line]
    assert all(path["color"] == (0, 0, 1) for path in d[48:124])
    spacing = (numerical[-1].x - numerical[0].x) / 20
    yield ["t", "blue", "cap_low", "cap_high", "numerical_blue_line"]
    for i, p in enumerate(numerical):
        hi, lo = cap_heights(d[48:124], p.x, spacing)
        yield [i, *map(scale, (points[i], lo, hi, p.y))]


def main():
    args = argparse.ArgumentParser(description=__doc__)
    args.add_argument("v1", type=Path)
    args.add_argument("v2", type=Path)
    args.add_argument("--output", type=Path, default=HERE / "results")
    options = args.parse_args()
    panels = {"cheng_positions.csv": histogram(options.v1),
              "cheng_concentration.csv": concentration(options.v2)}
    for name, rows in panels.items():
        with (options.output / name).open("w", encoding="utf-8", newline="") as file:
            csv.writer(file, lineterminator="\n").writerows(rows)


if __name__ == "__main__":
    main()
