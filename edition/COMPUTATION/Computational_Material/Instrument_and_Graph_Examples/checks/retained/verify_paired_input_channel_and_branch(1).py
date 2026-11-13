"""Deterministic paired-input audit. No measured or simulated experiments."""
from fractions import Fraction
import hashlib
import numpy as np
import mpmath as mp


def need(ok, desc):
    if not bool(ok):
        raise ArithmeticError(desc)


def local_weight(kraus):
    denom = sum(float(np.vdot(K,K).real) for K in kraus)
    need(denom>0,"Nonzero CP branch")
    local=0.
    for K in kraus:
        a=K[np.ix_([0,2],[0,2])]; d=K[np.ix_([1,3],[1,3])]
        H=(a+d)/2
        local += 2*np.vdot(H,H).real
    return local/denom


def branch_pair(kraus):
    S=sum(float(np.vdot(K,K).real) for K in kraus)
    pp=S/4
    h0=sum(float(np.vdot(K[:,0],K[:,0]).real) for K in kraus)
    h1=sum(float(np.vdot(K[:,1],K[:,1]).real) for K in kraus)
    need(h0>0 and h1>0,"Both input successes positive")
    g0,g1=h0/pp,h1/pp
    w=local_weight(kraus)
    D=np.diag([0,1,0,1]); Flip=np.array([[0,1,0,0],[1,0,0,0],[0,0,0,1],[0,0,1,0]],complex)
    psi=np.concatenate([K[:,0] for K in kraus]); phi=np.concatenate([Flip@K[:,1] for K in kraus])
    delta2=float(np.vdot(psi-phi,psi-phi).real)
    need(delta2 <= 2*S*(1-w)+1e-12, "Paired branch Frobenius inequality")
    c=(g0+g1-8*(1-w))/(2*np.sqrt(g0*g1))
    overlap=np.vdot(psi,phi).real/np.sqrt(h0*h1)
    need(overlap >= c-2e-12,"Overlap certificate")
    need((np.sqrt(g0)-np.sqrt(g1))**2 <=8*(1-w)+1e-12,"Success imbalance")
    if c>=0:
        need(c<=1+1e-12,"Incompatible physical parameters")
        # First-output probabilities, one test basis and any other such effect, cannot exceed global pure-state distance.
        cap=np.sqrt(max(0,1-c*c))
        p0=np.concatenate([K[:,0] for K in kraus]); p1=np.concatenate([K[:,1] for K in kraus]);
        # trace-out only second output, and environment, to obtain first-qubit reduced matrices
        R0=np.zeros((2,2),complex); R1=np.zeros((2,2),complex)
        for K in kraus:
            v0=K[:,0].reshape(2,2); v1=K[:,1].reshape(2,2)
            R0+=v0@v0.conj().T/h0
            R1+=v1@v1.conj().T/h1
        D0=float(sum(abs(np.linalg.eigvalsh(R0-R1)))/2)
        need(D0<=cap+3e-12,"Marginal distance certificate")
    return (w,g0,g1,c,overlap)


def source_constants():
    mp.mp.dps=75
    s=mp.mpf(131)/320; h=mp.mpf(99)/100
    q=mp.mpf(81711338569043)/224995905216000
    k=(mp.sqrt(q)-mp.sqrt(h*s))**2/(1-h)
    ell=mp.mpf('0.01'); d=s+k;f=1-d-ell
    a=d+6*ell/13
    beta=1-(mp.sqrt(mp.mpf('3.92'))-1)**2
    m0=a+beta; c=mp.mpf('.96')
    m1=(c*mp.sqrt(m0)+mp.sqrt(1-c*c)*mp.sqrt(1-m0))**2
    t=(2+m0+m1)/4
    purity=t*t+(1-t)**2
    dist=(1-m0+mp.sqrt((1-m0)**2+12*(1-mp.sqrt(m0))**2))/8
    expectation=mp.sqrt(1-c*c)
    print('Original source file (historical) SHA256: baf12ef1a1abfedb6a6b5bda71419289bdcb45a8407de4f042df3264d7b7b9ee')
    for n,x in [('s',s),('h',h),('q',q),('k',k),('f',f),('first-qubit eigenvalue a',a),('flip beta bound',beta),('reference output max m0',m0),('neighbor output max m1',m1),('Choi max eigenvalue cap',t),('Choi purity ceiling',purity),('half-trace-distance floor',dist),('paired-input click difference cap',expectation)]:
        print(f'{n}: {mp.nstr(x,30)}')
    need(mp.mpf('.8246170805237347')<m1<mp.mpf('.8246170805237348'),'neighbor eigenvalue rounding')
    need(mp.mpf('.7428654659689598')<purity<mp.mpf('.7428654659689599'),'purity rounding')
    need(mp.mpf('.1730027896903658')<dist<mp.mpf('.1730027896903659'),'trace distance rounding')
    return s,h,q,k,f,d


