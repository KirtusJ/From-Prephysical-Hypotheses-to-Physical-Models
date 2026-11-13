---
title: "Signed Exponential Remainder for Wilson-Dirac Covariance Distances"
author: 'Kirtus Justus (Theoretical Physicist) \textbullet{} 31 October 2026\tabularnewline Port Coquitlam, British Columbia, Canada'
date: ''
lang: en
header-includes:
 - \usepackage{microtype}
 - \usepackage{booktabs}
 - \usepackage{longtable}
---

## Abstract

The continuum Hilbert–Schmidt covariance-distance function associated with the fixed-positive-mass scaling of a one-dimensional Wilson–Dirac chain admits an exact, sign-definite remainder beyond its linear and logarithmic large-parameter terms. The remainder has a strictly positive integral kernel, an explicit global upper bound in terms of the modified Bessel function \(K_1\), and a sharp leading exponential equivalent. The calculation uses Fourier–Plancherel normalization, a Bessel first-moment identity, and classical integral representations. It concerns the covariance-distance scaling function, with the interval-size limit already taken; it entails no asymptotic assertion about the complete quasifree relative entropy.

## 1. Main result

For \(t,\mu>0\), define

\[
G(t)=K_0(t)^2+\left(K_1(t)-\frac1t\right)^2,
\qquad H(\mu)=\frac1{\pi^2}\int_0^\mu(\mu-t)G(t)\,dt,
\]

and

\[
A(\mu)=\frac\mu\pi-\frac{\log(\mu/2)+\gamma+1}{\pi^2},
\qquad
W(t)=\frac{2K_1(t)}t-K_0(t)^2-K_1(t)^2.
\]

Here \(\gamma\) denotes Euler's constant and \(K_\nu\) the modified Bessel function of the second kind.

**Theorem 1 (exact signed remainder and global quantitative bound).** For every \(\mu>0\),

\[
\boxed{
A(\mu)-H(\mu)=\frac1{\pi^2}\int_\mu^\infty(t-\mu)W(t)\,dt,
\qquad W(t)>0\quad(t>0).
}
\tag{1}
\]

Consequently,

\[
\boxed{0<A(\mu)-H(\mu)<\frac{2K_1(\mu)}{\pi^2\mu}\qquad(\mu>0).}
\tag{2}
\]

The gap \(A-H\) is strictly decreasing and strictly convex, and

\[
\boxed{
A(\mu)-H(\mu)
=\frac{\sqrt{2\pi}}{\pi^2}\,
\frac{e^{-\mu}}{\mu^{3/2}}\left(1+O(\mu^{-1})\right)
\quad(\mu\to\infty).
}
\tag{3}
\]

The upper bound (2) is asymptotically sharp: the ratio of its right-hand side to \(A-H\) tends to 1.

## 2. Proof

For completeness, the modified-Bessel recurrences and derivative identities are

\[
K_0'(t)=-K_1(t),\qquad
K_1'(t)=-K_0(t)-\frac{K_1(t)}t,
\]

and yield the exact first-moment identity

\[
\int_0^\mu tG(t)\,dt=
\log(\mu/2)+\gamma+2K_0(\mu)-\mu K_0(\mu)K_1(\mu).
\tag{4}
\]

Indeed the derivative of the right-hand side is \(\mu G(\mu)\); the constant follows from \(K_0(t)=-\log(t/2)-\gamma+O(t^2|\log t|)\) and \(tK_1(t)=1+O(t^2|\log t|)\) as \(t\downarrow0\). For clarity, the normalization is verified directly. The rescaled occupied-band projector difference at parameter one has Fourier multiplier

\[
F_1(p)=-\frac12\left[\left(\frac{p}{\sqrt{p^2+1}}-\operatorname{sgn}p\right)\sigma_x+\frac1{\sqrt{p^2+1}}\sigma_z\right].
\]

Using \(\operatorname{Tr}(\sigma_a\sigma_b)=2\delta_{ab}\), its squared Frobenius norm is

