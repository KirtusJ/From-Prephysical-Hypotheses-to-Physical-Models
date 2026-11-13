---
title: "Continuum Limit of the Wilson Majorant Boundary Defect"
author: 'Kirtus Justus (Theoretical Physicist) \textbullet{} 31 October 2026\tabularnewline Port Coquitlam, British Columbia, Canada'
date: ''
lang: en
header-includes:
 - \usepackage{microtype,booktabs,longtable}
 - \setlength{\emergencystretch}{3em}
---

## Abstract

For the positive Wilson majorant compressed to an even-length scalar interval in the fixed-scaled-mass regime, we prove existence of the limiting cross-boundary Hilbert–Schmidt leakage and express it by an absolutely convergent one-dimensional integral. We identify a positive finite limit, establish strict monotonicity and strict concavity of the limiting function, and determine its small-scaled-mass expansion. The result concerns the majorant alone; it does not imply a uniform estimate for the finite reference-modular discrepancy or the complete Wilson relative entropy.

## Definitions

Fix \(\mu>0\), let \(N\to\infty\) through even integers, and set \(r_N=\mu/(N+\mu)\). On the cell Brillouin zone let the orbital-scalar Wilson majorant have symbol

\[
G_r(k)=\tfrac12 g_r(k),\qquad
g_r(k)=1-\frac{|\sin(k/2)|}{\sqrt{\sin^2(k/2)+r^2\cos^2(k/2)}}.
\]

Let \(\chi_N\) project onto the \(N\)-site scalar interval, with the cell-preserving scalarization for which the nonzero off-diagonal coefficients occur at even scalar separations. For \(d\in\mathbb Z\), let

\[
c_d(r)=\frac{1}{2\pi}\int_{-\pi}^{\pi}G_r(k)e^{-idk}\,dk
=\frac1{2\pi}\int_0^\pi g_r(k)\cos(dk)\,dk.
\]

The coefficient at scalar separation \(2d\) has magnitude \(|c_d(r)|\); possible staggering phases do not affect its squared modulus. Define

\[
f(t)=1-\frac{t}{\sqrt{1+t^2}},\qquad
F(x)=\int_0^\infty f(t)\cos(2xt)\,dt\quad(x\ge0).
\]

The function \(f\) is nonnegative and integrable, with \(\int_0^\infty f(t)\,dt=1\); hence \(F\) is continuous and \(F(0)=1\).

## Theorem: exact limiting leakage

**Theorem 1.** For every fixed \(\mu>0\),

\[
\boxed{
\lim_{N\to\infty\atop N\,\mathrm{even}}
\|(I-\chi_N)G_{r_N}\chi_N\|_{\mathrm{HS}}^2
=\Phi(\mu)
:=\frac{2}{\pi^2}\int_0^\infty
\min\{\mu,2x\}\,F(x)^2\,dx.
}
\]

The integral converges absolutely and \(0<\Phi(\mu)<\infty\).

*Proof.* For \(r\in(0,1)\), set \(h_r(k)=g_r(k)\) on \([0,\pi]\). Under \(t=\tan(k/2)/r\), the Fourier coefficient becomes exactly

\[
 c_d(r)=\frac r\pi\int_0^\infty
 \frac{f(t)}{1+r^2t^2}\cos\bigl(2d\arctan(rt)\bigr)\,dt.
 \tag{1}
\]

For each fixed \(A<\infty\), dominated convergence, with the integral split at a fixed large \(t\)-cutoff, shows

\[
\sup_{d\ge0:\,rd\le A}
\left|\frac{\pi c_d(r)}r-F(rd)\right|\longrightarrow0
\qquad(r\downarrow0).
\tag{2}
\]

Indeed the phase difference tends uniformly to zero for \(rd\le A\) on compact \(t\)-ranges, while \(f\in L^1\) controls the tails.

A global Fourier coefficient bound supplies the necessary domination. Direct differentiation on \((0,\pi)\), writing \(s=\sin(k/2)\), \(c=\cos(k/2)\) and \(D^2=s^2+r^2c^2\), yields

\[
 h_r'(k)=-\frac{r^2c}{2D^3},\quad
 h_r''(k)=\frac{r^2s}{4D^3}
 +\frac{3r^2(1-r^2)sc^2}{4D^5}\ge0.
\]

Thus \(h_r'(0)=-1/(2r)\), \(h_r'(\pi)=0\), and \(\int_0^\pi h_r''(k)\,dk=1/(2r)\). Two integrations by parts for \(d\ge1\) give

\[
\left|c_d(r)\right|
\le \frac{1}{2\pi r d^2}.
\tag{3}
\]

On the other hand, (1) and \(\int f=1\) imply \(|c_d(r)|\le r/\pi\) for every \(d\). Together,

\[
\boxed{
\left|\frac{\pi c_d(r)}r\right|
\le\min\left\{1,\frac1{2(rd)^2}\right\},\qquad d\ge1.
}
\tag{4}
\]

The exact Fourier boundary identity, including the two signs of each nonzero scalar displacement, reads

\[
 L_N:=\|(I-\chi_N)G_{r_N}\chi_N\|_{\mathrm{HS}}^2
 =2\sum_{d=1}^\infty\min(N,2d)|c_d(r_N)|^2.
 \tag{5}
\]

Rewriting (5) as a mesh sum gives

