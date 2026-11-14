"""Check the binary echo phase circuit and readout counterexamples in exact arithmetic."""

from argparse import ArgumentParser
from fractions import Fraction as Q
from itertools import product
import json
from math import comb
from pathlib import Path


def require(condition, message):
    if not condition:
        raise ValueError(message)


# A pair (a,b) represents a+b*z with z=exp(i*pi/3), z²=z-1 and conjugate(z)=1-z.
zero, one, z = (0, 0), (1, 0), (0, 1)


def mul(x, y):
    a, b = x
    c, d = y
    return (a*c - b*d, a*d + b*c + b*d)


def conjugate(x):
    a, b = x
    return (a+b, -b)


def norm(x):
    squared = mul(x, conjugate(x))
    require(squared[1] == 0, "real squared norm")
    return squared[0]


def compose(left, right):
    def cell(i, j):
        x = mul(left[i][0], right[0][j])
        y = mul(left[i][1], right[1][j])
        return (x[0]+y[0], x[1]+y[1])
    return tuple(tuple(cell(i, j) for j in range(2)) for i in range(2))


def adjoint(v):
    return tuple(tuple(conjugate(v[j][i]) for j in range(2)) for i in range(2))


def phase_checks():
    identity = ((one, zero), (zero, one))
    flip = ((zero, one), (one, zero))
    d0, d1 = ((z, zero), (zero, one)), ((one, zero), (zero, z))
    r, t = Q(3, 5), Q(4, 5)
    # diag(z,1) times the real orthogonal map [[r,-t],[t,r]].
    v0 = (((0, r), (0, -t)), ((t, 0), (r, 0)))
    records = {}
    for name, v in [("all_blank", identity), ("no_blank", flip), ("complex_branch", v0)]:
        masses = []
        for step in range(3):
            require(compose(adjoint(v), v) == identity, "each echo circuit is unitary")
            a = v[0][0]
            b = norm(a)
            require(b + norm(v[1][0]) == 1, "complete binary read")
            masses.append(b)
            if step < 2:
                v = compose(v, compose(d0, compose(adjoint(v), compose(d1, v))))
                require(v[0][0] == mul(mul(z, (b, 0)), a), "complex blank amplitude z*b*a")
                require(norm(v[0][0]) == b**3, "cubic mass")
        records[name] = masses
    return records


def readout_checks():
    # Same masses: either first collect all three nonblank coordinates, or apply
    # the same scalar score to each separate coordinate before combining records.
    split, pooled = {}, {}
    for exponent in (1, 2, 4, 8):
        blank = Q(2, 5)**exponent
        fine = 3*Q(1, 5)**exponent
        coarse = Q(3, 5)**exponent
        split[exponent] = fine/(blank+fine)
        pooled[exponent] = coarse/(blank+coarse)
        require(split[exponent] == Q(3, 2**exponent+3), "fine-coordinate power scores")
        require(pooled[exponent] >= Q(1, 2), "binary pooled majority")
    require(split[8] == Q(3, 259) and pooled[8] == Q(6561, 6817), "resolved-port breaker")

    # On this grid F(u) is the response of the first physical port when its
    # kinematic mass is u. A strictly interior majority and constant response
    # attain the half bound even with an extreme physical port preference.
    worst = Q(1)
    panels = 0
    for low in range(9):
        for high in range(low, 9):
            decoded = (Q(high, 8) + 1 - Q(low, 8))/2
            worst = min(worst, decoded)
            panels += 1
    require(worst == Q(1, 2), "sharp fair-swap guarantee")
    require((Q(7, 8) + 1 - Q(7, 8))/2 == worst, "constant biased detector")
    return dict(nonblank_masses=["1/5"]*3, blank_mass="2/5", pooled=pooled, resolved=split,
                monotone_counter_panels=panels, minimum_fair_decoded=worst)


def repetition_checks():
    # One binary echo has masses 3/4 blank, 1/4 nonblank. Count all eight
    # joint masks for independent banks and for the GHZ-like two-branch state.
    n = 3
    product_layers = [Q(0)]*(n+1)
    ghz_layers = [Q(0)]*(n+1)
    for mask in product((0, 1), repeat=n):
        k = sum(mask)
        product_layers[k] += Q(3, 4)**(n-k)*Q(1, 4)**k
        if k == 0:
            ghz_layers[k] += Q(3, 4)
        elif k == n:
            ghz_layers[k] += Q(1, 4)
    require(product_layers == [Q(comb(n,k)*3**(n-k), 4**n) for k in range(n+1)], "product layers")
    for layers in [product_layers, ghz_layers]:
        require(sum(layers) == 1 and sum(k*w for k,w in enumerate(layers))/n == Q(1, 4),
                "complete symmetric joint law with matched one-bank nonblank mass")
    require(1-product_layers[0] == Q(37, 64) and 1-ghz_layers[0] == Q(1, 4), "OR breaker")
    return dict(banks=n, product_masses_by_hamming_weight=product_layers,
                ghz_masses_by_hamming_weight=ghz_layers,
                product_nonblank=1-product_layers[0], ghz_nonblank=1-ghz_layers[0])


def main():
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("output_file", type=Path)
    output = parser.parse_args().output_file
    depth, rate, delta_upper = 5, Q(1, 200), Q(1, 300)
    calls = 3**depth
    require(2*(1-delta_upper)**calls < 1, "crossing below one half")
    mean_upper = delta_upper + (1-delta_upper)*2*rate
    require(mean_upper == Q(133, 10000) < Q(1, 75), "incident mean leakage bound")
    audits = 598
    require((1-rate)**audits < Q(1, 20) <= (1-rate)**(audits-1),
            "first zero-count sample size at the specified rate and confidence")
    require(calls*audits == 145314 and Q(4, 3)*mean_upper == Q(133, 7500),
            "resource count and five-slot asymmetry bound")
    record = dict(phase_blank_masses=phase_checks(), readout=readout_checks(),
                  unmeasured_banks=repetition_checks(), depth=depth, echo_calls=calls,
                  incident_nonblank_rate=rate, strict_threshold_upper=delta_upper,
                  strict_mean_leakage_upper=mean_upper, strict_mean_asymmetry_upper=Q(4, 3)*mean_upper,
                  zero_count_audits=audits, raw_echo_calls=calls*audits)
    with output.open("x", encoding="utf-8", newline="\n") as stream:
        json.dump(record, stream, indent=2, default=str)
        stream.write("\n")


if __name__ == "__main__":
    main()
