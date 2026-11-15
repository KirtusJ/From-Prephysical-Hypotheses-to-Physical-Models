"""Challenger program for Lemma R_N and Proposition P_N (PREP_RING.md).

Groups A = product of cyclic groups, written additively; exact integer arithmetic.
Ring Z_N; walks from (0,R); right step -> (x+1,R), left -> (x-1,L).
Arc gains: a R->R, b R->L, c L->R, d L->L. D_delta: (0,0,0,delta).
B = b+c-2a, M = N/gcd(N,2), delta = a+d-b-c.

Predicates fixed before the first run:
P0 control: Z_5, A=Z_2, (1,0,0,1): B=0, M*B=0, kappa(5 right steps)=1, g-g_delta=1.
P1 (formula) for every walk of length <=12 on N=1..10 and every tested quadruple:
   g(w)-g_delta(w) == (rho-lam)a + lam(b+c)            if w ends on R
                   == (rho-lam)a + lam(b+c) + b+delta-d if w ends on L.
P2 (well-defined) if M*B==0 then for each (T, end vertex) the ratio g-g_delta takes one value.
P2' (converse) if M*B!=0 then some (T,vertex) with T<=12 has >=2 ratios, whenever
   a pair of walks with winding difference exists in range (count reported).
P3 (end to end Prop P_N) for each qualifying (A,quad) with M*B==0 (hypothesis tested,
   counted), each coset kappa<delta> of H, each target U in M(kappa<delta>),
   V in M(kappa+b-d+<delta>), |U|+|V| in 1..2(3): follow the proof (x0,mu0 minimal, U',V',
   brute-force D_delta event S' by BFS [stand-in for Lemma 5.34, also on rings with M<6],
   walk at xbar -> s, lam1, i = -s mod ord(N a), j = mu0-lam1 mod ord(b+c), prefixes) and
   simulate S in D: m_S(xbar,R)==U and m_S(xbar,L)==V. Targets outside BFS bound counted.
P4 prefix uniqueness/closure: masks {1..N-1,0} admit exactly one walk, ending at (0,R),
   iff N>=3; masks {-1},{0} likewise iff N>=3. Report N=1,2.
Seed 20261115. Results file results.txt; refuses to overwrite.
"""
import itertools, random, sys, os
from math import gcd
from collections import defaultdict

OUT = sys.argv[1] if len(sys.argv) > 1 else 'results.txt'
if os.path.exists(OUT):
    sys.exit('refuse to overwrite ' + OUT)
log = []
def P(*a):
    s = ' '.join(str(x) for x in a); log.append(s); print(s)

class G:
    def __init__(s, mods): s.m = tuple(mods)
    def add(s, x, y): return tuple((u+v) % n for u, v, n in zip(x, y, s.m))
    def neg(s, x): return tuple((-u) % n for u, n in zip(x, s.m))
    def mul(s, k, x): return tuple((k*u) % n for u, n in zip(x, s.m))
    def zero(s): return tuple(0 for _ in s.m)
    def elems(s): return list(itertools.product(*[range(n) for n in s.m]))
    def order(s, x):
        k = 1; y = x
        while y != s.zero(): y = s.add(y, x); k += 1
        return k
    def sub(s, x, y): return s.add(x, s.neg(y))
    def span(s, gens):
        H = {s.zero()}; fr = [s.zero()]
        while fr:
            h = fr.pop()
            for g in gens:
                y = s.add(h, g)
                if y not in H: H.add(y); fr.append(y)
        return H

def walks(N, T):
    """all walks length T: yield (steps tuple) ; steps 1=right 0=left"""
    return itertools.product((1, 0), repeat=T)

def walkdata(N, w):
    x, rail = 0, 'R'; nRR = nRL = nLR = nLL = 0; rho = lam = 0
    for st in w:
        if st == 1:
            if rail == 'R': nRR += 1
            else: nLR += 1
            x = (x+1) % N; rail = 'R'; rho += 1
        else:
            if rail == 'R': nRL += 1
            else: nLL += 1
            x = (x-1) % N; rail = 'L'; lam += 1
    return (x, rail), (nRR, nRL, nLR, nLL), rho, lam

def gain(A, q, cnt):
    a, b, c, d = q; g = A.zero()
    for k, e in zip(cnt, q): g = A.add(g, A.mul(k, e))
    return g

def delta(A, q):
    a, b, c, d = q
    return A.sub(A.add(a, d), A.add(b, c))
def Bof(A, q):
    a, b, c, d = q
    return A.sub(A.add(b, c), A.mul(2, a))

# ---------------- P0 control
A = G((2,)); q = ((1,), (0,), (0,), (1,)); N = 5; M = 5
B = Bof(A, q); dl = delta(A, q)
end, cnt, rho, lam = walkdata(N, (1,)*5)
g = gain(A, q, cnt); gd = gain(A, (A.zero(),)*3 + (dl,), cnt)
kap = A.add(A.mul(rho-lam, q[0]), A.mul(lam, A.add(q[1], q[2])))
P('P0 control: B=', B, 'M*B=', A.mul(M, B), 'end=', end, 'kappa=', kap, 'g-gdelta=', A.sub(g, gd),
  'PASS' if A.mul(M, B) == A.zero() and kap == (1,) and A.sub(g, gd) == (1,) and end == (0, 'R') else 'FAIL')

