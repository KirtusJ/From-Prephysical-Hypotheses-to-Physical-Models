# Interval susceptibility at the singular mass direction

Use the half-filled, two-orbital infinite Wilson–Dirac chain, compressed to L cells as in Z33 D1, assembled p.4, Eqs. (2)–(4), pin `0ca75f60c76af1be7f3c25c2ed8914e82243ff5d`. Logarithms are natural. Write $B=C_{L,0}$, $\Delta=C_{L,\mu/L}-B$, $m=\mu/L$, $h=\log(1/\mu)$. Throughout the joint statements, $L\to\infty$ and $\mu\to0^+$.

**Two joint estimates.** For every such sequence,

$$
 \liminf \frac{\mathcal D_L(\mu)}{\mu^2 h^2}\ ≥\ \frac16 .
$$

When $h/[\sqrt L(1+\sqrt 2)^{2L}]\to\infty$, there is equality in the stronger sense

$$
 \mathcal D_L(\mu)\sim\frac16 \mu^2 h^2 .
$$

The sufficient condition in the second statement is severe. For example it covers $\mu_L=\exp[-\exp(4L)]$. The first one already excludes the fixed-positive-mass relative coefficient along $\mu_L=\exp[-a\sqrt{\log L}]$ whenever $a>1$, since the liminf after division by $\mu^2\log L/6$ is then at least $a^2$. For $\mu_L=L^{-b}$, $b>0$, it gives a lower bound of order $\mu_L^2\log^2 L$. It does not establish equality on polynomial sequences.

## Rank-two approximation of the finite covariance

Let $u=L^{-1/2}(1,\ldots,1)$, $Q_L=|u\rangle\langle u|\otimes\sigma_z$, $a=\mu h/(2\pi)$. Uniformly for $L\ge1$, $0<\mu<1$,

$$
 \|\Delta+aQ_L\|_{\rm HS}\le C\mu.                                         \tag{1}
$$

This is an operator estimate. For $|k|\le 1/L$ express the compression as an integral of $L|u(k)\rangle\langle u(k)|\otimes[P_m(k)-P_0(k)]$, with $u_j(k)=L^{-1/2}e^{ijk}$, against $dk/(2\pi)$. The part $|k|<m$ has Hilbert–Schmidt norm $O(Lm)$. For $m\le|k|\le1/L$, the difference of projectors is $O(m/|k|)$ by differentiation of the normalized Bloch vector. Replacing $u(k)$ by $u$ costs $O(L\int_m^{1/L}(m/k)Lk\,dk)=O(\mu)$. The odd $\sigma_x$ part then cancels. The even z-component has coefficient

$$
 -\frac{L}{2\pi}\int_m^{1/L}(g_m-g_0)\,dk,
 \quad g_t(k)=\frac{t+1-\cos k}{\sqrt{\sin^2k+(t+1-\cos k)^2}}.
$$

For $t\le m\le k\le1/L$, direct differentiation gives

$$
 k\partial_tg_t=\frac{k\cos^2(k/2)}{2\sin(k/2)}
 \left(1+t+\frac{t^2}{4\sin^2(k/2)}\right)^{-3/2}
 =1+O(k^2+m+(m/k)^2).
$$

Integrating the error over t and k costs $O(\mu)$ in the compression. This leaves $-aQ_L$. Finally the higher-momentum symbol difference satisfies $\|P_m(k)-P_0(k)\|\le C m/|k|$ on the Brillouin zone by differentiating the Bloch projector and using $E_t(k)\ge 2\sin(|k|/2)$. The squared Hilbert–Schmidt norm of its Toeplitz compression is at most $L\int_{|k|>1/L}\|P_m-P_0\|_{\rm HS}^2 dk/(2\pi)=O(\mu^2)$ by Parseval. All constants are absolute.

## Endpoint spectral weights of the massless reference

