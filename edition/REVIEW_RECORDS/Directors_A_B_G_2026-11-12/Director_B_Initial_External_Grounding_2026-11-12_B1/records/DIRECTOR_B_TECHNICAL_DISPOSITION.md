# Director B | Initial External Grounding: geometry, topology, composition and bounded ACR review

**Program:** From Prephysical Hypotheses to Physical Models  
**Research direction / responsible author:** Kirtus Justus, Theoretical Physicist, Port Coquitlam, British Columbia, Canada  
**Reviewing participant:** GPT-6 (OpenAI), LLM Director B, at the author's direction  
**Date:** 12 November 2026, B.C. Pacific Time  
**Parent research stage:** Initial External Grounding, **OPEN**  
**Ontology:** **NOT IDENTIFIED.** No ontology selected, no stage advancement, no emergence of quantum or classical mechanics asserted.  
**Review character:** one actor with bounded self-checks and executed external-source and numerical verification. No actual separately instantiated sub-agents or external experts.

## A. Scope, governing basis and frozen-input handling

The commissioned task is *total ontology*: independently explain the emergence of quantum mechanics and classical mechanics and provide a complete physical map from genuinely prephysical hypotheses, without quietly importing an ontological system, clocks, measurements, Born probabilities, time evolution or tensor composition. This is a search objective, not a premise. This review selects no candidate merely because it is mathematically attractive. Negative and partial findings are retained.

Sources actually inspected:

1. Supplied outer archive `files(15).zip` (3 entries), containing `FPHPM_Baseline_2026-11-12.zip` (838 entries; 38 papers including two planned papers, 344 registry rows), baseline README, and D8's three-page Sobolev supplement. Baseline built-in verifier returned `BASELINE_CHECK_PASS 645 files; 38 papers; 344 registry rows; 85 legacy components accounted for`. The archive ZIP CRC checks passed.
2. Supplied `PCP_1.0_Enterprise_Edition.zip`. The Enterprise Edition verifier returned `PASS_EDITION_CHECK ENTERPRISE edition, 10 files`. The nested ACR Implementation verifier returned `PASS_LOCAL_STRUCTURAL_AND_DERIVED_CHECKS 57 payloads`, and the actual Core, Mathematics, Science and Quality Assurance provisions used were retrieved with its native local clause lookup. No product deployment or independent behavioral validation was established.
3. Supplied `Toy_Universe_Session_Packet(2).zip`, a FAR-1 construction identical in its `Toy_Universe_Specification.md` to the baseline's FAR-1 negative control (`SHA256 c39b621a85b005079559e0472dd82719577276955bce19257e9f13ff938e8986`). The toy model explicitly stipulates complex amplitudes, quantum probabilities, tensor composition, an update index and expansion law. It is not a competing derived ontology.
4. Director Z's *quoted disposition* (claimed edition `FPHPM-BASELINE-2026-11-12-Z1`). The actual claimed Z1 ZIP, G7 manuscript, calibration log and disposition files were not among the inspected attachments; accordingly specific G7 computations, bibliographic entries, and the reported n=1,2,3 Schild errors are **not independently verified against their source** here. The supplied pre-Z baseline contains only a `PLANNED.md` stub for G7. This is a source-bound limitation, not an assessment of Z's honesty or correctness.
5. Externally published sources actually retrieved and examined in pertinent portions: Gelander (2013) on limits of finite homogeneous metric spaces (theorem/corollary, first-page PDF screenshot inspected); Guigui–Pennec (2021 online, 2022 volume) on proper Schild rescaling; Barnum–Müller–Ududec (2014) on exact single-system postulates; Eftaxias–Weilenmann–Colbeck (2023) on GPT tensor products; University of Chicago's finite `SO(3)` subgroup classification notes; Rabei–Arvind–Mukunda–Simon (1999) on Bargmann phases; and a published Shamir–Strichartz multiplier-range summary cited in the D8 subcheck. Independent bibliographic authentication beyond publisher/repository presentation was not performed.

**Source boundaries:** Hashes and built-in release verifiers establish local file consistency, not publisher authenticity or correctness of the statements. The prior Director B/C/D reviews are **internal research provenance / self-citation**, not independent evidence. A previous subreview agreeing with this report must not be counted as an extra vote.

