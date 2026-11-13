"""Check four prescribed first-qubit marginals using a common Kraus dilation."""
import numpy as np

def check(ok,message):
    if not ok:
        raise ArithmeticError(message)

def hermitian_root(rho):
    vals,vecs=np.linalg.eigh(rho)
    check(np.min(vals)>-1e-13,'input positivity')
    return (vecs*np.sqrt(np.maximum(vals,0)))@vecs.conj().T

def witness(states):
    kraus=np.zeros((4,4,4),complex)
    overlaps=[]
    for pair in range(2):
        i=2*pair
        left,right=[hermitian_root(state) for state in states[i:i+2]]
        U,singular,Vh=np.linalg.svd(left@right)
        aligned=right@Vh.conj().T@U.conj().T
        overlaps.append(singular.sum())
        for bit,factor in enumerate((left,aligned)):
            for env in range(2):
                kraus[2*pair+env,bit::2,i+bit]=factor[:,env]
    masses=np.array([state.trace().real for state in states])
    H=sum(k.conj().T@k for k in kraus)
    check(np.allclose(H,np.diag(masses),atol=2e-14,rtol=0),'success effect')
    check(np.max(np.linalg.eigvalsh(H))<1+2e-14,'trace nonincrease')
    for i,state in enumerate(states):
        vectors=kraus[:,:,i]
        marginal=(vectors.T@vectors.conj()).reshape(2,2,2,2).trace(axis1=1,axis2=3)
        check(np.allclose(marginal,state,atol=2e-14,rtol=0),'prescribed first output')
    w=sum(np.linalg.norm(k[::2,::2]+k[1::2,1::2])**2 for k in kraus)/(2*sum(masses))
    check(abs(w-.5-sum(overlaps)/sum(masses))<2e-14,'maximum Choi weight')
    return w

if __name__=='__main__':
    A=np.array([[.7,.15j],[-.15j,.3]])
    B=np.array([[.4,.21],[.21,.6]])
    D=np.diag([.35,.65])
    v=np.array([1,1j])/np.sqrt(2)
    C=np.outer(v,v.conj())
    check(np.linalg.norm(A@B-B@A)>.01,'noncommuting pair')
    for arms in [(.4*A,.8*B,.5*C,.6*D),(0*A,.8*B,.5*C,.6*D),(.4*A,.8*B,0*C,0*D)]:
        print('Attained local weight',f'{witness(arms):.12f}')
    print('Prescribed first marginals, Kraus projection and zero-success cases passed.')
