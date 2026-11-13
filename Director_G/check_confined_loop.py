"""Confined complementary paths with a balanced, reversible force clock.

Run python -B check_confined_loop.py OUTPUT_DIRECTORY. Only the standard
library is used. All finite path, signed state, and rounding checks are exact.
"""

import argparse
import json
from collections import Counter
from fractions import Fraction
from itertools import pairwise, product
from math import pi
from pathlib import Path


def peak(a, r):
    """Largest signed departure area of a returning 2a-step path in [-r,r]."""
    j = min(a, r)
    return j * j + (a - j) * (2 * j - 1)


def lobe_limits(a, r):
    if a == 0:
        return 0, 0
    return 2 * a - 1 - peak(a - 1, r + 1), peak(a, r)


def extrema(a, r):
    b, c = a // 2, (a + 1) // 2
    return tuple(sum(pair) for pair in zip(lobe_limits(b, r), lobe_limits(c, r)))


def span_bound(a, span):
    if span == 0:
        return 0
    # Each edge of the occupied interval is used at least once upwards.
    # The largest extra crossing cost |j-mid|+|j+1-mid| is 1 at span=1.
    return (span * span + 1) // 2 + (a - span) * max(1, span - 1)


def heights(word):
    result = [0]
    for step in word:
        result.append(result[-1] + step)
    return result


def balanced_fields_for_area(departures, target):
    """Use the a largest slots, then exchange selected indices downward."""
    slots = sorted(range(len(departures)), key=departures.__getitem__)
    a = len(slots) // 2
    selected = list(range(a, 2 * a))
    area = 2 * sum(departures[slots[i]] for i in selected) - sum(departures)
    assert -area <= target <= area and (area - target) % 2 == 0
    for j in range(a):
        while area > target and selected[j] > j:
            i = selected[j]
            difference = departures[slots[i]] - departures[slots[i - 1]]
            assert difference in (0, 1)
            selected[j] -= 1
            area -= 2 * difference
    assert area == target and len(set(selected)) == a
    fields = [-1] * len(slots)
    for i in selected:
        fields[slots[i]] = 1
    assert sum(fields) == 0 and sum(f * z for f, z in zip(fields, departures)) == target
    return fields


def brute():
    rows = []
    for a in range(9):
        for r in range(1, min(5, a + 1) + 1):
            count = 0
            balanced = {}
            lobes = set()
            odd_span_slack = {}
            for word in product((-1, 1), repeat=2 * a):
                if sum(word):
                    continue
                path = heights(word)
                if max(map(abs, path)) > r:
                    continue
                count += 1
                levels = sorted(path[:-1])
                ranked = sum(levels[a:]) - sum(levels[:a])
                mid2 = min(path) + max(path)
                centered2 = sum(abs(2 * z - mid2) for z in levels)
                span = max(path) - min(path)
                assert 2 * ranked <= centered2 <= 2 * span_bound(a, span)
                balanced[span] = max(balanced.get(span, 0), ranked)
                odd_span_slack[span] = min(
                    odd_span_slack.get(span, centered2 - 2 * ranked), centered2 - 2 * ranked
                )
                if not word or word[0] == 1 and word[-1] == -1:
                    lobes.add(sum(levels))
            lo, hi = lobe_limits(a, r)
            assert lobes == set(range(lo, hi + 1, 2))
            d = min(a, 2 * r)
            assert max(balanced.values()) == extrema(a, r)[1] == span_bound(a, d)
            best = span_bound(a, d)
            maximizer, _ = build(a, r, best)
            for target in range(-best, best + 1, 2):
                balanced_fields_for_area(heights(maximizer)[:-1], target)
            rows.append(
                {
                    "half_ticks": a,
                    "radius": r,
                    "confined_returns": count,
                    "area_range_R_to_L": [lo, hi, 2],
                    "same_word_balanced_area_range": [-best, best, 2],
                    "best_balanced_by_span": balanced,
                    "midpoint_envelope_by_span": {s: span_bound(a, s) for s in balanced},
                    "min_twice_midpoint_minus_ranked_by_span": odd_span_slack,
                }
            )
    return rows


