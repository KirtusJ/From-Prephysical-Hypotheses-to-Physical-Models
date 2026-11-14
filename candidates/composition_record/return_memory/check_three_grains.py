"""Certify positive per-gain contrasts for all q>0 other than 1. Python standard library."""
from decimal import Context, Decimal, ROUND_CEILING, ROUND_FLOOR
from functools import cache
from itertools import permutations


DOWN = Context(prec=48, rounding=ROUND_FLOOR)
UP = Context(prec=48, rounding=ROUND_CEILING)
NEAREST = Context(prec=48)


class I:
    """Closed interval. All finite endpoints and operations use outward rounding."""
    def __init__(self, lo, hi=None):
        self.lo = Decimal(lo)
        self.hi = self.lo if hi is None else Decimal(hi)
        if self.lo > self.hi:
            raise ArithmeticError("unordered interval")

    def __add__(self, other):
        return I(DOWN.add(self.lo, other.lo), UP.add(self.hi, other.hi))

    def __neg__(self):
        return I(self.hi.copy_negate(), self.lo.copy_negate())

    def __sub__(self, other):
        return self + (-other)

    def __mul__(self, other):
        ends = [(x, y) for x in (self.lo, self.hi) for y in (other.lo, other.hi)]
        return I(min(DOWN.multiply(x, y) for x, y in ends),
                 max(UP.multiply(x, y) for x, y in ends))

    def __truediv__(self, other):
        if other.lo <= 0 <= other.hi:
            raise ArithmeticError("possible zero divisor")
        return self * I(DOWN.divide(Decimal(1), other.hi), UP.divide(Decimal(1), other.lo))


ZERO, ONE, TWO = I(0), I(1), I(2)


@cache
def log_weight(x, largest):
    if x == largest:
        return ZERO
    # Decimal.ln and .exp are correctly rounded to nearest-even: take one
    # representable neighbor outward. Do not use Decimal's general power().
    def ln(k):
        n = NEAREST.ln(Decimal(k))
        return I(NEAREST.next_minus(n), NEAREST.next_plus(n))
    return ln(x) - ln(largest)


def term(q, rate, tail):
    if rate is ZERO:
        return ONE
    x = q * rate
    high = NEAREST.next_plus(NEAREST.exp(x.hi))
    if tail:
        # All rates other than the exactly-zero leader are strictly negative.
        if rate.hi >= 0:
            raise ArithmeticError("unbounded-tail sign")
        return I(0, high)
    return I(NEAREST.next_minus(NEAREST.exp(x.lo)), high)


NORM = (8, 8, 32, 32, 32, 32, 32, 32)
TARGET = (1, 2, 1, 8, 9, 6, 18, 21)
P = tuple(I(a)/I(b) for a, b in zip(TARGET, NORM))
SITE = ((1,), (1, 1), (1,), (4, 4), (4, 5), (1, 5), (1, 17), (4, 17))
PORT = ((1,), (1, 1), (1,), (4, 4), (1, 4, 4), (1, 1, 4), (1, 1, 16), (1, 4, 16))
S3, S5 = (1, 1, 1, 5), (1, 1, 4, 4, 5, 17)
R3, R5 = (1, 1, 1, 1, 4), (1, 1, 1, 1, 4, 4, 4, 16)
MASK = tuple(((a,), (a, n-a)) for a, n in zip(TARGET, NORM))
GRAINS = (MASK, tuple(zip(SITE, (S3, S3) + (S5,)*6)),
          tuple(zip(PORT, (R3, R3) + (R5,)*6)))

def check_walk_inputs():
    """Enumerate the actual path signs for the eight settings and both controls."""
    settings = [(3, 5), (3, 3), (5, 4), (5, 1), (5, 3), (5, 5),
                (5, 6), (5, 8), (3, 0), (3, 1)]
    for i, (ticks, source) in enumerate(settings):
        field = [[0, 0] for _ in range(9)]
        for word in range(2**ticks):
            site, previous, sign = source, 0, 1
            for step in range(ticks):
                rail = (word >> step) & 1
                if rail == previous == 1:
                    sign = -sign
                site = (site + (1 if rail == 0 else -1)) % 9
                previous = rail
            field[site][rail] += sign
        squares = [[v*v for v in rails] for rails in field]
        target = [squares[0], squares[2]]
        def spectra(wells):
            return (sorted(sum(row) for row in wells if sum(row)),
                    sorted(x for row in wells for x in row if x))
        if i < len(TARGET):
            sites, ports = GRAINS[1][i], GRAINS[2][i]
            wanted_target = (sorted(sites[0]), sorted(ports[0]))
            wanted_full = (sorted(sites[1]), sorted(ports[1]))
            if spectra(target) != wanted_target or spectra(squares) != wanted_full:
                raise ArithmeticError(f"spectrum mismatch at {ticks}, {source}")
        else:
            wanted = ([], []) if source == 0 else ([1, 5], [1, 1, 4])
            if spectra(target) != wanted:
                raise ArithmeticError(f"calibration mismatch at {ticks}, {source}")


