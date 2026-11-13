#!/usr/bin/env python3
"""Attack on stipulation S7 and instance Z1-F of candidate model Z1 (the character and the force).
Attacker: sub-agent of the author's model family.

Conventions.  C = Z_M written additively, M = lcm(q,2); zeta = exp(2 pi i/q) is the element M/q, -1 is M/2.  The character
psi_k sends the generator to exp(2 pi i k/M), so psi_k(zeta) = zeta^k and psi_k(-1) = (-1)^k; "the conjugate j" of the task
(zeta -> zeta^j with the minus sign kept) is psi_k with k = j modulo q and k odd.  psi_k is FAITHFUL iff gcd(k,M)=1.
B_q: vertices 0,1; A[y][x] = gain of the arc x->y; A = [[1, zeta],[1, -zeta]]; start x0 = 0.
Z1-F ring: N sites, vertex index 2x+s (s=0: R, 1: L); from (x,s) arcs to (x+1,R) and (x-1,L); gain = (-1 if s=L and the arc
goes to L) times m(x)^f, m(x) = zeta^(-x), f the field multiple (f=1 is the model's field Phi = 2 pi/q); N = q; start (0,R).
Amplitudes are exact: elements of the group ring Z[Z_M], compared after reduction modulo the cyclotomic polynomial Phi_M (basis
1, x, ..., x^(phi(M)-1), x = exp(2 pi i/M)).  P_t(y) = |amp_t(y)|^2 / d^t.  Decimal values are printed from the exact element
in double precision.  Only the long return search (B2d) is floating point: complex128, repeated multiplication of a 2x2
matrix, error of order t*1e-16; the threshold 0.99 is the one the model document uses in its weakness W3.

Predicates, fixed before the first run (prediction in brackets):
 B1  For q = 5, 8, 10, 12 on B_q: there are two norm-preserving characters, not inverse to each other, whose tables P_t(y),
     t <= 12, differ; the smallest such t is recorded with the difference.  [pass; expected t = 2, P_2(0) = (1+cos(2 pi k/q))/2]
 B1b P for psi_k and psi_-k are equal for every t <= 12 (complex conjugation).  [pass]
 B1c The norm-preserving characters of B_q are exactly the faithful ones.  [expected to FAIL for q = 5, 10, 12: odd k that
     are not coprime to M are norm-preserving too.  A failure is kept: it is a finding on the wording "the conjugates".]
 B2g Galois: for every faithful k, P^(k)_t(y) = sigma_k(P^(1)_t(y)) as exact elements (sigma_k: x -> x^k), t <= 12.  [pass]
 B2a The gain digraph B_q has no automorphism (vertex permutation, with switching allowed) that induces g -> a g on C for
     any unit a other than 1.  [pass: the Galois action is not a symmetry of the carrier]
 B2c Equality-type invariants agree for all faithful k: (i) the first t <= 300 with P_t(x0) = 1 exactly (or none);
     (ii) the set of t <= 60 with P_t(1) = 0 exactly (dark vertex); (iii) whether the reversed carrier with inverted gains
     gives the same table as the carrier, t <= 12.  [pass]
 B2d Order-type invariants separate the classes: P_2(0) and the first t <= 200000 with P_t(x0) > 0.99 are not the same for
     all classes {k,-k} of faithful characters, for each q.  [pass]
 F1  S1 holds for the Z1-F ring with N = q, q = 5, 6, 8 (out-degree 2, no parallel arcs, derived digraph strongly connected).
     [pass]
 F2  The norm-preserving characters of the Z1-F ring are exactly the faithful ones (the document: "the conjugates of the
     faithful one").  [expected to FAIL for q = 5 and q = 6]
 F3  For every norm-preserving k the step matrix of psi_k on the carrier with field Phi equals, entry by entry, the step
     matrix of psi_1 on the carrier with field k Phi (so the rules agree on every event).  [pass]
 F4  For every norm-preserving k other than +-1 there is t <= 12 at which the sorted list of the P_t(y) over all vertices
     differs from that of k = 1: no relabelling of vertices whatever identifies the two models.  [pass]
 F5  The relabelling x -> k^-1 x mod N (s kept) does not carry the table of psi_k to that of psi_1 for faithful k != +-1.
     [pass]   F5b: it does for no k except 1.
 F6  Among digraph automorphisms of the ring (found by search) with switching, only a = 1 and possibly a = -1 are induced
     on C.  [pass]
Writes Attack_S7_Results.json; refuses to overwrite.  No randomness.
"""
import itertools, json, math, os, sys
import numpy as np
from sympy import cyclotomic_poly, Poly, symbols
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Attack_S7_Results.json")
if os.path.exists(OUT): sys.exit("refusing to overwrite " + OUT)
R = {}

