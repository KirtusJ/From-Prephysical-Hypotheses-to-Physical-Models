"""Cross-review checks for PRs #260 and #262 (Director G notes). Written before first run.

Predicates (fixed before running; failures are kept, never removed):
P0 control: random-basis X/Z measure-and-reprepare on BB84 inputs has mean fidelity 3/4 (exact).
P1 (#262, exact Fractions): s=5/16 gives direct 5/16, matched-pi 245/256, fair 325/512, x=187/512,
   t=11/256; p0(c),ppi(c) from explicit marker vectors equal (325 -/+ 165c)/512 for c in a rational grid.
P2 (#262 table): 4-row extreme-exponent table gives means (187,22,352)/512 and each extremum unique.
P3 (#262 tangent theorem): for every mode in the stated class (q>0 any c in [-1,1]; q<0 c in [0,1];
   q=0; q=+-inf with the same overlap rule; recorded modes d in [0,1]) Y - L(X) >= 0, with equality
   only at (q,c)=(1,1). Hypothesis tested per mode and counted. mpmath 50 digits; zero side: equality
   counted when |Y-L(X)| < 1e-40 (50-digit arithmetic, ~10 ops).
P3b outside the class (q<0, c<0): report how many modes have Y-L(X)<0 (expected: some, per note's table).
P4 (unreported parameter): repeat P1/P3 at s=1/4 and s=3/8 (note reports only s=5/16): does the
   tangent certificate's precondition 1<r<x/t and L<identity hold? Reported, not assumed.
P5 (#262, alternative reading of the fair arm, OUTSIDE note's model): power applied per unread-tag branch,
   X'=(R_q(y_c)+R_q(z_c))/2. Report whether (x,t) is reproduced by a nontrivial mixture
   (checked by LP-free test: whether any mode has Y-L'(X')<0 for the supporting line at (x,t) of that curve).
P6 (#260): for random states on C(2q) x Q(1q) x E (dim 2..4) and random measure-prepare devices with
   optimal outputs, A <= f(p) + 1e-9 (float tolerance: ~1e3 ops on unit-norm data, eps 2.2e-16);
   hypothesis tested per case (trace 1, PSD, POVM sums to I). Plus the attaining family hits f(p).
Seed 20261115. Refuses to overwrite its result file.
"""
import sys, os, json, random
from fractions import Fraction as F
import numpy as np
import mpmath as mp

OUT = sys.argv[1] if len(sys.argv) > 1 else "xr_result.json"
if os.path.exists(OUT):
    sys.exit(f"refusing to overwrite {OUT}")
res = {"predicates": {}, "failures": []}
def rec(name, ok, detail):
    res["predicates"][name] = {"pass": bool(ok), "detail": detail}
    if not ok: res["failures"].append(name)

# P0
fid = F(0)
for inp in [("Z",0),("Z",1),("X",0),("X",1)]:
    for basis in "ZX":
        fid += F(1,2)*(1 if basis == inp[0] else F(1,2))
rec("P0_control", fid/4 == F(3,4), str(fid/4))

def amp_numbers(s):
    # 2D good/bad basis; v=(sqrt s, sqrt(1-s)); D=I-2vv^T; F=diag(-1,1).
    # success masses exactly: direct s; D: s; DF: s(3-4s)^2; with marker overlap c computed symbolically:
    # good output amplitude = sqrt(s)(1-2s)*eG*phase - 2 sqrt(s)(1-s) eB
    g = s*(1-2*s)**2; b = 4*s*(1-s)**2; cross = 4*s*(1-2*s)*(1-s)
    return g, b, cross
mp.mp.dps = 50
def R(q, z):
    if isinstance(z, F): z = mp.mpf(z.numerator)/z.denominator
    else: z = mp.mpf(z)
    if q == "inf": return mp.mpf(0) if z < 0.5 else mp.mpf(1) if z > 0.5 else None
    if q == "-inf": return mp.mpf(1) if z < 0.5 else mp.mpf(0) if z > 0.5 else None
    return z**q/(z**q+(1-z)**q)

