"""xr66 challenger program (exact; no floats). Predicates fixed before first run.

Carrier: ring of N wells (or line), rails R/L, start (0,R), arcs (RR,RL,LR,LL)=(1,g,1,zg),
chi(z)=-1, chi_s(g)=exp(2 pi i s/q). Port prob (pure s) = |sum chi(gain)|^2/2^t; count = #words/2^t.

CONTROL  line, t=3: P(-1,L)=0, P(1,R)=4/8 coherent; count 2/8 each.
A1 ring N=4,q=3,t=3: (site1 R, site3 R)*8 = (4,0) for s=0, (4,3) for s=1 and s=2, (2,2) count.
C1 for q=2..6, D=2..5 (N=2D): direct ring propagation at port (t=kD+1, x=t mod 2D, R), k=1..K=floor(Q/2),
   equals RHS of note eq (1) with a_h computed on the LINE, for 5 random rational mixtures (seed 20261113).
C2 coefficient of J_k at stage k equals 2*a_0*a_k = 2*(-1)^(kD-1) (nonzero); system triangular by construction
   of (1): checked by C1 holding with only J_0..J_k present.
C3 recovery: c from tick-3 anchor (site -1, L) = c/4; J_1..J_K by forward substitution; Fourier inversion
   returns the chosen folded masses exactly.
C4 aliases: two mixtures with equal c and equal folded masses (key = {Ds mod q, -Ds mod q}) but different b_s
   give identical probabilities at EVERY port at every clock t<=Tmax=(K+2)D+3. Hypothesis tested per
   instance: a second distinct mixture with the same folded masses exists (else instance does not qualify).
C4m same with 10 random whole-position masks per instance (measured: count equal / unequal).
C5 w+- ensembles (Q>=2): identical at all ports for t<=KD, different at the selected port at t=KD+1.
C6 counterexample search: minimal T such that the pure responses (count + one label per folded class) over
   all ports at all clocks <=T are linearly independent; predicate: T_min == max(3, K*D+1).
   (A smaller T_min refutes "optimal last clock"; a larger one refutes identifiability.)
C7 q=3, 3 not| D: 2^(D+1) p_A = D^2(1-c)+Dc, 2^(D+1) p_B = 2+2 eps J_1 at t=D+1, sites D-1 and D+1, rail R.
C8 for all q,D: at every t<=D all ports have the same probability under every label s (earliest tick D+1).
X1 (extension, measured only) odd rings N=5,7 with D=N: C6-type minimal T vs max(3,KD+1).
Result file opened with mode 'x'. All failed predicates are kept in the file.
"""
import sys, json, random, itertools
from fractions import Fraction as Fr
import sympy as sp

def step(state, N, q, mask=None):
    new = {}
    for (x, rail, r), (sg, cn) in state.items():
        for o in (0, 1):  # 0=R,1=L
            nx = x + 1 if o == 0 else x - 1
            if N: nx %= N
            if mask is not None and nx not in mask: continue
            nr = r + (1 if o == 1 else 0)
            if q: nr %= q
            s2 = -sg if (rail == 1 and o == 1) else sg
            k = (nx, o, nr)
            a, b = new.get(k, (0, 0))
            new[k] = (a + s2, b + cn)
    return new

def ports(state, q):
    """port -> (signed vector n_r over r mod q, count)"""
    out = {}
    for (x, rail, r), (sg, cn) in state.items():
        v, c = out.setdefault((x, rail), ([0]*q, 0))
        v[r] += sg
        out[(x, rail)] = (v, c + cn)
    return out

def autocorr(v, q):
    return [sum(v[r]*v[(r+m) % q] for r in range(q)) for m in range(q)]

def cosq(k, q):
    return sp.cos(2*sp.pi*sp.Rational(k % q, q))

def pure(v, q, s):
    ac = autocorr(v, q)
    return sp.expand(sum(ac[m]*cosq(s*m, q) for m in range(q)))

def mixprob(v, cn, q, t, c, b):
    return sp.expand((c*cn + sum(b[s]*pure(v, q, s) for s in range(q) if b[s] != 0)) / sp.Integer(2)**t)

