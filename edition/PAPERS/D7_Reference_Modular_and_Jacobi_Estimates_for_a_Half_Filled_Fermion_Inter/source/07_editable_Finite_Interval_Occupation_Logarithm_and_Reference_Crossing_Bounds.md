---
title: "Finite-Interval Occupation Logarithm and Reference-Crossing Bounds"
author: 'Kirtus Justus (Theoretical Physicist) \textbullet{} 31 October 2026\tabularnewline Port Coquitlam, British Columbia, Canada'
date: ''
lang: en
header-includes:
 - \usepackage{microtype,booktabs,longtable}
 - \setlength{\emergencystretch}{3em}
---

## Abstract

We establish a sharp scalar occupation-logarithm inequality, an explicit logarithmic envelope for the half-filled sine-kernel crossing nuclear norm, and finite-dimensional trace consequences for Wilson–Dirac interval covariances. An elementary change of variables and a two-region majorization yield an explicit crossing bound with leading coefficient one-half in its logarithmic integral estimate. Weighted Hilbert–Schmidt geometry gives a companion inequality for the reference modular discrepancy. These inequalities refine the constants in a directional positive-modular-trace enclosure and a transverse reference estimate. The Wilson positive reference-modular trace asymptotic requires the separate weighted argument of *Uniform Bulk Modular Asymptotics and the Leading Wilson Entropy Law*.

## 1. Reference operators and hypotheses

Let \(N=2L\ge2\) be even. Denote by \(B_N\) the half-filled sine-kernel compression, \(J_N\) its commuting Jacobi operator, and

\[
W_N=B_N(I-B_N),\qquad
K_N=\log(I-B_N)-\log B_N,\qquad
E_N=K_N+N\eta(J_N/N).
\]

The finite spectrum of \(B_N\) lies strictly in \((0,1)\), and \(B_N\) and \(J_N\) commute. For the longitudinal and positive-majorant operators \(S_N,G_N\), use the Wilson full-line relations

\[
0\le2G\le I,\quad [G,P_0]=0,\quad S=G(I-2P_0)
\]

and their interval compressions. The finite particle–hole staggering \(D\) satisfies
\(DB_ND=I-B_N\), \(DG_ND=G_N\), \(DS_ND=-S_N\).
In this geometry the finite even-dimensional reference has no occupation eigenvalue \(1/2\).

Write
\[
M_N=\operatorname{Tr}G_N,
\quad M_{2,N}=\operatorname{Tr}(W_NJ_N^2),
\quad T_{K,N}=\operatorname{Tr}(W_NK_N^2).
\]

The Wilson-majorant and reference results used below are the finite mass identity
\[
M_N=N\left[\frac12-\frac{\arccos r}{\pi\sqrt{1-r^2}}\right],\qquad
r=\frac{\mu}{N+\mu},\qquad M_N\le\frac\mu\pi,
\]

and the reference estimates
\[
\operatorname{Tr}\sqrt{W_N}\le\frac2\pi I_N,
\quad I_N=\int_0^\infty
\frac{e^{-t}\sqrt{1-e^{-2Nt}}}{1-e^{-2t}}\,dt,
\quad M_{2,N}\le\frac{32}{\pi^2}(H_N+1),
\]

where \(H_N=\sum_{j=1}^N j^{-1}\). These imported Wilson-specific inputs require their own separately established proofs; no step below substitutes an external classical reference for them.

## 2. Optimal occupation-logarithm constant

**Theorem 1.** There is a unique \(x_*>0\) with \(x_*\tanh x_*=2\). The best universal constant in

\[
b(1-b)\log^2\!\frac{1-b}{b}\le C_{\log}\sqrt{b(1-b)},\qquad 0<b<1,
\]

is
\[
\boxed{C_{\log}=\frac{2x_*^2}{\cosh x_*}
=2.128888313309637149248092075357476\ldots.}
\]

*Proof.* With \(x=\tfrac12|\log((1-b)/b)|\), the ratio of the left side to \(\sqrt{b(1-b)}\) is \(2x^2/\cosh x\). Its derivative has sign \(2-x\tanh x\). The latter expression changes sign exactly once because \(x\tanh x\) is strictly increasing from zero to infinity. The ratio vanishes at both endpoints of the \(x\)-axis, and the unique maximum is attained by the two particle–hole conjugate occupations. \(\square\)

Therefore, by the spectral theorem,
\[
\boxed{T_{K,N}\le C_{\log}\operatorname{Tr}\sqrt{W_N}.}\tag{1}
\]