class Cyc:
    def __init__(self, L):
        self.L = L; x = symbols("x"); self.phi = [int(c) for c in Poly(cyclotomic_poly(L, x), x).all_coeffs()]
    def red(self, v):
        v = list(v); dphi = len(self.phi) - 1
        for k in range(len(v) - 1, dphi - 1, -1):
            c = v[k]
            if c:
                for i, a in enumerate(self.phi): v[k - i] -= c * a
        return tuple(v[:dphi])
    def norm2(self, v):
        L = self.L; out = [0] * L; nz = [(k, c) for k, c in enumerate(v) if c]
        for k, c in nz:
            for l, e in nz: out[(k - l) % L] += c * e
        return out
    def val(self, v): return sum(c * math.cos(2 * math.pi * k / self.L) for k, c in enumerate(v))
    def sigma(self, v, a):
        out = [0] * self.L
        for k, c in enumerate(v): out[(a * k) % self.L] += c
        return out

def Bq(q):
    M = q * 2 // math.gcd(q, 2)
    return {0: [(0, 0), (1, 0)], 1: [(0, M // q), (1, (M // q + M // 2) % M)]}, M
def ringF(q, f=1):
    N = q; M = q * 2 // math.gcd(q, 2); idx = lambda x, s: 2 * (x % N) + s
    succ = {idx(x, s): [(idx(x + 1, 0), (-f * x * (M // q)) % M),
                        (idx(x - 1, 1), (-f * x * (M // q) + (M // 2 if s == 1 else 0)) % M)] for x in range(N) for s in (0, 1)}
    return succ, M
def step_exp(succ, k, M): return {v: [(y, (k * g) % M) for y, g in succ[v]] for v in succ}   # exponents of x = exp(2 pi i/M)
def norm_pres(succ, k, M, cyc):
    d = len(succ[0]); E = step_exp(succ, k, M)
    for a in succ:
        for b in succ:
            acc = [0] * M; ca = dict(E[a]); cb = dict(E[b])
            for y in ca:
                if y in cb: acc[(cb[y] - ca[y]) % M] += 1
            if a == b: acc[0] -= d
            if any(cyc.red(acc)): return False
    return True
def tables(succ, k, M, cyc, T, x0=0, reverse=False):
    """exact P_t(y) * d^t as reduced elements, t = 0..T"""
    E = step_exp(succ, k, M)
    if reverse:
        Er = {v: [] for v in succ}
        for v in E:
            for y, g in E[v]: Er[y].append((v, (-g) % M))
        E = Er
    amp = {v: [0] * M for v in succ}; amp[x0][0] = 1; out = []
    for t in range(T + 1):
        out.append({v: cyc.red(cyc.norm2(amp[v])) for v in succ})
        new = {v: [0] * M for v in succ}
        for v in succ:
            a = amp[v]
            if any(a):
                for y, g in E[v]:
                    ny = new[y]
                    for i, c in enumerate(a):
                        if c: ny[(i + g) % M] += c
        amp = new
    return out
def fval(cyc, redv, den):   # decimal of a reduced element / den
    return sum(c * math.cos(2 * math.pi * i / cyc.L) for i, c in enumerate(redv)) / den
def derived_info(succ, M, x0=0):
    dd = {(v, g): [(y, (g + h) % M) for y, h in succ[v]] for v in succ for g in range(M)}
    def reach(s, adj):
        seen = {s}; st = [s]
        while st:
            u = st.pop()
            for w in adj[u]:
                if w not in seen: seen.add(w); st.append(w)
        return seen
    rev = {u: [] for u in dd}
    for u in dd:
        for w in dd[u]: rev[w].append(u)
    sc = len(reach((x0, 0), dd)) == len(dd) and len(reach((x0, 0), rev)) == len(dd)
    def per(adj, s):
        dist = {s: 0}; q = [s]; g = 0
        for u in q:
            for w in adj[u]:
                if w not in dist: dist[w] = dist[u] + 1; q.append(w)
                else: g = math.gcd(g, dist[u] + 1 - dist[w])
        return g
    und = {v: [y for y, _ in succ[v]] for v in succ}
    r = per(dd, (x0, 0)) if sc else None; r0 = per(und, x0)
    return dict(out_degrees=sorted({len(a) for a in succ.values()}), parallel=any(len({y for y, _ in a}) != len(a) for a in succ.values()),
                derived_strongly_connected=sc, period_derived=r, period_D=r0, order_C=M, order_C0=(M * r0 // r if sc else None))
def digraph_automorphisms(succ):
    V = sorted(succ); adj = {v: {y for y, _ in succ[v]} for v in V}; res = []
    def bt(i, pi, used):
        if i == len(V): res.append(dict(pi)); return
        v = V[i]
        for w in V:
            if w in used: continue
            ok = True
            for u in V[:i]:
                if (u in adj[v]) != (pi[u] in adj[w]) or (v in adj[u]) != (w in adj[pi[u]]): ok = False; break
            if ok and ((v in adj[v]) == (w in adj[w])):
                pi[v] = w; used.add(w); bt(i + 1, pi, used); used.discard(w); del pi[v]
    bt(0, {}, set()); return res
def induced_units(succ, M):
    """units a of Z_M for which some digraph automorphism pi and switching theta give gain(pi e) = a gain(e) + theta(t)-theta(s)"""
    gain = {(v, y): g for v in succ for y, g in succ[v]}; auts = digraph_automorphisms(succ); found = {}
    for a in [a for a in range(M) if math.gcd(a, M) == 1]:
        for pi in auts:
            # potential theta on vertices pi(v): propagate over the connected underlying graph
            diff = {(pi[v], pi[y]): (gain[(pi[v], pi[y])] - a * g) % M for (v, y), g in gain.items()}
            th = {0: 0}; st = [0]; ok = True
            nb = {}
            for (s, t), dlt in diff.items(): nb.setdefault(s, []).append((t, dlt)); nb.setdefault(t, []).append((s, (-dlt) % M))
            while st and ok:
                u = st.pop()
                for w, dlt in nb.get(u, []):
                    val = (th[u] + dlt) % M
                    if w not in th: th[w] = val; st.append(w)
                    elif th[w] != val: ok = False; break
            if ok: found.setdefault(a, 0); found[a] += 1
    return len(auts), found

# ======================= B: the two-vertex carrier
R["B1"] = {}; R["B1b"] = {}; R["B1c"] = {}; R["B2g"] = {}; R["B2a"] = {}; R["B2c"] = {}; R["B2d"] = {}
T = 12
for q in (5, 8, 10, 12):
    succ, M = Bq(q); cyc = Cyc(M)
    npk = [k for k in range(M) if norm_pres(succ, k, M, cyc)]; faithful = [k for k in npk if math.gcd(k, M) == 1]
    tab = {k: tables(succ, k, M, cyc, T) for k in npk}
    # B1
    first = None
    for t in range(T + 1):
        for k in npk:
            for l in npk:
                if k < l and (k + l) % M != 0 and tab[k][t] != tab[l][t] and first is None:
                    y = next(v for v in succ if tab[k][t][v] != tab[l][t][v])
                    first = dict(t=t, k=k, l=l, vertex=y, P_k=fval(cyc, tab[k][t][y], 2 ** t), P_l=fval(cyc, tab[l][t][y], 2 ** t),
                                 exact_k_times_2t=list(tab[k][t][y]), exact_l_times_2t=list(tab[l][t][y]))
        if first: break
    table = {str(k): {str(t): [round(fval(cyc, tab[k][t][v], 2 ** t), 12) for v in (0, 1)] for t in range(T + 1)} for k in npk}
    exact = {str(k): {str(t): [list(tab[k][t][v]) for v in (0, 1)] for t in range(T + 1)} for k in npk}
    classes = {}
    for k in npk: classes.setdefault(json.dumps([[list(tab[k][t][v]) for v in (0, 1)] for t in range(T + 1)]), []).append(k)
    R["B1"][f"q={q}"] = dict(M=M, norm_preserving_k=npk, faithful_k=faithful, j_of_k={str(k): k % q for k in npk},
        first_difference=first, classes_with_equal_tables=list(classes.values()), P_table_decimal=table,
        P_times_2t_exact_basis_1_x_x2=exact, passed=first is not None)
    R["B1b"][f"q={q}"] = all(tab[k] == tab[(-k) % M] for k in npk)
    R["B1c"][f"q={q}"] = dict(norm_preserving=npk, faithful=faithful, non_faithful_norm_preserving=[k for k in npk if k not in faithful],
        what_they_are={str(k): f"psi(zeta) = exp(2 pi i {k % q}/{q}), order of psi = {M // math.gcd(k, M)}" for k in npk if k not in faithful},
        passed=npk == faithful)
    # B2g
    full = {k: None for k in faithful}; okg = True
    E1 = step_exp(succ, 1, M)
    amp = {v: [0] * M for v in succ}; amp[0][0] = 1; unred = []
    for t in range(T + 1):
        unred.append({v: cyc.norm2(amp[v]) for v in succ})
        new = {v: [0] * M for v in succ}
        for v in succ:
            for y, g in E1[v]:
                for i, c in enumerate(amp[v]):
                    if c: new[y][(i + g) % M] += c
        amp = new
    for k in faithful:
        for t in range(T + 1):
            for v in succ: okg &= cyc.red(cyc.sigma(unred[t][v], k)) == tab[k][t][v]
    R["B2g"][f"q={q}"] = bool(okg)
    # B2a
    nauts, found = induced_units(succ, M)
    R["B2a"][f"q={q}"] = dict(digraph_automorphisms=nauts, units_induced={str(a): n for a, n in found.items()},
                              passed=set(found) == {1})
    # B2c
    inv = {}
    for k in faithful:
        tl = tables(succ, k, M, cyc, 300)
        one = lambda t: cyc.red([2 ** t] + [0] * (M - 1))
        fr = next((t for t in range(1, 301) if tl[t][0] == one(t)), None)
        dark = [t for t in range(1, 61) if not any(tl[t][1])]
        rev = tables(succ, k, M, cyc, T, reverse=True) == tab[k]
        inv[k] = dict(first_exact_return=fr, dark_times_vertex1=dark, reversal_symmetric=rev)
    vals = list(inv.values())
    R["B2c"][f"q={q}"] = dict(per_k={str(k): v for k, v in inv.items()}, passed=all(v == vals[0] for v in vals))
    # B2d (floating point)
    od = {}
    for k in faithful:
        z = np.exp(2j * np.pi * k / M) ** (M // q)
        U = np.array([[1, z], [1, -z]], dtype=complex) / np.sqrt(2); v = np.array([1, 0], dtype=complex); fr = None; best = (0, 0)
        for t in range(1, 200001):
            v = U @ v; p = abs(v[0]) ** 2
            if p > best[0]: best = (p, t)
            if p > 0.99: fr = t; break
        od[k] = dict(P2_at_0=fval(cyc, tab[k][2][0], 4), first_t_return_above_0_99=fr, best_seen=None if fr else best)
    cl = {}
    for k in faithful: cl.setdefault(min(k, M - k), od[k])
    distinct = {json.dumps(v) for v in cl.values()}
    R["B2d"][f"q={q}"] = dict(per_class={str(k): v for k, v in cl.items()}, classes=len(cl),
                              passed=(len(distinct) > 1) if len(cl) > 1 else None)
for key in ("B1",): R[key]["passed"] = all(R[key][f"q={q}"]["passed"] for q in (5, 8, 10, 12))
R["B1b"]["passed"] = all(R["B1b"][f"q={q}"] for q in (5, 8, 10, 12))
R["B1c"]["passed"] = all(R["B1c"][f"q={q}"]["passed"] for q in (5, 8, 10, 12))
R["B1c"]["note"] = "predicted to fail for q = 5, 10, 12"
R["B2g"]["passed"] = all(R["B2g"][f"q={q}"] for q in (5, 8, 10, 12))
R["B2a"]["passed"] = all(R["B2a"][f"q={q}"]["passed"] for q in (5, 8, 10, 12))
R["B2c"]["passed"] = all(R["B2c"][f"q={q}"]["passed"] for q in (5, 8, 10, 12))
R["B2d"]["passed"] = all(R["B2d"][f"q={q}"]["passed"] in (True, None) for q in (5, 8, 10, 12))

# ======================= F: the ring with a linear gain, N = q
R["F1"] = {}; R["F2"] = {}; R["F3"] = {}; R["F4"] = {}; R["F5"] = {}; R["F6"] = {}
for q in (5, 6, 8):
    succ, M = ringF(q, 1); cyc = Cyc(M); N = q
    info = derived_info(succ, M); R["F1"][f"q={q}"] = dict(info, passed=info["out_degrees"] == [2] and not info["parallel"] and info["derived_strongly_connected"])
    npk = [k for k in range(M) if norm_pres(succ, k, M, cyc)]; faithful = [k for k in npk if math.gcd(k, M) == 1]
    R["F2"][f"q={q}"] = dict(norm_preserving=npk, faithful=faithful,
        non_faithful={str(k): f"field {k % q} Phi (mod 2 pi), psi(-1) = {(-1) ** k}" for k in npk if k not in faithful},
        passed=npk == faithful)
    ok3 = True
    for k in npk:
        succk, _ = ringF(q, k)
        ok3 &= step_exp(succ, k, M) == step_exp(succk, 1, M)
    R["F3"][f"q={q}"] = bool(ok3)
    tab = {k: tables(succ, k, M, cyc, T) for k in npk}
    classes = {}
    for k in npk: classes.setdefault(json.dumps([[list(tab[k][t][v]) for v in sorted(succ)] for t in range(T + 1)]), []).append(k)
    f4 = {}; f5 = {}
    for k in npk:
        if k in (1, M - 1): continue
        ft = None
        for t in range(T + 1):
            a = sorted(tab[k][t][v] for v in succ); b = sorted(tab[1][t][v] for v in succ)
            if a != b:
                ft = dict(t=t, sorted_P_k=sorted(round(fval(cyc, x, 2 ** t), 10) for x in a),
                          sorted_P_1=sorted(round(fval(cyc, x, 2 ** t), 10) for x in b),
                          return_P_k=fval(cyc, tab[k][t][0], 2 ** t), return_P_1=fval(cyc, tab[1][t][0], 2 ** t)); break
        f4[k] = ft
        if math.gcd(k % N if k % N else N, N) == 1:
            kinv = pow(k % N, -1, N)
            # table of psi_k at (x,s) against table of psi_1 at (k^-1 x, s) and at (k x, s)
            same1 = all(tab[k][t][2 * x + s] == tab[1][t][2 * ((kinv * x) % N) + s] for t in range(T + 1) for x in range(N) for s in (0, 1))
            same2 = all(tab[k][t][2 * x + s] == tab[1][t][2 * ((k * x) % N) + s] for t in range(T + 1) for x in range(N) for s in (0, 1))
            f5[k] = dict(relabel_x_to_kinv_x=same1, relabel_x_to_k_x=same2)
    R["F4"][f"q={q}"] = dict(classes_with_equal_tables=list(classes.values()), first_difference_of_sorted_tables={str(k): v for k, v in f4.items()},
                             conj_equal=all(tab[k] == tab[(-k) % M] for k in npk), passed=all(v is not None for v in f4.values()))
    R["F5"][f"q={q}"] = dict(per_k={str(k): v for k, v in f5.items()},
                             passed=not any(v["relabel_x_to_kinv_x"] or v["relabel_x_to_k_x"] for v in f5.values()))
    nauts, found = induced_units(succ, M)
    R["F6"][f"q={q}"] = dict(digraph_automorphisms=nauts, units_induced={str(a): n for a, n in found.items()},
                             passed=set(found) <= {1, M - 1})
for key in ("F1", "F2", "F4", "F5", "F6"): R[key]["passed"] = all(R[key][f"q={q}"]["passed"] for q in (5, 6, 8))
R["F2"]["note"] = "predicted to fail for q = 5 and q = 6"
R["F3"]["passed"] = all(R["F3"][f"q={q}"] for q in (5, 6, 8))
R["summary"] = {k: R[k]["passed"] for k in ("B1", "B1b", "B1c", "B2g", "B2a", "B2c", "B2d", "F1", "F2", "F3", "F4", "F5", "F6")}
json.dump(R, open(OUT, "w"), indent=1, default=str)
print(json.dumps(R["summary"], indent=1))
