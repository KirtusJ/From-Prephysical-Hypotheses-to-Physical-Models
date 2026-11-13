#!/usr/bin/env python3
"""Challenger program for G10 Lemma 3.1 (lem:cyl) and Proposition 4.1 (prop:add). Paper text only.

Conventions.  A digraph is a dict vertex -> list of (successor, gain exponent mod q); at most one arc
per ordered pair.  A walk from x is a tuple of vertices starting with x.  An event is a frozenset of
walks of one length from one vertex.  Histories are replaced by walks of a horizon length H: if every
vertex has an outgoing arc, cyl(S) = cyl(S') iff the sets of length-H continuations agree (H >= both
lengths), because every walk of length H is the beginning of a history.  When some vertex has no
outgoing arc this replacement is NOT valid, and cyl is computed instead as the set of length-H
continuations that end at a vertex from which arbitrarily long walks exist ("live" vertices).

PREDICATES (fixed before the first run):
 L0  hypothesis per digraph: every vertex has an outgoing arc.  Count qualifying among 60 random digraphs.
 L1  lem:cyl(a) first part on qualifying digraphs: cyl(Ext S) = cyl(S) for 40 random events each.
 L2  lem:cyl(a) second part, both directions, on qualifying digraphs, events S (length j) and S'
     (length j' >= j) from the same vertex, 200 pairs per digraph, half of them built as
     Ext^(j'-j) S or a one-walk perturbation of it:  [cyl S = cyl S']  ==  [S' = Ext^(j'-j) S].
     Report how many pairs had cyl S = cyl S' (so that the equality case is really sampled).
 L3  the family of cylinder sets from one vertex is closed under complement (within the histories from
     that vertex) and union: for random S (length j), S' (length j'), the union and the complement are
     cyl of an explicit event of length max(j, j').
 L4  lem:cyl(b),(c) by construction: with nu_j(S) = c^(-j) |S|-weighted count w(S) = sum over walks of
     prod of arc weights p(e) where sum of p over arcs leaving a vertex = 1 (consistent, c=1), the value
     depends only on cyl(S): equal cylinders give equal values (to 1e-12, rounding of <= 3^6 products);
     and with nu_j(S) = |S| (not consistent when some out-degree > 1) two events with equal cylinders
     and different values exist on every qualifying digraph having a vertex of out-degree >= 2
     reachable from the start.
 L5  the hypothesis is needed and is not in the lemma's statement: on digraphs with a vertex without
     outgoing arcs (those failing L0), search for events S != S' of one length, or S' != Ext S, with
     equal cylinders.  Expected: found.  met = found on at least one such digraph (count reported).
 L6  events from two different vertices: cyl(S) = cyl(S') with both non-empty never happens. (wording check)
 A0  hypothesis per digraph for prop:add: no loops and every vertex has exactly d >= 1 outgoing arcs.
     Families: directed cycles (d=1), complete digraphs K_n without loops (n=3,4; d=n-1), circulants,
     random d-out-regular loopless digraphs on 4..6 vertices, gains random in Z_q, q in (1,2,3).
 A1  on each qualifying digraph, start vertex 0, walks up to length Lw = 5: the equations (4.2)
        sum_{e} F(we) = c F(w)
     in the unknowns c, a, f_g (g = gain of a closed walk at the start seen up to length Lw+1),
     with a = 1: every solution with c > 0 has c = d and f_g = 1 for all g.  (sympy.solve, exact.)
     Report how many digraphs are of the proof's first kind (some walk ends at y != x with no arc to x)
     and of the second kind.
 A2  same with a = 0: every solution with c > 0 has all f_g = 0.
 A3  boundary d = 1 (directed cycle, with non-trivial gains): A1 and A2 hold with c = 1.
 A4  the no-loop hypothesis is used: on the two-vertex digraph with a loop at each vertex and both
     arcs between them (d = 2), gains trivial, solve the same equations with a = 1.
     Recorded: the solutions.  Expected by the challenger: a solution other than (c=2, f=1) may exist;
     met = the program ran and recorded them (no claim).
Seed 20261113.  Result file challenge_lem_cyl_prop_add_results.json, never overwritten.
"""
import json, os, sys, random, itertools
import sympy as sp
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "challenge_lem_cyl_prop_add_results.json")
if os.path.exists(OUT): sys.exit("result file exists; refusing to overwrite")
random.seed(20261113)

def rand_digraph(n, maxout, allow_dead):
    D = {}
    for v in range(n):
        k = random.randrange(0 if allow_dead else 1, maxout + 1)
        D[v] = [(u, 0) for u in random.sample(range(n), min(k, n))]
    return D
def walks_from(D, x, L):
    ws = [(x,)]
    for _ in range(L): ws = [w + (u,) for w in ws for (u, _) in D[w[-1]]]
    return ws
def ext(D, S, k=1):
    S = set(S)
    for _ in range(k): S = {w + (u,) for w in S for (u, _) in D[w[-1]]}
    return frozenset(S)
