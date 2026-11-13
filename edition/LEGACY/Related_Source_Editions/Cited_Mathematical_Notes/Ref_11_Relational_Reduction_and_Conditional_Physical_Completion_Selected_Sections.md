# Relational Reduction and Conditional Physical Completion

## Interference, records, operational composition, and cosmological identification

**Kirtus Justus**  
Port Coquitlam, British Columbia, Canada  
**9 November 2026**

Mathematical and computational assistance: ChatGPT (OpenAI).

### Selected scientific sections

This edited textual edition retains the mathematical statements, arguments, hypotheses, and physical limitations of Sections 1–10. The original section and equation numbering is retained. A separately labelled categorical clarification, dated 10 November 2026, follows Section 2.

## 1. Problem and scope

A total ontology would require an independently justified account of physical states, effects, independent preparations, temporal calibration, energy, spatial metric, field content, gravity, and empirical predictions. The finite relational proposal considered here supplies none of those elements. Its mathematical contribution is a canonical normalization inside a stipulated homomorphism-equivalence class. It is therefore a conditional mathematical comparator, rather than a unique foundation.

Known relational theorems, stipulated physical trials, and consequences proved from those trials must be distinguished. All formal label sets in the core construction are mathematical bookkeeping, rather than physical points, moments, particles, or a preselected causal network.

The stronger physical questions are whether a rule selects quantum interference and noncommuting measurements, stable classical records and motion, a Lorentzian metric and field equations, or one mechanism predicting both cosmic expansion and gravitational clustering. Each such conclusion requires its own derivation and observational interpretation. The additional amplitude-and-record trial below makes those dependencies explicit.

## 2. Finite relational core: exact mathematical content

Fix a finite relational signature \(L\) of positive arities and the category of nonempty finite \(L\)-structures with positive-relation-preserving homomorphisms. Define

\[
T_B(A)=\mathbf 1\{\operatorname{Hom}(B,A)\ne\varnothing\},
\qquad
A\sim_{\mathrm{hom}}C\iff A\to C\text{ and }C\to A. \tag{2.1}
\]

Here \(B\) ranges over finite structures in the same language. Taking \(B=A\) and \(B=C\) proves that all the tests \(T_B\) together identify the homomorphism-equivalence class, rather than an isomorphism class. In the loopless graph language, \(K_2\) and \(K_3\) both satisfy the model inputs but are inequivalent: the probe \(B=K_3\) succeeds on \(K_3\) and fails on \(K_2\). The finite-core theorem therefore does not select a unique structure.

**Theorem 1 — Finite core.** Every nonempty finite \(L\)-structure \(A\) has a core unique up to isomorphism, with \(A\sim_{\mathrm{hom}}\operatorname{core}(A)\). All tests \(T_B\) are preserved. The map \([A]\mapsto[\operatorname{core}(A)]\) normalizes a specified class, but does not select \(A\) or the signature. This is established finite constraint-satisfaction mathematics [1–3].

*Proof sketch.* Choose an endomorphism of least image size. Its restriction to its image is bijective, so a suitable power is a retraction onto an induced substructure. An endomorphism of that retract with smaller image would contradict minimality. Two finite cores with homomorphisms both ways are isomorphic, since the resulting endomorphisms are automorphisms. Probe preservation follows by postcomposition.

Write \(Q_L\) for the thin poset of homomorphism-equivalence classes. Its meet is induced by categorical product and its join by disjoint union:

\[
[A]\wedge[C]=[A\times C],\qquad
[A]\vee[C]=[A\sqcup C]. \tag{2.2}
\]

Diagonal and projection maps, together with inclusion and folding maps, give
\([A^{\times k}]=[A]=[A^{\sqcup k}]\) for every \(k\ge1\). This idempotence removes copy number from every quotient-invariant statistic. In contrast,

\[
|\operatorname{Hom}(B,A^{\times k})|=|\operatorname{Hom}(B,A)|^k,
\qquad
|\operatorname{Hom}(B,A^{\sqcup k})|
=k^{c(B)}|\operatorname{Hom}(B,A)|, \tag{2.3}
\]

where \(c(B)\) counts Gaifman-connected components. Counts of zero or one can remain unchanged; not every particular count detects duplication.

**Proposition 1 — Operational factorization criterion.** For a surjective quotient map \(q:P\to Q\) and a statistic \(o:P\to Y\), a well-defined \(\bar o:Q\to Y\) with \(o=\bar o\circ q\) exists if and only if \(o\) is constant on every fiber of \(q\).

