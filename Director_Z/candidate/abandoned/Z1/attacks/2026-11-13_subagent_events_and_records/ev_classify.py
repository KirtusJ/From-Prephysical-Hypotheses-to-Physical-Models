#!/usr/bin/env python3
"""ev_classify.py -- attack on S2 and S3 of candidate model Z1 (instance Z1-R, the signed ring).

Carrier: vertices (x,R),(x,L); arcs from either to (x+1,R) and (x-1,L); gain -1 on (x,L)->(x-1,L),
+1 otherwise; start (0,R). N=None means a ring so long that nothing wraps (the model's "ring of 16");
N=3 is the wrapping ring of 3 sites. A walk of length t is a word of t moves; 2^t walks.

Rule class: mu(S) = sum over records k of F_k(multiset of symbols of the walks of S with record k),
F_k(empty)=0. The unknowns are the values F_k(m) on the multisets that occur.
  records: 'vertex' = (x, rail) [the model, S3]; 'pos' = x only; 'arc' = (x, rail, previous rail).
  symbol : 'gain' [the model]; 'gainprev' = (gain, previous rail).
  mode   : 'per' = a separate function at each record; 'uni' = the function may depend on the rails
           in the record but not on x.
Consistency equation for an event S of length t: mu(Ext S) - 2 mu(S) = 0.
It is imposed ONLY for S in a family of events, lengths 0..T (Ext S has length up to T+1):
  all    : every non-empty subset (the model's S2), T<=4 exhaustively
  a      : end-vertex events, S = all walks of length t ending in a set Y of vertices
  apos   : the same with sets of positions
  b1     : one read: all walks of length t whose vertex at one time s<=t lies in a set A
  b1pos  : the same, positions
  b2     : two reads at times s1<s2<=t
  b      : product events: vertex at every time s<=t in a prescribed set A_s (T<=4)
  bpos   : product events with sets of positions (T<=5)
  bs     : product events where each read prescribes one vertex or nothing
  c      : cylinders: all walks of length t with one prescribed initial segment of length k<=t
Reported for each run: number of unknowns n, exact rank, nullity; which model vectors (count |m|,
square (sum of gains)^2, and x|m| where x is in the record) satisfy all equations, and the rank of
their span; extra = nullity - that rank; and the same after projection onto the unknowns that
first occur at length <= t0 (t0 = 1,2,3) ("rules on short events that extend consistently to T+1").
Exactness: integer matrices, python-flint fmpz_mat rref and nullspace; the nullspace of a row subset
is verified against every equation with exact integer arithmetic (overflow guard stated in code).

PREDICATES, fixed before the first run (a failed predicate is kept and followed up):
 P1  all, vertex/gain, uni, N=None, T=4: projected (t0=2) dimension = 2 and projected extra = 0.
 P2  all, vertex/gain, per, N=None, T=4: projected (t0=2) extra = 0 with model span of dimension 3
     (count, x*count, square): x*count is consistent on the unwrapped line because a_{x+1}+a_{x-1}=2a_x.
 P3  all, vertex/gain, per, N=3,    T=4: projected (t0=2) dimension = 2.
 P4  family a  (vertex/gain, uni, N=None, T=5): extra > 0 (the classification fails).
 P5  family c  (same): extra > 0.
 P6  family b  (same, T=4): projected (t0=2) extra = 0 (the model's classification survives). UNCERTAIN.
 P7  family bpos (same, T=5): projected (t0=2) extra = 0. UNCERTAIN.
 P8  records 'pos', gain, all, T=4: the square (sum of gains at the position)^2 is NOT consistent, and
     the projected (t0=2) dimension = 1 (count only) in mode uni.
 P9  records 'arc', gain, all, T=4: the square is NOT consistent; projected (t0=2) dimension = 1 in mode uni.
 P10 records 'vertex', symbol 'gainprev', all, T=4, uni: projected (t0=2) dimension = 2 (no new rule).
The result file is not overwritten.

FOLLOW-UP fixed after the smoke run (M17, M18; file smoke_M17_M18.json), before the predicate runs:
the smoke run showed that at lengths <= 2 only one-element multisets occur, on which count and square
coincide, so the "dimension" parts of P1, P3, P8, P9, P10 at t0=2 are mis-specified (they will fail
for that reason and are kept). The comparison that is used is: projected extra at t0 = 1, 2, 3
(dimension of consistent rules beyond the model's own vectors) and the projected dimension at t0=3.
"""
import sys, json, os, random, itertools, time
from collections import Counter
import numpy as np
import flint

