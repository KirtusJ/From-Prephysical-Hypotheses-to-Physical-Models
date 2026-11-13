---
title: "Conformal Invariance and Sharp Wilson Majorant Boundary Bounds"
author: 'Kirtus Justus (Theoretical Physicist) \textbullet{} 31 October 2026\tabularnewline Port Coquitlam, British Columbia, Canada'
date: ''
lang: en
header-includes:
 - \usepackage{microtype,booktabs,longtable}
 - \setlength{\emergencystretch}{3em}
---

## Abstract

For the scalarized positive Wilson majorant, we establish an exact mass-independent weighted Fourier identity and a uniform bound on finite-interval Hilbert–Schmidt boundary leakage. The proof identifies the majorant symbol at each positive mass parameter with a disk-automorphic composition of one reference symbol and applies conformal invariance of the boundary homogeneous half-Sobolev seminorm. We derive the exact deficit from the saturated boundary energy and its fixed-mass finite-interval asymptotic. For the fixed-scaled-mass continuum leakage function, we determine its exact global supremum and its two leading inverse-power corrections at large scaled mass. The resulting uniform estimate improves the prefactor available in the reference-modular boundary-term bound, but does not settle the longitudinal reference-modular trace or the complete relative-entropy asymptotic.

## 1. Conventions

For a parameter \(r>0\), define the real, even \(2\pi\)-periodic scalar Wilson-majorant symbol

\[
G_r(k)=\frac12\left(1-\frac{|\sin(k/2)|}{\sqrt{\sin^2(k/2)+r^2\cos^2(k/2)}}\right),
\qquad -\pi\le k\le\pi,
\]

with Fourier coefficients

\[
c_d(r)=\frac{1}{2\pi}\int_{-\pi}^{\pi}G_r(k)e^{-idk}\,dk.
\]

In the cell-preserving scalarization of the two-orbital lattice, these coefficients occur at scalar displacements \(2d\). For a scalar interval of even length \(N\) and projection \(\chi_N\), the exact full-line Fourier boundary identity is

\[
\mathcal L_N(r):=\|(I-\chi_N)G_r\chi_N\|_{\mathrm{HS}}^2
=2\sum_{d=1}^\infty\min(N,2d)|c_d(r)|^2.\tag{1}
\]

This identity counts the two directions across the interval boundary and uses the Fourier coefficient normalization above. It is not a statement about an arbitrary two-orbital matrix-valued symbol under a different scalarization.

## 2. Universal weighted Fourier identity

**Theorem 1.** For every \(r>0\),

\[
\boxed{4\sum_{d=1}^\infty d\,|c_d(r)|^2=\frac{1}{2\pi^2}.}\tag{2}
\]

Consequently, for every admissible interval length \(N\),

\[
\boxed{0<\mathcal L_N(r)<\frac{1}{2\pi^2},}\tag{3}
\]

and its exact positive deficit is

\[
\boxed{\frac{1}{2\pi^2}-\mathcal L_N(r)
=2\sum_{d>N/2}(2d-N)|c_d(r)|^2.}\tag{4}
\]

*Proof.* Put \(a=(1-r)/(1+r)\in(-1,1)\), and let

\[
M_a(z)=\frac{z-a}{1-az}, \qquad |z|=1.
\]

Writing \(M_a(e^{ik})=e^{i\psi_r(k)}\), the half-angle identity gives

\[
\tan\frac{\psi_r(k)}2=\frac1r\tan\frac k2.
\]

The formula defining \(G_r\) therefore gives the pointwise boundary identity

\[
G_r(e^{ik})=G_1(M_a(e^{ik})),\qquad
G_1(k)=\tfrac12(1-|\sin(k/2)|).\tag{5}
\]

For a real boundary function \(u\) with Fourier coefficients \(\widehat u_n\), define the homogeneous half-Sobolev energy

