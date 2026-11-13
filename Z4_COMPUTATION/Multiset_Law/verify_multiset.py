"""Predicate program for the multiset block law (theorem_multiset.tex).

Setting: C = C_q, exponents mod q; a matrix B is a d x d array of exponents; chi^j(B_zy) = zeta^(j*B_zy).
Unknowns: F(m) for all multisets m over C_q of size <= N.  Equations: every instance of
    sum_z F(sum_y B_zy.m_y) = d sum_y F(m_y)   with  sum_y |m_y| <= N.
nullity(B,N) = number of unknowns minus exact rank over Q (flint fmpz_mat.rank), cross-checked by ranks
modulo the primes 1000003 and 998244353.

Prediction, computed from characters only, in exact arithmetic (polynomials modulo the cyclotomic polynomial),
without using the simplification made in the paper:
    pred(B) = #{ j mod q : zeta^(j*B_zy) = 1 for all z,y }
            + #{ (j,l), 0 <= j <= l < q : sum_z zeta^(j*B_zy + l*B_zy') = d*delta_{yy'} for all y,y' }.

PREDICATES (fixed before the first run; a failure is recorded, not edited away).
 H   (hypothesis, reported per matrix, never assumed): is_block = [B^(1)* B^(1) = d I];  generates = [entries generate C_q].
     The theorem claims P1 for EVERY matrix, block or not; the corollary P2 only where is_block and generates hold.
 P1  For every matrix in the lists LISTED (>= 10 blocks of the request), CONTROLS (non-blocks) and RANDOM
     (seed 20261113), and every N with 2 <= N <= Nmax(B):  nullity(B,N) == pred(B), and the three ranks agree.
 P2  For every matrix with is_block and generates:  pred(B) == 1 + #{ classes {j,-j} : B^(j)* B^(j) = d I },
     and every j coprime to q has B^(j)* B^(j) = d I.  The number of qualifying matrices is reported.
 P3  (search, reporting predicate) Over all dephased blocks (first row and column 0, rows in increasing order)
     in the ranges SEARCH, count those with some j, not coprime to q and not 0 mod q, with B^(j)* B^(j) = d I,
     split by whether the dephased core generates C_q.  At least one matrix B with entries generating C_q, is_block,
     and such a j must be exhibited and must pass P1; otherwise P3 is recorded as "none found in range".
 P4  Each CONTROL has is_block False (the control is what it says it is).
Result file: verify_multiset_result.json; the program refuses to overwrite it.
"""
import itertools, json, os, random, sys, math
from flint import fmpz_mat, nmod_mat, fmpz_poly

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "verify_multiset_result.json")
PRIMES = (1000003, 998244353)

# ---------- exact cyclotomic arithmetic ----------
_phi = {}
def is_zero_sum(counts, q):
    """sum_e counts[e] zeta_q^e == 0, exactly."""
    if q not in _phi: _phi[q] = fmpz_poly.cyclotomic(q)
    p = fmpz_poly([int(c) for c in counts])
    return (p % _phi[q]) == fmpz_poly([0]) if q > 1 else sum(counts) == 0

def gram_ok(B, q, j, l):
    """sum_z zeta^(j B_zy + l B_zy') == d delta_{yy'} for all y,y'."""
    d = len(B)
    for y in range(d):
        for y2 in range(d):
            c = [0]*q
            for z in range(d): c[(j*B[z][y] + l*B[z][y2]) % q] += 1
            if y == y2: c[0] -= d
            if not is_zero_sum(c, q): return False
    return True

def J0(B, q): return [j for j in range(q) if all((j*e) % q == 0 for r in B for e in r)]
def U(B, q): return [j for j in range(q) if gram_ok(B, q, j, (-j) % q)]
def pred(B, q):
    lin = len(J0(B, q))
    quad = sum(1 for j in range(q) for l in range(j, q) if gram_ok(B, q, j, l))
    return lin, quad
def generates(B, q):
    g = q
    for r in B:
        for e in r: g = math.gcd(g, e)
    return g == 1

# ---------- the linear system ----------
def comps(q, N):
    out = []
    for tot in range(N+1):
        for c in itertools.combinations_with_replacement(range(q), tot):
            v = [0]*q
            for g in c: v[g] += 1
            out.append(tuple(v))
    return out
def shift(m, k, q): return tuple(m[(g-k) % q] for g in range(q))

