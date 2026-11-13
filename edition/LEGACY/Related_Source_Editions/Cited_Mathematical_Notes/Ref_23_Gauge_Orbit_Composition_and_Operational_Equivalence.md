# Gauge-Orbit Composition and Operational Equivalence

*Selected sections of an unpublished mathematical note.*

**Original date:** 2026-11-08.  
**Research direction:** Kirtus Justus.  
**Mathematical and editorial assistance:** ChatGPT (OpenAI).

The selected statements, assumptions, arguments, and examples below are drawn from the original note. This editorial excerpt does not claim independent verification. Numerical results are source-reported unless established by the reproduced argument; cited literature is identified from the original note. Original section numbering is retained.


## 3. Conditional theorem: the diagonal orbit quotient is not naively compositional

Let a nontrivial group `G` act on a finite-dimensional Hilbert space `H` by unitaries `U_g`. For a state `rho`, write `[rho] = {U_g rho U_g† : g in G}`. The separately proposed physical state is the orbit `[rho]`.

For two jointly described systems, suppose that only *simultaneous* relabelings are admitted: the diagonal action is `U_g ⊗ U_g`. The whole-system SWAP operator `F` on `H ⊗ H` commutes with every `U_g ⊗ U_g`. Thus `E_+ = (I+F)/2` is a valid diagonal-invariant quantum effect.

Suppose `rho' = U_h rho U_h†` differs from `rho`. Both represent the same individual orbit. Nevertheless,

$$
\begin{aligned}
\Pr(+\mid\rho\otimes\rho)&=\tfrac12(1+\operatorname{Tr}\rho^2),\\
\Pr(+\mid\rho\otimes\rho')&=\tfrac12(1+\operatorname{Tr}\rho\rho'),\\
\Delta&=\tfrac14\|\rho-\rho'\|_2^2>0.
\end{aligned}
$$

Here `Tr[F(rho⊗sigma)] = Tr(rho sigma)` and `Tr(rho'^2)=Tr(rho^2)` prove the formula. The two joint states are distinguished by an admissible diagonal-invariant effect, so they cannot define a single product of separately specified orbits without additional relative-alignment information.

**Quantifier:** This refutes a *representative-independent product of arbitrary separate orbit states* using the diagonal gauge action. It does not refute a physical **copying instrument** that explicitly produces aligned copies, or a fully relational gauge theory that models shared reference data. An aligned-copy map is extra structure, not the ordinary product on individual orbit classes.

### Exact four-qubit counterexample

Let `|s> = (|01>-|10>)/sqrt(2)`, and define `A = |s>_12|s>_34` and `B = |s>_13|s>_24` on the same four-factor Hilbert space. A permutation of factors maps `A` to `B`; the projectors `rho_A` and `rho_B` belong to one permutation orbit. Yet

$$
|\langle A\mid B\rangle|^2=\operatorname{Tr}(\rho_A\rho_B)=\tfrac14.
$$

The aligned composite `rho_A⊗rho_A` has SWAP-positive probability `1`, while the independently relabeled composite `rho_A⊗rho_B` has `5/8`. Hence the exact gap is `3/8`. This is **not** the earlier `1/4` gap between `rho_A⊗rho_A` and `T(rho_A)⊗T(rho_A)`.

## 4. Two inequivalent repairs

### 4.1 Independent gauge actions on separately prepared systems

When the composite group is `G×G`, permitted effects commute with `U_g⊗U_h` independently. Let `T` be the ordinary single-copy group twirl. The product twirl is exactly `T⊗T`, so two states with the same single-copy twirl retain that equivalence under independent product preparation:

$$
T(\rho)=T(\rho')\,,\ T(\sigma)=T(\sigma')
\quad\Rightarrow\quad
(T\otimes T)(\rho\otimes\sigma)=(T\otimes T)(\rho'\otimes\sigma').
$$

But global SWAP generally **does not** commute with `U_g⊗U_h` for independently chosen `g,h`. This repair rules out the earlier SWAP distinction as an allowed effect. It loses precisely the shared-reference information required to distinguish relative orientations. It does not prove that there can be no relational observations in a larger theory; it specifies a more restrictive one.

### 4.2 A gauge-covariant relative-reference datum

Introduce a group element `r ∈ G` encoding the relative orientation between two **formal** representatives, and use triples `(rho, sigma, r)`. Give them the simultaneous action of two arbitrary frame changes `g,h`:

$$
(\rho,\sigma,r)\mapsto
(U_g\rho U_g^\dagger,\,U_h\sigma U_h^\dagger,\,grh^{-1}).
$$

The relational comparison

$$
J(\rho,\sigma,r)=\operatorname{Tr}(\rho U_r\sigma U_r^\dagger)
$$

is exactly invariant. Indeed, the aligned second state transforms as `U_g (U_r sigma U_r†) U_g†`; cyclicity of trace then proves `J'=J`. In the four-qubit model `J` takes value `1` for properly aligned pairings and `1/4` for a fixed misalignment.

**Interpretation and assumptions:** A conditional mathematical repair, not a physical ontology. The interpretation and availability of `r`, the measurement of `J`, and the preparation of joint systems are all presently *stipulated*. No argument derives the relative reference from the proposed signed structure. Nothing in this construction equates `r` with physical distance, order, time or phase of a physical clock.

## 5. Conditional theorem: sufficiently rich diagonal multicopy effects separate finite-group orbits

The failure of one-copy invariant-affine observables to distinguish `rho` from its twirl does **not** persist if **all** diagonal-invariant joint effects on sufficiently many identically prepared copies are allowed.

For a finite group `G`, fix a target density matrix `rho`. For any density matrix `X`, consider the invariant real polynomial

