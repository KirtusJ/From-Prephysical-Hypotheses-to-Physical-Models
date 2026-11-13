"""Checks for Paired-Input Constraints on Quantum Channels.
Research direction and responsibility: Kirtus Justus. Vancouver, 7 November 2026.
Requires NumPy and mpmath. All values are mathematical model quantities.
"""
from fractions import Fraction
import numpy as np
import mpmath as mp


def require(value, message):
    if not value:
        raise ArithmeticError(message)


def close(a,b,message):
    require(np.max(np.abs(np.asarray(a)-np.asarray(b))) < 3e-12,message)


def certify_constants():
    iv = mp.iv
    iv.dps = 65
    s = iv.mpf(131)/320
    q = iv.mpf(81711338569043)/224995905216000
    h = iv.mpf(99)/100
    k = (iv.sqrt(q)-iv.sqrt(h*s))**2/(1-h)
    a = s+k+iv.mpf('.06')/13
    beta = 1-(iv.sqrt(iv.mpf('3.92'))-1)**2
    m = a+beta
    c = iv.mpf('.96')
    m1 = (c*iv.sqrt(m)+iv.sqrt(1-c*c)*iv.sqrt(1-m))**2
    t = (2+m+m1)/4
    purity = t*t+(1-t)**2
    distance = (1-m+iv.sqrt((1-m)**2+12*(1-iv.sqrt(m))**2))/8
    H = lambda x: (9+6*x+x*x+(1-x)**2)/16
    spectrum_lower = 1-(1+iv.sqrt(15*(16*H(a+iv.mpf('.04'))-1)))/16
    eps = iv.mpf('.03')
    a_box = (1+iv.sqrt(8*eps**2+(2*a-1+2*eps)**2))/2
    beta_box = iv.mpf('.08')/13+eps
    for label, actual, left, right in [
        ('flip cap',beta,'.0397979746446661','.0397979746446662'),
        ('single-input ceiling',H(m),'.8078263982873538','.8078263982873539'),
        ('neighbor output top eigenvalue bound',m1,'.8246170805237347','.8246170805237348'),
        ('two-input ceiling',purity,'.7428654659689598','.7428654659689599'),
        ('Choi distance lower bound',distance,'.1730027896903658','.1730027896903659'),
        ('purity-only distance at flip cap .04',spectrum_lower,'.1015467670541872','.1015467670541873'),
        ('box purity ceiling',H(a_box+beta_box),'.8236941303189374','.8236941303189375'),
    ]:
        require(actual.a>iv.mpf(left) and actual.b<iv.mpf(right),label)
        print(label, "in", left, right)


def verify_flip_attainment():
    for t in [Fraction(0),Fraction(1,4),Fraction(2,3),Fraction(1)]:
        x=(1-t*t)/(1+t*t)
        y=2*t/(1+t*t)
        beta=y*y
        # K0=diag(x,1,1,1) and K1=y|01><00|. w=Tr((A+D)^*(A+D))/8.
        w=((1+x)**2+4)/8
        require(x*x+y*y==1 and 4*(1-w)==beta+(1-x)**2/2,"flip equality")


def trace_distance(C,P):
    return np.sum(np.abs(np.linalg.eigvalsh(C-P)))/2


def distance_formula(m):
    return (1-m+np.sqrt((1-m)**2+12*(1-np.sqrt(m))**2))/8


def maximum_joint(a,beta):
    b=min(beta,1-beta)
    if b < 1-a:
        v=np.array([np.sqrt(a),0.,0.,np.sqrt(b)])
        Q=np.outer(v,v)+np.diag([0,0,1-a-b,0])
    else:
        fraction=.5 if a==.5 else (a-b)/(2*a-1)
        c=np.sqrt(np.clip(fraction,0,1));s=np.sqrt(max(0.,1-c*c))
        v=np.array([np.sqrt(a)*c,np.sqrt(a)*s,-np.sqrt(1-a)*s,np.sqrt(1-a)*c])
        Q=np.outer(v,v)
    if beta>.5:
        flip=np.kron(np.eye(2),[[0,1],[1,0]])
        Q=flip @ Q @ flip.T
    return Q


