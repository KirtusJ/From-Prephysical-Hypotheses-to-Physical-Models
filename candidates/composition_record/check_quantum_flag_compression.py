"""Verify the finite flag code in integer ambient coordinates."""
import argparse
from collections import Counter
from fractions import Fraction
from itertools import combinations
import json
from pathlib import Path

from check_memory_errors import DIRECTIONS, ZERO, scalar


RESULT = Path(__file__).with_name("quantum_flag_compression.json")


def inner(a, b):
    return sum(x*y for x,y in zip(a,b))


def report():
    points = (ZERO, *DIRECTIONS)
    n = len(DIRECTIONS)
    # s_i = N e_i - 1; v_i = s_i / sqrt(N(N-1)).
    simplex = [[n*int(i == j)-1 for j in range(n)] for i in range(n)]
    blank = [1]*n
    assert all(inner(s,s) == n*(n-1) and inner(s,blank)==0 for s in simplex)
    assert all(inner(a,b)==-n for a,b in combinations(simplex,2))
    total_errors = Fraction()
    queries = []
    for q in DIRECTIONS:
        inside = [i for i,p in enumerate(DIRECTIONS) if scalar(p,q) == 0]
        assert len(inside)==6
        # Project each integer-coordinate state on span(blank, six vertices).
        # For an outside vertex, subtract -(sum v_i)/(N-|S|) before checking
        # orthogonality; only rational operations are needed for this projection.
        sub = [simplex[i] for i in inside]
        sum_sub = list(map(sum,zip(*sub)))
        errors = []
        for point, vec in zip(points, [blank, *simplex]):
            zero = scalar(point,q)==0
            if zero:
                projection = [Fraction(x) for x in vec]
            else:
                projection = [Fraction(-x,n-len(sub)) for x in sum_sub]
            # A separate coordinate representation of the same orthogonal projector.
            outside_mean = Fraction(sum(vec[i] for i in range(n) if i not in inside), n-len(sub))
            assert projection == [vec[i] if i in inside else outside_mean for i in range(n)]
            residual = [x-y for x,y in zip(vec,projection)]
            assert all(inner(residual,v) == 0 for v in [blank,*sub])
            prob_zero = inner(projection,projection) / inner(vec,vec)
            errors.append((1-prob_zero) if zero else prob_zero)
        assert Counter(errors)=={Fraction(0):7,Fraction(1,125):25}
        total_errors+=sum(errors)
        queries.append({"query": list(q), "errors_in_source_order": [str(e) for e in errors]})
    binary_rows = [tuple(int(scalar(p,q)!=0) for q in DIRECTIONS) for p in points]
    distances = Counter(sum(x!=y for x,y in zip(a,b)) for a,b in combinations(binary_rows,2))
    assert distances == {10:465,25:31}
    size = n*len(points)
    mean = total_errors/size
    classical = Fraction(min(distances),size)
    quantum_lower = Fraction(10,4*n*n)*(Fraction(n+1,n)-1)
    assert mean==Fraction(1,160) and classical==Fraction(5,496)
    assert classical-mean==Fraction(19,4960) and quantum_lower==Fraction(5,59582)
    # e1 and 2e1 encode identically, but a common shift by -e1 separates them.
    pair = [(1,0,0),(2,0,0)]
    add_v = lambda a: ((a[0]-1)%5,a[1],a[2])
    flags = [int(scalar(add_v(a), (1,0,0))!=0) for a in pair]
    assert flags == [0,1]
    return {"dimension":n, "source_order":[list(p) for p in points], "queries":queries,
            "state_pairs_by_query_distance":dict(sorted(distances.items())),
            "uniform_mean":str(mean), "maximum_conditional_error":"1/125",
            "optimal_classical_uniform_mean":str(classical),
            "uniform_mean_gap":str(classical-mean), "quantum_uniform_mean_lower":str(quantum_lower),
            "same_code_after_one_offset":{"sources":pair, "offset":[-1,0,0],"query":[1,0,0],"flags":flags}}


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--write",action="store_true",help="replace the stored exact report")
    args=p.parse_args()
    out = json.dumps(report(), indent=2) + "\n"
    if args.write:
        RESULT.write_text(out, encoding="utf-8", newline="\n")
    else:
        assert RESULT.read_text(encoding="utf-8") == out
        print("Verified simplex projections, all 992 late flags, and the additive-write control.")


if __name__=="__main__":
    main()
