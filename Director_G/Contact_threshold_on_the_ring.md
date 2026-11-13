# The contact phase at the two-particle band edge

**Kirtus Justus**, Theoretical Physicist

Port Coquitlam, British Columbia, Canada

Research supplement by Director G (OpenAI Codex).

On an even ring, the alternate contact sign $g=-1$ has threshold secular determinant exactly **one** in the zero-total-momentum sector of the rational staggered walk. Two other contact phases do place an eigenvalue at that threshold. Their limits can be calculated explicitly. A separate perturbation estimate on the line gives a sufficient scaling for small contact phases to preserve the determinant walk's continuum limit. [Occupation walk, gates and continuum conventions](Interacting_occupation_walk.md)

## Two contact channels

Take $N\ge2$ even two-mode cells. Periodic two-particle occupations use the antiperiodic one-particle momenta $k=(2j+1)\pi/N$. Write $x=e^{ik}$ and set

$$
 S=\frac15\begin{pmatrix}3&-4i\\-4i&3\end{pmatrix},\qquad
 U(x)=\frac15\begin{pmatrix}4&3i/x\\3ix&4\end{pmatrix}S,\qquad
 z_*=\left(\frac{24-7i}{25}\right)^2 .
$$

In the total-momentum-zero fiber use one representative $0<k<\pi$ per pair $k,-k$, with the two sublattice labels in that order. Each such block of the free two-particle cycle $U_0$ is $\mathcal A(x)=U(x)\otimes U(x^{-1})$. The same-cell contact vector $v$ is normalized over all translates. Pull the normalized intercell contact vector back through the first, intracell layer and call it $w$. It only has support on pairs in different cells, so $v,w$ are orthonormal. With $V=(v,w)$ the exact cycle on this fiber is

$$ U_g=U_0\bigl[I+(g-1)VV^\dagger\bigr]. $$

Indeed the phase on each contact commutes with the corresponding free bond gate, and the two pulled-back contact projectors have zero product. The free block eigenvalues are $1,1,e^{2i\omega(k)},e^{-2i\omega(k)}$, where $\cos\omega(k)=12(1+\cos k)/25$ and $\gamma=\omega(0)$. Since $\gamma<\omega(k)\le\pi/2$ on the allowed momenta, $z_*=e^{-2i\gamma}$ is outside the finite free spectrum. Factoring $z_*I-U_0$ and taking the determinant gives the scalar condition

$$
 d_N(g)=\det[I-(g-1)G_N]=0,\qquad
 G_N=V^\dagger(z_*I-U_0)^{-1}U_0V .
$$

## Removing the apparent singularity

The contact bras on a $k,-k$ block, apart from their common factor $1/\sqrt N$, are the rows of

$$
 C(x)=\begin{pmatrix}
 (0,1,-1,0)\\
 (0,-x,x^{-1},0)(S\otimes S)
 \end{pmatrix}.
$$

The first row takes the determinant of the two sublattice amplitudes. The second uses the intracell gate on each particle and translates one endpoint by a cell. With $b=\cos k$, multiplication of these four-dimensional matrices gives

$$
 C(z_*I-\mathcal A)^{-1}\mathcal A C^\dagger
 =\frac1{3+b}
 \begin{pmatrix}
 -(3+b)+i(69-27b)/14 & (b-1)(1-24i/7)\\
 2b^2+5b+1+24i(1-b)/7 & -(3+b)+i(16-128b)/21
 \end{pmatrix}.
$$

This rational identity can be checked before evaluating any roots of unity by substituting $b=(x+x^{-1})/2$ and using $\overline x=x^{-1}$. In particular the matrix in contact coordinates extends smoothly to $b=1$. The unrestricted resolvent at the infinite-volume band edge does not have this property.

$G_N$ is $1/N$ times the sum of these matrices on the $N/2$ positive momenta. Set

$$
 H_N=\frac1N\sum_{k}\frac1{3+\cos k},\qquad
 t_N=1-4H_N,\qquad
 A_N=\frac34-\frac{75}{28}t_N,\quad B_N=-\frac43-\frac{100}{21}t_N .
$$

