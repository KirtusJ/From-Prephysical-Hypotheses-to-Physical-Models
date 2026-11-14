"""Exact count and signed success probabilities of a sharp-launch position window.

Run python check_count_flight_windows.py OUTDIR. The output must be new.
"""
import argparse
from decimal import Decimal, localcontext
import json
from math import comb
from pathlib import Path


def require(ok, message):
    if not ok:
        raise ValueError(message)


def enclose_root(value, degree):
    """Integer bounds on 2**80 times the positive degree-th root."""
    scale = 1 << 80
    target = value * scale**degree
    lo, hi = 0, 1 << ((target.bit_length() + degree - 1)//degree)
    while hi - lo > 1:
        mid = (lo + hi)//2
        if mid**degree <= target:
            lo = mid
        else:
            hi = mid
    if hi**degree == target:
        return hi, hi
    if lo**degree == target:
        return lo, lo
    require(lo**degree < target < hi**degree, "root enclosure")
    return lo, hi


def exact_window(t, p0):
    # Centre = p0*T^(9/14) and width = T^(17/28) in lattice sites.
    scale = 1 << 80
    c0, c1 = enclose_root(t**9, 14)
    w0, w1 = enclose_root(t**17, 28)
    lower = (p0*c0-w1, p0*c1-w0)
    upper = (p0*c0+w0, p0*c1+w1)
    ceiling = lambda n: -((-n)//scale)
    require(ceiling(lower[0]) == ceiling(lower[1]), "ambiguous inclusive lower endpoint")
    require(upper[0]//scale == upper[1]//scale, "ambiguous inclusive upper endpoint")
    lo, hi = ceiling(lower[0]), upper[1]//scale
    return lo, hi, dict(scale=scale, lower_numerators=lower, upper_numerators=upper)


def row(field):
    # Field entries are ordered from left to right on the single occupied parity.
    following = [[0, 0] for _ in range(len(field)+1)]
    for j, (right, left) in enumerate(field):
        following[j+1][0] = right + left
        following[j][1] = right - left
    return following


def approx(n, d):
    with localcontext() as ctx:
        ctx.prec = 15
        return str(Decimal(n)/Decimal(d))


def check_panel(t, p0, field, unsigned):
    lo, hi, cert = exact_window(t, p0)
    kept = [i for i in range(t+1) if lo <= 2*i-t <= hi]
    require(bool(kept), "empty benchmark window")
    count = sum(unsigned[i] for i in kept)
    second_count = sum(comb(t, i) for i in kept)
    require(count == second_count, "unsigned Pascal and binomial disagreement")
    square = sum(field[i][0]**2 + field[i][1]**2 for i in kept)
    total = 2**t
    require(0 < count <= total and 0 < square <= total, "probability outside the open panel")
    return dict(ticks=t, target_velocity=p0, integer_window=[lo,hi],
                occupied_endpoints=[2*kept[0]-t, 2*kept[-1]-t], occupied_sites=len(kept),
                root_certificate=cert, denominator=total, counting_numerator=count,
                signed_square_numerator=square, counting_probability=approx(count,total),
                signed_square_probability=approx(square,total),
                count_posterior_at_equal_prior=approx(count,count+square))


def checks():
    targets={32,64,128,256,512,1024}
    field, unsigned = [(1,0)], [1]
    panels=[]
    # The counts are propagated without signs, not obtained from absolute signed totals.
    for t in range(1,max(targets)+1):
        field = row(field)
        unsigned = [a+b for a,b in zip([0]+unsigned,unsigned+[0])]
        if t in targets:
            require(sum(r*r+l*l for r,l in field) == 2**t, "signed norm at saved depth")
            require(sum(unsigned) == 2**t and unsigned[0] == unsigned[-1] == 1,
                    "complete original-launch denominator")
            panels.extend(check_panel(t,p,field,unsigned) for p in (0,1,2))
    require(len(panels)==18, "depth/velocity coverage")
    by_key={(r["ticks"],r["target_velocity"]):r for r in panels}
    central,slow,fast=[by_key[1024,p] for p in (0,1,2)]
    require(central["counting_numerator"]>central["signed_square_numerator"],
            "lost stationary enrichment")
    require(slow["counting_numerator"]>slow["signed_square_numerator"],
            "lost adverse finite moving-target result")
    require(fast["counting_numerator"]<fast["signed_square_numerator"],
            "lost fixed-velocity moving control")
    return dict(scope="Exact one-terminal model weights. No clock or apparatus identification.",
                launch="Sharp site zero, right rail, fair signed Hadamard on the unwrapped line.",
                scaling="delta=T^(-5/14), w=delta^(11/10), |x/T-p0*delta|<=w.",
                rounding="Integer boundary enclosures have denominator 2^80. Probability strings use 15 significant digits; integer fractions are authoritative.",
                panels=panels)


if __name__ == "__main__":
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory",type=Path)
    directory=parser.parse_args().directory
    result=checks()
    directory.mkdir(parents=True,exist_ok=True)
    with (directory/"count_flight_windows.json").open("x",encoding="utf8",newline="\n") as out:
        json.dump(result,out,separators=(",",":"))
        out.write("\n")