\[
 L_N=\frac2{\pi^2}\sum_{d=1}^\infty r_N
 \min(Nr_N,2dr_N)\left|\frac{\pi c_d(r_N)}{r_N}\right|^2.
\]

Since \(Nr_N\to\mu\), equation (2) provides uniform convergence of the summands on bounded intervals in the mesh variable \(x=dr_N\). The global bound (4) dominates the mesh tails by an integrable multiple of \(\min\{\mu+1,2x\}\min\{1,(2x^2)^{-1}\}^2\). Consequently the mesh sums converge to the stated integral. Positivity follows from \(F(0)=1\), continuity, and \(\mu>0\); finiteness follows from (4), which also yields \(|F(x)|\le\min\{1,(2x^2)^{-1}\}\) for \(x>0\). \(\square\)

## Structural properties and small-mass expansion

**Theorem 2.** The limiting function \(\Phi\) is increasing and concave on \((0,\infty)\), with

\[
\Phi'(\mu)=\frac2{\pi^2}\int_{\mu/2}^\infty F(x)^2\,dx>0,
\qquad
\Phi''(\mu)=-\frac1{\pi^2}F(\mu/2)^2\le0.
\]

Furthermore,

\[
\boxed{
\Phi(\mu)=\left(\frac1\pi-\frac14\right)\mu
-\frac{\mu^2}{2\pi^2}+o(\mu^2)
\quad(\mu\downarrow0).
}
\]

*Proof.* Differentiating the defining integral at the moving interface \(x=\mu/2\) yields the two derivative formulas; the interface contributions cancel. To see strict positivity of \(F(x)\) for \(x>0\), integrate by parts to write \(F(x)=(2x)^{-1}\int_0^\infty h(t)\sin(2xt)\,dt\), with \(h(t)=(1+t^2)^{-3/2}\) positive and strictly decreasing. Pairing successive positive and negative half-periods of the sine wave gives a strictly positive contribution from each pair. Hence \(F(x)>0\) for all \(x>0\), so \(\Phi'(\mu)>0\) and \(\Phi''(\mu)<0\) for all \(\mu>0\). For the small-\(\mu\) expansion, write

\[
\Phi(\mu)=\frac{2\mu}{\pi^2}\int_0^\infty F(x)^2\,dx
-\frac2{\pi^2}\int_0^{\mu/2}(\mu-2x)F(x)^2\,dx.
\]

Cosine-transform Plancherel, accounting for the frequency \(2x\), gives

\[
\int_0^\infty F(x)^2\,dx
=\frac\pi4\int_0^\infty f(t)^2\,dt
=\frac\pi4\left(2-\frac\pi2\right).
\]

For the final equality put \(t=\sinh u\), followed by \(y=e^{-u}\), to obtain \(\int f^2dt=2\int_0^1 y^2/(1+y^2)\,dy=2-\pi/2\). Since \(F(x)^2\to1\) as \(x\downarrow0\), the final integral is \(\mu^2/4+o(\mu^2)\). Substitution proves the expansion. \(\square\)

The identity \(F(x)=(2x)^{-1}\int_0^\infty\sin(2xt)(1+t^2)^{-3/2}\,dt\) for \(x>0\) follows by integration by parts and can be used for stable numerical quadrature. The half-period comparison in Theorem 2 establishes strict concavity for every \(\mu>0\).

## Application and limitation

If \(C_N=\chi_N G_{r_N}(I-\chi_N)P_0\chi_N\), then the cross-boundary Cauchy–Schwarz argument implies

\[
2|\operatorname{Tr}(C_NE_N)|
\le 2\sqrt{L_N}\,\sqrt{\operatorname{Tr}[B_N(I-B_N)E_N^2]}.
\]

Theorem 1 supplies \(\sqrt{L_N}=\sqrt{\Phi(\mu)}+o(1)\) at each fixed \(\mu>0\). Combined with the occupation-weighted quadratic modular estimate, this retains an \(O_\mu(\sqrt{\log N})\) boundary bound with an asymptotically identified Hilbert–Schmidt factor. It neither proves the required weighted bulk trace is sublogarithmic nor controls the full modular operator norm. The leading coefficient is established by the separate argument in *Uniform Bulk Modular Asymptotics and the Leading Wilson Entropy Law*; neither the entropy finite part nor an all-mode operator-norm bound follows from this boundary-defect limit.

## References

- NIST Digital Library of Mathematical Functions, §19.12, elliptic asymptotics for the exact first Jacobi moment: https://dlmf.nist.gov/19.12.
- D. Slepian, *Bell System Technical Journal* **57** (1978), 1371–1430, discrete time-frequency concentration.
- K. Justus, *Exact Spectral Majorants for a Wilson–Dirac Interval* (2026), full-line Wilson majorant and scalarization.
- K. Justus, *Fourier-Space Boundary Defects for Wilson–Dirac Covariances* (2026), exact finite-interval Fourier boundary identity.

## Contributions and acknowledgments

Kirtus Justus directed the mathematical research and established the publication scope. ChatGPT (OpenAI) developed the exact continuum-limit argument and its small-scaled-mass analysis. The arguments were rechecked algebraically and against the reference normalization; no formal proof certification is claimed. Claude (Anthropic), Gemini (Google), Grok (SpaceXAI), and DeepSeek (High-Flyer) are acknowledged for participation elsewhere in the research program, without attributing independent verification of the present derivations. No external peer review, formal proof-assistant verification, institutional endorsement, or experimental validation is claimed.
