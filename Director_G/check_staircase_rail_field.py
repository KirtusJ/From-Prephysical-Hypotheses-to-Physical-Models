"""Exact signed words, three-tick rail records and translated Fourier support.

Run python -B check_staircase_rail_field.py OUTDIR. The output must be new.
"""
import argparse
import json
from collections import Counter, defaultdict
from fractions import Fraction
from itertools import product
from pathlib import Path


def require(test, message):
    if not test:
        raise ValueError(message)


def walk(word, start, rail, order, wrap=True):
    x = start
    sign = 1
    gain = area = 0
    for step in word:
        gain += x // 2
        area += x
        if rail == step == "L":
            sign = -sign
        x += 1 if step == "R" else -1
        if wrap:
            x %= 4 * order
        rail = step
    return x, rail, gain, area, sign


def fold(j, order):
    return min(j % order, (-j) % order)


def phase_check():
    rows = []
    for order in (3, 4, 5, 8, 13):
        settings = histories = 0
        for k in range(order):
            for start in (-1, 0, 4 * order - 1):
                for rail in "RL":
                    for n in range(1, 8):
                        odd_ticks = (n + start % 2) // 2
                        for word in product("RL", repeat=n):
                            x, out, gain, area, sign = walk(word, start, rail, order)
                            line = walk(word, start, rail, order, wrap=False)
                            require((line[0] % (4 * order), line[1], line[2] % order, line[4])
                                    == (x, out, gain % order, sign), "ring seam")
                            require((2*k*gain - k*area + k*odd_ticks) % (2*order) == 0,
                                    "parity gauge in units of pi/M")
                            histories += 1
                        settings += 1
        rows.append(dict(M=order, settings=settings, histories=histories))
    return rows


def square_lags(ports, order, k, selector):
    # Coefficients multiply cos(2*pi*j/M); sum only after squaring each port.
    coeffs = Counter()
    for (x, rail), words in ports.items():
        if selector(x, rail):
            for g, s in words:
                for f, t in words:
                    coeffs[fold(k*(g-f), order)] += s*t
    return {i: x for i, x in sorted(coeffs.items()) if x}


def expected(order, k, base, contrast):
    coeffs = Counter({0: base})
    coeffs[fold(k, order)] += contrast
    return {i: x for i, x in sorted(coeffs.items()) if x}


def three_ticks():
    tally = []
    ports = defaultdict(list)
    for word in product("RL", repeat=3):
        x, rail, gain, _, sign = walk(word, 0, "R", 3, wrap=False)
        tally.append(["".join(word), x, rail, gain, sign])
        ports[x, rail].append((gain, sign))
    left = lambda x, rail: rail == "L"
    right = lambda x, rail: rail == "R"
    bright = lambda x, rail: (x, rail) == (1, "R")
    dark = lambda x, rail: (x, rail) == (-1, "L")
    all_ports = lambda x, rail: True
    records = []
    for order in (3, 4, 5, 8, 12, 13):
        for k in range(-(order // 2), order // 2 + 1):
            coeffs = {key: square_lags(ports, order, k, choice)
                      for key, choice in (("L", left), ("R", right), ("bright", bright),
                                          ("dark", dark), ("position_bin_covering_all", all_ports))}
            for key, base, contrast in (("L", 4, -2), ("R", 4, 2), ("bright", 2, 2),
                                        ("dark", 2, -2), ("position_bin_covering_all", 8, 0)):
                require(coeffs[key] == expected(order, k, base, contrast), "rail / endpoint law")
            records.append(dict(M=order, k=k, numerators=coeffs))
    count = {name: str(Fraction(sum(len(w) for (x, r), w in ports.items() if f(x, r)), 8))
             for name, f in (("L", left), ("R", right), ("bright", bright), ("dark", dark),
                             ("position_bin_covering_all", all_ports))}
    require(count == {"L": "1/2", "R": "1/2", "bright": "1/4", "dark": "1/4",
                      "position_bin_covering_all": "1"}, "count controls")
    return dict(word_columns=["word", "line_position", "last_rail", "staircase_gain", "sign"],
                words=tally, port_records=records, coefficient_convention=
                "Each numerator maps exact lag j to coefficient of cos(2*pi*j/M); divide by 8."
                " k=0 is also the field-off result for every coherent character.",
                count_on_and_off=count)


def support_checks():
    # On the 4M ring h=pi*k/M shifts the ordinary Fourier-bin index by -2k.
    rows = []
    for order in (12, 24, 48, 96):
        period = 4*order
        halfwidth = order // 12
        support = {(center+i) % period for center in (order, 3*order)
                   for i in range(-halfwidth, halfwidth+1)}
        for k in (0, 1, -1, order // 3, -(order // 3), order // 2):
            shifted = {(j-2*k) % period for j in support}
            overlap = len(support & shifted)
            require((overlap == 0) == (fold(k, order) > halfwidth),
                    "folded Fourier-support overlap")
            rows.append(dict(M=order, k=k, halfwidth_bins=halfwidth, support_size=len(support),
                             overlapping_bins=overlap))
    return rows


def run():
    return dict(phase_identity=phase_check(), three_ticks=three_ticks(),
                fourier_support=support_checks())


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path)
    directory = parser.parse_args().directory
    result = run()
    directory.mkdir(parents=True, exist_ok=True)
    with (directory / "staircase_rail_field.json").open("x", encoding="utf8", newline="\n") as out:
        json.dump(result, out, indent=2)
        out.write("\n")
