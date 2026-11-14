# Signed-Action Configuration Model: Explicit Ontological Stipulations and Conditional Tests

**Research stage:** Second external grounding, reconciliation, and construction of a total-ontology falsification target  
**Local research date:** 8 November 2026 (America/Vancouver)  
**Research direction:** Kirtus Justus  
**Independent calculations, literature comparison, drafting:** ChatGPT (OpenAI)  
**STATUS:** **EXPLICITLY STIPULATED, UNESTABLISHED ONTOLOGY.** All finite results below are conditional mathematical facts. They do not establish a prephysical reality, a fundamental signal, empirical novelty, spacetime emergence, or a derivation of quantum mechanics. This is not a paper or a finished steelman.

## 1. Purpose and provenance

The problem is to construct a clearly falsifiable candidate, rather than label an existing mathematical model a total ontology. Earlier conditional results leave three mathematically different possibilities open: (i) clock-free signed variational structure; (ii) positive decoherence kernels and compositional effects; and (iii) operationally closed state/effect/transformation packages. Their connection has **not** been derived. The original conceptual diagram (opposed signed spectra -> afrequent action/amplitude domain -> proposed effective geometry -> continuum response) is treated solely as a conceptual reference, not as evidence or a derived arrow.

**Reconciliation of supplied packet:** Rank-dependent normalization supports only a rank-r operational quotient under unrestricted PSD-affine assumptions; a faithful hybrid unit `J_N+delta I_N` is not multiplicative with the same delta on every composite dimension; compact doubly nonnegative kernels are coarse-graining/tensor closed but possess a classical paired-label interpretation; trace-normalizing J-normalized kernels is tensor-multiplicative but not mixture-affine; positive-direction and all-copy effect no-go theorems apply only under their stated observation law. The uploaded mathematical verifiers were inspected as source. The independent verifier accompanying this document was executed in ordinary and optimized Python modes; no verbatim execution of unmounted uploaded verifiers is claimed.

## 2. External grounding and novelty boundaries

1. **Causal fermion systems:** Finster, Grotz and Schiefeneder (2011), arXiv:1102.2585, already examine self-adjoint operators having signed spectra, a measure and a causal variational principle, with proposals for emergent spacetime. The October 9, 2026 paper of Finster and Fischer, *The Continuum Limit Analysis of Causal Fermion Systems for Curved Spacetimes* (Letters in Mathematical Physics 116, article 137), proves an Einstein–Dirac correspondence **in a setting constructed from algebraic QFT on a given globally hyperbolic spacetime**. The July 2026 Finster–Krpoun preprint's Einstein-equation derivation assumes smooth manifold support. These are substantial conditional results, not assumption-free origins of spacetime.
2. **Graph structure and quantum emergence:** Markopoulou and Smolin, *Quantum Theory from Quantum Gravity*, Phys. Rev. D 70, 124029 (2004), propose a route using a background-independent graph, stipulated low-energy dynamics and stochastic fluctuations. Konopka, Markopoulou and Severini, *Quantum Graphity: A Model of Emergent Locality*, Phys. Rev. D 77, 104029 (2008), study emergent locality in dynamic graph models. Both predate this hypothesis.
3. **Quantum measure and operational time-neutrality:** Sorkin, *Quantum Mechanics as Quantum Measure Theory* (1994); Boës and Navascués, *Composing Decoherence Functionals* (2017); Oreshkov and Cerf, *Operational Quantum Theory without Predefined Time* (2016, with erratum) already cover mathematically related generalizations. Oreshkov–Cerf explicitly import Hilbert spaces, boundary operations and probabilities. None certifies this candidate.
4. **Operational closure:** Filippov, Gudder, Heinosaari and Leppäjärvi, *Operational Restrictions in General Probabilistic Theories* (2020) show that physically plausible restrictions must be evaluated under classical mixing and postprocessing. Our proposed provisional quantum readouts are imported, not derived.

No novelty claim is warranted for the list of ingredients, the Ising partition functions, or the Born-rule comparison. The only potential novel claim would be a *further* precise derivation or physical prediction that withstands these comparators.

## 3. Totality conjecture [STIPULATED, UNPROVED]

**T0:** The physical world, including quantum laws, classical facts, causal direction, spacetime, continuum fields and gravitation, is an effective regime of a clock-unassigned signed-action structure. Opposite signs carry nonzero intrinsic magnitude, and action-dependent relative coherence gives rise to physically meaningful correlations under a uniquely justified composition and access rule. Effective space, time and a continuum are **not assumed to be physical** at the most fundamental level.

This is a claim to *attempt to derive and potentially disprove*, not a consequence of the finite model below. It is permissible here to stipulate a candidate for falsification; the scientific burden is to expose every such stipulation rather than treat it as established.

