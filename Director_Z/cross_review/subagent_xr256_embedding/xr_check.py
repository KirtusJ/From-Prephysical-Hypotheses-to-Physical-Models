"""Independent cross-review program for selecting_the_real_embedding.md.

Built from the circuit text of addressed_embedding.md only (no import of the
author's modules). State: dict address(0..3) -> (amp_R, amp_L) over Q(sqrt2),
elements (a,b) = a + b*r with Fractions. A free shift increments the address
mod 4 on L and holds it on R. Ticks 1,3 of each flight: H = c*[[1,1],[1,-1]]
on (R,L); tick 2: X on even address, eps*H on odd address. c is the value of
1/sqrt2 in the chosen embedding: (0, s/2), s=+1 specified, s=-1 conjugate.
The address is recorded (projectively) after ticks 3,6,9. Start on R, addr 0.
Comparisons in Q(sqrt2) use the real value with r = +sqrt2 (the physical
number); "conj" maps b -> -b.

Predicates, fixed before the first run (all results kept, failures kept):
 P1 support: for s=+1 and s=-1 (eps=+1) exactly 27 words positive, 37 zero,
    same positive set, total mass 1.
 P2 conjugation: W(s=-1,eps=+1)[w] == conj(W(s=+1,eps=+1)[w]) for all 64 w.
 P3 equivalence: W(s=-1,eps=+1) == W(s=+1,eps=-1) for all 64 w, AND the
    unnormalized branch state after every tick on every history agrees up to a
    single global sign per tick (so every conditional law agrees); also
    W(s=-1,eps=-1) == W(s=+1,eps=+1).
 P4 witness: 512*(l,m,h) at prefix (2,3) = (86-60r, 18-8r, 40+4r) for words
    (2,3,1),(2,3,3),(2,3,0); 0<l<m<h; conj(l) unique max over 27 positive
    words; (2),(2,3),(2,3,1) unique conj max among positive siblings; root and
    prefix-(2) conjugate child masses equal the note's lists; m^2<lh; m>2l;
    (1/(2l)-1/m)/27 > 1/100 exactly; P=l+m+h=8m; P>43l.
 P5 conjugate carriers (hypothesis per carrier: fixed conjugate embedding,
    every exponent q in [0,inf], normalization over positive support; carriers
    failing the hypothesis are counted and excluded): P_l >= 1/27*(1-1e-12),
    P_m <= P_l*(1+1e-12), J >= (A-M)/27*(1-1e-12), J > 0.01.
    Tolerance basis: double rounding over <=27-term sums; the measured
    minimum margins are reported instead of relying on the tolerance.
 P6 specified carriers (same hypothesis, s=+1): J >= -1e-12*scale.
 P7 out-of-scope probes, reported, not counted against the note:
    (a) block mode = one joint power on the first two writes, then local power
        on the third: is (2,3) the unique conj max among 9 depth-2 prefixes?
        minimum P_l found;
    (b) negative exponents: min J over conjugate complete-word q<0;
    (c) the analyzer coefficients P*A, P*M, P*B to 5 decimals.
 P8 unreported parameter: J at q=0, 1, inf and the minimum of J over a grid
    of conjugate complete-word and sequential modes.
Result file results_xr.txt opened with mode 'x' (never overwritten). Seed 256.
v2 (after run1 crashed in P7b with OverflowError at q=-100): powlaw scales
by the minimum weight when q<0. Predicates unchanged.
"""
from fractions import Fraction as F
from itertools import product
import math, random, sys

def add(x, y): return (x[0]+y[0], x[1]+y[1])
def neg(x): return (-x[0], -x[1])
def mul(x, y): return (x[0]*y[0]+2*x[1]*y[1], x[0]*y[1]+x[1]*y[0])
def conj(x): return (x[0], -x[1])
Z = (F(0), F(0)); ONE = (F(1), F(0))
def sgn(x):
    a, b = x
    if a >= 0 and b >= 0: return 0 if (a == 0 and b == 0) else 1
    if a <= 0 and b <= 0: return -1
    d = a*a - 2*b*b
    return (1 if a > 0 else -1) * (1 if d > 0 else (-1 if d < 0 else 0))
