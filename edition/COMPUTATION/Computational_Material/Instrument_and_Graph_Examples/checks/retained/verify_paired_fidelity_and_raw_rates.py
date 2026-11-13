#!/usr/bin/env python3
"""Deterministic verification of paired-input branch-fidelity conditions.

No device observations or simulated experimental trials.  All numeric examples
are algebraic constructions checking necessity/sufficiency or published model inputs.
"""
import math
from fractions import Fraction
import numpy as np
import mpmath as mp


def must(ok, msg):
    if not bool(ok):
        raise ArithmeticError(msg)


def herm_sqrt(x):
    vals, u = np.linalg.eigh(x)
    must(float(np.min(vals)) >= -5e-12, 'nonpositive input density')
    return (u*np.sqrt(np.maximum(vals,0)))@u.conj().T


def root_fidelity(x,y):
    return float(np.linalg.svd(herm_sqrt(x)@herm_sqrt(y),compute_uv=False).sum())


def first_output(ks, input_col):
    vec=ks[:,:,input_col]  # (environment, four output entries)
    op=vec.T@vec.conj()    # unnormalized 4x4 output
    p=float(np.trace(op).real)
    one=np.trace(op.reshape(2,2,2,2),axis1=1,axis2=3)/p
    return p, one


def w_local(ks):
    total=float(sum(np.linalg.norm(k[::2,::2]+k[1::2,1::2])**2 for k in ks))
    return total/8 # assumes sum_{j} Tr(K_j^*K_j)=4


def make_witness(rho0,rho1,g0,g1):
    """Raw Choi-normalized Kraus operators; choose physical pstar separately."""
    L, R=herm_sqrt(rho0),herm_sqrt(rho1)
    U, singular, Vh=np.linalg.svd(L@R)
    R=R@Vh.conj().T@U.conj().T
    must(abs(np.vdot(L,R).real-singular.sum())<2e-12,'Uhlmann phase')
    h=(4-g0-g1)/2
    must(h>=0,'inadmissible relative successes')
    V=np.zeros((4,3,4),complex) # four system outputs, 3 env flags, four inputs
    V[::2,:2,0]=math.sqrt(g0)*L
    V[1::2,:2,1]=math.sqrt(g1)*R
    V[0,2,2]=math.sqrt(h)
    V[1,2,3]=math.sqrt(h)
    ks=V.transpose(1,0,2)
    w=w_local(ks)
    F=root_fidelity(rho0,rho1)
    deficit=g0+g1-2*math.sqrt(g0*g1)*F
    must(abs(8*(1-w)-deficit)<2e-12,'sharp fidelity identity')
    effect=sum(K.conj().T@K for K in ks)
    must(np.linalg.norm(effect-np.diag([g0,g1,h,h]))<2e-12,'success effect')
    for col,rho,gi in [(0,rho0,g0),(1,rho1,g1)]:
        prob,actual=first_output(ks,col)
        must(abs(prob-gi)<2e-12 and np.linalg.norm(actual-rho)<2e-12,'conditional output')
    raw_scale=min(.5,1/max(1,g0,g1,h))
    must(np.linalg.eigvalsh(np.eye(4)-raw_scale*effect).min()>-2e-12,'physical branch scaling')
    return w, F, raw_scale


def h2_raw(r0,r1):
    return float(np.sum((np.sqrt(r0)-np.sqrt(r1))**2))


def inverse_click_interval(p0,p1,x,w0,pstar):
    """Sharp y interval given one conditional click rate x, with projective readout."""
    bound=(p0+p1-8*pstar*(1-w0))/(2*math.sqrt(p0*p1))
    if bound>1+1e-14: return None
    if bound<=0: return (0.,1.)
    angle=math.acos(math.sqrt(x))
    theta=math.acos(min(1.,bound))
    lower=math.cos(min(math.pi/2,angle+theta))**2
    upper=math.cos(max(0.,angle-theta))**2
    return lower,upper


