---
title: "Boundary-Corrected Longitudinal Modular Reduction for a Wilson–Dirac Interval"
author: 'Kirtus Justus (Theoretical Physicist) \textbullet{} 31 October 2026\tabularnewline Port Coquitlam, British Columbia, Canada'
date: ''
lang: en
header-includes:
 - \usepackage{microtype,booktabs,longtable}
 - \setlength{\emergencystretch}{3em}
---

## Abstract

For a finite interval cut from the infinite Wilson–Dirac occupied-band projection, the longitudinal perturbation can be rewritten exactly as a positive-majorant-weighted reference term plus a cross-boundary correction. The correction admits an explicit Hilbert–Schmidt bound controlled by the occupation-weighted modular quadratic form. As a consequence, the leading-order relative-entropy reduction can be equivalently formulated using the positive majorant and the reference occupation operator. This argument reformulates the modular estimate. The separate whole-line argument in *Uniform Bulk Modular Asymptotics and the Leading Wilson Entropy Law* controls that estimate and establishes the leading entropy law.

## 1. Operator setting

Let \(\mathcal H=\ell^2(\mathbb Z)\otimes\mathbb C^2\) and let \(\chi\) be the orthogonal projection onto \(L\) consecutive two-orbital cells, \(N=2L\). Operators on \(\operatorname{ran}\chi\) are implicitly restricted to that space. All full-line operators are expressed after one common, interval-preserving cellwise rotation and staggering.

Let \(P_0\) be the massless occupied-band projection and \(G\) the positive Wilson spectral majorant. For fixed \(\mu>0\) and \(m=\mu/L\), the full-line projector calculation gives

\[
P_0^2=P_0=P_0^*,\qquad G=G^*,\qquad 0\le G\le\tfrac12 I,
\qquad [G,P_0]=0,
\]
\[
S=G(I-2P_0),\qquad \operatorname{Tr}(\chi G\chi)\le\frac\mu\pi.
\tag{1}
\]

Define

\[
B_N=\chi P_0\chi,\qquad G_N=\chi G\chi,\qquad S_N=\chi S\chi,
\qquad W_N=B_N(I-B_N).
\tag{2}
\]

The compressed reference satisfies \(0<B_N<I\). Its commuting Jacobi operator \(J_N\) has off-diagonal entries \(j(N-j)/N\). Put

\[
K_N=\log(I-B_N)-\log B_N,
\quad E_N=K_N+N\eta(J_N/N),
\tag{3}
\]

with the half-filled reference scaling function \(\eta\) from the free-fermion Jacobi model. In particular, \(E_N=E_N^*\) and \([E_N,B_N]=0\). The occupation-weighted estimate is

\[
\operatorname{Tr}(W_NE_N^2)\le C(1+\log N)
\quad(N\ge2),
\tag{4}
\]

with a constant independent of \(N\). We explicitly retain (1) and (4) as input hypotheses to the new theorem.

## 2. Exact boundary-corrected decomposition

**Theorem 1.** Let \(Q=I-\chi\) and set

\[
C_N=\chi GQP_0\chi.
\]

Then for every finite interval,

\[
\boxed{S_N=G_N-G_NB_N-B_NG_N-C_N-C_N^*.}
\tag{5}
\]

Consequently,

\[
\boxed{
\operatorname{Tr}(S_NE_N)
=\operatorname{Tr}\bigl[G_N(I-2B_N)E_N\bigr]
-2\operatorname{Re}\operatorname{Tr}(C_NE_N).
}
\tag{6}
\]

**Proof.** From \(S=G(I-2P_0)\) and \([G,P_0]=0\),

\[
S_N=G_N-\chi(GP_0+P_0G)\chi.
\]

Insert \(I=\chi+Q\) between the two full-line operators in each product:

\[
\chi GP_0\chi=G_NB_N+\chi GQP_0\chi,
\]
\[
\chi P_0G\chi=B_NG_N+\chi P_0QG\chi.
\]

Because \(G,P_0\) are self-adjoint, the last term is \(C_N^*\). This proves (5), without assuming that \(G_N\) commutes with \(B_N\). Multiply by \(E_N\), trace, use \([E_N,B_N]=0\) and cyclicity, and combine the conjugate boundary traces to obtain (6). \(\square\)

## 3. Sublogarithmic boundary control

**Theorem 2.** Under the hypotheses (1)–(4),

\[
\boxed{
2\left|\operatorname{Tr}(C_NE_N)\right|
\le\sqrt{\frac{2\mu}{\pi}}\,
\left[\operatorname{Tr}(W_NE_N^2)\right]^{1/2}
=O_\mu(\sqrt{\log N}).}
\tag{7}
\]

**Proof.** The two factors in \(C_N=(QG\chi)^*(QP_0\chi)\) are Hilbert–Schmidt after restriction to the finite interval. Because \(0\le Q\le I\) and \(G^2\le G/2\),

\[
\begin{aligned}
\|QG\chi\|_{\mathrm{HS}}^2
&=\operatorname{Tr}(\chi GQG\chi)\\
&\le\operatorname{Tr}(\chi G^2\chi)
\le\tfrac12\operatorname{Tr}G_N
\le\frac\mu{2\pi}.
\end{aligned}
\tag{8}
\]

The full-line projection identity gives

\[
\chi P_0QP_0\chi
=\chi P_0\chi-(\chi P_0\chi)^2=W_N,
\]

and hence

\[
\|QP_0\chi E_N\|_{\mathrm{HS}}^2
=\operatorname{Tr}(E_NW_NE_N)
=\operatorname{Tr}(W_NE_N^2).
\tag{9}
\]

