---
title: "Sharp Logarithmic Jacobi Boundary Moment for a Half-Filled Fermion Interval"
author: 'Kirtus Justus (Theoretical Physicist) \textbullet{} 31 October 2026\tabularnewline Port Coquitlam, British Columbia, Canada'
date: ''
lang: en
header-includes:
 - \usepackage{microtype}
 - \usepackage{booktabs}
 - \usepackage{longtable}
---

## Abstract

For the half-filled sine-kernel covariance on an interval of even length and its commuting tridiagonal concentration operator, we establish the sharp coefficient of the logarithmic weighted second moment. The proof uses an exact full-line boundary-kernel factorization and elementary lattice sums. We also give an exact finite-size expression involving the trigamma function, yielding a second independent route for numerical reconstruction. This result characterizes the size of a reference spectral weight needed in Wilson–Dirac relative-entropy estimates. It does not determine the remaining reference-modular correction and does not establish the complete relative-entropy logarithmic law.

## 1. Definitions and result

Let \(P\) be the orthogonal projection on \(\ell^2(\mathbb Z)\) with real Fourier kernel

\[
T_d=\begin{cases}1/2,&d=0,\\ \sin(\pi d/2)/(\pi d),&d\neq0.\end{cases}
\]

Let \(\chi_N\) be the projection onto sites \(0,\ldots,N-1\), and define \(B_N=\chi_NP\chi_N\) on that interval. Define the Jacobi matrix \(J_N\) by zero diagonal and off-diagonal bonds \(\alpha_j=j(N-j)/N\), \(1\le j<N\), with \(\alpha_0=\alpha_N=0\). Put \(W_N=B_N(I-B_N)\).

**Theorem 1 (sharp second moment).** As even \(N\to\infty\),

\[
\boxed{\operatorname{Tr}(J_N^2W_N)=\frac{\log N}{3\pi^2}+O(1).}
\]

The constant in the \(O(1)\) term is absolute. Consequently, the \(O(\log N)\) scale of this moment cannot be replaced by \(o(\log N)\).

## 2. Exact Fourier boundary formula

Since \(P^2=P\),

\[
 W_N=\chi_NP(1-\chi_N)P\chi_N,\qquad
 \operatorname{Tr}(J_N^2W_N)=\|(1-\chi_N)P\chi_NJ_N\|_{\mathrm{HS}}^2.
\]

For \(0\le j<N\) and \(y\notin[0,N-1]\), the matrix element is

\[
 M_{yj}=\alpha_jT_{y-j+1}+\alpha_{j+1}T_{y-j-1}.
\]

For \(|y-j|=1\), the boundary coefficients make this element zero. For odd separations \(|y-j|\ge3\), both kernel indices are nonzero even integers, so the element again vanishes. For even \(d=y-j\),

\[
 |M_{yj}|^2=\frac{[d(\alpha_j-\alpha_{j+1})-(\alpha_j+\alpha_{j+1})]^2}{\pi^2(d^2-1)^2}.
\]

Reflection about the midpoint of the interval preserves \(J_N\) and the even Fourier kernel \(T_d\); hence the left and right exterior contributions have identical Hilbert–Schmidt norms.

For the left exterior write \(y=-\ell-1\), \(\ell\ge0\), and \(n=j+\ell+1\). Only even \(n\ge2\) contribute, and a direct substitution gives the *exact* numerator

\[
 d(\alpha_j-\alpha_{j+1})-(\alpha_j+\alpha_{j+1})
 = (\ell-j)-\frac{(2j+1)\ell+j}{N}.
\tag{1}
\]

Thus

\[
\operatorname{Tr}(J_N^2W_N)=\frac{2}{\pi^2}
\sum_{\substack{n\ge2\\n\ \mathrm{even}}}
\frac{1}{(n^2-1)^2}
\sum_{j=0}^{\min(n-1,N-1)}
\left[(n-1-2j)-\frac{(2j+1)(n-j-1)+j}{N}\right]^2.
\tag{2}
\]

All terms are nonnegative, and this expression converges absolutely at each fixed \(N\).

## 3. Extracting the logarithm with uniform remainder

For \(2\le n\le N\), let \(u_{n,j}=n-1-2j\) and \(r_{n,j}=[(2j+1)(n-j-1)+j]/N\). Elementary arithmetic gives

\[
\sum_{j=0}^{n-1}u_{n,j}^2=\frac{n(n^2-1)}3,
\qquad |u_{n,j}|\le n,\qquad |r_{n,j}|\le\frac{3n^2}{N}.
\]

Using \((n^2-1)^2\ge 9n^4/16\) for \(n\ge2\), the absolute difference between the terms from \((u-r)^2\) and from \(u^2\), after division by \((n^2-1)^2\), is bounded by \(C(1/N+n/N^2)\) for a universal constant \(C\). Its sum over even \(2\le n\le N\) is \(O(1)\).

For \(n>N\), at most \(N\) values of \(j\) contribute. Here \(0\le j<N\) and \(\ell=n-1-j\), and the numerator in (1) is bounded in absolute value by \(5n\). Hence the tail contributes at most

\[
 C N\sum_{n>N}n^{-2}=O(1).
\]

