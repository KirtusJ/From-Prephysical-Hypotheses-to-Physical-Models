# Time-Neutral Signed Actions: Refinement, Operational Access, and Compositional Tests

**Status: EXPLICITLY STIPULATED ONTOLOGICAL CANDIDATE FOR FALSIFICATION, not established physics.**  
**Research stage:** Second external grounding, reconciliation, and construction (not a final steelman).  
**Date:** 8 November 2026 (America/Vancouver).  
**Research direction:** Kirtus Justus. **Independent mathematical, computational, and editorial assistance:** ChatGPT (OpenAI).

## 1. Provenance and scope

This note independently stress-tests the finite signed-action graph ansatz alongside contemporaneous positive-kernel and operational-quotient audits. The original conceptual drawing, with signed spectra, a time-unassigned amplitude domain, candidate effective geometry, and a Ricker-type continuum, is retained only as historical conceptual context. No arrow in the drawing is a proven emergence map. In scientific analysis, an algebraic sign is not automatically electric charge or chirality, a graph is not automatically physical space, and an action index is not physical time.

The prior work demonstrates several **conditional mathematical results**: compact, tensor-closed, deterministically coarse-grain-closed doubly nonnegative kernel classes with classical correlated-pair interpretations; rank-one normalization restrictions on universally bounded affine effects over the full PSD cone; supported operational quotients of rank-r normalizers; and nonunique coherent extensions of classical stochastic maps. Their physical correspondence remains separate and unproven. Neither unusual mathematical outliers nor failed specific observation rules are discarded from this comparison.

## 2. Candidate stipulations, explicitly identified

**S1 (combinatorial relation and signed configurations):** A finite undirected graph `G=(V,E)` with configurations `sigma in {+1,-1}^V`, and positive parameters `m`, `kappa`.

**S2 (clock-unassigned action):** `S_G(sigma)=2*kappa*m^2*f_G(sigma)`, where `f_G` counts same-sign edges. This is a restricted antiferromagnetic Ising action. No physical time or causal arrow is supplied.

**S3 (statistical action weights and conjugate phase):** independently choose `beta>0`, `chi>0`, and put `z=exp(-2*beta*kappa*m^2)`, `theta=2*kappa*m^2/chi`. The weight is `p_G(sigma)=z^{f_G(sigma)}/Z_G(z)`, and a sign register receives phases `exp(+i*theta*f_G)` or `exp(-i*theta*f_G)`.

**S4 (imported quantum state and instrument):**

`|Psi_G> = sum_sigma sqrt(p_G(sigma)) |sigma> tensor |phi_{f_G(sigma)}>`, with

`|phi_f> = (exp(i*theta*f)|+> + exp(-i*theta*f)|->)/sqrt(2)`.

The complex Hilbert space, tensor factors, Born probabilities, and optional SWAP measurement are **stipulated quantum ingredients**. This is not yet a quantum reconstruction or physical pretemporal process. A claimed total ontology must derive or otherwise independently justify them.

## 2A. Stronger internal construction: one signed-action operator, without time

The finite action and signed sign register can be expressed in one explicitly **stipulated** operator. Let `alpha=2*kappa*m^2` and

`A_hat = sum_sigma alpha*f_G(sigma) |sigma><sigma| tensor Z_sign`.

The algebraic sign-exchange involution `C=I_config tensor X_sign` obeys `C A_hat C = -A_hat`. If `|Phi_0> = sum_sigma sqrt(p_G(sigma)) |sigma> tensor |+x>`, then the proposed complex state is exactly

`|Psi_G> = exp(i A_hat / chi) |Phi_0>`.

This supplies a single internal mathematical connection between the opposed signed sectors, the graph action and the relative phase rule. It does **not** derive the Hilbert space, complex exponential or physical meaning of action: all are inputs. For a nonempty finite graph its spectrum is contained in `[-alpha |E|, +alpha |E|]`; it is **not** either infinity shown in the historical conceptual diagram.

