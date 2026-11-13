"""Exact face-dependent Gram matrices and complete-tomography reference witnesses.
Research direction and responsibility: Kirtus Justus. Vancouver, 7 November 2026.
Requires Python 3, SymPy, NumPy. No measured or simulated trials.
"""
import numpy as np
import sympy as sp
from math import sqrt

I=sp.eye(2)
X=sp.Matrix([[0,1],[1,0]])
Y=sp.Matrix([[0,-sp.I],[sp.I,0]])
Z=sp.diag(1,-1)
kron=sp.kronecker_product
one=sp.eye(4)
ident=sp.eye(16)
ref0=sp.diag(1,0,0,0)


def require(test,reason):
    if not test:
        raise ArithmeticError(reason)


def choi(op):
    return op.reshape(16,1)/2


def projector(v):
    return v*v.H


def partial_out(op):
    return sp.Matrix(4,4,lambda i,j:sum(op[4*a+i,4*a+j] for a in range(4)))


def trprod(x,y):
    return sum(x[i,j]*y[j,i] for i in range(x.rows) for j in range(x.cols))


eta=choi(one)
theta=choi(sp.I*kron(Z,I))
v=choi(sp.I*kron(X,I))
Peta,Ptheta,F=map(projector,(eta,theta,v))
D=ident-Ptheta-Peta-F
axes=(Z,X,Y)
probs=[4*kron(kron((I+axis)/2,I),ref0) for axis in axes]
paulis=[kron(a,b)/2 for a in (I,X,Y,Z) for b in (I,X,Y,Z)][1:]


def exact_gram(sectors):
    B=sum(sectors,sp.zeros(16))
    def center(m):
        out=B*m*B
        return out-sum((trprod(proj,out)*proj/proj.trace() for proj in sectors),sp.zeros(16))
    tensors=[center(kron(one,H)) for H in paulis]
    obs=[center(M) for M in probs]
    Q=sp.Matrix(15,15,lambda i,j:trprod(tensors[i],tensors[j]))
    C=sp.Matrix(15,3,lambda i,j:trprod(tensors[i],obs[j]))
    R=sp.Matrix(3,3,lambda i,j:trprod(obs[i],obs[j]))
    # Remove the span of the marginal constraints. At f=r this span has rank one.
    S=Q.pinv()*C
    reduced=[obs[j]-sum((S[i,j]*tensors[i] for i in range(15)),sp.zeros(16))
             for j in range(3)]
    G=R-C.T*S
    require(all(partial_out(m).is_zero_matrix for m in reduced),'TP tangency')
    require(G==sp.Matrix(3,3,lambda i,j:trprod(reduced[i],reduced[j])),'Gram construction')
    return G,Q,reduced


