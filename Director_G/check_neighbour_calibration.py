"""Identify two directional response coefficients at the physical eraser detector.

Run python -B check_neighbour_calibration.py NEW_DIRECTORY. Test the same
right launch with timed holds or a three-swap exchange, a one-rail reference,
all retained cells, degenerate cases and inversion with distinct efficiencies.
"""
import argparse
from collections import Counter
from fractions import Fraction as F
from itertools import product
import json
from pathlib import Path

from check_parity_eraser import check, transpose
from check_parity_direction import tick


def marker(field, masses, left, right):
    sites = {x for x,_ in field} | {x for x,_ in masses}
    norm = {x:sum(field.get((x,c),0)**2 for c in (0,1)) for x in sites}
    result = Counter()
    for x in sites:
        u,v = (field.get((x,c),0) for c in (0,1))
        denominator = norm[x]+left*norm.get(x-1,0)+right*norm.get(x+1,0)
        send = F(1,2)+(F(u*v)/denominator if denominator else 0)
        incoming = sum(masses.get((x,c),0) for c in (0,1))
        check(0 <= send <= 1, "split range")
        result[x+1,0] += incoming*send
        result[x-1,1] += incoming*(1-send)
    check(sum(result.values()) == sum(masses.values()), "all launches conserved")
    return {port:m for port,m in result.items() if m}


def exchange(data):
    for a,b in [(-1,0),(0,1),(-1,0)]:
        move = {a:b,b:a}
        data = {(move.get(x,x),c):v for (x,c),v in data.items()}
    return data


def both_settings(left, right):
    field = {(2,0):1,(-1,1):1}
    masses = {port:F(1,2) for port in field}
    for _ in range(2):
        masses = marker(field,masses,left,right)
        field = tick(field)
    field, masses = transpose(field,1), transpose(masses,1)
    reference_field = {(0,0):1}
    reference = marker(reference_field,reference_field,left,right)
    check(reference == {(1,0):F(1,2),(-1,1):F(1,2)}, "efficiency reference")
    odds = []
    results = []
    for swapped in (False,True):
        a,m = (exchange(field),exchange(masses)) if swapped else (field,masses)
        check([a.get((0,c),0) for c in (0,1)] == [1,-1]
              and sum(m.get((0,c),0) for c in (0,1)) == F(1,4), "same parent")
        norms = [sum(a.get((x,c),0)**2 for c in (0,1)) for x in (-1,0,1)]
        check(norms == ([2,2,1] if swapped else [1,2,2]), "flanking norms")
        z = norms[0]*left+norms[2]*right
        output = marker(a,m,left,right)
        dark,bright = output.get((1,0),0),output.get((-1,1),0)
        check(dark+bright == F(1,4) and dark == z/(8*(2+z)), "absolute signal")
        # Test the ratio of expected counts with explicit unequal gains and brightnesses.
        eta_d,eta_b = F(2,3),F(3,7)
        raw_odds = (73*eta_d*dark)/(73*eta_b*bright)
        cal_odds = (41*eta_d*reference[1,0])/(41*eta_b*reference[-1,1])
        r = raw_odds/cal_odds
        check(0 <= r < 1 and r == z/(4+z), "calibrated pair odds")
        odds.append(r)
        cells = [[x,c,str(output.get((x,c),0))] for x,c in product(range(-5,6),(0,1))]
        check(sum(F(mass) for _,_,mass in cells) == 1,"listed all endpoints")
        results.append(dict(exchange=swapped,flanking_norms=norms,odds=str(r),cells=cells))
    z1,z2 = [4*r/(1-r) for r in odds]
    check((2*z2-z1)/3 == left and (2*z1-z2)/3 == right, "two-coefficient inverse")
    return dict(left=str(left),right=str(right),settings=results)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory",type=Path)
    dest = parser.parse_args().directory
    rates = [F(0),F(1,7),F(1),F(4),F(10**6)]
    rows = [both_settings(a,b) for a,b in product(rates,repeat=2)]
    check(len(rows) == 25,"coefficient grid")
    dest.mkdir(parents=True,exist_ok=True)
    with (dest/"neighbour_calibration.json").open("x",encoding="utf8",newline="\n") as stream:
        json.dump(rows,stream,separators=(",",":"))
        stream.write("\n")
