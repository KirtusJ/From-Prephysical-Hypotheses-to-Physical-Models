---
title: "Exact Reference Occupation Weights and Particle-Hole Pairing"
author: 'Kirtus Justus (Theoretical Physicist) \textbullet{} 31 October 2026\tabularnewline Port Coquitlam, British Columbia, Canada'
date: ''
lang: en
header-includes:
 - \usepackage{microtype}
 - \usepackage{booktabs}
 - \usepackage{longtable}
---

## Abstract

We calculate the total occupation-fluctuation weight of the finite half-filled sine-kernel reference covariance, retaining all finite-size terms, and identify exact particle–hole symmetries relevant to the Wilson–Dirac relative-entropy problem. An explicit harmonic-number/trigamma identity gives the logarithmic growth and its first algebraic corrections. The chiral involution pairs the eigenvalues of the commuting reference Jacobi matrix and the reference covariance and makes the trace of a Wilson positive majorant against every odd reference function vanish. The formula evaluates the half-filled free-fermion number fluctuation with explicit finite-size corrections; the exact symmetries constrain, but do not evaluate, the Wilson longitudinal modular residual.

## 1. Exact finite reference geometry

For even `N=2L`, consider the real symmetric matrix

\[
(B_N)_{ij}=\begin{cases}\tfrac12,&i=j,\\
\dfrac{\sin(\pi(i-j)/2)}{\pi(i-j)},&i\ne j,
\end{cases}\qquad 0\le i,j<N.
\]

The associated irreducible Jacobi matrix has `J_(j-1,j)=J_(j,j-1)=j(N-j)/N`. They commute. Let \(\Gamma_N=\operatorname{diag}(1,-1,1,-1,\ldots,-1)\). Since the off-diagonal entries of \(B_N\) vanish at even nonzero separations, while the nonzero off-diagonal entries connect opposite parities,

\[
\boxed{\Gamma_N B_N\Gamma_N=I-B_N,\qquad\Gamma_N J_N\Gamma_N=-J_N.}\tag{1}
\]

Since \(J_N\) has simple spectrum, each common eigenpair \((\lambda,b)\) of \((J_N,B_N)\) has an exactly paired eigenpair \((-\lambda,1-b)\). In particular, for every odd function \(f\) defined on the spectrum of \(J_N\), \(\Gamma_N f(J_N)\Gamma_N=-f(J_N)\).

Let \(G_N\) denote the positive Wilson majorant obtained by compression of the scalar two-orbital Fourier multiplier \(g_r(k)I_2/2\), after the interval-preserving unitary that produces \(B_N\). Its only nonzero matrix entries connect indices of the same parity; therefore

\[
\boxed{\Gamma_N G_N\Gamma_N=G_N.}\tag{2}
\]

For paired Jacobi eigenvectors \(v,\Gamma_Nv\), their majorant weights are equal:

\[
\langle\Gamma_Nv,G_N\Gamma_Nv\rangle=\langle v,G_Nv\rangle.
\]

Consequently, \(\operatorname{Tr}[G_N f(J_N)]=0\) for every odd \(f\). In particular, define the *exact* reference modular discrepancy

\[
 E_N=\log(I-B_N)-\log B_N+N\eta(J_N/N),
\]

where \(\eta\) is the odd half-filled reference scaling function. Functional calculus gives \(\Gamma_NE_N\Gamma_N=-E_N\), hence the exact cancellation

\[
\boxed{\operatorname{Tr}(G_NE_N)=0.}\tag{3}
\]

This does **not** imply \(\operatorname{Tr}[(A_N-B_N)E_N]=0\): the covariance difference is not \(G_N\). Equation (3) supplies a symmetry check and prevents incorrectly interpreting the majorant's signed first moment as the desired modular term.

## 2. Exact occupation-fluctuation trace

Define

\[
V_N:=\operatorname{Tr}[B_N(I-B_N)]=\sum_{j=1}^N b_j(1-b_j).
\]

**Proposition.** For every even integer \(N\ge2\),

\[
\boxed{V_N=\frac{N}{4}-\frac{2}{\pi^2}
 \sum_{\substack{1\le d<N\\d\ \mathrm{odd}}}\frac{N-d}{d^2}.}\tag{4}
\]

Writing \(H_n=\sum_{k=1}^n1/k\) and \(\psi_1(z)=\sum_{k=0}^\infty(z+k)^{-2}\), equivalently,

