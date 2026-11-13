---
title: "Exact Longitudinal Jacobi Moment and Wilson Majorant Mass for a Finite Interval"
author: 'Kirtus Justus (Theoretical Physicist) \textbullet{} 31 October 2026\tabularnewline Port Coquitlam, British Columbia, Canada'
date: ''
lang: en
header-includes:
 - \usepackage{microtype,booktabs,longtable}
 - \setlength{\emergencystretch}{3em}
---

## Abstract

For the occupied-band Wilson–Dirac projection compressed from the infinite lattice to a finite interval of two-orbital cells, we derive closed elliptic expressions for the first Jacobi moment of the longitudinal perturbation and for the total mass of its positive spectral majorant. At fixed scaled mass, the Jacobi moment has an explicitly determined logarithmic coefficient and finite constant. These statements concern the longitudinal operator against the *Jacobi generator*, not against the exact finite reference-modular discrepancy. They do not settle the leading coefficient or the finite part of the complete Wilson relative entropy.

## 1. Definitions and scalar Fourier normalization

Let \(N=2L\) and \(m=\mu/L\) with \(\mu>0\) fixed, and put
\[
 r=\frac{m}{m+2}=\frac{\mu}{N+\mu}\in(0,1),\qquad z=1-r^2.
\]
The reference Jacobi operator on \(\mathbb C^N\) is the real symmetric matrix
\[
 (J_N)_{j-1,j}=(J_N)_{j,j-1}=\frac{j(N-j)}N,\qquad 1\le j<N,
\]
with zero diagonal. The longitudinal Wilson perturbation \(S_N\) is the compression, in the fixed interval-preserving scalar basis, of the full-line operator \(S=G(I-2P_0)\), with \(P_0\) the half-filled occupied-band projection and \(G\) the positive Wilson majorant. The full-line Fourier multiplier is scalar Toeplitz after transformation; its odd scalar displacement coefficients are
\[
 s_d(r)=-\frac1\pi\int_0^{\pi/2}
 \left(1-\frac{\cos\theta}{\sqrt{\cos^2\theta+r^2\sin^2\theta}}\right)
 \cos(d\theta)\,d\theta,\qquad d\text{ odd},
\]
while \(s_d=0\) for even displacement, including \(s_0=0\). This identity follows directly from the full-line Wilson symbol, its positive-majorant factorization and the fixed cellwise scalarization. No finite-open-chain projector is introduced. Let \(\mathbf K(z)\) and \(\mathbf E(z)\) denote complete elliptic integrals with **parameter**, not modulus, \(z\).

## 2. Exact first Jacobi moment

**Theorem 1.** For every even \(N\ge2\) and \(\mu>0\),
\[
\boxed{\operatorname{Tr}(S_NJ_N)=\frac{N^2-1}{3\pi}
 \left[\frac{\mathbf E(1-r^2)-r^2\mathbf K(1-r^2)}{1-r^2}-1\right].}
\tag{1}
\]
At fixed \(\mu>0\), as \(N\to\infty\) along even integers,
\[
\boxed{\operatorname{Tr}(S_NJ_N)
 =-\frac{\mu^2}{6\pi}\log N
 +\frac{\mu^2}{4\pi}-\frac{\mu^2}{6\pi}\log\frac4\mu
 +O_\mu\!\left(\frac{\log N}{N}\right).}
\tag{2}
\]

*Proof.* As \(J_N\) has first off-diagonals only, and \(S_N\) has Toeplitz first off-diagonal \(s_1(r)\),
\[
\operatorname{Tr}(S_NJ_N)=2s_1(r)\sum_{j=1}^{N-1}\frac{j(N-j)}N
 =\frac{N^2-1}{3}s_1(r).
\]
The first coefficient of \(S_N\) is
\[
 s_1(r)=-\frac1\pi\left[1-\int_0^{\pi/2}
 \frac{\cos^2\theta}{\sqrt{1-(1-r^2)\sin^2\theta}}\,d\theta\right].
\]
The elementary identity
\[
\int_0^{\pi/2}\frac{\cos^2\theta}{\sqrt{1-z\sin^2\theta}}\,d\theta
 =\mathbf K(z)-\frac{\mathbf K(z)-\mathbf E(z)}{z}
 =\frac{\mathbf E(z)-(1-z)\mathbf K(z)}{z}
\]
gives (1). As \(r\downarrow0\), standard complete elliptic expansions yield
\[
\mathbf K(1-r^2)=\log\frac4r+O(r^2\log(1/r)),\quad
\mathbf E(1-r^2)=1+\frac{r^2}{2}\left(\log\frac4r-\frac12\right)
 +O(r^4\log(1/r)).
\]
Consequently,
\[
 s_1(r)=\frac{r^2}{\pi}\left(\frac34-\frac12\log\frac4r\right)
 +O(r^4\log(1/r)).
\]
Substitute \(r=\mu/(N+\mu)\) into the finite identity. Since \(N^2r^2=\mu^2+O_\mu(N^{-1})\) and
\(\log(4/r)=\log N+\log(4/\mu)+O_\mu(N^{-1})\), equation (2) follows with the stated remainder. \(\square\)

