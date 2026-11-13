---
title: "Half-Filled Sine-Kernel Endpoint and Extreme Modular Discrepancy"
author: 'Kirtus Justus (Theoretical Physicist) \textbullet{} 31 October 2026\tabularnewline Port Coquitlam, British Columbia, Canada'
date: ''
lang: en
header-includes:
 - \usepackage{microtype,booktabs,longtable}
 - \setlength{\emergencystretch}{3em}
---

## Abstract

For the half-filled finite sine kernel and its commuting Jacobi matrix, we derive an exact integral formula and endpoint expansion for the reference scaling function, a Gaussian variational estimate for the largest Jacobi eigenvalue, and an exact Fourier-polynomial differential equation. The established fixed-index discrete-prolate concentration asymptotic determines the leading reference-modular discrepancy exactly, with limit $(\log\pi-1)/2$. This is a fixed-mode conclusion and does not supply a uniform reference-modular estimate for the complete Wilson relative entropy.

## 1. Reference operators and conventions

Let $N=2L$ and let the Hermitian $N\times N$ matrices $B_N,J_N$ have entries

$$
(B_N)_{jk}=\frac1{2\pi}\int_{-\pi/2}^{\pi/2}e^{i(j-k)\theta}\,d\theta,
\qquad (J_N)_{j,j+1}=(J_N)_{j+1,j}=\frac{(j+1)(N-j-1)}N,
$$

for $0\le j,k<N$, with all other entries of $J_N$ zero. They commute, $J_N$ has simple spectrum, and $0<B_N<I$. Set

$$K_N=\log(I-B_N)-\log B_N,\qquad E_N=K_N+N\eta(J_N/N),$$

where

$$\eta(t)=\sum_{n=0}^\infty \frac{\pi\binom{2n}{n}\binom{4n}{2n}}{(2n+1)16^n}t^{2n+1},\qquad |t|\le \tfrac12.$$

The finite sine-kernel model specifies the reference operator and its commuting Jacobi operator.

## 2. Exact integral and endpoint expansion

**Proposition 1.** For $|t|\le 1/2$,

$$\boxed{\eta(t)=4t\int_0^1\frac{\sqrt{1-u^2}}{\sqrt{1-4t^2u^4}}\,du.} \qquad\text{(2.1)}$$

In particular,

$$\eta(1/2)=2\operatorname{arsinh}1,\quad A_\eta:=\max_{0<|t|\le1/2}\frac{|\eta(t)|}{|t|}=4\operatorname{arsinh}1,$$

and

$$C_\eta:=\max_{0<|t|\le1/2}\frac{|\eta(t)-\pi t|}{|t|^3}=4(A_\eta-\pi).$$

*Proof.* Expand $(1-4t^2u^4)^{-1/2}=\sum_{n\ge0}\binom{2n}{n}t^{2n}u^{4n}$. The beta integral gives

$$\int_0^1u^{4n}\sqrt{1-u^2}\,du=\frac{\pi\binom{4n}{2n}}{4\,16^n(2n+1)},$$

which gives the stated coefficients. At the endpoint the majorant is integrable; monotone convergence applies to positive coefficients (the negative endpoint follows by oddness). For $t=1/2$, cancellation of $1-u^2$ against $1-u^4$ gives $2\int_0^1(1+u^2)^{-1/2}\,du$. The two maxima occur at the endpoint because the respective power series have nonnegative coefficients. $\square$

**Theorem 2.** As $\delta\downarrow0$,

