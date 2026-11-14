"""xr41 own program for Director_G/Preparing_signed_sheet_residues.md (written from the note's text).

Run: python3 xr41_check.py OUTDIR   (result file opened with mode 'x'; fixed seed 41)

PREDICATES, fixed before first run. Each records qualify / met / failed; failures are kept in the result.
A1 timing map: for every word of length T<=10, every x0, M in 3,4,5, N in {2M,4M,8M} (hypothesis: N % 2M == 0):
   residue of the physical ring walk (x reduced mod N, gain floor(x/2) mod M at each departure)
   == sum_t floor((x0+t)/2) - sum_t d_t mod M.
A1n same with N not a multiple of 2M (hypothesis fails; measured only).
A2 loops at (0,R): LR has gain (+,-1), RLLR has gain (-,-1), both return to site 0 on R.
A3 pulse words: L^H R has H-1 reversals, LLR L^(H-2) R has H-2, both end at deficit H on R, for H in 4..9.
A4 table: deficits and departure-deficit sums of S,V,W from 0 and S from 2,4 equal the note's table; V vs S: sign only;
   W vs S: same sign, residue +1, for every start clock 0..4M-1 and offset 0..5, M in 3..6.
B1 compact wiring on N=4M, M>=3 (hypothesis): physical census == request, <=4 wells per tick,
   ticks == (5M+3)K+6+P with 0<=P<4M, exactly one W-count in 0..M-1 tunes each item.
   M=3,4: all targets, starts {0,1,N-1}; M=5,10,13: random. (M=10,13 not in the note's checker.)
B2 measured only: compact wiring on N=2M (M=3,4,5) and at M=2 on N=8 (outside the note's hypothesis).
B3 stationary-wall wiring on rings with N/2 > H+3 (hypothesis): census == request, <=4 wells, unique delay s in 0..M-1,
   ticks == 6+P+sum(l_i+M-1).
B4 stationary-wall wiring on N=4M at M=3,4 (hypothesis N/2>H+3 fails). Note's statement: M=3 empty fails;
   M=4 empty passes, all-residue fails.
B5 measured: naive tuning (each item tuned with all other controls S) -- note says it 'can give the wrong residue'.
C1 lifted walk on (site,rail,sign,residue), N=4M, M=3,4 (also N=2M and M=2,5 measured): every state has out-degree 2 and
   in-degree 2; lift strongly connected.
C2 exact: nullspace of (A - 2I) over Q has dimension 1 (constants) => no site/rail/gain dependent solution at k=2.
C3 exact: for k in {1,3/2,5/2,3,17/4}: every null vector of (A-kI) has coordinate sum 0 (so none is nonnegative nonzero);
   report nullity.  Numeric (measured): real eigenvalues of A and whether an eigenvector of one sign exists.
C4 line examples: h=z^x obeys h(x+1)+h(x-1)=(z+1/z)h(x) (exact, z=2,3/2); h=x obeys k=2 but is negative for x<0;
   on a ring of N sites z^x is single valued only if z^N=1.
D1 classification: unknown F on multisets of size<=n over {+-}xZ/M with F(0)=0, F(TU)=F(U), F(JU)=F(U) and
   F(U+V)+F(U+JV)=2F(U)+2F(V) whenever |U|+|V|<=n: solution space dimension (rank mod prime 2^61-1) vs the note's
   family dimension 1+floor(M/2)+1. M=3 n=4,5; M=4 n=4. Measured; truncation at n can add solutions.
D2 exact: count and each character square (M=3,4, rational cosines) satisfy the block identity on 300 random pairs.
"""
import sys, json, random, itertools
from fractions import Fraction
from collections import Counter
from pathlib import Path

random.seed(41)
R = {}
def rec(name, qualify, met, failed, **extra):
    R[name] = dict(qualify=qualify, met=met, failed_count=len(failed), failed=failed[:40], **extra)

def walk(word, x0, M, N=None, rail="R"):
    x, s, j = x0, 1, 0
    for o in word:
        xx = x % N if N else x
        j += xx // 2
        if rail == o == "L": s = -s
        x += 1 if o == "R" else -1
        rail = o
    return (x % N if N else x), rail, s, j % M

