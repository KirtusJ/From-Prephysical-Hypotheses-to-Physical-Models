"""Challenger 11: Corollary cor:return (return weight). Predicates fixed before the first run.

Carrier: finite V, gains in C = Z_{n1} x ... (exponent tuples), step given as dict (y,x)->gain
(so at most one arc per ordered pair by construction; H0 checks this is meaningful), x0 fixed.

Hypotheses tested per carrier (carrier qualifies only if all hold):
 H1 every vertex has exactly d >= 2 outgoing arcs.
 H2 derived digraph hat D on V x C strongly connected (BFS forward and backward from (x0,1)).
 H3 U(D) non-empty: set of characters psi with A^(psi)* A^(psi) = d, numerically, max abs deviation
    < 1e-9. Basis: entries are sums of <= |V| products of unit complex numbers (rounding ~1e-15);
    the measured separation between qualifying and non-qualifying deviations is reported (GAPMIN).
Reported: period r of \hat D, period r0 of D, |C0|, number of classes of U(D)|_{C0} under psi'~psi'^-1.

Predicates (t = 1..T, T = 2000):
 P0 mu(S_0)=1 and sum_y R_t(y) = 1 at t in {1,2,3,7,50} for a in {0,1/3,1}, c equal over classes
    (measured deviation reported; met if < 1e-9; basis: unitary iteration error <= t*|V|*1e-15).
 P1 exact: N_t * d <= d^t for every t >= 1 (integers).
 P2 for a in {0,1/3,1}, every class k, every t>=1: a N_t/d^t + (1-a) w_k(t) <= 1 - a(1-1/d) + 1e-9,
    with w_k(t) = |(U_psi^t)_{x0x0}|^2 (this covers every convex choice of c). Minimal margin measured.
 P3 w_k(t) agrees for all psi in U(D) with the same class of restriction to C0 (max spread measured;
    met if < 1e-9).
 P4 (part 2) for a = 0: max over t in [1000,2000] of min_k w_k(t) (all classes simultaneously, as the
    proof claims) is measured; met if >= 0.99 (0.99 is the paper's own reported figure, not a theorem:
    the theorem gives limsup only, so a miss is "measured only", not a failure of the corollary).
 P5 (part 3) at the best t for each a and class: a <= eta d/(d-1) + 1e-9 with eta = 1 - R_t.
 P6 when R_t(x0) = 0 for all t not in one residue class (periodic return) record it; consistent with
    (1)-(3) is a reading, not a predicate.
Counterexample search (C1): all out-regular digraphs with d=2 on 2 and 3 vertices and 3000 random ones
 (seed 11) with d in {2,3,4}, |V| <= 6, no gains needed: is N_t d > d^t for some 1<=t<=14, any x0?
 (C2): same with one parallel arc allowed (hypothesis violated): expected to break; kept.
Result file ret_result.json is not overwritten.
"""
import itertools, json, os, sys, cmath, math, random
from fractions import Fraction
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "ret_result.json")
if os.path.exists(OUT):
    sys.exit("refusing to overwrite " + OUT)
T = 2000
TOL = 1e-9


def gadd(g, h, mods):
    return tuple((a + b) % n for a, b, n in zip(g, h, mods))


def chars(mods):
    return list(itertools.product(*[range(n) for n in mods]))


def chi(k, g, mods):
    return cmath.exp(2j * math.pi * sum(Fraction(ki * gi, n) for ki, gi, n in zip(k, g, mods)))


