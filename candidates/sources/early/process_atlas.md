# Relational Atlases, Source-Specific Detector Constraints, and Contextual Completion

**Session C independent working continuation | 7 November 2026**  
**Program:** From Prephysical Hypotheses to Physical Models  
**Status:** Exact conditional mathematics and a deliberately FICTIONAL ontological candidate intended for falsification. Not a peer-reviewed paper, a physical emergence result, or an experimental measurement.

## 1. Intake and provenance

Read the two latest user-provided pasted audits: `Pasted text(20261107-042637).txt` and `Pasted text (2)(20261107-042650).txt`. The source PDFs and previous F0-F3 working notes were additionally reviewed in context and, where available, from the research Library. The new numerical and exact checks below are written independently and do not purport to replay any previous agent's archived scripts. The scientific October baseline is left unchanged. The separate Wilson finite-part manuscripts remain on their own proof-dependency ledger.

The first audit establishes an eventwise three-coupling log-convexity test under one common detector response and extends it to a stable source mixture of positive eigenmodes. The second establishes degree-three Hausdorff positivity constraints, a restricted adaptive sample lower bound, and a source-specific variance floor. These are internally consistent under the stated assumptions. The eventwise inequalities are necessary, not sufficient, for one physical detector kernel.

## 2. Exact source-specific detector obstruction beyond abstract truncated moments

### Model and theorem

Fix the calibrated baseline positive-mode incidence law

\[U\sim\operatorname{Gamma}(2,2),\qquad X=e^{-2aU},\quad 0<a<1.\]

Its transformed density is

\[f_X(x)=\frac{-\log x}{a^2}x^{1/a-1},\qquad 0<x<1.\]

Put \(y=-\log x\) and \(b=(1-a)/a\). Then \(f_X=e^{-by}y/a^2\), so maximizing over \(y\ge0\) yields

\[\|f_X\|_\infty=\frac{1}{e a(1-a)}.\]

A stationary detector with event-response function \(0\le r_B(x)\le1\) defines a submeasure \(d\nu_B=r_B(x)f_X(x)dx\) and event probability \(p_B=\nu_B((0,1))>0\). Hence its conditional event density is at most \(\|f_X\|_\infty/p_B\). For any real variable with density bounded by \(M\), the elementary symmetric decreasing rearrangement of the squared-distance integral gives \(\operatorname{Var}X\ge1/(12M^2)\): the formal unconstrained minimizer is uniform density \(M\) on an interval of length \(1/M\). Thus

\[\boxed{\operatorname{Var}(X\mid B)\ge \frac{e^2a^2(1-a)^2p_B^2}{12}.}\]

This uses the *known source law*, not merely abstract Hausdorff support. It is a conditional source-specific necessary condition.

### Counterexample

Set \(a=1/2\) and prescribe the event probabilities at couplings \(c=1,3/2,2\):

\[\left(p_1,p_{3/2},p_2\right)=\left(\frac14,\frac9{32},\frac{251}{1000}\right).\]

Normalize by \(c^2\): the positive event's moments of \(X\) are

\[r_B=(1/4,1/8,251/4000),\]

and the complementary event's normalized moments are

\[r_{\bar B}=(3/4,23/72,749/4000).\]

Both satisfy \(r_0\ge r_1\ge r_2\ge0\) and \(r_0r_2-r_1^2\ge0\). Thus their separate degree-two Hausdorff moment tests pass. But the specified registered-event distribution has conditional mean \(1/2\), second moment \(251/1000\), and variance \(1/1000\), strictly below the source-compatible floor

\[e^2/3072\approx0.00240529169887.\]

No coupling-independent response kernel \(R(B\mid u)\in[0,1]\) produces all three prescribed probabilities from the given gamma source. The failure is an **instrument-realizability obstruction**, not quantum contextuality.

The exact underlying measure statement is \(0\le\nu_B\le\nu\) for the known source probability measure \(\nu\). Abstract positivity of low-order moments of \(\nu_B\) and \(\nu-\nu_B\) is not enough to recover this domination.

### Other checks

