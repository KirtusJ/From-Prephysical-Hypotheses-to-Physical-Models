# The full relative-entropy coefficient at fixed Wilson interval length

Let L be the number of two-orbital cells, m=μ/L, and take μ positive. The finite relative entropy is massive first, on the infinite chain compressed to L cells, with natural logarithms. Its fixed-L small-mass expansion and the limit of its leading coefficient are

$$
 \mathcal D_L(\mu)=\kappa_L\mu^2\log^2(1/\mu)
                  +O_L\!\big(\mu^2\log(1/\mu)\big),
 \qquad \lim_{L\to\infty}\kappa_L=\frac16.
$$

The error constant can depend on L. This result establishes an iterated limit. At one cell $\kappa_1=1/(\pi^2-4)$. The following finite formula, convergence proof and numerical controls refer to the exact Wilson covariance. [D1, p. 4, Eqs. (2)–(4)](https://github.com/KirtusJ/From-Prephysical-Hypotheses-to-Physical-Models/blob/0ca75f60c76af1be7f3c25c2ed8914e82243ff5d/edition/PAPERS/D1_Relative_Entropy_of_Finite_Interval_Wilson_Dirac_Quasifree_States/D1_Relative_Entropy_of_Finite_Interval_Wilson_Dirac_Quasifree_States.pdf#page=4) · [D8, part 3, Thm 1, pp. 17–18](https://github.com/KirtusJ/From-Prephysical-Hypotheses-to-Physical-Models/blob/0ca75f60c76af1be7f3c25c2ed8914e82243ff5d/edition/PAPERS/D8_Wilson_Dirac_Covariance_Majorant_and_Boundary_Estimates/D8_Wilson_Dirac_Covariance_Majorant_and_Boundary_Estimates.pdf#page=17) · [D8, part 7, Prop. 5, p. 32](https://github.com/KirtusJ/From-Prephysical-Hypotheses-to-Physical-Models/blob/0ca75f60c76af1be7f3c25c2ed8914e82243ff5d/edition/PAPERS/D8_Wilson_Dirac_Covariance_Majorant_and_Boundary_Estimates/D8_Wilson_Dirac_Covariance_Majorant_and_Boundary_Estimates.pdf#page=32)

## Orbital basis and the finite trace Hessian

The occupied-band symbol is $\tfrac12[I-(\sin k\,\sigma_x+(m+1-\cos k)\sigma_z)/E_m(k)]$, $E_m^2=m^2+4(1+m)\sin^2(k/2)$. Let $A=C_{L,m}$, $B=C_{L,0}$, $e=L^{-1/2}(1,\ldots,1)^T$. At fixed L, in the original orbital basis,

$$
 A-B=-\frac{\mu\log(1/\mu)}{2\pi}|e\rangle\langle e|\otimes\sigma_z+O_L(\mu).
\tag{1}
$$

Here and below the finite-matrix error can be taken in operator norm. Write $g_t(k)=(t+1-\cos k)/E_t(k)$. For fixed integer displacement d the z-block difference is $-\int_0^\pi \cos(dk)(g_m-g_0)\,dk/(2\pi)$. On $(0,m)$, $0\le g_m-g_0\le1$. For $m\le k\le1$ and $0\le t\le m$,

$$
 k\partial_tg_t=\frac{k\cos^2(k/2)}{2\sin(k/2)}
       \left[1+t+\frac{t^2}{4\sin^2(k/2)}\right]^{-3/2}
       =1+O(k^2+m+(m/k)^2).
$$

Integration gives $m\log(1/m)+O_d(m)$; multiplying by $\cos(dk)$ changes the integral by $O_d(m)$ because $|\cos(dk)-1|\le d^2k^2/2$. On $[1,\pi]$ the integrand is $O(m)$. The x-block contains $\sin(dk)[\sin k/E_m-\sin k/E_0]$. For $k<m$ the bracket is bounded. For $m\le k\le1$, its absolute value is at most $C[m+(m/k)^2]$, as follows by taking the reciprocal square root of the bracket above with exponent $-1/2$ and using $|\sin k/E_0|\le1$. This integrates to $O(m)$. All cell pairs therefore have the same leading z-block, and $m\log(1/m)=(\mu/L)[\log(1/\mu)+\log L]$ gives (1).

For $f(x)=x\log x+(1-x)\log(1-x)$, the exact trace expression is $\mathrm{Tr}[f(A)-f(B)-f'(B)(A-B)]$. The eigenvalues $b_i$ of B are strictly between zero and one. Define

$$
 g(x,y)=\frac{\log(x/(1-x))-\log(y/(1-y))}{x-y},
 \qquad g(x,x)=\frac1{x(1-x)}.
$$

In the B eigenbasis, the trace Taylor expansion at B has quadratic term $\tfrac12\sum_{ij}g(b_i,b_j)|\Delta_{ij}|^2$, $\Delta=A-B$. The resolvent formula for the Fréchet derivative of $\log$ proves the divided difference, including repeated eigenvalues. Analyticity on a compact neighborhood of the fixed finite spectrum bounds the trace remainder by $O_L(\|\Delta\|^3)$. Substitution of (1) proves the stated error order at fixed L. The quadratic form uses both orbital sectors. Reversing the relative entropy would have the same Hessian but changes the finite trace formula.

## A single spectral measure gives the exact coefficient

Let $N=2L$, and $B_N=(b_{p-q})_{0\le p,q<N}$ with $b_0=1/2,\ b_d=\sin(\pi d/2)/(\pi d)$ for $d\ne0$. The unitary in D8, part 3, Theorem 1, is the direct sum of $(-1)^j RW$, with $R=\sigma_z$, $W=(I-i\sigma_x)H_2/\sqrt2$ and $H_2$ the normalized Hadamard. It conjugates the reference covariance to $B_N$ and sends $\sigma_z$ to $-\sigma_x$ in each unstaggered cell. Consequently the scalarized tangent in (1), after removing $\mu\log(1/\mu)/(2\pi)$, is

$$
 |r\rangle\langle r|-|s\rangle\langle s|,\quad
 r_{2j}=r_{2j+1}=\frac{(-1)^j}{\sqrt N},\quad s_n=(-1)^n r_n.
\tag{2}
$$

If $S$ is diagonal with entries $(-1)^n$, then $SB_NS=I-B_N$. Reversal $Jv_n=v_{N-1-n}$ commutes with $B_N$. The parity of r under J is $(-1)^{L-1}$, and s has the opposite parity. Thus the two quadratic-form cross terms vanish even in degenerate eigenspaces. The s spectral measure is the image of the r measure under $x\mapsto1-x$, and $g(1-x,1-y)=g(x,y)$. With $\nu_L(E)=\langle r,1_E(B_N)r\rangle$ one obtains

$$
 \boxed{\displaystyle \kappa_L=\frac1{4\pi^2}
      \int_0^1\int_0^1g(x,y)\,d\nu_L(x)\,d\nu_L(y).}
\tag{3}
$$

At L=1, r is an eigenvector at $1/2+1/\pi$. Formula (3) then gives $1/(\pi^2-4)$.

## The measures converge to the uniform distribution

Write $v_{\pm,n}=e^{\pm i\pi n/2}/\sqrt N$. These vectors are orthogonal, and $r=(1-i)v_+/2+(1+i)v_-/2$. Let $M_\pm$ be diagonal modulation by $e^{\pm i\pi n/2}$. The full-line lattice projections after demodulation have discrete Fourier multipliers $1_{[-\pi,0]}$ and $1_{[0,\pi]}$ respectively, since the unmodulated arc is $[-\pi/2,\pi/2]$. Define the isometry $E_N:\ell^2(\mathbb Z)\to L^2(\mathbb R)$ sending $u_n$ to $\sqrt N\,u_n$ on $[n/N,(n+1)/N)$. Its adjoint takes normalized cell integrals. It identifies time restriction $n=0,\dots,N-1$ with multiplication by $1_{[0,1]}$.

On the full line the embedded projections $E_N P_{\pm}E_N^*$ converge strongly to the usual negative and positive half-line Fourier projections $H_\pm$ (the orientation label on H follows the edge). Here is a direct check. For $\widehat f$ supported in $[-K,K]$ and $K<\pi N$, the discrete Fourier transform of $E_N^*f$ is supported in $[-K/N,K/N]$; the cell integral contributes only a scalar sinc and a phase. This follows by Fourier inversion on the support, without aliasing. Cutting positive or negative discrete frequency then agrees exactly with first applying the corresponding full-line projection and then cell-averaging. The embedded result is $E_NE_N^*H_\pm f\to H_\pm f$. Density of band-limited functions and uniform operator norm one prove strong convergence for any f. Multiplying on both sides by $1_{[0,1]}$ gives strong convergence of the finite demodulated covariances to the compressed half-line Fourier projections $C_\pm$. Products and polynomial functional calculus preserve strong convergence for this uniformly bounded sequence. Uniform approximation extends it to any continuous scalar test function on $[0,1]$, acting on $L^2(0,1)$ with the usual cell projections for the constant polynomial.

At either edge the embedded normalized vector is the constant function 1. Cross terms vanish. For example, in the plus frame the minus vector is the cell step function $(-1)^n$ on $[0,1]$. It converges weakly to zero, by cancellation on pairs of adjacent cells and density. The image of the constant vector under a continuous real spectral test in the plus frame converges in norm. These two facts give vanishing mixed matrix elements. Complex tests follow by decomposition into real and imaginary parts.

The scalar law of the constant function for $C_\pm$ can be computed explicitly. Set $u=\log(x/(1-x))$, $x=e^u/(1+e^u)$. The unitary change of variable $Tf(u)=\sqrt{x'(u)}f(x(u))$ sends the constant to $h(u)=1/(2\cosh(u/2))$. The principal-value Cauchy kernel of the half-line Fourier projection transforms, since

$$
 \frac{\sqrt{x'(u)x'(v)}}{x(u)-x(v)}
   =\frac1{2\sinh((u-v)/2)}.
$$

The two Fourier multipliers are $\lambda_\pm(\xi)=(1\pm\tanh(\pi\xi))/2$. Indeed, the nonidentity kernel in $C_\pm$ has coefficient $\pm i/(2\pi)$; the Fourier integral of the displayed principal-value kernel is $-i\pi\tanh(\pi\xi)$. This identity follows by summing the odd sine transform of the geometric expansion of $1/\sinh(t/2)$ on $t>0$, or by the residue theorem. Likewise $\int e^{-i\xi u}h(u)\,du=\pi/\cosh(\pi\xi)$, by the beta integral with $y=e^u$. With Plancherel normalization the spectral weight is $(\pi/2)\operatorname{sech}^2(\pi\xi)d\xi=|d\lambda_\pm|$. Each edge therefore contributes the uniform distribution on $[0,1]$; the two weights in r sum to one. The continuum diagonalization and the constant-vector weight also appear in Casini and Huerta, Eqs. (71), (73) and (74). [Authors' paper, pp. 10–11](https://arxiv.org/pdf/0903.5284v3#page=11)

## Endpoint control permits the trace-Hessian limit

Weak convergence alone does not justify the integral of g. For a unit vector $u$ in the spectral subspace $1_{[0,\lambda]}(B_N)$ put $F(q)=N^{-1/2}\sum_{n=0}^{N-1}u_ne^{-inq}$. Then $|F|\le1$, $|F'|\le N$, and

$$
 \frac{N}{2\pi}\int_{-\pi/2}^{\pi/2}|F(q)|^2\,dq
       =\langle u,B_Nu\rangle\le\lambda.
$$

If $|F(\pm\pi/2)|=a$, the adjacent inside segment of length $a/(2N)$ has $|F|\ge a/2$. Hence $a^3\le16\pi\lambda$. Since r is a sum of the two edge exponentials with coefficient absolute sum $\sqrt2$, take the supremum over all unit vectors in this subspace to obtain $\nu_L([0,\lambda])\le2(16\pi\lambda)^{2/3}$. Applying the same proof on the complementary arc gives the same bound for $\nu_L([1-\lambda,1])$.

With $R_L(t)=\int(x+t)^{-1}d\nu_L(x)$ and $\widetilde R_L(t)=\int(1-x+t)^{-1}d\nu_L(x)$, the logarithm divided difference gives

$$
 4\pi^2\kappa_L=\int_0^\infty
 [R_L(t)^2+\widetilde R_L(t)^2]\,dt .
$$

For $0<t<1$, integration by parts with the preceding distribution estimate bounds each transform by $C t^{-1/3}$, because $\int_0^1 x^{2/3}(x+t)^{-2}dx\le C t^{-1/3}$. For $t\ge1$, each is at most $t^{-1}$. The resulting bounds on the squares are integrable uniformly in L, so weak convergence now permits dominated convergence. The uniform law has $R(t)=\widetilde R(t)=\log(1+1/t)$. Substitution $s=\log(1+1/t)$ and expansion $e^s/(e^s-1)^2=\sum_{n\ge1} n e^{-ns}$ give $\int_0^\infty\log^2(1+1/t)\,dt=2\zeta(2)=\pi^2/3$. Thus $\kappa_L\to1/6$.

Casini and Huerta's continuum Eq. (75) gives the leading mass correction $-m^2L_t^2\log^2(m)/6$ to entanglement entropy, with total length $L_t$ fixed. The coefficient and constant-vector law have that prior derivation. The result above supplies a finite Wilson covariance, a massive-first relative-entropy coefficient at each discrete L, and endpoint control for passing that coefficient to the limit. It does not establish an upper asymptotic in every simultaneous scaling of μ and L. [Continuum calculation, Eqs. (74)–(75)](https://arxiv.org/pdf/0903.5284v3#page=11)

## Numerical checks

| L | $\kappa_L$ from (3) |
|---:|---:|
| 1 | 0.17036923302947074 |
| 2 | 0.16749385065157602 |
| 3 | 0.16710229283363605 |
| 4 | 0.16692069692297556 |
| 8 | 0.16673143926366616 |
| 16 | 0.16668292263709258 |

The checker constructs (3) in a scalar sine basis, then independently computes the Hessian from the original complex Wilson blocks at L=1, 2, 3, 4 and 6. A third calculation integrates the exact massive symbol and uses the nonlinear finite relative entropy at μ=10⁻⁸, 10⁻¹⁶ and 10⁻²⁴ for L=1,2,3. Convergence of the normalized nonlinear trace is slow because the relative correction is generally of order $1/\log(1/\mu)$. These evaluations use high-precision numerical arithmetic, without interval certification. No finite-L monotonicity or rate in L is used. [Reproducible checker](fixed.py)
