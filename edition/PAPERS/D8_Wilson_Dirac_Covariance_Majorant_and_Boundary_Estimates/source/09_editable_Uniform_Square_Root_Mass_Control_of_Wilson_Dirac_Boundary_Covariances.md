---
title: "Uniform Square-Root-Mass Control of Wilson-Dirac Boundary Covariances"
author: 'Kirtus Justus \textbullet{} Theoretical Physicist \textbullet{} 23 October 2026\tabularnewline Port Coquitlam, British Columbia, Canada'
date: ''
lang: en
header-includes:
 - \usepackage{microtype}
 - \usepackage{booktabs}
 - \usepackage{longtable}
---

## Abstract

For the one-dimensional two-orbital Wilson–Dirac occupied-band projections, we establish a mass-uniform trace-class estimate for the difference of the cross-boundary blocks of the infinite-chain projections compressed to a finite interval. If the interval contains \(L\) cells, the mass is \(m=\mu/L\), and \(\log(1+m)\le 1/4\), then the boundary trace norm is at most \(C\sqrt{\mu}\), for a universal constant \(C\). Consequently, the quasifree interval entropies differ by at most \(2C\sqrt\mu\). The proof uses a Fourier–Laplace/Hankel decomposition, retaining the finite-length square-root weight throughout the branch-point estimates. Combining this with the fixed-\(\mu\) Hilbert–Schmidt continuum theorem shows that the exponent \(1/2\) cannot be increased for a uniform estimate on the boundary trace norm. The entropy-difference limit is not determined by this bound.

## 1. Setting and theorem

Let \(P_m\) be the orthogonal Fourier-multiplier projection on \(\ell^2(\mathbb Z;\mathbb C^2)\) associated with the negative-energy band of

\[
 h_m(k)=\sin k\,\sigma_x+(1+m-\cos k)\sigma_z,
 \qquad P_m(k)=\tfrac12\bigl(I-h_m(k)/E_m(k)\bigr),
\]
\[
 E_m(k)=\sqrt{m^2+4(1+m)\sin^2(k/2)}.
\]

The massless projector \(P_0\) is defined almost everywhere. Let \(\chi_L\) project onto any \(L\) consecutive two-orbital cells, and set
\[
 m=\mu/L>0,\quad \kappa=\log(1+m),\quad
 Z_{L,\mu}=\chi_L(P_m-P_0)(I-\chi_L).
\]

**Theorem 1.** There is a universal finite constant \(C\) such that, for every \(L\ge1\) and \(\mu>0\) satisfying \(0<\kappa\le1/4\),
\[
 \boxed{\|Z_{L,\mu}\|_{S_1}\le C\sqrt{L\kappa}\le C\sqrt\mu.}\tag{1}
\]
For the compressed covariance matrices \(A_L=\chi_LP_m\chi_L\) and \(B_L=\chi_LP_0\chi_L\), on the interval subspace,
\[
 \boxed{|S(A_L)-S(B_L)|\le 2C\sqrt\mu.}\tag{2}
\]
For every fixed \(\mu>0\), the condition on \(\kappa\) holds for all sufficiently large \(L\). The constant does not depend on \(L\) or \(\mu\) in that range.

## 2. Exact Fourier–Laplace representation

Write \(a=e^\kappa=1+m\), and define, for \(t>0\),
\[
 h_\kappa(t)={\bf1}_{t>\kappa}
 \frac{e^{-\kappa/2}}{\sqrt{2(\cosh t-\cosh\kappa)}},
 \qquad h_0(t)=\frac1{2\sinh(t/2)},
\]
\[
 \rho_x(t)=\sinh t\,[h_\kappa(t)-h_0(t)],\qquad
 \rho_z(t)=(e^\kappa-\cosh t)h_\kappa(t)
                -(1-\cosh t)h_0(t).
\]