rng = random.Random(20261115)
GROUPS = [(2,), (3,), (4,), (5,), (6,), (8,), (2, 2), (2, 4), (3, 3), (12,), (2, 6)]

def quads(A, nrand=150):
    E = A.elems()
    if len(E) ** 4 <= 1296:
        return list(itertools.product(E, repeat=4))
    return [tuple(rng.choice(E) for _ in range(4)) for _ in range(nrand)]

# ---------------- P1, P2, P2'
TMAX = 12
walkinfo = {}
for N in range(1, 11):
    d = defaultdict(set)  # (T, vertex) -> set of (cnt, rho, lam)
    for T in range(1, TMAX+1):
        for w in walks(N, T):
            end, cnt, rho, lam = walkdata(N, w)
            d[(T, end)].add((cnt, rho, lam))
    walkinfo[N] = d
P('walk tables built')
p1fail = []; p2fail = []; stats = defaultdict(int)
for mods in GROUPS:
    A = G(mods)
    for q in quads(A):
        a, b, c, dd = q; dl = delta(A, q); B = Bof(A, q)
        qd = (A.zero(), A.zero(), A.zero(), dl)
        Lfac = A.sub(A.add(b, dl), dd)
        for N in range(1, 11):
            M = N // gcd(N, 2)
            hyp = A.mul(M, B) == A.zero()
            stats[('hyp' if hyp else 'nohyp')] += 1
            broke = False
            for (T, end), S in walkinfo[N].items():
                rs = set()
                for cnt, rho, lam in S:
                    r = A.sub(gain(A, q, cnt), gain(A, qd, cnt))
                    f = A.add(A.mul(rho-lam, a), A.mul(lam, A.add(b, c)))
                    if end[1] == 'L': f = A.add(f, Lfac)
                    if r != f: p1fail.append((mods, q, N, T, end, cnt))
                    rs.add(r)
                if len(rs) > 1:
                    broke = True
                    if hyp: p2fail.append((mods, q, N, T, end, rs))
            if not hyp:
                stats['nohyp_broken' if broke else 'nohyp_notbroken_in_range'] += 1
                if not broke and stats['nb_ex'] < 5:
                    stats['nb_ex'] += 1; P('  nohyp not broken in T<=12:', mods, q, 'N=', N)
P('P1 formula failures:', len(p1fail), p1fail[:3])
P('P2 hyp instances (group,quad,N):', stats['hyp'], 'well-definedness failures:', len(p2fail), p2fail[:3])
P("P2' nohyp instances:", stats['nohyp'], 'broken:', stats['nohyp_broken'], 'not broken within T<=12:', stats['nohyp_notbroken_in_range'])

# ---------------- P4 prefixes
def run_masks(N, masks, A=None, q=None):
    """explicit walks under masks; returns list of (end, gain, rho, lam)"""
    if A is None: A = G((1,)); q = (A.zero(),)*4
    cur = [((0, 'R'), A.zero(), 0, 0)]
    a, b, c, d = q
    for m in masks:
        nxt = []
        for (x, rail), g, rho, lam in cur:
            xr = (x+1) % N; xl = (x-1) % N
            if xr in m: nxt.append(((xr, 'R'), A.add(g, a if rail == 'R' else c), rho+1, lam))
            if xl in m: nxt.append(((xl, 'L'), A.add(g, b if rail == 'R' else d), rho, lam+1))
        cur = nxt
    return cur
for N in range(1, 11):
    pr = [{s % N} for s in range(1, N+1)]
    W = run_masks(N, pr)
    lr = run_masks(N, [{(-1) % N}, {0}])
    P('P4 N=%d right-prefix walks=%d ends=%s | left-right prefix walks=%d ends=%s' % (
        N, len(W), sorted(set(w[0] for w in W)), len(lr), sorted(set(w[0] for w in lr))),
      'OK' if (len(W) == 1 and W[0][0] == (0, 'R') and len(lr) == 1 and lr[0][0] == (0, 'R')) == (N >= 3) else 'FAIL')

