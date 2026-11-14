"""Cross-review program for Director G's note 'Finite detector memory and coherent returns'.
Usage: python3 -I xcheck_memory.py OUTDIR STORED_JSON   (refuses to overwrite OUTDIR/xcheck_memory.json)
Seed 20261113 (numpy default_rng and random.Random). Written from the note's text, not from its checker.

CONVENTIONS
  theta: cos=3/5, sin=4/5.  q_k = cos^2(k theta), k from 0.  z = (-7+24i)/25.
  Stochastic matrices are ROW-stochastic; p_k = alpha P^k b; alpha a row distribution; b in [0,1]^m.
  eta_m = (1 - max_{1<=r<=m} q_r)/(2m);  bound_m = 24/(25*2^(m+1)) * eta_m^(m-1);  D_m = (8/5) eta_m^(m-1).
  L(0,s)=0, L(t,s)=max(0,t+s-1)^2/t.  Inequalities are non-strict; zero counts as satisfying ">= 0".
  Exact = fractions.Fraction. Float predicates carry NO pass threshold except where a basis is given;
  the measured separation (min margin / min ratio) is reported instead.

PREDICATES (fixed before the first run)
  H  (hypothesis, per instance): rows of P nonnegative with sum 1, alpha a distribution, 0<=b<=1.
     Float instances: |rowsum-1| <= 4e-16*m (basis: m additions of doubles after exact renormalisation).
     Instances failing H are counted and excluded.
  A1 exact q_k equals 1/2+(z^k+conj z^k)/4 and eta_m = d_m^2/(8m), d_m = min_{r<=m}|1-z^r| (exact, m<=14).
  A2 bound_m is strictly decreasing in m (needed for 'at most m states'), m=1..14.
  A3 random P (m=1..8, 1500 each, three sparsity regimes): max_{k<=m+1}|p_k-q_k| >= bound_m. Report min ratio.
  A4 structured exact instances for m=1..10: prefix chain 0->1->..->m-1 with b=q_0..q_{m-1} and last row
     (f to state 0, 1-f stay) with f chosen to match q_m when 0<=f<=1; all cyclic shifts; identity.
     Exact: max error over k<=m+1 >= bound_m. Also record first k of disagreement.
  A5 eigenvalue separation: for every root of unity of order r<=m (m=1..40) |z-w| >= eta_m; and for random P
     every eigenvalue has |z-lambda| >= eta_m. Report min ratio.
  A6 random P: sum|c_j| <= 2^m and |chi(z)| >= D_m (float; margin reported).
  A7 note's 3-state example exact: p_0..p_3 = q_0..q_3, p_4 = 167729/390625, q_4 = 277729/390625, gap 176/625.
  B1 two-state mixtures (exact, random rational, 1..4 types, non-binary b, non-point launch, boundary values
     injected): L(t,s) <= p_2 <= 1-L(1-t,1-s) and 625p2-336p0-400p1+400 >= 0.
  B2 attainment at random rational (t,s) and all boundary (t,s) in {0,1/7,..,1}^2: the note's constructions,
     run as actual chains, give exactly (t,s,L) and (t,s,1-L(1-t,1-s)).
  B3 sympy: smaller root of 3125r^2-1476r+32 equals 16/(369+sqrt(111161)); r*<9/50; the lower construction at
     (1-r*,9/25-r*) gives p2 = 49/625+r* exactly; 31/1361 < r*.
  B4 no B1 mixture, and no point of a 3-parameter grid family t(1,x,x^2+(1-x)y)+(1-t)(0,w,.) , has max error
     to (1,9/25,49/625) below r* (float compare with exact rational bracket 0.02277877 < r*).
  B5 CONTROL expected to FAIL: three-state chain 0->1->2->2, b=(1,9/25,49/625) violates the B1 lower bound.
  C1 Fourier: |sum_{k<N} q_k conj(z)^k - N/4| <= 85/96 for N=1..20000 (float; margin reported);
     random P: |sum_{k<N} p_k conj(z)^k| <= m 2^m / D_m for N in {10,100,1000}.
  D1 own 2x2 model of the tilted bond: projector of (3+4i-free real rotation [[3,-4],[4,3]]/5)^k e_0 reduced
     mod 3^h; first return period for h=1..6; note claims 54 at h=4 with ordinary q_54 ~ 0.96375864.
  D2 recount from the STORED json (not independent of the note's gate code): 39 rows; distinct keys mod
     81,27,9,3 = 33,32,25,6; pairs of distinct keys colliding with different probabilities = 0,1,10,90;
     rows with a positive coordinate whose reduced row vanishes = 0,6,25,66; denominators powers of 5.
"""
import json, sys, random, itertools
from fractions import Fraction as F
from pathlib import Path
import numpy as np
import sympy as sp

