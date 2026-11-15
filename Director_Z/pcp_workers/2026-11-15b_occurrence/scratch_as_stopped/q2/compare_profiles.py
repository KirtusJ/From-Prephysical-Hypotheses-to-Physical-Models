#!/usr/bin/env python3
"""compare_profiles.py SEENFILE [SEENFILE ...]  -- Q2 comparison: profiles seen against profiles allowed.

Reads files written by enum_profiles (header gives M, B, K, closed).  For each, computes the allowed set:
all w=(v_0,u_0,v_1,u_1,...) of non-negative integers, first non-zero entry at index 0 or 1, last entry non-zero,
total <= B, at most K levels (len <= 2K), for which the array (w_{c-2i}) is totally non-negative, DECIDED BY the
criterion of cor:tp(ii),(iii) in exact arithmetic (sympy gcd, square-free parts, real-root counts, rational
isolating intervals):  one rail empty: the other polynomial has only real roots; both non-empty: g=gcd(u,v)
real-rooted, u/g and v/g square-free, real-rooted, roots alternating in decreasing order beginning with v/g.

PREDICATES (fixed before the first run):
 P0 control: #allowed(B=9,K=4)=550 and #allowed(B=7,K=7)=228 (the draft's numbers).
 P1 necessity: seen subset of allowed.  Hypothesis (profile from an event) holds for every seen profile; count reported.
 P2 sufficiency in bounds: allowed subset of seen.  Only meaningful if the search closed; hypothesis 'closed' is reported.
    Every allowed profile not seen is kept in the result file.
 P3 criterion against minors (window rows i=0..4, all columns that meet the support):
    P3a every allowed w has all minors of order <=3 in the window >= 0;
    P3b every w rejected by the root criterion has a negative minor of order <=4 in the window (those without: kept);
 No randomness. Result file compare_<stem>.json, never overwritten.
"""
import sys, json, os, itertools
from sympy import Poly, symbols, gcd, ZZ, QQ, Rational
z = symbols('z')

def real_rooted(p):
    if p.degree() <= 0: return True
    for f, m in p.sqf_list()[1]:
        if f.count_roots() != f.degree(): return False
    return True

def allowed_root(w):
    v = [int(x) for x in w[0::2]]; u = [int(x) for x in w[1::2]]
    pu = Poly(list(reversed(u)) or [0], z, domain=QQ); pv = Poly(list(reversed(v)) or [0], z, domain=QQ)
    if pu.is_zero: return real_rooted(pv)
    if pv.is_zero: return real_rooted(pu)
    g = pu.gcd(pv)
    if not real_rooted(g): return False
    a = pu.quo(g); b = pv.quo(g)          # a = u/g, b = v/g
    for p in (a, b):
        if p.degree() > 0 and (p.gcd(p.diff()).degree() > 0 or p.count_roots() != p.degree()): return False
    da, db = a.degree(), b.degree()
    if not (db == da or db == da + 1): return False
    if da + db == 0: return True
    prod = a * b
    ivs = prod.intervals(eps=Rational(1, 10**6))
    owners = []
    for (lo, hi), mult in ivs:
        if lo == hi: isb = (b.eval(lo) == 0)
        else:
            sb = b.eval(lo) * b.eval(hi); sa = a.eval(lo) * a.eval(hi)
            assert (sb < 0) != (sa < 0), (w, lo, hi)
            isb = sb < 0
        owners.append('v' if isb else 'u')
    owners.reverse()                         # decreasing order
    return all(o == ('v' if k % 2 == 0 else 'u') for k, o in enumerate(owners))

def det(m):
    n = len(m)
    if n == 1: return m[0][0]
    if n == 2: return m[0][0]*m[1][1]-m[0][1]*m[1][0]
    return sum((-1)**j * m[0][j] * det([r[:j]+r[j+1:] for r in m[1:]]) for j in range(n) if m[0][j])

