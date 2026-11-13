#!/usr/bin/env python3
"""Generate source-linked assessment register and NON-ontological dependency graph."""
import csv,json
from pathlib import Path
root=Path(__file__).resolve().parent
C=[
 ('DG-AB-01','Determinant of Levi-Civita tangent holonomy equals normalized Bargmann phase to power n+1 after CPn is assumed','SUPPORTED_IN_SCOPE','Conditional theorem, complex projective geometry explicitly imported','A-01;B-GEO-01;prior-G'),
 ('DG-AB-02','From determinant identity alone, a physical prephysical-quantum bridge exists','NOT_IDENTIFIED_IN_SCOPE','The theorem starts with quantum geometric inputs','A-02;B-GEO-01;prior-G'),
 ('DG-AB-03','Transition-probability metric alone determines signed Bargmann phase','REFUTED_IN_SCOPE','Conjugation leaves all pair probabilities unchanged and reverses nonreal phase','A-03;prior-G'),
 ('DG-AB-04','Three pairwise probabilities equal 1/4 determine phase on CP2','REFUTED_IN_SCOPE','Positive-semidefinite 3x3 Gram matrices admit arbitrary phase for these probabilities','A-04'),
 ('DG-AB-05','RP2 real three-level and CP1 complex two-level differ only by monodromy under full metric access','REFUTED_IN_SCOPE','Curvature 1 vs 4 is a local metric discriminator; monodromy remains a global difference','A-05;B-MON-02;prior-G'),
 ('DG-AB-06','Exactly finite homogeneous metric spaces converge GH to CPn n>=1','REFUTED_IN_SCOPE','Gelander 2013 Corollary 1.3 rules out positive-dimensional CPn','A-07;B-FIN-04;Gelander-2013'),
 ('DG-AB-07','Any exactly homogeneous finite induced-metric spherical subset has covering radius >= arccos(59/60)','SUPPORTED_IN_SCOPE','Finite O3 classification and axial split are assumptions/dependencies; not sharp bound','B-FIN-03;prior-G'),
 ('DG-AB-08','No I3 and symplectic pure-state manifold in all operational theories select complex QT','REFUTED_IN_SCOPE','Classical symplectic spin phase space is a countermodel to the unrestricted statement','A-09'),
 ('DG-AB-09','No I3 by itself supplies the Barnum Muller Ududec classification theorem','REFUTED_IN_SCOPE','Published theorem also requires classical decomposability and strong symmetry','A-10;A-11;B-NI3-06;Barnum-2014'),
 ('DG-AB-10','Elementary CP1 geometry and local quantum measurements alone determine bipartite state cone','NOT_IDENTIFIED_IN_SCOPE','Separable or full quantum, and whole K_t continuum, agree on all elementary systems','B-COMP-05;DG-COMP-01'),
 ('DG-AB-11','Uniform K_t interpolation is closed under 4-elementary parallel prep for 0<t<1','REFUTED_IN_SCOPE','E positive effect yields exact gap t(1-t)/4','DG-COMP-03'),
 ('DG-AB-12','Conditional CNOT and all local unitaries force full two-qubit quantum cone inside density matrices','SUPPORTED_IN_SCOPE','Schmidt decomposition and convexity prove exact conditional statement; all inputs imported','DG-COMP-04'),
 ('DG-AB-13','Fixed-settings Bell-CHSH violation implies ordinary full bipartite state cone','REFUTED_IN_SCOPE','K_t with sqrt(2)-1<t<1 violates CHSH but is proper subset of quantum density matrices','DG-COMP-02'),
 ('DG-AB-14','Static projective geometry uniquely determines physical clock and Hamiltonian','REFUTED_IN_SCOPE','Zero vs nonzero unitary generator share static metric','A-15'),
 ('DG-AB-15','Dephasing-induced rank-one stochastic update equals reversible classical Hamiltonian mechanics','REFUTED_IN_SCOPE','Update is noninjective; Hamiltonian flow invertible where defined','A-16'),
 ('DG-AB-16','D8 algebraic operator-norm reduction proves entire Wilson entropy theorem','UNRESOLVED','D8 result conditional on unproved lattice and trace/ideal inputs in this review','B-D8-08'),
 ('DG-AB-17','The exact Z1 G7 manuscript has been inspected and reproduced here','UNRESOLVED','Z quoted disposition only; full G7 not supplied','Z-quoted'),
 ('DG-AB-18','Both quantum and classical mechanics with full emergent empirical map are established','NOT_IDENTIFIED_IN_SCOPE','Input source set provides no unimported full causal/operational bridge','G1-root')
]
with (root/'CLAIM_DELTA.csv').open('w',newline='',encoding='utf8') as f:
 w=csv.writer(f);w.writerow(['id','claim_as_tested','disposition','warrant_scope_and_limit','source_claims_or_external']);w.writerows(C)
