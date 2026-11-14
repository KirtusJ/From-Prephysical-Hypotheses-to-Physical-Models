# Pair-Phase Quantum States: Bell Shareability, Variational Selection, and Restriction

**Date:** 8 November 2026, America/Vancouver  
**Research direction:** Kirtus Justus  
**Independent mathematical/computational audit:** ChatGPT (OpenAI)  
**Status:** Conditional finite-dimensional quantum mathematics. The pair-phase model is an explicitly **stipulated exploratory falsification target**, not an independently derived physical ontology, spacetime theory, or experiment.

## 1. Source and verification boundary

This note reconciles the six supplied contemporaneous materials: two research handoffs, two technical notes and two Python verifiers concerning the permutation-invariant total-spin Casimir, a selected-pair phase construction, source-sharing signed statistics, exact quantum prefix restriction and a proposed maximal-transverse-coherence rigidity theorem. They are **not** taken as verified merely because they report passing verifiers.

The developer-specified original upload paths were tested in the Python/CaaS runtime but were not present there. The file service returned separate materialization paths which were likewise not available to that runtime. Thus no byte-identical uploaded verifier execution is claimed. An **independently written verifier**, linked separately, passed 165 explicit exact/numerical checks in ordinary Python, `-O`, and `-OO`. Its checks include an independently assembled symbolic partial-transpose characteristic polynomial and a NumPy eigenvalue/CHSH adversary over nine parameter pairs. General conclusions below depend on analytic arguments; the finite checks are a second verification route.

## 2. Stipulated model and mathematical successes

Introduce imported qubit Pauli algebra, individual tensor factors, and conventional trace-one positive density matrices. For `0<r<1`, set `c=sqrt(1-r^2)` and

\[
\rho_\pm=\tfrac12(I+cX\pm rZ),\qquad
\Omega_N=\tfrac12\rho_+^{\otimes N}+\tfrac12\rho_-^{\otimes N}.
\]

The complete classical signed-`Z` probability law is

\[
P_N(\sigma)=\tfrac12\prod_i\frac{1+r\sigma_i}{2}
            +\tfrac12\prod_i\frac{1-r\sigma_i}{2}.
\]

For a selected pair, introduce the separate phase-operation assumption

\[
U_\phi=e^{i\phi Z\otimes Z},\qquad
\Xi_2(\phi)=U_\phi\Omega_2U_\phi^\dagger.
\]

All such unitaries leave the complete `Z`-basis probability law unchanged. At `phi=pi/4` the source's exact partial-transpose eigenvalues `{1/2,1/2,c^2/2,-c^2/2}`, its negativity `c^2/2`, and CHSH maximum `2 sqrt(1+c^4)` are correct. The fixed designated-matching prefix family is also mathematically consistent and preserves all signed-`Z` outcomes. The matching, factor algebras, quantum states and Born instruments are **inputs**, not consequences of a prephysical action.

## 3. A universal shareability obstruction not confined to the matching construction

**Conditional theorem.** No tripartite quantum state `Gamma_ABC` has the same CHSH-violating two-qubit state `Xi_2(pi/4)` on both `AB` and `AC`, where the factor and Pauli identifications are fixed.

**Proof.** The optimal CHSH score for the target pair is `S=2 sqrt(1+c^4)>2`. If both pair marginals were the target, choose the same optimal first-party observables on `A`, and equivalent optimal second-party observables for `B` and `C`. Toner--Verstraete monogamy would require `2 S^2 <=8`, which is false. QED.

**Quantitative version with the first pair exact.** If `Gamma_AB=Xi_2(pi/4)`, while `Gamma_AC` attempts to approximate it, fixed-test monogamy and `||B_CHSH||_op<=2 sqrt2` give

\[
D_{\rm tr}(\Gamma_{AC},\Xi_2)
\ge\frac{\sqrt{1+c^4}-\sqrt{1-c^4}}{2\sqrt2}.
\]

