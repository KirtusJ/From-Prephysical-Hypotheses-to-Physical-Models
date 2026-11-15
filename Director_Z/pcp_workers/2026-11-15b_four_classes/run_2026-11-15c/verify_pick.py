#!/usr/bin/env python3
"""verify_pick.py OUT LEANOUT PICKFILE...   independent recheck (sympy, not flint) of the Q5 picks of relpick.py.
PREDICATES fixed before the first run:
 V1 each picked relation satisfies cA*prod A - eps*cB*prod B == 0 mod X^S - SIGMA (j = 0), by sympy rem.
 V2 each h0 (sympy, from w-linear factors p^2+q^2+pq w) equals the stored h0 string.
 V3 the sympy gcd of the picked h0 equals m(w) = squarefree part of C_S(w) - 2 SIGMA up to a constant.
 V4 h0 has exact multiplicity 1 at each root of m for at least one picked relation (implied by V3; reported).
Also writes a Lean file stating each relation in a commutative ring with x^S = SIGMA, proved by linear_combination.
Result file opened with mode 'x'.
"""
import sys, json, sympy as sp
out=open(sys.argv[1],'x'); lean=open(sys.argv[2],'x')
X,w=sp.symbols('X w'); res=[]
lean.write('import Mathlib\n\n')
def cheb(n):
    a,b=sp.Integer(2),w
    if n==0: return a
    for _ in range(n-1): a,b=b,sp.expand(w*b-a)
    return b
for fn in sys.argv[3:]:
    d=json.load(open(fn)); S=int(d['argv'][1]); SIG=int(d['argv'][2])
    mf=sp.Poly(cheb(S)-2*SIG,w); m=sp.quo(mf,sp.gcd(mf,mf.diff(w))).monic()
    hs=[]; rows=[]
    for k,p in enumerate(d['Q5_pick']):
        PA=sp.prod([(a+b*X)**e for a,b,e in p['A']]); PB=sp.prod([(a+b*X)**e for a,b,e in p['B']])
        diff=sp.expand(p['cA']*PA-p['eps']*p['cB']*PB)
        Q,R=sp.div(sp.Poly(diff,X),sp.Poly(X**S-SIG,X))
        v1=R.is_zero
        h0=sp.Poly(p['cA']**2*sp.prod([(a*a+b*b+a*b*w)**e for a,b,e in p['A']])-p['cB']**2*sp.prod([(a*a+b*b+a*b*w)**e for a,b,e in p['B']]),w)
        stored=sp.Poly(sp.sympify(p['h0'].replace('^','**').replace('x','w')),w)
        v2=(h0-stored).is_zero
        mult=[]
        for rt in sp.Poly(m,w).all_roots():
            pass
        q,rr=sp.div(h0,m); v4=not sp.div(q,m)[1].is_zero if rr.is_zero else False
        q2=sp.gcd(q,m); v4=sp.degree(q2,w)==0
        hs.append(h0); rows.append(dict(V1=v1,V2=v2,simple_at_all_roots_of_m=v4,degX=sp.degree(diff,X)))
        nm=f"rel_s{S}_{'p' if SIG==1 else 'm'}{k}"
        A='*'.join(f'({a}+({b})*x)^{e}' for a,b,e in p['A']); B='*'.join(f'({a}+({b})*x)^{e}' for a,b,e in p['B'])
        lean.write(f"theorem {nm} (R : Type*) [CommRing R] (x : R) (h : x^{S} = {SIG}) :\n    ({p['cA']}:R)*({A}) = ({p['eps']*p['cB']}:R)*({B}) := by\n  linear_combination ({sp.sstr(Q.as_expr()).replace('**','^').replace('X','x')}) * h\n#print axioms {nm}\n\n")
    G=hs[0]
    for h in hs[1:]: G=sp.gcd(G,h)
    res.append(dict(file=fn,S=S,SIG=SIG,m=str(m.as_expr()),rels=rows,V3=sp.Poly(G,w).monic()==m))
json.dump(res,out,indent=1,default=str); out.close(); lean.close(); print(json.dumps(res,default=str))
