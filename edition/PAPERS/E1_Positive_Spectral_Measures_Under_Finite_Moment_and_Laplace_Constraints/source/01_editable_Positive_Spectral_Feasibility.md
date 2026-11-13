---
title: "Positive Spectral Measures Under Finite Moment and Laplace Constraints"
author: 'Kirtus Justus \textbullet{} Theoretical Physicist \textbullet{} 23 October 2026\tabularnewline Port Coquitlam, British Columbia, Canada'
date: ''
lang: en
header-includes:
 - \usepackage{microtype}
 - \usepackage{booktabs}
 - \usepackage{longtable}
---

**Abstract.** Finite positive Laplace and polynomial-moment observations constrain a spectrum but do not generally determine its lower support endpoint. We define the maximal compatible threshold as a well-posed extremal quantity and distinguish it from the actual threshold of an unknown measure. For an explicit six-observation benchmark, a positive three-atom representation and a global extended-Chebyshev Hermite dual yield an exact optimum. The same primal-dual method gives certified maxima for rectangular and correlated ellipsoidal observation uncertainty, and a high-precision numerical candidate for a local sign transition in the optimal observation correction; the latter presently lacks an enclosed crossing system in the accompanying verification materials. The strongest statements apply to the specified scalar moment problem, not to spectral gaps of an interacting quantum gauge theory.

**Keywords:** moment problems; Laplace transform; generalized quadrature; interval enclosures.

## 1. Mathematical objects, data and the target of optimization

The global-contact construction uses the theory of extended-Chebyshev systems and generalized Gaussian quadrature [1]. Interval enclosures of nonlinear equations follow standard validated-numerics principles [2].

Let $\mu$ be a positive Borel probability measure on $[0,\infty)$ with finite third moment. Define $M_j=\int E^j\,d\mu(E)$, $C(t)=\int e^{-tE}\,d\mu(E)$, and the actual support threshold $\Delta(\mu)=\inf\operatorname{supp}\mu$. For finite exact or uncertain observations $\mathcal Y$, define the *maximum compatible* threshold

$$ \Delta_{\max}(\mathcal Y)=\sup\{\Delta(\mu):\mu\ge0,\ \mu([0,\infty))=1,\ y(\mu)\in\mathcal Y\}. $$

**This extremum is an upper limit on what the data permit, not a lower bound on the unknown actual gap.** The benchmark observations are

$$ (M_0,M_1,M_2,M_3,C(\log2),C(2\log2))
=\left(1,\frac72,\frac{91}{6},\frac{147}{2},\frac{21}{128},\frac{455}{8192}\right). $$

The equal-weight six-atom measure $\frac16\sum_{j=1}^6\delta_j$ generates exactly these data and has actual threshold $1$. A different compatible three-atom measure has a strictly larger threshold. Thus even these *exact* observations do not identify the generating threshold.

## 2. Global Hermite dual certificate

Let $h=\log2$, and define the six-dimensional extended-Chebyshev space

$$\mathcal V=\operatorname{span}\{1,E,E^2,E^3,e^{-hE},e^{-2hE}\}. $$

For the ordered basis $(1,E,E^2,E^3,e^{-hE},e^{-2hE})$, the **six initial Wronskians** (using successive derivatives as rows) are

$$
\begin{aligned}
W_1&=1, & W_2&=1, & W_3&=2, & W_4&=12,\\
W_5&=12h^4e^{-hE}, & W_6&=-192h^9e^{-3hE}.
\end{aligned}
$$

For $h=\log 2>0$, each is everywhere nonzero. This verifies the standard sufficient extended-Chebyshev condition for the **ordered full flag**, not merely nonvanishing of the full six-function Wronskian. Consequently the zero-count bound of five real zeros counting multiplicity follows. For this particular space it also has a direct proof: the fourth derivative is $h^4e^{-2hE}(b_1e^{hE}+16b_2)$, which has at most one real zero unless it vanishes identically. Four applications of Rolle’s theorem give the five-zero bound; in the identically-zero case the original function is a polynomial of degree at most three. Consider

$$F(E)=E^3+c_2E^2+c_1E+c_0+b_1e^{-hE}+b_2e^{-2hE}.$$

