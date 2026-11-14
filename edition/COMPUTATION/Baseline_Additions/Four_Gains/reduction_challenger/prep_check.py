"""Challenger program for PREP_REDUCTION.md (Lemma R, Proposition P, ring paragraph).

Predicates fixed before the first run (kept whatever the outcome):
 P0 control: Z6, (1,2,3,4): delta=0, r=1, gain(RLLR from (0,R)) = 4.
 P1 Lemma R (line): for every listed group A, every gain quadruple (all if |A|^4 <= 4096, else 1500 random,
    seed 20261114), every walk of length T<=12 from (0,R): g = kappa_{T,x} + g_delta (end R),
    g = kappa_{T,x} + b + delta - d + g_delta (end L), additive notation; g, g_delta computed by traversal.
    Hypothesis per carrier: A finite abelian, gains in A (always holds; counted).
 P2 Prop P (line), constructive: for each sampled carrier and EVERY coset kappa<delta> of <delta> in H, and targets
    U in M(kappa<delta>), V in M(kappa b d^-1 <delta>) with |U|,|V| <= 2 (random subset), run steps 1-6 with
    Lemma 5.34 replaced by a brute-force search over position masks at site 0 plus a prefix of x right steps;
    the four-gain multisets of the final event, computed by exact DP over walks (not via Lemma R), equal (U,V).
    Failure of the brute-force search within its bound is reported as SEARCH-BOUND, not as a failure of P.
 P3 ring factor: on Z_N, N in {6,7,8,9,12}, T<=12, for walks w,w' of equal length ending at the same vertex,
    (g/g_delta)(w) - (g/g_delta)(w') = -(rho_w - rho_w')/M * B, B = b+c-2a (additive), rho difference divisible by M.
 P4 B^M = 1 => (a/d)^M in <delta>, all quadruples of small groups, M in {3..12}; also count quadruples with
    B^M in <delta> but B^M != 1 (Delta_N = <delta> while the recoding ratio is not fixed).
 P5 ring, odd N, B^M=1: the line proof's step 5 (pad by 2 only, at the site x of step 1) reaches every coset?
    Tested by: for each coset, does some T with T = x (mod 2)?? -- on odd N the event length parity is free; count
    cosets reached only by lengths T with T != x (mod 2) (reported, not a pass/fail of the paragraph).
 P6 ring, B^M != 1: exhibit an event (all walks of length T) at a vertex whose four-gain multiset is not any single
    translate of its D_delta multiset (shows the reduction really fails there).
Result file: results.txt, refused if it exists.
"""
import itertools, random, sys, os
from collections import Counter, defaultdict

OUT = "results.txt"
if os.path.exists(OUT):
    sys.exit("refusing to overwrite results.txt")
random.seed(20261114)
lines = []
def log(s):
    lines.append(s); print(s, flush=True)

class G:
    def __init__(self, mods): self.mods = tuple(mods)
    def els(self): return list(itertools.product(*[range(m) for m in self.mods]))
    def add(self, x, y): return tuple((a+b) % m for a, b, m in zip(x, y, self.mods))
    def neg(self, x): return tuple((-a) % m for a, m in zip(x, self.mods))
    def mul(self, k, x): return tuple((k*a) % m for a, m in zip(x, self.mods))
    def zero(self): return tuple(0 for _ in self.mods)
    def sub(self, x, y): return self.add(x, self.neg(y))
    def order(self, x):
        k, y = 1, x
        while y != self.zero(): y = self.add(y, x); k += 1
        return k
    def span(self, gens):
        S = {self.zero()}; fr = [self.zero()]
        while fr:
            y = fr.pop()
            for g in gens:
                z = self.add(y, g)
                if z not in S: S.add(z); fr.append(z)
        return S

GROUPS = [(2,), (3,), (4,), (5,), (6,), (8,), (2,2), (2,4), (3,3), (2,2,2), (4,4), (2,6)]

