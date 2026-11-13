"""Challenger program for prop:abund / cor:abund.  Predicates fixed before the first run.

Conventions: arc x->y with exponent e means A[y][x] = zeta^e, zeta = exp(2 pi i/q).  C = Z/q written
additively (exponents).  Dhat on V x Z/q, arc (x,g)->(y,g+e).  u = e(y1->z) - e(y2->z) (statement's u).
Period = gcd over arcs (a->b) of level[a]+1-level[b] for BFS levels (only for strongly connected).

H  (hypothesis, per carrier): A*A = d exactly in Z[zeta]; Dhat strongly connected.  Only carriers with H
    are tested on P1..P7; number qualifying is reported.
P1 every vertex has d successors and d predecessors, in D and in Dhat.
P2 r0 | r; shift of (x,g)->(x,g+h) between cyclic classes is independent of (x,g); pi is additive;
   image of pi = r0 Z/r; |C0| = q r0 / r.
P3 for each L in a window of r consecutive large lengths: gains at y1 form exactly one coset K of C0,
   gains at y2 are exactly K+u; all r/r0 cosets occur over the window (start vertex 0, and one more).
P3inv (control, expected to fail when 2u not in C0): gains at y2 are K-u.
P4 at every length 0..Lmax and every vertex, the gains present lie in one coset of C0.
P5 [exists L<=Lmax at which all q gains occur at y1 and at y2]  <=>  r == r0.
P6 for every common successor z' of y1,y2: u + (e(y2->z') - e(y1->z')) in C0; q0 >= 2.
P7 dimension of the solution space of the consistency equations (factor d), projected on the core
   unknowns (moduli of sums of <=2 elements of C0), equals phi(q0)/2 (1 if q0=2).  Events: all
   multisets of size <=T of walks to y1,y2 at one length (multiplicities checked against exact walk
   counts) plus random events on all vertices at r consecutive lengths.  Moduli keyed by the exact
   element |alpha|^2 of Z[zeta].  Ranks mod two primes (must agree).  T raised 3 -> 4 -> 5 only if the
   rank on the core exceeds the prediction (too few equations); every T-level result is kept.
   A value BELOW the prediction at any T, or above it at the final T, is a failure.
"""
import sys, os, json, random, itertools, math
from collections import deque, Counter
import numpy as np

OUT = sys.argv[1]
if os.path.exists(OUT):
    sys.exit("refuse to overwrite " + OUT)
random.seed(20261113)

def cyclo(n):
    # integer coefficient list (low->high) of Phi_n
    def pdiv(a, b):
        a = a[:]; qd = [0]*(len(a)-len(b)+1)
        for i in range(len(a)-len(b), -1, -1):
            c = a[i+len(b)-1]; qd[i] = c
            for j, bj in enumerate(b): a[i+j] -= c*bj
        assert all(v == 0 for v in a)
        return qd
    p = [-1]+[0]*(n-1)+[1]
    for dd in range(1, n):
        if n % dd == 0: p = pdiv(p, cyclo(dd))
    return p
def phi(n): return sum(1 for k in range(1, n+1) if math.gcd(k, n) == 1)

class Ring:
    def __init__(s, q):
        s.q = q; P = cyclo(q); s.n = len(P)-1
        red = []
        for k in range(q):
            v = [0]*(k+1); v[k] = 1
            while len(v) > s.n:
                c = v.pop()
                if c:
                    off = len(v)-s.n
                    for j in range(s.n): v[off+j] -= c*P[j]
            v += [0]*(s.n-len(v)); red.append(v)
        s.red = np.array(red, dtype=object)
    def norm_key(s, a):
        # a: length-q int vector (coefficients of zeta^k); returns canonical tuple of a*conj(a)
        q = s.q; c = [0]*q
        nz = [(k, int(v)) for k, v in enumerate(a) if v]
        for k, v in nz:
            for l, w in nz: c[(k-l) % q] += v*w
        r = [0]*s.n
        for k, v in enumerate(c):
            if v:
                row = s.red[k]
                for j in range(s.n): r[j] += v*int(row[j])
        return tuple(r)
    def canon(s, a):
        r = [0]*s.n
        for k, v in enumerate(a):
            if v:
                row = s.red[k]
                for j in range(s.n): r[j] += int(v)*int(row[j])
        return tuple(r)

def strongly_connected(nv, succ):
    def reach(adj):
        seen = [False]*nv; seen[0] = True; dq = deque([0])
        while dq:
            a = dq.popleft()
            for b in adj[a]:
                if not seen[b]: seen[b] = True; dq.append(b)
        return all(seen)
    pred = [[] for _ in range(nv)]
    for a in range(nv):
        for b in succ[a]: pred[b].append(a)
    return reach(succ) and reach(pred)
