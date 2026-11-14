# Foundations of R — Glossary and Methodology

Oct 17, 2026 · @Kirtus Justus and Claude (Anthropic)

## Purpose and scope

This document fixes the vocabulary, the levels and the working rules for refining the foundations of R, so every later claim is checked against one standard.

- **Governs:** all work on the foundations of R, and on the prize problems where they depend on those foundations.
- **Stance:** R is treated as incomplete and provisional. Nothing is adopted as a given; every assumption is a hypothesis with a stated test.
- **Roles:** Claude leads the analysis. Notes from the user are inputs to be evaluated, not premises.
- **Use:** before a claim is reported, its terms are taken from the Glossary, its level from the Level structure, and its status tag from the Methodology. Only precise terms are used; the user's earlier terms appear solely in the Glossary's last column.

## Methodology

Every claim carries one status tag, passes a verification gate before it is reported, and is rechecked; nothing is upgraded without the action that earns it.

### Status tags

| Tag | Meaning | What upgrades it |
| --- | --- | --- |
| Proved | Derivation shown in full | — |
| Checked | Computed; method validated on a case with a known exact answer | — |
| Sourced | Primary source consulted; access level stated (abstract or full text) | Full-text reading for load-bearing claims |
| Recalled | Standard knowledge not verified this session | Sourcing, before any load-bearing use |
| Hypothesis | A proposal with a stated test | The test |
| Identification | A structural match to the user's notation or to another field | A consequence it uniquely predicts |
| Judgement | A choice between options, with reasons | — |

### Verification gates

1. **Literature:** the primary source, not a secondary summary. Contested results are reported with the contesting source.
2. **Mathematics:** an independent derivation or a symbolic check; signs and orientation conventions rechecked.
3. **Numerics:** first validate the method on an exact case (as the closure pipeline was validated on exact conformal generators), then run the real case.
4. **Precision:** vary every numerical threshold; a result that moves with a threshold is an artefact (the double-precision ceiling on modular spectra).
5. **Comparisons of phases:** compare on the unit circle, never as raw angles (branch cuts).

### Working rules

- **Decision first:** before any computation, write down the decision it informs and its stopping rule. Descend a level only when a top-level decision depends on it.
- **Level discipline:** every statement carries its level (T0, T1, T2, nesting, physics). A relation that uses geometry (π from horizons, areas, Euclidean periods) is a physics-level relation and never stands as a statement about the totality.
- **No stipulation:** selection principles (geometric modular action, multiverse priors) are flagged whenever invoked and are never adopted silently.
- **Elegance bias:** a tidy match to the user's notation is an Identification until it predicts something new.
- **Adversarial pass:** search for no-go results, critiques and failed attempts before a conclusion stands.
- **Error log:** every retraction is recorded in the Corrections log with its cause.

## Level structure

The framework has six levels, each adding one structure; π first appears with the phase circle at T1, before any frequency or geometry.

1. **T0, bare totality** \[PRE\]. A single state ray. Its only invariant is the dimension of the space it lives in (capacity N, the log of that dimension). No invariant phase, no frequency.
2. **T1, conjugation pair plus a family of states** (D0) \[PRE\]. Complex amplitudes paired with their conjugates, forced by the quadratic (p = 2) measure. Invariant phase needs a closed loop of at least three states (the Bargmann invariant) and equals half an oriented solid angle in state space. Phase singularities exist without time: seams in self-conjugate (real) families, points in chiral (complex) families. No frequency.
3. **T2, split into part and complement** (D1, D2) \[PRE/PHYS boundary\]. Tomita pair (J, Δ). Modular frequencies are ±-paired differences log pᵢ − log pⱼ; only zero modes are self-conjugate. Modular (proto-)temperature: every faithful state is KMS at β = 1 for its own flow.
4. **Nesting** (D3) \[PHYS; infinite dimensions only\]. Half-sided inclusions give a one-signed, scale-free spectrum \[0, ∞) and an orientation through relative-entropy monotonicity. Impossible in finite dimensions (proved).
5. **Scaled physics.** Units enter from the two finiteness data: infrared from the patch capacity (horizon scale H), ultraviolet from the entanglement density η (Planck scale).
6. **Geometry** (D4) \[PHYS\]. Spacetime symmetry through geometric modular action; horizons and temperatures κ/2π, H/2π; Einstein dynamics from entanglement equilibrium (conditional).