At `r=1/2` this is `(5-sqrt(7))/(8 sqrt2) = 0.208088151568...`. This is necessary, not certified optimal. If **both** pairs may deviate by a common distance at most `delta`, the corresponding weaker universal witness is `delta >= (S-2)/(4 sqrt2)`, equalling `0.08838834765...` at `r=1/2`. These are distances in the *specified quantum state space*, not measured laboratory limits.

This strengthens the uploaded observation that the matched construction fails arbitrary-pair quantum equivalence: no modification can restore the **same** Bell-violating two-body marginal on two overlapping pairs without changing the pair state or quantum-operational hypotheses. The original **prefix-only, selected-matching** construction survives because it demands no such equivalence.

Prior art: Toner & Verstraete (2006), arXiv:quant-ph/0611001; Kumari, Ghose & Mann, *PRA* 96, 012128 (2017), DOI 10.1103/PhysRevA.96.012128.

## 4. Exact arbitrary-phase entanglement and Bell threshold

Write `w=sin(2 phi)` and `q=cos(2 phi)`. Direct conjugation gives

\[
\Xi_2(\phi)=\frac14\Big[I\otimes I+cq(X\otimes I+I\otimes X)
+c^2X\otimes X+r^2Z\otimes Z-cw(Y\otimes Z+Z\otimes Y)\Big].
\]

The partial-transpose characteristic polynomial factors exactly as

\[
\det(\lambda I-\Xi_2^{T_2})
=\frac{(4\lambda^2-2r^2\lambda-c^2w^2)
       (4\lambda^2-(4-2r^2)\lambda+c^2w^2)}{16}.
\]

Consequently the full partial-transpose spectrum is

\[
\frac{r^2\pm\sqrt{r^4+4c^2w^2}}4,\qquad
\frac{2-r^2\pm\sqrt{(2-r^2)^2-4c^2w^2}}4.
\]

For `0<r<1`, the only negative eigenvalue (unless `w=0`) is the minus sign in the first pair. Therefore

\[
\boxed{\mathcal N(r,\phi)=\frac{\sqrt{r^4+4c^2\sin^2(2\phi)}-r^2}{4}.}
\]

Entanglement holds **for every nontrivial entangling phase** `sin(2 phi)!=0`; small phase and fixed positive `r` give

\[
\mathcal N(r,\phi)=\frac{2(1-r^2)}{r^2}\phi^2+O(\phi^4).
\]

This limit is **not uniform as `r->0`**: at `r=0` the negativity is `|sin(2phi)|/2`, linear rather than quadratic near `phi=0`.

The Pauli correlation matrix is

\[
T_\phi=\begin{pmatrix}c^2&0&0\\0&0&-cw\\0&-cw&r^2\end{pmatrix}.
\]

Let `lplus=(r^2+sqrt(r^4+4c^2w^2))/2`. Its two largest squared singular values are `c^4` and `lplus^2`, so

\[
\boxed{S_{\max}(r,\phi)=2\sqrt{c^4+lplus^2}.}
\]

At `r=1/2`, Bell violation holds exactly when

\[
\sin^2(2\phi)>\frac{7-\sqrt7}{12},
\]

with first positive threshold `phi_crit=0.323235764626...` radians. Thus entanglement for infinitesimal phase does **not** imply CHSH violation at that phase.

At `r=1/2`, `phi=0.001`, the minimum PPT eigenvalue is `-5.9997040284e-6`, while the local `X` expectation loses `1.7320502302e-6`. These values were checked with exact identities and independent high-precision/numerical eigensolvers. They are theoretical outliers, not experimental departures.

Prior art: Peres (1996), arXiv:quant-ph/9604005; Horodecki, Horodecki & Horodecki (1995), DOI 10.1016/0375-9601(95)00214-N.

## 5. Arbitrary deletion: exact distance for *every* admissible `r`

At `phi=pi/4`, the branch-one-qubit marginal is

