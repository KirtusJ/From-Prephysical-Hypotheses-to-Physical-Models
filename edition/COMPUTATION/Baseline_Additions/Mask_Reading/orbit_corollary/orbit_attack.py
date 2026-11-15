"""Challenger program for Corollary cor:maskorbit (the list is an orbit) and the paragraph after it.

Arithmetic: exact. Every arc gain is a K-th root of unity (K = lcm(N,24)); an amplitude is an
element of the group ring Z[C_K]; |amp|^2 is computed exactly in Z[C_K] and reduced to the
canonical basis of Z[zeta_K] (mod the cyclotomic polynomial Phi_K). Two probabilities at a port
are equal iff the reduced vectors are equal (the factor 2^-t is common). Seed fixed: 20261114.

Conventions: walk on Z_N, vertices (x,R),(x,L); right step to (x+1,R), left step to (x-1,L);
gains a: R->R, b: R->L, c: L->R, d: L->L. Sharp start = amplitude 1 on (0,R). Masks are applied
after each step to the site occupied. Ports: every (t, x, rail) for 1<=t<=T, T = M+3.
u = b c / a^2, M = N/gcd(N,2). Equality "Re u'^M = Re u^M" is tested exactly as
u'^M in {u^M, conj(u^M)} (exponent arithmetic mod K).

Predicates (fixed before the first run):
 P0 hypothesis: candidate coins (a,b,c,d) drawn uniformly from mu_K^4; a coin qualifies iff
    ad = -bc exactly. Report drawn / qualifying per N. Only qualifying coins are used in P1-P3.
 P1 (if, maps): for each qualifying coin C and a random composition of the four maps
    (common phase g in mu_K, rail phase lambda in mu_K, site phase zeta in mu_N, conjugation),
    every port of every event (random masks + the fork + the fork after one tick + no mask)
    has equal probability from the sharp start. Expected: always.
 P2 (only if): for each pair of qualifying coins with Re u^M different, some port differs, and
    in particular the fork port (M+1, M+1, R) differs. Expected: always.
 P2b (clock): for such pairs no port with t <= M differs in any tested event. Expected: always.
 P3 (orbit transitivity): for each pair with Re u^M equal, the proof's construction
    (conjugate if needed, site phase zeta with zeta^-2 = u'/u... , then g, lambda) carries one
    coin exactly onto the other; and all port probabilities agree. Expected: always.
 P4 (scope, non-sharp start): start (0,R) amplitude 1, (0,L) amplitude i. Count orbit-related
    pairs (by rail phase or conjugation alone) whose statistics differ. Expected: some differ
    (so the maps are changes of description only if the start is transformed too).
 P5 (scope, eta != -1): coins with ad = +bc (eta=+1) and ad = i bc (eta=i): count pairs with
    equal Re u^M and equal eta whose sharp-start statistics differ. Expected eta=+1: none;
    eta=i: unknown, reported.
 P6 (N<=2): for N=1,2, same sharp-start statistics iff Re u equal (maps as in the corollary).
    Expected: true (the corollary would then hold for N>=1).
 P7 (four sites, {+-1}): N=4 coins (1,1,1,-1), (1,1,-1,1), (1,-1,1,1): equal statistics; no
    composition with g, lambda, zeta in {+-1} (and conjugation) relates u=1 to u=-1; list which
    (g, lambda, zeta) in mu_8 x mu_8 x mu_4 relate (1,1,1,-1) to each u=-1 coin.
Failed predicates are kept in the result file.
"""
import sys, os, math, json, random, hashlib
import numpy as np

SEED = 20261114
OUT = sys.argv[1] if len(sys.argv) > 1 else "result.json"
if os.path.exists(OUT):
    sys.exit("refusing to overwrite " + OUT)