For \(n\ge1\), the positive-distance Fourier coefficient of \(P_m-P_0\) is
\[
 T_n=-\frac1{2\pi}\int_0^\infty e^{-nt}
       [\rho_z(t)\sigma_z+i\rho_x(t)\sigma_x]dt,
 \qquad T_{-n}=T_n^*.
\tag{3}
\]
This follows by writing \(E_m(k)=e^{\kappa/2}\sqrt{2(\cosh\kappa-\cos k)}\), inserting the Poisson kernel, and taking the cosine/sine Fourier coefficients. In particular the normalized cosine representation is
\[
 \frac1\pi\int_0^\pi\frac{\cos(nk)}{\sqrt{2(\cosh\kappa-\cos k)}}dk
 =\frac1\pi\int_\kappa^\infty\frac{e^{-nt}}{\sqrt{2(\cosh t-\cosh\kappa)}}dt.
\]
All subsequent integrals involve the combination (3), in which the singular massless terms cancel; we do not assign a finite value to the individually divergent massless inverse-energy Fourier transform.

**Derivation of the normalized transform.** For $\kappa>0$ set $g_\kappa(k)=[2(\cosh\kappa-\cos k)]^{-1/2}$. The Poisson kernel identity
\[
\sum_{n\in\mathbb Z}e^{-|n|t}e^{ink}=\frac{\sinh t}{\cosh t-\cos k}
\]
can be integrated against $[2(\cosh t-\cosh\kappa)]^{-1/2}\,dt$ over $t>\kappa$. The substitution $u=\sqrt{2(\cosh t-\cosh\kappa)}$ reduces the resulting integral to
\[
 \int_0^\infty\frac{du}{u^2/2+\cosh\kappa-\cos k}=\pi g_\kappa(k).
\]
Comparison of Fourier coefficients proves the displayed cosine transform. Multiplication by $1+m-\cos k$ or $\sin k$ gives the $z$ and $x$ coefficients in (3). The limit $\kappa\downarrow0$ is taken in these combinations, where the singular terms cancel.


The right and left exterior half-lines each give a matrix-valued Hankel block. Rank-one factorization of \(e^{-t(i+j+1)}\), for \(0\le i<L\), \(j\ge0\), has nuclear norm
\[
 W_L(t)=e^{-t}\frac{\sqrt{1-e^{-2Lt}}}{1-e^{-2t}}.
\tag{4}
\]
Taking the Schatten norm of the \(2\times2\) orbital factor in (3), and accounting for both boundaries, yields the rigorous Bochner-integral estimate
\[
 \|Z_{L,\mu}\|_{S_1}\le\frac2\pi\int_0^\infty
 W_L(t)(|\rho_x(t)|+|\rho_z(t)|)dt.
\tag{5}
\]

## 3. Strengthened finite-length kernel bound

The essential improvement is to keep the finite-\(L\) numerator of (4) instead of prematurely replacing it by one. Because \(1-e^{-2Lt}\le2Lt\) and \(1-e^{-2t}\ge (1-e^{-2})t\) when \(0<t\le1\), there is a universal \(C_0\) such that
\[
 \boxed{W_L(t)\le C_0\sqrt{L/t}\quad(0<t\le1),\qquad
 W_L(t)\le C_0e^{-t}\quad(t\ge1).}\tag{6}
\]
The bound need not be optimal for large \(t\); its small-\(t\) behavior is what retains the \(\sqrt{L\kappa}\) scale.

## 4. Four-region proof

Assume \(0<\kappa\le1/4\). All constants in this section are universal.

**Region I: \(0<t<\kappa\).** The massive density vanishes: \(h_\kappa=0\). Exactly,
\[
 \rho_x=-\cosh(t/2),\qquad \rho_z=\sinh(t/2).
\]
Thus \(|\rho_x|+|\rho_z|\le C_1\), and (6) gives
\[
 \int_0^\kappa W_L(|\rho_x|+|\rho_z|)dt
 \le C_2\sqrt L\int_0^\kappa t^{-1/2}dt
 \le C_3\sqrt{L\kappa}.
\tag{7}
\]

