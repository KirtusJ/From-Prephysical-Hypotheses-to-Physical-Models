# Provisional Steelman: Zero-Dimensional Signed Action and Compositional Consistency

**Status:** EXPLICITLY STIPULATED ONTOLOGICAL CONSTRUCTION FOR FALSIFICATION. Phase II: second external grounding, reconciliation, and construction. This is **not** an established physical theory, a final pipeline steelman, a derivation of quantum mechanics, or a claim about physical events outside time.

**Date:** 8 November 2026 (America/Vancouver).  
**Research direction and responsibility:** Kirtus Justus.  
**Independent analytical, computational and editorial assistance:** ChatGPT (OpenAI).

## 1. Summary of the strongest defensible thesis

The substantive ontological possibility is *not* that a graph, a spatial oscillator or an Ising lattice was present before spacetime. It is that an internally distinguishable algebraic structure could have signed magnitude and nontrivial global action relationships with **no physical spatial coordinate, preassigned clock, local causal arrow or physical frequency**, and that a physical interpretation of time/geometry could be licensed only after additional independently defensible correspondences are established.

A nonzero action functional does not by itself imply chronological dynamics, and lack of a chronological dynamics does not justify calling the structure temporally static. Neither proposition establishes actual pretemporal physical activity. The original positive/negative spectra and proposed continuum remain conjectural, not mathematics already derived.

The **falsifiable constructive core** below is deliberately narrow: a sign-symmetric zero-spatial-dimensional action, one mathematically unambiguous extension rule for any finite number of internal instances, and a specified *optional* noncommutative operational representation. The construction survives the original four-slot quadratic action's failed five-to-four marginal closure because it does **not** preserve or silently retune that old action. It loses some stronger claims that the older construction attempted to make.

## 2. Retired claims and material source audits

The two contemporary six-item research handoffs agree in their important scopes:

1. The old four-slot anti-balanced law has count masses `(1/162, 16/81, 16/27, 16/81, 1/162)`, pair correlation `-5/27`, unique exchangeable five/six-slot extensions and no seven-slot extension. Its sharp total-variation gaps to seven and infinite exchangeability are respectively `74/945` and `47/216`.
2. Exact five/six-slot extensions require certain **zero** probability classes. No everywhere-finite Gibbs action can assign those exact extensions by positive Boltzmann weights. This is stronger than the pure quadratic-action closure failure.
3. Under the size-dependent quadratic law `P_N∝exp[-b M_N²/(2N)]`, deleting one slot from five yields `w_4(M)=2exp[-b(M²+1)/10]cosh(b M/5)`. Its four-count ratios fail a quadratic-family identity for every `b>0`, with relative defect `tanh⁴(2b/5)`, small-b leading order `16 b⁴/625`.
4. The old sign-comparison graph `i~j ⇔ σ_i≠σ_j` is either empty or complete bipartite, with diameter at most two when connected. Its normalized Laplacian spectrum is `{0,1^(N−2),2}`, independent of the bipartition sizes. A dimension diagnostic `d_spec(s)→2s` for large N at fixed s has **no stable dimensional plateau** and does not derive locality.
5. A full trace-one quantum *comparison representation* can be defined, but does not mean Hilbert-space preparation, the Born rule, local quantum instruments, or causal evolution have been independently derived. The signed graph state ansatz also failed closure under conventional vertex elimination.
6. The historical 5D Volume Inflection Model is a separate conditional Einstein-stress solution with assumed proper time and geometry, not part of the fundamental zero-dimensional ontology. Previous tests of particular string reductions are not universal string-theory no-go theorems.

The supplied verification sources were inspected in the research context. The original uploaded executables were not accessible through their named paths in the current code environment, so this note does **not** claim verbatim execution. A separate explicitly exception-checked program was built and run in ordinary Python, `-O`, and `-OO`.

## 3. Stipulations: root and operational comparison tiers

### Tier 0: the zero-spatial-dimensional root

**Z0, signed magnitude.** There is an abstract internal real signed variable `T∈[-1,1]`. It is not a point in physical space, a time reading, a physical electromagnetic charge, or a frequency. Introduce a nonzero amplitude scale `m`; the effective signed readout may later be `Q=m Z`, but `m` is not measured or calibrated at this root level.

**Z1, action without chronological boundaries.** Stipulate a real functional, with `0<r<1, λ>0`,

`S_0(T)=λ(T²−r²)²`.

It has two zero-action minima `T=+r` and `T=−r`. This is a mathematical variational condition on a *whole configuration*, not a statement that a variable physically moved between two moments. No spacetime coordinate or physical periodicity occurs. Other choices of `S_0` would be distinct ontologies.