def period_levels(nv, succ):
    lev = [None]*nv; lev[0] = 0; dq = deque([0])
    while dq:
        a = dq.popleft()
        for b in succ[a]:
            if lev[b] is None: lev[b] = lev[a]+1; dq.append(b)
    g = 0
    for a in range(nv):
        for b in succ[a]: g = math.gcd(g, lev[a]+1-lev[b])
    return g, lev

def rank_mod(rows, ncol, p):
    # rows: list of dict col->int ; returns rank mod p (dense numpy elimination)
    if not rows: return 0
    M = np.zeros((len(rows), ncol), dtype=np.int64)
    for i, r in enumerate(rows):
        for c, v in r.items(): M[i, c] = v % p
    rk = 0
    for c in range(ncol):
        nzr = np.nonzero(M[rk:, c])[0]
        if len(nzr) == 0: continue
        piv = rk+nzr[0]
        if piv != rk: M[[rk, piv]] = M[[piv, rk]]
        inv = pow(int(M[rk, c]), p-2, p)
        M[rk] = (M[rk]*inv) % p
        f = M[rk+1:, c].copy()
        idx = np.nonzero(f)[0]
        if len(idx):
            M[rk+1+idx] = (M[rk+1+idx] - np.outer(f[idx], M[rk])) % p
        rk += 1
        if rk == len(rows): break
    return rk

