#!/usr/bin/env python3
"""Verification of a dimension-generalized binary-factor channel theorem.
No external data, no assumed hardware observations. Checks stay active under -O/-OO.
"""
from __future__ import annotations
import hashlib, json, math
import numpy as np
from scipy.linalg import eigh, svd


def require(cond: bool, msg: str):
    if not cond:
        raise RuntimeError(msg)


def posroot(a: np.ndarray) -> np.ndarray:
    a=(a+a.conj().T)/2
    w,v=eigh(a)
    require(np.min(w)>-5e-13, 'PSD input has negative eigenvalue')
    return (v*np.sqrt(np.maximum(w,0)))@v.conj().T


def fidelity_root(a: np.ndarray,b: np.ndarray) -> float:
    return float(np.linalg.svd(posroot(a)@posroot(b),compute_uv=False).sum())


def aligned_purifications(a: np.ndarray,b: np.ndarray):
    ra,rb=posroot(a),posroot(b)
    u,sv,vh=np.linalg.svd(ra@rb)
    right=vh.conj().T@u.conj().T
    bamp=rb@right
    check=float(np.real(np.trace(ra.conj().T@bamp)))
    require(abs(check-sv.sum())<2e-12,'Uhlmann alignment failed')
    return ra,bamp


def construct(tau: list[np.ndarray]):
    d_out=tau[0].shape[0]
    d_in=len(tau)//2
    require(len(tau)==2*d_in and d_in>=1,'need a pair per A-input')
    for mat in tau:
        require(mat.shape==(d_out,d_out),'mismatched first-output Hilbert space')
        require(np.max(np.abs(mat-mat.conj().T))<1e-12,'not Hermitian')
        require(float(np.trace(mat).real)<=1+1e-12,'success effect inadmissible')
    env=d_in*d_out; ni=2*d_in; no=2*d_out
    kraus=[np.zeros((no,ni),dtype=complex) for _ in range(env)]
    for a in range(d_in):
        amp0,amp1=aligned_purifications(tau[2*a],tau[2*a+1])
        for b,amp in enumerate((amp0,amp1)):
            for out_a in range(d_out):
                for ancilla in range(d_out):
                    kraus[a*d_out+ancilla][2*out_a+b,2*a+b]=amp[out_a,ancilla]
    return kraus


def stats(kraus, d_in, d_out=None):
    d_out=d_in if d_out is None else d_out
    success=sum(np.linalg.norm(k,'fro')**2 for k in kraus)
    proj_norm=0.0
    for k in kraus:
        av=(k[::2,::2]+k[1::2,1::2])/2
        proj_norm+=2*np.linalg.norm(av,'fro')**2
    recon=[]
    for a in range(d_in):
        for b in range(2):
            col=2*a+b
            matrix=sum((k[:,col].reshape(d_out,2) @ k[:,col].reshape(d_out,2).conj().T for k in kraus),np.zeros((d_out,d_out),complex))
            recon.append(matrix)
    effect=sum((k.conj().T@k for k in kraus),np.zeros((2*d_in,2*d_in),complex))
    return proj_norm/success, success, recon, np.linalg.eigvalsh(effect)


