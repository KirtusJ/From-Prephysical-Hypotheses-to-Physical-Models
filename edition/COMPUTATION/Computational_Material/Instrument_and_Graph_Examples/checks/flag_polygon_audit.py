#!/usr/bin/env python3
"""Deterministic checks for flag-resolved Choi-weight and finite Gibbs claims.
No hardware data, no random simulated experiments. Checks remain active under -O / -OO.
"""
import math
import numpy as np
import scipy.linalg as la

def require(condition, message):
    if not bool(condition):
        raise RuntimeError(message)

def weight(kraus, d_in, d_out, q):
    total = 0.0
    local = 0.0
    for K in kraus:
        require(K.shape == (d_out*q, d_in*q), "wrong Kraus shape")
        total += np.vdot(K, K).real
        V = sum((K[r::q, r::q] for r in range(q))) / q
        local += q*np.vdot(V, V).real
    require(total > 0, "zero total success")
    return local/total

def output_on_basis(kraus, input_index):
    col = [K[:,input_index] for K in kraus]
    return sum(np.outer(v, v.conj()) for v in col)

def tensor_psd_sqrt(A):
    vals, vecs = la.eigh(A)
    require(min(vals) > -1e-11, "input matrix not PSD")
    return (vecs*np.sqrt(np.maximum(0.,vals)))@vecs.conj().T

def root_fidelity(A,B):
    X = tensor_psd_sqrt(A)
    return float(np.sum(np.linalg.svd(X@tensor_psd_sqrt(B), compute_uv=False)))

def binary_kraus(A,B,sign):
    sqrtA = tensor_psd_sqrt(A)
    sqrtB = tensor_psd_sqrt(B)
    U, singular, Vh = la.svd(sqrtA.conj().T @ sqrtB)
    rotation=Vh.conj().T@U.conj().T
    M0=sqrtA
    M1=sign*sqrtB@rotation
    d=M0.shape[0]
    E=M0.shape[1]
    Ks=[]
    for e in range(E):
        K=np.zeros((d*2,2),complex)
        K[0::2,0]=M0[:,e]
        K[1::2,1]=M1[:,e]
        Ks.append(K)
    return Ks

def trine_flag_kraus(sign):
    q=3
    probs=np.array([[1.,0.],[.25,.75],[0.,1.]])
    Ks=[]
    for j in range(2):
        K=np.zeros((2*q,q),complex)
        for b in range(q):
            K[j*q+b,b] = math.sqrt(probs[b,j])*(-1 if sign==-1 and b==1 else 1)
        Ks.append(K)
    return Ks

def thermal_trace_dist(A,V,beta):
    E1=la.expm(-beta*A); E1/=np.trace(E1)
    E2=la.expm(-beta*(A+V)); E2/=np.trace(E2)
    T=0.5*np.sum(abs(np.linalg.eigvalsh(E1-E2)))
    ev=np.linalg.eigvalsh(V)
    bound=math.tanh(beta*(float(ev[-1]-ev[0]))/4)
    return float(T), bound

# 1) Binary flag theorem for noncommuting, strictly positive matched matrices.
A=np.array([[.31,.08+.05j],[.08-.05j,.19]],complex)
B=np.array([[.24,-.06+.025j],[-.06-.025j,.26]],complex)
require(np.linalg.norm(A@B-B@A)>0.01,"noncommuting control accidentally commutes")
f=root_fidelity(A,B)
S=float(np.trace(A+B).real)
for sign in (1,-1):
    Ks=binary_kraus(A,B,sign)
    W=weight(Ks,1,2,2)
    formula=0.5+sign*f/S
    require(abs(W-formula)<5e-13,"binary endpoint failed")
    E=sum(K.conj().T@K for K in Ks)
    require(np.linalg.norm(E-.5*np.eye(2))<5e-13,"binary success effect failed")
    # The reported flag-b outcome is matrix A / B, respectively.
    for b,X in enumerate((A,B)):
        O=output_on_basis(Ks,b)
        Y=O[b::2,b::2]
        require(np.linalg.norm(Y-X)<5e-13,"binary output state mismatch")
        require(np.linalg.norm(O[1-b::2,1-b::2])<5e-13,"wrong flag nonzero")
