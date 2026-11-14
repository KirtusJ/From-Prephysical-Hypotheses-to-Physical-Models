"""Builder exploration for G10 cor:return, sign premise.  Seed 20261113 (no randomness is used; carriers are fixed).

Predicates, fixed before the first run.  For each carrier the HYPOTHESIS is tested first:
  H1 every vertex has the same out-degree d >= 2 (single arcs hold by the E[z][y] representation);
  H2 the derived digraph D-hat is strongly connected;
  H3 U(D) (characters with A*A = d, exact test) is non-empty.
Carriers failing H1-H3 are listed and not tested.  For qualifying carriers, with endpoint y = x0 = vertex 0:
  P1 (full coset)  there is a length t0 <= TMAX at which the gains of walks x0 -> x0 form a full coset of a
                   subgroup H, and at t0 + r0, t0 + 2 r0 (r0 = gcd of return lengths seen) the gain set is the same
                   coset or a translate and the minimum walk count per gain strictly increases.
  P2 (restrictions nontrivial) every k in U(D) is nontrivial on H.
  P3 (a-test)      for every k in U(D): sum_{g in coset} psi_k(g) = 0 exactly (zero_sum).
  P4 (c-test)      for each class rho of U(D)|H up to inversion and T = 1..TT, with m_T(h) = floor(T(1+Re rho(h))):
                   | sigma_rho(m_T) - T|H|e | < |H|  (e = 1/2, or 1 if rho has order two) and
                   | sigma_lam(m_T) | < |H| for every other class lam.  Reported: the largest error over |H|
                   (a measured ratio, must be < 1; no tolerance is used other than this comparison; floats).
  P5 (realizable)  m_TT is <= the walk counts at some length <= TMAX (length reported).
  P6 (negative constants are detected) rule a=-1, all c=1: weight of the one-per-gain event is -|H| < 0;
                   rule a=1, c_rho=-1, other c=1: some T <= TT gives weight < 0 (first such T reported).
Result file opened with mode 'x'.
"""
import sys, json, math, cmath, itertools
sys.path.insert(0, '/home/user/From-Prephysical-Hypotheses-to-Physical-Models/REVIEW_QUEUE/lib')
import pcplib as P

TMAX, TT = 40, 12
out = open(sys.argv[1], 'x')

def carriers():
    yield 'two_vertex_Z2', P.sign_carrier([[1, 1], [1, -1]]), (2,)
    for N in (3, 4, 5, 8): yield 'ring%d' % N, P.ring_carrier(N), (2,)
    yield 'W43', P.sign_carrier(P.W43), (2,)
    yield 'C6', P.sign_carrier(P.C6), (2,)
    yield 'F5_complete_Z5xZ5', [[(1, (i * j) % 5) for i in range(5)] for j in range(5)], (5, 5)
    yield 'fourier3_Z3', [[((i * j) % 3,) for i in range(3)] for j in range(3)], (3,)
    yield 'fourier4_Z4', [[((i * j) % 4,) for i in range(4)] for j in range(4)], (4,)
    # deliberately non-qualifying controls
    yield 'ctrl_all_plus_2', P.sign_carrier([[1, 1], [1, 1]]), (2,)
    yield 'ctrl_irregular', [[(0,), (0,), None], [(0,), None, (1,)], [None, (1,), (0,)]], (2,)