Suppose a positive three-atom measure $\mu_*=\sum_{i=1}^3w_i\delta_{x_i}$ has $0<x_1<x_2<x_3$ and $F$ has a simple zero at $x_1$ and double zeros at $x_2,x_3$. These five contacts exhaust the allowed zeros. Since the leading behavior is $F(E)\sim E^3$ at infinity, the double roots do not reverse the sign and

$$\boxed{F(E)\ge0\quad\text{for }E\ge x_1.}$$

Let $\mathcal U\subset\mathbb R^5$ be a compact convex set of allowed observation offsets and let $y_0+\mathcal U$ be the feasible observation set. No full-dimensionality assumption is imposed; exact data correspond to $\mathcal U=\{0\}$. Put $\beta=(c_1,c_2,1,b_1,b_2)$ and $h_{\mathcal U}(\beta)=\sup_{\delta\in\mathcal U}\beta\cdot\delta$.

**Theorem 1 (robust primal-dual sufficiency).** Suppose the three-atom measure $\mu_*$ above is feasible, all three weights are positive, and the exposed face satisfies

$$\{\delta\in\mathcal U:\beta\cdot\delta=h_{\mathcal U}(\beta)\}=\{y(\mu_*)-y_0\}.$$

Then $x_1$ is the global maximum compatible threshold, the maximum is attained, and $\mu_*$ is its unique maximizing measure.

*Proof.* For any feasible $\mu$, the support-function inequality gives $\int F\,d\mu\le c_0+\beta\cdot y(\mu_*)=0$. If $\Delta(\mu)\ge x_1$, nonnegativity of $F$ gives the reverse inequality. Equality restricts $\mu$ to $F$'s three contact energies and places $y(\mu)-y_0$ in the exposed face. Its being a singleton gives $y(\mu)=y(\mu_*)$. Normalization and the moments $M_1,M_2$ fix the three weights by an invertible Vandermonde system, so $\mu=\mu_*$. Its positive mass at $x_1$ establishes attainment at $x_1$ and rules out any larger feasible threshold. $\square$

The singleton exposed-face hypothesis is used for both optimality and uniqueness. The statement is a sufficient proof method; it does not guarantee existence of an appropriate primal-dual pair for arbitrary observations.

**Counterexample without the singleton hypothesis.** Let $d=8h^2-23h+12$ and choose

$$\begin{aligned}
c_0&=-2(24h^2-128h+71)/d,&c_1&=2(44h^2-191h+108)/d,\\
c_2&=-3(16h^2-55h+30)/d,&b_1&=72(4h-3)/d,\\
b_2&=-64(10h-7)/d.&&
\end{aligned}$$

Here $h=\log2$ and $d<0$. Direct substitution gives $F(1)=F(2)=F(3)=F'(2)=F'(3)=0$. The zero count above shows that these are exactly one simple and two double roots, so $F\ge0$ on $[1,\infty)$ and $F(0)<0$. Put

$$\begin{aligned}
\mu_*&=(\delta_1+\delta_2+\delta_3)/3,&\nu&=\delta_2,\\
a=y(\mu_*)&=(2,14/3,12,7/24,7/64),&b=y(\nu)&=(2,4,8,1/4,1/16),\\
y_0&=y(\delta_0)=(0,0,0,1,1),&n&=\beta/\|\beta\|_2,\\
L&=-F(0)/\|\beta\|_2,&z_a&=a-y_0-Ln,\quad z_b=b-y_0-Ln.
\end{aligned}$$

Both $z_a,z_b$ are perpendicular to $n$. With $R_0=\max(1,\|z_a\|_2,\|z_b\|_2)$, the set

$$\mathcal U=\{tn+z:|t|\le L,\ z\perp n,\ \|z\|_2\le R_0\}$$

is compact, convex, centrally symmetric and has nonempty five-dimensional interior. Both $a-y_0$ and $b-y_0$ lie on its upper exposed face. Thus $\mu_*$ is feasible, has positive weights, satisfies $\int F\,d\mu_*=0$ and $\beta\cdot(a-y_0)=h_{\mathcal U}(\beta)$, yet the feasible $\nu$ has threshold $2>1$. The contact and support-function equalities alone therefore do not imply optimality. This counterexample does not affect the benchmarks below, whose exposed faces are singletons.

## 3. Three sharp benchmark results

For the six observations the validated primal solutions and global dual argument yield

