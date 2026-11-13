---
title: "From Prephysical Hypotheses to Physical Models"
author: 'Kirtus Justus (Theoretical Physicist) \textbullet{} 31 October 2026\tabularnewline Port Coquitlam, British Columbia, Canada'
date: ''
lang: en
header-includes:
 - \usepackage{microtype}
 - \usepackage{booktabs}
 - \usepackage{longtable}
---

**Abstract.** This collection develops exact and quantitative results in several problems of mathematical identification: projector-equivalent Wilson–Dirac band Hamiltonians, relative entropy of restricted quasifree states, calibrated two-mode fermionic inference, positive spectral-measure feasibility, and representation-dependent transfer operators on compact groups. The methods combine explicit operator equivalences, Toeplitz–Jacobi concentration theory, positive-measure duality, numerical enclosures and calibrated observation maps. For the Wilson relative-entropy problem, exact reference geometry and two-bond asymptotics are supplemented by a positive-majorant theorem, finite-interval entropy bounds and reference-weighted estimates. An exact whole-line connection and a uniform fixed-interior expansion control the reference modular discrepancy after weighting by the Wilson majorant. For fixed positive scaled mass, these estimates and the cross-boundary trace-path limit determine the logarithmic coefficient, the finite part and an $O_\mu((\log L)^{-1})$ remainder of the specified Wilson relative entropy. A separate finite-dimensional estimate bounds the half-filled modular discrepancy uniformly by 7. The results concern interval restrictions of infinite-chain projectors. Conditional additive uniformity on bounded scaled masses is Proposition 7 of *Calibration, identified sets and uniform limits*; relative vanishing-mass, moving-edge and general-filling limits remain separate. Each result is stated for its specified operator, state or observation model.

**Keywords:** Mathematical identifiability; quasifree states; spectral feasibility; compact groups; conditional asymptotics.

## 1. Operator identification and mathematical inference

The CAR and finite-dimensional quasifree framework follows Araki [1]; generalized positive-quadrature background appears in Bojanov, Braess, and Dyn [2]. The concentration inequality used for finite-sample statements is Hoeffding’s [3]. The standard special-function identities are recorded in the NIST Digital Library of Mathematical Functions [4]. The classical discrete concentration and commuting free-fermion reference geometry is developed in [5,6].

The results concern several related but distinct mathematical structures: occupied-band projections, CAR quasifree covariances, positive spectral measures, inverse observation maps, and compact-group convolution semigroups. Their hypotheses specify the relevant Hilbert spaces, boundary conditions, operator topologies and observational protocols. Exact proofs and certified numerical enclosures provide different forms of mathematical evidence; calibration and experimental testing become relevant when a model is used to interpret measurements.

### Proof status and transfer of conclusions

A mathematical claim begins with its objects and quantifiers: the Hilbert space, operator domain, boundary condition, state class, observation map, normalization, admissible parameter set, and order of limits. A conditional statement lists each premise as a mathematical assertion whose truth can be checked. Phrases such as “appropriate uniform estimates” or “under standard hypotheses” do not specify a theorem when the missing estimates contain the substantive conclusion; such a statement is an open target until those hypotheses are quantified.

An exact finite identity, an identity of formal expansion coefficients, a finite-order uniform asymptotic estimate, and an empirical inference are different claims. A spectral asymptotic needs a connection to the exact operator with matched domains and normalizations, followed by a remainder estimate. For a trace application, the proof must also control the spectral weight outside the approximation region. A bounded remainder does not identify its limit. Uniformity at fixed interior cutoff does not establish a moving-edge theorem, and a fixed-index limit does not establish a moving-index estimate.

Each theorem has one designated statement and proof home. A paper importing it gives the source title and an exact named or numbered locator, repeats all hypotheses used locally, and identifies any displayed copy as a restatement. The synthesis describes scientific relationships and remaining questions; the glossary fixes terms and conventions; neither serves as an alternative proof repository. Results about different operators or observation classes are transferred only through an explicit map and a proved preservation statement.

Computational work is classified by the conclusion it actually establishes. Exact symbolic reductions are checked as identities on their stated domains. Rigorous numerical enclosures include the arithmetic, outward rounding or exact rational bounds, all relevant truncation errors, and the precise conclusion of the inclusion test. Local root existence, local uniqueness, feasibility, dual sign, and global optimality are separate assertions. High working precision, stable digits, a small residual, and agreement of independent implementations are useful diagnostics but do not replace these certificates. A numerical claim is downgraded if its certificate cannot be reproduced from the supplied inputs.

