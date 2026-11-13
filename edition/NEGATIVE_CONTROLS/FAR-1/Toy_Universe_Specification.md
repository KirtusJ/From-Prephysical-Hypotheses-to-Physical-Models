---
title: "Toy Universe Specification"
subtitle: "FAR-1: Finite Amplitude-Record Universe | formal rules, verified examples, model selection and withdrawal gates"
author: "Research direction: Kirtus Justus | Adversarial specification: LLM Director C"
date: "11 November 2026 | B.C. Pacific Time"
lang: en-CA
toc: true
toc-depth: 3
---

> **Status and epistemic contract.** FAR-1 is a fully specified **finite mathematical toy**, not a physically established ontology. Its complex vector space, amplitudes, probability rule, record instruments, update parameter, spatial ring and expansion law are **stipulations**. Propositions that follow from them are proved or numerically checked only in the stated scope. No emergence of quantum mechanics, Hamiltonian mechanics, gravitation, cosmology or a Millennium theorem is claimed. **Parent Unary PCP: Initial External Grounding, OPEN**, unchanged. This dossier closes an assistant session, not the parent phase.

# 0. Identity, provenance and scope

**Candidate identifier:** FAR-1 (Finite Amplitude-Record Universe). **Relationship to withdrawn TO-0:** no continuity of claimed ontological selection. TO-0 is a retained comparator showing that finite contextual bookkeeping and nonsignalling admit incompatible probability theories. FAR-1 instead installs conventional quantum probability explicitly in order to obtain a checkable integrated toy.

**Scientific status:** `STIPULATED`, with finite derived conditional theorems, independent numerical controls and a large `NOT_IDENTIFIED` physical bridge. **Authorship:** Research direction by Kirtus Justus. Director C prepared this mathematical artifact; other directors' prior results are internal research provenance, not independent physical replication or endorsement.

**Source intake:** The attached Director B Bell Memory/Sequential QA handoff passed direct ZIP integrity, 18/18 local manifest checks and the supplied fast release validator. Its 19-round and 28-round calculations were separately tested numerically. These do not bear evidentiary weight in favor of FAR-1; they are statistical and QA controls. The November 10 source baseline remains frozen at SHA-256 `fde41b3789930b0848cffd80b0ced68b052645808c393525266b1457d6d669cf`. Historical Wilson-Dirac $M_s$, eight-output copying optimum, calibration and physical emergence obligations remain open.

**Rival sources:** Existing quantum cellular automata, decoherent histories, causal sets, lattice/Regge gravity and standard cosmology already occupy much of this mathematical space. Treat FAR-1 as a recombination of familiar mathematical mechanisms, not a priority claim [E1-E7].

# 1. The selection problem was tested before writing these rules

A bounded adversarial comparison examined four architectures:

| Prototype | Mathematical commitment | Adverse control | Scope disposition |
|:--|:--|:--|:--|
| `CLS` | Finite classical stochastic latent sites | Classical probability maps are affine; no arbitrary coherent phase interference | Reject as source of exact interference under its premises |
| `CTX` / TO-0 | Contexts + compatible conditional output tables | Local, quantum and postquantum PR tables satisfy the same nonsignalling constraints | TO-0 total-ontology candidacy remains withdrawn |
| `ORD` | Finite order / geometric adjacency | No unique probability law, physical duration or metric follows | Do not select |
| `FAR-1` | Finite complex amplitudes + record instrument + scalar expansion | Achieves integrated examples **by importing** all major physical structures | Admit as **stipulated mathematical toy only** |

No prototype has earned standing as a physical ontology. FAR-1 is chosen as a **complete executable counterexample target**; other prototypes remain independent negative controls. This decision was made after, not despite, preserving the foundational nonselection results.

# 2. Definition of the finite toy universe

Fix an integer $N\ge1$ and a maximum formal step count $T\ge0$. Let $V=\mathbb Z/N\mathbb Z$ be a labelled cyclic set of sites. For $N=1$ there are no interaction edges; for $N=2$ there is a single undirected edge; for $N\ge3$, $E$ is the usual ring edge set $\{\{x,x+1\}:x\in V\}$.

Each site is given the **imported mathematical two-level complex space** $H_x=\mathbb C^2$. The total matter space and state set are

$$
H=\bigotimes_{x\in V}\mathbb C^2,\quad d=2^N,
\qquad
\mathcal S(H)=\{\rho\in M_d(\mathbb C):\rho=\rho^\dagger,\rho\succeq0,\operatorname{tr}\rho=1\}.
$$

