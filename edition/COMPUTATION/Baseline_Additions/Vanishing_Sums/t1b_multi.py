"""Task 1 (multi-embedding form used in the proof). V = C^2 (two embeddings sigma_1, sigma_s), P = g(t1,t2), t_j=|x_j|^2,
g polynomial of degree <=3 without constant term.  PREDICATE P1d: solution space of (V) is exactly span{t1,t2}."""
import sympy as sp, itertools, json, os
z=sp.symbols('z'); x1,y1,x2,y2,b1,c1,b2,c2=sp.symbols('x1 y1 x2 y2 b1 c1 b2 c2')  # y=conj x, c = conj b
cases={'q5 pentagon':(5,2,[0,1,2,3,4]),'q8 octagon':(8,3,list(range(8))),'q8 square':(8,3,[0,2,4,6]),'q12 square':(12,5,[0,3,6,9]),'q10 two pairs':(10,3,[0,5,1,6])}
out={}
for name,(q,s,ks) in cases.items():
    Phi=sp.cyclotomic_poly(q,z); m=len(ks)
    mons=[(i,j) for i in range(4) for j in range(4) if 1<=i+j<=3]
    cols=[]
    for (i,j) in mons:
        g=lambda X1,Y1,X2,Y2:(X1*Y1)**i*(X2*Y2)**j
        e=sum(g(x1+z**k*b1, y1+z**((q-k)%q)*c1, x2+z**(k*s%q)*b2, y2+z**((q-k*s)%q)*c2) for k in ks)-m*g(x1,y1,x2,y2)-m*g(b1,c1,b2,c2)
        P=sp.Poly(sp.expand(e),x1,y1,x2,y2,b1,c1,b2,c2)
        d={}
        for mon,c in P.terms():
            for (dg,),cc in sp.Poly(sp.rem(c,Phi,z),z).terms(): d[(mon,dg)]=cc
        cols.append(d)
    keys=sorted(set().union(*cols),key=str)
    M=sp.Matrix([[d.get(k,0) for d in cols] for k in keys])
    ns=M.nullspace()
    ok=len(ns)==2 and all(all(v[t]==0 for t,(i,j) in enumerate(mons) if i+j!=1) for v in ns)
    out[name]={'dim':len(ns),'P1d':bool(ok)}; print(name,out[name])
assert not os.path.exists('t1b_result.json'); json.dump(out,open('t1b_result.json','w'))
