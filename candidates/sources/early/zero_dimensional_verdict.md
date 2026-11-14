# Phase II Adversarial Audit of a Provisional Zero-Spatial-Dimensional Signed-Action Steelman

**Date:** 8 November 2026 (America/Vancouver).  
**Research direction:** Kirtus Justus.  
**Mathematical, computational, and editorial auditing:** ChatGPT (OpenAI).  
**Status:** EXPLICITLY STIPULATED ONTOLOGY FOR FALSIFICATION. Conditional mathematical review; not measured physics, a completed steelman of a physical theory, an empirical test of superstrings, or a claim of publication priority.

## 1. Audit scope, source integrity, and phase boundary

Six contemporaneous uploads consist of two pasted independent research handoffs, two technical notes, and two Python verifier sources. They concern: rigidity of the original four-sign distribution under five/six-sign extension; indefinite latent-bias nonidentification at higher order; a sharp finite-action-range approximation to that four-sign law; a nonprojective thermodynamic family whose global fluctuations remain distinguishable from independent signs; spectral-generator ambiguity; and conditional IKKT/string comparators. The *previous provisional steelman* is a different candidate and must be audited separately rather than presumed vindicated by those legacy calculations.

**Correction to one source-integrity claim.** The exact named Library file `zero_dimensional_composition_independent_audit_2026-11-08(2).py` was retrieved as source. Contrary to the accompanying assertion that `F`, `comb`, `descend`, `q4`, and `tv` were missing, this version imports `Fraction as F` and `comb`, defines `q4` before its use, and defines both `descend` and `tv` before the appended checks. Thus the stated missing-name objection does not apply to the inspected file. Its `PASS` message is printed before a later appended verification block, so **a premature PASS line alone is still not a full execution certificate**. The source was not executed verbatim because its materialized path was not accessible in this computation container; no successful verbatim execution is claimed. This finding corrects a particular erroneous source criticism without independently establishing every claim in that program.

A prior working verifier, `zero_dimensional_signed_action_steelman_verifier_2026-11-08.py`, was available locally and was rerun directly in Python default, `-O`, and `-OO`; it passed 119 explicit checks in each. The **new independently authored verifier** accompanying this note passed 217 explicit mathematical checks in all three modes. Test counts are reproducibility evidence, not proof of physical validity.

## 2. The dominant internal steelman failure: neither action generates the state

The proposed root has `T in [-1,1]`, `0<r<1`, and an action `S0(T)=lambda(T^2-r^2)^2`. It independently **chooses** the prior `nu=(delta_+r+delta_-r)/2`. Therefore `S0=0` almost surely in the entire admissible fundamental ensemble. The action has no value differences on which the proposed statistical prior depends. Neither the equal weights, the source-sharing convention, nor the selected correlation `r^2` is deduced from a nontrivial action comparison; the parameter `r` is already in the action's definition.

A different `Action[]`-like quantity is defined using supplied qubit operators `Q=mZ`, `R=X` and a trace-one state `Omega_1`:

`I(Q,R)=(kappa/4) Tr[Omega_1 [Q,R]^dagger[Q,R]]`.

Since `[Z,X]=2iY`, `[Q,R]^dagger[Q,R]=4m^2 I`, so **`I(Q,R)=kappa m^2` for *every* state** on this qubit algebra. In particular its derivative with respect to the correlation parameter `r` is zero. The scaling `(m,kappa)->(cm,kappa/c^2)` leaves this action value unchanged. It does not select the root prior, state, quantum operations, composition, or effective records. The mathematical positivity of `I` does not demonstrate a physical act or chronological process.

**Scoped disposition:** reject the claim that the current action principle generates the rest of the ontology. Retain the weaker mathematical result that an algebraically nontrivial positive functional can be defined without physical time, spatial periodicity, or conventional causal ordering. Do not infer stasis from the absence of a clock.

## 3. What the replacement actually establishes

With a common latent `T=+r` or `-r`, each with probability 1/2, the signed law is

`P_N(sigma)= (1/2) prod_i (1+r sigma_i)/2 + (1/2) prod_i (1-r sigma_i)/2`.

It is exactly normalized, exchangeable, sign-reversal invariant, and **projective** under removal of any index. In particular, means are zero and distinct-index pair and four-point expectations are `r^2` and `r^4`. This is a classical de Finetti mixture, whose existence and consistency do not need quantum mechanics or physical space. It is a constructive repair of the previous quadratic *family*, not a derivation from its action.

An *optional and additional* qubit correspondence chooses

`rho_t=(I+sqrt(1-t^2) X+t Z)/2`, `Omega_N=(rho_+r^{tensor N}+rho_-r^{tensor N})/2`.