def gt(x, y): return sgn(add(x, neg(y))) > 0
def val(x): return float(x[0]) + float(x[1])*math.sqrt(2)
def q2(a, b): return (F(a), F(b))

def evolve(s, eps, trace=None):
    c = (F(0), F(s, 2))
    H = lambda r, l: (mul(c, add(r, l)), mul(c, add(r, neg(l))))
    states = {(): {0: (ONE, Z)}}
    for t in range(1, 10):
        new = {}
        for hist, st in states.items():
            nxt = {}
            for a, (r, l) in st.items():
                if t % 3 == 2 and a % 2 == 0: r2, l2 = l, r
                else:
                    r2, l2 = H(r, l)
                    if t % 3 == 2: r2, l2 = mul((F(eps), F(0)), r2), mul((F(eps), F(0)), l2)
                R = nxt.setdefault(a, [Z, Z]); R[0] = add(R[0], r2)
                L = nxt.setdefault((a+1) % 4, [Z, Z]); L[1] = add(L[1], l2)
            if t % 3 == 0:
                for a, v in nxt.items():
                    new[hist+(a,)] = {a: tuple(v)}
            else:
                new[hist] = {a: tuple(v) for a, v in nxt.items()}
        states = new
        if trace is not None: trace.append({h: dict(v) for h, v in states.items()})
    W = {w: Z for w in product(range(4), repeat=3)}
    for h, st in states.items():
        m = Z
        for r, l in st.values(): m = add(m, add(mul(r, r), mul(l, l)))
        W[h] = add(W[h], m)
    return W