def lobe(a, r, target):
    """Start with the top envelope. Each local peak flip takes away area two."""
    lo, hi = lobe_limits(a, r)
    assert lo <= target <= hi and (target - hi) % 2 == 0
    if not a:
        return []
    j = min(a, r)
    word = [1] * j + [-1, 1] * (a - j) + [-1] * j
    path = heights(word)
    need = (hi - target) // 2
    while need:
        old = need
        # Keep first/last steps; never dip below -r.
        for t in range(2, 2 * a - 1):
            if path[t] == path[t - 1] + 1 == path[t + 1] + 1 and path[t] - 2 >= -r:
                path[t] -= 2
                need -= 1
                if not need:
                    break
        assert need < old
    out = [v - u for u, v in pairwise(path)]
    assert sum(path[:-1]) == target and (out[0], out[-1]) == (1, -1)
    return out


def build(a, r, d):
    b, c = a // 2, (a + 1) // 2
    blo, bhi = lobe_limits(b, r)
    clo, chi = lobe_limits(c, r)
    db = min(bhi, d - clo)
    dc = d - db
    assert blo <= db <= bhi and clo <= dc <= chi
    first = lobe(b, r, db)
    second = [-s for s in lobe(c, r, dc)]
    # For n=4b+2 mark the zero departure at the start of the longer lobe.
    signs = [1] * len(first) + [-1] * len(second)
    if b < c:
        signs[len(first)] = 1
    reference = first + second
    assert sum(signs) == 0
    path = heights(reference)
    assert path[-1] == 0 and max(map(abs, path)) <= r
    assert sum(s * z for s, z in zip(signs, path)) == d
    return reference, signs


def smallest(r, d):
    # A nonempty two-lobe program starts R and finishes R. Lower endpoint
    # can be positive for tight r; do not use a monotone objective on its own.
    a = 2
    while True:
        lo, hi = extrema(a, r)
        if lo <= d <= hi and (a - d) % 2 == 0:
            return a
        a += 1


def nearest(m):
    q, rem = divmod(m, 8)
    if rem == 4:
        return [q, q + 1]
    return [q + int(rem > 4)]


def radius_choice(m):
    # Round M^(3/8) without floating point.
    r = 1
    while (2 * r + 1) ** 8 < 2**8 * m**3:
        r += 1
    return r


