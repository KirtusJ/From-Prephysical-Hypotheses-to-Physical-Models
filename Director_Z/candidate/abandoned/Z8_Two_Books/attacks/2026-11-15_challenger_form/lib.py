"""Shared exact arithmetic for the Z8 challenger programs (own code; function/ not read).
Carrier (S1): vertices (x,s), s=0 rail R, s=1 rail L. Right step from (x,s) -> (x+1,R) sign +1.
Left step -> (x-1,L), sign -1 iff s==L (a left step that follows a left step). Start (0,R).
State = dict vertex -> (eps, n). H = sum_{eps!=0} eps^2/W * log n.
sign_lin decides the sign of sum c_i log n_i (c_i rational) exactly: reduce to integer exponents k_p of primes,
zero iff all k_p = 0 (unique factorization), else compare prod p^k (k>0) with prod p^-k (k<0) as integers.
If the integers would exceed BITLIM bits, fall back to 80-digit Decimal logs (counted in FALLBACK)."""
from fractions import Fraction as F
from math import gcd, log
from functools import reduce, lru_cache
from decimal import Decimal, getcontext
getcontext().prec = 80
BITLIM = 3_000_000
FALLBACK = [0]
MINABS = [None]
@lru_cache(None)
def factor(n):
    f = {}; p = 2
    while p * p <= n:
        while n % p == 0: f[p] = f.get(p, 0) + 1; n //= p
        p += 1
    if n > 1: f[n] = f.get(n, 0) + 1
    return tuple(f.items())
@lru_cache(None)
def dln(p): return Decimal(p).ln()
def sign_lin(terms):
    L = reduce(lambda a, b: a * b // gcd(a, b), [c.denominator for c, _ in terms], 1)
    k = {}
    for c, n in terms:
        assert n >= 1
        ci = int(c * L)
        for p, a in factor(n): k[p] = k.get(p, 0) + ci * a
    k = {p: v for p, v in k.items() if v}
    if not k: return 0
    g = reduce(gcd, [abs(v) for v in k.values()])
    k = {p: v // g for p, v in k.items()}
    bits = sum(abs(v) * log(p, 2) for p, v in k.items())
    if bits > BITLIM:
        FALLBACK[0] += 1
        val = sum(Decimal(v) * dln(p) for p, v in k.items())
        scale = sum(abs(Decimal(v)) * dln(p) for p, v in k.items())
        rel = abs(val) / scale
        if MINABS[0] is None or rel < MINABS[0]: MINABS[0] = rel
        assert rel > Decimal(10) ** -60, "undecided"
        return 1 if val > 0 else -1
    pos = neg = 1
    for p, v in k.items():
        if v > 0: pos *= p ** v
        else: neg *= p ** (-v)
    return (pos > neg) - (pos < neg)
def Hterms(st, w=lambda e, n: e * e):
    W = sum(w(e, n) for e, n in st.values())
    return [(F(w(e, n), W), n) for e, n in st.values() if w(e, n) != 0]
def neg(t): return [(-c, n) for c, n in t]
def Hfloat(st, w=lambda e, n: e * e):
    return float(sum(c * F(log(n)).limit_denominator(10**15) for c, n in Hterms(st, w))) if st else None
def Hval(st, w=lambda e, n: e * e):
    return sum(float(c) * log(n) for c, n in Hterms(st, w))
def step(st, N, mask=None):
    """one step; N=None is the line; mask = set of admitted sites or None (free)"""
    out = {}
    for (x, s), (e, n) in st.items():
        for (y, t, sg) in ((x + 1, 0, 1), (x - 1, 1, -1 if s == 1 else 1)):
            if N: y %= N
            if mask is not None and y not in mask: continue
            a, b = out.get((y, t), (0, 0))
            out[(y, t)] = (a + sg * e, b + n)
    return out
def mstep(st, N, mask=None):
    """mirror carrier: walks END at a pinned vertex; prepend a step. New start (x,s) precedes (x+1,R) and (x-1,L).
    sign of the prepended step is -1 iff it is a left step from rail L."""
    out = {}
    for (y, t), (e, n) in st.items():
        x = y - 1 if t == 0 else y + 1
        if N: x %= N
        if mask is not None and x not in mask: continue
        for s in (0, 1):
            sg = -1 if (s == 1 and t == 1) else 1
            a, b = out.get((x, s), (0, 0))
            out[(x, s)] = (a + sg * e, b + n)
    return out
def key(st): return tuple(sorted(st.items()))
def subsets(sites):
    sites = sorted(sites)
    for m in range(1, 1 << len(sites)):
        yield frozenset(s for i, s in enumerate(sites) if m >> i & 1)
def events(N, Tmax, stepf=step):
    """all mask sequences, masks = non-empty subsets of the sites reachable at that step (so no empty events).
    yields (T, masks, state)."""
    st0 = {(0, 0): (1, 1)}
    stack = [(0, (), st0)]
    while stack:
        T, ms, st = stack.pop()
        yield T, ms, st
        if T == Tmax: continue
        full = stepf(st, N)
        for m in subsets({x for x, _ in full}):
            stack.append((T + 1, ms + (tuple(sorted(m)),), {v: d for v, d in full.items() if v[0] in m}))
