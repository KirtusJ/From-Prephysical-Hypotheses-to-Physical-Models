#!/usr/bin/env python3
"""Independent bounded controls for Director G fourth grounding review.
Only tests explicitly stipulated finite graphs and effects. No physical ontology is inferred.
Usage: python verify_director_g_followup.py OUTPUT_DIRECTORY
"""
import csv,itertools,json,math,sys
from pathlib import Path
import numpy as np
from scipy.linalg import expm

out=Path(sys.argv[1]) if len(sys.argv)>1 else Path('verification_output')
out.mkdir(parents=True,exist_ok=True)
def write_csv(name,cols,rows):
 with (out/name).open('w',newline='',encoding='utf-8') as f:
  w=csv.DictWriter(f,fieldnames=cols,lineterminator='\n');w.writeheader();w.writerows(rows)
def write_json(name,obj):
 (out/name).write_text(json.dumps(obj,indent=2,sort_keys=True,ensure_ascii=False)+'\n',encoding='utf-8')
def lift_matrix(edges,V=5,q=3):
 B=np.zeros((V*q,V*q),dtype=object)
 for a,b,g in edges:
  for h in range(q):
   u=a*q+h;v=b*q+(h+g)%q
   B[u,v]+=1;B[v,u]+=1
 return B
E_BOW=[(0,1,0),(1,2,0),(2,0,0),(0,3,0),(3,4,0),(4,0,1)]
B=lift_matrix(E_BOW)
assert B.shape==(15,15) and (B.T==B).all() and (np.diag(B)==0).all()
assert {int(sum(row)) for row in B}=={2,4}
P=np.eye(15,dtype=object)
pr_exp=None
for k in range(1,20):
 P=P@B
 if min(P.flat)>0:
  pr_exp=k;break
assert pr_exp==5 and min(P.flat)==1
write_csv('primitive_certificate_B5.csv', ['row']+[f'c{j:02d}' for j in range(15)], [dict(row=i,**{f'c{j:02d}':int(P[i,j]) for j in range(15)}) for i in range(15)])

K_END=18
N=np.eye(15,dtype=object)[0]
counts=[];coverage=[]
for k in range(K_END+1):
 minval=min(int(x) for x in N)
 bound=2**(k-5) if k>=5 else None
 if bound is not None:assert minval>=bound
 coverage.append({'k':k,'total_paths':int(sum(N)),'min_endpoint_gain':minval,'min_bound':bound})
 for y in range(5):
  for g in range(3):
   counts.append({'k':k,'endpoint':y,'gain_mod_3':g,'paths':int(N[3*y+g])})
 N=N@B
write_csv('all_lift_endpoint_gain_counts.csv',['k','endpoint','gain_mod_3','paths'],counts)
write_csv('all_lift_coverage_bounds.csv',['k','total_paths','min_endpoint_gain','min_bound'],coverage)

# Verify the finite event approximation of arbitrary complex-projective directions.
# For k>=10, M=2^(k-6), R=M/2 and all nearest Eisenstein coordinates satisfy |a|,|b|<=M.
zeta=complex(-.5,math.sqrt(3)/2)
rng=np.random.default_rng(2026111204)
net=[]
for k in (10,12,14,16):
 M=2**(k-6);R=M/2
 assert R>math.sqrt(5)
 Nk=np.array([c['paths'] for c in counts if c['k']==k],dtype=object).reshape(5,3)
 for trial in range(256):
  z=rng.normal(size=5)+1j*rng.normal(size=5)
  z=z/np.linalg.norm(z)
  target=R*z
  aa=np.rint(target.real +target.imag/math.sqrt(3)).astype(int)
  bb=np.rint(2*target.imag/math.sqrt(3)).astype(int)
  assert max(np.max(np.abs(aa)),np.max(np.abs(bb)))<=M
  vec=aa+bb*zeta
  event_counts=np.column_stack([aa+M,bb+M,np.full(5,M)])
  assert np.all(event_counts>=0) and np.all(event_counts<=Nk.astype(np.int64))
  reconstructed=event_counts[:,0]+zeta*event_counts[:,1]+zeta**2*event_counts[:,2]
  assert np.max(np.abs(reconstructed-vec))<1e-10
  eps=float(np.linalg.norm(vec-R*z))
  assert eps<=math.sqrt(5)+1e-10
  angle=math.acos(min(1.,abs(np.vdot(z,vec))/np.linalg.norm(vec)))
  sin_bound=math.sqrt(5)/(R-math.sqrt(5))
  assert math.sin(angle)<=sin_bound+1e-12
  net.append({'k':k,'case':trial,'M':M,'R':R,'error_vector_norm':eps,'fs_angle_radians':angle,
              'sin_angle':math.sin(angle),'sin_upper_bound':sin_bound,'min_walk_supply':int(np.min(Nk)),
              'max_walks_used_in_one_cell':int(np.max(event_counts))})
