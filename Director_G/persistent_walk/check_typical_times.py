"""Verify the five-site return amplitudes and parity moments using exact arithmetic."""
from dataclasses import dataclass
from fractions import Fraction as F
from math import comb, factorial
import json


def require(condition, message):
    if not condition:
        raise ArithmeticError(message)


@dataclass(frozen=True)
class Quadratic:
    """a + b sqrt(5), in the real embedding with sqrt(5) positive."""
    a: F
    b: F = F(0)

    def __add__(self, other):
        return Quadratic(self.a + other.a, self.b + other.b)

    def __sub__(self, other):
        return Quadratic(self.a - other.a, self.b - other.b)

    def __mul__(self, other):
        return Quadratic(self.a * other.a + 5 * self.b * other.b,
                         self.a * other.b + self.b * other.a)

    def __truediv__(self, other):
        conjugate = Quadratic(other.a, -other.b)
        norm = other.a**2 - 5 * other.b**2
        product = self * conjugate
        return Quadratic(product.a / norm, product.b / norm)

    def __pow__(self, exponent):
        value = Quadratic(F(1))
        for _ in range(exponent):
            value = value * self
        return value

    def rational(self):
        require(self.b == 0, 'expected a rational quadratic-field element')
        return self.a


ONE = Quadratic(F(1))
TWO = Quadratic(F(2))
COSINES = (Quadratic(F(-1, 4), F(1, 4)), Quadratic(F(-1, 4), F(-1, 4)))


def check_amplitudes(pairs):
    """Compare both scalar recurrences with exact signed ten-port path counts."""
    traces = [TWO * c**2 for c in COSINES]
    even = [(TWO, s) for s in traces]
    odd = [(ONE, s - ONE) for s in traces]
    # Entries are signed path counts. Actual amplitudes divide them by sqrt(2)^t.
    paths = [1] + [0] * 9
    for t in range(2 * pairs):
        n = t // 2
        if t % 2:
            expected = ONE
            for cosine, (current, _) in zip(COSINES, odd):
                expected = expected + TWO * cosine * current
        else:
            expected = ONE + even[0][0] + even[1][0]
        require(expected.rational() / 5 == F(paths[0], 2**n), "signed port mismatch at tick %d" % t)
        advanced = [0] * 10
        for site in range(5):
            right, left = paths[2 * site:2 * site + 2]
            advanced[2 * ((site + 1) % 5)] = right + left
            advanced[2 * ((site - 1) % 5) + 1] = right - left
        paths = advanced
        if t % 2:
            for modes in (even, odd):
                for j, (current, following) in enumerate(modes):
                    modes[j] = following, traces[j] * following - current


def haar_moment(degree, constant_sq, coefficients_sq):
    """Integrate an even power by expanding it and integrating the two cosines."""
    total = Quadratic(F(0))
    for i in range(0, degree + 1, 2):
        for j in range(0, degree - i + 1, 2):
            k = degree - i - j
            multinomial = factorial(degree) // (factorial(i) * factorial(j) * factorial(k))
            cos_integral = F(comb(i, i // 2) * comb(j, j // 2), 2**(i+j))
            weight = Quadratic(multinomial * cos_integral * constant_sq**(k // 2))
            total = total + weight * coefficients_sq[0]**(i // 2) * coefficients_sq[1]**(j // 2)
    return total.rational()


def main():
    check_amplitudes(pairs=101)
    even_sq = (Quadratic(F(4, 25)),) * 2
    odd_sq = [Quadratic(F(4, 25)) * c**2 / (ONE + c**2) for c in COSINES]
    variances = []
    observed = {}
    for label, c_sq, coeffs in (("even", F(1, 25), even_sq), ("odd", F(1, 50), odd_sq)):
        mean = haar_moment(2, c_sq, coeffs)
        variance = haar_moment(4, c_sq, coeffs) - mean**2
        variances.append(variance)
        observed[label] = {"mean": str(mean), "variance": str(variance)}
    require(variances == [F(36, 625), F(2364, 525625)], 'incorrect parity variances')
    require(observed["even"]["mean"] == "1/5" and observed["odd"]["mean"] == "17/290", 'incorrect parity means')
    mse = sum(variances) / 2
    require(mse == F(3264, 105125), 'incorrect all-tick mean-square error')
    # (12+4 sqrt(3))/25 > 3/4 is equivalent to 16 sqrt(3) > 27.
    require(16**2 * 3 > 27**2, 'phase regions do not separate by more than three quarters')
    print(json.dumps({"matched_signed_ticks": 202, "parity": observed, "minimax_mse": str(mse),
                      "rms_decimal": float(mse)**0.5, "large_error_strict_threshold": "3/8",
                      "all_ticks_density_lower_bound": "1/72"}, indent=2))


if __name__ == "__main__":
    main()