## 4. A concrete finite candidate [ALL INPUTS STIPULATED]

**S1: Pregeometric relations.** Choose a finite undirected graph `G=(V,E)` as a combinatorial relation, not a physical metric, space, or succession of moments. Give each vertex a mathematical sign `sigma_v in {+1,-1}` and an intrinsic magnitude parameter `m>0`. The sign is an algebraic charge candidate, **not** electric charge, physical chirality or spatial direction.

**S2: Time-neutral action.** Choose `kappa>0` and

`S_G(sigma) = 2 kappa m^2 f_G(sigma)` , where `f_G` counts edges whose endpoint signs agree.

This is the fixed-magnitude restriction of the previously verified antiferromagnetic graph action. It contains no time parameter or causal arrow. Its zero-action global minimizers exist on bipartite graphs, but balanced global signed sums also require equal bipartition sizes. Frustrated graphs have positive minimum action.

**S3: Weights and conjugate phases, both imported.** Choose parameters `beta>0`, `chi>0`, let `z=exp(-2 beta kappa m^2)` and `theta=2 kappa m^2 / chi`, and set

`Z_G(z)=sum_sigma z^(f_G(sigma))`, `p_G(sigma)=z^(f_G(sigma))/Z_G(z)`.

Introduce another algebraic sign label `s in {+1,-1}`. Stipulate conjugate action amplitudes `exp(+i S_G/chi)` and `exp(-i S_G/chi)`. This imports a Gibbs-type weighting and a complex phase/action law. `chi` has not been identified as Planck's constant or a physical clock scale.

**S4: A provisional quantum chart, emphatically not derived quantum theory.** Stipulate the trace-normalized state

`|Psi_G> = sum_sigma sqrt(p_G(sigma)/2) ( exp(i theta f_G(sigma)) |sigma,+> + exp(-i theta f_G(sigma)) |sigma,-> )`.

This has norm one. It uses a complex Hilbert space, tensor factors and Born-style operators that must eventually be derived or replaced for T0 to qualify as a total ontology.

**S5: Composition and mixtures.** For independently designated systems `A,B` with **separate sign sectors** stipulate `|Psi_AB> = |Psi_A> tensor |Psi_B>`. A *shared* sign sector would be another, coupled model, not the independent-composition law. For ordinary preparation randomization stipulate convex mixing of trace-one density matrices, not J-normalized kernels. This is an explicit operational choice, not a prephysical deduction.

**S6: Provisional experimental comparison.** After tracing the graph configurations out, permit conventional quantum joint readouts of two independently prepared sign systems, including a SWAP-symmetry test. This assumption imports ordinary quantum instruments; it creates a falsification target, not a derivation of those instruments.

No separate foundational `R` variable, ordinary physical time, space, or spatial frequency is assumed by the finite formula. The roles of the diagram's `R`, effective 2+1 geometry and continuum remain **unassigned and open** rather than filled in arbitrarily.

## 5. Conditional deductions [PROVED UNDER S1–S6]

The sign marginal is

`rho_G^(sign) = 1/2 [[1,C_G],[conj(C_G),1]]`, with

`C_G = Z_G(z exp(2i theta))/Z_G(z)`.

It is positive because it is a convex mixture of normalized sign-qubit pure states. With `Q=m Z_sign`, `Tr(Q rho)=0` while `Tr(Q^2 rho)=m^2`. This is nonzero algebraic magnitude despite zero average signed charge; it does **not** prove complex amplitudes themselves cancel for every configuration, nor derive conservation of physical charge.

The sign marginal has `Tr(rho^2)=(1+|C_G|^2)/2`. A **separately stipulated conventional two-copy SWAP measurement** gives

`p_swap+ = (3+|C_G|^2)/4`.

The result is invariant under `S_G -> S_G + constant`, which rotates `C_G` by a common phase, and under signed exchange, which conjugates it. These are appropriate gauge/label controls. Measuring a fixed `X_sign` axis without an independently justified phase reference would instead be a spurious claim of absolute action orientation.

### Exact graph comparison, with parameters fixed in advance

For the triangle `C3` and square `C4`, exact counts give

`Z_C3(z)=2z(3+z^2)` and `Z_C4(z)=2(1+6z^2+z^4)`.

At `z=1/2` and `theta=pi/8`,

- `C_C3 = exp(i pi/4)*(12+i)/13`, `|C_C3|^2 = 145/169`, `p_swap+(C3) = 163/169`.
- `C_C4 = (15+24i)/41`, `|C_C4|^2 = 801/1681`, `p_swap+(C4) = 1461/1681`.
- The exact contrast is `27094/284089`, approximately 0.0953715209.

