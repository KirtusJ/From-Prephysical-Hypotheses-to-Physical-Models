#!/usr/bin/env python3
"""Challenger + micro-review program for G10 Propositions 6.1 (prop:exact) and 6.2 (prop:local).
Paper text only.

Conventions.  Ring of N sites; vertex index 2*x + s, s = 0 for R, 1 for L.  Arcs (x,s) -> (x+1,R)
gain +1; (x,R) -> (x-1,L) gain +1; (x,L) -> (x-1,L) gain -1.  A[target, source]; U = A/sqrt 2.
(T psi)(x,s) = psi(x-1,s) (translation by one site to the right).  M_m multiplies by m(x).
"U M_m" applies M_m first.  Angles are in units of pi and exact (fractions) in the second part.
Float tolerance TOL = 1e-12 for entries of 2N x 2N matrices with entries of modulus <= 1 built from
at most 3 products (rounding < 1e-15).

PREDICATES (fixed before the first run):
 E0  U is unitary and commutes with T (N = 4, 6, 12), within TOL.
 E1  T M_m T^-1 = M_{m(.-1)} with the stated convention, within TOL, for a random m.
 E2  exhaustive, (N, q) in ((4,2), (4,4), (6,2), (6,3), (6,6), (5,5), (4,8)): over ALL m: Z_N -> q-th roots,
     the set {m : exists lambda with T U M_m T^-1 = lambda U M_m} (lambda taken as the (0,0)-ratio and
     the identity tested on the whole matrix within TOL) equals the set {m : m(x-1)/m(x) is the same
     for all x in Z_N, indices mod N}.  Count both.
 E3  for every m in that set: lambda is a q-th root of unity, lambda^N = 1, m(x) = m(0) lambda^(-x),
     and the order of lambda divides q (so a translation by 2 pi/n needs n | q, in particular q >= n).
 E4  micro boundary: (a) constant m: lambda = 1; (b) N-periodicity: on the ring the linear gain with
     lambda^N != 1 is not a function on Z_N (the proposition's "m(x) = m(0) lambda^-x" needs lambda^N = 1
     on a ring) - recorded as a wording remark, check that no m in E2 has lambda^N != 1;
     (c) a staircase (blocks of 2 sites, N = 12, q = 3) is not in the set; (d) lambda = -1, q = 2, N even.
 E5  quasi-momentum: for m(x) = exp(-i Phi x), Phi = 2 pi/N * r: lambda = exp(+i Phi) with the above
     convention (sign recorded, not asserted by the paper).
 S0  spectrum of U on rings N = 64, 256, 1024: all eigenphases theta satisfy |theta| <= pi/4 or
     |theta - pi| <= pi/4 (within 1e-9, eigenvalue rounding of a normal matrix ~ 1e-13), and the
     largest |theta| in the first arc tends to pi/4: recorded distance pi/4 - max.
 S1  exact arithmetic: with Sigma = [-1/4, 1/4] U [3/4, 5/4] (units of pi, closed arcs) and
     I_q = intersection over j of (Sigma + 2j/q): I_1 = I_2 = Sigma; I_4 = {1/4, 3/4, 5/4, 7/4} exactly;
     I_q empty for q = 3 and 5 <= q <= 200.  Method: I_q is a finite union of closed arcs and points
     whose end points are among the rotated end points; membership is tested exactly at every rotated
     end point and at every midpoint between cyclically consecutive distinct end points.
 S2  micro boundary: (a) q = 4: the four points are band edges (end points of Sigma) and no midpoint
     is in I_4; (b) q = 8 and q = 12: empty although 4 | q; (c) with OPEN bands the q = 4 intersection
     would be empty (recorded: the statement depends on Sigma being closed); (d) q = 6: empty.
Seed 20261113.  Result file challenge_prop_exact_prop_local_results.json, never overwritten.
"""
import json, os, sys, itertools, cmath, math
from fractions import Fraction as Fr
import numpy as np
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "challenge_prop_exact_prop_local_results.json")
if os.path.exists(OUT): sys.exit("result file exists; refusing to overwrite")
rng = np.random.default_rng(20261113); TOL = 1e-12
def step(N):
    A = np.zeros((2 * N, 2 * N), complex)
    for x in range(N):
        for s in (0, 1):
            A[2 * ((x + 1) % N) + 0, 2 * x + s] = 1
            A[2 * ((x - 1) % N) + 1, 2 * x + s] = -1 if s == 1 else 1
    return A / math.sqrt(2)