def check():
    mp.mp.dps=65
    si=mp.mpf(131)/320;hi=mp.mpf(99)/100
    qi=mp.mpf(81711338569043)/224995905216000
    k=(mp.sqrt(hi*si)-mp.sqrt(qi))**2/(1-hi)
    d=si+k;ell=mp.mpf('0.01');a=d+6*ell/13
    c=mp.mpf('.96')
    G=lambda x:(c*mp.sqrt(x)+mp.sqrt(1-c*c)*mp.sqrt(1-x))**2
    beta=1-(mp.sqrt(mp.mpf('3.92'))-1)**2
    m=a+beta
    m1_old=G(m)
    t=(2+a+G(a)+mp.mpf('.04'))/4
    bound=t*t+(1-t)**2
    dist=(1-m+mp.sqrt((1-m)**2+12*(1-mp.sqrt(m))**2))/8
    must(mp.mpf('.7321043027225949')<bound<mp.mpf('.7321043027225950'),'purity enclosure')
    must(mp.mpf('.8246170805237347')<m1_old<mp.mpf('.8246170805237348'),'old output')
    must(mp.mpf('.1730027896903658')<dist<mp.mpf('.1730027896903659'),'distance floor')
    print('SOURCE CROSS-CHECK (model values only)')
    for lab,val in [('a',a),('beta maximum',beta),('old neighbor eigenvalue ceiling',m1_old),('refined purity ceiling',bound),('Choi distance floor',dist)]:
        print(lab, mp.nstr(val,30))

    # Noncommuting density marginals: verify sharp fidelity construction.
    rho0=np.array([[.55,.23j],[-.23j,.45]],complex)
    rho1=np.array([[.23,.12],[.12,.77]],complex)
    for g0,g1 in [(1,1),(.8,1.6),(1.5,2.5),(.04,.04),(.02,1.3)]:
        w,F,pstar=make_witness(rho0,rho1,g0,g1)
        must(w>=0 and w<=1 and pstar>0,'witness domain')
    zero=np.diag([1.,0.]); one=np.diag([0.,1.])
    w,F,pstar=make_witness(zero,one,.04,.04)
    must(abs(w-.99)<2e-13 and abs(F)<2e-13,'rare-success example')
    # Set p*=1/2 to give tested raw successes .02 and untested .98.
    must(.5*1.96==.98 and .5*.04==.02,'success normalization')
    r0=np.array([.02,0]);r1=np.array([0,.02])
    must(abs(h2_raw(r0,r1)-8*.5*(1-.99))<2e-15,'exact Hellinger equality')
    print('RARE-EVENT WITNESS: pstar=.5; successes (.02,.02,.98,.98); w=.99; first marginals orthogonal')
    print('Unconditional Hellinger discrepancy',format(h2_raw(r0,r1),'.16f'))

    # Equal relative successes: exact sharp binary-output interval from the classical fidelity.
    x=float(1-a)
    lo,up=inverse_click_interval(1.,1.,x,.99,1.)
    diff=up-x
    must(abs(diff-0.27295396145309825)<2e-14,'sharp contrast')
    rho0=np.diag([x,1-x]);rho1=np.diag([up,1-up])
    w,F,pstar=make_witness(rho0,rho1,1,1)
    must(abs(w-.99)<2e-13,'projective attainment at h=.96')
    print('Sharp binary projective output interval at x=1-a:',f'[{lo:.15f}, {up:.15f}]')
    print('Largest y-x at x=1-a:',format(diff,'.15f'))

    # Necessary/sufficient criterion for raw 2-output frequencies in a CP branch.
    for raw0,raw1,pstar in [([.15,.05],[.16,.24],.4), ([.02,0],[0,.02],.5),([.11,.08],[.08,.12],.22)]:
        raw0,raw1=np.array(raw0),np.array(raw1)
        p0,p1=raw0.sum(),raw1.sum()
        state0=np.diag(raw0/p0);state1=np.diag(raw1/p1)
        w,F,phys=make_witness(state0,state1,p0/pstar,p1/pstar)
        must(abs(h2_raw(raw0,raw1)-8*pstar*(1-w))<2e-12,'raw rate sufficiency')
        must(pstar <= phys+1e-13 or (pstar*max(p0/pstar,p1/pstar,(4-(p0+p1)/pstar)/2) <= 1+1e-13),'scale for raw rates')
    print('Three arbitrary raw success+click probability examples checked constructively.')

    # Joint convexity: exact direct Cauchy-Schwarz for pooled attempted rates.
    a0=np.array([.05,.10]);b0=np.array([.09,.05]); a1=np.array([.14,.12]);b1=np.array([.1,.19]);
    lhs=h2_raw((a0+a1)/2,(b0+b1)/2)
    rhs=(h2_raw(a0,b0)+h2_raw(a1,b1))/2
    must(lhs<=rhs+2e-15,'mixture joint convexity')
    print('Pooling check: H²(mean rates)=',f'{lhs:.15f}','<= mean H²=',f'{rhs:.15f}')
    print('All algebraic and matrix checks passed.')

if __name__=='__main__':
    check()
