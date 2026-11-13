---
title: "Fourier-Space Boundary Defects for Wilson-Dirac Covariances"
author: 'Kirtus Justus \textbullet{} Theoretical Physicist \textbullet{} 23 October 2026\tabularnewline Port Coquitlam, British Columbia, Canada'
date: ''
lang: en
header-includes:
 - \usepackage{microtype}
 - \usepackage{booktabs}
 - \usepackage{longtable}
---

## Abstract

For the compression of a self-adjoint, translation-invariant operator to a finite interval, we prove a Fourier-coefficient identity for the exact Hilbert–Schmidt boundary defect. It gives a positive spatial-separation formula and discrete monotonicity and concavity with respect to interval length when the operator is fixed. Applied to the Wilson–Dirac occupied-band projector difference, this formulation gives another derivation of the boundary-leakage identity. For the continuum scaling function, we obtain global derivative bounds and a higher-order large-mass expansion of the signed exponential remainder. The interval-length scaling limit remains dependent on the separately established Hilbert–Schmidt convergence result.

## 1. A general Fourier-coefficient identity

Let \(T\) be a bounded self-adjoint translation-invariant operator on \(\ell^2(\mathbb Z;\mathbb C^q)\), with block kernel \(T_d\in\mathbb C^{q\times q}\):

\[
(Tf)_a=\sum_{b\in\mathbb Z}T_{a-b}f_b,\qquad T_{-d}=T_d^*.
\]

Here the action is initially interpreted using its bounded Fourier multiplier; the sum of squared Frobenius norms \(\sum_d\|T_d\|_F^2\) is finite by Plancherel. Let \(\chi_L\) be projection onto sites \(0,\ldots,L-1\), and let \(Q_L=I-\chi_L\).

**Theorem 1 (exact Fourier boundary defect).** For every positive integer \(L\),

\[
\boxed{\operatorname{Tr}(\chi_LT^2\chi_L)-\|\chi_LT\chi_L\|_{\mathrm{HS}}^2
=\|Q_LT\chi_L\|_{\mathrm{HS}}^2
=\sum_{d\in\mathbb Z}\min\{|d|,L\}\,\|T_d\|_F^2.}
\tag{1}
\]

*Proof.* Translation invariance and self-adjointness give

\[
\operatorname{Tr}(\chi_LT^2\chi_L)=L\sum_{d\in\mathbb Z}\|T_d\|_F^2.
\]

The number of ordered pairs \((a,b)\) with \(a,b\in\{0,\ldots,L-1\}\) and \(a-b=d\) is \(L-|d|\) when \(|d|<L\), and zero otherwise. Consequently,

\[
\|\chi_LT\chi_L\|_{\mathrm{HS}}^2
=\sum_{|d|<L}(L-|d|)\|T_d\|_F^2.
\]

Subtracting gives the last expression in (1). Independently, inserting \(I=\chi_L+Q_L\) between the two copies of \(T\) gives

\[
\chi_LT^2\chi_L-(\chi_LT\chi_L)^2=\chi_LTQ_LT\chi_L
=(Q_LT\chi_L)^*(Q_LT\chi_L).
\]

Its trace proves the middle equality and positivity. \(\square\)

**Corollary 2 (discrete concavity for a fixed operator).** Write \(\mathfrak L_L(T)\) for the quantity in (1), and put \(\mathfrak L_0(T)=0\). For fixed \(T\),

\[
\boxed{\mathfrak L_{L+1}(T)-\mathfrak L_L(T)
=\sum_{|d|\ge L+1}\|T_d\|_F^2\ge0,}
\tag{2}
\]

\[
\boxed{\mathfrak L_{L+2}(T)-2\mathfrak L_{L+1}(T)+\mathfrak L_L(T)
=-\sum_{|d|=L+1}\|T_d\|_F^2\le0.}
\tag{3}
\]

Both follow by taking first and second differences of \(\min(L,|d|)\). The operator must be fixed when changing \(L\); neither assertion automatically applies to a sequence of operators whose masses vary with interval length.

## 2. Wilson–Dirac specialization

For the negative-energy projector of the original two-orbital Wilson–Dirac Bloch symbol,