SEED = 20261113
HERE = os.path.dirname(os.path.abspath(__file__))

# ---------------------------------------------------------------- walks
def walk_data(tmax, N):
    """D[t][i] = (xs, rails, gain); bit k of i is move k+1 (1 = R). Child of i at t+1: i and i|1<<t."""
    D = []
    for t in range(tmax + 1):
        L = []
        for i in range(1 << t):
            x, r, g = 0, 'R', 1
            xs, rs = [0], ['R']
            for k in range(t):
                mv = 'R' if (i >> k) & 1 else 'L'
                if r == 'L' and mv == 'L':
                    g = -g
                x += 1 if mv == 'R' else -1
                r = mv
                xs.append(x if N is None else x % N); rs.append(r)
            L.append((xs, rs, g))
        D.append(L)
    return D

def rec_key(w, t, rec):
    xs, rs, g = w
    pr = rs[t - 1] if t >= 1 else '0'
    if rec == 'vertex': return (xs[t], rs[t])
    if rec == 'pos':    return (xs[t],)
    if rec == 'arc':    return (xs[t], rs[t], pr)
    raise ValueError
def sym_of(w, t, sym):
    xs, rs, g = w
    pr = rs[t - 1] if t >= 1 else '0'
    return g if sym == 'gain' else (g, pr)

# ---------------------------------------------------------------- families
def masks_by(D, t, s, what):
    """dict value -> mask of walks of length t whose vertex/position at time s is value."""
    out = {}
    for i, (xs, rs, g) in enumerate(D[t]):
        v = (xs[s], rs[s]) if what == 'vertex' else xs[s]
        out[v] = out.get(v, 0) | (1 << i)
    return out

def subsets_or(masks):
    ms = list(masks)
    res = [0]
    for m in ms:
        res += [r | m for r in res]
    return res  # includes 0

def family(D, name, t):
    full = (1 << (1 << t)) - 1
    if t == 0:
        return {1}
    if name == 'all':
        return range(1, full + 1)
    if name in ('a', 'apos'):
        return set(subsets_or(masks_by(D, t, t, 'vertex' if name == 'a' else 'pos').values())) - {0}
    if name in ('b1', 'b1pos'):
        out = set()
        for s in range(1, t + 1):
            out |= set(subsets_or(masks_by(D, t, s, 'vertex' if name == 'b1' else 'pos').values()))
        return out - {0}
    if name == 'b2':
        out = set()
        for s1 in range(1, t + 1):
            A = subsets_or(masks_by(D, t, s1, 'vertex').values())
            out |= set(A)
            for s2 in range(s1 + 1, t + 1):
                B = subsets_or(masks_by(D, t, s2, 'vertex').values())
                out |= {a & b for a in A for b in B}
        return out - {0}
    if name in ('b', 'bpos', 'bs'):
        what = 'pos' if name == 'bpos' else 'vertex'
        cur = {full}
        for s in range(1, t + 1):
            if name == 'bs':
                opts = list(masks_by(D, t, s, what).values()) + [full]
            else:
                opts = subsets_or(masks_by(D, t, s, what).values())
            cur = {a & b for a in cur for b in opts}
        return cur - {0}
    if name == 'c':
        out = set()
        for k in range(0, t + 1):
            for p in range(1 << k):
                m = 0
                for i in range(1 << t):
                    if i & ((1 << k) - 1) == p:
                        m |= 1 << i
                out.add(m)
        return out
    raise ValueError(name)