At the pre-phase state, `E[A_hat]=0`, but `E[A_hat^2]=alpha^2 E[f_G^2]`. At `z=1/2`, this equals `alpha^2*(21/13)` on the triangle and `alpha^2*(112/41)` on the four-cycle. Direct exact matrix calculations confirm the sign-exchange symmetry, moment formulas and unitary norm. This distinguishes the freely stipulated amplitude magnitude `m` from realized *action magnitude*: on a bipartite graph in the zero-weight `z->0` limit, `E[A_hat^2]` vanishes even while `m>0`. On a frustrated triangle the limiting count is nonzero. There is no inferred physical activity or clock in these statements.

## 3. Baseline algebra and held-out contrasts: reproduced exactly

The sign-register marginal is

`rho_sign(G)=1/2 [[1,C_G],[conj(C_G),1]]`, `C_G=Z_G(z exp(2i theta))/Z_G(z)`.

For two independently prepared sign registers, a **supplied** conventional SWAP measurement gives

`p_SWAP(G) = [3+|C_G|^2]/4`.

The action-count polynomials are `Z_C3(z)=2z(3+z^2)`, `Z_C4(z)=2(1+6z^2+z^4)`. At `z=1/2`, `theta=pi/8`, exact independent calculation gives:

| Graph | `|C|^2` | `p_SWAP` |
|---|---:|---:|
| Triangle | `145/169` | `163/169` |
| Four-cycle | `801/1681` | `1461/1681` |

Difference: `27094/284089`. It distinguishes two **specified quantum preparations**, not established foundational physics. The original stipulated parameters are not independent once `beta*chi` is fixed: `-log z=beta*chi*theta`. At this illustrative point, `beta*chi=8 log 2/pi`; choosing `beta` and `chi` independently allows the point, but it remains uncalibrated physically.

## 4. Strong new obstruction: pure conditional states fail closure under vertex marginalization

Consider a triangle, retaining two vertices and tracing out the third. When retained vertex signs are equal, the eliminated spin yields action counts `f=3` and `f=1`. Their conditional weights are

`w3=z^2/(1+z^2)`, `w1=1/(1+z^2)`.

The conditional sign state is the mixed operator

`rho_eq = w3 |phi_3><phi_3| + w1 |phi_1><phi_1|`.

The overlap obeys `|<phi_3|phi_1>|^2=cos^2(2 theta)`. Its exact purity is

`Tr(rho_eq^2) = 1-[2z^2/(1+z^2)^2]sin^2(2 theta)`.

At `z=1/2`, `theta=pi/8`, its purity is exactly `21/25`, with determinant `2/25`. The opposite-sign retained branch has only `f=1` and stays pure.

**Theorem (generic conditional purity criterion):** For strictly positive weights, a mixture of the two conditional pure sign states is rank one if and only if `exp[2i theta(f_1-f_2)]=1`. More generally, after eliminating several vertices, the conditional sign state is pure if and only if all action counts occurring with nonzero conditional probability yield collinear sign states, equivalently their phase differences satisfy the same condition. The proof is that a positive mixture of rank-one projectors has rank one precisely when all contributing vectors span one line.

Consequently, the currently stipulated **pure** graph-configuration/sign ansatz cannot be exactly closed under generic graph marginalization. Merely renormalizing the Ising coupling (e.g. `z -> (1+z^2)/2` for the triangle) does **not** resolve this phase-induced mixture. This is a falsification of a closure claim about this ansatz, **not** a universal disproof of time-neutral ontology.

**Minimal conditional repair:** permit positive density operators (including configuration-conditional mixed sign states) as effective states, and regard vertex elimination as partial trace. This is mathematically consistent but **imports the ordinary quantum state space and partial-trace composition rule**, so no emergence theorem has been gained. A narrower family defined only by pure `|phi_f>` cannot supply these reduced states at generic phase.

## 5. Topology alias: restricted sign readouts versus graph-sensitive probes

For any tree on `n` vertices, `Z_T(z)=2(1+z)^(n-1)`. The complete action-count distribution, `C_T`, and all readings confined to the sign-register marginal are therefore identical for trees with the same number of vertices.

For the four-vertex path and three-leaf star, the action-count distributions agree exactly, but graph connectivity and zero-action vertex-sign balance differ. Under classical graph-configuration probabilities `p_G(sigma)`, the graph-wide invariant `M=sum_i sigma_i` has