All equations were independently checked by exact finite enumeration and complex-matrix calculations. **These are conditional predictions of a standard quantum state preparation with a specially chosen action-dependent phase.** They are not measured values or evidence for a new physical mechanism. A conventional quantum implementation of precisely those states reproduces the same predictions, so these numbers alone do not discriminate T0 from quantum mechanics.

### Action-shift and magnitude nonidentification

Adding an action constant changes `C_G -> exp(2ic/chi) C_G` but leaves `|C_G|` and the SWAP prediction unchanged. Under `m->a m`, `kappa->kappa/a^2`, the parameters `z` and `theta` are unchanged. Consequently this proposed observation class does not identify `m` independently of `kappa`. Calling `m` intrinsic does not supply a physical scale.

### Coarse-graining obstruction

For every trace-preserving channel `Lambda` acting only on the configuration register,

`Tr_config[(Lambda tensor id_sign)(rho)] = Tr_config[rho]`.

This is the ordinary no-signalling identity. Hence nonselective coarse-graining or dephasing of configurations **cannot change the sign marginal** or its SWAP prediction. Selecting a branch, coupling an environment to the sign, or using a different operational rule may change the situation, but each is an additional mechanism. A coarse-graining arrow in a conceptual diagram cannot be promoted to physical classicalization without specifying it.

### A stronger counterexample: distinct graph ontologies with identical action statistics

For **every** tree on `n` vertices, every assignment of same/opposite labels to its `n-1` edges is realized by exactly two vertex-sign configurations (choose one root sign; all other signs follow). Consequently

`Z_tree(z) = 2 (1+z)^(n-1)`

regardless of the shape of the tree. The action-phase contrast `C_tree=Z_tree(z exp(2i theta))/Z_tree(z)` and every sign-register readout computed from that contrast are therefore identical for all trees of equal size, at **every** parameter value.

The four-vertex path and the three-leaf star are nonisomorphic. Their zero-action signed configurations differ importantly: the path has total vertex-sign sum zero, whereas the star's zero-action assignments have signed sums `+2` and `-2`. Yet their action histograms are identical: two assignments with no equal-sign edges, six with one, six with two, and two with three. The independent exact verifier checks both graphs and the differing signed sums.

**Scope:** The nonidentifiability concerns the proposed reduced sign-register statistics and observables depending only on the action-count histogram. It is **not** an impossibility of graph tomography using independently available measurements of the full configuration register. Such measurements have not yet been derived. The example therefore exposes a blind spot in the current bridge, not a proof that relational topology is unreal.

The cancellation of the *sign-register* mean `Tr(Q rho)=0` is imposed by equal amplitudes for `s=+/-`; it is not derived from balance of the graph's vertex signs. The star counterexample makes that distinction unmistakable.

### Refinement extension S7 [ADDITIONAL STIPULATION; NOT CONSTRUCTED]

To turn the finite sector into an attempted **total ontology** rather than an isolated graph model, stipulate that a directed family of finite relational systems exists, equipped with normalization-preserving maps `R_{ell->k}` between different descriptions. These maps must obey projective consistency `R_{ell->k} R_{m->ell} = R_{m->k}` and `R_{ell->k}(rho_ell)=rho_k` when the descriptions refer to one effective physical state. Their indices label *resolution*, not physical times. Any operation class must be closed under the independently justified product and preparation-mixture rules. This is a **desired extension axiom**, not a theorem or an exhibited compatible family.

A direct obstruction arises even at the classical `p_G(sigma)` level. Compare a triangle with an edge after summing over the third vertex. For each fixed equal-sign pair, the marginal unnormalized weight is `z^3+z=z(1+z^2)`. For each fixed opposite-sign pair it is `2z`. Thus the effective two-spin coupling ratio is

`z_eff(triangle -> edge)=(1+z^2)/2`, which differs from the original `z` unless `z=1`.

For instance, `z=1/2` becomes `z_eff=5/8`. By contrast, removing a leaf from a three-vertex path preserves the original edge coupling ratio `z`, because the removed leaf contributes a common factor `1+z`. These identities were checked exactly in the independent verifier.

Thus even a familiar *classical* limit requires a stated renormalization/coarse-graining rule on loops. A fixed-coupling graph-action family is not automatically projectively consistent. Any purported continuum derivation must accommodate induced effective couplings and, on more complicated graphs, possibly additional interactions. Such running is standard statistical-mechanical prior art, not evidence of new prephysical activity.

## 6. A continuum test, not a continuum derivation [OPEN]

Given a graph, one can *define* a spectral diffusion diagnostic on its ordinary graph Laplacian `L_G`:

