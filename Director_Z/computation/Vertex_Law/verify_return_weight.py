#!/usr/bin/env python3
"""Check for paper G10, Corollary on recurrence (edition Z23).  Claim under test, fixed before the run.
Carrier D: finite gain digraph, at most one arc per ordered pair, exactly d >= 2 outgoing arcs at every vertex, derived digraph
strongly connected, and a character psi with A^(psi)* A^(psi) = d (hypothesis H, tested per carrier; carriers failing it are listed).
Rule mu(S) = a|S| + (1-a) ||v^psi_S||^2 with 0 <= a <= 1.  S_t = all walks of length t from x0 that end at x0;
R_t = mu(S_t)/d^t = a N_t/d^t + (1-a) |(U^t)_{x0 x0}|^2, with N_t the number of such walks and U = A^(psi)/sqrt(d).
Predicates:
 R1  N_t/d^t <= 1/d for every t = 1..T (exact integers);
 R2  U is unitary to 1e-12 (so |(U^t)_{x0x0}| <= 1), and hence R_t <= 1 - a(1 - 1/d) for t = 1..T and a in {0, 1/4, 1/2, 1}
     (checked with a float margin of 1e-9, the basis being accumulated rounding in T matrix products of size at most 16);
 R3  for a = 0 some t in 1..T has R_t >= 0.99 (recurrence of a finite unitary); if none is found in range the carrier is
     reported as "not reached in range", which is not a failure of the claim (the claim is about limsup) but is listed;
 R4  for a = 1/4, 1/2, 1 the largest R_t over t = 1..T is at most 1 - a(1 - 1/d) and so stays below 1 by at least a(1-1/d).
Carriers: two vertices [[1,1],[1,-1]] over C_2; B_q for q = 4, 6, 8, 12; signed arc digraph of rings N = 3, 4, 5, 6, 8;
the Fourier block of degree 3 on three vertices over C_3; twelve seeded random carriers kept only if H holds.
Writes Return_Weight_Results.json; refuses to overwrite.  Seed fixed."""
import cmath, json, math, os, sys, random
import numpy as np
OUT = "Return_Weight_Results.json"
if os.path.exists(OUT): sys.exit("refusing to overwrite " + OUT)
T = 4000; SEED = 20261123; random.seed(SEED)
def carrier_matrix(n, q, arcs):       # arcs: (tail, head, exponent)
    z = cmath.exp(2j * math.pi / q)
    A = np.zeros((n, n), dtype=complex); C = np.zeros((n, n), dtype=object)
    for y, x, k in arcs: A[x, y] = z ** k; C[x, y] = 1
    return A, C
def derived_strong(n, q, arcs):
    nodes = [(v, g) for v in range(n) for g in range(q)]
    out = {u: [] for u in nodes}; inn = {u: [] for u in nodes}
    for y, x, k in arcs:
        for g in range(q): out[(y, g)].append((x, (g + k) % q)); inn[(x, (g + k) % q)].append((y, g))
    def reach(adj):
        seen = {(0, 0)}; st = [(0, 0)]
        while st:
            u = st.pop()
            for w in adj[u]:
                if w not in seen: seen.add(w); st.append(w)
        return len(seen) == len(nodes)
    return reach(out) and reach(inn)
def ring(N):
    idx = lambda x, s: 2 * (x % N) + s        # s = 0 for R, 1 for L
    arcs = []
    for x in range(N):
        for s in (0, 1):
            arcs.append((idx(x, s), idx(x + 1, 0), 0)); arcs.append((idx(x, s), idx(x - 1, 1), 1 if s == 1 else 0))
    return 2 * N, 2, arcs