print(f"BINARY: root_fidelity={f:.15f} range=[{(.5-f/S):.15f},{(.5+f/S):.15f}]")

# 2) Three flags, full (joint) basis-output data, unitary isometric dilation.
Ks_plus=trine_flag_kraus(1)
Ks_minus=trine_flag_kraus(-1)
rho0=[output_on_basis(Ks_plus,i) for i in range(3)]
rho1=[output_on_basis(Ks_minus,i) for i in range(3)]
for kp,km in zip(Ks_plus,Ks_minus):
    require(kp.shape==(6,3) and km.shape==(6,3),"3-flag dims")
for ks in (Ks_plus,Ks_minus):
    effect=sum(K.conj().T@K for K in ks)
    require(np.linalg.norm(effect-np.eye(3))<1e-13,"3-flag TP failed")
require(max(np.linalg.norm(a-b) for a,b in zip(rho0,rho1))<1e-13,"basis outputs differ")
w_plus=weight(Ks_plus,1,2,3)
w_minus=weight(Ks_minus,1,2,3)
require(abs(w_plus-(4+math.sqrt(3))/9)<2e-13,"3-flag upper failed")
require(abs(w_minus-(2-math.sqrt(3))/9)<2e-13,"3-flag lower failed")
# Coherent input (|0>+|1>+|2>)/sqrt(3), flag projector |0,1> plus in A=0.
x=np.ones(3,complex)/math.sqrt(3)
y=np.zeros(6,complex);y[0]=1/math.sqrt(2);y[1]=1/math.sqrt(2)
def coh_click(ks):
    out=sum(np.outer(K@x,(K@x).conj()) for K in ks)
    return float(np.vdot(y,out@y).real)
click_plus=coh_click(Ks_plus); click_minus=coh_click(Ks_minus)
require(abs(click_plus-3/8)<1e-13,"coherent plus failed")
require(abs(click_minus-1/24)<1e-13,"coherent minus failed")
print(f"THREE FLAGS: w_min={w_minus:.15f}, w_max={w_plus:.15f}, coherence_clicks=({click_minus:.15f},{click_plus:.15f})")
print(f"THREE FLAGS: basis_outputs_equal=True, TP=True, coherent_difference={click_plus-click_minus:.15f}")

# 3) Square-root stability exponent from exact commuting binary data.
for e in (1e-2,1e-4,1e-6):
    P0=np.diag([1.,0.])
    P1=np.diag([0.,1.])
    P1p=np.diag([e,1.-e])
    before=0.5+root_fidelity(P0,P1)/2
    after=0.5+root_fidelity(P0,P1p)/2
    require(abs((after-before)-math.sqrt(e)/2)<1e-11,"sqrt stability failed")
print("STABILITY: exact exponent 1/2 example verified for eps=1e-2,1e-4,1e-6")

# 4) Sharp finite-dimensional Gibbs bound including 2-level equality and noncommuting trials.
for b,v in ((.2,1.),(1.,2.),(3.,1.8)):
    H=np.diag([-v/4,v/4])
    V=-2*H
    T,bound=thermal_trace_dist(H,V,b)
    require(abs(T-bound)<2e-13,"Gibbs equality case failed")
rng=np.random.default_rng(20261107)
max_gap=-1e6
count=0
for d in (2,3,4,5):
    for _ in range(120):
        X=rng.standard_normal((d,d))+1j*rng.standard_normal((d,d))
        Y=rng.standard_normal((d,d))+1j*rng.standard_normal((d,d))
        A=(X+X.conj().T)/2
        V=(Y+Y.conj().T)/2
        beta=float(rng.uniform(.03,2.5))
        T,bound=thermal_trace_dist(A,V,beta)
        gap=T-bound
        max_gap=max(max_gap,gap);count+=1
        require(gap<=1e-11,"finite Gibbs inequality violation")
print(f"GIBBS: 2-level equality passed; noncommuting matrices checked={count}; max(T-bound)={max_gap:.12g}")
print("ALL CHECKS PASS")