| Uncertainty specification | Maximum compatible threshold | Attainment |
|---|---:|---|
| Exact $M_0,\dots,M_3,C_1,C_2$ | $1.1382749195388818\ldots$ | Unique positive three-atom extremizer |
| $M_0=1$, each of five other coordinates within $10^{-6}$ | $1.1386525473350218\ldots$ | Unique positive three-atom extremizer at the sign-compatible box corner |
| $M_0=1$, correlated ellipsoid below | $1.1384574514846816\ldots$ | Unique positive three-atom extremizer at an exposed ellipsoid point |

For the ellipsoid set $\mathcal U_R=\{\delta:\delta^TR^{-1}\delta\le\varepsilon^2\}$, $\varepsilon=10^{-6}$, and

$$R=\begin{pmatrix}1&0&0&0&0\\0&1&0&0&0\\0&0&1&0&0\\0&0&0&1&1/2\\0&0&0&1/2&1\end{pmatrix}.$$

Its support function and unique maximizer, for nonzero $\beta$, are

$$\boxed{h_{\mathcal U_R}(\beta)=\varepsilon\sqrt{\beta^TR\beta},\qquad
\delta_*(\beta)=\varepsilon\frac{R\beta}{\sqrt{\beta^TR\beta}}.}$$

**Primal-dual systems.** Each benchmark has its own exact-rational interval certificate. The exact and rectangular cases use eleven unknowns: three nodes, three weights and five dual coefficients. Their equations impose normalization, the five observations, and the five Hermite contacts. The rectangular correction is $\varepsilon(1,-1,1,1,-1)$; the verified signs $c_1>0,c_2<0,b_1>0,b_2<0$, together with $\beta_3=1$, make this its unique exposed corner. The ellipsoid adds a twelfth variable $s>0$, imposes $s^2=\beta^TR\beta$, and uses the correction $\varepsilon R\beta/s$. The norm equation is scaled by $10^{-6}$ for numerical conditioning without changing its zeros. Its positive-definite $R$ and nonzero $\beta$ give a singleton exposed face. Exact data use the singleton $\mathcal U=\{0\}$.

**Local interval inclusion.** Write the primal-dual residual vector as $\mathscr R$, to distinguish it from the scalar Hermite dual $F$. For each stored rational center $c$ and rational preconditioner $A$, let $X=c+[-r,r]^n$, where $r=10^{-90}$. Outward-rounded rational arithmetic and interval automatic differentiation give bounds

$$B\ge\|A\mathscr R(c)\|_\infty,\qquad q\ge\sup_{x\in X}\|I-A\mathscr R'(x)\|_\infty.$$

Conservative rounded upper bounds from the exact rational results are

| Benchmark | $B$ upper bound | $q$ upper bound |
|---|---:|---:|
| Exact | $2.60\times10^{-123}$ | $3.08\times10^{-75}$ |
| Rectangular | $4.38\times10^{-123}$ | $9.43\times10^{-76}$ |
| Correlated ellipsoid | $2.22\times10^{-123}$ | $1.70\times10^{-75}$ |

Each satisfies $B+qr<r$ and $q<1$. Therefore $T(x)=x-A\mathscr R(x)$ is a contraction mapping $X$ strictly into itself. Moreover $q<1$ implies that $A\mathscr R'(c)$, hence $A$, is nonsingular. Banach's fixed-point theorem consequently proves a unique root of the primal-dual system within $X$. It does not establish global uniqueness of all roots of those equations. Positive ordered nodes, positive weights, the dual signs, and $s>0$ in the ellipsoid case are verified throughout the corresponding boxes. The contact zero count and Theorem 1 then establish the separate global extremal conclusion.

**Arithmetic and precision.** The verifier represents interval endpoints as integers in units of $10^{-140}$ and rounds all rational operations outward. It encloses $\log2$ by 160 terms of its rational atanh series with an explicit geometric tail bound. For each exponential, it divides the argument by 16, uses the Taylor polynomial through degree 120 with remainder bounded by $3/121!$, and squares outward four times. Every reduced argument has absolute value at most one. Floating-point computation supplies candidate centers and preconditioners only; certificate decisions use exact integer and rational operations. Complete decimal centers, rational preconditioners, exact inclusion bounds and the replayable verifier accompany the computational materials. General validated-numerics principles are described in [2,3].