def cyclo_reduction(K):
    # Phi_K via integer polynomial division of x^K-1 by Phi_d for d|K, d<K
    from functools import lru_cache
    @lru_cache(None)
    def phi(n):
        p = [0]*(n+1); p[0] = -1; p[n] = 1   # coefficients low->high of x^n - 1
        p = np.array(p, dtype=object)
        for d in range(1, n):
            if n % d == 0:
                q = np.array(phi(d), dtype=object)
                p = polydiv(p, q)
        return tuple(int(v) for v in p)
    def polydiv(p, q):
        p = list(p); q = list(q)
        out = [0]*(len(p)-len(q)+1)
        for i in range(len(p)-len(q), -1, -1):
            coef = p[i+len(q)-1] // q[-1]
            out[i] = coef
            for j in range(len(q)):
                p[i+j] -= coef*q[j]
        assert all(v == 0 for v in p[:len(q)-1])
        return np.array(out, dtype=object)
    P = list(phi(K)); deg = len(P)-1
    R = np.zeros((K, deg), dtype=np.int64)
    cur = [0]*deg
    for j in range(K):
        if j < deg:
            cur = [0]*deg; cur[j] = 1
        else:
            # cur = x * prev mod Phi
            top = prev[-1]
            cur = [0] + prev[:-1]
            for i in range(deg):
                cur[i] -= top*P[i]
        R[j] = cur
        prev = cur
    return R

def norm_vecs(A, K):
    # A: (n, K) int64 group-ring elements; return |a|^2 in Z[C_K]
    out = np.zeros_like(A)
    for i in range(A.shape[0]):
        v = A[i]
        if not v.any():
            continue
        vr = np.roll(v[::-1], 1)          # conj: exponent e -> -e
        full = np.convolve(v, vr)
        res = full[:K].copy(); res[:K-1] += full[K:]
        out[i] = res
    return out

def run_event(coin, N, K, masks, start):
    # coin: exponents (ea,eb,ec,ed) mod K. start: dict {(x,rail): exponent} amplitude roots
    ea, eb, ec, ed = coin
    amp = np.zeros((N, 2, K), dtype=np.int64)  # rail 0 = R, 1 = L
    for (x, r), e in start.items():
        amp[x % N, r, e % K] += 1
    ports = []
    for t, S in enumerate(masks, 1):
        new = np.zeros_like(amp)
        for x in range(N):
            vR, vL = amp[x, 0], amp[x, 1]
            if vR.any() or vL.any():
                new[(x+1) % N, 0] += np.roll(vR, ea) + np.roll(vL, ec)
                new[(x-1) % N, 1] += np.roll(vR, eb) + np.roll(vL, ed)
        keep = np.zeros(N, dtype=bool)
        for s in S: keep[s % N] = True
        new[~keep] = 0
        amp = new
        ports.append(amp.reshape(2*N, K).copy())
    return ports

def signature(coin, N, K, R, events, start):
    sig = []
    for masks in events:
        ports = run_event(coin, N, K, masks, start)
        A = np.concatenate(ports, axis=0)
        red = norm_vecs(A, K) @ R
        sig.append(red.reshape(len(masks), 2*N, -1))
    return sig

def fork_events(N, M):
    full = list(range(N))
    fork = [[j, -j] for j in range(1, M)] + [[M], [M+1]]
    fork1 = [[1]] + [[1+j, 1-j] for j in range(1, M)] + [[1+M], [2+M]]
    mirror = [[-1]] + [[-1-j, -1+j] for j in range(1, M)] + [[-1-M], [-2-M]]
    return [fork, fork1, mirror, [full]*(M+3)]