\[
\mu_t=\tfrac12(I-ctY+tZ),\qquad t=\pm r.
\]

The paired construction's three-factor state gives, after deleting the second rather than the last factor, the **separable** crossing-pair state

\[
\Lambda_{13}=\tfrac12\mu_{+r}\otimes\mu_{+r}
             +\tfrac12\mu_{-r}\otimes\mu_{-r}.
\]

It shares the complete two-sign `Z` outcome law with `Xi_2` but differs as a quantum state. The eigenvalues of `Xi_2-Lambda` are exactly

\[
\frac{r^4-1}{4},\quad
\frac{r^4-4r^2+3}{4},\quad
-\frac{(1-r^2)^2}{4}\quad\text{(twice)}.
\]

The only positive eigenvalue gives the exact trace distance

\[
\boxed{D_{\rm tr}(\Xi_2,\Lambda_{13})=
       \frac{(1-r^2)(3-r^2)}4.}
\]

At `r=1/2`, this equals the source's `33/64=0.515625`. As `r->0`, it tends to `3/4`, precisely where the root pair-sign correlation tends to zero and the entangling phase becomes maximally effective. As `r->1`, it tends to zero. The source's isolated witness is therefore one value of a stronger exact family.

A separate comparison with **two independently sourced one-qubit states** gives `Xi_1=I/2`, and at `r=1/2` the quantum trace distance `D_tr(Xi_2,I_4/4)=5/8`, while the signed-`Z` probability distance is only `r^2/2=1/8`. This difference depends on which quantum measurements are supplied; it does not identify an intrinsic physical source.

## 6. Permutation-symmetric all-to-all phase fails projectivity at every nontrivial angle

Define the independently stipulated alternative

\[
U_N(\phi)=\exp\!\left(i\phi\sum_{i<j}Z_iZ_j\right),\quad
\Gamma_N=U_N\Omega_NU_N^\dagger.
\]

For two and three factors respectively, exact Pauli expectations give

\[
\langle X_1X_2\rangle_{\Gamma_2}=c^2,\qquad
\langle X_1X_2\rangle_{\Gamma_3}=c^2\cos^2(2\phi).
\]

Thus if `sin(2 phi) !=0`, the `N=3 -> N=2` partial-trace relation fails, with witness `c^2 sin^2(2phi)`. The exceptional `phi=k pi/2` can be checked with one-factor `X`: for odd `k`, the two-factor value is `-c`, while the three-factor value is `+c`. Only `phi in pi Z` survives, for which the phase operator is a scalar and introduces no genuine entangling interaction.

**Exact no-go:** for any `0<r<1`, this *same-angle, permutation-symmetric all-to-all Ising phase family* is projectively consistent between two and three qubits **only at trivial phases**.

At `r=1/2` and `phi=pi/4`, the reduced-state difference has eigenvalues

\[
\{-3/8,\ 3/16-\sqrt{15}/8,\ 3/16+\sqrt{15}/8,\ 0\},
\]

so its trace distance is exactly `3/16+sqrt(15)/8 = 0.6716229...`. At `phi=0.001`, the `XX`-witness mismatch is approximately `2.999996e-6`, which is small but mathematically nonzero.

This does not forbid other symmetric quantum hierarchies, particularly with more complex operations or differently justified restriction maps. It rejects this **specific** proposal to eliminate preferred matchings by applying one fixed all-to-all phase at every size.

## 7. Cross-handoff incompatibility with the earlier state-selective total-spin action

The earlier independent construction uses

\[
H_2=J_x^2+J_y^2+J_z^2=2(I-P_s),
\]

whose unique **minimum** is the antisymmetric singlet. However the original `Omega_2` is a convex mixture of identical-product branch states and is supported in the symmetric triplet sector. `U_phi` commutes with two-factor SWAP, so **all** the phase-paired states `Xi_2(phi)` remain triplet supported. Hence