**Z2, explicit symmetric selection law.** Choose `ν=(δ_{+r}+δ_{−r})/2`, supported on the two minima. This **does not follow** from minimization alone; equal weighting is an additional sign-symmetry prescription.

**Z3, conditional composition rule.** Conditional on one shared `T=t`, distinct internal labels carry signs with `P(σ=±1 | t)=(1±t)/2`, independently given `t`. The full law for one source with N slots is

`P_N(σ_1,...,σ_N)=1/2 ∏_i (1+rσ_i)/2 + 1/2 ∏_i (1−rσ_i)/2`.

For *independent sources* use independent latent variables and the product of their complete laws. For instances of the *same source*, use the shared `T`. The source-sharing equivalence relation is part of the **stipulated composition context**; it is not yet derived geometry. There is no requirement that the two constructions be identical.

**Z4, observation interpretation still open.** `P_N` is a classical mathematical probability model. It is not a proof that observers, apparatuses, signals, settings or clocks exist. The meaning of physically accessible readouts must still be derived or calibrated.

### Tier 1: optional algebraic quantum comparison, not a fundamental derivation

To test how far the idea can be represented in existing mathematics, introduce the *-algebra `M_2(C)` with Pauli operators `X,Y,Z`. This noncommutative algebra and its positive trace-one states are **new inputs**. Let

`ρ_t = 1/2 [I + sqrt(1−t²) X + t Z]`, for `|t|<1`.

This is a pure positive density matrix with signed `Z` expectation `t`. At prescribed `t`, it is the unique maximizer of `Tr(ρ X)` among all qubit states with `Tr(ρ Z)=t`, using `X` as the calibrated coherence axis. Choosing that axis and selecting the extremum are additional stipulated rules.

Set `ρ_+=ρ_{+r}`, `ρ_−=ρ_{−r}`, and for one common source define

`Ω_N = 1/2 ρ_+^{⊗N} + 1/2 ρ_−^{⊗N}`.

The effective one-slot state is `Ω_1=(I+sqrt(1−r²)X)/2`. All `Ω_N` are positive, trace one, exchangeable and exactly projectively consistent. The ordinary `Z`-basis probabilities of `Ω_N` reproduce the classical `P_N` above. None of this proves that the Hilbert formalism or Born probabilities are fundamental consequences of `S_0`.

## 4. Exact theorems and checks within the steelman

### Proposition A: projective closure without retuning

For every `N≥1`, `Tr_last Ω_{N+1}=Ω_N`. Proof: each `ρ_±` has unit trace, so `Tr_last ρ_±^{⊗(N+1)}=ρ_±^{⊗N}`; the mixture preserves this identity. The same calculation gives normalization, positivity and permutation invariance. The analogous classical identity follows by summing `(1+tσ)/2` over `σ=±1`.

### Proposition B: signed cancellation with nonzero quadratic magnitude

Let `Q=mZ`. Then `Tr(Ω_1 Q)=0`, `Tr(Ω_1 Q²)=m²>0`. For distinct slots, all odd products of `Z` have expectation zero, while an even `k`-fold product has expectation `r^k`. With `r=1/2`, for instance, the two-slot `ZZ` expectation is `1/4` and the four-slot `ZZZZ` expectation is `1/16`.

This concerns an ensemble mean, not cancellation of each pair of complex amplitudes or total physical electric charge. It says nothing about conservation.

### Proposition C: one algebraically nontrivial action with no physical time

Take `Q=mZ` and `R=X`, and choose `κ>0`. Define the *unordered* commutator-cost functional

`I(Q,R) = κ/4 * Tr[ Ω_1 [Q,R]†[Q,R] ]`.

Since `[Z,X]=2iY`, `[Q,R]†[Q,R]=4m² I`, and hence `I(Q,R)=κm²>0`. Conjugation by `X` flips `Q` and preserves the state and the action cost. This is a mathematical mismatch functional between two noncommuting algebraic quantities. It neither requires nor supplies physical elapsed time, causal influence, energy conservation or chronological motion. Its numerical scale is not separately identified: `(m,κ)↦(cm,κ/c²)` leaves this action cost unchanged.

### An Action[] composition warning

Even without a physical clock, algebraic operations need not commute. For example, with `U_Z=(I+iZ)/sqrt(2)` and `U_X=(I+iX)/sqrt(2)`, both are unitary and

`U_Z U_X−U_X U_Z=−iY≠0`.

