"""xr74 cross-review program for 'Testing the coin as well as its phase'. Written from the note's
definitions, not from its checker. Exact Fractions except P10/P11 (floats; tolerance 1e-12 =
~1e4 ulp, basis: <100 double operations on O(1) numbers; measured residual is reported).
Seed 74. Refuses to overwrite its result file.

PREDICATES (fixed before first run). Each reports qualify / pass / fail; failures are kept.
P1  For exact U in U(2) (Gaussian-rational SU(2) from stereographic grid {-3..3}^3 times unit
    phases 1,(3+4i)/5,i; hypothesis tested: U U^dag = I exactly) and t=1..12: direct matrix power
    gives P(L at t | R) = q * Cheb2_{t-1}(s/2)^2, with q=|U_LR|^2, s=2Re u (S-part), and
    r=|tr U|^2 = s^2.
P2  Same U: projected history P(L at 1, R at 2) = q^2 (computed by projecting amplitudes).
P3  Random feasible mixtures (hypothesis tested: masses>=0, sum+c=1, 0<=q<=1, 0<=r<=4(1-q)),
    a in {0,1/3,1/4,1,7/5,3/2,19/10,2} (1/3, 7/5 not in the note's checker):
    W = sum m q (r-a)^2 + c(1+(a-1)^2)/2 and D = sum m (q-1/2)^2.
P4  Bounds on the same mixtures: c <= 2W/(1+(a-1)^2); nu(|q-1/2|>=e) <= D/e^2;
    nu(|r-a|>=d) <= 16D + 4W/d^2, for e,d in {1/10,1/4,1/2}.
P5  Alias pair q=1/2 +- (2-a)/8 at r=a, a<2: feasible, free L_t equal to target for t=1..40,
    F = 1/4 + ((2-a)/8)^2; cubic: q=7/16,9/16, F=65/256.
P6  (search) Other all-clock aliases: mass m at (q=0, r arbitrary) plus mass 1-m at
    (q=1/(2(1-m)), r=a), feasible iff q<=1-a/4. Predicate: free L_t equal target t=1..40 and
    F = 1/(4(1-m)); cubic extreme m=1/5 gives F=5/16.
P7  Reduced score T = L3+2(1-a)L2+(a^2-1)(F+1/4) = W+(a^2-1)D for a>1 on P3 mixtures, and
    T=0 <=> (W=0 and D=0).
P8  Endpoint a=2: on the exact feasible grid q=i/64, r=j/64 (hypothesis r<=4(1-q)):
    qr <= 4q(1-q) <= 1 and qr=1 only at (1/2,2).
P9  Loss, as reported: cubic pair with joint efficiency 64/65 gives observed F=1/4, D_obs=0,
    W=0, reduced score 0.
P9b (attack; expected to FAIL if the test is not loss-robust) "W=0 and D_obs=0 with efficiency
    eta<1 implies balanced": single pure coin (q, r=a) with eta=(4q-1)/(4q^2), q on a grid in
    (1/4, 1-a/4], q != 1/2. A case FAILS the predicate when W=D_obs=0 and q!=1/2.
P9c (attack) "reduced score zero implies c=0 under eta<1": balanced target mass 1-c plus count
    c=(1-eta)(a^2-1)/(2(1+(a-1)^2)), a>1 [derived: W=c(1+(a-1)^2)/2, D_obs=(eta-1)/4].
    FAILS when T_obs=0 with c>0.
P10 (outside class, float) tick-dependent unitary sequence U1,U2,U3 with q1=5/8,q2=3/5:
    predicate "W=D=0 implies stable balanced coin outside the stable class" FAILS if a sequence
    with |W|,|D|<1e-12 exists.
P11 (float) phase plate diag(1,i) between two free steps of Z_beta H, beta=exp(+-2 pi i/3):
    L probability = (2+-sqrt3)/4.
"""
import sys, json, random, cmath, math
from fractions import Fraction as Fr
from itertools import product
from pathlib import Path

res = {}
def rec(name, qualify, passed, failed, examples=None, note=None):
    res[name] = dict(qualify=qualify, passed=passed, failed=failed,
                     failed_examples=(examples or [])[:6], note=note)