$$\boxed{\eta'(1/2-\delta)=\frac1{\sqrt2}\log\frac1\delta+2\sqrt2\log2+o(1),} \qquad\text{(2.2)}$$

$$\boxed{\eta(1/2-\delta)=2\operatorname{arsinh}1-\frac\delta{\sqrt2}\log\frac1\delta-\frac{1+4\log2}{\sqrt2}\,\delta+o(\delta).} \qquad\text{(2.3)}$$

*Proof.* For $t<1/2$ differentiation under the integral gives

$$\eta'(t)=4\int_0^1\frac{\sqrt{1-u^2}}{(1-4t^2u^4)^{3/2}}\,du.$$

Set $\varepsilon=1-4t^2$, $y=1-u^2$. Then

$$\eta'(t)=2\int_0^1\frac{\sqrt y\,dy}{\sqrt{1-y}\,[\varepsilon+(1-\varepsilon)(2y-y^2)]^{3/2}}.$$

Subtract the singular model

$$I_\varepsilon=2\int_0^1\frac{\sqrt y}{(\varepsilon+2y)^{3/2}}\,dy
=\sqrt2\left[\operatorname{arsinh}\sqrt{2/\varepsilon}-\sqrt{\frac2{2+\varepsilon}}\right].$$

Its asymptotic is

$$I_\varepsilon=\frac1{\sqrt2}\log\frac1\varepsilon+\frac3{\sqrt2}\log2-\sqrt2+o(1).$$

Subtracting the two integrands before sending $\varepsilon\to0$ leaves an integrable function, uniformly bounded at $y=0$: expand the smooth factors near $y=0$ and use $y^2+\varepsilon y\lesssim(\varepsilon+y)^2$. The endpoint $y=1$ is integrable. Dominated convergence therefore gives the limiting difference

$$R=2\int_0^1\frac1y\left[\frac1{\sqrt{1-y}(2-y)^{3/2}}-\frac1{2^{3/2}}\right]dy.$$

With $u=\sqrt{1-y}$, this becomes

$$R=\int_0^1\left[\frac4{(1-u^2)(1+u^2)^{3/2}}-\frac{\sqrt2u}{1-u^2}\right]du.$$

The antiderivative, zero at $u=0$, is

$$2\frac{u}{\sqrt{1+u^2}}+\sqrt2\operatorname{artanh}\frac{\sqrt2u}{\sqrt{1+u^2}}+\frac1{\sqrt2}\log(1-u^2).$$

The logarithms cancel at $u=1$, giving $R=\sqrt2+(3/\sqrt2)\log2$. Consequently

$$\eta'(t)=\frac1{\sqrt2}\log\frac1\varepsilon+3\sqrt2\log2+o(1).$$

Since $t=1/2-\delta$ entails $\varepsilon=4\delta(1-\delta)$, this is (2.2). Integrating the derivative between $t$ and $1/2$, and using the endpoint value, yields (2.3). $\square$

## 3. Gaussian comparison for the top Jacobi eigenvalue

**Theorem 3.** Let $\lambda_N$ be the maximum eigenvalue of $J_N$ for even $N$. Then

$$\boxed{\lambda_N=\frac N2-\frac1{\sqrt2}+O(N^{-1}).} \qquad\text{(3.1)}$$

In addition, writing $\beta=\sqrt2$, every even $N\ge2$ obeys the explicit bound

$$\boxed{\lambda_N\le e^{-\beta/N}\left(\frac N2+\frac{6\cosh^2\beta}{5N}\right).} \qquad\text{(3.2)}$$

*Proof.* Write $x_j=j-(N-1)/2$ and choose $w_j=e^{-\beta x_j^2/N}>0$. Collatz–Wielandt gives $\lambda_N\le\max_j(J_Nw)_j/w_j$. An exact calculation with $y=2\beta x_j/N$ yields

$$\frac{(J_Nw)_j}{w_j}=e^{-\beta/N}\left[\frac N2\left(1-\frac{y^2}2\right)\cosh y-\frac{\cosh y}{2N}+\frac y\beta\sinh y\right].$$

The power series of $(1-y^2/2)\cosh y$ has no quadratic term, a quartic coefficient $-5/24$, and strictly negative higher even coefficients, so the expression is at most $1-5y^4/24$. Also $|y|\le\beta$ and $y\sinh y\le y^2\cosh\beta$. Hence

$$\frac{(J_Nw)_j}{w_j}\le e^{-\beta/N}\left[\frac N2-\frac{5N}{48}y^4+\frac{\cosh\beta}{\beta}y^2\right]
\le e^{-\beta/N}\left[\frac N2+\frac{6\cosh^2\beta}{5N}\right],$$

where the final step maximizes the displayed quadratic polynomial in $y^2\ge0$.

For the lower bound use the Rayleigh quotient of $w$. With $z_j=j+1-N/2$ for the bonds, an exact expression is

$$R_N=2e^{-\beta/(2N)}\frac{\sum_{j=0}^{N-2}(N/4-z_j^2/N)e^{-2\beta z_j^2/N}}{\sum_{j=0}^{N-1}e^{-2\beta x_j^2/N}}\le\lambda_N.$$

Both sums are truncated Gaussian lattice sums. Extending to the full integer and half-integer lattices incurs exponentially small errors (up to polynomial prefactors), since the first omitted points have magnitude proportional to $N$. Poisson summation then gives

$$\sum_{k\in\mathbb Z}e^{-2\beta(k+\rho)^2/N}=\sqrt{\frac{\pi N}{2\beta}}\left[1+O\left(e^{-\pi^2N/(2\beta)}\right)\right],\qquad \rho\in\{0,1/2\},$$

and the corresponding second Gaussian moment is $N/(4\beta)$ times the zeroth moment, up to exponentially small absolute relative errors. Therefore, for some $c>0$,

$$R_N=e^{-\beta/(2N)}\left(\frac N2-\frac1{2\beta}\right)+O(e^{-cN})
=\frac N2-\frac1{\sqrt2}+\frac3{8N}+O(N^{-2}).$$

Together with (3.2), which equals $N/2-1/\sqrt2+O(N^{-1})$, this proves (3.1). The $3/(8N)$ coefficient in the *lower bound* is not being asserted as the next coefficient of the true eigenvalue. $\square$

**Corollary 4.** Let $\lambda_N=\lambda_{\max}(J_N)$. Then

$$\boxed{N\eta(\lambda_N/N)=2N\operatorname{arsinh}1-\frac12\log N-\frac{1+\log(16\sqrt2)}2+o(1).} \qquad\text{(3.3)}$$

*Proof.* Set $\delta_N=1/2-\lambda_N/N=1/(\sqrt2N)+O(N^{-2})$ in Theorem 2. The $O(N^{-2})$ input error gives $o(1)$ after multiplication by $N$, since $\eta'$ grows only logarithmically. Simplification gives (3.3). $\square$

## 4. An exact generating-polynomial and Fourier-leakage formulation

**Theorem 5.** Let $J_Nv=\lambda v$ for a nonzero real vector $v=(v_0,\dots,v_{N-1})$ and define the polynomial $F(z)=\sum_{j=0}^{N-1}v_jz^j$. It satisfies the exact differential equation

$$\boxed{-z(1+z^2)F''(z)+[(N-1)+(N-3)z^2]F'(z)+[(N-1)z-N\lambda]F(z)=0.} \qquad\text{(4.1)}$$

If $b=v^*B_Nv/\lVert v\rVert^2$, then

$$\boxed{\frac{1-b}{b}=\frac{\int_{\pi/2<|\theta|\le\pi}|F(e^{i\theta})|^2\,d\theta}{\int_{-\pi/2}^{\pi/2}|F(e^{i\theta})|^2\,d\theta}.} \qquad\text{(4.2)}$$

For the top eigenpair, $v$ may be chosen strictly positive and symmetric under $j\mapsto N-1-j$; consequently $F(z)=z^{N-1}F(1/z)$.

*Proof.* The recurrence $N\lambda v_j=(j+1)(N-j-1)v_{j+1}+j(N-j)v_{j-1}$ is understood with $v_{-1}=v_N=0$. Multiply by $z^j$ and sum over $j$. The shifted sums give $(N-1)F'-zF''$ and $(N-1)zF+(N-3)z^2F'-z^3F''$, respectively, proving (4.1). Equation (4.2) follows directly from the Fourier projection formula for $B_N$ and Parseval. Positivity and strict Perron simplicity hold because all Jacobi off-diagonal entries are positive; reflection commutes with $J_N$, hence the top vector is symmetric. $\square$

**Fourier-leakage identity and endpoint criterion.** Let $v_N$ be the top normalized Jacobi eigenvector, and write $I_N^{\rm in}$ and $I_N^{\rm out}$ for the two integrals in (4.2). Its scalar modular discrepancy is

$$e_N^{\rm edge}=\log\frac{I_N^{\rm out}}{I_N^{\rm in}}+N\eta(\lambda_N/N).$$

By (3.3), **boundedness of this one edge discrepancy** is equivalent to

$$\boxed{\frac{I_N^{\rm out}}{I_N^{\rm in}}=\sqrt N\,e^{-2N\operatorname{arsinh}1+O(1)}.} \qquad\text{(4.3)}$$

The $O(1)$ is in the logarithm and means two-sided multiplicative bounds independent of $N$. The fixed-index concentration asymptotic in the next section establishes this criterion for the leading mode. It does not provide uniform control over eigenvalue indices that grow with $N$.


## 5. Extreme modular discrepancy from classical discrete-prolate concentration

**Theorem 6 (application of the classical discrete-prolate fixed-index asymptotic).** In the preceding half-filled normalization,

\[
\boxed{1-b_N\sim\sqrt\pi\,2^{9/4}\sqrt N\,e^{-2N\operatorname{arsinh}(1)}.}\qquad\text{(5.1)}
\]

Consequently,

\[
\boxed{\lim_{\substack{N\to\infty\\N\ \mathrm{even}}}e_N=\frac{\log\pi-1}{2}.}\qquad\text{(5.2)}
\]

In particular, the discrepancy for the **single top Jacobi eigenmode** is bounded uniformly over even $N\ge2$.

*Proof.* The classical discrete-prolate concentration matrix is

\[
P(N,W)_{jk}=\begin{cases}\frac{\sin(2\pi W(j-k))}{\pi(j-k)},&j\ne k,\\2W,&j=k.\end{cases}
\]

It equals \(B_N\) for \(W=1/4\). The fixed-index eigenvalue asymptotic of Slepian (1978), explicitly transcribed in Adcock, Huybrechs and Martín-Vaquero, *On the numerical stability of Fourier extensions*, §3.2, equation (3.10), states for \(k=0\),

\[
1-b_N\sim \sqrt\pi\,2^{9/4}\alpha^{1/4}(2-\alpha)^{-1/2}\sqrt N\,\beta^{-N},
\quad \alpha=1-\cos(2\pi W),\quad
\beta=\frac{\sqrt2+\sqrt\alpha}{\sqrt2-\sqrt\alpha}.
\]

At \(W=1/4\), \(\alpha=1\), while \(\beta=3+2\sqrt2=\exp(2\operatorname{arsinh}1)\). This proves (5.1). Since \(b_N\to1\), its odds satisfy

\[
\log\frac{1-b_N}{b_N}=-2N\operatorname{arsinh}(1)+\frac12\log N+\log(\sqrt\pi 2^{9/4})+o(1).
\]

Adding the Jacobi-edge expansion (3.3) and simplifying the constants proves (5.2). A convergent sequence is bounded for sufficiently large N; the finitely many remaining even N have finite discrepancies since \(0<b_N<1\). $\square$

**Source attribution.** The concentration-eigenvalue asymptotic used here is due to Slepian and is reproduced by Adcock, Huybrechs and Martín-Vaquero. This is an application of their theorem, not an independent proof of it. The source's theorem applies to fixed eigenvalue index and fixed bandwidth; no uniformity in an index growing with N has been imported. The proof of Slepian’s original asymptotic is not reproduced here.


## 6. Exact real angular equation

Let \(J_Nv=\lambda v\), \(F(z)=\sum_{j=0}^{N-1}v_jz^j\), and \(\phi(\theta)=e^{-i(N-1)\theta/2}F(e^{i\theta})\). Summing the Jacobi recurrence gives

\[
-z(1+z^2)F''+[(N-1)+(N-3)z^2]F'+[(N-1)z-N\lambda]F=0.
\]

**Proposition 7.** Every generating polynomial satisfies

\[
\boxed{\frac{d}{d\theta}\big(\cos\theta\,\phi'(\theta)\big)+\left[\frac{N^2-1}{4}\cos\theta-\frac{N\lambda}{2}\right]\phi(\theta)=0.}\qquad\text{(6.1)}
\]

*Proof.* On the unit circle \(z\partial_z=-i\partial_\theta\). Substitute \(F(e^{i\theta})=e^{i(N-1)\theta/2}\phi(\theta)\) into the displayed polynomial equation, collect terms in \(\phi''\), \(\phi'\), and \(\phi\), and divide by two. The resulting expression is (6.1). This algebra is independent of any asymptotic approximation. $\square$

For the top eigenvector, reflection symmetry makes \(\phi\) real and even. For even N, palindromicity of odd polynomial degree implies \(\phi(\pi)=0\), and (6.1) at the band edge gives

\[
\phi'(\pi/2)=-\frac{N\lambda_N}{2}\phi(\pi/2).\qquad\text{(6.2)}
\]

Multiplying (6.1) by \(\phi\) and integrating by parts gives the exact exterior identity

\[
\boxed{\int_{\pi/2}^{\pi}|\cos\theta|\,\phi'(\theta)^2\,d\theta
=\int_{\pi/2}^{\pi}\left[\frac{N^2-1}{4}|\cos\theta|+\frac{N\lambda_N}{2}\right]\phi(\theta)^2\,d\theta.}\qquad\text{(6.3)}
\]

The analogous interior formula over \([0,\pi/2]\) has \(\cos\theta\) instead of its absolute value and the minus sign preceding \(N\lambda_N/2\). Neither identity supplies a two-sided exterior mass estimate by itself.


## 7. Exact action and asymptotic interpretation

The leading interior normal-form action computed from (6.1) is

\[
\mathcal A=\frac12\int_0^{\pi/2}\sqrt{\sec\theta-1}\,d\theta=\operatorname{arsinh}(1).
\]

Indeed, with \(t=\tan(\theta/2)\) and then \(u=\sqrt{1-t^2}\), the integral becomes \(\sqrt2\int_0^1(2-u^2)^{-1}du=\operatorname{artanh}(1/\sqrt2)=\operatorname{arsinh}(1)\).

This matches the exponential action in the classical theorem (5.1). It is an exact evaluation of a leading formal action, **not** a standalone rigorous derivation of the prolate eigenvalue prefactor. In particular, the behavior at the singular band edge and the central turning point requires controlled connection formulas if one seeks a direct ODE proof.

## 8. Scope and limitations

The fixed-index theorem controls only the highest Jacobi eigenvector and its paired sine-kernel occupation. It cannot be extended to an index growing with $N$ without new estimates. The commuting sine-kernel/Jacobi spectrum includes central, transitional, and other edge regions that are not bounded by the single-mode result.

For the Wilson–Dirac interval problem the established reduction is

$$
\mathcal D_L(\mu)=\frac{\mu^2}{6}\log L+\operatorname{Tr}(S_NE_N)+O_\mu(\sqrt{\log L}),\qquad N=2L.
$$

Neither the scalar endpoint expansion nor the Slepian fixed-index result alone establishes the leading coefficient or finite part of the complete relative entropy. The separate argument in *Uniform Bulk Modular Asymptotics and the Leading Wilson Entropy Law* gives $\operatorname{Tr}(S_NE_N)=O_\mu(1)$ and the leading entropy coefficient; it does not establish the entropy finite part or an expansion uniform up to the spectral edge.

## References

- D. Slepian, “Prolate Spheroidal Wave Functions, Fourier Analysis, and Uncertainty V: The Discrete Case,” *Bell System Technical Journal* **57** (1978), 1371–1430. DOI: 10.1002/j.1538-7305.1978.tb02104.x.
- B. Adcock, D. Huybrechs, and J. Martín-Vaquero, “On the Numerical Stability of Fourier Extensions,” *Foundations of Computational Mathematics* **14** (2014), 635–687, §3.2, equation (3.10). DOI: 10.1007/s10208-013-9158-8.
- V. Eisler and I. Peschel, “Analytical Results for the Entanglement Hamiltonian of a Free-Fermion Chain,” *Journal of Physics A* **50** (2017), 284003. DOI: 10.1088/1751-8121/aa76b5.

## Contributions and acknowledgments

Kirtus Justus directed the research and determined the scientific scope. ChatGPT (OpenAI) derived and checked the scalar endpoint and Jacobi spectral-edge results, identified the precise classical discrete-prolate theorem for the fixed-index concentration asymptotic, and prepared the mathematical synthesis. The Slepian asymptotic is attributed to its original source; it is not claimed as an original result. Claude (Anthropic), Gemini (Google), Grok (SpaceXAI), and DeepSeek (High-Flyer) are acknowledged for broader research participation without attributing verification of these calculations to them. No external peer review, degree, academic affiliation or institutional endorsement is claimed.
