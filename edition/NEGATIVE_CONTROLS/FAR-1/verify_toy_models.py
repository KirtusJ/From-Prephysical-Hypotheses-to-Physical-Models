#!/usr/bin/env python3
"""Selected, separately reproducible FAR-1 toy mathematical checks. No physical interpretation."""
import math,json
import numpy as np
from scipy.linalg import expm
from functools import reduce
from itertools import product
H=np.array([[1,1],[1,-1]],complex)/math.sqrt(2)
P0=np.diag([1,0]).astype(complex);P1=np.diag([0,1]).astype(complex)
r={}
for kappa,phase in product((0,.25,1),(0,math.pi/2,math.pi)):
 u=H@np.diag([1,np.exp(1j*phase)])@H
 # correct sequence: |0> -> H -> Pphi -> Dk -> H
 psi=np.diag([1,np.exp(1j*phase)])@H@np.array([1,0],complex)
 rho=np.outer(psi,psi.conj());rho=(1-kappa)*rho+kappa*(P0@rho@P0+P1@rho@P1)
 p0=np.real(np.trace(P0@H@rho@H.conj().T))
 target=(1+(1-kappa)*math.cos(phase))/2
 assert abs(p0-target)<1e-12
 r[f'p0_k{kappa}_phase{round(phase,5)}']=round(float(p0),10)
I=np.eye(2,dtype=complex);X=np.array([[0,1],[1,0]],complex);Z=np.diag([1,-1]).astype(complex)
N=4;d=2**N
tensor=lambda ops:reduce(np.kron,ops)
Xops=[tensor([X if i==j else I for i in range(N)]) for j in range(N)]
Zops=[tensor([Z if i==j else I for i in range(N)]) for j in range(N)]
Hfield=sum(Xops);Hedges=sum(Zops[i]@Zops[(i+1)%N] for i in range(N))
Q=sum((np.eye(d)-op)/2 for op in Zops)/N
D=np.array([[(1-.35)**((i^j).bit_count()) for j in range(d)] for i in range(d)])
rho=np.zeros((d,d),complex);rho[0,0]=1;a=1;trajectory=[]
for n in range(6):
 q=float(np.real(np.trace(Q@rho)));purity=float(np.real(np.trace(rho@rho)))
 assert abs(np.trace(rho)-1)<1e-12 and np.linalg.eigvalsh(rho).min()>-1e-10
 trajectory.append([n,round(a,9),round(q,9),round(purity,9)])
 U=expm(-.1j*(-.6/a*Hedges-Hfield));assert np.linalg.norm(U.conj().T@U-np.eye(d))<1e-11
 rho=(U@rho@U.conj().T)*D
 a+=.1*a*math.sqrt(.01/a**4+.30/a**3+.69+.05*q/a**3)
r['four_site_trajectory']=trajectory
qQ=(2+math.sqrt(2))/4;p=199/200;gamma=85/128;n=28
alpha=qQ**n+n*gamma*(1-qQ)*qQ**(n-1)
power=p**n+n*gamma*(1-p)*p**(n-1)
assert alpha<.05 and power>.95
r['B_randomized_28_size']=alpha;r['B_randomized_28_power']=power
r['B_fixed19_quantum_size']=qQ**19
r['two_site_full_dephasing_Hadamard_T']=(np.abs(H)**2).tolist()
with open('/mnt/data/toy_universe_session_close/verified_toy_results.json','w') as f:json.dump(r,f,indent=2)
print('SELECTED TOY CHECKS PASS',trajectory[-1],alpha,power)
