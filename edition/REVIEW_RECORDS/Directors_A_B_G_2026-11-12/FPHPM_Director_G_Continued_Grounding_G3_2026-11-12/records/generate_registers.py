from pathlib import Path
import csv,json
ROOT=Path(__file__).resolve().parent
claims=[
 ('G3-C01','A2 18 payloads are internally byte-consistent','A2 supplied archive, manifest SHA-256','SUPPORTED_IN_SCOPE','own rerun A2 packet verifier','local consistency, not source authentication'),
 ('G3-C02','B2 18 payloads are internally byte-consistent','B2 supplied archive, manifest SHA-256','SUPPORTED_IN_SCOPE','own rerun B2 packet verifier','local consistency, not proof authentication'),
 ('G3-C03','A2 three-cycle P-P^T squares to -3I on rational zero-sum contrast','chosen permutation linearization','SUPPORTED_IN_SCOPE','A2 exact algebra + reproduced script','does not derive physical complex amplitudes'),
 ('G3-C04','A2 3-ray Gram determinant and rank boundary are correct','normalized complex vector triples with positive pair overlaps','SUPPORTED_IN_SCOPE','PSD 3-by-3 Gram determinant and reproductions','quantum geometry given at input'),
 ('G3-C05','B2 global conjugation preserves adaptive quantum outcome probabilities','all states instruments and effects conjugated together','SUPPORTED_IN_SCOPE','Kraus trace identity + rerun 96 adaptive tests','conjugating state against fixed apparatus differs'),
 ('G3-C06','B2 CP2 scalar tangent determinant alone does not identify Bargmann phase modulo conjugation','assumed CP^n geodesic triangles n>=2','SUPPORTED_IN_SCOPE','PSD Gram family with phi=0 vs 2pi/(n+1)','full matrix holonomy or continuous family not excluded'),
 ('G3-C07','Finite exact homogeneous metric spaces cannot GH-converge to CP^n','finite exact transitive isometry group; GH convergence','SUPPORTED_IN_SCOPE','Gelander 2013 theorem 1.1 cor 1.3, primary PDF','asymmetric approximations not excluded'),
 ('G3-C08','Every odd directed cycle yields polar complex J on full contrast module','imported real linearization and Euclidean metric','SUPPORTED_IN_SCOPE','Fourier proof + all 8 odd N tests 3-18','algebraic structure only'),
 ('G3-C09','Even directed cycles admit no J^2=-I on entire contrast module','full zero-sum real contrast of even N','SUPPORTED_IN_SCOPE','odd dimension and alternating kernel','mode deletion changes representation'),
 ('G3-C10','Reflection of any odd directed cycle sends polar J to -J, dihedral equivariant J impossible','P and its chosen orientation-reversing symmetry','SUPPORTED_IN_SCOPE','real Fourier commutant proof + 8 odd tests','physical orientation not identified'),
 ('G3-C11','Odd Veronese K_k has exposed pure S^2 and affine dimension (k+1)(k+2)/2','k odd; symmetric tensor state space','SUPPORTED_IN_SCOPE','polynomial span + exposing effect proof; ranks k=1 3 5 7','Euclidean sphere and effects stipulated'),
 ('G3-C12','All K_k have the exact qubit pure Born table under F_m and its FS metric/holonomy','designated F_m affine effects and comparison with CP1','SUPPORTED_IN_SCOPE','contraction identity + distance theorem','does not select F as physically unique'),
 ('G3-C13','K_3 contains mixtures with same all F_m but different valid E_x, exact gap 1/8','K_3 full unrestricted affine effects','SUPPORTED_IN_SCOPE','exact 120-degree triplet and antipodal mixtures','not empirical probability measurement'),
 ('G3-C14','F tests have d_k-3-dimensional kernel; E tests are separating','odd Veronese normalized states','SUPPORTED_IN_SCOPE','linear contraction rank+homogeneous polynomial span','projective tomography is additional premise'),
 ('G3-C15','Every finite adaptive projective measure-reprepare and SO3 rotation circuit is predicted identically by K_3 and its Bloch quotient','only specified rotations and rank-one projective instruments','SUPPORTED_IN_SCOPE','induction proof + 96 trials times eight words','arbitrary quantum POVMs and channels excluded'),
 ('G3-C16','Minimal tensor composites of K_3 are associative and permit independent preparations and nonsignaling local tests','convex hull of product states; product effects','SUPPORTED_IN_SCOPE','convex product definition and no-signaling proof','no quantum entanglement or physical composition'),
 ('G3-C17','Pure CP1 geometry plus its complete pure Born table and restricted projective circuits uniquely fix the full qubit operational theory','no extra tomography/effect completeness premises','REFUTED_IN_SCOPE','explicit K_1 versus K_3 exact countermodel','stronger postulates can select qubit'),
 ('G3-C18','The Born test family being tomographically separating on all states selects Bloch ball when sphere-extreme convexity and pure Born values are assumed','compact finite-dimensional convex K with ext=S2 and separating F_m','SUPPORTED_IN_SCOPE','affine surjection/injection theorem','assumed Born effects and tomography not emergent'),
 ('G3-C19','No restriction plus previous state-space selection yields full single-qubit state/effect cone','K=B3 and all affine [0,1] effects available','SUPPORTED_IN_SCOPE','dual-ball effect inequalities','dynamics and composition still absent'),
 ('G3-C20','All A2/B2 mathematical checks amount to independent scientific referee or physical grounding','internal single-actor script reruns','REFUTED_IN_SCOPE','source-provenance facts and absence of independent expert review','published external context limited by scope'),
 ('G3-C21','The present finite-cycle or Veronese constructions yield explained quantum and classical mechanics with a full empirical map','research program total ontology','UNRESOLVED','no physical primitive measurement time or classical bridge','zero ontology selection'),
 ('G3-C22','Director Z G7 paper and Z1 archive source details are verified in this continuation','only relay summary; Z files not attached','UNRESOLVED','source bytes unavailable in current inputs','do not silently promote source-relayed claims'),
 ('G3-C23','The cubic model meets Barnum-Muller-Ududec full higher-order-interference classification premises','not specified: filters spectrality strong symmetry and interference structure','UNRESOLVED','no specification or checks of necessary hypotheses','countermodel does not refute restricted published theorem'),
]
with (ROOT/'CLAIM_DELTA.csv').open('w',newline='') as f:
 w=csv.writer(f);w.writerow(['id','claim','scope','disposition','checked_basis','limitation']);w.writerows(claims)