The **toy state** before step $n$ is $(a_n,\rho_n)$, where $a_n>0$ is a scalar size register and $\rho_n\in\mathcal S(H)$. The toy sample space also includes a finite string of reported outcomes $R_{0:n-1}$. We distinguish the **unconditioned state** $\rho_n$, used for the deterministic benchmark scale update, from any **record-conditioned state** of an individual observational branch.

**Explicit non-conclusions:** neither $V$ nor $n$ is derived physical space/time; the two-level spaces are not claimed to be emergent physical qubits; the state-space tensor product is imported rather than selected; no physical substance corresponding to abstract "noise" is asserted.

A mathematical redundancy exists: cyclic relabelling of all site indices leaves the Hamiltonian and uniform record instrument equivariant. This is only a finite global *reindexing* symmetry. It is **not** a derivation of gauge theory, local gauge invariance or diffeomorphism symmetry.

# 3. Stipulated parameters and initial conditions

Let $\Delta>0$, $J\ge0$, $h\ge0$, $\kappa\in[0,1]$, $\zeta\ge0$, and $(\Omega_r,\Omega_m,\Omega_\Lambda)$ with each nonnegative and $\Omega_\Lambda>0$. The three background weights may sum to one, but this is a **normalization choice**, not a physical density closure when $\zeta\ne0$.

Set $\hbar_{\rm toy}=1$. Choose $a_0>0$ and $\rho_0\in\mathcal S(H)$. The reproducible benchmark uses:

$$
N=4,\quad T=5,\quad \Delta=0.1,\quad J=0.6,\quad h=1,
\quad \kappa=0.35,\quad\zeta=0.05,
$$
$$
(\Omega_r,\Omega_m,\Omega_\Lambda)=(0.01,0.30,0.69),\quad
a_0=1,\quad \rho_0=|0000\rangle\langle0000|.
$$

These are illustrative dimensionless numbers, **not estimated cosmological parameters**. No physical unit or clock calibration is supplied.

# 4. Matter evolution: stipulated amplitude dynamics

Let $X_x$ and $Z_x$ be Pauli matrices acting on site $x$ and identity elsewhere. Define, for $a>0$,

$$H_m(a)=-\frac Ja\sum_{\{x,y\}\in E} Z_xZ_y-h\sum_{x\in V}X_x,$$

$$U_a=\exp[-i\Delta H_m(a)].$$

$H_m(a)$ is Hermitian for all allowed parameters, so $U_a$ is unitary. The short-range Hamiltonian terms do **not** imply a strict exact light cone for $U_a$ in one finite step; no relativistic causal bound has been derived. Existing quantum lattice-model precedents are relevant [E1-E2].

If there were no record operation, $\rho_{n+1}=U_{a_n}\rho_nU_{a_n}^\dagger$ would preserve normalization, positivity, spectrum and purity, but not necessarily matter energy because the external size register changes $H_m(a_n)$. This is a conventional mathematical quantum evolution **assumed** in FAR-1.

# 5. Recording instrument and observation law

At one site define three measurement operators, indexed by $r\in\{\emptyset,0,1\}$:

$$M_\emptyset=\sqrt{1-\kappa}\,I,\qquad
M_0=\sqrt\kappa\,|0\rangle\langle0|,\qquad
M_1=\sqrt\kappa\,|1\rangle\langle1|.$$

They obey $\sum_rM_r^\dagger M_r=I$. For a complete record label ${\bf r}=(r_x)_{x\in V}$ set $M_{\bf r}=\bigotimes_x M_{r_x}$. The selective update and its Born-style record probability are

$$
\widetilde\rho_{n+1,\mathbf r}=M_{\mathbf r}U_{a_n}\rho_nU_{a_n}^\dagger M_{\mathbf r}^\dagger,
\quad
p(\mathbf r\mid a_n,\rho_n)=\operatorname{tr}\widetilde\rho_{n+1,\mathbf r}.
$$

When $p>0$, the state conditioned on observing ${\bf r}$ is $\rho_{n+1\mid\mathbf r}=\widetilde\rho_{n+1,\mathbf r}/p$. The unconditioned update used in the benchmark is

$$
\boxed{\rho_{n+1}=\Phi_{a_n}(\rho_n)=\sum_{\mathbf r}\widetilde\rho_{n+1,\mathbf r}.}
$$