## B. Scoped mathematical dispositions

### B-GEO-01 | Complex-projective holonomy determinant identity

**Claim:** For a piecewise shortest geodesic polygon of nonorthogonal neighboring rays in `CP^n` with `B = ∏⟨ψ_i|ψ_{i+1}⟩ ≠ 0`, the Levi-Civita tangent holonomy's **complex** determinant equals `(B/|B|)^(n+1)` with the manuscript's fixed bra-ket, path-orientation and complex-structure conventions.

**Finding:** `SUPPORTED_IN_SCOPE` as an exact **conditional mathematical identity**, not as physical emergence. There is an explicit bundle-level proof in the attached paper. Let `L` denote the tautological line bundle and `Q` its quotient; `T^(1,0) CP^n = L* ⊗ Q` and `det T = (L*)^(n+1)`. Geodesic horizontal lifting of `L` accumulates holonomy `(B/|B|)^(-1)`, so tangent complex determinant holonomy is `(B/|B|)^(n+1)`. The real determinant is simply `+1` and is not the same quantity.

**Independent executed check:** seeded 1,000 random nonorthogonal `CP^1` triangles; comparison of `exp(i Ω)` from oriented Bloch solid angles with `(B/|B|)^2`: maximum complex absolute residual `1.7045 × 10^-14`. A deliberately incorrect first power failed the known-invalid mutation check. Tests do not prove the `n>1` identity; the symbolic bundle proof supports its generality.

**Essential limitation:** This starts with a **complex Hilbert space**, inner product, transition-probability geometry, complex tangent structure and induced connections. The measured agreement of geometric phases in any physically instantiated system is a distinct empirical claim and was not established. A pure transition-probability **metric** invariant under conjugation does not select the sign of the complex structure; `b` and `conj(b)` are isometric mirror descriptions. An `(n+1)`-fold root of a determinant also leaves a discrete phase ambiguity without further structure. This is a normalization/representation caveat, not a physical counterexample to quantum mechanics.

### B-MON-02 | Real three-level projective monodromy

**Claim:** `RP^2` and `CP^1 ≅ S^2` differ globally even though their local spherical geometry can be scaled to agree. `RP^2` admits a reflection tangent-holonomy return map along a noncontractible loop.

**Finding:** `SUPPORTED_IN_SCOPE` mathematical. The lift of the `RP^2` noncontractible loop from north to south along a great semicircle has parallel basis `(T(t),e_y)`. On identifying south and north via the antipodal map, the return map is exactly `diag(1,-1)`. Its determinant is `-1`. Curvature generates the connected `SO(2)` holonomy, so full holonomy is `O(2)` and its real commutant is only `R·I`; for the oriented simply connected sphere it is `SO(2)` with commutant `C`. This explicitly demonstrates the need to test **full** holonomy and global loop structure rather than only restricted/infinitesimal holonomy. No physically observed monodromy is claimed.

### B-FIN-03 | Quantified uncovered cap for finite exact spherical homogeneity

**Claim:** Any nonempty finite exactly transitive metric subset `S ⊂ S²` under the **induced spherical geodesic distances** has covering radius at least `acos(59/60)`.

**Finding:** `SUPPORTED_IN_SCOPE` as a mathematical theorem, under the stated definition of exact homogeneity and the standard classification of finite subgroups of `SO(3)`.

**Proof split:** (a) if `S` spans a proper subspace of `R³`, a spherical point at angular distance `≥90°` exists. (b) Otherwise its finite full distance-isometry group `Γ` embeds in `O(3)`; `Γ+` has index ≤2. The three exceptional rotation families have group order ≤60, hence orbit cardinality `N≤120`. A covering by `N` caps of radius `r` needs `N 2π(1−cos r)≥4π`, yielding `r≥acos(1−2/N)≥acos(59/60)`. (c) Axial cyclic/dihedral groups with nonexceptional orders preserve an unoriented principal axis, yielding at most two latitude circles and therefore covering radius `≥45°`; the few small-order axial exceptions have `N≤8`, covered by (b)'s area reasoning.

