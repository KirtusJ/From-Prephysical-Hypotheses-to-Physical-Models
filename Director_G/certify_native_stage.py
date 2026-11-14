"""Certify one finite fixed-H selector stage using standard-library integer arithmetic.

python -B certify_native_stage.py M D
python -B certify_native_stage.py M D --output NEW_FILE
python -B certify_native_stage.py --examples --output NEW_FILE
Compact [lo,hi,2^bits] encodes a rational interval divided by its last entry.
"""
import argparse
from collections import Counter, defaultdict
from fractions import Fraction as Q
from functools import lru_cache
import json
from math import isqrt
from pathlib import Path

SCALE = 2**15


def require(ok, why):
    if not ok:
        raise ValueError(why)


def two_power(pair, n, radicand):
    """Power of u+i*v*sqrt(radicand) in its integer quadratic ring."""
    def times(left, right):
        a, b = left
        c, d = right
        return a*c-b*d*radicand, a*d+b*c
    result = (1, 0)
    while n:
        if n % 2:
            result = times(result, pair)
        pair = times(pair, pair)
        n //= 2
    return result


def rounded_integer(value):
    whole, remainder = divmod(abs(value.numerator), value.denominator)
    return (1 if value >= 0 else -1)*(whole + int(2*remainder > value.denominator))


def fringe_score(x, t):
    b, rad = t*t-x*x, t*t-2*x*x
    u, v = two_power((3*x*x-t*t, 2*x), x, rad)
    p, q = two_power((x*x, -t), t, rad)
    rational_score = Q(v*q*rad-u*p, b**(x+t))
    require(abs(rational_score) <= 1, "nonphysical score")
    return rounded_integer(SCALE*rational_score)


def clock(m, d):
    lo, hi = 0, m
    while hi-lo > 1:
        t = (lo+hi)//2
        if 4*d*d*t**3 <= m*m:
            lo = t
        else:
            hi = t
    return lo


