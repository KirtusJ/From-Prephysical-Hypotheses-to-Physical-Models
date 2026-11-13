---
title: "Positive Reference-Modular Localization and Bounds for the Wilson Majorant Jacobi Moment"
author: 'Kirtus Justus (Theoretical Physicist) \textbullet{} 31 October 2026\tabularnewline Port Coquitlam, British Columbia, Canada'
date: ''
lang: en
header-includes:
 - \usepackage{microtype,booktabs,longtable}
 - \setlength{\emergencystretch}{3em}
---

## Abstract

For the half-filled finite sine-kernel reference and a Wilson positive majorant, we prove a parameterized spectral-wing bound for the positive reference-modular trace and derive complementary upper and lower logarithmic bounds for the positive majorant-weighted Jacobi moment. The arguments use finite-dimensional order inequalities, the established Wilson majorant tail, the exact signed Jacobi first moment, and a published discrete-prolate eigenvalue bound. No uniform finite-size approximation of the reference modular generator by the Jacobi generator is assumed. The full fixed-positive-scaled-mass entropy expansion is proved separately in Theorem 1 of *Finite Part of Wilson–Dirac Relative Entropy*, with remainder $O_\mu(1/\log L)$. Theorem 3 of *Uniform Modular Control and Nonlinear Convergence for Wilson–Dirac Intervals* proves a finite-mode bound $\|E_N\|\le7$; it does not assert a uniform moving-edge expansion.

## 1. Operators and mathematical inputs

Let \(N=2L\) be even and \(\mu>0\) fixed. The reference covariance and commuting Jacobi matrix are

\[
B_N(i,j)=\begin{cases}\frac12&i=j,\\\frac{\sin[\pi(i-j)/2]}{\pi(i-j)}&i\ne j,\end{cases}
\qquad (J_N)_{j-1,j}=\frac{j(N-j)}N,
\]
with all other Jacobi entries zero. The reference modular operator and the positive Wilson majorant are

\[
K_N=\log(I-B_N)-\log B_N,\qquad G_N\succeq0,\qquad M_N=\operatorname{Tr}G_N\le\frac\mu\pi.
\]

Write \(S_N=S_N^*\) for the longitudinal Wilson covariance perturbation and assume the exact operator inequalities \(-G_N\preceq S_N\preceq G_N\). The following established majorant tail is used as a mathematical input, for every \(t>0\):

\[
\nu_N((t,\infty)):=\operatorname{Tr}\!\bigl(G_N\mathbf1_{\{|J_N|>t\}}\bigr)
\le\frac{a_\mu}{t}+\frac{b_\mu}{t^2},\quad
 a_\mu=\sqrt{\frac2{15}}\frac{\mu^2}{\pi},\quad b_\mu=\frac\mu{3\pi}.
\tag{1}
\]

The exact longitudinal first moment has the asymptotic

\[
\operatorname{Tr}(S_NJ_N)=-\frac{\mu^2}{6\pi}\log N+
\frac{\mu^2}{4\pi}-\frac{\mu^2}{6\pi}\log\frac4\mu
+O_\mu\!\left(\frac{\log N}{N}\right).
\tag{2}
\]

The published discrete-prolate lower eigenvalue estimate, combined with half-filled particle–hole symmetry, gives

\[
\|K_N\|\le 2N\operatorname{arsinh}(1)+3\log N+C
\tag{3}
\]
for an absolute \(C\) and even \(N\). The full Wilson entropy is already reduced, under its separately established hypotheses, to

\[
\mathcal D_L(\mu)=P_N+C_\mu+O_\mu(\sqrt{\log N}),\quad
P_N=\operatorname{Tr}(G_N|K_N|),\quad
C_\mu=\frac{\mu^2}{4}-\frac{\mu^2}{6}\log\frac8\mu.
\tag{4}
\]

The explicit \(C_\mu\) in (4) is **not** a certified entropy finite part: the displayed remainder has not been shown to converge. Equations (1)–(4) are inputs from the cited studies, not independently re-proved in this manuscript.

## 2. A spectral-wing trace inequality

**Lemma 1 (order domination).** Let \(G\succeq0\), \(-G\preceq S=S^*\preceq G\), and \(F=F^*\) be finite matrices. Then

