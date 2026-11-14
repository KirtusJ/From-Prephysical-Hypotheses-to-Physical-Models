"""Replay figure 4 in Nitsche et al. and three origin-sink alternatives."""
import argparse
from collections import defaultdict
from fractions import Fraction as F
import hashlib
import json
from math import comb
from pathlib import Path

PLOT_SHA = "4d596d90edbc7c4e170bdb5f71d060072350d3e5fc293a2fb12198bf11405aab"
# Pixel rows counted from top, inclusive. Red (reset) then blue (continual).
CAPS = [
    (280,293,271,301), (250,266,214,247), (222,242,214,247),
    (207,231,211,244), (195,220,211,244), (187,213,210,244),
    (178,207,210,244), (171,203,210,243), (166,197,210,244),
    (162,194,210,243), (157,191,210,243), (153,188,210,243),
    (150,185,209,243), (147,183,209,243), (143,180,209,243),
    (140,178,209,243), (136,175,209,242), (134,173,208,241),
]


def extract(pdf):
    import pymupdf
    with pymupdf.open(pdf) as doc:
        image_id, = [row[0] for row in doc[17].get_images()]
        pix = pymupdf.Pixmap(doc, image_id)
        assert (pix.width, pix.height, pix.n) == (800, 597, 3)
        assert hashlib.sha256(pix.samples).hexdigest() == PLOT_SHA
        rows = []
        for tick in range(2, 37, 2):
            xmid = round(100 + 16.3*tick)
            caps = []
            for red in [True, False]:
                seen = []
                for y in range(60, 534):
                    for x in range(xmid-4, xmid+5):
                        r, g, b = pix.pixel(x, y)
                        if b-g > 7 and (r-b > 30 if red else b-r > 30 and g-r > 7):
                            seen.append(y)
                            break
                caps.extend([min(seen), max(seen)])
            rows.append(tuple(caps))
    assert rows == CAPS


def band(upper, lower):
    # Read both axis lines and each cap to within one pixel of the recorded row.
    return [F(536-(lower+1), 478), F(538-(upper-1), 478)]


def amplitude_step(state):
    out = defaultdict(lambda: [0, 0])
    for x, (r, l) in state.items():
        out[x+1][0] += r+l
        out[x-1][1] += r-l
    return out


def even_step(blocks):
    # Two ticks followed by an exact position write, leaving the local coin intact.
    out = defaultdict(lambda: [0, 0, 0])
    for x, (rr, rl, ll) in blocks.items():
        a = rr+2*rl+ll
        b = rr-2*rl+ll
        out[x+2][0] += a
        out[x-2][2] += b
        for i, value in enumerate([b, rr-ll, a]):
            out[x][i] += value
    return out


def group_by_histories(ticks, write_ticks):
    # Independent signed paths with the full site register kept to terminal time.
    from itertools import product
    from collections import Counter
    amplitudes = Counter()
    for paths in product((1,-1), repeat=ticks):
        x, prev, sign, record = 0, 1, 1, []
        for t, move in enumerate(paths, 1):
            sign *= -1 if prev == move == -1 else 1
            x += move
            prev = move
            if x == 0:
                if t == ticks:
                    amplitudes[tuple(record), move] += sign
                break
            if t in write_ticks:
                record.append(x)
    return F(sum(a*a for a in amplitudes.values()),2**ticks)


def launch_mixture(rows, recorded_column):
    # Every row supplies an exact interval in the same launch fraction.
    lower, upper = F(0), F(1)
    limits, degenerate = [], []
    for row in rows:
        coherent = F(row["coherent_continual"])
        delta = F(row[recorded_column]) - coherent
        low_cap, high_cap = band(*row["continual_cap_rows"])
        if delta == 0:
            assert low_cap <= coherent <= high_cap
            degenerate.append(row["tick"])
            continue
        low, high = sorted(((low_cap-coherent)/delta, (high_cap-coherent)/delta))
        lower, upper = max(lower, low), min(upper, high)
        limits.append((row["tick"], high))
    assert lower <= upper
    return {"fraction_interval": [str(lower), str(upper)],
            "zero_passes": lower <= 0 <= upper,
            "upper_bound_clocks": [t for t, value in limits if value == upper],
            "equal_prediction_clocks": degenerate}


def independent_writes_at_half(ticks, interval):
    # Average over all subsets of eligible writes, each selected independently.
    from itertools import combinations
    total = F()
    for t in range(2, ticks+1, 2):
        eligible = range(interval, t, interval)
        subtotal = sum(group_by_histories(t, writes)
                       for n in range(len(eligible)+1)
                       for writes in combinations(eligible, n))
        total += subtotal / 2**len(eligible)
    return total