# ---------------------------------------------------------------- equations
class System:
    def __init__(self, D, rec, sym, mode):
        self.D, self.rec, self.sym, self.mode = D, rec, sym, mode
        self.unk = {}       # (reduced key, multiset) -> index
        self.level = []     # first length at which the unknown occurs
        self.fullkeys = []  # one example of the full key, for model vectors using x
        self.rows = {}      # frozenset(items) -> None
        self.nevents = 0
        self.cls = {}
    def classes(self, t):
        if t not in self.cls:
            ids, L = {}, []
            for i, w in enumerate(self.D[t]):
                c0 = self.D[t + 1][i]; c1 = self.D[t + 1][i | (1 << t)]
                k = (rec_key(w, t, self.rec), sym_of(w, t, self.sym),
                     rec_key(c0, t + 1, self.rec), sym_of(c0, t + 1, self.sym),
                     rec_key(c1, t + 1, self.rec), sym_of(c1, t + 1, self.sym))
                L.append(ids.setdefault(k, len(ids)))
            self.cls[t] = (L, {v: k for k, v in ids.items()})
        return self.cls[t]
    def red(self, key):
        if self.mode == 'per': return key
        return key[1:]
    def uidx(self, key, cnt, t):
        u = (self.red(key), tuple(sorted(cnt.items(), key=repr)))
        j = self.unk.get(u)
        if j is None:
            j = len(self.unk); self.unk[u] = j; self.level.append(t); self.fullkeys.append(key)
        else:
            if t < self.level[j]: self.level[j] = t
        return j
    def add_family(self, name, t):
        L, inv = self.classes(t)
        seen = set()
        for S in family(self.D, name, t):
            self.nevents += 1
            sig = Counter()
            m = S
            while m:
                low = m & -m
                sig[L[low.bit_length() - 1]] += 1
                m ^= low
            fs = frozenset(sig.items())
            if fs in seen: continue
            seen.add(fs)
            at, at1 = {}, {}
            for c, n in sig.items():
                k, s, k0, s0, k1, s1 = inv[c]
                at.setdefault(k, Counter())[s] += n
                at1.setdefault(k0, Counter())[s0] += n
                at1.setdefault(k1, Counter())[s1] += n
            row = Counter()
            for k, cnt in at.items():  row[self.uidx(k, cnt, t)] -= 2
            for k, cnt in at1.items(): row[self.uidx(k, cnt, t + 1)] += 1
            row = {j: v for j, v in row.items() if v}
            if row: self.rows[frozenset(row.items())] = None
    # model vectors
    def vec(self, which):
        v = [0] * len(self.unk)
        for (rk, ms), j in self.unk.items():
            n = sum(c for s, c in ms)
            sg = sum((s if self.sym == 'gain' else s[0]) * c for s, c in ms)
            if which == 'count': v[j] = n
            elif which == 'square': v[j] = sg * sg
            elif which == 'xcount': v[j] = self.fullkeys[j][0] * n
            elif which == 'n2': v[j] = n * n
            elif which == 'sum': v[j] = sg
            elif which == 'occupied': v[j] = 1
            elif which == 'nsum': v[j] = n * sg
            elif which == 'pm': v[j] = (n + sg) * (n - sg) // 4
            elif which == 's4': v[j] = sg ** 4
            elif which == 'abs': v[j] = abs(sg)
            elif which == 'sqprev':   # sum over previous rail of squared partial sums (gainprev only)
                p = Counter()
                for s, c in ms: p[s[1]] += s[0] * c
                v[j] = sum(a * a for a in p.values())
            elif which == 'crossprev':
                p = Counter()
                for s, c in ms: p[s[1]] += s[0] * c
                v[j] = p.get('R', 0) * p.get('L', 0)
            elif which == 'countprevR':
                v[j] = sum(c for s, c in ms if s[1] == 'R')
            else: raise ValueError
        return v

def dense(rows, n):
    A = np.zeros((len(rows), n), dtype=np.int64)
    for i, r in enumerate(rows):
        for j, v in r: A[i, j] = v
    return A

