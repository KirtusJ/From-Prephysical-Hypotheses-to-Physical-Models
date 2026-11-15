"""Kill tests KZ3 to KZ6 of the candidate sprint of 15 November 2026. The predicates are those of 00_PLAN.md,
committed before this program was written (commit of the plan precedes this file). Exact arithmetic throughout.
Usage: python3 kill_tests.py REPO_ROOT RESULT.json   (refuses to overwrite). Seed 20261115 for KZ6(a)."""
import sys, os, json, math, random, itertools, collections
from fractions import Fraction as Fr
ROOT, OUT = sys.argv[1], sys.argv[2]; assert not os.path.exists(OUT)
rep = {"argv": sys.argv[1:], "seed": 20261115}

# ---------- KZ3: count rule against the blank run of the cesium walk
d = json.load(open(os.path.join(ROOT, "Director_G/results/cesium_negative_read.json")))
blank = d["digitized"][0]["counts"]; a, b = blank["-1"], blank["1"]; n = a + b
tail = sum(math.comb(n, k) for k in range(n + 1) if abs(k - n / 2) >= abs(a - n / 2))
p = Fr(tail, 2 ** n)
rep["KZ3"] = {"counts_at_minus1_plus1": [a, b], "all_blank_counts": {k: v for k, v in blank.items() if v}, "two_sided_binomial_p": float(p),
              "p_exact_numerator_over_2^n": [tail, n], "predicate_p_below_1e-6": p < Fr(1, 10 ** 6), "verdict": "KILLED" if p < Fr(1, 10 ** 6) else "STANDS"}

# ---------- walks on the ring with the sign carrier (gain -1 on L after L), tracked by level
def field(N, T, masks=None):
    st = collections.Counter({(0, 0, 0, 0): 1})   # (site, rail, lam, sign) -> count
    for t in range(1, T + 1):
        new = collections.Counter()
        for (x, r, l, s), c in st.items():
            y = (x + 1) % N
            if masks is None or y in masks[t - 1]: new[(y, 0, l, s)] += c
            y = (x - 1) % N
            if masks is None or y in masks[t - 1]: new[(y, 1, l + 1, s ^ (1 if r == 1 else 0))] += c
        st = new
    return st
def levels(N, T, masks=None):
    M = N // 2 if N % 2 == 0 else N
    out = collections.defaultdict(lambda: collections.defaultdict(int))   # vertex -> lam -> signed sum
    for (x, r, l, s), c in field(N, T, masks).items(): out[(x, r)][l] += c * (-1) ** s
    return M, out

# ---------- KZ4: a lap map L with psi_{j+1} = L psi_j ?
def solve_consistent(pairs, dim):
    # unknown L (dim x dim); each pair gives dim equations; rows of L decouple: for each output coordinate i,
    # sum_k L[i][k] a[k] = b[i] over all pairs. Consistent iff rank([A]) == rank([A|b_i]) for every i.
    A = [list(map(Fr, a)) for a, _ in pairs]
    def rank(Mx):
        Mx = [r[:] for r in Mx]; rk = 0
        for c in range(len(Mx[0])):
            pv = next((i for i in range(rk, len(Mx)) if Mx[i][c] != 0), None)
            if pv is None: continue
            Mx[rk], Mx[pv] = Mx[pv], Mx[rk]
            for i in range(len(Mx)):
                if i != rk and Mx[i][c] != 0:
                    f = Mx[i][c] / Mx[rk][c]; Mx[i] = [x - f * y for x, y in zip(Mx[i], Mx[rk])]
            rk += 1
        return rk
    rA = rank(A)
    bad = [i for i in range(dim) if rank([r + [Fr(b[i])] for r, (_, b) in zip(A, pairs)]) != rA]
    return rA, bad
rep["KZ4"] = {"rings": []}
for N in (4, 6, 8):
    M = N // 2; verts = [(x, r) for x in range(N) for r in (0, 1)]; pairs = []
    for T in (6 * M, 6 * M + 2, 6 * M + 4):
        _, lv = levels(N, T)
        lams = sorted({l for v in lv for l in lv[v]})
        # a level = a residue class structure: walks at vertex v with lam = base_v + j*M; index levels by lifted position
        # psi_j(v): lifted position T - 2*lam; level j <-> winding number (T - 2*lam - x)/N with x in 0..N-1
        byj = collections.defaultdict(lambda: [0] * len(verts))
        for vi, (x, r) in enumerate(verts):
            for l, val in lv.get((x, r), {}).items():
                w = (T - 2 * l - x) // N; assert (T - 2 * l - x) % N == 0
                byj[w][vi] = val
        js = sorted(byj)
        for j in js:
            if j + 1 in byj and any(byj[j]) and any(byj[j + 1]): pairs.append((byj[j], byj[j + 1]))
    rA, bad = solve_consistent(pairs, len(verts))
    rep["KZ4"]["rings"].append({"N": N, "pairs": len(pairs), "rank_of_inputs": rA, "inconsistent_output_coordinates": len(bad), "consistent": not bad})
rep["KZ4"]["predicate_consistent_on_some_ring"] = any(r["consistent"] for r in rep["KZ4"]["rings"])
rep["KZ4"]["verdict"] = "STANDS" if rep["KZ4"]["predicate_consistent_on_some_ring"] else "KILLED"

