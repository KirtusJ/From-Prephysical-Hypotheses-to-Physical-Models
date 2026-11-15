"""Digitize two of the experimental dots in Su et al., npj Quantum Inf. 5, 40.

Usage: python read_su_figure5.py [published-Figure-5.png]
Requires Pillow. Omit the path to fetch the pinned original publisher PNG.
Prints figure measurements and a separate ideal-walk check, never raw counts.
"""
import argparse
from collections import defaultdict
from hashlib import sha256
from io import BytesIO
import json
from math import sqrt
from statistics import median
from urllib.request import urlopen

from PIL import Image

FIGURE = (
    "https://media.springernature.com/full/springer-static/image/"
    "art%3A10.1038%2Fs41534-019-0155-x/MediaObjects/41534_2019_155_Fig5_HTML.png"
)
FIGURE_HASH = "0b1d0aa7b08c7dfb66c8574e4b0b50ebc1e93bdaa258337548a8bab1cdc77778"


def require(condition, message):
    if not condition:
        raise ValueError(message)


def measure_dot(image, x, low_y, high_y):
    # Each box contains one experimental dot and its vertical capped bar.
    # The bright red experimental ink is darker in green/blue than the
    # underlying thick four-step red theory line. Verify across thresholds.
    measurements = []
    for channel_max in (30, 40, 48, 55):
        selected_rows = []
        for y in range(low_y, high_y + 1):
            row = [image.getpixel((u, y)) for u in range(x - 5, x + 6)]
            reds = [p for p in row if p[0] > 180 and max(p[1:]) < channel_max]
            if len(reds) >= 2:
                selected_rows.append(y)
        require(len(selected_rows) > 15, "experimental error bar missing")
        top, bottom = min(selected_rows), max(selected_rows)
        measurements.append((top, bottom, (top + bottom) / 2))
    top, bottom, center = (median(col) for col in zip(*measurements))
    require(max(m[2] for m in measurements) - min(m[2] for m in measurements) <= 1,
            "dot center depends on threshold")
    # Independent dot-center check uses the width of the marker between caps.
    widths = {}
    for y in range(int(top) + 4, int(bottom) - 3):
        pixels = [image.getpixel((u, y)) for u in range(x - 5, x + 6)]
        widths[y] = sum(r > 180 and max(g, b) < 48 for r, g, b in pixels)
    core = [y for y, width in widths.items() if width >= max(widths.values()) - 1]
    require(abs(center - median(core)) <= 2, "error bar midpoint misses dot center")
    # Pixel y = 382,273,164,55 at successive labels 0,0.2,0.4,0.6.
    spread = lambda y: (382 - y) / 545
    return {"dot_y_pixels": center, "statistical_bar_y_pixels": [top, bottom],
            "spread_rounded": round(spread(center), 2),
            "drawn_statistical_bar_rounded": [round(spread(bottom), 2), round(spread(top), 2)]}


def ideal_statistics(alpha):
    # Sc in the article is a pi/4 rotation. Coin state 0 moves left and 1 right.
    fields = {(x, rail): a * c for x, a in ((-1, alpha), (1, sqrt(1 - alpha**2)))
              for rail, c in ((0, 1 / sqrt(2)), (1, 1j / sqrt(2)))}

    def variance(state):
        mass = sum(abs(a)**2 for a in state.values())
        mean = sum(x * abs(a)**2 for (x, _), a in state.items()) / mass
        return sum((x - mean)**2 * abs(a)**2 for (x, _), a in state.items()) / mass

    initial = variance(fields)
    for _ in range(4):
        new = defaultdict(complex)
        for (x, rail), amplitude in fields.items():
            new[x - 1, 0] += (-1 if rail == 1 else 1) * amplitude / sqrt(2)
            new[x + 1, 1] += amplitude / sqrt(2)
        fields = new
    final = variance(fields)
    return {"variance_change_per_step": round((final - initial) / 4, 5),
            "standard_deviation_change_per_step": round((sqrt(final) - sqrt(initial)) / 4, 5)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("image", nargs="?", type=argparse.FileType("rb"))
    args = parser.parse_args()
    if args.image is not None:
        with args.image as stream:
            data = stream.read()
    else:
        with urlopen(FIGURE, timeout=45) as stream:
            data = stream.read()
    require(sha256(data).hexdigest() == FIGURE_HASH, "Figure version differs")
    image = Image.open(BytesIO(data)).convert("RGB")
    require(image.size == (1495, 484), "Unexpected figure geometry")
    for y in (382, 273, 164, 55):
        require(max(image.getpixel((116, y))) < 80, "y-axis calibration tick missing")
    for x in (122, 415, 709):
        require(max(image.getpixel((x, 6))) < 80, "x-axis calibration tick missing")
    result = {}
    for alpha, x, top, bottom in ((-0.6, 239, 135, 164), (0.6, 592, 229, 256)):
        reading = measure_dot(image, x, top, bottom)
        require(abs((x - 415.5) / 293.5 - alpha) < 0.005, "x value mismatches tick labels")
        result[str(alpha)] = {"published_figure": reading, "separate_ideal_recurrence": ideal_statistics(alpha)}
    print(json.dumps({"figure_sha256": FIGURE_HASH, "spread_per_pixel": 1 / 545,
                      "digitization_allowance": 2 / 545,
                      "note": "Drawn bars are identified by the authors as statistical errors. Coverage unspecified.",
                      "settings": result}, indent=2))


if __name__ == "__main__":
    main()