This is an exact algebraic ordering distinction, *not* evidence that either operation happened earlier in physical time. An ontology identifying `Action[]` with an unordered collection must define whether the composition is symmetrized, context dependent, globally constrained, or accompanied by a physical ordering that is independently derived. The absence of predefined causality cannot substitute for that rule.

### Proposition D: conditional empirical readout, with its exact context

At `r=1/2`, `Ω_1=(I+(sqrt3/2)X)/2`; a separately permitted conventional quantum `X+` effect would yield

`p_X+=(2+sqrt3)/4≈0.933013`.

The sign-pair probabilities from the shared-source two-slot preparation are `P(++)=P(--)=5/16`, `P(+-)=P(-+)=3/16`. A conventional SWAP test on two *independently prepared one-slot copies* would yield `p_SWAP+=15/16`.

These values are predictions of a known qubit preparation and measurement model **if that preparation and apparatus exist**. They are not predictions distinguishing the ontology from standard quantum theory.

### Proposition E: the indispensable source-composition distinction

The shared-source state `Ω_2` differs from the two-independent-source state `Ω_1⊗Ω_1` by exactly

`Ω_2−Ω_1⊗Ω_1 = (r²/4) Z⊗Z`.

For `r=1/2`, the trace distance is `1/8` and a `ZZ` correlation test differs by `1/4`. This difference is a mathematical *source-sharing convention*, not a novel physical effect. The state alone does not derive the source identities; assuming the two systems are physically equivalent would be an error.

## 5. Three mathematical reconstruction possibilities and their exact limitations

**Hilbert representation (GNS).** A unital C*-algebra with a positive normalized state `ω` admits a Hilbert representation constructed by quotienting the null space of the form `⟨A,B⟩=ω(A†B)` and completing. This is an established theorem, not a prephysical discovery. It does not derive why the observable algebra must be noncommutative or why laboratory instruments implement all positive effects. If the root algebra is commutative, its positive state has an ordinary classical probability representation.

**Possible time-like algebraic flow (modular theory).** For a faithful finite-dimensional state `ρ`, the map `σ_s(A)=ρ^{is} A ρ^{-is}` defines a one-parameter automorphism group. In the concrete example with `0<r<1`, the symmetric state `Ω_1` is faithful; its eigenvalues are `(1±sqrt(1−r²))/2`, so its modular action on `Z` is nontrivial. The symmetrized correlation is `cos(s log[p_+/p_-])`. No physical clock, beginning/end, frequency unit or causal direction is derived. The mathematical parameter and periodicity of this finite example are not a physical temporal oscillation. Connes and Rovelli's thermal-time hypothesis is the appropriate prior art, not a completed result about this ontology.

**Possible geometric correspondence (spectral structures).** A physical metric cannot be obtained from the name *relational*. Connes-type spectral distance requires an algebra, an appropriate Hilbert representation **and an independently characterized Dirac operator or Lipschitz seminorm**. Supplying such an operator would import metric information unless it is selected by the original action under a justified principle. The original opposite-sign graph fails the locality tests and is not retained as a foundational generator.

## 6. The steelman's principal internal limitation: entanglement

The source-sharing family `Ω_N` is explicitly a convex mixture of product states, so it is **separable for all finite N**. More broadly, the established quantum de Finetti theorem states that an infinitely exchangeable, projectively consistent sequence of finite-dimensional quantum states has a mixture-of-identical-product-states representation. It cannot contain entanglement between its distinguished tensor factors.

For local dichotomic quantum measurements, every separable state satisfies the CHSH bound `|S|≤2`. The observed violation of suitable Bell inequalities means that **if** the complete physical model identifies spatially separated laboratories with these individual slots and permits only the specified local operations, this construction cannot represent those data. It is not a complete physical quantum theory.

**Positive countercontrol, not a repair by fiat.** Dropping global exchangeability allows a projectively consistent *entangled* family: assign a maximally entangled pair to two distinguished internal factors and append independent other factors. Algebraically, the clock-unassigned unitary `U=exp(iπ Z⊗Z/4)` maps two `X+` qubits into a maximally entangled two-qubit state. The reduced single-qubit state is `I/2`; this family can be consistently enlarged by tensoring further factors. But the unitary rule, selected pair, complex Hilbert formalism and physical control are new inputs. They have not emerged from `S_0`. In particular the need to identify a special pair of internal slots replaces permutation symmetry with a non-derived relation.

Hence the correct hard fork is: either retain full infinite exchangeability and accept its quantum separability limitation, or derive a nonexchangeable interaction/composition law that permits entanglement without assuming the physical adjacency it seeks to explain. Neither side is currently finished.

