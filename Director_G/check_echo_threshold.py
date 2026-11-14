"""Exact controls for a binary pulse threshold and an unidentifiable detector pair."""
from argparse import ArgumentParser
from fractions import Fraction as Q
from itertools import product
import json
from pathlib import Path

from check_binary_echo import adjoint, compose, norm, one, phase_checks, z, zero


def require(condition, message):
    if not condition:
        raise ValueError(message)


def update(x, target):
    return 1-(1-x)**3 if target else x**3


def round_word(x, threshold, depth):
    word = []
    for _ in range(depth):
        up = threshold <= Q(1,2)
        word.append(int(up))
        threshold = update(threshold, up)
        x = update(x, up)
    return tuple(word), x, threshold


def detector(x, sign):
    # Odd about 1/2; linear on the legs of the lower tent.
    if x > Q(1,2):
        return 1-detector(1-x, sign)
    bump = max(0, Q(1,16)-2*abs(x-Q(1,4)))
    return x+sign*bump


def exact_checks():
    phase_checks()
    d0, d1 = ((z,zero),(zero,one)), ((one,zero),(zero,z))
    v = (((0,Q(3,5)),(0,Q(-4,5))),((Q(4,5),0),(Q(3,5),0)))
    initial = norm(v[1][0])
    rows = []
    for choices in product((0,1), repeat=3):
        gate = v
        x = initial
        for target in choices:
            select = d1 if target else d0
            gate = compose(gate, compose(d0, compose(adjoint(gate), compose(select, gate))))
            x = update(x, target)
            require(norm(gate[1][0]) == x, "two-target unitary polynomial")
        rows.append({"targets": choices, "nonblank_mass": str(x)})

    n, depth = 8, 4
    examples = {}
    for x in (Q(1,32),Q(1,4),Q(7,16),Q(15,16)):
        tally = []
        for j in range(n):
            t = Q(2*j+1,2*n)
            word, s, nominal = round_word(x,t,depth)
            require((x < t) == (s < nominal), "threshold order")
            for y in (x,s):
                plus,minus = detector(y, 1),detector(y, -1)
                require(0 <= plus <= 1 and 0 <= minus <= 1 and plus+minus == 2*y,
                        "hidden curves reproduce all single-program means")
            tally.append({"threshold":str(t), "word":word, "nonblank_mass":str(s)})
        examples[str(x)] = tally

    a,b = Q(1,4),Q(17,64)
    c,d = Q(15,64),Q(1,4)
    require(detector(a,1)>detector(b,1) and detector(c,-1)>detector(d,-1),
            "both continuous curves strictly decrease on an interval")
    r1,r2=detector(a,1),detector(a,-1)
    rr=(r1*r1+r2*r2)/2
    ra=(r1+r2)*a/2
    require(rr-2*ra+a*a == Q(1,256),"same-type paired reference contrast")
    summaries={}
    for x in (Q(1,32),Q(1,4),Q(7,16),Q(15,16)):
        tgrid = [Q(2*j+1,2*n) for j in range(n)]
        lower=Q(sum(t<x for t in tgrid),n)
        upper=Q(sum(t<=x for t in tgrid),n)
        require(lower <= upper and max(abs(lower-x),abs(upper-x))<=Q(1,2*n),
                "grid tie interval")
        summaries[str(x)] = [str(lower),str(upper)]
    return {"three_layers":rows, "depth_four":examples, "grid_limits":summaries,
            "paired_contrast":str(rr-2*ra+a*a)}


if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("output",type=Path)
    result = exact_checks()
    with parser.parse_args().output.open("x", encoding="utf8",newline="\n") as dest:
        json.dump(result,dest,indent=2)
        dest.write("\n")
