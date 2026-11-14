"""Exact bounds for a scalar-mask echo and two independent direct flag trials."""
from argparse import ArgumentParser
from bisect import bisect_right
from fractions import Fraction as Q
from itertools import pairwise
import json
from math import isqrt
from pathlib import Path

from check_coin_uniform_masks import from_below, scalar_shells, transfer


HALF = Q(1, 2)
PRECISION = 10**12


def require(condition, message):
    if not condition:
        raise ValueError(message)


def logistic(p):
    return 4 * p * (1-p)


def square(p):
    return p*p / (p*p+(1-p)**2)


def sharp_step(p):
    return HALF if p == HALF else Q(p > HALF)


def enclosure(p):
    lower, rem = divmod(p.numerator * PRECISION, p.denominator)
    return [lower, lower + int(rem != 0)]


def sqrt_enclosure(p):
    # Integer endpoints enclose PRECISION times the true square root.
    num = p.numerator * PRECISION**2
    lo = isqrt(num//p.denominator)
    return lo, lo+int(lo*lo*p.denominator != num)


def menu_gaps(points):
    angles = []
    for x,y in pairwise(points):
        plus_lo,plus_hi = sqrt_enclosure(y*(1-x))
        minus_lo,minus_hi = sqrt_enclosure(x*(1-y))
        angles.append((plus_lo-minus_hi,plus_hi-minus_lo))
    max_sin_lower = max(lo for lo,_ in angles)
    max_sin_upper = max(hi for _,hi in angles)
    return dict(left_half_nodes=len(points),full_nodes_with_reflection=2*len(points)-1,
                largest_mass_gap=enclosure(max(y-x for x,y in pairwise(points))),
                sin_largest_angular_gap=[max_sin_lower,max_sin_upper],
                zero_node_defect_distance_upper=min(PRECISION,2*max_sin_upper))


def shell_menu(ticks, divisions):
    denominator = 2**ticks
    shell = scalar_shells(transfer(ticks), denominator)
    weight = {r:n for n,r in shell}
    masks = {}
    for j in range(divisions+1):
        # tan(angle)=j/divisions makes sin²(angle) rational and places
        # more targets near zero, where the angular motion is fastest.
        target = Q(j*j, j*j+divisions*divisions)
        radii, mass = from_below(shell, target*denominator)
        require(mass == sum(weight[r] for r in radii), "routed shell total")
        numerator = int(mass)
        require(numerator == mass, "integral return count")
        masks.setdefault(numerator, radii)
    return masks, denominator


def certify(points, response):
    # Complementarity reflects the same residual to the upper half.
    # At 1/2, complementarity fixes the direct signal; endpoint fidelity
    # fixes the signal at its echoed mass 1, even if the half is unattained.
    samples = [(x, response(logistic(x)), logistic(response(x))) for x in points]
    require(all(a[1] <= b[1] and a[2] <= b[2] for a,b in pairwise(samples)),
            "both sampled functions rise on the left half")
    point = max(samples, key=lambda a:abs(a[1]-a[2]))
    worst = max((max(right[1]-left[2], right[2]-left[1]), left[0], right[0])
                for left,right in pairwise(samples))
    low = abs(point[1]-point[2])
    require(low <= worst[0], "enclosure of commutator sup")
    return dict(
        largest_sample_residual=enclosure(low),
        witness_s=str(point[0]),
        continuum_upper=enclosure(worst[0]),
        worst_interval=list(map(str,worst[1:])),
    )


def hidden_control():
    # Both cubics are complementary with derivative >= 0 on [0,1]:
    # the derivative of the perturbation is 1/2 - 6*(p-1/2)^2.
    def population(p):
        shift = p*(1-p)*(2*p-1)
        return p+shift,p-shift
    x = Q(1,4)
    plus,minus = population(x)
    def mean(pair):
        return sum(pair)/2
    common = (logistic(plus)+logistic(minus))/2
    separate = logistic(mean((plus,minus)))
    var = (plus-minus)**2/4
    require(mean(population(logistic(x))) == separate == logistic(x),
            "mean identity, independently redrawn types")
    require(separate-common == 4*var > 0, "shared types change pair statistic")
    return dict(input=str(x),type_specific_direct=[str(plus),str(minus)],
                independent_twice_disagreement=str(separate),
                matched_twice_disagreement=str(common),type_variance=str(var))


def finite_impostor(points):
    # Fix every sampled direct/echo argument and its complement. On each
    # open left-hand gap, use the value of its lower end; reflect the upper
    # half to obtain a complementary monotone discontinuous response.
    fixed = set(points) | {logistic(x) for x in points}
    anchors = sorted(fixed | {1-x for x in fixed})
    def response(x):
        if x > HALF:
            return 1-response(1-x)
        return anchors[bisect_right(anchors,x)-1]
    require(all(response(x)==x for x in anchors), "all required anchors fixed")
    left,right = max(pairwise(x for x in anchors if x<=HALF),key=lambda ab:ab[1]-ab[0])
    x = (left+right)/2
    require(response(x)!=x, "finite nondetection away from anchors")
    require(all(response(logistic(p))==logistic(response(p)) for p in points),
            "finite data coincide with identity")
    return dict(anchor_count=len(anchors),unprobed_input=str(x),
                discrepant_response=str(response(x)),absolute_discrepancy=enclosure(x-response(x)))


def build():
    small = scalar_shells(transfer(3),8)
    require(sum(n for n,r in small if r==3)==2, "three-tick outer shell")
    x=Q(1,4)
    direct=square(x)
    echo=square(logistic(x))
    paired=logistic(direct)
    require((direct,echo,paired,echo-paired)==(Q(1,10),Q(9,10),Q(9,25),Q(27,50)),
            "normalized square falsifier at 3 ticks")
    masks,den=shell_menu(256,32)
    points=sorted({Q(m,den) for m in masks}|{HALF})
    require(points[0]==0 and points[-1]==HALF, "left half covered")
    gap_data=menu_gaps(points)
    require(set(points)=={Q(n,den) for n in masks}|{HALF},
            "only routed nodes and the calibrated midpoint anchor")
    return dict(
        enclosure_denominator=PRECISION,
        three_tick_outer_shell=dict(radii=[3],mass="1/4",echo_escape_mass="3/4",
            square_direct=str(direct),square_echo=str(echo),
            twice_paired_disagreement=str(paired),residual=str(echo-paired)),
        finite_menu=dict(ticks=256,rational_tangent_divisions=32,mass_denominator=str(den),
            routed_left_half_masks=[dict(numerator=str(n),radii=masks[n]) for n in sorted(masks)],
            half_is_kinematically_routed=den//2 in masks,
            complementary_extension=True, gap_certificate=gap_data,
            identity=certify(points,lambda p:p),normalized_square=certify(points,square),
            threshold_step=certify(points,sharp_step),
            indistinguishable_on_finite_menu=finite_impostor(points)),
        hidden_response=hidden_control())


def main():
    parser=ArgumentParser(description=__doc__)
    parser.add_argument("output",type=Path)
    args=parser.parse_args()
    with args.output.open("x",encoding="utf-8",newline="\n") as out:
        json.dump(build(),out,indent=2)
        out.write("\n")


if __name__=="__main__":
    main()
