#!/usr/bin/env python3
"""Deterministic mathematical verifier for the November 7 scientific review.

Checks exact Choi-state counterexamples, graph spectra and cliques,
source-phase distinguishability, and certified finite-binomial thresholds.
Does not simulate laboratory data. Validation uses explicit exceptions (also under -O/-OO).
"""
from __future__ import annotations
from fractions import Fraction
from math import comb, log, ceil, sqrt
from pathlib import Path
import json, hashlib, itertools
import sympy as sp

def require(cond, message):
    if not bool(cond):
        raise RuntimeError(message)

def main():
    out={}
    I2=sp.eye(2)
    X=sp.Matrix([[0,1],[1,0]])
    Y=sp.Matrix([[0,-sp.I],[sp.I,0]])
    Z=sp.diag(1,-1)
    I4=sp.eye(4)
    def vnorm(U):
        return sp.Matrix([U[o,i]/2 for o in range(4) for i in range(4)])
    p=vnorm(I4)
    u=vnorm(sp.I*sp.kronecker_product(Z,I2))
    v=vnorm(sp.I*sp.kronecker_product(X,I2))
    def projection(w): return w*w.conjugate().T
    Pp,Pu,Pv=map(projection,[p,u,v])
    C1=(Pp+Pu)/4+Pv/2
    C2=projection(p-u)/4+Pv/2
    def ptr_out(C):
        return sp.Matrix(4,4,lambda i,j:sum(C[4*o+i,4*o+j] for o in range(4)))
    def output(C,psi):
        rho=projection(psi)
        return sp.Matrix(4,4,lambda o,q:4*sum(C[4*o+i,4*q+j]*rho[i,j]
                                            for i in range(4) for j in range(4)))
    for C in [C1,C2]:
        require(C==C.conjugate().T, 'non-Hermitian Choi')
        require(sp.simplify(sp.trace(C)-1)==0, 'Choi trace incorrect')
        require(sp.simplify(ptr_out(C)-I4/4)==sp.zeros(4), 'TP marginal incorrect')
        require(all(w>=0 for w in C.eigenvals()),'Choi not positive')
    require(sp.trace(C1*C1)==sp.Rational(3,8),'C1 purity incorrect')
    require(sp.simplify(sp.trace(C2*C2)-sp.Rational(1,2))==0,'C2 purity incorrect')
    for i in range(4):
        e=I4[:,i]
        require(sp.simplify(output(C1,e)-output(C2,e))==sp.zeros(4),'basis output differs')
    psi=sp.Matrix([1/sp.sqrt(2),0,1/sp.sqrt(2),0])
    M=sp.kronecker_product((I2+Y)/2,I2)
    y1=sp.simplify(sp.trace(M*output(C1,psi)))
    y2=sp.simplify(sp.trace(M*output(C2,psi)))
    require(y1==sp.Rational(1,2) and y2==sp.Rational(3,4),'Y+ rates wrong')
    require(sp.simplify(sp.trace(Pp*C1)-sp.Rational(1,4))==0 and sp.simplify(sp.trace(Pp*C2)-sp.Rational(1,4))==0,'h1')
    require(sp.simplify(sp.trace(Pu*C1)-sp.Rational(1,4))==0 and sp.simplify(sp.trace(Pu*C2)-sp.Rational(1,4))==0,'h0')
    out['choi']={'purity_C1':'3/8','purity_C2':'1/2','all_four_basis_outputs_equal':True,
                 'Y_plus_C1':'1/2','Y_plus_C2':'3/4','endpoint_phase_click':'1/4'}
    # Two sixteen-vertex graph constructions as Cayley graphs on Z4 x Z4.
    vertices=[(i,j) for i in range(4) for j in range(4)]
    shri_steps={(1,0),(3,0),(0,1),(0,3),(1,1),(3,3)}
    def adjacency(which):
        A=sp.zeros(16)
        for a,(i,j) in enumerate(vertices):
            for b,(k,l) in enumerate(vertices):
                if a==b: continue
                if which=='rook': A[a,b]=int((i==k) != (j==l))
                else:A[a,b]=int(((k-i)%4,(l-j)%4) in shri_steps)
        require(A==A.T and all(sum(A.row(i))==6 for i in range(16)),'graph defective')
        return A
    R=adjacency('rook'); T=adjacency('shrikhande')
    I16=sp.eye(16); J16=sp.ones(16)
    counts={'common_edges':0,'rook_only':0,'shrikhande_only':0,'common_nonedges':0}
    for i,j in itertools.combinations(range(16),2):
        if R[i,j] and T[i,j]:counts['common_edges']+=1
        elif R[i,j]:counts['rook_only']+=1
        elif T[i,j]:counts['shrikhande_only']+=1
        else:counts['common_nonedges']+=1
    require(counts=={'common_edges':32,'rook_only':16,'shrikhande_only':16,'common_nonedges':56},'pair counts incorrect')
    graph_stats={}
    for name,A in [('rook',R),('shrikhande',T)]:
        require(A*A==4*I16+2*J16,'strongly regular identity fails')
        P0=J16/16
        P4=(A+2*I16-8*P0)/4
        P8=I16-P0-P4
        for m,P in [(1,P0),(6,P4),(9,P8)]:
            require(P*P==P and sp.trace(P)==m,'spectral projector incorrect')
            require(all(P[i,i]==sp.Rational(m,16) for i in range(16)),'diagonal not uniform')
        four=sum(all(A[i,j] for i,j in itertools.combinations(c,2))
                  for c in itertools.combinations(range(16),4))
        graph_stats[name]={'laplacian_multiplicities':{'0':1,'4':6,'8':9},'cliques4':four}
    require(graph_stats['rook']['cliques4']==8 and graph_stats['shrikhande']['cliques4']==0,
            'clique count mismatch')
    # For vertices 0=(0,0),2=(0,2): rook edge, not Shrikhande edge.
    require(R[0,2]==1 and T[0,2]==0,'chosen graph pair is wrong')
    c=sp.symbols('c',real=True)
    p_rook=[(1+c)/16, (3+c)/8, (9-3*c)/16]
    p_shri=[(1+c)/16, (3-c)/8, (9+c)/16]
    require(all(sp.simplify(sum(p)-1)==0 for p in (p_rook,p_shri)),'not probability laws')
    require(sp.simplify(p_rook[1]-p_shri[1]-c/4)==0,'P4 difference wrong')
    require(sp.simplify(p_rook[2]-p_shri[2]+c/4)==0,'P8 difference wrong')
    # f4(s)=64s exp(-8s), f8(s)=256s exp(-16s) cross at s*=ln(4)/8.
    s0=sp.log(4)/8
    F4=1-sp.exp(-8*s0)*(1+8*s0)
    F8=1-sp.exp(-16*s0)*(1+16*s0)
    gamma_tv=sp.simplify(F8-F4)
    require(sp.simplify(gamma_tv-(3+4*sp.log(2))/16)==0,'Gamma TV wrong')
    affinity=lambda cc: (1+cc)/16+sp.sqrt(9-cc*cc)/8+sp.sqrt((9-3*cc)*(9+cc))/16
    cf=sp.Rational(1,10)
    aval=sp.N(affinity(cf),60)
    necessary=sp.log(sp.Rational(19,100))/(2*sp.log(aval))
    require(sp.N(necessary,15)>2379 and sp.N(necessary,15)<2380,'Hellinger count wrong')
    out['graphs']={**graph_stats,'edge_pair_class_counts':counts,'spectral_TV':'|cos(phase)|/4',
                   'continuous_scale_TV':'(3+4log(2))*|cos(phase)|/64',
                   'scale_TV_coefficient':str(sp.N(gamma_tv/4,17)),
                   'spectral_affinity_at_c_0_1':str(aval),
                   'necessary_95pct_power_attempts_c_0_1':2380}
    # Certified Bayesian min average errors for each specified fixed-horizon simple-law test.
    # Discrepancy in observation occurs with probability 1/denom per attempt, and
    # a successful informative outcome is Bernoulli(1/5) or Bernoulli(4/5).
    def conditional_error_twice_times_5m(m):
        z=sum(2*comb(m,k)*4**(m-k) for k in range(m//2+1,m+1))
        if m%2==0:z+=comb(m,m//2)*4**(m//2)
        return z
    def check_bayes(N,denom):
        H=100
        d=2*5**H*denom**N
        current=(denom-1)**N
        num=0
        for m in range(H+1):
            num+=comb(N,m)*current*conditional_error_twice_times_5m(m)*5**(H-m)
            current//=denom-1
        # Omitted mass bounded above by decreasing-geometric binomial tail.
        p_next=Fraction(comb(N,H+1)*current,denom**N)
        rat=Fraction(N-H-1,(H+2)*(denom-1))
        tail=p_next/(1-rat)
        below_05=(num*20<d)
        if below_05:
            require(20*(num*tail.denominator+d*tail.numerator)<d*tail.denominator,
                    'not certified below 0.05')
        else: require(20*num>d,'not certified above 0.05')
        return below_05, float(Fraction(num,d)),float(tail)
    thresholds={}
    for dnum,nlo,nhi in [(1000,7064,7065),(2000,14130,14131)]:
        lo=check_bayes(nlo,dnum);hi=check_bayes(nhi,dnum)
        require(lo[0] is False and hi[0] is True,'wrong crossing')
        thresholds[f'one_per_{dnum}']={'threshold_attempts':nhi,
            'error_preceding_N':f'{lo[1]:.15f}',
            'error_at_N':f'{hi[1]:.15f}',
            'omitted_tail_bound':f'{max(lo[2],hi[2]):.3e}',
            'certificate':'exact rational partial sums and rational geometric binomial tail bound'}
    out['simple_law_bayes_thresholds']=thresholds
    print(json.dumps(out,sort_keys=True,indent=2))

if __name__=='__main__':main()
