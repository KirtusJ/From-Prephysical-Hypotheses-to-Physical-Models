#!/usr/bin/env python3
"""Complete list of the coincidence pairs of Remark rem:tpprod(b) of the draft
G10_subsection_winding_products.tex (trivial twist, "the form used above").

Usage: python3 -B coincidence_pairs.py OUT.json SMAX     (OUT opened with mode 'x'; exact integers; no randomness)

DEFINITION (from the draft).  For s >= 3, n = s-1, a pair is two multisets a, b of n positive integers with
    e_j(b) = e_{s-j}(a),  1 <= j <= s-1,   equivalently  X*prod(a_i+X) == prod(1+b_j X)  mod X^s - 1.
The relation is symmetric in a and b.

BASIS OF COMPLETENESS (a written lemma, tested by P2, not assumed by P2).
  For positive integers, prod >= sum-(n-1).  j=1 and j=n give sum(b)=prod(a), prod(b)=sum(a); so with
  D(c)=prod(c)-sum(c):  D(b) = -D(a) and |D| <= n-1.  D(c) = -(n-1) exactly when c has at most one entry > 1.
  Hence in every pair at least one member lies in
     F_n = { c : at least two entries >= 2,  D(c) <= n-1 },
  which is finite (D is strictly increasing in each entry >= 2 once two entries are >= 2).
  For c in F_n the partner has product sum(c): finitely many candidates, all tried.

PREDICATES (fixed before the first run).
 P1 (control, known answers): the list for s=3 contains {(1,5),(2,3)}; the list for s=4 contains {(1,1,7),(1,3,3)}.
 P2 (the lemma against brute force that does not use it): for s=3,4 with every entry of a <= 60, s=5 with <= 30,
    s=6 with <= 14, s=7 with <= 9: for EVERY multiset a in the box, all partners b (any size of entries; found from
    prod(b)=sum(a)) are computed; the set of pairs so found equals the set of pairs of the F_n list that have a
    member in the box.
 P3 (direct verification): every listed pair satisfies X*prod(a_i+X) == prod(1+b_j X) mod X^s-1 by integer
    polynomial arithmetic, and the mirrored congruence with a and b exchanged.
 P4 (second method agrees): partners found by factorisation of sum(c) equal partners found by integer-root
    extraction of t^n + sum_j e_{n+1-j}(c) t^{n-j} (roots -a_i), for every c in F_n.
 REPORT (not a predicate; the question asked): for each s from 3 to SMAX the number of pairs, each pair, and
    D(a) (a pair with D != 0 has prod(a) != prod(b), the quantity that separated the two sides for s=3).
"""
import sys, json, itertools
from math import prod
OUT = sys.argv[1]; SMAX = int(sys.argv[2]); fout = open(OUT, 'x')
res = {"command": " ".join(sys.argv)}

def esym(c):
    p = [1]
    for x in c:
        q = [0] * (len(p) + 1)
        for i, v in enumerate(p):
            q[i] += v; q[i + 1] += v * x
        p = q
    return p            # p[j] = e_j(c)

def factorizations(P, n, lo=1):
    """nondecreasing n-tuples of positive integers with product P"""
    if n == 1:
        if P >= lo: yield (P,)
        return
    d = lo
    while d ** n <= P:
        if P % d == 0:
            for rest in factorizations(P // d, n - 1, d): yield (d,) + rest
        d += 1

def partners_fact(c):
    n = len(c); e = esym(c); out = []
    for b in factorizations(e[1], n):
        eb = esym(b)
        if all(eb[j] == e[n + 1 - j] for j in range(1, n + 1)): out.append(b)
    return sorted(out)

def partners_roots(c):
    n = len(c); e = esym(c)
    # prod (t + a_i) = sum_j e_j(a) t^(n-j),  e_j(a) = e_{n+1-j}(c)
    coef = [1] + [e[n + 1 - j] for j in range(1, n + 1)]      # descending powers
    roots = []; a = 1
    while len(coef) > 1 and a <= coef[-1]:
        # divide by (t + a) while exact
        while len(coef) > 1:
            q = [coef[0]]
            for v in coef[1:]: q.append(v - a * q[-1])
            if q[-1] != 0: break
            coef = q[:-1]; roots.append(a)
        a += 1
    return [tuple(roots)] if len(coef) == 1 else []

def F(n):
    """multisets of n positive integers, >= 2 entries >= 2, prod - sum <= n-1"""
    out = []
    def rec(y, k):
        if len(y) == k:
            c = (1,) * (n - k) + tuple(y)
            if prod(c) - sum(c) <= n - 1: out.append(c)
            return
        v = y[-1] if y else 2
        while True:
            fill = list(y) + [v] * (k - len(y))
            if prod(fill) - sum(fill) - (n - k) > n - 1: break
            rec(y + [v], k)
            v += 1
    for k in range(2, n + 1): rec([], k)
    return out

def congr(a, b, s):
    A = [0] + esym(a)[::-1]                       # X * prod(a_i + X): coefficient of X^(k+1) is e_{n-k}(a)
    red = [0] * s
    for i, v in enumerate(A): red[i % s] += v
    B = esym(b)                                   # prod(1 + b_j X): coefficient of X^j is e_j(b)
    red2 = [0] * s
    for i, v in enumerate(B): red2[i % s] += v
    return red == red2

lists = {}; p3 = True; p4 = True; sizes = {}
for s in range(3, SMAX + 1):
    n = s - 1; Fn = F(n); sizes[s] = len(Fn); pairs = set()
    for c in Fn:
        pf = partners_fact(c); pr = partners_roots(c)
        if pf != sorted(pr): p4 = False
        for b in pf: pairs.add(tuple(sorted([c, b])))
    for (a, b) in pairs:
        if not (congr(a, b, s) and congr(b, a, s)): p3 = False
    lists[s] = sorted(pairs)
res["F_sizes"] = sizes
res["REPORT"] = {str(s): [{"a": list(a), "b": list(b), "D_a": prod(a) - sum(a)} for a, b in lists[s]] for s in lists}
res["REPORT_counts"] = {str(s): len(lists[s]) for s in lists}
res["P1"] = {"holds": ((1, 5), (2, 3)) in lists[3] and ((1, 1, 7), (1, 3, 3)) in lists.get(4, [])}
boxes = {3: 60, 4: 60, 5: 30, 6: 14, 7: 9}; p2 = {}
for s, B in boxes.items():
    if s > SMAX: continue
    n = s - 1; brute = set()
    for a in itertools.combinations_with_replacement(range(1, B + 1), n):
        for b in partners_fact(a): brute.add(tuple(sorted([a, b])))
    inbox = {p for p in lists[s] if max(p[0]) <= B or max(p[1]) <= B}
    p2[str(s)] = {"box": B, "brute": len(brute), "list_in_box": len(inbox), "equal": brute == inbox,
                  "only_brute": sorted(brute - inbox), "only_list": sorted(inbox - brute)}
res["P2"] = {"cases": p2, "holds": all(v["equal"] for v in p2.values())}
res["P3"] = {"holds": p3}; res["P4"] = {"holds": p4}
json.dump(res, fout, indent=1); fout.close()
print(json.dumps({k: res[k] for k in ("REPORT_counts", "F_sizes")}), res["P1"]["holds"], res["P2"]["holds"], p3, p4)
