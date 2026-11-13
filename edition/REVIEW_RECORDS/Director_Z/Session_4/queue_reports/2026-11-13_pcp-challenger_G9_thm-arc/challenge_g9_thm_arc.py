#!/usr/bin/env python3
"""Challenger program for G9 Theorem 4.3 (label thm:arc, "Out-degree two"). Paper text only.

Statement: D a (finite) gain digraph, at most one arc per ordered pair of vertices (loops allowed),
A*A = 2.  Then (a) every vertex has two outgoing and two incoming arcs; (b) the vertices fall into
pairs {x,x'} with a common successor set {y,y'}, these sets partition V, and x,x' are the only
predecessors of y and of y'; (c) the zigzag relation chi(g(x->y) g(x'->y)^-1 g(x'->y') g(x->y')^-1) = -1;
(d) D is the arc digraph of a 2-in 2-out multidigraph D0.  Converse: the arc digraph of such D0 with
(c) at every node is norm-preserving of degree two.  "In particular |V| even, -1 in the image of chi."

Conventions: A[y][x] = gain exponent mod q of the arc x -> y, or None.  Exact arithmetic: a sum of
roots of unity is tested for zero by reduction modulo the cyclotomic polynomial.  A*A = 2 forces two
arcs out of every vertex (diagonal entries), so the enumeration is over matrices with exactly two
entries per column; this restriction is the diagonal part of the hypothesis and is not an assumption
of block structure.

PREDICATES (fixed before the first run):
 T1  the numbers of matrices with pairwise orthogonal columns agree with Table 1 of G9:
     Z2: n=2: 8, n=3: 0, n=4: 1152, n=5: 0, n=6: 691200;  Z4: n=3: 0, n=4: 73728;  Z3: n=4: 0, n=6: 0.
     The enumeration is a backtracking over columns that tests orthogonality EXACTLY and assumes
     nothing else.
 T2  every matrix found (all of them, for every case of T1 and for Z6 n=2, Z6 n=4, Z8 n=2) satisfies (a), (b), (c).
     Violations counted separately for (a) in-degree, (b) pairing, (b) partition of successor sets,
     (b) only predecessors, (c).
 T3  (d) on every matrix found for n <= 4 and on every 500th for n = 6: build D0 from the blocks and check
     that D has an arc a -> b exactly when a ends at the node at which b begins, and that every node of
     D0 has two incoming and two outgoing arcs.
 T4  converse: 300 random multidigraphs D0 with 2 arcs in and 2 arcs out at every node (1..5 nodes,
     loops and parallel arcs allowed, built from two random permutations; counts of those with a loop
     and with parallel arcs reported), gains random in Z_q (q in 2,4,6,8) subject to (c) at every node:
     the arc digraph has at most one arc per ordered pair and A*A = 2 exactly.  And 300 with (c)
     violated at one node: A*A != 2.
 T5  "|V| is even" and "-1 is a value of chi": follow from the counts (0 for odd n; 0 for Z3) - recorded;
     additionally for odd q in (3,5,7,9) and n = 2, 4: no matrix (exhaustive).
 T6  micro boundary: n=2 (D0 = one node with two loops); a D0 with a loop; a D0 with two parallel arcs;
     x = y (a vertex that is its own successor) occurs among the n=4 matrices (count).
 T7  finiteness is used: the directed binary tree with gains +1 (checked to depth 6 as a column
     orthogonality statement: distinct vertices have disjoint successor sets) has A*A = 2 on the
     columns present and every non-root vertex has ONE incoming arc; so (a) fails for countable V.
     Expected to hold as a fact about the tree; G9 assumes V finite in its Section 2.  Recorded for the
     use of the theorem in G10, where V may be countable.
Result file challenge_g9_thm_arc_results.json, never overwritten.  No random numbers except in T4 (seed 20261113).
"""
import json, os, sys, itertools, random, math
from sympy import cyclotomic_poly, Poly, symbols
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "challenge_g9_thm_arc_results.json")
if os.path.exists(OUT): sys.exit("result file exists; refusing to overwrite")
random.seed(20261113); xs = symbols('x')
_z = {}
def zero_sum(exps, q):
    """exact: is sum of zeta_q^e over e in exps zero?"""
    key = (q, tuple(sorted(e % q for e in exps)))
    if key not in _z:
        co = [0] * q
        for e in exps: co[e % q] += 1
        _z[key] = Poly(co[::-1], xs).rem(Poly(cyclotomic_poly(q, xs), xs)).is_zero
    return _z[key]