`E_star[M^2]-E_path[M^2]=8/27` at `z=1/2`.

The path's endpoint correlation equals `-1/27`, while the star's center–leaf correlation equals `-1/3`. The latter comparison presumes a vertex-labeling convention; the global `M^2` contrast does not.

Thus **graph topology is not invisible to the full stipulated preparation**: it is invisible to one restricted observation family. Accessing `M^2` would require an independently justified graph-configuration readout, not supplied by the existing sign-only SWAP protocol. Do not promote a restricted observability failure into an ontological nonexistence claim.

## 6. Classical-noise equivalence of the sign-register response

Define `|+x>=(|+>+|->)/sqrt(2)` and the ordinary quantum rotation `U_sigma=exp(i theta f_G(sigma) Z)`. Then

`rho_sign(G) = sum_sigma p_G(sigma) U_sigma |+x><+x| U_sigma^dagger`.

The candidate's reduced sign-register statistics therefore have **an exact conventional quantum implementation driven by a classical random variable** `F=f_G(sigma)`. In fact, `C_G(theta)=E[e^{2i theta F}]` is the characteristic function of `F`. At small `theta`,

`|C_G|^2=1-4 theta^2 Var(F)+O(theta^4)`, and

`p_SWAP=1-theta^2 Var(F)+O(theta^4)`.

At `z=1/2`, `Var(F_C3)=48/169` and `Var(F_C4)=1888/1681`. These coefficients were checked by exact differentiation. Thus the held-out sign-SWAP contrast does **not** distinguish the new ontology from classical action-count randomness combined with conventional quantum phase rotations.

A stronger contrast could concern coherent joint access to graph+sign degrees. The pure `|Psi_G><Psi_G|` and the classical-quantum mixture

`omega_G = sum_sigma p_G(sigma) |sigma><sigma| tensor |phi_f><phi_f|`

have identical graph-basis joint probabilities, identical conditional sign states given a graph-basis outcome, and identical reduced sign-register states. They differ on coherent joint effects. The hypothetical rank-one projector onto `|Psi_G>` gives probability `1` in the pure model and `sum_sigma p_G(sigma)^2` in the mixed model. For the triangle at `z=1/2`, this latter probability is exactly `49/338`. Such a joint projector is **not derived as physically accessible**; it is a model-discriminating mathematical measurement.

## 7. Charge/signed-direction reference restriction

If the ± sign register is promoted to **physical charge**, one must state whether the theory imposes charge superselection and which phase references are available.

For the reduced state `rho_sign=1/2[[1,C],[C*,1]]`, independently dephasing each prepared charge register gives `I_2/2`. A SWAP test on two such independently dephased registers yields `p_SWAP=3/4`, irrespective of `C`. At the stipulated triangle point this differs from the coherent `163/169` result.

By contrast, SWAP **commutes** with the total charge `Q_1+Q_2`. Twirling the **joint two-copy state only with respect to global total charge** leaves its SWAP expectation unchanged. Therefore shared/global versus independent/local reference restrictions give different outcomes. Neither choice follows from assigning opposite signs to an algebraic label. This is anticipated by the established literature on phase references and superselection rules (Bartlett, Rudolph, Spekkens, Rev. Mod. Phys. 79, 555, 2007).

The result is not a derivation of electric charge, chirality, or a causal arrow. It is a sharp demand that the candidate specify the operational meaning of its signed distinction before using phase-sensitive predictions.

## 8. Updated outlier and falsification register