def solve(rows, n):
    """Exact nullspace of the system. rows: list of frozenset((col, val)). Returns list of integer vectors."""
    rows = list(rows)
    random.Random(SEED).shuffle(rows)
    chunk = max(2 * n, 400)
    basis = np.zeros((0, n), dtype=object)
    pos = 0
    def absorb(batch):
        nonlocal basis
        A = dense(batch, n).astype(object)
        M = flint.fmpz_mat(np.vstack([basis, A]).tolist()) if len(basis) else flint.fmpz_mat(A.tolist())
        R, den, rk = M.rref()
        basis = np.array([[int(R[i, j]) for j in range(n)] for i in range(rk)], dtype=object).reshape(rk, n)
    while True:
        # absorb chunks until the rank is stable for one chunk (or rows exhausted)
        while pos < len(rows):
            r0 = len(basis)
            absorb(rows[pos:pos + chunk]); pos += chunk
            if len(basis) == r0 or len(basis) == n: break
        if len(basis) == n: return []
        Nm, k = flint.fmpz_mat(basis.tolist()).nullspace() if len(basis) else (None, n)
        if len(basis) == 0:
            NS = np.eye(n, dtype=object)
        else:
            NS = np.array([[int(Nm[i, j]) for j in range(k)] for i in range(n)], dtype=object)
        # verify every equation exactly. int64 is used only if |entries| * (row 1-norm bound) < 2^62.
        mx = max((abs(int(x)) for x in NS.flat), default=0)
        maxrow = max((sum(abs(v) for j, v in r) for r in rows), default=0)
        fast = mx * maxrow < 2 ** 62
        NSf = NS.astype(np.int64) if fast else NS
        bad = []
        for a in range(0, len(rows), 4000):
            A = dense(rows[a:a + 4000], n)
            if not fast: A = A.astype(object)
            P = A @ NSf
            nz = np.nonzero(np.array(P != 0, dtype=bool).any(axis=1))[0]
            bad += [rows[a + int(i)] for i in nz]
        if not bad:
            return [[int(NS[i, j]) for i in range(n)] for j in range(k)]
        absorb(bad[:chunk])   # failing equations are added and the nullspace recomputed

def rank_of(vectors, idx=None):
    if not vectors: return 0
    M = [[v[i] for i in (idx if idx is not None else range(len(vectors[0])))] for v in vectors]
    if not M[0]: return 0
    return flint.fmpz_mat(M).rank()

def satisfies(rows, v):
    return all(sum(v[j] * c for j, c in r) == 0 for r in rows)

def run(tag, fam, rec, sym, mode, N, T, D):
    t0 = time.time()
    S = System(D, rec, sym, mode)
    for t in range(0, T + 1):
        S.add_family(fam, t)
    n = len(S.unk); rows = list(S.rows)
    NS = solve(rows, n)
    names = ['count', 'square', 'n2', 'sum', 'occupied', 'nsum', 'pm', 's4', 'abs']
    if mode == 'per': names.append('xcount')
    if sym == 'gainprev': names += ['sqprev', 'crossprev', 'countprevR']
    ok = {nm: satisfies(rows, S.vec(nm)) for nm in names}
    model = [S.vec(nm) for nm in ('count', 'square', 'xcount') if ok.get(nm)]
    res = dict(tag=tag, family=fam, records=rec, symbol=sym, mode=mode, N=N, T=T,
               events=S.nevents, equations=len(rows), unknowns=n, rank=n - len(NS), nullity=len(NS),
               candidate_rules_consistent=ok, model_span=rank_of(model),
               extra=len(NS) - rank_of(model), projected={}, seconds=None)
    for t0_ in (1, 2, 3):
        idx = [j for j in range(n) if S.level[j] <= t0_]
        res['projected'][str(t0_)] = dict(unknowns=len(idx), dim=rank_of(NS, idx),
                                          model_span=rank_of(model, idx),
                                          extra=rank_of(NS, idx) - rank_of(model, idx))
    res['seconds'] = round(time.time() - t0, 1)
    return res, S, NS