def analyse(nvert, q, arcs, d, label, do_dim=True, Lmax=None):
    """arcs: list (x,y,e).  Returns record dict."""
    R = Ring(q)
    rec = {"label": label, "n": nvert, "q": q, "d": d, "arcs": arcs}
    out = [[] for _ in range(nvert)]; inn = [[] for _ in range(nvert)]
    E = {}
    for x, y, e in arcs:
        assert (x, y) not in E
        E[(x, y)] = e % q; out[x].append(y); inn[y].append(x)
    # H: A*A = d exactly
    ok = True
    for x in range(nvert):
        for x2 in range(x, nvert):
            v = [0]*q
            for y in out[x]:
                if (x2, y) in E: v[(E[(x2, y)]-E[(x, y)]) % q] += 1
            c = R.canon(v)
            target = tuple([d]+[0]*(R.n-1)) if x == x2 else tuple([0]*R.n)
            if c != target: ok = False
    rec["H_AstarA"] = ok
    nv = nvert*q
    hs = [[y*q+((g+E[(x, y)]) % q) for y in out[x]] for x in range(nvert) for g in range(q)]
    rec["H_hat_sc"] = strongly_connected(nv, hs)
    rec["H"] = rec["H_AstarA"] and rec["H_hat_sc"]
    if not rec["H"]: return rec
    # P1
    hp = Counter(b for a in range(nv) for b in hs[a])
    rec["P1"] = all(len(out[x]) == d and len(inn[x]) == d for x in range(nvert)) and \
        all(len(set(hs[a])) == d and hp[a] == d for a in range(nv))
    r0, _ = period_levels(nvert, out); r, lev = period_levels(nv, hs)
    rec["r"] = r; rec["r0"] = r0
    cls = [l % r for l in lev]
    pi = [(cls[0*q+h]-cls[0]) % r for h in range(q)]
    indep = all((cls[x*q+(g+h) % q]-cls[x*q+g]) % r == pi[h] for x in range(nvert) for g in range(q) for h in range(q))
    addit = all((pi[h]+pi[k]) % r == pi[(h+k) % q] for h in range(q) for k in range(q))
    C0 = [h for h in range(q) if pi[h] == 0]; q0 = len(C0)
    img = sorted(set(pi))
    rec["q0"] = q0
    rec["P2"] = (r % r0 == 0) and indep and addit and img == list(range(0, r, r0)) if r % r0 == 0 else False
    rec["P2"] = bool(rec["P2"] and q0*r == q*r0)
    cos = lambda g: pi[g % q]  # coset label of g
    # merging pair
    pair = None
    for y1 in range(nvert):
        for y2 in range(nvert):
            if y1 != y2 and set(out[y1]) & set(out[y2]):
                pair = (y1, y2); break
        if pair: break
    rec["pair"] = pair
    if pair is None: return rec
    y1, y2 = pair; Z = sorted(set(out[y1]) & set(out[y2])); z = Z[0]
    u = (E[(y1, z)]-E[(y2, z)]) % q
    rec["u"] = u; rec["m"] = len(Z)
    rec["P6"] = all(cos(u+E[(y2, zz)]-E[(y1, zz)]) == 0 for zz in Z) and q0 >= 2
    if Lmax is None: Lmax = 6*nv+40
    def counts(start):
        cur = [0]*nv; cur[start*q] = 1; res = [cur]
        for _ in range(Lmax):
            nxt = [0]*nv
            for a in range(nv):
                if cur[a]:
                    for b in hs[a]: nxt[b] += cur[a]
            cur = nxt; res.append(cur)
        return res
    P3 = True; P3inv = True; P4 = True; allq = False
    cnt0 = None
    for start in (0, nvert-1):
        cn = counts(start)
        if start == 0: cnt0 = cn
        for L in range(Lmax+1):
            for x in range(nvert):
                gs = [g for g in range(q) if cn[L][x*q+g]]
                if len(set(cos(g) for g in gs)) > 1: P4 = False
            if all(cn[L][y1*q+g] for g in range(q)) and all(cn[L][y2*q+g] for g in range(q)): allq = True
        seen = set()
        for L in range(Lmax-r+1, Lmax+1):
            g1 = [g for g in range(q) if cn[L][y1*q+g]]; g2 = set(g for g in range(q) if cn[L][y2*q+g])
            if not g1: P3 = False; continue
            K = set((g1[0]+h) % q for h in C0)
            if set(g1) != K: P3 = False
            if g2 != set((k+u) % q for k in K): P3 = False
            if g2 != set((k-u) % q for k in K): P3inv = False
            if min(cn[L][y1*q+g] for g in K) < 1000: P3 = False   # 'at least N' with N = 1000
            seen.add(cos(g1[0]))
        if len(seen) != r//r0: P3 = False
    rec["P3"] = P3; rec["P3inv_control"] = P3inv; rec["P4"] = P4
    rec["two_u_in_C0"] = cos(2*u) == 0
    rec["allq_at_one_length"] = allq
    rec["P5"] = (allq == (r == r0))
    if not do_dim: return rec
    # P7
    pred_dim = 1 if q0 == 2 else phi(q0)//2
    rec["pred_dim"] = pred_dim; rec["naive_dim_phi_q_half"] = 1 if q == 2 else phi(q)//2
    cn = cnt0
    Tmax = 5 if q0 <= 4 else (4 if q0 <= 8 else 3)
    L0 = next(L for L in range(Lmax-r, 0, -1) if cn[L][y1*q] )  # length at which gain 1 occurs at y1... coset K=C0
    K1 = [g for g in range(q) if cn[L0][y1*q+g]]; K2 = [g for g in range(q) if cn[L0][y2*q+g]]
    assert min(cn[L0][y1*q+g] for g in K1) >= 5 and min(cn[L0][y2*q+g] for g in K2) >= 5
    items = [(y1, g) for g in K1]+[(y2, g) for g in K2]
    keyid = {}; zero = tuple([0]*R.n)
    def kid(k):
        if k == zero: return None
        if k not in keyid: keyid[k] = len(keyid)
        return keyid[k]
    def equation(mult):
        # mult: dict (vertex,g)->multiplicity
        v = {}
        for (x, g), mlt in mult.items(): v.setdefault(x, [0]*q)[g] += mlt
        row = Counter()
        w = {}
        for x, vec in v.items():
            k = kid(R.norm_key(vec))
            if k is not None: row[k] -= d
            for y in out[x]:
                e = E[(x, y)]; t = w.setdefault(y, [0]*q)
                for g in range(q):
                    if vec[g]: t[(g+e) % q] += vec[g]
        for y, vec in w.items():
            k = kid(R.norm_key(vec))
            if k is not None: row[k] += 1
        return {c: val for c, val in row.items() if val}
    core = set()
    for g in C0:
        for h in C0:
            for vec in ([1 if j == g else 0 for j in range(q)],):
                core.add(kid(R.norm_key(vec)))
            vec = [0]*q; vec[g] += 1; vec[h] += 1
            c = kid(R.norm_key(vec))
            if c is not None: core.add(c)
    rows = {}
    def add(mult):
        rw = equation(mult)
        if rw: rows[tuple(sorted(rw.items()))] = rw
    rng = random.Random(7)
    for L in range(L0, L0+r):
        avail = [(x, g) for x in range(nvert) for g in range(q) if cn[L][x*q+g]]
        for _ in range(150):
            mult = Counter(rng.choice(avail) for _ in range(rng.randint(1, 4)))
            assert all(cn[L][x*q+g] >= mlt for (x, g), mlt in mult.items())
            add(dict(mult))
    levels = []
    for T in range(1, Tmax+1):
        for ms in itertools.combinations_with_replacement(items, T):
            add(dict(Counter(ms)))
        if T < 3: continue
        ncol = len(keyid); rl = list(rows.values())
        corel = sorted(core); rest = [c for c in range(ncol) if c not in core]
        remap = {c: i for i, c in enumerate(rest)}
        rl_rest = [{remap[c]: v for c, v in rw.items() if c in remap} for rw in rl]
        dims = []
        for p in (2147483629, 2147483587):
            # order columns: rest first then core -> dim(proj of nullspace on core) = |core| - (rank(M) - rank(M_rest))
            dims.append(len(corel)-(rank_mod(rl, ncol, p)-rank_mod(rl_rest, len(rest), p)))
        levels.append({"T": T, "equations": len(rl), "unknowns": ncol, "core": len(corel), "dim_core_two_primes": dims})
        if dims[0] == dims[1] and dims[0] <= pred_dim: break
    rec["dim_levels"] = levels
    last = levels[-1]["dim_core_two_primes"]
    rec["dim"] = last[0]
    rec["P7"] = (last[0] == last[1] == pred_dim) and all(min(l["dim_core_two_primes"]) >= pred_dim for l in levels)
    return rec