**Status:** the trace pairing is an **imported Born-style probability rule**. No frequency, detector, observation, subjective observer or measurement ontology is derived from the earlier prephysical program. This is deliberate: a fully specified toy may stipulate what the foundational research has not identified, provided the stipulation is visible.

For computational basis strings $s,t\in\{0,1\}^N$, the channel after the unitary multiplies off-diagonal matrix elements by

$$\bigl(1-\kappa\bigr)^{d_H(s,t)},$$

where $d_H$ is Hamming distance. Diagonal entries are unchanged by dephasing. This identity permits efficient exact numerical reproduction for small $N$.

The instrument defines a complete finite history distribution by composing selective maps. Since $a_n$ is driven by **unconditioned** $\rho_n$, the scale trajectory in FAR-1's benchmark does **not** depend on which individual record sequence actually occurs. This mean-field feature is mathematically consistent but physically suspect: there is no local single-history stress-energy law, no fluctuation backreaction, and no derivation of a conservation equation.

# 6. Geometry/expansion register: a stipulated scalar law

Define the occupied-fraction operator

$$Q=\frac1N\sum_{x\in V}\frac{I-Z_x}{2},\quad 0\preceq Q\preceq I,
\qquad q_n=\operatorname{tr}(Q\rho_n)\in[0,1].$$

Let

$$F(a,q)=\Omega_r a^{-4}+\Omega_m a^{-3}+\Omega_\Lambda+\zeta q a^{-3}.$$

The scale update is **defined**, not deduced, by

$$
\boxed{a_{n+1}=a_n+\Delta\,a_n\sqrt{F(a_n,q_n)}.}
$$

With $a_n>0$, $F\ge\Omega_\Lambda>0$, so $a_{n+1}>a_n>0$ for all finite steps. Matter influences geometry only through the abstract scalar $q_n$. Geometry influences matter through the $J/a_n$ coupling. This is a genuine finite **bidirectional mathematical coupling**, albeit a crude, noncovariant one.

**It is not GR:** there is no Lorentzian metric, light cone, local Einstein equation, gravitational constraint algebra, equivalence principle, covariance or stress-energy conservation. The $a^{-3}$ and $a^{-4}$ terms mimic familiar homogeneous cosmological scaling only by choice. The optional $\zeta q a^{-3}$ backreaction is not sourced from a conserved energy density.

For fixed $q$ and $\Delta\to0$ on a compact interval away from $a=0$, the scalar Euler discretization approximates $\dot a=a\sqrt{F(a,q)}$ by standard ODE convergence arguments. But when $q$ evolves with the quantum state, a *coupled* convergence theorem requires additional bounds and a specified simultaneous continuum scaling. No such theorem is asserted here.

# 7. Formal update algorithm and proof obligations

For $n=0,\ldots,T-1$:

1. Evaluate $q_n=\operatorname{tr}(Q\rho_n)$.
2. Calculate $H_m(a_n)$ and $U_{a_n}$.
3. Calculate every outcome probability $p({\bf r}\mid\rho_n,a_n)$; its sum must equal one.
4. Update the **unconditioned** state $\rho_{n+1}=\Phi_{a_n}(\rho_n)$.
5. Update $a_{n+1}=a_n+\Delta a_n\sqrt{F(a_n,q_n)}$.
6. Retain a separate sample-history distribution if sample records are needed. Do not confuse one sample history with the unconditioned density matrix.

**Theorem 1 (finite well-definedness).** If the initial state is positive and trace one, the stipulated finite update preserves positivity and unit trace for every $\rho_n$ and $a_n>0$. *Proof.* $U_a$ is unitary, each selective map is completely positive, and $\sum M_{\bf r}^\dagger M_{\bf r}=I$. Thus their sum is trace-preserving and completely positive. The scalar $F$ is strictly positive and the Euler factor $1+\Delta\sqrt F$ is strictly greater than one. Induction on $n$ completes the proof. This proves **internal existence for finite $T$**, not any infinite-time physical claim.

**Theorem 2 (record normalization).** For each pre-step state, $\sum_{\bf r}p({\bf r}\mid a,\rho)=1$. *Proof.* Cyclicity of trace and instrument completeness give $\operatorname{tr}(U_a\rho U_a^\dagger)=\operatorname{tr}\rho=1$.

