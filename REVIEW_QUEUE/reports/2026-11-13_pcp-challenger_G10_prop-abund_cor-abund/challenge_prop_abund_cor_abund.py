#!/usr/bin/env python3
"""Second challenger program for G10 Proposition 5.14 (prop:abund) and Corollary 5.15 (cor:abund), edition Z15.
Paper text only (body.tex lines 302-328).  Uses REVIEW_QUEUE/lib/pcplib.py (reviewer's own library).

Conventions: E[z][y] = gain of the arc y -> z; groups additive, tuples of exponents; D-hat has vertices (y, g) and
arcs (y, g) -> (z, g + gain).  "Class" = cyclic class of D-hat, numbered so that arcs go from class i to i+1 mod r.
u = gain(y1 -> z) - gain(y2 -> z) for the first common successor z.  Counting is exact (Python integers).

Carriers: arc digraphs of random d-in d-out multidigraphs on 1..3 nodes with a block of gains at each node:
 deg 2: [[0,0],[0,e]] with e of order two; groups Z2, Z4, Z6, Z8, Z12, Z2xZ2, Z2xZ4, Z2xZ6 (non-cyclic included);
 deg 3: Fourier block w^(zy), w of order 3; groups Z3, Z6, Z3xZ3, Z9 (w = 3), Z12 (w = 4);
 deg 4: Fourier block i^(zy) (groups Z4, Z8, Z12, Z4xZ2) and the real Hadamard block of Z2xZ2 type
        e^(z1 y1) f^(z2 y2) on groups Z2xZ2, Z2xZ4 (attention asked by the director: non-cyclic groups, degree four).
 Each with random row and column gains ("switched") and, for a third of them, none.

PREDICATES (fixed before the first run):
 H   per carrier: (h1) A*A = d exactly for the stated character; (h2) D-hat strongly connected.  Count built / h1 / h1&h2.
     Carriers failing h2 are kept aside for N1.
 A1  (a) every vertex of D has d successors and d predecessors.
 A2  (a) r0 divides r.
 A3  (a) the shift pi(h) = class(x, g+h) - class(x, g) mod r does not depend on (x, g); pi is a homomorphism;
     its image is r0 Z/r; the index of C0 = ker pi is r/r0.
 B1  (b) for every pair y1 != y2 with a common successor (count of pairs reported), for start vertices 0 and one random,
     for every coset K of C0: there is a length L <= LMAX = 4|V-hat| + 60 at which the set of gains of the walks to y1 is
     exactly K with every count >= N = 25, and the set of gains to y2 is exactly K + u with every count >= N.
 B2  (b) at every length 0..LMAX and every vertex y the set of gains of walks to y lies in one coset of C0.
 C1  (c) [there is a length <= LMAX at which every element of C is a gain of a walk to y1, and one for y2]  <=>  r = r0.
     Both directions counted separately.
 C2  (c) last sentence: for a character that is not faithful the hypothesis of Corollary 5.13 on VALUES can hold with
     r != r0: search the carriers for an instance (character values all occur at y1 and y2 at one length, r != r0).
     met = at least one found among carriers whose character is not faithful (count of such carriers reported).
 K1  cor:abund first claim, cyclic groups with the faithful character only (count reported): q0 = |C0| >= 2 whenever a
     pair with a common successor exists.
 K2  cor:abund: u + u_z' in C0 for every common successor z' of every pair (additive notation), and the multiset sums
     to zero in Z[zeta] (exact).
 K3  cor:abund dimension, through Theorem 5.12's equation (V) on Z[C0] with the carrier's own multiset (u u_z'):
     solution space on a box of Z[zeta_q0] has dimension phi(q0)/2 (1 for q0 = 2), every unknown occurring in an
     equation; done for every qualifying cyclic carrier with phi(q0) <= 4, box coefficients -2..2 (phi <= 2) or -1..1.
     NOTE this tests the reduction to (V), not consistency on all events of the carrier.
 K4  cor:abund through actual events (only carriers with at most 8 vertices and q0 in {2,4,6}, at most 12 of them):
     consistency equations mu(Ext S) = d mu(S) over 400 random events of lengths 1..6 from vertex 0 in unknowns
     phi(|alpha|^2 exact key); predicate: N_1 (the squared modulus) solves all of them exactly, and the solution space
     restricted to unknowns that occur has dimension >= 1 (it can exceed phi(q0)/2 on finitely many events).
 X1  the paper's four-vertex example for q = 4: A*A = 2, D aperiodic, D-hat strongly connected of period 2, and at
     every length 3..40 exactly two of the four gains occur at each vertex reached.
 N1  remark after the corollary ("where the gains of closed walks generate a proper subgroup, D-hat is not strongly
     connected"): on the carriers failing h2, the gains of closed walks at vertex 0 (lengths <= 2|V|+6) generate a
     proper subgroup; and on those passing h2 they generate C.
Seed 20261113.  Result file challenge_prop_abund_cor_abund_results.json, never overwritten.  Run time aim < 3 min.
"""
import json, os, sys, random, itertools, math
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
for p in (os.path.join(HERE, "..", "..", "lib"), "/home/user/From-Prephysical-Hypotheses-to-Physical-Models/REVIEW_QUEUE/lib"):
    if os.path.exists(os.path.join(p, "pcplib.py")): sys.path.insert(0, p); break
