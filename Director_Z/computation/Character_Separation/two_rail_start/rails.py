"""Ring walk with a start in both rails; exact arithmetic in Z[zeta_12]. Seed 20261113.

Notation: gains a,b,c,d (RR,RL,LR,LL), B=bc/a^2, H=ad/(bc), D=N/gcd(N,2), eta=chi(H), omega=chi(B)^D,
gamma=chi(c/a), start alpha|0,R>+beta|0,L> (unnormalised, alpha,beta in Z[zeta_12]), nA=|alpha|^2, nB=|beta|^2,
kappa=conj(alpha) beta gamma, s=(-1)^(D-1). X = 2^t P (unnormalised port value). N = 3..8.
Hypothesis tested per datum BEFORE any predicate: eta in {+1,-1}; only those enter; count reported.
KEY = (N, nA, nB, eta, omega+conj omega, kappa+conj kappa, (omega-conj omega)(kappa-conj kappa)).
SIG = all port values at all ticks of a fixed event list per N (free run, fork, two composites, 12 random).

PREDICATES (fixed before first run):
P1  equal KEY  =>  equal SIG                                   (eta = +-1)
P2  eta=-1, same (N,nA,nB), different KEY  =>  different SIG
P3a X(tick 1, port (1,R)) = nA+nB+2Re kappa                    (eta = +-1)
P3b fork: X = 2(nA+nB) + 2s(nA-nB)Re omega + 4s Im omega Im kappa      (eta=-1)
P3c composite via well 1:  X = (nA+nB+2Re kappa)(2+2s Re omega)        (eta=-1)
P3d composite via well -1: X = (nA+nB-2Re kappa)(2+2s Re omega)        (eta=-1)
P4  eta=-1: SIG(chi)=SIG(conj chi)  iff  Im(conj(alpha)beta)=0 or (gamma^2=1 and omega^2=1)
P5  sharp R start: at every tick, event, site, (|psi_R|^2, |psi_L|^2, conj(psi_R) psi_L gamma) is a
    function of (N, eta, omega) only                           (eta = +-1)
CONTROLS (expected to FAIL as universal statements; counts reported):
C1  "SIG depends only on (N,nA,nB,eta,Re omega,Re kappa)"
C2  "equal SIG => equal gamma"  (i.e. gamma itself is read)
C3  "equal SIG => equal omega"
"""
import sys, json, random, hashlib, itertools
import numpy as np
M = 12
def canon(v):
    v = [int(x) for x in v]
    v += [0] * (2 * M - len(v))
    for k in range(M, 2 * M):          # x^12 = 1
        v[k - M] += v[k]
    v = v[:M]
    for k in range(M - 1, 3, -1):      # Phi_12 = x^4 - x^2 + 1
        v[k - 2] += v[k]; v[k - 4] -= v[k]; v[k] = 0
    return tuple(v[:4])
def mul(u, v):
    w = np.convolve(u, v); r = np.zeros(M, dtype=np.int64)
    for k in range(len(w)): r[k % M] += w[k]
    return r
def cj(u):
    r = np.zeros(M, dtype=np.int64); u = list(u) + [0] * (M - len(u))
    for k in range(M): r[(-k) % M] += u[k]
    return r
def el(*pairs):
    r = np.zeros(M, dtype=np.int64)
    for k, c in pairs: r[k % M] += c
    return r
def root(k): return el((k, 1))
def cadd(*ts): return tuple(sum(x) for x in zip(*ts))
def cscale(c, t): return tuple(c * x for x in t)
def cmul(t, u): return canon(mul(np.array(t), np.array(u)))
ZERO = (0, 0, 0, 0)

def run(N, masks, al, be, g):
    """g = exponents (a,b,c,d). Returns list over ticks of dict (x,rail)->vec after mask."""
    st = {(0, 0): al.copy(), (0, 1): be.copy()}
    out = []
    for S in masks:
        new = {}
        for (x, r), v in st.items():
            for (nx, nr, e) in (((x + 1) % N, 0, g[0] if r == 0 else g[2]), ((x - 1) % N, 1, g[1] if r == 0 else g[3])):
                if S is not None and nx not in S: continue
                w = np.roll(v, e)
                if (nx, nr) in new: new[(nx, nr)] = new[(nx, nr)] + w
                else: new[(nx, nr)] = w
        st = new; out.append(st)
    return out

