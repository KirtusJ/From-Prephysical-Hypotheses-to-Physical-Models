"""Exact coherent prefix reference, dyadic addresses and finite bit-source controls."""

import argparse
from collections import Counter
from fractions import Fraction
from functools import reduce
from math import gcd
import json
from pathlib import Path


def require(condition, reason):
    if not condition:
        raise ValueError(reason)


# Each cell stores (a,b) for the integer numerator a+b*sqrt(2) over sqrt(2)^t.
# Multiplication by 1/sqrt(2) gives b+(a/2)*sqrt(2). Inputs seen here have even a
# whenever a Hadamard is applied, so these exact operations need no fractions.
def scale_pair(a, b):
    require(a % 2 == 0, "Hadamard would require an enlarged denominator")
    return b, a // 2


def addressed_h(column, i, j):
    a, b = column[i]
    c, d = column[j]
    column[i] = scale_pair(a+c, b+d)
    column[j] = scale_pair(a-c, b-d)


def norm_pair(coefficients):
    a, b = coefficients
    require(a*b == 0, "mixed radical in leaf norm")
    return a*a + 2*b*b


def support_content(row):
    g = reduce(gcd, row, 0)
    while g and not g % 2:
        g //= 2
    return g


def prefix(t, threshold):
    """Compare the first t independent binary digits to the t-bit threshold."""
    total = 1 << t
    require(0 < threshold < total and t >= 1, "use a deterministic endpoint for 0 or 1")
    width = 1+t+t//2
    state = [(0,0)] * width
    state[0] = (1 << (t//2), 0) if t % 2 == 0 else (0, 1 << (t//2))
    original = state.copy()
    marked = [False] * width
    labels = [""] * width
    h_gates = []
    # At stage k the slot k-1 is the only unresolved prefix, k is fresh.
    # A scheduled physical H parks the first-difference leaf to the left and
    # passes the equal-prefix rail to the right. The blank second input makes
    # the two outgoing signs equal in this ordered convention.
    for depth in range(1, t+1):
        parked, active = depth-1, depth
        require(state[active] == (0,0), "fresh active slot")
        addressed_h(state, parked, active)
        h_gates.append((parked, active))
        bit = (threshold >> (t-depth)) & 1
        marked[parked] = bool(bit)
        labels[parked] = f"different at {depth}"
        require(norm_pair(state[parked]) == total >> depth, "offshoot weight")
    labels[t] = "equal"
    require(norm_pair(state[t]) == 1 and not marked[t], "strict equality is dark")
    # Split only the early terminal numerators with an odd remaining exponent;
    # the final different leaf and the equal leaf already have integer numerator 1.
    spare = t+1
    for depth in range(1, t+1):
        if (t-depth) % 2:
            leaf = depth-1
            require(state[leaf][0] == 0 and state[spare] == (0,0), "parity split")
            addressed_h(state, leaf, spare)
            h_gates.append((leaf, spare))
            marked[spare] = marked[leaf]
            labels[spare] = labels[leaf] + " twin"
            spare += 1
    require(spare == width and all(b == 0 and a > 0 for a,b in state), "integer full carrier")
    numerators = [a for a,_ in state]
    bins = [[a for a, f in zip(numerators, marked) if f == side] for side in (False,True)]
    require([sum(a*a for a in row) for row in bins] == [total-threshold,threshold], "complete bin norms")
    require(all(support_content(row) == 1 for row in bins), "odd-content convention")
    for i,j in reversed(h_gates):
        addressed_h(state,i,j)
    require(state == original, "all signed gates reverse exactly on full carrier")
    return dict(t=t, threshold=threshold, width=width, controlled_H_count=len(h_gates),
                parked_labels=labels, marked=marked, positive_integer_numerators=numerators)


def decision(bits, threshold):
    """Classical circuit reads up to the first difference, or all bits for equality."""
    for k, (a,b) in enumerate(zip(bits, threshold), start=1):
        if a != b:
            return a < b, k
    return False, len(bits)


def run_tape(t, threshold, tape):
    target = f"{threshold:0{t}b}"
    chosen = Fraction(0)
    inspected = Fraction(0)
    for bits, probability in tape:
        require(len(bits) == t and set(bits) <= {"0","1"}, "tape address")
        hit, cost = decision(bits,target)
        chosen += probability * hit
        inspected += probability * cost
    return {"hit":str(chosen), "mean_inspections":str(inspected)}


def expected_cost(t):
    return Fraction(2) - Fraction(1, 1 << (t-1))


def sweep():
    rows = []
    total_tested = 0
    for t in range(1,12):
        n = 1 << t
        by_depth = Counter()
        for p in range(1,n):
            result = prefix(t,p)
            r = t - ((p & -p).bit_length()-1)
            m = p >> (t-r)
            require(m % 2 and (m << t) == (p << r), "reduced strictly dyadic threshold")
            by_depth[r] += 1
            if r < t:
                require(expected_cost(r) < expected_cost(t), "fixed horizon can waste bits")
            require(result["width"] == 1+t+t//2, "exact width")
        require(all(by_depth[r] == 1 << (r-1) for r in range(1,t+1)), "threshold counts")
        total_tested += n-1
        rows.append(dict(t=t, interior_thresholds=n-1, cell_count=1+t+t//2,
                         odd_remaining_exponent_splits=t//2,
                         with_lower_reduced_denominator=n//2-1,
                         literal_prefix_mean_inspections=str(expected_cost(t))))
    t,p = 4,9
    threshold = f"{p:0{t}b}"
    uniform = [(f"{i:0{t}b}", Fraction(1,1 << t)) for i in range(1 << t)]
    hidden = [("0"*t,Fraction(1,2)),("1"*t,Fraction(1,2))]
    require(all(sum(w for bits,w in hidden if bits[k]=="1") == Fraction(1,2) for k in range(t)),
            "correlated tape has every one-bit marginal fair")
    ordinary = run_tape(t,p,uniform)
    correlated = run_tape(t,p,hidden)
    require(ordinary == {"hit":"9/16","mean_inspections":"15/8"}, "ordinary tape")
    require(correlated == {"hit":"1/2","mean_inspections":"3/2"}, "correlated tape")
    # For a reduced threshold, exactly one prefix remains unresolved at each
    # depth k<r. A fair decision tree stopping everywhere by k could only
    # make a probability that is an integer multiple of 2^-k.
    for r in range(1,12):
        for m in range(1,1<<r,2):
            for k in range(r):
                require((m << k) % (1 << r) != 0, "some prefix must remain unresolved")
    reduced = run_tape(2,1,[(f"{i:02b}",Fraction(1,4)) for i in range(4)])
    literal = run_tape(4,4,uniform)
    require(reduced == {"hit":"1/4","mean_inspections":"3/2"} and
            literal == {"hit":"1/4","mean_inspections":"15/8"}, "nonreduced boundary")
    return dict(convention="b=1 means strictly less than P; equality is unmarked; original labels kept.",
                tested_thresholds=total_tested,sweep=rows,four_tick_9_of_16=prefix(t,p),
                binary_threshold=threshold,conditionally_fair_tape=ordinary,
                fair_marginals_same_hidden_bit=correlated,
                one_quarter_tapes=dict(literal_4_bits=literal,reduced_2_bits=reduced),
                endpoints=dict(zero_and_one="sharp deterministic outputs, zero inspections"))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path)
    path = parser.parse_args().output
    path.write_bytes((json.dumps(sweep(),indent=2)+"\n").encode("utf-8"))


if __name__ == "__main__":
    main()
