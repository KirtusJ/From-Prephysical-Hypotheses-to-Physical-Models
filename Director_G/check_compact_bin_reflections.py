"""Compile, replay and archive a two-reflection transfer to compact integer endpoints."""
from argparse import ArgumentParser
from fractions import Fraction as F
from functools import reduce
import json
from hashlib import sha256
from math import gcd, isqrt
from pathlib import Path


def check(condition, explanation):
    if not condition:
        raise ValueError(explanation)


def odd_gcd(v):
    g = reduce(gcd, v, 0)
    if g == 0:
        raise ValueError("empty bin")
    return g // (g & -g)


def dot(x, y):
    return sum(a*b for a, b in zip(x, y))


def extended_gcd(a, b):
    if not b:
        return abs(a), 1 if a >= 0 else -1, 0
    g, x, y = extended_gcd(b, a % b)
    return g, y, x-(a//b)*y


def dyadic_bezout(v):
    g, coefs = 0, []
    for a in v:
        g, p, q = extended_gcd(g, a)
        coefs = [p*c for c in coefs] + [q]
    check(g & (g-1) == 0, "integer gcd must be a power of two")
    result = [F(c, g) for c in coefs]
    check(dot(v, result) == 1, "Bezout repair failed")
    return result


def hyperplane_point(v, b, grid, norm2, bezout):
    approximate = [F(round(F(grid*b*x, norm2)), grid) for x in v]
    defect = b-dot(v, approximate)
    return [a+defect*c for a, c in zip(approximate, bezout)]


def four_squares(n, primitive=False):
    """Finite demonstration only. The paper supplies the expected-polynomial alternative."""
    for a in range(isqrt(n), -1, -1):
        for b in range(isqrt(n-a*a), -1, -1):
            for c in range(isqrt(n-a*a-b*b), -1, -1):
                remainder = n-a*a-b*b-c*c
                d = isqrt(remainder)
                if d*d == remainder and (not primitive or odd_gcd([a,b,c,d]) == 1):
                    return [a, b, c, d]
    raise ValueError("positive integer lacked a four-square representation")


def reflect(v, w, denominator):
    factor = dot(v, w)/F(denominator)
    return [a-factor*c for a, c in zip(v, w)]


def is_dyadic(x):
    d = F(x).denominator
    return d & (d-1) == 0


def binary_squares(n):
    """Base-four digits specify copies of squares of integer powers of two."""
    digits = []
    base = 1
    while n:
        n, digit = divmod(n, 4)
        digits.extend([base]*digit)
        base *= 2
    return digits


def pairwise_h(row):
    result = []
    for a, b in zip(row[::2], row[1::2]):
        result.extend((a+b, a-b))
    return result


def fraction_gate(row, action):
    kind, indices = action
    if kind == "global_H":
        return pairwise_h(row)
    if kind == "neg":
        row[indices[0]] *= -1
    elif kind == "swap":
        i, j = indices
        row[i], row[j] = row[j], row[i]
    elif kind == "K4":
        i, j, k, l = indices
        a, b, c, d = row[i], row[j], row[k], row[l]
        row[i], row[j], row[k], row[l] = [F(v,2) for v in (a+b+c+d,a-b+c-d,a+b-c-d,a-b-c+d)]
    else:
        raise ValueError(kind)
    return row


def normal_reducer(w):
    """C maps w to the zeroth signed coordinate. Whole-register H is stored without sqrt(2)."""
    d = max(F(a).denominator for a in w)
    row = [int(d*a) for a in w]
    n = dot(row, row)
    check(n > 0 and n & (n-1) == 0, "normal lacks power-of-two square norm")
    word = []
    if (n.bit_length()-1) % 2:
        word.append(("global_H", []))
        row = pairwise_h(row)
        n *= 2
    while n > 1:
        odds = [i for i, a in enumerate(row) if a % 2]
        check(len(odds) % 4 == 0, "odd residues")
        for j in range(0, len(odds), 4):
            slots = odds[j:j+4]
            for i in slots:
                if row[i] % 4 == 3:
                    row[i] *= -1
                    word.append(("neg", [i]))
            a,b,c,d0 = (row[i] for i in slots)
            outputs = (a+b+c+d0,a-b+c-d0,a+b-c-d0,a-b-c+d0)
            check(all(v % 4 == 0 for v in outputs), "denominator reduction")
            for i, v in zip(slots, outputs):
                row[i] = v//2
            word.append(("K4", slots))
        check(all(a % 2 == 0 for a in row), "unchanged coordinates must be even")
        row = [v//2 for v in row]
        n //= 4
    coordinate = next(i for i, a in enumerate(row) if a)
    check(sum(abs(a) for a in row) == 1, "normal did not reduce to a single address")
    if coordinate:
        word.append(("swap", [0,coordinate]))
    return word


def circuit_reflect(row, reducer):
    out = list(row)
    for action in [*reducer, ("neg",[0]), *reversed(reducer)]:
        out = fraction_gate(out, action)
    if any(gate[0] == "global_H" for gate in reducer):
        out = [a/F(2) for a in out]
    return out


def transport(x, y, digit_padding=False):
    sx = dot(x, x)
    check(sx == dot(y, y), "unequal norms")
    g, gy = odd_gcd(x), odd_gcd(y)
    record = dict(source=x, target=y, norm2=sx, odd_gcd=[g, gy])
    if g != gy:
        return dict(record, obstruction="odd gcd differs")
    x, y = [a//g for a in x], [b//g for b in y]
    n = dot(x, x)
    gap = 1 << (n.bit_length()-1)
    b = n-gap
    bx, by = dyadic_bezout(x), dyadic_bezout(y)
    grid = 1
    while True:
        p, q = hyperplane_point(x, b, grid, n, bx), hyperplane_point(y, b, grid, n, by)
        slack = n-dot(p, p)-dot(q, q)
        if slack > 0:
            break
        grid *= 2
    d = max(F(a).denominator for a in p+q)
    integer_slack = slack*d*d
    check(integer_slack.denominator == 1, "noninteger padding problem")
    fill = binary_squares(int(integer_slack)) if digit_padding else four_squares(int(integer_slack))
    padding = [F(a, d) for a in fill]
    z = p+q+padding
    width = 1 << (len(z)-1).bit_length()
    z += [0]*(width-len(z))
    x = x+[0]*(width-len(x))
    y = [0]*len(p)+y+[0]*(width-len(p)-len(y))
    check(dot(z, z) == n and dot(x, z) == b and dot(y, z) == b, "intermediate sphere point")
    w1, w2 = [a-c for a, c in zip(x, z)], [c-bb for c, bb in zip(z, y)]
    for w in (w1, w2):
        check(dot(w, w) == 2*gap, "reflection normalization")
        check(all(is_dyadic(a) for a in w) and is_dyadic(F(1, gap)), "gate entries")
    check(reflect(x, w1, gap) == z and reflect(z, w2, gap) == y, "forward trace")
    check(reflect(y, w2, gap) == z and reflect(z, w1, gap) == x, "reverse trace")
    words = [normal_reducer(w1), normal_reducer(w2)]
    check(circuit_reflect(x, words[0]) == z and circuit_reflect(z, words[1]) == y, "compiled endpoint")
    check(circuit_reflect(y, words[1]) == z and circuit_reflect(z, words[0]) == x, "compiled inverse")
    # Reflections and compiled words must agree as gates, including on columns
    # outside the source and its image. Replay every basis vector on the smaller panels.
    checked_columns = 0
    if width <= 32:
        for w, gates in zip((w1,w2),words):
            for index in range(width):
                unit = [int(j == index) for j in range(width)]
                check(circuit_reflect(unit, gates) == reflect(unit, w, gap), "full matrix replay")
                checked_columns += 1
    word_data = (dict(normal_reducers=words) if width <= 32 else
                 dict(normal_reducer_sha256=[sha256(json.dumps(word, separators=(",", ":")).encode()).hexdigest()
                                              for word in words]))
    return dict(record, gap=gap, inner_product=b, rounding_grid=grid,
                construction_width=len(p)+len(q)+len(fill), padded_width=width,
                z=[str(a) for a in z], **word_data,
                gates_per_reflection=[2*len(word)+1 for word in words], independent_basis_columns=checked_columns)


def flight(t):
    state = {(0,0): 1}
    for _ in range(t):
        after = {}
        for (x,r), a in state.items():
            for s in (0,1):
                port = (x+1-2*s,s)
                after[port] = after.get(port,0) + (-a if r == s == 1 else a)
        state = after
    return state


def main():
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    results = []
    for t in (4, 10, 20, 32, 80, 256):
        state = flight(t)
        check(sum(a*a for a in state.values()) == 1 << t, "full original mass")
        for chosen in (False,True):
            row = [v for (x,r),v in sorted(state.items()) if (x >= 0) == chosen]
            n = dot(row, row)
            g = odd_gcd(row)
            primitive_n = n // (g*g)
            methods = (False, True) if t == 32 else (t >= 80,)
            for use_digits in methods:
                compact = ([1] + binary_squares(primitive_n-1) if use_digits
                           else four_squares(primitive_n, primitive=True))
                target = [g*a for a in compact]
                results.append(dict(ticks=t, nonnegative_site=chosen,
                                    method="base four" if use_digits else "four squares",
                                    replay=transport(row, target, use_digits)))
    cases = [([3,5], [5,3,0,0]), ([3], [2,2,1,0]), ([9,15], [15,9,0,0]),
             ([1,1,1,1], [2,0,0,0]), ([0,5,3], [5,3])]
    controls = [transport(x,y) for x,y in cases]
    with args.output.open("x", encoding="utf8", newline="\n") as out:
        json.dump(dict(flights=results, controls=controls), out, separators=(",", ":"))
        out.write("\n")


if __name__ == "__main__":
    main()
