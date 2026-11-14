"""Exact stationary copy windows and one-attempt zero-field rail probabilities."""

import argparse
from collections import defaultdict
from fractions import Fraction as F
from functools import cache
from itertools import product
import json
from math import comb, factorial, prod
from pathlib import Path

from check_hidden_site_records import composition_survival, free_prefixes, require


def words(n):
    return product((0, 1), repeat=n)


def bernoulli(word, p):
    ones = sum(word)
    return p**ones * (1-p)**(len(word)-ones)


def regenerative_window(d, p):
    """Likelihoods for the interval model. The length unit is one detector use."""
    def motif(word):
        if any(mark != word[i % d] for i, mark in enumerate(word)):
            return F(0)
        return bernoulli(word[:d], p)

    @cache
    def probability(word, stationary=True):
        if not word:
            return F(1)
        # The residual includes the current use. A fresh interval has a different tail.
        def tail(n):
            return F(1, n) if stationary else F(2, n*(n+1))

        n = len(word)
        mass = tail(n) * motif(word)
        for k in range(1, n):
            mass += (tail(k)-tail(k+1)) * motif(word[:k]) * probability(word[k:], False)
        return mass
    return probability


@cache
def by_segments(word):
    m = len(word)+1
    cuts = [0, *(i for i, mark in enumerate(word, 1) if mark), m]
    return F(prod(comb(2*(end-start), end-start) for start, end in zip(cuts, cuts[1:])), 4**m)


def by_rails(word, rail, *, perturb_left=False):
    """Trace after m switches, with an integer density numerator and denominator 4^m."""
    rho = {(0, 0): 1}
    for copy in (*word, False):
        # From rail R the paths R,R,L and R,L,L end at x and x-2.
        # From L the paths L,R,R and L,L,R end at x+2 and x.
        if rail == 1:
            paths = ((0, 1), (-2, -1))
        else:
            paths = ((2, 1), (0, 1 if perturb_left else -1))
        updated = defaultdict(int)
        for (x, y), entry in rho.items():
            for dx, sx in paths:
                for dy, sy in paths:
                    if not copy or x+dx == y+dy:
                        updated[x+dx, y+dy] += entry * sx * sy
        rho = {xy: entry for xy, entry in updated.items() if entry}
        rail = -rail
    return F(sum(entry for (x, y), entry in rho.items() if x == y), 4**(len(word)+1))


def mixed_difference(middle):
    def w(first, last):
        return by_segments((first, *middle, last))
    return w(0, 0)-w(1, 0)-w(0, 1)+w(1, 1)


def check_first_difference(d, p):
    probability = regenerative_window(d, p)
    for width in range(1, d+1):
        for word in words(width):
            require(probability(word) == bernoulli(word, p), "short calibration word")

    m = d+2
    iid = composition_survival(free_prefixes(m), p)[m]
    mem = F(0)
    for word in words(d+1):
        tied = bernoulli(word[:-1], p) if word[0] == word[-1] else F(0)
        require(probability(word) == (d*bernoulli(word, p)+tied)/(d+1), "first long word")
        mem += probability(word)*by_segments(word)
    diff = sum(bernoulli(y, p)*mixed_difference(y) for y in words(d-1))
    require(mem-iid == p*(1-p)*diff/(d+1) > 0, "first survival gap")
    return dict(window=d, passes=m, independent=str(iid), regenerative=str(mem), gap=str(mem-iid))


def four_pass_panel():
    p = F(1, 3)
    q = 1-p
    independent = composition_survival(free_prefixes(4), p)[4]
    rows = []
    minimum, maximum = -min(p**2, q**2), p*q
    for c0, c1 in ((minimum, minimum), (minimum, maximum), (maximum, minimum),
                   (maximum, maximum), (F(0), F(0)), (F(1, 126), F(-1, 18))):
        left, right = defaultdict(F), defaultdict(F)
        s4 = F(0)
        for a, b, c in words(3):
            covariance = (c0, c1)[b]
            sign = 1 if a == c else -1
            triple = bernoulli((b,), p) * (bernoulli((a, c), p) + sign*covariance)
            require(triple >= 0, "negative triple mass")
            left[a, b] += triple
            right[b, c] += triple
            s4 += triple*by_rails((a, b, c), 1)
        require(left == right == {w: bernoulli(w, p) for w in words(2)}, "stationary pairs")
        require(s4 == independent+F(7, 128)*q*c0+F(1, 64)*p*c1, "covariance formula")
        rows.append(dict(c0=str(c0), c1=str(c1), four_passes=str(s4)))
    require([rows[i]["four_passes"] for i in (0, 3, 4, 5)] ==
            ["1/6", "13/72", "37/216", "37/216"], "endpoints and cancellation")
    return rows


def run():
    checked = 0
    for n in range(8):
        for word in words(n):
            require(by_rails(word, 1) == by_rails(word, -1) == by_segments(word), "rail trace")
            checked += 1
    correct, changed = by_rails((0,), 1), by_rails((0,), 1, perturb_left=True)
    require((correct, changed) == (F(3, 8), F(1, 8)), "left-rail sign control")
    for d in range(1, 10):
        a = free_prefixes(d)[d]
        require(mixed_difference((0,)*(d-1)) == a*F(d*d+d+1, 4*(d+1)*(d+2)), "no middle copy")
        require(all(mixed_difference(y) > 0 for y in words(d-1)), "mixed difference sign")
    require(mixed_difference(()) == F(1, 16), "smallest mixed difference")
    p = F(1, 3)
    panels = {}
    for rate in (F(1, 5), p, F(1, 2), F(2, 3)):
        panels[str(rate)] = [check_first_difference(d, rate) for d in range(1, 7)]
    require(panels[str(p)][1]["regenerative"] == "113/648", "four-pass witness")
    a = free_prefixes(64)
    lower = (1-p)**2 * a[64] / 63
    iid = composition_survival(a, p)[64]
    require(lower > 10000*iid, "64-pass separation")
    launches = 6100
    require(launches*iid < F(1, 32000), "false-positive bound for independent copies")
    require(launches*lower > 3 and sum(F(3**k, factorial(k)) for k in range(9)) > 20,
            "miss bound for independent stationary launches")
    return dict(
        model="stationary start independent of walker; intervals measured in uses; zero-field line",
        rail_patterns_from_each_launch=checked, positive_middle_words=sum(2**i for i in range(9)),
        review_controls=dict(two_passes=str(correct), changed_left_sign=str(changed),
                             three_pass_mixed_difference=str(mixed_difference(()))),
        first_survival_differences=panels, stationary_four_pass_panel_at_one_third=four_pass_panel(),
        sixty_four_passes_at_one_third_d2=dict(independent=str(iid), regenerative_lower_bound=str(lower)),
        independent_stationary_launch_design=dict(passes=64, launches=launches,
            reject_on="any launch completes all passes", null_union_upper_bound=str(launches*iid),
            alternative_miss_upper_bound="exp(-3) < 1/20"))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path)
    directory = parser.parse_args().directory
    data = run()
    directory.mkdir(parents=True, exist_ok=True)
    with (directory/"hidden_copy_memory.json").open("x", encoding="utf-8", newline="\n") as output:
        json.dump(data, output, indent=2)
        output.write("\n")
