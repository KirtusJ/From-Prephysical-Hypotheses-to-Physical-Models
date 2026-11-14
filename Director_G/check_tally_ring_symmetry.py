"""Check the Tally Ring phase-orbit calculation in integer root coordinates."""
from itertools import product
from math import gcd, lcm


def require(condition, message):
    if not condition:
        raise ValueError(message)


def transformed(coin, order, global_phase, rail_phase, ramp):
    a, b, c, d = coin
    shifts = (ramp, -rail_phase-ramp, rail_phase+ramp, -ramp)
    return tuple((e+global_phase+s) % order for e, s in zip((a,b,c,d), shifts))


def invariant(exponent, modulus):
    return min(exponent % modulus, -exponent % modulus)


def verify(n, image):
    order = lcm(n, image)
    gains = list(range(0, order, order//image))
    m = n//gcd(n, 2)
    checks = 0
    for a, b, c in product(gains, repeat=3):
        d = (order//2+b+c-a) % order
        u = (b+c-2*a) % order
        coin = transformed((a,b,c,d), order, -a, a-c, 0)
        require(coin == (0, u, 0, (order//2+u) % order), "canonical form")
        checks += 1
    for u in gains:
        canonical = (0, u, 0, (order//2+u) % order)
        reachable = set()
        for ramp in range(0, order, order//n):
            coin = transformed(canonical, order, -ramp, 0, ramp)
            v = (u-2*ramp) % order
            require(coin == (0, v, 0, (v+order//2) % order), "periodic rephasing")
            reachable.update((v, -v % order))
        for v in gains:
            require((v in reachable) == (invariant(m*u, order) == invariant(m*v, order)),
                    "orbit and real part disagree")
            checks += 1
    return checks


if __name__ == "__main__":
    total = sum(verify(n, image) for n in range(3, 15) for image in (2, 4, 6, 8, 10))
    # Four-site ring, using fourth-root exponents. Real ramps have exponents 0 or 2.
    require({(-2*r) % 4 for r in (0, 2)} == {0}, "restricted sign ramps")
    require((-2*1) % 4 == 2 and invariant(2*2, 4) == invariant(0, 4),
            "complex ramp connects the real coins")
    print(f"{total} coin and orbit checks; four-site restricted counterexample verified")
