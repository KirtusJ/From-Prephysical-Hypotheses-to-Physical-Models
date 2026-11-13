"""Constructive verification: conditional CP branch Choi purity.
No device records, no pseudo-experimental trials, no Monte Carlo.
Research direction and responsibility: Kirtus Justus.
Mathematical and computational assistance: ChatGPT (OpenAI).
7 November 2026, Vancouver, PCT (UTC-7).
"""
import math
import numpy as np

ATOL=2e-12
I4=np.eye(4,dtype=complex)
I16=np.eye(16,dtype=complex)

def require(x,m):
    if not bool(x): raise ArithmeticError(m)

def close(x,y,m):
    require(np.max(np.abs(np.asarray(x)-np.asarray(y)))<ATOL,m)

def project(v):
    return np.outer(v,np.conj(v))

def partial_output(C):
    # C indexed output first, then reference input.
    return np.trace(C.reshape(4,4,4,4),axis1=0,axis2=2)

def from_blocks(sigma,t):
    lam,Q=np.linalg.eigh(sigma)
    order=np.argsort(lam)[::-1]
    lam=np.maximum(lam[order],0);Q=Q[:,order]
    A=t*np.kron(sigma,np.diag([1,0,0,0]))
    lower=A+(1-t)/12*np.kron(I4,np.diag([0,1,1,1]))
    e0=np.eye(4,dtype=complex)[:,0]
    e1=np.eye(4,dtype=complex)[:,1]
    u=np.kron(Q[:,0],e0)
    v=np.kron(e0,e1)
    ket=math.sqrt(t*lam[0])*u+math.sqrt(1-t)*v
    upper=project(ket)
    for k in range(1,4):
        upper+=t*lam[k]*project(np.kron(Q[:,k],e0))
    return lower,upper

def check_state(C,sigma,t,m):
    close(C,C.conj().T,'Hermitian '+m)
    require(np.linalg.eigvalsh(C)[0]>-ATOL,'PSD '+m)
    close(np.trace(C),1,'trace '+m)
    input0=np.kron(I4,np.diag([1,0,0,0]))
    A=input0@C@input0
    close(A,t*np.kron(sigma,np.diag([1,0,0,0])),'measured block '+m)
    # Every normalized C is a physical CP instrument branch after positive rescaling.
    H=4*partial_output(C).T
    herm=(H+H.conj().T)/2
    lam=np.linalg.eigvalsh(herm)
    scale=1/max(max(lam),1)
    require(np.linalg.eigvalsh(I4-scale*herm)[0]>-ATOL,'non-TP physical branch scaling '+m)
    return float(np.trace(C@C).real)

def test_sigma(sigma,t):
    require(np.linalg.eigvalsh(sigma)[0]>-ATOL,'joint PSD')
    close(np.trace(sigma),1,'joint trace')
    lower,upper=from_blocks(sigma,t)
    P=float(np.trace(sigma@sigma).real)
    lam=float(np.linalg.eigvalsh(sigma)[-1])
    lo=t*t*P+(1-t)**2/12
    hi=t*t*P+(1-t)**2+2*t*(1-t)*lam
    close(check_state(lower,sigma,t,'lower'),lo,'lower purity')
    close(check_state(upper,sigma,t,'upper'),hi,'upper purity')
    for u in (0,.31,.74,1):
        mix=(1-u)*lower+u*upper
        val=check_state(mix,sigma,t,'mixed')
        require(lo-1e-12<=val<=hi+1e-12,'range')
    return lo,hi

def sigma_extrema(a,b):
    # 1/2<=a<=1, 0<=b<=1/2 (b is the less-likely second-output reading)
    minx=max(0,a+b-1)
    maxx=min(a,b)
    x=min(max((a+b)/2-.25,minx),maxx)
    lower=np.diag([a-x,x,1-a-b+x,b-x]).astype(complex)
    if b<1-a:
        v=np.array([math.sqrt(a),0,0,math.sqrt(b)],complex)
        upper=project(v)+np.diag([0,0,1-a-b,0])
    else:
        c=0.5 if abs(a-0.5)<1e-12 else (a-b)/(2*a-1)
        require(-ATOL<=c<=1+ATOL,'rotated Schmidt basis')
        c=max(0,min(1,c))
        R=np.array([[math.sqrt(c),-math.sqrt(1-c)],[math.sqrt(1-c),math.sqrt(c)]],complex)
        v=math.sqrt(a)*np.kron([1,0],R[:,0])+math.sqrt(1-a)*np.kron([0,1],R[:,1])
        upper=project(v)
    for name,C in (('low',lower),('high',upper)):
        red=C.reshape(2,2,2,2)
        first=np.trace(red,axis1=1,axis2=3)
        second=np.trace(red,axis1=0,axis2=2)
        close(first,np.diag([a,1-a]),'first marginal '+name)
        close(second[1,1],b,'second effect '+name)
    return lower,upper

def local_data_test(a,b,t):
    low_joint,hi_joint=sigma_extrema(a,b)
    L,tL=test_sigma(low_joint,t)
    tH,H=test_sigma(hi_joint,t)
    require(L<=H+ATOL,'ordered lower/upper')
    Pmin=float(np.trace(low_joint@low_joint).real)
    m=min(1,a+b)
    expected_lo=t*t*Pmin+(1-t)**2/12
    expected_hi=t*t*(m*m+(1-m)**2)+(1-t)**2+2*t*(1-t)*m
    close((L,H),(expected_lo,expected_hi),'optimized local measurements')
    return L,H

def main():
    for a,b,t in ((.8,.1,.25),(.8,.3,.25),(.5,.5,.25),(.8,.1,.075),(.8,.1,.65),(.6,.03,.8),(.9,.1,1.)):
        lo,hi=local_data_test(a,b,t)
        print(f'local a={a:.3f} b={b:.3f} normalized success t={t:.3f}: [{lo:.12f}, {hi:.12f}]')
    # Source's purely mathematical reference values, not observed hardware frequencies.
    s=131/320;h=.99;q=81711338569043/224995905216000
    k=(math.sqrt(q)-math.sqrt(h*s))**2/(1-h)
    d=s+k;r=1-d;ell=.01
    a=d+6*ell/13
    beta=1-(math.sqrt(3.92)-1)**2
    lo,hi=local_data_test(a,beta,.25)
    close(hi,.8078263982873538,'source ceiling conditional on beta')
    print('Source conditional purity ceiling recovered:',f'{hi:.15f}')
    # A rank-one Choi branch output must remain pure even if success depends on input.
    # For a=.8 and b=.1, the sharp upper is <1 at any 0<t<=1, not only at t=1/4.
    for t in (.0001,.01,.25,.95):
        _,hi=local_data_test(.8,.1,t)
        require(hi<1,'rank-one exclusion with nonzero success')
    print('Sharp interval verified for normalized trace-nonincreasing CP branches.')

if __name__=='__main__':main()
