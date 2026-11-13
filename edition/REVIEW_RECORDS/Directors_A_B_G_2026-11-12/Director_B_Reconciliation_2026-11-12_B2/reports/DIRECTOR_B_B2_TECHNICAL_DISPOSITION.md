# Director B | Second Reconciliation and Technical Disposition

**Program:** From Prephysical Hypotheses to Physical Models  
**Research direction and responsibility:** Kirtus Justus, Theoretical Physicist, Port Coquitlam, British Columbia, Canada  
**Analytic and computational assistance:** ChatGPT (GPT-6), Director B. Single model participant, not an independent sub-agent or scientific referee.  
**Date convention:** 12 November 2026, B.C. Pacific Time  
**Controlling state:** Initial External Grounding, **G1 OPEN**. No total ontology selected; no derivation of either quantum or classical mechanics from prephysical foundations claimed.  
**Output:** additive edition `FPHPM-DIRECTOR-B-2026-11-12-B2`; previous baseline and B1 preserved.

## 1. Direct-source intake and actual calibrations

The uploaded source files were opened directly. Director A's complete 24-entry archive and Director G's complete 14-entry archive were extracted in independent working directories. Their local package verifiers passed. The Director A geometry checker was rerun, reproducing six projective tangent-holonomy tests (maximum determinant absolute error `7.35974046709963e-13`) plus Gram, curvature, metric-net and dynamics tests. The Director G checker was rerun, reproducing its 96 spherical holonomy trials (maximum wrapped phase residual `1.5314274795707798e-15` rad), exact three-state phase witness, curvature check, and cap-area controls. Director G's 96-trial CSV and `RESULTS.json` were byte-for-byte unchanged by the rerun. These algorithms check different mathematical representations, not independently measured phenomena.

The carried baseline verifier passed: 645 payload files, 38 papers, 344 registry rows. The supplied PCP Version 1.0 Enterprise Edition verifier passed (ten files), and its included ACR Implementation local structural/derived verifier passed (57 payloads). Exact PCP Core 5.2, 4.4, 15.5 and 8.5 clauses were fetched using the supplied packet's read-only lookup tool. This is document retrieval and offline checks, **not** host-enforced adoption, a running PCP integration, behavioral validation, proof certification or external authentication. No executable sub-agent delegation endpoint was available, so all review passes remain sequential internal assessments by one assistant.

The separate `FPHPM_Baseline_2026-11-12_Z1.zip` and G7 manuscript cited by Director Z remain *not supplied as files*. Only Z's transmitted disposition is inspected. No source-specific G7 ladder/holonomy numerics or bibliography were invented, rerun or certified here.

## 2. Reconciliation: claims, not director personalities