def run_case(d:int,seed:int,boundary=False):
    rng=np.random.default_rng(seed)
    tau=[]
    for a in range(d):
        for b in range(2):
            if boundary and a==0 and b==0:
                mat=np.zeros((d,d),complex)
            else:
                z=rng.normal(size=(d,d))+1j*rng.normal(size=(d,d))
                mat=z@z.conj().T
                mat/=np.trace(mat).real
                mat*=0.14+0.75*rng.random()
                if boundary and b==1:
                    mat=z[:,[0]]@z[:,[0]].conj().T
                    mat=mat/np.trace(mat).real * (0.14+0.65*rng.random())
            tau.append(mat)
    if boundary:
        # keep nonzero tau positive while including a zero-success input
        tau[1]=np.eye(d)/d * 0.3
    k=construct(tau)
    w,S,recon,ee=stats(k,d)
    for a,b in zip(tau,recon):
        require(np.max(np.abs(a-b))<3e-12,'marginal equality failed')
    require(float(np.max(ee)) <=1+1e-12 and float(np.min(ee))>=-1e-12,'not trace nonincreasing')
    D=sum(float(np.trace(tau[2*a]+tau[2*a+1]).real)-2*fidelity_root(tau[2*a],tau[2*a+1]) for a in range(d))
    wm=1-D/(2*S)
    require(abs(w-wm)<2e-11, 'maximum-weight identity failed')
    require(.5-2e-11 <=wm <=1+1e-11, 'weight range failed')
    flip=[]
    for kj in k:
        kf=kj.copy()
        kf[::2,:]=kj[1::2,:]
        kf[1::2,:]=kj[::2,:]
        flip.append(kf)
    wz,S2,recon2,eff2=stats(flip,d)
    require(abs(wz)<2e-12 and abs(S-S2)<2e-12,'zero-weight map failed')
    require(max(np.max(np.abs(a-b)) for a,b in zip(tau,recon2))<3e-12,'zero-weight marginals failed')
    for lam in (0.0,.17,.50,.83,1.0):
        mix=[math.sqrt(lam)*kj for kj in k]+[math.sqrt(1-lam)*kj for kj in flip]
        wmixed,Sm,marg,_=stats(mix,d)
        require(abs(wmixed-lam*wm)<2e-11 and abs(Sm-S)<2e-11,'interval interpolation failed')
        require(max(np.max(np.abs(a-b)) for a,b in zip(tau,marg))<4e-12,'mixed marginal changed')
    return dict(first_dim=d,seed=seed,zero_input=boundary,success=round(S,12),wmax=round(wm,12),endpoint_error=float(abs(w-wm)),wmin=round(wz,12))


def rare_success(q:float,alpha=.05,power=.95,h=.001,L=.2,U=.8):
    tv=h*abs(U-L)*q
    n_tv=math.ceil(math.log(1-(power-alpha))/math.log1p(-tv))
    # KL data processing necessary bound when the alternative uses the low detector eigenspace on odd inputs.
    p_alt=L; p_null=U
    kl_ber = p_alt*math.log(p_alt/p_null)+(1-p_alt)*math.log((1-p_alt)/(1-p_null))
    kl_test = power*math.log(power/alpha)+(1-power)*math.log((1-power)/(1-alpha))
    n_kl=math.ceil(kl_test/(q*h*kl_ber))
    return dict(odd_assignment_cap=q,one_step_tv=tv,necessary_attempts_TV=n_tv,necessary_attempts_KL=n_kl,maximum_rejection_power_at_100=round(alpha+1-(1-tv)**100,12))


def rectangular_case(d_in,d_out,seed):
    rng=np.random.default_rng(seed)
    tau=[]
    for a in range(d_in):
        for b in (0,1):
            z=rng.normal(size=(d_out,d_out))+1j*rng.normal(size=(d_out,d_out))
            v=z@z.conj().T
            tau.append(v/np.trace(v).real*(.25+.45*rng.random()))
    kraus=construct(tau)
    w,S,rec,ee=stats(kraus,d_in,d_out)
    delta=sum(float(np.trace(tau[2*a]+tau[2*a+1]).real)-2*fidelity_root(tau[2*a],tau[2*a+1]) for a in range(d_in))
    formula=1-delta/(2*S)
    require(abs(formula-w)<3e-11,'rectangular theorem endpoint failed')
    require(max(np.max(np.abs(a-b)) for a,b in zip(tau,rec))<1e-11,'rectangular output mismatch')
    require(float(np.max(ee))<=1+1e-11,'rectangular trace nonincrease')
    return dict(input_dim=d_in,output_dim=d_out,wmax=round(w,12),endpoint_error=round(abs(w-formula),15))


