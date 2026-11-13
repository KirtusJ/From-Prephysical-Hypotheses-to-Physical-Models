"""Independent explicit trace-preserving Kraus witnesses for regular-simplex marginal states.
No constrained numerical optimizer, symbolic facts checked against direct matrices.
"""
from __future__ import annotations
import numpy as np
from numpy.linalg import norm


def require(ok, message):
    if not ok:
        raise AssertionError(message)


def simplex(q:int):
    # Basis of orthocomplement to uniform vector via QR
    H=np.eye(q)-np.ones((q,q))/q
    # eigen-decomposition, positive eigenspace; rows form isometry
    vals,V=np.linalg.eigh(H)
    B=V[:,1:].conj().T  # q-1 x q, columns simplex points before scaling
    X=np.sqrt(q/(q-1))*B
    return X


def channel(q):
    dprime=q-1
    X=simplex(q)
    roots=np.exp(2j*np.pi*np.arange(q)/q)
    K=np.zeros((dprime*q,q),complex)
    for b in range(q):
        for a in range(dprime):K[a*q+b,b]=roots[b]*X[a,b]
    # orthogonal projection to V⊗I_q
    diagonal=np.stack([K[b::q,b] for b in range(q)],axis=1)
    V=diagonal.mean(axis=1)
    proj=np.kron(V[:,None],np.eye(q))
    score=norm(proj,'fro')**2/norm(K,'fro')**2
    # shift second output flag by 1
    cyclic=np.roll(np.eye(q),1,axis=0)
    Kzero=np.kron(np.eye(dprime),cyclic) @ K
    diagonalzero=np.stack([Kzero[b::q,b] for b in range(q)],axis=1)
    wzero=norm(np.kron(diagonalzero.mean(axis=1)[:,None],np.eye(q)),'fro')**2/norm(Kzero,'fro')**2
    require(np.allclose(K.conj().T@K,np.eye(q),atol=1e-12), "CPTP isometry error")
    require(np.allclose(Kzero.conj().T@Kzero,np.eye(q),atol=1e-12), "zero endpoint isometry error")
    require(np.allclose(X.conj().T@X, (q/(q-1))*np.eye(q)-np.ones((q,q))/(q-1),atol=1e-12), "simplex Gram error")
    require(abs(score-1/(q-1))<1e-12, "optimal local weight error")
    require(wzero<1e-25, "zero-weight endpoint error")
    return score,wzero

if __name__=='__main__':
    import sys
    if '--negative-control' in sys.argv:
        actual,_=channel(3)
        require(abs(actual-0.6)<1e-12, 'deliberately false trine ceiling')
    print('q exact_true pairwise_false numerical_true zero_weight')
    for q in range(2,11):
        actual,zero=channel(q)
        print(f'{q} {1/(q-1):.12f} {2/q:.12f} {actual:.12f} {zero:.4g}')
