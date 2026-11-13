"""Check analytic Hölder stability corollary in commuting, explicitly-solvable examples.
All assertions use require(), active with Python -O and -OO.
"""
import numpy as np

def require(cond, msg):
    if not cond:raise RuntimeError(msg)

def commuting_T(tau):
    # tau shape (d, q, k) nonnegative diagonal matrices
    return sum(np.sum(np.square(np.sum(np.sqrt(arr),axis=0))) for arr in tau)

def run():
    rng=np.random.default_rng(20261107)
    maxima=[]
    for j in range(300):
        d=int(rng.integers(1,5));q=int(rng.integers(2,8));k=int(rng.integers(1,5))
        A=rng.random((d,q,k))
        B=rng.random((d,q,k))
        # make all arms have <=1 success
        A=A/(np.maximum(1, A.sum(axis=2,keepdims=True)))
        B=B/(np.maximum(1, B.sum(axis=2,keepdims=True)))
        for lam in [0.00001,0.001,0.1,1.0]:
            C=(1-lam)*A+lam*B
            S=A.sum();Sp=C.sum();delta=np.abs(A-C).sum()
            M=commuting_T(A);Mp=commuting_T(C)
            w=M/(q*S);wp=Mp/(q*Sp)
            bound=((np.sqrt(S)+np.sqrt(Sp))*np.sqrt(delta)+delta)/min(S,Sp)
            require(abs(w-wp)<=bound+1e-12, 'stability inequality violated')
            require(-1e-12 <= w <=1+1e-12,'invalid local weight')
            maxima.append(abs(w-wp)/bound if bound>0 else 0)
    print('commuting examples tested',len(maxima))
    print('all direct stability checks passed')
    print('max observed ratio of difference to conservative upper bound',f'{max(maxima):.8f}')

if __name__=='__main__':run()