\[
\boxed{\bigl|\operatorname{Tr}(SF)\bigr|\le\operatorname{Tr}(G|F|).}
\tag{5}
\]

*Proof.* Decompose \(F=F_+-F_-\) spectrally, with \(F_\pm\succeq0\). Trace monotonicity against each positive part gives \(|\operatorname{Tr}(SF_\pm)|\le\operatorname{Tr}(GF_\pm)\). The triangle inequality yields (5). No commutativity between \(G\) and \(F\) is required. \(\square\)

Let \(\Pi_{>R}=\mathbf1_{\{|J_N|>R\}}\), \(\Pi_{\le R}=I-\Pi_{>R}\), and \(P_N^{\le R}=\operatorname{Tr}(G_N|K_N|\Pi_{\le R})\). Because \([B_N,J_N]=0\), the operators \(|K_N|\) and \(\Pi_{>R}\) commute and their product is positive.

**Theorem 2 (quantitative positive-trace localization).** Under (1) and (3), for all \(R>0\),

\[
\boxed{0\le P_N-P_N^{\le R}
\le\bigl(2N\operatorname{arsinh}(1)+3\log N+C\bigr)
\left(\frac{a_\mu}{R}+\frac{b_\mu}{R^2}\right).}
\tag{6}
\]

*Proof.* Positivity follows from \(\operatorname{Tr}(G_NX)\ge0\) whenever \(G_N,X\succeq0\), taking \(X=|K_N|\Pi_{>R}\). Since \(0\preceq X\preceq\|K_N\|\Pi_{>R}\), trace monotonicity, (1), and (3) imply (6). \(\square\)

**Corollary 3 (adjustable sublogarithmic window).** Let \(h_N\to\infty\) with \(h_N=o(\log N)\), and set \(R_N=N/h_N\). Then

\[
\boxed{P_N-P_N^{\le R_N}=O_\mu(h_N)=o_\mu(\log N),}
\tag{7}
\]

and (4) becomes

\[
\boxed{\mathcal D_L(\mu)=P_N^{\le N/h_N}+C_\mu
+O_\mu\bigl(\sqrt{\log N}+h_N\bigr).}
\tag{8}
\]

*Proof.* Substitute \(R_N=N/h_N\) in (6). The leading term is \(2a_\mu\operatorname{arsinh}(1)h_N\), with lower-order contributions \(O_\mu(h_N\log N/N+h_N^2/N)\), hence (7). Equation (8) follows from (4). \(\square\)

For example, \(h_N=\log N/\log\log N\) produces the narrower region \(|J_N|\le N\log\log N/\log N\) while the discarded wing remains \(o(\log N)\). This choice **worsens the stated remainder** relative to \(h_N=\sqrt{\log N}\); it only tightens the window relevant for a leading-coefficient proof. In general the coarse bound requires \(R_N\gg N/\log N\). This is a sufficient scale for this method, not a necessary physical threshold.

The desired complete leading logarithmic coefficient is equivalent, under (4), to

\[
\boxed{P_N^{\le N/h_N}=\frac{\mu^2}{6}\log N+o_\mu(\log N).}
\tag{9}
\]

Equation (9) follows by combining the separate leading entropy law and positive-trace reduction with the discarded-wing estimate above. The finite-dimensional wing bound alone does not determine its coefficient.

## 3. Positive majorant-weighted Jacobi moment

Define \(Q_N(\mu)=\operatorname{Tr}(G_N|J_N|)\). Since \(J_N\) is a self-adjoint Jacobi matrix and \(\|J_N\|\le N/2\), the layer-cake representation gives

\[
Q_N(\mu)=\int_0^{N/2}\nu_N((t,\infty))\,dt.
\tag{10}
\]

**Theorem 4 (logarithmic coefficient bracket).** For every fixed \(\mu>0\),

\[
\boxed{\frac{\mu^2}{6\pi}\le
\liminf_{N\to\infty,\ N\,\mathrm{even}}\frac{Q_N(\mu)}{\log N}\le
\limsup_{N\to\infty,\ N\,\mathrm{even}}\frac{Q_N(\mu)}{\log N}\le
\sqrt{\frac2{15}}\frac{\mu^2}{\pi}.}
\tag{11}
\]