**Theorem 3 (classical probability channel at full dephasing).** Set $\kappa=1$ and assume the input $\rho$ is diagonal in the computational basis with probabilities $(p_s)$. Then $\Phi_a(\rho)$ is diagonal with

$$p'_{t}=\sum_s |(U_a)_{ts}|^2p_s.$$

The matrix $T_{ts}=|(U_a)_{ts}|^2$ is column-stochastic. This is a mathematical stochastic reduction, **not** a derivation of classical mechanics.

**Non-theorem (physical emergence):** no result above justifies the actual existence of a state with this Hilbert structure, the choice of the instrument, the clock interpretation of $n$, the presence of a cosmological scale factor, or the meaning of $\hbar_{\rm toy}$.

# 8. Four exact toy experiments

## 8.1 Single-site interference and record-induced suppression

Start in $|0\rangle$; apply $H_2=\frac1{\sqrt2}\begin{pmatrix}1&1\\1&-1\end{pmatrix}$, then $P_\phi=\operatorname{diag}(1,e^{i\phi})$, then the record channel of strength $\kappa$, and then $H_2$ again.

Direct matrix multiplication gives

$$\boxed{p_0(\phi,\kappa)=\frac{1+(1-\kappa)\cos\phi}{2}.}$$

For $(\phi,\kappa)=(0,0)$ the result is $1$; for $(\pi,0)$ it is $0$; for $(0,1)$ and $(\pi,1)$ it is $1/2$. These are **inferred from imported quantum operations**; they do not demonstrate why the operators or probabilities should exist physically.

## 8.2 Classical Markov comparator and failed selection

Apply either $U=I$ or $U=X$ to the same fully dephased, uniformly mixed input. Both preserve the stationary distribution $(1/2,1/2)$, while the first preserves a binary label and the second flips it. Static probabilities do not uniquely select dynamics. Apply $U=H_2$ instead and the induced transition matrix has all entries $1/2$.

This supplies both a positive control (the stochastic formula is correct) and a negative control (stationarity does not identify dynamics).

## 8.3 Four-site coupled matter and scale trajectory

For the benchmark parameters in Section 3, independently computed values are:

| $n$ | $a_n$ | $q_n$ | $\operatorname{tr}(\rho_n^2)$ |
|--:|--:|--:|--:|
| 0 | 1.000000000 | 0.000000000 | 1.000000000 |
| 1 | 1.100000000 | 0.009919248 | 0.955395390 |
| 2 | 1.205657116 | 0.032095978 | 0.847016034 |
| 3 | 1.317908072 | 0.061066797 | 0.706137027 |
| 4 | 1.437664328 | 0.093232322 | 0.566212548 |
| 5 | 1.565839943 | 0.126349517 | 0.445785736 |

Checks performed: every density operator remains Hermitian and normalized; all tested eigenvalues remain nonnegative within numerical tolerance; each tested unitary obeys $U^\dagger U=I$ within numerical tolerance; $a_n$ remains positive and grows. Numerical validation is not a proof of all input states, which is instead supplied by Theorems 1-2.

The decreasing purity is a feature of the particular **unconditioned record channel**, not a derivation of a thermodynamic second law.

## 8.4 Fixed-horizon Bell-statistics control, external to FAR-1

As a separate statistical-regression check, put $q_Q=(2+\sqrt2)/4$, $p=199/200$, and $n=28$. Reject the quantum null on 28 wins, and on exactly 27 wins independently reject with probability $\gamma=85/128$.

The stipulated binomial comparison gives

$$\alpha=q_Q^{28}+28\gamma(1-q_Q)q_Q^{27}=0.04973846493057\ldots,$$

$$\mathrm{power}=p^{28}+28\gamma(1-p)p^{27}=0.95025377009762\ldots.$$

These calculations match the source Director B result and were independently numerically reproduced. They are **not generated by FAR-1** and are carried only to prevent an implementation from confusing finite-horizon power, optional stopping, memory conditions and evidence of physics. The validity under memory requires the corresponding *per-round conditional win-probability bounds*; average winning rates alone do not imply them.

# 9. The problem of history, probability and classicality

FAR-1 has a concrete operational record law, not a derived Born rule. If one instead tries to use arbitrary complex path weights for fine histories, the formula

$$D(A,B)=\operatorname{tr}(C_A\rho_0 C_B^\dagger)$$