\[
\mathcal E(u)=\sum_{n\in\mathbb Z}|n|\,|\widehat u_n|^2
=\frac1{4\pi^2}\int_0^{2\pi}\!\int_0^{2\pi}
\frac{|u(e^{i\theta})-u(e^{i\varphi})|^2}
{|e^{i\theta}-e^{i\varphi}|^2}\,d\theta\,d\varphi.\tag{6}
\]

The identity holds first for trigonometric polynomials, by orthogonality and the Dirichlet-kernel identity, and then by approximation in the homogeneous \(H^{1/2}\) norm. Its normalization can be checked on \(u(e^{ik})=e^{ik}\). A disk automorphism satisfies

\[
|M_a(z)-M_a(w)|^2
=|M_a'(z)|\,|M_a'(w)|\,|z-w|^2,
\quad |z|=|w|=1,
\]

and its boundary angular Jacobian equals \(|M_a'(z)|\). Changing both variables in (6) proves \(\mathcal E(u\circ M_a)=\mathcal E(u)\). This also follows from conformal invariance of the Dirichlet energy of harmonic extensions. In particular, (5) implies \(\mathcal E(G_r)=\mathcal E(G_1)\).

For \(d\ge1\), elementary integration yields

\[
 c_d(1)=-\frac1{2\pi}\int_0^\pi\sin(k/2)\cos(dk)\,dk
=\frac1{\pi(4d^2-1)}.\tag{7}
\]

Since \(G_r\) is real and even, \(\mathcal E(G_r)=2\sum_{d\ge1}d|c_d(r)|^2\). The partial sum at \(r=1\) telescopes:

\[
4\sum_{d=1}^D d|c_d(1)|^2
=\frac4{\pi^2}\sum_{d=1}^D\frac d{(4d^2-1)^2}
=\frac1{2\pi^2}\left(1-\frac1{(2D+1)^2}\right).\tag{8}
\]

Letting \(D\to\infty\) and using invariance gives (2). Comparing (1) with the saturated sum (2) proves (3) and (4); strictness follows because the boundary symbol is not a trigonometric polynomial and hence has nonzero Fourier coefficients at arbitrarily large indices. \(\square\)

## 3. Fixed-parameter finite-interval deficit

**Theorem 2.** For each fixed \(r>0\), as \(N\to\infty\) through even integers,

\[
\boxed{\mathcal L_N(r)
=\frac1{2\pi^2}-\frac{1}{6\pi^2r^2N^2}+o_r(N^{-2}).}\tag{9}
\]

*Proof.* Let \(h_r(k)=2G_r(k)\) for \(0\le k\le\pi\). Its one-sided endpoint derivative is \(h'_r(0)=-1/(2r)\), while \(h'_r(\pi)=0\), and \(h''_r\in L^1(0,\pi)\) at every fixed \(r>0\). Twice integrating the cosine coefficient by parts, then applying the Riemann–Lebesgue lemma, gives

\[
\lim_{d\to\infty}d^2c_d(r)=\frac1{4\pi r}.\tag{10}
\]

Using (4) with \(A=N/2\), the asymptotic (10) is uniform in the tail \(d>A\) as \(A\to\infty\), whence

\[
\begin{aligned}
\frac1{2\pi^2}-\mathcal L_N(r)
&=4\sum_{d>A}(d-A)|c_d(r)|^2\\
&=\frac{1+o_r(1)}{4\pi^2r^2}\sum_{d>A}\frac{d-A}{d^4}\\
&=\frac{1+o_r(1)}{4\pi^2r^2}\left(\frac1{6A^2}+o(A^{-2})\right)
=\frac1{6\pi^2r^2N^2}+o_r(N^{-2}).
\end{aligned}
\]

The asymptotic is for **fixed** \(r\). It must not be used as a uniform approximation when \(r\) depends on \(N\). \(\square\)

## 4. Exact continuum saturation and its large-mass expansion

For \(\mu>0\), set \(r_N=\mu/(N+\mu)\). Define

\[
f(t)=1-\frac{t}{\sqrt{1+t^2}},\qquad
F(x)=\int_0^\infty f(t)\cos(2xt)\,dt.
\]

The continuum boundary-leakage function is

\[
\Phi(\mu)=\frac2{\pi^2}\int_0^\infty\min(\mu,2x)F(x)^2\,dx.\tag{11}
\]

This expression is the fixed-scaled-mass limit of \(\mathcal L_N(r_N)\); its derivation from scaled Fourier coefficients is independent of the conclusions below.

**Theorem 3.** The following weighted transform integral is exact:

\[
\boxed{\int_0^\infty xF(x)^2\,dx=\frac18.}\tag{12}
\]

Consequently,

\[
\boxed{\lim_{\mu\to\infty}\Phi(\mu)=\sup_{\mu>0}\Phi(\mu)=\frac1{2\pi^2}.}\tag{13}
\]

Moreover, as \(\mu\to\infty\),

\[
\boxed{\Phi(\mu)=\frac1{2\pi^2}
-\frac1{6\pi^2\mu^2}-\frac3{10\pi^2\mu^4}
+O(\mu^{-6}).}\tag{14}
\]

*Proof.* We first give a Fourier-analytic derivation of (12) independent of the Möbius argument. Set \(h(t)=(1+t^2)^{-3/2}\) and \(H(k)=\int_0^\infty h(t)\sin(kt)\,dt\). Integration by parts yields \(F(x)=H(2x)/(2x)\) for \(x>0\). A Laplace regularization of the positive quadratic integral gives

\[
\int_0^\infty\frac{H(k)^2}{k}\,dk
=\frac12\int_0^\infty\!\int_0^\infty
h(t)h(s)\log\frac{t+s}{|t-s|}\,dt\,ds.\tag{15}
\]

Indeed, inserting \(e^{-\varepsilon k}\), using the elementary sine-product integral, and taking \(\varepsilon\downarrow0\) yields (15); the logarithmic diagonal singularity is locally integrable against the smooth integrable factors. Substitute \(t=\tan u\), \(s=\tan v\), so that \(h(t)dt=\cos u\,du\) and

\[
\log\frac{t+s}{|t-s|}=\log\frac{\sin(u+v)}{|\sin(u-v)|}.
\]

For \(0<u,v<\pi/2\), the classical logarithmic sine Fourier series, interpreted by Abel summation, gives

\[
\log\frac{\sin(u+v)}{|\sin(u-v)|}
=2\sum_{n=1}^\infty\frac{\sin(2nu)\sin(2nv)}n.
\]

The integrated coefficients are

\[
 a_n=\int_0^{\pi/2}\cos u\sin(2nu)\,du
=\frac{2n}{4n^2-1}.
\]

Abel regularization and the integrability of the logarithmic kernel justify integrating the Fourier series. Therefore

\[
\int_0^\infty\frac{H(k)^2}{k}\,dk
=\sum_{n=1}^\infty\frac{a_n^2}n
=\sum_{n=1}^\infty\frac{4n}{(4n^2-1)^2}=\frac12.\tag{16}
\]

As \(xF(x)^2\,dx=\tfrac14H(k)^2dk/k\) under \(k=2x\), (12) follows. Monotone convergence in (11) gives (13).

For the refined expansion, integration by parts yields

\[
F(x)=\frac1{2x}\int_0^\infty h(t)\sin(2xt)\,dt.
\]

Since \(h(0)=1\), \(h''(0)=-3\), and sufficiently many derivatives of \(h\) are integrable, repeated integration by parts establishes

\[
F(x)=\frac{1}{4x^2}+\frac{3}{16x^4}+O(x^{-6}).\tag{17}
\]

Subtract (11) from (13):

\[
\frac1{2\pi^2}-\Phi(\mu)
=\frac2{\pi^2}\int_{\mu/2}^\infty(2x-\mu)F(x)^2\,dx.\tag{18}
\]

Substituting \(F(x)^2=1/(16x^4)+3/(32x^6)+O(x^{-8})\) into (18), with the remainder uniformly integrable over \(x\ge\mu/2\), gives

\[
\frac1{2\pi^2}-\Phi(\mu)
=\frac1{6\pi^2\mu^2}+\frac3{10\pi^2\mu^4}+O(\mu^{-6}),
\]

which proves (14). \(\square\)

## 5. A uniform modular boundary estimate

Let \(P_0\) be the full-line half-filled reference projector and \(B_N=\chi_NP_0\chi_N\), \(W_N=B_N(I-B_N)\). For any self-adjoint finite reference-modular discrepancy \(E_N\), put

\[
C_N=\chi_N G_r(I-\chi_N)P_0\chi_N.
\]

The Hilbert–Schmidt Cauchy–Schwarz inequality and the full-line projector identity give

\[
2|\operatorname{Tr}(C_NE_N)|
\le 2\sqrt{\mathcal L_N(r)}\,
\sqrt{\operatorname{Tr}(W_NE_N^2)}.
\]

Theorem 1 yields the **uniform** inequality

\[
\boxed{
2|\operatorname{Tr}(C_NE_N)|
\le\frac{\sqrt2}{\pi}\,
\sqrt{\operatorname{Tr}(W_NE_N^2)}.}\tag{19}
\]

This coefficient does not depend on \(r\) or \(N\). Under the separately established estimate \(\operatorname{Tr}(W_NE_N^2)=O(\log N)\), the right-hand side remains \(O(\sqrt{\log N})\). It neither establishes \(\operatorname{Tr}(S_NE_N)=o(\log N)\) nor proves the leading logarithmic coefficient or finite part of the complete Wilson relative entropy.

## 6. Mathematical scope

The exact identity (2) uses the stated scalar symbol and even-displacement scalarization. The fixed-\(r\) asymptotic (9) and fixed-\(\mu\) continuum limit (11) are different limiting operations; (9) is not uniform in a mass parameter shrinking with \(N\). The large-\(\mu\) expansion (14) concerns the continuum function after the finite-interval limit. None of these results addresses the joint sine-kernel/Jacobi moving-index spectrum required for the longitudinal modular estimate.

The separate weighted argument in *Uniform Bulk Modular Asymptotics and the Leading Wilson Entropy Law* establishes the complete leading law with bounded remainder. The local non-implication statements above describe the scope of the conformal method; they do not leave that leading coefficient unresolved.

## References

1. N. Arcozzi, R. Rochberg, E. T. Sawyer, B. D. Wick, *The Dirichlet space: a survey*, **New York Journal of Mathematics** 17A (2011), 45–86, https://arxiv.org/abs/1008.5342. Classical Dirichlet seminorm and conformal invariance.
2. K. Justus, *Fourier-Space Boundary Defects for Wilson–Dirac Covariances* (2026). Exact Fourier compression identity in the relevant scalarization.
3. K. Justus, *Continuum Limit of the Wilson Majorant Boundary Defect* (2026). Scaled-mass Fourier limit and small-mass expansion.
4. K. Justus, *Boundary-Corrected Longitudinal Modular Reduction* (2026). Application to the reference-modular boundary contribution.

## Contributions and acknowledgments

Kirtus Justus directs the research program and is responsible for decisions about scientific adoption and publication. ChatGPT (OpenAI) formulated and checked the conformal-energy argument, Fourier sum rule, and asymptotic consequences as AI-assisted mathematical work. Claude (Anthropic), Gemini (Google), Grok (SpaceXAI), and DeepSeek (High-Flyer) are acknowledged as participants in the broader program; no independent evaluation of these particular results is attributed to them. No external peer review, formal proof-assistant verification, institutional endorsement, or experimental confirmation is claimed.