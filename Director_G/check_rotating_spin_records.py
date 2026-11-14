"""Extract the 32 measured word frequencies from Huie et al., arXiv v4, Fig. 5(b)."""
import argparse
from fractions import Fraction
import hashlib
import io
import json
from pathlib import Path
import re
import tarfile
from urllib.request import urlopen
import zlib


SOURCE = "https://arxiv.org/src/2305.02926v4"
ARCHIVE_SHA = "60e88b33bd94d8a65fec0b3151d7afff75149e1be2dbd7a8c6f1dd2875d98557"
FIGURE_SHA = "40a36cbe3dc423241c604932f61cbc7a4e146eb4306e47d7b34ac685f47bd512"


def require(value, message):
    if not value:
        raise ValueError(message)


def figure(source):
    require(hashlib.sha256(source).hexdigest() == ARCHIVE_SHA, "different arXiv source")
    with tarfile.open(fileobj=io.BytesIO(source), mode="r:gz") as archive:
        data = archive.extractfile("Figure5.pdf").read()
    require(hashlib.sha256(data).hexdigest() == FIGURE_SHA, "different figure")
    return data


def drawing(data, number):
    # These object references and their stream encodings belong to this pinned PDF.
    tag = str(number).encode("ascii")
    require(b"/x" + tag + b" " + tag + b" 0 R " in data, "missing drawing reference")
    header = re.search(rb"(?m)^" + tag + rb" 0 obj\n", data)
    start = data.index(b"\nstream\n", header.end()) + len(b"\nstream\n")
    end = data.index(b"\nendstream", start)
    return zlib.decompress(data[start:end]).decode("ascii")


def bars(data, first, style):
    heights = []
    xs = []
    for index in range(first, first + 16):
        body = drawing(data, index)
        rectangle = re.findall(r"([-\d.]+) ([-\d.]+) ([-\d.]+) ([-\d.]+) re\s+" + style, body)
        require(len(rectangle) == 1, "expected one measurement bar")
        x, top, width, height = map(Fraction, rectangle[0])
        require(height < 0 and 6 < width < 7, "unexpected rectangle")
        require(abs(top + height + Fraction("238.156")) <= Fraction("0.001"), "different baseline")
        xs.append(x)
        heights.append(-height)
    require(all(6 < b-a < 7 for a,b in zip(xs,xs[1:])), "word order")
    # The red marks plot 1/16. Their height gives an independent check on the simplex scale.
    require("35.297 -223.301 m 42.195 -223.301 l" in drawing(data,119), "reference level")
    require(abs(sum(heights) - 16 * Fraction("14.855")) < Fraction("0.02"), "probability scale")
    return heights


def summarize(heights):
    bins = {format(i, "04b"): h for i,h in enumerate(heights)}
    total = sum(heights)
    first_flip = {}
    double_flip = {}
    for rail in "01":
        group = {word: h for word,h in bins.items() if word[0] == rail}
        exposure = sum(group.values())
        first_flip[rail] = sum(h for w,h in group.items() if w[0] != w[1]) / exposure
        double_flip[rail] = sum(h for w,h in group.items() if w[0] != w[1] and w[2] == w[0]) / exposure
    same02 = sum(h for w,h in bins.items() if w[0] == w[2]) / total
    all_same = sum(h for w,h in bins.items() if w[0] == w[1] == w[2]) / total
    double = sum(h for w,h in bins.items() if w[0] != w[1] and w[2] == w[0]) / total
    require(double == same02 - all_same, "event partition")
    flip_words = {}
    for word, height in bins.items():
        changes = "".join("0" if x == y else "1" for x, y in zip(word, word[1:]))
        flip_words[changes] = flip_words.get(changes, 0) + height / total
    order_spread = {}
    for flips in (1, 2):
        group = [p for sequence,p in flip_words.items() if sequence.count("1") == flips]
        order_spread[str(flips)] = float(max(group) - min(group))
    return dict(words={w: dict(pdf_height=str(h), frequency=float(h/total)) for w,h in bins.items()},
                first_flip_given_initial_bit={k:float(v) for k,v in first_flip.items()},
                double_flip_given_initial_bit={k:float(v) for k,v in double_flip.items()},
                pooled_flip_words={w:float(p) for w,p in sorted(flip_words.items())},
                within_flip_count_order_spread=order_spread,
                endpoint_same=float(same02), first_three_same=float(all_same), two_flips=float(double))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path, help="new output JSON file")
    parser.add_argument("--source", type=Path, help="local copy of the pinned arXiv source tar.gz")
    args = parser.parse_args()
    if args.source is None:
        with urlopen(SOURCE, timeout=30) as response:
            source = response.read()
    else:
        source = args.source.read_bytes()
    data = figure(source)
    results = dict(source=SOURCE, source_sha256=ARCHIVE_SHA, figure_sha256=FIGURE_SHA,
                   figure="Figure5.pdf panel (b), first to last read in displayed bit order",
                   unit="approximations from plotted heights", shot_denominators=None,
                   initially_and_finally_detected=summarize(bars(data,81,"B")),
                   initially_detected=summarize(bars(data,97,"S")))
    with args.output.open("x", encoding="utf8", newline="\n") as out:
        json.dump(results, out, indent=2)
        out.write("\n")


if __name__ == "__main__":
    main()