class G:  # Gaussian rational
    __slots__ = ("a", "b")
    def __init__(s, a, b=0): s.a, s.b = Fr(a), Fr(b)
    def __add__(s, o): return G(s.a+o.a, s.b+o.b)
    def __mul__(s, o): return G(s.a*o.a-s.b*o.b, s.a*o.b+s.b*o.a)
    def conj(s): return G(s.a, -s.b)
    def n(s): return s.a*s.a+s.b*s.b
    def __eq__(s, o): return s.a == o.a and s.b == o.b
def mm(A, B): return [[A[i][0]*B[0][j]+A[i][1]*B[1][j] for j in range(2)] for i in range(2)]
def dag(A): return [[A[j][i].conj() for j in range(2)] for i in range(2)]
I2 = [[G(1), G(0)], [G(0), G(1)]]
def cheb2sq(r, T):  # U_{t-1}(s/2) with s^2=r; use U_n recurrence in s then square -> needs s.
    raise NotImplementedError
def chebU(s, T):
    p = [Fr(0), Fr(1)]
    for _ in range(T): p.append(s*p[-1]-p[-2])
    return p  # p[t] = U_{t-1}(s/2)
def hsq(r, T):  # squares h_t = U_{t-1}^2 as polynomial in r, no square root:
    # U_{t-1}^2 = (1-T_{2t}... ) use h_{t+1} = (r-2) h_t - h_{t-1} + 2, h_0=0,h_1=1 (derived:
    # sin^2 recurrence with 2cos(2theta)=r-2). Verified against chebU in P1.
    h = [Fr(0), Fr(1)]
    for _ in range(T): h.append((r-2)*h[-1]-h[-2]+2)
    return h

# ---------- P1, P2 ----------
phases = [G(1), G(Fr(3, 5), Fr(4, 5)), G(0, 1)]
q1 = p1 = 0; f1 = []; q2 = p2 = 0; f2 = []
# index convention: rail order (R, L); row = outgoing, column = incoming. Prepared R = column 0.
for v in product(range(-3, 4), repeat=3):
    nn = sum(x*x for x in v)
    w, x, y, z = [Fr(k, 1+nn) for k in (1-nn, 2*v[0], 2*v[1], 2*v[2])]
    u, b = G(w, x), G(y, z)
    for ph in phases:
        U = [[ph*u, ph*b], [ph*G(-1)*b.conj(), ph*u.conj()]]
        if mm(U, dag(U)) != I2:
            continue
        q1 += 1
        q = U[1][0].n(); s = 2*w
        tr = U[0][0]+U[1][1]; r = tr.n()
        ok = (r == s*s) and U[0][1].n() == q
        P = I2; ch = chebU(s, 12); h = hsq(r, 12)
        for t in range(1, 13):
            P = mm(U, P)
            ok = ok and P[1][0].n() == q*ch[t]**2 == q*h[t] and P[0][0].n()+P[1][0].n() == 1
        if ok: p1 += 1
        else: f1.append(dict(v=v))
        q2 += 1
        # R -> L at tick 1 (amp U[1][0]); project on L; L -> R at tick 2 (amp U[0][1])
        joint = (U[0][1]*U[1][0]).n()
        if joint == q*q: p2 += 1
        else: f2.append(dict(v=v))
rec("P1_free_rates_chebyshev", q1, p1, q1-p1, f1)
rec("P2_monitored_F_is_q_squared", q2, p2, q2-p2, f2)

# ---------- mixtures ----------
def rates(comps, c, T):
    L = [c/2]*(T+1); L[0] = Fr(0)
    for m, q, r in comps:
        h = hsq(r, T)
        for t in range(1, T+1): L[t] += m*q*h[t]
    Fv = c/4 + sum(m*q*q for m, q, r in comps)
    return L, Fv
def valid(comps, c):
    return (c >= 0 and all(m >= 0 and 0 <= q <= 1 and 0 <= r <= 4*(1-q) for m, q, r in comps)
            and c+sum(m for m, _, _ in comps) == 1)
