"""Exact mixed-state primal/dual witness, boundary stability test and rational Bayes-risk enclosures."""
from decimal import Decimal, localcontext
from fractions import Fraction as F
import sympy as sp


def require(test,message):
    if not test:raise ArithmeticError(message)


def mixed_trine():
    q=3
    vectors=[sp.Matrix([1,0]),sp.Matrix([-1,sp.sqrt(3)])/2,sp.Matrix([-1,-sp.sqrt(3)])/2]
    rays=[v*v.H for v in vectors]
    amp=[(sp.eye(2)+2*p)/sp.sqrt(10) for p in rays]
    tau=[a*a.H for a in amp]
    require(tau[0]*tau[1]!=tau[1]*tau[0],'noncommutation')
    C=6/sp.sqrt(10)
    require(sum(amp,sp.zeros(2))==C*sp.eye(2),'sum of amplitudes')
    dual=[C*a.inv() for a in amp]
    require((sum((y.inv() for y in dual),sp.zeros(2))-sp.eye(2)).applyfunc(sp.simplify)==sp.zeros(2),'inverse sum')
    slack=sp.diag(*dual)-sp.kronecker_product(sp.ones(q),sp.eye(2))
    require(slack.applyfunc(sp.simplify).is_positive_semidefinite,'dual slack')
    upper=sp.simplify(sum(sp.trace(y*t) for y,t in zip(dual,tau)))
    lower=sp.simplify(sp.trace(sum(amp,sp.zeros(2))**2))
    require(upper==lower==sp.Rational(36,5),'joint certificates')
    # Isometry columns use output flags; coefficient index is the environment.
    K=[sp.zeros(6,3) for _ in range(2)]
    for b,a in enumerate(amp):
        for o in range(2):
            for e in range(2):K[e][o*q+b,b]=a[o,e]
    def wt(ops):
        total=sum(sp.trace(k.H*k) for k in ops)
        local=0
        for k in ops:
            v=sum((k[b::q,b] for b in range(q)),sp.zeros(2,1))/q
            local+=q*(v.H*v)[0]
        return sp.simplify(local/total)
    require((sum((k.H*k for k in K),sp.zeros(3))-sp.eye(3)).applyfunc(sp.simplify)==sp.zeros(3),'TP')
    shift=sp.Matrix(q,q,lambda i,j:int(i==(j+1)%q))
    K0=[sp.kronecker_product(sp.eye(2),shift)*k for k in K]
    for ops in (K,K0):
        for b,t in enumerate(tau):
            out=sum((k[:,b]*k[:,b].H for k in ops),sp.zeros(6))
            marg=sp.Matrix(2,2,lambda i,j:sum(out[q*i+f,q*j+f] for f in range(q)))
            require((marg-t).applyfunc(sp.simplify)==sp.zeros(2),'marginal')
    require(wt(K)==sp.Rational(4,5) and wt(K0)==0,'endpoints')
    print('Mixed noncommuting trine: exact primal=dual=36/5, CPTP interval [0,4/5].')
    # Compare the pure trine (ceiling 1/2) with the mixed trine (4/5).
    # A common output rotation and common success rescaling leave each ceiling fixed.
    rotate=sp.diag(1,sp.I)
    rotated=[rotate*t*rotate.H/2 for t in tau]
    B=sum(sp.sqrt(sp.trace(a*b)*2) for a,b in zip(rays,rotated))/3
    D=sum(sp.sqrt(2*sp.trace((a-2*b)**2)) for a,b in zip(rays,rotated))/3
    # Each single-block difference is traceless and 2 by 2.
    require(sp.simplify(1-B**2-sp.Rational(9,100))>=0,'fidelity stability comparison')
    require(sp.simplify(D*(1-D/4)-(1-B**2))>=0,'normalized trace discrepancy comparison')
    print('Verified normalized stability inequalities for noncommuting, unequally scaled tables.')


def stability_boundary():
    # With one fixed pure state and a mixture initially supported on the other ray,
    # the binary fidelity is sqrt(epsilon) and normalized trace discrepancy epsilon.
    x=sp.symbols('x',real=True,positive=True)
    eps=x*x
    change=x/2
    require(sp.limit(change/eps,x,0,dir='+')==sp.oo,'no linear bound at the singular boundary')
    print('Fixed-success binary boundary: normalized trace discrepancy epsilon; weight change sqrt(epsilon)/2.')


def bounds(N, t, L, stop):
    # Avoid the small probability of zero successes: scale all weights to w[0]=1.
    w=F(1); total=F(0); risk=F(0); tie=F(1); error=F(1,2)
    for m in range(stop+1):
        if m%2: error-=(F(1,2)-L)*tie
        elif m:
            k=m//2; tie*=F((2*k)*(2*k-1),k*k)*L*(1-L)
        total+=w; risk+=w*error
        w*=F(N-m,m+1)*t/(1-t)
    next_ratio=F(N-stop-1,stop+2)*t/(1-t)
    require(0<=next_ratio<1,'tail not decreasing')
    tail=w/(1-next_ratio)
    return risk/(total+tail),(risk+tail/2)/total,tail/total


def power():
    with localcontext() as ctx:
        ctx.prec=40
        for L,den,N in [(F(1,5),1000,7065),(F(1,5),2000,14131),(F(9,20),2000,540254)]:
            for n in (N-1,N):
                lo,hi,tail=bounds(n,F(1,den),L,760 if den==2000 and L==F(9,20) else 100)
                require(lo>F(1,20) if n<N else hi<F(1,20),'wrong side of threshold')
                if L==F(9,20):require(tail<F(14,10**132),'narrow-detector omitted mass')
                approx=Decimal(lo.numerator)/Decimal(lo.denominator)
                print(f'L={L}; informative success=1/{den}; N={n}; risk approximately {approx:.15f}; rational comparison verified.')


if __name__=='__main__':
    mixed_trine()
    stability_boundary()
    power()