is a decoherence functional only after the class operators $C_A$ and the framework have been defined. Disjoint history sets cannot generally receive additive probabilities when their interference terms are nonzero. The known consistent/decoherent histories literature makes this distinction [E3].

**Why "quantum to classical" is not solved:** (i) mathematical dephasing does not select an observed pointer basis; (ii) a stochastic probability transition is not the same thing as a symplectic flow; (iii) a local classical world of rods and clocks needs actual geometry and stable macroscopic variables; (iv) a large-action stationary-phase approximation alone does not establish suppression of all nonclassical alternatives. No theorem connecting these requirements has been established for FAR-1.

A separate imported classical comparator can be written as

$$S_{\rm cl}[q]=\sum_{n=0}^{T-1}\left[\frac{m(q_{n+1}-q_n)^2}{2\Delta}-\Delta V(q_n)\right].$$

Its stationary interior trajectories satisfy

$$m\frac{q_{n+1}-2q_n+q_{n-1}}{\Delta^2}=-V'(q_n).$$

This follows directly from discrete variation. But the action is **not derived from FAR-1's spin Hamiltonian or recording rule**. It is included as an independent classical target and a warning against declaring that a visually plausible path automatically obeys Newtonian dynamics.

# 10. Geometry, gravity and continuum obligations

The toy's ring is one spatial combinatorial circle, not a spatially three-dimensional manifold. Its expansion scalar is not a metric tensor. Its finite H is not Lorentz invariant. There is no curvature or Einstein equation. To make a geometry-bearing successor one might stipulate a simplicial complex with edge lengths and a Regge action involving hinge volumes and deficit angles. Regge calculus is an established discretization framework [E5]; installing its action would **not** derive general relativity from the present primitives.

A Lorentzian, dynamically constrained, physically coupled theory would require at least: a suitable causal structure; metric or equivalent geometrical observables; stress-energy and local conservation; gravitational constraint evolution; boundary terms; a demonstrated continuum scaling; a quantum measurement theory compatible with the geometry; and independent observational comparisons. This version does not contain those objects.

Causal-set programs provide a notable competing comparison: most finite causal structures do not look like continuum spacetimes, and an independent manifold-likeness/selection issue remains central [E4]. This reinforces, rather than rescues, FAR-1's selection problem.

# 11. Cosmological coverage and proposed *research questions*

Every entry below is an **unearned extension obligation**, not a solution, discovery or physically meaningful parameter estimate.

| Cosmological domain | What FAR-1 actually has | Proposed conditional extension / falsification gate |
|:--|:--|:--|
| Expansion history and acceleration | One positive scalar $a_n$ | Recover full FRW/GR constraints and an observation likelihood; compare CMB, BAO and supernova distances |
| Dark energy and possible evolution | Constant chosen $\Omega_\Lambda$ | Introduce independent dynamics for $w(a)$; test against DESI, CMB and systematics rather than post hoc fitting |
| Dark matter / structure formation | No halo, lensing or growth model | Add gravitating matter perturbations, conserved stress-energy and lensing predictions |
| Inflation and initial conditions | Chosen initial state | Derive perturbation spectrum, reheating and observable tensor/non-Gaussian predictions |
| Baryogenesis and particle content | Generic two-level labels | Establish quantum field content, symmetries and out-of-equilibrium dynamics |
| Neutrinos, CMB and nucleosynthesis | No neutrinos or plasma | Obtain a physically calibrated radiation/particle sector and compare independent datasets |
| Black holes, horizons and information | None | Establish Lorentzian metric, horizon definition, field quantization and entropy balance |
| Singularity/bounce and topology | Positive discrete scalar | Establish continuum existence/boundary criterion; avoid assuming that a finite step removes physical singularities |
| Hubble and related observational tensions | No dimensional Hubble constant or calibration | Fit a predeclared likelihood and include nuisance/systematic uncertainties |
| Gravitational waves and relativistic tests | No propagating geometry | Recover waves and established solar-system/strong-gravity observables with no arbitrary tuning |

External grounding: Particle Data Group 2025 cosmology reviews [E6] and DESI's July 2026 results [E7] describe real multi-dataset analysis. In particular, later DESI Lyman-alpha results can shift the comparison between evolving dark-energy and baseline models. No single cosmological narrative is imported as settled.

The phrase "all problems in cosmology" does not denote a mathematically enumerable finite set. This table is a **major-domain coverage map**, and should not be advertised as exhaustive.