def score_polynomial(m, t, table):
    """Sum coordinate-read squared amplitudes, with the terminal scores as weights."""
    states = {(0, "R"): {0: 1}}
    for _ in range(t):
        future = defaultdict(Counter)
        for (x, rail), row in states.items():
            right = future[(x+1) % (4*m), "R"]
            left = future[(x-1) % (4*m), "L"]
            s = -1 if rail == "L" else 1
            for j, count in row.items():
                gain = (j+x//2) % m
                right[gain] += count
                left[gain] += s*count
        states = {k: {i: a for i, a in v.items() if a} for k, v in future.items()}
    coeff = Counter()
    for x, score in table:
        row = states.get((x % (4*m), "R"), {})
        for u, a in row.items():
            for v, b in row.items():
                coeff[(u-v) % m] += score*a*b
    return {k: v for k, v in coeff.items() if v}


def trim(a):
    while a and a[-1] == 0:
        a.pop()
    return a


def divide(poly, monic):
    remainder = trim(list(poly))
    quotient = [0]*max(0, len(remainder)-len(monic)+1)
    while len(remainder) >= len(monic):
        j, a = len(remainder)-len(monic), remainder[-1]
        quotient[j] = a
        for i, b in enumerate(monic):
            remainder[i+j] -= a*b
        trim(remainder)
    return trim(quotient), remainder


@lru_cache(maxsize=None)
def cyclotomic(n):
    poly = [-1]+[0]*(n-1)+[1]
    divisors = set()
    for i in range(1, isqrt(n)+1):
        if n % i == 0:
            divisors.update((i, n//i))
    for d in sorted(divisors-{n}):
        poly, rem = divide(poly, cyclotomic(d))
        require(not rem, "cyclotomic exact division")
    return tuple(poly)


def weighted_sum(lhs, a, rhs, b):
    result = Counter()
    for u, v in lhs.items():
        result[u] += a*v
    for u, v in rhs.items():
        result[u] += b*v
    return {u: v for u, v in result.items() if v}


def sector_poly(poly, s, m):
    result = Counter()
    for k, a in poly.items():
        result[(k*s) % m] += a
    return {k: a for k, a in result.items() if a}


def atan_bounds(d, bits):
    value, power, j = Q(0), d, 0
    while True:
        value += Q((-1)**j, (2*j+1)*power)
        power *= d*d
        j += 1
        next_term = Q((-1)**j, (2*j+1)*power)
        if abs(next_term) <= Q(1, 2**bits):
            return min(value, value+next_term), max(value, value+next_term)


@lru_cache(maxsize=None)
def pi_bounds(bits):
    l5, h5 = atan_bounds(5, bits+8)
    l239, h239 = atan_bounds(239, bits+8)
    return 16*l5-4*h239, 16*h5-4*l239


def cos_bounds(x, bits):
    total, term, j = Q(1), Q(1), 0
    while True:
        j += 1
        term *= -x*x / ((2*j-1)*(2*j))
        if abs(term) <= Q(1, 2**(bits+4)):
            return min(total, total+term), max(total, total+term)
        total += term


def ceilq(x):
    return -(-x.numerator//x.denominator)


@lru_cache(maxsize=None)
def root_cos(m, k, bits):
    j = min(k % m, (-k) % m)
    unit = 2**bits
    if j == 0:
        return unit, unit
    if 2*j == m:
        return -unit, -unit
    if 4*j == m:
        return 0, 0
    # Reduce to an angle in [0,pi/2]. The cosine is 1-Lipschitz even
    # on the small rational enlargement of the angular interval.
    sign, scale = (1, Q(2*j, m)) if 4*j < m else (-1, Q(m-2*j, m))
    pl, ph = pi_bounds(bits+4)
    x = scale*(pl+ph)/2
    err = scale*(ph-pl)/2
    l, h = cos_bounds(x, bits)
    l, h = l-err, h+err
    if sign < 0:
        l, h = -h, -l
    return (l*unit).__floor__(), ceilq(h*unit)


def bounds(poly, m, bits):
    lo = hi = 0
    for k, a in poly.items():
        l, h = root_cos(m, k, bits)
        lo += a*(l if a >= 0 else h)
        hi += a*(h if a >= 0 else l)
    return lo, hi


def compare(poly, m):
    """Sign of a symmetric integer polynomial at the given primitive root."""
    require(all(poly.get((-k) % m, 0) == a for k, a in poly.items()),
            "a non-real polynomial cannot be ordered by its real part")
    degree = max(poly, default=0)
    dense = [poly.get(k, 0) for k in range(degree+1)]
    if not divide(dense, cyclotomic(m))[1]:
        return 0
    bits = 16
    while True:
        lo, hi = bounds(poly, m, bits)
        if lo > 0 or hi < 0:
            return 1 if lo > 0 else -1
        bits *= 2


def dark_poly(s, m):
    # p_s=(1-cos(2*pi*s/M))/4. Represent 8*p_s at zeta_M.
    result = Counter({0: 2})
    result[s % m] -= 1
    result[-s % m] -= 1
    return {k: a for k, a in result.items() if a}


def stage(m, d):
    require(m >= 3 and 1 <= d <= m//2 and d & (d-1) == 0, "require dyadic D <= floor(M/2)")
    t = clock(m, d)
    table = [(x, fringe_score(x,t)) for x in range(-t,t+1,2) if 4*x >= t and 2*x <= t]
    numerator = score_polynomial(m, t, table) if table else {}
    den = SCALE*2**t
    rivals = [0] if d == 1 else list(range(d, min(2*d-1,m//2)+1))
    sign = 1 if d == 1 else -1
    target = sector_poly(numerator, 1, m)
    polys = [sector_poly(numerator, s, m) for s in rivals]
    verdicts = []
    for rival in polys:
        diff = weighted_sum(target, sign, rival, -sign)
        decision = weighted_sum(diff, 2048, {0: den}, -1)
        verdicts.append(compare(decision, m))
    use_fringe = min(verdicts) >= 0
    if not use_fringe:
        den, target = 8, dark_poly(1,m)
        polys = [dark_poly(s,m) for s in rivals]
    # Order the actual competitors exactly (including legitimate ties).
    closest = 0
    for i in range(1,len(polys)):
        delta = weighted_sum(polys[i], sign, polys[closest], -sign)
        if compare(delta, m) > 0:
            closest = i
    gap = weighted_sum(target, sign, polys[closest], -sign)
    require(compare(gap, m) > 0, "certified chosen stage has nonpositive gap")
    bits = 32
    while True:
        gl, gh = bounds(gap, m, bits)
        if gl > 0:
            break
        bits *= 2
    tl, th = bounds(target, m, bits)
    vl, vh = bounds(polys[closest], m, bits)
    threshold = weighted_sum(target, 1, polys[closest], 1)
    denominator = den*2**bits
    return dict(M=m, d=d, candidate_ticks=t, rounded_window_table=table,
                candidate_score_polynomial=dict(denominator=SCALE*2**t,
                                                root_polynomial=sorted(numerator.items())),
                gap_to_one_over_2048_by_rival=list(zip(rivals, verdicts)),
                selected="rounded_fringe" if use_fringe else "three_tick_dark",
                selected_ticks=t if use_fringe else 3, closest_label=rivals[closest],
                target_side="above" if sign>0 else "below",
                target_mean_enclosure=[tl, th, denominator],
                closest_mean_enclosure=[vl, vh, denominator],
                positive_gap_enclosure=[gl, gh, denominator],
                exact_midpoint=dict(denominator=2*den,
                                    root_polynomial=sorted(threshold.items())),
                exact_gap=dict(denominator=den, root_polynomial=sorted(gap.items())))


def examples():
    require(rounded_integer(Q(3,2)) == 1 and rounded_integer(Q(-3,2)) == -1,
            "signed half-integer ties")
    require(fringe_score(2,4) == -14788, "exact nonempty score")
    root_sum = {j:1 for j in range(7)}
    require(compare(root_sum, 7) == 0 and
            compare(weighted_sum(root_sum,1,{0:1},1),7) == 1 and
            compare(weighted_sum(root_sum,1,{0:1},-1),7) == -1,
            "cyclotomic equality or strict side")
    require(compare({0: 1, 1: -1, 5: -1}, 6) == 0, "proper cyclotomic relation")
    cases = [stage(m,d) for m,d in ((3,1),(4,1),(17,1),(31,2),(64,1),(64,2),
                                    (97,2),(97,8),(128,2),(257,2))]
    require(cases[2]["selected"] == cases[5]["selected"] == "rounded_fringe" and
            cases[7]["selected"] == "three_tick_dark" and cases[7]["rounded_window_table"],
            "nonempty positive and adverse decisions")
    return dict(arithmetic="Integer signed sheet-coordinate propagation; real quadratic "
                "score rounding; cyclotomic equality; directed rational cosine bounds.",
                controls=dict(positive_half_tie=1, negative_half_tie=-1,
                              seventh_root_sum_and_plus_minus_one_signs=[0,1,-1]),
                stages=cases)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("M", type=int, nargs="?")
    parser.add_argument("D", type=int, nargs="?")
    parser.add_argument("--examples", action="store_true")
    parser.add_argument("--output", type=Path, help="new output file, default stdout")
    args = parser.parse_args()
    if args.examples:
        if args.M is not None or args.D is not None:
            parser.error("--examples takes no stage arguments")
        data = examples()
    elif args.M is not None and args.D is not None:
        data = stage(args.M,args.D)
    else:
        parser.error("supply M and D or --examples")
    if args.output is None:
        print(json.dumps(data, sort_keys=True, separators=(",", ":")))
    else:
        args.output.parent.mkdir(exist_ok=True, parents=True)
        with args.output.open("x", encoding="utf8", newline="\n") as out:
            json.dump(data, out, sort_keys=True, separators=(",", ":"))
            out.write("\n")