`K_G(tau) = Tr(exp(-tau L_G))/|V|`, `d_spec(tau) = -2 d(log K_G)/d(log tau)`.

Here `tau` is a mathematical resolution parameter, not physical time. On a fixed finite connected graph, `d_spec(tau)->0` as `tau->0` and `tau->infinity`. Therefore a putative effective two-spatial-dimensional plateau must occur at intermediate scales in an appropriate **sequence** of graphs. Even such a plateau would not derive a Lorentzian 2+1 spacetime, a physical clock, spatial periods, or a gravitational field equation.

A Ricker/Mexican-hat wavelet with zero integral and positive norm is a valid **target effective response** only after an effective continuum, measure and differentiation structure have been justified. It is not the fundamental domain or a derivation of that continuum.

## 7. Immediate failure tests and outliers [RETENTION WITHOUT ENDORSEMENT]

- **First quantitative failure:** The finite law depends on freely chosen `beta` and `chi`. If they are fitted anew for every graph or observation, its graph contrast is not a held-out physical prediction. Common parameter values must be independently fixed before tests.
- **Second failure:** Ordinary quantum states and Born measurements were stipulated; the finite model is not a derivation of quantum mechanics. A successful SWAP statistic would be a successful *standard quantum* prediction, not distinguishing empirical evidence.
- **Third failure:** If physical readouts are required to follow only the earlier J-normalized universally affine effect rule, that rule cannot access nonconstant full-cone information. The present Born chart changes normalization and effect assumptions. Its legitimacy must be established.
- **Fourth failure:** The action has no time, but nothing establishes it as physical activity. The candidate still needs operational clocks, causal interventions and an account of arrow selection.
- **Fifth failure:** No derivation exists of spatial locality, effective 2+1 Lorentzian geometry, continuum wavelet response, Einstein dynamics, or observed quantum fields.
- **Outliers retained:** fully imaginary coherence detectable by extended measurement contexts; nonnegative doubly-nonnegative kernels that possess classical pair models yet are operationally closed; faithful hybrid units whose monoidal composition fails; positive rank-one-null sectors; two-copy coherence reconstruction up to conjugation; scale-dependent graph frustration; and singular limits in which normalization sensitivity vanishes except under double scaling. None is discarded, and none is proof of a prephysical ontology.

## 8. Next Phase-II reconciliation obligation

Compare the proposed graph-action-to-complex-phase law with causal fermion systems' causal action, quantum graphity's graph dynamics, Sorkin's quantum measures, and operational theories without predefined time. The comparison must identify what each framework takes as a premise, what it actually proves, and which observation would discriminate them. Search for rules that tie a **state cone, unit functional, effects, instruments, composition, and continuum limit** to one independently justified action law, without deriving conclusions already inserted through assumptions.

**Decision:** T0 is now a *defined, conditional finite-sector candidate inside a stipulated total ontology*. It has not earned a complete steelman, physical certification, novelty certification, or the status of a total physical theory. The external grounding and construction phase remains active.

## Selected primary references

- Finster, Grotz and Schiefeneder, *Causal Fermion Systems: A Quantum Space-Time Emerging from an Action Principle* (2011), https://arxiv.org/abs/1102.2585.
- Finster and Fischer, *The continuum limit analysis of causal fermion systems for curved spacetimes* (published 9 October 2026), https://link.springer.com/article/10.1007/s11005-026-02168-3.
- Finster and Krpoun, *A Geometric Derivation of the Einstein Equations from the Causal Action Principle* (2026 preprint), https://arxiv.org/abs/2607.13871. Smooth manifold support is assumed in its analysis.
- Konopka, Markopoulou and Severini, *Quantum Graphity: A model of emergent locality*, Phys. Rev. D 77, 104029 (2008), https://doi.org/10.1103/PhysRevD.77.104029.
- Markopoulou and Smolin, *Quantum theory from quantum gravity*, Phys. Rev. D 70, 124029 (2004), https://doi.org/10.1103/PhysRevD.70.124029.
- Sorkin, *Quantum mechanics as quantum measure theory* (1994), https://arxiv.org/abs/gr-qc/9401003.
- Boës and Navascués, *Composing decoherence functionals*, Phys. Rev. A 95, 022114 (2017), https://doi.org/10.1103/PhysRevA.95.022114.
- Oreshkov and Cerf, *Operational quantum theory without predefined time*, New J. Phys. 18, 073037 (2016), https://doi.org/10.1088/1367-2630/18/7/073037, with published erratum.
- Filippov, Gudder, Heinosaari and Leppäjärvi, *Operational restrictions in general probabilistic theories*, Found. Phys. 50, 850–876 (2020), https://doi.org/10.1007/s10701-020-00352-6.
