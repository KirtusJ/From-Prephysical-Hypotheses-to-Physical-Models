---
title: "A Hilbert--Schmidt Scaling Limit for Finite-Interval Wilson--Dirac Covariances"
author: 'Kirtus Justus \textbullet{} Theoretical Physicist \textbullet{} 23 October 2026\tabularnewline Port Coquitlam, British Columbia, Canada'
date: ''
lang: en
header-includes:
 - \usepackage{microtype}
 - \usepackage{amsmath,amssymb,amsthm}
 - \usepackage{booktabs}
---

**Abstract.** For the restrictions of two infinite-chain Wilson--Dirac occupied-band projections to an interval of $L$ cells, we establish a Hilbert--Schmidt scaling limit when the massive parameter is $m=\mu/L$ with fixed $\mu>0$. The limiting integral operator on $L^2(0,1;\mathbb C^2)$ has an explicitly computable modified-Bessel kernel. A dimension-free lower bound for the finite quasifree relative entropy then gives a strictly positive limiting lower benchmark, without a spectral-mode localization hypothesis. The benchmark is an increasing, strictly convex function of $\mu$; its small-mass expansion and large-mass slope are explicit. The arguments use only the occupied-band symbol, Fourier--Plancherel theory, and finite-matrix convexity.

**Keywords:** Wilson--Dirac chain; quasifree fermions; Hilbert--Schmidt convergence; quantum relative entropy; Bessel functions; Toeplitz compression.

## 1. Model and result

Write $\sigma_x,\sigma_z$ for the Pauli matrices and fix $\mu>0$. For $m\ge0$ and $k\in[-\pi,\pi]$, put
$$
h_m(k)=\sin k\,\sigma_x+(1+m-\cos k)\,\sigma_z,
\qquad E_m(k)=\sqrt{m^2+4(1+m)\sin^2(k/2)}.
$$
The infinite-chain occupied-band multiplier is $P_m(k)=\tfrac12(I-h_m(k)/E_m(k))$. Its value at $k=m=0$ may be specified arbitrarily, since a single Fourier point is immaterial. Let $C_{L,m}$ be the block Toeplitz compression to $L$ consecutive two-orbital cells,
$$
(C_{L,m})_{jk}=\frac1{2\pi}\int_{-\pi}^{\pi}e^{i(j-k)\theta}P_m(\theta)\,d\theta,
\qquad 0\le j,k<L.
$$
We compare the massive and massless compressions at $m=\mu/L$:
$$
A_L=C_{L,\mu/L},\qquad B_L=C_{L,0},\qquad \Delta_L=A_L-B_L.
$$
The finite compressed covariances satisfy $0<C_{L,m}<I$ for every $m\ge0$. To see this, suppose that a nonzero finitely supported vector has zero quadratic form under $C_{L,m}$ or $I-C_{L,m}$. Its nonzero vector-valued Laurent polynomial $v(z)$, with $z=e^{ik}$, would then satisfy $h_m(k)v(z)=\pm E_m(k)v(z)$ almost everywhere. A nonzero component forces $E_m(k)$ to agree there with a rational function of $z$. But
$$
E_m(k)^2=m^2+2(1+m)-(1+m)(z+z^{-1})
$$
has a pole of odd order at $z=0$, whereas the square of a rational function has only poles of even order. This contradiction proves both strict inequalities.

The trace convention $\|M\|_2^2=\operatorname{Tr}(M^*M)$ is **un-normalized**, and the logarithms in the relative entropy are natural. Define
$$
\mathcal D_L(\mu)=\operatorname{Tr}\{A_L(\log A_L-\log B_L)
+(I-A_L)[\log(I-A_L)-\log(I-B_L)]\}.
$$
This is the relative entropy of the corresponding finite gauge-invariant quasifree states.

