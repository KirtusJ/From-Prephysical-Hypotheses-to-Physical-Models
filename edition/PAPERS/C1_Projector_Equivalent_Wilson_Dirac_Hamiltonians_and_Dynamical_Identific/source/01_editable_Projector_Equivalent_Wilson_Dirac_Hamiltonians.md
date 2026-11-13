---
title: "Projector-Equivalent Wilson–Dirac Hamiltonians and Dynamical Identification"
author: 'Kirtus Justus \textbullet{} Theoretical Physicist \textbullet{} 23 October 2026\tabularnewline Port Coquitlam, British Columbia, Canada'
date: ''
lang: en
header-includes:
 - \usepackage{microtype}
 - \usepackage{booktabs}
 - \usepackage{longtable}
---

**Abstract.** A strictly positive finite-range scalar deformation of a gapped two-band Wilson–Dirac Hamiltonian leaves the negative-energy band projector, hence the zero-temperature gauge-invariant quasifree state, unchanged while altering the excitation spectrum. We separate that exact state-level degeneracy from the ideal dynamical measurements that distinguish the Hamiltonians. We provide an algebraic three-momentum necessary relation, an arbitrary-six-node degree-restricted harmonic discriminator, and a conditional exact mass-and-deformation reconstruction. Each mathematical assertion has an explicit mass branch, observation class, and boundary condition. The counterexamples concern negative-mass reciprocal branches, higher-harmonic interpolation aliases, uncertain momenta, and finite open-chain truncation.

**Keywords:** Wilson–Dirac operators; occupied-band projectors; inverse spectral problems; finite-range deformations.

## 1. Model and theorem domains

The quasifree-state conventions use the canonical anticommutation relations as developed by Araki [1]. The finite-node identifiability arguments use standard polynomial interpolation [2].

Fix the infinite, translation-invariant one-dimensional two-orbital chain and the common CAR algebra. With $k\in[-\pi,\pi]$ and $m>0$, define

$$
 h_m(k)=\sin k\,\sigma_x+(m+1-\cos k)\sigma_z,\qquad
 E_m(k)=\sqrt{m^2+4(m+1)\sin^2(k/2)}.
$$

Let $g_\epsilon(k)=1+\epsilon\cos k$ with $|\epsilon|<1$, and $h_{m,\epsilon}(k)=g_\epsilon(k)h_m(k)$. The one-particle spectral gap at momentum $k$ is $2g_\epsilon(k)E_m(k)$. Here 'gap' means *interband splitting at a momentum*, not a continuum quantum-field-theoretic mass gap. At $m=0$ the isolated zero-energy fiber is irrelevant to the infinite-chain covariance almost everywhere; a finite discrete zero mode requires an occupation convention.

**Theorem 1 (exact zero-temperature projector equivalence).** For every $m>0$ and $|\epsilon|<1$,

$$ P_{m,\epsilon}(k)=P_m(k)=\frac12\left[I-\frac{h_m(k)}{E_m(k)}\right]. $$

*Proof.* Since $h_m(k)^2=E_m(k)^2I$, multiplication by the strictly positive scalar $g_\epsilon(k)$ changes eigenvalue magnitudes but not eigenspaces or signs. Its Fourier symbol is trigonometric polynomial of degree at most two, so the deformed hopping remains finite range. The two occupied-band projectors coincide pointwise. A gauge-invariant quasifree state is determined by its one-particle covariance, proving identity of every finite-interval restriction and equal-time correlation on a *common, fixed algebra*. $\square$

This theorem does not assert equality of energy measurements whose measuring operator changes with the Hamiltonian, of positive-temperature Gibbs states, or of finite *open-boundary* Hamiltonian projectors. Compression of a full-line spectral projector is not the spectral projector of a truncated open-chain Hamiltonian.

## 2. Ideal dynamics supplies information missing from the projector

For a momentum sector prepared with its lower band occupied and upper band empty, the interband operator $O_k=c_{+,k}^\dagger c_{-,k}+c_{-,k}^\dagger c_{+,k}$ obeys, in the ideal closed model,