All `rho_+r` and `rho_-r` are pure. All `Omega_N` are positive, trace one, exchangeable and exactly projective under quantum partial trace. Their ordinary `Z`-basis outcome law is exactly `P_N`. This is conventional quantum-state construction and Born measurement mathematics, not emergence of the quantum formalism from the signed action.

## 4. A missing composition law quantified exactly

Distinguish two contexts, both permitted by the supplied equations:

1. **Same latent source:** `Omega_2=(rho_+ tensor rho_+ + rho_- tensor rho_-)/2`.
2. **Independent sources:** `Omega_1 tensor Omega_1`.

Write `a=sqrt(1-r^2)` and `Omega_1=(I+aX)/2`. A direct expansion gives

`Omega_2 - Omega_1 tensor Omega_1 = (r^2/4) Z tensor Z`.

The trace distance is **`r^2/2`**, achieved by measuring whether the two `Z` outcomes agree. At `r=1/2` the difference is `1/8` in ideal equal-sign probability and in optimal quantum distinguishability.

But a different allowed test, a SWAP purity comparison between two independently prepared *two-register* states, has a much smaller contrast:

`p_SWAP(Omega_2)-p_SWAP(Omega_1 tensor Omega_1)=r^4/8`, equal to `1/128` at `r=1/2`, and only `1.25e-13` at `r=10^-3`.

**This is a nontrivial observation-family sensitivity outlier.** The model is projectively consistent, but it is **not** a monoidal state family satisfying `Omega_{N+M}=Omega_N tensor Omega_M` across ordinary instances for `r>0`. It can remain consistent by retaining an independent/common-source context distinction, but that context is an additional primitive relation. Nothing in `S0` or `I(Q,R)` determines it. Calling it a physical *common cause* would further import a causal interpretation not warranted by the mathematics.

## 5. Quantum completeness fails, although conditional sign recognition improves

Each `Omega_N` is an explicit convex mixture of product density operators. Thus it is separable across all local subsystems. It cannot reproduce experimentally confirmed Bell-inequality violations as a universal physical quantum-state model under standard independent local measurement conditions.

For two qubits, the correlation matrix is `diag(1-r^2,0,r^2)` in `X,Y,Z` coordinates. The standard two-qubit CHSH optimization gives

`S_CHSH,max=2 sqrt[(1-r^2)^2+r^4] <= 2`, with strict inequality for `0<r<1`.

At `r=1/2`, it is `sqrt(10)/2 = 1.58113883...`, compared with the experimentally attainable quantum ceiling `2 sqrt(2)` and the classical Bell threshold 2. The familiar quantum algebra is already assumed, but the chosen all-size state family realizes no Bell-violating entanglement.

**Positive, scoped counterbalance.** The two conditional pure states have squared overlap `1-r^2`; across N identically prepared same-sign slots the squared overlap is `(1-r^2)^N`. If ordinary quantum optimum discrimination is allowed, the equal-prior Helstrom error is

`P_err*(N) = (1-sqrt[1-(1-r^2)^N])/2`.

At `r=1/2`, it falls from 0.25 for N=1 to approximately 0.00251196 for N=16 and 0.0000251137 for N=32. This is a valid *conditional mathematical* route to highly discriminable classical information about a shared latent sign. The source, copy-availability, optimal instrument and enduring physical record are all assumed rather than derived. The comparison avoids incorrectly claiming that separability means all information is absent.

A distinguishable entangled pair may be appended projectively while retaining explicitly selected pair labels; that evades the **exchangeability** obstruction, but supplies a coupling/selection rule not generated by the zero-dimensional action. The broader ontology is not disproved by this one finite completion.

## 6. Exact finite marginal rigidity and general higher-order ambiguity coexist

The older four-sign law `P_4(sigma) proportional 2^{-M_4^2/4}` has count masses

`(1/162,16/81,16/27,16/81,1/162)` for 0,1,2,3,4 positive signs.

If every four-index marginal is fixed to this *full* law, the five- and six-sign extensions are unique **even without presupposed exchangeability**. One proof uses the degree-four nonnegative count polynomials `K(5-K)(K-2)(K-3)` and `K(6-K)(K-3)^2`. Their zero expectations force hard support, respectively `K5 in {0,2,3,5}` and `K6 in {0,3,6}`, after which all individual probabilities are fixed. A separate exact rank computation of all sign monomials through fourth order on the allowed supports gives column rank 22 of 22 in both cases.

No consistent seven-sign distribution has all four-index marginals equal to that four-sign law. The sharp minimum total variation to the average four-slot marginal of a seven-slot distribution is `74/945`; to a four-slot marginal of an infinitely exchangeable distribution it is `47/216`. These are mathematical distributional separations, not physical detector-error levels.

