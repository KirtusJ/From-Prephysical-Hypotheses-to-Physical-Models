"""Exact finite-field checking for the one-port detector calibration note."""
from fractions import Fraction
from itertools import permutations
from math import prod

P = 1009
U, V = 667, 387
FREQ = ((0, 0), (1, 0), (-1, 0), (0, 1), (0, -1), (2, 0), (-2, 0),
        (0, 2), (0, -2), (1, 1), (-1, -1), (1, -1), (-1, 1))
POSITIVES = ((1, 0), (0, 1), (2, 0), (0, 2), (1, 1), (1, -1))
MULT = (2, 2, 1, 1, 2, 2)


def require(condition, check):
    if not condition:
        raise ArithmeticError(check)


def inv(x):
    return pow(x, -1, P)


def character(z, w, e):
    return pow(z, e[0], P) * pow(w, e[1], P) % P


def opposite(e):
    return tuple(-i for i in e)


def solve(matrix, rhs):
    rows = [[s % P for s in row + [y]] for row, y in zip(matrix, rhs)]
    for j in range(len(rows)):
        k = next(i for i in range(j, len(rows)) if rows[i][j])
        rows[j], rows[k] = rows[k], rows[j]
        factor = inv(rows[j][j])
        rows[j] = [x * factor % P for x in rows[j]]
        for i in range(len(rows)):
            if i != j:
                multiple = rows[i][j]
                rows[i] = [(a - multiple * b) % P for a, b in zip(rows[i], rows[j])]
    return [row[-1] for row in rows]


def resultant(f, g):
    a, b, c = f
    x, y, z = g
    matrix = [[a, b, c, 0], [0, a, b, c], [x, y, z, 0], [0, x, y, z]]
    det = 0
    for order in permutations(range(4)):
        inversions = sum(order[i] > order[j] for j in range(4) for i in range(j))
        det += (-1)**inversions * prod(matrix[i][order[i]] for i in range(4))
    return det % P


def quadratic(function):
    c = function(0) % P
    b = (function(1) - function(-1)) * inv(2) % P
    a = (function(1) - b - c) % P
    require(all((a*x*x + b*x + c - function(x)) % P == 0 for x in (2, 3, 19)), "quadratic interpolation")
    return a, b, c


def known_angle_controls():
    """Verify unreduced real identities using rational unit phases and raw contrasts."""
    ca, sa = Fraction(3, 5), Fraction(4, 5)
    cb, sb = Fraction(-5, 13), Fraction(12, 13)
    require(ca*ca + sa*sa == cb*cb + sb*sb == 1, "rational phases are not unit")
    phase_pairs = ((ca, sa), (cb, sb), (ca*ca-sa*sa, 2*ca*sa),
                   (cb*cb-sb*sb, 2*cb*sb), (ca*cb-sa*sb, sa*cb+ca*sb),
                   (ca*cb+sa*sb, sa*cb-ca*sb))
    fixtures = ((Fraction(2, 5), Fraction(-3, 7)),
                (Fraction(1, 3), Fraction(4, 5)),
                (Fraction(2, 5), Fraction(2, 5)))
    for gain, other_gain in fixtures:
        magnitudes = [(gain*x-other_gain)**2 + (gain*y)**2 for x, y in phase_pairs]
        a, b, c, e2, h, j = magnitudes
        k, v = gain**2 + other_gain**2, 2*gain*other_gain
        require(k*(k-v) == k*(a+b) - v*(h+j)/2 - a*b, "sum-angle identity")
        second = 4*k*a - v*c - 2*a*a
        require(second == 4*k*b - v*e2 - 2*b*b, "agreement between the two doubling identities")
        require(second == (k-v)*(2*k+v), "double-angle identity")
        if gain != other_gain:
            require(second != (k-v)*(k+2*v), "incorrect factorization escaped the control")
    return len(fixtures)


