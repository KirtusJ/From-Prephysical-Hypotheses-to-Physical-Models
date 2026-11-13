---
title: "Clock-Scale Ambiguity, Static CAR States, and Gibbs Modular Equivalence"
author: 'Kirtus Justus \textbullet{} Theoretical Physicist \textbullet{} 23 October 2026\tabularnewline Port Coquitlam, British Columbia, Canada'
date: ''
lang: en
header-includes:
 - \usepackage{microtype}
---

**Abstract.** A time-translation representation determines evolution with respect to a chosen parameter but does not identify an externally calibrated physical time unit. In a bounded two-band fermionic model, multiplying a Bloch Hamiltonian by a strictly positive measurable scalar preserves its zero-temperature occupied projector, while specified dynamical or thermal observations can distinguish the resulting models. We prove a calibrated-parameter derivative identity and a finite-dimensional Gibbs/modular equivalence theorem with explicit sign conventions. These are exact mathematical statements, not claims that an experimental calibration or physical time standard has been implemented.

**Keywords:** time-translation parameter; CAR quasifree state; band projector; Gibbs state; modular automorphism; identifiability.

## 1. Assumptions and conventions

Let $\mathcal H=\ell^2(\mathbb Z;\mathbb C^2)$, with Fourier variable $k\in[-\pi,\pi]$. For $m\ge0$ define the bounded self-adjoint Bloch multiplier

$$h_m(k)=\sin k\,\sigma_x+(m+1-\cos k)\sigma_z,\qquad E_m(k)=\sqrt{m^2+4(m+1)\sin^2(k/2)}.$$

The negative-band covariance is $P_m=\mathbf 1_{(-\infty,0)}(H_m)$, using the *strictly negative* spectral convention. At $m=0$, the sole zero is at $k=0$, a set of measure zero for the full-chain Fourier multiplier. Gauge-invariant quasifree states are taken on one fixed CAR algebra, and measurements of varying Hamiltonians are not identified with measurements of one fixed observable [1].

## 2. Continuous additive changes of the time parameter

**Proposition 1 (positive linear rescaling).** Let $t:\mathbb R\to\mathbb R$ be continuous, additive, nonconstant and orientation-preserving. Then there is a unique $\tau_0>0$ such that $t(s)=\tau_0 s$. If $G$ is self-adjoint, $U(s)=e^{-isG}$, and one chooses the physical-time convention $U(s)=e^{-it(s)H_{\mathrm{phys}}/\hbar}$, then one possible generator convention is

$$H_{\mathrm{phys}}=\frac{\hbar}{\tau_0}G.$$

Any additive scalar shift of the Hamiltonian leaves adjoint automorphisms unchanged. Uniqueness *up to* an additive scalar requires sufficiently complete observable access, for example the full algebra $B(\mathcal H)$ or an irreducibly represented observable algebra. On a proper observable subalgebra, further generator ambiguities may arise. The translation group law does not determine $\tau_0$.

*Proof.* Additivity gives $t(q)=q t(1)$ for every rational $q$, and continuity extends this equality to every real $s$. Orientation preservation and nonconstancy imply $t(1)>0$. Substitution establishes the asserted unitary realization. Multiplying the unitary family by a scalar phase does not alter its adjoint action on observables. For a proper algebra, consider $\mathcal H=\mathbb C^2\otimes\mathbb C^2$ and $\mathcal A=B(\mathbb C^2)\otimes I$. The generators $G_1=\sigma_z\otimes I$ and $G_2=\sigma_z\otimes I+I\otimes\sigma_z$ induce identical adjoint automorphisms of every $A\in\mathcal A$, although $G_2-G_1$ is not scalar. This explicitly shows why the observable algebra must be specified when claiming generator uniqueness. $\square$

This is a statement about admissible parameter identifications, not a measured definition of a clock. Metrological calibration additionally concerns indications, measurement standards and associated uncertainties [2].

## 3. Exact invariance of zero-temperature state data

**Proposition 2 (positive scalar multipliers).** Suppose $a(k)$ is bounded, real, measurable and strictly positive almost everywhere. Let $\widetilde H_m$ be the Fourier multiplier with symbol $a(k)h_m(k)$. Then

$$\mathbf1_{(-\infty,0)}(\widetilde H_m)=P_m.$$

Consequently the corresponding gauge-invariant quasifree states, all their finite-interval restrictions and all expectations of *fixed* CAR observables coincide.

*Proof.* Almost everywhere, $h_m(k)$ and $a(k)h_m(k)$ have the same eigenvectors and the same eigenvalue signs. Their negative spectral projections are therefore identical almost everywhere, proving equality as decomposable bounded operators. Equality of the one-particle covariance fixes all gauge-invariant quasifree correlations by the CAR/Wick prescription [1]. Restriction to any fixed subalgebra preserves equality. $\square$

The multiplier may vary with momentum and therefore need not represent a change of time units. The proposition does not assert equality of finite **open-chain** ground-state projectors obtained by truncating the Hamiltonians, nor equality of thermal states at fixed inverse temperature. At a finite-dimensional zero eigenspace, any separate convention for occupation of zero modes must be kept fixed. Negative scaling has no analogous projector-invariance property.

