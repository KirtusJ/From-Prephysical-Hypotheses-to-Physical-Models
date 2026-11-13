---
title: "Relative Entropy of Finite-Interval Wilson–Dirac Quasifree States"
author: 'Kirtus Justus (Theoretical Physicist) \textbullet{} 31 October 2026\tabularnewline Port Coquitlam, British Columbia, Canada'
date: ''
lang: en
header-includes:
 - \usepackage{microtype}
 - \usepackage{booktabs}
 - \usepackage{longtable}
---

**Abstract.** We study the quantum relative entropy of finite-interval restrictions of the occupied-band quasifree states of a one-dimensional Wilson–Dirac chain, in the fixed-scaled-mass regime $m=\mu/L$, $\mu>0$. An exact interval-preserving unitary identifies the massless reference with the half-filled sine kernel and its commuting Jacobi operator. We derive the two-bond trace and its logarithmic asymptotic, establish a positive Wilson spectral majorant, and control the remaining nonlinear and cross-boundary entropy contributions at order $O_\mu(1)$. The fixed-interior modular expansion and global linear logit bounds imply a bounded longitudinal reference-modular trace and a vanishing transverse contribution. Together with the cross-boundary entropy trace path, the exact finite decomposition yields the fixed-positive-scaled-mass expansion
$\mathcal D_L(\mu)=\mu^2\log L/6+\mu^2(13/36-\pi/12-\log\mu/6)-\mathcal S(\mu)+O_\mu((\log L)^{-1})$,
as proved in Theorem 1 of *Finite Part of Wilson–Dirac Relative Entropy*. The modular and nonlinear estimates are sharpened in Theorem 3, Corollary 4 and Theorem 6 of *Uniform Modular Control and Nonlinear Convergence for Wilson–Dirac Intervals*. The comparison uses restrictions of infinite-chain occupied-band states, with fixed $\mu>0$.

**Keywords:** quasifree fermions; quantum relative entropy; Toeplitz and Jacobi matrices; conditional asymptotics.

## 1. Problem and model

The finite CAR quasifree-state framework is standard [1]. Elliptic complementary-modulus asymptotics and modified-Bessel representations use the NIST DLMF conventions [2]. The sine-kernel/commuting-tridiagonal structure belongs to the classical discrete-prolate literature [3,4]; the cellwise equivalence to this Wilson projector is proved below.

The comparison concerns restrictions of infinite-chain occupied-band projections to consecutive cells, rather than ground states of open finite chains. We keep the scaled mass $\mu>0$ fixed as $L\to\infty$. The interval geometry, boundary channels and quasifree-state convention are specified below.

### Mathematical framework

The proof separates an exact four-term entropy decomposition from asymptotic estimates of its terms. The positive-majorant and boundary estimates are derived for the specified Wilson symbols. The companion *Uniform Bulk Modular Asymptotics and the Leading Wilson Entropy Law* supplies the modular estimates needed for the leading law. Its exact spectral connection depends on the companion differential-domain and spectral-tail results. The finite-part assembly is Theorem 1 of *Finite Part of Wilson–Dirac Relative Entropy*, whose Section 7 combines the two-bond constant, nonlinear limit, vanishing modular trace and finite boundary trace path. The stronger modular and nonlinear bounds are Theorem 3, Corollary 4 and Theorem 6 of *Uniform Modular Control and Nonlinear Convergence for Wilson–Dirac Intervals*. Their exact connection and domain assumptions are stated in those manuscripts.

## The infinite-chain occupied-band projection

Fix $\mu>0$ and positive integer $L$ and put $$\label{eq:parameters}
N=2L,\qquad m=\mu/L,\qquad r=\frac{m}{m+2}=\frac{\mu}{N+\mu}.$$ For $k\in[-\pi,\pi]$ define the $2\times2$ Bloch Hamiltonian $$\label{eq:bloch}
h_m(k)=\sin k\,\sigma_x+(1+m-\cos k)\,\sigma_z,
\qquad E_m(k)=\sqrt{m^2+4(1+m)\sin^2(k/2)},$$ with occupied-band projection $P_m(k)=\tfrac12[\mathbf 1-h_m(k)/E_m(k)]$. At $m=0$, the value at the isolated degeneracy $k=0$ is immaterial to Fourier multiplication. The covariance compressed to $L$ consecutive cells is $$\label{eq:covariance}
(C_{L,m})_{ab}=\frac1{2\pi}\int_{-\pi}^{\pi}e^{ik(a-b)}P_m(k)\,dk,
\qquad 0\le a,b<L.$$ The full matrix has dimension $2L\times2L$; each entry displayed in the covariance formula is a $2\times2$ orbital block. Write $A_L=C_{L,\mu/L}$ for the massive covariance and $B_L=C_{L,0}$ for the massless reference. At finite $L$, the reference and massive compressions are strictly between zero and identity, although their smallest endpoint distances shrink sharply with $L$. Strictness follows because a finitely supported vector cannot belong to the range or kernel of the corresponding full-line nonconstant band projection while vanishing on the complement. The isolated massless degeneracy has measure zero in the Fourier integral.

## Entropy, orientation, and exact finite identity

For a positive contraction $C$, define the binary von Neumann entropy of its quasifree state by $$S(C)=-\operatorname{Tr}\big[C\log C+(\mathbf 1-C)\log(\mathbf 1-C)\big].$$ For covariances $A,B$ with spectra strictly inside $(0,1)$, set $$\label{eq:relentropy}
\mathcal D(A\Vert B)=\operatorname{Tr}\left[A(\log A-\log B)+(\mathbf 1-A)(\log(\mathbf 1-A)-\log(\mathbf 1-B))\right].$$ This is the relative entropy of the corresponding gauge-invariant quasifree density operators. The order is not interchangeable. In particular $\mathcal D_L(\mu)=\mathcal D(A_L\Vert B_L)$, with the massive state as the first argument.

