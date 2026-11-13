#!/usr/bin/env python3
"""Cycle-family polar-complex-structure parity and dihedral-reversal checks.
Every n=3,...,18 retained. Assumed Euclidean counting inner product / linearization.
"""
import csv,json,math
import numpy as np
from scipy.linalg import null_space
from pathlib import Path
ROOT=Path(__file__).resolve().parent;OUT=ROOT/'raw_trials';OUT.mkdir(exist_ok=True)
rows=[]
for n in range(3,19):
 P=np.zeros((n,n));R=np.zeros((n,n))
 for j in range(n):
  P[(j+1)%n,j]=1.
  R[(-j)%n,j]=1.
 A=P-P.T
 B=null_space(np.ones((1,n)))
 Av=B.T@A@B
 sv=np.linalg.svd(Av,compute_uv=False)
 parity='odd' if n%2 else 'even'
 pred=2*math.sin(math.pi/n) if n%2 else 0.
 symmetry=np.linalg.norm(R@P@R.T-P.T)
 reverse=np.linalg.norm(R@A@R.T+A)
 row=dict(n=n,parity=parity,contrast_dimension=n-1,rank_numeric=int(np.linalg.matrix_rank(Av,tol=1e-10)),
   min_singular=float(min(sv)),pred_min_singular=pred,
   rel_min_sing_discrepancy=abs(min(sv)-pred),reversal_P_residual=symmetry,reversal_A_residual=reverse,
   polar_J_square_residual='',polar_J_skew_residual='',polar_J_reversal_residual='')
 if n%2:
  # symmetric positive inverse root on contrast V: J=A(-A^2)^{-1/2}
  ev,U=np.linalg.eigh(-(Av@Av))
  assert min(ev)>0
  J=Av@(U@np.diag(1/np.sqrt(ev))@U.T)
  Rv=B.T@R@B
  row.update(polar_J_square_residual=float(np.linalg.norm(J@J+np.eye(n-1))),
    polar_J_skew_residual=float(np.linalg.norm(J.T+J)),
    polar_J_reversal_residual=float(np.linalg.norm(Rv@J@Rv.T+J)))
  assert max(row['polar_J_square_residual'],row['polar_J_skew_residual'],row['polar_J_reversal_residual'])<1e-12
 else: assert min(sv)<1e-12
 assert symmetry<1e-12 and reverse<1e-12
 rows.append(row)
with (OUT/'all_16_cycle_parity_tests.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
res={'status':'PASS','n_tested':'3-18 inclusive','cases':len(rows),'odd_invertible_count':sum(r['parity']=='odd' for r in rows),
'even_zero_singular_count':sum(r['parity']=='even' for r in rows),
'max_identity_residual':max(float(r['polar_J_square_residual']) for r in rows if r['parity']=='odd'),
'max_reverse_residual':max(float(r['polar_J_reversal_residual']) for r in rows if r['parity']=='odd'),
'all_cases_preserved':True,'scope':'Purely mathematical polar structure from a stipulated permutation representation; no physical dynamics'}
(ROOT/'RESULTS_CYCLES.json').write_text(json.dumps(res,indent=2)+'\n')
print(res)
