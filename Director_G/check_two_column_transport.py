"""Replay a common four-reflection circuit and directional obstructions on two columns."""
import argparse
import json
from fractions import Fraction as Q
from itertools import combinations
from math import gcd, lcm
from pathlib import Path

from check_compact_bin_reflections import (
    binary_squares, check, circuit_reflect, dyadic_bezout, four_squares,
    is_dyadic, normal_reducer, reflect,
)


def transpose(a):
    return [list(col) for col in zip(*a)]


def times(a, b):
    return [[sum(x*y for x, y in zip(row, col)) for col in zip(*b)] for row in a]


def minus(a, b):
    return [[x-y for x, y in zip(row, other)] for row, other in zip(a, b)]


def gram(a, b):
    return times(transpose(a), b)


def det(a):
    (x, y), (z, w) = a
    return x*w-y*z


def inverse(a):
    (x, y), (z, w) = a
    d = det(a)
    return [[Q(w, d), Q(-y, d)], [Q(-z, d), Q(x, d)]]


def diag(n):
    return [[n, 0], [0, n]]


def zeros(n):
    return [[0, 0] for _ in range(n)]


def right_inverse(rows):
    """Use the integer minors of a common dyadic multiple."""
    scale = lcm(*(Q(z).denominator for row in rows for z in row))
    matrix = [[int(x*scale) for x in row] for row in rows]
    pairs = list(combinations(range(len(rows)), 2))
    bezout = dyadic_bezout([det([matrix[i], matrix[j]]) for i, j in pairs])
    jmat = zeros(len(rows))
    for (i, j), k in zip(pairs, bezout):
        (a, b), (c, d) = matrix[i], matrix[j]
        jmat[i][0] += scale*k*d
        jmat[i][1] -= scale*k*c
        jmat[j][0] -= scale*k*b
        jmat[j][1] += scale*k*a
    check(gram(rows, jmat) == diag(1), "dyadic right inverse of transpose")
    return jmat


def dominant(k):
    return k[0][1] == k[1][0] and min(k[0][0], k[1][1]) > abs(k[0][1])


def positive(k):
    return k[0][1] == k[1][0] and k[0][0] > 0 and det(k) > 0


def reduce_slack(k):
    """Integral column shears and swaps give a diagonally dominant binary form."""
    check(positive(k), "positive-definite binary slack")
    form, chart = k, diag(1)
    while not dominant(form):
        a, c = form[0]
        if form[1][1] < a:
            step = [[0, 1], [1, 0]]
        else:
            step = [[1, -round(Q(c, a))], [0, 1]]
        chart = times(chart, step)
        form = times(transpose(step), times(form, step))
    check(abs(det(chart)) == 1, "unimodular slack chart")
    return chart, form


def repair(frame, ideal, cross, grid, right):
    rounded = [[Q(round(grid*x), grid) for x in row] for row in ideal]
    correction = times(right, minus(cross, gram(frame, rounded)))
    answer = [[x+y for x, y in zip(row, corr)] for row, corr in zip(rounded, correction)]
    check(gram(frame, answer) == cross, "exact repaired pairing")
    return answer


def squares(value, digit_padding):
    scale = Q(value).denominator
    check(is_dyadic(value) and value >= 0, "dyadic nonnegative slack")
    integer = int(value*scale*scale)
    entries = binary_squares(integer) if digit_padding else four_squares(integer)
    return [Q(x, scale) for x in entries if x]


