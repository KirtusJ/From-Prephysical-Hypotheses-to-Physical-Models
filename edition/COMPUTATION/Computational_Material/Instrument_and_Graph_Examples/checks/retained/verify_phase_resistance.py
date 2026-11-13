#!/usr/bin/env python3
"""Checks of scale-POVM pair interferometry and a finite-sample graph test.
Purely classical finite-dimensional matrix representations of stipulated one-particle POVM.
"""
import json, math
from pathlib import Path
import numpy as np
from scipy.linalg import eigh
from scipy.stats import binom
from scipy.integrate import quad


def graph_laplacian(n, edges):
    L=np.zeros((n,n),dtype=float)
    for i,j,w in edges:
        L[i,i]+=w; L[j,j]+=w; L[i,j]-=w;L[j,i]-=w
    return L


def rook_shrikhande():
    vertices=[(i,j) for i in range(4) for j in range(4)]
    idx={v:k for k,v in enumerate(vertices)}
    r_edges=[]; s_edges=[]
    S={(1,0),(3,0),(0,1),(0,3),(1,1),(3,3)}
    for a,(i,j) in enumerate(vertices):
        for b,(k,l) in enumerate(vertices):
            if b<=a:continue
            if i==k or j==l:r_edges.append((a,b,1))
            if ((k-i)%4,(l-j)%4) in S:s_edges.append((a,b,1))
    return graph_laplacian(16,r_edges),graph_laplacian(16,s_edges),idx


def pseudo(L):
    eig,U=eigh(L); P=np.zeros_like(L)
    P[:, :]= (U * np.where(eig>1e-9,1/eig,0)) @ U.T
    return P


def density_pair(n,i,j,sig,phi):
    # +/- amplitude convention with real phase offset phi
    psi=np.zeros(n,complex);psi[i]=1/math.sqrt(2);psi[j]=sig*np.exp(1j*phi)/math.sqrt(2)
    return np.outer(psi,psi.conj())


def sample_stats(L,i,j,phase_pos,phase_neg):
    n=L.shape[0];K=pseudo(L);P0=np.ones((n,n))/n
    def mixed(sig,phases):
        rho=sum(w*density_pair(n,i,j,sig,phi) for phi,w in phases)
        return float(np.real(np.trace(P0@rho))),float(np.real(np.trace(K@rho)))
    pplus,mplus=mixed(1,phase_pos);pminus,mminus=mixed(-1,phase_neg)
    cplus=n*pplus-1;cminus=1-n*pminus
    den=cplus+cminus
    b=(mplus-mminus)/den
    S=mplus+mminus-(cplus-cminus)*b
    r=S-2*b
    exact=float(K[i,i]+K[j,j]-2*K[i,j])
    return {"n":n,"nodes":[i,j],"p0plus":pplus,"p0minus":pminus,"mplus":mplus,"mminus":mminus,"cplus":cplus,"cminus":cminus,"recovered_Kij":b,"resistance_rec":r,"resistance_exact":exact,"absolute_error":abs(r-exact),"denominator":den}


def general_population_invariant_contrast(L,i,j,pop=0.73,phi=0.42):
    n=L.shape[0]
    K=pseudo(L);P0=np.ones((n,n))/n
    psi=np.zeros(n,dtype=complex)
    psi[i]=math.sqrt(pop);psi[j]=math.sqrt(1-pop)*np.exp(1j*phi)
    rho_A=np.outer(psi,psi.conj())
    rho_B=np.zeros((n,n),complex)
    rho_B[i,i]=pop;rho_B[j,j]=1-pop # fully dephased control
    pA=float(np.real(np.trace(P0@rho_A)))
    pB=float(np.real(np.trace(P0@rho_B)))
    mA=float(np.real(np.trace(K@rho_A)))
    mB=float(np.real(np.trace(K@rho_B)))
    recovered=(mA-mB)/(n*(pA-pB))
    return {"pair":[i,j],"population_first":pop,"relative_phase_radians":phi,"p0_coherent":pA,"p0_dephased":pB,"mean_coherent":mA,"mean_dephased":mB,
            "independent_spectral_coherent":independent_povm_moments(L,rho_A),
            "independent_spectral_dephased":independent_povm_moments(L,rho_B),"offdiag_recovered":recovered,"offdiag_exact":float(K[i,j]),"abs_error":abs(recovered-K[i,j]),"denominator":n*(pA-pB)}


def independent_povm_moments(L,rho):
    evals,U=eigh(L)
    spectral_weights=np.real(np.diag(U.T@rho@U))
    spectral_weights=np.where(np.abs(spectral_weights)<1e-12,0,spectral_weights)
    p0=float(np.sum(spectral_weights[evals<1e-9]))
    mean=float(np.sum(spectral_weights[evals>1e-9]/evals[evals>1e-9]))
    second=float(1.5*np.sum(spectral_weights[evals>1e-9]/(evals[evals>1e-9]**2)))
    return {"p0":p0,"mean":mean,"second":second}


def pclass(lam,s):
    return 4*lam*lam*s*np.exp(-2*lam*s)


