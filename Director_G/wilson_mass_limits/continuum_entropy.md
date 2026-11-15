# Small Dirac mass in the continuum and the Wilson entropy window

Casini and Huerta obtain the correct sign, spin multiplicity and candidate small-mass scale for the interval entropy. The operator limit in D8 uses the same spatial continuum Dirac projector, up to a fixed spinor change of basis and possibly occupation complementation. Identification of its regularized entropy difference with the D8 cross-boundary trace path requires control of the regulator and the small-mass remainder. The condition $\mu\log L\to\infty$ is sufficient **if** that estimate for the D8 path can be established. The directly proved finite-lattice window $\mu\log L/\log^3(e/\mu)\to\infty$ keeps its independent derivation. [Casini–Huerta, §4.2, pp. 10–12](https://arxiv.org/pdf/0903.5284v3) · [D8, part 1, model, finite trace path and (B9)](https://github.com/KirtusJ/From-Prephysical-Hypotheses-to-Physical-Models/blob/0ca75f60c76af1be7f3c25c2ed8914e82243ff5d/edition/PAPERS/D8_Wilson_Dirac_Covariance_Majorant_and_Boundary_Estimates/D8_Wilson_Dirac_Covariance_Majorant_and_Boundary_Estimates.pdf) · [Finite-lattice proof](window.md)

## The actual external coefficients

The paper treats a two-component complex Dirac fermion, with vacuum correlation operator restricted to one or more intervals. Its first-order perturbation has vanishing spinor trace. In equation (75) the second-order double logarithm in the entropy itself is negative. For an interval of unit physical length and dimensionless mass $\mu$, the calculated terms are

$$
 \delta S_{\rm CH}=
 -\tfrac16\mu^2\log^2\mu+
 \left(\frac{\log2-\gamma_E}{3}+\frac5{18}\right)\mu^2\log\mu+\cdots.
$$

For several intervals the double-log coefficient contains the square of their total length. Equation (83) is only one contribution to the single-log coefficient. For unit length, (77) supplies $(\log2-\gamma_E)/3$, (79) supplies $-1/6$, and (83) supplies $4/9$. For general length (83) also contains $-\tfrac13 m^2 L^2\log L\log m$. The unit-interval convention avoids mixing dimensionful mass and length logarithms. These terms concern the massive-minus-massless entropy. In the Wilson massive-first relative entropy it enters with a **minus** sign. [Casini–Huerta, equations (65)–(83), PDF pp.10–12](https://arxiv.org/pdf/0903.5284v3#page=10)

Equation (68) expands the resolvent perturbatively. Equations (69)–(83) calculate coefficients. To transfer this computation to D8 one still needs an estimate of the discarded terms, uniform up to the singular $\beta=1/2$ entropy-integral endpoint, that applies directly to D8's trace-path definition. The authors also report agreement of the single-interval coefficients with a Painlevé calculation. The original Casini–Fosco–Huerta study also defines the universal quantity $c(r)=r\,dS/dr$; recovering an entropy difference from such a derivative requires its integration normalization. Neither agreement nor matching a Dirac spinor fixes an arbitrary mass-dependent subtraction. [Casini–Huerta, below equation (83)](https://arxiv.org/pdf/0903.5284v3#page=12) · [Casini–Fosco–Huerta, equation (3)](https://arxiv.org/pdf/cond-mat/0505563v2#page=2)

## What would identify the two entropy differences

Conventions for gamma matrices and particle versus hole occupations do not obstruct the comparison. The continuum Hamiltonian $u\sigma_x+\mu\sigma_z$ represents the same two anticommuting Dirac matrices; the complement leaves the entropy unchanged because $h(p)=h(1-p)$. The ultraviolet comparison is a separate question. Casini–Huerta explicitly posit a regulator, mentioning a lattice as an example, and their massless integral needs endpoint regularization. D8 instead fixes the two-orbital infinite-chain Wilson projectors, the local cell embedding and a finite normalized limit

$$
 {\cal S}_{D8}(\mu)=\tfrac12\int_0^1
 \operatorname{Tr}\!\left[F'(H_0+\theta D_\mu)D_\mu\right]d\theta,
 \qquad D_\mu=H_\mu-H_0 .
$$

Here $D_\mu$ is trace class, even though the separate continuum entropy traces need not be finite. [Casini–Huerta, introductory regulator convention, PDF p.1](https://arxiv.org/pdf/0903.5284v3#page=1) · [D8, PDF pp.8–10, cross-block trace path and (B9)](https://github.com/KirtusJ/From-Prephysical-Hypotheses-to-Physical-Models/blob/0ca75f60c76af1be7f3c25c2ed8914e82243ff5d/edition/PAPERS/D8_Wilson_Dirac_Covariance_Majorant_and_Boundary_Estimates/D8_Wilson_Dirac_Covariance_Majorant_and_Boundary_Estimates.pdf)

A sufficient bridge can be stated rigorously. On a common embedded Hilbert space, let a second regulator have finite compressed projector pairs and cross-block operators $H_{0,n},H_{\mu,n}$. Assume $H_{0,n}\to H_0$ strongly and $D_n=H_{\mu,n}-H_{0,n}\to D_\mu$ in trace norm at fixed $\mu$. The self-adjoint cross blocks are uniformly bounded by $1/2$; $F'$ is bounded continuous there. Functional calculus gives strong convergence of $F'(H_{0,n}+\theta D_n)$ to $F'(H_0+\theta D_\mu)$. Subtract the $D_n-D_\mu$ contribution, then approximate $D_\mu$ by finite-rank operators to pass the trace with strong convergence. Uniform integrable domination follows from the trace-norm bound. The second regulator therefore gives exactly ${\cal S}_{D8}(\mu)$ after its common massive/massless removal. To import the external expansion, one still needs to identify its regularized computation with such a scheme, or evaluate the D8 relative trace directly, and justify the small-mass order for that quantity.

Matching low-energy dispersion or strong operator convergence alone cannot justify this step. Even in a sequence of finite-dimensional problems, placing an additional pure occupied orbital $\cos\theta\,|{\rm in}\rangle+\sin\theta\,|{\rm out}\rangle$ at a newly added orthogonal cutoff channel adds $h(\cos^2\theta)$ to the interval entropy. As that channel moves to successively higher basis index, the extra projector vanishes strongly while its finite entropy correction persists. Let the reference extra orbital be wholly interior and the massive angle depend on $\mu$. This construction illustrates a possible regulator obstruction, rather than a claimed feature of either actual model. Trace-norm convergence of the cross-block differences excludes it.

## Precise implication for the moving window

Assume the D5 finite estimates, uniform (B9) and, separately, $|{\cal S}_{D8}(\mu)|\le C\mu^2\log^2(e/\mu)$ for small $\mu$. D5 gives

$$
 \frac{|D_L(\mu)-\mu^2\log L/6|}{\mu^2\log L}
 \le C\left[
 \frac{\log^2(e/\mu)}{\log L}
 +\frac{1}{(\mu\log L)^2}\right].
$$

When $\mu\log L\to\infty$, eventually $\mu\ge1/\log L$ and the first term is $O((1+\log\log L)^2/\log L)=o(1)$. The second likewise vanishes. The exact coefficient of the continuum expansion is unnecessary for this implication. At $\mu=c/\log L$ the uniform error allowed by (B9), divided by the proposed leading term, is order one; tighter mass-dependent control would be required to go to that boundary by this argument.

In the direct finite proof, the exterior kernel estimate uses the massless jump, the Jensen function $y\log^2(e/\sqrt y)$ is concave through $y=0$, and the resolvent estimate for the trace-path remainder stays integrable at $u=1$ after splitting at $1-u=d^2$. The inner density integral pays three powers of $\log(e/\mu)$. Dropping those factors by substituting the external continuum coefficient would add the identification and remainder assumptions above.