**Calculated constant:** `acos(59/60)=10.475313843229452°`, conventionally rounded to `10.48°`. A strict literal lower bound of *at least* `10.48°` is not established by this argument: `10.48` is a rounded figure and slightly exceeds the proved constant. The result is not known sharp.

**Scope guard:** Finite symmetric orbits embedded in `S²` are not all finite approximating structures. Allowing irregular finite sets or asymptotic (rather than exact) homogeneity evades this specific bound. It does not exclude an emergent continuous quantum model from all finite prephysical structures.

### B-FIN-04 | Gromov–Hausdorff finite homogeneity obstruction

**Claim:** No sequence of **finite homogeneous metric spaces** converges in Gromov–Hausdorff distance to any positive-dimensional `CP^n` with its Fubini–Study metric.

**Finding:** `SUPPORTED_IN_SCOPE` as an application of **Gelander's published 2013 theorem**: the only manifolds approximable by such finite homogeneous metric spaces are tori. `CP^n` is not a torus. The theorem and corollary were inspected on the source PDF's first page and the journal extract; its full published proof was not line-audited in this session. This obstruction is stronger in its target domain than the embedded-orbit covering bound, but it does not apply without a **metric Gromov–Hausdorff convergence** hypothesis or if finite approximation need not be exactly homogeneous.

### B-COMP-05 | Nonselection of entangled composites from all elementary-system holonomies

**Claim under test:** Complete access to elementary-system qubit pure-state geometry, Fubini–Study metric, all qubit Born statistics and unitary single-system transformations is sufficient to determine ordinary complex **quantum composition**.

**Finding:** `NOT_IDENTIFIED_IN_SCOPE` (with an explicit two-model witness). The ordinary bipartite state space is all positive trace-one operators on `C²⊗C²`. The minimal GPT composite contains only the convex hull of product states, with standard local quantum effects/operations and separability-preserving global instruments. Both have identical *single-system* preparations, effects, reversible dynamics, transition probabilities and holonomies. The two-system Bell state is available only in the ordinary quantum composite: partial transpose eigenvalues `(-1/2,1/2,1/2,1/2)` prove it is entangled; its CHSH value is `2√2`, versus at most 2 for all separable states under local binary observables. The scripted checks reproduce `2.8284271247461894`, minimum partial-transpose eigenvalue `−0.5` up to floating-point error, and sampled product-state CHSH values no larger than 2.

**Interpretation:** This is a **refutation of sufficiency for that premise set**, not of quantum mechanics, and not of reconstruction programs imposing extra compositional assumptions. The exact insufficiency question is NOT_IDENTIFIED rather than asserting a physical ontology is disproved. Explicit operator-state models supply a constructive witness, not a count of unsuccessful ontological guesses.

### B-CLASS-06 | Scope of the claimed geometric discriminator

**Question:** Does no third-order interference by itself restrict single-system theories to the list for which a symplectic or holonomy-commutant discriminator might pick the complex case?

**Finding:** `UNRESOLVED` **as stated without additional postulates**. The published Barnum–Müller–Ududec 2014 classification uses **three** input postulates: classical decomposability, strong symmetry and no higher-order interference; a related fourth, observability of energy, is used for a further result. The list of real, complex, quaternionic, three-level octonionic theories and generalized balls cannot be imported from **no third-order interference alone**. Within the precisely delimited listed pure-state geometries, a globally defined symplectic structure is a promising mathematical discriminator; a proof of its full stated exhaustiveness and of physical access to it remains an obligation. The real `RP²` example above supplies an explicit full-versus-restricted holonomy witness, without claiming a real-quantum experiment was run.

### B-LAD-07 | Schild's ladder is a computation of a presupposed connection

**Finding:** `SUPPORTED_IN_SCOPE` for published convergence *with specified scaling*, `NOT_IDENTIFIED_IN_SCOPE` for any inference that ladder output itself establishes a prephysical-to-quantum bridge. Guigui–Pennec 2021/2022 analyze the error and show that appropriate scaling of the transported vector is required for convergence of iterated ladder schemes, with up to quadratic convergence under stated assumptions. They do **not** establish complex quantum identification from a generic metric. The Director Z quoted `~10^-6` computations for dimensions 1, 2 and 3 have not been source-rerun here, so these particular residuals remain `UNRESOLVED` as empirical execution claims. The earlier baseline's `6.2×10^-7` number remains an inherited output and is neither erased nor counted as independent confirmation.