def orth(c1, c2, q):
    (r1, e1), (r2, e2) = c1, c2
    common = [(e2[r2.index(r)] - e1[r1.index(r)]) for r in r1 if r in r2]
    return True if not common else zero_sum(common, q)
def enumerate_all(n, q, visit):
    cols = [((r1, r2), (a, b)) for r1, r2 in itertools.combinations(range(n), 2) for a in range(q) for b in range(q)]
    count = 0; chosen = []
    def rec(k):
        nonlocal count
        if k == n:
            count += 1; visit(chosen, count); return
        for c in cols:
            if all(orth(p, c, q) for p in chosen):
                chosen.append(c); rec(k + 1); chosen.pop()
    rec(0); return count
viol = dict(a_in=0, b_pair=0, b_partition=0, b_onlypred=0, c=0, d=0); dchecked = 0; self_succ = 0
def make_visit(n, q):
    def visit(ch, count):
        global dchecked, self_succ
        indeg = [0] * n
        for (rows, _) in ch:
            for r in rows: indeg[r] += 1
        if any(v != 2 for v in indeg): viol["a_in"] += 1
        succ = [frozenset(rows) for rows, _ in ch]
        groups = {}
        for x, s in enumerate(succ): groups.setdefault(s, []).append(x)
        if any(len(g) != 2 for g in groups.values()): viol["b_pair"] += 1; return
        sets = list(groups)
        if sorted(v for s in sets for v in s) != list(range(n)): viol["b_partition"] += 1
        for s, (x, xp) in groups.items():
            for y in s:
                if {u for u in range(n) if y in succ[u]} != {x, xp}: viol["b_onlypred"] += 1
            y, yp = sorted(s); g = lambda u, v: ch[u][1][ch[u][0].index(v)]
            if not zero_sum([g(x, y) - g(xp, y) + g(xp, yp) - g(x, yp), 0], q): viol["c"] += 1
        if n == 4 and any(x in succ[x] for x in range(n)): self_succ += 1
        if n <= 4 or count % 500 == 0:
            dchecked += 1
            blocks = list(groups.items())   # node i: successor set s_i, predecessor pair
            begins = {v: i for i, (s, pr) in enumerate(blocks) for v in s}     # v is a successor in block i: arc v begins... see below
            ends = {v: i for i, (s, pr) in enumerate(blocks) for v in pr}       # v is a predecessor in block i
            # paper: vertex v is an arc of D0 from beta (block where v is a successor) to beta' (block where v is a predecessor)
            ok = all(((b in succ[a]) == (ends[a] == begins[b])) for a in range(n) for b in range(n))
            # node i: outgoing arcs = vertices v with begins... v goes from begins[v] to ends[v]
            for i in range(len(blocks)):
                if sum(1 for v in range(n) if begins[v] == i) != 2 or sum(1 for v in range(n) if ends[v] == i) != 2: ok = False
            if not ok: viol["d"] += 1
    return visit
res = dict(predicates={}); P = res["predicates"]
table = {(2, 2): 8, (2, 3): 0, (2, 4): 1152, (2, 5): 0, (2, 6): 691200, (4, 3): 0, (4, 4): 73728, (3, 4): 0, (3, 6): 0}
counts = {}
for (q, n), exp in table.items(): counts[f"Z{q} n={n}"] = dict(found=enumerate_all(n, q, make_visit(n, q)), table=exp)
extra = {}
for (q, n) in ((6, 2), (6, 4), (8, 2)): extra[f"Z{q} n={n}"] = enumerate_all(n, q, make_visit(n, q))
P["T1"] = dict(counts=counts, met=all(v["found"] == v["table"] for v in counts.values()))
P["T2"] = dict(violations={k: viol[k] for k in ("a_in", "b_pair", "b_partition", "b_onlypred", "c")}, extra_cases=extra,
               met=all(viol[k] == 0 for k in ("a_in", "b_pair", "b_partition", "b_onlypred", "c")))