*Proof.* Necessity follows by evaluating at two representatives of the same quotient element. For sufficiency define \(\bar o(q(p))=o(p)\); fiber constancy makes the definition independent of the representative.

The counting function \(|\operatorname{Hom}(K_1,-)|\) fails this criterion on \(K_2\) and \(K_2\sqcup K_2\). Arbitrary single-vertex deletion also fails to descend: deleting from the first graph leaves no edge, whereas deleting from the second leaves an edge. The graphs \(P_5\) and \(K_{1,4}\) both have core \(K_2\), but their \(P_3\)-homomorphism counts are 14 and 20. The equivalence is complete only relative to the questions in (2.1); changing the observation language changes the mathematical problem.

### Added categorical clarification — 10 November 2026

In the full category just specified, the singleton \(E\) with every relation empty is **weakly initial**, not initial. Indeed, every function \(E\to A\) is a homomorphism, so
\(|\operatorname{Hom}(E,A)|=|A|\), which need not equal one. There is no initial object: for the full two-point structure \(F_2\), every map \(A\to F_2\) is a homomorphism, giving \(2^{|A|}\ge2\) such maps. The full singleton is terminal. In the thin homomorphism preorder, \(E\) represents a least element because parallel arrows are identified. These distinctions do not affect the finite-core theorem [15, §8].

## 3. Composition and process-selection obstructions

The quotient \(Q_L\) is thin, so every endomorphism is the identity. Nonidentity automorphisms of the original structures, such as exchanging the endpoints of \(K_2\), have been removed. Nontrivial physical dynamics cannot therefore arise solely as functorial images of endomorphisms in this thin quotient. A category retaining additional processes would require additional structure.

**Theorem 2 — Conditional finite operational rank collapse.** Suppose each class \(x\in Q_L\) is assigned a finite-dimensional real state span \(V_x\) of rank \(r(x)\ge1\). Assume normalized preparations span \(V_x\), local effects separate it, quotient-identical objects have operationally equivalent state/effect systems, and independently prepared products with factorizing product effects are admitted in the object assigned to \(x\wedge y\). Then

\[
r(x\wedge y)\ge r(x)r(y),\qquad r(x)=1\text{ for every }x. \tag{3.1}
\]

*Proof.* Choose independent normalized preparations and local effects with a nonsingular evaluation matrix \(E\) of size \(r(x)\); finite-dimensional separation permits this. Do the same for \(y\), obtaining \(F\). Product evaluations give \(E\otimes F\), a nonsingular matrix of size \(r(x)r(y)\). The composite therefore has at least that rank. Since \(x\wedge x=x\), one obtains \(r(x)\ge r(x)^2\), forcing a positive finite integer rank to be one.

The result requires independent preparations and factorizing product effects, which are not derived from the relational core. It requires neither complex quantum mechanics nor full local tomography of arbitrary composites. For example, the two classical full-support states \(\omega_0=(2/5,3/5)\) and \(\omega_1=(3/5,2/5)\) give a preparation matrix \(W\) with determinant \(-1/5\), while \(\det(W\otimes W)=1/625\). Their independent products span four directions although neither local state is perfectly distinguishable from the other in one use.

A stronger conditional result holds if the entire cartesian meet category is represented by a strong monoidal functor into Hilbert spaces with bounded linear maps, preserving terminal/deletion and diagonal/copy maps. Every nonzero output is then one-dimensional, even if infinite-dimensional outputs were initially allowed. The structure gives an invertible \(\delta:H\to H\otimes H\) and a counit \(\epsilon:H\to\mathbb C\) with \((\epsilon\otimes I)\delta=I\). If \(\dim H>1\), \(\epsilon\otimes I\) has nontrivial kernel, contradicting invertibility. This conclusion does not follow from an object-only isomorphism \(H\simeq H\otimes H\), which is possible for separable infinite-dimensional \(H\) [4,5].

## 4. A deliberately stipulated amplitude-and-record completion

A finite relational core selects neither an amplitude algebra nor a probability law. The following trial is therefore separate from Theorem 1.

- **H1 — Alternative labels.** Two distinguishable formal alternatives are represented by an orthonormal basis \(|0\rangle,|1\rangle\) of \(\mathbb C^2\). They are not asserted to be fundamental space points, slit positions, or moments.
- **H2 — Amplitude and readout law.** Preparations are normalized complex vectors or density operators; allowed effects are specified positive operators; probabilities obey the ordinary trace/Born rule. Reversible operations may include the Hadamard transformation and a relative phase transformation. These are substantial quantum assumptions.
- **H3 — Records.** A normalized environmental state \(|e_j\rangle\) can be correlated with each alternative. When \(N\) identical fragments are stipulated independent conditional on the alternative, their joint branch state is \(|e_j\rangle^{\otimes N}\).
- **H4 — Macroscopic interpretation.** Stable quasi-classical records and approximate trajectories require additional dynamical assumptions. A physical clock, Hamiltonian, locality, and metric have not been derived.