ops=[
 ('G3-OP01','Find a prephysical primitive selected without presupposed time or complex amplitudes','all prephysical relations unvalidated','OPEN','independently ground primitive and physical interpretation'),
 ('G3-OP02','Derive rather than choose the finite-relation linearization functor, dimension, metric and orientation','odd-cycle parity mathematical only','OPEN','demonstrate a representation-selection principle'),
 ('G3-OP03','Identify physically accessible effects or prove the Born F tests tomographically complete on mixed states','K3 exact obstruction','OPEN','derive separating effect family from primitive controls'),
 ('G3-OP04','Derive an operational Born rule from primitive measurements without assuming squared overlaps','F effects stipulated','OPEN','calibrated readout and probability derivation'),
 ('G3-OP05','Recover all physical quantum transformations beyond rotations and projective measure-reprepare','K3 matches restricted circuits','OPEN','derive general channels instruments and disturbance'),
 ('G3-OP06','Prove physically warranted quantum tensor composition and entangling preparations','K3 minimal and prior K_t composite nonunique','OPEN','operational preparation and Bell witness with calibrated systems'),
 ('G3-OP07','Derive objective physical time, energy and clock reference rather than treating graph arrows as steps','no clock','OPEN','prephysical-to-time bridge'),
 ('G3-OP08','Derive classical Hamiltonian mechanics and controlled quantum-classical limit','no dynamics or asymptotics','OPEN','scales, errors, trajectories, decoherence conditions'),
 ('G3-OP09','Externally validate physical predictions and uncertainty budgets in concrete disciplines','no laboratory evidence','OPEN','experimental map with units and falsification tests'),
 ('G3-OP10','Obtain actual Z1/G7 source packet and scrutinize ladder scaling and reference provenance','Z available only as quoted relay','OPEN','direct independent source verification'),
 ('G3-OP11','Independently referee new Veronese and odd-cycle theorems, looking for counterexamples','all self-reviewed','OPEN','external mathematician review'),
 ('G3-OP12','Test additional postulates of published reconstruction theorems against K3','strong symmetry spectrality higher-order interference not tested','OPEN','specify slit/filter operational model before claims'),
 ('G3-OP13','Determine whether extra E measurement is physically meaningful, implementable or excluded on independent grounds','exact theoretical discriminator','OPEN','instrument calibration or exclusion theorem'),
 ('G3-OP14','Check exact/asymptotic finite-carrier route under chosen convergence topology','Gelander only exact finite homogeneous GH','OPEN','explicit primitive-built asymmetric sequence and error control'),
 ('G3-OP15','Ground phase and complex-orientation references as operational rather than representation gauge','global conjugation only gauge with all instrumentation','OPEN','shared phase apparatus and equivalence contract'),
]
with (ROOT/'OPEN_PROBLEMS_DELTA.csv').open('w',newline='') as f:
 w=csv.writer(f);w.writerow(['id','obligation','current_failure','status','acceptance_test']);w.writerows(ops)
json.dump({'claim_count':len(claims),'open_problem_count':len(ops),'disposition_counts':{s:sum(r[3]==s for r in claims) for s in sorted(set(r[3] for r in claims))},'source':'internal single-actor reviews; external published sources checked separately'},(ROOT/'REGISTER_COUNTS.json').open('w'),indent=2)
print('registers',len(claims),len(ops))
