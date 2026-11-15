# How much one orbital can distinguish at any interval length

For every integer $L\ge1$ and $0<\mu\le1$, a measurement of one orbital on the Wilson interval gives the explicit bound

$$
D_L(\mu)\ge \frac{\mu^2\log^2(1/\mu)}{200\pi^2}.
$$

A second estimate holds as the mass tends to zero, with the infimum taken over **all** lengths, including one cell:

$$
\liminf_{\mu\downarrow0}\ \inf_{L\ge1}
\frac{D_L(\mu)}{\mu^2\log^2(1/\mu)}\ge\frac{1}{\pi^2}.
$$

The first statement gives a positive numerical floor at each $0<\mu<1$. The second uses the opposite shifts of two orthogonal spin orbitals and uniform control of the error in their occupation probabilities. The joint lower coefficient $1/6$ in the companion note requires $L\to\infty$. [Joint estimate](upper.md) · [Issued symbol and entropy convention, D1 p. 4](https://github.com/KirtusJ/From-Prephysical-Hypotheses-to-Physical-Models/blob/0ca75f60c76af1be7f3c25c2ed8914e82243ff5d/edition/PAPERS/D1_Relative_Entropy_of_Finite_Interval_Wilson_Dirac_Quasifree_States/D1_Relative_Entropy_of_Finite_Interval_Wilson_Dirac_Quasifree_States.pdf#page=4)

## The occupation shift

Let $m=\mu/L$, $u=L^{-1/2}(1,\ldots,1)$, and $\phi=u\otimes|z+\rangle$ in the original cell basis. Its occupation under the massless reference exceeds its massive occupation by

$$
d=\frac1{2\pi}\int_0^\pi F_L(k)\,[Z_m(k)-Z_0(k)]\,dk,\qquad
F_L(k)=\frac{\sin^2(Lk/2)}{L\sin^2(k/2)},\qquad
Z_s(k)=\frac{s+1-\cos k}{E_s(k)}.
$$

Here $E_s^2=s^2+4(1+s)\sin^2(k/2)$. The formula follows by inserting $\phi$ into the compressed occupied-band projector. The factor $1/2$ in that projector and reflection onto positive momenta give the prefactor shown. Since $\partial_sZ_s=\sin^2 k/E_s^3\ge0$, every momentum contributes with the same sign.

For $m\le k\le1/L$, $0\le s\le m$, one has $E_s^2\le3k^2$, $\sin k\ge5k/6$, and $F_L\ge(23/24)^2 L$. The last inequality follows from $\sin x\ge x(1-x^2/6)$ at $x=Lk/2\le1/2$. Integrating the derivative just on this interval yields

$$
d\ge\frac{25(23/24)^2}{216\pi\sqrt3}\,\mu\log(1/\mu)
 \ge\frac{\mu\log(1/\mu)}{20\pi}.
$$

The binary occupation measurement obeys data processing. Its Bernoulli relative entropy is at least $2d^2$ by Pinsker’s inequality with natural logarithms. This proves the explicit finite-length bound, with the endpoint $\mu=1$ following from nonnegativity.

## The error is uniform in the length

Uniformly for all $L\ge1$ and $0<\mu<1$,

$$
d=\frac{\mu}{2\pi}\,[\log(1/\mu)+O(1)].
$$

To see the uniformity directly, split the integral at $m$ and $1/L$. Below $m$, $0\le Z_m-Z_0\le1$ and $F_L\le L$, giving $O(\mu)$. Above $1/L$, $F_L\le[L\sin^2(k/2)]^{-1}$ and $\partial_s Z_s\le[2\sin(k/2)]^{-1}$. This gives $O((m/L)\int_{1/L}^\pi k^{-3}dk)=O(\mu)$.

In the middle, $F_L/L=1+O((Lk)^2)$ by the sinc expansion. For $0\le s\le m\le k\le1/L$ the exact derivative satisfies

$$
 k\partial_s Z_s
 =\frac{k\cos^2(k/2)}{2\sin(k/2)}
 \left(1+s+\frac{s^2}{4\sin^2(k/2)}\right)^{-3/2}
 =1+O\!\left(k^2+m+(m/k)^2\right).
$$

All constants are absolute. Each of $(Lk)^2$, $k^2$, $m$ and $(m/k)^2$ integrates against $dk/k$ to a bounded value on $[m,1/L]$. In particular $m\log(1/\mu)\le1/e$. The leading integral contributes $\mu\log(1/\mu)/(2\pi)$, and the errors contribute $O(\mu)$.

For $u\otimes|z-\rangle$ the shift is $-d$. In an orthonormal basis containing both orbitals, the squared Hilbert–Schmidt norm of the covariance difference is at least $2d^2$. The finite matrix inequality $D(A\Vert B)\ge 2\|A-B\|_{\mathrm{HS}}^2$ then gives $D_L\ge4d^2$. Substitution of the uniform estimate proves the claimed all-length liminf. This argument uses orthogonality of the test directions and requires no joint measurement or independence assumption. [D8 part 7, Prop. 5, Eq. (7), p. 32](https://github.com/KirtusJ/From-Prephysical-Hypotheses-to-Physical-Models/blob/0ca75f60c76af1be7f3c25c2ed8914e82243ff5d/edition/PAPERS/D8_Wilson_Dirac_Covariance_Majorant_and_Boundary_Estimates/D8_Wilson_Dirac_Covariance_Majorant_and_Boundary_Estimates.pdf#page=32)

The standard-library check verifies the rational comparisons for the explicit coefficient. Its optional SciPy calculation integrates the full shift, the restricted positive band, and the individual Toeplitz diagonals. For instance, at $L=32$, $\mu=1/1024$, the full integral and the Toeplitz reconstruction both give $d=0.00132823829353$. [Checker](orbital.py) · [Output](orbital.txt)
