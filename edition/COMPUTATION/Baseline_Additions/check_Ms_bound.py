#!/usr/bin/env python3
"""Numerical sanity check (not a proof) of the uniform H^s bound for the continuum interpolants
Y_theta = 1/2 + (1-theta) H(X_0) + theta H(X_mu),  H(X_b) = chi P_b (1-chi) + (1-chi) P_b chi,
chi = indicator of (0,1), P_b the continuum Dirac projection with symbol (1/2)[I - (u sx + b sz)/sqrt(u^2+b^2)].
Discretization: periodic grid on [-R, R) with N points, FFT multipliers.  Reports the L^2 operator norm of
W Y W^{-1}, W = (1+u^2)^{s/2}, which is the H^s -> H^s norm of Y on the grid, and the grid value of the
analytic bound 1/2 + 2 c_s c'_s with c_s, c'_s the grid multiplier norms of chi and 1-chi.
"""
import json, sys, numpy as np
def run(N, R, s, b_list, thetas):
    x = (np.arange(N) - N//2) * (2*R/N)
    u = 2*np.pi*np.fft.fftfreq(N, d=2*R/N)
    F = np.fft.fft(np.eye(N), axis=0) / np.sqrt(N); Fi = F.conj().T
    w = (1 + u**2)**(s/2)
    W = Fi @ np.diag(w) @ F; Wi = Fi @ np.diag(1/w) @ F
    chi = ((x > 0) & (x < 1)).astype(float); C = np.diag(chi); Cc = np.diag(1 - chi)
    opn = lambda A: float(np.linalg.norm(A, 2))
    cs, cps = opn(W @ C @ Wi), opn(W @ Cc @ Wi)
    I2 = np.eye(2); sx = np.array([[0, 1], [1, 0]]); sz = np.diag([1., -1.])
    def proj(b):
        r = np.sqrt(u**2 + b**2); r[r == 0] = 1.0
        P = np.zeros((2*N, 2*N), complex)
        for a in range(2):
            for c in range(2):
                sym = 0.5*(I2[a, c] - (u*sx[a, c] + b*sz[a, c])/r)
                P[a*N:(a+1)*N, c*N:(c+1)*N] = Fi @ np.diag(sym) @ F
        return P
    k2 = lambda A: np.kron(np.eye(2), A)
    Hx = lambda P: k2(C) @ P @ k2(Cc) + k2(Cc) @ P @ k2(C)
    H0 = Hx(proj(0.0)); out = []
    for b in b_list:
        Hb = Hx(proj(b))
        for th in thetas:
            Y = 0.5*np.eye(2*N) + (1-th)*H0 + th*Hb
            out.append(dict(mu=b, theta=th, Hs_norm=opn(k2(W) @ Y @ k2(Wi)), L2_norm=opn(Y)))
    return dict(N=N, R=R, s=s, c_s=cs, c_prime_s=cps, analytic_bound=0.5 + 2*cs*cps,
                max_Hs_norm=max(o["Hs_norm"] for o in out), max_L2_norm=max(o["L2_norm"] for o in out), cases=out)
res = [run(N, R, 0.25, [0.5, 8.0], [0.0, 0.5, 1.0]) for N, R in ((128, 8.0), (256, 8.0), (512, 8.0), (512, 16.0))]
ok = all(r["max_Hs_norm"] <= r["analytic_bound"] + 1e-9 and r["max_L2_norm"] <= 1 + 1e-9 for r in res)
for r in res: print(r["N"], r["R"], "c_s=%.3f c'_s=%.3f bound=%.3f max||Y||_Hs=%.3f max||Y||_L2=%.4f" % (r["c_s"], r["c_prime_s"], r["analytic_bound"], r["max_Hs_norm"], r["max_L2_norm"]))
json.dump(dict(note="numerical sanity check only; the bound is proved analytically", all_consistent=ok, runs=res), open(sys.argv[1] if len(sys.argv) > 1 else "Ms_Bound_Sanity.json", "w"), indent=1)
print("CONSISTENT" if ok else "INCONSISTENT")