# ---------- two classes: carrier with gains in Z2 x Z4 on the ring of N sites (a = 0, b = (0,1), c = 0, d = (1,1))
def add(g, h): return ((g[0] + h[0]) % 2, (g[1] + h[1]) % 4)
GA, GB, GC, GD = (0, 0), (0, 1), (0, 0), (1, 1)
def eps(N, T, masks=None):
    st = collections.Counter({(0, 0, (0, 0)): 1})
    for t in range(1, T + 1):
        new = collections.Counter()
        for (x, r, g), c in st.items():
            y = (x + 1) % N
            if masks is None or y in masks[t - 1]: new[(y, 0, add(g, GA if r == 0 else GC))] += c
            y = (x - 1) % N
            if masks is None or y in masks[t - 1]: new[(y, 1, add(g, GB if r == 0 else GD))] += c
        st = new
    out = {}
    for (x, r, g), c in st.items():
        e = out.setdefault((x, r), {})
        e[g] = e.get(g, 0) + c
    res = {}
    for v, m in out.items():
        base = min(g[1] for g in m) % 2          # second coordinate is constant modulo 2 at a vertex (checked)
        assert all(g[1] % 2 == base for g in m)
        e = [0, 0]
        for g, c in m.items(): e[((g[1] - base) // 2) % 2] += c * (-1) ** g[0]
        res[v] = (e[0], e[1], sum(m.values()))
    return res
def check_s2(N):
    M = N // 2; B = (0, 1); beta = (0, M % 4); return beta == (0, 2)   # s = 2, k even needs beta = (0,2): M = 2 mod 4
plus = lambda e: (e[0] + e[1]) ** 2
minus = lambda e: (e[0] - e[1]) ** 2
blind = lambda e: e[0] ** 2 + e[1] ** 2

# ---------- KZ5: multiplicativity of the lap-blind rule with the paper's product formula (each square multiplies)
rep["KZ5"] = {"cases": []}; fails = 0; tot = 0; first = None
for N, T in ((4, 4), (4, 6)):
    assert check_s2(N)
    E = eps(N, T)
    for v, w in itertools.product(E, E):
        tot += 1
        mu_prod = Fr(plus(E[v]) * plus(E[w]) + minus(E[v]) * minus(E[w]), 2)       # same formula on the product
        mu_mu = Fr(blind(E[v]) * blind(E[w]))
        if mu_prod != mu_mu:
            fails += 1
            if first is None: first = {"N": N, "T": T, "v": v, "w": w, "eps_v": E[v][:2], "eps_w": E[w][:2], "product_formula": str(mu_prod), "product_of_weights": str(mu_mu)}
rep["KZ5"].update({"pairs": tot, "failures": fails, "first_failure": first, "predicate_equal_in_every_pair": fails == 0, "verdict": "STANDS" if fails == 0 else "KILLED"})

# ---------- KZ6: odd-lap square: (a) consistency, (b) multiplicativity, (c) the fork
rng = random.Random(20261115); a_fail = 0; a_events = 0
for N in (4, 12):
    assert check_s2(N)
for N in (4, 12):
    for _ in range(300 if N == 4 else 60):
        T = rng.randint(2, 3 * N if N == 4 else 14); p = rng.choice([0.5, 0.7, 0.9])
        masks = [{x for x in range(N) if rng.random() < p} for _ in range(T + 1)]
        mu = lambda L: sum(minus(e) for e in eps(N, L, masks[:L]).values())
        m1 = mu(T); 
        if not eps(N, T, masks[:T]): continue
        m2 = sum(minus(e) for e in eps(N, T + 1, masks[:T] + [set(range(N))]).values())
        a_events += 1
        if m2 != 2 * m1: a_fail += 1
b_fail = 0; b_tot = 0
for N, T in ((4, 4), (4, 6)):
    E = eps(N, T)
    for v, w in itertools.product(E, E):
        b_tot += 1     # same formula on the product: the square of the product character is the product of the squares
        # checked from the definition: signed class sums of the product multiset
        e0 = E[v][0] * E[w][0] + E[v][1] * E[w][1]; e1 = E[v][0] * E[w][1] + E[v][1] * E[w][0]
        if (e0 - e1) ** 2 != minus(E[v]) * minus(E[w]): b_fail += 1
c_rows = []; c_fail = 0
for N in (4, 12, 20):          # rings with s = 2, k even for this carrier: M = 2 mod 4
    assert check_s2(N); M = N // 2
    masks = [{t % N, (-t) % N} for t in range(1, M + 1)] + [set(range(N))]
    E = eps(N, M + 1, masks)
    w = Fr(sum(minus(e) for e in E.values()), 1)
    per_vertex = {str(v): minus(e) for v, e in E.items()}
    pred = 2 + 2 * (-1) ** (M - 1) * (-1)     # times 2^-(M+1), summed over the two fork ports: see note
    c_rows.append({"N": N, "M": M, "weights_at_vertices_times_2^(M+1)": per_vertex, "sum": str(w)})
rep["KZ6"] = {"a_events": a_events, "a_failures": a_fail, "b_pairs": b_tot, "b_failures": b_fail, "c_rows": c_rows,
              "note": "this carrier has s = 2 with k even only for M = 2 mod 4, so the rings of the plan (N = 6, 8, 10, 12, 14) are replaced by N = 4, 12, 20; the fork weights are listed per vertex for comparison with the plan's formula"}
json.dump(rep, open(OUT, "x"), indent=1, default=str)
print(json.dumps({k: (v.get("verdict") if isinstance(v, dict) else v) for k, v in rep.items() if k.startswith("KZ")}))
print(rep["KZ3"]["counts_at_minus1_plus1"], rep["KZ3"]["two_sided_binomial_p"]); print(rep["KZ4"]["rings"]); print(rep["KZ5"]["failures"], rep["KZ5"]["pairs"], rep["KZ5"]["first_failure"]); print(rep["KZ6"]["a_events"], rep["KZ6"]["a_failures"], rep["KZ6"]["b_failures"]); [print(r) for r in c_rows]