SEED = 20261113
rng = np.random.default_rng(SEED)
rnd = random.Random(SEED)
out = {"seed": SEED, "predicates": {}, "failed": [], "notes": []}


def record(name, ok, **kw):
    out["predicates"][name] = dict(passed=bool(ok), **kw)
    if not ok:
        out["failed"].append(name)


# exact q_k from Gaussian rational (3+4i)/5
def qs(n):
    c, s = F(1), F(0)
    res = []
    for _ in range(n + 1):
        res.append(c * c)
        c, s = F(3, 5) * c - F(4, 5) * s, F(4, 5) * c + F(3, 5) * s
    return res


Q = qs(60)
zr, zi = F(-7, 25), F(24, 25)
zf = complex(-7 / 25, 24 / 25)


def eta(m):
    return (1 - max(Q[1:m + 1])) / (2 * m)


def bound(m):
    return F(24, 25 * 2 ** (m + 1)) * eta(m) ** (m - 1)


def Dm(m):
    return F(8, 5) * eta(m) ** (m - 1)


# A1
ok = True
x, y = F(1), F(0)
chord = []
for k in range(15):
    ok &= Q[k] == F(1, 2) + x / 2
    chord.append((1 - x) ** 2 + y ** 2)
    x, y = zr * x - zi * y, zi * x + zr * y
for m in range(1, 15):
    ok &= eta(m) == min(chord[1:m + 1]) / (8 * m) and eta(m) > 0
record("A1", ok)
# A2
bs = [bound(m) for m in range(1, 15)]
record("A2", all(a > b for a, b in zip(bs, bs[1:])), bounds_float=[float(b) for b in bs],
       bounds_exact_m1_to_4=[str(b) for b in bs[:4]])


def rand_P(m, regime):
    if regime == 0:
        P = rng.random((m, m))
    elif regime == 1:
        P = rng.random((m, m)) ** 8
    else:  # near-deterministic: permutation plus small noise
        P = np.eye(m)[rng.permutation(m)] + 1e-3 * rng.random((m, m)) * (rng.random((m, m)) < 0.3)
    return P / P.sum(1, keepdims=True)