Proof verification and implementation verification remain separate. Tests compare quantities with independently derived formulas, exact special cases, sign and symmetry identities, or certified bounds. They record parameters, precision and errors; they do not count successful commands as theorem evidence. Every material correction is propagated to the canonical theorem, its summaries, dependencies and glossary references. Earlier weaker estimates may remain useful, provided their scope is distinguished from the current strongest theorem.

External mathematical results are cited at the precise statement used. The source's hypotheses, normalization and topology are checked against the application. A paper's abstract, an informal claim of novelty, or another model's theorem is not a substitute for this comparison. A newly written proof remains a manuscript result pending critical review; computational replication alone does not establish novelty or independent peer review.

Mathematical identification remains distinct from empirical identification. The preparation, accessible observable algebra, time and energy calibration, sampling model, nuisance parameters, and statistical error must be specified and tested when applying the model to data. An injective ideal observation map does not establish that nature belongs to the proposed model class. The methodology therefore allows the model, assumptions and even the proposed correspondence to be revised or rejected without changing what was proved conditionally within that model.

The human author retains responsibility for the scholarly claims. AI assistance is attributed only at the level supported by records; no unsupported authorship, credential, external review, or institutional endorsement is inferred from it.

The volume contents and article source references identify the proof locations. *Mathematical Terminology* fixes the conventions used by those statements.

## 2. Model-specific mathematical results

### 2.1. Occupied-projector invariance and dynamical identification

For

\[
h_m(k)=\sin k\,\sigma_x+(m+1-\cos k)\sigma_z,
\qquad g_\varepsilon(k)=1+\varepsilon\cos k>0,
\]

and an infinite translation-invariant gapped number-conserving band model, multiplication by \(g_\varepsilon\) does not change the occupied negative-band projection \(P_-(k)\), although the splitting changes. This exact assertion does **not** apply to arbitrary finite open-boundary truncations, finite-temperature covariances at calibrated inverse temperature, or unrestricted deformations. Three-frequency constraints, six-node divided differences and quadratic normalized inversion require their precise positivity, polynomial-degree and mass-branch hypotheses (as stated in the dynamical-identification article). The all-degree arbitrary spectral-function identification is excluded by a positive higher-degree interpolation alias (through a constructive finite-node counterexample).

### 2.2. Finite-interval Wilson relative entropy

Let $A_L=C_{L,\mu/L}$ and $B_L=C_{L,0}$ be interval restrictions of the infinite Wilson–Dirac occupied-band projectors, with $\mu>0$ fixed and $N=2L$. The massless covariance is unitarily equivalent to the half-filled sine kernel $B_N$, commuting with $J_N$, whose off-diagonal bonds are $j(N-j)/N$. The exact two-bond contribution satisfies
\[
\boxed{\mathcal P_L=\frac{\mu^2}{6}\log L+
\mu^2\left(\frac16\log\frac8\mu-\frac14\right)
+O_\mu\!\left(\frac{\log L}{L}\right).}
\]

For the specified Wilson projector difference, a positive majorant $G_N$ gives $\operatorname{Tr}G_N\le\mu/\pi$ and
\[
0\le D_N^2\le G_N-G_N^2\le G_N,
\]
together with an explicit inverse-power tail bound in the Jacobi spectrum. The nonlinear correction is bounded. A uniform Hankel trace-class estimate gives $|S(A_L)-S(B_L)|\le 2C\sqrt\mu$ whenever $\log(1+\mu/L)\le1/4$; in particular the entropy difference is $O_\mu(1)$ at fixed mass. The reference occupation-weighted modular error obeys $\operatorname{Tr}[B_N(I-B_N)E_N^2]=O((\log N)/N^2)$, implying a transverse contribution $O_\mu(\sqrt{\log N}/N)$. The proof combines a fixed-interior expansion with a global linear logit bound, as established in *Uniform Bulk Modular Asymptotics and the Leading Wilson Entropy Law*. The exact occupation fluctuation has logarithmic expansion $\operatorname{Tr}[B_N(I-B_N)]=\pi^{-2}[\log(2N)+\gamma+1-1/(6N^2)+7/(20N^4)+O(N^{-6})]$; the particle–hole involution also gives $\operatorname{Tr}(G_NE_N)=0$, without cancelling the longitudinal trace.

