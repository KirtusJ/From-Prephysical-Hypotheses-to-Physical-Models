# Provisional construction specification | Compositional Event Algebra with Conditional Records

**Research direction:** Kirtus Justus. **Constructing reviewer:** LLM Director A.  
**Date convention:** 11 November 2026, B.C. Pacific Time.  
**Parent Unary PCP:** Initial External Grounding OPEN. **Status:** Stipulated candidate for adversarial development, not an established or chosen physical ontology.

## Target and non-target

**Target:** identify a defensible, explicitly stipulated mathematical route from a clock-free relational description to (i) operational quantum mechanics, including noncommutativity, composite systems and valid Born-type probabilities, and (ii) genuinely dynamical classical mechanics via records and a controlled semiclassical/continuum limit.

**Non-targets at this stage:** asserting that an algebra is a physical carrier; treating a prior Wilson–Dirac calculation as a derivation of these primitives; importing frequency/time/space in the raw stage; equating a stochastic Markov chain with Newtonian mechanics; describing an arbitrary chosen state as an experimentally prepared state.

## First commitment: an austere relational substrate

Stipulate a **finite groupoid** `G` of abstract objects and composable reversible arrows. Only object and arrow identity, source/target, associative partial composition, identities and inverses are assigned. There is *no* fundamental physical time, physical frequency, wavelength, background position, metric, energy, canonical momentum or Born probability. Composition is an abstract composability relation, not a time coordinate. The assumption of reversibility is itself a vulnerable candidate choice, not an inferred law.

**Negative control:** The same two abstract objects admit the identity-only groupoid and the full two-object pair groupoid. They have different convolution algebras, so object data alone cannot select the quantum candidate. This is an explicit underdetermination obstruction.

## Second commitment: complex composition algebra, fully disclosed import

Stipulate complex coefficients, an involution and the finite groupoid convolution algebra `A = C[G]`. For the pair groupoid on two objects, arrows `g_ij` obey `g_ij*g_kl=δ_{jk}g_il` and `(g_ij)^*=g_ji`. Sending `g_ij↦E_ij` gives an exact *-algebra isomorphism `C[G]≅M_2(C)`.

This proves a **representation result**. It does **not** derive complex amplitudes, relative phases or physical quantumness from composition alone. Any later word “emergence” must disclose this import.

## Third commitment: positivity and a state-to-observation bridge

Stipulate a normalized positive functional `ω(a^*a)≥0`, `ω(1)=1`. Standard GNS then yields a Hilbert space representation. When `A=M_2(C)`, write `ω(a)=tr(ρa)` for a density matrix `ρ`. For an admitted effect `0≤E≤1`, define `p(E)=ω(E)`; for an admitted instrument `{I_k}`, define its outcome probabilities through positive operators / CP maps.

**Logical status:** `p(E)=ω(E)` is Born-type statistics by **definition of the observation contract**, not a deduction that an actual physical detector realizes it. GNS is standard mathematics after positivity is supplied, and says nothing about how nature chooses `ω`, its tensor structure, effects or outcomes.

## Fourth commitment: composite noncommutativity as a positive control

For two stipulated qubit sectors take `A_AB=M_2(C)⊗M_2(C)`; the tensor composition is an *additional assumption*. Choose the normalized Bell state `|Φ+>=(|00>+|11>)/√2`. Set `A_0=Z`, `A_1=X`, `B_0=(Z+X)/√2`, `B_1=(Z-X)/√2`. Then

`<A_0 B_0+A_0 B_1+A_1 B_0-A_1 B_1>=2√2`.

An ordinary commutative locally jointly assigned model obeys `|CHSH|≤2` under its own locality/joint-assignment premises. The positive control demonstrates that this stipulated algebra *can represent* standard quantum correlations. It does not establish empirical implementations, no-signalling conditions, or uniqueness of the algebra. Noncommutativity is already imported by the chosen groupoid algebra.

## Fifth commitment: conditional records and a strictly limited classical sector

Choose projections `{P_j}` summing to the identity and define the dephasing/pinching channel `D(ρ)=Σ_j P_j ρ P_j`. For `0≤γ≤1`, the stipulated partial dephaser `D_γ=(1-γ)id+γ D` has, after `k` iterations, off-diagonal entries multiplied by `(1-γ)^k` in the selected basis. The diagonal probabilities form a commutative classical algebra, *conditional on that preferred record basis*.

If each step applies a unitary `U` and then pinches, diagonal inputs update under the column-stochastic matrix `T_{ji}=|U_{ji}|²`; for square unitary matrices it is doubly stochastic. This produces a classical stochastic chain on record labels. **Iteration count k is not automatically physical time.**