**Region II: \(\kappa<t<2\kappa\).** Elementary bounds on \(\cosh t-\cosh\kappa\), the massive prefactor, and the massless density show
\[
 |\rho_x|+|\rho_z|
 \le C_4\left(1+\frac{t+\kappa}{\sqrt{t^2-\kappa^2}}\right).
\]
Set \(t=\kappa u\) in (6). Then
\[
 \int_\kappa^{2\kappa}W_L(|\rho_x|+|\rho_z|)dt
 \le C_5\sqrt{L\kappa}
 \int_1^2u^{-1/2}\left(1+\frac{u+1}{\sqrt{u^2-1}}\right)du.
\tag{8}
\]
The final integral is finite: its singularity at \(u=1\) is only of order \((u-1)^{-1/2}\). Hence (8) is \(O(\sqrt{L\kappa})\).

**Region III: \(2\kappa<t<1\).** Since \(t\ge2\kappa\), the denominator of \(h_\kappa\) is uniformly comparable with \(t\); the exponential prefactor changes by \(O(\kappa)\) and the denominator by \(O(\kappa^2)\). Consequently,
\[
 |h_\kappa-h_0|\le C_6(\kappa/t+\kappa^2/t^3),
\]
\[
 |\rho_x|\le C_7(\kappa+\kappa^2/t^2),
 \qquad |\rho_z|\le C_7\kappa/t.
\]
Using (6), the region-III integral is bounded by
\[
 C_8\sqrt L\left[
 \kappa\int_{2\kappa}^1t^{-1/2}dt
 +\kappa^2\int_{2\kappa}^1t^{-5/2}dt
 +\kappa\int_{2\kappa}^1t^{-3/2}dt\right]
 \le C_9\sqrt{L\kappa}.
\tag{9}
\]
All exponents have been kept explicit; the potentially difficult lower endpoint contributes only \(O(\sqrt{L\kappa})\).

**Region IV: \(t\ge1\).** The inverse-energy denominators are separated from their singularities and
\[
 |\rho_x|+|\rho_z|\le C_{10}\kappa e^{t/2}.
\]
With \(W_L\le C_0e^{-t}\), the final integral is \(O(\kappa)\), which is \(O(\sqrt{L\kappa})\) for \(L\ge1\) and \(\kappa\le1\).

Adding the estimates (7)–(9) and the fourth region in (5) proves the first assertion of Theorem 1. Finally \(L\log(1+\mu/L)\le\mu\), proving the second inequality in (1).

## 5. Entropy continuity

For any infinite-space orthogonal projector \(P\), let \(X=\chi_LP(I-\chi_L)\) and \(C=\chi_LP\chi_L\) on the interval. Then \(XX^*=C(I-C)\). The singular-value entropy function
\[
 F(s)=h\!\left(\frac{1+\sqrt{1-4s^2}}2\right),
 \quad 0\le s\le\tfrac12,
\]
has derivative
\[
 F'(s)=\frac{4s}{\sqrt{1-4s^2}}
       \operatorname{artanh}\sqrt{1-4s^2},\quad 0\le F'(s)\le2.
\]
Mirsky's singular-value inequality and the scalar Lipschitz bound imply
\[
 |S(A_L)-S(B_L)|\le2\|\chi_L(P_m-P_0)(I-\chi_L)\|_1.
\]
Inserting (1) proves (2).

## 6. Optimality of the trace-norm exponent in the small-mass limit

The exponent in (1) cannot be raised uniformly. This conclusion also uses the separately established fixed-\(\mu\) Hilbert–Schmidt continuum theorem; it does not follow from the four-region upper bound alone.