\[
h_m(k)=\sin k\,\sigma_x+(1+m-\cos k)\sigma_z,
\quad P_m(k)=\tfrac12\left[I-\frac{h_m(k)}{\sqrt{m^2+4(1+m)\sin^2(k/2)}}\right],
\]

put \(T^{(m)}=P_m-P_0\) as a full-line operator, and denote its Fourier coefficients by \(T_d^{(m)}\). The interval compression is precisely the covariance difference used in the research program. Hence Theorem 1 gives the exact all-length identity

\[
\boxed{\operatorname{Tr}G_L-\|\Delta_L\|_{\mathrm{HS}}^2
=\sum_{d\in\mathbb Z}\min(L,|d|)\,\|T_d^{(m)}\|_F^2,}
\tag{4}
\]

where \(G_L=\chi_L(T^{(m)})^2\chi_L\). This holds for every \(m>0\), including the scaling choice \(m=\mu/L\). The representation makes clear that only nonzero spatial separations contribute to leakage. It is independent of the finite Jacobi basis and the modular spectral approximation.

For fixed \(\mu>0\), the separately established Hilbert–Schmidt convergence statement and the exact trace limit yield

\[
\lim_{L\to\infty}\mathfrak L_L(T^{(\mu/L)})=\Lambda(\mu)
=\frac1{\pi^2}\int_0^\infty\min(t,\mu)\Phi(t)\,dt,
\]

with \(\Phi(t)=K_0(t)^2+[K_1(t)-t^{-1}]^2\). Equation (4) supplies an alternative exact finite representation, not a replacement proof of the already stated finite-to-continuum sampling theorem.

**Continuum Fourier normalization.** With the inverse Fourier convention
$\check F(x)=(2\pi)^{-1}\int_{\mathbb R}e^{iux}F(u)\,du$, define
\[
F_\mu(u)=-\frac12\left[
\left(\frac{u}{\sqrt{u^2+\mu^2}}-\operatorname{sgn}u\right)\sigma_x
+\frac{\mu}{\sqrt{u^2+\mu^2}}\sigma_z\right].
\]
The Pauli trace identity gives
$\|F_\mu(u)\|_F^2=1-|u|/\sqrt{u^2+\mu^2}$ and
$(2\pi)^{-1}\int_{\mathbb R}\|F_\mu(u)\|_F^2du=\mu/\pi$.
The standard modified-Bessel Fourier transforms give, for $x\ne0$,
\[
\|\check F_\mu(x)\|_F^2
=\frac1{2\pi^2}\left[\mu^2K_0(\mu|x|)^2+
\left(\mu K_1(\mu|x|)-\frac1{|x|}\right)^2\right].
\]
Plancherel, evenness and the substitution $t=\mu|x|$ consequently prove
\[
\boxed{\int_0^\infty\Phi(t)\,dt=\pi.}
\]
This normalization makes the identity
$\Lambda(\mu)=\mu/\pi-H(\mu)=\pi^{-2}\int_0^\infty\min(t,\mu)\Phi(t)dt$
explicit; the finite-to-continuum limit itself is supplied by the separate
Hilbert–Schmidt scaling theorem.


## 3. Global differential bounds and a sharper remainder expansion

Let

\[
C(\mu)=\frac{\log(\mu/2)+\gamma+1}{\pi^2},\qquad
W(t)=\frac{2K_1(t)}t-K_0(t)^2-K_1(t)^2.
\]

Standard Bessel identities imply \(0<K_0(t)<K_1(t)<1/t\), so \(W(t)>0\) and

\[
\Phi(t)=\frac1{t^2}-W(t),\qquad 0<\Phi(t)<\frac1{t^2}.
\tag{5}
\]

The normalization constant is fixed directly: the Bessel derivative identities give
\[
\frac{d}{dt}\{-tK_0(t)K_1(t)+2K_0(t)+\log t\}=t\Phi(t).
\]
The expression in braces tends to $\log2-\gamma$ as $t\downarrow0$, and differs from $\log t$ by an exponentially decaying term at infinity. Combining this antiderivative with $\int_0^\infty\Phi(t)dt=\pi$ proves the exact signed-remainder representation