::: {#prop:finite .proposition}
**Proposition** (Finite relative-entropy trace identity). *For finite strictly positive contraction matrices $A,B$, with $\Delta=A-B$ and $K_B=\log(\mathbf 1-B)-\log B$, $$\label{eq:finiteid}
\mathcal D(A\Vert B)=\operatorname{Tr}(\Delta K_B)-[S(A)-S(B)].$$ No commutation assumption is required for $A$ and $B$.*
:::

::: proof
*Proof.* Expand the finite relative-entropy identity; group the $A$-only terms into $-S(A)$ and the $B$-only terms into $S(B)$. The remaining terms are $-\operatorname{Tr}(A\log B+(\mathbf 1-A)\log(\mathbf 1-B))+\operatorname{Tr}(B\log B+(\mathbf 1-B)\log(\mathbf 1-B))=\operatorname{Tr}((A-B)(\log(\mathbf 1-B)-\log B))$. The trace is linear and each logarithm is applied to its own positive contraction; nothing has been reordered across $A$ or $B$. $\square$
:::

## Scalar reference geometry and four-term decomposition

Write $H_2=2^{-1/2}\begin{pmatrix}1&1\\1&-1\end{pmatrix}$, $W=2^{-1/2}(I-i\sigma_x)H_2$, and $U=\bigoplus_{j=0}^{L-1}(-1)^j\sigma_zW$. This unitary acts separately on each cell of the finite interval. In the scalar ordering induced by $U$, set $A_N=UC_{L,m}U^\dagger$ and $B_N=UC_{L,0}U^\dagger$.

**Theorem (Exact scalar reference and commuting Jacobi matrix).** For every integer $L\ge1$,
$$\label{eq:ref}
(B_N)_{pq}=\begin{cases}\frac12,&p=q,\\[2pt] \frac{\sin[\pi(p-q)/2]}{\pi(p-q)},&p\ne q,\end{cases}\qquad
(J_N)_{j-1,j}=(J_N)_{j,j-1}=\frac{j(N-j)}N,\quad 1\le j<N,
$$
with all other Jacobi entries zero. Moreover $0<B_N<I$, $[J_N,B_N]=0$, $J_N$ has simple real spectrum, and $\lVert J_N/N\rVert\le1/2$.

*Proof.* For the massless symbol, Fourier integration yields the cell-displacement block
$$
(C_{L,0})_{ab}=\frac12\delta_{ab}I
-\frac{id}{2\pi(d^2-1/4)}\sigma_x
-\frac1{\pi(1-4d^2)}\sigma_z,\qquad d=a-b.
$$
These coefficients follow by integrating $\sin k/E_0(k)=\operatorname{sgn}(k)\cos(k/2)$ and $(1-\cos k)/E_0(k)=|\sin(k/2)|$. The identities $W\sigma_zW^\dagger=\sigma_x$ and $W\sigma_xW^\dagger=-\sigma_y$ show that the transformed off-orbital entries at displacement $d$ equal $(-1)^{d+1}/[\pi(2d-1)]$ and $(-1)^d/[\pi(2d+1)]$. These are precisely the scalar sine-kernel coefficients for index differences $2d-1$ and $2d+1$. The diagonal and like-orbital entries agree as well.

For $b_d=\sin(\pi d/2)/(\pi d)$ ($b_0=1/2$), direct evaluation of the commutator gives
$$
[J_N,B_N]_{pq}=\frac{N-p-q-1}{N}
\big[(p-q-1)b_{p-q-1}+(p-q+1)b_{p-q+1}\big]=0.
$$
The final equality is the sine addition identity. Since every off-diagonal Jacobi coefficient is strictly positive, the eigenvector recurrence gives simple spectrum. The sine kernel is a compression of the Fourier projection onto $[-\pi/2,\pi/2]$: a nonzero trigonometric polynomial has positive squared integral on that arc and its complement, yielding $0<B_N<I$. Finally, the maximum Jacobi row sum divided by $N$ is at most $1/2$. $\square$

The commuting basis in the modular analysis is the joint eigenbasis of $B_N$ and $J_N$. The massive covariance $A_N$ is evaluated in this same fixed basis.

The exact infinite-series reference scaling function is $$\label{eq:eta}
\eta(t)=\sum_{n=0}^{\infty}
\frac{\pi\binom{2n}{n}\binom{4n}{2n}}{(2n+1)16^n}\,t^{2n+1},\quad |t|\le\frac12.$$ Define $T_N=J_N/N$, the exact reference modular matrix $K_N=\log(\mathbf 1-B_N)-\log B_N$, its scaling-function error $E_N=K_N+N\eta(T_N)$, and the massive perturbation $\Delta_N=A_N-B_N$ in the same scalarized basis.

::: {#prop:four .proposition}
**Proposition** (Four exact finite branches). *With $\Delta S_L=S(A_L)-S(B_L)$, let $$\begin{aligned}
\mathcal P_L&=\operatorname{Tr}[\Delta_N(-\pi J_N)],&
\mathcal Q_N&=\operatorname{Tr}\{\Delta_N[-N\eta(T_N)+\pi J_N]\},\nonumber\\
\mathcal F_L&=\operatorname{Tr}(\Delta_NE_N).&&\label{eq:branches}
\end{aligned}$$ Then for every admissible $L,\mu$, $$\label{eq:four}
\boxed{\mathcal D_L(\mu)=\mathcal P_L+\mathcal Q_N+\mathcal F_L-\Delta S_L.}$$*
:::

::: proof
*Proof.* Substitute $K_N=-N\eta(T_N)+E_N$. Add and subtract the linear term $-\pi J_N$, using that the first coefficient in the reference spectral series is $\pi$. The identity uses only linearity of trace; in particular $\Delta_N$ is not assumed diagonal in the reference basis. $\square$
:::

## The exact two-bond contribution

Define, for $m\ge0$,
$$\label{eq:bonddefs}
u_m=\frac1{2\pi}\int_0^\pi\frac{m+1-\cos k}{E_m(k)}\,dk,\qquad
v_m=\frac1{2\pi}\int_0^\pi\frac{1-(m+1)\cos k}{E_m(k)}\,dk.
$$
The first is the intra-cell nearest-neighbor entry of $A_N$; the second is the inter-cell entry. At $m=0$, $u_0=v_0=1/\pi$.

**Theorem (Exact Fourier-to-elliptic two-bond formula).** With $r=m/(m+2)$ and $z=1-r^2$ for $m>0$, the linear trace branch is
$$\label{eq:twobond}
\mathcal P_L=-\pi\left[\frac{4L^2-1}{6}
\left(u_m+v_m-\frac2\pi\right)+\frac12(u_m-v_m)\right].
$$
If $\mathbf K(z)=\int_0^{\pi/2}(1-z\sin^2q)^{-1/2}dq$ and $\mathbf E(z)=\int_0^{\pi/2}(1-z\sin^2q)^{1/2}dq$, then
$$\label{eq:elliptic}
\begin{aligned}
u_m+v_m&=\frac2\pi\frac{\mathbf E(1-r^2)-r^2\mathbf K(1-r^2)}{1-r^2},\\
u_m-v_m&=\frac{2r}\pi\frac{\mathbf K(1-r^2)-\mathbf E(1-r^2)}{1-r^2}.
\end{aligned}
$$
The elliptic functions use the *parameter* $z$, whereas the complementary *modulus* in the DLMF convention is $r$.

*Proof.* The Fourier coefficients of the two Pauli components of $P_m(k)$, followed by the fixed cellwise unitary above, give $u_m=-z_0(m)$ and $v_m=z_1(m)+ix_1(m)$. The second expression simplifies through $\sin^2k-\cos k(m+1-\cos k)=1-(m+1)\cos k$. Since $J_N$ is tridiagonal, its trace pairing involves only these bonds. Their Jacobi weights sum to $(2L^2+1)/6$ for odd bonds and $(L^2-1)/3$ for even bonds, yielding the first formula. Taking the sum and difference of the Fourier integrals, substituting $q=(\pi-k)/2$, and using $E_m(k)=(m+2)\sqrt{1-z\cos^2(k/2)}$ proves the two elliptic identities. The formulas extend to $m=0$ by continuity. $\square$

**Corollary (Fixed-positive-mass two-bond asymptotic).** For every fixed $\mu>0$, with $m=\mu/L$,
$$\label{eq:Pestimate}
\mathcal P_L=\frac{\mu^2}{6}\log L+
\mu^2\left(\frac16\log\frac8\mu-\frac14\right)
+\mathcal O_\mu\left(\frac{\log L}{L}\right).
$$

*Proof.* Put $\ell=\log(4/r)$. The complementary-modulus expansions are $\mathbf K(1-r^2)=\ell+O(r^2\ell)$ and $\mathbf E(1-r^2)=1+\frac{r^2}{2}(\ell-\frac12)+O(r^4\ell)$. Therefore $u_m+v_m=\frac2\pi[1+r^2(\frac34-\frac\ell2)+O(r^4\ell)]$ and $u_m-v_m=\frac{2r}\pi[\ell-1+O(r^2\ell)]$. Substitute $r=\mu/(2L+\mu)$ and $\ell=\log L+\log(8/\mu)+O_\mu(1/L)$ into the exact two-bond formula. $\square$

## Nonlinear scaling and its exact positive series

For the specified Wilson comparison at fixed $\mu>0$, the nonlinear trace converges to $\mu^2c_\eta$. The all-degree proof and the estimate $O_\mu((\log N/N)^{1/3})$ are Theorem 7 of *Finite Part of Wilson–Dirac Relative Entropy*; Theorem 6 of *Uniform Modular Control and Nonlinear Convergence for Wilson–Dirac Intervals* sharpens the error to $O_\mu(\sqrt{\log N/N})$.

The scalar constant is $$\label{eq:constant}
c_\eta=\sum_{n=1}^{\infty}\frac{1}{2n(4n+1)(4n+2)(4n+3)}
=\frac{11}{18}-\frac\pi{12}-\frac{\log2}{2}.$$ The exact rational term is obtained by inserting the beta-integral coefficients $I_p=(p!)^2/(2p+1)!$ and the angular integral $A_p=\frac12\int_0^{\pi/2}\cos^{p-2}q\sin^2q\,dq$ into the reference spectral series for odd $p=2n+1$, then cancelling factorials. The closed form in the nonlinear constant formula follows from partial fractions and the classical even/odd harmonic-number series.

::: {#lem:ctail .lemma}
**Lemma** (Certified positive tail). *For every integer $K\ge1$, $$\label{eq:ctail}
0<c_\eta-\sum_{n=1}^K\frac{1}{2n(4n+1)(4n+2)(4n+3)}\le\frac{1}{384K^3}.$$*
:::

::: proof
*Proof.* Each term is at most $1/(128n^4)$, since $2n(4n+1)(4n+2)(4n+3)\ge128n^4$. The integral test gives $\sum_{n>K}n^{-4}\le\int_K^\infty x^{-4}\,dx=1/(3K^3)$. The summands are strictly positive. $\square$
:::

**Theorem used here (nonlinear finite-part convergence).** For the Wilson model and each fixed $\mu>0$, $\mathcal Q_N=\mu^2c_\eta+O_\mu(\sqrt{\log N/N})$ as even $N\to\infty$. This is Theorem 6 of *Uniform Modular Control and Nonlinear Convergence for Wilson–Dirac Intervals*. The proof uses an all-degree averaged displacement bound, including degrees $p\ge N$, together with the explicit positive-majorant and transverse-moment estimates. The positive scalar series and its tail bound below determine $c_\eta$; scalar coefficient convergence alone is not the matrix-trace limit.

::: {#prop:constant .proposition}
**Proposition** (Finite constant identity). *The branch constants satisfy $$\label{eq:constantreconcile}
\frac16\log\frac8\mu-\frac14+c_\eta
=\frac{13}{36}-\frac\pi{12}-\frac{\log\mu}{6}.$$*
:::

::: proof
*Proof.* Use $\log 8=3\log2$ and the nonlinear constant formula. Then $\frac16\log 8-\frac12\log2=0$ and $-\frac14+\frac{11}{18}=\frac{13}{36}$. $\square$
:::

## Modular error under uniform hypotheses

The genuinely nontrivial modular object is $$\label{eq:modular}
\mathcal F_L=\operatorname{Tr}(\Delta_NE_N),\qquad E_N=K_N+N\eta(T_N).$$ Let $v_j$ be a common orthonormal basis for $B_N$ and $J_N$ with eigenvalues $b_j$ and $\lambda_j$, and put $e_j=\langle v_j,E_Nv_j\rangle$. This joint diagonalization applies *only* to the reference operators.

**Theorem (Wilson majorant, pairing and spectral tail; imported).** Let $N=2L$, $m=\mu/L$, and let $\Delta_N=A_N-B_N$ be the scalarized covariance difference. There exist self-adjoint matrices $S_N,D_N$ and $G_N\ge0$ such that
\[
\Delta_N=S_N+D_N,\qquad -G_N\le S_N\le G_N,\qquad
\operatorname{Tr}G_N\le\frac\mu\pi.
\]
For the common reference eigenvectors $B_Nv_j=b_jv_j$, $J_Nv_j=\lambda_jv_j$, put $q_j=\langle v_j,G_Nv_j\rangle$. Then
\[
|\langle v_j,D_Nv_j\rangle|\le2\sqrt{q_jb_j(1-b_j)}
\]
and, with $\nu_N=\sum_jq_j\delta_{|\lambda_j|}$,
\[
\boxed{\nu_N((t,\infty))\le\min\left\{\frac\mu\pi,
\sqrt{\frac2{15}}\frac{\mu^2}{\pi t}+\frac\mu{3\pi t^2}\right\}\qquad(t>0).}
\]
The stronger interval-compression estimate is
\[
\boxed{0\le D_N^2\le G_N-G_N^2\le G_N.}
\]

*Proof.* The full-line occupied-band projectors obey $(P_m-P_0)^2=G$ and the corresponding longitudinal/transverse Pauli-algebra decomposition. The full-line relations give order domination and anticommutation. Compression preserves the operator order; the pairing inequality is obtained by applying the full-line identities to interval-supported vectors before taking the common reference expectation. The inverse-power spectral bounds follow from the finite Jacobi bond sums and a positive layer-cake argument, giving the displayed constants. Finally, for interval projection $\chi$ and $Q=I-\chi$,
\[
G_N-G_N^2-D_N^2=\chi GQG\chi+\chi DQD\chi\ge0.
\]
Products and commutators are **not** asserted to survive compression. The canonical Bloch-projector and Jacobi proofs are Theorems 1–3 in sections 2–3 of *Exact Spectral Majorants for a Wilson–Dirac Interval*. The stronger compression identity is the theorem in the section “Theorem: exact boundary remainders” of *Finite-Interval Compression and Transverse Control*. $\square$

**Corollary (uniform covariance distance).** The same projector identity implies $0\le\Delta_N^2\le G_N$ and $\|\Delta_N\|_{\rm HS}^2\le\mu/\pi$. The fixed-$\mu$ Hilbert–Schmidt scaling limit is described in the accompanying covariance supplement.

::: {#lem:logtail .lemma}
**Lemma** (Logarithmic moment from a critical tail). *Suppose $\nu$ is a finite positive Borel measure on $[0,\infty)$ with $\nu((t,\infty))\le D/t$ for every $t>0$. Then for $\beta>1$ and $\rho>0$, $$\label{eq:logtail}
\int_0^\infty\log\bigl(1+(t/\rho)^\beta\bigr)\,d\nu(t)
\le \frac{\pi D}{\rho\sin(\pi/\beta)}.$$*
:::

::: proof
*Proof.* The increasing integrand vanishes at the origin. Tonelli's theorem, applied to the integral of its nonnegative derivative, reduces the left side to at most $\frac D\rho\int_0^\infty\frac{\beta u^{\beta-2}}{1+u^\beta}\,du$. Substitute $z=u^\beta$; the beta integral evaluates to $\Gamma(1-1/\beta)\Gamma(1/\beta)=\pi/\sin(\pi/\beta)$. The condition $\beta>1$ ensures integrability at zero. $\square$
:::

**A sufficient alternative modular estimate.** The moving-window and global logarithmic-envelope conditions below imply the stated inverse-logarithmic bound. This conditional implication is separate from the fixed-mass finite-part proof. The latter uses the exact connection and finite-matrix estimates of *Finite Part of Wilson–Dirac Relative Entropy* and *Uniform Modular Control and Nonlinear Convergence for Wilson–Dirac Intervals*. The conditions displayed below are not asserted to follow from those results. They are unnecessary for the finite-part conclusion stated here.

**Assumption (uniform reference-modular estimates).** There exist constants $C_{\log},C_{\rm in},C_{\rm out},c_{\rm w}>0$ and an even $N_0$ such that for every even $N\ge N_0$, with $x=\log N$ and $h_j=2+|\lambda_j|$, every reference mode satisfies
\[
|e_j|\le C_{\log}\log\!\left(1+C_{\rm in}h_j^{103}/x\right)
\quad(h_j\le c_{\rm w}\sqrt{x}),
\]
and $|e_j|\le C_{\rm out}\log h_j$ for every $j$. These constants are independent of $N$ and the mode index. These remain additional spectral estimates, not consequences of Jacobi commutation alone. The variance input used below follows from the stronger $O((\log N)/N^2)$ estimate in the bounded-modular corollary, whose canonical proof is the “Positive weighted modular control” theorem in *Uniform Bulk Modular Asymptotics and the Leading Wilson Entropy Law*, section “Global envelope and weighted consequences.”

::: {#prop:modrate .proposition}
**Proposition** (Conditional quantitative modular rate). *Under the Wilson majorant theorem and the stated uniform reference-modular assumptions, for each fixed $\mu>0$, $$\label{eq:modrate}
|\mathcal F_L|=\mathcal O_\mu\bigl((\log N)^{-1/103}\bigr).$$*
:::

::: proof
*Proof.* Write $\mathcal F_L=\sum_j e_j(s_j+d_j)$ with $s_j=\langle v_j,S_Nv_j\rangle$ and $d_j=\langle v_j,D_Nv_j\rangle$. For the average contribution, $|s_j|\le q_j$. Apply the logarithmic-tail lemma with $\beta=103$ to the $t$-window where the moving-window estimate holds, using $2+t\le2t$ for $t\ge2$ and $\rho\asymp x^{1/103}$. The bounded low-energy part is $\mathcal O_\mu(x^{-1})$. For energies $t\gtrsim\sqrt x$, use the global logarithmic envelope and the spectral-tail bound, *retaining the boundary term in layer-cake integration*; the resulting contribution is $\mathcal O_\mu(\log x/\sqrt x)$. Hence $\sum_jq_j|e_j|=\mathcal O_\mu(x^{-1/103})$. For the staggered contribution, Cauchy--Schwarz and the staggered pairing bound give $$\sum_j|d_je_j|\le2(\operatorname{Tr}G_N)^{1/2}\{\operatorname{Tr}[E_N^2B_N(\mathbf 1-B_N)]\}^{1/2}
=\mathcal O_\mu(x^{-1/2}).$$ Combine the two absolute bounds. No cancellation among spectral modes is used. $\square$
:::

## Entropy difference as a trace-class boundary path

The continuum term $\mathcal S(\mu)$ is not defined as a difference between two individually divergent continuum entropies. The appropriate observable is the *cross-boundary perturbation* of the interval restriction of a full-line projection.

Let $X_m=\chi P_m(\mathbf 1-\chi)$, where $\chi$ is the position-space interval projection and $P_m$ is the full-line occupied-band projection, and set $Z_\mu=X_\mu-X_0$. Define $$\mathbb H(X)=\begin{pmatrix}0&X\\X^*&0\end{pmatrix},\quad
\mathbb D_\mu=\mathbb H(Z_\mu),\quad A_\theta=\mathbb H(X_0)+\theta\mathbb D_\mu,\quad Y_\theta=A_\theta+I/2.$$ The continuum notation means the rescaled half-line limit used in the cross-boundary construction, rather than simply substituting a mass into the Bloch Hamiltonian definition. Set $$h(p)=-p\log p-(1-p)\log(1-p),\quad
F(t)=h\left(\frac{1+\sqrt{1-4t^2}}2\right),\ |t|\le\frac12.$$ The derivative $F'$ is continuously defined at zero, is bounded on $[-1/2,1/2]$, and admits a polynomial approximation suited to noncommuting trace pairing. The entropy finite part is $$\label{eq:Sdefinition}
\mathcal S(\mu)=\frac12\int_0^1\operatorname{Tr}\bigl[F'(A_\theta)\mathbb D_\mu\bigr]d\theta,\qquad \mathcal S(0)=0.$$

::: {#lem:cross .lemma}
**Lemma** (Finite cross-block entropy identity). *If $P=P^*=P^2$ on a Hilbert space with finite-rank interval projection $\chi$, $C=\chi P\chi$, and $X=\chi P(\mathbf 1-\chi)$, then $XX^*=C-C^2$. The nonzero eigenvalues of $\mathbb H(X)$ are the signed square roots of the eigenvalues of $C-C^2$, and $$S(C)=\frac12\operatorname{Tr}F(\mathbb H(X))$$ with the usual interpretation of possible zero eigenvalues.*
:::

::: proof
*Proof and canonical source.* This is the singular-value part of the **Finite cross-block trace path** lemma in *Cross-Boundary Trace-Class Estimates for Wilson–Dirac Quasifree States*, section “Finite cross-block trace path.” That lemma also proves the exact finite entropy-difference path. With the piecewise-constant embedding used there, set $\mathbb D_{L,\mu}=\mathbb H(Z_{L,\mu})$, $A_{L,\theta}=\mathbb H(X_{L,0})+\theta\mathbb D_{L,\mu}$ and $Y_{L,\theta}=A_{L,\theta}+I/2$. Both $Y_{L,\theta}$ and $Y_\theta$ are positive contractions, and
\[
\Delta S_L=\frac12\int_0^1\operatorname{Tr}[F'(A_{L,\theta})\mathbb D_{L,\mu}]d\theta.
\]
The continuum trace path is finite because $\mathbb D_\mu$ is trace class and $F'$ is bounded. This use does not subtract two divergent continuum entropies. $\square$
:::

**Theorem (uniform entropy-difference bound; imported).** For the specific Wilson–Dirac projector family, with $m=\mu/L$ and $\mu>0$ fixed, there is a universal $C$ such that, whenever $\kappa=\log(1+\mu/L)\le 1/4$,
\[
\|\chi_L(P_{\mu/L}-P_0)(I-\chi_L)\|_1\le C\sqrt{L\kappa}\le C\sqrt\mu,
\qquad |S(A_L)-S(B_L)|\le 2C\sqrt\mu.
\]

*Proof.* For positive Fourier separation $n$, the massive-minus-massless projector coefficient admits the exact Fourier–Laplace representation
\[
T_n=-\frac1{2\pi}\int_0^\infty e^{-nt}
[\rho_z(t)\sigma_z+i\rho_x(t)\sigma_x]dt.
\]
Each of the two exterior half-line blocks is a Bochner integral of rank-one Hankel matrices with nuclear norm
\[
W_L(t)=e^{-t}\frac{\sqrt{1-e^{-2Lt}}}{1-e^{-2t}}.
\]
Writing $\kappa=\log(1+\mu/L)$, the four regions $(0,\kappa)$, $(\kappa,2\kappa)$, $(2\kappa,1)$, and $(1,\infty)$ give
\[
\int_0^\infty W_L(t)(|\rho_z(t)|+|\rho_x(t)|)dt
\le C'\sqrt{L\kappa}\le C'\sqrt\mu.
\]
The canonical proof is Theorem 1, with the four-region argument in section 4 and entropy argument in section 5, of *Uniform Square-Root-Mass Control of Wilson–Dirac Boundary Covariances*. For $F(s)=h((1+\sqrt{1-4s^2})/2)$ on $[0,1/2]$, $|F'(s)|\le2$. The identity $XX^*=A_L(I-A_L)$ and the singular-value perturbation inequality therefore yield $|\Delta S_L|\le2\|\chi_L(P_m-P_0)(I-\chi_L)\|_1$. $\square$

**Theorem (Boundary convergence and fractional regularity; imported).** *For the specified Wilson projectors and their piecewise-constant embedding, $\|Z_{L,\mu}-Z_\mu\|_1=O_M((\log L)/L)$ uniformly for $0\le\mu\le M$. For every $0<s<1/2$, $\|\mathbb D_\mu\|_{\mathcal S_1(L^2,H^s)}\le C_s\sqrt\mu$. The continuum positive-contraction interpolants $Y_\theta$ are bounded on $H^s$ uniformly in $\theta,\mu$, and $\|Y_{L,\theta}-Y_\theta\|_{H^s\to L^2}\le C_sL^{-s}$.*

*Proof source.* Equations (B5)–(B8) of *Cross-Boundary Trace-Class Estimates for Wilson–Dirac Quasifree States* prove these statements, with the full-line aliases retained. They concern this boundary subsystem and do not assert convergence of the nonlinear or longitudinal modular finite part.

::: {#lem:cheb .lemma}
**Lemma** (Chebyshev approximation of the entropy derivative). *Define $g(z)=F'(z/2)$ for $|z|\le1$. It has a decomposition $g(z)=-2z\log|z|+r(z)$ with $r\in C^2([-1,1])$, and its cosine-Chebyshev coefficients satisfy $|a_k|\le Ck^{-2}$. Consequently a degree-$n$ polynomial $q_n$ satisfies $\left\lVert q_n-g\right\rVert_\infty\le C/n$. Under the change of variables $z=2y-1$, its monomial coefficient $\ell^1$ norm is $\mathcal O(7^n)$.*
:::

::: proof
*Proof.* For $w=\sqrt{1-z^2}$, direct differentiation gives $$g(z)=\frac{2z}{w}\operatorname{artanh}w=\frac{2z}{w}[\log(1+w)-\log|z|].$$ Near $z=0$ the difference from $-2z\log|z|$ is the sum of an analytic function and an $\mathcal O(z^3\log|z|)$ term having two continuous derivatives; near the endpoints the specified expression is analytic. The cosine coefficients of $-2\cos\theta\log|\cos\theta|$ are $\mathcal O(k^{-2})$ by the Fourier expansion of $\log(2|\cos\theta|)$, while those of $r(\cos\theta)$ have the same decay by two integrations by parts. The polynomial tail is bounded by $\sum_{k>n}C/k^2$. Finally, $T_{k+1}(2y-1)=(4y-2)T_k(2y-1)-T_{k-1}(2y-1)$ bounds the monomial coefficient sum by $7^k$. $\square$
:::

::: {#thm:entropy .theorem}
**Theorem** (Entropy finite-part rate). *For the specified Wilson projectors, with the embedding and trace path defined above, for fixed $\mu>0$, $$\label{eq:entropy}
\Delta S_L=\mathcal S(\mu)+R_S,
\qquad R_S=\mathcal O_\mu(1/\log L).$$ The estimate is uniform for $0\le\mu\le M$ on each fixed compact mass interval $[0,M]$, but that fact does not extend the full relative-entropy theorem uniformly to zero mass.*
:::

::: proof
*Proof.* Apply the finite trace-path lemma in the boundary supplement and the definition of the continuum entropy functional. Replace the finite cross-boundary perturbation by its continuum counterpart at trace-norm cost $\mathcal O_\mu(\log L/L)$. Apply the proved $H^s$ interpolation estimate to the bounded functional calculus of the two interpolants. For each $\theta$, abbreviate $Y_L=Y_{L,\theta}$ and $Y=Y_\theta$; then use the noncommutative telescoping identity $$(Y_L^k-Y^k)\mathbb D_\mu=\sum_{j=0}^{k-1}Y_L^j(Y_L-Y)Y^{k-1-j}\mathbb D_\mu.$$ Every left factor is an $L^2$ contraction, the middle factor is $H^s\to L^2$ of order $L^{-s}$, and only continuum factors on the right require $H^s$ bounds. With a coefficient sum bounded by $\mathcal O(7^n)$, the final estimate is $$|R_S|\le C_{\mu,s}\bigl(\log L/L+n^{-1}+n(7M_s)^nL^{-s}\bigr).$$ Take $n\asymp\log L$ with a sufficiently small positive coefficient so that $(7M_s)^nL^{-s}\le L^{-s/2}$. The approximation term is $\mathcal O(1/\log L)$ and the other terms are smaller. $\square$
:::

## Leading relative-entropy law and modular estimates

Set $W_N=B_N(I-B_N)$, $M_{2,N}=\operatorname{Tr}(J_N^2W_N)$, and write $S_N,D_N$ for the longitudinal and transverse components in the majorant theorem. For the specified half-filled sine kernel,
\[
\boxed{M_{2,N}=\frac{\log N}{3\pi^2}+O(1).}
\]
An exact exterior-kernel factorization proves this asymptotic; its complete lattice sum and finite trigamma representation appear in *Sharp Logarithmic Jacobi Boundary Moment for a Half-Filled Fermion Interval*.

The companion *Exact Reference Occupation Weights and Particle–Hole Pairing*
provides the independent exact reference identity
\[
\operatorname{Tr}[B_N(I-B_N)]=\frac1{\pi^2}\left[
\log(2N)+\gamma+1-\frac1{6N^2}+\frac7{20N^4}+O(N^{-6})\right]
\]
for even $N$, together with $\Gamma_NB_N\Gamma_N=I-B_N$,
$\Gamma_NJ_N\Gamma_N=-J_N$, and $\operatorname{Tr}(G_NE_N)=0$.
The last identity is a symmetry cancellation for the **majorant**, not for the
longitudinal perturbation $S_N$; the latter is controlled by the weighted estimate below.


**Theorem (bounded nonlinear correction; imported).** For each fixed $\mu>0$,
\[
\mathcal Q_N^{\rm long}=O_\mu(1),\qquad
\mathcal Q_N^{\rm trans}=O_\mu\!\left(\sqrt{\frac{\log N}{N}}\right),
\qquad \mathcal Q_N=O_\mu(1).
\]

*Proof summary.* The canonical proof is in *Fourth-Moment Control of the Wilson Nonlinear Correction*, sections 2–4 (fourth moment, Theorem 2, and bounded full correction). The positive Jacobi spectral measure satisfies
\[
\operatorname{Tr}(G_NJ_N^4)\le\frac{a_\mu N^3}{6}+\frac{b_\mu N^2}{2},\quad
 a_\mu=\sqrt{\frac2{15}}\frac{\mu^2}{\pi},\quad b_\mu=\frac\mu{3\pi}.
\]
The positive-coefficient series gives $|\eta(t)-\pi t|\le C_\eta|t|^3$ for $|t|\le1/2$. Pairing and Cauchy–Schwarz imply
\[
|\mathcal Q_N^{\rm trans}|\le
2C_\eta\sqrt{\left(\frac{a_\mu}{6N}+\frac{b_\mu}{2N^2}\right)M_{2,N}}.
\]
Layer-cake integration similarly bounds the longitudinal term by
$C_\eta(3a_\mu/8+3b_\mu/(2N))$. $\square$

**Theorem (occupation-weighted reference-modular control; imported weaker route).** The exact reference modular discrepancy $E_N=\log(I-B_N)-\log B_N+N\eta(J_N/N)$ satisfies
\[
\boxed{\operatorname{Tr}(W_NE_N^2)=O(\log N).}
\]

*Proof.* The full-line half-filled projection $P$ satisfies
$W_N=X_NX_N^*$ with $X_N=\chi_NP(I-\chi_N)$. The two half-line sine-kernel blocks are unitary modulations of truncated Hilbert Hankel matrices. The elementary representation $1/(i+j+1)=\int_0^\infty e^{-t(i+j+1)}dt$ gives $\operatorname{Tr}\sqrt{W_N}=\|X_N\|_1=O(\log N)$. For $0<b<1$,
\[
b(1-b)\log^2\frac{1-b}b\le4\sqrt{b(1-b)}.
\]
The reference operators commute, so combining this bound with $|N\eta(\lambda/N)|\le A_\eta|\lambda|$ gives
\[
\operatorname{Tr}(W_NE_N^2)
\le8\operatorname{Tr}\sqrt{W_N}+2A_\eta^2M_{2,N}=O(\log N).
\]
The canonical constant-explicit proof is Theorem 1 in section 3 of *Logarithmic Weighted Modular Control for the Half-Filled Sine Kernel*, using the nuclear-factor estimate of section 2. This independent route is weaker than the uniform-interior consequence below. $\square$

**Corollary (transverse modular reduction).** The Wilson pairing inequality yields
\[
|\operatorname{Tr}(D_NE_N)|\le
2\sqrt{\frac\mu\pi\operatorname{Tr}(W_NE_N^2)}
=O_\mu(\sqrt{\log N}).
\]
In combination with the two-bond, nonlinear and entropy theorems, this gives the proved identities of asymptotic scale
\[
\boxed{\mathcal D_L(\mu)=\frac{\mu^2}{6}\log L+\mathcal F_L+O_\mu(1),}
\]
\[
\boxed{\mathcal D_L(\mu)=\frac{\mu^2}{6}\log L+\operatorname{Tr}(S_NE_N)
+O_\mu(\sqrt{\log L}).}
\]
**Theorem (uniform interior modular expansion and weighted bounds).** For the half-filled reference, even $N$, fixed $0<\tau<1/2$ and integer $K\ge1$,
\[
e_j=\sum_{k=1}^K\frac{\varphi_{2k-1}(\lambda_j/N)}{N^{2k-1}}
+O_{\tau,K}(N^{-2K-1}),\qquad |\lambda_j/N|\le\tau.
\]
The functions are the even WKB period coefficients and are real analytic and odd on $(-1/2,1/2)$. Moreover
\[
\frac{2\pi}{3}|J_N|\le|K_N|\le2\pi|J_N|,\qquad
|E_N|\le2\pi|J_N|\le\pi N I.
\]
These results are proved in *Uniform Bulk Modular Asymptotics and the Leading Wilson Entropy Law*, using the exact connection identity, the positive differential tail operator, and an integrable Riccati residual. They are not inferred from a numerical fit or an unbounded formal series.

**Corollary (bounded modular contribution).** For the Wilson majorant and splitting defined above,
\[
\operatorname{Tr}(G_N|E_N|)=O_\mu(1),\quad
\operatorname{Tr}(S_NE_N)=O_\mu(1),\quad
\operatorname{Tr}(W_NE_N^2)=O((\log N)/N^2),
\]
\[
\operatorname{Tr}(D_NE_N)=O_\mu(\sqrt{\log N}/N),\qquad
\mathcal F_L=O_\mu(1).
\]

*Proof.* With $\tau=1/4$ and $K=1$ the interior error is bounded by $C/N$. The complementary contribution to the positive weighted trace is at most
\[
\pi N\operatorname{Tr}(G_N\mathbf1_{\{|J_N|>N/4\}})
\le4\pi a_\mu+16\pi b_\mu/N.
\]
Thus the full trace is at most $C\mu/(\pi N)+4\pi a_\mu+16\pi b_\mu/N$ for sufficiently large even $N$. The operator inequalities $-G_N\le S_N\le G_N$ bound each signed diagonal entry in the reference eigenbasis, proving the longitudinal bound without requiring commutation. On the same interior, $e_j^2\le C^2/N^2$, and $\operatorname{Tr}W_N=O(\log N)$. On the complement the logit bound gives $\zeta_j(1-\zeta_j)\le e^{-\pi N/6}$. The contribution there is at most $\pi^2N^3e^{-\pi N/6}$. This proves the variance estimate. The transverse pairing inequality then gives $2\sqrt{(\mu/\pi)\operatorname{Tr}(W_NE_N^2)}=O_\mu(\sqrt{\log N}/N)$. $\square$

**Theorem (leading Wilson relative entropy).** For the occupied-band projector of the specified infinite chain, compressed to $L$ cells, with $m=\mu/L$ and fixed $\mu>0$,
\[
\boxed{\mathcal D(C_{L,\mu/L}\Vert C_{L,0})
=\frac{\mu^2}{6}\log L+O_\mu(1).}
\]

*Proof.* The exact four-branch identity has $\mathcal P_L=(\mu^2/6)\log L+O_\mu(1)$, $\mathcal Q_N=O_\mu(1)$, $\Delta S_L=O_\mu(1)$, and the bounded modular term just proved. Adding these estimates yields the result. The bounded nonlinear and entropy estimates used here are distinct from the stronger finite-part estimates cited below. $\square$

A bounded remainder alone need not have a limit, and the fixed-interior expansion alone does not control a moving edge window or the full modular norm. In the specified half-filled model, the additional estimates are supplied by the exact-connection arguments of *Finite Part of Wilson–Dirac Relative Entropy* and *Uniform Modular Control and Nonlinear Convergence for Wilson–Dirac Intervals*. They determine the finite part and give $\|E_N\|\le7$ without proving a moving-edge expansion.

## Fixed-positive-scaled-mass expansion

**Fixed-positive-scaled-mass relative-entropy expansion.** For the interval restrictions of the infinite-chain Wilson–Dirac occupied-band projectors, with the massive covariance in the first argument, $m=\mu/L$ and fixed $\mu>0$, Theorem 1 of *Finite Part of Wilson–Dirac Relative Entropy* gives
$$\mathcal D_L(\mu)=\frac{\mu^2}{6}\log L+\mu^2\left(\frac{13}{36}-\frac{\pi}{12}-\frac{\log\mu}{6}\right)-\mathcal S(\mu)+O_\mu((\log L)^{-1}).$$
Here $\mathcal S(\mu)$ is the finite cross-boundary trace path defined in Section 7 of that manuscript. It is not a difference of divergent continuum entropy traces. The constants and asymptotic onset may depend on $\mu$, and the stated rate is not claimed sharp.

**Proof.** Use the exact four-term decomposition, the two-bond expansion, Theorem 7 and Corollary 5 of *Finite Part of Wilson–Dirac Relative Entropy*, and its Section 7 boundary trace-path assembly. Their errors are $O_\mu(\log L/L)$, $O_\mu((\log L/L)^{1/3})$, $O_\mu(L^{-1/2})$ and $O_\mu((\log L)^{-1})$, respectively. The last bounds their sum for sufficiently large $L$. The two explicit scalar constants combine to $13/36-\pi/12-(\log\mu)/6$.

### A separate sufficient conditional expansion

::: {#thm:main .theorem}
**Theorem** (Conditional fixed-positive-mass Wilson relative-entropy expansion). *For the Wilson model specified by the Bloch Hamiltonian and covariance definitions, assume the nonlinear finite-part convergence and the uniform reference-modular moving-window and global logarithmic-envelope estimates stated above. The entropy finite-part rate is the proved boundary-subsystem theorem above. Then for every fixed $\mu>0$, $$\label{eq:main}
\boxed{\mathcal D_L(\mu)=\frac{\mu^2}{6}\log L+
\mu^2\left(\frac{13}{36}-\frac\pi{12}-\frac{\log\mu}{6}\right)-\mathcal S(\mu)+\mathcal O_\mu((\log L)^{-1/103}).}$$ The big-$O$ is as $L\to\infty$ through positive integers, with $\mu$ fixed. No claim is made of a sharp exponent, a practically useful finite-$L$ onset, or a bound uniform for moving $\mu$.*
:::

::: proof
*Proof.* Define the exact residuals $$\begin{aligned}
R_P&=\mathcal P_L-\frac{\mu^2}{6}\log L-\mu^2(\tfrac16\log(8/\mu)-\tfrac14),&
R_Q&=\mathcal Q_N-\mu^2c_\eta,\\
R_M&=\mathcal F_L,&R_S&=\Delta S_L-\mathcal S(\mu).
\end{aligned}$$ By the finite decomposition and constant identity, their combination is an *exact finite-$L$ identity*: $$\label{eq:residual}
\mathcal D_L(\mu)-\frac{\mu^2}{6}\log L
-\mu^2\Bigl(\frac{13}{36}-\frac\pi{12}-\frac{\log\mu}{6}\Bigr)+\mathcal S(\mu)=R_P+R_Q+R_M-R_S.$$ The component remainder estimates give respectively $R_P=\mathcal O_\mu(\log L/L)$, $R_Q=\mathcal O_\mu((\log L/L)^{1/3})$, $R_M=\mathcal O_\mu((\log L)^{-1/103})$, and $R_S=\mathcal O_\mu(1/\log L)$. Apply the triangle inequality to the specified residual formula; only the modular term dominates asymptotically. The required lower bounds on $L$ can be satisfied simultaneously because $\mu$ is fixed; $\log N=\log L+\log2$ preserves the modular rate. $\square$
:::

::: remark
**Remark 15** (Limits of the conclusion). *At $\mu=0$, the two states coincide and $\mathcal D_L(0)=0$, but the fixed-positive-mass hypotheses do not imply a uniform remainder in any shrinking-mass window. The compressed infinite-chain construction is not an open finite-chain ground state; the finite-size scaling is not an independent continuum reconstruction or a statement about infinite-volume relative entropy.*
:::

## Limitations of the conditional asymptotic

| $\mu$ | Direct covariance calculation | Four-term scalar decomposition | Absolute difference |
|---:|---:|---:|---:|
| $0.5$ | $0.216474955427$ | $0.216474955427$ | $9.5\times10^{-15}$ |
| $2.0$ | $0.879738032942$ | $0.879738032942$ | $2.6\times10^{-15}$ |

*Finite-dimensional normalization checks at $L=3$.* These check the algebraic decomposition, not the limiting remainder.

These tests do not certify uniform estimates for all $L$, nor replace the complete upstream Coulomb and trace-ideal arguments. Reference endpoint eigenvalues can be much smaller than double-precision roundoff; finite-matrix logarithms must use verified multiprecision or a strict spectral enclosure at sizes where this matters.

The estimates used in the fixed-positive-scaled-mass expansion have the following scopes. Nonlinear correction: $\mathcal Q_N=\mu^2c_\eta+O_\mu(\sqrt{\log N/N})$, by Theorem 6 of *Uniform Modular Control and Nonlinear Convergence for Wilson–Dirac Intervals*. Modular correction: $\|E_N\|\le7$, longitudinal trace $O_\mu(N^{-1})$, and full modular trace $O_\mu(\sqrt{\log N}/N)$, by its Theorem 3 and Corollary 4. Cross-boundary entropy: $\Delta S_L=\mathcal S(\mu)+O_M(1/\log L)$ for the specified boundary subsystem, uniformly for $0\le\mu\le M$. The first two full-model statements are made at fixed positive $\mu$; the boundary subsystem's uniformity does not by itself extend the complete entropy theorem to moving $\mu$.


The separate $1/103$ sufficient route retains its displayed moving-window hypotheses. It is a conditional fixed-$\mu$ asymptotic bound, not a useful numerical error certificate at moderate lattice lengths. The fixed-$\mu$ theorem stated above has the stronger $O_\mu(1/\log L)$ remainder.

## Appendix A. Explicit finite-dimensional nonlinear estimate {#app:errors}

For the exact Wilson model, and under the all-degree Fourier-walk and staggered-trace estimates, put $N=2L\ge\mu>0$, $r=\mu/(N+\mu)$, let $K\ge1$ be an integer, and set $$d_*(r)=\frac{2r}{\pi\sqrt{1-r^2}}\operatorname{arsinh}\frac{\sqrt{1-r^2}}r,
\qquad H(r)=\frac14+\frac38\log\frac1r.$$ Then the upper bound is $$\begin{aligned}
\label{eq:explicit}
|\mathcal Q_N-\mu^2c_\eta|\le B_{N,\mu,K}:={}&\frac{45}{\pi\sqrt2}Nr^2(1+\log(1/r))K(K+1)\nonumber\\
&+\frac{\pi}{24\sqrt2}N^2r^4H(r)+\frac{2c_\eta\mu^3}{N}\nonumber\\
&+\frac{\mu^2/8+2}{4\sqrt2 K}+\frac{\mu^2}{384K^3}
+3\zeta(3/2)d_*(r).
\end{aligned}$$ The terms respectively control finite walk averaging, the scalar difference, mass-scale normalization, finite and limiting series tails, and the staggered contribution. The bound is conservative for moderate $N$. It is valid under the uniform analytic lemmas, not an independently calibrated error bar.

## Appendix B. Quantifiers and operator topologies {#app:quant}

| Symbol / condition | Meaning and restriction |
|---|---|
| $L$, $N=2L$ | $L$ consecutive two-orbital cells; $N$ scalar coordinates after the interval unitary |
| $m=\mu/L$ | Bare Wilson mass; $\mu>0$ is fixed before $L\to\infty$ |
| $P_m$ | Negative-band projector of the infinite-chain Bloch Hamiltonian, **not** a finite-open-chain spectral projector |
| $A_L,B_L$ | Restrictions of massive and massless infinite-chain quasifree covariances; massive state is the first relative-entropy argument |
| $B_N,J_N$ | Massless scalar reference and commuting Jacobi operator; massive perturbation need not commute |
| $\eta$ | Exact infinite reference scaling series; $-N\eta(J_N/N)$ approximates, but does not define, the finite modular operator |
| $\mathbb D_\mu$ | Continuum cross-boundary perturbation defining the finite entropy trace path; not a continuum density matrix |
| $0<s<1/2$ | Fractional Sobolev nuclear regularity range for interval cutoff |
| $h=2+|\lambda|$ | Reference spectral scale; positive-arc window valid only with uniform reference geometry and matching assumptions |
| $\mathcal O_\mu$ | Implicit constants may depend on fixed $\mu$ |
| $N\ge\mu$ | Sufficient condition for the quoted nonlinear finite bound, giving $r\le1/2$ |
| $\mu=0$ | Identical finite comparison states, not proof of a full theorem uniform as $\mu\downarrow0$ |

## Appendix C. Analytical estimates for the conditional theorem {#app:analytic-estimates}

### C.1 Cross-boundary approximation and entropy bound

Set $a_L=L\log(1+\mu/L)$ and $L\ge\max(1,2\mu)$. The independent rank-one Laplace decomposition for the two boundary channels gives the explicit trace-norm estimate
$$\boxed{\|Z_{L,\mu}-Z_\mu\|_1\le\frac{a_L}{\pi L}\left(40+10\log\frac{2L}{a_L}\right)+(1+\sqrt2)C_{\rm ent}(\sqrt\mu-\sqrt{a_L}).}$$
Here $C_{\rm ent}>0$ is the finite explicit constant from the rank-one factor estimates in the supplementary derivation. The difference $\sqrt\mu-\sqrt{a_L}$ is nonnegative because $\log(1+x)\le x$. This bound implies $O_M((\log L)/L)$ for $0\le\mu\le M$, interpreted continuously at $\mu=0$.

The proof uses convergent binomial Fourier expansions rather than a contour deformation. For the continuum kernels, the integral identities for $K_0,K_1$ identify the half-line Fourier kernels of $(\mu-iu)/\sqrt{\mu^2+u^2}$, with the opposite boundary orientation tracked explicitly. The rank-one factorization yields, for $0<s<1/2$,
$$\|\mathbb D_\mu\|_{\mathcal S_1(L^2,H^s)}\le C_s\sqrt\mu.$$
The range $s<1/2$ is dictated by the fractional Sobolev cutoff. The separate interpolation bound $\|Y_L-Y\|_{H^s\to L^2}\le C_sL^{-s}$ requires the full-line step-projection identity, including alias contributions; dropping aliases would invalidate that argument.

Writing $g(z)=F'(z/2)=-2z\log|z|+r(z)$ with $r\in C^2[-1,1]$, the Chebyshev coefficients decay as $O(k^{-2})$. The degree-$n$ truncation approximates $g$ within $C/n$, and its monomial coefficient norm is $O(7^n)$. The telescoping identity
$$ (Y_L^k-Y^k)\mathbb D_\mu=\sum_{j=0}^{k-1}Y_L^j(Y_L-Y)Y^{k-1-j}\mathbb D_\mu $$
uses $H^s$ regularity only on the **rightmost continuum** factor. Choosing $n$ proportional to $\log L$ with a sufficiently small coefficient yields
$$ \sup_{0\le\mu\le M}|\Delta S_L(\mu)-\mathcal S(\mu)|=O_M((\log L)^{-1}). $$
Equations (B5)–(B8) and the finite trace-path lemma of the boundary supplement prove this **entropy-subsystem estimate** for the specified Wilson model. This proves the boundary contribution only. The separate nonlinear and reference-modular convergence estimates used in the full fixed-$\mu$ theorem are proved in *Finite Part of Wilson–Dirac Relative Entropy* and sharpened in *Uniform Modular Control and Nonlinear Convergence for Wilson–Dirac Intervals*.

### C.2 Uniform all-degree Jacobi estimate

For $N\ge2$ let $T_N$ be the $N\times N$ tridiagonal matrix with bond $\beta_j=j(N-j)/N^2$. Every odd $p\ge1$, **even when $p\ge N$**, obeys the analytic inequality
$$ \boxed{\sum_{\substack{1\le a<N\\a\text{ odd}}}\left|\sum_{i=0}^{N-a-1}(-1)^i(T_N^p)_{i,i+a}\right|\le\frac{4\sqrt p\,2^{-p}}N.} $$
For a nearest-neighbor path $\omega=(\epsilon_1,\ldots,\epsilon_p)$, its zero-extended weight is $P(x)=\prod_{\ell=1}^p\beta_+((x+b_\ell)/N)$ with $\beta_+(z)=\max(z(1-z),0)$. Its logarithmic derivative is monotone between the real external roots, and the derivative variation estimate gives $\|P''\|_{\rm TV}\le 32\sqrt p\,4^{-p}/N$ in lattice start-coordinate scaling, counting endpoint atoms. Cardinal triangular interpolation and $\sum_i(-1)^i\Delta^2P(i)=-4\sum_i(-1)^iP(i)$ bound one path by $8\sqrt p\,4^{-p}/N$; summation over at most $2^{p-1}$ positive-displacement paths proves the displayed inequality. This argument applies to both odd and even matrix dimensions.

Together with the proved Wilson covariance splitting and its Fourier coefficient bound, the staggered coefficient consequently improves to $\zeta(3/2)d_*(r)$, with no change to the stated nonlinear convergence rate. The all-degree Jacobi lemma alone does not yield the finite-part nonlinear limit or uniform positive-arc/Coulomb matching.

### C.3 Conditions required for the modular conclusion

The positive spectral majorant has the separately derived tail bound
$$ \operatorname{Tr}(G_N\mathbf1_{\{|J_N|>R\}})\le\min\left\{\frac\mu\pi,\sqrt{\frac2{15}}\frac{\mu^2}{\pi R}+\frac\mu{3\pi R^2}\right\}. $$
For a positive measure with $\nu((t,\infty))\le D/t$, layer-cake integration proves for $\alpha>1$
$$ \int_0^\infty\log(1+(t/\rho)^\alpha)\,d\nu(t)\le\frac{\pi D}{\rho\sin(\pi/\alpha)}. $$
Taking $\alpha=103$ supplies the claimed inverse-log rate **only after** the model-specific Coulomb/turning-point estimates and reference occupation identities have been established uniformly on their moving windows. The logarithm $\log(1+Ch^{103}/\log N)$ must not be linearized over the entire $h=O(\sqrt{\log N})$ window. The sufficient asymptotic onset can be astronomically large; the asymptotic cannot be presented as a small-$L$ error certificate.

The moving-window conditions in this subsection are sufficient for the conditional $1/103$ estimate, and no assertion that they hold is needed for the fixed-positive-scaled-mass finite part. The complete $O_\mu(1/\log L)$ theorem instead follows from the modular and nonlinear estimates and the boundary trace path identified above. A uniform moving-edge expansion remains a separate problem.

## References

1. H. Araki, "On Quasifree States of CAR and Bogoliubov Automorphisms," *Publications of the Research Institute for Mathematical Sciences* **6** (1971), 385–442, doi:10.2977/prims/1195193913.

2. National Institute of Standards and Technology, *Digital Library of Mathematical Functions*, §19.12 (elliptic integrals) and §10.32 (modified-Bessel integral representations).

3. D. Slepian, "Prolate Spheroidal Wave Functions, Fourier Analysis, and Uncertainty V: The Discrete Case," *Bell System Technical Journal* **57** (1978), 1371–1430, doi:10.1002/j.1538-7305.1978.tb02104.x.

4. F. A. Grünbaum, "Eigenvectors of a Toeplitz Matrix: Discrete Version of the Prolate Spheroidal Wave Functions," *SIAM Journal on Algebraic Discrete Methods* **2** (1981), 136–141, doi:10.1137/0602017.

5. V. Eisler and I. Peschel, "Analytical Results for the Entanglement Hamiltonian of a Free-Fermion Chain," *Journal of Physics A* **50** (2017), 284003, doi:10.1088/1751-8121/aa76b5.

6. V. V. Peller, *Hankel Operators and Their Applications*, Springer (2003), doi:10.1007/978-0-387-21681-2.

7. K. Justus, *Uniform Bulk Modular Asymptotics and the Leading Wilson Entropy Law*, research manuscript, October 2026. See the exact differential-tail input and uniform integrated Riccati residual proof therein.

## Acknowledgments and contributions

Kirtus Justus directed the research questions, mathematical scope and publication decisions and is the sole named author. ChatGPT (OpenAI) assisted in developing and checking the Wilson majorant, boundary, nonlinear and reference-modular arguments and preparing the manuscripts. Claude (Anthropic), Gemini (Google), Grok (SpaceXAI), and DeepSeek (High-Flyer) are acknowledged for contributions to the wider research effort, without assigning these particular derivations to them absent specific provenance. Responsibility for the scientific text rests with the named author.