def main():
    out = open("results_xr.txt", "x")
    def log(*a):
        line = " ".join(str(x) for x in a); print(line); out.write(line+"\n")
    res = {}
    trS, trC, trE = [], [], []
    WS = evolve(+1, +1, trS); WC = evolve(-1, +1, trC); WE = evolve(+1, -1, trE)
    WCE = evolve(-1, -1)
    words = list(WS)
    posS = {w for w in words if sgn(WS[w]) > 0}; posC = {w for w in words if sgn(WC[w]) > 0}
    zeroS = [w for w in words if WS[w] == Z]
    tot = Z
    for w in words: tot = add(tot, WS[w])
    res["P1"] = len(posS) == 27 and posS == posC and len(zeroS) == 37 and tot == ONE \
        and all(sgn(WS[w]) >= 0 and sgn(WC[w]) >= 0 for w in words)
    res["P2"] = all(WC[w] == conj(WS[w]) for w in words)
    ok = all(WC[w] == WE[w] for w in words) and all(WCE[w] == WS[w] for w in words)
    for t, (a, b) in enumerate(zip(trC, trE), 1):
        signs = set()
        for h in a:
            for addr in a[h]:
                for k in (0, 1):
                    x, y = a[h][addr][k], b[h][addr][k]
                    if x == y and x == Z: continue
                    if x == y: signs.add(1)
                    elif x == neg(y): signs.add(-1)
                    else: signs.add(None)
        if len(signs) != 1 or None in signs: ok = False
        log(f"tick {t}: conj(eps=+1) vs spec(eps=-1) amplitude sign set {sorted(signs, key=str)}")
    res["P3"] = ok
    # prefix masses
    def pm(W, p):
        m = Z
        for w in words:
            if w[:len(p)] == p: m = add(m, W[w])
        return m
    S = lambda x: mul(x, (F(512), F(0)))
    l, m, h = WS[(2, 3, 1)], WS[(2, 3, 3)], WS[(2, 3, 0)]
    p4 = (S(l), S(m), S(h)) == (q2(86, -60), q2(18, -8), q2(40, 4))
    p4 &= gt(l, Z) and gt(m, l) and gt(h, m)
    p4 &= all(gt(WC[(2, 3, 1)], WC[w]) for w in posC if w != (2, 3, 1))
    for p in [(2,), (2, 3), (2, 3, 1)]:
        sib = [p[:-1]+(j,) for j in range(4) if p[:-1]+(j,) != p and sgn(pm(WS, p[:-1]+(j,))) > 0]
        p4 &= len(sib) == 2 and all(gt(pm(WC, p), pm(WC, x)) for x in sib)
    p4 &= [S(pm(WC, (j,))) for j in (1, 2, 3)] == [q2(192, -128), q2(256, 128), q2(64, 0)]
    p4 &= [S(pm(WC, (2, j))) for j in (0, 1, 3)] == [q2(64, 32), q2(48, 32), q2(144, 64)]
    p4 &= pm(WS, (2, 2)) == Z
    lu, mu, hu = S(l), S(m), S(h)
    p4 &= gt(mul(lu, hu), mul(mu, mu)) and gt(mu, add(lu, lu))
    def inv(x):
        d = x[0]*x[0]-2*x[1]*x[1]; return (x[0]/d, -x[1]/d)
    gap = add(inv(add(lu, lu)), neg(inv(mu)))
    bound = mul(gap, (F(1, 27), F(0)))
    p4 &= gt(bound, q2(F(1, 100), 0))
    P = add(add(lu, mu), hu)
    p4 &= P == mul(q2(8, 0), mu) and gt(P, mul(q2(43, 0), lu))
    res["P4"] = p4
    log("bound (1/(2l)-1/m)/27 =", val(bound))
    # float model
    lf, mf, hf = val(lu), val(mu), val(hu)
    th = math.log(mf/lf)/math.log(hf/lf); A, M, B = (1-th)/lf, 1/mf, th/hf
    log(f"theta={th:.6f} A={A:.6f} M={M:.6f} B={B:.6f} (A-M)/27={(A-M)/27:.6f}")
    log(f"analyzer coeffs P*A={val(P)*A:.5f} P*M={val(P)*M:.5f} P*B={val(P)*B:.5f}")
    score = {(2, 3, 1): A, (2, 3, 3): -M, (2, 3, 0): B}
    wS = {w: val(WS[w])*512 for w in posS}; wC = {w: val(WC[w])*512 for w in posC}
    def powlaw(ws, q):
        if q == math.inf:
            mx = max(ws.values()); top = [k for k in ws if ws[k] == mx]
            return {k: (1/len(top) if k in top else 0.0) for k in ws}
        mx = max(ws.values()) if q >= 0 else min(ws.values())
        u = {k: (v/mx)**q for k, v in ws.items()}; z = sum(u.values())
        return {k: v/z for k, v in u.items()}
    def complete(ws, q): return powlaw(ws, q)
    def sequential(ws, qf):
        probs = {}
        def rec(p, pr):
            if len(p) == 3: probs[p] = probs.get(p, 0)+pr; return
            ch = {}
            for w, v in ws.items():
                if w[:len(p)] == p: ch[w[len(p)]] = ch.get(w[len(p)], 0)+v
            law = powlaw(ch, qf(p))
            for j, x in law.items():
                if x > 0: rec(p+(j,), pr*x)
        rec((), 1.0); return probs
    def block(ws, q1, q2_):
        ch2 = {}
        for w, v in ws.items(): ch2[w[:2]] = ch2.get(w[:2], 0)+v
        law = powlaw(ch2, q1); probs = {}
        for p, x in law.items():
            ch = {w[2]: v for w, v in ws.items() if w[:2] == p}
            for j, y in powlaw(ch, q2_).items(): probs[p+(j,)] = x*y
        return probs
    J = lambda pr: sum(score[k]*pr.get(k, 0) for k in score)
    rng = random.Random(256)
    def rq():
        r = rng.random()
        return 0.0 if r < .1 else (math.inf if r < .2 else rng.choice([rng.uniform(0, 3), rng.uniform(0, 60)]))
    nC = qualC = 0; failC = []; minPl = minJ = 1e9; maxratio = 0
    nS = qualS = 0; failS = []; minJS = 1e9
    for i in range(4000):
        kind = rng.choice(["complete", "sequential", "mixture"])
        def make(ws):
            if kind == "complete": qs = [rq()]; return qs, complete(ws, qs[0])
            if kind == "sequential":
                tab = {}
                def qf(p):
                    if p not in tab: tab[p] = rq()
                    return tab[p]
                pr = sequential(ws, qf); return list(tab.values()), pr
            comps = []; qs = []
            for _ in range(rng.randint(2, 4)):
                if rng.random() < .5: q = rq(); qs.append(q); comps.append(complete(ws, q))
                else:
                    tab = {}
                    def qf(p, tab=tab):
                        if p not in tab: tab[p] = rq()
                        return tab[p]
                    comps.append(sequential(ws, qf)); qs += list(tab.values())
            wt = [rng.random() for _ in comps]; z = sum(wt)
            pr = {}
            for c, x in zip(comps, wt):
                for k, v in c.items(): pr[k] = pr.get(k, 0)+v*x/z
            return qs, pr
        for emb in ("C", "S"):
            qs, pr = make(wC if emb == "C" else wS)
            hyp = all(q >= 0 for q in qs) and abs(sum(pr.values())-1) < 1e-9 \
                and set(k for k, v in pr.items() if v > 0) <= (posC if emb == "C" else posS)
            if emb == "C":
                nC += 1
                if not hyp: continue
                qualC += 1
                Pl, Pm, j = pr.get((2, 3, 1), 0), pr.get((2, 3, 3), 0), J(pr)
                minPl = min(minPl, 27*Pl); minJ = min(minJ, j)
                if Pl > 0: maxratio = max(maxratio, Pm/Pl)
                if not (Pl >= (1-1e-12)/27 and Pm <= Pl*(1+1e-12) and j >= (A-M)/27*(1-1e-12) and j > .01):
                    failC.append((kind, qs[:5], Pl, Pm, j))
            else:
                nS += 1
                if not hyp: continue
                qualS += 1; j = J(pr); minJS = min(minJS, j)
                if j < -1e-12: failS.append((kind, qs[:5], j))
    res["P5"] = not failC and qualC > 0
    res["P6"] = not failS and qualS > 0
    log(f"P5 conjugate carriers {nC}, qualifying {qualC}, failures {len(failC)}; min 27*P_l={minPl:.15f}; max P_m/P_l={maxratio:.6f}; min J={minJ:.6f}")
    for f in failC[:5]: log("  P5 FAIL", f)
    log(f"P6 specified carriers {nS}, qualifying {qualS}, failures {len(failS)}; min J={minJS:.3e}")
    for f in failS[:5]: log("  P6 FAIL", f)
    # P7 probes
    d2 = {}
    for w, v in wC.items(): d2[w[:2]] = d2.get(w[:2], 0)+v
    top2 = sorted(d2.items(), key=lambda kv: -kv[1])
    log("P7a conj depth-2 masses (x512), descending:", [(k, round(v, 4)) for k, v in top2])
    minblock = min(27*block(wC, q1, q2_).get((2, 3, 1), 0) for q1 in [0, .5, 1, 2, 5, 20, math.inf] for q2_ in [0, 1, math.inf])
    blockJ = min(J(block(wC, q1, q2_)) for q1 in [0, .5, 1, 2, 5, 20, math.inf] for q2_ in [0, 1, math.inf])
    log(f"P7a block mode: min 27*P_l={minblock:.6g}, min J={blockJ:.6g} ; (2,3) unique depth-2 conj max: {top2[0][0] == (2, 3)}")
    negJ = min(J(complete(wC, q)) for q in [-0.5, -1, -2, -5, -20, -100])
    log(f"P7b conjugate complete-word q<0: min J={negJ:.6g}")
    for q in [0.0, 1.0, math.inf]:
        log(f"P8 conj complete q={q}: J={J(complete(wC, q)):.6f}  P_l={complete(wC, q)[(2,3,1)]:.6f}; spec J={J(complete(wS, q)):.3e}")
    seq0 = sequential(wC, lambda p: 0.0); log(f"P8 conj sequential all q=0: 27*P_l={27*seq0[(2,3,1)]:.15f} J={J(seq0):.6f}")
    log(f"P8 ordinary J (spec q=1) = {J(complete(wS, 1.0)):.3e}")
    for k in sorted(res): log(k, "PASS" if res[k] else "FAIL")
    out.close()
    return 0 if all(res.values()) else 1

if __name__ == "__main__":
    sys.exit(main())