def nullity(B, q, N):
    d = len(B); vs = comps(q, N); idx = {v: i for i, v in enumerate(vs)}
    size = [sum(v) for v in vs]
    rows = set()
    def rec(y, left, chosen):
        if y == d:
            row = {}
            for z in range(d):
                o = [0]*q
                for yy in range(d):
                    s = shift(chosen[yy], B[z][yy], q)
                    for g in range(q): o[g] += s[g]
                i = idx[tuple(o)]; row[i] = row.get(i, 0) + 1
            for yy in range(d):
                i = idx[chosen[yy]]; row[i] = row.get(i, 0) - d
            r = tuple(sorted((i, c) for i, c in row.items() if c))
            if r: rows.add(r)
            return
        for v, s in zip(vs, size):
            if s > left: break
            rec(y+1, left-s, chosen+[v])
    rec(0, N, [])
    rows = sorted(rows)
    n = len(vs)
    if not rows: return n, n, [n, n], len(rows)
    M = fmpz_mat(len(rows), n)
    for a, r in enumerate(rows):
        for i, c in r: M[a, i] = c
    rq = M.rank()
    rp = []
    for p in PRIMES:
        Mp = nmod_mat(len(rows), n, p)
        for a, r in enumerate(rows):
            for i, c in r: Mp[a, i] = c % p
        rp.append(n - Mp.rank())
    return n, n - rq, rp, len(rows)

def nmax(q, d):
    k = q*d
    return 5 if k <= 8 else 4 if k <= 18 else 3

# ---------- matrices ----------
H4 = [[0,0,0,0],[0,1,0,1],[0,0,1,1],[0,1,1,0]]
def scale(B, s): return [[s*e for e in r] for r in B]
LISTED = [
 ("H2 over C2", 2, [[0,0],[0,1]]),
 ("Fourier3 over C3", 3, [[0,0,0],[0,1,2],[0,2,1]]),
 ("Fourier3 in subgroup of C6", 6, [[0,0,0],[0,2,4],[0,4,2]]),
 ("Fourier3 with a column negated, generating C6", 6, [[0,0,3],[0,2,1],[0,4,5]]),
 ("real Hadamard 4 over C2", 2, H4),
 ("real Hadamard 4 in C4", 4, scale(H4, 2)),
 ("Butson 4 over C4, generating", 4, [[0,0,0,0],[0,2,1,3],[0,2,3,1],[0,0,2,2]]),
 ("Fourier4 over C4", 4, [[(z*y) % 4 for y in range(4)] for z in range(4)]),
 ("[[1,i],[1,-i]] over C4", 4, [[0,1],[0,3]]),
 ("H2 in C4", 4, [[0,0],[0,2]]),
 ("H2 in C6", 6, [[0,0],[0,3]]),
 ("H2 in C8", 8, [[0,0],[0,4]]),
 ("H2 phased, generating C6", 6, [[0,1],[0,4]]),
 ("H2 phased rows and columns, C6", 6, [[2,1],[5,1]]),
]
CONTROLS = [
 ("all ones d=2 over C2", 2, [[0,0],[0,0]]),
 ("[[1,1],[1,w]] over C3", 3, [[0,0],[0,1]]),
 ("[[1,1],[1,i]] over C4", 4, [[0,0],[0,1]]),
 ("[[1,i],[1,i]] over C4", 4, [[0,1],[0,1]]),
 ("rank one 3x3 over C3", 3, [[0,1,2],[0,1,2],[0,1,2]]),
 ("3x3 over C2 (no real Hadamard of order 3)", 2, [[0,0,0],[0,1,0],[0,0,1]]),
 ("[[1,1],[1,-1]] with one entry w, C6", 6, [[0,0],[2,3]]),
 ("all ones d=3 over C1", 1, [[0,0,0],[0,0,0],[0,0,0]]),
]
SEARCH = [(2,q) for q in range(2,13)] + [(3,q) for q in (3,6,9,12)] + [(4,2),(4,4),(4,6),(4,8),(5,5),(5,10),(6,3),(6,4),(6,6)]

def search(d, q, cap=200000):
    """dephased blocks: first row and column zero, remaining rows strictly increasing."""
    cands = []
    for t in itertools.product(range(q), repeat=d-1):
        c = [0]*q; c[0] += 1
        for e in t: c[e] += 1
        if is_zero_sum(c, q): cands.append((0,)+t)
    def orth(a, b):
        c = [0]*q
        for x, y in zip(a, b): c[(x-y) % q] += 1
        return is_zero_sum(c, q)
    comp = {i: [k for k in range(i+1, len(cands)) if orth(cands[i], cands[k])] for i in range(len(cands))}
    found = []; trunc = False
    def rec(rows, allowed):
        nonlocal trunc
        if trunc: return
        if len(rows) == d-1:
            found.append([[0]*d] + [list(cands[i]) for i in rows])
            if len(found) >= cap: trunc = True
            return
        for i in allowed:
            rec(rows+[i], [k for k in comp[i] if k in aset(allowed)])
    cache = {}
    def aset(a):
        k = id(a)
        if k not in cache: cache[k] = (a, set(a))
        return cache[k][1]
    rec([], list(range(len(cands))))
    return found, trunc

