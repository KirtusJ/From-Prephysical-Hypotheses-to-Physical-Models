# Session C: Detector ambiguity and an explicitly fictional relational-atlas cosmology

**Research date:** 7 November 2026 UTC / 6 November 2026 Vancouver.  
**Program:** From Prephysical Hypotheses to Physical Models.  
**Status:** Independent model-specific calculations and deliberately invented candidates, NOT an empirical theory, not an externally refereed paper.

## I. Supplied evidence and source boundaries

Reviewed the uploaded *Session D Disposition* (2 pages) and *Session D Reconciled Diagram* (1 page), plus the separately accessible *Controlled Coupling Calibration* (7 pages) and October 31 Wilson documents. The diagrams distinguish prephysical signed relations, supplied quantum/graph inputs, conditional detector reconstruction and a separate Wilson proof track. The PDFs state that all new detector trials are synthetic. The source ZIP mentioned in the handoff was not itself replayed in this continuation.

The October 30/31 91-member baseline's accepted result is a leading Wilson-Dirac logarithm with bounded remainder. Separate October 31 manuscripts claim a fixed-positive-mass finite part with O_mu(1/log L) remainder, importing an exact spectral-concentration connection, operator-domain claims, a boundary entropy limit, trace estimates and a two-bond expansion. This note does NOT certify those upstream proof sources. The four-branch assembly needs the sum of two signed residual contributions to vanish; separate convergence suffices but is stronger than necessary.

## II. Controlled coupling: exact deduction and its fatal nuisance symmetry

**Assumed experiment (physical inputs):** isolated positive eigenmode with rate coordinate U=lambda_* S, controlled coupling c>0, and incident law f_c(u)=4c^2u exp(-2cu). The common detector is a subprobability kernel R(dz|u), independent of c, and recorded measures are per prepared trial: nu_c(B)=int f_c(u)R(B|u) du.

For a>0 put X=e^{-2aU} and c_j=1+ja. Since f_{c_j}/f_1 = c_j^2 X^j, the Radon-Nikodym ratios obey

    (d nu_{c_j}/d nu_1)(z)/c_j^2 = E[X^j | Z=z, detected at c=1].

The first three couplings recover m(z)=E[X|z], q(z)=E[X^2|z]. Necessarily q-m^2=Var(X|z)>=0. A zero conditional variance means U is measurable from z among detected outcomes, if the common-kernel hypothesis really holds. This does not independently verify that the instrument stayed unchanged.

**An exact all-coupling false identification:** fix k>1 and 0<eta0<1. Device A records z=u with coupling-dependent efficiency eta0 exp[-2c(k-1)u]; Device B records z=u/k with constant efficiency eta0/k^2. Direct variable substitution gives for every c>0

    g_A,c(z) = g_B,c(z) = 4 eta0 c^2 z exp(-2ckz),

and both have total click probability eta0/k^2. The entire registered-and-missed distribution therefore agrees at every c. Merely adding more of the same coupling settings cannot test the common-kernel assumption against this alternative. A bypass reference that independently characterizes the detector can challenge it.

**Finite-setting common-kernel obstruction (exact rational):** at baseline rate 1, X=e^{-2U} has density -log(x) on (0,1). With

    H(x) = x^3 -(3105/2588)x^2 +(5751/16175)x -4679/258800,

its weighted moments with x^j vanish for j=0,1,2, whereas the j=3 weighted moment is 878769/5072480000. Setting eta_+/-=1/2 +/- eps H(x), eps=25880/133199, produces two valid, different constant-with-respect-to-c click kernels. They give the same click probabilities at c=1,2,3 but differ by exactly 878769/815843875 at c=4. The construction extends to any fixed finite number of coupling settings through weighted orthogonal polynomials. The additional held-out setting is informative, not logically decisive for all possible kernels.

## III. A graph-realizable nuisance counterexample for three-scale-moment calibration