The sum in $H_N$ uses all $N$ momenta. The full-ring mean of $\cos k$ is zero. Dividing the entries above by $3+b$ and using symmetry between $k$ and $-k$ gives

$$
 I+2G_N=
 \begin{pmatrix}
 iA_N & t_N(1-24i/7)\\
 -t_N(1+24i/7) & iB_N
 \end{pmatrix}.
$$

Here $A_N B_N=-1+625t_N^2/49$ while $|1-24i/7|^2=625/49$. Thus $\det(I+2G_N)=1$ for every even $N$. Put $L_N=A_N+B_N$. For general $|g|=1$, writing $g=e^{i\theta}$ and using $I-(g-1)G_N=[(1+g)I+(1-g)(I+2G_N)]/2$ gives

$$ d_N(e^{i\theta})=e^{i\theta}\bigl[\cos\theta+(L_N/2)\sin\theta\bigr]. $$

At $g=-1$ this equals one. The two tuned roots differ in phase by $\pi$. To evaluate them, the Chebyshev polynomial $T_N(b)+1$ has precisely the full-ring cosine list as its roots, counted with multiplicity. Its logarithmic derivative at $b=-3$ gives $H_N=U_{N-1}(3)/(T_N(3)+1)$, where $U_{N-1}$ is the Chebyshev polynomial of the second kind. Equivalently, with $\rho=-3+\sqrt8$,

$$ H_N=\frac{1-\rho^N}{\sqrt8\,(1+\rho^N)}. $$

The limiting value is $1/\sqrt8$. The limiting tuned angles in $(-\pi,\pi]$ are approximately $-0.6750117040$ and $2.4665809496$. The finite eight-cell real-space matrices gave an eigenvalue within $2.1\times10^{-15}$ of $z_*$ at each of their two tuned phases. This comparison checks the phase convention independently of the contact-coordinate formula. Root exclusion at this single total momentum and energy leaves the scattering limit of the fixed negative sign open. In particular it gives no uniform near-edge resolvent estimate or classification of bound and resonant states on the line. [Direct occupation and spectral checks](results/contact_continuum.json)

## Weak contact phases on the line

Work instead in the fixed-gap positive band of both particles. On a momentum cutoff $|k|,|l|\le K$ sufficiently close to zero take a smooth normalized Bloch spinor $u(k)$. The even-bond contact form is the determinant of $u(k)$ and $u(l)$. The odd-bond form uses $Su(k),Su(l)$ and endpoint factors $e^{ik}$ or $e^{il}$. Both vanish at $k=l$ and are bounded by $C|k-l|$. For fixed total momentum, a relative momentum ranges over an interval of length at most $2K$ when parametrized by $k$. Applying Cauchy–Schwarz to the contact amplitude in that integral and then Parseval in the total momentum gives

$$ \|P_{\rm bond}\psi_{\rm free}\|\le C K^{3/2}\|\psi_{\rm free}\|. $$

This estimate also applies immediately after the first bond layer by using its rotated spinor. The free band phases at any cycle preserve the momentum support and norm. In a chronological difference of the two $n$-cycle propagators, every one-layer defect has norm $|g-1|$ times the incoming free contact norm, with a unitary factor on either side. Take $K=aP/\varepsilon$, $\tau=m\kappa a^2/\varepsilon$ and $n\tau\le T$. The resulting state error is bounded by

$$ C_{T,m,\kappa}|g-1|\,\frac{P^{3/2}}{\sqrt{a\varepsilon}}. $$

Consequently $|g-1|P^{3/2}=o(\sqrt{a\varepsilon})$ suffices to preserve the free-band limit whenever the original determinant walk's continuum approximation holds. Momentum tails can first be cut in norm using unitarity. For fixed physical momenta this gives a sufficient condition for phases approaching the determinant value. It does not settle fixed $g=-1$. In a unit-circumference ring the two opposite antiperiodic plane waves $k=\pm\pi/N$ have contact norm of order $N^{-3/2}$ at either layer. The sum of their free contact norms across order $N^2$ cycles grows as $\sqrt N$. This concerns the triangle estimate; cancellation between different times remains possible in the actual evolution. [Finite packet tests and adverse controls](check_contact_continuum.py)