write_csv('all_projective_approximation_trials.csv',list(net[0].keys()),net)

# Exact additive transport-sensitive measure, for all 3^3 edge labels and 3^3 gauge switches.
TRI=[(0,1),(1,2),(2,0)]
def triangle_walks(labels):
 edges={}
 for (a,b),g in zip(TRI,labels):edges[a,b]=g;edges[b,a]=(-g)%3
 w=[(0,0,(0,))]
 for _ in range(3):
  w=[(v,(gain+g)%3,seq+(v,)) for y,gain,seq in w for (a,v),g in edges.items() if a==y]
 return w,edges
def weight2(end,g): return (4 if g==0 else 1) if end==0 else 2
switch_rows=[]
for labels in itertools.product(range(3),repeat=3):
 w,edges=triangle_walks(labels)
 for gauges in itertools.product(range(3),repeat=3):
  sw={(a,b):(g+gauges[b]-gauges[a])%3 for (a,b),g in edges.items()}
  original=[weight2(y,g) for y,g,_ in w]
  transformed=[]
  for y,g,seq in w:
   gs=sum(sw[a,b] for a,b in zip(seq[:-1],seq[1:]))%3
   transformed.append(weight2(y,gs))
  assert original==transformed
  switch_rows.append({'g01':labels[0],'g12':labels[1],'g20':labels[2],
                      'h0':gauges[0],'h1':gauges[1],'h2':gauges[2],
                      'number_of_walks':len(w),'total_twice_mu':sum(original),
                      'max_weight_change':max(abs(a-b) for a,b in zip(original,transformed))})
assert len(switch_rows)==729
write_csv('all_triangle_switching_trials.csv',list(switch_rows[0].keys()),switch_rows)
wt0=weight2(0,0);wt1=weight2(0,1)
assert wt0==4 and wt1==1 # 2*mu: trivial holonomy ->2, nontrivial ->1/2
# negative control: weight on an OPEN walk as if it were gauge invariant
assert weight2(0,0)!=weight2(0,1) and (0+1-0)%3==1

# Synchronized product of two nontrivial-gain 4-cycles. Each has 4D full-length span.
C4_EDGES=[(0,1,0),(1,2,0),(2,3,0),(3,0,1)]
def plain_adj(edges,V):
 A=np.zeros((V,V),dtype=object)
 for a,b,_ in edges:A[a,b]+=1;A[b,a]+=1
 return A
A4=plain_adj(C4_EDGES,4)
state=np.eye(4,dtype=object)[0]
seen_single=set();seen_sync=set(); parity_rows=[]
for k in range(13):
 support={j for j in range(4) if state[j]>0}
 seen_single|=support
 seen_sync|={(a,b) for a in support for b in support}
 expected={0,2} if k%2==0 else {1,3}
 if k>=2:assert support==expected
 parity_rows.append({'k':k,'reachable_factor_vertices':','.join(map(str,sorted(support))),
   'factor_span_dimension_at_k':len(support),
   'product_span_dimension_at_k':len(support)**2,
   'synchronized_union_dimension_so_far':len(seen_sync),
   'full_tensor_dimension_from_union_so_far':len(seen_single)**2})
 state=state@A4
assert seen_single==set(range(4))
assert seen_sync==({(a,b) for a in (0,2) for b in (0,2)}|{(a,b) for a in (1,3) for b in (1,3)})
assert len(seen_sync)==8 and len(seen_single)**2==16
write_csv('all_synchronized_composition_rank_trials.csv',list(parity_rows[0].keys()),parity_rows)
# Explicit nontrivial holonomy: two paths from 0 to 2, length 2, of gains 0 and 2.
def list_gain_walks(edges,start,k):
 table={}
 for a,b,g in edges:table.setdefault(a,[]).append((b,g));table.setdefault(b,[]).append((a,(-g)%3))
 w=[(start,0,(start,))]
 for _ in range(k):w=[(b,(gain+g)%3,seq+(b,)) for a,gain,seq in w for b,g in table[a]]
 return w
c4paths=[(gain,seq) for y,gain,seq in list_gain_walks(C4_EDGES,0,2) if y==2]
assert sorted(g for g,_ in c4paths)==[0,2]
amplitude=sum(zeta**g for g,_ in c4paths)
assert abs(abs(amplitude)**2-1)<1e-12

# Conditional formal Hamiltonian time is possible, but not supplied by walk length.
H=np.zeros((5,5),dtype=complex)
for a,b,g in E_BOW:
 H[b,a]=zeta**g;H[a,b]=zeta**(-g)