**Countervailing general fact:** rigid special points in finite probability polytopes do not make higher-order correlations generally identifiable. Two latent-biased infinitely exchangeable sign models can have identical **complete** 1-, 2-, and 3-slot distributions yet differ on any given four-sign pattern by

`[eta(1-eta)/16] prod_i sigma_i`, with four-slot TV `eta(1-eta)/2`.

At `eta=10^-6`, TV is exactly `0.0000004999995`. More generally, for any finite integer k, choose an even n>k and the latent densities `nu_±(t)=[1±epsilon P_n(t)]dt/2` on [-1,1]. Legendre orthogonality makes all lower (<n) joint sign laws identical while their n-slot TV is

`epsilon * 2^n * (n!)^2/(2n+1)! >0`.

For n=4 and epsilon=1/2, this is `4/315`. **Scope qualification:** those alternative latent priors are generally *outside* the specific two-point prior supported on the minima of `S0`; they refute the *inference of a unique prior from finite observations*, not the internal consistency of a prior once postulated. Conversely, full knowledge of every finite-order marginal can identify a compactly supported latent law. The nonidentification is at each **fixed finite** observation-order cutoff, not at all possible orders simultaneously.

## 7. Bounded-action extension and global/local distinction

The supplied proof of the sharp five-sign Gibbs approximation withstands an independent exact constructive test. For per-configuration action range Delta, let R=exp(Delta)>=1. The minimum worst-case TV discrepancy across all five four-index marginals relative to the old four-sign law is

`d*(R)=16/27-3R/(3+5R)` for `1<=R<=78/5`, and `d*(R)=32/[27(5R+2)]` for `R>=78/5`.

The proof symmetrizes over permutations and sign reversal without increasing maximum error or the probability-ratio bound; with per-configuration weights a,b,c for extremal, one-away and balanced positive counts, the four-count probabilities are `(a+b,4(b+c),12c,4(b+c),a+b)`. The central-event and bounded-test dual inequalities certify the two branches. Explicit positive weights attain both. Independently, a SciPy HiGHS constrained linear program over **all 32 five-sign configurations and all five complete four-coordinate marginals** reproduced the optimum at `R=1,2,8,78/5,16,32,100` with absolute residuals below `3e-16`. This is numerical adversarial corroboration of the analytic theorem, not a substitute for its proof. At large Delta, `d*(exp Delta)=(32/135) exp(-Delta)+O(exp(-2Delta))`; exact equality is impossible at finite range under the all-four-marginals requirement. If only *one designated* four-slot marginal matters, adjoining an independent sign can reproduce it exactly with finite action range. This exception must not be lost.

A separate size-dependent quadratic family `P_N proportional exp[-b M_N^2/(2N)]` is not exactly projective, but its fixed-k marginals converge to independent fair signs. Yet its global distribution remains different from independent fair signs. At b=2 log2, the limiting full-distribution TV is about `0.207201924867`, and the KL divergence about `0.144400735194` nats. These are ideal mathematical comparisons, not observed anomalies. They show why global collective distinctions cannot be dismissed just because local pair correlations vanish. No physical access to the rescaled collective magnetization has been established.

## 8. Additional retained structural outliers

- The opposite-sign adjacency rule generates complete bipartite or empty graphs, not arbitrary local topology. The symmetric normalized Laplacian of `K_{p,q}` is isospectral at fixed p+q, whereas the combinatorial Laplacian may distinguish its splits. One scale's spectral-dimension value does not derive physical spatial dimensionality.
- Two nonisomorphic six-vertex biconnected Ising graphs share the full zero-field action-count polynomial while having a hypothetical squared-magnetization TV of `4/255` at z=1/2, and about `6.34438e-8` at z=0.99. Their per-readout theoretical KL at z=0.99 is about `1.06710e-14` nats. This is not observed physics.
- Earlier signed imaginary coherence sectors, null-normalized positive decoherence kernels, faithful-unit alternatives, double-nonnegative classical-pair subtheories and matrix-completely-positive exceptions remain retained. None has a derived physical observation rule under the present steelman.
- Ricker-like zero-mean positive-norm mathematical responses and putative 2+1 geometrical continuums remain *effective targets*, not fundamental coordinates or derived fields.
- The old finite negative-correlated four-slot law remains mathematically valid. Its failure to extend to seven slots does not refute every finite nonspatial system. Its exact five-/six-slot compatible extensions are not produced by the old everywhere-finite Gibbs action.

## 9. External comparators and the ontological contest

**Quantum de Finetti prior art:** Caves, Fuchs and Schack, *Unknown Quantum States: The Quantum de Finetti Representation*, J. Math. Phys. 43 (2002), arXiv:quant-ph/0104088. Full infinite quantum exchangeability within the complex tensor formalism leads to convex mixtures of power states. The theorem's operational reading does not establish that the latent sign is fundamentally physical.