The supplied 326-preparations-per-coupling Hoeffding guarantee is algebraically consistent: with \(d_M=\sqrt{\log(120)/(2M)}\), the condition \(2d_M<6/35\) first holds at \(M=326\). It is a conservative sufficiency certificate for the specified detector alternative, not an optimal sample complexity. The four-coupling example's normalized conditional moments \((m,q,r)=(1/2,1/3,1/5)\) violate \(mr-q^2\ge0\) by exactly \(-1/90\). Its permitted interval from degree-three Hausdorff positivity is \(2/9\le r\le5/18\). These claims were recomputed independently.

## 3. Inverse-limit ontology: mathematical completion can introduce new objects

The prior F3 working proposal was \(\mathfrak W=\varprojlim_I(\mathfrak M/\!\sim_I)\), identifying a world with a coherent family of observational equivalence classes.

**Counterexample.** Let the original candidate worlds be \(\mathfrak M=\mathbb N_0\), and let observational resolution \(k\) reveal only the residue modulo \(2^k\). Every quotient is \(\mathbb Z/2^k\mathbb Z\), and the compatible family

\[r_k=2^k-1\pmod{2^k}\]

is present in the inverse limit. No nonnegative integer realizes all these residues. The inverse limit is the 2-adic integers \(\mathbb Z_2\), so the completion contains ideal points not represented by the stipulated initial candidate class.

This does not make the completion inconsistent. It means **compatibility in all finite observation windows does not establish realizability by an originally admitted model**. A more daring F3 can deliberately take the completion as primitive, but then it must independently define admissibility, probabilities, dynamics, clock interpretation, and what makes ideal points physical.

## 4. Contextual probability gluing is a third, distinct extension problem

Three contexts AB, BC and AC each assign perfect anticorrelation to binary outcomes A,B,C in \(\{\pm1\}\), and uniform singles. All overlapping one-variable distributions agree. No global deterministic assignment has \(AB=BC=AC=-1\), since the product of the three pair products must be +1. Nor can a global probability distribution be supported on an empty satisfying set.

This is contextual marginal inconsistency in the sense of Abramsky-Brandenburger. It is **not the same problem** as detector-kernel domination or path holonomy. Nor does contextuality imply quantum theory: the Popescu-Rohrlich box has no-signalling marginals and CHSH value 4, whereas complex-Hilbert-space quantum theory obeys the Tsirelson bound \(2\sqrt2\). A genuine quantum derivation requires stricter axioms, such as the informational constraints developed by Chiribella, D'Ariano, and Perinotti, not contextuality alone.

## 5. Fictional candidate F3-P: the Process-Atlas Cosmos

**EXPLICITLY FICTIONAL AND STIPULATED.** The candidate below is designed for Sessions A/B/D to attempt to disprove. It is not a physical theory of the observed universe.

- **P1, primitive existence:** prephysical entities are composable directed relations with an involution reversing formal arrows, not initially a spatial graph or temporal process.
- **P2, protected signs:** every elementary relation carries a signed or phase-like mark; composition retains path products and closed-loop holonomy. The magnitude-only Laplacian is a *derived lossy view*, not the ontological substrate.
- **P3, operational charts:** an observer's access is a finite context of preparations, transformations, detectors, and registered outcomes, with a family of probability assignments consistent on shared calibrated contexts.
- **P4, admissibility:** a proposed global physical model must realize the charts with one internally compatible, source-dominated response architecture. Passing a finite truncated-moment hierarchy is only a local necessary test.
- **P5, completion ontology:** a world is stipulated to be an admissible completion of compatible finite process descriptions, not a particular chosen graph or coordinate basis. Nonrealizable or postquantum completion candidates are to be eliminated by separately specified axioms.
- **P6, quantum selection hypothesis:** the surviving process completions obey causality, local tomography, purification and related operational conditions sufficient to reconstruct complex quantum probabilities. This is a conjectured selection of actual microscopic process models, not established by P1-P5; informational reconstructions already provide important prior art.
- **P7, pregeometry:** locally meaningful separation is the minimal elementary-composition depth in a distinguished marked-process filtration, **if** that filtration is operationally stable. This gives a combinatorial premetric, not physical length or a Lorentzian metric.
- **P8, physical clock and gravity targets:** a nontrivial directed process order plus independently calibrated stable periodic references may produce physical duration. A speculative feedback of energy-bearing process states on allowed transitions may produce effective geometry and gravitational response. No such dynamical law or continuum limit is derived here.