\[
\boxed{V_N=\frac2{\pi^2}\Big(H_N-\tfrac12 H_{N/2}\Big)
+\frac{N}{2\pi^2}\psi_1\!\left(\frac{N+1}{2}\right).}\tag{5}
\]

As \(N\to\infty\) along even integers,

\[
\boxed{V_N=\frac1{\pi^2}\left(\log N+\gamma+\log2+1
-\frac{1}{6N^2}+\frac{7}{20N^4}+O(N^{-6})\right).}\tag{6}
\]

*Proof.* The diagonal of \(B_N\) contributes \(N/4\) to \(\operatorname{Tr}B_N-\operatorname{Tr}B_N^2\). At distance \(d\), the two off-diagonals contain \(N-d\) entries each. Their squares vanish for even \(d\) and equal \(1/(\pi^2d^2)\) for odd \(d\). This proves (4).

The classical odd-integer identity \(\sum_{d\ge1,\ d\text{ odd}}d^{-2}=\pi^2/8\) converts the un-cancelled term to a positive exterior tail:

\[
V_N=\frac2{\pi^2}\sum_{\substack{1\le d<N\\d\text{ odd}}}\frac1d
+\frac{2N}{\pi^2}\sum_{\substack{d\ge N\\d\text{ odd}}}\frac1{d^2}.
\]

The first sum equals \(H_N-\tfrac12H_{N/2}\), and the second equals \(\tfrac14\psi_1((N+1)/2)\), proving (5). The Euler–Maclaurin expansions of harmonic numbers and \(\psi_1\), at the displayed half-integer argument, yield

\[
2\Big(H_N-\tfrac12H_{N/2}\Big)=\log N+\gamma+\log2
+\frac1{6N^2}-\frac7{60N^4}+O(N^{-6}),
\]

\[
\frac{N}{2}\psi_1\left(\frac{N+1}{2}\right)
=1-\frac1{3N^2}+\frac7{15N^4}+O(N^{-6}).
\]

Adding these expansions gives (6). All sums and steps are exact until the final asymptotic expansion. \(\square\)

## 3. Consequences for weighted modular estimates

The exact trace fixes the total occupation-fluctuation weight: \(V_N\sim\pi^{-2}\log N\). For any \(\delta\in(0,\frac12)\), the number of reference eigenvalues in \([\delta,1-\delta]\) obeys

\[
\#\{j:b_j\in[\delta,1-\delta]\}\le\frac{V_N}{\delta(1-\delta)}
=O_\delta(\log N).
\]

This elementary counting consequence is not an estimate on the reference modular discrepancy. A stronger sufficient condition for finer reference-modular error estimates would be

\[
\operatorname{Tr}[E_N^2B_N(I-B_N)]
=\sum_j e_j^2b_j(1-b_j)=O((\log N)^{-1}),
\]

uniformly in even \(N\), which (4)–(6) alone do not imply. *Uniform Bulk Modular Asymptotics and the Leading Wilson Entropy Law* supplies the stronger bound \(\operatorname{Tr}[E_N^2B_N(I-B_N)]=O(\log N/N^2)\), using a compact-interior expansion and a global linear logit envelope. The total occupation weight still grows like \(\pi^{-2}\log N\); decay comes from control of the modular errors. The exact particle–hole and majorant cancellations alone do not provide that control.

## References

1. D. Slepian, “Prolate Spheroidal Wave Functions, Fourier Analysis, and Uncertainty—V: The Discrete Case,” *Bell System Technical Journal* **57** (1978), 1371–1430, doi:10.1002/j.1538-7305.1978.tb02104.x.
2. V. Eisler and I. Peschel, “Analytical Results for the Entanglement Hamiltonian of a Free-Fermion Chain,” *Journal of Physics A: Mathematical and Theoretical* **50** (2017), 284003, doi:10.1088/1751-8121/aa76b5.
3. NIST Digital Library of Mathematical Functions, §5.15 (polygamma functions), https://dlmf.nist.gov/5.15.

## Acknowledgments and contributions

Kirtus Justus directs the research program and is the sole named human author. ChatGPT (OpenAI) assisted with the present derivations, implementation checks and drafting. Claude (Anthropic), Gemini (Google), Grok (SpaceXAI), and DeepSeek (High-Flyer) are acknowledged for their wider project participation without unverified attribution to this calculation. The mathematical statements and their supporting derivations are presented for independent scrutiny.