\[
\|F_1(p)\|_F^2=1-\frac{|p|}{\sqrt{p^2+1}},\qquad
\int_{\mathbb R}\|F_1(p)\|_F^2\,dp=2.
\]

For the inverse transform \(\mathcal K_1(s)=(2\pi)^{-1}\int_{\mathbb R}e^{ips}F_1(p)\,dp\), the explicit Bessel kernel gives \(\|\mathcal K_1(s)\|_F^2=G(|s|)/(2\pi^2)\) for \(s\ne0\). Fourier–Plancherel therefore yields

\[
\frac1{\pi^2}\int_0^\infty G(t)\,dt
=\int_{\mathbb R}\|\mathcal K_1(s)\|_F^2\,ds
=\frac1{2\pi}\int_{\mathbb R}\|F_1(p)\|_F^2\,dp=\frac1\pi,
\]

so

\[
\boxed{\int_0^\infty G(t)\,dt=\pi.}
\tag{5}
\]

Equations (4)–(5), together with \(K_\nu(t)=O(e^{-t}t^{-1/2})\), establish \(A(\mu)-H(\mu)\to0\) as \(\mu\to\infty\). Differentiating the convergent integrals,

\[
\begin{aligned}
H'(\mu)&=\frac1\pi-\frac1{\pi^2}\int_\mu^\infty G(t)\,dt,\\
A'(\mu)&=\frac1\pi-\frac1{\pi^2\mu}.
\end{aligned}
\]

Since \(G(t)=t^{-2}-W(t)\), setting \(E=A-H\) gives

\[
E'(\mu)=-\frac1{\pi^2}\int_\mu^\infty W(t)\,dt,
\qquad E''(\mu)=\frac{W(\mu)}{\pi^2}.
\tag{6}
\]

The known vanishing of \(E\) at infinity and the exponential decay of \(W\) permit integration of (6) twice, giving the exact representation (1).

To prove its sign without numerical assumptions, use the standard representation

\[
K_\nu(t)=\int_0^\infty e^{-t\cosh u}\cosh(\nu u)\,du,
\qquad t>0,
\tag{7}
\]

