"""Identify an exogenous unread site-copy word by zero-field rail switches.

Run: python -B check_copy_word_inversion.py NEW_DIRECTORY
All arithmetic is exact. Bit i means a copy after the (i+1)st rail switch.
Each switch is a two-H-tick projection to the rail opposite its input.
"""

import argparse
from collections import defaultdict
from fractions import Fraction
import json
from math import comb, factorial, prod
from pathlib import Path


def require(condition, message):
    if not condition:
        raise ArithmeticError(message)


def arrows(incoming, x):
    """Both physical middle rails; keep the required final opposite rail."""
    final = -incoming
    for middle in (1, -1):
        sign1 = -1 if incoming == middle == -1 else 1
        sign2 = -1 if middle == final == -1 else 1
        yield x + middle + final, sign1 * sign2


def rail_density(m, mask, incoming):
    # Integer ket/bra pairs at denominator 4**j after j switches.
    density = {(0, 0): 1}
    for tick in range(m):
        updated = defaultdict(int)
        copying = mask & (1 << tick)
        for (x, y), amp in density.items():
            for a, sa in arrows(incoming, x):
                for b, sb in arrows(incoming, y):
                    if not copying or a == b:
                        updated[a, b] += sa * sb * amp
        density = updated
        incoming = -incoming
    return sum(amp for (x, y), amp in density.items() if x == y)