def run(N, q, T, masks=None):
    st = {(0, 0, 0): (1, 1)}
    res = {}
    for t in range(1, T+1):
        st = step(st, N, q, None if masks is None else masks[t-1])
        res[t] = ports(st, q)
    return res

def line_a(D, k):
    """a_h: signed sum over line words of length kD+1 ending R with hD left steps."""
    t = k*D+1
    st = {(0, 0, 0): (1, 1)}
    for _ in range(t): st = step(st, 0, 0)
    a = [0]*(k+1); F = 0
    for (x, rail, l), (sg, cn) in st.items():
        if rail == 0 and l % D == 0:
            a[l//D] += sg; F += cn
    return a, F

def rand_mix(rng, q):
    w = [rng.randint(0, 9) for _ in range(q+1)]
    if sum(w) == 0: w[0] = 1
    tot = sum(w)
    return sp.Rational(w[0], tot), [sp.Rational(x, tot) for x in w[1:]]

def key(s, D, q):
    a = (D*s) % q
    return min(a, (-a) % q)

def rref_rows(rows):
    rows = [list(map(Fr, r)) for r in rows]
    basis = []
    for r in rows:
        for b, p in basis:
            if r[p] != 0:
                f = r[p]/b[p]; r = [x-f*y for x, y in zip(r, b)]
        p = next((i for i, x in enumerate(r) if x != 0), None)
        if p is not None: basis.append((r, p))
    return [b for b, _ in basis]

def min_T(N, D, q, Tmax):
    reps = {}
    for s in range(q): reps.setdefault(key(s, D, q), s)
    reps = sorted(reps.values())
    need = len(reps)+1
    Tm = sp.Matrix([[cosq(s*m, q) for s in reps]+[0] for m in range(q)]+[[0]*len(reps)+[1]])
    res = run(N, q, Tmax)
    rows = []; ranks = []
    for t in range(1, Tmax+1):
        for (x, rail), (v, cn) in res[t].items():
            rows.append(autocorr(v, q)+[cn])
        B = rref_rows(rows); rows = [list(b) for b in B]
        M = sp.Matrix([[sp.Rational(x.numerator, x.denominator) for x in b] for b in B])*Tm
        rk = M.applyfunc(sp.radsimp).rank(simplify=True)
        ranks.append(rk)
        if rk == need: return t, need, ranks
    return None, need, ranks

def main(outdir):
    out = open(outdir + "/xr66_exact.json", "x")
    rng = random.Random(20261113)
    R = {"predicates": {}, "failed": [], "measured": {}}
    def rec(name, ok, info=None):
        R["predicates"].setdefault(name, {"met": 0, "failed": 0})
        R["predicates"][name]["met" if ok else "failed"] += 1
        if not ok: R["failed"].append({"predicate": name, "info": info})
    # CONTROL
    st = {(0, 0, 0): (1, 1)}
    for _ in range(3): st = step(st, 0, 1)
    p = ports(st, 1)
    ctl = {str(k): [v[0][0]**2, v[1]] for k, v in p.items()}
    R["control_line_t3_num_over_8(coherent,count)"] = ctl
    rec("CONTROL", p[(-1, 1)][0][0]**2 == 0 and p[(1, 0)][0][0]**2 == 4 and p[(-1, 1)][1] == 2 and p[(1, 0)][1] == 2, ctl)
    # A1
    res = run(4, 3, 3)[3]
    A = {}
    for site in (1, 3):
        v, cn = res[(site, 0)]
        A[site] = {"s0": str(pure(v, 3, 0)), "s1": str(pure(v, 3, 1)), "s2": str(pure(v, 3, 2)), "count": cn, "n_r": v}
    R["A_table_times8"] = A
    rec("A1", [A[1]["s0"], A[3]["s0"], A[1]["s1"], A[3]["s1"], A[1]["s2"], A[3]["s2"], A[1]["count"], A[3]["count"]]
        == ["4", "0", "4", "3", "4", "3", 2, 2], A)
    R["A_all_ports_t3_N4"] = {str(k): {"n_r": v[0], "count": v[1]} for k, v in res.items()}
    # C
    qual = {"C4_qualify": 0, "C4_not_qualify": 0, "C5_qualify": 0, "C5_not_qualify": 0}
    c6 = []
    for q in range(2, 7):
        for D in range(2, 6):
            N = 2*D; d = sp.igcd(D, q); Q = q//d; K = Q//2
            Tmax = (K+2)*D+3
            res = run(N, q, Tmax)
            # C8
            for t in range(1, D+1):
                for port, (v, cn) in res[t].items():
                    vals = {str(pure(v, q, s)) for s in range(q)}
                    rec("C8", len(vals) == 1, [q, D, t, port])
            # earliest: does D+1 distinguish some pair? (measured)
            dist = any(len({str(pure(v, q, s)) for s in range(q)}) > 1 for v, cn in res[D+1].values())
            R["measured"].setdefault("tick_D+1_distinguishes_some_labels", {})[f"q{q}D{D}"] = dist
            aL = {k: line_a(D, k) for k in range(1, K+1)}
            for k in range(1, K+1):
                rec("C2", aL[k][0][0] == 1 and aL[k][0][k] == (-1)**(k*D-1), [q, D, k, aL[k][0]])
            for trial in range(5):
                c, b = rand_mix(rng, q)
                J = lambda j: sp.expand(sum(b[s]*cosq(D*s*j, q) for s in range(q)))
                # C1
                pk = {}
                for k in range(1, K+1):
                    t = k*D+1; v, cn = res[t][(t % N, 0)]
                    pk[k] = mixprob(v, cn, q, t, c, b)
                    a, F = aL[k]
                    rhs = J(0)*sum(x*x for x in a) + 2*sum(J(j)*sum(a[h]*a[h+j] for h in range(k-j+1)) for j in range(1, k+1))
                    rec("C1", sp.expand(2**t*pk[k] - c*F - rhs) == 0 and F == cn, [q, D, k, trial])
                # C3
                v, cn = res[3][((-1) % N, 1)]
                pa = mixprob(v, cn, q, 3, c, b)
                c_hat = 4*pa; Jh = {0: 1-c_hat}
                for k in range(1, K+1):
                    t = k*D+1; a, F = aL[k]
                    known = Jh[0]*sum(x*x for x in a) + 2*sum(Jh[j]*sum(a[h]*a[h+j] for h in range(k-j+1)) for j in range(1, k))
                    Jh[k] = sp.expand((2**t*pk[k] - c_hat*F - known)/(2*a[0]*a[k]))
                for j in range(K+1, Q): Jh[j] = Jh[Q-j]
                ok = (sp.expand(c_hat - c) == 0)
                for l in range(Q):
                    sym = sp.expand(sum(Jh[j]*sp.cos(2*sp.pi*sp.Rational(j*l, Q)) for j in range(Q))/Q)
                    wl = sum(b[s] for s in range(q) if ((D//d)*s) % Q == l)
                    wml = sum(b[s] for s in range(q) if ((D//d)*s) % Q == (-l) % Q)
                    ok = ok and sp.simplify(sym - (wl+wml)/2) == 0
                rec("C3", ok, [q, D, trial, str(c), [str(x) for x in b]])
                # C4: alias mixture: move mass within folded classes
                classes = {}
                for s in range(q): classes.setdefault(key(s, D, q), []).append(s)
                b2 = list(b); moved = False
                for ks, mem in classes.items():
                    if len(mem) > 1:
                        tot = sum(b[s] for s in mem)
                        if tot != 0:
                            ws = [rng.randint(0, 5) for _ in mem]
                            if sum(ws) == 0: ws[0] = 1
                            for s, w in zip(mem, ws): b2[s] = tot*sp.Rational(w, sum(ws))
                if b2 != list(b): moved = True
                if not moved:
                    qual["C4_not_qualify"] += 1
                else:
                    qual["C4_qualify"] += 1
                    bad = None
                    for t in range(1, Tmax+1):
                        for port, (v, cn) in res[t].items():
                            if sp.expand(mixprob(v, cn, q, t, c, b) - mixprob(v, cn, q, t, c, b2)) != 0:
                                bad = [q, D, t, port]; break
                        if bad: break
                    rec("C4", bad is None, bad)
                    if trial < 2:
                        for mi in range(5):
                            Tm_ = 2*D+3
                            masks = [set(x for x in range(N) if rng.random() < 0.75) for _ in range(Tm_)]
                            rm = run(N, q, Tm_, masks)
                            bad = None
                            for t in rm:
                                for port, (v, cn) in rm[t].items():
                                    if sp.expand(mixprob(v, cn, q, t, c, b) - mixprob(v, cn, q, t, c, b2)) != 0:
                                        bad = [q, D, t, port]
                            rec("C4m", bad is None, bad)
            # C5
            if Q >= 2:
                qual["C5_qualify"] += 1
                reps = {}
                for s in range(q): reps.setdefault(((D//d)*s) % Q, s)
                bp = [sp.Integer(0)]*q; bm = [sp.Integer(0)]*q
                for l, s in reps.items():
                    bp[s] = sp.expand((1+sp.cos(2*sp.pi*sp.Rational(K*l, Q)))/Q)
                    bm[s] = sp.expand((1-sp.cos(2*sp.pi*sp.Rational(K*l, Q)))/Q)
                okw = sp.simplify(sum(bp)-1) == 0 and sp.simplify(sum(bm)-1) == 0 and all(x >= 0 for x in bp+bm)
                bad = None
                for t in range(1, K*D+1):
                    for port, (v, cn) in res[t].items():
                        if sp.simplify(mixprob(v, cn, q, t, 0, bp) - mixprob(v, cn, q, t, 0, bm)) != 0:
                            bad = [t, port]
                t = K*D+1; v, cn = res[t][(t % N, 0)]
                diff = sp.simplify(mixprob(v, cn, q, t, 0, bp) - mixprob(v, cn, q, t, 0, bm))
                rec("C5", okw and bad is None and diff != 0, [q, D, okw, bad, str(diff)])
            else:
                qual["C5_not_qualify"] += 1
            # C6
            tm, need, ranks = min_T(N, D, q, Tmax)
            pred = max(3, K*D+1)
            c6.append({"q": q, "D": D, "Q": Q, "K": K, "T_min": tm, "predicted": pred, "ranks_by_tick": ranks, "need": need})
            rec("C6", tm == pred, c6[-1])
            # C7
            if q == 3 and D % 3 != 0:
                for trial in range(5):
                    c, b = rand_mix(rng, q)
                    t = D+1
                    vA, cA = res[t][((D-1) % N, 0)]; vB, cB = res[t][((D+1) % N, 0)]
                    pA = mixprob(vA, cA, q, t, c, b); pB = mixprob(vB, cB, q, t, c, b)
                    J1 = sum(b[s]*cosq(D*s, q) for s in range(q)); eps = (-1)**(D-1)
                    okA = sp.expand(2**t*pA - (D*D*(1-c)+D*c)) == 0
                    okB_note = sp.expand(2**t*pB - (2+2*eps*J1)) == 0
                    okB_withc = sp.expand(2**t*pB - (2*(1-c)+2*eps*J1+2*c)) == 0
                    rec("C7_pA", okA, [D, trial])
                    rec("C7_pB_as_printed", okB_note, [D, trial, str(c)])
                    rec("C7_pB_with_J0_and_count(2J0+2epsJ1+2c)", okB_withc, [D, trial])
    R["C6_table"] = c6
    R["qualification"] = qual
    # X1 odd rings
    x1 = []
    for N in (5, 7):
        for q in range(2, 7):
            D = N; d = sp.igcd(D, q); Q = q//d; K = Q//2
            tm, need, ranks = min_T(N, D, q, (K+1)*D+3)
            x1.append({"N": N, "q": q, "K": K, "T_min": tm, "max(3,KD+1)": max(3, K*D+1), "ranks_by_tick": ranks})
    R["measured"]["X1_odd_rings"] = x1
    json.dump(R, out, indent=1, default=str); out.close()
    print(json.dumps({"predicates": R["predicates"], "n_failed": len(R["failed"]), "qual": qual}, indent=1))
    print("first failures:", R["failed"][:6])
    print("C6:", [(r["q"], r["D"], r["T_min"], r["predicted"]) for r in c6])
    print("X1:", [(r["N"], r["q"], r["T_min"], r["max(3,KD+1)"]) for r in x1])
    print("A:", A); print("control:", ctl)

main(sys.argv[1])