# ---------------- P3 end to end
def bfs(N, r, depth, cap):
    """D_delta with delta of order r; gains as exponents mod r. state: tuple over vertices of sorted gain tuples."""
    verts = [(x, rl) for x in range(N) for rl in 'RL']
    vi = {v: i for i, v in enumerate(verts)}
    start = [()] * len(verts); start[vi[(0, 'R')]] = (0,)
    start = tuple(start)
    parent = {start: None}
    found = {}
    frontier = [start]
    masks = [frozenset(m) for k in range(1, N+1) for m in itertools.combinations(range(N), k)]
    for t in range(depth):
        nf = []
        for st in frontier:
            for m in masks:
                new = [[] for _ in verts]
                for x in range(N):
                    for rl in 'RL':
                        for g in st[vi[(x, rl)]]:
                            xr = (x+1) % N; xl = (x-1) % N
                            if xr in m: new[vi[(xr, 'R')]].append(g)
                            if xl in m: new[vi[(xl, 'L')]].append((g + (1 if rl == 'L' else 0)) % r)
                if sum(len(v) for v in new) > cap or sum(len(v) for v in new) == 0: continue
                ns = tuple(tuple(sorted(v)) for v in new)
                if ns in parent: continue
                parent[ns] = (st, m); nf.append(ns)
                for x in range(N):
                    key = (x, ns[vi[(x, 'R')]], ns[vi[(x, 'L')]])
                    if key not in found: found[key] = ns
        frontier = nf
    def masks_of(ns):
        seq = []
        while parent[ns] is not None:
            st, m = parent[ns]; seq.append(set(m)); ns = st
        return seq[::-1]
    return found, masks_of

def msets(A, items, kmax):
    out = []
    for k in range(kmax+1):
        out += [tuple(sorted(c)) for c in itertools.combinations_with_replacement(sorted(items), k)]
    return out

bfscache = {}
p3 = defaultdict(int); p3fail = []
RINGS = [3, 4, 5, 6, 7, 8]
for mods in [(2,), (3,), (4,), (6,), (2, 2), (2, 4), (3, 3)]:
    A = G(mods)
    qs = quads(A, 60)
    rng.shuffle(qs); 
    for N in RINGS:
        M = N // gcd(N, 2)
        cnt_q = 0
        for q in qs:
            a, b, c, dd = q; B = Bof(A, q)
            if A.mul(M, B) != A.zero(): p3['nohyp_skipped'] += 1; continue
            if cnt_q >= 12: break
            cnt_q += 1; p3['hyp_quads'] += 1
            dl = delta(A, q); r = A.order(dl); bc = A.add(b, c)
            H = A.span([a, bc, dl]); Dg = [A.mul(k, dl) for k in range(r)]
            reps = []; seen = set()
            for h in sorted(H):
                if h in seen: continue
                reps.append(h); seen |= {A.add(h, e) for e in Dg}
            key = (N, r)
            if key not in bfscache:
                bfscache[key] = bfs(N, r, depth=9 if N <= 5 else 7, cap=4)
            found, masks_of = bfscache[key]
            for kap in reps:
                cos = {A.add(kap, e) for e in Dg}
                x0 = mu0 = None
                for s_ in range(A.order(a)):
                    for t_ in range(A.order(bc)):
                        if A.add(A.mul(s_, a), A.mul(t_, bc)) in cos and x0 is None: x0, mu0 = s_, t_
                k0 = A.add(A.mul(x0, a), A.mul(mu0, bc)); xbar = x0 % N
                shiftL = A.sub(A.add(A.add(k0, b), dl), dd)
                cosL = {A.add(A.sub(A.add(kap, b), dd), e) for e in Dg}
                assert shiftL in cosL
                for U in msets(A, cos, 2):
                    for V in msets(A, cosL, 2):
                        if not (1 <= len(U) + len(V) <= 3): continue
                        p3['targets'] += 1
                        Ue = tuple(sorted(Dg.index(A.sub(u, k0)) for u in U))
                        Ve = tuple(sorted(Dg.index(A.sub(v, shiftL)) for v in V))
                        k = (xbar, Ue, Ve)
                        if k not in found: p3['beyond_bound'] += 1; continue
                        Sm = masks_of(found[k])
                        Wd = run_masks(N, Sm, A, (A.zero(),)*3 + (dl,))
                        at = [w for w in Wd if w[0][0] == xbar]
                        _, _, rho1, lam1 = at[0]
                        assert (rho1 - lam1 - x0) % N == 0
                        s = (rho1 - lam1 - x0) // N
                        i = (-s) % A.order(A.mul(N, a)); j = (mu0 - lam1) % A.order(bc)
                        full = [{(-1) % N}, {0}] * j + [{t % N} for t in range(1, N+1)] * i + Sm
                        Wf = run_masks(N, full, A, q)
                        mR = tuple(sorted(w[1] for w in Wf if w[0] == (xbar, 'R')))
                        mL = tuple(sorted(w[1] for w in Wf if w[0] == (xbar, 'L')))
                        if mR == tuple(sorted(U)) and mL == tuple(sorted(V)): p3["pass"] += 1; p3["i>0"] += (i>0); p3["j>0"] += (j>0); p3["oddN"] += (N%2); p3["s!=0"] += (s!=0)
                        else:
                            p3['fail'] += 1
                            if len(p3fail) < 5: p3fail.append((mods, q, N, kap, U, V, mR, mL, i, j, s, lam1))
P('P3:', dict(p3))
P('P3 failures (first):', p3fail)
P('BFS keys:', {k: len(v[0]) for k, v in bfscache.items()})
open(OUT, 'x').write('\n'.join(log) + '\n')
