#!/usr/bin/env python3
"""Items 4 and 6(b): walks on rings Z_N, enumerated explicitly. Reviewer's own program.

Usage: python3 item46_walks.py <seed> <outfile> <n_random>

Walk = sequence of steps (0=right, 1=left) from (0,R); site after t steps = (t - 2*lambda_t) mod N; rail after a
step = R iff the step is right; M = N/gcd(N,2). Position product event of length T: all walks whose site after
s steps lies in A_s, s=1..T. Vertex = (site, rail). n_y(l) = number of walks of S ending at y with lambda = l.

PREDICATES (fixed before the first run). W-predicates on position product events (item 4):
 W1 lem:fgkappa: all lambda at one vertex are congruent mod M.
 W2 lem:winding(i): n(l)n(l') <= n(l+M)n(l'-M) for l'-l >= 2M, l'-l in MZ.
 W3 lem:winding(ii): n(l)n(l+2M) <= n(l+M)(n(l+M)-1).
 W4 'hence': lambda values at a vertex form a progression of difference M without gaps; inner values have n>=2.
 W5 lem:windingrails first: n_L(l)n_R(l') <= n_L(l+M)n_R(l'-M) for l'-l >= M.
 W6 lem:windingrails second: n_R(l)n_L(l') <= n_R(l+M)n_L(l'-M) for l'-l >= 2M.
 W7 cor:nowind sentence 3: no site whose walks are exactly one walk on L with lambda=l and one on R with lambda=l+M.
 W8 cor:nowind sentence 1 (level form): no vertex with exactly three walks having three different lambda.
 Recorded, not predicates (sharpness): X1 = number of events where the second rail inequality FAILS at l'-l = M
 (not claimed by the lemma); X2 = number of sites whose walks are exactly one on R at lambda=l and one on L at l+M
 (the mirror pattern, not excluded by the corollary); X3 = W8 for ARBITRARY events (random subsets of walks), where
 the corollary's first sentence, read without 'position product', is expected to fail.
B-predicates (item 6(b)), exact: psi takes values i^p, p in Z_4, on the four gains (pa,pb,pc,pd); the hypothesis
 HYP: psi(delta) = -1, i.e. pa+pd-pb-pc == 2 mod 4, is tested per instance and the number qualifying reported.
 Amplitude at a vertex: Psi_y(u) = sum_w u^{lambda(w)} psi(gain(w)), a polynomial in u with Gaussian integer
 coefficients; mu(S) = sum_y Psi_y(u) * conj(Psi_y)(u^{-1}), a Laurent polynomial with Gaussian integer coefficients.
 B1 for instances with HYP: mu(Ext S) == 2 mu(S) as Laurent polynomials (so for every complex u with |u|=1,
    of any order; no floating point, no tolerance), S a position product event.
 B2 the same for S an arbitrary set of walks of one length (random subset).
 B3 the same for S a set of walks of mixed lengths (walks counted at their end vertex whatever the length).
 B4 negative control, expected to FAIL: instances WITHOUT HYP satisfy the identity (count how many do).
 B5 negative control, expected to FAIL: u = 2 (not a unit; conj(u)=u) with HYP, exact integers.
Rings N=1..9, lengths T=1..11; exhaustive masks for N<=3,T<=3; the rest random with the given seed.
"""
import sys, random, itertools, json
from math import gcd
from collections import defaultdict

def walks_of(N, masks):
    # returns list of step tuples
    res = []
    T = len(masks)
    def rec(t, site, steps):
        if t == T: res.append(tuple(steps)); return
        for st in (0, 1):
            ns = (site + (1 if st == 0 else -1)) % N
            if ns in masks[t]:
                steps.append(st); rec(t + 1, ns, steps); steps.pop()
    rec(0, 0, [])
    return res

def endinfo(N, w):
    lam = sum(w); T = len(w)
    site = (T - 2 * lam) % N
    rail = 'R' if (T == 0 or w[-1] == 0) else 'L'
    return site, rail, lam

def psi_exp(w, p):
    pa, pb, pc, pd = p
    rail = 0; e = 0
    for st in w:
        if rail == 0: e += pa if st == 0 else pb
        else: e += pc if st == 0 else pd
        rail = st
    return e % 4

I4 = [(1, 0), (0, 1), (-1, 0), (0, -1)]
def mu_laurent(N, S, p):
    amp = defaultdict(lambda: defaultdict(lambda: [0, 0]))
    for w in S:
        site, rail, lam = endinfo(N, w)
        re, im = I4[psi_exp(w, p)]
        c = amp[(site, rail)][lam]; c[0] += re; c[1] += im
    tot = defaultdict(lambda: [0, 0])
    for y, pol in amp.items():
        items = list(pol.items())
        for l1, (a1, b1) in items:
            for l2, (a2, b2) in items:
                # (a1+ib1) * conj(a2+ib2) u^{l1-l2}
                c = tot[l1 - l2]; c[0] += a1 * a2 + b1 * b2; c[1] += b1 * a2 - a1 * b2
    return {e: tuple(v) for e, v in tot.items() if v != [0, 0]}

def mu_u2(N, S, p):
    amp = defaultdict(lambda: [0, 0])
    for w in S:
        site, rail, lam = endinfo(N, w)
        re, im = I4[psi_exp(w, p)]
        c = amp[(site, rail)]; c[0] += re * 2 ** lam; c[1] += im * 2 ** lam
    return sum(a * a + b * b for a, b in amp.values())

def ext(S): return [w + (st,) for w in S for st in (0, 1)]