def check_distance(a,beta):
    joint=maximum_joint(a,beta)
    lam,vec=np.linalg.eigh(joint)
    idx=np.argsort(lam)[::-1]
    lam,vec=np.maximum(lam[idx],0.),vec[:,idx]
    m=min(1.,a+min(beta,1-beta))
    close(lam[0],m,"joint maximum eigenvalue")
    # U chooses an output eigenbasis. Use those same vectors when extending the isometry.
    U=vec
    kraus=[U @ np.diag([np.sqrt(lam[0]),1,1,1])]
    for j in range(1,4):
        K=np.zeros((4,4),complex);K[:,0]=np.sqrt(lam[j])*vec[:,j];kraus.append(K)
    close(sum(K.conj().T @ K for K in kraus),np.eye(4),"isometry")
    C=sum(np.outer(K.ravel(),K.ravel().conj())/4 for K in kraus)
    P=np.outer(U.ravel(),U.ravel().conj())/4
    output=4*C.reshape(4,4,4,4)[:,0,:,0]
    close(output,joint,"fixed joint output")
    close(np.trace(output.reshape(2,2,2,2),axis1=1,axis2=3),np.diag([a,1-a]),"first output")
    close(np.trace(output.reshape(2,2,2,2),axis1=0,axis2=2)[1,1],beta,"second outcome")
    close(trace_distance(C,P),distance_formula(m),"attained minimum distance")



def check_supplied_reference():
    """Check the paired-input inequalities on the given reference state."""
    s=131/320; h=.99; q=81711338569043/224995905216000
    k=(np.sqrt(q)-np.sqrt(s*h))**2/(1-h)
    d=s+k; residual=.01; f=1-d-residual
    identity=np.eye(2)
    paulis=[identity,np.array([[0,1],[1,0]],complex),
            np.array([[0,-1j],[1j,0]],complex),np.diag([1,-1])]
    u=1j*np.kron(paulis[3],identity)
    v=1j*np.kron(paulis[1],identity)
    # The given rank-one Choi sectors are the normalized vectorizations of these Kraus matrices.
    matrices=[np.sqrt(s)*np.eye(4)-np.sqrt(k)*u, np.sqrt(f)*v]
    for i,P in enumerate(paulis):
        for j,Q in enumerate(paulis):
            if j!=0 or i==2:
                matrices.append(np.sqrt(residual/13)*np.kron(P,Q))
    close(sum(K.conj().T @ K for K in matrices),np.eye(4),"reference trace preservation")
    Choi=sum(np.outer(K.ravel(),K.ravel().conj())/4 for K in matrices)
    V=np.stack(matrices,axis=1)  # output, environment, input
    psi=V[:,:,0]
    flip=np.kron(identity,paulis[1])
    phi=flip @ V[:,:,1]
    weight=sum(np.linalg.norm(K[::2,::2]+K[1::2,1::2])**2/8 for K in matrices)
    delta=sum(np.linalg.norm(K[::2,::2][:,0]-K[1::2,1::2][:,0])**2+
              np.linalg.norm(K[1::2,::2][:,0]-K[::2,1::2][:,0])**2 for K in matrices)
    close(np.linalg.norm(psi-phi)**2,delta,"block comparison identity")
    require(delta<=8*(1-weight)+1e-13,"paired population inequality")
    require(4*weight-3<=np.vdot(psi,phi).real+1e-13,"vector overlap")
    require(np.linalg.eigvalsh(phi@phi.conj().T)[-1]<=.824617080524,"neighbor output bound")
    require(np.trace(Choi@Choi).real<=.742865465969,"paired-input ceiling")

if __name__=='__main__':
    certify_constants()
    verify_flip_attainment()
    check_supplied_reference()
    for a,beta in [(.5,0),(.5,.5),(.8,.1),(.8,.3),(.8,.9),(1.,0),(.5294729345035379,.03979797464466614)]:
        check_distance(a,beta)
    print("Sharp flip equality and distance extremizers passed.")