def neg_minor(w, kmax, R=5):
    n = len(w); C = n + 2*(R-1)
    A = [[(w[c-2*i] if 0 <= c-2*i < n else 0) for c in range(C)] for i in range(R)]
    for k in range(2, kmax+1):
        for rows in itertools.combinations(range(R), k):
            for cols in itertools.combinations(range(C), k):
                if det([[A[i][c] for c in cols] for i in rows]) < 0: return (k, rows, cols)
    return None

def candidates(B, K):
    out = []
    def rec(w, tot):
        if w and w[-1] > 0 and (w[0] > 0 or (len(w) > 1 and w[1] > 0)): out.append(tuple(w))
        if len(w) >= 2*K: return
        for x in range(0, B - tot + 1):
            if len(w) == 1 and w[0] == 0 and x == 0: continue
            rec(w + [x], tot + x)
    rec([], 0)
    return out

def no_internal_zero(seq):
    nz = [i for i, x in enumerate(seq) if x]
    return not nz or all(seq[i] for i in range(nz[0], nz[-1]+1))

def allowed_set(B, K, stats):
    al = []; rej = []
    for w in candidates(B, K):
        stats['candidates'] += 1
        # cheap necessary filter (order-2 minors within one rail: no internal zeros, log-concavity)
        v = w[0::2]; u = w[1::2]
        ok = no_internal_zero(v) and no_internal_zero(u) and all(s[i]*s[i] >= s[i-1]*s[i+1] for s in (u, v) for i in range(1, len(s)-1))
        if not ok: stats['prefiltered'] += 1; continue
        (al if allowed_root(w) else rej).append(w)
    return al, rej

def main():
    res = {}
    st = {'candidates': 0, 'prefiltered': 0}
    c1, _ = allowed_set(9, 4, st); c2, _ = allowed_set(7, 7, st)
    res['P0'] = {'allowed_B9_K4': len(c1), 'allowed_B7_K7': len(c2), 'pass': len(c1) == 550 and len(c2) == 228}
    print('P0', res['P0'])
    for fn in sys.argv[1:]:
        stem = os.path.basename(fn)[:-4]; out = 'compare_' + stem + '.json'
        if os.path.exists(out): print('refuse to overwrite', out); sys.exit(3)
        lines = open(fn).read().split('\n'); hdr = dict(kv.split('=') for kv in lines[0][2:].split())
        M, B, K, closed = int(hdr['M']), int(hdr['B']), int(hdr['K']), hdr['closed'] == '1'
        seen = set(tuple(int(x) for x in l.split()) for l in lines[2:] if l.strip())
        st = {'candidates': 0, 'prefiltered': 0}
        al, rej = allowed_set(B, K, st); als = set(al)
        p3a_fail = [w for w in al if neg_minor(w, 3) is not None]
        p3b_nowit = [w for w in rej if neg_minor(w, 4) is None]
        r = {'file': fn, 'header': hdr, 'M': M, 'B': B, 'K': K, 'closed': closed, 'seen': len(seen), 'allowed': len(al),
             'candidates': st['candidates'], 'prefiltered_by_order2': st['prefiltered'], 'root_rejected': len(rej),
             'P1_seen_not_allowed': sorted(seen - als), 'P1_pass': not (seen - als), 'P1_hypothesis_holds_for': len(seen),
             'P2_allowed_not_seen': sorted(als - seen), 'P2_pass': closed and not (als - seen), 'P2_hypothesis_closed': closed,
             'P3a_allowed_with_negative_minor_order_le3': p3a_fail, 'P3b_root_rejected_without_negative_minor_order_le4': p3b_nowit,
             'P3_pass': not p3a_fail and not p3b_nowit}
        json.dump(r, open(out, 'x'), indent=0)
        print(stem, {k: r[k] for k in ('closed', 'seen', 'allowed', 'P1_pass', 'P2_pass', 'P3_pass')}, 'not seen:', len(als - seen), 'P3b no witness:', len(p3b_nowit))
main()
