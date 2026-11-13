"""Exact model bounds and direct matrix checks.
Kirtus Justus · research direction and responsibility · Vancouver, November 7, 2026.
Use Python 3, NumPy and mpmath. No measurement records are generated.
"""
import mpmath as mp
import numpy as np


def require(condition, description):
    if not condition:
        raise ArithmeticError(description)


def close(actual, expected, description):
    require(np.max(np.abs(np.asarray(actual) - np.asarray(expected))) < 2e-12, description)


def minimum_joint(a, b):
    # The second basis vector denotes its less likely reported outcome.
    x = np.clip((a+b)/2 - 0.25, max(0., a+b-1), min(a,b))
    return np.diag([a-x, x, 1-a-b+x, b-x]).astype(complex)


def maximum_joint(a, b):
    if b < 1-a:
        vector = np.array([np.sqrt(a), 0., 0., np.sqrt(b)])
        return np.outer(vector,vector) + np.diag([0.,0.,1-a-b,0.])
    # Purify the first marginal; rotate the second Schmidt basis.
    fraction = 0.5 if a == 0.5 else (a-b)/(2*a-1)
    c = np.sqrt(np.clip(fraction,0,1))
    s = np.sqrt(max(0.,1-c*c))
    vector = np.array([np.sqrt(a)*c,np.sqrt(a)*s,-np.sqrt(1-a)*s,np.sqrt(1-a)*c])
    return np.outer(vector,vector)


def upper_channel(joint):
    values, vectors = np.linalg.eigh(joint)
    order = np.argsort(values)[::-1]
    values, vectors = np.maximum(values[order],0.), vectors[:,order]
    isometry = np.zeros((4,4,4),complex)
    for j in range(4):
        isometry[:,j,0] = np.sqrt(values[j])*vectors[:,j]
    for j in range(1,4):
        isometry[:,0,j] = vectors[:,j]
    columns = isometry.reshape(16,4)
    close(columns.conj().T @ columns, np.eye(4), "isometry")
    ket = isometry.transpose(1,0,2).reshape(4,16)/2
    return ket.T @ ket.conj()


def lower_channel(joint):
    direct = np.diag([1.,0,0,0])
    return (np.kron(joint,direct)+np.kron(np.eye(4)/4,np.eye(4)-direct))/4


def check_endpoints(a, beta):
    b = min(beta,1-beta)
    m = min(1.,a+b)
    low, high = minimum_joint(a,b), maximum_joint(a,b)
    if beta > 0.5:
        flip = np.kron(np.eye(2),[[0,1],[1,0]])
        low, high = flip @ low @ flip.T, flip @ high @ flip.T
    bounds = [((low @ low).trace().real+0.75)/16,
              (9+6*m+m*m+(1-m)**2)/16]
    for state, joint, expected in zip([lower_channel(low),upper_channel(high)],[low,high],bounds):
        matrix = state.reshape(4,4,4,4)
        close(np.trace(matrix,axis1=0,axis2=2),np.eye(4)/4,"input marginal")
        close(4*matrix[:,0,:,0],joint,"same input output")
        require(np.linalg.eigvalsh(state).min() > -1e-12,"positive Choi matrix")
        out = joint.reshape(2,2,2,2)
        close(np.trace(out,axis1=1,axis2=3),np.diag([a,1-a]),"first marginal")
        close(np.trace(out,axis1=0,axis2=2)[1,1],beta,"second rate")
        close(np.trace(state @ state),expected,"attained bound")
    return bounds


def spectral_constant():
    eye = np.eye(4)
    pauli_x = np.kron([[0,1],[1,0]],np.eye(2))
    p, v = eye.reshape(-1)/2, 1j*pauli_x.reshape(-1)/2
    measured = np.outer(p,p.conj())+np.outer(v,v.conj())
    for axis in [np.array([1,0]),np.array([1,1j])/np.sqrt(2),np.array([3,4])/5]:
        q = np.kron(np.kron(np.outer(axis,axis.conj()),np.eye(2)),np.diag([1,0,0,0]))
        close(np.linalg.eigvalsh(measured @ q @ measured)[-2:],[0,0.25],"principal angles")
        close(np.linalg.eigvalsh(2*measured+4*q)[[0,-1]],[0,3+np.sqrt(3)],"spectral span")


def check_interval():
    iv = mp.iv
    iv.dps=55
    s=iv.mpf(131)/320; h=iv.mpf(99)/100; q=iv.mpf(81711338569043)/224995905216000
    k=(iv.sqrt(s*h)-iv.sqrt(q))**2/(1-h)
    d=s+k; ell=iv.mpf(".01"); f=1-d-ell; a=d+6*ell/13
    def separation(eps):
        e=iv.mpf(eps)
        return 2*(s+f)-1-4*e-(1+iv.sqrt((2*a-1+2*e)**2+8*e**2))/2
    require(separation(".03990195042113343").a>0 and
            separation(".03990195042113345").b<0,"five-rate box crossing")
    m=a+4*ell
    upper=(9+6*m+m**2+(1-m)**2)/16
    require(upper.b < iv.mpf(".807905661518"),"outward upper bound")
    return float(a.mid), float(f.mid), float(d.mid)


if __name__ == "__main__":
    a,f,d=check_interval()
    for av,beta in [(0.5,0.),(.5,.5),(1.,.2),(1.,1.),(.8,.1),(.8,.3),
                    (.8,.9),(a,.04),(a,8*.01/13)]:
        check_endpoints(av,beta)
    spectral_constant()
    w=2*(131/320+f)-1-a
    print("Reference first eigenvalue",f"{a:.15f}")
    print("Two-population gap",f"{w:.15f}")
    print("Half-trace distance certificate",f"{w/(3+np.sqrt(3)):.15f}")
    print("Five-rate box crossing between 0.03990195042113343 and 0.03990195042113345")
    print("Ordinary-detector ceiling with no second-qubit reading",f"{check_endpoints(a,.04)[1]:.15f}")
    print("Model second-qubit probability",f"{8*.01/13:.15f}")
    print("Local-data-only interval",*[f"{x:.15f}" for x in check_endpoints(a,8*.01/13)])
