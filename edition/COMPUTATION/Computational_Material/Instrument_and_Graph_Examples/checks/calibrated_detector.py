"""Exact verification of four-input Choi-weight feasibility with a common
calibrated binary effect on the FIRST output qubit.

All inputs and examples are mathematical, not experimental data.
Research direction and responsibility: Kirtus Justus.
mathematical and computational assistance: ChatGPT (OpenAI).
November 7, 2026, Vancouver, PCT (UTC-7).
Dependencies: Python 3 and SymPy.
"""
from fractions import Fraction as F
from decimal import Decimal, localcontext
from math import sqrt
import sympy as sp


def need(condition, label):
    if not bool(condition):
        raise ArithmeticError(label)


def q(n, d=1):
    return sp.Rational(n, d)


def root_discrepancy(rows, a, b):
    return sum((sp.sqrt(rows[a][j])-sp.sqrt(rows[b][j]))**2 for j in (0,1))


def project_local(K):
    # Basis |first bit, second bit> = 00,01,10,11.
    A = sp.Matrix(2,2,lambda i,j:(K[2*i,2*j]+K[2*i+1,2*j+1])/2)
    return sp.kronecker_product(A, sp.eye(2))


def witness():
    # Spectral populations in eigenbasis of E on the first output qubit.
    spectral = [[q(9,100),q(4,100)], [q(4,100),q(9,100)],
                [q(16,100),q(9,100)],[q(9,100),q(16,100)]]
    success=[sum(row) for row in spectral]
    S=sum(success)
    L,U=q(1,5),q(4,5)
    gap=U-L
    # Reference calculations exactly, prior to any Kraus representation.
    z=[L*s+gap*v[0] for s,v in zip(success,spectral)]
    need(success == [q(13,100),q(13,100),q(1,4),q(1,4)], 'success')
    need(z == [q(8,100),q(5,100),q(146,1000),q(104,1000)], 'click rates')
    recon=[[(z[i]-L*success[i])/gap,(U*success[i]-z[i])/gap] for i in range(4)]
    need(recon == spectral,'calibrated inversion')
    D01=sp.simplify(root_discrepancy(spectral,0,1))
    D23=sp.simplify(root_discrepancy(spectral,2,3))
    need(D01 == q(1,50) and D23 == q(1,50), 'sharp spectral discrepancies')
    wmax=sp.simplify(1-(D01+D23)/(2*S))
    need(wmax == q(37,38), 'maximal local Choi weight')
    # Four exact Kraus matrices. Environment labels are pair × spectral outcome.
    ks=[]
    for b in (0,1):
        for j in (0,1):
            K=sp.zeros(4)
            for t in (0,1):
                i=2*b+t
                K[2*j+t,i]=sp.sqrt(spectral[i][j])
            ks.append(K)
    H=sum((K.H*K for K in ks),sp.zeros(4))
    need(H == sp.diag(*success),'trace nonincrease, exact success effect')
    need((sp.eye(4)-H).is_positive_semidefinite,'effect <= identity')
    en=sp.diag(U,U,L,L)
    no=sp.eye(4)-en
    for i in range(4):
        ket=sp.eye(4)[:,i]
        got_success=sum(((K*ket).H*(K*ket))[0] for K in ks)
        got_click=sum(((K*ket).H*en*(K*ket))[0] for K in ks)
        got_no=sum(((K*ket).H*no*(K*ket))[0] for K in ks)
        need(got_success==success[i] and got_click==z[i] and got_no==success[i]-z[i],
             'Born rates input '+str(i))
    Scheck=sum(sp.trace(K.H*K) for K in ks)
    Wcheck=sum(sp.trace(project_local(K).H*project_local(K)) for K in ks)
    need(Scheck==S and sp.simplify(Wcheck/Scheck)==wmax,'Choi local weight')
    # Compare the correct spectral test to use of raw click/no click values as if projective.
    raw=[[z[i],success[i]-z[i]] for i in range(4)]
    D_raw=sp.N(root_discrepancy(raw,0,1)+root_discrepancy(raw,2,3),45)
    w_raw=sp.N(1-D_raw/(2*S),45)
    need(D_raw < D01+D23 and w_raw > wmax,'strict degradation')
    # Predictable test score on the ACTUAL imperfect-detector output bit, not spectral labels.
    pi=[q(3,8),q(3,8),q(1,8),q(1,8)]
    slopes={(0,0):q(2,3),(0,1):q(3,2),(1,0):q(3,4),(1,1):q(4,3)}
    d={}
    for b in (0,1):
        for j in (0,1):
            t=slopes[b,j]
            d[2*b,j]=1-t
            d[2*b+1,j]=1-1/t
    eps=1-wmax
    kappas={}
    for i in range(4):
        for y in (0,1):
            kappas[i,y]=sp.simplify(d[i,1]+(q(y)-L)/gap*(d[i,0]-d[i,1]))
    expectation=sum(kappas[i,1]*z[i]+kappas[i,0]*(success[i]-z[i]) for i in range(4)) - 2*eps*S
    need(sp.simplify(expectation)==0,'mean-zero null score')
    stake=q(1,100)
    factors=[1+stake*(kappas[i,y]-2*eps)/pi[i] for i in range(4) for y in (0,1)]
    need(min(factors)>0,'strict positivity of stake factors')
    need(1+stake*q(0)>=0,'failure factor')
    # Degenerate POVM E = L I has no spectral readout information beyond successes.
    Ddeg=sum((sp.sqrt(success[2*b])-sp.sqrt(success[2*b+1]))**2 for b in (0,1))
    need(Ddeg==0,'degenerate detector control')
    # Common spectrum is NOT a common effect. Identity channel with rotated effects violates
    # the w=1 bound without contradicting it: premise of common effect is broken.
    E0=sp.diag(U,U,L,L)
    E1=sp.diag(L,L,U,U)
    rho0=sp.eye(4)[:,0]
    rho1=sp.eye(4)[:,1]
    need((rho0.H*E0*rho0)[0]==U and (rho1.H*E1*rho1)[0]==L,'rotated detector control')
    print('PROJECTIVE SOURCE REPLAY: D01=D23=1/50, S=19/25, wmax=37/38.')
    print('CALIBRATED EFFECT: eigenvalues L=1/5 U=4/5; all four click rates match exactly.')
    print('RAW SUCCESS-CLICK DISCREPANCY:',format(float(D_raw),'.15f'))
    print('RAW PROJECTIVE-ASSUMED MAX WEIGHT:',format(float(w_raw),'.15f'))
    print('CORRECT CALIBRATED MAX WEIGHT: 37/38 =',format(float(wmax),'.15f'))
    print('EXACT KRAUS CERTIFICATE: trace nonincrease, effect, four-input Born rates, local weight pass.')
    print('ACTUAL-BIT SEQUENTIAL FACTOR: zero conditional mean; positive factors at stake 1/100.')
    print('NEGATIVE CONTROLS: scalar effect loses spectral information; arm-dependent effects violate premises.')
    print('ALL EXACT AND DETERMINISTIC CHECKS PASSED.')


if __name__=='__main__':
    witness()