def numerical_witnesses():
    s=131/320; h=.99; q=81711338569043/224995905216000
    k=(s*h-sqrt(s*h*q))**2/(s*h*(1-h))
    d=s+k; r=1-d
    i=np.eye(2);x=np.array(X,complex)
    def check(U,f):
        require(np.linalg.norm(U.conj().T@U-np.eye(4))<3e-13,'unitarity')
        vec=U.reshape(16)/2
        for K,targ in ((eta,d),(theta,0),(v,f)):
            require(abs(abs(np.vdot(np.array(K,complex).ravel(),vec))**2-targ)<2e-13,'sector weight')
        out=U[:,0].reshape(2,2)
        p0=d+6*(r-f)/13
        require(np.linalg.norm(out@out.conj().T-np.diag([p0,1-p0]))<3e-13,'entire reduced output')
        ref=d*np.array(Peta,complex)+f*np.array(F,complex)+(r-f)*np.array(D,complex)/13
        J=d*d+f*f+(r-f)**2/13
        require(abs(np.vdot(vec,ref@vec)-J)<3e-13,'overlap identity')
    c0=sqrt(d+6*r/13); c1=2*sqrt(d)-c0
    U=np.diag([c0,c1,c1,c0]).astype(complex)
    for a,b,c in [(0,3,c0),(1,2,c1)]:
        U[a,b]=U[b,a]=1j*sqrt(1-c*c)
    check(U,0)
    # Concentrate each spectator group's weights on a single Pauli channel.
    keep=np.array(projector(choi(kron(I,X))),complex)
    flip=np.array(projector(choi(kron(X,X))),complex)
    for f in (0,r/2,r-.01,r):
        ell=r-f
        base=d*np.array(Peta,complex)+f*np.array(F,complex)+ell*np.array(D,complex)/13
        concentrated=d*np.array(Peta,complex)+f*np.array(F,complex)+(ell/13)*(6*keep+7*flip)
        expected=np.diag([d+6*ell/13,1-d-6*ell/13])
        for t in (0,.4,1):
            state=(1-t)*base+t*concentrated
            marginal=np.trace(state.reshape(4,4,4,4),axis1=0,axis2=2)
            require(np.max(np.abs(marginal-np.eye(4)/4))<3e-13,'mixture is trace preserving')
            reduced=4*np.trace(state[::4,::4].reshape(2,2,2,2),axis1=1,axis2=3)
            require(np.linalg.norm(reduced-expected)<3e-13,'three reference outputs')
            J=d*d+f*f+ell*ell/13
            require(abs(np.trace(state@state)-J-t*t*72*ell*ell/169)<3e-13,'reference interval')
    for gamma in (-sqrt(d*r),.19,0.,sqrt(d*r)):
        state=d*np.array(Peta,complex)+r*np.array(F,complex)
        coherence=np.array(eta*v.H+v*eta.H,complex)
        state+=gamma*coherence
        require(np.linalg.eigvalsh(state).min()>-1e-13,'upper endpoint positive')
        marginal=np.trace(state.reshape(4,4,4,4),axis1=0,axis2=2)
        require(np.linalg.norm(marginal-np.eye(4)/4)<3e-13,'upper endpoint CPTP')
        rates=[np.trace(state@np.array(m,complex)).real for m in probs]
        require(np.linalg.norm(np.array(rates)-[d,.5,.5+gamma])<3e-13,'upper endpoint line')
        require(abs(np.trace(state@state)-(d*d+r*r+2*gamma**2))<3e-13,'upper endpoint purity')
    # Solve d*f=(42/169)*(r-f)^2 via the stable smaller-root formula.
    alpha=42/169
    f=2*alpha*r*r/(d+2*alpha*r+sqrt(d*d+4*alpha*d*r))
    U=(sqrt(d)*i+1j*sqrt(f)*x)/sqrt(d+f)
    target=np.array([sqrt(6/13),-1j*sqrt(7/13)])
    col=U.conj().T@target
    col*=np.exp(-1j*np.angle(col[0]))
    N=np.array([[col[0].real,col[1].conjugate()],[col[1],-col[0].real]])
    V=np.kron(U,i)@(sqrt(d+f)*np.eye(4)+1j*sqrt(r-f)*np.kron(N,x))
    check(V,f)
    print('Pure and minimum-purity channels coincide at the three reference rates for f=0 and',
          f'{f:.12f}')


def main():
    cases=[
        ('interior',[Peta,F,D],sp.diag(sp.Rational(1230,91),sp.Rational(97,7),sp.Rational(97,7))),
        ('f=0',[Peta,D],sp.diag(sp.Rational(159,13),sp.Rational(25,2),sp.Rational(254,21))),
        ('f=r',[Peta,F],sp.diag(0,0,sp.Rational(1,2)))]
    for name, sectors, target in cases:
        G,Q,measured=exact_gram(sectors)
        require(G==target,'exact Gram for '+name)
        print(name,'(Z, rotated X, rotated Y)',list(G.diagonal()),'marginal rank',Q.rank())
        if name=='f=0':
            s=131/320; h=.99; q=81711338569043/224995905216000
            k=(s*h-sqrt(s*h*q))**2/(s*h*(1-h))
            d=s+k; r=1-d
            state=d*np.array(Peta,complex)+r*np.array(D,complex)/13
            base=state.copy()
            for j,move in enumerate([.001,.002,-.003]):
                state+=move/float(G[j,j])*np.array(measured[j],complex)
            require(np.linalg.eigvalsh(state).min()>-1e-13,'zero-face interior')
            for j,move in enumerate([.001,.002,-.003]):
                require(abs(np.trace(np.array(probs[j],complex)@(state-base))-move)<1e-13,
                        'zero-face equality shifts')
        if name=='interior':
            s=131/320; h=.99; q=81711338569043/224995905216000
            k=(s*h-sqrt(s*h*q))**2/(s*h*(1-h))
            d=s+k;r=1-d;f=r/2
            A=sqrt(s/d);B=sqrt(k/d)
            shifts=[.005,A*.007+B*(-.004),-B*.007+A*(-.004)]
            base=d*np.array(Peta,complex)+f*np.array(F,complex)+(r-f)*np.array(D,complex)/13
            state=base+sum(float(y/G[j,j])*np.array(m,complex) for j,(y,m) in enumerate(zip(shifts,measured)))
            require(np.linalg.eigvalsh(state).min()>-1e-13,'interior witness positivity')
            purity=np.trace(state@state).real
            require(abs(purity-.336263620116203)<1e-14,'interior purity')
            print('Independent witness purity',format(purity,'.15f'))
    numerical_witnesses()


if __name__=='__main__':
    main()
