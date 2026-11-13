"""Follow-up to failed predicate E4 of xr_clock.py (result_run1.json is kept unchanged).
E4 used a 1e-15 float threshold with no stated basis. Follow-up predicates, fixed before running:
 E4f1 the same quantities at 40 digits (mpmath): for every even delay 2q, q=0..M-1, M in {16,64,2048},
      |P+(k=1) - P+(k=M/2+1)| < 1e-35; for delay 1 the difference equals cos(2pi/M) within 1e-35.
 E4f2 the float residuals of run 1 are measured and stored (no threshold): expected a few ulp (~1e-16).
Refuses to overwrite its result file."""
import sys, os, json, math, mpmath as mp
mp.mp.dps = 40
dest = sys.argv[1]
if os.path.exists(dest): sys.exit("refusing to overwrite")
tiny = mp.mpf(10) ** -35; ok = True; worst = mp.mpf(0)
for M in (16, 64, 2048):
    P = lambda k, d: mp.cos(mp.pi * k * d / M) ** 2
    for q in range(M):
        r = abs(P(1, 2 * q) - P(M // 2 + 1, 2 * q)); worst = max(worst, r); ok &= r < tiny
    ok &= abs(P(1, 1) - P(M // 2 + 1, 1) - mp.cos(2 * mp.pi / M)) < tiny
M = 16; pl = lambda k, d: math.cos(math.pi * k * d / M) ** 2
fl_even = max(abs(pl(1, 2 * q) - pl(M // 2 + 1, 2 * q)) for q in range(M))
fl_odd = abs(pl(1, 1) - pl(M // 2 + 1, 1) - math.cos(2 * math.pi / M))
json.dump(dict(E4f1=dict(met=bool(ok), worst=mp.nstr(worst, 5)), E4f2=dict(float_even_residual=fl_even, float_odd_residual=fl_odd)), open(dest, "x"), indent=1)
print(ok, mp.nstr(worst, 5), fl_even, fl_odd)