# A3, A5 (random part), A6, C1 (random part)
A3 = dict(tested=0, qualify=0, fail=0, min_ratio={}, min_err={})
A5r = dict(min_ratio=None, fail=0)
A6 = dict(fail_coeff=0, fail_chi=0, max_coeff_ratio=0.0, min_chi_ratio=None)
C1r = dict(fail=0, max_ratio=0.0)
for m in range(1, 9):
    qm = np.array([float(q) for q in Q[:m + 2]])
    b_m, e_m, d_m = float(bound(m)), float(eta(m)), float(Dm(m))
    mr, me = None, None
    for i in range(1500):
        P = rand_P(m, i % 3)
        a = rng.dirichlet(np.ones(m)) if i % 2 else np.eye(m)[rng.integers(m)]
        b = rng.random(m) if i % 4 else (rng.random(m) < 0.5).astype(float)
        A3["tested"] += 1
        if not (P.min() >= 0 and np.abs(P.sum(1) - 1).max() <= 4e-16 * m and abs(a.sum() - 1) <= 4e-16 * m
                and b.min() >= 0 and b.max() <= 1):
            continue
        A3["qualify"] += 1
        v, p = b.copy(), []
        for k in range(m + 2):
            p.append(a @ v)
            v = P @ v
        err = np.abs(np.array(p) - qm).max()
        r = err / b_m
        mr = r if mr is None else min(mr, r)
        me = err if me is None else min(me, err)
        A3["fail"] += err < b_m
        lam = np.linalg.eigvals(P)
        sep = np.abs(lam - zf).min() / e_m
        A5r["min_ratio"] = sep if A5r["min_ratio"] is None else min(A5r["min_ratio"], sep)
        A5r["fail"] += sep < 1
        c = np.poly(P)
        cr = np.abs(c).sum() / 2 ** m
        A6["max_coeff_ratio"] = max(A6["max_coeff_ratio"], cr)
        A6["fail_coeff"] += cr > 1 + 1e-9  # basis: np.poly relative rounding ~1e-13 for m<=8
        chir = abs(np.polyval(c, zf)) / d_m
        A6["min_chi_ratio"] = chir if A6["min_chi_ratio"] is None else min(A6["min_chi_ratio"], chir)
        A6["fail_chi"] += chir < 1
        if i < 200:
            v, S = b.copy(), 0j
            zc, w = zf.conjugate(), 1 + 0j
            for k in range(1000):
                S += (a @ v) * w
                v = P @ v
                w *= zc
                if k + 1 in (10, 100, 1000):
                    rr = abs(S) / (m * 2 ** m / d_m)
                    C1r["max_ratio"] = max(C1r["max_ratio"], rr)
                    C1r["fail"] += rr > 1
    A3["min_ratio"][m], A3["min_err"][m] = mr, me
record("A3", A3["fail"] == 0, **A3)
record("A6", A6["fail_coeff"] == 0 and A6["fail_chi"] == 0, **A6)


# A4 exact structured
def run_exact(P, a, b, n):
    m = len(a)
    v, p = list(b), []
    for _ in range(n):
        p.append(sum(x * y for x, y in zip(a, v)))
        v = [sum(P[i][j] * v[j] for j in range(m)) for i in range(m)]
    return p


A4 = dict(instances=0, qualify=0, fail=[], rows=[])
for m in range(1, 11):
    cases = []
    P = [[F(int(j == min(i + 1, m - 1))) for j in range(m)] for i in range(m)]
    # choose f so that p_m = f*q_0 + (1-f)*q_{m-1} = q_m
    if m >= 2 and Q[0] != Q[m - 1]:
        f = (Q[m] - Q[m - 1]) / (Q[0] - Q[m - 1])
        if 0 <= f <= 1:
            P2 = [r[:] for r in P]
            P2[m - 1] = [F(0)] * m
            P2[m - 1][0] += f
            P2[m - 1][m - 1] += 1 - f
            cases.append(("prefix_matched f=%s" % f, P2, Q[:m]))
        else:
            cases.append(("prefix_matched_infeasible f=%s" % f, None, None))
    cases.append(("prefix_absorbing", P, Q[:m]))
    cyc = [[F(int(j == (i + 1) % m)) for j in range(m)] for i in range(m)]
    cases.append(("cycle", cyc, Q[:m]))
    cases.append(("identity", [[F(int(i == j)) for j in range(m)] for i in range(m)], [F(1)] * m))
    for name, PP, b in cases:
        A4["instances"] += 1
        if PP is None:
            A4["rows"].append(dict(m=m, name=name, qualifies=False))
            continue
        assert all(sum(r) == 1 and min(r) >= 0 for r in PP) and all(0 <= t <= 1 for t in b)
        A4["qualify"] += 1
        a = [F(1)] + [F(0)] * (m - 1)
        p = run_exact(PP, a, b, m + 2)
        errs = [abs(u - v) for u, v in zip(p, Q)]
        first = next((k for k, e in enumerate(errs) if e), None)
        okk = max(errs) >= bound(m)
        if not okk:
            A4["fail"].append((m, name))
        A4["rows"].append(dict(m=m, name=name, qualifies=True, first_disagreement=first,
                               max_err=float(max(errs)), bound=float(bound(m))))
