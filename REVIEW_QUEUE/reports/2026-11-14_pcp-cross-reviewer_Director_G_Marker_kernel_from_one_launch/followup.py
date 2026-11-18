"""Follow-up to FAILED predicates P1(omega_k) and P4 of xr_marker.py (kept as FAIL in run1/xr_marker.json).
F1: omega(k) - (pi/2 - k) evaluated at 80 digits (sympy simplify did not reduce the asin/acos form); also exact: sin(pi/2-k)=cos k=1/sqrt3 = sin k/sqrt2 and pi/2-k in (-pi/2,pi/2).
F2: C(n)=residual*t^1.5 for n up to 1500: report sup, inf over blocks of 300 (bounded = consistent with O(t^-3/2); P4's 'later sup <= earlier sup' was stricter than the claim).
Refuses to overwrite followup.json."""
import sys, json, os, mpmath as mp, sympy as sp
if os.path.exists("followup.json"): sys.exit("refusing to overwrite")
mp.mp.dps = 80
k = mp.acos(1/mp.sqrt(3)); f1 = mp.asin(mp.sin(k)/mp.sqrt(2)) - (mp.pi/2 - k)
ks = sp.acos(1/sp.sqrt(3)); exact = sp.simplify(sp.sin(ks)/sp.sqrt(2) - sp.cos(ks)) == 0
mp.mp.dps = 40
H0 = 3*mp.sqrt(2)/8; cur = {0:(1,0)}; blocks = {}
N = 1500
for t in range(1, 4*N+1):
    nx = {}
    for x,(u,v) in cur.items():
        a = nx.setdefault(x+1,[0,0]); a[0] = u+v
        b = nx.setdefault(x-1,[0,0]); b[1] = u-v
    cur = nx
    if t % 4 == 0:
        n = t//4; u,v = cur[2*n]; ph = 6*n*k + mp.pi/4; fac = 4/mp.sqrt(2*mp.pi*t*H0); sc = mp.mpf(2)**(t//2)
        r = mp.hypot(mp.mpf(u)/sc - fac*0.75*mp.cos(ph), mp.mpf(v)/sc - fac*(mp.cos(ph)/4 - mp.sin(ph)/(2*mp.sqrt(2))))
        C = float(r*mp.mpf(t)**1.5); b = (n-1)//300
        lo, hi = blocks.get(b, (9e9, 0)); blocks[b] = (min(lo, C), max(hi, C))
json.dump(dict(F1_abs=float(abs(f1)), F1_exact_sine_identity=bool(exact), F2_blocks_of_300_n_min_max_C=blocks), open("followup.json","x"), indent=1)
print(float(abs(f1)), exact, blocks)
