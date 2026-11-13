#!/usr/bin/env python3
"""Adaptive 3-step projective-instrument indistinguishability control for K_3.
Single-actor numerical implementation; mathematical result independently proved in PDF.
"""
import itertools,csv,json,math
import numpy as np
from pathlib import Path
ROOT=Path(__file__).resolve().parent
OUT=ROOT/'raw_trials';OUT.mkdir(exist_ok=True)
rng=np.random.default_rng(2026111204)

def unit():
 v=rng.normal(size=3);return v/np.linalg.norm(v)
def rot():
 Q,R=np.linalg.qr(rng.normal(size=(3,3)));Q=Q@np.diag(np.sign(np.diag(R)))
 if np.linalg.det(Q)<0: Q[:,0]*=-1
 return Q

def tensor3(v):return np.einsum('i,j,k->ijk',v,v,v)
def tau(T):return np.einsum('ijj->i',T)
def F(T,m):return (1+float(m@tau(T)))/2

s3=math.sqrt(3)
A=np.zeros((3,3,3))
narr=[np.array([1.,0,0]),np.array([-0.5,s3/2,0]),np.array([-0.5,-s3/2,0])]
B=sum(tensor3(v) for v in narr)/3
assert np.linalg.norm(tau(B))<1e-15
assert abs(B[0,0,0]-0.25)<1e-15

def push(T,branch,R,m):
 # Local rotation followed by projective binary test, output is a re-prepared eigenstate.
 Trot=np.einsum('ia,jb,kc,abc->ijk',R,R,R,T,optimize=True)
 prob=F(Trot,branch*m)
 return prob, tensor3(branch*m)

def push_qubit(v,branch,R,m):
 vrot=R@v
 return (1+float(branch*m@vrot))/2,branch*m
rows=[]; max_error=0.
for trial in range(96):
 # Adaptive control settings differ at each of 1+2+4 histories, not merely fixed settings.
 controls={h:(rot(),unit()) for l in range(3) for h in itertools.product([-1,1],repeat=l)}
 total=0.
 for word in itertools.product([-1,1],repeat=3):
  pA=pB=pQ=1.
  stateA=A.copy();stateB=B.copy();stateQ=np.zeros(3)
  for stage,branch in enumerate(word):
   R,m=controls[word[:stage]]
   a,stateA=push(stateA,branch,R,m)
   b,stateB=push(stateB,branch,R,m)
   c,stateQ=push_qubit(stateQ,branch,R,m)
   pA*=a;pB*=b;pQ*=c
  dAB=abs(pA-pB);dAQ=abs(pA-pQ);dBQ=abs(pB-pQ)
  max_error=max(max_error,dAB,dAQ,dBQ)
  rows.append(dict(trial=trial,word=''.join('+' if x==1 else '-' for x in word),p_A=pA,p_B=pB,p_qubit=pQ,abs_A_minus_B=dAB,abs_A_minus_Q=dAQ,abs_B_minus_Q=dBQ))
  total+=pA
 assert abs(total-1)<1e-12,total
assert max_error<1e-12,max_error
with (OUT/'all_768_adaptive_projective_words.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
result={'status':'PASS','scope':'three-stage finite adaptive rotations and binary projective measure-reprepare instruments; K_3 and standard qubit with same tau','seed':2026111204,'trials':96,'rows':len(rows),'maximum_abs_probability_residual':max_error,'exact_additional_effect_gap':'1/8','all_rows_retained':True,'limits':'does not cover arbitrary quantum POVMs, general quantum instruments, tensor product dynamics or physical readout'}
(ROOT/'RESULTS_INSTRUMENT.json').write_text(json.dumps(result,indent=2)+'\n')
print(result)
