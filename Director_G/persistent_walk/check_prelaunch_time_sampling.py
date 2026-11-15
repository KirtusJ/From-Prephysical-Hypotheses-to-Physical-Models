"""Exact checks for cosine-weighted time assignment in the five-site return test."""
from array import array
from fractions import Fraction as Q
from math import ceil, isqrt

SCALE = 1 << 112
ACCEPT_LEVELS = 1 << 32
SAMPLER_ALLOWANCE = Q(1, 10**9)
W_LO = Q(636615, 10**6)
W_HI = Q(636625, 10**6)


def require(test, detail):
    if not test:
        raise ValueError(detail)


def sqrt_scaled(value):
    return isqrt(value * SCALE)


def phase_root():
    # cos(alpha)=(3-sqrt(5))/8 and cos(beta)=(3+sqrt(5))/8.
    # Each staged operation below is rounded down on a 112-bit grid.
    s = sqrt_scaled(5 * SCALE)
    a = (3 * SCALE - s) // 8
    b = (3 * SCALE + s) // 8
    sa = sqrt_scaled(SCALE - a * a // SCALE)
    sb = sqrt_scaled(SCALE - b * b // SCALE)
    return ((a * b + sa * sb) // SCALE, (sa * b - a * sb) // SCALE)


def root_enclosure():
    # Evaluate the same radicals a second way with outward integer intervals.
    def add(x, y):
        return (x[0] + y[0], x[1] + y[1])
    def sub(x, y):
        return (x[0] - y[1], x[1] - y[0])
    def mul(x, y):
        v = [i*j for i in x for j in y]
        return (min(v)//SCALE, -((-max(v))//SCALE))
    def sqrt(x):
        return (sqrt_scaled(x[0]), 1 + sqrt_scaled(x[1]))
    def div8(x):
        return (x[0]//8, -((-x[1])//8))
    def whole(x):
        return (x*SCALE, x*SCALE)
    s = sqrt(whole(5))
    a = div8(sub(whole(3), s))
    b = div8(add(whole(3), s))
    sa = sqrt(sub(whole(1), mul(a, a)))
    sb = sqrt(sub(whole(1), mul(b, b)))
    return (add(mul(a, b), mul(sa, sb)), sub(mul(sa, b), mul(a, sb)))


def cosine_centers(count):
    """112-bit fixed-point Re(z^k), in grid units, for k=0,...,count-1."""
    a, b = phase_root()
    u, v = SCALE, 0
    for _ in range(count):
        yield u
        u, v = ((u*a-v*b)//SCALE, (u*b+v*a)//SCALE)


def make_design(n):
    """Build signed acceptance thresholds once for the given horizon."""
    require(n in (250_000, 450_000), "unsupported design")
    signed = array("q")
    for center in cosine_centers(2*n-1):
        amount = min(ACCEPT_LEVELS, ACCEPT_LEVELS*abs(center)//SCALE)
        signed.append(amount if center >= 0 else -amount)
    return signed


def draw_setting(n, signed, randbits):
    """Return (terminal tick, click is a success). Supply independent fair bits.

    Example: signed=make_design(n), then draw_setting(n, signed, secrets.randbits)
    freshly for each launch. Device preparation must be isolated from this choice.
    """
    require(len(signed) == 2*n-1, "mismatched horizon")
    bits = (n-1).bit_length()
    mask = (1 << bits)-1
    while True:
        word = randbits(2*bits + 32)
        j = word & mask
        k = (word >> bits) & mask
        threshold_word = word >> (2*bits)
        if j < n and k < n:
            value = signed[j+k]
            if threshold_word < abs(value):
                return 2*(j+k), value > 0


def check_normalizations():
    # W = E |Re(z^L)| with triangular PMF; z has unit modulus.
    # The powers are centers only. Error propagation is bounded in complex
    # Euclidean norm to avoid exponentially widening coordinate rectangles.
    a, b = phase_root()
    ex, ey = root_enclosure()
    root_error = max(abs(a-i) for i in ex) + max(abs(b-i) for i in ey)
    require(root_error <= 24, "root exceeds 24 lattice units in l1")
    ns = (250_000, 450_000)
    total = {n: 0 for n in ns}
    for k, u in enumerate(cosine_centers(2 * max(ns) - 1)):
        for n in ns:
            weight = n - abs(k - (n-1))
            if weight > 0:
                total[n] += weight * abs(u)
    for n in ns:
        max_steps = 2*n-2
        # error_{k+1} <= error_k + (1+error_k)*24/SCALE + 2/SCALE.
        # By induction error_k <= 50*k/SCALE because this upper bound is <1.
        error = Q(50*max_steps, SCALE)
        require(error < 1, "unit-scale power error budget")
        epsilon = error + Q(1, ACCEPT_LEVELS)
        require(epsilon/(W_LO-epsilon) < SAMPLER_ALLOWANCE, "sampler allowance")
        estimate = Q(total[n], SCALE*n*n)
        require(W_LO < estimate-error and estimate+error < W_HI, "W bounds")
        print(f"N={n}, W in ({W_LO}, {W_HI}), estimate {float(estimate):.13f}")


def upper_tail(n, k, p):
    """Unnormalized integer binomial tail; one common exact denominator."""
    a, b = p.numerator, p.denominator-p.numerator
    term = b**n
    total = 0
    for j in range(n + 1):
        if j >= k:
            total += term
        if j < n:
            numerator = term * (n-j) * a
            divisor = (j+1) * b
            term, remainder = divmod(numerator, divisor)
            require(remainder == 0, "integral binomial recursion")
    return Q(total, p.denominator**n)


def profile(n, k, stochastic_upper, alternative_lower):
    null_p = Q(1,2) + stochastic_upper / W_LO + SAMPLER_ALLOWANCE
    alternative_p = Q(1,2) + alternative_lower / W_HI - SAMPLER_ALLOWANCE
    first = upper_tail(n, k, null_p)
    second = upper_tail(n, n-k+1, 1-alternative_p)
    require(max(first,second) < Q(1,20), "one or both error tails exceed .05")
    print(f"{n} launches, >= {k} successes, "
          f"tails <= {ceil(first * 10**8) / 10**8:.8f}, {ceil(second * 10**8) / 10**8:.8f}")


def main():
    check_normalizations()
    # Controls exercise rejection of invalid candidate coordinates, rounding to
    # zero, and the negative-phase score, using a tiny synthetic table.
    words = iter([3, (1 << 2) + 2, 1])
    require(draw_setting(3, [0,-ACCEPT_LEVELS,0,0,0], lambda bits: next(words))
            == (2, False), "synthetic negative-phase or rejection control")
    require(draw_setting(3, [ACCEPT_LEVELS,0,0,0,0], lambda bits: 0)
            == (0, True), "positive-phase control")
    profile(811, 485, Q(1369,31250), Q(20699999689,258750000000))
    profile(4923, 2858, Q(1369,31250), Q(585539,10**7))
    profile(806, 444, Q(1369,101250), Q(251349,5_000_000))


if __name__ == "__main__":
    main()
