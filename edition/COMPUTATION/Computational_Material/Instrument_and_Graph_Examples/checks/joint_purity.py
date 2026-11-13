"""Deterministic audit of a joint 3-axis purity bound for a specified Choi process.
Research direction and responsibility: Kirtus Justus. Calculation assistance: ChatGPT (OpenAI).
November 7, 2026, Vancouver (UTC-7).
No hardware data, simulated trials, or fictional-model inputs are used.
"""
import numpy as np
from math import sqrt, pi, cos
from fractions import Fraction as F

def require(ok, reason):
    if not bool(ok):
        raise ValueError(reason)

def near(actual, expected, reason, tol=4e-12):
    require(np.max(np.abs(np.asarray(actual)-np.asarray(expected))) < tol, reason)

I2=np.eye(2, dtype=complex)
X=np.array([[0,1],[1,0]], dtype=complex)
Y=np.array([[0,-1j],[1j,0]], dtype=complex)
Z=np.diag([1,-1]).astype(complex)
I4=np.eye(4, dtype=complex)
I16=np.eye(16, dtype=complex)
ket=lambda U:U.reshape(16)/2
project=lambda a:np.outer(a,a.conj())
Tr=lambda A:np.trace(A).real
partial_out=lambda A:np.trace(A.reshape(4,4,4,4), axis1=0, axis2=2)
s=131/320;h=.99;q=81711338569043/224995905216000
k=(s*h-sqrt(s*h*q))**2/(s*h*(1-h));d=s+k;r=1-d
p,u,v=[ket(z) for z in (I4,1j*np.kron(Z,I2),1j*np.kron(X,I2))]
eta=(sqrt(s)*p-sqrt(k)*u)/sqrt(d)
theta=(sqrt(k)*p+sqrt(s)*u)/sqrt(d)
Peta,Pv,Ptheta=map(project,(eta,v,theta))
B=I16-Ptheta
D=I16-project(p)-project(u)-Pv
P00=np.diag([1,0,0,0]).astype(complex)

def tangent_projection(M):
    """Hilbert-Schmidt projection onto supported traceless population/TP tangent space."""
    K=B@M@B
    K-=Tr(K@Peta)*Peta
    K-=Tr(K@Pv)*Pv
    K-=Tr(K@D)/13*D
    L=partial_out(K)
    require(abs(np.trace(L))<3e-13, 'traceless marginal')
    return K-(2/7)*B@np.kron(I4,L)@B, K, L


def main():
    axes=(Z,X,Y)
    operators=[]; tangents=[]; M1=[]; marginals=[]
    for Q in axes:
        MQ=4*np.kron(np.kron((I2+Q)/2,I2),P00)
        A,K,L=tangent_projection(MQ)
        operators.append(MQ); tangents.append(A); M1.append(K); marginals.append(L)
        near(A,A.conj().T,'Hermitian observable')
        near(partial_out(A),np.zeros((4,4)),'trace preservation tangent')
        near(Tr(Peta@A),0,'eta population')
        near(Tr(Pv@A),0,'v population')
        near(Tr(D@A),0,'spectator population')
        near(np.linalg.norm(A@theta),0,'null sector')

    gram=np.array([[Tr(a@b) for b in tangents] for a in tangents])
    target=np.diag([F(1230,91),F(97,7),F(97,7)]).astype(float)
    near(gram,target,'exact projected Gram matrix')
    gram1=np.array([[Tr(a@b) for b in M1] for a in M1])
    gramL=np.array([[Tr(a@b) for b in marginals] for a in marginals])
    target1=np.array([[F(276,13),9,9],[9,F(49,2),F(21,2)],[9,F(21,2),F(49,2)]],dtype=float)
    targetL=np.array([[27,F(63,2),F(63,2)],[F(63,2),F(149,4),F(147,4)],[F(63,2),F(147,4),F(149,4)]],dtype=float)
    near(gram1,target1,'pre-TP Gram');near(gramL,targetL,'marginal Gram')
    near(gram1-(2/7)*gramL,gram,'tangent projection formula')

    # At an interior F population, the lower-purity state is positive on its support.
    f=r/2
    rho0=d*Peta+f*Pv+(r-f)*D/13
    J=d*d+f*f+(r-f)**2/13
    p0=np.array([d+6*(r-f)/13, 0.5,0.5])
    near(Tr(rho0@rho0),J,'minimum purity')
    near(partial_out(rho0),I4/4,'trace-preserving marginal')
    near([Tr(M@rho0) for M in operators],p0,'reference probabilities')
    # Independent nonzero transverse and longitudinal deviations.
    shifts=np.array([0.005,0.007,-0.004])
    rho=rho0+sum((shifts[j]/gram[j,j])*tangents[j] for j in range(3))
    require(np.linalg.eigvalsh(rho).min()>-1e-12,'positivity')
    near(Tr(rho),1,'trace one');near(partial_out(rho),I4/4,'TP marginal')
    near([Tr(M@rho) for M in operators],p0+shifts,'three independent measurements')
    near(Tr(rho@rho),J+sum(shifts[j]**2/gram[j,j] for j in range(3)),'local equality')
    # The same fixed phase readout remains unchanged: the entire visible sector is fixed.
    E=project(sqrt(h)*p+sqrt(1-h)*u)
    E0=lambda phase:Tr((project(p)+np.exp(1j*phase)*(I16-project(p))).conj().T@E@(project(p)+np.exp(1j*phase)*(I16-project(p)))@rho0)
    E1=lambda phase:Tr((project(p)+np.exp(1j*phase)*(I16-project(p))).conj().T@E@(project(p)+np.exp(1j*phase)*(I16-project(p)))@rho)
    for phase in [0,pi/7,pi/2,pi,1.33*pi,2*pi]:
        near(E1(phase),E0(phase),'full phase curve retained')
    near(Tr(Pv@rho),f,'second outcome retained')
    print('Projected Gram diagonal:', *(f'{v:.12f}' for v in np.diag(gram)))
    print('Purity coefficients:', *(f'{1/v:.12f}' for v in np.diag(gram)))
    print('Interior F probability:', f'{f:.12f}')
    print('Three-axis reference rates:', *(f'{v:.12f}' for v in p0))
    print('Three-axis deviations:', *(f'{v:.12f}' for v in shifts))
    print('Attained purity bound:',f'{Tr(rho@rho):.15f}')
    print('Positive Choi perturbation and six off-grid phase checks passed.')

if __name__=='__main__':
    main()