| Matter | Director Z transmitted text | Directly inspected A/G plus prior B1 | Director B's controlling B2 disposition |
| --- | --- | --- | --- |
| Tangent determinant law on assumed Fubini–Study `CP^n` | Supported, unrefereed | A analytic Chern proof + six CP1–CP3 ODE trials; G tautological-bundle proof + 96 CP1 spherical trials; B1 also supported | **SUPPORTED_IN_SCOPE** as a *conditional geometric identity*. B2 directly integrates eight CP2 holonomies, with maximum error `4.953206193633819e-12`. Not a prephysical or operational selection. |
| Signed Bargmann phase from transition metric alone | Strong transport unselected | A and G exact conjugation controls; G witness `(9±3i)/16`; published qubit multistate theorem | Universal signed reconstruction **REFUTED_IN_SCOPE**. But choice of global sign can be a *representation gauge*, not an independently necessary physical law; see B2 theorem. |
| `CP^1` versus `RP^2` only separated by monodromy | Conditional discriminator | A/G: locally different curvature 4 versus 1 under the *same* normalized transition-distance rule; restricted holonomy commutants both `C` | Literal “only” geometric assertion **REFUTED_IN_SCOPE**. Narrowed restricted-statistic observation remains **CONDITIONAL**, pending actual G7 text. |
| No third-order interference + symplectic pure space selects complex QM | Conditional selection | Classical spin supplies broad countermodel, qualified by infinite-dimensional statistical state space and effect-induced metric; published Barnum–Müller–Ududec theorem requires other postulates | Universal unrestricted selection **REFUTED_IN_SCOPE**. Strong finite-dimensional operational reconstruction **CONDITIONAL** and must carry every assumption. |
| Exactly homogeneous finite carriers approach projective pure spaces | Finite cap / Gelander-Turing obstruction | Gelander's *original* theorem/corollary examined; A/G finite-orbit bounds refine symmetry scope | Exact finite-stage homogeneity under Gromov–Hausdorff convergence **REFUTED_IN_SCOPE**. Arbitrarily close *approximately* homogeneous nonsymmetric finite nets **SUPPORTED_IN_SCOPE** when the target homogeneous metric is already supplied. |
| 10.48-degree uncovered cap | Quoted | G derivation: unitary `SO(3)` >=14.83511158 deg; Wigner `O(3)` >=10.47531384 deg | Both scope-qualified lower bounds retained; `10.48°` is rounding of the second and not a strict certified inequality. Z's unseen theorem scope **UNRESOLVED**. |
| Schild-ladder `n=1,2,3` residuals | Reported approximately `1e-6` | A directly integrated tangent connection; G computed exact spherical transports; neither is a Schild-ladder rerun. Published ladder scaling caveat verified | Z-specific run **UNRESOLVED**; not conflated with A/G routines. |
| Single-system geometry uniquely fixes quantum composition | Not selected | Prior Director B1 exact separable-versus-ordinary composite witness | **NOT_IDENTIFIED_IN_SCOPE**; identical local pure geometry does not decide entanglement or Bell predictions. |
| Determinant holonomy + three pair probabilities recovers Bargmann phase | Not asserted as a separate gate | A's fixed-probability CP2 continuum; determinant exponent in A/G/B1 | **REFUTED_IN_SCOPE** for individual triangle data: two CP2 triples share all three probabilities and determinant `1`, yet have inequivalent phase `1` versus `exp(2πi/3)`; B2 proof and direct ODE checks. |
| Absolute orientation must be selected as necessary prephysical bridge | Sometimes treated as open obligation | A correctly says conjugate *representations* need not differ as ontologies; G/B1 emphasize sign warrant | **REFINED/CONDITIONAL:** quotient by *global* conjugation is sufficient for identical finite quantum-instrument statistics. A fixed external reference makes *relative* conjugation physically distinguishable. Neither establishes quantum emergence. |

Repeated director agreement is one shared evidence lineage unless there is a genuinely independent derivation or external primary source. Source-specific original claims are preserved; this table is not a silent replacement of them.

## 3. Three B2 mathematical results

### B2-T1. Full-model complex conjugation and operational equivalence (proved mathematically)

Let `rho` be any density operator on a *stipulated* finite-dimensional complex Hilbert space and let each history-dependent quantum instrument have Kraus matrices `K_{x|h}` satisfying `sum_x K†K=I` at each history. For any outcome word `w`, its quantum probability is `Tr(K_w rho K_w†)` where `K_w` is the chronologically composed operator. Under **simultaneous** entrywise conjugation of all model representations, `rho' = conjugate(rho)` and `K'_{x|h} = conjugate(K_{x|h})`, the new probability equals the complex conjugate of the original probability, hence exactly the original *real* probability. The conjugated instruments remain completely positive and trace preserving. The result holds for finite adaptive experiments and similarly for any finite-dimensional composite system when *every* component is conjugated consistently.

**Refutation control:** with `|+i>=(|0>+i|1>)/sqrt(2)` and effect `E=|+i><+i|`, `Tr(E rho)=1`, but `Tr(E conjugate(rho))=0`; if `E` is conjugated as well, the result returns to `1`. Thus global representational equivalence must not be mistaken for the claim that changing one state against unchanged physical apparatus is experimentally invisible. Complex conjugation is not being implemented as a quantum channel on an unknown input.

**Ontology consequence:** An absolute `J` versus `-J` sign is not automatically a *necessary independent operational identification* when the acceptance criterion is equality of all complete experimental statistics *up to common representation change*. Choosing an orientation relative to independently fixed reference devices is a different, stronger demand. It may be genuinely operational, and its experimental warrant must be established in that setting. This is a refinement of the obligation map, not proof that handedness, clocks or quantum dynamics are gauge in every physical theory.

### B2-T2. Determinant-holonomy branch nonidentification (exact counterexample)

