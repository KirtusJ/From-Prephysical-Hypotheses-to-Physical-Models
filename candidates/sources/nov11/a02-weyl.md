# Director A | Compositional Event Algebra with Conditional Records, construction iteration 2

**Research program:** From Prephysical Hypotheses to Physical Models  
**Research direction:** Kirtus Justus  
**Constructing reviewer:** LLM Director A (OpenAI)  
**Date:** 11 November 2026, B.C. Pacific Time  
**PCP parent:** Initial External Grounding OPEN. This is *voluntary construction investigation inside grounding*, not authorization to enter the formal Steelman phase.  
**Status:** Explicitly stipulated, withdrawable candidate. No physical carrier, ontology, clock, experimental preparation, or physical law is established.

## 1. Scope and relationship to prior iteration

The first iteration selected a finite reversible groupoid `G`, its **stipulated** complex convolution *-algebra, a **stipulated** positive normalized state, a **stipulated** effect/instrument observation contract, and conditional CP dephasing/records. The two-object pair groupoid yields `M_2(C)`; its qubit sector and *additional* tensor-composition rule allow a CHSH `2 sqrt(2)` positive control. Under a preferred record basis, dephasing gives a classical stochastic chain. These are accurate mathematical representation results, **not a derivation of Born probabilities, individual outcomes, physical time or Hamiltonian mechanics**.

This iteration retains those commitments as *auditable costs* and adds one specific conditional route toward classical **kinematics**. It also proves a non-selection obstruction that challenges the candidate at a more primitive stage. Both are equally important outcomes.

## 2. Negative theorem: full relabeling symmetry cannot select a canonical conjugate pair

Let `P_N` be the pair groupoid on an otherwise unstructured `N`-element set, with convolution algebra `A_N=C[P_N] ≅ M_N(C)`. Under object relabeling by `S_N`, the matrix algebra transforms by simultaneous permutation conjugation, `A ↦ P A P^{-1}`.

**Theorem (unconditional, finite-dimensional).** For `N>=2`,

`M_N(C)^{S_N} = { α I + β (J-I) : α,β ∈ C }`, where `J` is the all-ones matrix.

Proof: permutation invariance forces all diagonal entries to equal one common value and all off-diagonal entries to equal a second value; conversely such matrices are invariant. The invariant algebra is commutative. Thus no **individually distinguished**, object-relabeling-invariant pair of elements can satisfy a nontrivial noncommutative Weyl relation.

**Scope:** This rules out selecting a *canonical ordered conjugate pair of observables* by the bare unlabeled pair groupoid alone, under the stated invariance requirement. It does not forbid symmetry breaking, added relational labels, a physically selected reference, or a covariant *family* of choices. Those would require additional structure and supporting evidence. A stronger invariance under all inner automorphisms would leave only scalar matrices.

This is a real selection obstruction: the candidate cannot simply claim that a position/momentum pair is already latent in the arrow-composition law.

## 3. Conditional finite-matrix-to-Poisson construction

**New stipulated ingredients, visibly imported:** a cyclic ordering of the `N` objects, an identification of chosen matrix modes with Fourier modes on a classical two-torus, complex phases, and the dimensionless comparison parameter `h_N=2π/N`. None is derived from the raw groupoid; none is a physical frequency or a physical clock. They explicitly *supply* the phase-space interpretation whose emergence is under investigation.

Let `ω_N=e^{2πi/N}`. On `C^N`, define the unitary cyclic shift `U_N e_j=e_{j+1 mod N}` and clock `V_N e_j=ω_N^j e_j`. They obey `V_N U_N=ω_N U_N V_N`.

For integer modes `(k,l)`, set

`W_N(k,l)=exp(πi k l/N) U_N^k V_N^l`.

A direct multiplication gives

`W_N(k,l) W_N(k',l') = exp[-πi σ/N] W_N(k+k',l+l')`,

where `σ=k l'-l k'`. Therefore

`[W_N(k,l),W_N(k',l')]/(i h_N)=-(N/π) sin(πσ/N) W_N(k+k',l+l')`.