def main():
    seed = int(sys.argv[1]); outfile = sys.argv[2]; nrand = int(sys.argv[3])
    out = open(outfile, 'x')
    out.write(json.dumps({"cmd": " ".join(sys.argv)}) + "\n")
    rng = random.Random(seed)
    cnt = defaultdict(int); fails = defaultdict(list)
    def bad(name, info):
        cnt[name + "_fail"] += 1
        if len(fails[name]) < 5: fails[name].append(info)
    def check_event(N, masks, S):
        M = N // gcd(N, 2)
        cnt["pp_events"] += 1
        if not S: cnt["pp_empty"] += 1; return
        cnt["pp_nonempty"] += 1
        n = defaultdict(lambda: defaultdict(int))
        for w in S:
            site, rail, lam = endinfo(N, w); n[(site, rail)][lam] += 1
        tag = (N, [sorted(m) for m in masks])
        for y, tab in n.items():
            ls = sorted(tab)
            if len({l % M for l in ls}) > 1: bad("W1", tag)
            for l in ls:
                for l2 in ls:
                    if l2 - l >= 2 * M and (l2 - l) % M == 0:
                        if tab[l] * tab[l2] > tab.get(l + M, 0) * tab.get(l2 - M, 0): bad("W2", tag)
                if l + 2 * M in tab:
                    if tab[l] * tab[l + 2 * M] > tab.get(l + M, 0) * (tab.get(l + M, 0) - 1): bad("W3", tag)
            if ls != list(range(ls[0], ls[-1] + 1, M)): bad("W4", tag)
            if any(tab[l] < 2 for l in ls[1:-1]): bad("W4", tag)
            if len(ls) >= 3: cnt["vertices_with_3plus_levels"] += 1
            if len(ls) == 3 and sum(tab.values()) == 3: bad("W8", tag)
        for site in range(N):
            nR = n.get((site, 'R'), {}); nL = n.get((site, 'L'), {})
            x1 = False
            for l in nL:
                for l2 in nR:
                    if l2 - l >= M and nL[l] * nR[l2] > nL.get(l + M, 0) * nR.get(l2 - M, 0): bad("W5", tag)
            for l in nR:
                for l2 in nL:
                    if l2 - l >= 2 * M and nR[l] * nL[l2] > nR.get(l + M, 0) * nL.get(l2 - M, 0): bad("W6", tag)
                    if l2 - l == M and nR[l] * nL[l2] > nR.get(l + M, 0) * nL.get(l2 - M, 0): x1 = True
            if x1: cnt["X1_second_rail_ineq_fails_at_M"] += 1
            if sum(nR.values()) == 1 and sum(nL.values()) == 1:
                lR = next(iter(nR)); lL = next(iter(nL))
                cnt["sites_one_R_one_L"] += 1
                if lR == lL + M: bad("W7", tag)
                if lL == lR + M: cnt["X2_mirror_pattern_R_l_L_l+M"] += 1
    def check_B(N, S, kind):
        p = tuple(rng.randrange(4) for _ in range(4))
        hyp = (p[0] + p[3] - p[1] - p[2]) % 4 == 2
        if not S: return
        l = mu_laurent(N, S, p); r_ = mu_laurent(N, ext(S), p)
        same = (r_ == {e: (2 * a, 2 * b) for e, (a, b) in l.items()})
        if hyp:
            cnt[kind + "_HYP_qualifying"] += 1
            if not same: bad(kind, (N, p, len(S)))
            cnt["B5_tested"] += 1
            if mu_u2(N, ext(S), p) == 2 * mu_u2(N, S, p): cnt["B5_holds_for_u=2"] += 1
            else: cnt["B5_fails_for_u=2(expected)"] += 1
            if len(l) > 1: cnt[kind + "_HYP_with_u_dependence"] += 1
        else:
            cnt["B4_noHYP_tested"] += 1
            if same: cnt["B4_noHYP_identity_holds"] += 1
            else: cnt["B4_noHYP_identity_fails(expected)"] += 1
    # exhaustive small
    for N in (1, 2, 3):
        subsets = [set(c) for k in range(N + 1) for c in itertools.combinations(range(N), k)]
        for T in (1, 2, 3):
            for masks in itertools.product(subsets, repeat=T):
                S = walks_of(N, masks); check_event(N, masks, S);
                if S: check_B(N, S, "B1")
    cnt["exhaustive_done"] = 1
    for it in range(nrand):
        N = rng.randint(1, 9); T = rng.randint(1, 11)
        dens = rng.choice([0.5, 0.7, 0.85, 1.0])
        masks = [set(x for x in range(N) if rng.random() < dens) for _ in range(T)]
        if rng.random() < 0.5 and T >= 2:   # force walks to end at one site, to load a vertex
            masks[-1] = {rng.randrange(N)}
        S = walks_of(N, masks)
        check_event(N, masks, S)
        if S:
            check_B(N, S, "B1")
            allw = list(itertools.product((0, 1), repeat=T))
            sub = [w for w in allw if rng.random() < rng.choice([0.05, 0.3, 0.6])]
            if sub:
                check_B(N, sub, "B2")
                nn = defaultdict(lambda: defaultdict(int))
                for w in sub:
                    site, rail, lam = endinfo(N, w); nn[(site, rail)][lam] += 1
                cnt["X3_arbitrary_events"] += 1
                if any(len(t) == 3 and sum(t.values()) == 3 for t in nn.values()):
                    cnt["X3_arbitrary_events_with_3walks_3levels_vertex"] += 1
            T2 = rng.randint(1, 9)
            mixed = sub + [w for w in itertools.product((0, 1), repeat=T2) if rng.random() < 0.3]
            mixed = list(set(mixed))
            if mixed: check_B(N, mixed, "B3")
    res = {"counts": dict(cnt), "first_failures": {k: v for k, v in fails.items()}}
    out.write(json.dumps(res, default=str) + "\n"); out.close()
    print(json.dumps(res, default=str, indent=1))

if __name__ == "__main__":
    main()