When a single eigenmode produces S~Gamma(2,2lambda), a power-distorted readout Y=kappa S^p has scalar moment ratio

    E[Y]E[Y^3]/E[Y^2]^2 = Gamma(2+p)Gamma(2+3p)/Gamma(2+2p)^2.

At p=1 the ratio is 4/3. Its claimed inference of p=1 requires genuine eigenmode isolation. For p=0.8 and a spectral mixture on eigenvalues 1 and 4, there are positive mixing weights w approximately 0.0076468189365 or 0.6057894632643 for which the same ratio equals exactly 4/3 (weights are roots of a continuous scalar equation). This is not an abstract unphysical spectral list: the three-vertex connected weighted path with consecutive edge conductances

    a=1.728713553878169, b=0.771286446121831

has eigenvalues 0,1,4. A normalized coherent preparation with spectral weights w and 1-w realizes the counterexample. Thus a nonlinear p=0.8 detector plus a mixed input can pass the ideal single-mode third-moment statistic, even though the single-mode theorem itself remains correct.

## IV. FICTIONAL cosmological candidate F2, intended to fail

**No clause below is a derivation from physics. Each is a deliberately invented postulate.**

F2.1 The prephysical world is a set V of signed relational intensities, without coordinates.
F2.2 Their magnitudes generate a positive finite or locally finite graph Laplacian L.
F2.3 Oriented loop phases constitute U(1) connections and generate cosmic chirality.
F2.4 Quantum bosonic and fermionic algebras are assigned to the relational modes; particle excitations occupy their representations.
F2.5 A stable spectral-dimension plateau and effective resistance determine an emergent three-dimensional spatial geometry.
F2.6 A modular time parameter is identified with physically calibrated evolution; homogeneous cosmic expansion is modeled by L(tau)=a(tau)^(-2)L0.
F2.7 Matter energy changes relational weights, thereby inducing gravitational response and evolving the geometry.
F2.8 An operational consistency functional selects one observer-independent physical cosmos from the class of all relational descriptions.

These axioms amount to a fictional cosmology with particles, an emergent spatial dimension, gauge orientation, gravity, and expansion. They are specifically presented so other sessions can derive contradictions.

### Falsification F2-A: expansion becomes detector calibration

By functional calculus, W_s(a^-2 L0)=W_(s/a^2)(L0), and (a^-2 L0)^+=a^2 L0^+. The scale law for a given eigenmode changes S -> a^2 S. A static universe with a detector scale drift S -> a^2 S reproduces identical scale measurements. Hence F2 cannot infer cosmic expansion from these observations without an independent reference. This challenges only F2's proposed inference, not empirical cosmological expansion.

### Falsification F2-B: real preparations cannot identify flux orientation

For Hermitian magnetic Laplacians with L_-phi=conjugate(L_phi), real spectral functions obey f(L_-phi)=conjugate(f(L_phi)). Since the expectation of a Hermitian operator is real, every real input x gives <x,f(L_-phi)x>=<x,f(L_phi)x>. All real-input scale-only experiments, including arbitrarily many couplings, are blind to flux reversal. A complex input x=(|0>+i|1>)/sqrt(2) resolves this ambiguity on a magnetic triangle at phi=pi/3; at s=0.20 the two Ricker filter-intensity probabilities differ by about -0.004395911902. The missing operational ingredient is a phase reference or a directional dynamical channel. F2 cannot claim real scalar spectral measurements have generated physical chirality.

### Falsification F2-C: a spectral dimension is not a Lorentzian spacetime

Define the fictional spectral-dimension estimator d_spec(s)=2s Tr(L exp(-sL))/Tr(exp(-sL)). For every fixed finite connected graph d_spec(s)->0 as s->0 and s->infty. A 48^3 periodic cubic graph has numerical d_spec about 3.084 at s=5, 3.019 at s=20, and nearly zero at s=1500, while at s=0.02 it is 0.235. The three-dimensional intermediate plateau does not select a unique graph topology, define a Lorentzian causal cone, or provide physical units. Cospectral nonisomorphic graphs have identical heat trace and spectral-dimension function for all s.

