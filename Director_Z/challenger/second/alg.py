import sympy as sp
r=sp.symbols('r')
for k in range(1,13):
    P=r**(k+1)-(k+1)*r+k; Ps=k*r**(k+1)-(k+1)*r**k+1
    Q=sum((i+1)*r**(k-1-i) for i in range(k)); Qs=sum((i+1)*r**i for i in range(k))
    assert sp.expand(P-(r-1)**2*Q)==0 and sp.expand(Ps-(r-1)**2*Qs)==0
    g=sp.gcd(sp.Poly(Q,r),sp.Poly(Qs,r)); res=sp.resultant(Q,Qs,r)
    U,V,gg=sp.gcdex(Q,Qs,r)
    assert sp.expand(U*Q+V*Qs-1)==0
    # P*(rho) identity mod P
    rem=sp.rem(sp.expand(r*Ps-k*(k+1)*(r-1)**2),P,r)
    print(k,g.degree(),res,rem)
# elimination check, symbolic d
d,X,Y,fa,fb,fk=sp.symbols('d X Y fa fb fk')
k=d-2
sol=sp.solve([X+(d-1)*Y-d*fa-d*(d-1)*fb, Y+(d-1)*X-d*fk-d*(d-1)*fb],[X,Y])
print(sp.simplify(k*sol[Y]+fk-(k+1)*fa-k*(k+1)*fb))