import pcplib as L
OUT = os.path.join(HERE, "challenge_prop_abund_cor_abund_results.json")
if os.path.exists(OUT): sys.exit("result file exists; refusing to overwrite")
rng = random.Random(20261113)

def fam():
    out = []
    def M2(e, mod): z = L.gzero(mod); return [[z, z], [z, e]]
    for mod, e, k in (((2,), (1,), (1,)), ((4,), (2,), (1,)), ((6,), (3,), (1,)), ((8,), (4,), (1,)), ((12,), (6,), (1,)),
                      ((6,), (3,), (3,)), ((12,), (6,), (3,)), ((4,), (2,), (1,)),
                      ((2, 2), (1, 0), (1, 0)), ((2, 2), (1, 1), (1, 0)), ((2, 4), (1, 0), (1, 1)), ((2, 4), (0, 2), (0, 1)), ((2, 6), (1, 0), (1, 1))):
        out.append(("deg2", mod, k, M2(e, mod)))
    def F(d, w, mod): return [[tuple((z * y * wi) % m for wi, m in zip(w, mod)) for y in range(d)] for z in range(d)]
    for mod, w, k in (((3,), (1,), (1,)), ((6,), (2,), (1,)), ((9,), (3,), (1,)), ((12,), (4,), (1,)), ((3, 3), (1, 0), (1, 1)), ((3, 3), (1, 1), (1, 0)), ((6,), (2,), (2,))):
        out.append(("deg3", mod, k, F(3, w, mod)))
    for mod, w, k in (((4,), (1,), (1,)), ((8,), (2,), (1,)), ((12,), (3,), (1,)), ((4, 2), (1, 0), (1, 1)), ((4, 2), (1, 1), (1, 0))):
        out.append(("deg4 fourier", mod, k, F(4, w, mod)))
    for mod, e, f, k in (((2, 2), (1, 0), (0, 1), (1, 1)), ((2, 4), (1, 0), (0, 2), (1, 1)), ((2, 2), (1, 0), (1, 0), (1, 0)), ((4,), (2,), (2,), (1,))):
        H = [[L.gadd(tuple((z1 * y1 * a) % m for a, m in zip(e, mod)), tuple((z2 * y2 * a) % m for a, m in zip(f, mod)), mod)
              for (y1, y2) in itertools.product(range(2), repeat=2)] for (z1, z2) in itertools.product(range(2), repeat=2)]
        out.append(("deg4 hadamard", mod, k, H))
    return out

def faithful(k, mod): 
    G = L.group(mod); return len({L.chi_exp(k, g, mod) for g in G}) == len(G)
def cosets(C0, G, mod):
    seen = set(); out = []
    for g in G:
        K = frozenset(L.gadd(g, h, mod) for h in C0)
        if K not in seen: seen.add(K); out.append(K)
    return out