For example, $a(k)=1+\frac35\cos k$ is bounded below by $\frac25$ and changes the one-particle dispersion while keeping the occupied projector. This yields a finite-range deformation, not a physical-scale identification.

## 4. An ideal calibrated two-time observable

Fix a positive rate $\gamma$ and define the annihilation-operator Heisenberg convention so that the associated one-particle evolution is $e^{-i\gamma H_m t}$. In the quasifree ground state, write the on-site vacancy correlation matrix as

$$F_{\gamma}(t;0)=\frac1{2\pi}\int_{-\pi}^{\pi}e^{-i\gamma h_m(k)t}(I-P_m(k))\,dk,$$

and set $f_\gamma(t)=\operatorname{tr}_{\mathbb C^2}F_{\gamma}(t;0)$.

**Proposition 3 (ideal generator-rate identification).** For each fixed finite $m\ge0$,

$$f_\gamma(0)=1,\quad f_\gamma'(0)=-i\gamma\overline E_m,\quad
\overline E_m=\frac1{2\pi}\int_{-\pi}^{\pi}E_m(k)\,dk>0.$$

Hence, for the specifically defined ideal observable and a calibrated time variable, $\gamma=i f_\gamma'(0)/\overline E_m$. At $m=0$, $\overline E_0=4/\pi$.

*Proof.* Except at the measure-zero band crossing when $m=0$, $I-P_m(k)$ is the rank-one positive-energy spectral projection. Therefore $f_\gamma(t)=(2\pi)^{-1}\int e^{-i\gamma E_m(k)t}dk$. Since $E_m$ is bounded, differentiation under the integral is legitimate and gives the first two equalities. For $m=0$, $E_0(k)=2|\sin(k/2)|$, whose average equals $4/\pi$. $\square$

This identity presupposes the specified preparation, observable and calibrated physical-time argument. The mathematics does not show that a device can prepare the state or measure this complex correlation with the necessary precision. If $m$ is unknown, the derivative identifies only the product $\gamma\overline E_m$ until another observation determines $m$.

## 5. Finite Gibbs states and the sign of modular evolution

**Proposition 4 (finite Gibbs equivalence).** Let $H,H'$ be finite-dimensional self-adjoint many-body Hamiltonians and $\beta,\beta'>0$. Define the faithful normalized density matrices

$$\rho=Z^{-1}e^{-\beta H},\qquad \rho'=(Z')^{-1}e^{-\beta'H'}.$$

With $\sigma_s(A)=\rho^{is}A\rho^{-is}$ and $\alpha_t(A)=e^{itH/\hbar}Ae^{-itH/\hbar}$, one has

$$\sigma_s=\alpha_{-\hbar\beta s}.$$

Moreover $\rho=\rho'$ if and only if $\beta H-\beta'H'=cI$ for some real scalar $c$.

*Proof.* The scalar normalization $Z$ cancels from $\rho^{is}A\rho^{-is}$, leaving $e^{-i\beta sH}Ae^{i\beta sH}$. The normalized faithful Gibbs matrices are equal exactly when their principal self-adjoint logarithms are equal. Thus $-\beta H-(\log Z)I=-\beta'H'-(\log Z')I$, which is equivalent to the stated scalar-identity relation. Conversely that relation makes the normalized exponentials equal. $\square$

For a finite *number-conserving free-fermion grand-canonical Gibbs state at fixed chemical-potential convention*, the one-particle covariance is $C=(I+e^{\beta h})^{-1}$; when $0<C<I$, its logit determines the dimensionless one-particle generator. This does not identify a separately calibrated physical Hamiltonian, and it is not a formula for an arbitrary interacting Gibbs state or an arbitrary compressed infinite-volume thermal covariance. Adding a scalar to the full many-body $H$ differs from adding a scalar to one-particle $h$, which shifts the many-body number operator under second quantization.

## 6. Scope of the results

The four propositions establish exact equivalences or inversion identities under explicitly declared assumptions. They do not identify a physical clock, establish a new model of time, or promote conditional infinite-volume estimates into theorems. In particular, the equality of static projectors is logically independent of the estimates needed to compare distinct-mass relative entropies.

## References

1. H. Araki, "On Quasifree States of CAR and Bogoliubov Automorphisms," *Publications of the Research Institute for Mathematical Sciences* **6** (1970/71), 385–442, doi:10.2977/PRIMS/1195193913.
2. JCGM, *International Vocabulary of Metrology*, §2.39, "calibration," https://jcgm.bipm.org/vim/en/2.39.html.

## Acknowledgments and AI-assisted research

Kirtus Justus supplied research direction, mathematical materials, and requirements for rigorous scrutiny. ChatGPT (OpenAI) assisted in drafting and checking proofs, examining external references, preparing computational tests and editing this manuscript. Claude (Anthropic), Gemini (Google), Grok (SpaceXAI), and DeepSeek (High-Flyer) are acknowledged for participation in the broader research program; no particular new proof or numerical result is attributed to them without supporting documentation. These acknowledgments do not imply institutional endorsement or external peer review. The named human author assumes responsibility for the scholarly content.