res = []
for name, E, mod in carriers():
    r = {'carrier': name}
    n = len(E); G = P.group(mod); L = P.lcm(mod); nG = len(G)
    degs = {sum(1 for z in range(n) if E[z][y] is not None) for y in range(n)}
    h1 = len(degs) == 1 and min(degs) >= 2
    verts, S = P.lift(E, mod)
    h2 = P.strongly_connected(S)
    U = [k for k in G if h1 and P.norm_preserving(E, mod, k) is not None]
    r.update(H1=h1, H2=h2, H3=len(U) > 0, nU=len(U))
    if not (h1 and h2 and U):
        r['qualifies'] = False; res.append(r); continue
    r['qualifies'] = True; d = min(degs)
    wc = P.walk_counts(S, 0, TMAX)
    at = [{G[i]: c for i, c in w.items() if i < nG} for w in wc]      # endpoint x0 = vertex 0: indices 0..nG-1
    if isinstance(verts, dict): verts = [k for k, _ in sorted(verts.items(), key=lambda kv: kv[1])]
    assert verts[0] == (0, P.gzero(mod)) and all(verts[i][0] == 0 for i in range(nG))
    r0 = 0
    for t in range(1, TMAX + 1):
        if at[t]: r0 = math.gcd(r0, t)
    def coset_of(gs):
        gs = sorted(gs); H = sorted({P.gsub(g, gs[0], mod) for g in gs})
        closed = all(P.gadd(a, b, mod) in H for a in H for b in H)
        return H if closed and len(H) == len(gs) else None
    t0 = None
    for t in range(1, TMAX - 2 * r0 + 1):
        if not (at[t] and at[t + r0] and at[t + 2 * r0]): continue
        H = coset_of(at[t])
        if H is None: continue
        ok = all(coset_of(at[t + j * r0]) == H for j in (1, 2))
        mins = [min(at[t + j * r0].values()) for j in (0, 1, 2)]
        if ok and mins[0] < mins[1] < mins[2]: t0 = t; break
    r.update(r0=r0, P1=t0 is not None, t0=t0)
    if t0 is None: res.append(r); continue
    r.update(H_order=len(H), min_counts=mins)
    base = min(at[t0])
    # P2, P3
    r['P2'] = all(any(P.chi_exp(k, h, mod) != 0 for h in H) for k in U)
    r['P3'] = all(P.zero_sum([P.chi_exp(k, P.gadd(base, h, mod), mod) for h in H], L) for k in U)
    # classes of restrictions up to inversion
    cls = {}
    for k in U:
        v = tuple(P.chi_exp(k, h, mod) for h in H); w = tuple((-e) % L for e in v)
        cls.setdefault(min(v, w), k)
    keys = sorted(cls); r['n_classes'] = len(keys)
    z = lambda e: cmath.exp(2j * math.pi * e / L)
    worst = 0.0; p6 = {}; mT_max = {}
    for rho in keys:
        e2 = all((2 * e) % L == 0 for e in rho); main = 1.0 if e2 else 0.5
        first_neg = None
        for T in range(1, TT + 1):
            m = [math.floor(T * (1 + math.cos(2 * math.pi * e / L)) + 1e-9) for e in rho]   # 1e-9: guards exact integers
            w = 1 * sum(m)                                                               # rule a=1, c_rho=-1, others 1
            for lam in keys:
                s = sum(mi * z(e) for mi, e in zip(m, lam))
                err = abs(s - T * len(H) * main) if lam == rho else abs(s)
                worst = max(worst, err / len(H))
                w += (-1 if lam == rho else 1) * abs(s) ** 2
            if w < 0 and first_neg is None: first_neg = (T, w)
            if T == TT: mT_max[rho] = m
        p6[str(rho)] = first_neg
    r.update(P4=worst < 1, P4_worst_error_over_H=worst)
    need = [max(mT_max[rho][i] for rho in keys) for i in range(len(H))]
    tl = next((t for t in range(t0, TMAX + 1, r0) if coset_of(at[t]) == H and
               all(at[t][P.gadd(min(at[t]), h, mod)] >= nd for h, nd in zip(H, need))), None)
    r.update(P5=tl is not None, P5_length=tl, P6a_weight=-len(H), P6=all(v is not None for v in p6.values()), P6_first_negative=p6)
    res.append(r)

q = [r for r in res if r['qualifies']]
summary = {'carriers': len(res), 'qualifying': len(q), 'not_qualifying': [r['carrier'] for r in res if not r['qualifies']],
           'all_pass': all(r.get(p) for r in q for p in ('P1', 'P2', 'P3', 'P4', 'P5', 'P6')),
           'failed': [(r['carrier'], p) for r in q for p in ('P1', 'P2', 'P3', 'P4', 'P5', 'P6') if not r.get(p)]}
json.dump({'summary': summary, 'results': res}, out, indent=1, default=str); out.close()
print(json.dumps(summary, indent=1))
for r in q: print(r['carrier'], {k: r.get(k) for k in ('nU', 'r0', 't0', 'H_order', 'min_counts', 'n_classes', 'P4_worst_error_over_H', 'P5_length', 'P6_first_negative')})