cars = {"two_vertex_C2": (2, 2, [(0, 0, 0), (0, 1, 0), (1, 0, 0), (1, 1, 1)])}
for q in (4, 6, 8, 12): cars[f"B_{q}"] = (2, q, [(0, 0, 0), (0, 1, 0), (1, 0, 1), (1, 1, (1 + q // 2) % q)])
for N in (3, 4, 5, 6, 8): cars[f"ring_{N}"] = ring(N)
cars["fourier3_C3"] = (3, 3, [(y, x, (x * y) % 3) for y in range(3) for x in range(3)])
for i in range(12):
    n = random.choice([2, 3, 4]); q = random.choice([2, 3, 4]); d = 2
    arcs = []
    for y in range(n):
        for x in random.sample(range(n), d): arcs.append((y, x, random.randrange(q)))
    cars[f"random_{i}"] = (n, q, arcs)
R = {"seed": SEED, "T": T, "carriers": {}, "not_qualifying": []}
allok = {"R1": True, "R2": True, "R4": True}; reached = 0; qual = 0
for name, (n, q, arcs) in cars.items():
    A, Cn = carrier_matrix(n, q, arcs)
    dset = {sum(1 for a in arcs if a[0] == y) for y in range(n)}
    pairs_ok = len({(a[0], a[1]) for a in arcs}) == len(arcs)
    d = dset.pop() if len(dset) == 1 else None
    H = pairs_ok and d is not None and d >= 2 and derived_strong(n, q, arcs) and np.allclose(A.conj().T @ A, d * np.eye(n), atol=1e-12)
    if not H: R["not_qualifying"].append(name); continue
    qual += 1
    U = A / math.sqrt(d); unit = float(np.max(np.abs(U.conj().T @ U - np.eye(n))))
    Nt = [[int(v) for v in row] for row in Cn]; P = [row[:] for row in Nt]; cnt_ratio_max = 0.0; r1 = True
    Ut = U.copy(); best0 = (0.0, 0); maxR = {a: 0.0 for a in (0.25, 0.5, 1.0)}; r2 = unit < 1e-12
    for t in range(1, T + 1):
        if t > 1:
            P = [[sum(Nt[i][k] * P[k][j] for k in range(n)) for j in range(n)] for i in range(n)]; Ut = U @ Ut
        num = P[0][0]; r1 = r1 and num * d <= d ** t
        coh = abs(Ut[0, 0]) ** 2; cr = num / d ** t; cnt_ratio_max = max(cnt_ratio_max, cr)
        if coh > best0[0]: best0 = (float(coh), t)
        for a in maxR:
            Rt = a * cr + (1 - a) * coh; maxR[a] = max(maxR[a], Rt); r2 = r2 and Rt <= 1 - a * (1 - 1 / d) + 1e-9
        r2 = r2 and coh <= 1 + 1e-9
    r4 = all(maxR[a] <= 1 - a * (1 - 1 / d) + 1e-9 for a in maxR)
    reached += best0[0] >= 0.99
    allok["R1"] &= r1; allok["R2"] &= r2; allok["R4"] &= r4
    R["carriers"][name] = dict(vertices=n, order=q, degree=d, unitarity_defect=unit, largest_count_ratio=cnt_ratio_max, R1=bool(r1), R2=bool(r2), R4=bool(r4),
                               best_coherent_return=best0[0], at_t=best0[1], R3_reached=bool(best0[0] >= 0.99),
                               largest_R_for_a={str(a): maxR[a] for a in maxR}, bound_for_a={str(a): 1 - a * (1 - 1 / d) for a in maxR})
R["summary"] = dict(carriers=len(cars), qualifying=qual, R1=bool(allok["R1"]), R2=bool(allok["R2"]), R4=bool(allok["R4"]), R3_reached_in_range=int(reached), R3_not_reached=int(qual - reached))
json.dump(R, open(OUT, "w"), indent=1); print(json.dumps(R["summary"])); print("not qualifying:", R["not_qualifying"])
for k, v in R["carriers"].items(): print(k, "count max", round(v["largest_count_ratio"], 4), "coherent best", round(v["best_coherent_return"], 5), "at", v["at_t"], "R(1/2) max", round(v["largest_R_for_a"]["0.5"], 4))