$$
f_\rho(X)=\prod_{g\in G}\big\|X-U_g\rho U_g^\dagger\big\|_2^2.
$$

It vanishes on the entire `G`-orbit of `rho` and is strictly positive on every state outside that orbit. It is invariant under the group action because the factors are permuted.

Every squared-distance factor is the expectation of a fixed Hermitian operator `K_g` on **two copies** of `X`:

$$
K_g=F-A_g\otimes I-I\otimes A_g+(\operatorname{Tr}\rho^2)I\otimes I,
\qquad A_g=U_g\rho U_g^\dagger,
$$

so `Tr(K_g X⊗X)=||X-A_g||_2²`. The tensor product of these operators over all `g` yields a Hermitian observable `M` on `2|G|` copies whose expectation is `f_rho(X)`. Average `M` over the **diagonal** group action. Because the polynomial is invariant, this changes neither expectation nor its separating property. An affine spectral shift and rescaling of this finite-dimensional Hermitian operator supplies a valid invariant effect `0≤E≤I` with different probabilities on any two distinct orbits (choosing the target as one of them).

Thus, **under the exceptionally strong premise of access to all diagonal-invariant effects on arbitrary finite copy numbers, operational equivalence is exactly orbit equivalence** for a finite group. The simple constructive bound is `2|G|` copies; it is not claimed optimal. This is a standard finite-group invariant-theory phenomenon in an explicit quantum-observable form, not a novel theorem of physics or an emergence of the measurement postulates.

**Four-copy positive example:** For `G=Z_2` acting on a qubit by conjugation with `X`, the pure state `|0><0|` and the maximally mixed state `I/2` share the same one-copy twirl, but lie in different orbits. The source reports an exact four-copy invariant effect with probabilities `1/3` and `5/12`, respectively, and spectrum contained in `[0,1]`. The particular effect matrix and its normalization are not reproduced in this selected passage; these numerical values remain source-reported. Simpler two-copy effects already distinguish these particular states.

## 6. Anonymous pairing selection is impossible without extra structure

**Elementary symmetry control.** Let `X` be a finite set of `n` distinguishable formal slots with no additional relational structure. Its full automorphism group is `S_n`, which acts transitively on the unordered pairs `{{i,j}:i≠j}`. An `S_n`-invariant set of distinct pairs is therefore either empty or the whole complete graph. For every even `n≥4`, neither can be a perfect matching.

Consequently, the bare symmetry of an anonymous finite set cannot select one unique pairing. An invariant action may have all `(n-1)!!` perfect matchings as degenerate minimizers, but selecting one realization requires a symmetry-breaking mechanism, a distinguished structure, a relative-reference description or additional physical data. This control does **not** exclude a signed relational substrate with actual, stipulated symmetry-breaking information; it excludes deriving a preferred matching from *complete anonymity alone*.

An additional and stronger assumption at every size, namely exact permutation invariance plus conventional quantum partial-trace consistency, invokes the standard infinite quantum de Finetti theorem: the resulting density matrices are mixtures of product states and show no ordinary pairwise Bell nonlocality under tensor-factor local measurements. The theorem requires one exactly coherent, infinitely extendible sequence. It does not apply to isolated `n`-body state families, differently chosen restriction maps, or an as-yet-undefined physical gauge quotient.

## 7. Two separate equivalence relations, and why a nonlinear Bell objective is vulnerable

One-copy invariant-affine equivalence is equality of twirls:

$$
\rho\sim_1\sigma\quad\Longleftrightarrow\quad T(\rho)=T(\sigma).
$$

It is coarser than orbit equivalence. The nonlinear Bell-resource objective `A_N(rho)=-sum_{i<j}[S_max(rho_ij)-2]_+` is permutation-invariant on each orbit, but it is **not** constant on twirl fibers. A pure optimal dimer has negative action, while its `S_4`-twirl has action zero. Mixing two distinct optimal four-qubit matchings likewise produces `A_4=0` for `1-1/sqrt(2)≤p≤1/sqrt(2)`. These are legitimate conditional properties of ordinary qubit states, not linear Hamiltonian expectations.

The diagonal **all-multicopy** observation class can in principle distinguish all finite-group orbits and make such an invariant nonlinear property identifiable on those orbit classes. It simultaneously creates the problem of specifying relative preparation references; there is no free resolution. Choosing a sufficiently rich observation class is a substantive postulate, not a mathematical result forced by the word *gauge*.


## Limits of the selected passage


The group-twirl expressions presume that the stated normalized twirl is defined. The explicit polynomial separation construction in section 5 is for finite groups. The reported four-copy numerical example is not a substitute for an explicit effect matrix.


## Mathematical sources identified in the original note


- S. Cheng and M. J. W. Hall, *Anisotropic Invariance and the Distribution of Quantum Correlations*, Physical Review Letters 118 (2017), 010401. https://doi.org/10.1103/PhysRevLett.118.010401 . Independently optimized three-qubit CHSH monogamy within the stipulated qubit model.

- C. M. Caves, C. A. Fuchs and R. Schack, *Unknown Quantum States: The Quantum de Finetti Representation*, Journal of Mathematical Physics 43 (2002), 4537, and the 2007 erratum on a coherent sequence. https://doi.org/10.1063/1.1494475

- S. D. Bartlett, T. Rudolph and R. W. Spekkens, *Reference Frames, Superselection Rules, and Quantum Information*, Reviews of Modern Physics 79 (2007), 555. https://doi.org/10.1103/RevModPhys.79.555

- A.-C. de la Hamette and T. D. Galley, *Quantum Reference Frames for General Symmetry Groups*, Quantum 4 (2020), 367. https://doi.org/10.22331/q-2020-11-30-367