### B-D8-08 | Supplementary D8 Sobolev bound (scoped)

**Input:** The separately supplied 3-page `D8_Uniform_Sobolev_Bound.pdf` is byte-identical to baseline D8 part 17 (SHA-256 `f4fc667565625b32ecc060110a2ade348a3c9b84f0054dec5bfd66fb4a37635f`). Its source TeX is present in the baseline.

**Finding:** `SUPPORTED_IN_SCOPE` for its displayed **algebraic operator-norm reduction** under the well-known Shamir–Strichartz interval-indicator multiplier theorem for `0≤s<1/2`. Each `P_b^c` is a Fourier-symbol orthogonal projector, hence contracts `H^s`. The inner/outer block action then gives `||H(X_b)||_(ℋs→ℋs)≤max(c_s,c_s')`, so `||Y_θ||≤M_s=1/2+max(c_s,c_s')≤3/2+2κ_s` uniformly in θ and μ. The **corollary** still explicitly assumes lattice estimate (B8), lattice contraction, the nuclear ideal input, and polynomial coefficient bounds. These were not reproved; the full Wilson entropy theorem is **not** independently certified by this subcheck. Source numerical sanity checks are not treated as analytical proof.

## C. Ontological map: necessary edges, present status

| From | To | Requirement | Disposition |
|---|---|---|---|
| Bare prephysical relational primitives | Probabilistic preparations and records | Defined empirical interface without imported Born rule or clock | **Open** |
| Operational model class | Complex local quantum geometry | Derived assumptions, no-I3 conditions, class discrimination, signed phase access | **Conditional mathematics; physical bridge open** |
| Local complex quantum geometry | Quantum multi-system composition | Justified tensor product, entanglement, transformation/effect structure | **Not identified; explicit minimal-composite witness** |
| Quantum multi-system operations | Real-time dynamics and fields | Hamiltonian, localization, physical clock and units, Lorentz/gauge structure | **Open** |
| Quantum dynamics | Classical phase-space mechanics | Explicit scaling/decoherence/coarse-graining assumptions, observables, errors and limits | **Open; classical stochastic dephasing alone insufficient** |
| Entire mathematical map | Physical model | Calibrated observation, uncertainty, independent prediction and falsification | **Open** |

A plausible sequence of conditional mathematical arrows, however elegant, cannot stand in for an actual construction of the missing arrows. The program is not restricted to this particular ordering: alternative non-spacetime/non-signal primitives and nonmetric limit constructions remain open candidates. No toy ontology was promoted merely because CP geometry is internally coherent.

## D. Director Z reconciliation (source-controlled)

**Retained as mathematical leads:** determinant identity; global topology/monodromy as a discriminator; limits on exactly homogeneous finite carriers; calibrated ladder methods. These now have direct analytic arguments or published anchors **within specified domains**. The numeric residuals and source-specific G7 arguments remain quotes until original artifacts are inspected.

**Sharpened conditions:** (1) exact determinant identity requires complex determinant and fixed complex structure, excludes orthogonal adjacent rays and carries a conjugation/phase-root caveat; (2) Gelander applies to Gromov–Hausdorff exact homogeneity and cannot exclude heterogeneous limits; (3) the `10.48°` bound is rounded from `10.475313843...°`; (4) the classification of generalized quantum-like single systems requires all the Barnum–Müller–Ududec postulates used for the listed alternatives, not no-I3 in isolation; (5) even perfect local-holonomy identification leaves composition unselected.

**Status:** No change to parent Initial External Grounding, no ontology selected, no G7 source silently invented or imported. No upstream research baseline or PCP release modified. The standalone B packet is an additive, independently traceable handoff. Any future Z1 merge should map by theorem statement and actual source identity, not by filename or chronology alone.

## E. Bounded ACR usage and method lessons