### Falsification F2-D: the alleged quantum and time bridges are postulates

Functional calculus of L produces a commuting algebra and cannot, by itself, supply noncommuting canonical quantum operators. Assigning a Fock space solves this formally by assumption, not emergence. Modular flow of a finite tracial state is trivial; for Gibbs rho proportional to exp(-beta H), modular flow is unitary conjugation generated by beta H, which does not independently calibrate a physical clock. This is consistent with established thermal-time research but not a derivation of F2's cosmic time.

### Falsification F2-E: operational stability cannot select more than an orbit without anchors

If a proposed consistency functional is invariant under a nontrivial stabilizer group of all available evidence, applying any stabilizer to a minimizing candidate produces another minimizing candidate. The dressed-qubit thermal example supplies such a stabilizer. F2 can at best select an observational equivalence class until new physically grounded interventions constrain the symmetry. Picking an arbitrary representative with a complexity penalty is model selection, not experimental proof of privileged locality.

### Verdict

F2 is **rejected as a prephysical derivation** of quantum mechanics, calibrated time, Lorentzian geometry and observable chirality. Some clauses remain mathematically consistent as *postulated effective physics*, but they cannot be promoted into an independently established physical emergence theorem. F2-R may be retained as a narrower operational atlas: predict only quantities invariant under the allowed representation/calibration equivalences, and demand independent phase and timing references for any stronger interpretation. F2-R is a design target, not a theory of our universe.

## V. Hand-off challenges for A, B and C

1. A: specify a nontrivial quantum observable algebra and physical clock without importing them, or prove a no-go for a clearly defined prephysical axiom class.
2. B: find a finite, resource-bounded coupling/instrument contract that provably rejects a meaningful family of context-dependent detectors; quantify unavoidable blind directions.
3. C: build phase-sensitive, source-controlled tests on magnetic graphs; preregister a real-preparation null and a complex-preparation holdout. Explicitly test expansion/scale gauge under two independent references.
4. All: keep a separate fixed-mu Wilson proof ledger. The standalone October 31 modular and nonlinear manuscripts depend on exact operator-domain and boundary entropy inputs; they are not substitutes for rechecking those dependencies. The leading logarithm in the baseline is already a distinct mathematical result.

## External context and prior art

- Lundeen et al., *Tomography of quantum detectors*, Nature Physics 5 (2009) 27-30, https://doi.org/10.1038/nphys1133.
- Guţă & Yamamoto, *System Identification for Passive Linear Quantum Systems*, IEEE TAC 61 (2016), 921-936, https://doi.org/10.1109/TAC.2015.2448491.
- Levitt & Guţă, *Identification of single-input-single-output quantum linear systems*, Phys. Rev. A 95 (2017), 033825.
- Connes & Rovelli, *Von Neumann algebra automorphisms and time-thermodynamics relation in generally covariant quantum theories*, Class. Quantum Grav. 11 (1994), 2899-2917.
- Zanardi, Lidar & Lloyd, *Quantum tensor product structures are observable induced*, Phys. Rev. Lett. 92 (2004), 060402.
- Wilming & Werner, *Lieb-Robinson bounds imply locality of interactions*, Phys. Rev. B 105 (2022), 125101 (presupposes an observable/site setup).

## Reproducibility

Run `python session_c_f2_verification.py` in the same folder as `session_c_f2_results.json`. The verification uses exact SymPy rationals for the finite-setting detector polynomial and ordinary double-precision matrices for the magnetic and finite-lattice tests. Normal and `-O` / `-OO` execution produced byte-identical JSON in the tested environment. This does not certify the upstream uploads or experimental observations. All detector and cosmological data in this note are synthetic or mathematical.