\[
\boxed{\operatorname{Tr}(\Xi_2(\phi)P_s)=0,\qquad
\operatorname{Tr}(\Xi_2(\phi)H_2)=2.}
\]

These Bell-capable states therefore **maximize** the previous two-factor Casimir action, rather than minimize it. The two constructions are individually valid but cannot be described as a single unchanged action-to-state derivation.

A stronger convexity observation applies to any *linear* expectation-cost action `S_H(rho)=Tr(rho H)` on the full convex set of density matrices. The phase-paired `Xi_2` is mixed rank two, with nonzero eigenvalues

\[
\{1-r^2/2,\ r^2/2\},\quad 0<r<1.
\]

No mixed state can be the **unique** minimizer of such a linear cost: if a convex combination of distinct pure states minimizes a linear function, each contributing pure state must separately minimize it. To select `Xi_2` uniquely would require a nonlinear state functional, added constraints, an independently specified preparation, or another selection mechanism. One may stipulate such a mechanism, but it is not already present in the previous Casimir model.

## 8. Reconciled status, exceptions and evidence boundary

**Retain as verified conditional mathematics:** exact prefix consistency with distinguished pairs, complete signed-`Z` law unchanged by the phase, nontrivial Bell capability, arbitrary-angle negativity and CHSH formula, monogamy restriction, general arbitrary-deletion distance, and the rank/spectrum results. The source's all-order signed-law + maximal-one-site-`X` rigidity theorem remains consistent with the evidence and its proof assumptions; it is not automatically a statement about arbitrary physical operational state spaces.

**Reject as stronger explanatory readings:** arbitrary pair interchangeability for the Bell-violating state; exact projectivity of the fixed-angle all-to-all interaction; derivation of phase-paired `Xi_2` as a minimum of the preceding total-spin Casimir; unique linear-action selection of the rank-two mixed state; derivation of Born effects, a physical clock, physical quantum subsystem accessibility, causal propagation, metric or gravity.

**Retain tiny mathematical effects:** the `phi=0.001` PPT eigenvalue `-5.9997e-6`, one-site transverse loss `1.73205e-6`, all-to-all XX restriction defect `2.999996e-6`; the previously recorded Legendre finite-order aliases, exchangeable finite extension staircase, zero-mean positive-norm signals, imaginary-coherence models and extremely small co-Ising KL distances. None is measured evidence.

**Physical comparison:** graph-state phase gates and Bell monogamy are standard quantum theory. The foundational candidate still takes internal tensor factors, complex Hilbert space, a conditional latent source, a selected matching, phase exponentiation and conventional measurement rules as inputs. No independently grounded prephysical-to-physical bridge has been established. These exact successes and failures serve as adversarial conditions on future attempts, without selecting a total ontology.

### Selected external primary sources

- Toner and Verstraete (2006), *Monogamy of Bell correlations and Tsirelson's bound*, https://arxiv.org/abs/quant-ph/0611001.
- Kumari, Ghose and Mann (2017), *Sufficient condition for nonexistence of symmetric extension of qudits using Bell inequalities*, Phys. Rev. A 96, 012128, https://doi.org/10.1103/PhysRevA.96.012128.
- Horodecki, Horodecki and Horodecki (1995), *Violating Bell inequality by mixed spin-1/2 states*, https://doi.org/10.1016/0375-9601(95)00214-N.
- Peres (1996), *Separability Criterion for Density Matrices*, https://doi.org/10.1103/PhysRevLett.77.1413.
- Briegel and Raussendorf (2001), *Persistent Entanglement in Arrays of Interacting Particles*, https://doi.org/10.1103/PhysRevLett.86.910.

**Disposition:** Initial independent external grounding remains active. Keep the successfully constructed phase-paired state only as an explicitly stipulated, matching-dependent falsification target. Its pairwise monogamy, all-to-all refinement, and cross-action inconsistency results are exact and must be carried into subsequent tests. No ontological or empirical certification follows.
