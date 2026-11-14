# Nonspatial Algebraic Action: State Selection, Multiplicity, and Operational Identification

**Working Phase II exploratory ontology-construction audit | 8 November 2026 (America/Vancouver)**  
**Research direction:** Kirtus Justus. **Mathematical and computational assistance:** ChatGPT (OpenAI).  
**Status:** **Explicitly stipulated finite mathematical comparison, not established physics, not a paper or certification.** The cross-adversarial contest is closed. Existing theories are used only for independent scientific grounding, inherited mathematics, and stringent countercontrols. This note does not claim novelty for the singlet or Heisenberg/Casimir construction.

## 1. Source reconciliation and defects preserved

The supplied November 8 audits of projectively consistent signed ensembles and alternative quantum completions agree on the main limitations of the earlier steelman. Its supported root law is \(\nu=(\delta_{+r}+\delta_{-r})/2\), while \(S_0(t)=\lambda(t^2-r^2)^2\) vanishes on the entire selected support. Accordingly \(\lambda\) cannot determine relative probabilities, quantum state completion, source sharing, or measurement access. The separate cost \(\kappa\operatorname{Tr}(\rho[mZ,X]^\dagger[mZ,X])/4=\kappa m^2\) is *state-independent* for every trace-one qubit density matrix. Neither selects the claimed state. These failures are genuine shortcomings of the stronger derivation claims, not logical contradictions in the underlying finite distributions.

An angular family of pure, sign-covariant completions \(\rho_\pm^{(\varphi)}=[I+c\cos\varphi X\pm c\sin\varphi Y\pm rZ]/2\), \(c=\sqrt{1-r^2}\), has precisely the same full signed Z-basis statistics and projective composition while changing X-basis statistics. At \(r=1/2\), changing \(\varphi=0\) to \(\pi/2\) changes the one-system X+ outcome by \(\sqrt3/4\). Another two-system entangled pure completion has the same one-site states and signed pair table as the separable law but a different XX correlation and Bell-CHSH maximum \(\sqrt5\). Neither the root action nor its commutator cost resolves the ambiguity. The original infinitely exchangeable quantum family is separable and nonfaithful on the full matrix algebra for composite sizes \(N\ge2\); faithfulness and physical time are not recovered by an unsupported modular-flow argument.

The finite four-sign law proportional to \(2^{-M_4^2/4}\) remains a distinct, *retired as a universal action* countercontrol: it has a unique full-marginal 5-/6-slot extension, no 7-slot extension, exact sharp distances \(74/945\) (7 slots) and \(47/216\) (infinite exchangeability), and an action-marginalization obstruction at every nonzero quadratic coupling. Infinitely exchangeable signed models may have identical joint laws through every prescribed finite order and differ at higher order, as proved by orthogonal-polynomial latent measures. None of these are observed statistical anomalies.

**Source-provenance qualification:** one previous review described a particular similarly named Python snapshot as having undefined identifiers, while another inspected copy contains the necessary definitions. No byte-identical snapshot comparison has established the status of *every* version. A verified calculation cannot be invalidated by an ungrounded source allegation, and a repaired copy does not prove an earlier distinct version executed. The present analysis uses an independently written and executed verifier, rather than asserting verbatim reproduction of the current uploaded script bytes.

## 2. Explicitly stipulated two-system algebraic test

**Inputs S1–S5 (not derived):** finite-dimensional complex Hilbert space \(\mathbb C^2\otimes\mathbb C^2\), two operational factors, Pauli matrices \(X,Y,Z\), an abstract internal diagonal \(SU(2)\) representation, positive trace-one states, and a variational minimum rule. No physical coordinate, metric, clock, causality, spatial orientation, physical electrical charge or apparatus has been defined. The three generator labels are *internal*, and their supplied existence is a substantial premise.

Let \(J_a=(\sigma_a\otimes I+I\otimes\sigma_a)/2\) and \(H_2=\sum_{a=x,y,z}J_a^2\). This is a familiar total-spin Casimir/antiferromagnetic two-spin construction. Write \(|\psi^-\rangle=(|01\rangle-|10\rangle)/\sqrt2\) and \(P_s=|\psi^-\rangle\langle\psi^-|\). Exact algebra yields

\[
H_2=\frac32I_4+\frac12(X\otimes X+Y\otimes Y+Z\otimes Z)=2(I_4-P_s).
\]

Thus \(H_2\succeq0\), with unique eigenvalue zero on \(P_s\) and eigenvalue two on the three-dimensional orthogonal triplet space. For all positive trace-one \(\rho\),

\[
\mathcal S_2(\rho)=\operatorname{Tr}(\rho H_2)=2[1-\operatorname{Tr}(\rho P_s)]\ge0,
\]

