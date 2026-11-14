"""Replay the four-tick position reference appended to a retained walk output."""
import argparse
from collections import Counter
from fractions import Fraction as F
from itertools import product
import json
from pathlib import Path

OFFSETS = (-4, -2, 0, 2, 4)
MASS = (1, 2, 2, 10, 1)
WORDS = (1, 4, 6, 4, 1)


def shift(site, direction, length):
    if 0 <= site+direction < length:
        return site+direction, direction
    return site, -direction


def panel(length, start, ticks=4):
    signed, unsigned = Counter(), Counter()
    for directions in product((1, -1), repeat=ticks):
        x, rail = start
        sign = 1
        for d in directions:
            sign *= -1 if rail == d == -1 else 1
            x, rail = shift(x, d, length)
        signed[x, rail] += sign
        unsigned[x, rail] += 1
    return signed, unsigned


def fold(j, length):
    j %= 2*length
    return min(j, 2*length-1-j)


def summed(values, squared):
    site = Counter()
    for (x, rail), v in values.items():
        site[x] += v*v if squared else v
    return site


def joint_example():
    # Three free science ticks, a persistent copy of both coordinates, and
    # four appended ticks. Enumerate the whole physical flight a second way.
    length, seed = 7, (3,1)
    science, _ = panel(length, seed, ticks=3)
    bank = {(None, *seed):1}
    for tick in range(1,8):
        following = Counter()
        for (old,x,r), amplitude in bank.items():
            for d in (1,-1):
                y,s = shift(x,d,length)
                tag = (y,s) if tick == 3 else old
                following[tag,y,s] += amplitude * (-1 if r == d == -1 else 1)
        bank = following
    cells = Counter()
    for (old,x,r), v in bank.items():
        cells[old,x] += v*v
    assert sum(cells.values()) == 128
    output = []
    for (x,r), a in sorted(science.items()):
        ys = [fold(x+r*j,length) for j in OFFSETS]
        joint = [cells[(x,r),y] for y in ys]
        assert joint == [a*a*n for n in MASS]
        output.append({"origin":[x,r],"signed_prefix":a,"final_wells":ys,
                       "joint_numerators_over_128":joint})
    return output


def powered(weights, q):
    values = [x**q if x else F(0) for x in weights]
    return [F(v,sum(values)) for v in values]


def run():
    checked = []
    for length in range(5,49):
        for x in range(length):
            for r in (1,-1):
                sites = [fold(x+r*j,length) for j in OFFSETS]
                assert len(set(sites)) == 5
                a,n = panel(length,(x,r))
                assert summed(a,True) == dict(zip(sites,MASS))
                assert summed(n,False) == dict(zip(sites,WORDS))
        checked.append({"length":length,"directed_starts":2*length})
    smaller = {}
    for t in (1,2,3):
        a,_ = panel(11,(5,1),t)
        smaller[t] = sorted(summed(a,True).values())
        assert len(set(smaller[t])) <= 2
    alias,_ = panel(4,(0,1))
    assert summed(alias,True) == {0:2,1:2,2:10,3:2}
    # A detector sorting the rails before applying its power can evade the
    # entire position histogram when one forgets the retained prefix.
    signed,_ = panel(11,(5,1))
    fine = sorted(signed)
    rare, other = F(9,20), F(11,20)
    p0,p2 = (powered([signed[i]**2 for i in fine],q) for q in (0,2))
    suffix = Counter()
    for i,a,b in zip(fine,p0,p2):
        suffix[i[0]-5] += rare*a+other*b
    assert [suffix[j] for j in OFFSETS] == [F(m,16) for m in MASS]
    witness = [F(1,4),F(3,4)]
    altered = [rare*a+other*b for a,b in zip(powered(witness,0),powered(witness,2))]
    assert altered == [F(7,25),F(18,25)]
    return {"suffix_displacements":OFFSETS, "squared_numerators_over_16":MASS,
            "unsigned_counts":WORDS, "checked_boundary_sizes":checked,
            "through_three_ticks_interior":smaller, "aliased_four_well_example":summed(alias,True),
            "seven_tick_joint_experiment":joint_example(),
            "hidden_rail_counterexample":{
                "powers":[0,2], "population":[str(rare),str(other)],
                "pooled_reference":[str(suffix[j]) for j in OFFSETS],
                "science_mass":[str(x) for x in witness], "science_rates":[str(x) for x in altered]}}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output",type=Path)
    args = parser.parse_args()
    result = run()
    with args.output.open("x",encoding="utf-8",newline="\n") as output:
        output.write(json.dumps(result,indent=2)+"\n")