# 12. Millennium Prize problem disposition and $\pi,\tau$

A toy's finite recurrence, lattice action or numerical approximation cannot satisfy an unrelated official infinite/continuum theorem. The following separate research questions do not constitute proposed proofs:

| Official topic | Possible toy-related analogy | Exact missing mathematical deliverable |
|:--|:--|:--|
| $P$ versus $NP$ | Computational cost of finite toy simulation | A proof for all instances in the formal uniform complexity classes |
| Riemann hypothesis | Spectral analogies | A theorem about all nontrivial Riemann zeta zeros |
| Birch and Swinnerton-Dyer | Finite arithmetic states | A general theorem relating elliptic curve rank and $L$-function behavior |
| Hodge conjecture | Combinatorial homology | A theorem about rational Hodge classes of arbitrary smooth complex projective varieties |
| Yang-Mills existence/mass gap | Finite spin spectra and positive gaps | A nonperturbative four-dimensional continuum construction meeting the official axioms |
| Navier-Stokes existence/smoothness | Finite update stability | The required 3D continuum theorem under the official problem alternatives; Clay currently lists it Active despite the announced September 2026 proposed resolution |
| Poincare conjecture | Ring topology | Established solved independently (Perelman); no new result here |

Source and status: Clay Mathematics Institute [E8-E10]. No proof, resolution, priority, prize claim or new formal statement is asserted for FAR-1.

Within ordinary real mathematics, define

$$\pi:=4\arctan(1)=3.14159265\ldots,\qquad \tau_{\mathrm{turn}}:=2\pi=6.28318530\ldots.$$

Both are imported mathematical constants. Neither is a frequency, period or oscillatory property of any assumed prephysical structure. The tag $\tau_{\mathrm{turn}}$ avoids confusion with optical depth, stopping times, other tau parameters and prior internal research symbols.

# 13. Bounded adversarial child examinations

The new local review profiles follow the updated PCP 1.0's bounded procedures; a focused examination need not remain at G1 after completing its stated work. **Formal child-Council registration is not asserted** because the authoritative parent state and integration receipt were not supplied.

| Sub-PCP | Scope and adverse test | G1, G5, G6 local status | Disposition |
|:--|:--|:--|:--|
| TU-01 | Compare classical, contextual, causal-order and amplitude architectures | Locally finished | No prephysical route selected |
| TU-02 | Positivity, trace preservation, record normalization, scale positivity and 4-site checks | Locally finished | `SUPPORTED_IN_SCOPE`, internal only |
| TU-03 | Interference, dephasing and classical Markov limit; demand Newton/Hamilton bridge | Locally finished | Stochastic limit proved; mechanics emergence not identified |
| TU-04 | Geometry, empirical cosmology, all seven prize topics | Locally finished screening | No physical or open-math solutions |
| TU-05 | Source verification, claim-to-evidence separation, sequential Bell contracts, QA false acceptance | Locally finished | Bounded reproducibility only |

A locally finished review may conclude "not identified" or "unsupported". Completion describes reaching a scope-specific decision, not approving the claim. There were no independent human experiments, hidden additional directors, background-running Councils or PCP state transitions.

**Review gate outcome:** the chosen FAR-1 satisfies *formal finite consistency*; it fails the selection, physical observation, continuum and explanatory novelty gates. The appropriate PCP disposition is `STIPULATED CONDITIONAL MODEL`, not `PHYSICAL EMERGENCE`.

# 14. Verification, reproducibility and false-acceptance controls

The source artifact includes a separately authored Python checker `verify_toy_models.py`, using NumPy/SciPy to test exact algebraic identities within numerical tolerance and to generate the benchmark table. The mathematical theorems about positivity and completeness in Sections 4-7 do not rely on this floating-point checker.

The checker performs: (1) normalization and positivity under prescribed parameters; (2) unitary residual controls; (3) exact analytic comparison of the interference formula; (4) verification of a full-dephasing induced stochastic transition; (5) scale-factor positivity on the tested finite trajectory; and (6) independent computation of the inherited seven-bit Bell bound.

**Negative controls that must fail stronger claims:** replacing complex amplitudes by generic nonnegative probabilities removes phase interference; merely matching Bell marginals leaves classical/quantum/PR ambiguity; a static stationary state does not select the transition; numerical agreement with a chosen $a_n$ recurrence does not identify its gravitational interpretation; and a self-authored archive manifest authenticates neither scientific evidence nor local PCP gate completion.