def events(N, rng):
    D = N // (2 if N % 2 == 0 else 1)
    ev = {}
    ev['free'] = [None, None, None]
    ev['fork'] = [{j % N, (-j) % N} for j in range(1, D)] + [{D % N}, {(D + 1) % N}]
    ev['comp+'] = [{1 % N}] + [{(1 + j) % N, (1 - j) % N} for j in range(1, D)] + [{(1 + D) % N}, {(D + 2) % N}]
    ev['comp-'] = [{(-1) % N}] + [{(-1 - j) % N, (-1 + j) % N} for j in range(1, D)] + [{(-1 - D) % N}, {(-D - 2) % N}]
    for i in range(12):
        T = rng.randint(2, 8); ms = []
        for _ in range(T):
            k = rng.randint(1, N); ms.append(set(rng.sample(range(N), k)))
        ev['rnd%d' % i] = ms
    return D, ev

def sig(N, ev, al, be, g):
    s = []
    for name, ms in ev.items():
        for t, st in enumerate(run(N, ms, al, be, g)):
            for key in sorted(st):
                p = canon(mul(st[key], cj(st[key])))
                if p != ZERO: s.append((name, t + 1, key, p))
    return tuple(s)

def main():
    outname = sys.argv[1]
    fout = open(outname, 'x')
    rng = random.Random(20261113)
    ORD = [2, 3, 4, 6, 12]
    STARTS = [(el((0, 1)), el()), (el(), el((0, 1))), (el((0, 1)), el((0, 1))), (el((0, 1)), el((3, 1))),
              (el((0, 1)), el((1, 1))), (el((0, 1)), el((6, 1))), (el((0, 2)), el((0, 1))), (el((0, 1)), el((3, 2))),
              (el((0, 1), (1, 1)), el((0, 1))), (el((3, 1)), el((0, 1))), (el((0, 1)), el((2, 1))), (el((0, 1)), el((0, 2)))]
    # carriers
    total = 0; qual = []; etas = {1: 0, -1: 0}
    while len(qual) < 260 and total < 20000:
        total += 1
        orders = [rng.choice(ORD) for _ in range(rng.randint(1, 3))]
        gains = [[rng.randrange(n) for n in orders] for _ in range(4)]
        ch = [rng.randrange(n) for n in orders]
        ex = [sum(r * x * (M // n) for r, x, n in zip(ch, gg, orders)) % M for gg in gains]
        a, b, c, d = ex
        H = (a + d - b - c) % M
        if H not in (0, 6): continue           # hypothesis: eta real
        eta = 1 if H == 0 else -1; etas[eta] += 1
        si = rng.randrange(len(STARTS))
        qual.append(dict(orders=orders, gains=gains, ch=ch, ex=ex, eta=eta, start=si))
    res = dict(seed=20261113, carriers_drawn=total, qualifying=len(qual), eta_plus=etas[1], eta_minus=etas[-1], perN={})
    tot = {k: [0, 0] for k in ['P1', 'P2', 'P3a', 'P3b', 'P3c', 'P3d', 'P4', 'P5']}   # [checked, failed]
    ctl = {k: [0, 0] for k in ['C1', 'C2', 'C3']}
    fails = []
    p4_cases = {'lhs_true': 0, 'lhs_false': 0}
    nonreal_prep = 0
    for N in range(3, 9):
        D, ev = events(N, rng)
        s = 1 if (D - 1) % 2 == 0 else -1
        recs = []; prep = {}
        for q in qual:
            a, b, c, d = q['ex']; eta = q['eta']
            al, be = STARTS[q['start']]
            Bx = (b + c - 2 * a) % M; om = root(Bx * D); ga = root(c - a)
            ka = mul(mul(cj(al), be), ga)
            nA = canon(mul(al, cj(al))); nB = canon(mul(be, cj(be)))
            reO = canon(om + cj(om)); reK = canon(ka + cj(ka))            # 2Re omega, 2Re kappa
            imim = canon(mul(om - cj(om), ka - cj(ka)))
            # imim = (om-conj om)(ka-conj ka) = -4 Im om Im ka
            key = (nA, nB, eta, reO, reK, imim)
            S = sig(N, ev, al, be, q['ex'])
            recs.append(dict(q=q, key=key, sig=S, om=canon(om), ga=canon(ga)))
            sd = {(n, t, k): p for (n, t, k, p) in S}
            nsum = cadd(nA, nB)
            # P3a
            tot['P3a'][0] += 1
            if sd.get(('free', 1, (1, 0)), ZERO) != cadd(nsum, reK): tot['P3a'][1] += 1; fails.append(('P3a', N, q))
            if eta == -1:
                two_sReO = cscale(s, reO)
                fork_pred = cadd(cscale(2, nsum), cmul(cadd(nA, cscale(-1, nB)), two_sReO), cscale(-s, imim))
                got = sd.get(('fork', D + 1, ((D + 1) % N, 0)), ZERO)
                tot['P3b'][0] += 1
                if got != fork_pred: tot['P3b'][1] += 1; fails.append(('P3b', N, q))
                fac = cadd((2, 0, 0, 0), two_sReO)
                tot['P3c'][0] += 1
                if sd.get(('comp+', D + 2, ((D + 2) % N, 0)), ZERO) != cmul(cadd(nsum, reK), fac): tot['P3c'][1] += 1; fails.append(('P3c', N, q))
                tot['P3d'][0] += 1
                if sd.get(('comp-', D + 2, ((-D - 2) % N, 1)), ZERO) != cmul(cadd(nsum, cscale(-1, reK)), fac): tot['P3d'][1] += 1; fails.append(('P3d', N, q))
                # P4 conjugate character
                Sc = sig(N, ev, al, be, [(-x) % M for x in q['ex']])
                z = mul(cj(al), be); imz = canon(z - cj(z))
                lhs = (imz == ZERO) or ((2 * (c - a)) % M == 0 and (2 * Bx * D) % M == 0)
                p4_cases['lhs_true' if lhs else 'lhs_false'] += 1
                tot['P4'][0] += 1
                if (S == Sc) != lhs: tot['P4'][1] += 1; fails.append(('P4', N, q))
            # P5 preparation from sharp R
            e0 = el((0, 1))
            for name, ms in ev.items():
                for t, st in enumerate(run(N, ms, e0, el(), q['ex'])):
                    for x in range(N):
                        pr = st.get((x, 0)); pl = st.get((x, 1))
                        if pr is None and pl is None: continue
                        pr = pr if pr is not None else el(); pl = pl if pl is not None else el()
                        V = canon(mul(mul(cj(pr), pl), ga))
                        val = (canon(mul(pr, cj(pr))), canon(mul(pl, cj(pl))), V)
                        k5 = (eta, canon(om), name, t, x)
                        tot['P5'][0] += 1
                        if k5 in prep:
                            if prep[k5] != val: tot['P5'][1] += 1; fails.append(('P5', N, q, name, t, x))
                        else:
                            prep[k5] = val
                            if V != canon(cj(np.array(V))): nonreal_prep += 1
        # pairwise predicates
        for r1, r2 in itertools.combinations(recs, 2):
            k1, k2 = r1['key'], r2['key']; same = r1['sig'] == r2['sig']
            if k1 == k2:
                tot['P1'][0] += 1
                if not same: tot['P1'][1] += 1; fails.append(('P1', N, r1['q'], r2['q']))
            elif k1[:3] == k2[:3] and k1[2] == -1:
                tot['P2'][0] += 1
                if same: tot['P2'][1] += 1; fails.append(('P2', N, r1['q'], r2['q']))
            if k1[:5] == k2[:5]:
                ctl['C1'][0] += 1
                if not same: ctl['C1'][1] += 1
            if same:
                ctl['C2'][0] += 1; ctl['C3'][0] += 1
                if r1['ga'] != r2['ga']: ctl['C2'][1] += 1
                if r1['om'] != r2['om']: ctl['C3'][1] += 1
        res['perN'][N] = dict(D=D, events=len(ev), distinct_keys=len({r['key'] for r in recs}),
                              distinct_sigs=len({r['sig'] for r in recs}), sig_sha=hashlib.sha256(repr([r['sig'] for r in recs]).encode()).hexdigest())
    res['predicates_checked_failed'] = tot; res['controls_checked_counterexamples'] = ctl
    res['P4_cases'] = p4_cases; res['P5_distinct_nonreal_prepared_values'] = nonreal_prep
    res['failures_first20'] = [repr(f) for f in fails[:20]]; res['n_failures'] = len(fails)
    json.dump(res, fout, indent=1, sort_keys=True); fout.close()
    print(json.dumps({k: v for k, v in res.items() if k != 'perN'}, indent=1))
    sys.exit(1 if fails else 0)
main()