Write $K_N=\log(I-B_N)-\log B_N$ and $E_N=K_N+N\eta(J_N/N)$. For a common mode with $J_Nv_j=\lambda_jv_j$ and $B_Nv_j=\zeta_jv_j$, let $e_j=\log[(1-\zeta_j)/\zeta_j]+N\eta(\lambda_j/N)$.

For each fixed $0<\tau<1/2$ and integer $K\ge1$, the common reference modes satisfy
\[
e_j=\sum_{k=1}^K N^{1-2k}\varphi_{2k-1}(\lambda_j/N)
+O_{\tau,K}(N^{-2K-1}),\qquad |\lambda_j|\le\tau N.
\]
The coefficients are the even WKB periods; the statement is an asymptotic expansion to each finite order, not a convergent infinite series. In particular $|e_j|\le C/N$ for $|\lambda_j|\le N/4$. Globally, $|e_j|\le\pi N$. The Wilson majorant tail therefore gives
\[
\operatorname{Tr}(G_N|E_N|)=O_\mu(1),\qquad
|\operatorname{Tr}(S_NE_N)|\le\operatorname{Tr}(G_N|E_N|).
\]
No commutation of $G_N$ with the reference is required. Substituting these bounds and the bounded nonlinear and entropy terms into the exact finite decomposition proves
\[
\boxed{\mathcal D_L(\mu)=\frac{\mu^2}{6}\log L+O_\mu(1),\qquad \mu>0\text{ fixed}.}
\]
For the interval restrictions of the infinite-chain Wilson–Dirac occupied-band projectors, with the massive covariance in the first argument, $m=\mu/L$ and fixed $\mu>0$, Theorem 1 of *Finite Part of Wilson–Dirac Relative Entropy* gives
$$\mathcal D_L(\mu)=\frac{\mu^2}{6}\log L+\mu^2\left(\frac{13}{36}-\frac{\pi}{12}-\frac{\log\mu}{6}\right)-\mathcal S(\mu)+O_\mu((\log L)^{-1}).$$
Here $\mathcal S(\mu)$ is the finite cross-boundary trace path defined in Section 7 of that manuscript. It is not a difference of divergent continuum entropy traces. The constants and asymptotic onset may depend on $\mu$, and the stated rate is not claimed sharp.

For the even-dimensional half-filled reference, Theorem 3 of *Uniform Modular Control and Nonlinear Convergence for Wilson–Dirac Intervals* proves $\|E_N\|\le7$ for every even $N\ge2$. Its Corollary 4 gives a longitudinal modular trace $O_\mu(N^{-1})$ and a full modular trace $O_\mu(\sqrt{\log N}/N)$. Theorem 6 gives
$$\mathcal Q_N=\mu^2\left(\frac{11}{18}-\frac{\pi}{12}-\frac{\log2}{2}\right)+O_\mu\!\left(\sqrt{\frac{\log N}{N}}\right).$$
These estimates use the exact concentration connection, the specified Wilson majorant and pairing bounds, and finite-path estimates. They do not require a uniform moving-edge asymptotic expansion.

### 2.3. Two-mode quasifree feasibility and calibration

For a gauge-invariant state on **exactly two fermionic modes**, the covariance-matched quasifree **unhalved trace-norm** formula is exact (in the associated mathematical article). The conventional operational trace distance is half this norm. With a normalized joint-number histogram \(q=(q_{00},q_{10},q_{01},q_{11})\), put \(a=q_{10}q_{01}\) and \(b=q_{00}q_{11}\). The sharp feasible trace-distance interval is

\[
\boxed{4(b-a)_+\;\le\;\|\rho-\omega_{C(\rho)}\|_1
\;\le\;4\max\{b,|a-b|\}.}
\]

All values in the interval are attainable; existence of a compatible quasifree state is equivalent to \(a\ge b\), whereas counting alone forces quasifreeness only for \(a=b=0\) (in the two-mode counting theorem). Thus counting-only data can sometimes reject, but generally cannot certify, this model class. The signed common *in-plane* detector-tilt inversion and calibrated orbital-direction rank recovery remain dependent on the specified observation map (as established under the stated calibration hypotheses). An arbitrary three-dimensional readout axis admits counterexamples (through a constructive finite-node counterexample). Finite-shot coverage requires independent preparations and justified readout-error bounds; an unrestricted stochastic readout channel can erase every parameter distinction.

