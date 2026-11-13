---
title: "Fourth-Moment Control of the Wilson Nonlinear Correction"
author: 'Kirtus Justus (Theoretical Physicist) \textbullet{} 31 October 2026\tabularnewline Port Coquitlam, British Columbia, Canada'
date: ''
lang: en
header-includes:
 - \usepackage{microtype}
 - \usepackage{booktabs}
 - \usepackage{longtable}
---

## Abstract

For the mass-scaled Wilson–Dirac interval covariance, we derive a vanishing bound for the transverse nonlinear correction, sharpening a square-root-logarithmic upper bound. The argument combines the proven positive spectral-majorant tail estimate with the sine-kernel/Jacobi second moment. Specifically, the transverse contribution is \(O_\mu(\sqrt{\log N/N})\), while the longitudinal contribution remains \(O_\mu(1)\). Consequently the complete nonlinear correction is uniformly bounded at fixed scaled mass. Together with a separately established cross-boundary entropy bound, this reduces the leading relative-entropy problem to its exact reference-modular residual, without proving the latter vanishes or has a prescribed asymptotic order.

## 1. Model and inputs

Let \(N=2L\) and \(m=\mu/L\) with fixed \(\mu>0\). Consider the interval compression of the occupied-band projection of

\[
h_m(k)=\sin k\,\sigma_x+(1+m-\cos k)\sigma_z.
\]

Under the established massless scalarization, the reference covariance is \(B_N\), with commuting Jacobi matrix \(J_N\). Write \(W_N=B_N(I-B_N)\), and decompose the perturbation as \(\Delta_N=S_N+D_N\). Let \(v_j\) be common eigenvectors of \(B_N\) and \(J_N\), with eigenvalues \(b_j\in(0,1)\) and \(\lambda_j\); put \(q_j=\langle v_j,G_Nv_j\rangle\ge0\).

The already proved Wilson spectral-majorant theorem supplies

\[
\lvert\langle v_j,S_Nv_j\rangle\rvert\le q_j,\qquad
\lvert\langle v_j,D_Nv_j\rangle\rvert\le2\sqrt{q_jb_j(1-b_j)},
\]
\[
\sum_{|\lambda_j|>t}q_j\le\frac{a_\mu}{t}+\frac{b_\mu}{t^2},\qquad
a_\mu=\sqrt{\frac2{15}}\frac{\mu^2}{\pi},\quad b_\mu=\frac{\mu}{3\pi},\qquad t>0.
\]

The Jacobi normalization ensures \(|\lambda_j|\le N/2\). The exact half-filled sine-kernel boundary identity implies

\[
0\le M_{2,N}:=\operatorname{Tr}(J_N^2W_N)
\le\frac{32}{\pi^2}(H_N+1),
\]

and the refined exterior-lattice computation proves \(M_{2,N}=(3\pi^2)^{-1}\log N+O(1)\).

Define \(\eta(t)=\pi t\,{}_3F_2(\frac14,\frac12,\frac34;1,\frac32;4t^2)\) and \(V_N=-N[\eta(J_N/N)-\pi J_N/N]\). The positive-coefficient hypergeometric series gives

\[
\lvert\eta(t)-\pi t\rvert\le C_\eta|t|^3\quad(|t|\le\tfrac12),
\qquad C_\eta=4\pi\bigl[{}_3F_2(\tfrac14,\tfrac12,\tfrac34;1,\tfrac32;1)-1\bigr].
\]

All inputs are specific to the Wilson–Dirac/sine-kernel model and do not assume a reference-modular comparison.

## 2. A fourth-moment bound for the positive majorant

**Lemma 1.** For every even \(N\ge2\),

\[
\boxed{\operatorname{Tr}(G_NJ_N^4)=\sum_jq_j|\lambda_j|^4
\le\frac{a_\mu N^3}{6}+\frac{b_\mu N^2}{2}.}
\]

**Proof.** The diagonal representation holds because \(J_N^4\) is diagonal in the common reference eigenbasis, regardless of whether \(G_N\) commutes with \(J_N\). For the positive measure \(\nu_N=\sum_jq_j\delta_{|\lambda_j|}\), layer-cake integration and the Jacobi spectral radius give

\[
\begin{aligned}
\operatorname{Tr}(G_NJ_N^4)
&=4\int_0^{N/2}t^3\nu_N((t,\infty))\,dt\\
&\le4\int_0^{N/2}(a_\mu t^2+b_\mu t)\,dt
=\frac{a_\mu N^3}{6}+\frac{b_\mu N^2}{2}.
\end{aligned}
\]

The singular appearance of the spectral-tail bound near \(t=0\) causes no problem: the integrated majorant is finite. \(\square\)

## 3. Improved transverse estimate

**Theorem 2.** Let \(\mathcal Q_N^{\rm trans}=\operatorname{Tr}(D_NV_N)\). Then

\[
\boxed{
|\mathcal Q_N^{\rm trans}|
\le2C_\eta\sqrt{\left(\frac{a_\mu}{6N}+\frac{b_\mu}{2N^2}\right)M_{2,N}}
=O_\mu\!\left(\sqrt{\frac{\log N}{N}}\right).
}
\]

