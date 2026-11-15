"""Rigorous finite-duration Fourier witness for return to (0,R) on five sites.

Dyadic interval arithmetic (80 fractional bits plus unbounded integer parts).
The only transcendentals in the definition are specified by algebraic roots.
The output certifies conservative thresholds; no fitting and no device data.
"""
from dataclasses import dataclass
from decimal import Decimal, ROUND_CEILING, ROUND_FLOOR, localcontext
from fractions import Fraction
from math import ceil, isqrt, log
import json


PRECISION = 80
SCALE = 1 << PRECISION


def require(ok, message):
    if not ok:
        raise ValueError(message)


@dataclass(frozen=True)
class Interval:
    lo: int
    hi: int

    def __add__(self, other):
        return Interval(self.lo + other.lo, self.hi + other.hi)

    def __sub__(self, other):
        return Interval(self.lo - other.hi, self.hi - other.lo)

    def __mul__(self, other):
        products = [a*b for a in (self.lo, self.hi) for b in (other.lo, other.hi)]
        return Interval(min(products) // SCALE, -(-max(products) // SCALE))

    def __truediv__(self, other):
        require(0 < other.lo, "Only a strictly positive denominator is supported")
        inverse = Interval(SCALE*SCALE // other.hi,
                           -(-(SCALE*SCALE) // other.lo))
        return self * inverse

    def sqrt(self):
        require(0 <= self.lo, "Negative radicand")
        lower = isqrt(self.lo*SCALE)
        upper = isqrt(self.hi*SCALE)
        upper += int(upper*upper < self.hi*SCALE)
        return Interval(lower, upper)

    def times(self, integer):
        require(integer >= 0, "Expected a nonnegative integer")
        return Interval(integer*self.lo, integer*self.hi)


def point(integer):
    return Interval(SCALE*integer, SCALE*integer)


def numerical_bounds(value):
    with localcontext() as context:
        context.prec = 48
        context.rounding = ROUND_FLOOR
        lower = Decimal(value.lo) / SCALE
        context.rounding = ROUND_CEILING
        upper = Decimal(value.hi) / SCALE
        return [str(lower), str(upper)]


def walk_mode(cosine):
    # Choose the momentum block with cos(k)=cosine and positive sin(k).
    # Fourier Hadamard eigenvalues are exp(i omega) and -exp(-i omega)
    # for the convention in which the right shift multiplies by exp(i k).
    sin_omega = ((point(1) - cosine*cosine) / point(2)).sqrt()
    cos_omega = (point(1) - sin_omega*sin_omega).sqrt()
    # Positive-branch root projector, also including the site's Fourier weight 1/5.
    plus_weight = (point(1) + cosine / (point(2).sqrt()*cos_omega)) / point(10)
    return sin_omega, cos_omega, plus_weight


def main():
    # k=2pi/5 and k=4pi/5, respectively. Both sines are positive.
    cos1 = (point(5).sqrt() - point(1)) / point(4)
    cos2 = (point(-1) - point(5).sqrt()) / point(4)
    s1, c1, weight1 = walk_mode(cos1)
    s2, c2, weight2 = walk_mode(cos2)
    # zeta = exp(i (omega1 - omega2)).
    x = c1*c2 + s1*s2
    y = s1*c2 - c1*s2
    # Four ordered eigenvalue pairs have exactly this ratio, by momentum
    # conjugacy and the signs of the two branches. Others can only add.
    minus1, minus2 = point(1)/point(5) - weight1, point(1)/point(5) - weight2
    spectral_weight = (weight1*weight2 + minus1*minus2).times(2)
    require(Fraction(spectral_weight.lo, SCALE) > Fraction(13, 400),
            "Claimed lower bound on visible weight failed")

    h = 55
    distances = []
    a, b = point(1), point(0)
    for _ in range(1, h+1):
        a, b = a*x - b*y, a*y + b*x
        # Squared distance to 1 for a unit complex number.
        distances.append((point(2) - a.times(2)).sqrt())
    separation = Interval(min(v.lo for v in distances), min(v.hi for v in distances))
    require(Fraction(separation.lo, SCALE) > Fraction(1, 10),
            "Claimed 55-state circle separation failed")

    n = 5_000_000
    # Center the terminal response b at 1/2, leaving a constant part.
    # Prefix Fourier sums for the residual are bounded by 8h/d_h**2.
    # The lag-zero correction costs <=1/(2n). The constant is a
    # nonnegative Fejer kernel <=2/(n**2*|1-zeta|**2).
    d_lower = Fraction(1, 10)
    geometric_upper = (Fraction(16*h, n) + Fraction(2, n*n)) / d_lower**2
    geometric_upper += Fraction(1, 2*n)
    null_upper = Fraction(177, 10000)
    require(geometric_upper < null_upper, "Null bound exceeds rounded threshold")
    ideal_lower = Fraction(13, 400)
    gap = ideal_lower - null_upper
    threshold = (ideal_lower + null_upper) / 2
    # Conservative Hoeffding minimax probabilities: strict differences
    # from the data-independent threshold exceed gap/2. Scores lie in [-1, 1].
    runs = ceil(8*log(20) / float(gap*gap))
    print(json.dumps({
        "max_classical_states": h, "uniform_time_grid_size": n,
        "max_tested_lag": n-1, "dyadic_interval_bits": PRECISION,
        "selected_mode_weight_bounds": numerical_bounds(spectral_weight),
        "circle_separation_bounds": numerical_bounds(separation),
        "strict_classical_mean_upper": str(null_upper),
        "strict_ideal_mean_lower": str(ideal_lower),
        "certified_margin": str(gap),
        "joint_test_threshold": str(threshold),
        "independent_model_launches_for_error_at_most_five_percent": runs,
    }, indent=2))


if __name__ == "__main__":
    main()