def midpoint(x, y, delta, digit_padding=False, *, right_x=None, right_y=None):
    """Optionally supply dyadic right inverses of the transposed source/target."""
    h = gram(x, x)
    check(gram(y, y) == h, "equal joint Gram")
    cross = minus(h, diag(delta))
    aim = times(inverse(h), cross)
    k0 = minus(h, times(times(cross, aim), diag(2)))
    check(positive(k0), "chosen chart and scale must give positive-definite ideal slack")
    def verified(frame, supplied, name):
        if supplied is None:
            return right_inverse(frame)
        check(len(supplied) == len(frame) and all(len(row) == 2 for row in supplied),
              f"{name}: right inverse must have one two-entry row per frame row")
        check(all(type(v) in (int, Q) and is_dyadic(v) for row in supplied for v in row),
              f"{name}: right inverse must use exact dyadic entries")
        check(gram(frame, supplied) == diag(1), f"{name}: transpose times right inverse must be identity")
        return supplied

    r_x, r_y = verified(x, right_x, "right_x"), verified(y, right_y, "right_y")
    grid = 1
    while True:
        a = repair(x, times(x, aim), cross, grid, r_x)
        b = repair(y, times(y, aim), cross, grid, r_y)
        k = minus(minus(h, gram(a, a)), gram(b, b))
        if positive(k):
            break
        grid *= 2
    slack_chart, form = reduce_slack(k)
    c = form[0][1]
    tail = [[r, r if c > 0 else -r] for r in squares(abs(c), digit_padding)]
    tail.extend([r, 0] for r in squares(form[0][0]-abs(c), digit_padding))
    tail.extend([0, r] for r in squares(form[1][1]-abs(c), digit_padding))
    tail = times(tail, inverse(slack_chart))
    check(gram(tail, tail) == k and (digit_padding or len(tail) <= 12), "rank-one slack terms")
    return a+b+tail, grid, k


def certify(x, y, z, delta, raw_x=None, raw_y=None):
    width = 1 << (len(z)-1).bit_length()
    pad_x = lambda rows: rows+zeros(width-len(rows))
    pad_y = lambda rows: zeros(len(x))+rows+zeros(width-len(x)-len(rows))
    start, end = pad_x(x), pad_y(y)
    middle = pad_x(z)
    h = gram(start, start)
    cross = minus(h, diag(delta))
    check(gram(end, end) == gram(middle, middle) == h, "three equal Grams")
    check(gram(start, middle) == gram(end, middle) == cross, "two full cross Grams")
    words = []
    normal_data = []
    for src, dst in [(start, middle), (middle, end)]:
        normals = minus(src, dst)
        check(gram(normals, normals) == diag(2*delta), "perpendicular equal-length normals")
        check(gram(src, normals) == diag(delta), "each reflection fixes the other column")
        for normal in transpose(normals):
            check(all(is_dyadic(v) for v in normal), "dyadic normal")
            reducer = normal_reducer(normal)
            words.append(reducer)
            normal_data.append(normal)
    columns = transpose(pad_x(x if raw_x is None else raw_x))
    original = [v[:] for v in columns]
    for reducer, normal in zip(words, normal_data):
        direct = [reflect(v, normal, delta) for v in columns]
        columns = [circuit_reflect(v, reducer) for v in columns]
        check(columns == direct, "compiled gates versus explicit reflection")
    check(columns == transpose(pad_y(y if raw_y is None else raw_y)), "both original columns transported")
    for reducer in reversed(words):
        columns = [circuit_reflect(v, reducer) for v in columns]
    check(columns == original, "reverse gate word on both columns")
    return dict(slots=width, gates_per_reflection=[2*len(w)+1 for w in words],
                chart_gram=h, midpoint=z, delta=delta, all_columns_reversed=True)


def walk(ticks):
    # Rail rows within each site. Columns are the two original launch rails.
    sites = {0: [[1, 0], [0, 1]]}
    for _ in range(ticks):
        following = {}
        for x, (a, b) in sites.items():
            following.setdefault(x+1, zeros(2))[0] = [u+v for u, v in zip(a, b)]
            following.setdefault(x-1, zeros(2))[1] = [u-v for u, v in zip(a, b)]
        sites = following
    return sites


def minor_gcd(rows):
    return gcd(*(det([a, b]) for a, b in combinations(rows, 2)))


