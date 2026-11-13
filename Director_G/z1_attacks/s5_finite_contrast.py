"""Attack S5 of candidate Z1 v0.1 on its signed ring; standard library.

Run: python -B s5_finite_contrast.py OUTPUT_DIRECTORY
The result is created exclusively. A failed declared predicate remains in the JSON.
"""
import argparse
import json
from collections import Counter, defaultdict
from fractions import Fraction as F
from itertools import product
from pathlib import Path


RINGS = (3, 4, 5, 6, 8, 16)
COEFFICIENTS = (F(0), F(1, 7), F(1, 2), F(1))
PREDICATES = {
    "S1": "Each tested carrier has two distinct successors, and its signed lift is strongly connected.",
    "characters": "The signed columns have Gram matrix 2I; the unsigned columns fail this test.",
    "S2_S3_S4_samples": "On all 2^8 subsets at tick 3 the proposed mixture weights are nonnegative, give unit singleton weight, add over distinct terminal labels, and double on continuation. The empty event has zero weight.",
    "first_contrast": "All full-record endpoint laws agree at ticks 0,1,2. At tick 3 the bright and dark signed path pairs are precisely LRR/RLR and LRL/RLL. Both count probabilities are 1/4.",
    "identified_a": "For each tested mixture p1(bright)-p3(bright)=p3(dark)=a/4. The nondecrease holds exactly at a=0, and both raw sufficient statistics recover a.",
    "in_range": "On each tested ring, at least one in-range count/character mixture with positive a obeys the finite S1-S4 checks while failing the bright test. The population endpoints a=0,1 attain the predicted extremes.",
    "unsharp_controls": "A slope tolerance of 1/16 admits a=1/4: the exact bound a<=4 delta is attained. If positivity is discarded, a=-1/2 passes the one-sided bright test but gives a negative dark probability.",
    "monitored_control": "With a fresh full path record at every tick, both bright and dark masses are 1/4 at tick three, even when the native gates have the same signs.",
    "coarse_read": "A position-only meter gives P3(x=1)-P1(x=1)=1/8-a/4, plus 1/8 on N=4 where the ballistic -3 also wraps to 1. Nondecrease allows a=1/2 on every ring.",
    "coarse_recheck": "Registered after the first run: on N=4 RRL and LLL both have sign + and reach (1,L); the coarse drift is (1-a)/2 there. It is 1/8-a/4 on the other tested rings. Compare all contributing words.",
    "late_register_control": "An actual pointer first copied after tick three and on each later tick retains the whole early unmarked table, but under squared-coordinate readout has return <=1/2 at all positive times. Check the first 16 late steps against the analytic bound.",
}


def arcs(n, state):
    x, incoming = state
    return [(((x+1) % n, "R"), 1), (((x-1) % n, "L"), -1 if incoming == "L" else 1)]


def graph_checks(n):
    vertices = list(product(range(n), "RL"))
    lift = {(state, g): [(new, g*h) for new, h in arcs(n, state)]
            for state, g in product(vertices, (1, -1))}
    reverse = defaultdict(list)
    for start, targets in lift.items():
        for end in targets:
            reverse[end].append(start)
    source = ((0, "R"), 1)
    def reach(graph):
        seen = {source}
        stack = [source]
        while stack:
            for end in graph[stack.pop()]:
                if end not in seen:
                    stack.append(end)
                    seen.add(end)
        return len(seen)
    signed_ok = True
    unsigned_ok = True
    columns = [dict(arcs(n, state)) for state in vertices]
    for i, col in enumerate(columns):
        for j, other in enumerate(columns):
            if sum(h*other.get(end, 0) for end, h in col.items()) != 2*(i == j):
                signed_ok = False
            if len(col.keys() & other.keys()) != 2*(i == j):
                unsigned_ok = False
    forward, backward = reach(lift), reach(reverse)
    return dict(forward=forward, backward=backward, lift_size=len(lift),
                distinct_two=all(len(col) == 2 for col in columns),
                signed_gram=signed_ok, unsigned_gram=unsigned_ok)


def extend(n, pool):
    return [(end, sign*h, word+end[1]) for start, sign, word in pool for end, h in arcs(n, start)]


def counts(pool):
    amplitude, multiplicity = Counter(), Counter()
    for end, sign, word in pool:
        amplitude[end] += sign
        multiplicity[end] += 1
    return multiplicity, amplitude


def weight(a, multiplicity, amplitude):
    return a*multiplicity + (1-a)*amplitude**2


def event_audit(n, pool):
    tested, good = 0, True
    for mask in range(1 << len(pool)):
        selected = [walk for i, walk in enumerate(pool) if mask & (1 << i)]
        before = counts(selected)
        after = counts(extend(n, selected))
        for a in COEFFICIENTS:
            pieces = [weight(a, c, before[1][end]) for end, c in before[0].items()]
            direct = a*len(selected)+(1-a)*sum(z*z for z in before[1].values())
            continued = a*sum(after[0].values())+(1-a)*sum(z*z for z in after[1].values())
            good &= (all(p >= 0 for p in pieces) and sum(pieces) == direct and continued == 2*direct)
            if len(selected) <= 1:
                good &= direct == len(selected)
        tested += 1
    return tested, good