The exact rational endpoints of the correlated-ellipsoid first-node interval share the **80 fractional digits**
$$\Delta_{\max}(\mathcal U_R)=1.13845745148468164795870658112096059644751252685084364686503566728597685193350532\ldots.$$ 
The common prefix is checked by exact integer truncation; the printed ellipsis does not assert additional certified digits. These are computer-assisted enclosures under the documented arithmetic and implementation assumptions, not a formal proof-assistant development. The separate $\rho_c$ crossing does not inherit this enclosure.

**Interpretation.** A small floating-point residual alone does not establish an exact solution. Local inclusion, global support optimality and inference about an unknown generating measure are distinct questions. The certificates and Theorem 1 answer the first two for these specified scalar moment problems. They do not identify the generating threshold or establish a mass gap in an interacting quantum gauge theory.

## 4. A correlation-dependent observation transition

Extend the ellipsoid to $R(\rho)$ by replacing its off-diagonal Laplace entries $1/2$ by $\rho\in(-1,1)$. The $C_2$ component of the extremal observation correction is proportional to $b_2+\rho b_1$. **Numerical candidate (local transverse correction crossing; not interval-certified in the accompanying evidence).** A high-precision jointly solved primal-dual system suggests a crossing satisfying $b_2+\rho b_1=0$ near

$$\boxed{\rho_c=0.58802677404044760093599\ldots,\qquad
\Delta_{\max}(\rho_c)=1.13844553503596911790614\ldots .}$$

Here the correction to the *second Laplace datum* crosses zero with the three support weights remaining strictly positive. A sign change of a measured correction is not a root collision, phase transition, or support-topology change. The reported numerical residuals and apparent transversality motivate a local existence proof, but no outward-rounded inclusion for the augmented crossing equations accompanies these materials. Neither existence/uniqueness of the exact crossing nor global uniqueness on $(-1,1)$ is established here.

## 5. Conditioning, low-energy inference and limits

At the exact benchmark and with $M_0$ fixed, the sensitivity vector is approximately

$$\nabla_y\Delta_{\max}=(49.4940,-7.6434,0.4136,201.7217,-118.5863).$$

Its worst-case linearized box sensitivity is $\varepsilon\|\nabla\Delta\|_1$, whereas its ellipsoid sensitivity is $\varepsilon\sqrt{\nabla\Delta^TR\nabla\Delta}$. These are different deterministic uncertainty geometries; $R$ is **not automatically an experimentally measured covariance matrix**.

General positivity bounds can also constrain low-energy weight. If $M_0=C(0)$ and $\delta,t>0$, then

$$\max\left(0,\frac{C(t)-M_0e^{-t\delta}}{1-e^{-t\delta}}\right)
\le\mu([0,\delta])\le\min\big(M_0,e^{t\delta}C(t)\big).$$

These inequalities are often weak, but unlike the maximal compatible gap they bound a different object: the weight of an energy interval. When multiple moments and times are available, a finite-error primal-dual program can improve such bounds with separately justified calibration uncertainty.

## References

1. B. D. Bojanov, D. Braess, and N. Dyn, "Generalized Gaussian Quadrature Formulas," *Journal of Approximation Theory* **48** (1986), 335–353, doi:10.1016/0021-9045(86)90008-0.

2. A. Neumaier, *Interval Methods for Systems of Equations*, Cambridge University Press, 1990. (General reference for verified nonlinear enclosures.)

3. S. M. Rump, "Verification methods: Rigorous results using floating-point arithmetic," *Acta Numerica* **19** (2010), 287–449, doi:10.1017/S096249291000005X.

## Acknowledgments and AI-assisted research

Kirtus Justus provided research direction, the scientific questions, the supplied mathematical materials, and requirements for critical evaluation. ChatGPT (OpenAI) assisted with mathematical checking, manuscript preparation, and editorial examination. Additional AI systems used in the research program include Claude (Anthropic), Gemini (Google), Grok (SpaceXAI), and DeepSeek (High-Flyer). No particular proof, numerical calculation, or independent review is attributed to those systems without supporting records. AI systems are not listed as authors; responsibility for the submitted scholarly claims rests with the named author. The acknowledgment does not imply endorsement by any AI provider or independent peer review.