def run():
    free = {0: (1, 0)}
    survivor = {0: (1, 0)}
    blocks = {0: (1, 0, 0)}
    separated = [{0: (1, 0)}]
    cumulative = cumulative_even = F()
    reset_miss = F(1)
    previous_fine = F()
    rows = []
    for t in range(1, 37):
        denom = 2**t
        free = amplitude_step(free)
        reset_miss *= 1-F(sum(c*c for c in free.get(0, ())), denom)
        survivor = amplitude_step(survivor)
        first = F(sum(c*c for c in survivor.pop(0, ())), denom)
        cumulative += first
        assert cumulative + F(sum(r*r+l*l for r,l in survivor.values()),denom) == 1

        phases = [amplitude_step(s) for s in separated]
        separated_first = sum(F(sum(c*c for c in s.pop(0, ())), denom) for s in phases)
        assert first == separated_first
        if t == 1:
            separated = [{x: pair for x, pair in phases[0].items() if x*side>0} for side in [-1,1]]
        else:
            separated = phases

        if t % 2:
            assert first == 0
            continue
        blocks = even_step(blocks)
        rr, _, ll = blocks.pop(0, (0,0,0))
        first_even = F(rr+ll,denom)
        cumulative_even += first_even
        assert cumulative_even+F(sum(r+l for r,_,l in blocks.values()),denom)==1
        fine = 1-F(comb(t,t//2),denom)
        if t <= 10:
            for writes, q in [((),first),(range(1,t),fine-previous_fine),(range(2,t,2),first_even)]:
                assert q == group_by_histories(t, writes)
        previous_fine = fine
        raw = CAPS[t//2-1]
        red,blue = band(*raw[:2]),band(*raw[2:])
        rows.append({
            "tick":t, "reset_cap_rows":raw[:2], "continual_cap_rows":raw[2:],
            "reset_expanded_interval":list(map(float,red)), "continual_expanded_interval":list(map(float,blue)),
            "coherent_continual":str(cumulative), "side_tag_continual":str(cumulative),
            "exact_site_each_even_tick":str(cumulative_even), "exact_site_each_tick":str(fine),
            "coherent_reset":float(1-reset_miss),
            "inside_expanded_plotted_ranges": {
                "coherent_continual": blue[0]<=cumulative<=blue[1],
                "site_each_even_tick": blue[0]<=cumulative_even<=blue[1],
                "site_each_tick": blue[0]<=fine<=blue[1],
                "coherent_reset": red[0]<=1-reset_miss<=red[1]}})
    def returned(r, l):
        return [F((r+l)**2, 4), F((r-l)**2, 4)]

    inverse_control = {"coherent": returned(1,1), "phase_flip": returned(1,-1),
                       "hidden_side": [a+b for a,b in zip(returned(1,0), returned(0,1))]}
    assert list(inverse_control.values()) == [[1,0],[0,1],[F(1,2),F(1,2)]]
    mixtures = {}
    for column, step, t in [("exact_site_each_tick",1,8), ("exact_site_each_even_tick",2,10)]:
        data = launch_mixture(rows, column)
        row = rows[t//2-1]
        by_launch = (F(row["coherent_continual"]) + F(row[column])) / 2
        by_tick = independent_writes_at_half(t, step)
        assert by_launch != by_tick
        data["half_fraction_control"] = {"tick":t, "draw_once_per_launch":str(by_launch),
                                         "draw_independently_per_eligible_tick":str(by_tick)}
        mixtures[column] = data
    return {"comparison": "Processed figure 4 cumulative recurrence probabilities, not raw counts.",
            "proposed_one_tick_inverse_source_R_then_L": {k:list(map(str,v)) for k,v in inverse_control.items()},
            "fixed_launch_mixture_all_continual_bars": mixtures,
            "plot_rgb_sha256":PLOT_SHA, "axis_rows_for_zero_and_one":[537,59],
            "source_clock_zero":0, "even_clock_rows":rows}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path)
    parser.add_argument("--pdf", type=Path, help="Verify the figure raster and re-extract cap rows.")
    args = parser.parse_args()
    if args.pdf:
        extract(args.pdf)
    with args.output.open("x", encoding="utf-8", newline="\n") as sink:
        sink.write(json.dumps(run(), indent=2)+"\n")
