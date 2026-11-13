"""return_times.py -- Attack B(iii),(iv) on S5 of candidate model Z1.  Exact integers / rationals.

Signed ring of N sites (as in alt_rules.py), x0 = (0,R), A the signed step matrix, U = A/sqrt2.
Model return weight R_t = ((A^t)_{x0,x0})^2 / 2^t.  "R_t > 0.99" is tested as 100*num > 99*2^t (integers).
TMAX = 100000 (a budget, no other basis).

Predicates fixed before the first run:
Q1  N = 4: first t >= 1 with R_t = 1 is 8;  N = 8: it is 24  (the candidate's claim).
Q2  for N in 3..12, N not in {4,8}: no t in 1..TMAX has R_t = 1.
Q3  certificate of "never": for N not in {4,8} the minimal polynomial over Q of U^2 = A^2/2 relative to e_x0
    has a coefficient that is not an integer.  (If R_t = 1 then A^t e = +-2^(t/2) e, so (U^2)^t e = e, so that
    polynomial divides x^t - 1 and is monic with integer coefficients.)  For N in {4,8} it has integer coefficients.
Q4  for every N in 3..12 a first t with R_t > 0.99 exists in 1..TMAX (reported; failures kept).
Q5  intermediate records: on N = 4, t = 8 and N = 8, t = 24, the return weight when the end vertex is also
    recorded at the midpoint s = t/2,  sum_z |U^s_{x0 z}|^2 |U^s_{z x0}|^2, is < 1, and the return weight when
    it is recorded at every step, N_t/2^t, is <= 1/2.  Both reported exactly.
Q6  no joint distribution: on N = 8 the weights of the classes "at y at length 2 and at z at length 3"
    (subsets of walks of length 3) summed over y do not give P_3(z) for some z (reported).
Result file not overwritten.
"""
import sys, os, json
from fractions import Fraction as Fr
from flint import fmpq_mat, fmpq
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "return_times_result.json")
if os.path.exists(OUT): sys.exit("result exists; refusing to overwrite")
TMAX = 100000
def carrier(N):
    V = [(x, c) for x in range(N) for c in "RL"]; idx = {v: i for i, v in enumerate(V)}
    succ = []
    for v in V:
        x, c = v
        succ.append([(idx[((x+1) % N, "R")], 1), (idx[((x-1) % N, "L")], -1 if c == "L" else 1)])
    return V, idx, succ
def step(vec, succ):
    out = [0]*len(vec)
    for y, val in enumerate(vec):
        if val:
            for z, s in succ[y]: out[z] += s*val
    return out
res = {"TMAX": TMAX, "N": {}}
for N in range(3, 13):
    V, idx, succ = carrier(N); n = len(V); x0 = idx[(0, "R")]
    vec = [0]*n; vec[x0] = 1; first1 = None; first99 = None; best = (Fr(0), 0)
    for t in range(1, TMAX+1):
        vec = step(vec, succ); num = vec[x0]*vec[x0]
        if first99 is None and 100*num > 99 << t: first99 = t
        if first1 is None and num == 1 << t: first1 = t
        if first1 is not None and first99 is not None: break
    # relative minimal polynomial of A^2/2 at e_x0 via Krylov vectors
    K = []; w = [Fr(0)]*n; w[x0] = Fr(1); K.append(w)
    def app(w):
        a = step(step(w, succ), succ); return [Fr(x)/2 for x in a]
    coeffs = None
    for k in range(1, n+1):
        w = app(K[-1])
        M = fmpq_mat(n, k, [fmpq(K[j][i].numerator, K[j][i].denominator) for i in range(n) for j in range(k)])
        if M.rank() == k:
            b = fmpq_mat(n, 1, [fmpq(x.numerator, x.denominator) for x in w])
            aug = fmpq_mat(n, k+1, [ (M[i, j] if j < k else b[i, 0]) for i in range(n) for j in range(k+1)])
            if aug.rank() == k:
                # solve M c = w  using a full-rank row selection through rref
                R, rk = aug.rref()
                c = [None]*k
                for i in range(k):
                    piv = next(j for j in range(k) if R[i, j] != 0); c[piv] = R[i, k]
                coeffs = [str(-x) for x in c] + ["1"]   # x^k - sum c_j x^j
                break
        K.append(w)
    integral = all("/" not in s for s in coeffs)
    res["N"][N] = dict(first_exact=first1, first_above_099=first99, relminpoly_U2_low_to_high=coeffs, relminpoly_integral=integral)
    print(N, first1, first99, integral, coeffs, flush=True)
RN = res["N"]
pred = {
 "Q1": RN[4]["first_exact"] == 8 and RN[8]["first_exact"] == 24,
 "Q2": all(RN[N]["first_exact"] is None for N in RN if N not in (4, 8)),
 "Q3": all(RN[N]["relminpoly_integral"] == (N in (4, 8)) for N in RN),
 "Q4": all(RN[N]["first_above_099"] is not None for N in RN),
}
# Q5, Q6
def powvec(N, start, t):
    V, idx, succ = carrier(N); vec = [0]*len(V); vec[start] = 1
    for _ in range(t): vec = step(vec, succ)
    return vec
q5 = {}
for N, t in ((4, 8), (8, 24)):
    V, idx, succ = carrier(N); x0 = idx[(0, "R")]; s = t//2
    fwd = powvec(N, x0, s)
    mid = sum(Fr(fwd[z]**2, 2**s)*Fr(powvec(N, z, s)[x0]**2, 2**s) for z in range(len(V)) if fwd[z])
    cnt = [0]*len(V); cnt[x0] = 1
    for _ in range(t):
        o = [0]*len(V)
        for y, val in enumerate(cnt):
            for z, _s in succ[y]: o[z] += val
        cnt = o
    q5[N] = dict(t=t, midpoint_recorded=str(mid), every_step_recorded=str(Fr(cnt[x0], 2**t)), coherent="1")
    pred_ok = mid < 1 and Fr(cnt[x0], 2**t) <= Fr(1, 2)
    q5[N]["ok"] = pred_ok
pred["Q5"] = all(v["ok"] for v in q5.values()); res["Q5"] = q5
V, idx, succ = carrier(8); x0 = idx[(0, "R")]
v2 = powvec(8, x0, 2); v3 = powvec(8, x0, 3)
q6 = {}
for z in range(len(V)):
    tot = Fr(0)
    for y in range(len(V)):
        for zz, s in succ[y]:
            if zz == z and v2[y]: tot += Fr((s*v2[y])**2, 8)
    if tot or v3[z]: q6[str(V[z])] = dict(sum_over_y_of_joint=str(tot), P3=str(Fr(v3[z]**2, 8)))
res["Q6"] = q6; pred["Q6"] = any(v["sum_over_y_of_joint"] != v["P3"] for v in q6.values())
res["predicates"] = pred
json.dump(res, open(OUT, "x"), indent=1)
print(pred); print(q5); print(q6)
