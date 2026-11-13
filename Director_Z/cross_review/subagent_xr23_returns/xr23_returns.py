#!/usr/bin/env python3
"""xr23_returns.py -- own program for the staircase walk of the note
'What a return to the launch port says about probability'. No author code imported.

Walk (from the note's text): ring Z_N, N=4M; rail d in {R=+1, L=-1} (incoming rail);
sheet j mod M; launch (0,R,0), counted as positive. One tick from (x,d,j): choose d';
sign *= -1 iff d==L and d'==L; j += floor(x/2) mod M with x taken in 0..N-1; x += d'.
n = number of histories, D = (#positive) - (#negative), at a resolved port (x,d,j).
Count return q_t = n_{(0,R)}/2^t ; coherent return R_t = sum_j D_{(0,R),j}^2 / 2^t ;
P_t(c) = c q_t + (1-c) R_t.

PREDICATES (fixed before the first run). Orders M in {3,4,5}; M=6,7 additionally for F3.
Hypotheses, tested per instance (H*), then claims.
 H1 base digraph: every vertex (x,d) has exactly 2 out-arcs to 2 distinct vertices (no parallel arcs).
 H2 lifted graph on (x,d,j,sign): every lifted port has exactly 2 predecessors.
 H3 lifted graph strongly connected (forward and backward BFS from launch reach all 16 M^2 ports); period measured.
 H4 characters psi=(a,eps) of Z_M x Z_2: A_psi^* A_psi = 2I iff eps=-1 (float; tolerance 1e-12, basis: entries are
    unit-modulus numbers summed in pairs, rounding < 1e-15).
 H5 unitarity: sum over resolved ports of D^2 equals 2^t at every t<=T (exact).
 F1 five ticks: histories reaching (1,R,-1 mod M) are exactly LRRLR and RLLRR with opposite signs.
 F2 five ticks, port (1,R) sheet-blind: count numerator 6.
 F3 same port: square numerator 0 (M=3), 6 (M=4), 4 (M>=5; tested 5,6,7).
 F4 M=4, tick six, port (2,L): count 5 and square 3 (my reading of 'numerators five and three over 64').
 F5 deleting LRRLR from the full 32-history event: sum of D^2 = 33, count = 31; only the port of F1 changes.
 Q1 q_t = (1/2N) sum_j cos(2 pi j/N)^t for even 2<=t<=40, zero for odd t (float; max deviation reported;
    tolerance 1e-12, basis: N<=20 terms each with relative rounding ~ t*1e-16).
 Q2 q_2 = 1/4 exactly; q_t strictly decreasing over even t in 2..T; q_t > 1/N.
 Q3 q_t <= 1/4 for all 1<=t<=T (exact).
 R1 P_t(c) <= 1-3c/4 for 1<=t<=T, c in {0,1/4,1} (exact rationals).
 R2 P_t(c) <= 1 for all t and R_t <= 1 (exact).
 R3 exists even t in [2,T] with R_t > 0.99 (exact). If not: measured only; max R_t and its t are reported, and a float
    scan of even t up to TF is reported as measured only.
 A1 abundance: for k in {1,2,3}, p in {0,1}, at tick 12k+10M+10+p every resolved port (x,d,j) with x = p mod 2 has
    n_+ >= 2^k and n_- >= 2^k.  (Also measured: first tick from which every same-parity port has n_+,n_- >= 1.)
 C1 continuation (seed 20261113): 20 random subsets S of the 2^7 histories of depth 7; resolved weight
    W_c(S)=sum_ports [c n + (1-c) D^2]; W_c(Ext S) = 2 W_c(S) for c in {0,1/4,1} (exact).
 C2 coarsening: same subsets; base law c n + (1-c)/M sum_{a} |sum_j w^{a j} D_j|^2 at each base port equals
    sum_j [c n_j + (1-c) D_j^2] (float, tol 1e-9, basis: <=128 unit terms).
Failed predicates are kept in the result file with status 'failed'. Result file is never overwritten.
"""
import sys, os, json, math, cmath, random, itertools
from fractions import Fraction as Fr
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'xr23_returns_result.json')
if os.path.exists(OUT):
    sys.exit('refusing to overwrite ' + OUT)
