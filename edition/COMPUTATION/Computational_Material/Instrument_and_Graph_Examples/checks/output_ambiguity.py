#!/usr/bin/env python3
"""Deterministic checks of a fixed-readout equivalence family.

Research direction and responsibility: Kirtus Justus.
Mathematical/computational assistance: ChatGPT (OpenAI).
7 November 2026, Vancouver PCT (UTC-7).
This is model mathematics, not experimental data or a physical-source claim.
"""
from __future__ import annotations
import hashlib
import numpy as np
from fractions import Fraction


def check(condition, message):
    if not condition:
        raise ArithmeticError(message)


def close(a, b, message, atol=2e-12):
    check(np.max(np.abs(a-b)) <= atol, message)

I2=np.eye(2,dtype=complex)
X=np.array([[0,1],[1,0]],complex)
Y=np.array([[0,-1j],[1j,0]],complex)
Z=np.diag([1,-1]).astype(complex)
P2=[('I',I2),('X',X),('Y',Y),('Z',Z)]

def ket(A): return A.reshape(16)/2

def proj(x): return np.outer(x,x.conj())

def marginal_reference(rho):
    return np.trace(rho.reshape(4,4,4,4),axis1=0,axis2=2)

def marginal_output(rho):
    return np.trace(rho.reshape(4,4,4,4),axis1=1,axis2=3)

def prepared_output(rho):
    return 4*rho.reshape(4,4,4,4)[:,0,:,0]

def trace(rho): return np.trace(rho)

s=float(Fraction(131,320)); h=float(Fraction(99,100))
q=float(Fraction(81711338569043,224995905216000))
a=s*h
k=(a-np.sqrt(a*q))**2/(s*h*(1-h))
d=s+k; r=1-d;f=r/2;ell=r-f
p=ket(np.eye(4));u=ket(1j*np.kron(Z,I2));v=ket(1j*np.kron(X,I2))
theta=(np.sqrt(k)*p+np.sqrt(s)*u)/np.sqrt(d)
eta=(np.sqrt(s)*p-np.sqrt(k)*u)/np.sqrt(d)
B=np.eye(16)-proj(theta)
E=proj(np.sqrt(h)*p+np.sqrt(1-h)*u)
match=proj(p)
F=proj(v)

spectators=[]
for l,A in P2:
  for m,C in P2:
    if (l,m) not in {('I','I'),('Z','I'),('X','I')}:
      spectators.append(((l,m),ket(np.kron(A,C))))
check(len(spectators)==13,'spectator count')
S0=[a for a in spectators if a[0][0] in ('I','Z')]
S1=[a for a in spectators if a[0][0] in ('X','Y')]
check(len(S0)==6 and len(S1)==7,'first-qubit partition')
D=sum((proj(a[1]) for a in spectators),np.zeros((16,16),complex))
close(D,np.eye(16)-proj(p)-proj(u)-proj(v),'spectator projection')


def state(weights):
  rho=d*proj(eta)+f*proj(v)
  for key,vect in spectators:
    rho+=weights[key]*proj(vect)
  return rho

weights_uniform={key:ell/13 for key,_ in spectators}
weights_concentrated={key:0. for key,_ in spectators}
weights_concentrated[S0[0][0]]=6*ell/13
weights_concentrated[S1[0][0]]=7*ell/13
rho_uniform=state(weights_uniform)
rho_concentrated=state(weights_concentrated)
# A stronger example fixes the complete TWO-QUBIT output on |00>.
# Pauli operators differing only by phases on |00> produce identical output
# density matrices, so their mixture weights remain invisible to this input.
output_groups={}
for (L,C),vect in spectators:
    key=(int(L in ('X','Y')), int(C in ('X','Y')))
    output_groups.setdefault(key,[]).append((L,C))
check([len(output_groups[(a,b)]) for a,b in ((0,0),(0,1),(1,0),(1,1))]==[2,4,3,4],
      'two-qubit output groups')
weights_joint={key:0. for key,_ in spectators}
for key, members in output_groups.items():
    weights_joint[members[0]]=len(members)*ell/13
rho_joint=state(weights_joint)

for label,rho in [('uniform',rho_uniform),('concentrated',rho_concentrated),('joint-output-equivalent',rho_joint)]:
  close(rho,rho.conj().T,label+' Hermitian')
  check(min(np.linalg.eigvalsh(rho))>=-3e-13,label+' positive')
  close(trace(rho),1.,label+' trace')
  close(marginal_reference(rho),np.eye(4)/4,label+' trace preserving')
  close(marginal_output(rho),np.eye(4)/4,label+' unital')
  close(trace(match@rho),s,label+' match population')
  close(trace(F@rho),f,label+' F population')
  close(rho@theta,np.zeros(16),label+' null ray')
  for phase in [0,np.pi/7,np.pi/2,np.pi,4*np.pi/3,1.8*np.pi]:
    U=match+np.exp(1j*phase)*(np.eye(16)-match)
    Born=trace(E@U@rho@U.conj().T)
    expected=abs(np.sqrt(s*h)-np.exp(1j*phase)*np.sqrt((1-h)*k))**2
    close(Born,expected,label+' phase curve')
  output=prepared_output(rho)
  first=np.trace(output.reshape(2,2,2,2),axis1=1,axis2=3)
  close(first,np.diag([d+6*ell/13,f+7*ell/13]),label+' full first-qubit output')

