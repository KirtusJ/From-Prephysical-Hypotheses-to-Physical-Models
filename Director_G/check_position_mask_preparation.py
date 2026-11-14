"""Verify preparation of signed rail multisets by successive whole-position masks.

Run python check_position_mask_preparation.py OUTDIR. The output must be new.
For each kept history the sole negative edge is an L step immediately after L.
"""
import argparse
from collections import Counter
from itertools import product
import json
from math import gcd
from pathlib import Path


def require(condition, message):
    if not condition:
        raise ValueError(message)


def make_schedule(right, left):
    """At tick t keep sites x=t-2*d for the deficits d in the given set."""
    rows = []
    deficit = 0
    for rail in "LLLRLLLR":
        deficit += rail == "L"
        rows.append({0, deficit})

    walls = {0, 4, 6, 10}
    # The six L steps at closure reverse every sign in the left accumulator.
    for base, counts in ((0, left[::-1]), (6, right)):
        for number, middle in ((counts[0], (1, 2, 2, 3)), (counts[1], (1, 2, 3))):
            for _ in range(number):
                rows.extend(walls | {base + step} for step in middle)
                rows.extend((walls, walls))  # land at the wall in L, then join in R
    rows.append({4, 10})  # remove the two singleton reservoirs
    for step in range(1, 7):
        rows.append({4 + step, 10})
    return rows


def recenter(rows, target):
    """Reach the required translated input at gain +1 in R before the schedule."""
    displacement = target - (len(rows) - 20)
    if displacement >= 0:
        wire = "R" * displacement
    else:
        wire = "L" * (1 - displacement) + "R"
    if sum(a == b == "L" for a, b in zip("R" + wire, wire)) % 2:
        wire += "RLRLLR"  # zero displacement, ends in R, one LL
    offset = 0
    prefix = []
    for rail in wire:
        offset += rail == "L"
        prefix.append({offset})
    return prefix + [{d + offset for d in row} for row in rows], wire


def grouped_rails(rows):
    """Count signs using the two oriented predecessor multisets on the line."""
    field = {(0, "R"): (1, 0)}
    for allowed in rows:
        following = {}
        for d in allowed:
            for rail in "RL":
                source = d - (rail == "L")
                p, q = field.get((source, "R"), (0, 0))
                a, b = field.get((source, "L"), (0, 0))
                if rail == "L":
                    a, b = b, a
                if p + q + a + b:
                    following[d, rail] = (p + a, q + b)
        field = following
    t = len(rows)
    return Counter({(t - 2*d, rail, sign): value
                    for (d, rail), pair in field.items()
                    for sign, value in zip((1, -1), pair) if value})


def physical_histories(rows, circumference=None):
    """Extend each retained word in physical x coordinates, before applying its mask."""
    histories = [(0, "R", 1)]
    for t, row in enumerate(rows, 1):
        sites = {t - 2*d for d in row}
        if circumference:
            sites = {x % circumference for x in sites}
        surviving = []
        for x, incoming, sign in histories:
            for outgoing, dx in (("R", 1), ("L", -1)):
                y = x + dx
                if circumference:
                    y %= circumference
                if y in sites:
                    next_sign = -sign if incoming == outgoing == "L" else sign
                    surviving.append((y, outgoing, next_sign))
        histories = surviving
    return Counter(histories)


def rail_counts(counts, site):
    require(all(x == site for x, _, _ in counts), "unexpected terminal well")
    return tuple((counts[site, c, 1], counts[site, c, -1]) for c in "RL")


def check_line(right, left, target=None):
    rows = make_schedule(right, left)
    native_ticks = 15 + 6*(right[0] + left[1]) + 5*(right[1] + left[0])
    require(len(rows) == native_ticks and max(map(len, rows)) <= 5, "native clock or aperture")
    x = len(rows) - 20
    wire = ""
    if target is not None:
        rows, wire = recenter(rows, target)
        x = target
    counts = grouped_rails(rows)
    require(physical_histories(rows) == counts, "physical word/rail recurrence disagreement")
    require(rail_counts(counts, x) == (right, left), "wrong terminal multiset")
    return dict(right=right, left=left, site=x, ticks=len(rows), prefix=wire)


