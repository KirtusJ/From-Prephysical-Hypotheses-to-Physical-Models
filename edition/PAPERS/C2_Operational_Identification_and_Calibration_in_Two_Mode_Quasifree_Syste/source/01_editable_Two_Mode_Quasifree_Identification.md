---
title: "Operational Identification and Calibration in Two-Mode Quasifree Systems"
author: 'Kirtus Justus \textbullet{} Theoretical Physicist \textbullet{} 23 October 2026\tabularnewline Port Coquitlam, British Columbia, Canada'
date: ''
lang: en
header-includes:
 - \usepackage{microtype}
 - \usepackage{booktabs}
 - \usepackage{longtable}
---

**Abstract.** We separate three logically different problems: determining a finite-mode state from measured observables, determining parameters in an explicitly selected thermal model, and deciding whether that model adequately describes observations. A two-mode gauge-invariant state admits an exact quasifree unhalved trace-norm witness and sharp occupation-only feasibility bounds. Restricted complete joint-number histograms identify Wilson–Dirac thermal parameters under a shared in-plane detector tilt, whereas unrestricted detector orientations admit aliases. Four momentum settings identify a first-harmonic spectrum from orbital-axis-invariant total-number data but suffer two singular differential strata. One calibrated interior orbital statistic restores first-order rank. Statistical guarantees are conditional on calibration and independent preparation, not consequences of exact algebra alone.

**Keywords:** CAR algebra; quasifree states; identifiability; calibration; quantum statistics.

## 1. Observation objects and the exact two-mode witness

We use the standard gauge-invariant CAR conventions [1]. Simultaneous sample bounds below employ Hoeffding’s concentration inequality [2].

Fix two fermionic modes $a_1,a_2$ and a gauge-invariant state $\rho$ commuting with the total-number operator. Let $q_{ab}$, $a,b\in\{0,1\}$, be the joint-number probabilities, and let $C_{ij}=\langle a_i^\dagger a_j\rangle_\rho$ be its one-particle covariance. The state has a one-dimensional vacuum block, a positive $2\times2$ one-particle block, and a one-dimensional double-occupation block. No quasifree assumption has yet been made. This article uses the occupation-index convention $C_{ij}=\langle a_i^\dagger a_j\rangle$. The operator-index convention $C^{\mathrm{op}}_{ij}=\langle a_j^\dagger a_i\rangle$ used in *Restricted Observables and CAR-State Distinguishability* satisfies $C^{\mathrm{op}}=C^{\mathsf T}=\overline C$; spectra, determinants, and $|C_{12}|^2$ are unchanged.

For the present model, $\|X\|_1=\operatorname{Tr}|X|$ denotes the **unhalved Schatten trace norm**. The conventional operational trace distance is $T(\rho,\sigma)=\frac12\|\rho-\sigma\|_1$; numerical formulae below use the unhalved convention unless $T$ is written explicitly.

Let $\omega_C$ be the *gauge-invariant quasifree* state with the same covariance. Define

$$ W=q_{10}q_{01}-q_{00}q_{11}-|C_{12}|^2. $$

**Theorem 1 (two-mode quasifree distance identity).** Exactly for the stated two-mode gauge-invariant class,

$$\boxed{\|\rho-\omega_C\|_1=4|W|,\qquad W=0\Longleftrightarrow \rho=\omega_C.}$$

*Proof.* Set $x=C_{11}$ and $y=C_{22}$. The number probabilities determine $x=q_{10}+q_{11}$, $y=q_{01}+q_{11}$. The quasifree Wick formula sets $q^{G}_{11}=xy-|C_{12}|^2$, giving $W=q^G_{11}-q_{11}$. The two states have the same one-particle coherence (up to the fixed CAR basis convention), so their difference has four diagonal entries $W,-W,-W,W$ in occupation-number sectors. The eigenvalues of this difference are those four numbers, hence the trace norm equals $4|W|$, while $T(\rho,\omega_C)=2|W|$. $\square$

An experiment that records the joint histogram **alone** has no direct access to $|C_{12}|^2$ for arbitrary states: measuring covariance quadratures in a consistently calibrated orbital basis is a separate requirement. In particular, dephasing a genuinely coherent Gibbs state in the counting basis can preserve its number histogram while changing $C_{12}$. The witness must not be called a certification of a particular Gibbs Hamiltonian; it certifies quasifreeness only in the specified state class.

For probability vectors $p,q\in\mathbb R^4$ on the simplex, let $F(q)=q_{10}q_{01}-q_{00}q_{11}$. The derivative has $\ell^1$ norm $\sum_i|\partial_iF|=1$, yielding