def walk_gain(A, q, steps, N=None):
    a, b, c, d = q
    x, rail, g = 0, 'R', A.zero()
    rho = 0; nLL = 0
    for s in steps:
        if s == 'R':
            g = A.add(g, a if rail == 'R' else c); x += 1; rho += 1; rail = 'R'
        else:
            g = A.add(g, b if rail == 'R' else d)
            if rail == 'L': nLL += 1
            x -= 1; rail = 'L'
    if N: x %= N
    return x, rail, g, rho, nLL

# P0
A6 = G((6,)); q0 = ((1,), (2,), (3,), (4,))
delta0 = A6.sub(A6.add(q0[0], q0[3]), A6.add(q0[1], q0[2]))
x0, r0, g0, _, _ = walk_gain(A6, q0, "RLLR")
p0 = (delta0 == (0,) and A6.order(delta0) == 1 and g0 == (4,) and (x0, r0) == (0, 'R'))
log(f"P0 control: delta={delta0} r={A6.order(delta0)} gain(RLLR)={g0} end={(x0,r0)} -> {'PASS' if p0 else 'FAIL'}")

def quads(A, cap):
    E = A.els()
    if len(E)**4 <= cap: return list(itertools.product(E, repeat=4))
    return [tuple(random.choice(E) for _ in range(4)) for _ in range(1500)]

# P1: walks by traversal; gain determined by (nRR,nRL,nLR,nLL) but we compute directly
WALKS = []
for T in range(0, 13):
    for st in itertools.product('RL', repeat=T):
        cnt = Counter(); rail = 'R'; x = 0
        for s in st:
            cnt[rail+s] += 1; rail = s; x += 1 if s == 'R' else -1
        WALKS.append((T, x, rail, (cnt['RR'], cnt['RL'], cnt['LR'], cnt['LL'])))
CLASSES = Counter(WALKS)   # exact: gain of a walk = nRR a + nRL b + nLR c + nLL d
log(f"P1 walks T<=12: {len(WALKS)}, distinct (T,x,rail,arc-count) classes: {len(CLASSES)}")
# sanity: arc-count gain equals traversal gain on a sample
A = G((2,4)); okt = True
for _ in range(300):
    q = tuple(random.choice(A.els()) for _ in range(4))
    T = random.randint(0, 12); st = ''.join(random.choice('RL') for _ in range(T))
    x, rail, g, _, _ = walk_gain(A, q, st)
    cnt = Counter(); rr = 'R'
    for s in st: cnt[rr+s] += 1; rr = s
    g2 = A.zero()
    for k, arc in zip(q, ('RR','RL','LR','LL')): g2 = A.add(g2, A.mul(cnt[arc], k))
    okt &= (g == g2)
log(f"P1 sanity traversal == arc-count gain on 300 random walks: {okt}")

p1_tot = 0; p1_fail = []; p1_carriers = 0
for mods in GROUPS:
    A = G(mods)
    for q in quads(A, 4096):
        a, b, c, d = q; p1_carriers += 1
        delta = A.sub(A.add(a, d), A.add(b, c))
        for (T, x, rail, (nRR, nRL, nLR, nLL)), mult in CLASSES.items():
            g = A.zero()
            for k, n in zip(q, (nRR, nRL, nLR, nLL)): g = A.add(g, A.mul(n, k))
            gd = A.mul(nLL, delta)
            lam = (T - x)//2
            kap = A.add(A.mul(x, a), A.mul(lam, A.add(b, c)))
            pred = A.add(kap, gd) if rail == 'R' else A.add(A.add(kap, A.sub(A.add(b, delta), d)), gd)
            p1_tot += 1
            if pred != g: p1_fail.append((mods, q, T, x, rail))
log(f"P1 Lemma R: carriers {p1_carriers} (all qualify: finite abelian), class checks {p1_tot}, failures {len(p1_fail)} -> {'PASS' if not p1_fail else 'FAIL'}")
for f in p1_fail[:5]: log(f"  P1 fail {f}")