T = 3000; TF = 400000
R_, L_ = 1, -1
res = {'predicates': [], 'measured': {}}
def pred(name, M, ok, detail=None, kind=None):
    res['predicates'].append({'name': name, 'M': M, 'status': kind or ('met' if ok else 'failed'), 'detail': detail})
def g(x, M): return (x // 2) % M
def succ(st, M):
    x, d, j, s = st; N = 4 * M; out = []
    for d2 in (R_, L_):
        out.append(((x + d2) % N, d2, (j + g(x, M)) % M, -s if (d == L_ and d2 == L_) else s))
    return out
def run_word(w, M):
    st = (0, R_, 0, 1)
    for ch in w: st = succ(st, M)[0 if ch == 'R' else 1]
    return st
def dp_step(P, M):
    Q = {}
    for (x, d, j), (a, b) in P.items():
        for (x2, d2, j2, s2) in succ((x, d, j, 1), M):
            pa, pb = Q.get((x2, d2, j2), (0, 0))
            Q[(x2, d2, j2)] = (pa + a, pb + b) if s2 == 1 else (pa + b, pb + a)
    return Q
def table(words, M):
    P = {}
    for w in words:
        x, d, j, s = run_word(w, M)
        a, b = P.get((x, d, j), (0, 0)); P[(x, d, j)] = (a + (s == 1), b + (s == -1))
    return P
def weight(P, c): return sum(c * (a + b) + (1 - c) * (a - b) ** 2 for a, b in P.values())
CS = [Fr(0), Fr(1, 4), Fr(1)]
for M in (3, 4, 5, 6, 7):
    N = 4 * M
    words5 = [''.join(w) for w in itertools.product('RL', repeat=5)]
    P5 = table(words5, M)
    if M >= 5 or M in (3, 4):
        cnt = sum(a + b for (x, d, j), (a, b) in P5.items() if (x, d) == (1, R_))
        sq = sum((a - b) ** 2 for (x, d, j), (a, b) in P5.items() if (x, d) == (1, R_))
        pred('F3', M, sq == {3: 0, 4: 6}.get(M, 4), {'square': sq})
        pred('F2', M, cnt == 6, {'count': cnt})
    hits = sorted((w, run_word(w, M)[3]) for w in words5 if run_word(w, M)[:3] == (1, R_, (M - 1) % M))
    pred('F1', M, hits == [('LRRLR', 1), ('RLLRR', -1)], hits)
    Pd = table([w for w in words5 if w != 'LRRLR'], M)
    changed = [k for k in set(P5) | set(Pd) if P5.get(k, (0, 0)) != Pd.get(k, (0, 0))]
    pred('F5', M, weight(Pd, 0) == 33 and weight(Pd, 1) == 31 and weight(P5, 0) == 32 and changed == [(1, R_, (M - 1) % M)],
         {'sq': weight(Pd, 0), 'count': weight(Pd, 1), 'changed': changed})
    if M > 5: continue
    if M == 4:
        P6 = table([''.join(w) for w in itertools.product('RL', repeat=6)], M)
        c6 = sum(a + b for (x, d, j), (a, b) in P6.items() if (x, d) == (2, L_))
        s6 = sum((a - b) ** 2 for (x, d, j), (a, b) in P6.items() if (x, d) == (2, L_))
        pred('F4', M, (c6, s6) == (5, 3), {'count': c6, 'square': s6})
        for MM in (3, 5, 6):
            Pm = table([''.join(w) for w in itertools.product('RL', repeat=6)], MM)
            res['measured']['tick6_(2,L)_M%d' % MM] = [sum(a + b for (x, d, j), (a, b) in Pm.items() if (x, d) == (2, L_)),
                                                        sum((a - b) ** 2 for (x, d, j), (a, b) in Pm.items() if (x, d) == (2, L_))]
    # hypotheses
    base = [(x, d) for x in range(N) for d in (R_, L_)]
    pred('H1', M, all(len({(s[0], s[1]) for s in succ((x, d, 0, 1), M)}) == 2 for x, d in base))
    lifted = [(x, d, j, s) for x in range(N) for d in (R_, L_) for j in range(M) for s in (1, -1)]
    preds = {v: [] for v in lifted}
    for v in lifted:
        for u in succ(v, M): preds[u].append(v)
    pred('H2', M, all(len(set(p)) == 2 and len(p) == 2 for p in preds.values()))
    def bfs(nb):
        dist = {(0, R_, 0, 1): 0}; q = [(0, R_, 0, 1)]
        for v in q:
            for u in nb(v):
                if u not in dist: dist[u] = dist[v] + 1; q.append(u)
        return dist
    df = bfs(lambda v: succ(v, M)); db = bfs(lambda v: preds[v])
    per = 0
    for v in lifted:
        if v in df:
            for u in succ(v, M):
                if u in df: per = math.gcd(per, df[v] + 1 - df[u])
    pred('H3', M, len(df) == len(lifted) and len(db) == len(lifted), {'ports': len(lifted), 'period': per})
    okH4 = True; det = {}
    for a in range(M):
        for eps in (1, -1):
            psi = lambda j, s: cmath.exp(2j * math.pi * a * j / M) * (eps if s == -1 else 1)
            worst = 0.0
            for (x, d) in base:
                for (x2, d2) in base:
                    ov = 0
                    s1 = {(u[0], u[1]): psi(u[2], u[3]) for u in succ((x, d, 0, 1), M)}
                    s2 = {(u[0], u[1]): psi(u[2], u[3]) for u in succ((x2, d2, 0, 1), M)}
                    for k in s1:
                        if k in s2: ov += s1[k].conjugate() * s2[k]
                    worst = max(worst, abs(ov - (2 if (x, d) == (x2, d2) else 0)))
            isU = worst < 1e-12; det['a=%d,eps=%d' % (a, eps)] = worst
            okH4 &= (isU == (eps == -1))
    pred('H4', M, okH4, det)
    # long exact run
    P = {(0, R_, 0): (1, 0)}
    q = [Fr(1)]; Rt = [Fr(1)]; okH5 = True; ab = {}
    need = {12 * k + 10 * M + 10 + p: (k, p) for k in (1, 2, 3) for p in (0, 1)}
    first_all = None; run_ok = None
    for t in range(1, T + 1):
        P = dp_step(P, M)
        if sum((a - b) ** 2 for a, b in P.values()) != 2 ** t: okH5 = False
        q.append(Fr(sum(a + b for (x, d, j), (a, b) in P.items() if (x, d) == (0, R_)), 2 ** t))
        Rt.append(Fr(sum((a - b) ** 2 for (x, d, j), (a, b) in P.items() if (x, d) == (0, R_)), 2 ** t))
        if t <= 200:
            full = all(min(P.get((x, d, j), (0, 0))) >= 1 for x in range(t % 2, N, 2) for d in (R_, L_) for j in range(M))
            if full and run_ok is None: run_ok = t
            if not full: run_ok = None
        if t in need:
            k, p = need[t]
            mn = min(min(P.get((x, d, j), (0, 0))) for x in range(p, N, 2) for d in (R_, L_) for j in range(M))
            pred('A1', M, mn >= 2 ** k, {'k': k, 'p': p, 'tick': t, 'min_signed_multiplicity_bits': mn.bit_length()})
    res['measured']['first_tick_from_which_all_same_parity_ports_have_both_signs_M%d' % M] = run_ok
    pred('H5', M, okH5)
    dev = max(abs(float(q[t]) - (sum(math.cos(2 * math.pi * j / N) ** t for j in range(N)) / (2 * N) if t % 2 == 0 else 0.0))
              for t in range(1, 41))
    pred('Q1', M, dev < 1e-12, {'max_dev': dev})
    pred('Q2', M, q[2] == Fr(1, 4) and all(q[t + 2] < q[t] for t in range(2, T - 1, 2)) and all(q[t] > Fr(1, N) for t in range(2, T + 1, 2)),
         {'q2': str(q[2]), 'q_T_minus_1overN': float(q[T] - Fr(1, N))})
    pred('Q3', M, all(q[t] <= Fr(1, 4) for t in range(1, T + 1)))
    for c in CS:
        bad = [t for t in range(1, T + 1) if c * q[t] + (1 - c) * Rt[t] > 1 - Fr(3, 4) * c]
        pred('R1', M, not bad, {'c': str(c), 'violations': bad[:5],
                                'max_P_t>=1': float(max(c * q[t] + (1 - c) * Rt[t] for t in range(1, T + 1)))})
    pred('R2', M, all(r <= 1 for r in Rt))
    best = max(range(1, T + 1), key=lambda t: Rt[t]); hit = [t for t in range(2, T + 1, 2) if Rt[t] > Fr(99, 100)]
    pred('R3', M, bool(hit), {'first_t_above_0.99': hit[:3], 'max_R_t': float(Rt[best]), 'argmax_t': best,
                              'top5': sorted(((float(Rt[t]), t) for t in range(1, T + 1)), reverse=True)[:5]},
         kind=None if hit else 'measured only')
    res['measured']['R_t_small_M%d' % M] = {t: str(Rt[t]) for t in (2, 4, 6, 8, 10, 12)}
    res['measured']['q_t_small_M%d' % M] = {t: str(q[t]) for t in (2, 4, 6, 8, 10, 12)}
    # float scan
    try:
        import numpy as np
        idx = {(x, d, j): i for i, (x, d, j) in enumerate((x, d, j) for x in range(N) for d in (R_, L_) for j in range(M))}
        U = np.zeros((len(idx), len(idx)))
        for k, i in idx.items():
            for (x2, d2, j2, s2) in succ(k + (1,), M): U[idx[(x2, d2, j2)], i] = s2 / math.sqrt(2)
        U2 = U @ U; v = np.zeros(len(idx)); v[idx[(0, R_, 0)]] = 1
        tgt = [idx[(0, R_, j)] for j in range(M)]; bestf = (0.0, 0); firstf = None
        for n in range(1, TF // 2 + 1):
            v = U2 @ v; r = float((v[tgt] ** 2).sum())
            if r > bestf[0]: bestf = (r, 2 * n)
            if r > 0.99 and firstf is None: firstf = (r, 2 * n)
        res['measured']['float_scan_M%d' % M] = {'TF': TF, 'max_R': bestf, 'first_above_0.99': firstf, 'norm_drift': float(abs(v @ v - 1))}
    except Exception as e:
        res['measured']['float_scan_M%d' % M] = 'not run: %r' % (e,)
    # C1, C2
    rng = random.Random(20261113 + M)
    words7 = [''.join(w) for w in itertools.product('RL', repeat=7)]
    ok1 = ok2 = True; worst = 0.0
    for _ in range(20):
        S = [w for w in words7 if rng.random() < 0.5]
        PS = table(S, M); PE = table([w + e for w in S for e in 'RL'], M)
        for c in CS:
            if weight(PE, c) != 2 * weight(PS, c): ok1 = False
            for (x, d) in base:
                Dj = [PS.get((x, d, j), (0, 0)) for j in range(M)]
                lhs = float(c) * sum(a + b for a, b in Dj) + float(1 - c) / M * sum(
                    abs(sum(cmath.exp(2j * math.pi * a * j / M) * (Dj[j][0] - Dj[j][1]) for j in range(M))) ** 2 for a in range(M))
                rhs = float(sum(c * (a + b) + (1 - c) * (a - b) ** 2 for a, b in Dj))
                worst = max(worst, abs(lhs - rhs))
    pred('C1', M, ok1); pred('C2', M, worst < 1e-9, {'max_dev': worst})
tot = {}
for p in res['predicates']: tot[p['status']] = tot.get(p['status'], 0) + 1
res['totals'] = tot
res['failed'] = [p for p in res['predicates'] if p['status'] == 'failed']
with open(OUT, 'x') as f: json.dump(res, f, indent=1, default=str)
print(json.dumps(tot)); print(json.dumps(res['failed'], default=str)[:3000]); print(json.dumps(res['measured'], default=str)[:6000])
for p in res['predicates']:
    if p['name'] in ('R3', 'R1', 'A1', 'F4', 'H3', 'Q1') : print(p['name'], p['M'], p['status'], json.dumps(p['detail'], default=str)[:400])