def live(D):
    L = set(D)
    while True:
        L2 = {v for v in L if any(u in L for (u, _) in D[v])}
        if L2 == L: return L
        L = L2
H = 6
def cyl(D, S, Lv):
    return frozenset(w for w in ext(D, S, H - (len(next(iter(S))) - 1)) if w[-1] in Lv) if S else frozenset()
def rand_event(D, x, j):
    ws = walks_from(D, x, j)
    if not ws: return frozenset()
    return frozenset(random.sample(ws, random.randrange(0, len(ws) + 1)))

res = dict(seed=20261113, predicates={}); P = res["predicates"]
digs = [rand_digraph(random.randrange(2, 6), 3, allow_dead=(i % 3 == 0)) for i in range(60)]
qual = [D for D in digs if all(D[v] for v in D)]; dead = [D for D in digs if not all(D[v] for v in D)]
P["L0"] = dict(built=len(digs), qualifying=len(qual), met=len(qual) > 0)
f1 = f2 = n2 = eq2 = f3 = f4a = 0; f4b_checked = f4b_found = 0; f6 = 0
for D in qual:
    Lv = live(D); assert Lv == set(D)
    p = {v: [random.random() for _ in D[v]] for v in D}; p = {v: [t / sum(p[v]) for t in p[v]] for v in D}
    def wgt(S):
        tot = 0.0
        for w in S:
            pr = 1.0
            for i in range(len(w) - 1): pr *= p[w[i]][[u for (u, _) in D[w[i]]].index(w[i + 1])]
            tot += pr
        return tot
    for _ in range(40):
        x = random.choice(list(D)); j = random.randrange(0, 4); S = rand_event(D, x, j)
        if S and cyl(D, ext(D, S), Lv) != cyl(D, S, Lv): f1 += 1
    for t in range(200):
        x = random.choice(list(D)); j = random.randrange(0, 4); jp = random.randrange(j, 5); S = rand_event(D, x, j)
        if not S: continue
        target = ext(D, S, jp - j)
        if t % 2 == 0:
            Sp = set(target)
            if t % 4 == 0 and Sp:
                allw = walks_from(D, x, jp); w = random.choice(allw)
                Sp ^= {w}
            Sp = frozenset(Sp)
        else: Sp = rand_event(D, x, jp)
        if not Sp: continue
        n2 += 1; lhs = cyl(D, S, Lv) == cyl(D, Sp, Lv); rhs = Sp == target; eq2 += lhs
        if lhs != rhs: f2 += 1
        if lhs and abs(wgt(S) - wgt(Sp)) > 1e-12: f4a += 1
        # L3
        J = max(j, jp); U = ext(D, S, J - j) | ext(D, Sp, J - jp)
        if cyl(D, U, Lv) != cyl(D, S, Lv) | cyl(D, Sp, Lv): f3 += 1
        C = frozenset(walks_from(D, x, j)) - S
        allH = frozenset(walks_from(D, x, H))
        if (cyl(D, C, Lv) if C else frozenset()) != allH - cyl(D, S, Lv): f3 += 1
    # L4 second half
    x = 0; reach = {x}; fr = [x]
    while fr:
        v = fr.pop()
        for (u, _) in D[v]:
            if u not in reach: reach.add(u); fr.append(u)
    if any(len(D[v]) >= 2 for v in reach):
        f4b_checked += 1; found = False
        for j in range(0, 4):
            for w in walks_from(D, x, j):
                S = frozenset([w]); E = ext(D, S)
                if cyl(D, S, Lv) == cyl(D, E, Lv) and len(S) != len(E): found = True
        f4b_found += found
    # L6
    vs = list(D)
    if len(vs) >= 2:
        for _ in range(20):
            x, y = random.sample(vs, 2); S = rand_event(D, x, 2); Sp = rand_event(D, y, 2)
            if S and Sp and cyl(D, S, Lv) == cyl(D, Sp, Lv): f6 += 1
P["L1"] = dict(failures=f1, met=f1 == 0)
P["L2"] = dict(pairs=n2, pairs_with_equal_cylinders=int(eq2), failures=f2, met=f2 == 0 and eq2 > 0)
P["L3"] = dict(failures=f3, met=f3 == 0)
P["L4"] = dict(consistent_family_failures=f4a, count_family_digraphs_checked=f4b_checked, count_family_conflict_found=f4b_found,
               met=f4a == 0 and f4b_checked == f4b_found)
found5 = 0; ex5 = None
for D in dead:
    Lv = live(D); hit = False
    for x in D:
        for j in range(0, 4):
            ws = walks_from(D, x, j)
            for w in ws:
                if w[-1] not in Lv and not hit:
                    # {w} has the empty cylinder: equal to the cylinder of the empty event, and S' = {} != Ext^0 {w}
                    S = frozenset([w]); 
                    if cyl(D, S, Lv) == frozenset(): hit = True; ex5 = ex5 or dict(digraph={str(k): [u for u, _ in v] for k, v in D.items()}, walk=list(w))
    found5 += hit