def tangent_suite(s, tag):
    g, b, cross = amp_numbers(s)
    p0 = lambda c: g + b - cross*c; ppi = lambda c: g + b + cross*c
    x = 1 - (g+b); t = 1 - ppi(1)
    out = {"s": str(s), "direct": str(s), "phase0_c1": str(p0(1)), "pi": str(ppi(1)),
           "fair": str(g+b), "x": str(x), "t": str(t)}
    if tag == "5/16":
        ok = (p0(1) == F(5,16) and ppi(1) == F(245,256) and g+b == F(325,512) and x == F(187,512)
              and t == F(11,256) and cross == F(165,512))
        # explicit marker vectors check
        for c in [F(k,8) for k in range(-8,9)]:
            eG = np.array([1.0,0.0]); eB = np.array([float(c), (1-float(c)**2)**0.5])
            for sign, ref in [(1,p0(c)),(-1,ppi(c))]:
                amp = sign*float(s)**0.5*(1-2*float(s))*eG - 2*float(s)**0.5*(1-float(s))*eB
                if abs(amp@amp - float(ref)) > 1e-12: ok = False
        rec("P1_numbers_5/16", ok, out)
    if x >= F(1,2) or t <= 0:
        return {"precondition": False, **out}
    xm, tm = mp.mpf(x.numerator)/x.denominator, mp.mpf(t.numerator)/t.denominator
    r = mp.log((1-tm)/tm)/mp.log((1-xm)/xm)
    L = lambda z: tm + r*tm*(1-tm)/(xm*(1-xm))*(mp.mpf(z)-xm)
    pre = {"r": float(r), "1<r<x/t": bool(1 < r < xm/tm), "L0<0": bool(L(0) < 0), "L1<1": bool(L(1) < 1)}
    qs = [F(k,4) for k in range(-40,41)] + ["inf","-inf"]
    cs = [F(k,16) for k in range(-16,17)]
    inclass = viol = eq = 0; outside_neg = 0; minslack = None; eqlist = []
    for q in qs:
        for c in cs:
            y = 1 - ppi(c)
            qq = q if isinstance(q,str) else mp.mpf(q.numerator)/q.denominator
            allowed = (c >= 0) or (q == "inf") or (not isinstance(q,str) and q >= 0)
            X, Y = R(qq, x), R(qq, y)
            if X is None or Y is None: continue  # tie at an extremum: excluded (note: "unique")
            slack = Y - L(X)
            if allowed:
                inclass += 1
                if abs(slack) < mp.mpf(10)**-40: eq += 1; eqlist.append((str(q),str(c)))
                elif slack < 0: viol += 1
                minslack = slack if minslack is None else min(minslack, slack)
            elif slack < 0:
                outside_neg += 1
    for d in [F(k,64) for k in range(65)]:
        inclass += 1
        if F(0) + 0 > 0: pass
        if mp.mpf(d.numerator)/d.denominator - L(mp.mpf(d.numerator)/d.denominator) <= 0: viol += 1
    out.update(pre=pre, in_class_modes=inclass, violations=viol, equalities=eqlist,
               outside_class_negative=outside_neg)
    return out

r516 = tangent_suite(F(5,16), "5/16")
rec("P3_tangent_5/16", r516["violations"] == 0 and r516["equalities"] == [("1","1")]
    and all(r516["pre"].values()), r516)
rec("P3b_outside_class_has_negatives", r516["outside_class_negative"] > 0,
    r516["outside_class_negative"])
for s in [F(1,4), F(3,8)]:
    rs = tangent_suite(s, str(s))
    rec(f"P4_tangent_s={s}", rs.get("precondition", True) and rs["violations"] == 0
        and all(rs["pre"].values()), rs)

# P2 table
rows = [(165,"-inf",-1),(22,"-inf",1),(187,"inf",1),(138,"inf",0)]
g,b,cross = amp_numbers(F(5,16))
means = [0,0,0]; uniq = True
for w,q,c in rows:
    for i, fail in enumerate([F(187,512), 1-(g+b+cross*c), 1-(g+b-cross*c)]):
        v = R(q, fail)
        if v is None: uniq = False; continue
        means[i] += w*int(v)
rec("P2_table", means == [187,22,352] and uniq, means)

# P5 per-tag-branch reading (outside the note's model)
x, t = F(187,512), F(11,256)
pts = []
for q in [F(k,8) for k in range(-80,81)] + ["inf","-inf"]:
    for c in [F(k,8) for k in range(0,9)]:
        qq = q if isinstance(q,str) else mp.mpf(q.numerator)/q.denominator
        y = 1-(g+b+cross*c); z = 1-(g+b-cross*c)
        a1, a2 = R(qq,y), R(qq,z)
        if a1 is None or a2 is None: continue
        pts.append(((a1+a2)/2, a1, str(q), str(c)))