$$\boxed{|F(p)-F(q)|\le\|p-q\|_\infty.}$$

This sharpens the histogram contribution to a simultaneous finite-shot witness certificate. Readout bias, the two coherence quadratures and systematic basis drift must be bounded separately. An empty model-relative confidence set is a valid conditional rejection; a nonempty one is not proof that the physical state belongs to the chosen family.

## 2. Explicit thermal family and complete histogram reconstruction

Let $a=m+1\ge1$, $\lambda>0$, $|\epsilon|<1$, $\eta\in\mathbb R$ and

$$ E_a(k)=\sqrt{\sin^2k+(a-\cos k)^2},\qquad D(k)=\lambda(1+\epsilon\cos k)E_a(k). $$

For one common, unknown **signed in-plane detector tilt** $\theta\in(-\pi/2,\pi/2)$, set $r_\theta(k)=\{(a-\cos k)\cos\theta+\sin k\sin\theta\}/E_a(k)$. The full joint-number histogram, ordered $(00,10,01,11)$, is

$$q(k)=Z^{-1}(1,e^\eta[\cosh D-r_\theta\sinh D],e^\eta[\cosh D+r_\theta\sinh D],e^{2\eta}),$$
$$ Z=1+2e^\eta\cosh D+e^{2\eta}. $$

For strict positive observations the algebraic inverse is

$$ \eta=\tfrac12\log(q_{11}/q_{00}),\quad
 D=\operatorname{arcosh}\frac{q_{10}+q_{01}}{2\sqrt{q_{00}q_{11}}},\quad
 r_\theta=\frac{q_{01}-q_{10}}{2\sqrt{q_{00}q_{11}}\sinh D}. $$

**Theorem 2 (three-momentum identification, conditional).** For any $k_*\in(\pi/2,\pi)$, complete histograms at $(\pi/2,k_*,\pi)$ identify $(m,\lambda,\epsilon,\eta,\theta)$ uniquely *within the above shared-in-plane-tilt model*. They have a full-column-rank parameter Jacobian for every finite admissible tuple.

*Proof.* Write $k_1=\pi/2$, $k_2=k_*$ and
$\phi_a(k)=\arctan[\sin k/(a-\cos k)]$. Then
$r_\theta(k)=\cos(\phi_a(k)-\theta)$ at the two interior nodes.
The angles lie in $(0,\pi/4]$, decrease strictly with $a$, and decrease
strictly with $k$ on the stated interval. The observation at $\pi$ gives
$\cos\theta$, so a possible alias has $\theta'=\theta$ or
$\theta'=-\theta$.