| Case | Exact status | Scientific limitation |
|---|---|---|
| Signed action without an assigned clock | Internally coherent mathematical action | No demonstrated physical activity, independent intervention, or temporally causal mechanism |
| Pure graph-conditional phase ansatz | Normalized and supplies exact conditional sign statistics | **Fails closure under generic elimination of graph variables** |
| Mixed conditional-state extension | Mathematical repair under standard quantum partial trace | Imports the entire density-operator/state-update framework |
| Graph-topology aliases | Sign-only action-count readouts identical for same-size trees | Graph-wide signed observables can distinguish some aliases if access exists |
| Classical random-phase implementation | Exactly reproduces all proposed sign-register measurements | No foundational quantum signature in these readouts |
| Local vs global phase reference | Different SWAP results under different superselection restrictions | Physical charge/access rules not established |
| Rank-one normalized unrestricted PSD kernels | Positive normalized generalized measures | No globally informative bounded affine readout on the entire cone |
| Doubly nonnegative kernels | Compact, composable, deterministic-coarse-grain closed, informative | Direct classical correlated-pair explanation |
| DNN 5-cycle not matrix-CP | Classical pair correlations not a conditionally i.i.d. shared-latent form | Not a quantum violation |
| Purely imaginary coherence | Can show composite event effects absent in single-copy real subsets | Some closure/trace cap requirements exclude it |
| Ricker continuum/2+1 geometry | Meaningful effective mathematical targets | Neither effective metric nor continuum generated from present graph action |

**Status of totality conjecture:** A finite conditional signed-action sector exists. A time-neutral global ontology, physical charge, independent instrument rules, classical records, quantum/classical correspondence, calibrated time, emergent 2+1 geometry, Ricker continuum, and gravitational field equations have **not** been derived. This phase constructs and challenges a falsification target; it does not yet authorize a final steelman.

## 9. Prior-art comparison (selected primary sources)

- Fischer and Paganini, *Causal fermion systems: spacetime as the web of correlations of a many-body quantum system*, Classical and Quantum Gravity 43, 045005 (2026), DOI 10.1088/1361-6382/ae2379. A closely related relational ontology argued by the authors; different operator/measure premises.
- Finster and Fischer, *The continuum limit analysis of causal fermion systems for curved spacetimes*, Letters in Mathematical Physics 116, article 137 (9 October 2026), DOI 10.1007/s11005-026-02168-3. Conditional Einstein–Dirac correspondence starting with algebraic QFT on globally hyperbolic spacetime.
- Finster, Grotz and Schiefeneder, *Causal Fermion Systems: A Quantum Space-Time Emerging from an Action Principle*, arXiv:1102.2585 (2011). Signed spectra, action and proposed emergent causality have direct prior art.
- Markopoulou and Smolin, *Quantum theory from quantum gravity*, Phys. Rev. D 70, 124029 (2004), DOI 10.1103/PhysRevD.70.124029. Stipulated graph dynamics/stochasticity in quantum-reconstruction attempt.
- Konopka, Markopoulou and Severini, *Quantum graphity: A model of emergent locality*, Phys. Rev. D 77, 104029 (2008), DOI 10.1103/PhysRevD.77.104029. Graph degrees of freedom and low-dimensional locality in selected model regimes.
- Bartlett, Rudolph and Spekkens, *Reference frames, superselection rules, and quantum information*, Rev. Mod. Phys. 79, 555 (2007), DOI 10.1103/RevModPhys.79.555. Phase-reference/superselection limits.
- Filippov, Gudder, Heinosaari and Leppäjärvi, *Operational restrictions in general probabilistic theories*, Found. Phys. 50, 850 (2020), DOI 10.1007/s10701-020-00352-6. Operational closure under simulation and mixing.
- Boës and Navascués, *Composing decoherence functionals*, Phys. Rev. A 95, 022114 (2017), DOI 10.1103/PhysRevA.95.022114. Strong positivity and compositional prior art.

## 10. Reproducibility

The independent SymPy script `time_neutral_signed_action_exact_stress_verifier_2026-11-08.py` computes the exact graph visibilities, tree alias, sign-sum contrast, conditional purity and determinant, charge twirl/SWAP controls, small-phase variance expansion, pure-versus-classical-quantum projector test, and finite signed-action operator checks. It uses explicit exceptions (checks remain enabled under Python `-O` and `-OO`). Executed successfully in all three modes. The existing candidate's own verifier `signed_action_configuration_exact_verifier_2026-11-08.py` also executed successfully in all three modes. Uploaded contemporaneous scripts were read in supplied source form; their original mounted copies were unavailable to the container runtime, so verbatim execution of those uploaded programs is not claimed. Theorems are proved by the displayed mathematics; a script is a consistency check, not a physical replication or publication-priority certificate.