**Theorem 1 (Covariance scaling and relative-entropy bound).** For fixed $\mu>0$, the matrices $\Delta_L$ have a Hilbert--Schmidt continuum limit after the canonical piecewise-constant embedding of the $L$ cells into $(0,1)$. Its kernel for $s=x-y\ne0$ is
$$
\mathcal K_\mu(s)=
\frac{i}{2\pi}\left[\frac1s-\mu\,\operatorname{sgn}(s)K_1(\mu|s|)\right]\sigma_x
-\frac{\mu}{2\pi}K_0(\mu|s|)\sigma_z.
\tag{1}
$$
In particular,
$$
\boxed{\lim_{L\to\infty}\|\Delta_L\|_2^2=H(\mu)
=\frac1{\pi^2}\int_0^1(1-s)\left\{\mu^2K_0(\mu s)^2+
\left[\frac1s-\mu K_1(\mu s)\right]^2\right\}ds.}
\tag{2}
$$
The associated relative entropy obeys
$$
\boxed{\liminf_{L\to\infty}\mathcal D_L(\mu)\ge2H(\mu)>0.}
\tag{3}
$$

The additional estimates in *Uniform Bulk Modular Asymptotics and the Leading Wilson Entropy Law* establish the relative entropy's leading logarithmic coefficient with bounded remainder. Equation (3) is a separate all-mass, fixed-$\mu$ lower benchmark that can be evaluated without using that theorem.

## 2. Proof of the Hilbert--Schmidt limit

**Lemma 2 (Rescaled Fourier multipliers).** Set
$$
F_L(t)=\mathbf1_{[-\pi L,\pi L]}(t)
\big[P_{\mu/L}(t/L)-P_0(t/L)\big].
$$
As $L\to\infty$, $F_L\to F_\mu$ in $L^2(\mathbb R;M_2(\mathbb C))$, where, for $t\ne0$,
$$
F_\mu(t)=-\frac12\left\{
\left[\frac{t}{\sqrt{t^2+\mu^2}}-\operatorname{sgn}t\right]\sigma_x
+\frac\mu{\sqrt{t^2+\mu^2}}\sigma_z\right\}.
\tag{4}
$$
Moreover $\|tF_L\|_{L^2(\mathbb R;\mathrm{F})}^2=O_\mu(L)$.

*Proof.* For fixed $t\ne0$, use $L\sin(t/L)\to t$ and $L(1-\cos(t/L))\to0$ in the normalized Bloch vector. The massless $\sigma_x$ component tends to $\operatorname{sgn}t$, while its $\sigma_z$ component tends to zero, giving (4).

For $k\ne0$ in the Brillouin zone, the vector $h_m(k)$ has length $E_m(k)\ge E_0(k)=2|\sin(k/2)|\ge2|k|/\pi$. Differentiating its normalized direction with respect to $m$ gives a Euclidean norm at most $1/E_m(k)$. The mean-value bound for the difference of the two rank-one spectral projections, supplemented by the elementary uniform bound for differences of projections, therefore gives
$$
\|F_L(t)\|_{\mathrm F}\le C\min\left\{1,\frac\mu{|t|}\right\}
\quad(t\ne0),
\tag{5}
$$
with $C$ independent of $L$ and $\mu$. The right side is square-integrable in $t$ for fixed $\mu>0$ and also bounds $F_\mu$. Dominated convergence proves the $L^2$ assertion. Finally $|t|\|F_L(t)\|_{\mathrm F}\le C\mu$ on its support, an interval of length $2\pi L$, so the stated weighted $L^2$ bound follows. $\square$

Let
$$
K_L(s)=\frac1{2\pi}\int_{\mathbb R}e^{its}F_L(t)\,dt,
\qquad K_\mu=\mathcal F^{-1}F_\mu
$$
using the same Fourier normalization. Plancherel and Lemma 2 imply
$$
\|K_L-K_\mu\|_{L^2(\mathbb R;\mathrm F)}\longrightarrow0,
\qquad
\|K_L'\|_{L^2(\mathbb R;\mathrm F)}^2=O_\mu(L).
\tag{6}
$$
In particular $K_L\in H^1(\mathbb R;M_2)$ has a continuous representative, so its lattice samples are well-defined.