- **Root review:** single `FOCUSED` review of G1/G5/G6 only; user goal and original broad claim retained. Core + Mathematics + Science + Quality Assurance provisions were explicitly applied. Engineering, Cryptography and Statistics modules were not formally selected merely because software hashes or numeric residuals occurred.
- **Nested bounded self-checks:** B-GEO (analytic bundle proof + wrong-exponent control); B-FIN (finite-group branch split + axial contrary check); B-OPS (composition counterexample + Bell/PPT); B-D8 (multiplier-bound algebra). These are sequential focused investigations by the **same participant**, not four independent agents. No autonomous sub-agent execution facility was available, and no role-played assessor dialogue was counted as independent review.
- **Propagation/termination:** no recursion on already passed local integrity checks; no unwarranted FULL-gate claim. A nested review closes when a bounded witness or unresolved dependency is recorded. Material source changes reopen only affected claims. Avoid repeated confirmations from shared sources. Maintain exact scope, units, quantifiers, source date and evidence level through handoffs.
- **Observed tool use:** local PCP Edition/ACR verification programs, local clause lookup, baseline verifier, SHA-256 and ZIP CRC, a fresh independently written NumPy program, its known-invalid mutation controls, source-web retrieval and inspected PDF page. None is a host-integrated ACR enforcement control or a behavioral trial of ACR effectiveness.
- **Proportionate quality:** one positive source acceptance, one wrong-exponent rejection, one false Bell-target rejection. These demonstrate that this verifier detects **those two** deliberately injected faults. It has no established sensitivity to other faults and is not a proof checker for the general theorems.
- **Specific method improvement:** prioritize *minimal operational countermodels* when an attractive geometric theorem is presented as a selection principle. The CP^n determinant law is mathematically sound in its declared model, but the minimal tensor-product construction immediately tests whether the inferred full quantum ontology was actually selected. This reduces agreement/precedence bias without assigning blanket skepticism to valid mathematical results.

## F. Open items retained or newly isolated

1. **O-B-01:** Obtain Director Z's actual Z1 archive/G7 sources, reproduce its n=1..3 ladder methods, inspect code for vector scaling and numerical error enclosure, verify citations and exact 10.48° theorem premises. No conclusion about those files is made absent them.
2. **O-B-02:** Establish whether a physically realizable **prephysical** relation can select the transition-probability geometry, the complex structure **up to physical gauge**, a valid effect cone and operationally meaningful oriented triple phases. Do not presume a qubit exists prior to this derivation.
3. **O-B-03:** Give and test explicit, independent composition and reversible dynamics principles capable of excluding the minimal separable-composite witness without importing the desired ordinary quantum answer.
4. **O-B-04:** Check higher real/quaternionic/octonionic projective holonomy groups, relevant low-dimensional exceptions and global topology directly against primary mathematical sources, not memory-based tables alone.
5. **O-B-05:** If any finite homogeneous approximation is proposed, write the exact metric, group action, embedding/limit topology and homogeneity conditions. Investigate *asymptotically* homogeneous or asymmetric carriers without importing continuum structure.
6. **O-B-06:** Supply a unit-bearing calibrated physical time/space map and a mathematically controlled quantum-to-classical limit with identified observables, dynamics and errors; FAR-1 dephasing is not a Hamiltonian classical mechanics derivation.
7. **O-B-07:** For D8, independently inspect B8, B7, B6, polynomial coefficient and trace-class hypotheses before any claim to close the Wilson entropy chain; the present local reduction alone does not close those dependencies.
8. **O-B-08:** Independently audit this B packet's proofs and potential edge cases, especially the normalizer/axis clause in the finite-orbit covering theorem, and prove/refute any unexpected counterexamples. An internal self-check cannot replace expert assessment.

## G. End-of-session disposition

`TOTAL_ONTOLOGY = NOT_IDENTIFIED_IN_SCOPE` (for presently examined input information and retained untested bridge obligations); this is **not** a universal impossibility theorem or a prediction that no future model can work. `PARENT_STAGE = INITIAL_EXTERNAL_GROUNDING / OPEN`. The new mathematical findings are scoped to conditional geometry, topology, finite homogeneity and composition. Open source gaps remain explicit; no phase transition or manuscript baseline promotion follows.

*All AI-authored analyses and executed local checks in this packet are internal research provenance, not external expert review. Scientific responsibility and research direction remain Kirtus Justus. No endorsement by OpenAI or any other provider is implied.*