H1–H3 make exact toy experiments calculable. Their quantum and decoherence ingredients have established prior literature [7,8]; the calculations do not independently establish a prephysical origin for those ingredients.

## 5. Quantum interference: exact two-output calculation

Start with

\[
|\Psi_{SE}\rangle=
\frac{|0\rangle|e_0\rangle+e^{i\phi}|1\rangle|e_1\rangle}{\sqrt2},
\qquad \langle e_j|e_j\rangle=1. \tag{5.1}
\]

Apply \(H=\frac1{\sqrt2}\begin{pmatrix}1&1\\1&-1\end{pmatrix}\) to the first factor, then measure effects \(|0\rangle\langle0|\) and \(|1\rangle\langle1|\). Put \(\gamma=\langle e_0|e_1\rangle\).

**Proposition 2 — Conditional two-output interference.** Under H1–H3,

\[
p_0=\frac{1+\operatorname{Re}(e^{i\phi}\gamma)}2,
\qquad p_1=1-p_0. \tag{5.2}
\]

If \(|e_0\rangle=|e_1\rangle\), the probabilities are \((\cos^2(\phi/2),\sin^2(\phi/2))\). If the record states are orthogonal, the probabilities are \((1/2,1/2)\) for every \(\phi\).

*Proof.* The detector-0 component is \((|e_0\rangle+e^{i\phi}|e_1\rangle)/2\); its squared norm is \((2+2\operatorname{Re}(e^{i\phi}\gamma))/4\). Detector 1 uses the difference.

The formula shows how the stipulated amplitude rule differs from adding classical probabilities. The complex Hilbert space, Hadamard operation, environmental states, and Born rule were specified before the calculation. Thus (5.2) does not derive quantum mechanics from finite cores. An observable phase setting and its calibration are further physical inputs.

## 6. Uncertainty is a consequence of an imported algebra

For a conventional two-level quantum system, let

\[
Z=\begin{pmatrix}1&0\\0&-1\end{pmatrix},\quad
X=\begin{pmatrix}0&1\\1&0\end{pmatrix},\quad
Y=\begin{pmatrix}0&-i\\i&0\end{pmatrix}. \tag{6.1}
\]

Their commutator is \([Z,X]=2iY\), and Robertson's inequality gives
\(\Delta Z\,\Delta X\ge|\langle Y\rangle|\). In the state
\(|+y\rangle=(|0\rangle+i|1\rangle)/\sqrt2\), one has
\(\langle Z\rangle=\langle X\rangle=0\), \(\langle Y\rangle=1\), and
\(\Delta Z=\Delta X=1\), so equality holds.

The \(Z\)-up state instead gives a certain \(Z\) result and equal probabilities for the two \(X\) outcomes. The two measurements are incompatible, rather than examples of classical imprecision. The Pauli algebra, complex phase, Born probabilities, and observed outcomes have not been selected by the finite-core assumptions.

## 7. Independent records and a controlled quasi-classical limit

Strengthen H3 to \(N\) conditionally independent fragments with the same real overlap \(\gamma\in[0,1]\). Their branch-state overlap is \(\gamma^N\), and

\[
p_0(N,\phi)=\frac{1+\gamma^N\cos\phi}{2},
\qquad p_1(N,\phi)=1-p_0(N,\phi). \tag{7.1}
\]

At zero phase, define \(V_N=2p_0(N,0)-1\). For positive integers \(N\),

\[
V_N=V_1^N=\gamma^N. \tag{7.2}
\]

If \(0\le\gamma<1\), then \(V_N\to0\). At \(\gamma=1/2\), the zero-phase probabilities are \(p_0(1)=3/4\), \(p_0(2)=5/8\), \(p_0(4)=17/32\), and \(p_0(8)=257/512\). These are exact predictions of the stipulated toy model. Violating the equality after controlling record independence and detector error refutes that composition law.

Suppression of reduced-state off-diagonal entries does not by itself imply unique experienced outcomes, a classical trajectory, spatial localization, a preferred time coordinate, or a derivation of macroscopic ontology. Classical phase-space dynamics generally requires stable pointer observables, dynamical laws, and narrow-state approximations [7,8]. For a conventional Hamiltonian \(H=p^2/(2m)+V(x)\) and a supplied physical clock, Ehrenfest identities give