rng = random.Random(74)
def rmix():
    k = rng.randint(1, 4)
    wts = [rng.randint(0, 9) for _ in range(k+1)]
    if sum(wts) == 0: wts[0] = 1
    tot = sum(wts); comps = []
    for i in range(k):
        q = Fr(rng.randint(0, 32), 32)
        r = 4*(1-q)*Fr(rng.randint(0, 24), 24)
        if rng.random() < 0.1: r = r + Fr(1, 7)   # deliberately sometimes infeasible
        comps.append((Fr(wts[i], tot), q, r))
    return comps, Fr(wts[k], tot)
As = [Fr(0), Fr(1, 3), Fr(1, 4), Fr(1), Fr(7, 5), Fr(3, 2), Fr(19, 10), Fr(2)]
tried = q3 = p3 = q4 = p4 = q7 = p7 = 0; f3 = []; f4 = []; f7 = []
for _ in range(4000):
    comps, c = rmix(); tried += 1
    if not valid(comps, c): continue
    L, Fv = rates(comps, c, 3)
    for a in As:
        q3 += 1
        W = L[3]+2*(1-a)*L[2]+(a*a-1)*L[1]; Dv = Fv-L[1]+Fr(1, 4)
        wW = sum(m*q*(r-a)**2 for m, q, r in comps)+c*(1+(a-1)**2)/2
        wD = sum(m*(q-Fr(1, 2))**2 for m, q, r in comps)
        if W == wW and Dv == wD: p3 += 1
        else: f3.append(dict(a=str(a)))
        q4 += 1
        ok = c <= 2*W/(1+(a-1)**2)
        for e in (Fr(1, 10), Fr(1, 4), Fr(1, 2)):
            ok = ok and sum(m for m, q, r in comps if abs(q-Fr(1, 2)) >= e) <= Dv/e**2
            ok = ok and sum(m for m, q, r in comps if abs(r-a) >= e) <= 16*Dv+4*W/e**2
        if ok: p4 += 1
        else: f4.append(dict(a=str(a), comps=str(comps), c=str(c)))
        if a > 1:
            q7 += 1
            T = L[3]+2*(1-a)*L[2]+(a*a-1)*(Fv+Fr(1, 4))
            if T == W+(a*a-1)*Dv and ((T == 0) == (W == 0 and Dv == 0)): p7 += 1
            else: f7.append(dict(a=str(a)))
rec("P3_W_D_identities", q3, p3, q3-p3, f3, note=f"{tried} mixtures drawn; qualify counts (mixture,a) pairs with valid mixture")
rec("P4_bounds", q4, p4, q4-p4, f4)
rec("P7_reduced_score", q7, p7, q7-p7, f7)

# ---------- P5 alias pair, P6 other aliases ----------
h = Fr(1, 2); q5 = p5 = 0; f5 = []; q6 = p6 = 0; f6 = []; alias_F = {}
for a in As + [Fr(k, 16) for k in range(0, 33)]:
    if a >= 2: continue
    d = (2-a)/8
    pair = [(h, h-d, a), (h, h+d, a)]
    if not valid(pair, Fr(0)): continue
    q5 += 1
    Lt, Ft = rates([(Fr(1), h, a)], Fr(0), 40); Lp, Fp = rates(pair, Fr(0), 40)
    ok = Lt == Lp and Fp == Fr(1, 4)+d*d and Ft == Fr(1, 4)
    if a == Fr(3, 2): ok = ok and (h-d, h+d, Fp) == (Fr(7, 16), Fr(9, 16), Fr(65, 256))
    if ok: p5 += 1
    else: f5.append(dict(a=str(a)))
    for mnum in range(1, 16):
        m = Fr(mnum, 20); qq = 1/(2*(1-m))
        for r0 in (Fr(0), Fr(1), Fr(4)):
            al = [(m, Fr(0), r0), (1-m, qq, a)]
            if not valid(al, Fr(0)): continue
            q6 += 1
            La, Fa = rates(al, Fr(0), 40)
            if La == Lt and Fa == 1/(4*(1-m)):
                p6 += 1
                key = str(a); alias_F[key] = max(alias_F.get(key, Fr(0)), Fa)
            else: f6.append(dict(a=str(a), m=str(m)))
rec("P5_alias_pair", q5, p5, q5-p5, f5)
rec("P6_other_aliases_diagonal_plus_one_coin", q6, p6, q6-p6, f6,
    note="largest alias F found per a (grid m=k/20): " + str({k: str(v) for k, v in sorted(alias_F.items())[:0]})
         + " cubic: " + str(alias_F.get("3/2")) + " ; eta=1/(4F) -> " + str(1/(4*alias_F["3/2"])))