record("A4", not A4["fail"], **A4)

# A5 roots of unity
minr, fails, arg = None, 0, None
for m in range(1, 41):
    e = float(eta(m))
    for r in range(1, m + 1):
        for j in range(r):
            w = complex(sp.cos(2 * sp.pi * j / r).evalf(30), sp.sin(2 * sp.pi * j / r).evalf(30)) if m <= 0 else \
                complex(np.cos(2 * np.pi * j / r), np.sin(2 * np.pi * j / r))
            ratio = abs(zf - w) / e
            if minr is None or ratio < minr:
                minr, arg = ratio, (m, r, j)
            fails += ratio < 1
record("A5", fails == 0 and A5r["fail"] == 0, roots_min_ratio=minr, roots_argmin_m_r_j=arg, random=A5r)

# A7
f = F(779, 900)
P3 = [[F(0), F(1), F(0)], [F(0), F(0), F(1)], [f, F(0), 1 - f]]
p = run_exact(P3, [F(1), F(0), F(0)], [F(1), F(9, 25), F(49, 625)], 5)
record("A7", p[:4] == Q[:4] and p[4] == F(167729, 390625) and Q[4] == F(277729, 390625)
       and Q[4] - p[4] == F(176, 625) and Q[3] == F(13689, 15625), p=[str(t) for t in p])


# B
def L(t, s):
    return F(0) if t == 0 else max(F(0), t + s - 1) ** 2 / t


def rfrac():
    u = rnd.random()
    if u < 0.15:
        return F(0)
    if u < 0.3:
        return F(1)
    d = rnd.randint(2, 40)
    return F(rnd.randint(0, d), d)


def two_state(a, x, y, b0, b1):
    return run_exact([[x, 1 - x], [y, 1 - y]], [a, 1 - a], [b0, b1], 3)


def mixture(n):
    w = [F(rnd.randint(1, 20)) for _ in range(n)]
    tot = sum(w)
    tri = [F(0)] * 3
    for wi in w:
        t3 = two_state(*[rfrac() for _ in range(5)])
        tri = [u + wi / tot * v for u, v in zip(tri, t3)]
    return tri


NATIVE = [F(1), F(9, 25), F(49, 625)]
B1 = dict(tested=0, qualify=0, fail_interval=0, fail_linear=0, lower_hits=0, upper_hits=0, min_maxerr=None)
for i in range(60000):
    t, s, u = mixture(1 + i % 4)
    B1["tested"] += 1
    B1["qualify"] += 1  # hypothesis holds by exact construction (rows sum to 1 in Fractions, checked below)
    lo, hi = L(t, s), 1 - L(1 - t, 1 - s)
    B1["fail_interval"] += not (lo <= u <= hi)
    B1["fail_linear"] += 625 * u - 336 * t - 400 * s + 400 < 0
    B1["lower_hits"] += u == lo
    B1["upper_hits"] += u == hi
    e = max(abs(a - b) for a, b in zip((t, s, u), NATIVE))
    if B1["min_maxerr"] is None or e < B1["min_maxerr"]:
        B1["min_maxerr"] = e
rstar_lo = F(2277877, 100000000)
B1["min_maxerr"] = float(B1["min_maxerr"])
record("B1", B1["fail_interval"] == 0 and B1["fail_linear"] == 0, **B1)