### 2.4. Global positive-measure spectral feasibility

For a positive probability measure on \([0,\infty)\), finitely many polynomial moments and Laplace values define an inverse feasibility problem. A properly signed extended-Chebyshev Hermite dual certifies a globally optimal **largest feasible lower-support threshold**, not the actual threshold of an unknown measure (in the associated mathematical article). The exact-data, rectangular-error, and fixed ellipsoidal-error benchmarks have distinct analytic and computational certificate requirements. A proposed correlation-dependent correction crossing is presently supported by a high-precision numerical root, not by a reproduced outward-rounded enclosure for the augmented crossing system. Fresh exact-rational interval certificates enclose the exact-data, rectangular and correlated-ellipsoid primal-dual systems separately in boxes of radius $10^{-90}$. The repaired sufficiency theorem requires a singleton exposed uncertainty face for both optimality and uniqueness; each benchmark satisfies that condition. The **80-digit fractional prefix** of the correlated-ellipsoid optimal support threshold is

\[
\resizebox{0.98\linewidth}{!}{$x_1=1.13845745148468164795870658112096059644751252685084364686503566728597685193350532\ldots.$}
\]

The full extremal conclusion also invokes the analytic positive-measure dual; the enclosure alone verifies its specified nonlinear system. Each benchmark has its own positive-weight, ordered-node and dual-sign certificate; the analytic theorem supplies global optimality separately. The separate $\rho_c$ crossing remains a numerical candidate, not part of this interval certificate. The fixed ellipsoid specifies deterministic observation uncertainty and is not an inferred measurement covariance matrix.

### 2.5. Auxiliary compact-group transfer and ultraviolet topology

For an explicitly specified central SU(2) convolution family, the character Hilbert space has one state per representation label whereas full \(L^2(SU(2))\) carries multiplicity \(n^2\). The resulting Schatten and normalized-trace ultraviolet statements refer to different topologies and scalings (in the associated mathematical article). The bi-invariant commutant assertion is exact (under the stated symmetry condition); the Schatten–Duhamel estimate applies to bounded self-adjoint, **possibly noncommuting**, perturbations under the stated semigroup hypotheses. Normalized Gibbs operators obey the general scalar-shift-invariant bound

\[
\boxed{\|\rho_{A+V}(s)-\rho_A(s)\|_1
\le\min\{2,s\,\operatorname{osc}(V)\}.}
\]

This bound is independent of representation multiplicity. In the conventional trace-distance normalization, its right side is halved and capped at $1$. The sharp Bessel moving-window limits and proposed noncommuting ultraviolet construction are unproved targets: neither quantified sufficient remainder hypotheses nor an explicit complete construction are supplied. The diagonal moving-projection example establishes its own normalized rate order, and the fixed-positive-time operator-norm limits have a separate elementary proof. The Hilbert space and representation multiplicity remain those of the specified compact-group model.

## 3. Mathematical relationships and limits of transfer

**Ground-state equivalence.** Positive scalar Bloch multiplication preserves the common-algebra infinite-chain occupied projector. Accordingly, the two *same-mass ground states* and all their finite-region restrictions coincide, so their relative entropy with respect to each other is exactly zero. This does **not** set to zero another model's relative entropy between different masses.

**Calibrated thermal distinction.** At fixed inverse temperature \(\beta>0\), a two-band number-conserving Gibbs covariance reads

\[
C_{\beta,g}(k)=\tfrac12\left[I-\tanh(\beta g(k) E_m(k)/2)\,h_m(k)/E_m(k)\right].
\]

Strictly positive multipliers that are invisible in the ground-state occupied projector can be distinguishable in this calibrated thermal observation. Unknown temperature, time or energy scale changes the inverse problem.

**Positive heat-kernel spectral measure.** Fix \(\gamma,s_0>0\) in the *auxiliary* SU(2) model, with \(a_{\gamma,n}=-\gamma\log(I_n(\gamma)/I_1(\gamma))\) and representation multiplicities \(d_n\in\{1,n^2\}\) as specified by the chosen Hilbert space. Then

\[
\mu_{\gamma,s_0}=\frac1{Z_\gamma(s_0)}\sum_{n\ge1}d_n e^{-s_0a_{\gamma,n}}\delta_{a_{\gamma,n}}
\quad\Longrightarrow\quad
\int e^{-tE}\,d\mu_{\gamma,s_0}(E)=\frac{Z_\gamma(s_0+t)}{Z_\gamma(s_0)}.
\]