def analyse(name, V, arcs, mods, x0):
    """arcs: dict (y,x) -> gain tuple, arc x -> y."""
    res = {"name": name, "nV": len(V), "mods": mods, "x0": str(x0)}
    idx = {v: i for i, v in enumerate(V)}
    out = {v: [(y, g) for (y, x), g in arcs.items() if x == v] for v in V}
    degs = {len(out[v]) for v in V}
    res["H1"] = (len(degs) == 1 and min(degs) >= 2)
    if not res["H1"]:
        res["qualifies"] = False
        return res
    d = degs.pop()
    res["d"] = d
    res["loop_at_x0"] = (x0, x0) in arcs
    C = chars(mods)
    one = tuple(0 for _ in mods)
    # derived digraph
    def bfs(start, fwd=True):
        dist = {start: 0}
        fr = [start]
        while fr:
            nf = []
            for (x, g) in fr:
                if fwd:
                    nb = [(y, gadd(g, h, mods)) for (y, h) in out[x]]
                else:
                    nb = [(xx, gadd(g, tuple(-a for a in h), mods)) for (y, xx), h in arcs.items() if y == x]
                for u in nb:
                    if u not in dist:
                        dist[u] = dist[(x, g)] + 1
                        nf.append(u)
            fr = nf
        return dist
    df = bfs((x0, one)); db = bfs((x0, one), False)
    n_hat = len(V) * len(C)
    res["H2"] = (len(df) == n_hat and len(db) == n_hat)
    # period of hat D and D
    r = 0
    for (x, g), dx in df.items():
        for (y, h) in out[x]:
            u = (y, gadd(g, h, mods))
            if u in df:
                r = math.gcd(r, dx + 1 - df[u])
    res["r"] = r
    # period of D
    dD = {x0: 0}; fr = [x0]
    while fr:
        nf = []
        for x in fr:
            for (y, h) in out[x]:
                if y not in dD:
                    dD[y] = dD[x] + 1; nf.append(y)
        fr = nf
    r0 = 0
    for x in dD:
        for (y, h) in out[x]:
            r0 = math.gcd(r0, dD[x] + 1 - dD[y])
    res["r0"] = r0
    C0 = sorted(g for g in C if (x0, g) in df and r and df[(x0, g)] % r == 0)
    res["C0_size"] = len(C0)
    res["index_matches_r_over_r0"] = (r0 != 0 and len(C) // max(len(C0), 1) == r // r0)
    # characters
    U = []
    devs = []
    mats = {}
    for k in C:
        A = np.zeros((len(V), len(V)), dtype=complex)
        for (y, x), g in arcs.items():
            A[idx[y], idx[x]] = chi(k, g, mods)
        dev = float(np.max(np.abs(A.conj().T @ A - d * np.eye(len(V)))))
        devs.append(dev)
        if dev < TOL:
            U.append(k); mats[k] = A / math.sqrt(d)
    good = [x for x in devs if x < TOL]; bad = [x for x in devs if x >= TOL]
    res["UD_size"] = len(U)
    res["dev_max_qualifying"] = max(good) if good else None
    res["dev_min_nonqualifying"] = min(bad) if bad else None
    res["H3"] = len(U) > 0
    res["qualifies"] = bool(res["H1"] and res["H2"] and res["H3"])
    if not res["qualifies"]:
        return res
    # classes of restrictions to C0 under inverse
    def restr(k):
        return tuple(round(chi(k, g, mods).real, 9) for g in C0) , tuple(round(abs(chi(k, g, mods).imag), 9) for g in C0)
    def key(k):
        a = tuple((round(chi(k, g, mods).real, 9), round(chi(k, g, mods).imag, 9)) for g in C0)
        b = tuple((re, -im + 0.0) for re, im in a)
        return min(a, b)
    classes = {}
    for k in U:
        classes.setdefault(key(k), []).append(k)
    cl = list(classes.values())
    res["n_classes"] = len(cl)
    res["class_sizes"] = [len(c) for c in cl]
    # exact walk counts
    n = len(V)
    M = [[0] * n for _ in range(n)]
    for (y, x) in arcs:
        M[idx[y]][idx[x]] = 1
    vec = [0] * n; vec[idx[x0]] = 1
    Nt = [1]; tot_ok = True; p1_fail = []
    allv = [vec]
    for t in range(1, T + 1):
        vec = [sum(M[i][j] * vec[j] for j in range(n) if M[i][j]) for i in range(n)]
        Nt.append(vec[idx[x0]])
        if sum(vec) != d ** t:
            tot_ok = False
        if vec[idx[x0]] * d > d ** t:
            p1_fail.append(t)
        if t in (1, 2, 3, 7, 50):
            allv.append(list(vec))
    res["total_walks_is_d^t"] = tot_ok
    res["P1_fail_t"] = p1_fail[:10]; res["P1"] = (len(p1_fail) == 0)
    res["max_N_t*d/d^t"] = float(max(Fraction(Nt[t] * d, d ** t) for t in range(1, T + 1)))
    cnt = [float(Fraction(Nt[t], d ** t)) for t in range(T + 1)]
    # unitary iteration
    w = {}
    full = {}
    for k in U:
        v = np.zeros(n, dtype=complex); v[idx[x0]] = 1
        ws = [1.0]; fl = {0: np.abs(v) ** 2}
        for t in range(1, T + 1):
            v = mats[k] @ v
            ws.append(abs(v[idx[x0]]) ** 2)
            if t in (1, 2, 3, 7, 50):
                fl[t] = np.abs(v) ** 2
        w[k] = np.array(ws); full[k] = fl
    res["unitary_norm_drift_bound"] = "T*nV*1e-15 = %.1e" % (T * n * 1e-15)
    # P3
    spread = 0.0
    for c in cl:
        for k in c[1:]:
            spread = max(spread, float(np.max(np.abs(w[k] - w[c[0]]))))
    res["P3_spread"] = spread; res["P3"] = spread < TOL
    reps = [c[0] for c in cl]
    # P0
    dev0 = 0.0
    for a in (0.0, 1 / 3, 1.0):
        for ti, t in enumerate((1, 2, 3, 7, 50)):
            cntv = np.array([float(Fraction(x, d ** t)) for x in allv[ti + 1]])
            tot = a * cntv.sum() + (1 - a) / len(reps) * sum(full[k][t].sum() for k in reps)
            dev0 = max(dev0, abs(tot - 1))
    res["P0_dev"] = dev0; res["P0"] = dev0 < TOL
    # P2, P5
    cntarr = np.array(cnt)
    p2 = {}; p5 = {}
    for a in (0.0, 1 / 3, 1.0):
        bound = 1 - a * (1 - 1 / d)
        mm = None; ok5 = True; best = []
        for k in reps:
            R = a * cntarr + (1 - a) * w[k]
            margin = float(np.min(bound - R[1:]))
            mm = margin if mm is None else min(mm, margin)
            tb = int(np.argmax(R[1:])) + 1
            eta = 1 - R[tb]
            ok5 = ok5 and (a <= eta * d / (d - 1) + TOL)
            best.append((tb, float(R[tb])))
        p2["%.4f" % a] = mm; p5["%.4f" % a] = {"ok": ok5, "best_t_R": best}
    res["P2_min_margin"] = p2; res["P2"] = all(m >= -TOL for m in p2.values())
    res["P5"] = all(v["ok"] for v in p5.values()); res["P5_detail"] = p5
    # a=0 largest R_t per class, and simultaneous
    res["a0_max_R_per_class"] = [(int(np.argmax(w[k][1:])) + 1, float(np.max(w[k][1:]))) for k in reps]
    sim = np.min(np.array([w[k] for k in reps]), axis=0)
    res["P4_sim_max_t1000_2000"] = float(np.max(sim[1000:])); res["P4"] = res["P4_sim_max_t1000_2000"] >= 0.99
    res["P4_sim_max_all_t>=1"] = (int(np.argmax(sim[1:])) + 1, float(np.max(sim[1:])))
    # P6
    zeros = [t for t in range(1, 61) if Nt[t] == 0]
    res["P6_t<=60_with_N_t=0"] = zeros[:30]
    res["a1_max_R"] = float(max(cnt[1:]))
    return res


def Z(n):
    return (n,)


def from_matrix(E, x0=0):
    """E[y][x] = gain exponent tuple or None."""
    V = list(range(len(E)))
    arcs = {(y, x): E[y][x] for y in V for x in V if E[y][x] is not None}
    return V, arcs, x0


def coined_ring(n, lazy=False):
    """vertices (x,c); arc (x,c)->(x+1,0) gain H[0][c], (x-1,1) gain H[1][c]; H=[[1,1],[1,-1]] over Z2.
    lazy: second target is (x,1) instead (loop at (x,1) with gain -1)."""
    V = [(x, c) for x in range(n) for c in (0, 1)]
    arcs = {}
    for x in range(n):
        for c in (0, 1):
            arcs[(((x + 1) % n, 0), (x, c))] = (0,)
            tgt = (x, 1) if lazy else ((x - 1) % n, 1)
            arcs[(tgt, (x, c))] = (1,) if c == 1 else (0,)
    return V, arcs


def kron(E1, m1, E2, m2):
    """product carrier with gains in Z_m1 x Z_m2."""
    n1, n2 = len(E1), len(E2)
    E = [[None] * (n1 * n2) for _ in range(n1 * n2)]
    for a in range(n1):
        for b in range(n1):
            for c in range(n2):
                for e in range(n2):
                    if E1[a][b] is not None and E2[c][e] is not None:
                        E[a * n2 + c][b * n2 + e] = (E1[a][b][0], E2[c][e][0])
    return E


H = [[(0,), (0,)], [(0,), (1,)]]
carriers = []
V, arcs, x0 = from_matrix(H); carriers.append(("hadamard2_Z2_loop_at_x0", V, arcs, (2,), x0))
V, arcs, x0 = from_matrix(H, 1); carriers.append(("hadamard2_Z2_x0=1_loop_gain-1", V, arcs, (2,), x0))
for n in (3, 4, 5, 6):
    V, arcs = coined_ring(n); carriers.append(("coined_ring_%d" % n, V, arcs, (2,), (0, 0)))
V, arcs = coined_ring(4, lazy=True); carriers.append(("lazy_ring_4_loop_at_x0", V, arcs, (2,), (0, 1)))
F3 = [[((j * k) % 3,) for k in range(3)] for j in range(3)]
V, arcs, x0 = from_matrix(F3); carriers.append(("fourier3_Z3_deg3", V, arcs, (3,), x0))
F5 = [[((j * k) % 5,) for k in range(5)] for j in range(5)]
V, arcs, x0 = from_matrix(F5); carriers.append(("fourier5_Z5_two_classes", V, arcs, (5,), x0))
Z8 = [[(1,), (1,)], [(1,), (5,)]]
V, arcs, x0 = from_matrix(Z8); carriers.append(("zeta_hadamard_Z8_r4", V, arcs, (8,), x0))
K4 = [[(1, 0), (1, 0)], [(1, 0), (1, 1)]]
V, arcs, x0 = from_matrix(K4); carriers.append(("a(1,1;1,b)_Z2xZ2", V, arcs, (2, 2), x0))
V, arcs, x0 = from_matrix(kron(F3, 3, H, 2)); carriers.append(("fourier3_x_hadamard_Z3xZ2_deg6", V, arcs, (3, 2), x0))
F4 = [[((j * k) % 4,) for k in range(4)] for j in range(4)]
V, arcs, x0 = from_matrix(F4); carriers.append(("fourier4_Z4", V, arcs, (4,), x0))
# deliberately non-qualifying (kept): all-ones 2x2, and the 3-vertex example of the paper's text
V, arcs, x0 = from_matrix([[(0,), (0,)], [(0,), (0,)]]); carriers.append(("allones2_Z2_NONQUAL", V, arcs, (2,), x0))
E3 = [[None, None, (0,)], [(0,), (0,), None], [(0,), (1,), (0,)]]
V, arcs, x0 = from_matrix(E3); carriers.append(("three_vertex_count_only_NONQUAL", V, arcs, (2,), x0))

results = [analyse(*c) for c in carriers]

# counterexample search C1/C2
random.seed(11)
def maxratio(succ, d, tmax=14):
    n = len(succ); worst = Fraction(0); arg = None
    for x0 in range(n):
        vec = [0] * n; vec[x0] = 1
        for t in range(1, tmax + 1):
            nv = [0] * n
            for x in range(n):
                if vec[x]:
                    for y in succ[x]:
                        nv[y] += vec[x]
            vec = nv
            q = Fraction(vec[x0] * d, d ** t)
            if q > worst:
                worst = q; arg = (x0, t)
    return worst, arg
c1 = {"tested": 0, "violations": 0, "max_ratio_N_t*d/d^t": 0.0}
def test_simple(succ, d):
    c1["tested"] += 1
    q, arg = maxratio(succ, d)
    if q > 1:
        c1["violations"] += 1; c1.setdefault("examples", []).append((succ, arg))
    c1["max_ratio_N_t*d/d^t"] = max(c1["max_ratio_N_t*d/d^t"], float(q))
for n in (2, 3):
    opts = list(itertools.combinations(range(n), 2))
    for choice in itertools.product(opts, repeat=n):
        test_simple([list(c) for c in choice], 2)
for _ in range(3000):
    d = random.choice((2, 3, 4)); n = random.randint(d, 6)
    test_simple([random.sample(range(n), d) for _ in range(n)], d)
c2 = {"tested": 0, "violations": 0, "max_ratio": 0.0}
for _ in range(500):
    d = random.choice((2, 3)); n = random.randint(d, 5)
    succ = [random.sample(range(n), d) for _ in range(n)]
    x = random.randrange(n); succ[x] = [x, x] + succ[x][2:]  # two parallel loops: hypothesis violated
    c2["tested"] += 1
    q, arg = maxratio(succ, d)
    if q > 1:
        c2["violations"] += 1; c2.setdefault("example", (succ, arg, float(q)))
    c2["max_ratio"] = max(c2["max_ratio"], float(q))

summary = {
    "carriers_total": len(results),
    "carriers_qualifying": sum(1 for r in results if r["qualifies"]),
    "nonqualifying": [(r["name"], r.get("H1"), r.get("H2"), r.get("H3")) for r in results if not r["qualifies"]],
}
for p in ("P0", "P1", "P2", "P3", "P4", "P5"):
    q = [r for r in results if r["qualifies"]]
    summary[p] = {"met": sum(1 for r in q if r[p]), "failed": [r["name"] for r in q if not r[p]]}
out = {"summary": summary, "C1_simple_digraphs": c1, "C2_parallel_arcs_hypothesis_violated": c2, "carriers": results}
with open(OUT, "x") as f:
    json.dump(out, f, indent=1, default=str)
print(json.dumps(summary, indent=1))
print("C1", {k: v for k, v in c1.items() if k != "examples"}); print("C2", c2)
for r in results:
    if r["qualifies"]:
        print(r["name"], "d", r["d"], "r", r["r"], "r0", r["r0"], "|C0|", r["C0_size"], "|U|", r["UD_size"], "classes", r["n_classes"],
              "loop", r["loop_at_x0"], "| P2 margins", {k: "%.3g" % v for k, v in r["P2_min_margin"].items()},
              "| a0 max", r["a0_max_R_per_class"], "| sim", "%.6f" % r["P4_sim_max_t1000_2000"], "| a1 max", r["a1_max_R"],
              "| zeros", r["P6_t<=60_with_N_t=0"][:8], "| spread %.1e" % r["P3_spread"], "| P0dev %.1e" % r["P0_dev"],
              "| sep", r["dev_max_qualifying"], r["dev_min_nonqualifying"])
    else:
        print(r["name"], "NONQUAL", {k: r.get(k) for k in ("H1", "H2", "H3", "UD_size", "r")})