RUNS = [
    # tag, family, records, symbol, mode, N, T
    ('P1',  'all', 'vertex', 'gain', 'uni', None, 4),
    ('P2',  'all', 'vertex', 'gain', 'per', None, 4),
    ('P3',  'all', 'vertex', 'gain', 'per', 3, 4),
    ('P4',  'a',   'vertex', 'gain', 'uni', None, 5),
    ('P5',  'c',   'vertex', 'gain', 'uni', None, 5),
    ('P6',  'b',   'vertex', 'gain', 'uni', None, 4),
    ('P7',  'bpos','vertex', 'gain', 'uni', None, 5),
    ('P8',  'all', 'pos',    'gain', 'uni', None, 4),
    ('P9',  'all', 'arc',    'gain', 'uni', None, 4),
    ('P10', 'all', 'vertex', 'gainprev', 'uni', None, 4),
    # further families and modes, no predicate fixed (reported as measured)
    ('M1',  'apos','vertex', 'gain', 'uni', None, 5),
    ('M2',  'b1',  'vertex', 'gain', 'uni', None, 5),
    ('M3',  'b1pos','vertex','gain', 'uni', None, 5),
    ('M4',  'b2',  'vertex', 'gain', 'uni', None, 5),
    ('M5',  'bs',  'vertex', 'gain', 'uni', None, 5),
    ('M6',  'a',   'vertex', 'gain', 'per', None, 5),
    ('M7',  'c',   'vertex', 'gain', 'per', None, 5),
    ('M8',  'b',   'vertex', 'gain', 'per', None, 4),
    ('M9',  'bpos','vertex', 'gain', 'per', None, 5),
    ('M10', 'b',   'vertex', 'gain', 'per', 3, 4),
    ('M11', 'all', 'pos',    'gain', 'per', None, 4),
    ('M12', 'all', 'arc',    'gain', 'per', None, 4),
    ('M13', 'all', 'vertex', 'gainprev', 'per', None, 4),
    ('M14', 'all', 'pos',    'gain', 'per', 3, 4),
    ('M15', 'all', 'arc',    'gain', 'per', 3, 4),
    ('M16', 'all', 'vertex', 'gainprev', 'per', 3, 4),
    ('M17', 'all', 'vertex', 'gain', 'uni', None, 3),
    ('M18', 'b',   'vertex', 'gain', 'uni', None, 3),
    ('M19', 'bpos','vertex', 'gain', 'uni', None, 4),
    ('M20', 'all', 'pos',    'gainprev', 'uni', None, 4),
]

def main():
    out = os.path.join(HERE, sys.argv[1] if len(sys.argv) > 1 else 'ev_classify_results.json')
    if os.path.exists(out):
        sys.exit('result file exists, not overwritten: ' + out)
    only = sys.argv[2].split(',') if len(sys.argv) > 2 else None
    Dc = {}
    results = []
    for tag, fam, rec, sym, mode, N, T in RUNS:
        if only and tag not in only: continue
        if N not in Dc: Dc[N] = walk_data(7, N)
        r, S, NS = run(tag, fam, rec, sym, mode, N, T, Dc[N])
        results.append(r)
        print(json.dumps(r), flush=True)
    by = {r['tag']: r for r in results}
    def P(tag, cond, text):
        if tag in by:
            return dict(predicate=tag, text=text, passed=bool(cond(by[tag])))
    preds = [
        P('P1', lambda r: r['projected']['2']['dim'] == 2 and r['projected']['2']['extra'] == 0, 'all/uni: projected dim 2, extra 0'),
        P('P2', lambda r: r['projected']['2']['extra'] == 0 and r['model_span'] == 3, 'all/per/unwrapped: model span 3, projected extra 0'),
        P('P3', lambda r: r['projected']['2']['dim'] == 2, 'all/per/N=3: projected dim 2'),
        P('P4', lambda r: r['extra'] > 0, 'family a: extra > 0'),
        P('P5', lambda r: r['extra'] > 0, 'family c: extra > 0'),
        P('P6', lambda r: r['projected']['2']['extra'] == 0, 'family b: projected extra 0'),
        P('P7', lambda r: r['projected']['2']['extra'] == 0, 'family bpos: projected extra 0'),
        P('P8', lambda r: (not r['candidate_rules_consistent']['square']) and r['projected']['2']['dim'] == 1, 'records pos: square inconsistent, projected dim 1'),
        P('P9', lambda r: (not r['candidate_rules_consistent']['square']) and r['projected']['2']['dim'] == 1, 'records arc: square inconsistent, projected dim 1'),
        P('P10', lambda r: r['projected']['2']['dim'] == 2, 'vertex/gainprev: projected dim 2'),
    ]
    preds = [p for p in preds if p]
    for p in preds: print(p)
    with open(out, 'x') as f:
        json.dump(dict(seed=SEED, results=results, predicates=preds), f, indent=1)

if __name__ == '__main__':
    main()