For fixed parameters this is a positive probability measure with finite polynomial moments and vacuum support threshold zero. This is a mathematical map from one fixed auxiliary spectrum into another model's general observation class; it does not reproduce another model's six observation values without a separate computation.

**Observation-channel nonuniqueness.** A joint-number histogram may be shared by a quasifree and a nonquasifree state, and an arbitrary column-constant stochastic readout map can make all physical histograms observationally identical. No statistical sample size repairs absent calibration or a non-identifying observation family.

## 4. Scope of results

| Subject | Established scope | Additional conditions |
|---|---|---|
| Projector-equivalent Hamiltonians | Exact equality of occupied-band projectors in a common infinite translation-invariant model | Not an equality of finite open-boundary spectral projectors or dynamics |
| Finite-interval relative entropy | Exact reference and two-bond results; fixed-$\mu$ finite part with $O_\mu((\log L)^{-1})$ remainder; even half-filled bound $\|E_N\|\le7$ | Specified Wilson model; conditional bounded-mass additive uniformity (companion Proposition 7); relative vanishing-mass limits remain separate |
| Two-mode quasifree identification | Exact state-space witness and counting-only feasibility characterization | Experimental inference additionally requires preparation independence and calibrated observables |
| Spectral feasibility | Global positive-measure duality and explicitly stated benchmark optimizers | Nonrational optima additionally rely on rigorous arithmetic enclosures and dual sign conditions |
| Compact-group semigroups | Exact representation formulas and bounded-perturbation estimates | Sharp moving-window ultraviolet limits require uniform Bessel estimates and summable tails |

## 5. Open mathematical questions

For this fixed-positive-scaled-mass comparison, the finite part and an inverse-logarithmic remainder are determined, and the half-filled reference has a uniform finite-dimensional modular bound. Further questions concern moving-edge expansions, relative vanishing-mass limits, general filling and sharper boundary-entropy control; conditional bounded-mass additive uniformity is supplied by the companion Proposition 7. A bound on the exact finite spectral modes does not itself supply a moving-edge expansion at arbitrary interpolation parameters. The auxiliary $SU(2)$ problem has separate uniform modified-Bessel and spectral-tail requirements, and the proposed correlation-dependent spectral-feasibility crossing requires a complete interval certificate. These are distinct mathematical questions.

Applications to data require specifying how the idealized state and observation maps are realized and calibrated. This methodological issue accompanies, rather than replaces, the operator-theoretic and inverse-problem results of the collection.

## References

1. H. Araki, "On Quasifree States of CAR and Bogoliubov Automorphisms," *Publications of the Research Institute for Mathematical Sciences* **6** (1971), 385–442, doi:10.2977/prims/1195193913.

2. B. D. Bojanov, D. Braess, and N. Dyn, "Generalized Gaussian Quadrature Formulas," *Journal of Approximation Theory* **48** (1986), 335–353, doi:10.1016/0021-9045(86)90008-0.

3. W. Hoeffding, "Probability Inequalities for Sums of Bounded Random Variables," *Journal of the American Statistical Association* **58** (1963), 13–30, doi:10.1080/01621459.1963.10500830.

4. National Institute of Standards and Technology, *Digital Library of Mathematical Functions*, §§10.32, 10.41, 19.12.

5. D. Slepian, “Prolate Spheroidal Wave Functions, Fourier Analysis, and Uncertainty—V: The Discrete Case,” *Bell System Technical Journal* **57** (1978), 1371–1430, doi:10.1002/j.1538-7305.1978.tb02104.x.

6. V. Eisler and I. Peschel, “Analytical Results for the Entanglement Hamiltonian of a Free-Fermion Chain,” *Journal of Physics A* **50** (2017), 284003, doi:10.1088/1751-8121/aa76b5.

## Acknowledgments and contributions

Kirtus Justus directed the research questions, selection of mathematical models and publication standards and is the sole named author. ChatGPT (OpenAI) assisted with derivations, critical checks and manuscript preparation, including the Wilson mathematical continuation. Claude (Anthropic), Gemini (Google), Grok (SpaceXAI), and DeepSeek (High-Flyer) contributed to the wider research process; attribution of particular arguments is limited to traceable records. The named author is responsible for the claims presented here.
