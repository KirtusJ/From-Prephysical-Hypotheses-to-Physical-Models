"""Reproduce launch-normalized records for successive three-tick position filters.

Run python check_repeated_position_records.py OUTDIR. Uses only the standard library.
"""
import argparse
from collections import Counter
from fractions import Fraction
from itertools import product
import json
from pathlib import Path


def require(ok, message):
    if not ok:
        raise ValueError(message)


def block(channel, home):
    first = {home - 1, home + 1} if channel == "C" else {home + 1}
    return [first, {home}, {home + 1}]


def signed_words(rows, home=0, incoming="R"):
    accepted = []
    rejected_at = Counter()
    for directions in product("RL", repeat=len(rows)):
        x, rail, sign = home, incoming, 1
        for tick, (next_rail, allowed) in enumerate(zip(directions, rows), 1):
            x += 1 if next_rail == "R" else -1
            if next_rail == rail == "L":
                sign = -sign
            rail = next_rail
            if x not in allowed:
                rejected_at[tick] += 1
                break
        else:
            accepted.append(("".join(directions), x, rail, sign))
    require(len(accepted) + sum(rejected_at.values()) == 2**len(rows), "word coverage")
    return accepted, rejected_at


def record(rows, home=0, incoming="R"):
    words, rejected = signed_words(rows, home, incoming)
    multiplicities = Counter((x, rail, sign) for _, x, rail, sign in words)
    # Independent predecessor update. Keep both rails at every admitted position.
    field = {(home, incoming): (1, 0)}
    for allowed in rows:
        following = {}
        for x in allowed:
            for rail, parent in (("R", x - 1), ("L", x + 1)):
                p, q = field.get((parent, "R"), (0, 0))
                a, b = field.get((parent, "L"), (0, 0))
                if rail == "L":
                    a, b = b, a
                if p + q + a + b:
                    following[x, rail] = (p + a, q + b)
        field = following
    cells = []
    for (x, rail), (p, q) in sorted(field.items()):
        require((p, q) == (multiplicities[x, rail, 1], multiplicities[x, rail, -1]),
                "word and predecessor counts differ")
        cells.append(dict(site=x, rail=rail, positive=p, negative=q))
    require(sum(p+q for p, q in field.values()) == len(words), "missing accepted port")
    return dict(masks=[sorted(row) for row in rows], accepted_words=words,
                rejected_words_by_first_failed_tick=sorted(rejected.items()), cells=cells)


def probability(data, a, c, rail=None):
    # One original launch, with F(1,0)=a+c. Rejected masks are never renormalized.
    mass = 0
    for cell in data["cells"]:
        if rail is None or rail == cell["rail"]:
            p, q = cell["positive"], cell["negative"]
            mass += a * (p + q) + c * (p - q)**2
    return Fraction(mass, (2**len(data["masks"])) * (a + c))


def serial_records():
    data = {}
    words = {"C": ["RLR", "LRR"], "I": ["RLR"]}
    for channel in "CI":
        data[channel] = record(block(channel, 0))
    for first, second in product("CI", repeat=2):
        data[first+second] = record(block(first, 0) + block(second, 1))
    for schedule, panel in data.items():
        expected = {"".join(p) for p in product(*(words[s] for s in schedule))}
        require(set(tuple(w) for w in panel["accepted_words"]) ==
                {(w, len(schedule), "R", 1) for w in expected}, "serial accepted words")
    for home in (-3, 4):
        for channel in "CI":
            translated = record(block(channel, home), home)
            expected = [(w, x+home, rail, s) for w, x, rail, s in data[channel]["accepted_words"]]
            require(translated["accepted_words"] == expected, "translated launch")
    rates = []
    for a, c in ((0, 1), (1, 0), (1, 1), (3, 1), (1, 3), (6, 2)):
        alpha = Fraction(a, a+c)
        measured = {s: probability(panel, a, c) for s, panel in data.items()}
        expected = {"C": (2-alpha)/4, "I": Fraction(1, 8), "CC": (4-3*alpha)/16,
                    "CI": (2-alpha)/32, "IC": (2-alpha)/32, "II": Fraction(1, 64)}
        require(measured == expected, "single and serial per-launch probabilities")
        fresh = {}
        for first, second in product("CI", repeat=2):
            key = first+second
            fresh[key] = measured[first] * measured[second]
            gap = measured[key] - fresh[key]
            expected_gap = alpha*(1-alpha)/16 if key == "CC" else 0
            require(gap == expected_gap, "fresh restart discrepancy")
        contrast = measured["CC"]*measured["II"]/(measured["CI"]*measured["IC"])
        require(contrast == (4-3*alpha)/(2-alpha)**2, "serial setting odds")
        rates.append(dict(a=a, c=c, alpha=alpha, serial=measured, fresh=fresh,
                          cc_gap=measured["CC"]-fresh["CC"], four_setting_contrast=contrast))
    return data, rates