**Lemma 3 (Sampling does not change the limit).** Map the standard basis of $\mathbb C^L$ into $L^2(0,1)$ by $e_j\mapsto\sqrt L\,\mathbf1_{[j/L,(j+1)/L)}$. Under its tensor product with $I_{\mathbb C^2}$, the finite covariance difference becomes an integral operator with kernel
$$
M_L(x,y)=K_L\!\left(\frac{\lfloor Lx\rfloor-\lfloor Ly\rfloor}{L}\right).
$$
Then $\|M_L-K_\mu(x-y)\|_{L^2((0,1)^2;\mathrm F)}\to0$.

*Proof.* The exact block Fourier formula, after $t=L\theta$, gives $(\Delta_L)_{jk}=L^{-1}K_L((j-k)/L)$, which establishes the displayed kernel. If $x$ and $y$ belong to the $j$th and $k$th cells, let $s_0=(j-k)/L$ and $s=x-y$. Then $|s-s_0|\le1/L$, and the fundamental theorem of calculus and Cauchy--Schwarz give
$$
\|K_L(s)-K_L(s_0)\|_{\mathrm F}^2\le
\frac1L\int_{s_0-1/L}^{s_0+1/L}\|K_L'(u)\|_{\mathrm F}^2du.
$$
Each pair of cells has area $L^{-2}$; for each difference $d=j-k$, there are $L-|d|$ pairs, and the intervals $[(d-1)/L,(d+1)/L]$ overlap at most threefold. Consequently,
$$
\|M_L-K_L(x-y)\|_{L^2((0,1)^2;\mathrm F)}^2
\le\frac3{L^2}\|K_L'\|_{L^2(\mathbb R;\mathrm F)}^2=O_\mu(L^{-1}).
$$
Also
$$
\int_0^1\!\int_0^1\|K_L(x-y)-K_\mu(x-y)\|_{\mathrm F}^2dx\,dy
=\int_{-1}^{1}(1-|s|)\|K_L(s)-K_\mu(s)\|_{\mathrm F}^2ds
\le\|K_L-K_\mu\|_{L^2(\mathbb R;\mathrm F)}^2.
$$
Equation (6) completes the proof. $\square$

**Lemma 4 (Modified-Bessel kernel).** For $s\ne0$, $K_\mu(s)$ is given by (1).

*Proof.* The cosine transform
$$
\int_0^\infty\frac{\cos(ts)}{\sqrt{t^2+\mu^2}}dt=K_0(\mu|s|)
$$
and $K_0'(z)=-K_1(z)$ give the Fourier transform of $t/\sqrt{t^2+\mu^2}$ by differentiation. The Fourier transform of $\operatorname{sgn}t$ is $i/(\pi s)$ in the tempered-distribution sense with the present sign convention. Their difference lies in $L^2$; the singular terms cancel when combined. The $\sigma_z$ component is the ordinary even cosine transform. Substitution into (4) yields (1). $\square$

*Proof of the limit (2).* The $K_0(\mu|s|)$ component has a logarithmic singularity at $s=0$; the coefficient of $\sigma_x$ vanishes there at rate $O_\mu(s|\log|s||)$. Thus the kernel is locally square-integrable. Orthogonality of the Pauli matrices under the Frobenius inner product yields
$$
\|K_\mu(s)\|_{\mathrm F}^2=\frac1{2\pi^2}
\left\{\left[\frac1s-\mu\operatorname{sgn}(s)K_1(\mu|s|)\right]^2
+\mu^2K_0(\mu|s|)^2\right\}.
$$
Lemma 3 gives convergence of the embedded operators in Hilbert--Schmidt norm. Integrating over the unit square, using $\int_0^1\int_0^1f(x-y)dxdy=\int_{-1}^1(1-|s|)f(s)ds$, proves (2). $\square$

## 3. Finite-dimensional entropy inequality

**Proposition 5 (Sharp covariance Hilbert--Schmidt bound).** If $0<A,B<I$ are finite Hermitian matrices of the same size, then
$$
\mathcal D(A\Vert B)\ge2\operatorname{Tr}(A-B)^2.
\tag{7}
$$
The coefficient $2$ cannot be increased uniformly over all such matrices.