def native_obstruction():
    sites = walk(37)
    rows = sites[25]+sites[-25]
    factor = gcd(*(v for row in rows for v in row))
    reduced = [[v//factor for v in row] for row in rows]
    p = gram(reduced, reduced)[0][0]
    check(factor == 80 and p == 5401250 and gram(reduced, reduced) == diag(p), "actual walk shell")
    check(all(gcd(*col) == 1 for col in transpose(reduced)), "both source columns individually primitive")
    primitive = [1]+binary_squares(p-1)
    reference = [[u, 0] for u in primitive]+[[0, u] for u in primitive]
    check(gram(reference, reference) == diag(p) and minor_gcd(reference) == 1, "disjoint primitive reference")
    check(minor_gcd(reduced) == 25 and all((b-3*a) % 5 == 0 for a, b in reduced), "source rank drops in direction (−3,1)")
    return dict(ticks=37, sites=[25,-25], original=rows, common_factor=factor, reduced=reduced,
                reduced_squared_norm=p, reference_column=primitive, source_minors_gcd=25,
                reference_minors_gcd=1, reduced_source_rows_mod_5=[[a%5,b%5] for a,b in reduced])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("output", type=Path)
    dest = ap.parse_args().output
    sites = walk(3)
    x = sites[-1]+sites[1]
    y = [[2,0],[1,0],[1,0],[0,2],[0,1],[0,1]]
    z = [[0,0],[0,-1],[1,0],[0,0],[1,0],[0,0],[0,0],[0,1],[0,0],[0,0],[2,0],[0,2]]
    sharp = certify(x, y, z, 4)

    # Primitive 2-column frame with unequal eigenvalues and nonzero cross term.
    a = [[1,0],[0,1],[1,1],[1,0]]
    b = [[0,-1],[1,0],[-1,-1],[1,0]]
    chart = [[1, 6], [0, 1]]
    row_basis = [[1,2],[-2,1]]  # common proper direction-sensitive row module
    xx, yy = times(times(a, chart), row_basis), times(times(b, chart), row_basis)
    check(gram(xx, xx) == gram(yy, yy), "original nonscalar Gram")
    check(times(times(xx, inverse(row_basis)), inverse(chart)) == a, "first chart cancellation")
    check(times(times(yy, inverse(row_basis)), inverse(chart)) == b, "second chart cancellation")
    mid, grid, slack = midpoint(a, b, 2)
    for options in [dict(right_x=right_inverse(a)), dict(right_y=right_inverse(b)),
                    dict(right_x=right_inverse(a), right_y=right_inverse(b))]:
        check(midpoint(a, b, 2, **options) == (mid, grid, slack), "supplied and computed inverses agree")
    alternative = [[1, 0], [0, 1], [0, 0], [0, 0]]  # a starts with the identity
    z_alt, _, _ = midpoint(a, b, 2, right_x=alternative)
    certify(a, b, z_alt, 2, xx, yy)
    non_dyadic = [[Q(2,3), 0], [0,1], [0,0], [Q(1,3),0]]
    check(gram(a, non_dyadic) == diag(1), "negative control is a rational right inverse")
    for key, invalid in [("right_x", zeros(len(a))), ("right_y", right_inverse(b)[:-1]),
                         ("right_x", non_dyadic), ("right_y", right_inverse(b)+[[0,0]])]:
        try:
            midpoint(a, b, 2, **{key:invalid})
        except ValueError as error:
            check(str(error).startswith(key+":"), "refusal names the supplied right inverse")
        else:
            raise ValueError("invalid supplied right inverse accepted")
    tilted = certify(a, b, mid, 2, xx, yy)
    tilted.update(grid=grid, slack=slack, original_gram=gram(xx, xx), common_row_basis=row_basis,
                  inverse_chart=inverse(chart), source=xx, target=yy)
    skew = [[2, 9], [9, 41]]
    slack_chart, reduced = reduce_slack(skew)
    check(dominant(reduced) and times(transpose(slack_chart), times(skew, slack_chart)) == reduced,
          "an initially non-dominant positive residual")
    z2, grid2, k2 = midpoint(a, b, 2, digit_padding=True)
    digit_replay = certify(a, b, z2, 2, xx, yy)
    digit_replay.update(grid=grid2, slack=k2, non_dominant_example=skew,
                        unimodular_slack_chart=slack_chart, reduced_slack_example=reduced)
    first, second = row_basis, [[1,-2],[2,1]]
    check(gram(first, first) == gram(second, second) == diag(5), "abstract equal Grams")
    check(det(first) == det(second) == 5, "equal determinant divisors")
    check(all((b-2*a)%5 == 0 for a,b in first) and any((b-2*a)%5 for a,b in second),
          "distinct directional modules")
    cases = dict(three_tick_control=sharp, nondiagonal_chart=tilted, digit_padding=digit_replay,
                 native_obstruction=native_obstruction(), directional_obstruction=dict(x=first, y=second, gram=diag(5), prime=5))
    dest.mkdir()
    (dest/"two_column_transport.json").write_bytes((json.dumps(cases, indent=2, default=str)+"\n").encode())


if __name__ == "__main__":
    main()
