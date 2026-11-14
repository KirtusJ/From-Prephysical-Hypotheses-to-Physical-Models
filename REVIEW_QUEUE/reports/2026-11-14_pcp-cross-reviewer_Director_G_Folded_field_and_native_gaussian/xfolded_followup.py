"""Follow-up to failed predicates P2 and P3 of xfolded_check.py (kept failed in run1/xfolded_result.json).
Suspected cause: sympy.simplify did not reduce (-1)**(3/4) forms to zero; the test '== 0' was too strict a symbolic test.
PREDICATES (fixed before run): evaluate the same differences with mpmath at 40 digits.
F2  |f_1(+1)-(1+i)/2| and |f_1(-1)-(1-i)/2| < 1e-35 (40-digit arithmetic, a handful of operations).
F3  |U(k*)v - e^{i pi/4}v|, |U(k*)v_- + e^{-i pi/4}v_-| < 1e-35, v=(1,-i)/sqrt2, v_-=(1,i)/sqrt2.
Refuses to overwrite OUTDIR/xfolded_followup.json.
"""
import sys, os, json, mpmath as mp
mp.mp.dps = 40
i = mp.mpc(0, 1); r2 = mp.sqrt(2); ph = mp.exp(-i*mp.pi/4)
a = abs(i*ph*(1/r2) - (1+i)/2); b = abs((1/i)*ph*(i/r2) - (1-i)/2)
ks = -mp.pi/2
U = mp.matrix([[mp.exp(-i*ks), mp.exp(-i*ks)], [mp.exp(i*ks), -mp.exp(i*ks)]])/r2
v = mp.matrix([1, -i])/r2; vm = mp.matrix([1, i])/r2
c = mp.norm(U*v - mp.exp(i*mp.pi/4)*v); d = mp.norm(U*vm + mp.exp(-i*mp.pi/4)*vm)
res = dict(F2=dict(passed=bool(a < 1e-35 and b < 1e-35), residuals=[str(a), str(b)]), F3=dict(passed=bool(c < 1e-35 and d < 1e-35), residuals=[str(c), str(d)]))
print(res)
os.makedirs(sys.argv[1], exist_ok=True)
with open(os.path.join(sys.argv[1], "xfolded_followup.json"), "x") as fh: json.dump(res, fh, indent=1); fh.write("\n")