\[
\frac{d\langle x\rangle}{dt}=\frac{\langle p\rangle}{m},
\qquad
\frac{d\langle p\rangle}{dt}=-\langle V'(x)\rangle. \tag{7.3}
\]

Newton-like motion follows only when \(\langle V'(x)\rangle\approx V'(\langle x\rangle)\) in a controlled narrow-state regime. The quantities \(x,p,t,m,H\) are already physical inputs; record multiplication and core reduction do not generate them.

## 8. Geometric reconstruction: a correlation-to-distance counterexample

Positive semidefiniteness alone does not justify defining distance by inverse correlation strength.

**Proposition 3 — Correlations need not yield logarithmic distances.** The matrix

\[
R=\begin{pmatrix}
1&4/5&7/25\\
4/5&1&4/5\\
7/25&4/5&1
\end{pmatrix} \tag{8.1}
\]

is positive semidefinite, has unit diagonal and positive off-diagonal entries, but \(d_{ij}=-\log R_{ij}\) violates the triangle inequality.

*Proof.* Its eigenvalues are \(0,18/25,57/25\). Moreover,

\[
d_{13}=\log(25/7),\qquad d_{12}+d_{23}=2\log(5/4). \tag{8.2}
\]

Since \(25/7>25/16\), the first quantity is larger than the second.

**Proposition 4 — Gram-distance positive control.** If \(R\) is a real positive-semidefinite matrix with unit diagonal, then

\[
\widetilde d_{ij}=\sqrt{2(1-R_{ij})}
\]

is a Euclidean pseudometric. It is a metric when its associated Gram vectors are distinct.

*Proof.* Write \(R_{ij}=\langle v_i,v_j\rangle\) for unit vectors. Then \(\widetilde d_{ij}=\|v_i-v_j\|_2\), so the norm gives nonnegativity, symmetry, and the triangle inequality. Distinct vectors give identity of indiscernibles.

The transform from correlation to distance matters. Even a valid Euclidean metric does not establish Lorentzian signature, local causal cones, length units, curvature, dynamics, or a physical matter sector. Those require further derivations.

## 9. Cosmological tests: expansion and structure growth

The relational construction supplies no action, energy-momentum tensor, physical clock, sound horizon, or metric perturbation equations. It therefore predicts no cosmic expansion history \(H(z)\), \(S_8\), gravitational lensing potential, dark-matter abundance, or vacuum energy.

A future physical completion producing effective FLRW geometry and a material sector would need to calculate background expansion and structure growth from the same parameters. A conventional effective description may write

\[
\frac{H(a)^2}{H_0^2}
=\Omega_r a^{-4}+\Omega_m a^{-3}+\Omega_k a^{-2}+\Omega_{\mathrm{de}}f(a), \tag{9.1}
\]

and linear subhorizon growth in a specified modified-Poisson parametrization may obey