def literal(m, r, d, a):
    word, signs = build(a, r, d)
    assert word[0] == word[-1] == 1
    initial = {(-3, 1, 3): 2, (0, 1, 1): -3, (4, 1, 0): 1, (0, -1, 1): 2, (4, -1, 1): -1}
    records = []
    for mode in ("calibrated", "reverse_calibration", "negative_lobe_not_reflected", "constant_field"):
        directions = word
        fields = signs
        if mode == "calibrated":
            fields = [-f for f in signs]
        elif mode == "negative_lobe_not_reflected":
            cut = 2 * (a // 2)
            directions = word[:cut] + [-j for j in word[cut:]]
        elif mode == "constant_field":
            fields = [1] * len(word)
        pos = heights(directions)
        common = sum(fields)
        arm = sum(f * z for f, z in zip(fields, pos))
        assert pos[-1] == 0 and max(map(abs, pos)) <= r
        state = initial
        for t, (step, field) in enumerate(zip(directions, fields)):
            new = Counter()
            for (x, c, y), v in state.items():
                outs = (1, -1) if t == 0 else (c * step * directions[t - 1],)
                for rail in outs:
                    sign = -1 if t == 0 and rail == c == -1 else 1
                    new[x + rail, rail, (y + field * x) % m] += sign * v
            state = {k: v for k, v in new.items() if v}
        want = Counter()
        for (x, c, y), v in initial.items():
            for s in (1, -1):
                sign = -1 if s == c == -1 else 1
                want[x, directions[-1] * s, (y + common * x + s * arm) % m] += sign * v
        assert state == {p: v for p, v in want.items() if v}
        assert sum(v * v for v in state.values()) == 2 * sum(v * v for v in initial.values())
        # exp(-i h y): L/R = exp(-i h * (yL-yR)).
        delta_gain = -2 * directions[-1] * arm
        if mode == "calibrated":
            assert common == 0 and delta_gain == 2 * d
        elif mode == "reverse_calibration":
            assert common == 0 and delta_gain == -2 * d
        records.append(
            {
                "mode": mode,
                "common_gain_slope": common,
                "L_minus_R_gain": delta_gain,
                "complete_signed_output": [[*key, v] for key, v in sorted(state.items())],
            }
        )
    return records


def main():
    census = brute()
    small = []
    for m in range(3, 257):
        for r in (1, 2, 3, 5):
            for d in nearest(m):
                a = smallest(r, d)
                build(a, r, d)
                small.append([m, r, d, a])
    scales = []
    for m in (
        3,
        4,
        5,
        8,
        12,
        16,
        31,
        32,
        33,
        63,
        64,
        65,
        127,
        128,
        129,
        512,
        4096,
        32768,
        262144,
        2097152,
    ):
        r = radius_choice(m)
        delta = (2 * pi / m) ** 0.25
        for d in nearest(m):
            a = smallest(r, d)
            n = 2 * a
            R = r * delta**2
            T = n * delta**3
            word, _ = build(a, r, d)
            scales.append(
                {
                    "M": m,
                    "d": d,
                    "radius_cap": r,
                    "n": n,
                    "tight_area_at_n": extrema(a, r)[1],
                    "R_cap": R,
                    "actual_R": max(map(abs, heights(word))) * delta**2,
                    "T": T,
                    "cap_R_times_T_over_delta": R * T / delta,
                    "speed": 1 / delta,
                    "fixed_c1_elapsed_at_least": n * delta**2,
                    "angle_error_turns": str(abs(Fraction(2 * d, m) - Fraction(1, 4))),
                    "modes": literal(m, r, d, a),
                }
            )
    return {
        "convention": "Moving on every tick with a real initial H then programmed global I or X rail routing; site gain f_t*x at departure, f_t=+1 or -1. Fully coherent supplied field reversal changes the generator. The native-H selective instrument in the companion requires heralding and is not simulated here.",
        "balanced_bound": "n=2a; a returning path visits each directed edge equally upwards and downwards. With span D and midpoint u, each edge j contributes h_j=|j-u|+|j+1-u| per up/down pair. One obligatory crossing per edge sums to ceil(D²/2). Remaining a-D crossings contribute at most max(1,D-1) each for D>=1. Every balanced sign assignment has signed area <= sum |z_t-u|. For fixed path its maximum is sum of the largest a departures minus the smallest a (median). The envelope is nondecreasing in D>=1 up to a, including the D=1 to D=2 equality for a>=2. Take D=min(2r,a). Upper/lower reflected lobes with half-lengths floor(a/2),ceil(a/2) attain the balanced bound, flipping the field at the first zero departure of the longer lobe to balance slots if needed.",
        "two_lobes": "For lobe half-length b radius r, P(b,r)=j²+(b-j)(2j-1), j=min(b,r). The pointwise top path rises to j, bounces until its descent to zero. Bottom R-start L-end path is the reflection about height 1 of the top interior path of half-length b-1 with upper radius r+1; it stays below +r. Allowed signed areas range in steps of two from 2b-1-P(b-1,r+1) to P(b,r). A downward local peak flip takes area two until the bottom path is reached. Since the two lobe intervals add, attainable compensated areas in this family have parity a. Earliest tabulated n is within this R-start R-end two-lobe family; other circuits can realize small targets earlier.",
        "physical_units": "epsilon=delta, h=2pi/M=delta^4 (F=1), lattice distance delta², tick delta³. Every two returning branches in radius r have relative gain <=2nr even with a common signed force. Approaching quarter phase implies (r delta²)(n delta³)>= (pi/4-o(1))delta. Taking r asymptotic to a constant times delta^(-3/2) and n asymptotic to M/(8r) makes both physical radius and physical elapsed time of order sqrt(delta), with zero common momentum kick. A fixed physical speed c with unchanged phase per hop requires per-slot time >=delta²/c, hence RT>=pi/(4c)-o(1). Retiming a physical field that couples over elapsed time can change h and is a separate model. Neither pulse switches nor the physical sheet increment are costed.",
        "root_order_controls": "Nearest positive unwrapped d to M/8 including both tie choices. Exact quarter iff 8 divides M. Reversing all signs conjugates the output, missing the spatial reflection or missing field reversal changes the program. Coherent projected rail read uses L/R=exp(-2ihd) in the calibrated setting; common momentum slope zero for all initial sites.",
        "exhaustive_census": census,
        "small_columns": ["M", "r", "d", "first_two_lobe_half_length"],
        "small_programs": small,
        "scalable_literal_checks": scales,
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("directory", type=Path)
    directory = parser.parse_args().directory
    result = main()
    directory.mkdir(parents=True, exist_ok=True)
    (directory / "confined_loop.json").write_text(
        json.dumps(result, separators=(",", ":")) + "\n", encoding="utf8"
    )
    print(
        len(result["exhaustive_census"]),
        "censuses;",
        len(result["small_programs"]),
        "calibrations;",
        len(result["scalable_literal_checks"]),
        "literal cases.",
    )