assert np.allclose(H,H.conj().T)
deg=np.real(np.diag(H@H)).round().astype(int).tolist()
assert deg==[4,2,2,2,2] and not np.allclose(H@H, np.eye(5)*np.real(np.trace(H@H)/5))
unitary=[]
for tau in (0.,.25,1.,math.sqrt(2),3.5,10.):
 U=expm(-1j*tau*H)
 unitary.append({'tau_formal':tau,'unitarity_residual':float(np.max(np.abs(U.conj().T@U-np.eye(5))))})
 assert unitary[-1]['unitarity_residual']<1e-12
write_csv('all_formal_unitary_controls.csv',list(unitary[0].keys()),unitary)

# Symmetric filter: optimize unconditional witness exactly; no quantum implementation claim.
from fractions import Fraction
filter_rows=[]
for t in (Fraction(1,100),Fraction(1,10),Fraction(1,4),Fraction(1,2),Fraction(3,4),Fraction(9,10),Fraction(99,100)):
 x=t/(2*(1+t)); p=x*(t+(1-t)*x);f=t/(t+(1-t)*x)
 gap=f-(1+t)/2
 uncond=p*gap
 asserted=t*t*(1-t)/(8*(1+t))
 assert uncond==asserted and gap>0 and p>0
 filter_rows.append({'t':str(t),'x_opt_uncond':str(x),'success_p':str(p),'conditional_gap':str(gap), 'unconditional_gap':str(uncond)})
write_csv('all_filter_unconditional_witness_controls.csv',list(filter_rows[0].keys()),filter_rows)

# Two distinct formal composite dynamics on the same tensor state space.
X=np.array([[0.,1.],[1.,0.]])
Hcat=np.kron(X,X)
Hcart=np.kron(X,np.eye(2))+np.kron(np.eye(2),X)
initial=np.array([1.,0.,0.,0.],dtype=complex)
interaction=[]
for tau in (0.,math.pi/8,math.pi/4,math.pi/2):
 psi_cat=expm(-1j*tau*Hcat)@initial
 psi_cart=expm(-1j*tau*Hcart)@initial
 conc_cat=2*abs(psi_cat[0]*psi_cat[3]-psi_cat[1]*psi_cat[2])
 conc_cart=2*abs(psi_cart[0]*psi_cart[3]-psi_cart[1]*psi_cart[2])
 assert abs(conc_cat-abs(math.sin(2*tau)))<1e-12 and conc_cart<1e-12
 interaction.append({'tau_formal':tau,'categorical_concurrence':float(conc_cat),'cartesian_concurrence':float(conc_cart),
                    'norm_error_categorical':float(abs(np.linalg.norm(psi_cat)-1)),
                    'norm_error_cartesian':float(abs(np.linalg.norm(psi_cart)-1))})
assert abs(interaction[2]['categorical_concurrence']-1)<1e-12
write_csv('all_formal_composite_dynamics_trials.csv',list(interaction[0].keys()),interaction)

results={'research_gate':'G1 OPEN; no total ontology',
 'lift':{'vertices':15,'primitive_exponent':pr_exp,'minimum_entry_B5':int(min(P.flat)),'degrees':deg,'minimum_count_k18':coverage[18]['min_endpoint_gain']},
 'exact_lattice_construction':{'m':5,'gain_order':3,'amplitudes':'Eisenstein integers Z[zeta_3]^5','approximations':len(net),'max_FS_angle_by_k':{str(k):max(r['fs_angle_radians'] for r in net if r['k']==k) for k in (10,12,14,16)}},
 'grade_one_counterexample':{'gauge_cases':len(switch_rows),'max_gauge_residual':0,'nontrivial_closed_weight_twice_mu':[wt0,wt1]},
 'sync_composition':{'one_factor_full_dim':4,'expected_tensor_dim':16,'synchronized_dim':8,'missing_dimension':8,'nontrivial_interference_magnitude_sq':abs(amplitude)**2},
 'formal_adjacency':{'Hermitian':True,'nonuniform_H2_diagonal':deg,'max_unitarity_residual':max(x['unitarity_residual'] for x in unitary)},
 'formal_composites':{'categorical_concurrence_at_pi_over_4':interaction[2]['categorical_concurrence'],'cartesian_concurrence_at_pi_over_4':interaction[2]['cartesian_concurrence']},
 'filter':{'cases':len(filter_rows),'formula':'W_opt=t^2(1-t)/[8(1+t)]'},
 'trial_counts':{'lift_cell_rows':len(counts),'lift_coverage_rows':len(coverage),'phase_approximation_rows':len(net), 'gauge_switch_rows':len(switch_rows),'sync_rank_rows':len(parity_rows),'formal_unitary_rows':len(unitary),'formal_composite_rows':len(interaction),'filter_rows':len(filter_rows)}}
write_json('RESULTS_G4.json',results)
print('ALL_G4_CHECKS_PASS',json.dumps(results,sort_keys=True))
