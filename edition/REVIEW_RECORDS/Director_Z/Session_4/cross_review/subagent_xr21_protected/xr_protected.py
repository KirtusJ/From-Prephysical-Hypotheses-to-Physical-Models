"""Cross-review program for Director_G/Protected_records_and_coordinate_weights.md.
Own reconstruction from the note's text; the author's code is not imported.
Exact integer / Fraction arithmetic only. Seed 20261113. Refuses to overwrite its result file.

Conventions: H(a,b)=(a+b,a-b)/sqrt2 on an ORDERED pair; a state is (integer numerators, depth k),
meaning numerators/sqrt(2)^k. Logical index = (sel*d+cell)*2+priv, sel 0=A 1=B. Ring mode = 2*site+c,
c=0 right-mover R, c=1 left-mover L; U=S H, S moves R to site+1 and L to site-1.

PREDICATES (fixed before the first run)
A. Two coherent preparations (hypothesis per instance: x,y integer, same width, both norms 2^t, same t).
 A1 route X (x supplied in A; B half gets U_y U_x^-1; A half does private Hadamards) ends in exactly
    (x,y)/sqrt2 with private bit blank; same for route Y (y supplied in B); the two FULL final vectors
    are equal entry by entry, and their depths (clock counts) are equal.
 A2 under the quadratic rule the protected subset {(A,i,priv 0/1)} (route X) / {(B,j,*)} (route Y)
    has constant mass at every layer.
 A3 (measured, not pass/fail) what still distinguishes the two preparations: initial vector, gate word.
 A4 (measured) number of instances in which the globally normalised fourth-power rule changes a
    protected mass somewhere along a route.
B. Stated numbers: 81/88, 162/239, 1/20, 1/8, 1/40, 1/16, 1/28, 5/16.
C. Eight-coordinate calibration, t=0..16 (15,16 are not reported by the note). For each t:
 C1 every 1<=n<b has a four-square representation of S-2n^2-2 and both rows have norm S;
 C2 every b<n<=sqrt S has a four-square representation of S-n^2 with all fillers <= b;
 C3 the normaliser row (two entries 2^((t-1)/2), or four entries 2^(t/2-1)) has norm S, entries <= b;
 C4 solving the linear relations with f(0)=0 symbolically in f(1) gives f(n)=n^2/S for all n;
 C5 every row used is exactly synthesizable by my parity fold (reaches one +-1 in t layers).
 (measured) counts of reference pairs and signed cases through t=14, to compare with 424 and 877.
D. Single-rail modulo-two obstruction (hypothesis per instance: N has an odd divisor >1).
 D1 for random forward-only controlled words (site-dependent swap before/after coin, signs before/after
    coin), length 1..40, the numerator matrix mod 2 equals (z+1/z)^(t-1) diag(z,1/z) K;
 D2 for qualifying N every column of every such word has an odd numerator at t>=1, hence no localized
    input reaches one basis port (also checked directly: no column is a single nonzero entry).
 D3 (measured) non-qualifying N=4,8,16: first t at which U^t numerators are all even; U^24=I on N=8.
E. Doubled rail (N including 12 and 14, not reported by the note): W=diag(U,U^T), J rail exchange.
 E1 J W J W = I exactly; so a localized input returns to one basis port at positive depth 2,
    i.e. the conclusion of D fails there although N has an odd divisor.
 E2 pre-coin switch: (J W J)(W with X_x before coin) = X_x on the plus rail, minus rail blank at end;
    post-coin: (W with X_x after coin)(J W J) = S X_x S^-1 on the plus rail, minus rail blank at end.
 E3 omitting one J fails E1 (control, expected to fail; kept).
F. Stored author result results/local_comparison_router.json read as data: (measured) are the two
   routes' 128 physical numerators identical; are the per-stage expanded-word digests identical.
"""
import json, random, sys, os
from fractions import Fraction as Fr
from math import isqrt

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "xr_protected_result_run2.json")
if os.path.exists(OUT):
    sys.exit("result file exists; refusing to overwrite")
random.seed(20261113)
R = {"met": [], "failed": [], "measured": {}}
def pred(name, ok, info=None):
    (R["met"] if ok else R["failed"]).append({"name": name, "info": info})