The exact scalarization in D1 p.4, Eq. (6), or D8 part 3, Thm 1, pp.17–18, takes $B$ to the N-by-N sine kernel $B_N$, $N=2L$, the compression of the arc $[-\pi/2,\pi/2]$. It sends the constant-spatial two-spin subspace onto the span of $e_\pm=N^{-1/2}(e^{\pm i\pi j/2})_{j=0}^{N-1}$. Indeed the on-site unitary is fixed up to the cell factor $(-1)^j$, and both edge vectors have that cell factor. They are orthogonal for even N.

Let $P_x=1_{[0,x]}(B_N)$. For any unit $v\in\mathrm{ran}\,P_x$, let $p(q)=\langle e(q),v\rangle$, where $e(q)=N^{-1/2}(e^{ijq})_j$. We have $|p'|\le N$, $|p|\le1$. An endpoint value of magnitude A forces $|p|\ge A/2$ on a length $A/(2N)$ inside the arc, so

$$
 x\ge\langle v,B_Nv\rangle={N\over2\pi}\int_{-\pi/2}^{\pi/2}|p(q)|^2dq\ge A^3/(16\pi).
$$

Taking the supremum in v gives $\|P_x e_\pm\|^2\le(16\pi x)^{2/3}$. The complement arc gives the same for $1-B_N$. Consequently on the two-dimensional subspace, with E its orthogonal embedding,

$$
 \|E^*(B+t)^{-1}E\|+\|E^*(I-B+t)^{-1}E\|\le C\min(t^{-1/3},t^{-1}).
                                                                             \tag{2}
$$

For t≤1 integrate the cumulative spectral mass bound by parts, or sum over dyadic intervals beginning at t. For t≥1 use the resolvent norm. Bounds for linear combinations follow by Cauchy–Schwarz over the two edge vectors. Squaring the right-hand side gives an integrable majorant in $t\in(0,\infty)$.

## Resolvent at the massless continuum interval

For fixed $t>0$, both compressed resolvents in (2) tend in their two-dimensional space to $r(t)I_2$, where $r(t)=\log(1+1/t)$.

One elementary route uses the original physical spin basis. Isometrically embed lattice vectors into continuum step functions on cells of width $1/L$, using amplitude $\sqrt L$; the constant spatial vector becomes the function 1 on $(0,1)$ exactly. The embedded infinite massless Fourier projector converges strongly to the continuum multiplier $(I-\operatorname{sgn}(k)\sigma_x)/2$. For band-limited test inputs the base-band matrix elements converge by pointwise convergence of the symbols and the cell sinc form factor; the base-band output therefore converges weakly to the continuum projection. The norm squared of the lattice output equals the matrix element of the projector on the input, which tends to the continuum projection norm squared. This gives strong convergence even in the presence of output aliases. Density gives the full result; see also Z33 D8 part 1, p.6, and p.9 Eq. (B8). Compress on both sides by the fixed unit interval and use the resolvent identity. Although the lattice operator is zero on the orthogonal complement of the step functions, our two vectors belong to its step subspace. The same reasoning applies to its complement resolvent.

In the $\sigma_x$ eigenbasis these interval blocks are $B_\pm=(I\pm iH)/2$, up to interchange, where $Hf(x)=\pi^{-1}\,\mathrm{PV}\int_0^1 f(y)/(x-y)dy$. Under $x=e^v/(1+e^v)$, the unitary map $Wf(v)=\sqrt{x(1-x)}f(x)$ sends H to convolution with $1/[2\pi\sinh(v/2)]$. Its multiplier is $-i\tanh(\pi s)$. For instance, expand the odd kernel on the positive half-line into exponentials and sum $\sum_{n\ge0}[(n+1/2)^2+s^2]^{-1}=\pi\tanh(\pi s)/(2s)$, the logarithmic derivative of Euler's product for cosh. With the unitary Fourier convention,

$$
 |\widehat{W1}(s)|^2=\frac{\pi}{2}\operatorname{sech}^2(\pi s).
$$

