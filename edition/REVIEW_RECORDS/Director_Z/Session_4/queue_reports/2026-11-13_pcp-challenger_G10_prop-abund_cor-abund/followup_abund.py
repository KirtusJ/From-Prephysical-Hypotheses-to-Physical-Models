#!/usr/bin/env python3
"""Follow-up to three FAILED predicates of challenge_prop_abund_cor_abund.py (kept, not edited).

K3 failed on 19 carriers, all with m = 4 common successors: dimensions 2 (q0=4), 4 (q0=8), 3 (q0=12) against 1, 2, 2.
   Suspected cause: box too small (the paper reports the same for its own runs).
N1 failed on 16 carriers.  Suspected cause in my predicate: D itself was not strongly connected (several nodes of
   the random base digraph not joined), a case the paper's remark does not cover.
X1 failed.  Cause read off a printout made after the run: I required exactly two gains at every vertex from length 3;
   the paper says "only two of the four gains occur", and the maximum over vertices is 1,1,1,2,2,... .

PREDICATES (fixed before this run):
 K3b for q0 in (4, 8, 12) and EVERY multiset of 4 exponents (e1<=e2<=e3<=e4, containing 0) with zeta^e summing to zero
     (exact; count reported): the solution space of (V) with a in box A and b in box B has dimension phi(q0)/2, where
     A = B = -4..4 squared for q0 = 4 and A = {-2..2}^4, B = {-1..1}^4 for q0 = 8, 12.  Rank by eigenvalues of M^T M:
     null dimension = number of eigenvalues below 1e-9 * largest; the eigenvalue gap is recorded (matrix entries are
     small integers, exact in floating point; M^T M entries are integers below 2^53).
     If this fails for some multiset, K3c: same with f restricted further is NOT attempted; the failure is reported.
 N1b on 261 carriers rebuilt with the same generator and seed: among those with A*A = d AND D strongly connected,
     [D-hat strongly connected] <=> [gains of closed walks at vertex 0, lengths <= 2|V|+6, generate C].  Count each side.
 X1b on the paper's example, from each of the four starting vertices, lengths 0..60: at most two gains at any vertex
     at any length; the two gains at a vertex form a coset of {0, 2}; from length 5 on exactly two at every vertex reached.
Result file followup_abund_results.json, never overwritten.
"""
import json, os, sys, itertools, random, math
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
for p in (os.path.join(HERE, "..", "..", "lib"), "/home/user/From-Prephysical-Hypotheses-to-Physical-Models/REVIEW_QUEUE/lib"):
    if os.path.exists(os.path.join(p, "pcplib.py")): sys.path.insert(0, p); break
import pcplib as L
OUT = os.path.join(HERE, "followup_abund_results.json")
if os.path.exists(OUT): sys.exit("result file exists; refusing to overwrite")
res = {}
k3 = []
for q0 in (4, 8, 12):
    R = L.Ring(q0)
    A = [tuple(t) for t in itertools.product(range(-4, 5) if R.n == 2 else range(-2, 3), repeat=R.n)]
    B = A if R.n == 2 else [tuple(t) for t in itertools.product(range(-1, 2), repeat=R.n)]
    Ncache = {}
    def N(a):
        if a not in Ncache: Ncache[a] = R.N(a)
        return Ncache[a]
    for es in itertools.combinations_with_replacement(range(q0), 4):
        if es[0] != 0 or not L.zero_sum(list(es), q0): continue
        keys = {}; rows = set()
        shifted = {e: {b: R.mulz(b, e) for b in B} for e in set(es)}
        for a in A:
            for b in B:
                row = {}
                for e in es:
                    k = N(R.add(a, shifted[e][b])); j = keys.setdefault(k, len(keys)); row[j] = row.get(j, 0) + 1
                for t in (a, b):
                    j = keys.setdefault(N(t), len(keys)); row[j] = row.get(j, 0) - 4
                rows.add(tuple(sorted((j, v) for j, v in row.items() if v)))
        rows.discard(()); n = len(keys); G = np.zeros((n, n))
        for row in rows:
            js = [j for j, _ in row]; vs = np.array([v for _, v in row], float); G[np.ix_(js, js)] += np.outer(vs, vs)
        z = keys[N(R.zero())]; G[z, z] += 1
        ev = np.linalg.eigvalsh(G); dim = int((ev < 1e-9 * ev[-1]).sum()); exp = len(R.J)
        kept = float(ev[dim]) if dim < n else None
        k3.append(dict(q0=q0, exps=list(es), unknowns=n, distinct_equations=len(rows), dim=dim, expected=exp,
                       largest_null_eigenvalue=float(ev[dim - 1]) if dim else None, smallest_kept=kept, largest=float(ev[-1])))
res["K3b"] = dict(cases=k3, met=all(c["dim"] == c["expected"] for c in k3) and len(k3) > 0)
# N1b: regenerate
src = open(os.path.join(HERE, "challenge_prop_abund_cor_abund.py")).read()
ns = {"L": L, "itertools": itertools}
exec(src[src.index("def fam():"):src.index("res = dict(seed")], ns)
rng = random.Random(20261113); both = neither = mism = dsc = 0; total = 0
for (name, mod, k, M) in ns["fam"]():
    for rep in range(9):
        nodes = 1 + rep % 3; E = L.block_carrier(nodes, M, mod, rng, switch=(rep % 3 != 2)); total += 1
        if L.norm_preserving(E, mod, k) is None: continue
        if not L.strongly_connected([list(s) for s in L.succ(E)]): continue
        dsc += 1; idx, S = L.lift(E, mod); sc = L.strongly_connected(S)
        full = len(ns["closed_gain_subgroup"](E, mod, 2 * len(E) + 6)) == len(L.group(mod))
        both += sc and full; neither += (not sc) and (not full); mism += sc != full
res["N1b"] = dict(built=total, norm_preserving_and_D_strongly_connected=dsc, both=both, neither=neither, mismatches=mism, met=mism == 0 and both > 0 and neither > 0)
ex = [(0, 2, 0), (0, 3, 1), (1, 0, 1), (1, 1, 3), (2, 0, 0), (2, 1, 0), (3, 2, 0), (3, 3, 3)]
E = [[None] * 4 for _ in range(4)]
for (a, b, e) in ex: E[b][a] = (e,)
idx, S = L.lift(E, (4,)); inv = {i: yg for yg, i in idx.items()}; atmost = coset = exact = True
for st in range(4):
    for Lw, cur in enumerate(L.walk_counts(S, idx[(st, (0,))], 60)):
        per = {}
        for v in cur: per.setdefault(inv[v][0], set()).add(inv[v][1][0])
        for s in per.values():
            atmost &= len(s) <= 2; coset &= len({g % 2 for g in s}) == 1
            if Lw >= 5: exact &= len(s) == 2
res["X1b"] = dict(at_most_two=bool(atmost), within_a_coset_of_the_subgroup_of_order_two=bool(coset), exactly_two_from_length_5=bool(exact), met=bool(atmost and coset and exact))
res["all_met"] = all(v["met"] for v in res.values())
json.dump(res, open(OUT, "w"), indent=1)
for c in k3: print(c["q0"], c["exps"], c["unknowns"], c["distinct_equations"], c["dim"], c["expected"], c["largest_null_eigenvalue"], c["smallest_kept"])
print(res["N1b"], res["X1b"], res["all_met"])