# supporting-line test: is (x,t) an extreme point of the point cloud's convex hull, exposed?
# check all lines through (x,t) with slope m: need some m with all points on one side.
best = None
for k in range(-2000, 2001):
    m = mp.mpf(k)/100
    mn = min(p[1] - (t + m*(p[0]-x)) for p in pts)
    if best is None or mn > best[0]: best = (mn, float(m))
rec("P5_per_tag_branch_exposed", best[0] > -mp.mpf(10)**-30,
    {"max_over_slopes_of_min_slack": float(best[0]), "slope": best[1], "n_modes": len(pts)})

# P6 #260 revival bound
rng = np.random.default_rng(20261115)
def f(p): return 1.0 if p <= 0.5 else 0.75 + 0.5*np.sqrt(p*(1-p))
k0 = np.array([1,0.]); k1 = np.array([0,1.]); h0 = (k0+k1)/2**.5; h1 = (k0-k1)/2**.5
psi = {(0,0):k0,(0,1):k1,(1,0):h0,(1,1):h1}
Omega = np.zeros(8)
for (bb,ss),v in psi.items():
    cvec = np.zeros(4); cvec[2*bb+ss] = 1
    Omega += 0.5*(-1)**(bb*ss)*np.kron(cvec, v)
cases = qual = worst = 0; worst = -9
for trial in range(4000):
    dE = int(rng.integers(1,5)); K = int(rng.integers(2,6))
    mode = trial % 2
    if mode == 0:
        Psi = rng.normal(size=8*dE) + 1j*rng.normal(size=8*dE)
    else:  # near-ideal leaking family plus noise
        th = rng.uniform(0, np.pi); e0 = np.zeros(dE, complex); e0[0]=1
        e1 = np.zeros(dE, complex); e1[0]=np.cos(th)
        if dE > 1: e1[1]=np.sin(th)
        else: e1[0]=1
        Psi = np.zeros(8*dE, complex)
        for (bb,ss),v in psi.items():
            cvec = np.zeros(4); cvec[2*bb+ss]=1
            Psi += 0.5*(-1)**(bb*ss)*np.kron(np.kron(cvec,v),[e0,e1][bb])
        Psi += 0.05*rng.uniform()*(rng.normal(size=8*dE)+1j*rng.normal(size=8*dE))
    Psi /= np.linalg.norm(Psi)
    T = Psi.reshape(4, 2*dE)  # C x (QE)
    Ms = [rng.normal(size=(2*dE,2*dE))+1j*rng.normal(size=(2*dE,2*dE)) for _ in range(K)]
    S = sum(m.conj().T@m for m in Ms); w, U = np.linalg.eigh(S); Sih = U@np.diag(w**-.5)@U.conj().T
    Ms = [Sih@m.conj().T@m@Sih for m in Ms]
    povm_ok = np.allclose(sum(Ms), np.eye(2*dE), atol=1e-10) and all(np.linalg.eigvalsh(m).min() > -1e-12 for m in Ms)
    if mode == 1:  # strategy: measure E to guess basis, then Q in that basis (approx Helstrom via projectors)
        pass
    cases += 1
    if not povm_ok: continue
    qual += 1
    A = 0.0
    for m in Ms:
        wk = np.array([[np.real(T[2*bb+ss].conj()@m@T[2*bb+ss]) for ss in (0,1)] for bb in (0,1)])
        base = wk.sum()/2
        vz = wk[0,0]-wk[0,1]; vx = wk[1,0]-wk[1,1]
        A += base + 0.5*np.hypot(vz, vx)
    rho = Psi.reshape(8, dE)
    p = float(np.linalg.norm(Omega@rho)**2)
    worst = max(worst, A - f(p))
# attaining family with the optimal (Helstrom) device, exact formula check
att = []
for th in np.linspace(0.01, np.pi-0.01, 25):
    p = (1+np.cos(th))/2; A = 0.75 + np.sin(th)/4; att.append(abs(A-f(p)))
rec("P6_revival_bound", worst <= 1e-9 and max(att) < 1e-12,
    {"cases": cases, "qualifying": qual, "max_A_minus_f": float(worst), "attain_err": float(max(att))})
# design target: f(p)=0.824222 -> p
pt = (1+mp.sqrt(1-16*(mp.mpf("0.824222")-mp.mpf(3)/4)**2))/2
res["design_target_p_for_A_0.824222"] = float(pt)
with open(OUT, "x") as fh: json.dump(res, fh, indent=1, default=str)
print(json.dumps({k: v["pass"] for k, v in res["predicates"].items()}), res["failures"],
      res["design_target_p_for_A_0.824222"])
