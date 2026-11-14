"""Exact finite inputs for the randomized two-setting terminal record."""
import argparse
from fractions import Fraction
from itertools import accumulate, product
import json
from pathlib import Path

from check_reciprocal_ring_score import cover_walk, seam_words


def cells_for_setting(rows, addressed):
    bins = {}
    for j, (r, l, words) in enumerate(rows):
        x = j % 6
        key = (x, j // 6 if x in addressed else None)
        cell = bins.setdefault(key, {"modes": [], "words": 0})
        cell["modes"].extend(z*z for z in (r, l) if z)
        cell["words"] += words
    return {key: cell for key, cell in bins.items() if cell["modes"] or cell["words"]}


def partitions(values):
    """Distinct pooled mass lists over every set partition of this short bin."""
    groups = {()}
    for value in values:
        following = set()
        for group in groups:
            following.add(tuple(sorted((*group, value))))
            for i in range(len(group)):
                pooled = list(group)
                pooled[i] += value
                following.add(tuple(sorted(pooled)))
        groups = following
    return groups


def possible_cells(bins):
    options = [partitions(cell["modes"]) for cell in bins.values()]
    return {tuple(sorted((m for group in combination for m in group), reverse=True))
            for combination in product(*options)}


def majorization_gaps(large, small):
    n = max(len(large), len(small))
    big = sorted(large, reverse=True) + [0]*(n-len(large))
    little = sorted(small, reverse=True) + [0]*(n-len(small))
    return [x-y for x, y in zip(accumulate(big), accumulate(little))]


def analyze():
    rows = cover_walk(6,11)
    assert rows == seam_words(6,11)
    A = cells_for_setting(rows,{1,3})
    B = cells_for_setting(rows,{3,5})
    for panel in (A,B):
        assert sum(sum(cell["modes"]) for cell in panel.values()) == 2048
        assert sum(cell["words"] for cell in panel.values()) == 2048
    pure = lambda panel: {k:(v["modes"][0],v["words"]) for k,v in panel.items()
                          if len(v["modes"]) == 1}
    assert pure(A) == {(1,1):(576,220),(3,0):(225,341)}
    assert pure(B) == {(3,0):(225,341),(5,1):(81,463)}
    a,b,c = 81,225,576
    assert b > 2*a and c > 2*b
    coarse = sorted((sum(v["modes"]) for v in A.values()), reverse=True)
    fine = sorted((m for v in B.values() for m in v["modes"]), reverse=True)
    endpoint = majorization_gaps([2*m for m in fine], 2*coarse)
    assert endpoint == [591,982,1054,928,883,712,505,298,153,0]
    opts_A, opts_B = possible_cells(A), possible_cells(B)
    for choice_A, choice_B in product(opts_A,opts_B):
        gaps = majorization_gaps([2*m for m in choice_B], 2*list(choice_A))
        assert min(gaps) >= 0 and gaps[-1] == 0
        assert len(choice_B) <= 2*len(choice_A)  # zero-power limit
        assert max(choice_A) > c and max(choice_B) > b  # infinity
    t1 = Fraction(220,c)-Fraction(341,b)
    t2 = Fraction(463,a)-Fraction(341,b)
    assert c*c*a > b**3 and t2 > 0 and t1+t2/2 == Fraction(31319,32400)
    def describe(panel):
        return [{"well":x,"sheet":s,**v} for (x,s),v in panel.items()]
    return {"A":describe(A),"B":describe(B),"total_words_each":2048,
            "pooled_A":coarse,"split_B":fine,"twice_mass_prefix_gaps":endpoint,
            "partition_vectors_A_B":[len(opts_A),len(opts_B)],
            "all_partition_pairs_checked":len(opts_A)*len(opts_B),
            "count_lower_after_dividing_by_u_per_2048":str(t1+t2/2),
            "ordinary_low_bin_in_B":str(Fraction(a,2048))}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    with args.output.open("x", encoding="utf8", newline="\n") as out:
        json.dump(analyze(), out, indent=2, allow_nan=False)
        out.write("\n")