The two exterior sides together therefore give

\[
 \operatorname{Tr}(J_N^2W_N)
 =\frac{2}{3\pi^2}\sum_{\substack{2\le n\le N\\ n\ \mathrm{even}}}\frac{n}{n^2-1}+O(1).
\]

Writing \(N=2M\) and telescoping the partial fractions yields

\[
\sum_{\substack{2\le n\le N\\n\ \mathrm{even}}}\frac{n}{n^2-1}
=\frac12\sum_{k=1}^{M}\left(\frac1{2k-1}+\frac1{2k+1}\right)
=\frac12[H_N+H_{N+1}-H_{N/2}-1]
=\frac12\log N+O(1).
\]

This proves Theorem 1. \(\square\)

## 4. Exact finite-size evaluation with trigamma functions

Equation (2) also has a one-dimensional special-function form. For \(0\le j<N\), define

\[
 k_j=\left\lceil\frac{j+1}{2}\right\rceil,\quad
 a_j=1-\frac{2j+1}{N},\quad
 b_j=-(2j+1)+\frac{2j^2+2j+1}{N}.
\]

(The symbol \(b_j\) in this section denotes a polynomial coefficient, **not** a reference occupation number.) Put

\[
 C_j^- =\frac14\psi_1(k_j-\tfrac12),\qquad
 C_j^+=\frac14\psi_1(k_j+\tfrac12),\qquad
 D_j=\frac1{2k_j-1},
\]

\[
 U_j=\frac{C_j^-+C_j^+-D_j}{4},\qquad
 V_j=\frac{C_j^--C_j^+}{4},\qquad
 R_j=\frac{D_j}{2}+U_j.
\]

Then the following identity is exact for every positive even \(N\):

\[
\boxed{\operatorname{Tr}(J_N^2W_N)=\frac2{\pi^2}
\sum_{j=0}^{N-1}\bigl(a_j^2R_j+2a_jb_jV_j+b_j^2U_j\bigr).}
\tag{3}
\]

Indeed, at fixed \(j\), the numerator in (2) equals \(a_j n+b_j\), with even \(n\ge j+1\). The three series \(\sum n^2/(n^2-1)^2\), \(\sum n/(n^2-1)^2\), and \(\sum 1/(n^2-1)^2\) evaluate respectively to \(R_j,V_j,U_j\) by partial fractions and the trigamma series. Formula (3) gives an independent finite-size reconstruction, without finite-matrix products or a Fourier quadrature cutoff.

## 5. Consequence and limitation for the Wilson relative-entropy problem

The known Wilson nonlinear correction may be bounded by pairing its transverse covariance component with a reference spectral weight containing \(\operatorname{Tr}(J_N^2W_N)\). Theorem 1 shows this moment is intrinsically logarithmic, not bounded. Thus the older second-moment-only Cauchy–Schwarz estimate gives \(O_\mu(\sqrt{\log N})\), but the second moment alone cannot justify an improved scale. The separate *Fourth-Moment Control of the Wilson Nonlinear Correction*, sections 2–4, combines this moment with a positive fourth-moment bound to obtain a vanishing transverse contribution $O_\mu(\sqrt{(\log N)/N})$ and a bounded full nonlinear term. The nonlinear finite constant is obtained by Theorem 7 of *Finite Part of Wilson–Dirac Relative Entropy*. Theorem 6 of *Uniform Modular Control and Nonlinear Convergence for Wilson–Dirac Intervals* improves the error to $O_\mu(\sqrt{(\log N)/N})$. This uses all-degree path control in addition to the moment bound proved here.

The separate term $\mathcal F_L=\operatorname{Tr}[(A_N-B_N)E_N]$ is bounded by the weighted theorem in *Uniform Bulk Modular Asymptotics and the Leading Wilson Entropy Law*. Together with the bounded nonlinear and entropy terms, that result establishes the complete leading law at fixed positive scaled mass. Neither the boundary moment alone nor equation (3) supplies this modular estimate. The complete fixed-positive-scaled-mass finite part and its $O_\mu(1/\log L)$ remainder are Theorem 1 of *Finite Part of Wilson–Dirac Relative Entropy*, using the separate modular, nonlinear and boundary estimates. The boundary moment alone does not imply them.

## Literature

1. D. Slepian, “Prolate spheroidal wave functions, Fourier analysis, and uncertainty. V: The discrete case,” *Bell System Technical Journal* **57** (1978), 1371–1430. https://doi.org/10.1002/j.1538-7305.1978.tb02104.x.
2. V. Eisler and I. Peschel, “Analytical results for the entanglement Hamiltonian of a free-fermion chain,” *Journal of Physics A: Mathematical and Theoretical* **50** (2017), 284003. https://doi.org/10.1088/1751-8121/aa76b5.

## Contributors and contributions

Kirtus Justus directed the research and is the sole human author. ChatGPT (OpenAI) assisted with derivations, computations and drafting. Claude (Anthropic), Gemini (Google), Grok (SpaceXAI), and DeepSeek (High-Flyer) are acknowledged for broader program participation, without unsupported attribution to this proof. No external peer review or institutional endorsement is claimed.
