#!/usr/bin/env python3
"""bezout_lean.py LEANOUT PICKFILE...  For each pick file with exactly two relations h1, h2: sympy gcdex gives
u1 h1 + u2 h2 = m (monic).  Writes Lean theorems: h_i = m * k_i (divisibility) and u1 h1 + u2 h2 = m, over any field of
characteristic 0.  PREDICATE fixed before the run: B1 gcdex returns exactly m (else the file records FAILED). Lean output
file opened with mode 'x'."""
import sys, json, sympy as sp
w=sp.symbols('w'); L=open(sys.argv[1],'x'); L.write('import Mathlib\n\n')
def cheb(n):
    a,b=sp.Integer(2),w
    if n==0: return a
    for _ in range(n-1): a,b=b,sp.expand(w*b-a)
    return b
st=lambda e: sp.sstr(sp.expand(e)).replace('**','^')
for fn in sys.argv[2:]:
    d=json.load(open(fn)); S=int(d['argv'][1]); SIG=int(d['argv'][2]); tag=f"s{S}{'p' if SIG==1 else 'm'}"
    mf=sp.Poly(cheb(S)-2*SIG,w); m=sp.quo(mf,sp.gcd(mf,mf.diff(w))).monic().as_expr()
    hs=[sp.expand(sp.sympify(p['h0'].replace('^','**').replace('x','w'))) for p in d['Q5_pick']]
    assert len(hs)==2
    u1,u2,g=sp.gcdex(hs[0],hs[1],w)
    ok=sp.expand(g-m)==0
    print(fn,'B1',ok)
    if not ok: L.write(f'-- FAILED {fn}\n'); continue
    for i,h in enumerate(hs):
        k=sp.quo(h,m,w)
        L.write(f"theorem div_{tag}_{i} (R : Type*) [Field R] [CharZero R] (w : R) :\n    {st(h)} = ({st(m)})*({st(k)}) := by ring\n#print axioms div_{tag}_{i}\n\n")
    L.write(f"theorem bez_{tag} (R : Type*) [Field R] [CharZero R] (w : R) (h1 h2 : R)\n    (e1 : h1 = {st(hs[0])}) (e2 : h2 = {st(hs[1])}) :\n    ({st(u1)})*h1 + ({st(u2)})*h2 = {st(m)} := by\n  rw [e1, e2]; ring\n#print axioms bez_{tag}\n\n")
L.close()