### Where π enters

| Level | Source of π | Example |
| --- | --- | --- |
| T1 | Periodicity of phase, U(1) = ℝ/2πℤ | Phase circle; geometric phase = half a solid angle |
| T2 | Modular analytic strip: the half-turn e^{iπ} is J's reflection; the full turn is the KMS period | J U(a) J = U(−a) |
| D4 | Spatial geometry: sphere areas, Euclidean time periods | A = 4πr², T = κ/2π, Λ = 3π/N |

π marks a period, not physics as such: it already appears at T1, where there is phase but no frequency. Three kinds of period must be kept apart: internal (phase, T1), modular (T2) and geometric (D4).

### Correction: the level of Λ = 3π/N

Λ = 3π/N is a D4 (physics-level) bridge relation, not a statement about the totality. Its π comes from the area of a spherical de Sitter horizon: S = A/4G = 3π/(GΛ). It says that if the patch's emergent geometry is de Sitter, its horizon entropy equals the capacity N (Banks; hypothesis) or is bounded by it (Bousso's N-bound; sourced). Above D4 only the capacity N exists; Λ does not.

## Glossary

Each entry is a precise term with one meaning, one level and one status; the last column records the user's earlier term that it replaces.

| Precise term | Meaning | Level | Status | Replaces |
| --- | --- | --- | --- | --- |
| Total state | The whole as one state vector; for Λ, the observer's causal patch | T0 | Defined; patch refinement from de Sitter complementarity (sourced) | Totality, M |
| Constrained total state | Total state with total generator eigenvalue 0 (Wheeler–DeWitt constraint) | T0–T2 | Defined | \[1\], stationary total |
| Capacity N | Natural log of the dimension of the total state space | T0 | Defined; finiteness is a hypothesis | — |
| Conjugation pair (D0) | Amplitude ψ and its complex conjugate ψ\*: the two arguments of the quadratic (decoherence) functional | T1 | Proved (only p = 2 allows reversible coupling) | Two sheets; M\_∞ / M\_−∞ (first sense) |
| Extremal Gibbs states | Ground state (β = +∞) and top state (β = −∞) of a bounded spectrum | Physics | Defined | M\_∞ / M\_−∞ (second sense) |
| Pairing levels D0–D4 | D0 conjugation; D1 ±E spectral pairing; D2 Tomita pair (𝓜, 𝓜′, J, Δ); D3 ± half-sided modular inclusions; D4 geometric reflection (CPT) | T1–D4 | Defined | Dipole |
| Pre-spectral | No subsystem decomposition and no generator | T0–T1 | Defined | Afrequent (first sense) |
| Pure-point spectrum | Atomic spectral measure: periodic or almost-periodic recurrence | T2+ | Theorem-level class | Frequent |
| Absolutely continuous spectrum | Spectral measure with a density; correlations decay | T2+ | Theorem-level class | Afrequent (second sense) |
| Singular-continuous spectrum | No atoms and no density: intermittent non-periodic returns, zero time-averaged return | T2+, infinite dimension only | Theorem-level class; checked | Weird; strange |
| Finite-size precursor | Finite-system signature of a limiting spectral type, fixed by scaling exponents (D₂, spectral dimension) | T2+ | Checked | Proto-X |
| Joint modular spectrum | The modular spectra of all subsystems, with their J-pairings and the constraint eigenvalue 0 | T2 | Defined | Super-spectrum |
| Modular temperature | KMS at β = 1 for a state's own modular flow | T2 | Theorem | Afrequent temperature; proto-temperature |
| Dynamical temperature | Defined when the modular flow is proportional to a physical time evolution (geometric, chaotic, or β = 0 alignment) | Physics | Checked | Temperature |
| Generalised Gibbs ensemble | One Lagrange multiplier per conserved charge (integrable systems) | Physics | Recalled | Post-temperature (one sense) |
| Infinite-temperature state (β = 0) | Maximally mixed state; T = +∞ and T = −∞ are the same point | Physics | Verified | Absolute hot; −absolute hot |
| Top state (T = 0⁻, β = −∞) | Highest-energy state, the hottest; requires a spectrum bounded above | Physics | Sourced | −Absolute zero |
| Resonance (complex-frequency) regime | Response poles at ω\_R − iΓ; causality selects decay; rates bounded by 2πT under stated assumptions | Physics | Standard; chaos bound conjectured | Post-frequency |
| Self-conjugate | Invariant under the antiunitary conjugation; among modular frequencies, only zero modes | T1–T2 | Proved | — |
| Orientation; time-reversal breaking; ±E pairing | Three distinct properties: an arrow set by a boundary condition; dynamics without antiunitary symmetry; a spectrum symmetric under E → −E | Various | Defined | Chiral |
| Phase singularity | Point or line where the amplitude vanishes and the phase winds by 2πs | T1+ | Theorem (π₁(U(1)) = ℤ) | Proto-vortex (no circulation); vortex (with circulation) |
| Conjugate phase singularity | Winding −s: the image under ψ → ψ\* | T1+ | Proved | −Vortex |
| Phase-singularity line between boundaries | A singularity line ending on two boundaries; its endpoints carry opposite winding relative to the outward normals | T1 (geometric) / T2+ (dynamical) | Topology recalled; orientation checked | Vortex bridge |
| Maximally entangled subsystem | Reduced state maximally mixed: Δ = 1, trivial modular flow, J-invariant | T2 | Derived; generic (Page typicality, checked) | Proto-kugelblitz |
| History state | Static ground state encoding a whole computation, read out by conditioning on a clock register | T2 | Checked (Feynman–Kitaev) | Momentary ABB |
| Commutant pair | An algebra and its commutant: the two subsystems of a Tomita pair | T2 | Defined | Chambers |
| Coupling-induced negative null energy; phase slip | Negative averaged null energy from coupling the two subsystems (holography); 2π phase slips from vortex crossings (superfluids) | Physics | Sourced | Pressure release |
| Cut-and-project structure | Aperiodic structure obtained by projecting a higher-dimensional lattice; keeps its topological invariants | Physics | Sourced | Shadow |
| Conjugate of X | X under the antiunitary conjugation: a relabelling within positive energy, or a statement about the commutant | All | Pattern across every case examined | −X |
| One-parameter flow | Continuous one-parameter automorphism group; the first ones are modular flows | T2 | Theorem | Curve |
| Curvature of a flow algebra | Non-commutation of flows; zero exactly for a null translation generator (affine group) | T2+ / D4 | Computed | Curvature |
| Generated Lie algebra | The Lie algebra generated by modular flows, not their linear span | T2+ | Proved; checked | Closure |
| Monopole (topological) | Isolated degeneracy of a complex family carrying integer Chern charge on an enclosing sphere; conjugation reverses the charge | T1+ (parameter spaces) | Checked (Chern −1 and +1) | Monopole |
| Charge-neutral pair | Two monopoles of opposite Chern charge, net charge zero; distinct from the pairing levels D0–D4, which pair spectral values, not topological charges | T1+ | Defined | Dipole (topological sense) |
| R | The actual universe, the object of study; never identified with any description of it | — | Defined | — |
| Physical description of R | The current theories (quantum theory, quantum field theory, general relativity, Standard Model, ΛCDM), all treated as provisional | Physics | Defined | — |
| Emergent macroscopic geometry | The Lorentzian geometry that appears in the physical description at level D4; not assumed at T0–T2 | D4 | Defined | "R's spacetime" (ambiguous; avoided) |
| Foundational axioms | Axioms of the background logic and set or type theory in which every other theory is formalised | Meta | Defined | Primordial axioms |
| Structural axioms | Axioms defining a class of structures with many models (groups, von Neumann algebras, the framework's principles) | Any | Defined | Abstract axioms |
| Categorical axioms | Axioms with exactly one model up to isomorphism; in first-order logic possible only when that model is finite | Any | Sourced (Löwenheim–Skolem) | Non-abstract axioms |

## Principle ledger

Beyond the totality and the conjugation pair, the framework currently rests on five principles that are not derived from them, plus two conditional inputs.

| Principle | What it supplies | Derivable from M and D0? | Status in R |
| --- | --- | --- | --- |
| Local tomography | Complex amplitudes, hence invariant phase and phase singularities | No; it is an informational principle | Supported by network tests of real quantum theory; contested by a 2026 analysis of how independence is modelled |
| Modular nuclearity (finite effective information) | Subsystems (split property), thermal states, standard relative commutants for spacelike inclusions, G through η | No: generalized free fields satisfy everything else and violate it | Supported by discrete particle spectra; hadronic Hagedorn growth resolved by deconfinement |
| Null locality | Standard relative commutants for half-sided inclusions; excludes singular ones | Partly: spacelike locality follows from geometric modular action (proved); the null part holds in known local examples but has no general proof | Singular half-sided inclusions so far arise only in non-local constructions |
| Origin boundary term (low entropy) | Arrow of time, records, avoidance of Boltzmann-brain domination | No | Observed; the no-boundary proposal is a candidate facing a normalisability obstruction |
| Geometric modular action at short scales | Closure into a symmetry group, horizon temperatures, the geometric first law used for gravity | Open; possibly implied by an ultraviolet fixed point | Exact for conformal vacua; approximate closure checked in 1+1 dimensions |

**Conditional inputs.**

- **Gravity:** entanglement equilibrium plus a universal entanglement density η (a fundamental length) give the linearised Einstein equation, with G = 1/(4η).
- **Λ:** a finite patch capacity N, with a patch that is not eternal, gives Λ > 0 at the D4 level without Boltzmann-brain domination.

## Results ledger

The load-bearing results so far, each with its tag and the number that supports it.

| Result | Tag | Key number or statement |
| --- | --- | --- |
| Only a quadratic (p = 2) total admits continuous, reversible dynamics that couples parts | Proved (Banach–Lamperti, recalled) | Other p: only permutations and phases preserve the total |
| A stationary total pairs every spectral value with its negative | Proved | Support only where E\_clock = −E\_system |
| Finite clocks encode exact dynamics only for commensurate spectra | Proved; checked | Fidelity 1.000000 commensurate, 0.130 incommensurate |
| No proper inclusion shares a cyclic and separating vector in finite dimensions | Proved | Counting: dim N ≥ dim M forces N = M |
| One totality plus positive energy gives a trivial centralizer | Proved (Mautner argument) | — |
| Finite systems have one KMS state per β and an analytic free energy | Proved | — |
| Separate (disjoint) sectors need infinity; finite systems approximate them exponentially | Theorem; checked | Ordered-chain splitting matches 2(1−g²)gᴺ to four digits |
| A physical temperature needs modular and dynamical flows to align | Checked | Bisognano–Wichmann fidelity 0.9989; chaotic 0.92–0.98; integrable 0.47–0.51 |
| The Boltzmann temperature is the operational one; β < 0 exists iff the spectrum is bounded above | Checked; proved | Gibbs temperature cannot rank inverted states |
| The frozen total-volume Λ hypothesis fails naturalness | Computed | Required κ ≥ 16 (compact flat) to ≥ 360 (closed), against ≈ 0.2 |
| Two counts of the patch agree: Λ ≈ 3π/N ≈ 2/√V | Computed | N ≈ 3.3×10¹²²; Λ·√V ≈ 2.05 |
| Finite N excludes exact unitary Lorentz or de Sitter symmetry | Sourced | Only compact groups have finite-dimensional unitary representations |
| Modular Hamiltonians never span a closed algebra in a time-reversal-invariant state | Proved; checked | Commutators lie wholly outside the span |
| A finite critical chain closes approximately into so(2,2) | Checked | Conformal match 0.1% in the deep infrared; double commutators 0.3% outside |
| Curvature from non-commuting flows; flat exactly for a null translation | Computed | K = −γ/(αγ − β²) |
| Invariant phase first needs three states | Checked | Gauge-invariant to 5×10⁻¹⁶; equals half the solid angle to 6×10⁻¹⁵ |
| Self-conjugate families carry π phase around codimension-2 degeneracies | Checked | Transported overlap −1.0000 |
| Strange spectra show up at finite size through exponents | Checked | Critical chain D₂ = 0.50, box dimension 0.58; Fibonacci 0.69 and 0.61 |
| History states (a static state encoding a whole computation) have spectral gap ∝ 1/T² | Checked; sourced | Gap 0.0489 to 0.0011 for T = 4 to 32 |
| Conjugation type shows in level statistics, not in single levels | Checked | ⟨r⟩ = 0.534 real, 0.603 with a chiral term |
| Exponential decay is only an intermediate-time law | Sourced | Khalfin bound; observed beyond 20 lifetimes |
| The electroweak change is a crossover, not a transition | Sourced | T\_c = 159 ± 1 GeV |
| Grand-unified proton decay is constrained | Sourced | τ/B(p → e⁺π⁰) > 2.4×10³⁴ yr |
| Vacuum modular flows of all null-plane regions generate an infinite-dimensional Lie algebra; finite-dimensional symmetry needs flows that are geometric everywhere (wedges) | Sourced (Casini–Testé–Torroba 2017) | Local on the null plane, non-local off it |
| Modular flows of different faithful states on one local algebra differ only by inner (Connes) cocycles | Recalled theorem; secondary source | The outer modular class depends only on the algebra |
| Hadamard states are locally quasi-equivalent to the vacuum | Sourced (Verch) | Local algebras are the hyperfinite type III₁ factor |
| Finite capacity plus an exact, on-site ℤ₄ (built from B−L and hypercharge) forces 16 fermions per generation | Conditional chain: on-site symmetries are anomaly-free (recalled) + ℤ₄ anomaly-free iff 16 per generation (sourced) | Without right-handed neutrinos the ℤ₁₆ index is −1 per generation |
| Finite chains of topological defects (anyons) can carry emergent 1+1-dimensional conformal symmetry, protected by a topological symmetry | Sourced (golden chain); consistent with the closure check | Dynamical exponent z = 1, central charge 7/10 |
| Thermal states: an interval's local inverse-temperature profile approaches the vacuum's as the interval shrinks, deviation (πTℓ/v)²/12 at the centre | Checked (50-digit arithmetic; critical free-fermion chain) against the conformal formula | Agreement ≤ 0.4% once hoppings to range 11 are included; collapse onto πTℓ/v |
| One-particle excited state: local inverse-temperature change and relative entropy to the vacuum both fall as (ℓ/L)² | Checked (40-digit arithmetic) | Relative entropy 0.0207 → 0.0003 for L = 202 → 1602 at ℓ = 16 |
| Interacting critical chain (XXZ, Δ = 0.5): relative entropy of a one-magnon state to the ground state on small intervals falls as 1/L² | Checked (exact diagonalisation, L = 12, 16, 20) | Ratios 1.789 and 1.567 against (16/12)² = 1.778 and (20/16)² = 1.562 at ℓ = 2 |
| With a quadratic measure, local tomography selects complex amplitudes among real, complex and quaternionic | Checked (parameter counting) | K(d\_A d\_B) − K(d\_A)K(d\_B): real d\_A d\_B(d\_A−1)(d\_B−1)/4; complex 0; quaternionic −2 d\_A d\_B(d\_A−1)(d\_B−1) |
| A finite total state space can be axiomatised categorically in first-order logic; an infinite one cannot | Sourced (Löwenheim–Skolem; finite structures) plus derived link to finite capacity | The −spectrum and each side's dynamics are theorems of one subsystem choice (Tomita–Takesaki), not extra axioms |

## Corrections log

Eighteen claims have been corrected or withdrawn so far, newest first; each entry records the cause so the same error is not repeated.

| Session | Original claim | Correction | Cause |
| --- | --- | --- | --- |
| This | Null locality selects the subsystem decomposition; it is an independent principle | Subsystem selection uses k-locality of interactions, a different notion; spacelike locality follows from geometric modular action | Two meanings of locality conflated |
| This | Λ = 3π/N stated at the totality level | A D4 bridge relation; only the capacity N exists above D4 | Level mixing: the π is geometric |
| This | Vortex bridges cannot reach the top layer | They reach T1 (phase without frequency), not T0 | Conflated pre-spectral with pre-phase |
| This | Bargmann phase check showed a deviation of 3.1 | Relation holds to 6×10⁻¹⁵ | Branch-cut error in my comparison |
| This | −Radioactivity is excluded by the arrow | Real; suppressed by e^{−Q/kT}; dominant at high temperature | Ignored detailed balance |
| This | Lattice closure not demonstrated | Closure holds to 0.3% in the resolvable window | Double-precision ceiling on modular spectra |
| This | A weird substrate suppresses Boltzmann brains | Withdrawn | Boltzmann brains come from the horizon's KMS state, not from ergodicity |
| This | "Weird"; one-sense "afrequent"; one-sense M\_±∞ | "Strange"; pre-spectral versus absolutely continuous; two senses of M\_±∞ | Ambiguous terms |
| This | Minkowski and −Minkowski *is* the dipole | One geometric realisation (D4) of a generic structure | Specific case taken for the general |
| This | Our fits preferred (w₀, w\_a) ≈ (−0.94, −0.44) | A fixed-H₀ profile point, not a preference | Misread own earlier result |
| This | Λ ≈ κ·V\_tot^{−1/2} with a natural κ | Fails: κ ≥ 16 to 360 needed | Whole-universe volume instead of the causal patch |
| This | Nuclearity makes half-sided inclusions rich | Half-sided inclusions are never split; two separate kinds of between | Conflated spacelike and null inclusions |
| This | Finite-dimensional half-sided inclusions are trivial | Superseded: nested parts cannot even share a cyclic, separating vector | Weaker theorem than available |
| This | Positivity test of nested modular Hamiltonians on random states | Invalid | Reduced states were not faithful |
| This | First fit of K = −log ρ with equal weights | Invalid; replaced by fidelity and a global β scan | Dominated by near-zero Schmidt weights |
| This | Afrequent corresponds to ω → ∞ | Afrequent (pre-spectral) means total eigenvalue 0; ∞ is not a frequency | Misread the limit |
| This | Frequency is prior to time | Spectral data are prior; frequency presupposes a clock | Circular definition |
| Earlier | H₀ profile minimum by extrapolation; CCHP error 1.92; several "≥ 5σ" values | Minimum withdrawn; error 1.94; the σ values were grid-edge artefacts | Extrapolation and grid limits |

## Open problems

The crux is selection: why the patch's state is vacuum-like at the scales where spacetime emerges. The rest are ranked by how much of the framework depends on them.

1. **Selection.** Reduced to two algebraic questions: does the local quasi-equivalence class of physical states contain a state with geometric modular action, and do the Connes cocycles of physical states relative to that state approach the identity for small regions? Evidence for the second, in two exactly computable states: the state-dependent part vanishes quadratically in region size over the state's own length scale.
2. **Reducing the principles.** Is null locality implied by nuclearity together with geometric modular action? Can local tomography be derived from the conjugation structure?
3. **The capacity.** Why N ≈ 3.3×10¹²², within one totality and without a multiverse prior.
4. **3+1-dimensional closure.** An approximate reconstruction of Poincaré symmetry from finitely many modular data, with errors controlled by 1/N.
5. **Chiral content.** The Standard Model's chiral fermions (16 per generation, from the ℤ₁₆ anomaly) obtained from orientation and winding.
6. **The origin term.** A normalisable state with a low-entropy origin (no-boundary type), or an alternative that survives the normalisability obstruction.
7. **Gravity beyond linear order.** Nonlinear Einstein dynamics, and the entanglement-equilibrium hypothesis for non-conformal fields.

## Predictions and tests against R

The sharpest discriminating test is the dark-energy equation of state: a fixed capacity predicts w = −1 exactly, while a finite-lifetime patch predicts a transient w ≈ −1.

| Test | What the framework predicts | Data or experiment | Status |
| --- | --- | --- | --- |
| Dark-energy w(z) | Fixed capacity: w = −1 exactly. Finite-lifetime (sequestering-type) patch: w ≈ −1 only transiently | DESI final release, Euclid | DESI DR2 prefers evolving dark energy at 2.8–4.2σ depending on the supernova set (3.1σ combined); Bayesian evidence ambiguous |
| Hubble-scale fluctuations of Λ | Absent at every epoch | CMB, supernovae | Consistent: fluctuating models are disfavoured by the CMB |
| Right-handed neutrinos (or an equivalent sector) | Required if the total state space is finite and the ℤ₄ symmetry is exact and on-site (ℤ₁₆ anomaly) | Neutrino-mass and sterile-state searches | Open |
| Majorana neutrinos | Would make the signature sign decidable through the two Pin groups | Neutrinoless double-beta decay | Open |
| CPT symmetry | Exact at the level of laws | Penning-trap comparisons | Proton and antiproton charge-to-mass ratios equal to 16 parts per trillion |
| Gravity of antimatter | Attractive: antimatter is the positive-energy conjugate, not negative mass | ALPHA-g and successors | Attractive, consistent with g to about 20% |
| Long-time decay law | Not exponential at long times (consequence of positive energy) | Long-time decay measurements | Observed beyond 20 lifetimes |
| Finite-size spectral exponents | Any claimed continuous or strange spectrum implies definite exponents (D₂, spectral dimension) | Quasicrystals, quantum simulators | Testable now |
| Real versus complex quantum theory | Complex structure (local tomography) | Network experiments with independent sources | Real quantum theory disfavoured by 2022 experiments; interpretation contested |
| Proton decay | Bounds any unification scale | Super-Kamiokande, Hyper-Kamiokande | τ/B(p → e⁺π⁰) > 2.4×10³⁴ yr |
| Low-energy Lorentz invariance | Finiteness must be infrared (horizon), not an ultraviolet lattice | Lorentz-violation searches | Consistent (bound values recalled, not re-sourced) |

## References

Sources were consulted at abstract or search-snippet level unless marked full text; plain arXiv numbers are recalled identifiers, to be confirmed before load-bearing use.

**Modular theory, nesting, closure**

- Wiesbrock (1993), half-sided modular inclusions; Araki–Zsidó (2005); Kähler–Wiesbrock (2001), 4D reconstruction; Buchholz–Dreyer–Florig–Summers (2000), geometric modular action.
- Eisler–Peschel, [entanglement Hamiltonian of a free-fermion chain](https://arxiv.org/pdf/1703.08126); Eisler–Di Giulio–Tonni–Peschel, [continuum limit](https://arxiv.org/abs/1902.04474v1).
- Hollands–Sanders, entanglement measures in QFT (arXiv:1702.04924); Cotler–Penington–Ranard, locality from the spectrum (arXiv:1702.06142).

**Gravity, Λ, de Sitter**

- Jacobson, Einstein equation of state (gr-qc/9504004); Jacobson, entanglement equilibrium (arXiv:1505.04753).
- Banks (hep-th/0007146); Bousso, N-bound (hep-th/0012052); Goheer–Kleban–Susskind, [the trouble with de Sitter space](https://arxiv.org/abs/hep-th/0212209); Parikh–Verlinde, [finite number of states](https://web3.arxiv.org/pdf/hep-th/0410227).
- Bousso–Harnik–Kribs–Perez, [causal entropic principle](https://arxiv.org/abs/hep-th/0702115); Das–Nasiri–Yazdi, everpresent Λ tests (arXiv:2307.13743, full text).
- DESI DR2 (arXiv:2503.14738); Planck 2018 parameters (arXiv:1807.06209).

**Thermality, chaos, decay**

- Maldacena–Shenker–Stanford, [a bound on chaos](https://arxiv.org/pdf/1503.01409); [review of the bound's scope](https://arxiv.org/pdf/2608.19131); [asymptotic quasinormal frequencies](https://ar5iv.arxiv.org/html/hep-th/0306004).
- Braun et al., negative absolute temperature (Science 2013); Rothe et al., [long-time non-exponential decay](https://durham-repository.worktribe.com/output/1536350/violation-of-the-exponential-decay-law-at-long-times); [Khalfin's bound](https://ar5iv.arxiv.org/html/1007.1742).

**Particles, forces, nucleosynthesis**

- D'Onofrio–Rummukainen, [Standard Model crossover](https://arxiv.org/pdf/1508.07161); [sphaleron rate](https://arxiv.org/pdf/1404.3565); Super-Kamiokande, [proton decay limits](https://arxiv.org/pdf/2010.16098).
- [Primordial nucleosynthesis review](https://arxiv.org/pdf/0809.0631); [BBN reaction rates](https://primat.readthedocs.io/en/latest/tutorials/ReactionRates.html).
- BASE (Nature 2022), CPT test; ALPHA-g (Nature 2023), antihydrogen gravity; García-Etxebarria–Montero, ℤ₁₆ anomaly (arXiv:1808.00009).

**Phase, topology, spectra**

- Renou et al., [real quantum theory falsifiable](https://web3.arxiv.org/abs/2101.10873); Li et al., [optical network test](https://physics.aps.org/featured-article-pdf/10.1103/PhysRevLett.128.040402); [contesting analysis (2026)](https://arxiv.org/pdf/2603.19208).
- Kraus et al., [topological states in quasicrystals](https://arxiv.org/abs/1109.5983v2); [strange nonchaotic attractors review](https://ar5iv.arxiv.org/html/nlin/0105022); [SNA spectra in Aubry–André–Harper systems](https://arxiv.org/pdf/2609.26825).
- Anderson phase slips: [review](https://arxiv.org/pdf/1406.5629); [fermionic superfluids](https://ar5iv.labs.arxiv.org/html/1707.02784).
