"""Task 1. Polynomial solutions of (V) on C.
Predicates (fixed before run):
 P1a: for each listed vanishing multiset u and each k in {1,2,3,4}, g(t)=t^k, f=g(|a|^2) satisfies (V)
      identically iff k==1.
 P1b: for monomial f=a^j conj(a)^k (j+k<=8), (V) holds identically iff
      (j,k)=(1,1), or (k=0 or j=0) and p_r=0 for 0<r<max(j,k) and p_max(j,k)=m.   [p_r = sum u^r]
 P1c: the full solution space among real polynomials of the form sum_k c_k |a|^(2k), k=1..4 (mixed degrees) is
      one-dimensional (c_2=c_3=c_4=0).
"""
import sympy as sp, itertools, json, os
a,ab,b,bb=sp.symbols('a ab b bb')
def root(q,k): return sp.exp(2*sp.pi*sp.I*sp.Rational(k,q))
def R(q,ks): return [(q,k) for k in ks]
sets={
 'pair(1,-1)':[(2,0),(2,1)],
 'tri':[(3,0),(3,1),(3,2)],
 'sq':[(4,0),(4,1),(4,2),(4,3)],
 'tri x2':[(3,0),(3,0),(3,1),(3,1),(3,2),(3,2)],
 'two pairs 6':[(6,0),(6,3),(6,1),(6,4)],
 'tri+pair':[(6,0),(6,2),(6,4),(6,0),(6,3)],
 'tri+rot pair':[(12,0),(12,4),(12,8),(12,3),(12,9)],
 'pent':[(5,k) for k in range(5)],
 'order30 six':[(30,6),(30,12),(30,18),(30,24),(30,5),(30,25)],
 'oct':[(8,k) for k in range(8)],
}
out={}
allok=True
for name,us in sets.items():
    m=len(us)
    def p(r):
        return sp.nsimplify(sp.simplify(sum(sp.exp(2*sp.pi*sp.I*sp.Rational(k*r,q)) for q,k in us).rewrite(sp.cos)),rational=False)
    import cmath
    def pn(r): return sum(cmath.exp(2j*cmath.pi*k*r/q) for q,k in us)
    assert abs(pn(1))<1e-12
    # work with exact cyclotomic numbers: use common order
    Q=sp.ilcm(*[q for q,_ in us]); z=sp.symbols('z'); Phi=sp.cyclotomic_poly(Q,z)
    def lhs(j,k):
        e=0
        for q,kk in us:
            u=z**(kk*Q//q); ub=z**((Q-kk*Q//q)%Q)
            e+= (a+u*b)**j*(ab+ub*bb)**k
        e=sp.expand(e - m*a**j*ab**k - m*b**j*bb**k)
        P=sp.Poly(e,a,ab,b,bb)
        return [sp.rem(c,Phi,z) for c in P.coeffs()]
    res={}
    for j in range(0,9):
        for k in range(0,9-j):
            if j+k==0: continue
            holds=all(c==0 for c in lhs(j,k))
            mx=max(j,k)
            pred=(j==1 and k==1) or ((j==0 or k==0) and all(abs(pn(r))<1e-9 for r in range(1,mx)) and abs(pn(mx)-m)<1e-9)
            if holds!=pred: allok=False; print('P1b FAIL',name,j,k,holds,pred)
            if holds: res[f'{j},{k}']=True
    # P1c mixed degrees: unknown c1..c4
    cs=sp.symbols('c1:5'); eqs=[]
    for k in range(1,5):
        pass
    tot={}
    M=[]
    for k in range(1,5):
        e=0
        for q,kk in us:
            u=z**(kk*Q//q); ub=z**((Q-kk*Q//q)%Q)
            e+=(a+u*b)**k*(ab+ub*bb)**k
        e=sp.expand(e-m*(a*ab)**k-m*(b*bb)**k)
        P=sp.Poly(e,a,ab,b,bb)
        for mon,c in P.terms():
            c=sp.Poly(sp.rem(c,Phi,z),z)
            for (d,),cc in c.terms():
                tot.setdefault((mon,d),[0]*4)[k-1]=cc
    Mx=sp.Matrix(list(tot.values())) if tot else sp.zeros(1,4)
    dim=4-Mx.rank()
    ns=Mx.nullspace()
    ok=(dim==1 and ns[0][1]==0 and ns[0][2]==0 and ns[0][3]==0)
    if not ok: allok=False; print('P1c FAIL',name,dim)
    out[name]={'m':m,'monomials a^j abar^k satisfying (V)':sorted(res),'dim of span{|a|^2k,k<=4} solutions':dim,'P1c':ok,
               'power sums p1..p8':[str(complex(round(pn(r).real,9),round(pn(r).imag,9))) for r in range(1,9)]}
    print(name,out[name])
out['ALL_PREDICATES_HOLD']=allok
fn='t1_result.json'
assert not os.path.exists(fn)
json.dump(out,open(fn,'w'),indent=1)
print('ALL',allok)