# ---------- P2 ----------
def dp_event(A, q, masks, N=None):
    """exact multiset of gains per vertex for the position product event with sets masks[0..T-1]."""
    a, b, c, d = q
    st = {(0, 'R'): Counter({A.zero(): 1})}
    for Ms in masks:
        nst = defaultdict(Counter)
        for (x, rail), ms in st.items():
            for step in 'RL':
                nx = x + (1 if step == 'R' else -1)
                if N: nx %= N
                if nx not in Ms: continue
                arc = (a if rail == 'R' else c) if step == 'R' else (b if rail == 'R' else d)
                for g, m in ms.items(): nst[(nx, step)][A.add(g, arc)] += m
        st = {k: v for k, v in nst.items() if sum(v.values())}
    return st

def search_Ddelta(r, Ut, Vt, maxT=9, window=(-4, 4), cap=400000):
    """BFS over position masks in D_delta (exponents mod r) for target multisets at site 0.
    Returns masks or None.  States: frozenset of (vertex, exponent, count)."""
    def key(st): return frozenset((v, e, m) for v, ms in st.items() for e, m in ms.items())
    start = {(0, 'R'): Counter({0: 1})}
    frontier = [(start, [])]; seen = {key(start)}
    tgtR = Counter({e: m for e, m in Ut.items() if m}); tgtL = Counter({e: m for e, m in Vt.items() if m})
    for T in range(1, maxT+1):
        nf = []
        for st, masks in frontier:
            reach = sorted({x + s for (x, _) in st for s in (1, -1) if window[0] <= x + s <= window[1]})
            for k in range(1, len(reach)+1):
                for sub in itertools.combinations(reach, k):
                    Ms = set(sub); nst = defaultdict(Counter)
                    for (x, rail), ms in st.items():
                        for step in 'RL':
                            nx = x + (1 if step == 'R' else -1)
                            if nx not in Ms: continue
                            inc = 1 if (step == 'L' and rail == 'L') else 0
                            for e, m in ms.items(): nst[(nx, step)][(e+inc) % r] += m
                    nst = {kk: v for kk, v in nst.items() if sum(v.values())}
                    if not nst: continue
                    if Counter(nst.get((0, 'R'), {})) == tgtR and Counter(nst.get((0, 'L'), {})) == tgtL and (tgtR or tgtL):
                        return masks + [Ms]
                    kk = key(nst)
                    if kk in seen: continue
                    if sum(m for v in nst.values() for m in v.values()) > 6: continue
                    seen.add(kk); nf.append((nst, masks + [Ms]))
                    if len(seen) > cap: return None
        frontier = nf
    return None