def three_tick_flux():
    """F(p,q)=a(p+q)+c(p-q)^2; each numerator is stored as coefficients of (a,c)."""
    settings = ((-1, 1), (-1,), (1,))
    expected = [((1, 1), (2, 0)), ((1, 0), (1, 0)), ((0, 1), (1, 0))]
    panels = []
    for first_wells, endpoints in zip(settings, expected):
        accepted, rejected = [], []
        tally = Counter()
        for word in product("RL", repeat=3):
            x = 0
            incoming = "R"
            sign = 1
            for t, outgoing in enumerate(word, 1):
                x += 1 if outgoing == "R" else -1
                if incoming == outgoing == "L":
                    sign = -sign
                incoming = outgoing
                if (t == 1 and x not in first_wells) or (t == 2 and x != 0):
                    rejected.append("".join(word))
                    break
            else:
                accepted.append(dict(word="".join(word), site=x, rail=incoming, sign=sign))
                tally[x, incoming, sign] += 1
        require(len(accepted) + len(rejected) == 8, "incomplete three-tick word list")
        # Third tick is unrestricted; these four sites exhaust its free light cone.
        deficits = [{(1-x)//2 for x in first_wells}, {1}, set(range(4))]
        require(tally == grouped_rails(deficits), "three-tick masked tally disagrees")
        cells = []
        for (x, rail), (p, q) in zip(((-1, "L"), (1, "R")), endpoints):
            require((tally[x, rail, 1], tally[x, rail, -1]) == (p, q), "three-tick named port")
            cells.append(dict(site=x, rail=rail, multiset=(p, q),
                              score_coefficients=(p+q, (p-q)**2)))
        require(sum(p+q for p, q in endpoints) == len(accepted), "unaccounted terminal port")
        total = tuple(sum(cell["score_coefficients"][i] for cell in cells) for i in range(2))
        require(total == ((4, 4) if len(first_wells) == 2 else (2, 2)), "launch denominator")
        panels.append(dict(first_wells=first_wells, accepted=accepted, rejected_words=rejected,
                           cells=cells, accepted_score_coefficients=total))
    return dict(second_wells=[0], third_wells="unrestricted",
                initial_port=[0, "R"], coefficient_order=["a", "c"],
                per_launch_denominator="8*(a+c), where a+c=F(1,0)>0", panels=panels)


def checks():
    tick_counts = Counter()
    for p, q, r, s in product(range(4), repeat=4):
        case = check_line((p, q), (r, s))
        tick_counts[case["ticks"]] += 1
    require(sum(tick_counts.values()) == 256, "incomplete line grid")

    target = ((2, 0), (1, 2))
    origin = len(make_schedule(*target)) - 20
    fixed_sites = [check_line(*target, target=origin + shift) for shift in (0, 3, -1, -2)]
    require(any(c["prefix"].endswith("RLRLLR") for c in fixed_sites), "missing signed prefix")

    # Admit one additional physical site a second time near the source reservoir.
    # This adds a canceling pair at exactly the same final port as the original path.
    leaked = make_schedule((1, 0), (0, 0))
    require(7 not in leaked[9], "leak control is already admitted")
    leaked[9] = leaked[9] | {7}
    bad = grouped_rails(leaked)
    require(bad == physical_histories(leaked), "leak control oracles disagree")
    after = rail_counts(bad, len(leaked) - 20)
    require(after == ((2, 1), (0, 0)), "leak control did not add a canceling pair")

    cyclic = []
    for n in (4, 12, 16, 18, 20, 21, 22, 23, 24, 25, 26, 32):
        failures = []
        for p, q, r, s in product(range(2), repeat=4):
            target = (p, q), (r, s)
            rows = make_schedule(*target)
            x = (len(rows) - 20) % n
            observed = rail_counts(physical_histories(rows, n), x)
            if observed != target:
                failures.append(dict(target=target, observed=observed, ticks=len(rows)))
        period = n // gcd(n, 2)
        if period > 11:
            require(not failures, "alias inside the guaranteed ring range")
        if n == 20:
            require(len(failures) == 16, "missing adverse ring control")
        cyclic.append(dict(circumference=n, deficit_period=period, cases=16, failures=failures))

    return dict(scope="Whole-position product masks on the signed walk. Counts are ordered (+,-).",
                line_grid=dict(multiplicities=[0, 1, 2, 3], cases=256,
                               cases_by_depth=sorted(tick_counts.items())),
                named=[check_line((0, 0), (0, 0)), check_line((1, 0), (0, 0)),
                       check_line((0, 0), (0, 1)), check_line((31, 11), (17, 5))],
                fixed_sites=fixed_sites,
                leak=dict(tick=10, added_deficit=7, physical_site=-4,
                          target=((1, 0), (0, 0)), observed=after),
                rings=cyclic, three_tick_flux=three_tick_flux())


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path)
    output_dir = parser.parse_args().directory
    result = checks()
    output_dir.mkdir(parents=True, exist_ok=True)
    with (output_dir / "position_mask_preparation.json").open("x", encoding="utf8", newline="\n") as out:
        json.dump(result, out, separators=(",", ":"))
        out.write("\n")