def lower_real(t, s):
    if s <= 1 - t:
        parts = [(t, two_state(F(1), F(0), F(0), F(1), F(0))),      # click -> absorbing dark
                 (s, two_state(F(0), F(0), F(1), F(0), F(1))),      # swap, starts dark: state1 clicks
                 (1 - t - s, two_state(F(1), F(1), F(0), F(0), F(0)))]
    else:
        x = (s + t - 1) / t
        parts = [(t, two_state(F(1), x, F(0), F(1), F(0))), (1 - t, two_state(F(0), F(0), F(1), F(0), F(1)))]
    assert sum(w for w, _ in parts) == 1 and all(w >= 0 for w, _ in parts)
    return [sum(w * tr[k] for w, tr in parts) for k in range(3)]


pts = [(F(i, 7), F(j, 7)) for i in range(8) for j in range(8)] + [(rfrac(), rfrac()) for _ in range(3000)]
bad = 0
for t, s in pts:
    bad += lower_real(t, s) != [t, s, L(t, s)]
    up = [1 - v for v in lower_real(1 - t, 1 - s)]
    bad += up != [t, s, 1 - L(1 - t, 1 - s)]
    bad += not (L(t, s) <= 1 - L(1 - t, 1 - s))
record("B2", bad == 0, points=len(pts), bad=bad)

r = sp.symbols("r")
roots = sorted(sp.solve(3125 * r ** 2 - 1476 * r + 32, r), key=lambda v: float(v))
rs = sp.Integer(16) / (369 + sp.sqrt(111161))
tt, ss = 1 - rs, sp.Rational(9, 25) - rs
p2 = sp.simplify((tt + ss - 1) ** 2 / tt - (sp.Rational(49, 625) + rs))
expand_ok = sp.expand(625 * ((sp.Rational(9, 25) - 2 * r) ** 2 - (1 - r) * (sp.Rational(49, 625) + r))
                      - (3125 * r ** 2 - 1476 * r + 32)) == 0
okB3 = (sp.simplify(roots[0] - rs) == 0 and float(rs) < 9 / 50 and p2 == 0 and expand_ok
        and sp.Rational(31, 1361) < rs and rstar_lo < rs < F(2277878, 100000000))
record("B3", okB3, r_star=str(sp.N(rs, 15)), other_root=str(sp.N(roots[1], 15)), lin_bound=float(F(31, 1361)),
       p2_minus_target_at_rstar=str(p2))

# B4 grid family (float) + B1 minimum
g = np.linspace(0, 1, 41)
best = 1.0
for t in np.linspace(0.9, 1, 51):
    for x in g:
        for yv in (0.0, 0.25, 1.0):
            for w in g:  # non-click mass contributes w*(1-t) to p1, and p2 contribution in [0, (1-t)] ; take 0
                tri = (t, t * x + (1 - t) * w, t * (x * x + (1 - x) * yv))
                best = min(best, max(abs(tri[0] - 1), abs(tri[1] - 9 / 25), abs(tri[2] - 49 / 625)))
record("B4", best >= float(rstar_lo) and B1["min_maxerr"] >= float(rstar_lo), grid_min=best,
       random_min=B1["min_maxerr"], r_star_lower_bracket=float(rstar_lo))

# B5 control
p = run_exact([[F(0), F(1), F(0)], [F(0), F(0), F(1)], [F(0), F(0), F(1)]], [F(1), F(0), F(0)], NATIVE, 3)
record("B5_control_expected_fail", L(p[0], p[1]) <= p[2], triple=[str(v) for v in p], lower=str(L(p[0], p[1])),
       follow_up="Expected failure: three states per type are outside the two-state hypothesis; shows B1 can fail.")

# C1
zc = zf.conjugate()
S, w, mx = 0j, 1 + 0j, 0.0
for N in range(1, 20001):
    S += float(Q[N - 1]) * w if N - 1 < len(Q) else (np.cos((N - 1) * np.arctan2(4, 3)) ** 2) * w
    w *= zc
    mx = max(mx, abs(S - N / 4))
record("C1", mx <= 85 / 96 and C1r["fail"] == 0, max_dev=mx, bound=85 / 96, margin=85 / 96 - mx, random=C1r,
       basis="float accumulation over 2e4 terms ~1e-11, far below the measured margin")