def main():
    require(all(P % i for i in range(2, 32)), "prime modulus")
    require(244**2 % P == 5, "square root of five")
    require((U + inv(U)) % P == ((3 - 244) * inv(4)) % P, "first trace relation")
    require((V + inv(V)) % P == ((3 + 244) * inv(4)) % P, "second trace relation")
    nodes = {e: character(U, V, e) for e in FREQ}
    require(len(set(nodes.values())) == 13, "distinct nodes")
    n = {e: inv(prod(x - nodes[f] for f in FREQ if f != e)) for e, x in nodes.items()}
    for k in range(12):
        require(sum(n[e] * pow(nodes[e], k, P) for e in FREQ) % P == 0, "null moment")
    a, b, c, e2, h, j = norms = [
        n[e]*n[opposite(e)]*inv(m*m) % P for e, m in zip(POSITIVES, MULT)]
    d = (h + j) * inv(2) % P

    def central(v):
        return ((c - e2) * v + 2 * (a*a - b*b)) * inv(4 * (a-b)) % P

    def sum_angles(v):
        k = central(v)
        return k*(k-v) - k*(a+b) + v*d + a*b

    def double_angle(v):
        k = central(v)
        return (k-v)*(2*k+v) - 4*k*a + v*c + 2*a*a

    f, g = quadratic(sum_angles), quadratic(double_angle)
    require(norms == [814, 853, 1005, 1006, 739, 284], "conjugate node products")
    require(f == (293, 687, 881) and g == (889, 172, 256), "resultant inputs")
    require(resultant(f, g) == 833, "resultant")
    print("unreduced real-identity rational-angle fixtures passed =", known_angle_controls())
    print("12 settings: six squared magnitudes modulo 1009 =", norms)
    print("necessary quadratics (descending) =", f, g, "resultant =", resultant(f, g))

    # Independent closed-form 13-reading decoder, including signed contrasts.
    matrix = [[pow(nodes[e], k, P) for e in FREQ] for k in range(13)]
    fixtures = 0
    for z, w in ((1, 1), (1, 27), (231, 479), (P-1, P-1)):
        for gain, dark in ((1, 0), (463, 817), (P-1, 37)):
            obs = []
            for k in range(13):
                zt = z * pow(U, k, P) % P
                wt = w * pow(V, k, P) % P
                amplitude = (1 + zt + inv(zt) + wt + inv(wt)) * inv(5) % P
                obs.append((dark + gain * amplitude**2) % P)
            cf = dict(zip(FREQ, solve(matrix, obs)))
            expected_coefficients = {(0, 0): (dark + gain*inv(5)) % P}
            for exponent, multiplicity in zip(POSITIVES, MULT):
                for signed in (exponent, opposite(exponent)):
                    expected_coefficients[signed] = (
                        gain*multiplicity*character(z, w, signed)*inv(25)) % P
            require(cf == expected_coefficients, "interpolated coefficient mismatch")
            # Lagrange interpolation on the first 12 observations, fixing C0
            # to the directly known fixture value. Recover every other mode.
            known_dc = cf[0, 0]
            short = [[pow(nodes[e], k, P) for e in FREQ[1:]] for k in range(12)]
            short_cf = solve(short, [y-known_dc for y in obs[:12]])
            require(short_cf == [expected_coefficients[e] for e in FREQ[1:]], "twelve-row coefficient solve")
            # Any other assigned DC shifts the entire coefficient vector along n.
            delta_dc = 19
            shifted = solve(short, [y-known_dc-delta_dc for y in obs[:12]])
            require(all((y-x)*n[0, 0] % P == delta_dc*n[e] % P
                       for e, x, y in zip(FREQ[1:], short_cf, shifted)), "affine null direction")
            recover_z = 2 * cf[2, 0] * inv(cf[1, 0]) % P
            recover_w = 2 * cf[0, 2] * inv(cf[0, 1]) % P
            recover_g = 25 * cf[1, 0]**2 * inv(4 * cf[2, 0]) % P
            recover_d = (cf[0, 0] - recover_g * inv(5)) % P
            require((recover_z, recover_w, recover_g, recover_d) == (z, w, gain, dark), "phase and detector recovery")
            fixtures += 1
    print("13-setting independent finite-field decoder fixtures passed =", fixtures)


if __name__ == "__main__":
    main()