cache = {}
p2_cases = 0; p2_fail = []; p2_bound = 0; p2_carriers = 0; cos_total = 0
for mods in [(2,), (3,), (4,), (6,), (2,2), (2,4), (3,3), (2,2,2)]:
    A = G(mods); E = A.els()
    qs = [tuple(random.choice(E) for _ in range(4)) for _ in range(6)]
    # force edge cases: a trivial, delta trivial, H != A
    z = A.zero(); qs.append((z, E[1], E[1], A.add(E[1], E[1])))         # a = 0, delta = 0
    qs.append((E[1], z, z, z))                                          # bc = 0, delta = a
    for q in qs:
        a, b, c, d = q; p2_carriers += 1
        delta = A.sub(A.add(a, d), A.add(b, c)); bc = A.add(b, c)
        r = A.order(delta); D = sorted(A.span([delta]))
        dl = [A.mul(j, delta) for j in range(r)]  # exponent j -> element
        H = A.span([a, d, bc])
        cosets = {}
        for h in H: cosets.setdefault(frozenset(A.add(h, t) for t in D), h)
        for cos, kappa in cosets.items():
            cos_total += 1
            # targets
            Lcos = [A.add(A.sub(A.add(kappa, b), d), t) for t in dl]
            Rcos = [A.add(kappa, t) for t in dl]
            targets = []
            for nu in range(0, 3):
                for nv in range(0, 3):
                    if nu + nv == 0: continue
                    U = Counter(random.choice(Rcos) for _ in range(nu)); V = Counter(random.choice(Lcos) for _ in range(nv))
                    targets.append((U, V))
            targets = random.sample(targets, 3)
            for U, V in targets:
                p2_cases += 1
                # step 1
                ea, eb = A.order(a), A.order(bc)
                x = mu0 = None
                for xx in range(ea):
                    for mm in range(eb):
                        k0 = A.add(A.mul(xx, a), A.mul(mm, bc))
                        if A.sub(k0, kappa) in D: x, mu0 = xx, mm; break
                    if x is not None: break
                k0 = A.add(A.mul(x, a), A.mul(mu0, bc))
                # step 2: exponents
                shiftL = A.add(k0, A.sub(A.add(b, delta), d))
                Ut = Counter(); Vt = Counter()
                for g, m in U.items(): Ut[dl.index(A.sub(g, k0))] += m
                for g, m in V.items(): Vt[dl.index(A.sub(g, shiftL))] += m
                ck = (r, frozenset(Ut.items()), frozenset(Vt.items()))
                if ck not in cache: cache[ck] = search_Ddelta(r, Ut, Vt)
                m0 = cache[ck]
                if m0 is None: p2_bound += 1; continue
                # step 3: Lemma 5.34 at site x = prefix of x right steps then shifted masks
                masks = [{s} for s in range(1, x+1)] + [{y + x for y in M} for M in m0]
                T0 = len(masks); assert (T0 - x) % 2 == 0
                lam1 = (T0 - x)//2
                # step 5
                k = next(kk for kk in range(eb) if (lam1 + kk - mu0) % eb == 0)
                pad = []
                for _ in range(k): pad += [{-1}, {0}]
                S = pad + masks
                st = dp_event(A, q, S)
                gotU = st.get((x, 'R'), Counter()); gotV = st.get((x, 'L'), Counter())
                ok = (Counter({g: m for g, m in gotU.items() if m}) == U and Counter({g: m for g, m in gotV.items() if m}) == V)
                # also D_delta multiset preserved by padding
                if not ok: p2_fail.append((mods, q, kappa, dict(U), dict(V), x, mu0, T0, k, dict(gotU), dict(gotV)))
log(f"P2 Prop P: carriers {p2_carriers}, cosets kappa<delta> in H tested {cos_total}, target cases {p2_cases}, "
    f"SEARCH-BOUND {p2_bound}, failures {len(p2_fail)} -> {'PASS' if not p2_fail else 'FAIL'} (on {p2_cases-p2_bound} constructed)")
for f in p2_fail[:5]: log(f"  P2 fail {f}")

# ---------- P3 ----------
p3_checks = 0; p3_fail = []; p3_div = True
for N in (6, 7, 8, 9, 12):
    M = N // (2 if N % 2 == 0 else 1)
    for mods in [(4,), (2, 4), (3, 3), (5,)]:
        A = G(mods)
        for q in [tuple(random.choice(A.els()) for _ in range(4)) for _ in range(5)]:
            a, b, c, d = q; delta = A.sub(A.add(a, d), A.add(b, c)); B = A.sub(A.add(b, c), A.mul(2, a))
            for T in range(0, 13):
                byv = defaultdict(list)
                for st in itertools.product('RL', repeat=T):
                    x, rail, g, rho, nLL = walk_gain(A, q, st, N)
                    byv[(x, rail)].append((rho, A.sub(g, A.mul(nLL, delta))))
                for v, L in byv.items():
                    r0_, q0_ = L[0]
                    for rho, rat in L[1:]:
                        p3_checks += 1
                        if (rho - r0_) % M: p3_div = False; continue
                        j = (rho - r0_)//M
                        if A.sub(rat, q0_) != A.mul(-j*M, B): p3_fail.append((N, mods, q, T, v))
log(f"P3 ring factor B^(-Mj): checks {p3_checks}, rho-differences divisible by M: {p3_div}, failures {len(p3_fail)} -> {'PASS' if not p3_fail and p3_div else 'FAIL'}")