def probabilities(grain, q, order, tail=False):
    """Taylor derivatives through requested order for (sum target)/(sum all).

    Divide every exponential by largest**q first; the same quotient and all
    derivatives then use terms exp(q log(weight/largest)) which stay bounded.
    """
    @cache
    def moments(cells, largest):
        sums = [ZERO] * (order + 1)
        for x in set(cells):
            rate = log_weight(x, largest)
            value = I(cells.count(x)) * term(q, rate, tail)
            for j in range(order + 1):
                sums[j] = sums[j] + value
                value = value * rate
        return sums

    ans = []
    for target, all_cells in grain:
        largest = max(all_cells)
        n, z = moments(target, largest), moments(all_cells, largest)
        p = n[0]/z[0]
        if order == 0:
            ans.append(p)
            continue
        dp = (n[1]-p*z[1])/z[0]
        ans.append(dp if order == 1 else (n[2]-p*z[2]-TWO*dp*z[1])/z[0])
    return ans


def det(rows):
    value = ZERO
    for perm in permutations(range(3)):
        inversions = sum(a > b for i, a in enumerate(perm) for b in perm[i+1:])
        t = rows[0][perm[0]] * rows[1][perm[1]] * rows[2][perm[2]]
        value = value - t if inversions % 2 else value + t
    return value


def coefficients():
    # The exact w is DEFINED by the three tangent equations; enclosing its
    # floating approximation and merely checking 0 lies in w.P' is insufficient.
    fixed = [ONE, ZERO, ONE, I(-1), I(-1), ZERO, ZERO, I("-0.7")]
    unknown = (1, 5, 6)
    derivs = [probabilities(g, ONE, 1) for g in GRAINS]
    rows = [[v[k] for k in unknown] for v in derivs]
    rhs = [-sum((w*x for w, x in zip(fixed, v)), ZERO) for v in derivs]
    determinant = det(rows)
    if determinant.lo <= 0 <= determinant.hi:
        raise ArithmeticError("undetermined tangent solve")
    for j, k in enumerate(unknown):
        replaced = [[rhs[i] if c == j else row[c] for c in range(3)]
                    for i, row in enumerate(rows)]
        fixed[k] = det(replaced) / determinant
    return fixed


def certify():
    check_walk_inputs()
    weights = coefficients()
    for name, grain in zip(("whole mask", "sites", "oriented ports"), GRAINS):
        if any(sum(num)*n != sum(den)*a
               for (num, den), a, n in zip(grain, TARGET, NORM)):
            raise ArithmeticError("inconsistent exact ordinary mass")

        def gap(span, order=0, tail=False):
            v = probabilities(grain, span, order, tail)
            if order == 0:
                v = [x-p for x, p in zip(v, P)]
            return sum((w*x for w, x in zip(weights, v)), ZERO)

        def cover(left, right, order, threshold=Decimal(0)):
            pending = [(Decimal(left), Decimal(right))]
            count = 0
            minimum = Decimal("Infinity")
            while pending:
                l, r = pending.pop()
                bound = gap(I(l, r), order).lo
                if bound > threshold:
                    minimum = min(minimum, bound)
                    count += 1
                    continue
                mid = NEAREST.divide(NEAREST.add(l, r), Decimal(2))
                if mid == l or mid == r or count + len(pending) > 100000:
                    raise ArithmeticError(f"cannot certify {name}: {l}, {r}, order {order}")
                pending.extend(((l, mid), (mid, r)))
            return count, minimum

        # Exact zero and slope at 1 follow from the mass identities and Cramer's
        # rule above; a positive second derivative covers both punctured sides.
        center = cover("0.95", "1.05", 2)
        left = cover("0", "0.95", 0)
        right = cover("1.05", "64", 0)
        tail = gap(I(64), tail=True).lo
        if tail <= 0:
            raise ArithmeticError(f"cannot certify {name} on [64,infinity)")
        # A prespecified separation from one gives a practically interpretable
        # bound on the gain-weighted frequency of strong power distortions.
        threshold = Decimal("0.06")
        cover("0", "0.5", 0, threshold)
        cover("2", "64", 0, threshold)
        if tail <= threshold:
            raise ArithmeticError(f"gap below outlier threshold for {name}")
        bounds = (left[1], center[1], right[1], tail)
        def lower_text(x):
            quantum = Decimal((0, (1,), x.adjusted()-6))
            return format(DOWN.quantize(x, quantum), ".6e")
        print(f"{name}: counts left/center/right {left[0]}/{center[0]}/{right[0]}; "
              f"lower bounds gap(left), gap''(center), gap(right), gap(tail) "
              + ", ".join(lower_text(x) for x in bounds))
        print(f"{name}: per-gain gap > 0.06 throughout q <= 0.5 and q >= 2")


if __name__ == "__main__":
    certify()