with **unique minimizer** \(\rho=P_s\). This action is genuinely state-selective, in contrast to the earlier state-independent commutator cost. It selects a vector with \(\langle Z_i\rangle=0\), \(\langle(mZ_i)^2\rangle=m^2\), and \(\langle X_1X_2\rangle=\langle Y_1Y_2\rangle=\langle Z_1Z_2\rangle=-1\). Given separately supplied ordinary quantum operations on the two factors, its CHSH maximum is \(2\sqrt2\). Nothing about this calculation supplies physical spacelike separation or a clock.

**Stability:** The singlet fidelity is *exactly* \(F_s(\rho)=1-\mathcal S_2(\rho)/2\). The trace distance to \(P_s\) obeys \(D_{\mathrm{tr}}(\rho,P_s)\le\sqrt{\mathcal S_2(\rho)/2}\) by the standard fidelity/trace-distance inequality. For the illustrative white-noise family \(\rho_\epsilon=(1-\epsilon)P_s+\epsilon I_4/4\), \(\mathcal S_2=3\epsilon/2\), \(D_{\mathrm{tr}}=3\epsilon/4\), and the singlet-optimal CHSH settings yield \(2\sqrt2(1-\epsilon)\). This is an exact *algebraic measurement prediction*, not a claimed experiment or evidence of prephysical reality.

**Classical rival with exactly matched Z data:** \(\rho_{\rm cl}=(|01\rangle\langle01|+|10\rangle\langle10|)/2\) has the same four joint Z probabilities as \(P_s\). But \(\operatorname{Tr}(\rho_{\rm cl}H_2)=1\) and \(\langle X_1X_2\rangle=0\). With the particular singlet-optimal CHSH settings, \(\rho_{\rm cl}\) produces \(\sqrt2\), compared with \(2\sqrt2\) for \(P_s\). Thus noncommuting action and observations add mathematical constraints beyond signed Z statistics, **but those structures were independently stipulated**.

## 3. Hard multiplicity and restriction failure

The natural all-size generalization \(H_N=\sum_a(\frac12\sum_{i=1}^N\sigma_a^{(i)})^2\) is permutation invariant and contains no spatial graph. The candidate might try to choose its minimizing state at every \(N\) and claim projective compatibility under restriction. This fails.

- \(N=2\): eigenvalues \(0\) (multiplicity one) and \(2\) (multiplicity three); unique singlet minimum.
- \(N=3\): minimum eigenvalue \(3/4\), multiplicity four; no zero-spin state.
- \(N=4\): eigenvalues \(0\) (multiplicity two), \(2\) (multiplicity nine), and \(6\) (multiplicity five). A zero-action ground state is no longer unique.

Let \(P_{0,4}\) project onto the two-dimensional four-spin zero-total-spin space. The natural permutation-invariant supported state \(\rho_4=P_{0,4}/2\) has the two-spin marginal

\[
\operatorname{Tr}_{3,4}(\rho_4)
=\frac12P_s+\frac16(I_4-P_s)\ne P_s.
\]

Its singlet fraction is \(1/2\), its \(Z_1Z_2\) correlation is \(-1/3\), and its trace distance from the independently selected \(N=2\) minimizer is \(1/2\). The normalized projector on the three-spin minimum also has the **same** two-spin marginal as the symmetric four-spin minimum, a small exact N=3/4 plateau. These formulas were checked by direct 8×8 and 16×16 exact matrices.

A selected four-spin state \(P_s^{(12)}\otimes P_s^{(34)}\) also has zero total-spin action, and its designated (1,2) restriction *does* remain pure singlet. It fails the requirement that **every** pair be so selected; its pairing is an independent source/interaction designation.

**General incompatibility:** a bipartite density matrix \(\rho_{AB}\) that is pure forces any extension to factorize as \(\rho_{ABC}=\rho_{AB}\otimes\rho_C\). Therefore a maximally entangled pure singlet on AB cannot simultaneously be a pure singlet on AC. In particular, no permutation-invariant projective state family with a pure singlet as its two-slot marginal exists beyond two slots. This is a strong monogamy/restriction objection, not a no-go for every nonspatial quantum ontology.

For even \(N\), if \(\rho_N\) is the permutation-invariant normalized projector onto the total-spin-zero sector, then, by \(SU(2)\) and permutation invariance plus \(\langle J_N^2\rangle=0\),

\[
\left\langle\sum_a\sigma_a^{(i)}\sigma_a^{(j)}\right\rangle=-\frac3{N-1}\quad(i\ne j).
\]

Hence its two-factor marginal is a Werner-type mixture with singlet weight

\[
p_s(N)=\frac{N+2}{4(N-1)}: \qquad p_s(2)=1,\ p_s(4)=\frac12,\ p_s(6)=\frac25,\ \lim_{N\to\infty}p_s(N)=\frac14.
\]

The global total-spin constraint remains exactly zero, while a *fixed pair* of internal factors becomes maximally mixed as even \(N\to\infty\). This is an information-location distinction, not a physical mechanism of emergence. Exact all-size state-selection from a single action plus arbitrary finite restriction has still **not** been obtained.

## 4. Stronger operational underidentification: tensor factorization is not primitive