def rand_deg2(q, k, mode):
    n = 2*k; src = list(range(n)); random.shuffle(src); tgt = list(range(n)); random.shuffle(tgt)
    arcs = []
    s = None
    if mode == 1:
        ss = [x for x in range(2, q) if q % x == 0 and (q//2) % x == 0]
        if ss: s = random.choice(ss); t = random.randrange(s)
    def ex():
        if s is None: return random.randrange(q)
        return (t+s*random.randrange(q//s)) % q
    for b in range(k):
        x, x2 = src[2*b], src[2*b+1]; y, y2 = tgt[2*b], tgt[2*b+1]
        e1, e2, e3 = ex(), ex(), ex(); e4 = (e3+e2-e1+q//2) % q
        arcs += [(x, y, e1), (x2, y, e2), (x, y2, e3), (x2, y2, e4)]
    return n, arcs
def rand_deg3(q, k, mode):
    n = 3*k; src = list(range(n)); random.shuffle(src); tgt = list(range(n)); random.shuffle(tgt)
    arcs = []; s = None
    if mode == 1:
        ss = [x for x in range(2, q) if (q//3) % x == 0]
        if ss: s = random.choice(ss); t = random.randrange(s)
    for b in range(k):
        if s is None:
            a = [random.randrange(q) for _ in range(3)]; bb = [random.randrange(q) for _ in range(3)]
        else:
            a = [(t+s*random.randrange(q//s)) % q for _ in range(3)]; bb = [(s*random.randrange(q//s)) % q for _ in range(3)]
        for i in range(3):
            for kk in range(3):
                arcs.append((src[3*b+kk], tgt[3*b+i], (a[i]+bb[kk]+(q//3)*i*kk) % q))
    return n, arcs

results = []
# 1. the four-vertex example of the text
ex4 = [(0, 2, 0), (0, 3, 1), (1, 0, 1), (1, 1, 3), (2, 0, 0), (2, 1, 0), (3, 2, 0), (3, 3, 3)]
results.append(analyse(4, 4, ex4, 2, "text-example-4-vertices"))
# 2. random carriers
plan = [(2, q, k) for q in (4, 6, 8, 12) for k in (1, 2, 3)] + [(3, q, k) for q in (6, 9, 12) for k in (1, 2)]
NPER = int(sys.argv[2]) if len(sys.argv) > 2 else 6
for (d, q, k) in plan:
    for i in range(NPER):
        mode = i % 2
        n, arcs = (rand_deg2 if d == 2 else rand_deg3)(q, k, mode)
        results.append(analyse(n, q, arcs, d, f"d{d}-q{q}-k{k}-mode{mode}-{i}"))
        print(results[-1]["label"], {kk: vv for kk, vv in results[-1].items() if kk not in ("arcs", "label")}, flush=True)
with open(OUT, "x") as f: json.dump(results, f, indent=1)
# summary
Hq = [r for r in results if r["H"]]
print("\ncarriers", len(results), "H holds", len(Hq), "H fails", len(results)-len(Hq),
      "(A*A fail", sum(1 for r in results if not r["H_AstarA"]), ")")
print("r != r0 among H:", sum(1 for r in Hq if r["r"] != r["r0"]))
for P in ("P1", "P2", "P3", "P3inv_control", "P4", "P5", "P6", "P7"):
    have = [r for r in Hq if P in r]
    print(P, "pass", sum(1 for r in have if r[P]), "fail", sum(1 for r in have if not r[P]), "of", len(have))
print("P3inv fails vs two_u_in_C0:", Counter((r["P3inv_control"], r["two_u_in_C0"]) for r in Hq if "P3" in r))
print("dims (q,q0,pred,naive,dim):", Counter((r["q"], r["q0"], r["pred_dim"], r["naive_dim_phi_q_half"], r["dim"]) for r in Hq if "dim" in r))
print("example:", {kk: vv for kk, vv in results[0].items() if kk != "arcs"})
