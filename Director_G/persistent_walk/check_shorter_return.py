"""Verify the shorter five-site test using integer interval and rational arithmetic.

Run with standard-library Python 3.9 or later, including with -I -B -O.
Every interval endpoint represents an integer divided by SCALE.
"""
from fractions import Fraction
from math import factorial, isqrt

SCALE = 10**80
N = 250_000
STATE_CAP = 55
RESOLVENT_BOUND = 37_000
LAUNCHES = 2_400
THRESHOLD = Fraction(619, 10_000)


def require(condition, message):
    if not condition:
        raise ArithmeticError(message)


def integer(k):
    return (k * SCALE, k * SCALE)


def add(x, y):
    return (x[0] + y[0], x[1] + y[1])


def subtract(x, y):
    return (x[0] - y[1], x[1] - y[0])


def times(x, y):
    corners = [a * b for a in x for b in y]
    return (min(corners) // SCALE, -((-max(corners)) // SCALE))


def divide_integer(x, n):
    require(n > 0, "positive denominator required")
    return (x[0] // n, -((-x[1]) // n))


def root(x):
    require(x[0] >= 0, "nonnegative radicand required")
    return (isqrt(x[0] * SCALE), 1 + isqrt(x[1] * SCALE))


def conjugate(z):
    return (z[0], subtract(integer(0), z[1]))


def product(z, w):
    real = subtract(times(z[0], w[0]), times(z[1], w[1]))
    imag = add(times(z[0], w[1]), times(z[1], w[0]))
    return (real, imag)


def upper_phase(cosine):
    return (cosine, root(subtract(integer(1), times(cosine, cosine))))


def chord_squared(z):
    # All arguments enclose phases of unit modulus.
    return times(integer(2), subtract(integer(1), z[0]))


def frequency_checks():
    one = (integer(1), integer(0))
    sqrt_five = root(integer(5))
    u = upper_phase(divide_integer(subtract(integer(3), sqrt_five), 8))
    v = upper_phase(divide_integer(add(integer(3), sqrt_five), 8))
    zeta = product(u, conjugate(v))
    zeta_power = one
    for lag in range(1, STATE_CAP + 1):
        zeta_power = product(zeta_power, zeta)
        distance_sq = chord_squared(zeta_power)
        radii = add(root(integer(STATE_CAP)), root(integer(STATE_CAP - lag)))
        rhs = times(integer(2), times(radii, radii))
        require(RESOLVENT_BOUND * distance_sq[0] > rhs[1], f"packing at lag {lag}")

    modes = [one, u, conjugate(u), v, conjugate(v)]
    resonances = {(1, 3), (4, 2)}  # u/v and conjugate(v)/conjugate(u)
    for i, a in enumerate(modes):
        for j, b in enumerate(modes):
            if (i, j) in resonances:
                continue
            shifted = product(product(a, conjugate(b)), conjugate(zeta))
            require(chord_squared(shifted)[0] * 10_000 > 529 * SCALE,
                    f"nonresonant separation at {(i, j)}")
    require(chord_squared(zeta)[0] * 100 > 36 * SCALE, "centering frequency")
    require(chord_squared(product(zeta, zeta))[0] > SCALE, "second harmonic")


def test_bounds():
    null_upper = Fraction(1, 2) * Fraction(2 * RESOLVENT_BOUND, N)**2
    signal_leakage = Fraction(23, 25) * Fraction(200, 23 * N)**2
    centering_leakage = Fraction(1, 2) * Fraction(20, 6 * N)**2
    ideal_lower = Fraction(2, 25) - signal_leakage - centering_leakage
    margin = min(THRESHOLD - null_upper, ideal_lower - THRESHOLD)
    require(margin == Fraction(4523, 250_000), "minimum margin")
    variance_upper = (1 + Fraction(2, N)**2) / 8
    exponent = LAUNCHES * margin**2 / (2 * (variance_upper + margin / 3))
    # For positive x, exp(x) > sum_{j=0}^m x^j/j!.
    require(sum(exponent**j / factorial(j) for j in range(15)) > 20,
            "Bernstein tail exceeds the allowed risk")
    print(f"packing lags passed: {STATE_CAP}")
    print("nonresonant pairs passed: 23")
    print(f"null mean at most: {null_upper}")
    print(f"ideal mean at least: {ideal_lower}")
    print(f"threshold: {THRESHOLD}")
    print(f"minimum margin: {margin}")
    print(f"second-moment bound: {variance_upper}")
    print(f"Bernstein exponent at least: {exponent}")
    print(f"launches: {LAUNCHES}")
    print(f"maximum tick: {4 * (N - 1)}")
    print("each one-sided error is less than 1/20")


if __name__ == "__main__":
    frequency_checks()
    test_bounds()