$$\langle O_k(t)O_k(0)\rangle=e^{-i\Lambda\,[2g_\epsilon(k)E_m(k)]t/\hbar}.$$

A common unknown positive time-to-energy factor $\Lambda/\hbar$ cancels in ratios of correctly identified angular frequencies. This observation class requires coherent interband access, a common clock, calibrated momentum labels, and a chosen band occupation; the mathematical formula alone does not certify that instrument.

**Theorem 2 (three-momentum necessary relation).** For $m=1$, $k_1=\pi/3$, $k_2=2\pi/3$, and $k_3=\pi$, define $R_{12}=\omega(k_1)/\omega(k_2)$ and $R_{32}=\omega(k_3)/\omega(k_2)$. Then

$$ R_{12}=\sqrt{3/7}\,\frac{1+\epsilon/2}{1-\epsilon/2},\qquad
 R_{32}=\frac{3(1-\epsilon)}{\sqrt7(1-\epsilon/2)},\qquad
 \boxed{\sqrt{21}R_{12}+2\sqrt7 R_{32}=9}. $$

The first ratio is strictly increasing in $\epsilon$, so it identifies $\epsilon$ *inside this fixed-mass family*. The final equality is necessary but not sufficient for membership. For a periodic finite chain the three momenta require chain length divisible by six.

## 3. Finite-degree harmonic extensions

Put $c=\cos k$, $s=m+1>1$, $\lambda>0$, and let the strictly positive deformation be $g(c)=1+bc+tc^2$. The squared positive thermal splitting is

$$ Q(c)=D(c)^2=\lambda^2g(c)^2(s^2+1-2sc). $$

It is a polynomial of degree at most five with leading coefficient $[c^5]Q=-2\lambda^2s t^2$.

**Theorem 3 (six-node discriminator).** At arbitrary six *distinct, exactly known* cosine nodes $c_0,\dots,c_5$,

$$\boxed{\sum_{i=0}^{5}\frac{Q(c_i)}{\prod_{j\ne i}(c_i-c_j)}=-2\lambda^2s t^2.}$$

*Proof.* Lagrange interpolation reconstructs the polynomial $Q$ uniquely and its leading coefficient equals the displayed divided difference. $\square$ It follows that within the specified quadratic-harmonic class the signed statistic vanishes exactly when $t=0$. For $g(c)=\sum_{j=0}^r a_jc^j$, the analogous $(2r+1)$-st divided difference from $2r+2$ distinct nodes is $-2\lambda^2s a_r^2$. Neither theorem rules out unrestricted higher harmonics.

**Theorem 4 (exact six-node injection with a mass-branch condition).** With $s>1$, $g(0)=1$, $g>0$ on $[-1,1]$, and exact $D(c_i)>0$, the six data determine $(m,\lambda,b,t)$ uniquely within the normalized quadratic family.

*Proof.* The interpolated $Q(c)$ has exactly one root of odd multiplicity, $r=(s+s^{-1})/2>1$; if the deformation also vanishes there, that root's multiplicity changes by an even amount and remains odd. The condition $s>1$ fixes $s=r+\sqrt{r^2-1}$. The polynomial $Q/(s^2+1-2sc)$ equals $(\lambda g)^2$, whose strictly positive polynomial square root on the physical interval is fixed; its constant coefficient is $\lambda$, and its remaining coefficients give $b,t$. $\square$

The normalization $g(0)=1$ is indispensable: without it, a common amplitude can move between $g$ and $\lambda$. The branch is indispensable too: $s\mapsto s^{-1}$ and $\lambda\mapsto s\lambda$ leave *all* splittings unchanged, but move $m$ out of the stated positive-mass domain.

## 4. Statistical identifiability is a separate problem

The signed leading-coefficient witness is quadratic in $t$, so its derivative with respect to $t$ vanishes at $t=0$. That does **not** imply that the full six-band occupation data have zero nuisance-profiled local information about $t$: their first-order variation contains momentum functions not spanned by the first-harmonic nuisance directions. The relevant Fisher statement requires independent finite-temperature occupations, correctly labeled bands, a common offset, and the declared parametric model; it does not extend to arbitrary instruments.

