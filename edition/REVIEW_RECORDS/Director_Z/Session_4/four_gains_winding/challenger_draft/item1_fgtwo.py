#!/usr/bin/env python3
"""Item 1/2: Theorem thm:fgtwo on actual four-gain carriers, exact linear algebra (python-flint fmpz_mat.rank,
exact over Q). Written by the reviewer sub-agent; uses no program of the repository.

Usage: python3 item1_fgtwo.py <seed> <outfile> <maxcells>
  seed      : integer seed for the choice of carriers per class
  outfile   : result file, opened with mode 'x' (refuses to overwrite)
  maxcells  : cap on rows*cols of the 'all pairs' matrix; n is the largest n<=7 within the cap (n>=4 forced)

Carrier: abelian group A (additive tuples), gains (a,b,c,d), ring size N in {9,16}; M=N/gcd(N,2) (9 or 8).
delta=a+d-b-c, r=ord(delta), beta=M*(b+c-2a), H=<a,d,b+c>, Delta_N=<delta,beta>,
s=min{j>=1: j*beta in <delta>}, k=least k>=0 with 2beta=k*delta (parity meaningful only for r even).
Convention: (T_g m)(x)=m(x-g), i.e. T_g adds g to every gain. eps_i(m)=sum_{j=0}^{r-1}(-1)^j m(i*beta+j*delta).

Unknowns: F_R(m) for nonempty multisets m, |m|<=n, supported in one coset of Delta_N inside H;
          F_L(m) for nonempty multisets m, |m|<=n, supported in one coset of Delta_N inside b+H. F(empty)=0.
          NO relation between F_L and F_R and NO invariance is assumed.
Equations (eq:fg): for each coset kappa+Delta_N of H, U in M(kappa+Delta_N), V in M(kappa+b-d+Delta_N), |U|+|V|<=n:
          F_R(T_a U + T_c V) + F_L(T_b U + T_d V) - 2F_R(U) - 2F_L(V) = 0
   system 'adm': only pairs with U or V supported in one coset of <delta> (empty counts as one coset);
   system 'all': every pair.
dimproj(sys,n,n') = dimension of the solution space of the truncated system restricted to unknowns of size <= n'
                  = (ncols - rank A) - (ncols_high - rank A_high), exact.

PREDICATES (fixed before the first run):
 P0  hypothesis: s == 2 for the carrier (tested for every enumerated carrier; number qualifying reported).
 P1  the theorem's functions (count; for r even q-form eps0^2+eps1^2; for r even and k even also eps0*eps1),
     placed as F_R(m)=f(m-kappa) on kappa+Delta_N and F_L=F_R o T_c, satisfy every equation of 'all'. Exact integers.
 P2  dimproj(adm,n,n') == E for n' in {n-1,n-2}, E = 1 + (2 if r even and k even, 1 if r even and k odd, 0 if r odd).
 P3  dimproj(adm,n,n') == dimproj(all,n,n') for n' in {n-1,n-2,n-3}.
 P4  the theorem's functions are linearly independent on sizes <= n' (rank == E) for n' in {n-1,n-2}, n'>=2.
 P5  negative control, expected to FAIL to be a solution: for r even and k odd, eps0*eps1 placed through coset
     representatives violates some equation of 'adm' (confirms c=0 for k odd is forced, not a convention).
 P6  sign formulas: eps1(T_beta W)==eps0(W) and eps0(T_beta W)==(-1)^k eps1(W) for 200 random W in Z^{Delta_N}
     (r even only); sigma_chi == eps0 + chi(beta) eps1 for every character chi of Delta_N with chi(delta)=-1,
     chi(beta)^2 == (-1)^k, number of such chi == 2 (exact: characters evaluated as exponents modulo ord).
Truncation: a failure of P2 with P3 holding is a property of the cut (the proof uses multisets E_g of size r and
multiples of the all-ones multiset), not of the restriction to admissible pairs; both are recorded, none deleted.
"""
import sys, itertools, random, time, json
from math import gcd, comb
from fractions import Fraction
import flint