# ---------- P8 endpoint ----------
q8 = p8 = 0; f8 = []; eqs = []; near = None
for i in range(0, 65):
    for j in range(0, 257):
        q, r = Fr(i, 64), Fr(j, 64)
        if not r <= 4*(1-q): continue
        q8 += 1
        ok = q*r <= 4*q*(1-q) <= 1
        if q*r == 1: eqs.append((str(q), str(r)))
        elif near is None or q*r > near[0]: near = (q*r, str(q), str(r))
        if ok: p8 += 1
        else: f8.append((str(q), str(r)))
ok_eq = eqs == [("1/2", "2")]
rec("P8_endpoint_inequality", q8, p8, q8-p8, f8,
    note=f"equality cases {eqs} (only (1/2,2): {ok_eq}); largest qr below 1 on grid: {near[0]} at q={near[1]}, r={near[2]}; "
         "just inside: L2=1-e allows count c=2e or a coin at qr=1-e, so the endpoint statement is exact-only")

# ---------- P9 loss ----------
a = Fr(3, 2); pair = [(h, Fr(7, 16), a), (h, Fr(9, 16), a)]
L, Fv = rates(pair, Fr(0), 3); obs = Fv*Fr(64, 65)
W = L[3]+2*(1-a)*L[2]+(a*a-1)*L[1]; Dobs = obs-L[1]+Fr(1, 4); T = L[3]-L[2]+Fr(5, 4)*(obs+Fr(1, 4))
ok = obs == Fr(1, 4) and W == 0 and Dobs == 0 and T == 0
rec("P9_reported_loss_false_pass", 1, int(ok), int(not ok))
q9 = fpass = 0; ex = []; etas = []
for a in As:
    for k in range(1, 64):
        q = Fr(k, 64)
        if not (Fr(1, 4) < q <= 1-a/4) or q == h: continue
        eta = (4*q-1)/(4*q*q)
        if not 0 <= eta < 1: continue
        q9 += 1
        L, Fv = rates([(Fr(1), q, a)], Fr(0), 3)
        W = L[3]+2*(1-a)*L[2]+(a*a-1)*L[1]; Dobs = eta*Fv-L[1]+Fr(1, 4)
        if W == 0 and Dobs == 0:
            fpass += 1; etas.append(eta)
            if a == Fr(3, 2) and len(ex) < 6: ex.append(dict(a=str(a), q=str(q), eta=str(eta)))
rec("P9b_loss_robustness_single_coin", q9, q9-fpass, fpass, ex,
    note=f"predicate 'W=0 and D_obs=0 at eta<1 implies balanced' fails in every qualifying case; eta range seen [{min(etas)}, {max(etas)}]; formula eta=(4q-1)/(4q^2) covers (0,1) as q runs (1/4,1/2)")
q9c = fc = 0; ex = []
for a in As:
    if a <= 1: continue
    for eta in (Fr(64, 65), Fr(9, 10), Fr(1, 2), Fr(99, 100)):
        c = (1-eta)*(a*a-1)/(2*(1+(a-1)**2))
        comps = [(1-c, h, a)]
        if not valid(comps, c): continue
        q9c += 1
        L, Fv = rates(comps, c, 3)
        Tobs = L[3]+2*(1-a)*L[2]+(a*a-1)*(eta*Fv+Fr(1, 4))
        W = L[3]+2*(1-a)*L[2]+(a*a-1)*L[1]
        if Tobs == 0 and c > 0 and W > 0:
            fc += 1; ex.append(dict(a=str(a), eta=str(eta), count=str(c), W=str(W)))
rec("P9c_reduced_score_hides_count_under_loss", q9c, q9c-fc, fc, ex,
    note="four-setting W still detects this count; the reduced three-setting score does not")

# ---------- P10 tick-dependent, float ----------
def coin(q, phi, chi=0.0):
    return [[math.sqrt(1-q)*cmath.exp(1j*chi), math.sqrt(q)*cmath.exp(1j*phi)],
            [-math.sqrt(q)*cmath.exp(-1j*phi), math.sqrt(1-q)*cmath.exp(-1j*chi)]]
