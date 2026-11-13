"""Follow-up to xr9_check.py (its predicates all passed; two diagnostics needed a second look).
F1  P6 at kappa=-1, N=640 had reference edge weight 1.3e-5 at Lc=20 (truncation ~ 4e-3 in norm),
    so the reported state error 0.0107 may be the reference, not the walk. Predicate fixed now:
    with Lc=30 at N=160 and N=640 (kappa=-1), edge weight < 1e-12 at both and
    err(640)/err(160) <= 0.6. Also report kappa=+1 at Lc=30.
F2  P8 reported max ratio 1.82 from roundoff at tiny q. Predicate: with mpmath (40 digits) on
    q = j/1000, j=1..1000, |omega(k*+q)-omega(k*)-q^2/2|/(q^4/6) <= 1, and its limit at small q
    is within 1e-4 of 1 (quartic coefficient -1/6).
F3  sheet-unresolved input: sector r of a localized sheet applies gain phase exp(-2 pi i r g/M),
    i.e. coupling r*kappa. Predicate (exact arithmetic identity, N=20, M=N^3+1, kappa=1, eps=1):
    L*r for r=2,3 equals the count-built scale that kappa'=r*kappa would give up to rounding
    (|r*L - L'| <= r/2+1/2), and the fraction of sectors r in 0..M-1 whose per-tick maximal phase
    angle 2*|r'|*2pi*L/M (r' = centred residue) exceeds 1 radian is > 0.9.
"""
import os, sys, json, re
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "xr9_followup_result.json")
if os.path.exists(OUT): sys.exit("refusing to overwrite " + OUT)
src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "xr9_check.py")).read()
head = src.split('OUT = os.path')[0]
walk = src.split("# ---------- walk ----------")[1].split("# P4")[0]
p6 = src.split("# P6\n")[1].split("rows = []")[0]
cnt = src.split("# ---------- counts ----------")[1].split("rows = []; ok = True")[0]
cg = "def count_gain" + src.split("def count_gain")[1].split("rows = []")[0]
exec(head.split('"""')[2]); exec(cnt); exec(cg); exec(walk); exec(p6)
res = {}
rows = []
for kappa in (-1.0, 1.0):
    for N in (160, 640):
        eps = delta = sqrt(2*pi/N); tau = eps*delta**2; M = N**3+1; Lc = 30
        ls = np.arange(-Lc, Lc+1)
        q0 = (0.9, -0.8); l0 = (round(0.3/eps), round(-0.5/eps))
        f1 = np.exp(-eps*(ls-l0[0])**2/2 - 1j*ls*q0[0]); f2 = np.exp(-eps*(ls-l0[1])**2/2 - 1j*ls*q0[1])
        c0 = np.outer(f1, f2); c0 /= vnorm(c0)
        n = max(1, round(0.6/tau)); t = n*tau
        ct = Ref(Lc, eps, kappa).evolve(c0, t)
        ang, th = sampled_angles(N, M, kappa, delta)
        psi = run_walk(N, encode(N, c0, Lc), ang, n)
        rows.append(dict(kappa=kappa, N=N, Lc=Lc, chart_ok=bool(2*pi*Lc/N <= pi/2), err=vnorm(psi-encode(N, ct, Lc)),
            edge_weight=float(np.sum(np.abs(ct[[0, -1], :])**2)+np.sum(np.abs(ct[:, [0, -1]])**2))))
        print(rows[-1], flush=True)
res["F1"] = dict(ok=bool(rows[0]["edge_weight"] < 1e-12 and rows[1]["edge_weight"] < 1e-12 and rows[1]["err"]/rows[0]["err"] <= 0.6),
                 ratio_neg=rows[1]["err"]/rows[0]["err"], ratio_pos=rows[3]["err"]/rows[2]["err"], rows=rows)
mp.mp.dps = 40
rat = []
for j in range(1, 1001):
    q = mp.mpf(j)/1000
    rat.append(abs(mp.asin(mp.sin(-mp.pi/2+q)/mp.sqrt(2))+mp.pi/4-q*q/2)/(q**4/6))
res["F2"] = dict(ok=bool(max(rat) <= 1 and abs(rat[0]-1) < 1e-4), max_ratio=float(max(rat)), at_small_q=float(rat[0]), at_1=float(rat[-1]))
N = 20; M = N**3+1; delta = 2*pi/N
g, L = count_gain(N, M, 1.0, delta)
okr = True; det = []
for r in (2, 3):
    g2, L2 = count_gain(N, M, float(r), delta)
    det.append((r, L, L2)); okr = okr and abs(r*L-L2) <= r/2+0.5
big = sum(1 for r in range(M) if 2*min(r, M-r)*2*pi*L/M > 1)/M
res["F3"] = dict(ok=bool(okr and big > 0.9), scales=det, fraction_sectors_strong=big, L=L, M=M)
res["all_pass"] = all(v["ok"] for v in res.values() if isinstance(v, dict))
json.dump(res, open(OUT, "x"), indent=1)
print({k: (v["ok"] if isinstance(v, dict) else v) for k, v in res.items()}); print(res["F2"], res["F3"])