# ---------- P4 ----------
p4_q = 0; p4_fail = 0; p4_extra = 0; ex_extra = None
for mods in [(2,), (3,), (4,), (6,), (2, 2), (2, 4), (3, 3)]:
    A = G(mods)
    for q in itertools.product(A.els(), repeat=4):
        a, b, c, d = q; delta = A.sub(A.add(a, d), A.add(b, c)); B = A.sub(A.add(b, c), A.mul(2, a))
        D = A.span([delta])
        for M in range(3, 13):
            p4_q += 1
            BM = A.mul(M, B); adM = A.mul(M, A.sub(a, d))
            if BM == A.zero() and adM not in D: p4_fail += 1
            if BM != A.zero() and BM in D:
                p4_extra += 1
                assert adM in D
                if ex_extra is None and M >= 6: ex_extra = (mods, q, M)
log(f"P4 B^M=1 => (a/d)^M in <delta>: (carrier,M) pairs {p4_q}, failures {p4_fail} -> {'PASS' if not p4_fail else 'FAIL'}")
log(f"P4b pairs with B^M != 1 but B^M in <delta> (Delta_N=<delta>, ratio not fixed): {p4_extra}; example (M>=6) {ex_extra}")

# ---------- P5 ----------
# odd N, B^M = 1: line-proof step 5 uses lengths T = x (mod 2) only. On odd N the ratio at (x,R), length T, is
# a^rho (bc-a)^lam with any rho, 2rho = T+x mod N.  Cosets reached by lengths T = x mod 2 vs all T.
p5_rows = 0; p5_gap = []
for N in (7, 9):
    M = N
    for mods in [(2,), (4,), (2, 2), (2, 4), (6,)]:
        A = G(mods)
        for q in itertools.product(A.els(), repeat=4):
            a, b, c, d = q; delta = A.sub(A.add(a, d), A.add(b, c)); B = A.sub(A.add(b, c), A.mul(2, a))
            if A.mul(M, B) != A.zero(): continue
            p5_rows += 1
            D = frozenset(A.span([delta])); bc = A.add(b, c)
            def cos(g): return frozenset(A.add(g, t) for t in D)
            H = A.span([a, d, bc]); allc = {cos(h) for h in H}
            x = 0
            same, anyp = set(), set()
            for T in range(0, 2*N*A.order(a)*A.order(bc) + 2):
                rho = next(rr for rr in range(N) if (2*rr - T - x) % N == 0)
                rho_l = rho + N * ((T - rho) // N + 1) if False else rho
                lam = T - rho
                ratio = A.add(A.mul(rho, a), A.mul(lam, A.sub(bc, a)))
                anyp.add(cos(ratio))
                if (T - x) % 2 == 0: same.add(cos(ratio))
            if same != allc: p5_gap.append((N, mods, q, len(same), len(allc), len(anyp)))
log(f"P5 odd N with B^M=1: carriers {p5_rows}; carriers where lengths T=x (mod 2) at fixed site x=0 miss a coset: {len(p5_gap)}; example {p5_gap[:2]}")

# ---------- P6 ----------
p6 = None
for mods in [(4,), (2, 4), (3, 3)]:
    A = G(mods)
    for q in itertools.product(A.els(), repeat=4):
        a, b, c, d = q; delta = A.sub(A.add(a, d), A.add(b, c)); B = A.sub(A.add(b, c), A.mul(2, a))
        N, M = 12, 6
        if A.mul(M, B) == A.zero(): continue
        T = 8
        masks = [set(range(N))] * T
        st4 = dp_event(A, q, masks, N)
        qd = (A.zero(), A.zero(), A.zero(), delta)
        std = dp_event(A, qd, masks, N)
        for v in st4:
            m4, md = st4[v], std[v]
            if not any(Counter({A.add(g, t): m for g, m in md.items()}) == m4 for t in A.els()):
                p6 = (mods, q, N, T, v); break
        if p6: break
    if p6: break
log(f"P6 ring N=12, B^M!=1: vertex where four-gain multiset is no translate of the D_delta multiset: {p6}")

with open(OUT, "x") as f: f.write("\n".join(lines) + "\n")