In particular \(\mathcal Q_N^{\rm trans}\to0\) as \(N\to\infty\) at each fixed \(\mu>0\).

**Proof.** In the reference eigenbasis, \(V_N\) has diagonal entries \(w_j\) with \(|w_j|\le C_\eta|\lambda_j|^3/N^2\). Using the pairing inequality followed by Cauchy–Schwarz with the **fourth positive-majorant moment**, not merely its total mass, yields

\[
\begin{aligned}
|\mathcal Q_N^{\rm trans}|
&\le\frac{2C_\eta}{N^2}\sum_j|\lambda_j|^3\sqrt{q_jb_j(1-b_j)}\\
&\le\frac{2C_\eta}{N^2}
\left(\sum_jq_j\lambda_j^4\right)^{1/2}
\left(\sum_j\lambda_j^2b_j(1-b_j)\right)^{1/2}\\
&=\frac{2C_\eta}{N^2}
\sqrt{\operatorname{Tr}(G_NJ_N^4)\operatorname{Tr}(J_N^2W_N)}.
\end{aligned}
\]

Apply Lemma 1 and the established Jacobi moment bound. \(\square\)

The finite-length estimate is explicit; the sharp asymptotic coefficient for \(M_{2,N}\) is not required to obtain the rate, only its \(O(\log N)\) upper bound.

## 4. Bounded nonlinear correction and modular reduction

The established longitudinal estimate is

\[
|\mathcal Q_N^{\rm long}|\le C_\eta\left(\frac{3a_\mu}{8}+\frac{3b_\mu}{2N}\right).
\]

Therefore

\[
\boxed{
|\mathcal Q_N|\le C_\eta\left(\frac{3a_\mu}{8}+\frac{3b_\mu}{2N}\right)
+2C_\eta\sqrt{\left(\frac{a_\mu}{6N}+\frac{b_\mu}{2N^2}\right)M_{2,N}}
=O_\mu(1).}
\]

The exact two-bond asymptotic and finite quasifree relative-entropy decomposition are

\[
\mathcal P_L=\frac{\mu^2}{6}\log L+O_\mu(1),\qquad
\mathcal D_L=\mathcal P_L+\mathcal Q_N+\mathcal F_L-\Delta S_L,
\]

where \(\mathcal F_L=\operatorname{Tr}[(A_N-B_N)E_N]\) is the exact reference-modular residual. Theorem 1 of *Uniform Square-Root-Mass Control of Wilson–Dirac Boundary Covariances*, with its entropy argument in section 5, proves $\Delta S_L=O_\mu(1)$ for this Wilson scaling. Combining that imported bound with the nonlinear result of this paper yields

\[
\boxed{\mathcal D_L=\frac{\mu^2}{6}\log L+\mathcal F_L+O_\mu(1).}
\]

This reduction alone does not prove \(\mathcal F_L=o(\log L)\), convergence to a finite constant, or a proposed inverse-logarithmic convergence rate. The separate theorem in *Uniform Bulk Modular Asymptotics and the Leading Wilson Entropy Law* proves \(\mathcal F_L=O_\mu(1)\), sufficient for the leading law. Theorem 3 of *Uniform Modular Control and Nonlinear Convergence for Wilson–Dirac Intervals* proves $\|E_N\|\le7$ for every even $N\ge2$, under the exact concentration connection specified there. This later result is separate from the reduction proved above.

## 5. Evidence and scope

The fourth-moment estimate and theorem are exact mathematical consequences of the stated majorant and sine-kernel results. Independent finite arithmetic compares the improved bound with the earlier bound for eight Wilson configurations; all satisfy the stronger estimate. These tests are consistency checks, not the proof. The claimed rate holds at fixed \(\mu\) only, with no uniform assertion for \(\mu\) varying with \(N\).

### External mathematical context

- V. Eisler and I. Peschel, “Analytical results for the entanglement Hamiltonian of a free-fermion chain,” *J. Phys. A* **50** (2017) 284003, doi:10.1088/1751-8121/aa76b5.
- D. Slepian, “Prolate spheroidal wave functions, Fourier analysis, and uncertainty. V: The discrete case,” *Bell System Technical Journal* **57** (1978), 1371–1430, doi:10.1002/j.1538-7305.1978.tb02104.x.
- S. Karnik, J. Romberg and M. A. Davenport, “Improved bounds for the eigenvalues of prolate spheroidal wave functions and discrete prolate spheroidal sequences,” *Applied and Computational Harmonic Analysis* **55** (2021), 97–128, doi:10.1016/j.acha.2021.04.002.

These references support the classical concentration-operator setting; they do not independently prove the new Wilson-specific fourth-moment consequence.

### Acknowledgments and contributions

Kirtus Justus directed the research. ChatGPT (OpenAI) developed and audited this fourth-moment derivation and its computational corroboration. Claude (Anthropic), Gemini (Google), Grok (SpaceXAI), and DeepSeek (High-Flyer) are acknowledged as broader research contributors without attribution of this derivation to them. There has been no external human peer review or institutional endorsement.
