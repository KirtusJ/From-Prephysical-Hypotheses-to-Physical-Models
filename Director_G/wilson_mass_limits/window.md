# A finite-interval entropy estimate and a positive shrinking-mass window

Let $A=C_{L,m}$, $B=C_{L,0}$ be compressions of the infinite-chain Wilson occupied-band projectors in the original two-orbital convention, $0<\mu=mL\le1$, and $L\ge4$. Put $\ell_\mu=\log(e/\mu)$. There is an absolute constant $C$ such that

$$
 |S(A)-S(B)|\le C\mu\ell_\mu^3. \tag{1}
$$

Consequently the finite modular, nonlinear and two-bond estimates in D4/D5 give, for $L$ sufficiently large,

$$
 \left|D(A\Vert B)-{\mu^2\over6}\log L\right|
 \le C\left(\mu\ell_\mu^3 + \sqrt{\log(2L)/(2L)}\right). \tag{2}
$$

In particular the ratio tends to one on every sequence $\mu_L\downarrow0$ with

$$
 \frac{\mu_L\log L}{\log^3(e/\mu_L)}\longrightarrow\infty. \tag{3}
$$

This includes $\mu_L=(\log L)^{-a}$ for every $0<a<1$. The proof of (1) uses the finite projector and its explicit Fourier coefficients. The passage from (1) to (2) uses the Riccati and Jacobi estimates underlying D4 Corollary 4 and Theorem 6, which retain their exact-connection and spectral-domain hypotheses. Neither bound invokes the D8 continuum entropy convergence estimate (B9). The separate lower bound along $\mu_L=1/L$ remains compatible with (2). [D8, parts 1, 3 and 9](https://github.com/KirtusJ/From-Prephysical-Hypotheses-to-Physical-Models/blob/0ca75f60c76af1be7f3c25c2ed8914e82243ff5d/edition/PAPERS/D8_Wilson_Dirac_Covariance_Majorant_and_Boundary_Estimates/D8_Wilson_Dirac_Covariance_Majorant_and_Boundary_Estimates.pdf) · [D4](https://github.com/KirtusJ/From-Prephysical-Hypotheses-to-Physical-Models/blob/0ca75f60c76af1be7f3c25c2ed8914e82243ff5d/edition/PAPERS/D4_Uniform_Modular_Control_and_Nonlinear_Convergence_for_Wilson_Dirac_Int/D4_Uniform_Modular_Control_and_Nonlinear_Convergence_for_Wilson_Dirac_Int.pdf) · [D5](https://github.com/KirtusJ/From-Prephysical-Hypotheses-to-Physical-Models/blob/0ca75f60c76af1be7f3c25c2ed8914e82243ff5d/edition/PAPERS/D5_Conditional_Uniform_Additive_Limit_of_Wilson_Dirac_Relative_Entropy_on/D5_Conditional_Uniform_Additive_Limit_of_Wilson_Dirac_Relative_Entropy_on.pdf)

## The nonlinear entropy increment

Write $X_s=\chi P_s(1-\chi)$, $H_s=\left(\begin{smallmatrix}0&X_s\\X_s^*&0\end{smallmatrix}\right)$, and $D=H_m-H_0$. Each $H_s$ is self-adjoint with norm at most $1/2$; the same is true for $H_0+\theta D$. The relevant operators have a common finite-dimensional invariant subspace outside of which they vanish. With $h(p)=-p\log p-(1-p)\log(1-p)$ and $F(x)=h((1+\sqrt{1-4x^2})/2)$, the projection identity $X_sX_s^*=C_{L,s}(I-C_{L,s})$ gives

$$
 2[S(A)-S(B)]=\operatorname{Tr}[F'(H_0)D]
 +\int_0^1\operatorname{Tr}\{[F'(H_0+\theta D)-F'(H_0)]D\}\,d\theta . \tag{4}
$$

D8 part 9 Theorem 1, whose small-$\kappa$ estimates apply for $L\ge4$, gives $\|D\|_1=2\|X_m-X_0\|_1\le C\sqrt\mu$. Here $\kappa=\log(1+\mu/L)$.

For self-adjoint $U,V$ of norm at most $1/2$, $d=\|U-V\|\le1$, one has

$$
 \|F'(U)-F'(V)\|\le C d\log(e/d). \tag{5}
$$

Indeed differentiating the scalar formula for $F$ and integrating the elementary representation of $\operatorname{artanh}$ gives

$$
 F'(x)=4\int_0^1\frac{x}{1-u^2+4u^2x^2}\,du .
$$

On $u\le1/2$, both denominators are bounded below by $3/4$. The inverse difference identity and $\|U^2-V^2\|\le d$ bound the operator integrand difference by $Cd$. For $1/2<u<1$, let $a=(1-u^2)^{1/2}/(2u)$. The integrand is $u^{-2}$ times one half the sum of $(x-ia)^{-1}$ and $(x+ia)^{-1}$. The resolvent identity and the single-resolvent bound yield $C\min(a^{-1},d/a^2)$. Since $a$ is comparable to $\sqrt{1-u}$, splitting at $1-u=d^2$ proves (5); for $d\ge1/2$ the boundedness of $F'$ suffices. The integrals converge in operator norm, including at zero eigenvalues. Equation (5) with $\|D\|\le\|D\|_1$ bounds the second term in (4) by $C\mu\log(e/\mu)$ for small $\mu$. On a fixed subinterval away from zero (1) already follows from the $O(\sqrt\mu)$ estimate.

## Why the linear term is smaller than the nuclear-norm bound

At zero mass the Fourier kernel of $P_0$ between cells distance $r\ne0$ is bounded in orbital operator norm by $C/|r|$. One derivation uses the massless normalized Bloch components $\operatorname{sgn}(k)\cos(k/2)$ and $|\sin(k/2)|$ for $-\pi<k<\pi$. Both have bounded variation, and integration by parts in their Fourier coefficients proves the estimate.

On either exterior half-line, for $t>0$ let $v_t(j)=(1-e^{-2t})^{1/2}e^{-tj}$, $j\ge0$, tensored with a unit spinor. It is normalized. Number the $L$ interior cells starting at the adjacent boundary. When $a=Lt\le1$, each interior orbital vector satisfies

$$
 \|(X_0v_t)(i)\|
 \le C\sqrt{t}\sum_{j\ge0}\frac{e^{-tj}}{i+j+1}
 \le C\sqrt{t}\,[1+\log(1/(t(i+1)))],\quad 0\le i<L .
$$

Splitting at $j=1/t$ gives the last estimate by a harmonic sum and an exponentially weighted tail. Summing squares and using the decreasing-function bound
$\sum_{i=1}^L\log^2(L/i)\le\int_0^L\log^2(L/y)\,dy=2L$
gives

$$
 \|X_0v_t\|\le C\sqrt a\,[1+\log(1/a)]. \tag{6}
$$

Regard the exterior vector as $\xi=(0,v_t)$. Then $\|H_0\xi\|=\|X_0v_t\|$. The scalar integral for $F'$ also gives $|F'(x)|\le C |x|\log(e/|x|)$ on $[-1/2,1/2]$. The function $y\mapsto y\log^2(e/\sqrt y)$ is increasing and concave on $[0,1/4]$, with continuous value zero at the origin. Jensen in the spectral measure of $H_0^2$ at $\xi$ therefore implies

$$
 \|F'(H_0)\xi\|\le C\|H_0\xi\|\log(e/\|H_0\xi\|)
 \le C\sqrt a\,[1+\log(1/a)]^2,\quad 0<a\le1 . \tag{7}
$$

To obtain the last estimate, use (6) where its right-hand side is below $1/2$, and use $\|F'\|_\infty\le2$ on the remaining compact range. The same estimate applies to either boundary and every unit spinor. It controls $F'(H_0)$ on the exterior factor, where the rank-one Hankel formula supplies an available vector.

## Integrating the rank-one cross-block formula

In D8 part 9 equations (3)–(6) the two half-line blocks of $Z=X_m-X_0$ are integrals of the interior-to-exterior rank-one Laplace factors (and their $2\times2$ orbital factors). For each $t$ the spatial norm is

$$
 W_L(t)=e^{-t}\frac{\sqrt{1-e^{-2Lt}}}{1-e^{-2t}} .
$$

The orbital trace norms are bounded by $C M_\kappa(t)$, where $M_\kappa=|\rho_x|+|\rho_z|$ in that paper. For a rank-one matrix $|u\rangle\langle v_t|$, self-adjointness of $F'(H_0)$ bounds the absolute trace after multiplication by $F'(H_0)$ by $\|u\|\|F'(H_0)(0,v_t)\|$. Its adjoint gives the same estimate. Hence the linear term of (4) is bounded by the integral of $C M_\kappa W_L$ times the additional factor in (7) when $Lt\le1$; at $Lt>1$ use the constant bound 2.

For $0<\mu\le1/4$ we have $2\kappa\le1/L$, $L\kappa$ comparable to $\mu$, and $L\kappa\le\mu$. The following estimates contain constants independent of $L,\mu$.

* On $0<t<\kappa$, $M_\kappa\le C$. The product of $W_L\le C\sqrt{L/t}$ with (7) is at most $CL[1+\log(1/(Lt))]^2$. Integration contributes $O(\mu\ell_\mu^2)$.
* On $\kappa<t<2\kappa$ the same product bound holds. Here $M_\kappa(t)\le C[1+(t+\kappa)/\sqrt{t^2-\kappa^2}]$; it has integral $O(\kappa)$ over this interval. Its contribution is $O(\mu\ell_\mu^2)$.
* On $2\kappa<t\le1$ the D8 density estimate reduces to $M_\kappa(t)\le C\kappa/t$. From $2\kappa$ through $1/L$, (7) and the finite-length kernel bound thus give at most $CL\kappa\int_{2\kappa}^{1/L}[1+\log(1/(Lt))]^2\,dt/t=O(\mu\ell_\mu^3)$. From $1/L$ through 1, the exact formula above gives $W_L\le C/t$. Together with $\|F'\|_\infty\le2$ this contributes $O(\kappa L)$.
* At $t\ge1$, $W_L\le Ce^{-t}$ and $M_\kappa\le C\kappa e^{t/2}$, giving $O(\kappa)$.

These integrals bound the first term of (4) by $C\mu\ell_\mu^3$, proving (1). The remaining $1/4<\mu\le1$ regime follows by increasing the constant in the finite $O(\sqrt\mu)$ bound. No assumption that the entropy is monotone in the Wilson mass enters the proof.

## Combining the three other terms

The exact finite decomposition is $D=\mathcal P+\mathcal Q+\mathcal F-\Delta S$. For $N=2L$, $0\le\mu\le1$, D4 Corollary 4 and D5 pp.2–3 give $\mathcal F=O(\sqrt{\log N}/N)$ uniformly and $\mathcal Q=c_\eta\mu^2+O(\sqrt{\log N/N})$ uniformly by taking the common truncation $K=\lfloor\sqrt{N/\log N}\rfloor$ in D4 (8). D5 p.3's complementary-modulus expansion gives
$\mathcal P=(\mu^2/6)\log L+\mu^2[(1/6)\log(8/\mu)-1/4]+O(\log N/N)$
uniformly in that mass interval. The $\mu$-dependent explicit terms are $O(\mu\ell_\mu^3)$. Substituting (1) proves (2). Condition (3) forces $\mu\log L\to\infty$, so the power-small finite-length term in (2) divided by $\mu^2\log L$ also vanishes.

Bound (1) is a first-order estimate with logarithmic losses. It leaves open a quadratic rate such as $O(\mu^2\log^p(e/\mu))$, possible cancellation between the two orbital sectors in the linear trace, and the exact transition between relative-law and counterexample regimes.