def cm(A, B): return [[A[i][0]*B[0][j]+A[i][1]*B[1][j] for j in range(2)] for i in range(2)]
a = 1.5; qa, qb = 5/8, 3/5
L1 = qa; Fseq = qa*qb; Dseq = Fseq-L1+0.25
target_L2 = 0.9
lo, hi = 0.0, math.pi
def L2of(chi): return abs(cm(coin(qb, 0.0, chi), coin(qa, 0.0))[1][0])**2
vals = [(L2of(k*math.pi/2000), k*math.pi/2000) for k in range(2001)]
# bisect on a bracketing interval
br = next(((vals[k][1], vals[k+1][1]) for k in range(2000) if (vals[k][0]-target_L2)*(vals[k+1][0]-target_L2) <= 0), None)
found = False; Wseq = None
if br:
    lo, hi = br
    for _ in range(200):
        mid = (lo+hi)/2
        if (L2of(lo)-target_L2)*(L2of(mid)-target_L2) <= 0: hi = mid
        else: lo = mid
    U21 = cm(coin(qb, 0.0, lo), coin(qa, 0.0)); L2 = abs(U21[1][0])**2
    L3want = -2*(1-a)*L2-(a*a-1)*L1
    # U3 real rotation by angle th: amplitude on L = -sin(th) x_R + cos(th) x_L ; scan phase too
    xR, xL = U21[0][0], U21[1][0]
    best = None
    for k in range(20001):
        q3_ = k/20000
        for ph in (0.0, math.pi/2, math.pi, 1.0):
            U3 = coin(q3_, ph)
            L3 = abs(U3[1][0]*xR+U3[1][1]*xL)**2
            if best is None or abs(L3-L3want) < best[0]: best = (abs(L3-L3want), q3_, ph)
    # refine q3 by bisection around best
    ph = best[2]
    def L3of(q3_):
        U3 = coin(min(max(q3_, 0.0), 1.0), ph); return abs(U3[1][0]*xR+U3[1][1]*xL)**2
    lo3, hi3 = max(best[1]-1/20000, 0.0), min(best[1]+1/20000, 1.0)
    if (L3of(lo3)-L3want)*(L3of(hi3)-L3want) <= 0:
        for _ in range(200):
            mid = (lo3+hi3)/2
            if (L3of(lo3)-L3want)*(L3of(mid)-L3want) <= 0: hi3 = mid
            else: lo3 = mid
    L3 = L3of(lo3)
    Wseq = L3+2*(1-a)*L2+(a*a-1)*L1
    found = abs(Wseq) < 1e-12 and abs(Dseq) < 1e-12
rec("P10_tick_dependent_sequence_outside_class", 1, int(not found), int(found),
    [dict(q1=qa, q2=qb, L1=L1, L2=L2 if br else None, L3=L3 if br else None, F=Fseq, W=Wseq, D=Dseq)],
    note="FAIL means: a clock-dependent unitary sequence with unbalanced first two coins has W=D=0 (residuals shown; tolerance 1e-12)")

# ---------- P11 phase plate ----------
okp = True; vals11 = []
for sg in (1, -1):
    beta = cmath.exp(sg*2j*math.pi/3); k = 1/math.sqrt(2)
    U = [[k, k], [beta*k, -beta*k]]; Pl = [[1, 0], [0, 1j]]
    M = cm(U, cm(Pl, U)); pL = abs(M[1][0])**2
    want = (2+sg*math.sqrt(3))/4
    vals11.append(dict(sign=sg, p=pL, want=want, resid=abs(pL-want), other_entry=abs(M[0][1])**2))
    okp = okp and abs(pL-want) < 1e-12
rec("P11_phase_plate", 2, 2 if okp else 0, 0 if okp else 2, None, note=str(vals11))

out = Path(sys.argv[1]); out.mkdir(parents=True, exist_ok=True)
with (out/"xr74_result.json").open("x", encoding="utf8", newline="\n") as f:
    json.dump(dict(seed=74, predicates=res), f, indent=1, default=str, sort_keys=True); f.write("\n")
for k, v in res.items():
    print(f"{k}: qualify={v['qualify']} pass={v['passed']} fail={v['failed']}")