P["L5"] = dict(digraphs_with_dead_end=len(dead), counterexample_to_a_found_on=found5, example=ex5, met=found5 > 0,
               note="a walk ending where no history continues has an empty cylinder; (a) 'only if' fails without the hypothesis, which is stated in the section text before the lemma and not in the lemma")
P["L6"] = dict(failures=f6, met=f6 == 0)

# ---- prop:add
def regular_ok(D):
    ds = {len(D[v]) for v in D}
    return len(ds) == 1 and min(ds) >= 1 and all(u != v for v in D for (u, _) in D[v])
def with_gains(Dn, q): return {v: [(u, random.randrange(q)) for (u, _) in Dn[v]] for v in Dn}
fam = []
for n in (3, 4, 5): fam.append((f"cycle n={n}", {v: [((v + 1) % n, 0)] for v in range(n)}))
for n in (3, 4): fam.append((f"complete n={n}", {v: [(u, 0) for u in range(n) if u != v] for v in range(n)}))
fam.append(("circulant n=5 {1,2}", {v: [((v + 1) % 5, 0), ((v + 2) % 5, 0)] for v in range(5)}))
fam.append(("circulant n=6 {1,3}", {v: [((v + 1) % 6, 0), ((v + 3) % 6, 0)] for v in range(6)}))
for i in range(14):
    n = random.randrange(4, 7); d = random.randrange(1, 4)
    fam.append((f"random n={n} d={d} #{i}", {v: [(u, 0) for u in random.sample([u for u in range(n) if u != v], d)] for v in range(n)}))
fam.append(("deliberately irregular", {0: [(1, 0)], 1: [(0, 0), (2, 0)], 2: [(0, 0)]}))
fam.append(("deliberately with loop", {0: [(0, 0), (1, 0)], 1: [(0, 0), (1, 0)]}))
c = sp.Symbol('c')
def solve_add(D, q, a_val, Lw=5):
    d = len(D[0]); eqs = set(); fs = {}
    def F(w):
        if w[-1] != w[0] : return sp.Integer(a_val)
        g = sum(D[w[i]][[u for (u, _) in D[w[i]]].index(w[i + 1])][1] for i in range(len(w) - 1)) % q
        return fs.setdefault(g, sp.Symbol(f"f{g}"))
    kind1 = False
    for L in range(0, Lw + 1):
        for w in walks_from(D, 0, L):
            if w[-1] != 0 and all(u != 0 for (u, _) in D[w[-1]]): kind1 = True
            eqs.add(sp.expand(sum(F(w + (u,)) for (u, _) in D[w[-1]]) - c * F(w)))
    eqs.discard(sp.Integer(0))
    sols = sp.solve(list(eqs), [c] + list(fs.values()), dict=True)
    return d, sols, list(fs.values()), kind1
a1 = []; n_q = 0; a1_fail = 0; a2_fail = 0; k1 = k2 = 0; a3 = []
for name, Dn in fam:
    if not regular_ok(Dn): a1.append(dict(name=name, excluded="hypothesis not met")); continue
    for q in (1, 2, 3):
        D = with_gains(Dn, q); n_q += 1
        d, sols, fsyms, kind1 = solve_add(D, q, 1); k1 += kind1; k2 += not kind1
        pos = [s for s in sols if not (s.get(c, c).is_number and (s[c].is_real is False or s[c] <= 0))]
        ok = all(s.get(c) == d and all(s.get(f) == 1 for f in fsyms) for s in pos) and len(pos) >= 1
        a1_fail += not ok
        d, sols0, fsyms0, _ = solve_add(D, q, 0)
        pos0 = [s for s in sols0 if not (s.get(c, c).is_number and (s[c].is_real is False or s[c] <= 0))]
        ok0 = all(all(s.get(f, None) == 0 for f in fsyms0) for s in pos0)
        a2_fail += not ok0
        rec = dict(name=name, q=q, d=d, kind1=bool(kind1), closed_gains=len(fsyms), sols_a1=str(pos), sols_a0=str(pos0), A1=bool(ok), A2=bool(ok0))
        a1.append(rec)
        if name.startswith("cycle"): a3.append(ok and ok0)
P["A0"] = dict(built=len(fam), qualifying_graphs=sum(1 for r in fam if regular_ok(r[1])), instances_with_gains=n_q, met=n_q > 0)
P["A1"] = dict(failures=a1_fail, first_kind=k1, second_kind=k2, met=a1_fail == 0)
P["A2"] = dict(failures=a2_fail, met=a2_fail == 0)
P["A3"] = dict(cycle_instances=len(a3), met=all(a3) and len(a3) > 0)
D = {0: [(0, 0), (1, 0)], 1: [(0, 0), (1, 0)]}
d, sols, fsyms, _ = solve_add(D, 1, 1)
P["A4"] = dict(solutions=str(sols), met=True, note="hypothesis 'no loops' violated on purpose; recorded only")
res["prop_add_instances"] = a1
res["all_met"] = all(v["met"] for v in P.values())
json.dump(res, open(OUT, "w"), indent=1, default=str)
for k, v in P.items(): print(k, v)
print("all met", res["all_met"])
