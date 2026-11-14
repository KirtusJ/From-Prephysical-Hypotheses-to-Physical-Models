"""Run python -B check_equal_clock_lags.py NEW_DIRECTORY (standard library).

Use position masks on the 4M-ring, one sharp R input and the same final
(home,R) port and clock in every lag setting at each order. Keep all
surviving signed sheet bins; a residue collision retains its multiplicity.
"""
import argparse
from collections import Counter
from fractions import Fraction
import json
from math import cos, gcd, pi
from pathlib import Path


def require(test, message):
    if not test:
        raise ValueError(message)


def branches(lag):
    if lag % 2 == 0:
        common = "R" * ((lag-4)//2)
        return "RR"+common+"LLR", "LL"+common+"RRR"
    k = (lag-9)//2
    common = "R"*(k-1)+"L"
    return "RR"+common+"RLLLR", "LL"+common+"LRRRR"


def path(word, home):
    x, gain, sign, rail = home, 0, 1, "R"
    sites = []
    for move in word:
        gain += x//2
        if rail == move == "L":
            sign = -sign
        x += 1 if move == "R" else -1
        sites.append(x)
        rail = move
    return sites, gain, sign


def return_to_home(words, clock):
    x = words[0].count("R") - words[0].count("L")
    remaining = clock-len(words[0])
    require(remaining >= abs(x+1)+1 and (remaining-x) % 2 == 0, "return timing")
    right = (remaining-x)//2
    suffix = "L"*(remaining-right) + "R"*right
    require(right >= 1, "terminal rail")
    return [w+suffix for w in words]


def ring_filter(masks, order, circumference, home):
    """Forward propagation uses both outgoing arcs at every admitted site."""
    counts = Counter({(home % circumference, "R", 0, 1): 1})
    for mask in masks:
        allowed = {x % circumference for x in mask}
        following = Counter()
        for (x, rail, gain, sign), n in counts.items():
            phase = (gain + x//2) % order
            for move, delta in (("R", 1), ("L", -1)):
                y = (x+delta) % circumference
                if y in allowed:
                    s = -sign if rail == move == "L" else sign
                    following[y, move, phase, s] += n
        counts = following
    return counts


def setting(order, circumference, home, lag, clock):
    words = return_to_home(branches(lag), clock)
    first, second = (path(w, home) for w in words)
    require(first[0][-1] == second[0][-1] == home and
            first[2] == second[2] and first[1]-second[1] == lag, "line word phases")
    masks = list(zip(first[0], second[0]))
    actual = ring_filter(masks, order, circumference, home)
    intended = Counter((home % circumference, "R", phase % order, sign)
                       for _, phase, sign in (first, second))
    return actual, intended, [first[1], second[1]], first[2]


def scan(order):
    lags = [13 + (r-13) % order for r in range(order)]
    # Need the final step to be R. A common even clock puts all endpoints
    # back on the launch parity, including when the launch is seam-adjacent.
    min_ticks = []
    for lag in lags:
        w, _ = branches(lag)
        x = w.count("R")-w.count("L")
        min_ticks.append(len(w)+abs(x+1)+1)
    clock = max(min_ticks)
    require(clock % 2 == 0, "common even return clock")
    size = 4*order
    by_home = []
    for home in (0, size-1):
        settings = []
        for r, lag in enumerate(lags):
            actual, intended, phases, sign = setting(order, size, home, lag, clock)
            require(actual == intended and sum(actual.values()) == 2, "extra or missing ring word")
            settings.append(dict(residue=r, lag=lag, line_gains=phases, common_sign=sign,
                                 surviving_bins=[[*key,n] for key,n in sorted(actual.items())]))
        by_home.append(dict(physical_home=home, settings=settings))

    # Cosine decreases with folded residue from 0 through floor(M/2).
    # This ranks all exact rates without rounding near a tied maximum.
    peaks = []
    for s in range(order//2+1):
        folded = [min((s*r) % order, (-s*r) % order) for r in range(1,order)]
        winners = [r for r, f in enumerate(folded,1) if f == min(folded)]
        nonflat = s != 0  # Compare all settings, including the zero lag.
        require((nonflat and 1 in winners) == (s == 1), "ordinary lag selection")
        if gcd(s,order) == 1:
            require(len(winners) == 2 and all((s*r) % order in (1,order-1) for r in winners),
                    "primitive-class peaks")
        elif s:
            require(all((s*r) % order == 0 for r in winners), "nonprimitive alias")
        peaks.append(dict(frequency=s, maximum_nonzero_lags=winners, flat=not nonflat))
    prefactor = Fraction(2, 2**clock)
    # For s=1, counting is flat at the prefactor, while the zero-frequency
    # squared score is flat at twice that rate. With fewer than four
    # residues every nonzero lag is already in {+1,-1}.
    gap = float(prefactor)*(cos(2*pi/order)-cos(4*pi/order)) if order >= 4 else None
    return dict(order=order, circumference=size, ticks=clock, homes=by_home, peaks=peaks,
                count_rate=str(prefactor), coherent_zero_lag_rate=str(2*prefactor),
                ordinary_to_runner_up_gap_approx=gap)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path)
    out = parser.parse_args().directory/"equal_clock_lags.json"
    if out.exists():
        parser.exit(2, f"Refusing to overwrite {out}\n")
    scans = [scan(m) for m in (3,4,5,6,7,8,9,10,12,15,16,17,21,32,64)]
    # On a too-small ring the two masks can admit extra words. Keep both
    # the actual and intended answers, including a small ring that works.
    boundaries = []
    for order in (1,2,3):
        actual, intended, _, _ = setting(order, 4*order, 0, 13, 12)
        boundaries.append(dict(order=order, lag=13, ticks=12,
                               actual=[[*k,n] for k,n in sorted(actual.items())],
                               intended=[[*k,n] for k,n in sorted(intended.items())]))
    require(sum(row[-1] for row in boundaries[0]["actual"]) != 2, "four-site alias control")
    result = dict(scans=scans, small_ring_controls=boundaries,
                  bin_columns=["physical site","terminal rail","sheet residue","word sign","multiplicity"],
                  coherent_rate="count_rate * (1 + cos(2*pi*s*r/order))")
    out.parent.mkdir(parents=True,exist_ok=True)
    with out.open("x",encoding="utf-8",newline="\n") as f:
        json.dump(result,f,separators=(",",":"),allow_nan=False)
        f.write("\n")


if __name__ == "__main__":
    main()