**Steelman:** The same deeper category of relations could present three different stable defects: nontrivial loop holonomy (gauge structure), inability to globally glue classical context outcomes (a candidate sign of nonclassicality), and restricted composability/transition cost (candidate locality and causal accessibility). Their mathematics is different, so a deeper unifying physical law is a conjecture, not a consequence of their formal similarity.

**Distinctive risk:** a completed atlas may be too large (2-adic phantom worlds), too small (detector contexts falsely glued), or postquantum (PR-box-type contexts). This is why the admissibility principles, not an arbitrary complexity minimum, are the next theorem target.

## 6. Proposed A/B/C/D handoff

- **A:** Identify the weakest category of marked relations permitting a bona fide noncommutative process calculus without importing Hilbert-space probabilities. State exactly which quantum reconstruction axioms are subsequently imported.
- **B:** Challenge detector compatibility with the source-dominance counterexample. Generalize finite-moment obstructions to a positive kernel completion test under nontrivial prepared-source mixtures.
- **C:** Study the inverse-limit completion's nonrealizable points and characterize which compatibility/positivity axioms give a concrete process model. Build finite holonomy and contextuality examples while avoiding false quantum claims.
- **D:** Formulate the physical preparation/clock/phase-reference contracts required to discriminate an admitted relational atlas from classical, postquantum and graph-equivalent alternatives.

## 7. Selected external references

- Abramsky and Brandenburger, *The Sheaf-Theoretic Structure of Non-Locality and Contextuality*, New Journal of Physics 13 (2011) 113036, doi:10.1088/1367-2630/13/11/113036.
- Chiribella, D'Ariano and Perinotti, *Informational derivation of quantum theory*, Physical Review A 84 (2011) 012311, doi:10.1103/PhysRevA.84.012311.
- Popescu and Rohrlich, *Quantum nonlocality as an axiom*, Foundations of Physics 24 (1994) 379-385.
- Coecke and Kissinger, *Picturing Quantum Processes*, Oxford University Press (2017), categorical process theory.
- Surya, *The causal set approach to quantum gravity*, Living Reviews in Relativity 22 (2019) 5, doi:10.1007/s41114-019-0023-1.
- Hawkins, Markopoulou and Sahlmann, *Evolution in quantum causal histories*, Classical and Quantum Gravity 20 (2003) 3839, doi:10.1088/0264-9381/20/16/320.

No independent physical correspondence, publication novelty or peer-review result is claimed. This is a working wildcard research packet.

## 8. A first concrete forward model retaining the signed loop data

Instead of immediately passing to F0's magnitude-only Laplacian, use the signed magnetic adjacency matrix \(A_\sigma\) and form a convergent weighted path sum

\[G(z)=(I-zA_\sigma)^{-1}=\sum_{r=0}^\infty z^rA_\sigma^r,\qquad |z|<1/\rho(A_\sigma).\]

This is a **fictional candidate response observable**, though its matrix identity is standard and exact. It is not a unitary time propagator or a measurement probability without an additional normalized instrument contract. Products of edge signs weight each path; closed paths retain signed holonomy.

For two triangles with identical magnitude-only graph Laplacians, one with all positive signs and one with a single negative edge, choose \(z=1/4\). Their resolvents are, exactly,

\[G_+=\begin{pmatrix}6/5&2/5&2/5\\2/5&6/5&2/5\\2/5&2/5&6/5\end{pmatrix},\quad G_-=\begin{pmatrix}10/9&2/9&-2/9\\2/9&10/9&2/9\\-2/9&2/9&10/9\end{pmatrix}.\]

The raw squared amplitude for site 0 to site 1 is \(4/25\) versus \(4/81\), a difference \(224/2025\). If an independently characterized instrument produces output probabilities proportional to squared column amplitudes (e.g. by uniformly attenuating a nonunitary filter and conditioning on success), the conditional probability for the output 1 is \(1/11\) versus \(1/27\). All values are verified exactly with rational arithmetic by the independent script.

This is a useful *forward target* for A/B: a process-level signed input can preserve loop information in an interference-sensitive response that the magnitude-only Laplacian provably erased. Its physical interpretation, detector realization, complex-phase extension, clock and connection to fundamental chirality remain unestablished.