Take the same four-dimensional complex Hilbert space and pure vector \(|\psi^-\rangle\). Choose the unitary \(U\) whose columns are the singlet, \(|00\rangle\), the symmetric \((|01\rangle+|10\rangle)/\sqrt2\), and \(|11\rangle\). Then \(U^\dagger|\psi^-\rangle=|00\rangle\). Define alternative, commuting subalgebras

\[
\mathcal A_1'=U(M_2\otimes I)U^\dagger,\qquad
\mathcal A_2'=U(I\otimes M_2)U^\dagger.
\]

Relative to those new factor algebras, the very same vector state has product-state expectations. Relative to the original accessible factor algebras, it is maximally entangled. This does *not* imply that physical Bell data are subjective: the actual observable operations are different between the two subsystem assignments. It shows that a zero-dimensional mathematical vector and action do not uniquely identify which subalgebras correspond to independently accessible physical subsystems. This is established prior art in **Paolo Zanardi, Virtual Quantum Subsystems**, PRL 87, 077901 (2001), DOI 10.1103/PhysRevLett.87.077901; and **Zanardi, Lidar, Lloyd, Quantum Tensor Product Structures Are Observable Induced**, PRL 92, 060402 (2004), DOI 10.1103/PhysRevLett.92.060402.

The older commutative signed root algebra \(C(\{+m,-m\})\) is incapable by *-homomorphism or its own GNS representation of generating noncommuting Pauli observables as **images of its existing elements**: all source elements commute, so all their representation images commute. An enlarged noncommutative algebra or a separately justified operational reconstruction remains necessary. 

## 5. What is and is not gained

**Gained:** a finite, nonspatial, time-unassigned variational action with an actual unique two-system state selector, a spectral gap, an explicitly Bell-capable quantum minimum, a matched classical signed-data rival, and exact mathematical robustness controls. It is a useful **successful partial construction** and an equally useful falsification target.

**Not gained:** a single universal all-size action/state/restriction law, an explanation for internal multiplicity or pair selection, a derivation of the Pauli/noncommutative algebra, the Born rule, physical measurement accessibility, physical charge, chirality, a physical clock, causal influence, a locally emergent metric, gravitational dynamics, or a physical signal. SU(2) generators and two quantum factors were supplied as internal algebraic structure, not derived from signed magnitude. The singlet action is standard spin physics in a nonspatial interpretation, not claimed as new physical law.

The limiting underidentification controls from the current files remain registered: the original 4-sign law uniquely extends to five and six slots but not seven; the sharp seven-slot distance is 74/945; the infinite distance is 47/216; the Legendre latent examples distinguish arbitrarily high finite orders (at n=4, epsilon=1/2, TV=4/315); the original signed pure quantum completion is not forced by the signed law; singlet vs Z-diagonal state has indistinguishable signed Z outcomes despite different noncommutative data; and the prior tiny higher-order and co-Ising differences are theoretical, not measured anomalies.

## 6. Scientific next tests

A genuine next candidate should specify for each finite abstract collection of internal degrees of freedom an algebra \(\mathcal A_F\), a state space, an action \(S_F\), and physical candidate effects, together with *specified, observable-preserving* restriction maps \(R_{G\to F}\) and a composition law. A minimally necessary consistency test for a preferred minimizer is \(R_{G\to F}(\arg\min S_G)\subseteq\arg\min S_F\). The total-spin example fails this for the natural permutation-invariant minimizers, though selected-pair restrictions can work at the cost of source labels. An information-destroying replacement channel must not be counted as an explanatory refinement merely for commuting algebraic diagrams.

The research should then examine whether any action **independently** selects the operational subalgebras, Born effects, source-sharing equivalence and clock/geometry correspondences. It should compare those predictions with laboratory evidence and established quantum models under identical defined operations. The standard to surpass is not rhetorical ambition or the novelty of notation, but the amount of independently grounded physical structure actually derived.

## 7. Verification and provenance

The accompanying `phase_ii_nonspatial_action_state_selection_verifier_2026-11-08.py` was authored independently of the uploaded scripts and executed in ordinary Python, `-O`, and `-OO`. Every mode passed **67 explicit exact-arithmetic checks** covering the 2-, 3- and 4-site total-spin spectra, singlet selection, classical rival, Bell algebra, eigenprojectors, 4-to-2 failure, matched 3/4 ground-marginal plateau, and transformed tensor-factor algebras. The finite algebraic proofs above, not a successful run count, support general propositions. The latest user-uploaded files were available as parsed source in the conversation, but their specified runtime-mounted paths were not present in this active container; verbatim execution of those uploaded snapshots is **not claimed**. No experimental data or ontological certification is inferred.

**Disposition:** Cross-adversarial competition closed. Phase II continues as explicitly stipulated ontology construction with strict adversarial self-audit. The two-system state-selective action is a valid **conditional partial success** and its all-size restriction failure is equally exact. Retain both, without attaching fundamental physical status to either.