def binomial_test():
    t=math.log(2)/4
    # Edge: weights spectral 4:1/2,8:3/8; nonedge: 4:1/4, 8:5/8
    T=lambda lam: (1+2*lam*t)*math.exp(-2*lam*t)
    p_edge=.5*T(4)+.375*T(8)
    p_non=.25*T(4)+.625*T(8)
    tv=(3+2*math.log(4))/64
    # by Neyman Pearson with two outcomes (s>t or not) across repeated photons
    a=math.log(p_edge/p_non); b=math.log((1-p_edge)/(1-p_non))
    def bayes(M):
        # choose rook if k*a+(M-k)*b>0: k> M*(-b)/(a-b)
        split=M*(-b)/(a-b)
        cutoff=int(math.floor(split + 1e-12))
        return 0.5*(binom.cdf(cutoff,M,p_edge)+binom.sf(cutoff,M,p_non)),cutoff
    threshold=next((M for M in range(1,3000) if bayes(M)[0]<=.10),None)
    cert=math.ceil(2*math.log(10)/tv**2)
    # exact integration of continuous trace distance
    diff=lambda s: (32*s*math.exp(-8*s)+96*s*math.exp(-16*s))-(16*s*math.exp(-8*s)+160*s*math.exp(-16*s))
    tv_int=(quad(lambda s: -diff(s),0,t,epsabs=1e-14)[0]+quad(diff,t,np.inf,epsabs=1e-14)[0])/2
    # complete scale-register trace distance
    trace_distance=math.sqrt(17)/36
    return {"single_site_zero_p":1/8,"threshold_scale":t,"edge_above_p":p_edge,"nonedge_above_p":p_non,"exact_tv":tv,"tv_quad_truncation_4":tv_int,"binary_full_single_shot_tv":p_edge-p_non,"minimum_binary_Bayes_trials_for_10_percent":threshold,"binary_Bayes_at_min":bayes(threshold),"certified_Hoeffding_trials_10_percent":cert,"quantum_scale_register_trace_distance":trace_distance}


def first_moment_check(L,i,j):
    vals,U=eigh(L);v=(np.eye(L.shape[0])[i]-np.eye(L.shape[0])[j])/math.sqrt(2)
    weights=np.abs(U.T@v)**2
    exact=sum(weights[k]/vals[k] for k in range(len(vals)) if vals[k]>1e-10)
    second=1.5*sum(weights[k]/vals[k]**2 for k in range(len(vals)) if vals[k]>1e-10)
    def pdf(s): return sum(weights[k]*pclass(vals[k],s) for k in range(len(vals)) if vals[k]>1e-10)
    integral=quad(lambda s:s*pdf(s),0,np.inf,epsabs=1e-12)[0]
    return {"exact_mean":exact,"numerical_integral":integral,"second_moment":second,"variance":second-exact*exact}


def main():
    R,S,idx=rook_shrikhande()
    for L in [R,S]:
        spec=np.round(eigh(L,eigvals_only=True),9)
        assert np.array_equal(spec,np.array([0]+[4]*6+[8]*9,dtype=float))
    p=graph_laplacian(5,[(0,1,2.1),(1,2,1.7),(2,3,3.3),(3,4,0.9)])
    samples={
      "weighted_path_phase_drift_mixed":sample_stats(p,0,4,[(0.37,0.7),(-0.6,0.3)],[(0.72,.4),(-0.20,.6)]),
      "rook_pair_phase_drift_mixed":sample_stats(R,idx[(0,0)],idx[(0,2)],[(0.55,.4),(-.33,.6)],[(0.93,.25),(-0.22,.75)]),
      "shrikhande_pair_phase_drift_mixed":sample_stats(S,idx[(0,0)],idx[(0,2)],[(0.55,.4),(-.33,.6)],[(0.93,.25),(-0.22,.75)])
    }
    for z in samples.values(): assert z["absolute_error"]<1e-12
    # Exact phase null for independent balanced preparations: the mean-zero intensity reproduces cos expectations
    result={"phase_recovery":samples,
            "coherent_vs_dephased":{
               "weighted_path":general_population_invariant_contrast(p,0,4),
               "rook":general_population_invariant_contrast(R,idx[(0,0)],idx[(0,2)]),
               "shrikhande":general_population_invariant_contrast(S,idx[(0,0)],idx[(0,2)])},
            "binomial_discrimination":binomial_test(),
            "mean_scale_checks":{"path_endpoints":first_moment_check(p,0,4),"rook_edge":first_moment_check(R,idx[(0,0)],idx[(0,1)]),"rook_nonedge":first_moment_check(R,idx[(0,0)],idx[(1,1)])}}
    assert abs(result['binomial_discrimination']['exact_tv']-result['binomial_discrimination']['binary_full_single_shot_tv'])<2e-15
    assert abs(result['binomial_discrimination']['exact_tv']-result['binomial_discrimination']['tv_quad_truncation_4'])<1e-12
    for z in result['mean_scale_checks'].values():assert abs(z['exact_mean']-z['numerical_integral'])<1e-10
    for z in result['coherent_vs_dephased'].values():
        assert z['abs_error'] < 1e-12
        assert abs(z['independent_spectral_coherent']['p0']-z['p0_coherent']) < 1e-12
        assert abs(z['independent_spectral_coherent']['mean']-z['mean_coherent']) < 1e-12
        assert abs(z['independent_spectral_dephased']['mean']-z['mean_dephased']) < 1e-12
    f=str(Path(__file__).resolve().parent/"independent_results.json")
    with open(f,'w',encoding='utf8') as out: json.dump(result,out,indent=2,sort_keys=True)
    print(json.dumps(result,indent=2,sort_keys=True))

if __name__=='__main__':main()