## 7. Ruthless external comparisons: superstrings and matrix constructions

**Strongest string-side evidence.** Perturbative superstrings provide specific conditional S-matrix amplitudes, protected spectra, anomaly cancellation constraints and restricted black-hole state counts. The fixed type-II ten-dimensional tree-level four-graviton *log-form-factor* angular coefficient ratios are exactly `3/4` (cubic) and `13/16` (quintic). These are not observed differential cross-section ratios. The zero-dimensional signed model does not yet predict graviton propagation, scattering angles or an S-matrix, and thus does not compete with that calculation.

**Strongest nonspatial comparator.** The IKKT/IIB matrix model is zero-dimensional in its base-coordinate formulation, but supplies ten Lorentz-index matrices, supersymmetry, fermions, an action and an integration rule. Its full nonperturbative type-IIB equivalence remains a conjectural objective. A 2025 regulator audit challenged apparent Lorentzian classicalization. Conditional 2026 numerical and algebraic investigations of emergent dimensionality rely on deformations, gauge- or generator-related premises; they do not license a premise-free origin of the observed universe.

**The timelessness claim is not unique.** Tomita–Takesaki modular theory, Connes/Rovelli's thermal-time hypothesis, generally covariant boundary approaches, matrix models and causal fermion systems provide established routes to mathematical nonchronological structures. The steelman must compete by supplying a complete derivational chain and, eventually, matched predictions, not simply the phrase *action without time*.

**Separate historical cosmology.** The Volume Inflection Model assumes a 5D proper-time metric, compact directions and a stress law; its tuned stationary volume requires `K=-3H` and `κρ=-6H²`. Its finite-torus scalar benchmark fails the tuned cubic at every finite aspect. This model is neither a foundation of the zero-dimensional candidate nor a complete test of string theory.

## 8. Alternative explanations and very small outliers retained

1. The original anti-balanced four-slot action remains a valid finite law; unique five/six extensions and its sharp minimum seven/infinite distances `74/945`, `47/216` are retained despite the need to retire its unlimited-generative interpretation.
2. A hard-supported six-slot ensemble cannot arise as the exact extension of an everywhere-finite Gibbs action. Full support and exact projectivity must not be silently traded.
3. Two **different** infinitely exchangeable latent-bias models can share all one-, two-, and three-slot signed moments and differ at fourth order by `η−η²`; at `η=10^−6` this difference is exactly `0.000000999999`. This limits identification even in the replacement model unless its latent prior is independently fixed.
4. The original five-/six-vertex co-Ising graph aliases remain mathematical controls. For the biconnected six-vertex pair at `z=0.99`, the hypothetical squared-magnetization total variation is about `6.34438×10^−8` and KL about `1.06710×10^−14` nats, not experimental residuals.
5. The size-dependent antialignment family has a valid locally independent thermodynamic limit while collective fluctuations retain a nontrivial variance deficit. That is a separate **nonprojective** limiting route, not the exactly projective steelman adopted here.
6. Purely imaginary decoherence-kernel coherence, rank-one normalizer null sectors, faithful-unit regularizations, DNN classical-pair representations and the DNN five-cycle beyond matrix-CP factorization remain distinct controls. No automatic physical reading is assigned.
7. Finite-dimensional modular phase recurrence is a mathematical periodicity in a dimensionless parameter. It is not physical temporal oscillation. The Ricker zero-mean positive-norm response is a further conditional effective description requiring a supplied continuum coordinate and measure.

## 9. Falsification / decision gates before formal pipeline steelman

**G1, generative law:** The root action, support/measure and conditional composition rule must be independently motivated. More than one prior or source-sharing relation fits the same low-order signed data.

**G2, internal composition and restriction:** All admitted preparation/source contexts must have a single natural composition rule, exactly or with controlled error, not arbitrary replacement channels that merely satisfy projective commutation identities.

**G3, genuinely quantum operation:** Recover tested Bell/noncommuting instruments or explicitly supply an interaction mechanism that leads to them. Full infinite exchangeability plus local tensor-factor readouts is insufficient.

**G4, classical records and causal order:** Derive robust, independently accessible, persistent record categories. Show when physical causal propagation is warranted without assuming a directed clock in the starting action.

**G5, geometry:** Derive a metric/causal cone and a stable dimensional regime across resolution scales. Single-point spectral-dimension values or complete bipartite adjacency are insufficient.