J=d*d+f*f+ell*ell/13
Umax=d*d+f*f+(85./169)*ell*ell
Ujoint=d*d+f*f+(45./169)*ell*ell
close(trace(rho_uniform@rho_uniform),J,'simplex minimum purity')
close(trace(rho_concentrated@rho_concentrated),Umax,'simplex maximum purity')
close(trace(rho_joint@rho_joint),Ujoint,'joint-output simplex maximum purity')
close(prepared_output(rho_uniform),prepared_output(rho_joint),'full two-qubit output on |00>')
for t in (0., .25, .58, 1.):
  interp=(1-t)*rho_uniform+t*rho_joint
  close(trace(interp@interp),J+t*t*(Ujoint-J),'nine-dimensional simplex purity')
for t in [0,.17,.37,.62,1.]:
  rho=(1-t)*rho_uniform+t*rho_concentrated
  expected=J+t*t*(Umax-J)
  close(trace(rho@rho),expected,'purity interpolation')
  close(marginal_reference(rho),np.eye(4)/4,'interpolated TP')

# On the support of the saturated phase curve, the phase effects all lie on one ray.
for phase in [0,.2,.81,1.9,np.pi,5.5]:
  U=match+np.exp(1j*phase)*(np.eye(16)-match)
  restricted=B@U.conj().T@E@U@B
  scalar=np.vdot(eta,restricted@eta)
  close(restricted,scalar*proj(eta),'phase effect collapse')

# Lower bounds on unidentifiable tangent dimensions, counting linear constraints only.
# Hermitian operators on support B: 15**2=225 real dimensions.
# TP: <=16 real constraints. Additional fixed eta and F populations: <=2.
# Full tomography on the first output for one product input: <=3.
# Unitality, if imposed, adds <=15 extra conditions, because trace is already fixed.
check(15**2-16-2-3==204,'CPTP dimension lower bound')
check(15**2-16-2-3-15==189,'unital dimension lower bound')

# Numerical rank diagnostic only; the rigorous lower bound uses constraint counting.
pauli4=[np.kron(A,C) for _,A in P2 for _,C in P2]
matrices=[np.kron(np.eye(4),H) for H in pauli4]
matrices.append(match)
for phase in [0,np.pi/2,np.pi,3*np.pi/2]:
  U=match+np.exp(1j*phase)*(np.eye(16)-match)
  matrices.append(U.conj().T@E@U)
matrices.append(F)
ref00=np.diag([1.,0.,0.,0.]).astype(complex)
for A in (X,Y,Z):
  matrices.append(4*np.kron(np.kron((I2+A)/2,I2),ref00))

def gram_rank(Ms):
  projected=[B@op@B for op in Ms]
  gram=np.array([[np.trace(left@right).real for right in projected] for left in projected])
  return sum(np.linalg.svd(gram,compute_uv=False)>1e-8)

rank_tp=gram_rank(matrices)
rank_unital=gram_rank(matrices+[np.kron(H,np.eye(4)) for H in pauli4[1:]])
check(rank_tp==21 and rank_unital==36, 'numerical linear constraint rank')

print('Original two-mode and channel models retain separate observation maps.')
print('Fixed phase effects collapse to one ray on the supported 15D Hilbert space.')
print('Trace-preserving local compatible-family dimension >= 204 real.')
print('Numerical constraint ranks (TP / TP+unital) = %d / %d.' % (rank_tp,rank_unital))
print('Unital trace-preserving local compatible-family dimension >= 189 real.')
print('Explicit mixed-unitary spectator-weight simplex dimension = 11 real.')
print('First-qubit preserving / flipping spectator directions = 6 / 7.')
print('Explicit mixed-unitary SAME-TWO-QUBIT-OUTPUT simplex dimension = 9 real.')
print('Computational-output spectator groups have sizes 2 / 4 / 3 / 4.')
print('At f=r/2: d = %.15f, r = %.15f, f = %.15f' % (d,r,f))
print('Eleven-dimensional first-output simplex purity interval = [%.15f, %.15f].' % (J,Umax))
print('Nine-dimensional whole-output simplex purity interval = [%.15f, %.15f].' % (J,Ujoint))
print('Exact phase, F, both Choi marginals and full first-output tomography match.')
print('All model mathematics checks passed; no physical trials.')