Now **separately stipulate** the smooth two-torus `T^2` with coordinates `(q,p)` and its standard Poisson bracket. Identify its Fourier mode `f_{k,l}(q,p)=exp[i(kq+lp)]` with `W_N(k,l)` using a quantization map `Q_N`. Classical Fourier-mode brackets satisfy

`{f_{k,l},f_{k',l'}}=-σ f_{k+k',l+l'}`.

Hence the exact finite operator-norm discrepancy is

`|| [Q_N(f_{k,l}),Q_N(f_{k',l'})]/(i h_N) - Q_N({f_{k,l},f_{k',l'}}) || = |σ-(N/π) sin(πσ/N)|`

and the unconditional elementary bound is

`<= π² |σ|³/(6N²)`.

For any **fixed** pair of finite trigonometric polynomials `f=Σ a_α f_α`, `g=Σ b_β f_β`, using the operator triangle inequality gives the explicit **conditional** Dirac-type bound

`|| [Q_N(f),Q_N(g)]/(i h_N)-Q_N({f,g}) || <= (π²/(6N²)) Σ_{α,β}|a_α b_β| |σ(α,β)|³`.

This tends to zero at `O(N^-2)` for fixed finite Fourier support, with this *stipulated* phase-space identification. No uniformity for Fourier support increasing with `N` has been proved. No one-parameter physical dynamics has been constructed.

### Exact discrete canonical transformation: a positive control

Let `F_N` be the discrete Fourier unitary with entries `N^-1/2 ω_N^{jk}`. It satisfies exactly

`F_N U_N F_N^*=V_N`, `F_N V_N F_N^*=U_N^-1`, and thus

`F_N W_N(k,l) F_N^*=W_N(-l,k)`.

The right side is the quantization of the classical symplectic rotation `(q,p)↦(p,-q)`, because `f_{k,l}(p,-q)=f_{-l,k}(q,p)`. This is an **exact, discrete covariance identity** in the selected model. It is not a continuous Hamiltonian flow or a physical time-evolution law. The finite Fourier transform has been imported as a special unitary; the bare pair groupoid does not select it.

### Verification

A separately written NumPy checker verifies the Weyl relation, fixed-mode `O(N^-2)` bounds and exact Fourier covariance for `N=5,7,11,17,31,71`, including negative modes and nonzero symplectic pairings. It also verifies that the permutation-invariant matrix space has dimension two for `N=3,4,7`. The algebraic proofs above are independent of these finite controls. Known noncommutative-torus and deformation-quantization literature predates this construction; neither novelty nor physics is claimed.

## 4. Why this is NOT a classical-mechanics emergence theorem

The torus, cyclic order, pairing of modes with `(q,p)`, symplectic bracket, comparison scale `h_N` and discrete Fourier rotation were **all separately selected**. Therefore the limit establishes a *mathematical compatibility/control* between already stipulated quantum-style matrices and an already stipulated classical phase space. It does not select a physical geometry, derive a canonical pair, produce continuous motion, supply mass/energy units, or justify a physical clock.

In particular, it does not yet give an Egorov estimate for a continuous one-parameter family `α_t^N` converging to a Hamiltonian flow `Φ_t`, and it does not derive Newton's law or a relativistic field theory. A rigorous next constructive challenge is to choose a fixed smooth Hamiltonian `H`, define dynamics and a class of symbols with uniform remainder, and prove an estimate

`|| α_t^N(Q_N(f)) - Q_N(f∘Φ_t) || ≤ ε_N(f,H,T)` for `|t|≤T`, `ε_N→0`.

Here `t` is **auxiliary mathematical flow time** until an independently calibrated physical duration bridge exists. Egorov correspondence is already established in conventional semiclassical analysis, so reproducing it would be a mathematical positive control rather than evidence of new ontology.

## 5. Quantum-sector selection and measurement debts remain