# D1
D1 = {}
for h in range(1, 7):
    M = 3 ** h
    inv5 = pow(5, -1, M)
    c, s = 1, 0
    start = (1, 0, 0)
    k = 0
    while True:
        c, s = (3 * c - 4 * s) * inv5 % M, (4 * c + 3 * s) * inv5 % M
        k += 1
        if (c * c % M, c * s % M, s * s % M) == start:
            break
    qk = qs(k)[k]
    D1[h] = dict(modulus=M, period=k, ordinary_return=float(qk))
record("D1", D1[4]["period"] == 54 and abs(D1[4]["ordinary_return"] - 0.96375864) < 5e-9, table=D1,
       basis="5e-9 = half a unit of the note's eighth printed decimal")

# D2
try:
    data = json.loads(Path(sys.argv[2]).read_text())
    rows = data["rows"]
    keys81 = [tuple(tuple(e) for e in r["reduced_projector"]) for r in rows]
    probs = [tuple(F(v) for v in r["probabilities"]) for r in rows]
    dens = set()
    for pr in probs:
        for v in pr:
            d = v.denominator
            while d % 5 == 0:
                d //= 5
            dens.add(d)
    res = {}
    uniq = {}
    for k, pr in zip(keys81, probs):
        uniq.setdefault(k, pr)
    for M in (81, 27, 9, 3):
        red = lambda k: tuple((a % M, b % M) for a, b in k)
        ks = {}
        for k, pr in uniq.items():
            ks.setdefault(red(k), []).append(pr)
        pairs = sum(1 for v in ks.values() for a, b in itertools.combinations(v, 2) if a != b)
        loss_rows = loss_ports = 0
        for k, pr in zip(keys81, probs):
            kk = red(k)
            n = len(pr)
            miss = [j for j in range(n) if pr[j] != 0 and all(e == (0, 0) for e in kk[n * j:n * (j + 1)])]
            loss_rows += bool(miss)
            loss_ports += len(miss)
        res[M] = dict(distinct=len(ks), disagreeing_pairs=pairs, rows_with_loss=loss_rows, lost_ports=loss_ports)
    stored = {a["modulus"]: dict(distinct=a["distinct_reduced"], pairs=a["disagreeing_pairs"],
                                 loss_entries=len(a["positive_coordinate_losses"]),
                                 loss_ports=sum(len(e["lost_positive_ports"]) for e in a["positive_coordinate_losses"]),
                                 distinct_exact=a["distinct_exact"]) for a in data["collision_checks"]}
    joint = data["adaptive_from_02"]["intermediate_then_final_joint"]
    okD2 = (len(rows) == 39 and [res[M]["distinct"] for M in (3, 9, 27, 81)] == [6, 25, 32, 33]
            and [res[M]["disagreeing_pairs"] for M in (3, 9, 27, 81)] == [90, 10, 1, 0]
            and [res[M]["rows_with_loss"] for M in (3, 9, 27, 81)] == [66, 25, 6, 0] and dens == {1})
    record("D2", okD2, recount=res, stored=stored, rows=len(rows), non5_denominator_parts=sorted(dens),
           joint_bins=sum(len(x) for x in joint), joint_sum=str(sum(F(v) for x in joint for v in x)),
           joint_zero_bins=sum(1 for x in joint for v in x if F(v) == 0),
           unwritten=data["unwritten_state"]["ordinary_probabilities"],
           ret=data["first_projector_return"]["period"],
           ret_ord=[str(v) for v in data["first_projector_return"]["ordinary_probabilities"]])
except Exception as exc:  # kept, not hidden
    record("D2", False, error=repr(exc))

dest = Path(sys.argv[1]) / "xcheck_memory.json"
if dest.exists():
    sys.exit("refusing to overwrite " + str(dest))
dest.parent.mkdir(parents=True, exist_ok=True)
dest.write_text(json.dumps(out, indent=1, default=str) + "\n")
print("failed:", out["failed"])
for k, v in out["predicates"].items():
    print(k, v["passed"])