def pointer_paths(m, mask, incoming):
    # Literally propagate the two physical ticks. A site pointer appends its
    # address to the basis word; all retained pointers remain orthogonal.
    states = {(0, incoming, ()): 1}
    for tick in range(2*m):
        updated = defaultdict(int)
        on_projection = tick % 2 == 1
        for (site, rail, tags), amp in states.items():
            for out in (1, -1):
                if on_projection and out != -incoming:
                    continue
                new_site = site + out
                sign = -1 if out == rail == -1 else 1
                new_tags = tags
                if on_projection and mask & (1 << (tick//2)):
                    new_tags = tags + (new_site,)
                updated[new_site, out, new_tags] += sign*amp
        states = updated
        if on_projection:
            incoming = -incoming
    return sum(amp*amp for amp in states.values())


def mobius(values, upper):
    transformed = list(values)
    d = (len(values)-1).bit_length()
    for bit in (1 << i for i in range(d)):
        for mask in range(len(values)):
            if (mask & bit == 0) == upper:
                transformed[mask] -= transformed[mask ^ bit]
    return transformed


def binomial_weight(j):
    return Fraction(comb(2*j, j), 4**j)


def segment_product(m, mask, connected):
    cuts = [0] + [j for j in range(1, m) if mask & (1 << (j-1))] + [m]
    lengths = [v-u for u, v in zip(cuts, cuts[1:])]
    return prod(binomial_weight(j)/(2*j-1 if connected else 1) for j in lengths)


def observe(kernel, law):
    return [sum((weight*kernel[x | f] for x, weight in enumerate(law) if weight),
                Fraction(0)) for f in range(len(kernel))]


def invert(means, connected):
    cumulative = [y/b for y, b in zip(mobius(means, upper=True), connected)]
    return mobius(cumulative, upper=False)


def common_numerators(values, denominator):
    scaled = [v*denominator for v in values]
    require(all(x.denominator == 1 for x in scaled), "inexact table denominator")
    return [int(x) for x in scaled]


def priors(d):
    n = 1 << d
    for name, weights in (
        ("no_copy", [int(x == 0) for x in range(n)]),
        ("all_copy", [int(x == n-1) for x in range(n)]),
        ("iid_one_third", [2**(d-x.bit_count()) for x in range(n)]),
        ("copy_all_or_none", [int(x == 0) + 2*int(x == n-1) for x in range(n)]),
        ("order_sensitive_full_support",
         [1 + ((13*x + 5*(x ^ (x >> 1)).bit_count()) % 17) for x in range(n)]),
    ):
        yield name, weights


def check_prior(m, kernel, connected, name, weights):
    d, n = m-1, len(kernel)
    denominator = sum(weights)
    law = [Fraction(w, denominator) for w in weights]
    means = observe(kernel, law)
    recovered = invert(means, connected)
    require(law == recovered, "full word inversion")
    c_m = connected[0]
    signs = [(-1)**f.bit_count() for f in range(n)]
    parity_mean = sum(s*y for s, y in zip(signs, means))/n
    require(n*parity_mean/c_m == law[0], "random fair mask score")
    second_moment = n*sum(means)/c_m**2
    require(second_moment >= law[0]**2, "unconditional one-shot variance")
    # Unlabelled independent forcing, with each boundary left alone with
    # probability t. The constant term is a known deterministic-mask result.
    interpolated = []
    if d:
        for j in range(d+1):
            t = Fraction(j, d)
            interpolated.append(sum(y*(1-t)**f.bit_count()*t**(d-f.bit_count())
                                    for f, y in enumerate(means)))
        diff = sum((-1)**(d-j)*comb(d,j)*v for j,v in enumerate(interpolated))
        require(diff*d**d/factorial(d) == c_m*law[0], "untagged forcing-rate inversion")
    return dict(name=name, prior_denominator=denominator, prior_numerators=weights,
                means_denominator=denominator*4**m,
                means_numerators=common_numerators(means, denominator*4**m),
                recovered_prior_numerators=common_numerators(recovered, denominator),
                signed_fair_mask_mean=str(parity_mean),
                signed_estimator_variance=str(second_moment-law[0]**2),
                untagged_means_at_t_j_over_d=list(map(str, interpolated)))


def minimality_witnesses(kernel, connected):
    # Hold every mean but one fixed, by perturbing the interior uniform law.
    n = len(kernel)
    rows = []
    for f in range(n-1):
        shift = [Fraction(int(j == f)) for j in range(n)]
        v = invert(shift, connected)
        require(sum(v) == 0 and v[0] != 0, "omitted proper setting alters all-clear")
        require(observe(kernel, v) == shift, "isolated setting direction")
        eps = 1/(2*n*max(map(abs,v)))
        perturbed = [Fraction(1,n)+eps*w for w in v]
        require(min(perturbed) > 0 and sum(perturbed) == 1, "positive alternative")
        rows.append(dict(omitted=f, sole_mean_change=str(eps),
                         alternative_all_clear=str(perturbed[0])))
    return rows


def census(m):
    d = m-1
    n = 1 << d
    right = [rail_density(m, f, 1) for f in range(n)]
    left = [rail_density(m, f, -1) for f in range(n)]
    require(right == left, "two launch rails")
    kernel = [Fraction(k, 4**m) for k in right]
    require(kernel == [segment_product(m, f, False) for f in range(n)], "gap formula")
    connected = mobius(kernel, upper=True)
    require(connected == [segment_product(m, f, True) for f in range(n)],
            "strictly positive union spectrum")
    require(kernel[-1] == Fraction(1, 2**m), "blind all-forced/count control")
    terminal = [rail_density(m, f | n, 1) for f in range(n)]
    require(terminal == right, "terminal address copy invisible in pass probability")
    if m <= 5:
        for rail in (1, -1):
            for f in range(2*n):
                require(pointer_paths(m, f, rail) == right[f % n], "literal named pointers")
    return dict(m=m, dimension=n, denominator=4**m, right_kernel_numerators=right,
                left_kernel_numerators=left, extra_final_copy_right_numerators=terminal,
                connected_numerators=common_numerators(connected, 4**m),
                literal_pointer_checks_both_launches_and_final_copy=4*n if m<=5 else 0,
                proper_setting_omissions=(minimality_witnesses(kernel, connected) if m<=6 else None),
                priors=[check_prior(m, kernel, connected, name, weights)
                        for name, weights in priors(d)])


def controls():
    kernel = [Fraction(rail_density(3, f, 1), 4**3) for f in range(4)]
    one = [Fraction(v) for v in (0,1,0,0)]
    mix = [Fraction(v,3) for v in (1,0,0,2)]
    pure_rows, mixed_rows = observe(kernel, one), observe(kernel, mix)
    require(pure_rows[0] == mixed_rows[0] and pure_rows != mixed_rows,
            "unforced alone is blind")
    # Illegal setting-dependent leakage copies the mixture at F=0, and takes
    # the deterministic law on all other trials.
    illegal_rows = [mixed_rows[0], *pure_rows[1:]]
    require(illegal_rows == pure_rows, "exogeneity counterexample")
    count_rows = [Fraction(1,8)]*4
    require(count_rows == observe(kernel, [0,0,0,1]), "persistent fair count mimic")
    return dict(m=3, proper_single_cut_prior=list(map(str,one)), correlated_prior=list(map(str,mix)),
                single_cut_means=list(map(str,pure_rows)), correlated_means=list(map(str,mixed_rows)),
                forced_dependent_rival_means=list(map(str,illegal_rows)),
                forced_dependent_rival_unforced_all_clear=str(mix[0]),
                persistent_fair_count_and_always_copy_means=list(map(str,count_rows)))


def run():
    return dict(
        definitions=dict(mask="Bit j-1 is an unread sharp site copy after switch j; rows in increasing integer mask order.",
                         switches="Two signed H ticks followed by an opposite-rail pass. Launch is sharp at 0. Zero field, unwrapped line.",
                         kernel="All-pass mass for the indicated copy mask. For ideal forcing F and exogenous X the row is kernel[F OR X]. Failure is its complement.",
                         connected="Upper Boolean difference of kernel; all entries positive. Upper difference of observed means divided entrywise by connected gives Pr(X subset U).",
                         scope="Independent setting, stable exogenous word law, squared named records, calibrated copy instrument. Boundary correlations allowed. An endpoint copy or fair-count admixture cannot be separated from every rival by these pass rates alone.",
                         minimality="All proper deterministic settings needed for arbitrary exogenous all-clear weight given the known all-copy rate. The fair random mask permits one parity-tagged signed statistic. The variance is per original trial, including failures."),
        orders=[census(m) for m in range(1,9)], controls=controls())


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("destination", type=Path)
    path = parser.parse_args().destination / "copy_word_inversion.json"
    if path.exists():
        raise FileExistsError(path)
    result = run()
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("x", encoding="utf-8", newline="\n") as stream:
        json.dump(result, stream, indent=2, allow_nan=False)
        stream.write("\n")