*Proof.* Lemma 1 with \(F=J_N\) gives \(Q_N\ge|\operatorname{Tr}(S_NJ_N)|\). The exact asymptotic (2) then proves the lower limit. For the upper limit, split (10) at \(t=1\). For \(N\ge2\), the interval \((0,1)\) contributes at most \(M_N\), while (1) gives

\[
Q_N\le M_N+a_\mu\log(N/2)+b_\mu(1-2/N).
\]

Divide by \(\log N\) and let \(N\to\infty\), using \(M_N\le\mu/\pi\). \(\square\)

The lower bound already has the coefficient \(\mu^2/(6\pi)\) anticipated for \(Q_N\), but the majorant-tail estimate alone does not establish a matching upper bound. A numerical observation that \(Q_N+\operatorname{Tr}(S_NJ_N)\) remains small over tested finite sizes is not a proof of boundedness or decay.

## 4. A sufficient two-part proof obligation

The positive-trace problem can be decomposed *algebraically* as

\[
P_N=\pi Q_N + \underbrace{\operatorname{Tr}\bigl[G_N(|K_N|-\pi|J_N|)\bigr]}_{\Delta_N^{\mathrm{abs}}}.
\tag{12}
\]

Therefore the pair of estimates

\[
Q_N=\frac{\mu^2}{6\pi}\log N+o_\mu(\log N),\qquad
\Delta_N^{\mathrm{abs}}=o_\mu(\log N)
\tag{13}
\]

would imply (9), and hence the full leading relative-entropy coefficient. These conditions are sufficient, **not individually necessary**, because cancellations between two terms cannot be ruled out. Neither estimate in (13) is proved here.

The positive operator structure and signed exact Jacobi moment thus give a precise framework for separating majorant spectral-weight growth from the modular comparison. The separate weighted theorem in *Uniform Bulk Modular Asymptotics and the Leading Wilson Entropy Law* gives \(P_N=\pi Q_N+O_\mu(1)\); combined with the proved entropy law and the positive-trace reduction, this also yields \(Q_N=(\mu^2/(6\pi))\log N+O_\mu(\sqrt{\log N})\).

## 5. Scientific limitations and references

All operator statements concern the infinite-chain occupied-band projectors compressed to the specified finite interval. The positive-majorant tail, entropy reduction, and elliptic first moment are mathematical inputs from the named companion papers. Numerical experiments on finite matrices are corroboration only. Fixed-index discrete-prolate asymptotics must not be substituted for estimates uniform over moving spectral indices. The finite-part convergence and any uniform moving-edge expansion are separate from the established leading entropy coefficient.

\newpage

**References**

- B. Adcock, D. Huybrechs and J. Martín-Vaquero, “On the Numerical Stability of Fourier Extensions,” *Foundations of Computational Mathematics* **14** (2014), 635–687, https://doi.org/10.1007/s10208-013-9158-8, Theorem 3.1.
- D. Slepian, “Prolate Spheroidal Wave Functions, Fourier Analysis, and Uncertainty V: The Discrete Case,” *Bell System Technical Journal* **57** (1978), 1371–1430, https://doi.org/10.1002/j.1538-7305.1978.tb02104.x.
- K. Justus, *Exact Spectral Majorants for a Wilson–Dirac Interval*, companion mathematical manuscript.
- K. Justus, *Exact Longitudinal Jacobi Moment and Wilson Majorant Mass*, companion mathematical manuscript.
- K. Justus, *Logarithmic Weighted Modular Control for the Half-Filled Sine Kernel*, companion mathematical manuscript.
- K. Justus, *A Positive Reference-Modular Trace for Wilson–Dirac Intervals*, companion mathematical manuscript.

**Contributions and acknowledgments.** Kirtus Justus directed the research and publication standards. ChatGPT (OpenAI) performed the present derivations, source examination, numerical cross-checks and drafting, in AI-assisted research that has not been externally peer reviewed. Claude (Anthropic), Gemini (Google), Grok (SpaceXAI) and DeepSeek (High-Flyer) are acknowledged as broader programme participants without attributing this specific derivation to them or implying endorsement.
