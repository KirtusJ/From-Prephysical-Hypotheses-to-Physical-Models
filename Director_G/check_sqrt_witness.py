"""Exact moments of a sign-coupled perturbation of the attaining threshold law."""
from fractions import Fraction as Q
import json
from math import sqrt
from pathlib import Path
from check_multigap_bias import optimum


def tent(z):
    return min(z, Q(1, 2)-z)


def tent_area(a, b):
    cuts = sorted({a, b, max(a, min(b, Q(1, 4)))})
    return sum((v-u)*(tent(v)+tent(u))/2 for u,v in zip(cuts,cuts[1:]))


def main():
    menu=json.loads((Path(__file__).parent/'results/echo_probability_map.json').read_text())['finite_menu']
    den=int(menu['mass_denominator'])
    x=sorted({Q(int(v['numerator']), den) for v in menu['routed_left_half_masks']} | {Q(1,2)})
    widths=[b-a for a,b in zip(x,x[1:])]
    t,base,_=optimum(widths)
    H=sum((widths[i-1]+widths[i])*tent(x[i])**2 for i in range(1,len(widths)))
    F=Q(0)
    floor=Q(0)
    for a,b in zip(x,x[1:]):
        h=b-a
        if h<=t:
            continue
        # Unconditional winning-threshold density equals 1/h on the two edge strips.
        F+=(tent_area(a,b-t)+tent_area(a+t,b))/h
        floor+=2*(1-t/h)*min(tent(a),tent(b))
    assert F>=floor>base and H>0
    gain=F-base
    assert gain**2 > H
    M=Q(1,10**8)
    assert M<H
    print(f"F={float(F):.12f}, floor={float(floor):.12f}, H={float(H):.12f}")
    print(f"coefficient={float(gain)/sqrt(H):.12f}, reachable={float(base)+float(gain)*sqrt(M/H):.12f}")


if __name__=='__main__':
    main()