def closed_gain_subgroup(E, mod, maxlen):
    n = len(E); cur = {(0, L.gzero(mod))}; gains = set()
    for _ in range(maxlen):
        cur = {(z, L.gadd(g, E[z][y], mod)) for (y, g) in cur for z in range(n) if E[z][y] is not None}
        gains |= {g for (y, g) in cur if y == 0}
    H = {L.gzero(mod)}; ch = True
    while ch:
        new = {L.gadd(a, b, mod) for a in H for b in gains} | H; ch = len(new) > len(H); H = new
    return H

res = dict(seed=20261113, carriers=[], predicates={}); P = res["predicates"]
cnt = dict(built=0, h1=0, h12=0); fails = {k: 0 for k in ("A1", "A2", "A3", "B1", "B2", "C1_if", "C1_onlyif", "K1", "K2", "K3", "K4", "N1")}
pairs_total = 0; c2_found = 0; c2_candidates = 0; k_cyc = 0; k3_done = 0; k4_done = 0; r_ne = 0; noncyc = 0; deg4 = 0; aside = 0
k3_detail = []
for (name, mod, k, M) in fam():
    for rep in range(9):
        nodes = 1 + rep % 3
        E = L.block_carrier(nodes, M, mod, rng, switch=(rep % 3 != 2)); cnt["built"] += 1
        d = L.norm_preserving(E, mod, k)
        if d is None or d < 2: continue
        cnt["h1"] += 1
        n = len(E); G = L.group(mod); idx, S = L.lift(E, mod); sc = L.strongly_connected(S)
        Hsub = closed_gain_subgroup(E, mod, 2 * n + 6)
        if not sc:
            aside += 1
            if len(Hsub) == len(G): fails["N1"] += 1
            continue
        if len(Hsub) != len(G): fails["N1"] += 1
        cnt["h12"] += 1; noncyc += len(mod) > 1; deg4 += d == 4
        sD = L.succ(E); pred = [sum(1 for y in range(n) if E[z][y] is not None) for z in range(n)]
        if any(len(s) != d for s in sD) or any(p != d for p in pred): fails["A1"] += 1
        r, cls = L.period(S); r0, _ = L.period([list(s) for s in sD])
        if r % r0: fails["A2"] += 1
        pi = {}; ok = True
        for h in G:
            sh = {(cls[idx[(x, L.gadd(g, h, mod))]] - cls[idx[(x, g)]]) % r for x in range(n) for g in G}
            if len(sh) != 1: ok = False
            pi[h] = min(sh)
        ok &= all(pi[L.gadd(a, b, mod)] == (pi[a] + pi[b]) % r for a in G for b in G)
        ok &= set(pi.values()) == {(r0 * t) % r for t in range(r)}
        C0 = [h for h in G if pi[h] == 0]; ok &= len(G) == len(C0) * (r // r0)
        if not ok: fails["A3"] += 1
        r_ne += r != r0
        LMAX = 4 * len(S) + 60
        pairs = [(a, b) for a in range(n) for b in range(a + 1, n) if set(sD[a]) & set(sD[b])]; pairs_total += len(pairs)
        Ks = cosets(C0, G, mod); isfaith = faithful(k, mod); cyc = len(mod) == 1 and isfaith
        counts_by_start = {}
        for st in {0, rng.randrange(n)}:
            wc = L.walk_counts(S, idx[(st, L.gzero(mod))], LMAX)
            gains = []   # per length: dict y -> dict g -> count
            inv = {i: yg for yg, i in idx.items()}
            for cur in wc:
                dd = {}
                for v, c in cur.items(): y, g = inv[v]; dd.setdefault(y, {})[g] = c
                gains.append(dd)
            counts_by_start[st] = gains
            for dd in gains:
                for y, gg in dd.items():
                    if not any(set(gg) <= K for K in Ks): fails["B2"] += 1
            for (y1, y2) in pairs:
                z = sorted(set(sD[y1]) & set(sD[y2]))[0]; u = L.gsub(E[z][y1], E[z][y2], mod)
                for K in Ks:
                    Ku = frozenset(L.gadd(g, u, mod) for g in K)
                    if not any(set(dd.get(y1, {})) == set(K) and set(dd.get(y2, {})) == set(Ku) and min(dd[y1].values()) >= 25 and min(dd[y2].values()) >= 25 for dd in gains):
                        fails["B1"] += 1
                all1 = any(len(dd.get(y1, {})) == len(G) for dd in gains); all2 = any(len(dd.get(y2, {})) == len(G) for dd in gains)
                if (r == r0) and not (all1 and all2): fails["C1_if"] += 1
                if (r != r0) and (all1 or all2): fails["C1_onlyif"] += 1
                if not isfaith:
                    c2_candidates += 1; Lq = L.lcm(mod); vals = {L.chi_exp(k, g, mod) for g in G}
                    if r != r0 and any({L.chi_exp(k, g, mod) for g in dd.get(y1, {})} == vals and {L.chi_exp(k, g, mod) for g in dd.get(y2, {})} == vals for dd in gains): c2_found += 1
        if cyc and pairs:
            k_cyc += 1; q = mod[0]; q0 = len(C0)
            if q0 < 2: fails["K1"] += 1; continue
            y1, y2 = pairs[0]; Z = sorted(set(sD[y1]) & set(sD[y2])); u = L.gsub(E[Z[0]][y1], E[Z[0]][y2], mod)
            ms = [L.gadd(u, L.gsub(E[z][y2], E[z][y1], mod), mod) for z in Z]
            if any(m not in C0 for m in ms) or not L.zero_sum([m[0] for m in ms], q): fails["K2"] += 1; continue
            R = L.Ring(q0); 
            if R.n <= 4:
                k3_done += 1; step = q // q0; us = [m[0] // step for m in ms]
                rngs = range(-2, 3) if R.n <= 2 else range(-1, 2)
                B = [tuple(t) for t in itertools.product(rngs, repeat=R.n)]; keys = {}; eqs = []
                def ix(key):
                    if key not in keys: keys[key] = len(keys)
                    return keys[key]
                for a in B:
                    for b in B:
                        row = {}
                        for e in us: j = ix(R.N(R.add(a, R.mulz(b, e)))); row[j] = row.get(j, 0) + 1
                        for t in (a, b): j = ix(R.N(t)); row[j] = row.get(j, 0) - len(us)
                        eqs.append(row)
                Mx = np.zeros((len(eqs) + 1, len(keys)))
                for i, row in enumerate(eqs):
                    for j, v in row.items(): Mx[i, j] = v
                Mx[len(eqs), keys[R.N(R.zero())]] = 1
                dim, gap, kept, dropped = L.null_dim(Mx); exp = 1 if q0 == 2 else len(R.J)
                occ = int(np.any(Mx != 0, axis=0).sum()) == len(keys)
                k3_detail.append(dict(name=name, q=q, q0=q0, m=len(us), dim=dim, expected=exp, gap=gap, unknowns=len(keys)))
                if dim != exp or not occ: fails["K3"] += 1
            if n <= 8 and q0 in (2, 4, 6) and k4_done < 12:
                k4_done += 1; Rq = L.Ring(q); keys = {}; rows = []
                def ix2(key):
                    if key not in keys: keys[key] = len(keys)
                    return keys[key]
                for _ in range(400):
                    Lw = rng.randrange(1, 7); walks = set()
                    for _ in range(rng.randrange(1, 9)):
                        w = [0]
                        for _ in range(Lw): w.append(rng.choice(sD[w[-1]]))
                        walks.add(tuple(w))
                    v = {}; ext = {}
                    for w in walks:
                        g = sum(E[w[i + 1]][w[i]][0] for i in range(Lw)) % q
                        v[w[-1]] = Rq.add(v.get(w[-1], Rq.zero()), Rq.pw[g])
                        for z in sD[w[-1]]: ext[z] = Rq.add(ext.get(z, Rq.zero()), Rq.pw[(g + E[z][w[-1]][0]) % q])
                    row = {}
                    for val in ext.values(): j = ix2(Rq.N(val)); row[j] = row.get(j, 0) + 1
                    for val in v.values(): j = ix2(Rq.N(val)); row[j] = row.get(j, 0) - d
                    rows.append(row)
                Mx = np.zeros((len(rows) + 1, len(keys)))
                for i, row in enumerate(rows):
                    for j, vv in row.items(): Mx[i, j] = vv
                if Rq.N(Rq.zero()) in keys: Mx[len(rows), keys[Rq.N(Rq.zero())]] = 1
                vec = np.array([0.0] * len(keys))
                for key, j in keys.items(): vec[j] = Rq.emb(key, 1).real
                if np.abs(Mx @ vec).max() > 1e-9: fails["K4"] += 1     # integers up to ~1e3: rounding < 1e-11
        res["carriers"].append(dict(name=name, mod=list(mod), char=list(k), nodes=nodes, n=n, d=d, r=r, r0=r0, C0=len(C0), pairs=len(pairs), faithful=bool(isfaith)))
P["H"] = dict(built=cnt["built"], h1=cnt["h1"], h1_and_h2=cnt["h12"], not_strongly_connected=aside, non_cyclic_qualifying=noncyc, degree_four_qualifying=deg4, with_r_ne_r0=r_ne, met=cnt["h12"] > 0 and noncyc > 0 and deg4 > 0 and r_ne > 0)
for kk in ("A1", "A2", "A3", "B2"): P[kk] = dict(failures=fails[kk], met=fails[kk] == 0)
P["B1"] = dict(pairs=pairs_total, failures=fails["B1"], met=fails["B1"] == 0 and pairs_total > 0)
P["C1"] = dict(failures_if=fails["C1_if"], failures_only_if=fails["C1_onlyif"], met=fails["C1_if"] == 0 and fails["C1_onlyif"] == 0)
P["C2"] = dict(pair_instances_with_unfaithful_character=c2_candidates, found_with_r_ne_r0=c2_found, met=c2_found > 0)
P["K1"] = dict(cyclic_faithful_with_pair=k_cyc, failures=fails["K1"], met=fails["K1"] == 0 and k_cyc > 0)
P["K2"] = dict(failures=fails["K2"], met=fails["K2"] == 0)
P["K3"] = dict(done=k3_done, failures=fails["K3"], detail=k3_detail, met=fails["K3"] == 0 and k3_done > 0)
P["K4"] = dict(done=k4_done, failures=fails["K4"], met=fails["K4"] == 0 and k4_done > 0)
P["N1"] = dict(failures=fails["N1"], carriers_not_strongly_connected=aside, met=fails["N1"] == 0)
# X1
ex = [(0, 2, 0), (0, 3, 1), (1, 0, 1), (1, 1, 3), (2, 0, 0), (2, 1, 0), (3, 2, 0), (3, 3, 3)]
E = [[None] * 4 for _ in range(4)]
for (a, b, e) in ex: E[b][a] = (e,)
d = L.norm_preserving(E, (4,), (1,)); idx, S = L.lift(E, (4,)); sc = L.strongly_connected(S); r, _ = L.period(S); r0, _ = L.period([list(s) for s in L.succ(E)])
wc = L.walk_counts(S, idx[(0, (0,))], 40); inv = {i: yg for yg, i in idx.items()}; two = True
for cur in wc[3:]:
    per = {}
    for v in cur: per.setdefault(inv[v][0], set()).add(inv[v][1])
    two &= all(len(s) == 2 for s in per.values())
P["X1"] = dict(d=d, r0=r0, strongly_connected=bool(sc), r=r, exactly_two_gains=bool(two), met=bool(d == 2 and r0 == 1 and sc and r == 2 and two))
res["all_met"] = all(v["met"] for v in P.values())
json.dump(res, open(OUT, "w"), indent=1, default=str)
for kk, v in P.items(): print(kk, {a: b for a, b in v.items() if a != "detail"})
print("K3 dims:", sorted({(t["q"], t["q0"], t["m"], t["dim"], t["expected"]) for t in k3_detail}))
print("all met", res["all_met"])