## 3. Exact mass of the positive Wilson majorant

The full-line positive majorant has the orbital-scalar Bloch multiplier
\[
 G(k)=\frac12g_r(k)I_2,\qquad
 g_r(k)=1-\frac{|\sin(k/2)|}{\sqrt{\sin^2(k/2)+r^2\cos^2(k/2)}}.
\]
Under the interval-preserving scalarization, its diagonal average is unchanged.

**Theorem 2.** For every even \(N\ge2\) and \(\mu>0\),
\[
\boxed{\operatorname{Tr}G_N=N\left[
\frac12-\frac{\arccos r}{\pi\sqrt{1-r^2}}\right].}
\tag{3}
\]
For fixed \(\mu>0\),
\[
\boxed{\operatorname{Tr}G_N=\frac\mu\pi
 -\frac{\mu^2}{N}\left(\frac1\pi+\frac14\right)+O_\mu(N^{-2}).}
\tag{4}
\]

*Proof.* The trace is \(N\) times the zeroth scalar Fourier coefficient of \(G\). By symmetry,
\[
 \frac1N\operatorname{Tr}G_N
 =\frac1\pi\int_0^{\pi/2}
 \left(1-\frac{\sin\theta}{\sqrt{\sin^2\theta+r^2\cos^2\theta}}\right)d\theta.
\]
The first term integrates to \(1/2\). Substitute \(u=\cos\theta\) in the second term to obtain
\[
\int_0^1\frac{du}{\sqrt{1-(1-r^2)u^2}}
 =\frac{\arcsin\sqrt{1-r^2}}{\sqrt{1-r^2}}
 =\frac{\arccos r}{\sqrt{1-r^2}}.
\]
This proves (3). Taylor-expanding \(\arccos r/\sqrt{1-r^2}=\pi/2-r+(\pi/4)r^2+O(r^3)\), and substituting \(r=\mu/(N+\mu)\), proves (4). \(\square\)

**Consequence.** The boundary-corrected modular estimate can retain the actual finite majorant mass:
\[
 2|\operatorname{Tr}(C_NE_N)|
 \le\sqrt{2\operatorname{Tr}G_N}\,\sqrt{\operatorname{Tr}(W_NE_N^2)}.
\]
This sharpens the numerical prefactor in the bound obtained from \(\mu/\pi\) but does not by itself improve the \(O_\mu(\sqrt{\log N})\) bound obtained by this method. The separate weighted theorem in *Uniform Bulk Modular Asymptotics and the Leading Wilson Entropy Law* gives a stronger estimate. The cross-boundary Hilbert–Schmidt leakage is bounded above by \(\tfrac12\operatorname{Tr}G_N\).

## 4. Scope of the modular application

The exact moment identifies the first Jacobi moment of the longitudinal perturbation, not the modular trace \(\operatorname{Tr}(S_NE_N)\). An approximation to \(E_N\) that is valid only for central Jacobi modes cannot be substituted into the full trace without an appropriate uniform, weighted error estimate. The reference-modular estimates in *Uniform Bulk Modular Asymptotics and the Leading Wilson Entropy Law* establish the complete leading law with bounded remainder. Convergence to a finite part still requires further estimates; the moment identity here does not provide them.

The cross-boundary leakage of the positive majorant has an exact fixed-scaled-mass limit, given in *Continuum Limit of the Wilson Majorant Boundary Defect*. The majorant mass and the boundary-leakage norm are different quantities.

## References

- NIST Digital Library of Mathematical Functions, §19.12, complete elliptic integrals near complementary modulus zero. https://dlmf.nist.gov/19.12
- D. Slepian, *Bell System Technical Journal* **57** (1978), 1371–1430. DOI: 10.1002/j.1538-7305.1978.tb02104.x.
- V. Eisler and I. Peschel, *Journal of Physics A* **50** (2017), 284003. DOI: 10.1088/1751-8121/aa76b5.
- K. Justus, *Exact Spectral Majorants for a Wilson–Dirac Interval* (2026).
- K. Justus, *Continuum Limit of the Wilson Majorant Boundary Defect* (2026).

## Contributions and acknowledgments

Kirtus Justus directed the mathematical research and established the publication scope. ChatGPT (OpenAI) derived and checked the elliptic moment and majorant-mass identities and prepared the manuscript. Claude (Anthropic), Gemini (Google), Grok (SpaceXAI), and DeepSeek (High-Flyer) are acknowledged for documented broader participation only, without attributing independent verification of these results to them. No external peer review, experimental validation, or formal proof-assistant verification is claimed.