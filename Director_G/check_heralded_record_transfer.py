"""Check posterior and record counterexamples, exact late-parity counts and refinement."""
import argparse
from fractions import Fraction as Q
from itertools import product
import json
from pathlib import Path


def require(condition, message):
    if not condition:
        raise ValueError(message)


def rare_herald(k):
    # Split H over n equal cells and place the rejected mass in one cell.
    # Ratios of square roots are rational for these chosen k and n.
    y = Q(1, k*k+1)
    n = k**6
    # Sum of square roots in H is sqrt(n*y), outside sqrt(1-y).
    accepted_bad = Q(k*k, k*k+1)
    bad_prior = y
    posterior = bad_prior*accepted_bad / ((1-bad_prior)*y + bad_prior*accepted_bad)
    require(accepted_bad**2*(1-y) == (1-accepted_bad)**2*n*y, "square-root herald yield")
    require(posterior == Q(1,2), "selection amplification")
    return dict(k=k, cells_in_herald=n, ordinary_yield=y, bad_prior=bad_prior,
                bad_exponent="1/2", bad_yield=accepted_bad, bad_posterior=posterior)


def power_samples():
    rows = []
    for k in (2,4,8,16,32):
        n = 2**k
        q = 1+Q(1,k)
        # Two tube masses 1/2, second decomposed into 2^k equal words.
        # After taking q-th powers their ratio is n^(1-q)=1/2.
        require((1-q)*k == -1, "mistuned split group")
        rows.append(dict(cells_in_split_tube=n, exponent=q, ordinary_split_tube=Q(1,2),
                         powered_split_tube=Q(1,3), powered_after_grouping=Q(1,2)))
    return rows


def parity_panel(bits, nchecks):
    masks = range(1 << bits)
    failures_for_difference = {}
    for diff in masks:
        agreement = sum((mask & diff).bit_count() % 2 == 0 for mask in masks)
        mismatch = 1 - Q(agreement, 1 << bits)**nchecks
        expected = (1-Q(1,2**nchecks)) if diff else 0
        require(mismatch == expected, "uniform late parity sensitivity")
        failures_for_difference[diff] = mismatch
    return dict(bits=bits, independent_checks=nchecks, failures_for_every_xor=failures_for_difference)


def audit_counterexamples():
    # Online readers return the designated bit faithfully or its complement on
    # the second position. Different expected correlated paths at a crossing.
    records=[(x,x^1,x) for x in (0,1)]  # first side, stored last side, reported last side
    require(sum(b for _,b,_ in records) == sum(c for _,_,c in records), "marginal honesty")
    require(all(b != c for _,b,c in records), "opposite crossing histories")
    # Auditor reveals one of two masks before report. Alter the word by an
    # element of the indicated mask's kernel. All reported hashes pass.
    adaptive = []
    for mask in range(4):
        diff = next(d for d in range(1,4) if (mask & d).bit_count()%2 == 0)
        adaptive.append([mask,diff])
    return dict(crossing_records=records, early_two_bit_mask_and_invisible_falsification=adaptive)


def good_power_bound():
    # Rational power q=2 gives an exactly computable boundary check. Additional
    # nonintegral probes below use floats only as a numerical cross-check.
    rows = []
    for raw in ((1,), (0,1,1), (1,3,15,27), (1,2,3,4,5,6)):
        support = sum(x>0 for x in raw)
        p = [Q(x,sum(raw)) for x in raw]
        for q in (0.125,0.75,1.0,1.25,1.875):
            weights = [float(x)**q for x in p]
            tv = sum(abs(float(x)-z/sum(weights)) for x,z in zip(p,weights))/2
            bound = min(1.0, support**abs(q-1)-1)
            require(tv <= bound + 1e-15, "finite support bound")
            rows.append(dict(weights=raw, q=q, tv=tv, bound=bound))
        norm = sum(x*x for x in p)
        exact = sum(abs(x*x/norm-x) for x in p)/2
        require(exact <= support-1, "exact square boundary")
    return rows


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output",type=Path)
    args = parser.parse_args()
    result = dict(rare_herald=[rare_herald(k) for k in (2,4,8,32,128)],
                  refinement=power_samples(), read_audits=[parity_panel(d,c) for d,c in
                  product((1,2,3,4),(1,2))], counterexamples=audit_counterexamples(),
                  finite_support_checks=good_power_bound())
    with args.output.open("x",encoding="utf8",newline="\n") as out:
        json.dump(result,out,indent=2,default=str,allow_nan=False)
        out.write("\n")


if __name__ == "__main__":
    main()