def apply_maps(coin, K, N, rng, steps=4):
    ea, eb, ec, ed = coin
    for _ in range(steps):
        k = rng.randrange(4)
        if k == 0:
            g = rng.randrange(K); ea, eb, ec, ed = ea+g, eb+g, ec+g, ed+g
        elif k == 1:
            l = rng.randrange(K); eb, ec = eb-l, ec+l
        elif k == 2:
            z = (K//N)*rng.randrange(N); ea, eb, ec, ed = ea+z, eb-z, ec+z, ed-z
        else:
            ea, eb, ec, ed = -ea, -eb, -ec, -ed
    return tuple(e % K for e in (ea, eb, ec, ed))

def u_exp(coin, K):
    ea, eb, ec, ed = coin
    return (eb+ec-2*ea) % K

def reu_equal(c1, c2, K, M):
    w1 = (M*u_exp(c1, K)) % K; w2 = (M*u_exp(c2, K)) % K
    return w2 == w1 or w2 == (-w1) % K

def construct(c1, c2, K, N, M):
    # proof's construction: returns image of c1 or None
    ea, eb, ec, ed = c1
    u1, u2 = u_exp(c1, K), u_exp(c2, K)
    if (M*u2) % K != (M*u1) % K:
        ea, eb, ec, ed = -ea % K, -eb % K, -ec % K, -ed % K
        u1 = (-u1) % K
    if (M*u2) % K != (M*u1) % K:
        return None
    for j in range(N):
        z = (K//N)*j
        if (u1 - 2*z) % K == u2:
            break
    else:
        return None
    ea, eb, ec, ed = ea+z, eb-z, ec+z, ed-z
    g = c2[0]-ea
    ea, eb, ec, ed = ea+g, eb+g, ec+g, ed+g
    lam = c2[2]-ec
    eb, ec = eb-lam, ec+lam
    return tuple(e % K for e in (ea, eb, ec, ed))

def sig_eq(s1, s2, tmax=None):
    for e1, e2 in zip(s1, s2):
        a = e1 if tmax is None else e1[:tmax]
        b = e2 if tmax is None else e2[:tmax]
        if not np.array_equal(a, b):
            return False
    return True

def draw_coins(K, rng, ncand, eta_exp):
    got = []; q = 0
    for _ in range(ncand):
        c = tuple(rng.randrange(K) for _ in range(4))
        if (c[0]+c[3]-c[1]-c[2]-eta_exp) % K == 0:
            q += 1; got.append(c)
    return got, q

def main():
    rng = random.Random(SEED)
    res = {"seed": SEED, "per_N": {}, "fail": []}
    for N in list(range(3, 10)) + [1, 2]:
        M = N // math.gcd(N, 2); K = math.lcm(N, 24); T = M + 3
        R = cyclo_reduction(K)
        events = fork_events(N, M) if N >= 3 else [[list(range(N))]*(T)]
        for _ in range(14):
            p = rng.choice([0.3, 0.5, 0.7])
            events.append([[x for x in range(N) if rng.random() < p] or [rng.randrange(N)] for _ in range(T)])
        ncand = 30*K
        coins, q = draw_coins(K, rng, ncand, K//2)
        coins = coins[:16]
        sharp = {(0, 0): 0}
        d = {"M": M, "K": K, "candidates": ncand, "qualifying": q, "used": len(coins), "events": len(events)}
        sigs = {c: signature(c, N, K, R, events, sharp) for c in coins}
        # P1
        p1n = p1f = 0
        for c in coins:
            img = apply_maps(c, K, N, rng)
            assert (img[0]+img[3]-img[1]-img[2]-K//2) % K == 0
            s = signature(img, N, K, R, events, sharp)
            p1n += 1
            if not sig_eq(s, sigs[c]):
                p1f += 1; res["fail"].append(["P1", N, c, img])
        d["P1"] = [p1n, p1f]
        # P2, P2b, P3
        p2n = p2f = p2fork = p2bf = p3n = p3f = 0
        for i in range(len(coins)):
            for j in range(i+1, len(coins)):
                c1, c2 = coins[i], coins[j]
                if reu_equal(c1, c2, K, M):
                    p3n += 1
                    img = construct(c1, c2, K, N, M)
                    if img != c2 or not sig_eq(sigs[c1], sigs[c2]):
                        p3f += 1; res["fail"].append(["P3", N, c1, c2, img])
                else:
                    p2n += 1
                    if sig_eq(sigs[c1], sigs[c2]):
                        p2f += 1; res["fail"].append(["P2", N, c1, c2])
                    if N >= 3:
                        fk = sigs[c1][0][M, 2*(((M+1) % N)) + 0]  # rows: x*2+rail? fixed below
                    if not sig_eq(sigs[c1], sigs[c2], tmax=M):
                        p2bf += 1; res["fail"].append(["P2b", N, c1, c2])
        d["P2_pairs_fail"] = [p2n, p2f]; d["P2b_fail"] = p2bf; d["P3_pairs_fail"] = [p3n, p3f]
        # fork port specifically: event 0, t = M+1 (index M), site M+1, rail R -> row (x, rail) reshaped as (N,2)
        if N >= 3:
            ff = 0; fn = 0
            for i in range(len(coins)):
                for j in range(i+1, len(coins)):
                    c1, c2 = coins[i], coins[j]
                    if not reu_equal(c1, c2, K, M):
                        fn += 1
                        row = ((M+1) % N)*2 + 0
                        if np.array_equal(sigs[c1][0][M][row], sigs[c2][0][M][row]):
                            ff += 1; res["fail"].append(["P2fork", N, c1, c2])
            d["P2fork_pairs_fail"] = [fn, ff]
        # P4 non-sharp start: (0,R)=1, (0,L)=i
        if N >= 3:
            st = {(0, 0): 0, (0, 1): K//4}
            p4n = p4d = 0; ex = None
            for c in coins[:8]:
                s0 = signature(c, N, K, R, events[:4], st)
                l = rng.randrange(1, K)
                for img in [(c[0], (c[1]-l) % K, (c[2]+l) % K, c[3]), tuple((-e) % K for e in c)]:
                    p4n += 1
                    if not sig_eq(s0, signature(img, N, K, R, events[:4], st)):
                        p4d += 1; ex = ex or [c, img]
            d["P4_pairs_differ"] = [p4n, p4d, ex]
        # P5 eta=+1 and eta=i
        if N in (3, 4, 5):
            for name, ee in (("eta+1", 0), ("eta_i", K//4)):
                cs, qq = draw_coins(K, rng, 20*K, ee); cs = cs[:10]
                ss = {c: signature(c, N, K, R, events[:6], sharp) for c in cs}
                n_eq = n_diff = 0; ex = None
                for i in range(len(cs)):
                    for j in range(i+1, len(cs)):
                        if reu_equal(cs[i], cs[j], K, M):
                            n_eq += 1
                            if not sig_eq(ss[cs[i]], ss[cs[j]]):
                                n_diff += 1; ex = ex or [cs[i], cs[j]]
                # also conjugate pairs
                nc = 0
                for c in cs:
                    cc = tuple((-e) % K for e in c)
                    if not sig_eq(ss[c], signature(cc, N, K, R, events[:6], sharp)):
                        nc += 1
                d["P5_" + name] = {"qualifying": qq, "equalReuM_pairs": n_eq, "differ": n_diff, "example": ex, "conj_pairs_differ": nc}
        res["per_N"][N] = d
        print(N, json.dumps(d, default=str), flush=True)
    # P7
    N, K = 4, 24; R = cyclo_reduction(K); M = 2
    E = lambda c: tuple(0 if v == 1 else K//2 for v in c)
    c0, c1, c2 = E((1, 1, 1, -1)), E((1, 1, -1, 1)), E((1, -1, 1, 1))
    events = fork_events(N, M)
    rr = random.Random(SEED+7)
    for _ in range(14):
        events.append([[x for x in range(N) if rr.random() < 0.5] or [0] for _ in range(M+3)])
    s = [signature(c, N, K, R, events, {(0, 0): 0}) for c in (c0, c1, c2)]
    p7 = {"equal_stats": [sig_eq(s[0], s[1]), sig_eq(s[0], s[2])]}
    rel = {1: [], 2: []}
    for conj in (0, 1):
        for g in range(8):
            for l in range(8):
                for z in range(4):
                    ea, eb, ec, ed = c0
                    if conj: ea, eb, ec, ed = -ea, -eb, -ec, -ed
                    G, L, Z = g*3, l*3, z*6
                    img = tuple(e % K for e in (ea+G+Z, eb+G-L-Z, ec+G+L+Z, ed+G-Z))
                    for k, tgt in ((1, c1), (2, c2)):
                        if img == tgt:
                            rel[k].append({"conj": conj, "g": f"e^(2pi i {g}/8)", "lambda": f"e^(2pi i {l}/8)", "zeta": f"i^{z}"})
    p7["relating_maps_to_(1,1,-1,1)"] = rel[1]; p7["relating_maps_to_(1,-1,1,1)"] = rel[2]
    p7["any_with_all_in_pm1"] = any(r["g"] in ("e^(2pi i 0/8)", "e^(2pi i 4/8)") and r["zeta"] in ("i^0", "i^2") for k in rel for r in rel[k])
    res["P7"] = p7
    print(json.dumps(p7, indent=1))
    with open(OUT, "x") as f:
        json.dump(res, f, default=str, indent=1)
    print("fails:", len(res["fail"]))

main()