**Software QA boundary:** no provided validator can certify that the physical assumptions hold, that all prose claims are correct, that a proof has been globally checked or that a source identity was independently authenticated. The previous B/C gate-status and saved-reference mutation audits remain part of the internal provenance record. Optional-stopping and sequential-validity assumptions must be listed separately; repeating a fixed 19-round test until it passes is not valid at its nominal 5% false-rejection rate [E13].

# 15. Explicit withdrawal and continuation thresholds

FAR-1 is to be *retired as a foundational candidate* if any of the following remains true after a future committed selection test: its complex probability rule continues to be imported without explanatory warrant; alternative finite implementations fit all its proposed observable outputs; its observation rule cannot be independently identified; the selected update cannot reproduce the relevant symmetry and continuum constraints; its cosmological term can fit arbitrary observations only by free parameter additions; or its apparent new mathematics reduces to a standard imported theorem without an additional demonstrated implication.

It may nevertheless remain an educational numerical model even if every foundational claim fails. The finite theorems should not be discarded solely because the ontology claim fails.

A genuinely new physical claim would require a pre-registered discriminating observable, a likelihood with calibrated uncertainties, explicit alternatives, a non-circular link to actual apparatus, and independent replication. A proof claim requires a statement that meets its exact published mathematical target and an auditable proof, not a successful finite computation.

# 16. Final disposition

**Admit FAR-1 as a fully stipulated finite toy universe; reject any inference that it is a physically selected total ontology.** It contains finite matter, update, selective records, a toy size variable, feedback and computational tests. It does not explain the stipulated principles and does not recover relativistic gravity, macroscopic Newtonian mechanics or the actual universe.

The historical TO-0 withdrawal remains intact. The November 10 baseline stays frozen. Its Wilson-Dirac $M_s$ dependency, exact eight-output copying optimum, physical observation and calibration bridges, and PCP comparative-effectiveness question remain open.

**End of this Director C session artifact. Parent Unary PCP remains Initial External Grounding, OPEN.**

# References and provenance

[E1] P. Arrighi (2019), *An overview of quantum cellular automata*, https://doi.org/10.1007/s11047-019-09762-6 .

[E2] T. Farrelly (2020), *A review of Quantum Cellular Automata*, https://quantum-journal.org/papers/q-2020-11-30-368/ .

[E3] Stanford Encyclopedia of Philosophy, *The Role of Decoherence in Quantum Mechanics*, https://plato.stanford.edu/entries/qm-decoherence/ and *Consistent Histories*, https://plato.stanford.edu/entries/qm-consistent-histories/ .

[E4] S. Surya (2019), *The causal set approach to quantum gravity*, https://doi.org/10.1007/s41114-019-0023-1 ; S. Carlip (2024), *Causal sets and an emerging continuum*, https://doi.org/10.1007/s10714-024-03281-1 .

[E5] *Discrete Approaches to Quantum Gravity in Four Dimensions* (Regge calculus), https://link.springer.com/article/10.12942/lrr-1998-13 .

[E6] Particle Data Group, *Astrophysics & Cosmology* (2025), https://pdg.lbl.gov/2025/reviews/astro-cosmo.html .

[E7] DESI (2026), *New DESI DR2 Lyman-alpha Results Shed Light on Dark Energy*, https://www.desi.lbl.gov/2026/07/30/new-desi-dr2-lyman-alpha-results-shed-light-on-dark-energy/ .

[E8] Clay Mathematics Institute, *The Millennium Prize Problems*, https://www.claymath.org/Millennium%20Problems/ .

[E9] Clay Mathematics Institute (11 September 2026), *Navier-Stokes Announcement*, https://www.claymath.org/news/navier-stokes-announcement/ .

[E10] Clay Mathematics Institute, *Rules*, https://www.claymath.org/millennium-problems/rules/ .

[E11] Abramsky and Brandenburger (2011), *The Sheaf-Theoretic Structure of Non-Locality and Contextuality*, https://ora.ox.ac.uk/objects/uuid%3A6b6946ba-203e-4cac-bf25-22b5e4302ad0 .

[E12] NIST, *Metrological Traceability*, https://www.nist.gov/metrology/metrological-traceability .

[E13] Director B Bell Memory/Sequential QA handoff, uploaded 11 November 2026, internal research provenance only; validates statistical contracts and documents checker-coverage limitations. No physical replication.
