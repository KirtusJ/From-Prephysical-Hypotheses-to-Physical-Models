"""Deterministic verification of conditional quantum-readout bounds.
Research direction: Kirtus Justus. Mathematical assistance: ChatGPT (OpenAI).
November 7, 2026, Vancouver, BC. No measured or synthetic shots.
"""
import math
import numpy as np

def require(condition, message):
    if not condition:
        raise ArithmeticError(message)

s=131/320
h=0.99
q=81711338569043/224995905216000
require(q < s*h, "Verification failed")
ell=0.01
k=(s*h-math.sqrt(s*h*q))**2/(s*h*(1-h))
d=s+k
r=1-d
I=np.eye(2,dtype=complex)
X=np.array([[0,1],[1,0]],dtype=complex)
Y=np.array([[0,-1j],[1j,0]],dtype=complex)
Z=np.diag([1,-1]).astype(complex)
I4=np.eye(4,dtype=complex)
ket=lambda A:A.reshape(-1)/2
projector=lambda v:np.outer(v,v.conj())
p=ket(I4)
u=ket(1j*np.kron(Z,I))
v=ket(1j*np.kron(X,I))
e=math.sqrt(h)*p+math.sqrt(1-h)*u
E=projector(e)
F=projector(v)
P=projector(p)
R=np.eye(16)-P

# Check near-boundary two-sign unitary channels and first-qubit blindness.
f=r-ell
Us=(math.sqrt(s)*I-1j*math.sqrt(k)*Z+1j*math.sqrt(f)*X)/math.sqrt(d+f)
target=np.array([math.sqrt(6/13),math.sqrt(7/13)],complex)
col=Us.conj().T@target
col*=np.exp(-1j*np.angle(col[0]))
a,b=col
N=np.array([[a.real,b.conjugate()],[b,-a.real]],complex)
Vs=[np.kron(Us,I) @ (math.sqrt(1-ell)*I4+sgn*1j*math.sqrt(ell)*np.kron(N,X)) for sgn in (+1,-1)]
chs=[projector(ket(V)) for V in Vs]
readout=lambda rho:float(np.trace(E@rho).real)
first=lambda out:np.trace(out.reshape(2,2,2,2),axis1=1,axis2=3)
last0=np.array([1,0,0,0],complex)
for V,rho in zip(Vs,chs):
    require(np.linalg.norm(V.conj().T@V-I4)<1e-13, "Verification failed")
    require(abs(np.trace(F@rho)-f)<1e-13, "Verification failed")
    require(abs(np.trace(P@rho)-s)<1e-13, "Verification failed")
    require(np.linalg.norm(np.trace(rho.reshape(4,4,4,4),axis1=0,axis2=2)-I4/4)<1e-13, "Verification failed")
    require(abs(readout(rho)-q)<1e-13, "Verification failed")
    require(abs(np.trace(E@P@rho@R)-np.trace(E@P@chs[0]@R))<1e-13, "Verification failed")
out_plus=Vs[0]@last0
out_minus=Vs[1]@last0
rho_plus=projector(out_plus)
rho_minus=projector(out_minus)
require(np.linalg.norm(first(rho_plus)-first(rho_minus))<1e-13, "Verification failed")
Yplus=float(np.trace(np.kron(I,Y)@rho_plus).real)
Yminus=float(np.trace(np.kron(I,Y)@rho_minus).real)
require(abs(Yplus+Yminus)<1e-13, "Verification failed")
require(abs(Yplus-2*a.real*math.sqrt(ell*(1-ell)))<1e-13, "Verification failed")
half=(chs[0]+chs[1])/2
require(abs(np.trace(half@half).real-(1-2*ell*(1-ell)))<1e-13, "Verification failed")

# Balanced phase-offset trace-distance stability bound, derived for arbitrary states.
delta=math.pi/3
qref=(2*math.sqrt(s*h)-math.sqrt(q))**2
shared=(1+math.cos(delta))/2*(qref-q)
coh=math.sin(delta)*math.sqrt(h*(1-h))
Dcritical=shared/coh
require(shared>0 and 0<Dcritical<1, "Verification failed")

# Independent adverse-state example in dimension two. Uses a single positive effect.
b0=(1-s)*(1-h)
C=(q-s*h-b0)/(2*math.sqrt(s*(1-s)*h*(1-h)))
require(-1<C<1, "Verification failed")
gamma=math.acos(C)
p2=np.array([1,0],complex)
u2=np.array([0,1],complex)
e2=math.sqrt(h)*p2+math.sqrt(1-h)*u2
E2=projector(e2)
psi=lambda sign:math.sqrt(s)*p2+math.sqrt(1-s)*np.exp(sign*1j*gamma)*u2
rho_plus2=projector(psi(-1))
rho_minus2=projector(psi(+1))
ph=lambda offset:np.diag([1,np.exp(1j*(math.pi+offset))])
born=lambda eff,rho:float(np.trace(eff@rho).real)
dplus=born(E2,ph(+delta)@rho_plus2@ph(+delta).conj().T)-born(E2,rho_plus2)
dminus=born(E2,ph(-delta)@rho_minus2@ph(-delta).conj().T)-born(E2,rho_minus2)
D=float(np.sum(abs(np.linalg.eigvalsh(rho_plus2-rho_minus2)))/2)
require(abs(born(E2,rho_plus2)-q)<1e-13, "Verification failed")
require(abs(born(E2,rho_minus2)-q)<1e-13, "Verification failed")
require(abs((dplus+dminus)/2-(-0.001806421220915608))<1e-12, "Verification failed")
require((dplus+dminus)/2 >= shared-coh*D-1e-13, "Verification failed")
require(D>Dcritical, "Verification failed")

print('Near-boundary residual ell:',f'{ell:.8f}')
print('Minimum purity, two-sign family:',f'{np.trace(half@half).real:.12f}')
print('Pure endpoint purities:',*(f'{np.trace(rho@rho).real:.12f}' for rho in chs))
print('First-qubit reduced-output difference:',f'{np.linalg.norm(first(rho_plus)-first(rho_minus)):.3e}')
print('Second-qubit Y expectation, plus/minus:',f'{Yplus:.12f}',f'{Yminus:.12f}')
print('Balanced +60/-60 shared-state lower contrast:',f'{shared:.15f}')
print('Group-state trace-distance coefficient:',f'{coh:.15f}')
print('Sufficient strict-rise if group half-trace-distance below:',f'{Dcritical:.15f}')
print('Adverse density witness trace distance:',f'{D:.15f}')
print('Adverse density witness mean contrast:',f'{(dplus+dminus)/2:.15f}')
print('All deterministic assertions passed.')
