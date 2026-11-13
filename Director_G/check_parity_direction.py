"""Verify the one-swap direction record. Run python -B check_parity_direction.py OUTDIR."""

import argparse
from collections import Counter
from fractions import Fraction
from itertools import product
import json
from pathlib import Path


PREDICATES = [
    "At each active depth 1 through 8 test the decoded physical amplitude at every port against direct tagged path enumeration.",
    "For all eight horizons retain the matched blind hold, the on-site marker and the radius-one marker, including dark ports.",
    "For both isolated sharp rails verify equality of local and neighbouring-site marker predictions at all eight depths.",
    "After the swap test the native-depth-three blind cancellation and the depth-four tagged left detector against exact rational predictions.",
]


def tick(amps):
    out = Counter()
    for (site, rail), amp in amps.items():
        out[site+1, 0] += amp
        out[site-1, 1] += amp if rail == 0 else -amp
    return {port: value for port, value in out.items() if value}


def words(ticks):
    counts = Counter()
    for rails in product(range(2), repeat=ticks):
        neg = sum(left == right == 1 for left, right in zip(rails, rails[1:]))
        site = ticks-2*sum(rails)
        counts[1-rails[0], site, rails[-1]] += (-1)**neg
    return counts


def marker_step(amps, masses, radius):
    out = Counter()
    sites = {y for y, _ in masses} | {y for y, _ in amps}
    norm = {y: sum(amps.get((y,c), 0)**2 for c in range(2)) for y in sites}
    for y in sites:
        incoming = sum(masses.get((y,c), 0) for c in range(2))
        denominator = sum(norm.get(z,0) for z in range(y-radius,y+radius+1))
        right = Fraction(1,2)
        if denominator:
            right += Fraction(amps.get((y,0),0)*amps.get((y,1),0), denominator)
        assert 0 <= right <= 1
        out[y+1,0] += incoming*right
        out[y-1,1] += incoming*(1-right)
    assert sum(out.values()) == sum(masses.values())
    return {port: p for port,p in out.items() if p}


def sharp_control(site, rail, horizon):
    amps = {(site,rail): 1}
    masses = {(site,rail): Fraction(1)}
    for h in range(horizon):
        square = {p: Fraction(v*v, 2**h) for p,v in amps.items()}
        assert masses == square
        assert marker_step(amps,masses,0) == marker_step(amps,masses,1)
        masses = marker_step(amps,masses,1)
        amps = tick(amps)


def run():
    physical = {(2,0): 1, (-1,1): 1}
    blank = tick({(0,0): 1})
    onsite = {p: Fraction(1,2) for p in physical}
    neighbour = onsite.copy()
    rows = []
    for t in range(1,9):
        tagged = words(t)
        h = t-1
        expected_physical = {(x+b,c): v for (b,x,c),v in tagged.items() if v}
        assert physical == expected_physical
        expected_blind = Counter()
        for (b,x,c),v in tagged.items():
            expected_blind[x,c] += v
        assert blank == {p:v for p,v in expected_blind.items() if v}
        assert onsite == {p: Fraction(v*v,2**t) for p,v in physical.items() if v}
        assert all(sum(p for (y,c),p in neighbour.items() if (y-h)%2 == parity) ==
                   Fraction(1,2) for parity in range(2))
        records = []
        for y in range(-t,t+2):
            b = int((y-h)%2 == 0)
            for c in range(2):
                assert physical.get((y,c),0) == tagged.get((b,y-b,c),0)
                records.append([y,c,b,y-b,physical.get((y,c),0),
                                str(onsite.get((y,c),0)),str(neighbour.get((y,c),0)),
                                blank.get((y,c),0)])
        if t == 3:
            assert blank.get((-1,1),0) == 0
            assert physical[-1,1] == 1 and physical[0,1] == -1
            assert onsite[-1,1] == onsite[0,1] == Fraction(1,8)
            assert [physical.get((2,c),0) for c in range(2)] == [1,1]
            assert [physical.get((1,c),0) for c in range(2)] == [1,0]
            assert [physical.get((3,c),0) for c in range(2)] == [0,0]
        if t == 4:
            assert onsite.get((1,1),0) == 0
            assert neighbour.get((1,1),0) == Fraction(1,24)
        rows.append({"native_ticks":t, "timestamps_including_route_or_hold":t+1,
                     "records":records})
        onsite = marker_step(physical,onsite,0)
        neighbour = marker_step(physical,neighbour,1)
        physical,blank = tick(physical),tick(blank)
    sharp_control(2,0,8)
    sharp_control(-1,1,8)
    return {"predicates":PREDICATES,
            "first_run_correction": "The first oracle assertion assigned the two opposite t=3 left-rail signs in reverse. The explicit LRL and RLL words give +1 at y=-1 and -1 at y=0. The blind sum and both squared masses are unchanged.",
            "columns":["physical site","rail (0=R)","decoded first R bit",
                       "logical site","routed raw tally","onsite mass","radius-one mass",
                       "blind raw tally at same physical site/rail"],
            "denominator_for_raw_squares":"2^native_ticks",
            "panels":rows}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("outdir",type=Path)
    folder = parser.parse_args().outdir
    result = run()
    folder.mkdir(parents=True,exist_ok=True)
    with (folder/"parity_direction.json").open("x",encoding="utf8",newline="\n") as f:
        json.dump(result,f,indent=1)
        f.write("\n")


if __name__ == "__main__":
    main()