For six cosine nodes, the barycentric formula can be ill conditioned for perturbed momentum labels, near-colliding nodes, or finite-error estimates of $Q$. A higher-harmonic polynomial that vanishes at all measured nodes produces an exact, indistinguishable finite-data alias. Thus global *exact* parameter injection in a degree-restricted family is not unrestricted function identification.

**Counterexample 1 (constructive finite-node higher-harmonic alias; counterexample).** Fix a continuous strictly positive deformation $g_0(c)$ on $[-1,1]$ and finitely many distinct sampled nodes $c_1,\ldots,c_M$. Set $H(c)=\prod_{j=1}^M(c-c_j)$ and $g_\tau(c)=g_0(c)+\tau H(c)$. For every nonzero $\tau$ satisfying $|\tau|\|H\|_\infty<\min_{[-1,1]}g_0$, the deformed symbol remains strictly positive and differs away from the sampled nodes, while $g_\tau(c_j)=g_0(c_j)$ for all $j$. Hence every sampled splitting and all equal-time occupied-projector observations coincide, although the unsampled spectral functions differ. This countermodel requires allowing polynomials of degree at least $M$; it does **not** contradict Theorem 3 or Theorem 4 within their declared quadratic-harmonic family. It also does not establish finite-shot indistinguishability under additional off-node measurements.

## 5. Finite-boundary limitation and exact state-relative-entropy bridge

**Finite open-chain counterexample.** Multiplying the full-line symbol by $g_\epsilon$ *before* truncating to seven open sites generally produces distinct negative-energy projectors. At $m=1$, $\epsilon=0.37$, the explicit $14\times14$ open-chain matrices give $\|P_0^{\rm open}-P_{0.37}^{\rm open}\|_{\rm op}\simeq0.0065324543$. The specified finite matrices demonstrate that the full-line projector equivalence need not persist for open-chain spectral projections. The open-chain example distinguishes truncating the symbol from projecting the truncated Hamiltonian.

**Ground-state relative entropy.** On the common infinite-chain CAR algebra and for the same $m>0$, Theorem 1 gives the *same* gauge-invariant quasifree ground state, so their restrictions to every finite interval have relative entropy **exactly zero**. This statement is about comparing $h_m$ with $g_\epsilon h_m$ at the **same mass**. It is not an assertion that the distinct-mass states in another model have zero relative entropy. At positive inverse temperature $\beta$, the one-particle thermal covariance instead depends on the multiplier,
$$ C_{\beta,g}(k)=\tfrac12\Bigl[I-\tanh\!\bigl(\tfrac12\beta g(k)E_m(k)\bigr)\,h_m(k)/E_m(k)\Bigr]. $$
Consequently calibrated thermal observations can distinguish some deformations invisible to zero-temperature projector observations. There is no implied laboratory calibration or physical selection.

## References

1. H. Araki, "On Quasifree States of CAR and Bogoliubov Automorphisms," *Publications of the Research Institute for Mathematical Sciences* **6** (1971), 385–442, doi:10.2977/prims/1195193913.

2. J.-P. Berrut and L. N. Trefethen, "Barycentric Lagrange Interpolation," *SIAM Review* **46** (2004), 501–517, doi:10.1137/S0036144502417715.

## Acknowledgments and AI-assisted research

Kirtus Justus provided research direction, the scientific questions, the supplied mathematical materials, and requirements for critical evaluation. ChatGPT (OpenAI) assisted with mathematical checking, manuscript preparation, and editorial examination. Additional AI systems used in the research program include Claude (Anthropic), Gemini (Google), Grok (SpaceXAI), and DeepSeek (High-Flyer). No particular proof, numerical calculation, or independent review is attributed to those systems without supporting records. AI systems are not listed as authors; responsibility for the submitted scholarly claims rests with the named author. The acknowledgment does not imply endorsement by any AI provider or independent peer review.