In `CP^2`, for any `phi` in `[-pi,pi]`, take the Hermitian Gram matrix

```text
  G_phi = [ 1,                  1/2, (1/2) exp(-i phi) ]
          [ 1/2,                1,   1/2                 ]
          [ (1/2) exp(i phi),   1/2, 1                   ].
```

Its order-2 principal minors are `3/4`; `det G_phi=(1+cos(phi))/4 >= 0`; hence it is a realizable Gram matrix of three unit vectors in `C^3`, including the rank-two endpoints. All three pair transition probabilities are exactly `1/4`. The cyclic Bargmann invariant is `B_phi = exp(i phi)/8`. Assuming the already-proved conditional projective determinant law, the complex tangent determinant holonomy is `D_phi = exp(3 i phi)`.

Compare `phi=0` with `phi=2pi/3`. Their three pair probabilities are identical and both holonomy determinants equal `1`, while `B_0/|B_0|=1` and `B_1/|B_1|=exp(2pi i/3)`, and these two phases do **not** become equal upon global complex conjugation. Thus the scalar determinant and three distances together fail even to reconstruct the phase *modulo conjugation*. The construction embeds in any `CP^n`, `n>=2`: compare `phi=0` and `phi=2pi/(n+1)`.

**Limit:** This does not show that the *full* metric neighborhood, the entire `U(n)` holonomy matrix, or a continuously tracked family of loops cannot recover additional phase information. In particular a continuous based deformation can supply winding/branch information that a single endpoint determinant lacks. Direct B2 CP2 connection integrations of eight cases, including `phi=±pi`, passed with maximum numerical determinant error `4.953206193633819e-12`; those computations are *not* proofs nor Schild-ladder tests.

### B2-T3. Approximate-homogeneity escape lemma (proved mathematically)

Let `(M,d)` be a **compact homogeneous metric space** and let `X_epsilon` be any finite epsilon-net with the restricted metric. Then `d_GH(X_epsilon,M) <= epsilon`. For any `p,q` in `X_epsilon`, choose a genuine ambient isometry `g` of `M` with `g(p)=q`. Define a relation

```text
  R_g = { (x,y) in X_epsilon × X_epsilon : d(g x, y) <= epsilon }.
```

The epsilon-net condition and its application through `g^{-1}` imply both coordinate projections of `R_g` cover the finite set. `(p,q)` belongs to `R_g`, and for any two pairs in it,

```text
  |d(x,x') - d(y,y')|
    = |d(g x,g x') - d(y,y')|
    <= d(g x,y) + d(g x',y') <= 2 epsilon.
```

So `R_g` is a correspondence of distortion at most `2 epsilon`, interpolating any chosen `p` to any chosen `q`. It is an *approximate correspondence*, not an exact bijective isometry or a genuine finite group action. Every compact metric space has arbitrarily fine finite nets. If the target is homogeneous, such nets have this approximate transitivity irrespective of whether their exact finite isometry group is trivial.

For a **positive control**, an explicit `CP^1`-sphere latitude/longitude net with `N+1` latitudes and `2N` meridians has `2 + 2N(N-1)` distinct points, mesh radius at most `epsilon=pi/(2N)` in Fubini–Study units, and so satisfies the lemma. The distinct pole and interior nearest-neighbor degree counts show that the nets used in numerical checks are not themselves transitive. Twelve finite-net correspondence trials at `N=4,8,16`, each retaining 12,000 paired-distance samples, reproduced the distortion inequality without eliminating any trial. This is a rigorously specified *nonhomogeneous escape from an exact-homogeneity premise*, not an emergence of the sphere or of quantum probabilities: the target metric and ambient isometries are explicitly imported.

## 4. Adjusted but still entirely open bridge map

