"""Bounded exhaustive search: preparation PREP(Delta_N) for four gains on rings Z_N.

Setting: two-rail digraph on Z_N, gains in A = Z_m1 x Z_m2 (additive), a: R->R, b: R->L,
c: L->R, d: L->L. Walks from (0,R). Position product event of length T: walks with
position after s steps in A_s, s=1..T. delta=a+d-b-c, B=b+c-2a, M=N/gcd(N,2),
Delta_N=<delta, M(a-d)>, H=<a,d,b+c>.

Predicates (fixed before the first run):
 P0 control: Z_6, A=Z_4, (0,1,0,0): delta=3, B=1, B*M=3, Delta_N=Z_4.
 P1 hypothesis, per case, tested before P2: B*M != 0 in A. Report the number qualifying.
    Cases with B*M == 0 are run too but reported separately (not counted as qualifying).
 P2 per case: target set = all pairs (U,V), kappa in H, U a multiset of kappa+Delta_N,
    V a multiset of kappa+b-d+Delta_N, 1 <= |U|+|V| <= KT. A target is REACHED if some state
    reachable with T <= TMAX, every intermediate state carrying at most KCAP walks in total,
    has m(x,R)=U, m(x,L)=V at some site x (selecting site x in the last mask gives a position
    product event). Predicate P2 PASS iff every target reached. A MISS is only a bounded miss.
 P3 consistency: every reached pair lies in the target family (Lemma gains at one length).
    A violation is a FAIL of the lemma or of the program.
 P4 N in {1,2}: no reached pair has |U|=1, V empty (proved in REPORT).
Exact integer arithmetic only. Seed 20261113 (no randomness used). Result file opened 'x'.
"""
import sys, itertools, random, math, json
random.seed(20261113)

def run_case(N, mods, a, b, c, d, TMAX, KCAP, KT, SMAX=400000):
    m1, m2 = mods
    G = [(i, j) for i in range(m1) for j in range(m2)]
    gi = {g: k for k, g in enumerate(G)}
    add = lambda x, y: ((x[0]+y[0]) % m1, (x[1]+y[1]) % m2)
    neg = lambda x: ((-x[0]) % m1, (-x[1]) % m2)
    mul = lambda k, x: ((k*x[0]) % m1, (k*x[1]) % m2)
    def span(gens):
        S = {(0, 0)}
        while True:
            S2 = S | {add(s, g) for s in S for g in gens}
            if S2 == S: return S
            S = S2
    M = N // math.gcd(N, 2)
    delta = add(add(a, d), neg(add(b, c)))
    B = add(add(b, c), neg(mul(2, a)))
    BM = mul(M, B)
    e = mul(M, add(a, neg(d)))
    Dl = span([delta, e]); H = span([a, d, add(b, c)])
    qual = BM != (0, 0)
    nG = len(G); V = 2*N
    # state: tuple of counts, index (x*2+rail)*nG + g
    def step(st, mask):
        new = [0]*(V*nG)
        for x in range(N):
            for rail in (0, 1):
                base = (x*2+rail)*nG
                for k in range(nG):
                    cnt = st[base+k]
                    if not cnt: continue
                    g = G[k]
                    xr, xl = (x+1) % N, (x-1) % N
                    if xr in mask:
                        h = add(g, a if rail == 0 else c)
                        new[(xr*2)*nG+gi[h]] += cnt
                    if xl in mask:
                        h = add(g, b if rail == 0 else d)
                        new[(xl*2+1)*nG+gi[h]] += cnt
        return tuple(new)
    def canon(st):
        best = None
        for s in range(N):
            r = st[2*nG*s:] + st[:2*nG*s]
            if best is None or r < best: best = r
        return best
    start = [0]*(V*nG); start[0*nG+gi[(0, 0)]] = 1
    layer = {tuple(start)}
    seen = set(layer)
    reached = set()
    truncated = False
    for T in range(1, TMAX+1):
        nxt = set()
        for st in layer:
            succ = set()
            for x in range(N):
                if any(st[(x*2)*nG:(x*2+2)*nG]):
                    succ.add((x+1) % N); succ.add((x-1) % N)
            succ = sorted(succ)
            for r in range(1, len(succ)+1):
                for mask in itertools.combinations(succ, r):
                    ns = step(st, set(mask))
                    tot = sum(ns)
                    if tot == 0 or tot > KCAP: continue
                    cs = canon(ns)
                    if cs in seen: continue
                    seen.add(cs); nxt.add(cs)
        for st in nxt:
            for x in range(N):
                U = st[(x*2)*nG:(x*2+1)*nG]; W = st[(x*2+1)*nG:(x*2+2)*nG]
                if sum(U)+sum(W) <= KT and sum(U)+sum(W) > 0:
                    reached.add((U, W))
        layer = nxt
        if not layer:
            break
        if len(seen) > SMAX:
            truncated = True; break
    # targets
    targets = set()
    for kap in H:
        cR = sorted({add(kap, t) for t in Dl}); cL = sorted({add(add(add(kap, b), neg(d)), t) for t in Dl})
        for u in range(0, KT+1):
            for v in range(0, KT+1-u):
                if u+v == 0: continue
                for Um in itertools.combinations_with_replacement(cR, u):
                    for Vm in itertools.combinations_with_replacement(cL, v):
                        Uc = [0]*nG; Wc = [0]*nG
                        for g in Um: Uc[gi[g]] += 1
                        for g in Vm: Wc[gi[g]] += 1
                        targets.add((tuple(Uc), tuple(Wc)))
    hit = targets & reached
    outside = reached - targets
    miss = sorted(targets - reached)
    def show(p):
        U, W = p
        return ([G[k] for k in range(nG) for _ in range(U[k])], [G[k] for k in range(nG) for _ in range(W[k])])
    return dict(N=N, M=M, mods=mods, gains=[a, b, c, d], delta=delta, B=B, BM=BM, e=e,
                Delta=len(Dl), H=len(H), qualifies=qual, TMAX=TMAX, KCAP=KCAP, KT=KT,
                truncated=truncated, closed=(not layer), states=len(seen), last_T=T, targets=len(targets),
                reached=len(hit), P2="PASS" if not miss else "MISS(bounded)",
                P3="PASS" if not outside else "FAIL", outside=[show(p) for p in sorted(outside)[:5]],
                miss_examples=[show(p) for p in miss[:6]])

if __name__ == "__main__":
    out = sys.argv[1]
    f = open(out, "x")
    # P0 control
    r = run_case(6, (4, 1), (0, 0), (1, 0), (0, 0), (0, 0), 1, 1, 1)
    p0 = (r["delta"] == (3, 0) and r["B"] == (1, 0) and r["BM"] == (3, 0) and r["Delta"] == 4)
    f.write(json.dumps({"P0": "PASS" if p0 else "FAIL", "control": {k: r[k] for k in ("delta", "B", "BM", "Delta")}}) + "\n"); f.flush()
    cases = json.loads(sys.argv[2])
    nq = 0
    for cs in cases:
        r = run_case(*cs)
        nq += r["qualifies"]
        f.write(json.dumps(r) + "\n"); f.flush()
        print(r["N"], r["mods"], r["gains"], "qual", r["qualifies"], "Delta", r["Delta"], r["P2"], r["reached"], "/", r["targets"], "P3", r["P3"], "T", r["last_T"], "trunc", r["truncated"], "closed", r["closed"], "states", r["states"], flush=True)
    f.write(json.dumps({"qualifying": nq, "cases": len(cases)}) + "\n")
    f.close()