def trans(N):
    T = np.zeros((2 * N, 2 * N))
    for x in range(N):
        for s in (0, 1): T[2 * ((x + 1) % N) + s, 2 * x + s] = 1
    return T
def Mm(m): return np.diag(np.repeat(np.asarray(m, complex), 2))
res = dict(seed=20261113, predicates={}); P = res["predicates"]
e0 = max(max(np.abs(step(N).conj().T @ step(N) - np.eye(2 * N)).max(), np.abs(step(N) @ trans(N) - trans(N) @ step(N)).max()) for N in (4, 6, 12))
P["E0"] = dict(max_defect=float(e0), met=bool(e0 < TOL))
N = 12; m = np.exp(2j * np.pi * rng.random(N)); T = trans(N)
e1 = np.abs(T @ Mm(m) @ T.T - Mm(np.roll(m, 1))).max()   # roll(m,1)[x] = m[x-1]
P["E1"] = dict(max_defect=float(e1), met=bool(e1 < TOL))
e2 = {}; e2ok = True; e3ok = True; lam_bad = 0
for (N, q) in ((4, 2), (4, 4), (6, 2), (6, 3), (6, 6), (5, 5), (4, 8)):
    U = step(N); T = trans(N); z = cmath.exp(2j * math.pi / q); setA = set(); setB = set(); orders = set()
    for ex in itertools.product(range(q), repeat=N):
        m = np.array([z ** e for e in ex]); X = U @ Mm(m); Y = T @ X @ T.T
        i, j = np.argwhere(np.abs(X) > 0.5)[0]; lam = Y[i, j] / X[i, j]
        if np.abs(Y - lam * X).max() < TOL:
            setA.add(ex)
            k = [k for k in range(q) if abs(z ** k - lam) < 1e-9]
            if not k: e3ok = False; continue
            k = k[0]
            if (k * N) % q != 0: lam_bad += 1; e3ok = False
            if any((ex[x] - (ex[0] - k * x)) % q != 0 for x in range(N)): e3ok = False
            orders.add(q // math.gcd(q, k))
        if len({(ex[(x - 1) % N] - ex[x]) % q for x in range(N)}) == 1: setB.add(ex)
    e2[f"N={N},q={q}"] = dict(all_m=q ** N, operator_identity=len(setA), difference_constant=len(setB), equal=setA == setB, orders_of_lambda=sorted(orders))
    e2ok &= setA == setB; e3ok &= all(q % o == 0 for o in orders)
P["E2"] = dict(per_case=e2, met=bool(e2ok)); P["E3"] = dict(lambda_power_N_not_one=lam_bad, met=bool(e3ok))
N = 12; U = step(N); T = trans(N)
def is_scalar(m):
    X = U @ Mm(m); Y = T @ X @ T.T; i, j = np.argwhere(np.abs(X) > 0.5)[0]; lam = Y[i, j] / X[i, j]
    return bool(np.abs(Y - lam * X).max() < TOL), lam, float(np.abs(Y - lam * X).max())
ca = is_scalar(np.ones(N)); w = cmath.exp(2j * math.pi / 3)
cc = is_scalar(np.array([w ** (x // 2) for x in range(N)])); cd = is_scalar(np.array([(-1) ** x for x in range(N)]))
P["E4"] = dict(a_constant=(ca[0] and abs(ca[1] - 1) < TOL), b_no_lambda_with_lambda_N_ne_1=lam_bad == 0,
               c_staircase_in_set=cc[0], c_staircase_defect=cc[2], d_alternating=(cd[0] and abs(cd[1] + 1) < TOL),
               met=bool(ca[0] and abs(ca[1] - 1) < TOL and lam_bad == 0 and (not cc[0]) and cd[0] and abs(cd[1] + 1) < TOL),
               wording_remark="on a ring of N sites 'm(x) = m(0) lambda^-x' additionally needs lambda^N = 1; the statement does not say so")
r = 1; Phi = 2 * math.pi * r / N; s5 = is_scalar(np.array([cmath.exp(-1j * Phi * x) for x in range(N)]))
P["E5"] = dict(scalar=s5[0], lambda_equals_exp_plus_i_Phi=bool(abs(s5[1] - cmath.exp(1j * Phi)) < TOL), met=bool(s5[0]))
s0 = {}; s0ok = True
for N in (64, 256, 1024):
    th = np.angle(np.linalg.eigvals(step(N))); a = np.abs(th); inband = (a <= math.pi / 4 + 1e-9) | (a >= 3 * math.pi / 4 - 1e-9)
    s0[N] = dict(outside=int((~inband).sum()), pi4_minus_max_first_arc=float(math.pi / 4 - a[a < math.pi / 2].max()),
                 min_second_arc_minus_3pi4=float(a[a > math.pi / 2].min() - 3 * math.pi / 4)); s0ok &= bool(inband.all())
P["S0"] = dict(per_N=s0, met=bool(s0ok))
def in_sigma(t, closed=True):
    t = t % 2
    for lo, hi in ((Fr(-1, 4), Fr(1, 4)), (Fr(3, 4), Fr(5, 4)), (Fr(7, 4), Fr(9, 4))):
        if (lo <= t <= hi) if closed else (lo < t < hi): return True
    return False
def inter(q, closed=True):
    ends = sorted({(e + Fr(2 * j, q)) % 2 for j in range(q) for e in (Fr(1, 4), Fr(3, 4), Fr(5, 4), Fr(7, 4))})
    mids = [((ends[i] + (ends[(i + 1) % len(ends)] + (2 if i + 1 == len(ends) else 0))) / 2) % 2 for i in range(len(ends))]
    mem = lambda t: all(in_sigma(t - Fr(2 * j, q), closed) for j in range(q))
    return [e for e in ends if mem(e)], [m for m in mids if mem(m)], ends, mids
p1, m1, ends1, mids1 = inter(1); p2, m2, ends2, mids2 = inter(2)
sig_ok = all(sorted(pp) == [Fr(1, 4), Fr(3, 4), Fr(5, 4), Fr(7, 4)] and all(in_sigma(t) for t in mm) and len(mm) == 2 for pp, mm in ((p1, m1), (p2, m2)))
p4, m4, _, _ = inter(4); q4_ok = sorted(p4) == [Fr(1, 4), Fr(3, 4), Fr(5, 4), Fr(7, 4)] and m4 == []
nonempty = [q for q in [3] + list(range(5, 201)) if any(inter(q)[:2])]
P["S1"] = dict(q1_q2_equal_Sigma=bool(sig_ok), q4_points=[str(t) for t in sorted(p4)], q4_midpoints_in=len(m4), nonempty_q_in_3_and_5_to_200=nonempty,
               met=bool(sig_ok and q4_ok and not nonempty))
p4o, m4o, _, _ = inter(4, closed=False)
P["S2"] = dict(a=bool(q4_ok), b_q8_q12_empty=not any(inter(8)[:2]) and not any(inter(12)[:2]), c_open_bands_q4_empty=(p4o == [] and m4o == []),
               d_q6_empty=not any(inter(6)[:2]), met=bool(q4_ok and not any(inter(8)[:2]) and not any(inter(12)[:2]) and not any(inter(6)[:2])))
res["all_met"] = all(v["met"] for v in P.values())
json.dump(res, open(OUT, "w"), indent=1, default=str)
for k, v in P.items(): print(k, v)
print("all met", res["all_met"])
