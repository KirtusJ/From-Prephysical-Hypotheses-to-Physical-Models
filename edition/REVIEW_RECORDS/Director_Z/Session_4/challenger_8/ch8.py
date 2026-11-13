"""Challenger 8: Theorem thm:vertexlaw, exact check. Predicates fixed before first run.

Hypothesis test per carrier (H): finite; every vertex has exactly d>=2 out-arcs; at most one arc
per ordered pair (targets distinct); gains in finite abelian C.  Number qualifying is reported.
P1  for each qualifying carrier and S in {2,3} (and 4 when |V||C|<=16): exact dimension of the
    solution space of (GL) restricted to families of total size <=S (unknowns F_y(m), 1<=|m|<=S,
    F_y(0)=0) equals  sum_T |C|/|Gamma_T| + sum_{unordered {psi,lam}} dim K_{psi lam}.
P2  for each carrier and each character s: dim E_s (linear algebra over Q(zeta)) equals the number
    of terminal classes T with s trivial on Gamma_T (Gamma_T by search of closed walks).
P3  dim K_{psi lam} <= dim E_{psi lam} for all pairs.
P4  strongly connected and Gamma_V=C: dimension (S=3) equals 1+|U(D)/~|.
P4b trivial character not in U(D), every carrier.
P5  (6a) two disjoint Hadamard digraphs over C_2: |sigma_psi|^2 on copy 1, 0 on copy 2 satisfies
    every (GL) equation of total size <=4.
P6  (6b) F(m)=|m| if m=2^k e_h else 0 satisfies F(2m)=2F(m) for all |m|<=24 over C_2 and C_3, and
    F(3e)-3F(2e)+3F(e)-F(0) = -3.
P7  hand candidate (source r of in-degree 0, a,b of in-degree 1, feeding a 2-vertex terminal class;
    idea: non-polynomial solutions might live on the tree-like transient part): P1 at S=3 and 4.
P8  (item 7) for every carrier with a full block (d vertices with one successor set):
    U(D) subset of U(B) for that block.
Measured only: category counts.  Seed 20261113.  Result file is opened with mode 'x'.
"""
import itertools, random, sys, json
from math import gcd, comb
from flint import fmpz_mat

SEED = 20261113

def lcm(a, b): return a*b//gcd(a, b)