def main():
    if os.path.exists(OUT):
        print("refusing to overwrite", OUT); sys.exit(1)
    res = {"predicates": {}, "listed": [], "controls": [], "random": [], "search": [], "failures": []}
    fail = res["failures"]

    def run(name, q, B, bucket):
        d = len(B)
        isb = gram_ok(B, q, 1, q-1 if q > 1 else 0); gen = generates(B, q)
        lin, quad = pred(B, q); u = U(B, q)
        rec = {"name": name, "q": q, "d": d, "B": B, "is_block": isb, "generates": gen,
               "pred_linear": lin, "pred_quadratic": quad, "pred": lin+quad, "J0": J0(B, q), "U": u, "N": []}
        for N in range(2, nmax(q, d)+1):
            n, nq, np_, neq = nullity(B, q, N)
            ok = (nq == lin+quad) and all(x == nq for x in np_)
            rec["N"].append({"N": N, "unknowns": n, "equations": neq, "nullity_Q": nq, "nullity_mod_p": np_, "P1": ok})
            if not ok: fail.append({"predicate": "P1", "name": name, "N": N, "nullity": nq, "pred": lin+quad})
        if isb and gen:
            classes = len({min(j, (-j) % q) for j in u})
            units_ok = all(j in u for j in range(q) if math.gcd(j, q) == 1)
            ok2 = (lin+quad == 1+classes) and units_ok
            rec["P2"] = ok2; rec["classes"] = classes
            if not ok2: fail.append({"predicate": "P2", "name": name})
        res[bucket].append(rec)
        print(f"{bucket:8s} {name:48s} q={q} d={d} block={isb!s:5} gen={gen!s:5} pred={lin}+{quad} "
              f"null={[x['nullity_Q'] for x in rec['N']]} P1={all(x['P1'] for x in rec['N'])}", flush=True)
        return rec

    for name, q, B in LISTED: run(name, q, B, "listed")
    for name, q, B in CONTROLS:
        r = run(name, q, B, "controls")
        if r["is_block"]: fail.append({"predicate": "P4", "name": name})
    rng = random.Random(20261113)
    for k in range(40):
        q = rng.choice([2,3,4,5,6]); d = rng.choice([2,2,3])
        B = [[rng.randrange(q) for _ in range(d)] for _ in range(d)]
        run(f"random {k}", q, B, "random")

    # P3 search
    exhibited = None
    for d, q in SEARCH:
        found, trunc = search(d, q)
        extra_gen = extra_sub = 0; ex = None
        for B in found:
            u = U(B, q)
            nonunit = [j for j in u if j % q != 0 and math.gcd(j, q) != 1]
            if nonunit:
                if generates(B, q):
                    extra_gen += 1
                    if ex is None: ex = (B, nonunit)
                else:
                    extra_sub += 1
                    if ex is None: ex = (B, nonunit)
        res["search"].append({"d": d, "q": q, "dephased_blocks": len(found), "truncated": trunc,
                              "with_nonunit_j_core_generates": extra_gen, "with_nonunit_j_core_in_subgroup": extra_sub,
                              "example": ex})
        print(f"search d={d} q={q}: blocks={len(found)} trunc={trunc} nonunit-j: core generates {extra_gen}, core in subgroup {extra_sub}, ex={ex}", flush=True)
    # exhibited matrix for P3: a listed block that generates and has a non-unit j in U
    for r in res["listed"]:
        nonunit = [j for j in r["U"] if j % r["q"] != 0 and math.gcd(j, r["q"]) != 1]
        if r["is_block"] and r["generates"] and nonunit and all(x["P1"] for x in r["N"]):
            exhibited = {"name": r["name"], "B": r["B"], "q": r["q"], "nonunit_j": nonunit}; break
    res["predicates"]["P3_exhibited"] = exhibited
    if exhibited is None: fail.append({"predicate": "P3", "note": "none found in range"})

    allrec = res["listed"] + res["controls"] + res["random"]
    res["predicates"]["H_counts"] = {
        "matrices": len(allrec), "is_block": sum(r["is_block"] for r in allrec),
        "block_and_generates (qualify for P2)": sum(r["is_block"] and r["generates"] for r in allrec),
        "listed_blocks": sum(r["is_block"] for r in res["listed"]),
        "random_blocks": sum(r["is_block"] for r in res["random"])}
    res["predicates"]["P1_instances"] = sum(len(r["N"]) for r in allrec)
    res["predicates"]["P1_pass"] = sum(x["P1"] for r in allrec for x in r["N"])
    res["predicates"]["P2_qualifying"] = sum("P2" in r for r in allrec)
    res["predicates"]["P2_pass"] = sum(r.get("P2", False) for r in allrec)
    res["predicates"]["P4_pass"] = all(not r["is_block"] for r in res["controls"])
    with open(OUT, "x") as f: json.dump(res, f, indent=1, sort_keys=True)
    print(json.dumps(res["predicates"], indent=1)); print("failures:", fail)

if __name__ == "__main__":
    main()