Cauchy–Schwarz for the Hilbert–Schmidt inner product, (8), (9), and (4) prove the assertion. \(\square\)

The exact Hilbert–Schmidt factor is the boundary leakage \(\Lambda_N=\operatorname{Tr}(\chi GQG\chi)=\operatorname{Tr}(\chi G^2\chi)-\operatorname{Tr}(G_N^2)\). Consequently, the proof also gives

\[
2|\operatorname{Tr}(C_NE_N)|\le 2\sqrt{\Lambda_N}\,[\operatorname{Tr}(W_NE_N^2)]^{1/2}.
\]

For fixed \(\mu>0\), the companion theorem *Continuum Limit of the Wilson Majorant Boundary Defect* establishes \(\Lambda_N\to\Phi(\mu)>0\). This identifies the asymptotic Hilbert–Schmidt prefactor without changing the \(O_\mu(\sqrt{\log N})\) growth order.

## 4. Equivalent leading-order obstruction

The established four-branch entropy decomposition and its auxiliary estimates give, for fixed \(\mu>0\),

\[
\mathcal D_L(\mu)=\frac{\mu^2}{6}\log L
+\operatorname{Tr}(S_NE_N)+O_\mu(\sqrt{\log L}),
\qquad N=2L.
\tag{10}
\]

**Corollary 3.** Under the same hypotheses,

\[
\boxed{
\mathcal D_L(\mu)=\frac{\mu^2}{6}\log L
+\operatorname{Tr}\bigl[G_N(I-2B_N)E_N\bigr]
+O_\mu(\sqrt{\log L}).}
\tag{11}
\]

In a common orthonormal eigenbasis \(B_Nv_j=b_jv_j\), \(J_Nv_j=\lambda_jv_j\), with \(E_Nv_j=e_jv_j\) and \(q_j=\langle v_j,G_Nv_j\rangle\ge0\), the remaining bulk trace is exactly

\[
\boxed{
\operatorname{Tr}\bigl[G_N(I-2B_N)E_N\bigr]
=\sum_{j=1}^{N}q_j(1-2b_j)e_j.}
\tag{12}
\]

Thus the original condition \(\operatorname{Tr}(S_NE_N)=o(\log N)\) is **equivalent** to the signed bulk condition

\[
\sum_jq_j(1-2b_j)e_j=o(\log N).
\tag{13}
\]

A sufficient noncancellation criterion is

\[
\boxed{\sum_jq_j|1-2b_j|\,|e_j|=o(\log N).}
\tag{14}
\]

It is no stronger than the stronger sufficient bound \(\sum_jq_j|e_j|=o(\log N)\), since \(|1-2b_j|\le1\); the extra occupation factor suppresses contributions from reference levels near half-filling. The separate weighted theorem in *Uniform Bulk Modular Asymptotics and the Leading Wilson Entropy Law* proves the stronger bound \(\sum_jq_j|e_j|=O_\mu(1)\), and hence both conditions at fixed positive scaled mass. Numerical tests alone would not prove either condition.

## 5. Scope and limitations

Equations (5) and (6) are exact at finite interval length. Equation (7) is a proved consequence of the explicitly identified Wilson-majorant and weighted-modular inputs. Equation (11) is a reduction with a rigorously bounded error; identifying its leading coefficient additionally uses the weighted theorem cited next. The bulk trace in (13) is controlled by the separate weighted theorem in *Uniform Bulk Modular Asymptotics and the Leading Wilson Entropy Law*. A finite entropy part and an inverse-logarithmic convergence rate do not follow from this reduction alone. For the specified interval restrictions with fixed positive scaled mass, Theorem 1 of *Finite Part of Wilson–Dirac Relative Entropy* supplies that limit and rate.

The interval is a compression of the *infinite-chain occupied-band projection*. None of the statements concerns ground-state projectors of a finite open Wilson chain unless additional arguments establish that identification. Operators on the full line are never replaced by products of their compressions without the boundary terms displayed above.

## References and mathematical inputs

- D. Slepian, “Prolate spheroidal wave functions, Fourier analysis, and uncertainty V: The discrete case,” *Bell System Technical Journal* **57** (1978), 1371–1430, DOI: 10.1002/j.1538-7305.1978.tb02104.x.
- V. Eisler and I. Peschel, “Analytical results for the entanglement Hamiltonian of a free-fermion chain,” *Journal of Physics A* **50** (2017), 284003, DOI: 10.1088/1751-8121/aa76b5.
- K. Justus, “Exact Spectral Majorants for a Wilson–Dirac Interval,” research manuscript (2026), for the model-specific full-line decomposition and trace majorant.
- K. Justus, “Logarithmic Weighted Modular Control for the Half-Filled Sine Kernel,” research manuscript (2026), for the input (4).
- K. Justus, “Finite-Interval Wilson–Dirac Relative Entropy,” research manuscript (2026), for the four-branch reduction (10).
- K. Justus, “Continuum Limit of the Wilson Majorant Boundary Defect” (2026), for the fixed-scaled-mass limit of the Hilbert–Schmidt factor.

## Contributions and acknowledgments

Kirtus Justus directed the research program and supplied its mathematical starting point. ChatGPT (OpenAI) developed the displayed boundary decomposition, its Hilbert–Schmidt estimate, and the accompanying computational cross-checks; these derivations have not undergone independent external peer review. Claude (Anthropic), Gemini (Google), Grok (SpaceXAI), and DeepSeek (High-Flyer) are acknowledged as participants in the broader research effort without assigning them unverified contributions to this argument. No institutional affiliation, endorsement, or peer-review status is implied.