The pinching map is a stipulated open-system/operational channel and by itself does not explain individual measurement outcomes. The apparatus, environmental selection of a pointer basis, record definiteness and decoherence scales remain physical bridge obligations.

## Sixth commitment (UNRESOLVED): continuous mechanics and time

To meet the *total* ontological target, it is not enough to extract a stochastic chain. One must construct families indexed by a dimensionless resolution parameter `ε→0`, with quantum algebras `A_ε`, controlled observables `Q_ε(f)`, admissible states and specified dynamics. Conditional classical Hamiltonian emergence should establish, on a stated function class and time interval, a bracket limit of the form

`(1/(i ħ_ε))[Q_ε(f),Q_ε(g)] - Q_ε({f,g}) → 0`,

plus an Egorov-type comparison between evolved quantum observables and a classical Hamiltonian flow, with explicit norm/topology and remainder. Here `ħ_ε` is an **introduced comparison/scaling quantity** requiring physical calibration; it is not “infinite frequency” or a prephysical wavelength. The symplectic manifold, its dimension, mass/energy units, and physical time must be *constructed or justified separately*, not borrowed by a change of notation. A classical Hamiltonian special case leading to Newton's equations requires a separately warranted `H=p²/(2m)+V(x)`.

### Exact finite-dimensional obstruction

If `Q,P` are finite matrices, `tr([Q,P])=0`. Thus `[Q,P]=iħ I` with nonzero `ħ` is impossible: `0=iħ dim(H)`. No isolated finite graph/groupoid algebra can **exactly** realize the unbounded continuous canonical commutation relations. A scaling family or a different algebraic target is mandatory.

## Principal preference-bias and adversarial controls

| Rival or obstruction | What must be shown to distinguish the candidate |
| --- | --- |
| Commutative finite algebra with same objects | A genuine operational noncommutative witness under justified preparation and measurement assumptions |
| Real, quaternionic or generalized probabilistic models | Why a complex C*-algebra and tensor product are selected rather than simply convenient |
| Classical stochastic records | A result strictly stronger than classical Markov behaviour, not a tautological restatement of measurement probabilities |
| Finite-dimensional CCR trace obstruction | Explicit scaling construction and controlled error theorem |
| Environment-induced decoherence without definite outcomes | A separate account of record actualization or a carefully limited operational target |
| Physical time absent in the raw structure | Independently testable clock-bridge law; no conflation with arrow composition or update count |
| Device/source aliases from prior B/C work | An observational contract that resolves or bounds independent preparation, inversion dependence, drift and calibration |
| Alternative foundations (informational reconstructions, histories, C*-algebraic models) | A genuinely distinguishing theorem or new empirical prediction; rephrasing established formalism is insufficient |

## Status of separate bridge obligations

| Proposed step | Status at this checkpoint |
| --- | --- |
| Raw groupoid and composition law | Stipulated, not physical |
| Complex convolution algebra | Stipulated scalar field; finite isomorphism proved |
| Positivity/state functional | Stipulated; GNS follows conditionally |
| Composite tensor product and CHSH | Stipulated; positive finite control reproduced |
| Quantum instruments/Born readout | Stipulated operational law; source/measurement implementation open |
| Preferred records and CP dephasing | Stipulated; formal diagonal limit checked |
| Classical Markov statistics | Proven within specified channel and basis |
| Continuous classical Hamiltonian mechanics | Not constructed; scaling/geometry/time debts outstanding |
| Physical emergence/ontological uniqueness | Not established |
| Relativistic fields, gravity and quantum continuum | Outside current successful construction; separate outstanding target if “total” includes them |

## First methodical sequence of admissible checks

1. Seek **counterexamples** to the uniqueness of each stipulated algebraic ingredient, especially complex coefficients and the tensor product. Keep the commutative rival visible.
2. Determine whether weaker explicit operational assumptions can reconstruct the noncommutative event algebra without presupposing Born measurements, comparing rigorously with established GPT reconstruction results.
3. Construct a controlled finite-to-continuum family that escapes the canonical-commutator trace obstruction, without smuggling in a physical clock or phase-space geometry.
4. Distinguish record statistics, stochastic dynamics and Hamiltonian dynamics by separate theorems and adversarial cases.
5. Require independent warrants for actual preparation, observable readout and uncertainty before making any physical statement.

**Stop/withdrawal rule:** If the algebra and Born law can be obtained only by reintroducing their full quantum content as primitives, the right disposition is *quantum-compatible algebraic representation*, **not emergence of quantum mechanics**. If the continuum family does not yield symplectic/Hamiltonian flow, do not describe the diagonal stochastic sector as “emergent classical mechanics.”

**PCP stage:** Initial External Grounding remains OPEN. This construction track may be examined, corrected, weakened or discarded without implicit approval to move to another stage.