def deficits(word, d=0):
    out = []
    for o in word:
        d += o == "L"; out.append(d)
    return out

# ---------- A ----------
def A1(good):
    q = m = 0; f = []
    for M in (3, 4, 5):
        Ns = (2*M, 4*M, 8*M) if good else (2*M+2, 4*M+2, 3*M if M % 2 == 0 else 3*M+1, 4*M-2)
        for N in Ns:
            if (N % (2*M) == 0) != good or N % 2: continue
            for T in range(0, 11):
                for w in itertools.product("RL", repeat=T):
                    ds = [0] + deficits(w)[:-1] if T else []
                    for x0 in range(N):
                        q += 1
                        pred = (sum((x0+t)//2 for t in range(T)) - sum(ds)) % M
                        if walk(w, x0, M, N)[3] == pred: m += 1
                        elif len(f) < 40: f.append([M, N, "".join(w), x0])
                        else: f.append(None) if False else None
    return q, m, f
q, m, f = A1(True); rec("A1", q, m, f)
q, m, f = A1(False); R["A1n"] = dict(qualify_under_hypothesis=0, tested_outside=q, agree=m, disagree=q-m, examples=f[:5])

f = []
for M in range(2, 12):
    a = walk("LR", 0, M); b = walk("RLLR", 0, M)
    if a != (0, "R", 1, (-1) % M) or b != (0, "R", -1, (-1) % M): f.append([M, a, b])
rec("A2", 10, 10-len(f), f)

f = []
for H in range(4, 10):
    for w, n in (("L"*H+"R", H-1), ("LLR"+"L"*(H-2)+"R", H-2)):
        rev = sum(a == b == "L" for a, b in zip("R"+w, w))
        if rev != n or deficits(w)[-1] != H or w[-1] != "R": f.append([H, w, rev])
rec("A3", 12, 12-len(f), f)

S, V, Wd = "LRRLR", "RLLRR", "RLRLR"
f = []; q = 0
table = {("S", 0): ([1,1,1,2,2], 5), ("V", 0): ([0,1,2,2,2], 5), ("W", 0): ([0,1,1,2,2], 4), ("S", 2): ([3,3,3,4,4], 15), ("S", 4): ([5,5,5,6,6], 25)}
for (nm, d0), (row, tot) in table.items():
    w = {"S": S, "V": V, "W": Wd}[nm]; q += 1
    ds = deficits(w, d0)
    if ds != row or sum([d0]+ds[:-1]) != tot: f.append([nm, d0, ds])
for M in range(3, 7):
    for clock in range(4*M):
        for off in range(6):
            x0 = clock - 2*off; q += 1
            s = walk(S, x0, M); v = walk(V, x0, M); w = walk(Wd, x0, M)
            ok = v == (s[0], "R", -s[2], s[3]) and w == (s[0], "R", s[2], (s[3]+1) % M) and s[2] == 1 and s[0] == x0+1
            if not ok: f.append([M, clock, off])
rec("A4", q, q-len(f), f)

# ---------- B ----------
def census(rows, M, N, start):
    st = Counter({(start % N, "R", 1, 0): 1}); mx = 0
    for t, ds in enumerate(rows, 1):
        allowed = {(start+t-2*d) % N for d in ds}; mx = max(mx, len(allowed), len(ds))
        nx = Counter()
        for (x, c, s, j), n in st.items():
            for o, dx in (("R", 1), ("L", -1)):
                y = (x+dx) % N
                if y in allowed: nx[(y, o, -s if c == o == "L" else s, (j + x//2) % M)] += n
        st = nx
    return st, mx

def compact(M, N, right, left, target, start, naive=False):
    items = [("R", g) for g in right] + [("L", g) for g in left]; K = len(items)
    T0 = (5*M+3)*K + 6
    P = (target - (start + T0 - 2*(2*M*K+4))) % (4*M)
    sel = [[S]*M for _ in items]
    def lineage(i, sel):
        w = ""
        for i2, (role, _) in enumerate(items):
            if i2 == len(right): w += "LLR" if items[i][0] == "R" else "RRR"
            for k in range(M): w += sel[i2][k] if i2 <= i else S
            w += "LLR" if i2 == i else "RRR"
        if len(right) == K: w += "LLR" if items[i][0] == "R" else "RRR"
        w += "R"*P + ("RRR" if items[i][0] == "R" else "RLL")
        return w
    notes = []
    for i, (role, (sign, res)) in enumerate(items):
        base = sel if not naive else [[S]*M for _ in items]
        trial = [list(r) for r in base]
        if walk(lineage(i, trial), start, M, N)[2] != sign: trial[i][0] = V
        hits = []
        for c in range(M):
            t2 = [list(r) for r in trial]; t2[i][1:1+c] = [Wd]*c
            if c > M-1: continue
            if walk(lineage(i, t2), start, M, N)[2:] == (sign, res): hits.append(c)
        if len(hits) != 1: notes.append(["tuning count", i, hits]); c = hits[0] if hits else 0
        else: c = hits[0]
        sel[i][0] = trial[i][0]; sel[i][1:1+c] = [Wd]*c
    rows = []; off = 0
    def controls(i, walls):
        nonlocal off
        for k in range(M):
            sd = deficits(sel[i][k]); st = deficits(S)
            for u in range(5): rows.append({off+sd[u]} | {off+d+st[u] for d in walls})
            off += 2
    for i in range(len(right)):
        controls(i, (2,)); rows.extend([{off, off+2, off+1}, {off, off+2}, {off, off+2}])
    rows.extend([{off, off+3}, {off, off+4}, {off, off+4}])
    for i in range(len(right), K):
        controls(i, (2, 4)); rows.extend([{off, off+2, off+4, off+1}, {off, off+2, off+4}, {off, off+2, off+4}])
    rows.extend([{off, off+2, off+4}]*P)
    rows.extend([{off+2, off+4}, {off+3, off+4}, {off+4}])
    got, mx = census(rows, M, N, start)
    want = Counter((target % N, role, s, g) for role, (s, g) in items)
    ok = got == want and mx <= 4 and len(rows) == T0+P and not notes
    return ok, dict(ticks=len(rows), max_wells=mx, notes=notes, extra=sorted((got-want).items())[:6], missing=sorted((want-got).items())[:6])

def requests(M, n):
    bins = [(s, j) for s in (1, -1) for j in range(M)]
    out = [([], []), (bins, bins[::-1]), ([(1, 0), (-1, 0), (1, 0)], [(-1, M-1)]*2), ([(1, 1)], []), ([], [(-1, 2 % M)])]
    for _ in range(n):
        out.append(([random.choice(bins) for _ in range(random.randint(0, 4))], [random.choice(bins) for _ in range(random.randint(0, 4))]))
    return out

q = 0; f = []; per = {}
for M in (3, 4, 5, 10, 13):
    N = 4*M; c0 = q
    starts = (0, 1, N-1) if M <= 4 else (0, N-1, random.randrange(N))
    targets = range(N) if M <= 4 else (0, N-1, random.randrange(N), random.randrange(N))
    for r, l in requests(M, 6 if M <= 5 else 3):
        for s in starts:
            for t in targets:
                q += 1
                ok, info = compact(M, N, r, l, t, s)
                if not ok: f.append([M, N, r, l, t, s, info])
    per[M] = q-c0
rec("B1", q, q-len(f), f, cases_per_M=per)

meas = {}
for M, N in ((3, 6), (4, 8), (5, 10), (2, 8), (2, 4)):
    n = bad = 0; ex = None
    for r, l in requests(M, 4):
        for s in (0, 1):
            for t in range(N):
                n += 1
                try: ok, info = compact(M, N, r, l, t, s)
                except Exception as e: ok, info = False, dict(error=repr(e))
                if not ok:
                    bad += 1
                    if ex is None: ex = [r, l, t, s, info]
    meas[f"M={M},N={N}"] = dict(qualify_under_hypothesis=0, tested=n, match=n-bad, mismatch=bad, first_mismatch=ex)
R["B2"] = meas

def walls_wiring(M, N, right, left, target, start, H=None):
    H = H or {3: 4, 4: 5}.get(M, M-1)
    items = [("R", g) for g in right] + [("L", g) for g in left]
    def pulses(): return ("L"*H+"R", "LLR"+"L"*(H-2)+"R")
    notes = []
    # choose pulse by sign (lineage has one further reversal: LLR transfer or closing LL)
    chosen = []
    for role, (sign, res) in items:
        c = [p for p in pulses() if (-1)**sum(a == b == "L" for a, b in zip("R"+p, p)) == -sign]
        if len(c) != 1: notes.append("pulse choice")
        chosen.append(c[0])
    body = sum(len(p)+M-1 for p in chosen)
    P = (target - (start + body + 6 - 2*(H+2))) % N
    def lineage(i, s):
        w = ""
        for i2 in range(len(items)):
            if i2 == len(right): w += "LLR" if items[i][0] == "R" else "RRR"
            L = len(chosen[i2])+M-1
            w += ("R"*s + chosen[i2] + "R"*(M-1-s)) if i2 == i else "R"*L
        if len(right) == len(items): w += "LLR" if items[i][0] == "R" else "RRR"
        return w + "R"*P + ("RRR" if items[i][0] == "R" else "RLL")
    rows = []
    def slot(i, walls):
        role, (sign, res) = items[i]
        hits = [s for s in range(M) if walk(lineage(i, s), start, M, N)[1:] == (role, sign, res)]
        if len(hits) != 1: notes.append(["delay count", i, hits])
        s = hits[0] if hits else 0
        ds = deficits(chosen[i])
        for u in range(len(chosen[i])+M-1):
            rows.append(set(walls) | ({ds[u-s]} if 0 <= u-s < len(ds) else set()))
    for i in range(len(right)): slot(i, (0, H))
    rows.extend([{0, H+1}, {0, H+2}, {0, H+2}])
    for i in range(len(right), len(items)): slot(i, (0, H, H+2))
    rows.extend([{0, H, H+2}]*P); rows.extend([{H, H+2}, {H+1, H+2}, {H+2}])
    got, mx = census(rows, M, N, start)
    want = Counter((target % N, role, s, g) for role, (s, g) in items)
    ok = got == want and mx <= 4 and len(rows) == 6+P+body and not notes
    return ok, dict(ticks=len(rows), max_wells=mx, notes=notes, extra=sorted((got-want).items())[:6], missing=sorted((want-got).items())[:6])

q = 0; f = []; per = {}
for M, N in ((3, 24), (4, 32), (5, 20), (6, 24), (7, 28), (10, 40), (13, 52), (14, 56)):
    H = {3: 4, 4: 5}.get(M, M-1); c0 = q
    assert N//2 > H+3
    for r, l in requests(M, 3):
        for s in (0, N-1):
            for t in (0, 1, N-1, random.randrange(N)):
                q += 1
                ok, info = walls_wiring(M, N, r, l, t, s)
                if not ok: f.append([M, N, r, l, t, s, info])
    per[f"{M},{N}"] = q-c0
rec("B3", q, q-len(f), f, cases=per)

meas = {}
for M in (3, 4):
    N = 4*M; bins = [(s, j) for s in (1, -1) for j in range(M)]
    for nm, r, l in (("empty", [], []), ("all", bins, bins[::-1])):
        n = bad = 0; ex = None
        for s in range(N):
            for t in range(N):
                n += 1; ok, info = walls_wiring(M, N, r, l, t, s)
                if not ok:
                    bad += 1
                    if ex is None: ex = [t, s, info]
        ok00, _ = walls_wiring(M, N, r, l, 0, 0)
        meas[f"M={M},N={N},{nm}"] = dict(qualify_under_hypothesis=0, tested=n, match=n-bad, mismatch=bad, start0_target0_match=ok00, first_mismatch=ex)
R["B4"] = meas
R["B4"]["note_statement_start0_target0"] = "M=3 empty False; M=3 all (not stated); M=4 empty True; M=4 all False"

n = bad = 0
for M in (3, 4, 5):
    for r, l in requests(M, 6):
        n += 1; ok, info = compact(M, 4*M, r, l, 0, 0, naive=True); bad += not ok
R["B5"] = dict(tested=n, naive_wrong=bad, naive_right=n-bad)

# ---------- C ----------
P61 = (1 << 61) - 1
def lift(M, N):
    states = [(x, r, s, j) for x in range(N) for r in "RL" for s in (1, -1) for j in range(M)]
    idx = {v: i for i, v in enumerate(states)}
    succ = []
    for (x, r, s, j) in states:
        g = (j + x//2) % M
        succ.append([idx[((x+1) % N, "R", s, g)], idx[((x-1) % N, "L", -s if r == "L" else s, g)]])
    return states, succ

def nullspace(rows, n, k):
    # exact over Q: matrix A - kI, rows as dict
    mat = []
    for i, su in enumerate(rows):
        v = [Fraction(0)]*n
        for t in su: v[t] += 1
        v[i] -= k; mat.append(v)
    piv = []; r = 0
    for c in range(n):
        p = next((i for i in range(r, n) if mat[i][c] != 0), None)
        if p is None: continue
        mat[r], mat[p] = mat[p], mat[r]
        inv = 1/mat[r][c]; mat[r] = [a*inv for a in mat[r]]
        for i in range(n):
            if i != r and mat[i][c] != 0:
                fac = mat[i][c]; mat[i] = [a - fac*b if b else a for a, b in zip(mat[i], mat[r])]
        piv.append(c); r += 1
    free = [c for c in range(n) if c not in piv]
    basis = []
    for fc in free:
        v = [Fraction(0)]*n; v[fc] = Fraction(1)
        for i, c in enumerate(piv): v[c] = -mat[i][fc]
        basis.append(v)
    return basis

C = {}
for M, N, hyp in ((3, 12, True), (4, 16, True), (3, 6, False), (4, 8, False), (2, 8, False), (2, 4, False), (5, 20, False)):
    states, succ = lift(M, N); n = len(states)
    indeg = Counter(t for su in succ for t in su)
    deg_ok = all(indeg[i] == 2 for i in range(n)) and all(len(set(su)) == 2 for su in succ)
    def reach(adj):
        seen = {0}; stack = [0]
        while stack:
            for t in adj[stack.pop()]:
                if t not in seen: seen.add(t); stack.append(t)
        return len(seen)
    radj = [[] for _ in range(n)]
    for i, su in enumerate(succ):
        for t in su: radj[t].append(i)
    strong = reach(succ) == n and reach(radj) == n
    entry = dict(hypothesis_N_eq_4M_M_in_3_4=hyp, states=n, degrees_two=deg_ok, strongly_connected=strong)
    if n <= 256:
        b2 = nullspace(succ, n, Fraction(2))
        entry["nullity_k2"] = len(b2)
        entry["k2_null_is_constant"] = len(b2) == 1 and len(set(b2[0])) == 1
        other = {}
        for k in (Fraction(1), Fraction(3, 2), Fraction(5, 2), Fraction(3), Fraction(17, 4), Fraction(0), Fraction(-2)):
            b = nullspace(succ, n, k)
            other[str(k)] = dict(nullity=len(b), all_null_vectors_sum_zero=all(sum(v) == 0 for v in b))
        entry["other_k"] = other
    C[f"M={M},N={N}"] = entry
R["C1_C2_C3"] = C
try:
    import numpy as np
    num = {}
    for M, N in ((3, 12), (4, 16)):
        states, succ = lift(M, N); n = len(states)
        A = np.zeros((n, n))
        for i, su in enumerate(succ):
            for t in su: A[i, t] += 1
        ev, vec = np.linalg.eig(A)
        order = sorted(set(round(float(abs(e)), 9) for e in ev), reverse=True)[:3]
        num[f"M={M},N={N}"] = dict(largest_three_moduli=order, eigenvalues_equal_2_numeric=int(sum(abs(e-2) < 1e-9 for e in ev)),
                                   note="measured only; modulus-2 eigenvalues other than 2 are complex/negative periodicity eigenvalues",
                                   modulus2_values=sorted({(round(float(e.real), 6), round(float(e.imag), 6)) for e in ev if abs(abs(e)-2) < 1e-6}))
    R["C3_numeric"] = num
except ImportError:
    R["C3_numeric"] = "numpy absent"

c4 = []
for z in (Fraction(2), Fraction(3, 2)):
    c4.append(all(z**(x+1) + z**(x-1) == (z + 1/z)*z**x for x in range(-6, 7)) and z + 1/z > 2)
R["C4"] = dict(z_power_examples_ok=c4, h_eq_x_harmonic_k2=all((x+1)+(x-1) == 2*x for x in range(-6, 7)), h_eq_x_negative_at=-1,
               ring_single_valued_requires="z^N=1, i.e. z=1 for z>0 (z=2,N=12: %s)" % (Fraction(2)**12 == 1))

# ---------- D ----------
def rank_mod(rows, ncol):
    rows = [dict(r) for r in rows]; rank = 0; pivots = {}
    for r in rows:
        r = {c: v % P61 for c, v in r.items() if v % P61}
        while r:
            c = min(r)
            if c in pivots:
                pr = pivots[c]; fac = r[c]
                for cc, vv in pr.items():
                    nv = (r.get(cc, 0) - fac*vv) % P61
                    if nv: r[cc] = nv
                    else: r.pop(cc, None)
            else:
                inv = pow(r[c], P61-2, P61); pivots[c] = {cc: vv*inv % P61 for cc, vv in r.items()}; rank += 1; break
    return rank

def D1(M, n):
    labels = [(s, j) for s in (1, -1) for j in range(M)]
    ms = [tuple(sorted(c)) for k in range(n+1) for c in itertools.combinations_with_replacement(range(2*M), k)]
    idx = {u: i for i, u in enumerate(ms)}
    def T(u): return tuple(sorted(labels.index((labels[a][0], (labels[a][1]+1) % M)) for a in u))
    def J(u): return tuple(sorted(labels.index((-labels[a][0], labels[a][1])) for a in u))
    eqs = [{idx[()]: 1}]
    for u in ms:
        for im in (T(u), J(u)):
            if im != u: eqs.append({idx[u]: 1, idx[im]: -1})
    for u in ms:
        for v in ms:
            if len(u)+len(v) <= n:
                e = Counter()
                e[idx[tuple(sorted(u+v))]] += 1; e[idx[tuple(sorted(u+J(v)))]] += 1; e[idx[u]] -= 2; e[idx[v]] -= 2
                eqs.append(dict(e))
    return dict(unknowns=len(ms), equations=len(eqs), solution_dim_mod_p=len(ms)-rank_mod(eqs, len(ms)), note_family_dim=1 + M//2 + 1)
R["D1"] = {f"M={M},n={n}": D1(M, n) for M, n in ((3, 4), (3, 5), (4, 4), (4, 5), (5, 4), (6, 4))}

cosq = {3: [Fraction(1), Fraction(-1, 2), Fraction(-1, 2)], 4: [Fraction(1), Fraction(0), Fraction(-1), Fraction(0)]}
def Fterm(M, s, U):
    if s == "count": return Fraction(len(U))
    D = [sum(a for a, j in U if j == jj) for jj in range(M)]
    return sum(D[a]*D[b]*cosq[M][(s*(a-b)) % M] for a in range(M) for b in range(M))
q = 0; f = []
for M in (3, 4):
    bins = [(s, j) for s in (1, -1) for j in range(M)]
    for _ in range(300):
        U = [random.choice(bins) for _ in range(random.randint(0, 7))]; Vv = [random.choice(bins) for _ in range(random.randint(0, 7))]
        JV = [(-a, j) for a, j in Vv]; b = random.randrange(M); Tb = lambda X: [(a, (j+b) % M) for a, j in X]
        for s in ["count"] + list(range(M//2+1)):
            q += 1
            if Fterm(M, s, Tb(U+Vv)) + Fterm(M, s, Tb(U+JV)) != 2*Fterm(M, s, U) + 2*Fterm(M, s, Vv) or Fterm(M, s, U) < 0: f.append([M, s, U, Vv])
rec("D2", q, q-len(f), f)

out = Path(sys.argv[1]); out.mkdir(parents=True, exist_ok=True)
with (out/"xr41_result.json").open("x") as fh:
    json.dump(R, fh, indent=1, default=str); fh.write("\n")
for k, v in R.items():
    if isinstance(v, dict) and "qualify" in v: print(k, v["qualify"], v["met"], v["failed_count"])