\[
D''(a)+\left(\frac3a+\frac{H'(a)}{H(a)}\right)D'(a)
-\frac{3\Omega_mH_0^2}{2a^5H(a)^2}\mu(a,k)D(a)=0. \tag{9.2}
\]

The functions \(f(a)\) and \(\mu(a,k)\), initial conditions, matter content, and calibration are not determined by the relational model. These equations specify tests for a physical completion. Independently fitting \(f\) and \(\mu\) would not establish a common microscopic explanation.

The published Planck base-\(\Lambda\)CDM inference quoted for comparison is \(H_0\simeq67.4\pm0.5\ \mathrm{km\,s^{-1}\,Mpc^{-1}}\) [9]. The cited SH0ES distance-ladder analysis gives \(73.04\pm1.04\) in the same units [10]. Their calibrations and model assumptions differ. The cited June 2026 review of \(S_8\) discusses different consistency judgments for DES Y6 and KiDS Legacy against a combined CMB comparison [11]. The cited November 2026 review discusses degeneracy among dynamical dark energy, modified gravity, interactions, and systematics, with DESI BAO alone broadly consistent with flat \(\Lambda\)CDM [12]. These are dated literature comparisons, rather than observations made by the relational model.

A cosmological explanation would require parameter-constrained predictions for CMB, BAO, distance-ladder, supernova, weak-lensing, clustering, and local-gravity observations, including their covariance and controlled systematics. The amplitude-and-record trial provides none of these predictions.

## 10. Falsification questions, alternatives, and conclusions

| Claim or test | Mathematical basis or assumptions | Conclusion |
|---|---|---|
| Finite relational cores and homomorphism quotient | Established finite-structure theorem | A conditional normalization within a specified class |
| Quantum amplitudes follow from core reduction | No derivation supplied | Not established |
| Interference formula (5.2) | Exact under H1–H3 | A consequence of stipulated quantum mathematics |
| Visibility power law (7.2) | Exact under conditionally independent identical records | A falsifiable conditional composition law |
| Uncertainty and records fully explain measurement outcomes | No derivation supplied | Not established |
| Classical trajectories follow from the core alone | No dynamics or narrow-state limit supplied | Not established |
| Positive correlations always give a logarithmic metric | Exact counterexample in Section 8 | False for the stated transform |
| One common cosmological solution follows from the core | No dynamics or data fit supplied | Not established |
| Finite operational rank with copy-preserving quotient composition | The assumptions of Theorem 2 | Only rank one is possible |

A comparison space may include classical stochastic models, real and complex quantum theories, generalized probabilistic theories, contextual sheaves, process algebras, and infinite or nonrelational candidates. They must be assessed against the same justified experiments. Neither familiar terminology nor unfamiliar structure supplies evidence by itself.

The finite relational core is a useful mathematical comparator, but these results do not establish it as a standalone foundation of a total ontology. The amplitude-and-record construction is an explicit hypothetical physical completion. Its mathematical consequences remain conditional on its additional assumptions. A distinct relational category, or a nonrelational proposal, may require different tests and derivations.

## References

1. P. Hell and J. Nešetřil, “The core of a graph,” *Discrete Mathematics* **109** (1992), 117–126. https://doi.org/10.1016/0012-365X(92)90282-K.
2. P. Hell and J. Nešetřil, *Graphs and Homomorphisms*, Oxford University Press (2004), Chapter 3. https://doi.org/10.1093/acprof:oso/9780198528173.003.0003.
3. M. Bodirsky, “Cores of Countably Categorical Structures,” *Logical Methods in Computer Science* **3** (2007). https://arxiv.org/abs/cs/0612069.
4. S. Abramsky, “No-Cloning in Categorical Quantum Mechanics” (2009). https://arxiv.org/abs/0910.2401.
5. C. Heunen and J. Vicary, *Categories for Quantum Theory: An Introduction*, Oxford University Press (2019), Chapter 4. https://doi.org/10.1093/oso/9780198739623.003.0004.
6. H. Barnum and A. Wilce, “Information Processing in Convex Operational Theories,” *Electronic Notes in Theoretical Computer Science* **270** (2011), 3–15. https://doi.org/10.1016/j.entcs.2011.01.002.
7. W. H. Zurek, “Decoherence, einselection, and the quantum origins of the classical,” *Reviews of Modern Physics* **75** (2003), 715. https://doi.org/10.1103/RevModPhys.75.715.
8. M. Gell-Mann and J. B. Hartle, “Quantum Mechanics in the Light of Quantum Cosmology” (2018). https://arxiv.org/abs/1803.04605.
9. Planck Collaboration, “Planck 2018 results. VI. Cosmological parameters,” *Astronomy & Astrophysics* **641** (2020), A6. https://doi.org/10.1051/0004-6361/201833910.
10. A. G. Riess et al., “A Comprehensive Measurement of the Local Value of the Hubble Constant,” *Astrophysical Journal Letters* **934** (2022), L7. https://doi.org/10.3847/2041-8213/ac5c5b.
11. I. Pantos and L. Perivolaropoulos, “Status of the S8 tension: A 2026 review of probe discrepancies,” *Physics of the Dark Universe* **52** (2026), 102286. https://doi.org/10.1016/j.dark.2026.102286.
12. X. Zhang, “Diagnosing dark energy in the post-DESI era: From effective dynamics to multi-probe consistency tests,” *Science China Physics, Mechanics & Astronomy* **69** (2026), 120401. https://doi.org/10.1007/s11433-026-3116-4.
13. L. Hardy, “Reformulating and Reconstructing Quantum Theory” (2011). https://arxiv.org/abs/1104.2066.
14. G. Chiribella, G. M. D’Ariano, and P. Perinotti, “Informational derivation of quantum theory,” *Physical Review A* **84** (2011), 012311. https://doi.org/10.1103/PhysRevA.84.012311.
15. K. Justus, with ChatGPT (OpenAI) assistance, *Operational Identification of Records, Controls, and Continuous-Time Dynamics*, 10 November 2026, Section 8, “Initial and terminal objects.” The categorical clarification above reproduces its argument.