*Proof.* Let $f(u)=u\log u+(1-u)\log(1-u)$ on $(0,1)$, and put $V=A-B$, $B_t=B+tV$, and $g(t)=\operatorname{Tr}f(B_t)$. Direct rearrangement of the trace entropy gives $\mathcal D(A\Vert B)=g(1)-g(0)-g'(0)$. Diagonalize $B_t$ with eigenvalues $\lambda_i(t)$. Differentiation of a trace spectral function gives
$$
g''(t)=\sum_{i,j}|V_{ij}^{(t)}|^2
\begin{cases}
\displaystyle\frac{f'(\lambda_i)-f'(\lambda_j)}{\lambda_i-\lambda_j},&\lambda_i\ne\lambda_j,\\[6pt]
f''(\lambda_i),&\lambda_i=\lambda_j.
\end{cases}
$$
This divided-difference identity is valid also at degeneracies by continuous extension. Since $f''(u)=1/[u(1-u)]\ge4$, every coefficient in the sum is at least $4$ by the scalar mean-value theorem. Therefore $g''(t)\ge4\|V\|_2^2$. Taylor's integral identity gives
$$
\mathcal D(A\Vert B)=\int_0^1(1-t)g''(t)dt\ge2\|V\|_2^2.
$$
For one-dimensional $B=1/2$ and $A=1/2+\epsilon$, the ratio $\mathcal D(A\Vert B)/\epsilon^2\to2$ as $\epsilon\to0$, proving sharpness. $\square$

*Proof of (3).* Apply (7) to $A_L$ and $B_L$, and take the lower limit using (2). The strict positivity follows from $K_0(t)>0$ for $t>0$, since its squared contribution has positive integral. $\square$

## 4. Dependence on the mass parameter

Put
$$
G(t)=K_0(t)^2+\left(K_1(t)-\frac1t\right)^2,\qquad t>0.
$$
The change of variable $t=\mu s$ gives a useful second representation,
$$
\boxed{H(\mu)=\frac1{\pi^2}\int_0^\mu(\mu-t)G(t)\,dt.}
\tag{8}
$$
The behavior of $K_0$ and $K_1$ at zero shows $G(t)=O(1+|\log t|^2)$, while $G(t)=t^{-2}+O(e^{-t}t^{-1/2})$ at infinity.

**Corollary 6 (Monotonicity and convexity).** The function $H$ is twice continuously differentiable on $(0,\infty)$ and
$$
H'(\mu)=\frac1{\pi^2}\int_0^\mu G(t)dt>0,
\qquad H''(\mu)=\frac{G(\mu)}{\pi^2}>0.
\tag{9}
$$

**Proposition 7 (Exact integral and large-mass slope).** One has
$$
\int_0^\infty\left[K_0(t)^2+\left(K_1(t)-\frac1t\right)^2\right]dt=\pi,
\qquad \boxed{\lim_{\mu\to\infty}\frac{H(\mu)}\mu=\frac1\pi.}
\tag{10}
$$

*Proof.* Formula (4), with $\mu=1$, gives the exact Frobenius square
$$
\|F_1(t)\|_{\mathrm F}^2=1-\frac{|t|}{\sqrt{t^2+1}}.
$$
Its integral over $\mathbb R$ is $2$, by the elementary antiderivative $t-\sqrt{1+t^2}$ on the positive axis. Fourier--Plancherel thus gives $\int_{\mathbb R}\|K_1(s)\|_{\mathrm F}^2ds=1/\pi$. Inserting the Bessel kernel (1) and using its even Frobenius norm gives the first identity in (10). The expression $H(\mu)/\mu=\pi^{-2}\int_0^\mu(1-t/\mu)G(t)dt$ converges to $\pi^{-2}\int_0^\infty G(t)dt$ by dominated convergence. $\square$