Suppose first that $\theta'=\theta$. If $a'\ne a$, strict monotonicity
in $a$ rules out equal interior angles. Equality of their cosines must
therefore use the reflected branch at both nodes:
$\phi_a(k_i)+\phi_{a'}(k_i)=2\theta$ for $i=1,2$.
The left side decreases strictly from $k_1$ to $k_2$, a contradiction.
Thus $a'=a$ in this case.

If $\theta'=-\theta$, the reflected cosine branch would require
$\phi_a(k_i)+\phi_{a'}(k_i)=0$, which is impossible. The remaining
branch requires $\phi_a(k_i)-\phi_{a'}(k_i)=2\theta$ at both nodes.
For $a\ne a'$, its tangent is
$$(a'-a)\sin k/[aa'+1-(a+a')\cos k],$$
whose absolute value is strictly smaller at $k_2$ than at $k_1$.
This again is impossible. If $a=a'$, the equation forces $\theta=0$.
The angle ranges exclude extra $2\pi$ branches. Hence $a,\theta$ are
unique. Two splittings at distinct cosine nodes determine
$(\lambda,\lambda\epsilon)$ by an invertible linear system, and the
vacuum/double-occupation ratio determines $\eta$.

For first-order rank, put
$p_i=\partial_a\phi_a(k_i)=-\sin k_i/E_a(k_i)^2$ and
$s_i=\sin(\phi_a(k_i)-\theta)$. The rows of the directional
Jacobian in $(a,\theta)$ are $(-s_i p_i,s_i)$ and
$(0,-\sin\theta)$ at $\pi$. If $\theta\ne0$, at most one $s_i$
vanishes, since the two interior angles differ. The row at $\pi$ and a
nonzero interior row therefore have nonzero determinant. At $\theta=0$,
the determinant from the two interior rows is
$$\sin\phi_a(k_1)\sin\phi_a(k_2)(p_2-p_1)>0,$$
because $p_2>p_1=-1/(a^2+1)$. The splitting map has full rank in
$(\lambda,\epsilon)$ since $\lambda>0$ and the cosine nodes differ;
$\eta$ supplies the remaining independent coordinate. The histogram
inversion is smooth at these nodes because all probabilities and
splittings are strictly positive. This proves full column rank. $\square$

## 3. Four total-number momenta: exact identification versus conditioning

The total-number categories eliminate the orbital direction:

$$ (p_0,p_1,p_2)=Z^{-1}(1,2e^\eta\cosh D,e^{2\eta}). $$

Hence four distinct, known cosine nodes determine four samples of $Q(c)=D(c)^2$, a cubic for the first-harmonic family. In the branch $a=m+1\ge1$, its exact polynomial determines the Wilson mass and thermal parameters under the positivity assumptions. The four-node observation map is globally injective in this specified family.

It is not everywhere a *regular* inverse. Put

$$r=\frac12(a+a^{-1}),\quad L=\lambda\sqrt a,\quad
 Q(c)=2L^2(1+\epsilon c)^2(r-c).$$

Two separate differential singularities occur: $a=1$ (the derivative $dr/da$ vanishes), and the positive-mass root collision $1+\epsilon r=0$ (the cubic-coefficient Jacobian drops rank). At either, there exist admissible paths with mass separation of order $h$ but total-number probability separation of order $h^2$, yielding $D_{\mathrm{KL}}=O(h^4)$ for fixed finite designs. Thus $N^{-1/4}$ lower-bound behavior is possible for total-number-only mass estimation near these strata; it is not the same claim as globally nonunique parameters.

**Theorem 3 (calibrated directional rank recovery).** One additional orbital-direction observable in the *known Hamiltonian basis* at an interior $k$ has

$$s(a,k)=\frac{a-\cos k}{E_a(k)},\qquad\boxed{\partial_a s(a,k)=\frac{\sin^2k}{E_a(k)^3}>0.}$$

This is nonzero in the mass directions responsible for both singularities, restoring full-column first-order rank for the augmented ideal observation map. It may be measured at an existing momentum. The assumption of independently calibrated and stable orbital axes is essential; this is not a claim that such calibration is experimentally available.

**Explicit Jacobian minors.** Set $Q(c)=\lambda^2(1+\epsilon c)^2(a^2+1-2ac)$ and write its coefficients as $Q_0,\ldots,Q_3$. The four $3\times3$ minors of $\partial(Q_0,Q_1,Q_2,Q_3)/\partial(a,\lambda,\epsilon)$, in lexicographically ordered row triples, are exactly
$$8\lambda^5(a^2-1)[\epsilon(a^2+1)+2a]\,(1,\epsilon,\epsilon^2,\epsilon^3).$$
Both singular strata follow. Independently, $\det\partial(Q_0,Q_1)/\partial(\lambda,\epsilon)=4\lambda^3(a^2+1)^2>0$. Adding the calibrated interior directional statistic contributes a maximal minor with absolute value
$$ \frac{4\lambda^3(a^2+1)^2\sin^2k}{(a^2+1-2a\cos k)^{3/2}}>0. $$
This proves **first-order local rank recovery**, not a finite-sample confidence guarantee or calibration feasibility.

## 4. Simultaneous finite-error inference

At three momenta, let $\widehat q_{i,s}$ be multinomial empirical fractions from $n_i$ independent preparations. Suppose every setting has a justified deterministic per-category readout error $\beta_i$. Hoeffding's union bound yields with probability at least $1-\alpha$,

$$|\widehat q_{i,s}-q_{i,s}(\xi_0)|\le \sqrt{\frac{\log(24/\alpha)}{2n_i}}+\beta_i\quad\text{for all 12 cells.}$$

The compatible set of parameters in a predeclared compact admissible domain is therefore a valid model-relative confidence region. Converting this into a diameter or sample guarantee additionally requires a quantitative inverse modulus and calibration bounds. Profiled Fisher information describes only the local tangent experiment, not global aliasing or goodness of fit.

## 5. Exact histogram-only quasifree feasibility and partial identification

**Theorem 4 (sharp counting-data theorem).** Let $q=(q_{00},q_{10},q_{01},q_{11})$ be any nonnegative normalized joint-number histogram. Consider *all* gauge-invariant two-mode density operators producing precisely $q$, with their individually covariance-matched quasifree states $\omega_C$. Put $a=q_{10}q_{01}$ and $b=q_{00}q_{11}$. Then

$$
\boxed{\min_{\rho\mapsto q}\|\rho-\omega_{C(\rho)}\|_1=4(b-a)_+,\qquad
\max_{\rho\mapsto q}\|\rho-\omega_{C(\rho)}\|_1=4\max\{b,|a-b|\}.}
$$

Every value between the displayed extrema is attained. There exists a gauge-invariant quasifree state producing $q$ **if and only if** $a\ge b$. Every gauge-invariant state producing $q$ is quasifree **if and only if** $a=b=0$.

*Proof.* In the occupation basis $|00\rangle,|10\rangle,|01\rangle,|11\rangle$, every state with histogram $q$ has a block-diagonal density matrix with one-particle block

$$\begin{pmatrix}q_{10}&z\\ \bar z&q_{01}\end{pmatrix}.$$

Its positivity is equivalent to $0\le |z|^2\le a$. By Theorem 1, $\|\rho-\omega_C\|_1=4|a-b-|z|^2|$. As $u=|z|^2$ ranges continuously over $[0,a]$, the signed defect ranges over $[-b,a-b]$. Elementary optimization of its absolute value gives both sharp extrema. Zero is attainable exactly when $a\ge b$. The distance vanishes for *every* permissible coherence only when $a=0=b$. $\square$

**Finite-error falsification.** If a normalized empirical histogram $\widehat q$ obeys the simultaneous deterministic error envelope $\|q-\widehat q\|_\infty\le\delta$, the elementary product Lipschitz bound for $F(q)=q_{10}q_{01}-q_{00}q_{11}$ gives

$$\boxed{\|\rho-\omega_C\|_1\ge 4[\widehat q_{00}\widehat q_{11}-\widehat q_{10}\widehat q_{01}-\delta]_+.}$$

Thus counting-only data can directly *reject* gauge-invariant quasifreeness when the product of empty and double-occupation probabilities is too large. The reverse inequality does not certify quasifreeness without measured coherence, except for the degenerate $a=b=0$ cases. Finite-shot confidence statements require a justified simultaneous error envelope; the deterministic theorem itself does not assume a sampling model.

### Exact examples

- $q=(9/20,1/20,1/20,9/20)$ forces **unhalved trace-norm distance** at least $4/5$ (operational trace distance at least $2/5$), regardless of any unmeasured coherence.
- $q=(1/10,2/5,2/5,1/10)$ admits both a quasifree state and non-quasifree states, with **unhalved trace-norm distance** ranging from zero to $3/5$ (operational trace distance from zero to $3/10$).
- The vacuum histogram $q=(1,0,0,0)$ admits only a quasifree state.

These are feasibility and falsification results on a specified two-mode state class, not a certification of the Gibbs Hamiltonian or an experimental apparatus.

## 6. Observation-alias controls and what counting alone cannot prove

For the exact histogram $q=(1/10,2/5,2/5,1/10)$, the one-particle coherence $z$ can satisfy $0\le|z|^2\le4/25$. By Theorem 1 the covariance-matched quasifree distance is $4|3/20-|z|^2|$. Thus $|z|^2=3/20$ is quasifree and $z=0$ is nonquasifree (distance $3/5$), **with exactly the same joint counting data**. A fully general stochastic readout map can likewise send every underlying histogram to one common observed histogram. These are exact aliases, not noise effects; calibrating the observation map and measuring coherence are logically separate premises.

For the simultaneous 12-cell Hoeffding envelope the independence condition is *independent experimental preparations within each setting*; it is not an assertion of independent categories within a single multinomial draw. Readout systematic error must be bounded separately. Such a confidence region is conditional on the specified data-generating model and does not prove its truth.

## References

1. H. Araki, "On Quasifree States of CAR and Bogoliubov Automorphisms," *Publications of the Research Institute for Mathematical Sciences* **6** (1971), 385–442, doi:10.2977/prims/1195193913.

2. W. Hoeffding, "Probability Inequalities for Sums of Bounded Random Variables," *Journal of the American Statistical Association* **58** (1963), 13–30, doi:10.1080/01621459.1963.10500830.

## Acknowledgments and AI-assisted research

Kirtus Justus provided research direction, the scientific questions, the supplied mathematical materials, and requirements for critical evaluation. ChatGPT (OpenAI) assisted with mathematical checking, manuscript preparation, and editorial examination. Additional AI systems used in the research program include Claude (Anthropic), Gemini (Google), Grok (SpaceXAI), and DeepSeek (High-Flyer). No particular proof, numerical calculation, or independent review is attributed to those systems without supporting records. AI systems are not listed as authors; responsibility for the submitted scholarly claims rests with the named author. The acknowledgment does not imply endorsement by any AI provider or independent peer review.