## 3. Explicit reference-crossing integral

**Theorem 2.** For every integer \(N\ge2\),
\[
\boxed{I_N\le F_N:=
\operatorname{arsinh}\sqrt{N-1}+\sqrt N\arcsin(N^{-1/2}).}\tag{2}
\]

In particular,
\[
F_N=\tfrac12\log N+1+\log2+O(N^{-1}).\tag{3}
\]

*Proof.* Set \(u=e^{-2t}\) in the defining integral to obtain the exact identity
\[
I_N=\frac12\int_0^1\frac{\sqrt{1-u^N}}{\sqrt u(1-u)}\,du.
\]
Let \(a=1-N^{-1}\). On \((0,a)\), \(\sqrt{1-u^N}\le1\). On \((a,1)\), Bernoulli's inequality \(u^N\ge1-N(1-u)\) gives \(\sqrt{1-u^N}\le\sqrt{N(1-u)}\). Consequently,
\[
\begin{split}
I_N&\le\frac12\int_0^a\frac{du}{\sqrt u(1-u)}
+\frac{\sqrt N}2\int_a^1\frac{du}{\sqrt{u(1-u)}}\\
&=\operatorname{artanh}\sqrt{1-N^{-1}}
+\sqrt N\arcsin(N^{-1/2})\\
&=F_N.
\end{split}
\]
Expanding the two elementary functions at large \(N\) gives (3). \(\square\)

For a completely explicit comparison with a logarithmic envelope, note that
\(\operatorname{arsinh}\sqrt{N-1}\le\tfrac12\log N+\log2\), and the function \(\arcsin x/x\) is increasing for \(0<x<1\). Consequently, for \(N\ge2\),
\[
F_N\le\tfrac12\log N+\log2+\frac{\pi}{2\sqrt2}
<\frac{\log N+2\sqrt2+e^{-1}}{1-e^{-2}}.
\]
The displayed inequalities are uniform in \(N\) and do not claim optimality of the integral majorant.

**Corollary 3.** Every finite interval satisfies
\[
\operatorname{Tr}\sqrt{W_N}\le \frac{2F_N}{\pi},\qquad
T_{K,N}\le\frac{2C_{\log}F_N}{\pi}.\tag{4}
\]

This does not assert asymptotic equality; the upper bound carries no inferred lower-bound coefficient.

## 4. Directional Wilson positive-trace enclosure

Let \(P_N=\operatorname{Tr}(G_N|K_N|)\). The full-line projector relations give \(0\le G+S\le2G\) and \(G+S\le I-P_0\), and the inequalities persist under interval compression. For a reference eigenvector with occupation \(b>1/2\), denote \(q=\langle v,G_Nv\rangle\) and \(s=\langle v,S_Nv\rangle\). Then \(u=q+s\) obeys \(0\le u\le2q\) and \(u\le1-b\). Particle–hole pairing yields
\[
P_N-\operatorname{Tr}(S_NK_N)
=2\sum_{b_j>1/2}u_j|k_j|\ge0.
\]
Since \(u_j\le\sqrt{2q_j(1-b_j)}\), \(\sum_{b_j>1/2}q_j=M_N/2\), \(b_j\ge1/2\), and \(T_{K,N}=2\sum_{b_j>1/2}b_j(1-b_j)k_j^2\), Cauchy–Schwarz proves
\[
\boxed{0\le P_N-\operatorname{Tr}(S_NK_N)
\le U_N:=2\sqrt{M_NT_{K,N}}.}\tag{5}
\]

**Corollary 4 (fully explicit error).** With \(C_{\log}\) from Theorem 1 and \(F_N\) from Theorem 2,
\[
\boxed{U_N\le U^{\mathrm{elem}}_{N,\mu}
:=2\sqrt{\frac{2C_{\log}M_NF_N}{\pi}}.}\tag{6}
\]

For fixed positive \(\mu\), the bound has the asymptotic upper-envelope behavior
\[
U^{\mathrm{elem}}_{N,\mu}
=\frac2\pi\sqrt{C_{\log}\mu\log N}\,[1+o(1)].\tag{7}
\]

The factor \(O(\sqrt{\log N})\) is not improved to \(O(1)\). Combining (5) with the independently proved cubic Jacobi envelope gives, with \(C_\eta=16\operatorname{arsinh}(1)-4\pi\), \(a_\mu=\sqrt{2/15}\,\mu^2/\pi\), \(b_\mu=\mu/(3\pi)\),
\[
V_{N,\mu}=C_\eta\left(\frac{3a_\mu}8+\frac{3b_\mu}{2N}\right),
\]