1. **Prephysical primitives -> mathematical carrier:** OPEN. The primitive, admissible relations, equivalence, observables and topology are not derived. No qubit or amplitude is presumed.
2. **Carrier -> operational outcomes / probability:** OPEN. Neither `d_FS` nor a Born-rule transition law has a nonstipulated operational warrant; finite-net positive controls import the entire target.
3. **Outcome data -> projective/symplectic structure:** conditional geometry with multiple selection gaps; *absolute conjugate orientation* may be quotiented as a common representational gauge, while relative orientation demands a fixed experimental reference. The det-holonomy scalar by itself has a root-of-unity branch ambiguity.
4. **Local theory -> multi-system composition, state/effect cones and instruments:** OPEN; separable-composite alternative survives all single-system checks. Direct composition-sensitive experiments and a justified reconstruction are required.
5. **Quantum operations -> time, energy and fields:** OPEN. A static geometry is compatible with inequivalent dynamical generators; no unit-bearing physical clock, localization or causal spacetime is supplied.
6. **Quantum -> classical Hamiltonian mechanics:** OPEN. Classical additivity or rank-one dephasing is not reversible Hamiltonian flow. A controlled asymptotic dynamical regime with observable/error correspondence is required.
7. **Model -> empirical physical ontology:** OPEN. Operational calibration, likelihoods, reproducibility, independent comparison, uncertainty, physically risky predictions and falsifiers are absent.

The quotient-by-global-conjugation observation **does not remove** composition, dynamics, physical phase references, or empirical selection obligations. It only prevents a possibly unobservable choice of global mathematical convention from being mistaken for a necessary empirical discriminator.

## 5. Specific open obligations

- **B2-OP-01:** Acquire the actual Z1/G7 manuscripts and their scripts; inspect the exact scope of holonomy/monodromy and the purported Schild-ladder runs, especially rung scaling, chart changes and phase convention.
- **B2-OP-02:** State what *operational equivalence* is acceptable for a total ontology: exact equality of all circuit probabilities modulo global representational conjugation, or additional orientation/energy/time-reference structure. Test the gate without assuming that either is fundamentally necessary.
- **B2-OP-03:** Identify a primitive experiment, with accessible effects and calibrated controls, that can distinguish composition rules (or prove an impossibility under the supplied primitive class). Never define an emergent qubit by assuming ordinary Hilbert tensor composition.
- **B2-OP-04:** If finite relational carriers are pursued, separately specify finite-stage exact symmetry, approximate correspondences and the convergence topology. The present approximate-homogeneity lemma imports `M` and therefore offers no prephysical construction by itself.
- **B2-OP-05:** Give a quantum-to-classical derivation with a *specified* time/semiclassical/decoherence limit, Hamiltonian dynamics and error bounds. Compare with experimentally accessible records and scales.
- **B2-OP-06:** Audit B2 proofs, particularly whether a concrete operational framework invalidates the global conjugation quotient or adds nontrivial phase-ref/energy orientation constraints. A single model's cross-check is not independent review.
- **B2-OP-07:** Independently verify the inherited B1 finite-group normalizer argument and entropy D8 corollary dependencies before promoting either beyond its bounded scope.

## 6. Evidence and method classification

**New B2 mathematics:** three explicit proofs/counterexamples above, conditional on *named* structures; eight CP2 tangent-ODE sanity checks, 259 Gram/phase-grid trials, 96 finite adaptive instrument tests (eight word probabilities each), and 12 finite-net tests. No sample exclusions. For `phi=±pi` the initial affine chart crossed a coordinate pole; the calculations were rerun after a deterministic **unitary chart change**, preserving those endpoints in the numerical table. An initial mistaken assertion that the 257-point grid plus two additional phases had 260 rather than 259 distinct angles was corrected; the first CSV is an identical duplicate with a wrong filename and was not shipped. The checker rejects an exponent-two holonomy mutant and detects state-only conjugation against a fixed reference.

**External evidence:** Gelander's primary 2013 theorem was inspected (including its original PDF first page), along with the publisher's 2014 Barnum–Müller–Ududec article, the published 2026 Li–Wagner–Zhang paper and Guigui–Pennec's ladder paper. External publications establish mathematical context and declared postulates; they do **not** supply laboratory validation of this prephysical program.

**Internal provenance:** A, G, Z text and prior B1 are internal participant submissions, not independent external expert corroboration. No sub-agents were available or portrayed as available. PCP/ACR is `ABSORBED_TEXT` plus targeted offline clause retrieval and local verification, not runtime enforcement; ACR's measured efficacy was not evaluated. The root review remains open; no baseline files were edited.

*This is a scoped research and reconciliation overlay, not a paper claiming physical emergence or a journal-refereed result. Research direction: Kirtus Justus. AI-assisted analysis: ChatGPT, GPT-6, Director B. No provider endorsement implied.*
