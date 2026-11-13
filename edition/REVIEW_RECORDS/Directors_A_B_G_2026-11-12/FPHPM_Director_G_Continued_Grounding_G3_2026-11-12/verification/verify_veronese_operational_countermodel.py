#!/usr/bin/env python3
"""Self-contained, deterministic tests for the odd Veronese GPT countermodel.
No imported qubit is asserted to emerge. Scripts are internal checks, not a proof verifier.
All trials retained, including small residuals and boundary results.
"""
from __future__ import annotations
import csv, json, math, itertools, hashlib
from pathlib import Path
import numpy as np
import sympy as sp

ROOT=Path(__file__).resolve().parent
OUT=ROOT/'raw_trials'; OUT.mkdir(parents=True,exist_ok=True)
seed=2026111203
rng=np.random.default_rng(seed)

def triples(k):
 return [(a,b,k-a-b) for a in range(k+1) for b in range(k-a+1)]

def coeff(k,a):
 return math.sqrt(math.factorial(k)/math.prod(math.factorial(x) for x in a))

def phi(v,k):
 return np.array([coeff(k,a)*math.prod(float(v[i])**a[i] for i in range(3)) for a in triples(k)])

def contraction_matrix(k):
 # tau_i[T] equals complete contraction of k-1 tensor indices with (k-1)/2 Kronecker pairs.
 assert k%2==1
 m=(k-1)//2
 a_list=triples(k); a_index={a:i for i,a in enumerate(a_list)}
 M=np.zeros((3,len(a_list)))
 for i in range(3):
  for beta in triples(m):
   a=tuple(2*beta[j]+(1 if j==i else 0) for j in range(3))
   multinom=math.factorial(m)/math.prod(math.factorial(b) for b in beta)
   M[i,a_index[a]]+=multinom/coeff(k,a)
 return M

def unitvec():
 v=rng.normal(size=3)
 return v/np.linalg.norm(v)

def random_rotation():
 Q,R=np.linalg.qr(rng.normal(size=(3,3)))
 Q=Q@np.diag(np.sign(np.diag(R)))
 if np.linalg.det(Q)<0: Q[:,0]*=-1
 return Q

def discrepancy(a,b): return abs(float(a)-float(b))

# Independent exact (symbolic) witnesses.
sq3=sp.sqrt(3)
vecsA=[sp.Matrix([0,0,1]),sp.Matrix([0,0,-1])]
vecsB=[sp.Matrix([1,0,0]),sp.Matrix([-sp.Rational(1,2),sq3/2,0]),sp.Matrix([-sp.Rational(1,2),-sq3/2,0])]
def moment(vs):
 return sp.MutableDenseNDimArray([sp.simplify(sum(sp.prod(v[i] for i in (a,b,c)) for v in vs)/len(vs)) for a,b,c in itertools.product(range(3),repeat=3)],(3,3,3))
TA=moment(vecsA); TB=moment(vecsB)
assert all(TA[i,j,l]==0 for i,j,l in itertools.product(range(3),repeat=3))
assert sp.simplify(TB[0,0,0]-sp.Rational(1,4))==0
assert all(sp.simplify(sum(TB[i,j,j] for j in range(3)))==0 for i in range(3))
assert all(sp.simplify(sum(TA[i,j,j] for j in range(3)))==0 for i in range(3))
EA=sp.Rational(1,2)*(1+TA[0,0,0]); EB=sp.Rational(1,2)*(1+TB[0,0,0]);
assert EA==sp.Rational(1,2) and EB==sp.Rational(5,8)
assert EB-EA==sp.Rational(1,8)
# All of these probabilities are for entirely stipulated affine effects.
exact={
 'seed':seed,
 'model':'K_k=conv{n^{tensor k}:|n|=1}, odd k, in Sym^k(R^3)',
 'affine_dimension_formula':'(k+1)(k+2)/2',
 'source_notion':'mathematical control, not physics',
 'mixture_A':'0.5*(north^3+south^3)',
 'mixture_B':'1/3*(u0^3+u120^3+u240^3) in xy plane',
 'tau_A':[0,0,0],'tau_B':[0,0,0],
 'tensor_A_xxx':str(TA[0,0,0]),'tensor_B_xxx':str(TB[0,0,0]),
 'born_effects_all_directions_on_both_mixtures':'1/2',
 'cubic_effect_x_A':str(EA),'cubic_effect_x_B':str(EB),
 'separation':str(EB-EA),
 'pure_test_c=1/2':{str(k):{'Born':'3/4','Veronese':str((1+sp.Rational(1,2)**k)/2)} for k in [1,3,5,7]},
 'mutation_test_identify_E3_as_F':'REJECTED (5/8 != 1/2 on mixtures A/B)',
}
(ROOT/'EXACT_RESULTS.json').write_text(json.dumps(exact,indent=2)+'\n')