def positive_ports():
    baseline = [{-1, 1}, {-2}, {-3, -1}, {-2}]
    opened = [baseline[0], {-2, 0}, baseline[2], baseline[3]]
    panels = [record(rows) for rows in (baseline, opened)]
    expected = [(1, 0, 0, 1), (1, 0, 1, 2)]  # R+,R-,L+,L-
    for panel, (rp, rm, lp, lm) in zip(panels, expected):
        require(panel["cells"] ==
                [dict(site=-2, rail="L", positive=lp, negative=lm),
                 dict(site=-2, rail="R", positive=rp, negative=rm)], "four-tick signed ports")
    gains = {"R": Fraction(7, 11), "L": Fraction(2, 9)}
    brightness = (Fraction(13, 5), Fraction(7, 16))
    comparisons = []
    for a, c in ((0, 1), (1, 1), (3, 1), (1, 0)):
        odds = []
        rates = []
        for panel, b in zip(panels, brightness):
            per_launch = {rail: probability(panel, a, c, rail) for rail in "RL"}
            rates.append(per_launch)
            odds.append((b*gains["L"]*per_launch["L"])/(b*gains["R"]*per_launch["R"]))
        ratio = odds[1]/odds[0]
        require(ratio == 1+2*Fraction(a, a+c), "gain-canceling positive comparison")
        comparisons.append(dict(a=a, c=c, per_launch=rates, odds_ratio=ratio))

    # Check that the equality of accepted signed arrays has an input hypothesis.
    left_launch = [record(rows, incoming="L") for rows in (baseline, opened)]
    signed = []
    for panel in left_launch:
        signed.append({cell["rail"]: cell["positive"] - cell["negative"] for cell in panel["cells"]})
    require(signed == [{"R": -1, "L": 1}, {"R": -1, "L": 3}], "wrong-rail countercontrol")
    return dict(settings=["baseline", "opened"], panels=panels, rates=comparisons,
                unequal_left_launch_signed=signed)


def run():
    serial, rates = serial_records()
    missed_translation = record(block("C", 0) + block("C", 0))
    require(not missed_translation["cells"], "untranslated second mask should miss the walker")
    half = next(row for row in rates if row["a"] == row["c"] == 1)
    require(half["cc_gap"] == Fraction(1, 64), "missing factor on half mixture")
    require(half["serial"]["CC"] / half["serial"]["C"] == Fraction(5, 12),
            "conditional repeated block differs from a fresh launch")
    return dict(scope="Exact conditional model predictions; probabilities use all original launches.",
                words="R/L are unit right/left steps; only L followed by L is negative.",
                serial=serial, rates=rates, translated_single_homes=[-3, 4],
                controls=dict(untranslated_second_C=missed_translation,
                              half_mixture_P_C_after_C=Fraction(5, 12),
                              half_mixture_fresh_P_C=Fraction(3, 8)),
                positive_ports=positive_ports())


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path)
    directory = parser.parse_args().directory
    result = run()
    directory.mkdir(parents=True, exist_ok=True)
    with (directory / "repeated_position_records.json").open("x", encoding="utf8", newline="\n") as out:
        json.dump(result, out, default=str, separators=(",", ":"))
        out.write("\n")
