---
title: "Finite-Interval Compression and Transverse Control"
author: 'Kirtus Justus (Theoretical Physicist) \textbullet{} 31 October 2026\tabularnewline Port Coquitlam, British Columbia, Canada'
date: ''
lang: en
header-includes:
 - \usepackage{microtype}
 - \usepackage{booktabs}
 - \usepackage{longtable}
---

## Abstract

We examine compression of the full-line projector relations for the occupied-band covariances of a one-dimensional Wilson–Dirac chain. The full-line squared-difference and transverse identities imply positive finite-interval inequalities with exact boundary-leakage remainders. A stronger transverse domination follows, together with an explicit noncommutation example showing why the corresponding full-line operator products cannot be transported unchanged to finite intervals.

## Operator setting

Let \(P_m\) and \(P_0\) be the full-line occupied-band projections for the Wilson–Dirac Bloch symbol

\[
h_m(k)=\sin k\,\sigma_x+(1+m-\cos k)\sigma_z,
\quad P_m(k)=\frac12\left(I-\frac{h_m(k)}{\sqrt{m^2+4(1+m)\sin^2(k/2)}}\right).
\]

Fix an interval of \(L\) two-orbital cells, with projection \(\chi\), \(N=2L\), \(\mu>0\), and \(m=\mu/L\). After a common interval-preserving rotation and staggering, the full-line covariance difference is \(T=P_m-P_0=S+D\), where

\[
S=-\frac{g_r}{2}Q_0,\qquad
D=\frac{a_r}{2}Q_\perp,\qquad
G=\frac{g_r}{2}I,
\]

\[
r=\frac{\mu}{N+\mu},\qquad
u_r=\frac{|\sin(k/2)|}{\sqrt{\sin^2(k/2)+r^2\cos^2(k/2)}},
\quad g_r=1-u_r,\quad
 a_r=\frac{r\cos(k/2)}{\sqrt{\sin^2(k/2)+r^2\cos^2(k/2)}}.
\]

The Hermitian involutions \(Q_0,Q_\perp\) anticommute. In particular, the **full-line** identities are

\[
T^2=G,\qquad D^2=G-G^2,\qquad0\le G\le\frac12I.
\]

Set \(\Delta_N=\chi T\chi\), \(D_N=\chi D\chi\), and \(G_N=\chi G\chi\), as operators on \(\operatorname{ran}\chi\).

## Theorem: exact boundary remainders

For every positive integer \(L\) and \(\mu>0\),

\[
\boxed{G_N-\Delta_N^2=\chi T(I-\chi)T\chi\ge0,}
\]

\[
\boxed{G_N-G_N^2-D_N^2
=\chi G(I-\chi)G\chi+\chi D(I-\chi)D\chi\ge0.}
\]

Therefore,

\[
\boxed{0\le\Delta_N^2\le G_N\le\tfrac12 I,\quad
0\le D_N^2\le G_N-G_N^2\le G_N.}
\]

Taking the finite trace in the first relation gives the exact leakage formula

\[
\operatorname{Tr}G_N-\|\Delta_N\|_{\mathrm{HS}}^2
=\|(I-\chi)T\chi\|_{\mathrm{HS}}^2.
\]

**Proof.** For any bounded self-adjoint \(X\), insertion of \(I=\chi+(I-\chi)\) gives

\[
\chi X^2\chi-(\chi X\chi)^2=\chi X(I-\chi)X\chi\ge0.
\]

Apply this identity to \(T\) and use \(T^2=G\) for the first formula. For the second, apply it to both \(G\) and \(D\), obtaining

\[
G_N^2=\chi G^2\chi-\chi G(I-\chi)G\chi,
\quad
D_N^2=\chi D^2\chi-\chi D(I-\chi)D\chi.
\]

Substitute the full-line equality \(G-G^2-D^2=0\). Every remainder is a positive square. Because \(0\le G_N\le I/2\), the remaining order comparisons follow. The trace identity is the Hilbert–Schmidt norm identity for \((I-\chi)T\chi\). \(\square\)

## Proposition: the compressed majorant need not commute with the compressed reference

Let \(B_N=\chi P_0\chi\) in the scalarized basis. At \(N=4\), define

\[
c_1=\frac1\pi\int_0^\pi g_r(k)\cos k\,dk.
\]

The scalarized sine kernel \(B_4\) and the same-parity Toeplitz matrix \(G_4\) satisfy

\[
\boxed{[G_4,B_4]_{0,1}=-\frac{2c_1}{3\pi}\ne0.}
\]

Indeed \(g_r(k)=1-(1+r^2\cot^2(k/2))^{-1/2}\) decreases strictly over \((0,\pi)\), so integration by parts shows \(c_1=-\pi^{-1}\int_0^\pi g_r'(k)\sin k\,dk>0\). The matrix formula follows by direct multiplication of the sine-kernel entries \(B_{ij}=\sin[\pi(i-j)/2]/[\pi(i-j)]\) off the diagonal and the parity-supported Fourier coefficients of \(G_4\). \(\square\)

The full-line \([G,P_0]=0\) is nevertheless sufficient for the Wilson staggered-pairing inequality: that proof decomposes the interval-supported vector using the full-line projector before evaluating the compressed expectation. The finite model does not require the false identity \([G_N,B_N]=0\).

## Scientific scope and acknowledgments

The theorem pertains to the specified infinite-chain band projections and finite interval compressions, for every \(L\ge1\) and \(\mu>0\). No reference-modular, Coulomb, all-degree nonlinear, or cross-boundary entropy limit follows solely from these identities. The leading relative-entropy law follows only after combining these identities with the separate bounded nonlinear, boundary-entropy and weighted modular estimates, as done in *Uniform Bulk Modular Asymptotics and the Leading Wilson Entropy Law*.

Kirtus Justus provided the research direction and materials. ChatGPT (OpenAI) assisted with derivation, verification, and manuscript preparation. Claude (Anthropic), Gemini (Google), Grok (SpaceXAI), and DeepSeek (High-Flyer) are acknowledged as participants in the broader research workflow without assignment of unsupported specific contributions. The mathematical conclusions have not undergone external peer review, and no institution or AI provider is represented as endorsing them.