Indeed, write \(\Delta_L=\chi_L(P_m-P_0)\chi_L\), \(G_L=\chi_L(P_m-P_0)^2\chi_L\). Exact positive compression gives
\[
 \|Z_{L,\mu}\|_2^2
 =\operatorname{Tr}(G_L-\Delta_L^2).
\]
For fixed \(\mu>0\), the full-line Fourier trace and the continuum covariance-distance result in *Hilbert-Schmidt Scaling Limit for Wilson-Dirac Covariances* show
\[
 \lim_{L\to\infty}\|Z_{L,\mu}\|_2^2
 =\Lambda(\mu)=\frac\mu\pi-H(\mu).
\]
The continuum Hilbert–Schmidt scaling function is
\[
 H(\mu)=\frac1{\pi^2}\int_0^1(1-s)\left[
 \mu^2K_0(\mu s)^2+
 \left(\frac1s-\mu K_1(\mu s)\right)^2\right]ds.
\]
The classical small-argument Bessel expansions imply
\[
 K_0(z)=O(1+|\log z|),\qquad
 K_1(z)-z^{-1}=O(z(1+|\log z|)),\quad 0<z\le1,
\]
so \(H(\mu)=O(\mu^2(1+|\log\mu|)^2)=o(\mu)\) as \(\mu\downarrow0\). Therefore
\[
 \lim_{\mu\downarrow0}\frac{\Lambda(\mu)}\mu=\frac1\pi.
\]
Since the nuclear norm dominates the Hilbert–Schmidt norm, we conclude
\[
 \boxed{
 \liminf_{\mu\downarrow0}\liminf_{L\to\infty}
 \frac{\|Z_{L,\mu}\|_1}{\sqrt\mu}
 \ge\frac1{\sqrt\pi}>0.}\tag{10}
\]
Thus no estimate \(\|Z_{L,\mu}\|_1\le C\mu^{1/2+\epsilon}\), for any \(\epsilon>0\), can hold uniformly for all sufficiently large \(L\) and small \(\mu\) in this sequence. **This optimality statement applies to the boundary trace norm, not to the entropy difference.**

## 7. Scope

The proof uses the specific Wilson–Dirac Bloch projectors, a finite interval of consecutive cells, and the mass scaling \(m=\mu/L\). It does not establish uniformity for arbitrary mass sequences or other lattice Hamiltonians. It does not prove convergence of \(S(A_L)-S(B_L)\) as \(L\to\infty\) for a fixed positive \(\mu\). Nor does it establish a proposed finite entropy contribution, a uniform reference-modular spectral approximation, or the full relative-entropy logarithmic coefficient.

The stronger boundary convergence and entropy-difference limit are proved in *Cross-Boundary Trace-Class Estimates for Wilson–Dirac Quasifree States*. The complete leading logarithm is established in *Uniform Bulk Modular Asymptotics and the Leading Wilson Entropy Law*. These are separate arguments. Theorem 1 of *Finite Part of Wilson–Dirac Relative Entropy* combines the boundary limit with modular and nonlinear convergence to obtain the complete fixed-positive-scaled-mass finite part and an $O_\mu(1/\log L)$ remainder. The bound proved in this article alone does not establish that limit.

## References

- NIST Digital Library of Mathematical Functions, Chapter 10, §§10.30–10.31 (modified Bessel limiting forms and power series), https://dlmf.nist.gov/10.30 and https://dlmf.nist.gov/10.31.
- V. Eisler and I. Peschel, “Analytical results for the entanglement Hamiltonian of a free-fermion chain,” *Journal of Physics A* **50** (2017), 284003, https://doi.org/10.1088/1751-8121/aa76b5 (reference spectral context; not a proof of the Wilson bound).
- D. Slepian, “Prolate spheroidal wave functions, Fourier analysis and uncertainty. V: The discrete case,” *Bell System Technical Journal* **57** (1978), 1371–1430, https://doi.org/10.1002/j.1538-7305.1978.tb02104.x (classical concentration framework; not a proof of the Wilson bound).

## Contributors and acknowledgments

Kirtus Justus is the sole named human author. ChatGPT (OpenAI) assisted in deriving and testing the Fourier–Laplace and four-region estimates. Claude (Anthropic), Gemini (Google), Grok (SpaceXAI), and DeepSeek (High-Flyer) are acknowledged for contributions to the wider research program; no unverified theorem-specific contribution is assigned to them.