O=[
 ('DG-OP-01','Source grounding','Inspect actual Z1/G7 manuscript, ladders and references; do not attribute the quoted G7 calculations to inspected files','OPEN'),
 ('DG-OP-02','Operational emergence','Derive a preparation/effect/record structure with calibrated uncertainty from non-quantum prephysical primitives','OPEN'),
 ('DG-OP-03','Complex structure','Find a non-imported orientation/phase-selection law and an operational sign-sensitive test','OPEN'),
 ('DG-OP-04','Composition','Supply a physical, independently justified rule selecting a multi-system state/effect cone and verify convexity, positivity, locality, instruments, discard and reassociation','OPEN'),
 ('DG-OP-05','Gate mechanism','Derive rather than stipulate a reversible entangling interaction sufficient for the CNOT or other gate selection theorem','OPEN'),
 ('DG-OP-06','Multi-system alternatives','Classify possible coherent all-arity extensions of 2-party intermediate K_t, or show explicit further no-go; do not assume uniform interpolation','OPEN'),
 ('DG-OP-07','Clock and dynamics','Provide an operational physical clock, units, energy observability and a derived generator with falsifiable calibration','OPEN'),
 ('DG-OP-08','Classical limit','Derive classical Hamiltonian mechanics with a controlled limiting procedure, stated observables and errors; dephasing is not enough','OPEN'),
 ('DG-OP-09','External expert checks','Seek independent mathematical and domain-expert review for newly proposed composition theorems and B finite-group axial split','OPEN')]
with (root/'OPEN_PROBLEMS_DELTA.csv').open('w',newline='',encoding='utf8') as f:
 w=csv.writer(f);w.writerow(['id','domain','obligation','status']);w.writerows(O)
nodes=[
 ('P','Prephysical relational primitives','OPEN'),
 ('O','Calibrated preparations / records / effects','OPEN'),
 ('Q','Complex projective single-system geometry','CONDITIONAL'),
 ('S','Signed phase and holonomy observables','NONIDENTIFIED'),
 ('C2','Admissible two-system state and effect cones','NONIDENTIFIED'),
 ('C4','All-arity closure: preparation / discard / reassociation','NEW_INDEPENDENT_GATE'),
 ('U','Reversible entangling transformations','OPEN'),
 ('T','Physical dynamics and clocks','OPEN'),
 ('L','Controlled quantum-to-classical limit','OPEN'),
 ('E','Independent empirical and uncertainty map','OPEN'),
 ('F','Total ontology as defined','NOT_IDENTIFIED')
]
edges=[
 ('P','O','emergence, operational calibration','OPEN'),
 ('O','Q','complex statistical manifold identification','OPEN'),
 ('Q','S','oriented transport representation','OPEN'),
 ('Q','C2','local data insufficient','NOT_IDENTIFIED'),
 ('S','C2','phase alone insufficient','NOT_IDENTIFIED'),
 ('C2','C4','independent-preparation closure','OPEN'),
 ('C4','U','consistent allowed gate','OPEN'),
 ('U','T','calibrated generator and clock','OPEN'),
 ('T','L','classical Hamiltonian limit','OPEN'),
 ('L','E','evidence and calibrations','OPEN'),
 ('E','F','full physical map','OPEN'),
]
g={'graph_type':'SCIENTIFIC_OBLIGATION_GRAPH_NOT_A_PROVEN_ONTOLOGY',
   'root_G1':'OPEN','ontology_selected':False,
   'nodes':[{'id':x,'label':name,'status':status} for x,name,status in nodes],
   'edges':[{'source':a,'target':b,'needed':' '+need if not need else need,'status':status} for a,b,need,status in edges],
   'controls':{'same_local_data_different_composites':'Sep2 vs Quantum2 vs K_t','four_party_uniform_extension':'REFUTED_IN_SCOPE interior t','CNOT_choice':'conditional theorem, imported gate'}}
(root/'ONTOLOGY_OBLIGATION_GRAPH.json').write_text(json.dumps(g,indent=2)+'\n')
print('recorded',len(C),'claims',len(O),'open problems',len(nodes),'nodes')
