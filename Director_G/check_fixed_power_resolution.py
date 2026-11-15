"""Fixed-power hiding interval for the registered six-well spectrum."""
from argparse import ArgumentParser
from decimal import Decimal, ROUND_CEILING, ROUND_FLOOR, localcontext
from fractions import Fraction
from itertools import product
import json
from math import isqrt
from pathlib import Path


def power_bounds(v, exponent):
    """Enclose exp(exponent*ln(v)) for an integer v>0 and exact exponent >=0.

    Python decimal ln and exp are correctly rounded to nearest. Adjacent
    representable numbers enclose the true result at the chosen precision.
    """
    with localcontext() as ctx:
        ctx.prec = 65
        logv = Decimal(v).ln()
        ctx.rounding = ROUND_FLOOR
        lower = exponent*logv.next_minus()
        ctx.rounding = ROUND_CEILING
        upper = exponent*logv.next_plus()
        return lower.exp().next_minus(), upper.exp().next_plus()


def surplus_interval(row, s, smallest):
    """Enclose sum a^(1+s) - sum(a)*smallest^s without cancellation tests."""
    terms = [power_bounds(a, 1+s) for a in row]
    ref_lo, ref_hi = power_bounds(smallest, s)
    with localcontext() as ctx:
        ctx.prec = 65
        ctx.rounding = ROUND_CEILING
        ref_upper = sum(row)*ref_hi
        ctx.rounding = ROUND_FLOOR
        ref_lower = sum(row)*ref_lo
        low = sum(a for a, b in terms) - ref_upper
        ctx.rounding = ROUND_CEILING
        high = sum(b for a, b in terms) - ref_lower
        return str(low), str(high)


def normalized(v):
    return [Fraction(x, sum(v)) for x in v]


def zero_box_witness(rows):
    masses = list(map(sum, rows))
    target = [Fraction(m, min(masses)) for m in masses]
    upper = [len(row) for row in rows]
    split = [(y-1)/(n-1) for y, n in zip(target, upper)]
    weights = []
    for bits in product((False, True), repeat=len(rows)):
        corner = [n if bit else 1 for bit, n in zip(bits, upper)]
        bary = Fraction(1)
        for bit, b in zip(bits, split):
            bary *= b if bit else 1-b
        weights.append((bits, bary*sum(corner)/sum(target), normalized(corner)))
    assert all(w >= 0 for _, w, _ in weights) and sum(w for _, w, _ in weights) == 1
    mix = [sum(w*p[x] for _, w, p in weights) for x in range(len(masses))]
    assert mix == normalized(masses)
    return [{"all_modes_separate": b, "weight": str(w),
             "site_law": list(map(str, p))} for b, w, p in weights]


def run():
    source = Path(__file__).with_name("results") / "pure_mass_criterion.json"
    record = json.loads(source.read_text(encoding="utf-8"))["six_wells"]
    amps = record["cover_amplitudes"]
    rows = [[v*v for row in (amps[x], amps[x+6]) for v in row if v]
            for x in record["base_sites"]]
    masses = list(map(sum, rows))
    minimum = min(masses)
    assert masses == [729, 558, 761] and list(map(len, rows)) == [3, 3, 3]
    # Record outward enclosures at both sides, including nonbinding rows.
    endpoints = {}
    for q in ("1.2675150158", "1.2675150159"):
        bounds = [surplus_interval(row, Decimal(q)-1, minimum) for row in rows]
        endpoints[q] = bounds
    assert all(Decimal(upper) < 0 for lower, upper in endpoints["1.2675150158"])
    assert Decimal(endpoints["1.2675150159"][2][0]) > 0
    assert all(Decimal(hi) < 0 for _, hi in endpoints["1.2675150159"][:2])
    squared = [sum(a*a for a in row) for row in rows]
    roots = [[isqrt(a) for a in row] for row in rows]
    assert all(r*r == a for rs, cells in zip(roots, rows) for r, a in zip(rs, cells))
    assert all(m >= 23**2 and m <= 23*sum(rs) for m, rs in zip(masses, roots))
    # q=2 needs max(split_i / m_i) <= minimum. The third bin violates it.
    assert squared[2] > masses[2]*minimum
    return {"base_sites": record["base_sites"], "positive_mode_masses": rows,
            "ordinary_bin_masses": masses, "q0_vertex_mixture": zero_box_witness(rows),
            "q_half_common_box_point": [str(Fraction(m, 23)) for m in masses],
            "q_half_split_weights": list(map(sum, roots)),
            "q2_minimum_required_ratios": [str(Fraction(v, m)) for v, m in zip(squared, masses)],
            "root_surplus_bounds_by_site": endpoints}


if __name__ == "__main__":
    cli = ArgumentParser(description=__doc__)
    cli.add_argument("output", type=Path)
    args = cli.parse_args()
    with args.output.open("x", encoding="utf-8", newline="\n") as f:
        json.dump(run(), f, indent=2)
        f.write("\n")