**Proposition 8 (Small-mass expansion).** Let $a_\mu=\log(2/\mu)-\gamma$, where $\gamma$ is Euler's constant. As $\mu\downarrow0$,
$$
\boxed{H(\mu)=\frac{\mu^2}{\pi^2}
\left(\frac{a_\mu^2}{2}+\frac{3a_\mu}{2}+\frac74\right)
+O\!\left(\mu^4[1+|\log\mu|]^2\right).}
\tag{11}
$$

*Proof.* The standard modified-Bessel expansions, uniformly for $0<s\le1$ and small $\mu$, give
$$
K_0(\mu s)=a_\mu-\log s+O\!\left(\mu^2s^2[1+|\log(\mu s)|]\right),
\quad \frac1s-\mu K_1(\mu s)=O\!\left(\mu^2s[1+|\log(\mu s)|]\right).
$$
Use these in (2). The integrable error terms have the stated order. The elementary integrals $\int_0^1(1-s)ds=1/2$, $\int_0^1(1-s)(-\log s)ds=3/4$, and $\int_0^1(1-s)(\log s)^2ds=7/4$ yield (11). $\square$

The limit $L\to\infty$ throughout this manuscript is taken with $\mu$ fixed. Equations (10)--(11) describe the **subsequent** behavior of the limiting function $H(\mu)$ as its argument changes; they require no exchange of the $L$ and $\mu$ limits.

## 5. Numerical diagnostics

The table below compares direct finite-lattice Fourier integration of $\operatorname{Tr}(\Delta_L^2)$ with independent quadrature of the Bessel representation (2). Numerical values are rounded and are not interval enclosures.

| $\mu$ | $H(\mu)$ | $\|\Delta_{16}\|_2^2$ | $\|\Delta_{64}\|_2^2$ | $\|\Delta_{128}\|_2^2$ |
|:---:|---:|---:|---:|---:|
| $0.00625$ | $0.00009107247233$ | $0.00009059369729$ | $0.00009097366525$ | $0.00009102547241$ |
| $0.05$ | $0.002852564396$ | $0.002817285774$ | $0.002844634318$ | $0.002848706782$ |
| $0.5$ | $0.084815500230$ | $0.080385074026$ | $0.083727553206$ | $0.084275474084$ |
| $2$ | $0.471615679441$ | $0.406078605117$ | $0.454191601689$ | $0.462834231123$ |

As a separate check, the finite Frobenius coefficient sum was compared against explicit construction of the complex block Toeplitz matrix, and the matrix-entropy inequality was tested on noncommuting positive contractions. All derivations above are analytical; the numerical diagnostics help expose normalization and Fourier-sign mistakes.

## References

1. H. Araki, "On quasifree states of CAR and Bogoliubov automorphisms," *Publications of the Research Institute for Mathematical Sciences* **6** (1971), no. 3, 385--442, doi:10.2977/prims/1195193913.
2. NIST Digital Library of Mathematical Functions, §§10.29, 10.31--10.32 (modified-Bessel derivatives, series, and integral representations), https://dlmf.nist.gov/10.32 and https://dlmf.nist.gov/10.31.
3. R. Bhatia, *Matrix Analysis*, Graduate Texts in Mathematics **169**, Springer (1997), especially trace spectral functions and divided differences.
4. J. Pitrik and D. Virosztek, "On the Joint Convexity of the Bregman Divergence of Matrices," arXiv:1405.7885 (2014); used for background on matrix Bregman divergences, not as a substitute for Proposition 5.

## Acknowledgments and contributions

Kirtus Justus is responsible for the research direction, selection of the mathematical problem, and the final scientific claims presented under his byline. ChatGPT (OpenAI) assisted with the derivation of the kernel limit, matrix-entropy inequality, numerical verification, and manuscript drafting. Claude (Anthropic), Gemini (Google), Grok (SpaceXAI), and DeepSeek (High-Flyer) are acknowledged as participants in the broader research workflow; no specific contribution to this derivation is attributed to them without source-level provenance. All mathematical claims remain subject to human review. No institutional endorsement is implied.