- `C` coefficients and *-algebra multiplication are stipulated; noncommutative `M_N(C)` already imports much quantum kinematics.
- A normalized positive state and an effects/instrument observation rule are stipulated. GNS produces Hilbert representations **after** positivity is granted, not a preparation procedure or empirical Born law.
- Selecting tensor products, Bell states, and local operations to demonstrate CHSH `2 sqrt(2)` assumes the relevant composite and measurement resources. The record-compatible classical rival remains viable wherever the observable menu is diagonal.
- Dephasing is an assumed CP map and does not by itself select a single definite outcome or uniquely identify a pointer basis.
- Finite matrices cannot satisfy `[Q,P]=i ħ I` for nonzero `ħ` because `tr[Q,P]=0`. The controlled limit avoids exact finite CCR but does not establish an unbounded representation or physical canonical commutation.
- Published operational reconstructions already derive quantum theory from explicitly stated information-processing axioms. The candidate must show additional independent assumptions, discriminating predictions, or a strictly weaker derivation, not repackage an existing operational reconstruction.
- The previously established graph/noise aliases show that even a complete recorded law may not identify its latent source, inversion and detector mechanisms without warranted assumptions. This remains an explicit **falsification and measurement-interface obligation** for the candidate.

## 6. Commitments, competing models and withdrawal criteria

**Working construction commitment** (not belief in its ontology): continue `P_N → C[P_N] → state/effect model → records → added cyclic phase-space correspondence → controlled Hamiltonian limit`, retaining all imports on a dependency ledger.

**Live competitors:** identity-only groupoid (commutative classical alternative); finite real/quaternionic algebras; operational GPT reconstructions; causal/histories frameworks; ordinary preselected torus quantization; classical record/Markov models; alternative time/geometry assignments.

**Kill criteria / negative outcomes with equal standing:**

1. If complex amplitudes, positivity, tensor products and the Born rule cannot be weakened without importing most of quantum mechanics, classify the result **quantum-compatible representation**, not emergence.
2. If extra cyclic order/torus symplectic data remain indispensable and unselected, classify the classical result **conditional deformation quantization**, not emergence of classical geometry or mechanics.
3. If the continuous flow/time bridge fails or requires arbitrary physical units, do not speak of classical mechanics, only discrete symplectic covariance and bracket control.
4. If actual operational observations admit classically observationally equivalent alternatives, no empirical identification can be claimed from that observation menu.
5. If the program's physical source/clock/detector contracts are untestable, suspend physical interpretation without discarding valid mathematics.

The parent PCP phase stays **Initial External Grounding, OPEN**. No demand for positive ontology, no imported fundamental physical time/frequency, no assertion that LLM agreement is independent proof, and no claim that this track fixes Wilson–Dirac or quantum-copying obligations.

## 7. External precedent and boundaries

- Finite pair-groupoid convolution and matrix algebra: A. Sims, *Hausdorff étale groupoids and their C*-algebras*, §3.1, https://aidansims.com/papers/Sims2017.pdf (also Roman–Villatoro, example 4.2, https://www.mathnet.ru/links/9e6c7930b90a340dc3318ab25b86d02d/sigma2095.pdf).
- GNS representation from positive functional: *Mathematical Structures on State Sets*, https://www.sciencedirect.com/science/article/pii/S1574691707000062.
- Informational reconstruction under explicit operational axioms: Chiribella–D'Ariano–Perinotti, *Phys. Rev. A* **84**, 012311 (2011), https://doi.org/10.1103/PhysRevA.84.012311.
- Noncommutative torus deformation: *Pseudodifferential Operators on Noncommutative Tori: A Survey* (2024), https://link.springer.com/article/10.1007/s44007-024-00122-0.
- Classical dynamics under deformation quantization: M. Rieffel, *The Classical Limit of Dynamics for Spaces Quantized by an Action of R^d*, https://www.cambridge.org/core/journals/canadian-journal-of-mathematics/article/classical-limit-of-dynamics-for-spaces-quantized-by-an-action-of-d/4ECCD173172E9065FDA86BB49772E268.
- Standard Egorov correspondence: S. Nonnenmacher, *Introduction to Semiclassical Analysis*, https://www.imo.universite-paris-saclay.fr/~stephane.nonnenmacher/enseign/Course-Semiclassical-Analysis2024-total.pdf.
- Decoherence and the problem of definite outcomes: Stanford Encyclopedia of Philosophy, https://plato.stanford.edu/archives/spr2022/entries/qm-decoherence/.

These are **external background precedents**, not endorsements or independent validations of a new physical ontology.
