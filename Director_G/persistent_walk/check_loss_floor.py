"""Certify fixed-budget launch lower bounds using rational path counts and logarithm bounds."""
from fractions import Fraction as F
from decimal import Decimal, localcontext
import json

STATE_CAP = 55


def require(ok, message):
    if not ok:
        raise ArithmeticError(message)


def next_counts(current):
    following = [0] * 10
    for site in range(5):
        right, left = current[2 * site:2 * site + 2]
        following[2 * ((site + 1) % 5)] = right + left
        following[2 * ((site - 1) % 5) + 1] = right - left
    return following


def maximum_after_prefix(r):
    """All remaining probabilities are <=1, hence the geometric stopping certificate."""
    best = F(0)
    at_tick = None
    counts = [1] + [0] * 9
    tick = 0
    survival = F(1)
    while True:
        if tick >= STATE_CAP - 1:
            if survival <= best:
                return at_tick, best, tick
            tail_click = survival * F(counts[0]**2, 2**tick)
            if tail_click > best:
                best, at_tick = tail_click, tick
        counts = next_counts(counts)
        tick += 1
        survival *= r


def logarithm_interval(x, terms):
    """For x>=1, enclose ln(x) by the 2*atanh series and a geometric tail."""
    require(x >= 1, "positive logarithm required")
    a = (x - 1) / (x + 1)
    square = a * a
    power = a
    total = F(0)
    for k in range(terms):
        total += 2 * power / (2*k + 1)
        power *= square
    return total, total + 2 * power / ((2*terms+1) * (1-square))


def ceiling(x):
    return -(-x.numerator // x.denominator)


def certified_ceiling(lower, upper):
    first, last = ceiling(lower), ceiling(upper)
    require(first == last, "logarithm bounds straddle an integer")
    return first


def decimal_text(x):
    with localcontext() as context:
        context.prec = 15
        return str(Decimal(x.numerator) / Decimal(x.denominator))


def main():
    log19_lo, log19_hi = logarithm_interval(F(19), 360)
    outputs = []
    for rate in (F(63,100), F(4,5), F(9,10)):
        tick, delta, close = maximum_after_prefix(rate)
        lo, hi = logarithm_interval(1 / (1 - delta), 10)
        zero_floor = certified_ceiling(log19_lo / hi, log19_hi / lo)

        dark = F(1,100)
        excursion = (1-dark)*delta
        variance_floor = min(dark*(1-dark), (dark+excursion)*(1-dark-excursion))
        factor = 8 * variance_floor * F(9,10) / excursion**2
        with_floor = certified_ceiling(factor*log19_lo, factor*log19_hi)
        outputs.append({"survival": str(rate), "maximizing_tick": tick,
                        "envelope_closes_at_tick": close, "tail_click_max": decimal_text(delta),
                        "necessary_launches_dark_zero": zero_floor,
                        "necessary_launches_dark_one_percent": with_floor})

    require([row["maximizing_tick"] for row in outputs] == [58, 60, 60],
            "incorrect tail maximum")
    require([row["necessary_launches_dark_zero"] for row in outputs]
            == [2407270941225, 2276494, 1940], "changed noiseless-background lower bound")
    print(json.dumps(outputs, indent=2))


if __name__ == "__main__":
    main()