def marked_after_three(n, early):
    # A fresh orthogonal pointer records the complete endpoint at every t>=3,
    # immediately after the current native step. Orthogonal retained histories
    # make every subsequent single-arc branch probability exactly 1/2.
    mass = {end: F(z*z, 8) for end, z in counts(early)[1].items()}
    returns = [mass.get((0, "R"), F(0))]
    for _ in range(16):
        next_mass = Counter()
        for start, prob in mass.items():
            for end, unused in arcs(n, start):
                next_mass[end] += prob/2
        mass = next_mass
        returns.append(mass.get((0, "R"), F(0)))
        assert sum(mass.values()) == 1
    return returns


def census(n):
    pools = [[((0, "R"), 1, "")]]
    for _ in range(3):
        pools.append(extend(n, pools[-1]))
    data = [counts(pool) for pool in pools]
    b, d = (1, "R"), (n-1, "L")
    signed_paths = {name: {word: sign for end, sign, word in pools[3] if end == port}
                    for name, port in (("bright", b), ("dark", d))}
    graph = graph_checks(n)
    tested, event_ok = event_audit(n, pools[3])
    early_equal = all(all(c == s[end]**2 for end, c in m.items()) for m, s in data[:3])
    def prob(a, t, end):
        m, s = data[t]
        return weight(a, m[end], s[end])/2**t
    def position(a, t):
        return sum(prob(a, t, (1, rail)) for rail in "RL")
    checks, samples = {}, []
    for a in COEFFICIENTS:
        p1, p3, dark = prob(a, 1, b), prob(a, 3, b), prob(a, 3, d)
        samples.append(dict(a=a, p1_b=p1, p3_b=p3, p3_d=dark,
                            position_change=position(a, 3)-position(a, 1),
                            bright_nondecrease=p3 >= p1, recovered_a=4*(p1-p3)))
    m3, s3 = data[3]
    checks["S1"] = graph["distinct_two"] and graph["forward"] == graph["backward"] == 4*n
    checks["characters"] = graph["signed_gram"] and not graph["unsigned_gram"]
    checks["S2_S3_S4_samples"] = tested == 256 and event_ok
    checks["first_contrast"] = (early_equal and signed_paths["bright"] == {"RLR": 1, "LRR": 1}
                                and signed_paths["dark"] == {"RLL": -1, "LRL": 1}
                                and m3[b] == m3[d] == 2)
    checks["identified_a"] = all(r["p1_b"]-r["p3_b"] == r["p3_d"] == r["a"]/4
                                 and r["bright_nondecrease"] == (r["a"] == 0) for r in samples)
    checks["in_range"] = (event_ok and samples[0]["p3_b"] == F(1, 2) and samples[-1]["p3_b"] == F(1, 4)
                          and any(r["a"] > 0 and not r["bright_nondecrease"] for r in samples))
    delta = F(1, 16)
    negative = -F(1, 2)
    checks["unsharp_controls"] = (prob(4*delta, 1, b)-prob(4*delta, 3, b) == delta
                                  and prob(negative, 3, b) > prob(negative, 1, b)
                                  and prob(negative, 3, d) < 0)
    checks["monitored_control"] = F(m3[b], 8) == F(m3[d], 8) == F(1, 4)
    wrap = F(int(n == 4), 8)
    checks["coarse_read"] = all(r["position_change"] == F(1, 8)+wrap-r["a"]/4 for r in samples)
    extra = {word: sign for end, sign, word in pools[3] if end == (1, "L")}
    expect_extra = {"RRL": 1, "LLL": 1} if n == 4 else {"RRL": 1}
    checks["coarse_recheck"] = (extra == expect_extra and
                                all(row["position_change"] == ((1-row["a"])/2 if n == 4
                                    else F(1, 8)-row["a"]/4) for row in samples))
    late = marked_after_three(n, pools[3])
    checks["late_register_control"] = (all(prob(0, t, (0, "R")) <= F(1, 2) for t in (1, 2, 3))
                                       and max(late) <= F(1, 2))
    return dict(ring=n, graph=graph, checked_t3_subsets=tested, paths=signed_paths,
                additional_paths_at_position_1_finishing_L=extra,
                mixture_samples=samples, late_marked_return_at_t3_through_19=late,
                controls=dict(delta=delta, tolerance_saturating_a=4*delta,
                              negative_a=negative, negative_dark=prob(negative, 3, d),
                              path_marked_bright=F(m3[b], 8), path_marked_dark=F(m3[d], 8)),
                predicates=checks)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path)
    folder = parser.parse_args().output
    folder.mkdir(parents=True, exist_ok=True)
    target = folder/"s5_finite_contrast.json"
    if target.exists():
        parser.exit(2, f"refusing to overwrite {target}\n")
    rows = [census(n) for n in RINGS]
    failures = [[r["ring"], name] for r in rows for name in PREDICATES if not r["predicates"].get(name)]
    expected_adverse = [[4, "coarse_read"]]
    result = dict(candidate="Director Z, Candidate model Z1 v0.1, Z1-R. Starting vertex (0,R).",
                  predetermined=PREDICATES, tested_coefficients=COEFFICIENTS, rows=rows,
                  failed_predicates=failures, checks=len(rows)*len(PREDICATES),
                  expected_retained_first_run_failure=expected_adverse,
                  failure_set_reproduced=failures == expected_adverse)
    with target.open("xb") as stream:
        stream.write((json.dumps(result, default=str, indent=2)+"\n").encode("utf-8"))
    print(f"{result['checks']-len(failures)}/{result['checks']} ring predicates passed; failures {failures}.")
    raise SystemExit(failures != expected_adverse)