**Thermal time / GNS prior art:** Connes and Rovelli (1994) propose a state-dependent modular flow in generally covariant quantum theory; this retains noncommutative algebra and state as inputs. The GNS theorem represents states on assumed C*-algebras in Hilbert spaces and does not itself derive the physical Born rule or accessible measurement operations. A time-unassigned *algebraic action* is therefore a genuine mathematical possibility but not a distinctive physical theory without additional dynamics and observation laws.

**Superstring/IKKT prior art:** Ishibashi, Kawai, Kitazawa and Tsuchiya (1997) propose a 0D *base-coordinate* type-IIB matrix action with ten Lorentz-index bosonic matrices, fermions and supersymmetric structure. Asano et al. (2025) identify a Lorentz-breaking-regulator artifact in a prior Lorentzian treatment. Anagnostopoulos et al. (August 2026) report 3+1 expanding structure in a deformed complex-Langevin system. Liao and Maeta (July 2026) obtain a test-scalar effective four-dimensional geometry under a specified Lie-algebra generator ansatz. These are substantive controlled or qualified comparisons, not universal physical proof. Specific perturbative string sectors have fixed four-graviton tree Gamma-factor low-energy logarithmic coefficient ratios 3/4 and 13/16 at the specified angular comparison, which the signed-action steelman does not predict.

The historical Volume Inflection Model is a separate conditional classical 5D Einstein-stress construction, not a prediction of the 0D signed root. Failure of a selected compactification to reproduce that classical event does not prove the signed ontology or disprove every string construction.

**Comparative status:** String constructions retain a pronounced advantage in developed conditional quantum/gravity mathematics. Neither contender has been certified as the uniquely true total ontology under a common physical dataset. The signed candidate cannot win by withholding predictions, and superstring theory cannot win an empirical contest solely by mathematical sophistication.

## 10. Provisional verdict and next gate

**Mathematically retained:** An explicitly assumed zero-base-spatial-coordinate signed law can have nonzero magnitude, an action-like functional with no physical time parameter, exactly consistent all-N correlated finite distributions, and a conventional quantum representation. It can give conditionally increasingly accurate classical sign discrimination with N copies, *assuming* permitted optimal quantum measurements.

**Directly rejected as explanatory claims for this steelman:** (i) the double-well action generates its selected prior or correlations; (ii) the auxiliary commutator-cost action selects correlations; (iii) the shared-source state family is identical to independent tensor composition; (iv) the fully exchangeable state family produces Bell-violating quantum entanglement; (v) the Hilbert-space and Born observation rules were derived rather than supplied; and (vi) any effective physical space, clock, causality, spin-two gravity or Ricker continuum has already emerged.

**Next adversarial test:** Require one fundamental mathematical rule that *simultaneously* fixes the admissible state and action, assigns independent/shared-source composition without inserting a preferred physical relation, specifies a stable nontrivial observation class, and predicts how geometry/time and quantum entanglement can arise. Test independent predictions against a fixed superstring/IKKT sector with matched observables. Until such a rule exists, this is a **provisional steelman under Phase II examination**, not a certified successful total ontology and not yet a warranted transition to pipeline strawman/demolition.

## Verification and references

The accompanying `phase_ii_provisional_steelman_ruthless_verifier_2026-11-08.py` executed successfully under ordinary Python, `-O`, and `-OO`. It independently tests 217 finite exact/symbolic identities including signed distributions, supported action, quantum composition, measured-source distinctions, Bell correlations, optimal sign discrimination, sharp finite extendibility, bounded-action Gibbs approximation, Legendre high-order nonidentification, and string-sector coefficient controls. General theorems additionally require their proofs above. The separate `phase_ii_full_32_configuration_minimax_lp_check_2026-11-08.py` tested the sharp bounded-action theorem against full nonsymmetrized five-sign numerical optimization. Original current-user-upload Python files were reviewed via content rather than falsely claimed executed verbatim; their materialized paths were unavailable to this container.

Selected public sources: Caves/Fuchs/Schack, https://arxiv.org/abs/quant-ph/0104088; Connes/Rovelli, https://arxiv.org/abs/gr-qc/9406019; GNS theorem overview https://www.mat.univie.ac.at/~kriegl/Skripten/2019SSe.pdf; Hensen et al. Bell experiment https://www.nature.com/articles/nature15759; IKKT regulator critique https://doi.org/10.1103/PhysRevLett.134.041603; deformed Lorentzian IKKT simulation https://doi.org/10.1093/ptep/ptag159; Liao/Maeta effective geometry https://doi.org/10.1103/gfcj-9vb3; Legendre identities https://dlmf.nist.gov/14.7 and https://dlmf.nist.gov/18.17; finite exchangeability Konstantopoulos/Yuan https://doi.org/10.1090/tran/7701.