class Grp:
    def __init__(s, a, b=1):
        s.a, s.b = a, b
        s.el = [(i, j) for i in range(a) for j in range(b)]
        s.ix = {h: i for i, h in enumerate(s.el)}
        s.n = len(s.el); s.e = lcm(a, b)
        s.chars = list(s.el)
        comp = {2: [[-1]], 3: [[0, -1], [1, -1]], 4: [[0, -1], [1, 0]]}[s.e]
        s.phi = len(comp)
        I = [[int(i == j) for j in range(s.phi)] for i in range(s.phi)]
        s.rep = [I]
        for k in range(1, s.e): s.rep.append(mm(s.rep[-1], comp))
        s.I = I
    def mul(s, g, h):  # indices
        x, y = s.el[g], s.el[h]
        return s.ix[((x[0]+y[0]) % s.a, (x[1]+y[1]) % s.b)]
    def inv(s, g):
        x = s.el[g]; return s.ix[((-x[0]) % s.a, (-x[1]) % s.b)]
    def ch(s, c, g):  # exponent mod e of chars[c] at element g
        j, h = s.chars[c], s.el[g]
        return (s.e//s.a*j[0]*h[0] + s.e//s.b*j[1]*h[1]) % s.e
    def cmul(s, c1, c2):
        x, y = s.chars[c1], s.chars[c2]
        return s.ix[((x[0]+y[0]) % s.a, (x[1]+y[1]) % s.b)]

def mm(A, B):
    n = len(A)
    return [[sum(A[i][k]*B[k][j] for k in range(n)) for j in range(n)] for i in range(n)]

def nulldim(G, rows, ncols):
    """rows: list of dict col -> phi x phi int matrix (element of Z[zeta]); null dim over Q(zeta)."""
    p = G.phi
    if not rows: return ncols
    M = fmpz_mat(len(rows)*p, ncols*p)
    for r, row in enumerate(rows):
        for c, blk in row.items():
            for i in range(p):
                for j in range(p):
                    if blk[i][j]: M[r*p+i, c*p+j] = blk[i][j]
    rk = M.rank()
    assert rk % p == 0
    return ncols - rk//p

def addb(row, c, blk, sign=1, G=None):
    p = len(blk)
    cur = row.get(c) or [[0]*p for _ in range(p)]
    row[c] = [[cur[i][j]+sign*blk[i][j] for j in range(p)] for i in range(p)]

# carrier: arcs[y] = list of (z, gain index), length d, distinct z
def hyp(G, n, d, arcs):
    return d >= 2 and all(len(arcs[y]) == d and len({z for z, _ in arcs[y]}) == d for y in range(n))

def reach(n, arcs):
    R = [{y} for y in range(n)]
    ch = True
    while ch:
        ch = False
        for y in range(n):
            new = set(R[y])
            for v in list(R[y]):
                for z, _ in arcs[v]: new |= R[z]
            if new != R[y]: R[y] = new; ch = True
    return R

def terminal_classes(n, arcs):
    R = reach(n, arcs); out = []
    for y in range(n):
        if all(y in R[z] for z in R[y]):
            T = frozenset(R[y])
            if T not in out: out.append(T)
    return out, R

def gamma(G, arcs, b):
    seen = set(); st = [(z, g) for z, g in arcs[b]]
    while st:
        x = st.pop()
        if x in seen: continue
        seen.add(x)
        for z, g in arcs[x[0]]: st.append((z, G.mul(x[1], g)))
    return {g for v, g in seen if v == b}

def dimE(G, n, d, arcs, s):
    rows = []
    for y in range(n):
        row = {}
        for z, g in arcs[y]: addb(row, z, G.rep[G.ch(s, g)])
        addb(row, y, [[d*x for x in r] for r in G.I], -1)
        rows.append(row)
    return nulldim(G, rows, n)

def dimK(G, n, d, arcs, psi, lam):
    rows = []
    for y in range(n):
        for y2 in range(n):
            row = {}
            for z, g in arcs[y]:
                for z2, g2 in arcs[y2]:
                    if z == z2: addb(row, z, G.rep[(G.ch(psi, g)+G.ch(lam, g2)) % G.e])
            if y == y2: addb(row, y, [[d*x for x in r] for r in G.I], -1)
            if row: rows.append(row)
    return nulldim(G, rows, n)

def inU(G, cols, d, psi):
    """cols: list of dict z->gain (columns); psi in U iff sum_z conj(psi(col_y))psi(col_y') = d delta."""
    p = G.phi
    for a in range(len(cols)):
        for b in range(len(cols)):
            S = [[0]*p for _ in range(p)]
            for z, g in cols[a].items():
                if z in cols[b]:
                    blk = G.rep[(G.ch(psi, cols[b][z])-G.ch(psi, g)) % G.e]
                    S = [[S[i][j]+blk[i][j] for j in range(p)] for i in range(p)]
            want = [[(d if a == b else 0)*x for x in r] for r in G.I]
            if S != want: return False
    return True

def multisets(nitems, S):
    for k in range(S+1):
        yield from itertools.combinations_with_replacement(range(nitems), k)

def gl_rows(G, n, d, arcs, S):
    """integer rows of (GL) for families of total size <=S. Unknown index: (y, count vector)."""
    q = G.n; col = {}
    def cid(y, m):
        k = (y, m)
        if k not in col: col[k] = len(col)
        return col[k]
    for y in range(n):                       # all unknowns, fixed order
        for ms in multisets(q, S):
            if ms:
                v = [0]*q
                for h in ms: v[h] += 1
                cid(y, tuple(v))
    rows = set()
    for fam in multisets(n*q, S):
        m = [[0]*q for _ in range(n)]
        for it in fam: m[it//q][it % q] += 1
        w = [[0]*q for _ in range(n)]
        for y in range(n):
            if any(m[y]):
                for z, g in arcs[y]:
                    for h in range(q):
                        if m[y][h]: w[z][G.mul(g, h)] += m[y][h]
        row = {}
        for z in range(n):
            if any(w[z]): c = cid(z, tuple(w[z])); row[c] = row.get(c, 0)+1
        for y in range(n):
            if any(m[y]): c = cid(y, tuple(m[y])); row[c] = row.get(c, 0)-d
        row = tuple(sorted((c, v) for c, v in row.items() if v))
        if row: rows.add(row)
    return sorted(rows), col

def gl_dim(G, n, d, arcs, S):
    rows, col = gl_rows(G, n, d, arcs, S)
    M = fmpz_mat(max(len(rows), 1), len(col))
    for r, row in enumerate(rows):
        for c, v in row: M[r, c] = v
    return len(col)-M.rank()

def analyse(name, G, n, d, arcs):
    rec = {"name": name, "C": (G.a, G.b), "n": n, "d": d,
           "arcs": [[(z, G.el[g]) for z, g in a] for a in arcs]}
    rec["H"] = hyp(G, n, d, arcs)
    if not rec["H"]: return rec
    Ts, R = terminal_classes(n, arcs)
    gam = [gamma(G, arcs, min(T)) for T in Ts]
    rec["nT"] = len(Ts); rec["gam"] = [len(g) for g in gam]
    rec["sc"] = (len(Ts) == 1 and len(Ts[0]) == n)
    indeg = [0]*n
    for y in range(n):
        for z, _ in arcs[y]: indeg[z] += 1
    rec["indeg"] = indeg
    nc = G.n
    # P2
    p2 = True; Ef = []
    for s in range(nc):
        f = sum(1 for g in gam if all(G.ch(s, x) == 0 for x in g))
        e = dimE(G, n, d, arcs, s); Ef.append(e)
        if e != f: p2 = False
    rec["P2"] = p2
    # K
    ksum = 0; p3 = True; kd = {}
    for a in range(nc):
        for b in range(a, nc):
            k = dimK(G, n, d, arcs, a, b)
            if k: kd[f"{a},{b}"] = k
            ksum += k
            if k > Ef[G.cmul(a, b)]: p3 = False
    rec["P3"] = p3; rec["K"] = kd
    rec["formula"] = sum(nc//len(g) for g in gam)+ksum
    cols = [dict(arcs[y]) for y in range(n)]
    U = [s for s in range(nc) if inU(G, cols, d, s)]
    rec["U"] = U; rec["P4b"] = (0 not in U)
    dims = {}
    for S in (2, 3, 4):
        if S == 4 and n*G.n > 16: continue
        dims[S] = gl_dim(G, n, d, arcs, S)
    rec["dims"] = dims
    rec["P1"] = {S: (v == rec["formula"]) for S, v in dims.items()}
    if rec["sc"] and len(gam[0]) == nc:
        classes = {frozenset((s, G.inv(s))) for s in U}
        rec["P4"] = (dims[3] == 1+len(classes)); rec["P4_expected"] = 1+len(classes)
    # P8 full blocks
    bysucc = {}
    for y in range(n): bysucc.setdefault(frozenset(z for z, _ in arcs[y]), []).append(y)
    p8 = None
    for ss, ys in bysucc.items():
        for blk in itertools.combinations(ys, d):
            UB = [s for s in range(nc) if inU(G, [cols[y] for y in blk], d, s)]
            ok = set(U) <= set(UB)
            p8 = ok if p8 is None else (p8 and ok)
    rec["P8"] = p8
    return rec

def build():
    out = []
    C2, C3, C4, V4 = Grp(2), Grp(3), Grp(4), Grp(2, 2)
    def ix(G, t): return G.ix[t if isinstance(t, tuple) else (t, 0)]
    def car(name, G, d, spec):
        arcs = [[(z, ix(G, g)) for z, g in a] for a in spec]
        out.append((name, G, len(spec), d, arcs))
    # hand-built
    car("had2_C2", C2, 2, [[(0, 0), (1, 0)], [(0, 0), (1, 1)]])
    car("had2_C4_real", C4, 2, [[(0, 0), (1, 0)], [(0, 0), (1, 2)]])
    car("had2_C4_i", C4, 2, [[(0, 0), (1, 0)], [(0, 1), (1, 3)]])
    car("allones2_C2", C2, 2, [[(0, 0), (1, 0)], [(0, 0), (1, 0)]])
    car("fourier3_C3", C3, 3, [[(0, 0), (1, 0), (2, 0)], [(0, 0), (1, 1), (2, 2)], [(0, 0), (1, 2), (2, 1)]])
    car("bip4_C2_had", C2, 2, [[(2, 0), (3, 0)], [(2, 0), (3, 1)], [(0, 0), (1, 0)], [(0, 0), (1, 1)]])
    car("bip4_C2_allg", C2, 2, [[(2, 1), (3, 1)], [(2, 1), (3, 1)], [(0, 1), (1, 1)], [(0, 1), (1, 1)]])
    car("twohad_C2", C2, 2, [[(0, 0), (1, 0)], [(0, 0), (1, 1)], [(2, 0), (3, 0)], [(2, 0), (3, 1)]])
    car("had_V4", V4, 2, [[(0, (0, 0)), (1, (0, 0))], [(0, (1, 0)), (1, (0, 1))]])
    car("had_V4_b", V4, 2, [[(0, (0, 0)), (1, (0, 0))], [(0, (0, 0)), (1, (1, 0))]])
    car("cyc3_d2_C3", C3, 2, [[(1, 0), (2, 1)], [(2, 0), (0, 1)], [(0, 0), (1, 2)]])
    car("K3loops_C2", C2, 3, [[(0, 1), (1, 0), (2, 0)], [(0, 0), (1, 1), (2, 0)], [(0, 0), (1, 0), (2, 1)]])
    car("src_into_had_C2", C2, 2, [[(1, 0), (2, 1)], [(1, 0), (2, 0)], [(1, 0), (2, 1)]])
    car("two_terminal_mixed_C4", C4, 2, [[(0, 0), (1, 0)], [(0, 1), (1, 3)], [(2, 0), (3, 0)], [(2, 0), (3, 2)],
                                           [(0, 1), (2, 3)], [(4, 1), (3, 0)]])
    car("HAND_tree_into_terminal_C3", C3, 2, [[(1, 0), (2, 1)], [(3, 0), (4, 2)], [(3, 1), (4, 0)],
                                              [(3, 0), (4, 0)], [(3, 0), (4, 1)]])
    car("HAND_tree_into_terminal_C2", C2, 2, [[(1, 0), (2, 1)], [(3, 0), (4, 1)], [(3, 1), (4, 0)],
                                              [(3, 0), (4, 0)], [(3, 0), (4, 1)]])
    # deliberately non-qualifying (hypothesis test must reject): out-degrees differ
    car("NONQUAL_outdeg", C2, 2, [[(0, 0), (1, 0)], [(0, 0)]])
    rng = random.Random(SEED)
    groups = [("C2", C2), ("C3", C3), ("C4", C4), ("V4", V4)]
    def rgain(G, sub):
        if sub == "full": return rng.randrange(G.n)
        if sub == "triv": return 0
        if G is C4: return rng.choice([G.ix[(0, 0)], G.ix[(2, 0)]])
        if G is V4: return rng.choice([G.ix[(0, 0)], G.ix[(1, 0)]])
        return 0
    k = 0
    for gname, G in groups:
        for d, n, kind, sub in [(2, 2, "any", "full"), (2, 3, "any", "full"), (2, 4, "any", "full"),
                                (2, 4, "any", "sub"), (2, 5, "trans", "full"), (2, 4, "two", "full"),
                                (2, 6, "two", "full"), (3, 3, "any", "full"), (3, 4, "any", "full"),
                                (3, 4, "any", "sub"), (3, 5, "trans", "full"), (2, 6, "any", "full"),
                                (3, 6, "two", "full")]:
            arcs = []
            for y in range(n):
                if kind == "any": pool = list(range(n))
                elif kind == "trans":  # last d+... vertices closed: vertices >= n-(d+1)+... terminal part
                    t0 = n-d if d == 3 else n-3
                    pool = list(range(t0, n)) if y >= t0 else list(range(n))
                else:  # two closed parts
                    h = d if d == 3 else 2
                    if y < h: pool = list(range(h))
                    elif y < 2*h: pool = list(range(h, 2*h))
                    else: pool = list(range(n))
                tg = rng.sample(pool, d)
                arcs.append([(z, rgain(G, sub)) for z in sorted(tg)])
            k += 1
            out.append((f"rand{k}_{gname}_d{d}_n{n}_{kind}_{sub}", G, n, d, arcs))
    return out

def main():
    fout = open("results_ch8.jsonl", "x")
    recs = []
    for name, G, n, d, arcs in build():
        r = analyse(name, G, n, d, arcs); recs.append(r)
        fout.write(json.dumps(r, default=list)+"\n"); fout.flush()
        print(name, r.get("H"), r.get("nT"), r.get("gam"), r.get("sc"), r.get("formula"), r.get("dims"),
              r.get("U"), r.get("P2"), r.get("P4"), r.get("P8"), flush=True)
    q = [r for r in recs if r["H"]]
    S = {"carriers": len(recs), "qualifying": len(q)}
    inst = [(r["name"], s, ok) for r in q for s, ok in r["P1"].items()]
    S["P1"] = [sum(ok for _, _, ok in inst), len(inst)]
    S["P1_S4"] = [sum(ok for _, s, ok in inst if s == 4), sum(1 for _, s, _ in inst if s == 4)]
    S["P1_failed"] = [(a, b) for a, b, ok in inst if not ok]
    for p in ("P2", "P3", "P4b"): S[p] = [sum(bool(r[p]) for r in q), len(q)]
    p4 = [r for r in q if "P4" in r]; S["P4"] = [sum(r["P4"] for r in p4), len(p4)]
    p8 = [r for r in q if r["P8"] is not None]; S["P8"] = [sum(r["P8"] for r in p8), len(p8)]
    S["P7"] = {r["name"]: r["P1"] for r in q if r["name"].startswith("HAND")}
    S["measured"] = {
        "sc_gamma_full": sum(1 for r in q if r["sc"] and r["gam"][0] == r["C"][0]*r["C"][1]),
        "sc_gamma_proper": sum(1 for r in q if r["sc"] and r["gam"][0] < r["C"][0]*r["C"][1]),
        "nonsc_one_terminal": sum(1 for r in q if not r["sc"] and r["nT"] == 1),
        "two_terminal": sum(1 for r in q if r["nT"] == 2),
        "indeg0or1": sum(1 for r in q if min(r["indeg"]) <= 1),
        "U_nonempty": sum(1 for r in q if r["U"]), "U_empty": sum(1 for r in q if not r["U"]),
        "K_offdiag(psi*lam!=1)": sum(1 for r in q if any(True for k in r["K"])),
        "d2": sum(1 for r in q if r["d"] == 2), "d3": sum(1 for r in q if r["d"] == 3)}
    # P5
    C2 = Grp(2)
    arcs = [[(0, 0), (1, 0)], [(0, 0), (1, 1)], [(2, 0), (3, 0)], [(2, 0), (3, 1)]]
    rows, col = gl_rows(C2, 4, 2, arcs, 4)
    val = {c: ((m[0]-m[1])**2 if y < 2 else 0) for (y, m), c in col.items()}
    S["P5"] = all(sum(v*val[c] for c, v in row) == 0 for row in rows); S["P5_rows"] = len(rows)
    # P6
    def F(m):
        nz = [x for x in m if x]
        if len(nz) == 1 and nz[0] & (nz[0]-1) == 0: return nz[0]
        return 0
    ok = True; cnt = 0
    for q_ in (2, 3):
        for m in itertools.product(range(25), repeat=q_):
            if sum(m) <= 24:
                cnt += 1
                if F(tuple(2*x for x in m)) != 2*F(m): ok = False
    S["P6_law"] = [ok, cnt]; S["P6_third_difference"] = F((3, 0))-3*F((2, 0))+3*F((1, 0))-F((0, 0))
    fout.write(json.dumps({"SUMMARY": S})+"\n"); fout.close()
    print(json.dumps(S, indent=1))

main()