def main():
    seed = int(sys.argv[1]); outfile = sys.argv[2]; maxcells = int(sys.argv[3])
    out = open(outfile, 'x')
    def emit(o):
        out.write(json.dumps(o) + "\n"); out.flush()
    emit({"cmd": " ".join(sys.argv), "seed": seed, "maxcells": maxcells, "flint": flint.__version__})
    rng = random.Random(seed)
    groups = [(4,), (2, 2), (2, 4), (6,), (8,), (2, 2, 2), (12,), (3, 4), (2, 6)]
    classes = {}
    tot = 0; qual = 0
    for mods in groups:
        els = list(itertools.product(*[range(m) for m in mods]))
        add = lambda x, y: tuple((p + q) % m for p, q, m in zip(x, y, mods))
        neg = lambda x: tuple((-p) % m for p, m in zip(x, mods))
        mul = lambda n, x: tuple((n * p) % m for p, m in zip(x, mods))
        zero = tuple(0 for _ in mods)
        def gen(gs):
            S = {zero}; fr = [zero]
            while fr:
                nx = []
                for x in fr:
                    for g in gs:
                        y = add(x, g)
                        if y not in S: S.add(y); nx.append(y)
                fr = nx
            return S
        gtot = 0; gq = 0
        for a, b, c, d in itertools.product(els, repeat=4):
            for N in (9, 16):
                M = N // gcd(N, 2)
                delta = add(add(a, d), neg(add(b, c)))
                beta = mul(M, add(add(b, c), neg(mul(2, a))))
                D = gen([delta]); r = len(D)
                s = 1
                while mul(s, beta) not in D: s += 1
                gtot += 1
                if s != 2: continue
                gq += 1
                k = 0; x = zero; b2 = mul(2, beta)
                while x != b2: x = add(x, delta); k += 1
                H = gen([a, d, add(b, c)]); DN = gen([delta, beta])
                key = (mods, r, (k % 2) if r % 2 == 0 else None, len(H) // len(DN))
                classes.setdefault(key, []).append((a, b, c, d, N))
        tot += gtot; qual += gq
        emit({"group": mods, "carriers_enumerated": gtot, "P0_s_eq_2_qualifying": gq})
    emit({"total_enumerated": tot, "total_qualifying_s2": qual, "n_classes": len(classes)})
    summary = []
    for key in sorted(classes, key=lambda z: (len(z[0]), z[0], z[1], -1 if z[2] is None else z[2], z[3])):
        lst = classes[key]
        a, b, c, d, N = lst[rng.randrange(len(lst))]
        res = run_case(key[0], a, b, c, d, N, maxcells, rng)
        res["class_size"] = len(lst)
        emit(res); summary.append(res)
        print(json.dumps({q: res[q] for q in ("group", "gains", "N", "r", "k", "hidx", "n", "E", "P1", "P2", "P3", "P4", "P5", "P6", "dims", "secs")}), flush=True)
    fails = [(x["group"], x["gains"], x["N"], p) for x in summary for p in ("P1", "P2", "P3", "P4", "P5", "P6") if x[p] is False]
    emit({"cases": len(summary), "failed_predicates": fails})
    print("cases", len(summary), "failed", fails)

def run_case(mods, a, b, c, d, N, maxcells, rng):
    t0 = time.time()
    els = list(itertools.product(*[range(m) for m in mods]))
    add = lambda x, y: tuple((p + q) % m for p, q, m in zip(x, y, mods))
    neg = lambda x: tuple((-p) % m for p, m in zip(x, mods))
    mul = lambda n, x: tuple((n * p) % m for p, m in zip(x, mods))
    zero = tuple(0 for _ in mods)
    def gen(gs):
        S = {zero}; fr = [zero]
        while fr:
            nx = []
            for x in fr:
                for g in gs:
                    y = add(x, g)
                    if y not in S: S.add(y); nx.append(y)
            fr = nx
        return S
    M = N // gcd(N, 2)
    delta = add(add(a, d), neg(add(b, c)))
    beta = mul(M, add(add(b, c), neg(mul(2, a))))
    D = gen([delta]); r = len(D)
    s = 1
    while mul(s, beta) not in D: s += 1
    assert s == 2  # P0 per case
    k = 0; x = zero; b2 = mul(2, beta)
    while x != b2: x = add(x, delta); k += 1
    H = gen([a, d, add(b, c)]); DN = sorted(gen([delta, beta]))
    q = len(DN); assert q == 2 * r
    hidx = len(H) // q
    # coset reps of Delta_N in H
    reps = []; seen = set()
    for h in sorted(H):
        if h not in seen:
            reps.append(h); seen |= {add(h, x) for x in DN}
    rep_of = {}
    for h in reps:
        for x in DN: rep_of[add(h, x)] = h
    bd = add(b, neg(d))
    dcos = lambda x: frozenset(add(x, y) for y in D)
    # choose n
    n = 4
    for cand in (5, 6, 7):
        if hidx * (comb(2 * q + cand, cand) - 1) * 2 * hidx * (comb(q + cand, cand) - 1) <= maxcells: n = cand
    def msets(base, maxsize):
        elems = sorted(add(base, x) for x in DN)
        res = [()]
        for sz in range(1, maxsize + 1):
            res += list(itertools.combinations_with_replacement(elems, sz))
        return res
    col = {}
    def idx(rail, m):
        key = (rail, m)
        if key not in col: col[key] = len(col)
        return col[key]
    for h in reps:
        for m in msets(h, n)[1:]: idx('R', m)
        for m in msets(add(h, b), n)[1:]: idx('L', m)
    ncols = len(col)
    tr = lambda g, m: tuple(sorted(add(x, g) for x in m))
    onecos = lambda m: len({dcos(x) for x in m}) <= 1
    rows_all = []; adm_flag = []
    for h in reps:
        MU = msets(h, n); MV = msets(add(h, bd), n)
        for U in MU:
            for V in MV:
                if len(U) + len(V) > n or (not U and not V): continue
                row = {}
                def addc(rail, m, v):
                    if m:
                        j = col[(rail, m)]; row[j] = row.get(j, 0) + v
                addc('R', tuple(sorted(tr(a, U) + tr(c, V))), 1)
                addc('L', tuple(sorted(tr(b, U) + tr(d, V))), 1)
                addc('R', U, -2); addc('L', V, -2)
                rows_all.append(row); adm_flag.append(onecos(U) or onecos(V))
    rows_adm = [rw for rw, f in zip(rows_all, adm_flag) if f]
    size_of = [0] * ncols
    for (rail, m), j in col.items(): size_of[j] = len(m)
    def rank(rows, cols_keep):
        cmap = {j: i for i, j in enumerate(cols_keep)}
        if not cmap or not rows: return 0
        Mx = flint.fmpz_mat(len(rows), len(cmap))
        for i, rw in enumerate(rows):
            for j, v in rw.items():
                if j in cmap: Mx[i, cmap[j]] = v
        return Mx.rank()
    allc = list(range(ncols))
    dims = {}
    rk = {"adm": rank(rows_adm, allc), "all": rank(rows_all, allc)}
    for npr in (n - 1, n - 2, n - 3):
        high = [j for j in allc if size_of[j] > npr]
        for nm, rows in (("adm", rows_adm), ("all", rows_all)):
            dims[f"{nm}_{npr}"] = (ncols - rk[nm]) - (len(high) - rank(rows, high))
    # theorem's functions
    def eps(i, m0):  # m0 multiset (tuple) inside Delta_N
        tot = 0
        for j in range(r):
            g = add(mul(i, beta), mul(j, delta))
            tot += (-1) ** j * m0.count(g)
        return tot
    def fval(kind, m0):
        if kind == "count": return len(m0)
        if kind == "Q": return eps(0, m0) ** 2 + eps(1, m0) ** 2
        if kind == "C": return eps(0, m0) * eps(1, m0)
    def FR(kind, m):
        h = rep_of[m[0]]
        return fval(kind, tr(neg(h), m))
    def vec(kind):
        v = [0] * ncols
        for (rail, m), j in col.items():
            v[j] = FR(kind, m) if rail == 'R' else FR(kind, tr(c, m))
        return v
    kinds = ["count"] + (["Q"] if r % 2 == 0 else []) + (["C"] if (r % 2 == 0 and k % 2 == 0) else [])
    E = len(kinds)
    vecs = {kd: vec(kd) for kd in kinds}
    def satisfies(v, rows):
        bad = 0
        for rw in rows:
            if sum(cf * v[j] for j, cf in rw.items()) != 0: bad += 1
        return bad
    P1 = all(satisfies(vecs[kd], rows_all) == 0 for kd in kinds)
    P2 = all(dims[f"adm_{npr}"] == E for npr in (n - 1, n - 2))
    P3 = all(dims[f"adm_{npr}"] == dims[f"all_{npr}"] for npr in (n - 1, n - 2, n - 3))
    P4 = True
    for npr in (n - 1, n - 2):
        if npr < 2: continue
        low = [j for j in allc if size_of[j] <= npr]
        Mx = flint.fmpz_mat([[vecs[kd][j] for j in low] for kd in kinds])
        if Mx.rank() != E: P4 = False
    P5 = None; p5bad = None
    if r % 2 == 0 and k % 2 == 1:
        p5bad = satisfies(vec("C"), rows_adm)
        P5 = p5bad > 0
    # P6
    P6 = None; p6 = {}
    if r % 2 == 0:
        ok = True
        for _ in range(200):
            W = {g: rng.randint(-5, 5) for g in DN}
            def epsW(i, Wd):
                return sum((-1) ** j * Wd[add(mul(i, beta), mul(j, delta))] for j in range(r))
            TW = {g: W[add(g, neg(beta))] for g in DN}   # (T_beta W)(g)=W(g-beta)
            if epsW(1, TW) != epsW(0, W) or epsW(0, TW) != (-1) ** k * epsW(1, W): ok = False
        # characters of Delta_N: homomorphisms to Z_L (L = exponent), chi(g)=exp(2 pi i phi(g)/L)
        L = 1
        for m_ in mods: L = L * m_ // gcd(L, m_)
        L2 = L if L % 4 == 0 else (2 * L if L % 2 == 0 else 4 * L)
        chars = set()
        for coeffs in itertools.product(*[range(m_) for m_ in mods]):
            phi = lambda g: sum(cf * gi * (L // m_) for cf, gi, m_ in zip(coeffs, g, mods)) % L
            chars.add(tuple(phi(g) for g in DN))
        good = [ch for ch in chars if (ch[DN.index(delta)] * 2) % (2 * L) == L % (2 * L) and L % 2 == 0]
        good = [ch for ch in chars if L % 2 == 0 and ch[DN.index(delta)] == L // 2]
        p6["n_chi"] = len(good)
        if len(good) != 2: ok = False
        for ch in good:
            pb = ch[DN.index(beta)]
            # chi(beta)^2 == (-1)^k  <=> 2*pb == k*L/2 mod L
            if (2 * pb) % L != (k * (L // 2)) % L: ok = False
            # sigma_chi == eps0 + chi(beta) eps1 as identity of functionals: chi(i*beta+j*delta) == chi(beta)^i (-1)^j
            for i in range(2):
                for j in range(r):
                    g = add(mul(i, beta), mul(j, delta))
                    if ch[DN.index(g)] != (i * pb + j * (L // 2)) % L: ok = False
            p6.setdefault("chi_beta_over_L", []).append(str(Fraction(pb, L)))
        P6 = ok
    return {"group": list(mods), "gains": [list(a), list(b), list(c), list(d)], "N": N, "M": M, "delta": list(delta),
            "beta": list(beta), "r": r, "s": s, "k": k, "hidx": hidx, "n": n, "ncols": ncols, "rows_all": len(rows_all),
            "rows_adm": len(rows_adm), "rank": rk, "dims": dims, "E": E, "kinds": kinds, "P1": P1, "P2": P2, "P3": P3,
            "P4": P4, "P5": P5, "P5_violated_rows": p5bad, "P6": P6, "P6_detail": p6, "secs": round(time.time() - t0, 1)}

if __name__ == "__main__":
    main()