This follows directly from $W1(v)=[2\cosh(v/2)]^{-1}$, the substitution $u=e^v$, and $\int_0^\infty u^{z-1}/(1+u)du=\pi/\sin(\pi z)$ at $z=1/2-is$. The scalar eigenvalue $b_\pm(s)=(1\pm\tanh(\pi s))/2$ has $|db_\pm/ds|=|\widehat{W1}|^2$. Its spectral measure in the constant orbital is thus exactly Lebesgue measure on (0,1), for both spin chiralities. Their cross elements vanish. Integrating $(b+t)^{-1}$ proves the claimed limit of r(t). These are constant-orbital spectral probabilities, not the unweighted eigenvalue distribution of the interval covariance.

## Entropy Hessian and two-parameter consequences

For finite matrices write $f(x)=x\log x+(1-x)\log(1-x)$. The entropy is the Bregman divergence of $\operatorname{Tr}f$. Integrating its trace Hessian along the line gives

$$
 D(B+\Delta\|B)=\int_0^1(1-s)\mathsf H_{B+s\Delta}(\Delta,\Delta)ds,
$$

$$
 \mathsf H_C(X,X)=\sum_{T=C,I-C}\int_0^\infty
 \operatorname{Tr}[(T+t)^{-1}X(T+t)^{-1}X]dt .                           \tag{3}
$$

The integrands are nonnegative squared Hilbert–Schmidt norms of $(T+t)^{-1/2}X(T+t)^{-1/2}$. This derivation is valid for finite positive contractions strictly inside both endpoints, the specified finite covariances.

First, for $X=Q_L=E\sigma_zE^*$, each integrand is bounded in absolute value by twice the square of (2) and tends to $2r(t)^2$. Thus dominated convergence gives

$$
 \mathsf H_B(Q_L,Q_L)\longrightarrow4\int_0^\infty\log^2(1+1/t)dt=4\pi^2/3.        \tag{4}
$$

Integration by parts gives $2\int_0^1[-\log v]/(1-v)dv=2\sum_{n\ge1}n^{-2}=\pi^2/3$ for the single integral.

**Joint lower bound.** Restrict (3) to $\delta\le t\le R$ before taking limits, with $0<\delta<R<\infty$. This gives a lower bound by positivity. There $\|\Delta\|\to0$ and (1) gives $\Delta/a=-Q_L+O_{\rm HS}(1/h)$; resolvent identities bound every replacement error uniformly in $s\in[0,1]$. Thus the liminf of $D/a^2$ is at least $2\int_\delta^R r(t)^2dt$. Send $\delta\downarrow0$, $R\uparrow\infty$. Substitution of a yields the coefficient $1/6$. The argument makes no estimate uniform at t=0 for the perturbed covariance.

**Upper and equality in a sufficient joint sector.** Set $g_L=\min\{\lambda_{\min}(B),\lambda_{\min}(I-B)\}$. D2, assembled p.8, Thm 7, Eq. (42), bounds the complete reference logit norm by $\pi N$. Thus $g_L\ge(1+e^{2\pi L})^{-1}$. More intrinsically for this proof, it suffices that $h\sqrt{g_L}\to\infty$; the D2 bound supplies the sufficient sector $h e^{-\pi L}\to\infty$. Then $a/g_L\to0$: indeed $g_L^{-1}=o(h^2)$, $a=e^{-h}h/(2\pi)$. By (1), $\varepsilon=\|\Delta\|/g_L\to0$. For $0\le s\le1$, each resolvent in (3) is bounded in Loewner order between $(1+\varepsilon)^{-1}$ and $(1-\varepsilon)^{-1}$ times its counterpart at B (the same holds for the complement). The quadratic integrand has the corresponding squared factors because its matrix on vectorized X is $R^{\mathsf T}\otimes R$, monotone for positive R. Therefore $D=(1+o(1))\mathsf H_B(\Delta,\Delta)/2$. Writing $X=\Delta+aQ_L$, (1) gives $\mathsf H_B(X,X)\le2g_L^{-1}\|X\|_{\rm HS}^2=O(\mu^2/g_L)=o(a^2)$. The triangle inequality for the Hessian norm and (4) yield $D/a^2\to2\pi^2/3$, proving the matching upper and lower coefficient.