pure_rows=[]; mixture_rows=[]; summary={}; max_pure_res=0.0; max_mix_res=0.0
for k in [1,3,5,7]:
 C=contraction_matrix(k); D=len(triples(k)); assert D==(k+1)*(k+2)//2
 # Rank and nullity computed numerically on points, independent analytical theorem in paper.
 sample=np.stack([phi(unitvec(),k) for _ in range(max(250,6*D))])
 sv=np.linalg.svd(sample,compute_uv=False)
 rank=int(np.linalg.matrix_rank(sample, tol=1e-10))
 assert rank==D,(k,rank,D,sv[-1])
 assert np.linalg.matrix_rank(C)==3
 for trial in range(384):
  n=unitvec();m=unitvec();R=random_rotation()
  pn=phi(n,k);pm=phi(m,k);c=float(n@m)
  norm_res=abs(np.dot(pn,pn)-1.0)
  kernel_res=float(np.linalg.norm(C@pn-n))
  tensor_dot_res=discrepancy(pn@pm,c**k)
  F=(1+float(m@(C@pn)))/2
  E=(1+float(pm@pn))/2
  FR=(1+float((R@m)@(C@phi(R@n,k))))/2
  ER=(1+float(phi(R@m,k)@phi(R@n,k)))/2
  F_res=discrepancy(F,(1+c)/2)
  E_res=discrepancy(E,(1+c**k)/2)
  comp_res=discrepancy(E+(1+float(phi(-m,k)@pn))/2,1.0)
  equiv_res=max(discrepancy(FR,F),discrepancy(ER,E))
  pfs=(1+c)/2; distance=math.acos(math.sqrt(min(1,max(0,pfs))))
  metric_res=discrepancy(distance,math.acos(max(-1,min(1,c)))/2)
  residual=max(norm_res,kernel_res,tensor_dot_res,F_res,E_res,comp_res,equiv_res,metric_res)
  max_pure_res=max(max_pure_res,residual)
  assert -1e-12<=F<=1+1e-12 and -1e-12<=E<=1+1e-12
  pure_rows.append(dict(k=k,trial=trial,cosine=c,F_Born=F,E_tensor=E,F_minus_E=F-E,rotated_F=FR,rotated_E=ER,
    norm_residual=norm_res,contraction_residual=kernel_res,tensor_dot_residual=tensor_dot_res,F_residual=F_res,
    E_residual=E_res,complement_residual=comp_res,rotation_residual=equiv_res,FS_distance_residual=metric_res,maximum_abs_residual=residual))
 for trial in range(96):
  count=int(rng.integers(2,9));ns=[unitvec() for _ in range(count)];weights=rng.dirichlet(np.ones(count))
  m=unitvec(); R=random_rotation();T=sum(w*phi(n,k) for w,n in zip(weights,ns)); T_rot=sum(w*phi(R@n,k) for w,n in zip(weights,ns));mean=sum(w*n for w,n in zip(weights,ns));
  F=(1+float(m@(C@T)))/2;Fdirect=(1+float(m@mean))/2
  E=(1+float(phi(m,k)@T))/2;Edirect=sum(w*(1+float(m@n)**k)/2 for w,n in zip(weights,ns))
  Frot=(1+float((R@m)@(C@T_rot)))/2; Erot=(1+float(phi(R@m,k)@T_rot))/2
  pair_bound=(0<=F<=1 and 0<=E<=1)
  residual=max(discrepancy(F,Fdirect),discrepancy(E,Edirect),discrepancy(Frot,F),discrepancy(Erot,E))
  max_mix_res=max(max_mix_res,residual)
  assert pair_bound
  mixture_rows.append(dict(k=k,trial=trial,num_components=count,min_weight=float(min(weights)),max_weight=float(max(weights)),
    F_Born=F,E_tensor=E,Born_direct=Fdirect,E_direct=Edirect,rotated_F=Frot,rotated_E=Erot,max_abs_residual=residual))
 summary[k]={
  'state_dimension_analytic':D,'span_rank_numeric':rank,'span_smallest_singular_value':float(sv[-1]),
  'contraction_rank':int(np.linalg.matrix_rank(C)),'Born_effect_kernel_dimension':D-3,
  'pure_trials':384,'mixed_trials':96,
  'min_E_pure':float(min(r['E_tensor'] for r in pure_rows if r['k']==k)),
  'max_E_pure':float(max(r['E_tensor'] for r in pure_rows if r['k']==k)),
  'max_pure_residual':float(max(r['maximum_abs_residual'] for r in pure_rows if r['k']==k)),
  'max_mixed_residual':float(max(r['max_abs_residual'] for r in mixture_rows if r['k']==k)),
 }

def csvwrite(path,rows):
 with open(path,'w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
csvwrite(OUT/'all_1536_pure_trials.csv',pure_rows)
csvwrite(OUT/'all_384_mixed_trials.csv',mixture_rows)
assert max_pure_res<1e-12 and max_mix_res<1e-12,(max_pure_res,max_mix_res)
results={'status':'PASS_SCOPE_BOUND_SYMBOLIC_AND_NUMERIC','theory':'stipulated finite-dimensional GPT countermodel only',
'seed':seed,'exact_witness':exact,'tested_odd_degrees':summary,'all_pure_trial_count':len(pure_rows),'all_mixed_trial_count':len(mixture_rows),
'max_pure_residual':max_pure_res,'max_mixed_residual':max_mix_res,
'outlier_policy':'No trial exclusions. Full signed residuals and extrema retained.',
'limits':['No emergent qubit','No prephysical Born rule','No time or physical dynamics','No higher-order interference characterization','No quantum tensor product','No experimental test','No independent expert review']}
(ROOT/'RESULTS_G3.json').write_text(json.dumps(results,indent=2,sort_keys=True)+'\n')
print('PASS veronese GPT',[(k,v['state_dimension_analytic'],v['span_rank_numeric']) for k,v in summary.items()])
print('exact distinguishability: 1/2 versus 5/8; 1/8 gap; projective measurements both 1/2')
print('all rows',len(pure_rows),'pure',len(mixture_rows),'mixed; residual maxima',max_pure_res,max_mix_res)