# ---------- parity fold ----------
def fold(v, t):
    """layers (ordered matchings) reducing numerators v (norm 2^t) to +-e_r; returns layers, r, sign"""
    v = list(v); layers = []
    for rem in range(t, 0, -1):
        if sum(a*a for a in v) != 2**rem: return None
        odd = [i for i, a in enumerate(v) if a % 2]; ev = [i for i, a in enumerate(v) if a % 2 == 0]
        if len(odd) % 2 or len(ev) % 2: return None
        seq = odd + ev; pairs = [(seq[2*k], seq[2*k+1]) for k in range(len(seq)//2)]
        w = v[:]
        for a, b in pairs:
            s, d_ = v[a] + v[b], v[a] - v[b]
            if s % 2 or d_ % 2: return None
            w[a], w[b] = s // 2, d_ // 2
        v = w; layers.append(pairs)
    nz = [i for i, a in enumerate(v) if a]
    if len(nz) != 1 or abs(v[nz[0]]) != 1: return None
    return layers, nz[0], v[nz[0]]

def norm_state(v, k):
    v = list(v)
    while k >= 2 and all(a % 2 == 0 for a in v):
        v = [a // 2 for a in v]; k -= 2
    return v, k

def quartic_mass(v, subset):
    tot = sum(a**4 for a in v)
    return Fr(sum(v[i]**4 for i in subset), tot)
def quad_mass(v, k, subset):
    return Fr(sum(v[i]**2 for i in subset), 2**k)

FLIP = 0
def route(x, y, t, src):
    """src='X': x supplied in A, active half B.  src='Y': y supplied in B, active half A."""
    d = len(x); n = 4 * d
    idx = lambda s, c, p: (s * d + c) * 2 + p
    fx, fy = fold(x, t), fold(y, t)
    v = [0] * n; k = t; word = []
    if src == 'X':
        for c in range(d): v[idx(0, c, 0)] = x[c]
        act, pas, ffrom, fto = 1, 0, fx, fy
    else:
        for c in range(d): v[idx(1, c, 0)] = y[c]
        act, pas, ffrom, fto = 0, 1, fy, fx
    init = v[:]
    prot = [[idx(pas, c, 0), idx(pas, c, 1)] for c in range(d)]
    def layer(pairs, tag):
        nonlocal v, k
        assert sorted(i for p in pairs for i in p) == list(range(n))
        w = v[:]
        for a, b in pairs: w[a], w[b] = v[a] + v[b], v[a] - v[b]
        v = w; k += 1; word.append([tag, pairs])
    hist = []
    def snap(): hist.append(([quad_mass(v, k, s) for s in prot], [quartic_mass(v, s) for s in prot]))
    # selector split: ordered pair (A,c,0),(B,c,0); private-1 slots paired across selector (blank)
    # FOLLOW-UP to run 1 (A1 failed 40/40, kept in xr_protected_result_run1_A1failed.json): the ordered pair
    # must have the SUPPLIED half first; with (A,B) order route Y gives (y,-y), i.e. (x,-y) at the end.
    # FLIP=1 reproduces run 1's order as a retained control.
    o = (pas, act) if not FLIP else (0, 1)
    layer([(idx(o[0], c, 0), idx(o[1], c, 0)) for c in range(d)] + [(idx(o[0], c, 1), idx(o[1], c, 1)) for c in range(d)], "split")
    snap()
    priv = [(idx(pas, c, 0), idx(pas, c, 1)) for c in range(d)]
    def act_layer(pairs):
        layer([(idx(act, a, 0), idx(act, b, 0)) for a, b in pairs] + [(idx(act, a, 1), idx(act, b, 1)) for a, b in pairs] + priv, "active")
        snap()
    for pairs in ffrom[0]: act_layer(pairs)
    # signed permutation in the active half: root of source column -> root of target column
    r1, s1, r2, s2 = ffrom[1], ffrom[2], fto[1], fto[2]
    a, b = idx(act, r1, 0), idx(act, r2, 0)
    v[a], v[b] = v[b], v[a]
    if s1 * s2 < 0: v[b] = -v[b]
    word.append(["signed_perm", [a, b, s1 * s2]]); snap()
    for pairs in reversed(fto[0]): act_layer(pairs)
    return init, v, k, word, hist

def check_pair(x, y, t, name):
    d = len(x)
    if not (len(y) == d and d % 2 == 0 and sum(a*a for a in x) == 2**t == sum(a*a for a in y)
            and fold(x, t) and fold(y, t)):
        return None
    iX, vX, kX, wX, hX = route(x, y, t, 'X'); iY, vY, kY, wY, hY = route(x, y, t, 'Y')
    exp = [0] * (4 * d)
    for c in range(d): exp[2 * c] = x[c]; exp[2 * (d + c)] = y[c]
    e = norm_state(exp, t + 1)
    a1 = norm_state(vX, kX) == e and norm_state(vY, kY) == e and vX == vY and kX == kY
    global FLIP
    FLIP = 1; _, vF, kF, _, _ = route(x, y, t, 'Y'); FLIP = 0
    ctrl = dict(run1_order_routeY_equals_expected=norm_state(vF, kF) == e,
                run1_order_routeY_is_x_minus_y=norm_state(vF, kF) == norm_state([a if i < 2*d else -a for i, a in enumerate(exp)], t + 1),
                routeX_ok=norm_state(vX, kX) == e)
    a2 = all(h[0] == hX[0][0] for h in hX) and all(h[0] == hY[0][0] for h in hY)
    a4 = any(h[1] != hX[0][1] for h in hX) or any(h[1] != hY[0][1] for h in hY)
    return dict(name=name, A1=a1, A2=a2, quartic_changes=a4, init_differs=iX != iY, word_differs=wX != wY,
                layers=(len(wX), len(wY)), equal_entries=len(set(x) & set(y)) > 0,
                hist_len=len(hX), ctrl=ctrl)

def rand_col(d, t):
    v = [0] * d; v[random.randrange(d)] = random.choice([1, -1])
    for _ in range(t):
        p = list(range(d)); random.shuffle(p); w = v[:]
        for j in range(0, d, 2):
            a, b = p[j], p[j+1]; w[a], w[b] = v[a] + v[b], v[a] - v[b]
        v = w
        # one unnormalised H doubles the norm; keep raw numerators over sqrt(2)^steps
    return v

cases = [([2, 1, 1, 1, 1, 0, 0, 0], [1]*8, 3, "note_end_to_end"),
         ([2, 1, 1, 1, 1, 0, 0, 0], [2, 2, 0, 0, 0, 0, 0, 0], 3, "x_vs_two_twos"),
         ([3, 1, 1, 1, 1, 1, 1, 1], [2, 2, 2, 2, 0, 0, 0, 0], 4, "three_vs_four_twos"),
         ([1, 1], [1, -1], 1, "depth1"),
         ([2, 1, 1, 1, 1, 0, 0, 0], [1]*7 + [0], 3, "nonqualifying_norm7_control")]
for t in range(1, 7):
    for r in range(6):
        cases.append((rand_col(8, t), rand_col(8, t), t, f"random_t{t}_{r}"))
qual = []; nonq = 0
for x, y, t, name in cases:
    r = check_pair(x, y, t, name)
    if r is None: nonq += 1; continue
    qual.append(r)
R["measured"]["A_instances"] = dict(total=len(cases), qualifying=len(qual), nonqualifying=nonq,
    with_equal_signed_entry=sum(r["equal_entries"] for r in qual),
    initial_vectors_differ=sum(r["init_differs"] for r in qual),
    gate_words_differ=sum(r["word_differs"] for r in qual),
    layer_counts_equal=sum(r["layers"][0] == r["layers"][1] for r in qual),
    quartic_changes_protected_mass=sum(r["quartic_changes"] for r in qual),
    quartic_unchanged_names=[r["name"] for r in qual if not r["quartic_changes"]],
    run1_order_control=dict(routeY_wrong=sum(not r["ctrl"]["run1_order_routeY_equals_expected"] for r in qual),
        routeY_is_x_minus_y=sum(r["ctrl"]["run1_order_routeY_is_x_minus_y"] for r in qual), routeX_ok=sum(r["ctrl"]["routeX_ok"] for r in qual)))
pred("A1 full final vectors equal and equal (x,y)/sqrt2, private blank, equal depth",
     all(r["A1"] for r in qual), [r["name"] for r in qual if not r["A1"]])
pred("A2 quadratic protected masses constant", all(r["A2"] for r in qual), [r["name"] for r in qual if not r["A2"]])

# ---------- B ----------
big = [3] + [1]*7
b1 = Fr(81, sum(a**4 for a in big)) == Fr(81, 88)
# herald refinement: L=3, D=4, m=3; coordinate a: a^2 success entries of m/(a D), F=D^2-m^2 failure entries 1/D
fine = []
for ci, a in enumerate(big):
    fine += [(ci, Fr(a) * Fr(3, a * 4))] * (a * a) + [(ci, Fr(a) * Fr(1, 4))] * 7
assert sum(v*v for _, v in fine) == sum(a*a for a in big)
tot4 = sum(v**4 for _, v in fine)
b2 = sum(v**4 for c, v in fine if c == 0) / tot4 == Fr(162, 239)
x = [2, 1, 1, 1, 1, 0, 0, 0]; y = [1]*8
qx = Fr(1, sum(a**4 for a in x)); qy = Fr(1, sum(a**4 for a in y)); qj = Fr(1, sum(a**4 for a in x + y))
b3 = (qx, qy, qx/2, qy/2, qj) == (Fr(1, 20), Fr(1, 8), Fr(1, 40), Fr(1, 16), Fr(1, 28))
b4 = Fr(2*2 + 1*1, 2**4) == Fr(5, 16)
pred("B 81/88", b1); pred("B 162/239", b2, str(sum(v**4 for c, v in fine if c == 0) / tot4))
pred("B 1/20,1/8,1/40,1/16,1/28", b3); pred("B 5/16 from counts (2,1,0,0,0) at t=4 (arithmetic only)", b4)

# ---------- C ----------
def four_sq(m, cap=None):
    lim = isqrt(m) if cap is None else min(cap, isqrt(m))
    for p in range(lim, -1, -1):
        r1 = m - p*p
        if r1 < 0: continue
        for q in range(min(p, isqrt(r1)), -1, -1):
            r2 = r1 - q*q
            for r in range(min(q, isqrt(r2)), -1, -1):
                r3 = r2 - r*r; s = isqrt(r3)
                if s*s == r3 and s <= r: return (p, q, r, s)
    return None
C = {k: True for k in ("C1", "C2", "C3", "C4", "C5")}; cfail = []
pairs14 = large14 = signed14 = 0; perdepth = {}
for t in range(0, 17):
    S = 2**t; b = isqrt(S // 2); top = isqrt(S)
    if t == 0:
        perdepth[t] = dict(S=1, b=0, pairs=0, large=0); signed14 += 3; continue
    coef = {0: Fr(0), 1: Fr(1)}   # f(n) = coef[n]*f(1)
    npairs = nlarge = 0
    for n in range(1, b):
        rep = four_sq(S - 2*n*n - 2)
        if rep is None: C["C1"] = False; cfail.append(("C1", t, n)); continue
        r1 = [n+1, n-1, 0, 0, *rep]; r2 = [n, n, 1, 1, *rep]
        if sum(a*a for a in r1) != S or sum(a*a for a in r2) != S: C["C1"] = False; cfail.append(("C1n", t, n))
        if t <= 12 or n % 97 == 1:
            if not (fold(r1, t) and fold(r2, t)): C["C5"] = False; cfail.append(("C5", t, n))
        coef[n+1] = 2*coef[n] + 2*coef[1] - coef[n-1]; npairs += 1
    nz = [2**((t-1)//2)]*2 + [0]*6 if t % 2 else [2**(t//2-1)]*4 + [0]*4
    if sum(a*a for a in nz) != S or max(nz) > b or not fold(nz, t): C["C3"] = False; cfail.append(("C3", t))
    f1 = 1 / sum(coef[a] for a in nz if a)
    for n in range(b+1, top+1):
        rep = four_sq(S - n*n)
        if rep is None or max(rep) > b: C["C2"] = False; cfail.append(("C2", t, n)); continue
        row = [n, *rep, 0, 0, 0]
        if t <= 12 or n % 97 == 1:
            if not fold(row, t): C["C5"] = False; cfail.append(("C5L", t, n))
        coef[n] = (1 - sum(coef[a]*f1 for a in rep)) / f1; nlarge += 1
    for n in range(0, top+1):
        if n not in coef or coef[n]*f1 != Fr(n*n, S): C["C4"] = False; cfail.append(("C4", t, n))
    perdepth[t] = dict(S=S, b=b, pairs=npairs, large=nlarge)
    if t <= 14: pairs14 += npairs; large14 += nlarge; signed14 += 2*top + 1
for k_, v_ in C.items(): pred(k_ + " t=0..16", v_, [c for c in cfail if c[0].startswith(k_)][:10])
R["measured"]["C_counts_through_t14"] = dict(small_range_pairs=pairs14, large_range_rows=large14,
    normaliser_rows=14, signed_depth_value_cases=signed14, note_says=dict(reference_pair_compilations=424, signed_cases=877),
    C5_scope="fold run on every row for t<=12 and on a 1-in-97 sample for t=13..16")
R["measured"]["C_per_depth"] = perdepth

# ---------- D, E ----------
def tick(v, N, pre=None, post=None, sgn_pre=None, sgn_post=None, transpose=False):
    """plus rail U = S (post) H (pre);   transpose rail U^T = (pre)^T H (post)^T S^-1 ; integer numerators"""
    def X(v, sites):
        v = v[:]
        for s in sites or (): v[2*s], v[2*s+1] = v[2*s+1], v[2*s]
        return v
    def Z(v, modes):
        v = v[:]
        for m in modes or (): v[m] = -v[m]
        return v
    def H(v):
        w = v[:]
        for s in range(N): w[2*s], w[2*s+1] = v[2*s] + v[2*s+1], v[2*s] - v[2*s+1]
        return w
    def S(v, inv=False):
        w = [0]*(2*N); dlt = -1 if inv else 1
        for s in range(N): w[2*((s+dlt) % N)] = v[2*s]; w[2*((s-dlt) % N)+1] = v[2*s+1]
        return w
    if not transpose:
        return S(X(Z(H(Z(X(v, pre), sgn_pre)), sgn_post), post))
    return Z(X(H(X(Z(S(v, inv=True), sgn_post), post)), pre), sgn_pre)

def odd_div(N):
    while N % 2 == 0: N //= 2
    return N > 1
def polymul(a, b, N):
    c = [0]*N
    for i, ai in enumerate(a):
        if ai:
            for j, bj in enumerate(b):
                if bj: c[(i+j) % N] ^= 1
    return c
D = dict(words=0, qualifying_words=0, D1_fail=[], D2_fail=[], nonqual_single_port=[])
for N in (3, 5, 6, 7, 9, 10, 12, 14, 18, 20, 4, 8, 16):
    q = odd_div(N); zz = [0]*N; zz[1] ^= 1; zz[N-1] ^= 1
    for trial in range(12):
        T = random.randint(1, 40)
        cols = []
        for start in (0, 1):
            pass
        ctrl = [dict(pre=random.sample(range(N), random.randint(0, N)), post=random.sample(range(N), random.randint(0, N)),
                     sgn_pre=random.sample(range(2*N), random.randint(0, 2*N)), sgn_post=random.sample(range(2*N), random.randint(0, 2*N)))
                for _ in range(T)]
        D["words"] += 1; D["qualifying_words"] += q
        pw = [1] + [0]*(N-1)
        for _ in range(T-1): pw = polymul(pw, zz, N)
        for start in (0, 1):
            v = [0]*(2*N); v[start] = 1
            for c in ctrl: v = tick(v, N, **c)
            # predicted mod 2: coin row R gets z*pw, row L gets z^-1*pw (independent of input coin)
            predR = [pw[(s-1) % N] for s in range(N)]; predL = [pw[(s+1) % N] for s in range(N)]
            got = [a % 2 for a in v]
            if got != [predR[s] if c == 0 else predL[s] for s in range(N) for c in (0, 1)]: D["D1_fail"].append((N, trial, start))
            single = sum(1 for a in v if a) == 1
            if q and (not any(got) or single): D["D2_fail"].append((N, trial, start, T))
            if not q and single: D["nonqual_single_port"].append((N, T))
pred("D1 mod-2 power formula on all words", not D["D1_fail"], D["D1_fail"][:5])
pred("D2 odd numerator in every column, no single-port output (qualifying N)", not D["D2_fail"], D["D2_fail"][:5])
alle = {}
for N in (4, 8, 16, 6, 12):
    v = [0]*(2*N); v[0] = 1; first = None
    for t in range(1, 200):
        v = tick(v, N)
        if all(a % 2 == 0 for a in v): first = t; break
    alle[N] = first
v = [0]*16; v[0] = 1
for t in range(24): v = tick(v, 8)
u24 = all(tick_col == (2**12 if i == j else 0) for j in (0,) for i, tick_col in enumerate(v))
cols_ok = True
for j in range(16):
    v = [0]*16; v[j] = 1
    for t in range(24): v = tick(v, 8)
    cols_ok &= v == [2**12 if i == j else 0 for i in range(16)]
D["first_t_with_all_even_column_from_R0"] = alle; D["U24_identity_N8_all_columns"] = cols_ok
R["measured"]["D"] = {k: (v if not isinstance(v, list) else v[:10]) for k, v in D.items()}

E = dict(E1_fail=[], E2_fail=[], E3_control_failed_as_expected=[], E3_control_passed=[])
for N in (2, 6, 10, 12, 14, 18):
    def W(vp, vm, **c): return tick(vp, N, **c), tick(vm, N, transpose=True, **c)
    for j in range(4*N):
        vp = [0]*(2*N); vm = [0]*(2*N)
        (vp if j < 2*N else vm)[j % (2*N)] = 1
        p0, m0 = vp[:], vm[:]
        a, b = W(vp, vm); a, b = b, a; a, b = W(a, b); a, b = b, a      # W, J, W, J  == J W J W
        if (a, b) != ([2*z for z in p0], [2*z for z in m0]): E["E1_fail"].append((N, j))
        a, b = W(vp, vm); a, b = W(a, b); a, b = b, a                    # one J omitted
        (E["E3_control_passed"] if (a, b) == ([2*z for z in p0], [2*z for z in m0]) else E["E3_control_failed_as_expected"]).append((N, j))
    for xsite in range(N):
        for j in range(2*N):
            vp = [0]*(2*N); vp[j] = 1; vm = [0]*(2*N)
            a, b = W(vp, vm, pre=[xsite]); a, b = b, a; a, b = W(a, b); a, b = b, a
            want = vp[:]; want[2*xsite], want[2*xsite+1] = want[2*xsite+1], want[2*xsite]
            if a != [2*z for z in want] or any(b): E["E2_fail"].append(("pre", N, xsite, j))
            a, b = vm, vp; a, b = W(a, b); a, b = b, a; a, b = W(a, b, post=[xsite])   # J W J then switched W
            want = vp[:]; r_, l_ = 2*((xsite+1) % N), 2*((xsite-1) % N)+1
            want[r_], want[l_] = want[l_], want[r_]
            if a != [2*z for z in want] or any(b): E["E2_fail"].append(("post", N, xsite, j))
pred("E1 JWJW=I exactly, N in 2,6,10,12,14,18 (localized input returns to one port at depth 2)", not E["E1_fail"], E["E1_fail"][:5])
pred("E2 isolated X_x (pre) and S X_x S^-1 (post), minus rail blank at end", not E["E2_fail"], E["E2_fail"][:5])
ctl = sorted(set(n for n, _ in E["E3_control_passed"]))
pred("E3 control: omitting one J breaks the echo on every tested N (expected to hold as a failure)", not ctl, dict(sizes_where_omission_still_passes=ctl))
R["measured"]["E"] = dict(E1_fail=len(E["E1_fail"]), E2_fail=len(E["E2_fail"]),
    omit_J_columns_failed=len(E["E3_control_failed_as_expected"]), omit_J_columns_passed=len(E["E3_control_passed"]),
    omit_J_sizes_with_all_columns_passing=[n for n in (2, 6, 10, 12, 14, 18)
        if not any(m == n for m, _ in E["E3_control_failed_as_expected"])])

# ---------- F ----------
if len(sys.argv) > 1:
    d = json.load(open(sys.argv[1]))["entire_comparison"]
    a, b = d["source_x_route"], d["source_y_route"]
    sa = [s["expanded_word_sha256"] for s in a["stages"]]; sb = [s["expanded_word_sha256"] for s in b["stages"]]
    R["measured"]["F_stored_router"] = dict(
        final_128_numerators_identical=a["physical_mode_numerators"] == b["physical_mode_numerators"],
        denominators_equal=a["occupancy_squared_denominator"] == b["occupancy_squared_denominator"],
        nonzero_modes=sum(1 for z in a["physical_mode_numerators"] if z),
        stage_names=[s["stage"] for s in a["stages"]],
        stages_with_identical_word_digest=[i for i in range(len(sa)) if sa[i] == sb[i]],
        stages_with_different_word_digest=[i for i in range(len(sa)) if sa[i] != sb[i]],
        start_vectors=(d["start_x"], d["start_y"]),
        peak_minus_modes=([s["intermediate_peak_occupied_minus_modes"] for s in a["stages"]],
                          [s["intermediate_peak_occupied_minus_modes"] for s in b["stages"]]),
        static_mask_first_change=([s["first_change_of_input_static_two_rail_mask"] for s in a["stages"]],
                                  [s["first_change_of_input_static_two_rail_mask"] for s in b["stages"]]))
R["counts"] = dict(met=len(R["met"]), failed=len(R["failed"]), measured_only=len(R["measured"]))
with open(OUT, "x") as f: json.dump(R, f, indent=1, default=str)
print(json.dumps(R, indent=1, default=str))