\[
R(\mu):=\Lambda(\mu)-C(\mu)
=\frac1{\pi^2}\int_\mu^\infty(t-\mu)W(t)\,dt>0.
\tag{6}
\]

**Proposition 3 (derivative bounds).** For all \(\mu>0\),

\[
\boxed{0<\Lambda'(\mu)<\frac1{\pi^2\mu},\qquad
-\frac1{\pi^2\mu^2}<\Lambda''(\mu)<0.}
\tag{7}
\]

Moreover \(R'(\mu)<0\), \(R''(\mu)>0\). Indeed,

\[
\Lambda'(\mu)=\frac1{\pi^2}\int_\mu^\infty\Phi(t)dt,
\quad\Lambda''(\mu)=-\frac{\Phi(\mu)}{\pi^2},
\quad R'(\mu)=-\frac1{\pi^2}\int_\mu^\infty W(t)dt,
\quad R''(\mu)=\frac{W(\mu)}{\pi^2}.
\]

The strictly positive inequalities follow from (5) and (6). \(\square\)

**Proposition 4 (three-term exponential equivalent).** As \(\mu\to\infty\),

\[
\boxed{R(\mu)=\frac{\sqrt{2\pi}}{\pi^2}\frac{e^{-\mu}}{\mu^{3/2}}
\left[1-\frac{21}{8\mu}+\frac{1185}{128\mu^2}+O(\mu^{-3})\right].}
\tag{8}
\]

*Proof.* The standard Bessel expansion gives

\[
K_1(t)=\sqrt{\frac\pi{2t}}e^{-t}
\left[1+\frac3{8t}-\frac{15}{128t^2}+O(t^{-3})\right].
\]

The squares \(K_0(t)^2+K_1(t)^2=O(e^{-2t}/t)\) make an exponentially smaller contribution. Therefore

\[
W(t)=\sqrt{2\pi}\,e^{-t}t^{-3/2}
\left[1+\frac3{8t}-\frac{15}{128t^2}+O(t^{-3})\right]
+O(e^{-2t}/t).
\]

In (6), substitute \(t=\mu+s\), expand uniformly under the integrable majorant \(s e^{-s}\) and use \(\int_0^\infty s^j e^{-s}ds=j!\). The \(\mu^{-1}\) coefficient is \(3/8-(3/2)\cdot2=-21/8\). The \(\mu^{-2}\) coefficient is

\[
\frac{15}{8}\cdot6-\frac{15}{16}\cdot2-\frac{15}{128}=\frac{1185}{128}.
\]

The uniform higher-order remainder and exponentially small squared-Bessel contribution give the stated error. \(\square\)

## 4. Scope

These results apply to a specified translation-invariant covariance difference, together with the continuum scaling function in *Hilbert-Schmidt Scaling Limit for Wilson-Dirac Covariances*. They are not statements about the full quasifree relative entropy. That comparison additionally uses nonlinear, modular and cross-boundary estimates: the complete fixed-$\mu$ assembly is Theorem 1 and Section 7 of *Finite Part of Wilson–Dirac Relative Entropy*, with sharpened modular and nonlinear bounds in *Uniform Modular Control and Nonlinear Convergence for Wilson–Dirac Intervals*. In particular, the discrete concavity in (3) is **only** a fixed-operator statement.

## References

1. NIST Digital Library of Mathematical Functions, §§10.29, 10.32, 10.40, https://dlmf.nist.gov/10.29, https://dlmf.nist.gov/10.32, https://dlmf.nist.gov/10.40.
2. V. Eisler and I. Peschel, “Analytical results for the entanglement Hamiltonian of a free-fermion chain,” *J. Phys. A* **50** (2017), 284003, doi:10.1088/1751-8121/aa76b5.

## Acknowledgments and contributions

Kirtus Justus directs the research and is the sole named human author. ChatGPT (OpenAI) prepared this proof draft and carried out the numerical reconstruction. Claude (Anthropic), Gemini (Google), Grok (SpaceXAI), and DeepSeek (High-Flyer) are acknowledged as participants in the broader project without assigning specific contributions to this note absent verifiable provenance. No external peer review or institutional endorsement is claimed.