def explicitly_realized_rare_success(h=.001,L=.2,U=.8):
    """Two actual CP TNI maps with equal input success; only odd-arm readouts differ."""
    K_null=[]; K_alt=[]
    for a in (0,1):
        kn=np.zeros((4,4),complex)
        ka=np.zeros((4,4),complex)
        for b in (0,1):
            kn[b,2*a+b]=math.sqrt(h)  # first output |0>, preserve output B
            ka[2*b+b,2*a+b]=math.sqrt(h) # even first output |0>, odd |1>
        K_null.append(kn); K_alt.append(ka)
    e=np.kron(np.diag([U,L]),np.eye(2))
    out=[]
    for tag,K in [('null',K_null),('alternative',K_alt)]:
        w,S,_,success_spectrum=stats(K,2)
        clicks=[];successes=[]
        for i in range(4):
            rho=sum((np.outer(k[:,i],k[:,i].conj()) for k in K),np.zeros((4,4),complex))
            clicks.append(float(np.trace(e@rho).real))
            successes.append(float(np.trace(rho).real))
        require(np.max(np.abs(np.array(successes)-h))<1e-13,'unexpected success')
        require(np.max(success_spectrum) <= 1+1e-12,'not TNI')
        out.append(dict(branch=tag,weight=round(w,12),successes=[round(x,6) for x in successes],clicks=[round(x,6) for x in clicks]))
    require(abs(out[0]['weight']-1)<1e-12 and abs(out[1]['weight']-.5)<1e-12,'weight example failed')
    require(out[0]['clicks']==[round(h*U,6)]*4,'null click distribution')
    require(out[1]['clicks']==[round(h*U,6),round(h*L,6),round(h*U,6),round(h*L,6)],'alternative click distribution')
    return out


def boundary_cases(d):
    tau_equal=[];tau_orth=[]
    eye=np.eye(d)
    for a in range(d):
        t=eye/d*(.2+.04*a)
        tau_equal.extend([t,t])
        u=eye[:,[0]]@eye[:,[0]].conj().T*(.3+.02*a)
        v=eye[:,[1]]@eye[:,[1]].conj().T*(.5-.03*a)
        tau_orth.extend([u,v])
    for tt,target in ((tau_equal,1.),(tau_orth,.5)):
        K=construct(tt)
        wm,S,rec,ev=stats(K,d)
        require(abs(wm-target)<2e-12 and np.max(ev)<1+1e-12,'boundary pair example failed')
        require(max(np.max(np.abs(a-b)) for a,b in zip(tt,rec))<2e-12,'boundary marginals')
    return dict(dim=d,identical_pair_wmax=1,orthogonal_pair_wmax=.5)


def main():
    cases=[run_case(d,1000+53*d+seed,False) for d in (2,3,4) for seed in (1,2)]
    cases.extend([run_case(2,88,True)])
    print('PAIRED_INPUT_GENERALIZATION')
    for c in cases: print(json.dumps(c,sort_keys=True))
    print('RECTANGULAR_FIRST_FACTOR_CHECKS')
    for dims in ((3,2),(2,4)):
        print(json.dumps(rectangular_case(*dims,seed=702+dims[0]),sort_keys=True))
    print('EXACT_BOUNDARY_CASES')
    print(json.dumps(boundary_cases(3),sort_keys=True))
    print('EXPLICIT_RARE_SUCCESS_KRAUS_MODELS')
    for v in explicitly_realized_rare_success():print(json.dumps(v,sort_keys=True))
    print('RARE_SUCCESS_POWER_NECESSARY_BOUNDS')
    for q in (.25,.5,.75,1.): print(json.dumps(rare_success(q),sort_keys=True))
    print('LOW_CONTRAST_KL_COMPARISON')
    print(json.dumps(rare_success(.5,h=.001,L=.45,U=.55),sort_keys=True))
    print('VERIFICATION_COMPLETE')

if __name__=='__main__':main()