**G6, field physics:** Recover Lorentz covariance, spin-two gravitational interactions, matter and gauge dynamics with correct experimentally constrained limits. Satisfy physical conservation identities and known scattering/astronomical tests.

**G7, empirical discrimination:** Specify a string sector and a candidate sector with matched preparations, probes, calibration and predicted outcomes. Do not reward the signed candidate for not making a prediction, or reject the whole string program because one vacuum or regulator fails.

**G8, no unnoticed assumptions:** Every claimed result must identify which of the algebra, positivity, measurement, action, source partition, Hilbert or geometry was stipulated and which was proved.

## 10. Provisional judgment

**Mathematical steelman:** Successful in a narrow sense. The explicitly proposed zero-spatial-dimensional state can have a signed positive magnitude, a nonzero algebraic action with no physical clock, a sign symmetry, exact all-size projective composition, and a consistent conditional noncommutative representation. These claims can be proved without introducing physical space or an initial/final temporal boundary.

**Ontological and physical steelman:** Incomplete. It does not derive why the root algebra, signed variable, action, global latent source, positive state, Born-rule instruments or effective physical distinctions must exist. The exactly exchangeable quantum representation is separable. No macroscopic record, clock, physical causal propagation, metric, spin-two gravitational sector, observed quantum violation or independent string-comparison prediction has been derived.

**Cross-adversarial result:** Superstrings currently lead on *developed conditional physical mathematics*. This is not a measured probability of ultimate ontological truth. The zero-dimensional signed-action hypothesis remains a specifically stipulated falsification target. It is not rescued by renaming imported quantum formalism *emergent*.

## References and prior art (selected, not exhaustive)

- Caves, Fuchs and Schack, *Unknown Quantum States: The Quantum de Finetti Representation*, J. Math. Phys. 43 (2002), 4537, https://arxiv.org/abs/quant-ph/0104088; see the published erratum clarifying the infinite-sequence definition.
- Connes and Rovelli, *Von Neumann Algebra Automorphisms and Time-Thermodynamics Relation in General Covariant Quantum Theories*, Class. Quantum Grav. 11 (1994), 2899, https://arxiv.org/abs/gr-qc/9406019.
- Gelfand–Naimark–Segal construction, formalized in Isabelle/HOL by Schmoetten and Fleuriot (March 2026), https://isa-afp.org/entries/Gelfand_Naimark_Segal.html.
- Ishibashi, Kawai, Kitazawa and Tsuchiya, *A Large-N Reduced Model as Superstring*, Nucl. Phys. B 498 (1997), 467, https://arxiv.org/abs/hep-th/9612115.
- Asano et al., *Defining the Type IIB Matrix Model without Breaking Lorentz Symmetry*, Phys. Rev. Lett. 134, 041603 (2025), https://doi.org/10.1103/PhysRevLett.134.041603.
- *Supersymmetric origin of four-dimensional space-time in the IIB matrix model*, Nuclear Physics B 1030 (2026), 117610, https://doi.org/10.1016/j.nuclphysb.2026.117610. Leading-order and background restrictions apply.
- Konstantopoulos and Yuan, *On the Extendibility of Finitely Exchangeable Probability Measures*, Trans. Amer. Math. Soc. 371 (2019), 7067–7092, https://doi.org/10.1090/tran/7701.
- Hensen et al., *Loophole-free Bell inequality violation using electron spins separated by 1.3 kilometres*, Nature 526 (2015), 682, https://doi.org/10.1038/nature15759.
- Shalm et al., *A Strong Loophole-Free Test of Local Realism*, Phys. Rev. Lett. 115 (2015), 250402, https://doi.org/10.1103/PhysRevLett.115.250402.
- Finster, Grotz and Schiefeneder, *Causal Fermion Systems: A Quantum Space-Time Emerging from an Action Principle*, https://arxiv.org/abs/1102.2585.
- Filippov, Gudder, Heinosaari and Leppäjärvi, *Operational Restrictions in General Probabilistic Theories*, Found. Phys. 50 (2020), 850, https://doi.org/10.1007/s10701-020-00352-6.

## Reproducibility statement

An independent explicit-exception SymPy verifier checks positivity, parity, all-state normalization, exact partial-trace consistency through four slots, low-order correlations, commutator action, calibrated quantum probabilities, source-sharing trace distance, an internally generated algebraic automorphism, a projectively consistent distinguished entangled pair, a conventional Bell control, retained sharp extension bounds and selected string-sector angular ratios. It was executed in standard Python, `-O` and `-OO`. Numerical and symbolic checks verify the claimed finite identities; the general propositions are analytic and the physics remains hypothetical.
