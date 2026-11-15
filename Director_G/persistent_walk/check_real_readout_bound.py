"""Certify the real-readout Fourier bound and two fresh-setting count decisions."""
from fractions import Fraction as F
from pathlib import Path
from runpy import run_path


N = 250_000
R = 36_733
NULL_UPPER = F(547842242, 10**9)
IDEAL_LOWER = F(625662671, 10**9)


def require(test, detail):
    if not test:
        raise ArithmeticError(detail)


def check_geometry():
    intervals = run_path(str(Path(__file__).with_name("check_shorter_return.py")))
    scale, whole, add, sub, mul, div, sqrt, conj, prod, phase = (
        intervals[name] for name in ("SCALE", "integer", "add", "subtract", "times",
                                     "divide_integer", "root", "conjugate",
                                     "product", "upper_phase")
    )
    sqrt5 = sqrt(whole(5))
    u = phase(div(sub(whole(3), sqrt5), 8))
    v = phase(div(add(whole(3), sqrt5), 8))
    zeta = prod(u, conj(v))
    identity = (whole(1), whole(0))
    lagged = identity
    # For each lag d, the largest sum of cap half-widths is at (55-d, 55).
    # cos(phi_j + phi_k) = (1-j/R)(1-k/R) - sin(phi_j)sin(phi_k).
    def cap_cos(k):
        return div(whole(R-k), R)

    def cap_sin(k):
        return div(sqrt(whole(k*(2*R-k))), R)

    for d in range(1, 56):
        lagged = prod(lagged, zeta)
        cap_sum_cos = sub(mul(cap_cos(55), cap_cos(55-d)),
                          mul(cap_sin(55), cap_sin(55-d)))
        require(lagged[0][1] < cap_sum_cos[0], f"angular separation at lag {d}")

    power = identity
    factor = zeta
    exponent = N
    while exponent:
        if exponent & 1:
            power = prod(power, factor)
        factor = prod(factor, factor)
        exponent //= 2
    real = power[0]
    require(-99 * scale < 1000 * real[0] <= 1000 * real[1] < -98 * scale,
            "rounded phase real part")
    # For real x,y,z in [-1,1], divide x-2wy+w^2 z by w, |w|=1.
    # At a sign vertex, x=z gives a real value of modulus <=2+2|Re w|.
    # The other case x=-z gives squared modulus 4*(2-(Re w)^2).
    cap = F(2821536, 10**6)
    re_abs = F(-real[0], scale)
    re_min_abs = F(-real[1], scale)
    require(2+2*re_abs < cap and 4*(2-re_min_abs**2) < cap**2,
            "real numerator vertex bound")
    null = F(1, 2) + F(1, 2) * F(R, N)**2 * cap / F(636615, 10**6) + F(1, 10**9)
    ideal = F(1, 2) + F(20699999689, 258750000000) / F(636625, 10**6) - F(1, 10**9)
    require(null < NULL_UPPER and ideal > IDEAL_LOWER, "fresh-setting endpoints")
    print("55 angular-cap separations; resolvent <= 36733")
    print("Real numerator vertex bound < 2.821536")
    print("Fresh-setting null success < 0.547842242; ideal success > 0.625662671")


def check_decisions():
    tails = run_path(str(Path(__file__).with_name("check_one_port_boundary.py")))
    boundary = tails["boundary_probabilities"]
    alpha = F(1, 20)
    null_tail, null_point = boundary(431, 253, NULL_UPPER)
    ideal_tail, ideal_point = boundary(431, 253, IDEAL_LOWER)
    optimal = (alpha - null_tail) / null_point
    require(0 < optimal < 1 and ideal_tail + optimal*ideal_point < F(949470, 10**6),
            "431 endpoint power ceiling")

    coin = F(858, 1024)
    null_tail, null_point = boundary(432, 254, NULL_UPPER)
    ideal_tail, ideal_point = boundary(432, 254, IDEAL_LOWER)
    require(null_tail + coin*null_point < F(49988, 10**6) and
            ideal_tail + coin*ideal_point > F(950023, 10**6),
            "432 randomized rule")
    size, _ = boundary(437, 256, NULL_UPPER)
    power, _ = boundary(437, 256, IDEAL_LOWER)
    require(size < F(49878, 10**6) and power > F(952065, 10**6), "437 fixed rule")
    print("431 launches: best endpoint power at size 5% < 0.949470")
    print("432 launches: reject above 254, or with 858/1024 at 254;"
          " size < 0.049988, power > 0.950023")
    print("437 launches: reject at >= 257; size < 0.049878, power > 0.952065")


if __name__ == "__main__":
    check_geometry()
    check_decisions()