def reference_kraus(s,k,f):
    I=np.eye(2,dtype=complex)
    X=np.array([[0,1],[1,0]],complex)
    Y=np.array([[0,-1j],[1j,0]],complex)
    Z=np.diag([1,-1]).astype(complex)
    out=[np.sqrt(float(s))*np.eye(4)-1j*np.sqrt(float(k))*np.kron(Z,I),1j*np.sqrt(float(f))*np.kron(X,I)]
    for ia,P in enumerate((I,X,Y,Z)):
        for ib,Q in enumerate((I,X,Y,Z)):
            if ib!=0 or ia==2:
                out.append(np.sqrt(.01/13)*np.kron(P,Q))
    need(np.max(np.abs(sum(K.conj().T@K for K in out)-np.eye(4)))<1e-12,'Reference Kraus normalization')
    return out


def branch_nonuniform_check():
    beta=.03
    K0=np.diag([np.sqrt(.8*(1-beta)),np.sqrt(.6),np.sqrt(.8),np.sqrt(.6)]).astype(complex)
    K1=np.zeros((4,4),complex);K1[1,0]=np.sqrt(.8*beta)
    kraus=[K0,K1]
    H=sum(K.conj().T@K for K in kraus)
    need(np.linalg.eigvalsh(H).max()<=1+1e-13,'Branch trace-nonincreasing')
    return branch_pair(kraus)


def main():
    s,h,q,k,f,d=source_constants()
    ref=branch_pair(reference_kraus(s,k,f))
    non=branch_nonuniform_check()
    for label,vals in [('Reference TP example',ref),('Nonuniform branch example',non)]:
        print(label+': w,g0,g1,overlap floor,actual=',','.join(f'{v:.12g}' for v in vals))
    for a,beta in [(0.5,0),(0.5,0.5),(0.8,0.1),(0.8,0.3),(0.8,0.9),(1.,0),(.5294729345035379,.03979797464466614)]:
        distance_witness(a,beta)
    check_randomization_eprocess()
    print('All Kraus, local-distance and optional-stopping checks passed.')


# Extra independent local-output distance witness, executed by a separate command.
def distance_witness(a,beta):
    b=min(beta,1-beta)
    if b<1-a:
        v=np.array([np.sqrt(a),0,0,np.sqrt(b)],complex)
        Omega=np.outer(v,v.conj())+np.diag([0,0,1-a-b,0]).astype(complex)
    else:
        fraction=.5 if abs(a-.5)<1e-14 else (a-b)/(2*a-1)
        c=np.sqrt(np.clip(fraction,0,1));tt=np.sqrt(1-c*c)
        v=np.array([np.sqrt(a)*c,np.sqrt(a)*tt,-np.sqrt(1-a)*tt,np.sqrt(1-a)*c])
        Omega=np.outer(v,v.conj()).astype(complex)
    if beta>.5:
        swap=np.kron(np.eye(2),np.array([[0,1],[1,0]]))
        Omega=swap@Omega@swap
    evals,evecs=np.linalg.eigh(Omega)
    order=np.argsort(evals)[::-1]
    evals=np.maximum(evals[order],0);V=evecs[:,order]
    m=min(1.,a+b)
    need(abs(evals[0]-m)<1e-13,"Output maximum eigenvalue")
    K0=V@np.diag([np.sqrt(evals[0]),1,1,1])
    mats=[K0]
    for j in range(1,4):
        Kj=np.zeros((4,4),complex);Kj[:,0]=np.sqrt(evals[j])*V[:,j];mats.append(Kj)
    need(np.linalg.norm(sum(K.conj().T@K for K in mats)-np.eye(4))<1e-12,"Kraus TP")
    vec=lambda K:K.reshape(16)/2
    C=sum(np.outer(vec(K),vec(K).conj()) for K in mats)
    P=np.outer(vec(V),vec(V).conj())
    dist=sum(abs(np.linalg.eigvalsh(C-P)))/2
    predicted=(1-m+np.sqrt((1-m)**2+12*(1-np.sqrt(m))**2))/8
    need(abs(dist-predicted)<1e-12,"Sharp local distance formula")
    out=4*C.reshape(4,4,4,4)[:,0,:,0]
    need(np.max(abs(out-Omega))<1e-12,"Output matches exactly")
    return dist


def check_randomization_eprocess():
    """Directly optimize a Bernoulli randomized-arm test's conditional mgf, with no sampled trials."""
    import math
    delta=.28
    for lam in (.05,.2,.5,1.0):
        F=(math.exp(lam)+(1-delta)*math.exp(-lam)+delta)/2
        for p1 in np.linspace(0,1,41):
            for p0 in np.linspace(0,min(1,p1+delta),41):
                mgf=(math.exp(lam)*p0+math.exp(-lam)*p1+2-p0-p1)/2
                need(mgf<=F+2e-14,'Conditional e-process mgf violated')
        need(math.log(F)<=lam*delta/2+lam*lam/2+1e-14, 'Exact mgf should not exceed Hoeffding')
    print('Exact Bernoulli randomized-arm e-factor and Hoeffding comparison verified for four positive bets.')

if __name__ == '__main__':
    main()