**A sharper elementary reduction to a published polynomial bound.** Apply the sharp complex-polynomial Remez inequality, Tikhonov and Yuditskii, *Sharp Remez inequality*, Thm 1.2, [arXiv:1809.09726v2](https://arxiv.org/abs/1809.09726v2). For a polynomial p of degree at most N−1 with unit coefficient norm, Parseval gives $\sup_{\mathbb T}|p|\ge1$. Let $\lambda=(2\pi)^{-1}\int_{\mathrm{arc}}|p|^2$ on a semicircle. On that arc the set where $|p|>\sqrt{2\pi N\lambda}$ has length at most $1/N$, so the retained set has length at least $\pi-1/N$. The theorem gives

$$
1\le\sup|p|\le\sqrt{2\pi N\lambda}\, T_{N-1}\left(\sec[(\pi+1/N)/4]\right)
\le C\sqrt{N\lambda}\,(1+\sqrt2)^N .
$$

Indeed $\operatorname{arcosh}(\sec v)$ has bounded derivative near $v=\pi/4$, and its value there is $\log(1+\sqrt2)$. Both semicircles obey the bound, hence $g_L\ge c/[N(1+\sqrt2)^{2N}]$. With N=2L this gives the explicit sufficient condition in the opening, independently of D2's concentration analysis.

**Limit of this approach.** For polynomially small $\mu$, (1) alone does not control the small-t remainder in the entropy Hessian. Even when the reference eigenvalue is b, a rank-one error $x$ in that eigenspace has Hessian $x^2/[b(1-b)]$. Thus a Hilbert–Schmidt bound by itself loses an inverse spectral gap. The two special constant-orbital directions avoid that loss by (2); the full Wilson remainder needs additional spectral localization or cancellation. No sharp polynomial-sector upper bound is established here.

## Finite check

The accompanying [susceptibility.py](susceptibility.py) constructs the issued finite sine kernel and diagonalizes it at increased precision. It computes the trace Hessian by divided differences in the finite reference eigenbasis, independently of the continuum transform. The estimates of the coefficient at L=1, 4, 16 and 24 are respectively 0.1703692330, 0.1669206969, 0.1666829226 and 0.1666738965. The limiting value is 1/6. The precise outputs are in [susceptibility.txt](susceptibility.txt).

## Lattice sources

[D1, p. 4, symbol, covariance and entropy](https://github.com/KirtusJ/From-Prephysical-Hypotheses-to-Physical-Models/blob/0ca75f60c76af1be7f3c25c2ed8914e82243ff5d/edition/PAPERS/D1_Relative_Entropy_of_Finite_Interval_Wilson_Dirac_Quasifree_States/D1_Relative_Entropy_of_Finite_Interval_Wilson_Dirac_Quasifree_States.pdf#page=4) · [D2, p. 8, Thm 7 and Eq. (42)](https://github.com/KirtusJ/From-Prephysical-Hypotheses-to-Physical-Models/blob/0ca75f60c76af1be7f3c25c2ed8914e82243ff5d/edition/PAPERS/D2_Uniform_Bulk_Modular_Asymptotics_and_the_Leading_Wilson_Entropy_Law/D2_Uniform_Bulk_Modular_Asymptotics_and_the_Leading_Wilson_Entropy_Law.pdf#page=8) · [D8, pp. 8–10, Eqs. (B7)–(B9)](https://github.com/KirtusJ/From-Prephysical-Hypotheses-to-Physical-Models/blob/0ca75f60c76af1be7f3c25c2ed8914e82243ff5d/edition/PAPERS/D8_Wilson_Dirac_Covariance_Majorant_and_Boundary_Estimates/D8_Wilson_Dirac_Covariance_Majorant_and_Boundary_Estimates.pdf#page=9) · [D8, pp. 17–18, scalarization](https://github.com/KirtusJ/From-Prephysical-Hypotheses-to-Physical-Models/blob/0ca75f60c76af1be7f3c25c2ed8914e82243ff5d/edition/PAPERS/D8_Wilson_Dirac_Covariance_Majorant_and_Boundary_Estimates/D8_Wilson_Dirac_Covariance_Majorant_and_Boundary_Estimates.pdf#page=17)
