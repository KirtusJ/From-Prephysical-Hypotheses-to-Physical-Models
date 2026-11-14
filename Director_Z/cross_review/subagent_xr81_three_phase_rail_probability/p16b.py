"""P16 (post hoc, fixed after run2 before this run): among native third-turn triangles {s,Ts,T^2 s}, T=G D G^-1 (G even word, len<=6),
s an even-word point (len<=6), count those with barycentre exactly 0; group by F2 triangle mean. Predicate: all zero-barycentre
native triangles have the same F2 mean (i.e. F2 invisible to them). Also the ordinary law mean must be 1/2 for all."""
import sys, json
from fractions import Fraction as Q
from itertools import product
from pathlib import Path
def H(s): return (s[2], -s[1], s[0])
def D(s): return ((-s[0]-3*s[1])/2, (s[0]-s[1])/2, s[2])
def word(w, s):
    for c in w:
        s = H(s)
        if c == "1": s = D(s)
    return s
def inv(w, s):
    for c in reversed(w):
        if c == "1": s = D(D(s))
        s = H(s)
    return s
F2 = lambda s: (1+s[2])/2+(1-s[2]**2)/8
pts = {}
for n in (0, 2, 4, 6):
    for b in product("01", repeat=n):
        w = "".join(b); pts.setdefault(word(w, (Q(0), Q(0), Q(1))), w)
means = {}; nq = 0; ordbad = 0
for n in range(0, 7):
    for b in product("01", repeat=n):
        g = "".join(b)
        T = lambda s: word(g, D(inv(g, s)))
        for s, w in pts.items():
            t1 = T(s); t2 = T(t1)
            assert T(t2) == s
            if any(s[k]+t1[k]+t2[k] != 0 for k in range(3)): continue
            nq += 1
            m = (F2(s)+F2(t1)+F2(t2))/3
            ordbad += (s[2]+t1[2]+t2[2]) != 0
            means.setdefault(str(m), []).append((g, w))
out = dict(qualifying=nq, distinct_F2_means={k: dict(count=len(v), example=v[0]) for k, v in means.items()}, ordinary_mean_not_half=ordbad,
           passed=int(len(means) <= 1), failed=int(len(means) > 1))
print(json.dumps(out, indent=1))
with Path(sys.argv[1]).open("x") as f: json.dump(out, f, indent=1, sort_keys=True); f.write("\n")