\[
\boxed{
P_N+\pi\operatorname{Tr}(S_NJ_N)-U^{\mathrm{elem}}_{N,\mu}-V_{N,\mu}
\le\operatorname{Tr}(S_NE_N)
\le P_N+\pi\operatorname{Tr}(S_NJ_N)+V_{N,\mu}.}\tag{8}
\]

## 5. Weighted reference-modular variance

Let \(A_\eta=4\operatorname{arsinh}(1)\), so the established scaling-function bound is \(|\eta(t)|\le A_\eta|t|\) for \(|t|\le1/2\). Because \(B_N,J_N\), and their functions commute, the weighted Hilbert–Schmidt triangle inequality gives
\[
\begin{split}
\sqrt{\operatorname{Tr}(W_NE_N^2)}
&=\|\sqrt{W_N}(K_N+N\eta(J_N/N))\|_2\\
&\le\sqrt{T_{K,N}}
+\sqrt{\operatorname{Tr}\{W_N[N\eta(J_N/N)]^2\}}\\
&\le\sqrt{C_{\log}\operatorname{Tr}\sqrt{W_N}}
+A_\eta\sqrt{M_{2,N}}.
\end{split}
\]

**Corollary 5.** Consequently,
\[
\boxed{\sqrt{\operatorname{Tr}(W_NE_N^2)}
\le\sqrt{\frac{2C_{\log}F_N}{\pi}}
+\frac{4\sqrt2 A_\eta}{\pi}\sqrt{H_N+1}.}\tag{9}
\]

The established transverse pairing estimate \(|\langle v_j,D_Nv_j\rangle|\le2\sqrt{q_jb_j(1-b_j)}\) now gives
\[
\boxed{\left|\operatorname{Tr}(D_NE_N)\right|
\le2\sqrt{M_N}\left[
\sqrt{\frac{2C_{\log}F_N}{\pi}}
+\frac{4\sqrt2 A_\eta}{\pi}\sqrt{H_N+1}
\right].}\tag{10}
\]

Both results are still \(O_\mu(\sqrt{\log N})\). They rely on the Wilson pairing, crossing and second-moment theorems, not on a pointwise finite-size approximation of individual modular eigenvalues.

## 6. Scientific scope

The leading-order Wilson reduction and the exact Jacobi first moment imply the reformulation
\[
\mathcal D_L(\mu)=P_N+\frac{\mu^2}4-\frac{\mu^2}6\log\frac8\mu
+O_\mu(\sqrt{\log N}),\qquad N=2L.
\]
The finite-dimensional bounds here do not determine the limit of \(P_N/\log N\). The separate leading entropy law of *Uniform Bulk Modular Asymptotics and the Leading Wilson Entropy Law*, combined with the positive-trace reduction above, establishes
\[
\boxed{P_N=\frac{\mu^2}6\log N+o_\mu(\log N).}
\]
The estimates established here concern occupation sums and reference crossing. The finite-part limit and uniform modular bound are established in *Finite Part of Wilson–Dirac Relative Entropy* and *Uniform Modular Control and Nonlinear Convergence for Wilson–Dirac Intervals*, respectively. Their results do not assert a moving-edge interpolation expansion.

## References

- NIST Digital Library of Mathematical Functions, §19.12, *Asymptotic Approximations*, https://dlmf.nist.gov/19.12 (classical elliptic-integral background).
- V. Eisler and I. Peschel, *Analytical results for the entanglement Hamiltonian of a free-fermion chain*, *Journal of Physics A* **50** (2017), 284003; DOI `10.1088/1751-8121/aa76b5` (commuting free-fermion entanglement-Hamiltonian background).
- Companion mathematical manuscripts for the Wilson-specific majorant, reference crossing, Jacobi moment and relative-entropy reduction, retained in the scientific collection.

## Contributions and acknowledgments

Kirtus Justus directs the research program and publication decisions. ChatGPT (OpenAI) derived and checked the scalar and crossing estimates and their propagated consequences as AI-assisted mathematical work. Claude (Anthropic), Gemini (Google), Grok (SpaceXAI), and DeepSeek (High-Flyer) are acknowledged as participants in the wider program, without attributing contributions to this manuscript unsupported by its provenance. No institutional endorsement, external peer review, or formal proof-assistant certification is implied.
