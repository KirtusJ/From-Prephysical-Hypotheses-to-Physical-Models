"""Mathematical verification of branch-relative readout constraints.
No simulated device trials. Fixed-seed random matrices are algebraic stress-tests only.
Scientific mathematical note (unrelated material excluded).
Research direction and responsibility: Kirtus Justus.
Mathematical and computational assistance: ChatGPT (OpenAI).
7 November 2026, Vancouver, PCT (UTC-7).
"""
import math
import numpy as np
import sympy as sp

rng = np.random.default_rng(82711)
ATOL=2e-11

def need(ok,msg):
    if not bool(ok): raise ArithmeticError(msg)

def close(a,b,msg):
    need(np.max(np.abs(np.asarray(a)-np.asarray(b)))<ATOL,msg)

def local_weight(Ks):
    # second-bit blocks in standard basis 00,01,10,11
    total=0.0
    for K in Ks:
        A=K[np.ix_([0,2],[0,2])]
        D=K[np.ix_([1,3],[1,3])]
        H=(A+D)/2
        total+=2*np.vdot(H,H).real/4
    return total

def branch(Ks):
    trace=sum(np.vdot(K,K).real for K in Ks)
    need(trace>0,'nonzero branch')
    normalized=[K*(2/math.sqrt(trace)) for K in Ks]
    G=sum(K.conj().T@K for K in normalized)
    gam0=float(G[0,0].real)
    gam1=float(G[1,1].real)
    need(gam0>1e-12,'nonzero input 00 success')
    beta=sum(np.vdot(K[[1,3],0],K[[1,3],0]).real for K in normalized)/gam0
    w=local_weight(normalized)
    rhs=gam0*beta+0.5*(math.sqrt(gam0*(1-beta))-math.sqrt(gam1))**2
    need(4*(1-w)+1e-10>=rhs,'general branch inequality')
    return w,beta,gam0,gam1,rhs,4*(1-w)

def sharp(gam0,gam1,beta):
    need(gam0>0 and gam1>=0 and gam0+gam1<=4 and 0<=beta<=1,'bad sharp inputs')
    u=(4-gam0-gam1)/2
    K0=np.diag([math.sqrt(gam0*(1-beta)),math.sqrt(gam1),math.sqrt(u),math.sqrt(u)]).astype(complex)
    K1=np.zeros((4,4),complex)
    K1[1,0]=math.sqrt(gam0*beta)
    G=K0.conj().T@K0+K1.conj().T@K1
    close(G,np.diag([gam0,gam1,u,u]),'prescribed normalized success effect')
    w,p,gm0,gm1,rhs,lhs=branch([K0,K1])
    close((gm0,gm1,p),(gam0,gam1,beta),'constructed probabilities')
    close(lhs,rhs,'sharpness attained')
    # Positive scaling turns normalized maps into genuine trace-nonincreasing CP branch.
    physical_scale=1/max(gam0,gam1,u,1)
    K0*=math.sqrt(physical_scale); K1*=math.sqrt(physical_scale)
    eig=np.linalg.eigvalsh(K0.conj().T@K0+K1.conj().T@K1)
    need(max(eig)<=1+ATOL,'physical trace-nonincreasing Kraus pair')

def symbolic():
    g0,g1,b,alpha=sp.symbols('g0 g1 b alpha',nonnegative=True,real=True)
    # Formula after grouping Kraus first columns and setting alpha=0.
    expr=g0*b+sp.Rational(1,2)*(sp.sqrt(g0*(1-b))-sp.sqrt(g1))**2
    x=sp.symbols('x',nonnegative=True,real=True)
    ident=sp.expand((2*expr).subs(b,1-x**2) - (2*g0+g1-g0*x**2-2*x*sp.sqrt(g0*g1)))
    need(sp.simplify(ident)==0,'inversion identity')
    print('Symbolic inversion identity verified.')

def stress():
    n=0
    for rank in (1,2,4,8):
        for _ in range(60):
            A=rng.normal(size=(4*rank,4))+1j*rng.normal(size=(4*rank,4))
            scale=0.2/math.sqrt(float(np.linalg.norm(A.conj().T@A,2)))
            Ks=[scale*A[4*k:4*k+4] for k in range(rank)]
            branch(Ks)
            n+=1
    # Sharpness tests including cases with different input successes.
    values=[(1,1,0),(1,1,.04),(1,1,1),(.65,1.17,.15),(2.5,.2,.37),(.9,.4,.5),(3,1,1),(.001,3,.2)]
    for g0,g1,beta in values: sharp(g0,g1,beta)
    print('General non-trace-preserving branch inequality verified on',n,'complex Kraus ensembles.')
    print('Sharpness and legitimate TNI realizations verified on',len(values),'specified triples.')

def illustration():
    # Supplied exact population inputs; not empirical observations.
    s=131/320; h=.99; q=81711338569043/224995905216000
    k=(math.sqrt(q)-math.sqrt(h*s))**2/(1-h)
    d=s+k; r=1-d; ell=.01; f=r-ell
    w0=s+f+k
    need(abs(w0-.99)<1e-12,'weight at source point')
    beta_max=1-(math.sqrt(4-8*(1-w0))-1)**2
    need(.03979797464466<beta_max<.03979797464468,'TP envelope')
    print('TP or equal-relative-success case: w0',f'{w0:.12f}', 'beta ceiling',f'{beta_max:.15f}')

def rank_one_branch():
    # General CP TNI rank-one Choi still sends a pure tested input to a pure conditional output.
    a=.8
    for beta in (.2,.4,.8):
        # Pure joint output with Schmidt first spectrum (a,1-a).
        c=(beta-(1-a))/(2*a-1)
        c=np.clip(c,0,1)
        V=np.array([[math.sqrt(c),-math.sqrt(1-c)],[math.sqrt(1-c),math.sqrt(c)]],complex)
        v=math.sqrt(a)*np.kron([1,0],V[:,0])+math.sqrt(1-a)*np.kron([0,1],V[:,1])
        sigma=np.outer(v,v.conj())
        pi=np.trace(sigma.reshape(2,2,2,2),axis1=1,axis2=3)
        pj=np.trace(sigma.reshape(2,2,2,2),axis1=0,axis2=2)
        need(abs(np.linalg.eigvalsh(pi)[-1]-a)<ATOL,'Schmidt marginal')
        need(abs(pj[0,0].real-beta)<ATOL,'second outcome')
        K=np.outer(v,np.array([1,0,0,0],complex))
        need(max(np.linalg.eigvalsh(K.conj().T@K))<=1+ATOL,'TNI preparation branch')
    print('Rank-one TNI compatibility construction verified for local marginal readings.')

if __name__=='__main__':
    symbolic();stress();illustration();rank_one_branch()
