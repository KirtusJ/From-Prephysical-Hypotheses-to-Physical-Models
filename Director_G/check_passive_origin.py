"""Exact passive origin returns and a two-read intervention for the eight-site walk."""
import json
from fractions import Fraction

from check_cairo_cycle import RECORD, require, transfer_matrices, walk_effects


FIRST = frozenset({0, 2})
SECOND = frozenset({0, 2, 4, 10, 14, 16})
LAUNCH_WEIGHTS = ((FIRST, Fraction(5, 8)), (SECOND, Fraction(3, 8)))


def conditional_return(marked, period, lag):
    hits = sum((phase + lag) % period in marked for phase in marked)
    return Fraction(hits, len(marked))


def check_passive_trace():
    # Translation symmetry extends this localized two-column return at 24
    # to the identity on all eight sites and both rails.
    require(transfer_matrices(24) == [(4096, 0, 0, 4096)] + [(0, 0, 0, 0)] * 7,
            "24-step period of the ideal walk")
    rates = []
    for t in range(24):
        diagonal, cross, other = walk_effects(t)[0]
        require(diagonal == other and cross == 0, f"Return depends on input coin at {t}")
        quantum = Fraction(diagonal, 2**t)
        passive = sum(w * conditional_return(s, 24, t) for s, w in LAUNCH_WEIGHTS)
        require(quantum == passive, f"Passive return mismatch at {t}")
        rates.append(quantum)
    require(sum(rates) == Fraction(7, 2), "Return sum for a full observation period")
    return rates


def check_approximations(rates):
    for n in (1, 2, 5):
        blocks = [FIRST] * (5*n) + [SECOND] * n
        marked = {24*i + phase for i, block in enumerate(blocks) for phase in block}
        period = 24 * len(blocks)
        require(len(marked) == 16*n, "Marked phases in concatenated orbit")
        for lag in range(97):
            error = abs(conditional_return(marked, period, lag) - rates[lag % 24])
            require(error <= Fraction(lag, 8*n), f"Two-boundary estimate at {lag}")
        require(conditional_return(marked, period, 24) == 1 - Fraction(1, 4*n),
                "Exact single-orbit deficit at 24")


def check_intervention():
    # Write every two-step amplitude with denominator 2 and every four-step
    # amplitude with denominator 4. Obtain the two full matrices by propagation.
    a, b, c, d = (Fraction(x, 2) for x in transfer_matrices(2)[0])
    through_origin = (a*a + b*c, a*b + b*d, c*a + d*c, c*b + d*d)
    unobserved = tuple(Fraction(x, 4) for x in transfer_matrices(4)[0])
    bypass_origin = tuple(x-y for x, y in zip(unobserved, through_origin))
    for branch, expected in ((unobserved, Fraction(1, 8)),
                             (through_origin, Fraction(1, 4)),
                             (bypass_origin, Fraction(1, 8))):
        a, b, c, d = branch
        require(a*a + c*c == b*b + d*d == expected and a*b + c*d == 0,
                "Projected branch must have the predicted weight for every coin")
    passive_both_hits = sum(w * Fraction(
        sum((p+2) % 24 in s and (p+4) % 24 in s for p in s), len(s))
        for s, w in LAUNCH_WEIGHTS)
    require(passive_both_hits == Fraction(1, 16), "Two passive hits in constructed control")


def check_figure():
    rows = json.loads(RECORD.read_text(), parse_float=Fraction)["cairo_opt_sites_0_to_7_by_tick_0_to_8"]
    center = (rows[2][0] + rows[4][0]) / 2
    radius = (rows[2][0] - rows[4][0]) / 2
    # Mass 'center' has least period two and the remainder has period >8.
    residual = max(abs(row[0] - (center if t % 2 == 0 else 0))
                   for t, row in enumerate(rows) if t > 0)
    require(residual == radius == Fraction(95160, 10**6), "Sharp fit to plotted rates")
    print(f"Displayed site-zero rates at clocks 2 and 4: {float(rows[2][0]):.6f}, "
          f"{float(rows[4][0]):.6f}. Sharp maximum residual: {float(radius):.6f}.")


if __name__ == "__main__":
    rates = check_passive_trace()
    check_approximations(rates)
    check_intervention()
    check_figure()
    print("24 exact passive rates agree. Their sum is 7/2.")
    print("Fourth-step origin rate: 1/8 with no intermediate read, 3/8 with the binary read.")