P["T3"] = dict(matrices_checked=dchecked, violations=viol["d"], met=viol["d"] == 0 and dchecked > 0)
# T4 converse
def arc_digraph(k, q, break_one):
    p1 = list(range(k)); p2 = list(range(k)); random.shuffle(p1); random.shuffle(p2)
    arcs = [(i, p1[i]) for i in range(k)] + [(i, p2[i]) for i in range(k)]     # 2 out, 2 in at each node
    n = len(arcs); E = [[None] * n for _ in range(n)]
    for node in range(k):
        ins = [a for a in range(n) if arcs[a][1] == node]; outs = [a for a in range(n) if arcs[a][0] == node]
        (x, xp), (y, yp) = ins, outs
        g = [random.randrange(q) for _ in range(3)]                           # x->y, x'->y, x->y'
        g4 = (g[2] + g[1] - g[0] + q // 2) % q                                 # x'->y' from (c)
        if break_one and node == 0: g4 = (g4 + 1 + random.randrange(q - 1)) % q if q > 2 else (g4 + 1) % q
        E[y][x], E[y][xp], E[yp][x], E[yp][xp] = g[0], g[1], g[2], g4
    return E, any(a == b for a, b in arcs), len(set(arcs)) < len(arcs)
def AstarA2(E, q):
    n = len(E)
    for x in range(n):
        if sum(1 for y in range(n) if E[y][x] is not None) != 2: return False
        for xp in range(x + 1, n):
            com = [E[y][xp] - E[y][x] for y in range(n) if E[y][x] is not None and E[y][xp] is not None]
            if com and not zero_sum(com, q): return False
    return True
good = bad = loops = par = 0
for t in range(300):
    q = random.choice((2, 4, 6, 8)); k = random.randrange(1, 6)
    E, hl, hp = arc_digraph(k, q, False); loops += hl; par += hp; good += AstarA2(E, q)
    E, _, _ = arc_digraph(k, q, True); bad += not AstarA2(E, q)
P["T4"] = dict(with_zigzag_norm_preserving=good, of=300, D0_with_loop=loops, D0_with_parallel_arcs=par, broken_not_norm_preserving=bad, met=good == 300 and bad == 300)
odd = {f"Z{q} n={n}": enumerate_all(n, q, lambda ch, c: None) for q in (3, 5, 7, 9) for n in (2, 4)}
P["T5"] = dict(odd_q_counts=odd, met=all(v == 0 for v in odd.values()) and counts["Z2 n=3"]["found"] == 0 and counts["Z2 n=5"]["found"] == 0)
P["T6"] = dict(n2_count=counts["Z2 n=2"]["found"], n4_matrices_with_a_vertex_that_is_its_own_successor=self_succ, D0_loop_cases=loops, D0_parallel_cases=par,
               met=counts["Z2 n=2"]["found"] == 8 and loops > 0 and par > 0 and self_succ > 0)
# T7 binary tree to depth 6: vertex = bit string; successors s+'0', s+'1'
verts = [''.join(b) for L in range(0, 6) for b in itertools.product('01', repeat=L)]
disjoint = all(not ({a + '0', a + '1'} & {b + '0', b + '1'}) for a, b in itertools.combinations(verts, 2))
indeg1 = all(sum(1 for a in verts if v in (a + '0', a + '1')) == 1 for v in verts if v)
P["T7"] = dict(columns_orthogonal_with_two_entries=bool(disjoint), every_nonroot_vertex_has_one_incoming_arc=bool(indeg1), met=bool(disjoint and indeg1),
               note="A*A = 2 holds on a countable tree with all gains +1, where (a), (b), 'the image of chi contains -1' all fail; the theorem needs V finite (G9 Section 2 says so)")
res["all_met"] = all(v["met"] for v in P.values())
json.dump(res, open(OUT, "w"), indent=1, default=str)
for k, v in P.items(): print(k, v)
print("all met", res["all_met"])
