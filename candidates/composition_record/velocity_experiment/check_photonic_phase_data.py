"""Replay Wang et al., Fig. 15B. Read the pinned vector plot without installing a PDF library."""

import argparse
import hashlib
import io
import re
import tarfile
import urllib.request
import zlib
from collections import defaultdict
from pathlib import Path


SOURCE = "https://arxiv.org/src/1907.04159"
FIGURE = "Fig/SI/compare.pdf"
SHA256 = "aba9cf3838e6b03b63a4ae6a626a37a997b860a806d51792d26695ab002e3c22"


def fetch_figure():
    with urllib.request.urlopen(SOURCE, timeout=30) as response:
        data = response.read(8_000_001)
    if len(data) > 8_000_000:
        raise ValueError("Unexpected source archive size")
    with tarfile.open(fileobj=io.BytesIO(data), mode="r:*") as archive:
        entry = archive.getmember(FIGURE)
        if not entry.isfile() or entry.size != 10_527:
            raise ValueError("Unexpected figure member")
        with archive.extractfile(entry) as figure:
            return figure.read()


def read_error_bars(pdf):
    if hashlib.sha256(pdf).hexdigest() != SHA256:
        raise ValueError("Figure differs from the source used for this extraction")
    # The FOP exporter put the data paths and both grayscale axes in object 2.
    stream = pdf.split(b"2 0 obj\n", 1)[1].split(b"stream\n", 1)[1]
    drawing = zlib.decompress(stream).decode("ascii")
    for y in (446, 43):
        if f"941 {y} m\n1493 {y} l\nS" not in drawing:
            raise ValueError("Expected ordinate axis endpoints of panel B")
    start, span = 446, 446 - 43
    xs = [941 + 69 * j for j in range(9)]
    strokes = defaultdict(list)
    for block in drawing.split("\nq\n"):
        # Each half of an error bar has exactly one vertical segment, drawn
        # from the common center to a cap. Ignore model curves and markers.
        color = re.search(r"^(0 0 1|0 1 0) RG$", block, re.M)
        line = re.search(r"^10 M\n(\d+) ([\d.]+) m\n\1 ([\d.]+) l\nS\nQ", block, re.M)
        if line and color and int(line[1]) in xs:
            strokes[(int(line[1]), color[1])].append((float(line[2]), float(line[3])))
    rows = []
    for j, x in enumerate(xs):
        values = []
        for color in ("0 0 1", "0 1 0"):
            pair = strokes[(x, color)]
            if len(pair) != 2 or pair[0][0] != pair[1][0]:
                raise ValueError(f"Broken or absent error bar, row {j}, color {color}")
            center = pair[0][0]
            lo, hi = sorted(cap for _, cap in pair)
            if not lo < center < hi or abs((lo + hi) / 2 - center) > 0.0001:
                raise ValueError(f"Asymmetric bar, row {j}, color {color}")
            values.extend(((start - center) / span, (hi - lo) / (2 * span)))
        rows.append(values)
    return rows


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--figure", type=Path, help="locally saved Fig/SI/compare.pdf")
    source.add_argument("--fetch", action="store_true", help="read the arXiv source in memory")
    args = parser.parse_args()
    pdf_bytes = args.figure.read_bytes() if args.figure else fetch_figure()
    print("alpha_in_pi_over_16,P_Q,bar_Q,P_C,bar_C,Q_minus_C")
    for j, (q, eq, c, ec) in enumerate(read_error_bars(pdf_bytes)):
        print(f"{j},{q:.6f},{eq:.6f},{c:.6f},{ec:.6f},{q - c:+.6f}")