which gives \(0<K_0(t)<K_1(t)\). Also \((tK_1(t))'=-tK_0(t)<0\), while \(\lim_{t\downarrow0}tK_1(t)=1\). Thus \(K_1(t)<1/t\), and hence

\[
0<W(t)=\frac{2K_1(t)}t-K_0(t)^2-K_1(t)^2
<\frac{2K_1(t)}t.
\tag{8}
\]

For \(t\ge\mu\), (7) and \(\cosh u\ge1\) imply

\[
K_1(t)\le e^{-(t-\mu)}K_1(\mu).
\tag{9}
\]

Using \(t^{-1}\le\mu^{-1}\) in (8), insert (9) into (1) and evaluate \(\int_0^\infty se^{-s}ds=1\). This proves (2), including strictness. Equation (6) yields \(E'<0\) and \(E''>0\).

Finally, the classical large-argument expansion for \(K_1\) gives

\[
W(t)=\sqrt{2\pi}\,e^{-t}t^{-3/2}\bigl(1+O(t^{-1})\bigr)
\qquad(t\to\infty),
\tag{10}
\]

because \(K_0(t)^2+K_1(t)^2=O(e^{-2t}t^{-1})\). Substitute \(t=\mu+s\) in (1), factor out \(e^{-\mu}\mu^{-3/2}\), and integrate against \(se^{-s}\). The uniform remainder estimate for \(t\ge\mu\) gives relative error \(O(\mu^{-1})\), proving (3). As (2) has the same leading equivalent, its ratio to the exact gap tends to 1. \(\square\)

**Further asymptotic consistency check.** The same integral representation also permits two additional inverse-mass coefficients:

\[
A(\mu)-H(\mu)=\frac{\sqrt{2\pi}}{\pi^2}\frac{e^{-\mu}}{\mu^{3/2}}\left(1-\frac{21}{8\mu}+\frac{1185}{128\mu^2}+O(\mu^{-3})\right).
\]

Indeed, the standard expansion $K_1(t)=\sqrt{\pi/(2t)}e^{-t}[1+3/(8t)-15/(128t^2)+O(t^{-3})]$ implies $W(t)=\sqrt{2\pi}e^{-t}t^{-3/2}[1+3/(8t)-15/(128t^2)+O(t^{-3})]+O(e^{-2t}/t)$. Setting $t=\mu+s$, expanding the remaining powers of $1+s/\mu$ in the exponentially weighted integral, and using $\int_0^\infty s^{j+1}e^{-s}ds=(j+1)!$ gives the stated coefficients. The expansion is justified by the uniform large-$t$ remainder and an integrable polynomial-times-$e^{-s}$ envelope for $s\ge0$ when $\mu$ is sufficiently large.


## 3. Computed checks

The following values are numerical checks of the exact formula, not ingredients of the proof. The gap is evaluated directly as the positive integral in (1), avoiding loss of precision through subtraction of two nearly equal large quantities.

| \(\mu\) | Exact-gap quadrature \(A-H\) | Global upper bound \(2K_1/(\pi^2\mu)\) | Gap divided by bound |
|---:|---:|---:|---:|
| 0.5 | \(5.49950703804\times10^{-2}\) | \(6.71330299650\times10^{-1}\) | 0.08192 |
| 2 | \(5.19873489905\times10^{-3}\) | \(1.41713766968\times10^{-2}\) | 0.36685 |
| 5 | \(1.03260959912\times10^{-4}\) | \(1.63922008668\times10^{-4}\) | 0.62994 |
| 10 | \(2.92623963802\times10^{-7}\) | \(3.77903159964\times10^{-7}\) | 0.77434 |
| 20 | \(5.19584664189\times10^{-12}\) | \(5.96078396912\times10^{-12}\) | 0.87167 |
| 40 | \(4.00735359517\times10^{-21}\) | \(4.30469733616\times10^{-21}\) | 0.93093 |

In particular the two-term expression \(A(\mu)\) is an *upper bound* for \(H(\mu)\) at every positive \(\mu\), not merely an asymptotic approximation for large \(\mu\).

## 4. Scope

The continuum function \(H\) arises after taking the interval-length limit \(L\to\infty\) with the scaling parameter \(\mu>0\) fixed. The subsequent \(\mu\to\infty\) asymptotic is a second limit; no uniform joint-limit assertion is made. This calculation does not determine the logarithmic coefficient or finite part of the complete Wilson–Dirac quasifree relative entropy, whose finite-part convergence remains a separate problem. The leading entropy law with bounded remainder follows from the separate estimates assembled in *Uniform Bulk Modular Asymptotics and the Leading Wilson Entropy Law*.

## References

1. National Institute of Standards and Technology, *Digital Library of Mathematical Functions*, §§10.29 (recurrences and derivatives), 10.31 (small-argument expansions), 10.32.9 (integral representation), and 10.40 (large-argument expansions): https://dlmf.nist.gov/10.29, https://dlmf.nist.gov/10.31, https://dlmf.nist.gov/10.32, https://dlmf.nist.gov/10.40.
2. H. Araki, “On Quasifree States of CAR and Bogoliubov Automorphisms,” *Publications of the Research Institute for Mathematical Sciences* **6** (1970/71), 385–442, doi:10.2977/prims/1195193913.
3. D. Slepian, “Prolate Spheroidal Wave Functions, Fourier Analysis, and Uncertainty—V: The Discrete Case,” *Bell System Technical Journal* **57** (1978), 1371–1430, doi:10.1002/j.1538-7305.1978.tb02104.x.

## Acknowledgments and contributions

Kirtus Justus directs the research and is the sole named human author. ChatGPT (OpenAI) assisted with the analytic derivation, numerical checks and manuscript drafting. Claude (Anthropic), Gemini (Google), Grok (SpaceXAI) and DeepSeek (High-Flyer) are acknowledged for their broader participation in the research workflow, without assigning unverified contributions to the present theorem. The work has not undergone external scholarly peer review. No institutional endorsement or AI-provider endorsement is implied.
