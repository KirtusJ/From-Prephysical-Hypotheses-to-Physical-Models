# Foundations of R: Methodology & Glossary

**Document series:** `FR-MG`  
**Edition:** `1.2`  
**Document identifier:** `FR-MG-ED-1.2`  
**Effective date:** 18 October 2026  
**Editorial status:** Consolidated, provisional reference for the research programme  
**Scientific status:** No scientific claim is upgraded merely by this edition  
**Research release covered through:** `FR-RR-v6.2` as represented by the currently available release chain  
**Supersedes editorially:** The terminology and method role previously carried by the file named `Foundations_of_R_v1.5_Glossary_and_Methodology_FINAL.md`; it does not supersede or renumber any research release.

> **Governing rule:** A formal definition, a theorem under stated hypotheses, a numerical result in a specified model, and a claim about physical Reality are different kinds of statement. Evidence does not flow automatically from one kind to another.

---

## Executive orientation

This document stabilizes the vocabulary, claim ledger, release identifiers, and verification rules used by *Foundations of R*. It is intended to reduce ambiguity before new research proceeds. It does not declare that R is a complete theory, that its ontology is established, or that every inherited computation has been re-certified.

The document records the current mathematical status, evidence boundary, and unresolved physical bridges of the Foundations of R programme through research release `FR-RR-v6.2`. The identifier taxonomy in Section 1 defines the separate roles of research releases, document editions, computational runs, audits, tests, and distribution packages. A verified computation is not by itself a theorem, and a theorem under external hypotheses is not by itself a result about R.

The current scientific posture is:

- The finite-source retention results are mathematically well-typed and reproducible in their declared finite settings.
- The endpoint pair \(M(-\infty)=-1\), \(M(+\infty)=+1\) determines the signed endpoint sum to be zero, but does not determine an interior profile, a source distribution, a target task, a physical channel, or a preferred readout.
- The modular edge construction remains a model-specific result under its hypotheses. The R-specific identification of its observable content remains open.
- The T-level structure and the D0-D4 pairing ladder are separate organizing schemes until an explicit relation is adopted and justified.
- The R-specific source, task, admissible observable/readout class, and selection principle have not been independently specified. The correct selection status remains `UNSELECTED`; the endpoint/source/task question is `UNDERDETERMINED` relative to the current assumptions.
- The T2 finite-split modular-spectrum proposal is a candidate mathematical instance. The explicit 180-state source supplied with Packet 3 reproduces the reported 6.8251864297-bit mutual information for both declared readouts; this verifies that finite construction, not a physical interpretation or observable selection for R.
- The reproduced P5′ raw Wilson series and the independent staggered-lattice sweep show finite-size trends compatible with logarithmic growth in the stated models. They do not prove an infinite-volume divergence or determine a continuum Araki relative entropy.

## 0. Document identity, scope, and revision rules

### 0.1 What this document is

`FR-MG-ED-1.2` is an **edition of the Methodology & Glossary document series**. It is a reference and governance document. It establishes preferred terminology, required evidence labels, reproducibility expectations, and the current interpretation of terms used across R research branches.

It is not:

- a new scientific research release;
- a computational run;
- a certification that all prior research claims are true;
- a claim that all source files have been independently read in full;
- an observable-selection decision;
- a proof of the Origin relation or a physical theory of signal loss;
- a substitute for individual claim records.

### 0.2 Scope and coverage

This edition records methodology and evidence status for research releases through `FR-RR-v6.2`, including modular inclusions and convergence, finite-source information retention, endpoint identifiability, and finite-precision measurement. Packet 3 provides additional finite-source and P5′ artifacts. Claims derived from those artifacts are labelled at the level actually checked, with physical mappings left open where the required model inputs are absent.

The source copy of the legacy v1.5 glossary is preserved in `legacy_sources/`. The earlier `Foundations of R - Glossary and Methodology.md` file and two `Proposed Foundations of R v1.2` Word drafts are also preserved as editorial-history artifacts. The v1.2 files explicitly identify themselves as advisory working drafts; the two Word files have matching extracted paragraph text, with the “Typography Corrected” variant changing presentation rather than asserting a new research release. The `FR-MG-ED-1.2` identifier remains scoped to this document series; it is not a claim that legacy draft labels form a monotonic chronology. Statements in the old v1.5 file about “current status” refer to that file’s cutoff and must not override later status ledgers.

### 0.3 Revision principles

1. **No silent upgrade.** A definition or glossary edit does not upgrade a theorem, computation, physical bridge, or selection status.
2. **Stable claim IDs.** A claim keeps its ID while its status, assumptions, proof, and revision history change.
3. **One claim per record.** Break a paragraph that combines several inferential steps into separate linked claims.
4. **Scope first.** State the domain, model, state, algebra, regulator, topology, and source distribution before evaluating a conclusion.
5. **Prefer conditional truth.** If a theorem holds under hypotheses not established for R, mark the mathematical theorem as established under those hypotheses and the R bridge as open.
6. **Corrections are preserved.** Superseded claims remain in a correction ledger with the reason and downstream consequences.
7. **Reproduction is not proof.** Repeating arithmetic supports reproducibility; it does not prove a general theorem or validate the model's physical interpretation.
8. **No narrative selection.** Do not select a definition, observable, state, or loss operator because it yields a preferred Origin story.
9. **No infinite extrapolation from finite grids.** Describe every enumeration by its declared domain. Its exhaustiveness is only with respect to that domain.
10. **No unnamed “version.”** Name the object whose revision is being tracked.

### 0.4 Contributions and provenance

The project maintains a persistent record of supplied contributions and their evidential boundaries. A contribution record identifies the artifact and the work attributable to it; it does not imply endorsement of every claim in the document or grant authorship of external papers.

| Contributor ID | Recorded contribution | Attribution boundary |
|---|---|---|
| `FR-CONTRIB-KIRTUS-JUSTUS` | **Kirtus Justus**: Foundations of R programme materials, model definitions, research questions, source artifacts, and project-level decisions | Project contributions are attributed to Kirtus Justus. This attribution does not settle an open scientific question or imply that cited external authors endorse the programme. |
| `FR-CONTRIB-CLAUDE-CC3` | Cross-check Packet 3: correction records, the explicit 180-state finite source and verifiers, the qubit partition verifier, raw P5′ Wilson data, staggered fixed-x data, scripts, logs, and run records | Attribution attaches to the supplied packet as labelled. It does not authenticate a human identity or imply endorsement of an R-specific physical interpretation. |
| `FR-CONTRIB-LEGACY-V42` | v4.2 reconciliation audit and its typed T–D dependency ledger, short-scale free-Dirac derivation, and prior audit trail | Historical audit contribution preserved as supplied; individual underlying runs retain their own evidence limits. |
| `FR-CONTRIB-CHATGPT-ED12` | Edition 1.2 source verification, numerical recomputation, evidence-status reconciliation, integration of corrections, reproducibility tooling, and publication QA | AI-assisted editorial and verification contribution, not authorship of the underlying research programme or cited scholarship; it does not confer endorsement on open physical claims. |
| `FR-CONTRIB-LITERATURE` | External scholarly sources cited in Section 14 | Each paper’s authorship remains with the cited source. Citation is not a claim that those authors contributed to or endorse Foundations of R. |

The persistent machine-readable register is `contributor_registry.csv`; the stable correction record is `correction_registry.csv`. The raw numeric and source provenance records are preserved in `evidence/packet3/`, and the fine-σ quantized-information sweep is implemented in `audit/fine_sigma_sweep.py` with its output at `audit/outputs/fine_sigma_sweep.json`. Packet 3 is preserved byte-for-byte under `contributions/received/`, while its runnable source/data artifacts are also included in `evidence/packet3/` for convenient verification. The original correction CSV remains preserved unmodified as received.

## 1. Identifier and version taxonomy

### 1.1 The six distinct objects

| Object | Preferred label | What the identifier means | Example |
|---|---|---|---|
| Research programme | `FR` / *Foundations of R* | The ongoing body of proposals, formal models, and research questions | `FR` |
| Scientific research release | `FR-RR-vX.Y` | A scoped release of research artifacts, claims, data, and code | `FR-RR-v6.2` |
| Methodology/glossary document | `FR-MG-ED-X.Y` | An editorial edition of the reference document | `FR-MG-ED-1.2` |
| Computational run | `FR-RUN-YYYYMMDD-AREA-NNN` | One execution with fixed input hashes, code, parameters, environment, and outputs | `FR-RUN-20261018-RETENTION-001` |
| Audit or cross-check | `FR-AUD-YYYYMMDD-SCOPE-NNN` | A review of named artifacts and claims, with an explicit verification level | `FR-AUD-20261018-MG-001` |
| Distribution package | `FR-PKG-<release-or-document-id>` | A transport bundle. A package may contain multiple runs, source files, and reports | `FR-PKG-MG-ED-1.2` |

A test suite is a code artifact. A **test run** is an execution of that suite. A **research run** may contain multiple commands, tests, and outputs. An **audit** assesses what the artifacts establish. A **release** versions a managed set of research artifacts and claims. A **package** transports files. A **document edition** versions an editorial reference work. A **research run number does not automatically increment the release number**, and a new glossary edition does not make any research release newer. These objects can link to each other, but none is a synonym for another.

### 1.2 Identifier scope

Identifiers are scoped to artifact series. `Foundations_of_R_v1.5_Glossary_and_Methodology_FINAL.md` is a legacy editorial document, not a research release. `Foundations_of_R_v6.2_Finite_Precision_and_Noisy_Identifiability_Packet.zip` names a research-release/package artifact. Current references use `FR-MG-ED-1.2` for this glossary edition and `FR-RR-v6.2` for the covered research-release chain. Bare numeric labels must not be used to cross-reference different artifact types.

### 1.3 What qualifies as a research release

A research release should declare:

- release ID and scope;
- claim IDs and status changes;
- included source files and baseline files;
- data provenance and transformations;
- verification commands and actual outcomes;
- Python/compiler/library versions where relevant;
- root-relative manifest and hash algorithm;
- known limitations and omitted artifacts;
- previous release(s) preserved and whether they are byte-identical.

A release number alone is not a quality grade. A higher research release number means a later managed artifact set, not necessarily stronger science. Governance-only releases can improve reliability without advancing the mathematical result.

### 1.4 What qualifies as a computational run

A run record is immutable after finalization. It should specify inputs by hash, code by hash or version-controlled commit, parameter values, environment, random seeds, command line, start/end time, exit status, standard output/error, and generated artifacts. Re-running identical code is a new run record even when output files are byte-identical.

A rerun is not independent merely because it was executed twice. Stronger independence may require a separately written implementation, analytic derivation, a different numerical method, or an independently controlled benchmark.

### 1.5 Audit identifiers and cross-checks

An audit must state whether it checked: (a) bytes and manifests, (b) command reproduction, (c) algorithm correctness, (d) the underlying mathematical claim, (e) external-source applicability, and (f) the physical bridge. Passing one audit layer must not be presented as passing all layers.

A cross-check packet that is cited but unavailable in the current artifact set is classified as **reported but not independently inspected**. Do not invent a packet hash, script count, or test result when the packet is not available.

### 1.6 Manifest rules

Manifests in the current chain use paths relative to the **packet root**, even when the manifest file itself lives under `outputs/`. Verify from the package root, not from `outputs/`. A correct root-relative manifest can appear entirely broken when run from the wrong working directory; the verifier should make its root explicit rather than rely on operator intuition.

Do not include interpreter-generated artifacts such as `__pycache__/*.pyc` in a portable source manifest unless the exact interpreter/build environment is intentionally part of the artifact. They are environment-specific, do not substitute for source files, and can make otherwise portable packages unnecessarily brittle. If retained for historical integrity, mark them as build artifacts and exclude them from the portable source-integrity gate in the next clean release.

A reproducible package should be assembled from a clean staging directory, not from a directory contaminated by old outputs, temporary files, or caches. The manifest must exclude itself or use a separately defined detached-signature convention to avoid recursive self-hashing.

---

## 2. Claim typing, evidence, and status

### 2.1 Three axes, plus a separate lifecycle status

Every load-bearing claim should receive at least three classifications:

1. **Claim kind:** what kind of statement is being made.
2. **Evidence level:** what verification supports it.
3. **Domain:** where it is asserted to hold.

Its lifecycle state is recorded separately. These are orthogonal axes. “Theorem” is not an evidence grade; “physical” is not a level of confirmation; “open” is not a mathematical kind.

#### Claim-kind labels

| Kind | Meaning | Minimum record |
|---|---|---|
| Definition | Sets the meaning of a symbol or object | Domain, conventions, assumptions, edge cases |
| Axiom / assumption | Premise adopted for a branch | Motivation, scope, consequences, rejected alternatives |
| Conjecture / hypothesis | Testable or assessable proposed claim | Truth conditions, scope, support, counterexamples, falsifier |
| Lemma / theorem | Mathematical implication | Full hypotheses, proof or exact source, domain of validity |
| Calculation | Exact symbolic or numerical evaluation | Inputs, algorithm, conventions, check, limitations |
| Empirical claim | Claim about the world or data | Data, uncertainty, model, alternatives, falsifier |
| Bridge hypothesis | Mapping from formal mathematics/model to physical meaning | Map, assumptions, predicted consequences, discriminating test |
| Identification | Structural correspondence or analogy | The two structures and a consequence not used to construct the match |
| Prediction | Outcome not yet established | Numeric or qualitative output, uncertainty, decision rule, falsifier |
| Research judgement | Choice of scope, priority, or model route | Criteria and trade-offs; not called a theorem |
| Correction / withdrawal | Replacement or rejection of a previous claim | Former statement, error, reason, dependencies affected |

#### Evidence labels

| Evidence label | Minimum meaning | What it does not mean |
|---|---|---|
| Defined | Object is fixed by convention | Does not establish physical existence or uniqueness |
| Assumed | Result is conditional on declared premises | Does not validate the premises |
| Derived | Conclusion follows from displayed reasoning | Does not enlarge the theorem's domain |
| Source-checked, full text | Primary text examined for the claim at issue | Does not prove the source applies to R |
| Source-checked, record/abstract | Official abstract, metadata, or corrections inspected | Does not substitute for proof-level review when theorem details matter |
| Source-checked, partial | Excerpt or snippet inspected | Not enough to settle a disputed load-bearing claim |
| Symbolically checked | Exact algebra checked by hand or independent symbolic tools | Does not establish a physical bridge |
| Numerically checked | Computation reproduces within a specified tolerance | Does not establish the general claim behind the code |
| Numerically validated in stated regime | Benchmarks, precision, sensitivity, and controls pass for declared model/observable | Does not establish continuum convergence or universality |
| Independently reproduced | A separate run or method matched stated output | Independence level must be described; copying the same script is weak evidence |
| Reported, not reproduced | Output or audit claim is cited but unavailable or not rerun | Must not be reported as verified by the current audit |
| Open / unverified | Verification gate not met | Must not be used as an established premise |
| Withdrawn | Claim is no longer accepted in its previous form | Must not reappear without a new derivation and explicit reinstatement |

#### Domain labels

- **Mathematical:** a formally specified structure, implication, or counterexample.
- **Model-specific:** a result within a specified finite model, regulator, state, boundary condition, or numerical protocol.
- **Physical / empirical:** a claim about the actual world or its adequate physical description.
- **Interpretive / metaphysical:** a statement about what a formal construction means for R as total Reality; requires an explicit bridge and discriminating consequences.

A mathematical theorem and its R-specific interpretation should usually be separate linked claims. Example: the finite-source retention theorem is mathematical; the choice of a particular task as “the information that R must preserve” is an R-model/interpretation claim and remains unspecified.

### 2.2 Lifecycle states: do not collapse them

| State | Definition |
|---|---|
| `ESTABLISHED_UNDER_HYPOTHESES` | The mathematical or computational statement passed its gate within explicit premises and scope |
| `CONDITIONAL` | The result follows only if named assumptions are adopted or proven |
| `CANDIDATE` | A specified route or construction is available but not selected or fully validated |
| `OPEN` | A required proof, source check, calculation, or bridge remains incomplete |
| `UNDERDETERMINED` | More than one inequivalent outcome satisfies the current assumptions; the current assumptions cannot select uniquely |
| `UNSELECTED` | A choice is deliberately not made; this describes decision state, not by itself a theorem of underdetermination |
| `BLOCKED_UNDER_CURRENT_ASSUMPTIONS` | A named goal is impossible under the declared assumptions, typically by a theorem or counterexample |
| `REPORTED_NOT_REPRODUCED` | Evidence is present as a report but has not been independently reconstructed from source artifacts |
| `WITHDRAWN` | The earlier statement was corrected or retracted |
| `DEFERRED_BY_SCOPE` | The programme intentionally parks the item without asserting either truth or falsity |

`UNDERDETERMINED` and `UNSELECTED` are different. An item can be unselected because a choice was never made. It is underdetermined when alternatives demonstrably survive the current premises. An item can be both underdetermined and unselected. `OPEN` is broader than either; `BLOCKED_UNDER_CURRENT_ASSUMPTIONS` is stronger and requires a named obstruction.

### 2.3 Minimum claim record

```yaml
claim_id: FR-CLAIM-<stable-id>
statement: <one proposition>
kind: <definition|assumption|theorem|calculation|bridge|...>
domain: <mathematical|model-specific|physical|interpretive>
level: <T0|T1|T2|D0|...|not-applicable>
lifecycle_state: <one of the states above>
evidence_level: <one of the evidence labels above>
assumptions: []
objects_and_types: <spaces, maps, algebras, states, operators>
conventions: <signs, units, normalization, topology, boundary conditions>
proof_or_source: <URI, theorem/section, proof record>
source_access: <full text|record/abstract|partial|not checked>
computation: <run IDs, commands, data hashes, tolerances>
known_counterexamples: []
falsifier_or_stopping_rule: <explicit>
dependencies: []
changes: []
```

One paragraph may generate several claim records. In particular, do not fuse (a) a finite-dimensional identity, (b) its use in an R model, and (c) a claim about physical Reality.

---

## 3. Mathematical and computational method

### 3.1 Mathematical proof gate

Before a mathematical result is accepted, record:

- object types and domains/codomains;
- whether the object is finite-dimensional, bounded/unbounded, faithful/nonfaithful, cyclic/separating, local/global;
- topology and convergence mode: pointwise, norm, strong, weak, strong-resolvent, trace norm, distributional, or asymptotic;
- state and algebra conventions, including modular sign and state order;
- boundary conditions, normalization, units, and order of limits;
- exact hypotheses of every imported theorem;
- an edge-case or counterexample check whenever the claim involves uniqueness, continuity, injectivity, or limiting behavior.

Do not use “converges” without naming the object, norm/topology, and quantifiers. “For each fixed time” is not “uniformly over a time interval”; strong convergence is not operator-norm convergence; pointwise finite-size agreement is not convergence as the regulator is removed.

### 3.2 Numerical verification gate

A robust numerical record must state the decision the computation informs, the expected control result, the algorithm, precision, conditioning, spectral cutoffs, boundary treatment, and the failure threshold declared before fitting where feasible. Include independent checks by one or more of: a symbolic result, higher precision, separate implementation, exact diagonalization, an analytically soluble model, a transformed coordinate system, or a counterexample control.

For covariance/modular calculations, ordinary double precision can be inadequate when eigenvalues approach 0 or 1 and are passed through logarithms. Report eigenvalue floors, any clipping or regularization, the smallest eigenvalue distance from the singular endpoints, arithmetic precision, and sensitivity across plausible floors. Clipping can change the state and therefore the modular operator; it is not a neutral numerical repair.

A scaling exponent fitted over a short window is evidence for a finite-window trend, not enough by itself to identify a unique limiting spectral type. Fit-range, size, boundary, precision, floor, and regularizer sensitivity must be reported.

### 3.3 Reproducibility and integrity gate

The canonical packet workflow is:

1. start from an explicit release source tree;
2. build in a clean staging directory;
3. generate outputs with bytecode/cache generation disabled unless such artifacts are the object of study;
4. execute documented commands from the stated root;
5. parse every JSON/CSV output strictly;
6. verify every root-relative manifest entry;
7. check any embedded predecessor archive against the separately identified predecessor's byte hash;
8. extract the final ZIP into a clean directory and rerun release checks;
9. report unrun or timed-out commands rather than treating them as successful;
10. produce a final validation record containing actual counts and exit codes.

Hash integrity proves that the bytes match a manifest. It does not prove the code is mathematically correct. Tests show that expected cases behave as encoded. They do not prove that expected cases cover every failure mode.

### 3.4 Generated coverage and “exhaustive” claims

Use “exhaustive” only with an explicit finite domain. For example, the v5.9 stress test exhaustively enumerates its declared finite grid of maps, distributions, tasks, and channel settings. It does not exhaust all finite distributions, all maps on arbitrary source sets, all continuous distributions, or all physical readout models.

Count assertions separately from cases, and cases separately from independent theorems. A thousand parameter points checking the same identity provide breadth and regression protection; they are not a thousand independent proofs.

### 3.5 Adversarial review and stopping rules

For every candidate claim ask:

- Does a known theorem rule out the construction under the exact assumptions used?
- Is a necessary hypothesis actually proved, or only presumed?
- Does another source, task, state, profile, resolution, or readout yield the same observed output?
- Was the parameter, observable class, spectral floor, or fitting interval chosen after observing the desired result?
- Does the result survive an independently chosen observable not used to construct it?
- What observation, computation, or counterexample would weaken or falsify the claim?
- What is the least expensive discriminating test?

Stop a numerical branch when the predeclared decision is answered, the observable is dominated by uncontrolled systematics, or a cheaper test can decide the question. Further computation on an under-specified model may produce detail without reducing uncertainty.

### 3.6 Literature verification gate

For a load-bearing claim, prefer the primary source. Record the exact version, date, theorem/proposition, scope, and access level. Search-result snippets are navigation aids, not a source verification level. If a preprint corrects an earlier version, cite the corrected version and retain the correction note. If a PDF cannot be obtained but the public record or HTML can be read, label precisely what was inspected.

An external theorem may provide a benchmark without applying to R. Transfer requires a matching map of assumptions: algebra, state, embedding, regulator, topology, faithfulness, boundary condition, locality, and observable class as appropriate.

### 3.7 Independence and circularity

A prediction is independent only if its target value was not used to select the principal inputs. If observed \(\Lambda\) is used to infer \(N\), the resulting equation is a consistency relation, not an independent prediction of \(\Lambda\). If an entropy exponent is used to identify a universality class, the same exponent is not independent confirmation of that class. If a covariance floor is tuned to match a target leakage, the result is calibration until tested on a separate observable or held-out regime.

---

## 4. Structural architecture: T-levels and D0-D4 are separate schemes

### 4.1 Two axes, not a single ladder

The programme uses two different organizational systems:

- **T-levels** mark the introduction of richer kinds of mathematical structure.
- **D0-D4** describe proposed pairings or modular/geometric relations.

Same-number labels do not establish a one-to-one mapping. The T-D relationship can be proposed as refinement, implication/inclusion, or parallel description, but any adopted option must be declared. Until then, use the schemes independently and do not cite a T/D alignment as evidence of a theorem.

### 4.2 T0: total-state and capacity question

T0 is the proposed bare total state before a subsystem decomposition, operational clock, or generator is introduced. If the total Hilbert space is finite-dimensional, the project sometimes writes

\[
N=\ln \dim \mathcal H_{\mathrm{tot}}.
\]

This quantity is in natural-log units (nats). Bits would use \(\log_2\). Finite dimensionality, the value of \(N\), and a physical interpretation as horizon entropy are separate claims.

The expression \(H_{\mathrm{tot}}|\Psi\rangle=0\) is not well-typed at a level expressly defined to contain no operator or generator. Move the equation to the first level with a declared constraint operator, or define a different constraint object and state its type. A constraint operator is not automatically a time-evolution generator.

### 4.3 T1: conjugation, state families, and phase

T1 introduces candidate conjugation structure, state families, and possible invariant phase information. A theorem about continuous reversible mixing under a quadratic norm is conditional on its exact map class and assumptions. It does not by itself select complex quantum theory over real or quaternionic alternatives, establish local tomography, or identify a physical phase with frequency or time.

A coordinate phase, a gauge-invariant loop phase, physical frequency, and wavelength are distinct objects. A three-state Bargmann invariant can represent a relational phase around a specified loop; it does not imply that an acyclic graph cannot carry amplitudes or coordinate phases.

### 4.4 T2: subsystem, complement, state, and modular objects

T2 introduces a subsystem algebra \(\mathcal M\), a suitable state, and, under the relevant hypotheses, modular objects such as \(J\) and \(\Delta\). Fix the sign convention when stating the modular KMS condition. For \(\sigma_t^\omega(A)=\Delta_\omega^{it}A\Delta_\omega^{-it}\), the form \(\omega(A\sigma_{i\beta}^\omega(B))=\omega(BA)\) uses \(\beta=-1\) for analytic \(A,B\); \(\beta=+1\) corresponds to the reversed flow \(t\mapsto\sigma_{-t}^\omega\). A faithful state is KMS for its own modular flow under the matching convention. This does not by itself establish physical thermodynamic temperature: that requires a justified identification of modular flow with physical time evolution, including units and proportionality conventions.

The finite-split Schmidt-spectrum construction described in Section 8 is a candidate mathematical T2 instance. It does not constitute an R ontology or observable-selection decision until a source ensemble, task, readout class, and independent connection to R are justified.

### 4.5 D0-D4 pairing ladder

| Label | Proposed role | Limit on inference |
|---|---|---|
| D0: conjugation pairing | Pair an amplitude/state component with its conjugate | Does not alone select the scalar field or local tomography |
| D1: spectral pairing | Pair spectral values such as \(+E\) and \(-E\) under a declared symmetry/constraint | Requires a generator and spectral hypotheses |
| D2: Tomita pairing | Relate an algebra and commutant through modular conjugation and modular operator | Requires a suitable algebra-state pair and standardness |
| D3: half-sided modular inclusion | One-sided modular invariance of a specified inclusion with associated positive translation structure | Not an exact finite-dimensional standard-inclusion result; approximations need their own metric and limit |
| D4: geometric pairing/reflection | Relate modular structure to spacetime symmetry, reflection, or CPT-type relations | Requires a geometric modular-action bridge and state selection |

### 4.6 Typed T–D dependency ledger

The T-level and D-level systems remain separate organizational schemes. The following dependency table records necessary added structure and valid conditional routes; it does not derive the D-levels from the T-level labels alone.

| D-level item | T-level relationship | Required input or hypothesis | Supported conclusion and limit |
|---|---|---|---|
| D0: antiunitary/conjugation `C` | Added structure associated with the T1 stage; not forced by a norm alone | Complex inner product plus separately declared antiunitary involution | Inner-product geometry and a quadratic (`p=2`) norm do not select a unique conjugation; alternatives remain. |
| D1: symmetric modular generator | Available only with the operator-bearing modular structure associated with T2 | Standard modular pair and `J Δ J = Δ⁻¹` | Under modular-theory hypotheses, the `log Δ` spectrum is symmetric about zero. This does not uniquely provide a physical Hamiltonian. |
| D2: standard pair | Requires suitable T2 algebra/state data, not merely the T2 label | Algebra, faithful normal state/vector, cyclic and separating conditions | These operator-bearing data are not furnished by a level name alone. |
| D3: proper half-sided modular inclusion (HSMI) | Extra structure beyond T2 | `N ⊊ M`, a common standard vector, and one-sided modular invariance | T2 does not imply D3. The exact common-standard-vector/proper-inclusion formulation is obstructed in finite dimension; a finite diagnostic is not the algebraic property. |
| D4: geometric modular action | Requires a geometric region family and action beyond a bare D3 inclusion | Declared family of regions and an identified geometric modular group/action | Suitable wedge/boost hypotheses can imply HSMI for corresponding translated wedges. D3 alone does not generally identify a geometric region family. |
| Exact finite-dimensional unitary action of a connected noncompact simple symmetry group | A separate group-representation claim, not a T/D label consequence | Continuous finite-dimensional unitary representation of the specified connected noncompact simple group | No nontrivial representation under that hypothesis. This does not apply to every noncompact group: noncompact abelian groups such as `R` have one-dimensional unitary characters. |
| Finite capacity implies spatial sites | No established T-to-site implication | Specified spatial tensor factorization, graph, local algebras, and interaction structure | Capacity does not force factorization or site structure; those remain independent model choices. |

The other items in the historical typed table are conditional consistency statements: a cosmological-constant identity using `N := S_dS` is not an independent prediction when `N` is defined from the measured horizon entropy; and `w=-1` tests only the explicitly declared fixed-capacity branch. These statements do not supply an R-specific observable or state.

### 4.7 Structural levels are not physical scales

T0/T1/T2 and D0-D4 are structural labels unless a mapping explicitly assigns physical units or scales. Do not describe them as successive time, energy, or length scales solely because they are ordered in the exposition.

---

## 5. Core glossary: foundational, state, and information terms

### 5.1 Foundational terms

| Term | Definition and correct use | Current status/caution |
|---|---|---|
| **R** | The target research programme and its intended account of Reality | Its intended ontology is not identical by definition to a particular finite model or notebook |
| **Reality / totality** | The total referent that R aims to describe | Metaphysical scope; must not be used as a synonym for one universe model without an explicit bridge |
| **Formal object** | A state, operator, algebra, map, probability model, or other declared mathematical object | A formal object can be consistent without physically existing |
| **Model** | A specified mathematical structure interpreted for a chosen question | Its conclusions apply only to the stated assumptions and observable class |
| **Bridge hypothesis** | A mapping from formal/model objects to physical or ontological claims | Requires independent motivation and a discriminating consequence |
| **Origin** | A proposed primitive, boundary, or explanatory origin in R | Remains open/under-typed until the object, operation, domain, and inferential target are specified |
| **Hypothesis** | A proposition being tested or proposed | It is not evidence, probability, novelty, or existence |
| **Axiom** | A premise adopted as part of a formal branch | Must be labelled as adopted, not claimed to have been derived |
| **Selection principle** | A rule choosing one state/model/observable among alternatives | An explicit choice is not evidence that the choice is physically correct |
| **Independent motivation** | A rationale for a rule not selected because it produces the target result | Must include alternatives and a test that could reject the rule |
| **Underdetermination** | The declared assumptions permit inequivalent outcomes | Relative to the stated assumption set; extra justified premises may remove it |

### 5.2 States, Hilbert space, and capacity

| Term | Definition and correct use | Current status/caution |
|---|---|---|
| **State ray** | A one-dimensional subspace representing a pure state in Hilbert-space language | Does not fix the Hilbert-space dimension or physical interpretation |
| **Pure state** | An extreme point of the chosen convex state space; in finite quantum mechanics, represented by a rank-one density operator | Type-III local algebras do not have pure normal states in the same way as type-I finite-dimensional density matrices |
| **Mixed state** | A non-extreme state, often represented by a density matrix in type-I finite systems | Do not silently assume a trace-class density matrix for a type-III local algebra |
| **Faithful state** | A state that is nonzero on every nonzero positive element (for a density matrix, full rank) | Faithfulness is an assumption for several modular convergence results |
| **Normal state** | A state continuous in the relevant ultraweak topology of a von Neumann algebra | Distinguish normality from faithfulness |
| **Total Hilbert-space dimension** | \(\dim\mathcal H_{\mathrm{tot}}\), if finite | Infinite dimensionality makes \(\ln\dim\mathcal H\) unusable as a finite capacity without another definition |
| **Capacity \(N\)** | In one proposed route, \(N=\ln\dim\mathcal H_{\mathrm{tot}}\) for finite dimension | Units are nats; does not equal bits unless converted; value and physical interpretation remain open |
| **Entropy bound** | An upper bound on an entropy or information measure | Not an equality and not proof of a finite-dimensional Hilbert space |
| **Effective finite capacity** | A cutoff- or resource-dependent restriction on accessible degrees of freedom | Must specify the operational definition and how it relates to exact state-space dimension |
| **Horizon entropy** | Entropy associated with a specified gravitational horizon under a stated framework | Cannot be equated with \(\ln\dim\mathcal H\) without additional hypotheses |
| **Density matrix** | Positive trace-one operator representing a state on a type-I system | It is not a general representation of normal states on every von Neumann algebra |
| **Tensor factorization** | An identification \(\mathcal H\simeq\mathcal H_A\otimes\mathcal H_B\) | Even when dimensions factor arithmetically, preferred subsystems and spatial adjacency do not follow |
| **Site structure** | A chosen family of local factors/degree-of-freedom algebras and an associated locality graph | Finite dimension does not by itself provide sites or geometry |
| **State-selection problem** | The task of justifying which state is physically relevant | Defining a rule and proving its output satisfies desired conditions are separate obligations |

### 5.3 Probability and information terms

| Term | Definition | Rule/caution |
|---|---|---|
| **Source** | A declared random variable or uncertainty model over possible inputs/states | A single fixed state has zero Shannon entropy; nonzero coordinates do not themselves define an ensemble |
| **Support** | Values with positive probability under a distribution | A deterministic map's collisions outside support do not affect source recoverability |
| **Target task** | A function \(T=t(X)\) or decision-relevant distinction of the source | Must be named before a readout is judged successful |
| **Readout** | The value accessible after applying a declared measurement or map | Specify whether the retained object is a vector, scalar, spectrum with multiplicity, rounded value, or distribution |
| **Channel** | A stochastic map from input to output | Requires an input and output alphabet or measurable spaces, transition law, and any resource constraints |
| **Shannon entropy** | \(H(X)=-\sum_x p(x)\log_2p(x)\) for a finite source in bits | Depends on the source distribution, not just on amplitude labels |
| **Conditional entropy** | \(H(X\mid Y)\), residual uncertainty about X after Y | Zero iff X is determined by Y almost surely in the finite discrete setting |
| **Mutual information** | \(I(X;Y)=H(X)-H(X\mid Y)\) for discrete variables | For deterministic \(Y=F(X)\), \(I(X;Y)=H(Y)\); this is not Shannon-Hartley capacity |
| **Data-processing inequality** | For Markov chain \(X\to Y\to Z\), \(I(X;Z)\le I(X;Y)\) | Does not order arbitrary incomparable readouts, and does not imply that every non-injective map destroys every task |
| **Source recoverability** | Exact recovery of X from Y | For deterministic finite maps, iff F is injective on the positive-probability support |
| **Task recoverability** | Exact recovery of T from Y | Iff every fiber of F intersecting the support contains only one task value, equivalently \(H(T\mid Y)=0\) |
| **Fiber / equivalence class** | Set \(F^{-1}(y)\) of inputs merged by readout F | A task survives iff it is constant on every relevant fiber |
| **Partition refinement** | One readout has at least as fine a partition as another | Downstream deterministic processing may coarsen but cannot refine an upstream partition |
| **Information loss** | Loss of a specified input/task distinction under a named readout/channel | Do not infer it from a zero aggregate alone |
| **Mutual-information tie** | Two readouts yield equal I(X;Y) for a specific source | Does not make their partitions or task usefulness equivalent |

### 5.4 R-specific and imported physics vocabulary

These terms occur in older R notes but are not all canonical scientific categories. Keep them as provisional vocabulary with explicit criteria rather than silently promoting them into physical ontology.

| Term or phrase | Preferred definition / use | Status and minimum test |
|---|---|---|
| **Kugelblitz** | A hypothetical black hole formed by sufficiently concentrated radiation | A model-specific gravitational-collapse claim; specify radiation stress-energy, geometry, and collapse conditions |
| **“Singularity of light”** | At most a historical metaphor for a radiation-collapse scenario; not a literal luminous substance at a singularity | Prefer “black hole formed from concentrated radiation” for formation and the exact singularity criterion for the interior; no unreferenced pair-production-radius estimate is retained |
| **Strange spectrum** | A spectral classification, such as a singular-continuous component, for a specified operator and state/measure | The operator, spectral measure, limit, finite-size controls, and absolutely continuous/pure-point alternatives must be stated |
| **Strange light** | A provisional label for a declared photonic/wave model with a specified singular-continuous spectral property or critical-state regime | These are alternative operational criteria, not synonyms; finite-stack transmission does not alone prove spectral type of an infinite Maxwell operator |
| **Strange fluidity** | Either a spectral property of a declared fluid observable or strange nonchaotic dynamics in a specified driven system | Keep spectral classification separate from attractor geometry and Lyapunov exponents; not a generic claim about Navier-Stokes flow |
| **Light fluidity / quantum fluid of light** | An effective hydrodynamic description of optical fields in specified nonlinear or driven media | Model-specific analogy with established regimes; not a claim that vacuum light is literally a material fluid |
| **Optical vortex / antivortex** | A phase singularity with nonzero winding; the sign is defined relative to a stated contour orientation | Measure winding and resolution stability; distinguish vortex charge from frequency sign, energy sign, helicity, and complex conjugation |
| **“Minus light” / “negative light vortex”** | Ambiguous legacy phrases that must be replaced by a named operation or standard term | Use “antivortex,” “complex-conjugate mode,” “opposite-helicity state,” or “negative-frequency mode” only when that exact object is meant |
| **Helicity, parity, time reversal, conjugation** | Distinct transformations/actions on states, fields, or amplitudes | State the representation and convention; a sign change in one scalar phase/winding variable does not establish a helicity or time-reversal statement |

The audited terminology table in the legacy v1.5 appendix remains available in `legacy_sources/`. Its old source checks are historical; this edition does not re-certify every bibliographic claim in that appendix. Any use of these terms in a load-bearing argument requires current source-level support and an operational consequence.

## 6. Modular and operator-algebra vocabulary

| Term | Definition and correct use | Current status/caution |
|---|---|---|
| **Von Neumann algebra** | A unital *-algebra of bounded operators closed in the weak operator topology (equivalently, a dual operator algebra) | State the representation and algebra explicitly |
| **Commutant** | \(\mathcal M'=\{B: BA=AB\text{ for all }A\in\mathcal M\}\) | The commutant is representation-dependent as a concrete set of operators |
| **Standard pair** | An algebra/vector (or suitable algebra/state representation) satisfying cyclic and separating conditions | Must be checked, not inferred from finite nesting |
| **Tomita operator** | Closure of the antilinear map \(A\Omega\mapsto A^*\Omega\) on \(\mathcal M\Omega\) under standardness assumptions | Its polar decomposition underlies modular data |
| **Modular conjugation \(J\)** | Antiunitary involution from the polar decomposition of the Tomita operator | A mathematical object; geometric reflection is an extra identification |
| **Modular operator \(\Delta\)** | Positive self-adjoint operator from that polar decomposition | Domain and state/algebra pair matter |
| **Modular flow** | \(\sigma_t^\omega(A)=\Delta_\omega^{it}A\Delta_\omega^{-it}\) in a suitable representation | Modular parameter is not automatically physical time |
| **Modular Hamiltonian** | Often \(K=-\log\Delta\) or, in a type-I density-matrix setting, \(-\log\rho\), depending on convention | State whether constants, sign, and complement are included |
| **KMS condition** | A thermal analyticity/equilibrium condition for a state relative to a specified automorphism group and inverse-temperature convention | For `σ_t(A)=Δ^{it}AΔ^{-it}`, `ω(Aσ_{iβ}(B))=ω(BA)` uses `β=-1` for analytic A,B; `β=+1` applies to the reversed flow. Physical temperature requires a physical-flow identification. |
| **Contribution register** | Persistent record of contributors, artifacts, and attribution boundaries | A recorded contribution is not blanket endorsement; scholarly paper authorship remains with cited publications. See Appendix D. |
| **P5′ fixed-μ raw run** | Finite-size raw data, parameters, slopes, scripts, and run metadata for the declared regulator sequence | Establishes only the declared finite numerical observation; no continuum statement follows automatically. |
| **Noncompact simple-group representation constraint** | Absence of nontrivial finite-dimensional continuous unitary representations for the specified connected noncompact simple Lie group hypothesis | Does not apply to every noncompact group; e.g. `R` has one-dimensional unitary characters. |
| **Relative modular operator** | Operator \(\Delta_{\psi,\omega}\) associated with a pair of suitable faithful normal states | Fix state order and convention before writing a cocycle or entropy formula |
| **Connes cocycle** | \((D\psi:D\omega)_t\), a unitary cocycle comparing modular flows of faithful normal states | Strong convergence is not operator-norm convergence; varying algebras require compatible embeddings and further hypotheses |
| **Araki relative entropy** | Noncommutative relative-entropy functional for states on a von Neumann algebra | May be infinite; distinguish finite-regulator values from continuum limits |
| **In-state cocycle deviation** | Quantity such as \(\|((D\omega:D\psi)_t-I)\xi_\psi\|\) for a declared vector and convention | Relative entropy can bound this under the stated hypotheses; it does not bound operator norm |
| **Operator-norm convergence** | Convergence in \(\|A_n-A\|\) | Much stronger than strong operator convergence; finite-dimensional counterexamples show state-level control does not imply it |
| **Strong operator convergence** | \(A_n\xi\to A\xi\) for every fixed vector \(\xi\) | Not uniform over unit vectors |
| **Strong-resolvent convergence** | Strong convergence of resolvents at nonreal parameters for self-adjoint operators | Not the same as norm-resolvent convergence or a uniform spectral estimate |
| **Same-folium normality** | Two representations/states have a normal relationship within the relevant folium of states | Cannot be assumed for raw comparisons between different cutoffs/embeddings |
| **Split property** | A local-net property allowing an intermediate type-I factor between suitably separated local algebras | Can follow from nuclearity-like phase-space assumptions in specific theorems; does not select R's sites |
| **Nuclearity** | Compactness/trace-class-like condition on a specified phase-space map | Not synonymous with finite capacity, local tomography, or Standard Model content |
| **Local net** | Assignment of algebras to spacetime regions with specified properties such as isotony and locality | A net is structural input; its physical regions and observables still need interpretation |
| **Half-sided modular inclusion (HSMI)** | Inclusion \(\mathcal N\subsetneq\mathcal M\) with a common standard vector and one-sided modular invariance under exact hypotheses | Exact nontrivial finite-dimensional standard HSMI is obstructed; finite diagnostics are not full HSMI proofs |
| **Positive translation generator** | Generator of a one-parameter unitary group with nonnegative spectrum arising in a modular-inclusion theorem | The theorem's conditions are required; it is not an automatic physical spatial translation |
| **Geometric modular action (GMA)** | Modular flow acts geometrically on the relevant net in specified settings | A property of a state/algebra/region system; it does not by itself select that state |
| **D3 diagnostic** | A finite or one-particle quantity designed to test an aspect of the D3/HSMI route | Must be named narrowly; it is not the full algebraic HSMI condition |

### 6.1 Relative-entropy cocycle bound: correct scope

For faithful normalized normal states \(\psi,\omega\) in a common standard-form representation, use an explicit convention. In one convention, let \(u_t=(D\omega:D\psi)_t\), \(S=S(\psi\Vert\omega)<\infty\), and let \(\xi_\psi\) represent \(\psi\). The v4.1 proof record establishes the conditional in-state inequality

\[
\|(u_t-I)\xi_\psi\|^2\le 2|t|\left(S+\sqrt{2S}\right).
\]

The derivation uses the spectral probability measure \(\mu\) of the relative modular operator in \(\xi_\psi\), the change of measure \(d\nu=\lambda\,d\mu\), the identity \(D_{\mathrm{KL}}(\mu\Vert\nu)=S\), total-variation control via Pinsker, and \(|e^{it\log\lambda}-1|^2\le 2|t|\,|\log\lambda|\). The inequality is about one specified vector at fixed t. It is not an operator-norm estimate.

The supplied finite-dimensional rotated-small-eigenvalue counterexample reports relative entropy and the in-state deviation tending to zero while \(\|u_t-I\|\) remains order one. This is consistent with the distinction between vector-level control and a supremum over all unit vectors. The table and proof need to remain separate forms of evidence: the proof supports the inequality; the table illustrates the failure of the stronger inference.

### 6.2 State norm convergence and cocycles: a separate theorem

The full HTML of Abbas Edalat, arXiv:2607.24445v2, Appendix B, Lemma B.1, was inspected for this edition. It assumes a fixed sigma-finite von Neumann algebra in a common standard form, a faithful normal state \(\omega\), and faithful normal states \(\psi_n\) with \(\|\psi_n-\omega\|_{\mathcal M_*}\to0\). Under those hypotheses the paper proves norm convergence of natural-cone vector representatives, strong-resolvent convergence of relative modular operators and their logarithms, strong convergence \([D\psi_n:D\omega]_t\to I\) at each fixed t, and convergence of the stated modular correlation \(\psi_n(A\sigma_t^{\psi_n}(B))\) for fixed \(A,B,t\).

This result is narrower than “the R cocycle converges.” It does not by itself establish operator-norm convergence, uniformity over all t, or continuity when the algebra and representation vary with the regulator. It is compatible with a separate obstruction for raw fixed-cutoff comparisons between changing compact-local embeddings. The algebra/state/embedding hypotheses must match before transfer to R.

---

## 7. Origin, signed endpoints, profiles, and signal loss

### 7.1 The raw endpoint expression

The string

\[
0=(M_{+\infty}=+1\ \land\ M_{-\infty}=-1)
\]

is not an ordinary numerical equality if the parenthesized expression is a conjunction of propositions. Keep the endpoint conditions as conditions. If \(M\) has an appropriate domain and limits, then the signed endpoint sum is a separate definition/consequence:

\[
M(+\infty)=+1,\quad M(-\infty)=-1,\qquad S_{\mathrm{end}}:=M(+\infty)+M(-\infty)=0.
\]

This does not imply that the endpoint vector is zero, that a norm or total variation is zero, or that a signal has zero energy/information/capacity.

For \(m=(m_1,m_2)^T=(1,-1)^T\),

\[
S=m_1+m_2=0,\qquad D=m_1-m_2=2,\qquad \|m\|_2=\sqrt2,\qquad |m_1|+|m_2|=2.
\]

The signed sum is one functional. The contrast, norm, and total variation are different functionals.

### 7.2 Signal-loss taxonomy

| Operation | Mathematical object | What it does | What cannot be inferred automatically |
|---|---|---|---|
| Signed cancellation | Scalar functional \(\Sigma(m)=m_1+m_2\) | Maps \((1,-1)\mapsto0\) | The two components have not thereby been physically erased |
| Projection/readout loss | Many-to-one map, e.g. sum alone | Merges inputs that yield the same output | Global non-injectivity need not destroy every task on a restricted source |
| Selective erasure | Linear map \(E_-=\operatorname{diag}(1,0)\) | Maps \((1,-1)\mapsto(1,0)\) | Not common scalar attenuation; it changes signed balance |
| Common attenuation | \(A_g(m)=gm\) | Maps \((1,-1)\mapsto(g,-g)\) | Preserves zero signed sum while shrinking contrast; physical meaning requires a channel model |
| Baseline shift | Invertible map \(T(x)=x+1\) | Maps \(-1\mapsto0\) | A known reversible shift does not lose information |
| Rectification | \(r(x)=\max(x,0)\) | Maps \((1,-1)\mapsto(1,0)\) | It is nonlinear; composition order and retained readout matter |
| Noise | Stochastic channel | Changes output distributions and distinguishability | Effect depends on source, noise law, and receiver; “noise” is not a unique operator |
| Quantization | Discrete mapping from continuous readout to bins | Merges values at finite precision | Boundary phase and noise can affect which values collide |

Rectification and aggregation need not commute: \(\Sigma(r(1,-1))=1\), whereas \(r(\Sigma(1,-1))=0\). This is an exact map-composition fact, not a theorem about R's dynamics.

### 7.3 Shannon-Hartley and mutual information

For the ideal band-limited AWGN channel under the conventional average-power constraint,

\[
C=B\log_2\left(1+\frac{P_{\mathrm{rx}}}{P_{\mathrm{noise}}}\right)
\]

is the channel-capacity formula in bits per second. It is a supremum over admissible codes/input distributions for that channel model, not the mutual information of one fixed finite-alphabet encoder. The formula requires a declared bandwidth, received power, noise power, and AWGN assumptions.

For a fixed source and readout, use \(I(X;Y)\), with units of bits per symbol or per source draw. Do not compare that directly with a capacity rate in bits per second without an explicit symbol rate/time normalization. With fixed receiver noise and amplitude gain g, received SNR often scales as \(g^2\); if noise or measurement conditions change too, recalculate the SNR rather than reusing the monotonicity statement.

### 7.4 Profiles and endpoints

The candidate profiles

\[
M_T(x)=\tanh x,\qquad M_E(x)=\operatorname{erf}x,\qquad M_R(x)=\frac{x}{\sqrt{1+x^2}}
\]

all have value 0 at 0 and limits \(-1,+1\) at the two ends, but differ in interior values, derivatives, and spectra. An endpoint pair does not determine the profile or its scale.

For \(M_k(x)=\tanh(kx)\), \(k>0\), the endpoints remain unchanged while the derivative norm and spectral width vary. At x=1, the three displayed candidates are separated by a minimum gap of about 0.05448737. A uniform quantizer with step q smaller than this gap gives different bins for all three values regardless of quantizer phase; with bounded sample error ε a sufficient condition is \(\Delta_{\min}>q+2\epsilon\). This is only a guarantee for the stated finite candidate family and readout location.

### 7.5 Scale-free rule: theorem and important correction

Suppose \(M:\mathbb R\to\mathbb R\) obeys

\[
M(\lambda x)=M(x)\quad\forall\lambda>0,\qquad M(-x)=-M(x),
\]

and \(\lim_{x\to+\infty}M(x)=1\), \(\lim_{x\to-\infty}M(x)=-1\). Then M is constant on the positive half-line: for any x,y>0, choose \(\lambda=y/x\) to get M(y)=M(x). The limit forces M(x)=1 for x>0. Oddness gives M(x)=-1 for x<0 and M(0)=0. Therefore M is the sign function with the convention \(\operatorname{sgn}(0)=0\).

This is an exact result under the stated assumptions. It needs a caveat: the sign function is discontinuous at zero. If the candidate profile class also requires continuity at zero, the assumptions are incompatible and the class is empty, not a smooth-profile singleton. A “no scale” condition therefore selects the sign function only when discontinuous profiles are admissible; it does not select one of the smooth v6.1 profiles.

### 7.6 Endpoints and transforms

For a sufficiently regular profile with integrable derivative \(g=M'\), the endpoint change fixes \(\int g=2\). It does not fix the shape or spectrum of g. Fourier inversion applies to a specified function/distribution class and full complex transform, with boundary information as needed. Transforming magnitude-only spectra generally loses phase and can introduce non-uniqueness. Substituting \(x=\pm\infty\) directly into the ordinary Fourier kernel is not a valid transform prescription; define a profile space, distributional extension, regularization, or a separate finite-sector map.

The terms “signal loss,” “nullspace,” “cancellation,” “information,” “energy,” and “capacity” must not be exchanged casually. They refer to different maps, functionals, or physical models.

---

## 8. Finite-source retention contracts and the T2 candidate instance

### 8.1 Finite-source theorem

Let X be a finite random variable with positive-probability support \(\operatorname{supp}(P_X)\), and let \(Y=F(X)\) for deterministic F. Then

\[
I(X;Y)=H(Y),\qquad H(X\mid Y)=H(X)-H(Y).
\]

The whole source is exactly recoverable from Y iff F is injective on the support, equivalently \(H(X\mid Y)=0\). If T=t(X) is a target task, T is exactly recoverable from Y iff t is constant on every fiber \(F^{-1}(y)\) that intersects the support, equivalently \(H(T\mid Y)=0\).

This theorem is independent of the name R. Its use for R requires R to declare a source/uncertainty model, target task, and admissible readout class.

### 8.2 Source/readout examples

For the equiprobable source \(X\in\{(1,-1),(-1,1)\}\), the source carries one bit. The signed sum maps both states to 0 and loses that bit. Contrast distinguishes them. Selective erasure and componentwise rectification preserve the bit if the full output vector is retained; they can lose it if followed by summation.

For the uniform four-state source \(X\in\{\pm1\}^2\), the sum and contrast readouts both have entropy 1.5 bits, but induce different partitions and are not post-processable into one another on that support. Equal mutual information does not make readouts task-equivalent.

### 8.3 Partition contract

Define \(x\sim_F x'\) iff F(x)=F(x'). The readout partitions the support into equivalence classes. Deterministic post-processing can only coarsen this partition. A task survives if and only if none of its relevant partition blocks mixes different task values. This provides a simple auditable contract:

1. declare the source support and probabilities;
2. declare the task;
3. declare the readout and exact output representation;
4. compute the induced fibers;
5. report source/task conditional entropy or an exact combinatorial check;
6. record numerical tolerances if outputs are floating point.

### 8.4 T2 finite split: useful candidate, not R selection

For a bipartite pure state with faithful Schmidt probabilities \(p=(p_1,\ldots,p_d)\), \(p_i>0\), \(\sum_i p_i=1\), the finite-dimensional modular operator for the subsystem algebra has eigenvalues \(p_i/p_j\), indexed by ordered pairs (i,j). The multiset of eigenvalues of \(\log\Delta\) is therefore

\[
\{\log p_i-\log p_j:1\le i,j\le d\}.
\]

Counting multiplicities, the sum is exactly zero:

\[
\sum_{i,j}(\log p_i-\log p_j)=0.
\]

If “sum of the spectrum” means summing distinct spectral values while discarding multiplicities, that is a different operation and need not equal zero. Use the trace/multiplicity convention explicitly.

Define normalized inverse Schmidt probabilities by \(p_i^*=(1/p_i)/\sum_j(1/p_j)\). Then

\[
\log p_i^*-\log p_j^*=-(\log p_i-\log p_j),
\]

so the modular log-spectrum multiset is unchanged by p→p*. For generic d≥3 spectra, p and p* are genuinely different unordered Schmidt spectra; exceptional self-inverse/permutation-symmetric spectra must be excluded. If a source chooses p and p* equiprobably and they have the same modular-spectrum readout, that readout has one bit of residual source uncertainty. Entropy generally differs between p and p*, but this must be checked for the selected source, not assumed.

For the explicit 180-state source supplied in Packet 3, uniform weights `1/180` and the included standard-library verifier reproduce the same partition size for the modular-spectrum and entropy readouts: each has 60 two-element fibers and 60 singleton fibers, hence 120 classes. For either readout, `I(X;Y) = log₂(180) − 2/3 = 6.8251864297` bits and `H(X|Y)=2/3` bit. The signed-sum readout is constant on all 180 states, so its mutual information is zero. The two 120-class partitions are incomparable; the Schmidt-spectrum readout gives the identity partition. The equivalence-class checks are stable under the supplied tolerances `10⁻⁹`, `10⁻⁷`, and `10⁻⁵`. These results establish the supplied finite construction and are not an R-specific source, task, or observable-selection result. The attached contract retains `selection_status = UNSELECTED` and `physical_interpretation = UNSPECIFIED_FOR_R`.

### 8.5 Qubit Gibbs alternative: a stress test, not automatic new selection

For a two-level Gibbs state with gap \(\delta E>0\), probabilities are a function of \(\beta\delta E\). The entropy is invariant under exchanging the two probabilities and depends on the magnitude of the log-odds. The unordered modular spectrum also contains the reciprocal ratio pair \(e^{\pm\beta\delta E}\) and depends only on \(|\beta\delta E|\). Consequently, for the ordinary unordered qubit Gibbs source, entropy and modular spectrum can induce the same partition over \(\beta\) values; they do not automatically furnish a second completion with a different partition. The supplied independent standard-library verifier enumerates the declared qubit family and confirms 13 equivalence classes with identical entropy and unordered modular-spectrum partitions. A different result would require a declared orientation-sensitive observable, extra labels, or a different source/task construction. Such additions must be listed as model inputs, not smuggled in as a property of “the qubit Gibbs reading.”

---

## 9. Cosmology, capacity, site structure, and scaling

### 9.1 Capacity and the cosmological constant

The proposed relation between capacity N and cosmological scale \(\Lambda\) depends on what N means and whether an entropy bound is saturated. A bound is not an equality. If N is calculated using the same observed \(\Lambda\) that the equation is later said to predict, the result is a consistency calculation, not an independent prediction.

Any such claim must specify the horizon/patch, units, entropy convention, logarithm base, whether N is a Hilbert-space dimension or entropy-like quantity, and an independent route to N. A physical interpretation of \(\eta\) as universal entanglement density requires its definition, units, universality argument, and bridge to the relevant gravitational equation.

### 9.2 Spatial site structure

Finite Hilbert-space dimension does not by itself entail a preferred tensor-product factorization, a local interaction graph, or a spatial lattice. Prime dimensions forbid an exact nontrivial finite tensor factorization into dimensions greater than one; composite dimensions allow factorizations but do not choose among them. A spatial lattice is one model route and has energy-cutoff consequences under conventional tiling assumptions. A local-net route is structurally different and needs isotony, locality, state, and split/nuclearity hypotheses. Nuclearity does not automatically supply sites or fermion content.

### 9.3 Fixed-regulator and continuum limits

Limit order is part of every claim. A quantity can tend to zero as mass/deformation parameter \(\mu\to0\) at fixed regulator L while growing with L for fixed \(\mu>0\). These statements are not contradictory; the iterated limits may fail to commute.

The supplied raw Wilson-chain data at fixed \(\mu=0.00625\) are:

| L | raw \(D/\mu^2\) |
|---:|---:|
| 8 | 7.414891703720506 |
| 12 | 7.490127829519515 |
| 16 | 7.541122926473356 |
| 24 | 7.611195822165920 |
| 32 | 7.660172725977954 |

The adjacent secant slopes versus \(\ln L\), recomputed from those raw values, are 0.185555, 0.177262, 0.172821, and 0.170247. They decrease toward 1/6 ≈ 0.16667 over this finite sequence, but the sequence does not establish convergence to that value. It is a finite-size trend consistent with a logarithmic term, not a proof of fixed-\(\mu\) asymptotic divergence or an infinite continuum Araki relative entropy. The raw Wilson data and slope verifier are included with a run record. However, regenerating the Wilson series uses a path-patched v4.0 covariance script supplied through the external `V40_SCRIPT` environment variable; this dependency is identified by hash in the run record and the complete Wilson generation path is not self-contained in this package. The separately written staggered-lattice sweep is independent code. The staggered slopes also decrease over \(\ell=8,12,16,24\), from about 0.25 to about 0.16, and the final step dips below 1/6. An attempted Wilson point at \(L=48\) was excluded because the calculated spectral margin was negative at the chosen precision/quadrature settings. These limitations are part of the data record.

The fixed-regulator small-\(\mu\) asymptotic and the fixed-\(\mu\), increasing-\(L\) sequence are different claims and must not be merged. Neither numerical sequence by itself settles the continuum order of limits.

### 9.4 Geometry, gravity, and state selection

Geometric modular action (GMA) is a property of a specified algebra/state/region arrangement. State selection is a separate mechanism. A state selected because it has GMA does not make GMA an independent prediction. A regular cosmological saddle does not alone establish normalizability, the perturbation state, the lapse contour, equivalence to the Bunch-Davies prescription, or a physical arrow of time. A linearized gravity relation and a nonlinear Einstein equation are separate claims with separate assumptions.

### 9.5 Spectral type and short-scale GMA

A finite-size exponent or a fit to \(cL-d\ln L+C\) does not uniquely determine a limiting spectral measure. State the operator sequence, boundary conditions, spectrum window, broadening, size sequence, fit range, precision, and limit procedure. Reproduce site-block modular-spectrum claims from raw data before promoting them beyond a reported diagnostic.

For a massive versus massless free Dirac field in 1+1 dimensions restricted to an interval of length `r`, write `μ = m r`. Casini–Fosco–Huerta’s short-distance entropic c-function expansion gives `c(μ) = 1/3 − (1/3) μ² log² μ + O(μ² |log μ|)` (their Eq. 48), hence `ΔS_EE = −(1/6) μ² log²(1/μ) + O(μ² |log μ|)`. For the same restricted-state comparison, the first-law identity is `D(ρ_m^A || ρ_0^A) = Δ⟨K_0⟩ − ΔS_EE`, with the massless reference modular Hamiltonian `K_0 = 2π ∫₀ʳ dx [x(r−x)/r] T₀₀⁽⁰⁾(x)`. At fixed momentum cutoff `Λ`, the kinetic-energy-density difference in the stated convention is

\[
\Delta\langle T_{00}^{(0)}\rangle
=\frac1\pi\int_0^\Lambda\!dk\left(k-\frac{k^2}{\sqrt{k^2+m^2}}\right)
=\frac{m^2}{2\pi}\left[\log\frac{2\Lambda}{m}-\frac12\right]
+O(m^4/\Lambda^2).
\]

Using `∫₀ʳ dx [x(r−x)/r] = r²/6` gives `Δ⟨K₀⟩ = (μ²/6)[log(2Λr/μ) − 1/2] + …`. At fixed `Λr` this term has only a single logarithm in `μ`, so it does not alter the leading double-log term from `−ΔS_EE`. Therefore this model and cutoff ordering support the leading term

\[
D(\rho_m^A\Vert\rho_0^A) = \frac16\mu^2\log^2(1/\mu) + O(\mu^2|\log\mu|).
\]

The coefficient is mathematically supported under the stated free-Dirac, same-interval, fixed-cutoff assumptions and is also supported numerically by Wilson four-point windows close to `1/6` and staggered fits around `0.1663–0.1673`. It is not a universal GMA theorem and does not prove a regulator-independent continuum limit. Keep it distinct from the separate fixed-`μ` cutoff-growth sequence in Section 9.3; their limits and regulators differ.

---

## 10. External literature and source audit status

### 10.1 Chen's local modular-data preprint

The official Zenodo record identifies Jiaxuan Chen's *Convergence of local modular data for half-line free fermions and a locality/passband obstruction to raw fixed-cutoff global quasi-equivalence*, v2, published 31 July 2026. The public record and correction notes were inspected; the hosted PDF fetch failed in this audit, so the full mathematical proof is not marked as independently full-text verified here. The record says v2 corrects v1: for pinned Daubechies schemes, endpoint-touching windows have a stated \(O(a^{1/2})\) upper bound driven by an endpoint boundary layer, not the former arbitrary \(O(a^s)\) claim for all windows. It reports local modular-data convergence under specific quasi-free CAR, covariance, exhaustion, and faithfulness hypotheses, alongside a scoped obstruction for raw fixed-cutoff global comparison.

This is an external benchmark, not an automatic theorem for R's Chern-edge or Wilson regulators. R must supply compatible one-particle spaces, embeddings, exhaustion projections, embedded covariances, endpoint faithfulness, local-algebra identification, and an explicit acceptance topology before using the result.

### 10.2 arXiv:2607.24445: fixed-algebra modular continuity

arXiv:2607.24445 is Abbas Edalat, *Finite-Precision Algebraic Quantum Field Theory: Quantum Parcels, Locality, Modular Structure and Factors*, v2 dated 29 August 2026. The HTML full text was available and Appendix B, Lemma B.1, was inspected. It is not the Chen preprint. Lemma B.1 proves relative modular continuity for faithful normal states on one fixed sigma-finite von Neumann algebra in a common standard form when \(\psi_n\to\omega\) in predual norm. Part (iv) states strong convergence of the fixed-time Connes cocycle to the identity and convergence of specified modular correlators under those hypotheses.

This strengthens the source verification compared with an earlier snippet-only attribution, but it does not establish a varying-algebra or varying-regulator cocycle theorem for R, operator-norm convergence, or uniform-in-time convergence. Keep it separate from Chen's wavelet/locality result.

### 10.3 Two lattice/wavelet references are not interchangeable

- Morinelli, Morsella, Stottmeister, and Tanimoto, “Scaling Limits of Lattice Quantum Fields by Wavelets,” *Communications in Mathematical Physics* 387, 299-360 (2021), DOI 10.1007/s00220-021-04152-5, develops an operator-algebraic wavelet scaling construction for specified scalar lattice fields and the free-field scaling limit.
- Osborne and Stottmeister, “Conformal Field Theory from Lattice Fermions,” *Communications in Mathematical Physics* 398, 219-289 (2023), DOI 10.1007/s00220-022-04521-8, is a closer free-fermion/CFT construction. It concerns specified 1+1-dimensional free lattice fermion models and convergence of stated generators/correlation functions under its hypotheses.

Neither paper by its existence alone validates the R regulator or proves the intended D3/HSMI property. The precise model class and convergence statement must match.

### 10.4 Source-access ledger for this edition

| Source/claim | Access level in this edition | Status and limitation |
|---|---|---|
| Legacy v1.5 glossary | Local file read | Used as historical baseline, not re-certified wholesale |
| v5.5-v6.2 release manifests | Independently recomputed from packet roots | 109/109 listed hashes match; see Section 11 |
| v5.5-v6.1 embedded predecessor archives | Independently byte-compared | All seven direct predecessor pairs match exactly |
| Chen v2 Zenodo record/correction notes | Official record and notes inspected; PDF fetch failed | Source-checked at record/abstract level, proof not independently reviewed in this edition |
| Osborne–Stottmeister journal metadata | Publisher record checked | Title, authors, CMP 398, pages 219–289 (2023), and DOI verified; transfer to R remains conditional |
| Borchers CMP 143 citation | Project Euclid/LQP source record checked | Correct title is “The CPT-theorem in two-dimensional theories of local observables,” CMP 143(2), 315–332 (1992) |
| Packet 3 | Original ZIP preserved; 21/21 listed hashes verified | Supplied verifiers pass; the scientific interpretations retain the limits stated in the relevant sections |
| Edalat arXiv:2607.24445v2 | Official arXiv metadata and full HTML inspected | Appendix B, Lemma B.1 source-checked; preprint, not peer-reviewed here |
| 180-state T2 modular-spectrum example | Packet 3 CSV, generator, contract, run record, and standard-library verifier included and rerun | Reproduced for the declared finite source; no R source/task/readout selection |
| P5′ fixed-μ Wilson and staggered data | Packet 3 raw CSVs, scripts, logs, and run records included; slope verifier rerun | Finite numerical trends reproduced; asymptotic/continuum claim remains open |
| `Foundations_of_R_Claude_Crosscheck_Packet_2.zip` | Not included in the current packet set; Packet 3 provides a new explicit 180-state construction | The Packet 3 construction is reproduced; this does not prove that it is byte-identical to the absent Packet 2 artifact |

---

## 11. Release-chain reconciliation through research release v6.2

### 11.1 Integrity results

The following manifests were rerun with paths resolved from each packet root, not the `outputs/` directory. All listed hashes matched the extracted bytes.

| Research release | Manifest entries | Verified | Interpreter-specific `.pyc` entries in manifest |
|---|---:|---:|---:|
| v5.5 Shannon-Hartley and signal loss | 14 | 14 | 0 |
| v5.6 negative endpoint reduction | 15 | 15 | 1 |
| v5.7 composed loss operators | 13 | 13 | 0 |
| v5.8 information retention contracts | 14 | 14 | 2 |
| v5.9 finite-source stress test | 14 | 14 | 0 |
| v6.0 source-task-observable contract | 13 | 13 | 0 |
| v6.1 endpoint identifiability | 13 | 13 | 0 |
| v6.2 finite precision and noisy identifiability | 13 | 13 | 0 |
| **Total** | **109** | **109** | **3** |

The direct predecessor archive embedded in each of v5.6, v5.7, v5.8, v5.9, v6.0, v6.1, and v6.2 is byte-identical to the separately preserved predecessor packet. This verifies that link in the package chain; it does not prove every historical claim in each packet.

The `.pyc` files in v5.6 and v5.8 were included and their hashes match the current archive. This is an integrity pass but a portability weakness. Future packages should avoid generated bytecode in the authoritative manifest and preserve only source plus explicit environment metadata unless the bytecode itself is a research artifact.

### 11.2 Reported verification counts

The release records report the following numerical checks/tests. These counts are retained as results recorded by the respective packets; they are not combined into a single cross-release theorem count.

| Research release | Reported checks | Reported tests | Scope |
|---|---:|---:|---|
| v5.5 | Script passes | Not stated in supplied summary | Shannon-Hartley illustrative table, finite channel assumptions |
| v5.6 | 28 | 12 | Negative-endpoint operator alternatives |
| v5.7 | 35 | 16 | Composed loss/readout operators and finite alphabet |
| v5.8 | 39 | 10 | Deterministic finite-source retention contract |
| v5.9 | 88,568 | 6 | Declared finite-grid stress test, including maps/tasks/BSC grid |
| v6.0 | 14 top-level + 6,234 grid checks | 8 | Source/task/observable contract examples |
| v6.1 | 35 | 9 | Endpoint profile countermodels and finite-precision readout examples |
| v6.2 | 31 | 11 | Quantization, noise, and profile-identifiability checks |

The large v5.9 number is generated coverage over a finite declared grid. It is not 88,568 independent theorems. The v6.0 count is also finite-grid validation, not a proof that a model-selection contract can decide the physics without the contract fields being supplied.

### 11.3 Scientific status summary

The chain supports a sequence of methodological and finite-model results:

- the endpoint pair alone does not select a profile or loss operator;
- named finite readouts can be tested for source/task retention;
- the same readout can retain one task and lose another;
- equal mutual information does not imply equal partitions;
- finite precision and measurement noise can alter profile identifiability in source- and quantizer-specific ways; for the declared three-profile equal-prior source with a step-0.1, phase-zero quantizer, a finite sweep from σ=0.001 to 0.010 in increments of 0.00005 attains 0.9238227270 bits at σ=0.00400, compared with 0.9188069711 bits at σ=0.005 and 0.9182958341 bits in the noiseless quantized source; this is a grid result, not proof of a continuous global maximum;
- Shannon-Hartley capacity applies only after a channel and constraints are supplied.

It does not provide an R-specific source/task/observable model, a physical communication channel, a selected observable algebra, or a new continuum/regulator theorem.

---

## 12. Current scientific ledger and priority queue

### 12.1 Status ledger

| Research item | Current statement | Status |
|---|---|---|
| Origin / signed endpoint clue | Endpoint conditions can be formalized; raw equality/conjunction remains under-typed | `OPEN` / `UNDERDETERMINED` |
| Scale-free profile rule | Exact scale invariance plus oddness and endpoint limits yields the sign function; continuity at 0 makes the conditions inconsistent | Mathematical theorem under stated premises; R bridge open |
| Shannon-Hartley connection | Correct for a specified ideal AWGN channel with bandwidth, power, and noise assumptions | Standard theorem, no R channel supplied |
| Signal-loss operator | Several inequivalent maps realize “reduce -1 to 0” | `UNSELECTED` |
| Finite-source retention | Support injectivity and task fiber-constancy are exact finite-source criteria | `ESTABLISHED_UNDER_HYPOTHESES` |
| R source/task/readout contract | The fields needed for an R-specific claim are described but not filled | `UNDERDETERMINED` |
| Observable algebra | Parity-even and U(1)-neutral candidate routes remain distinct under the recorded hypotheses | `UNSELECTED` / `UNDERDETERMINED` |
| T2 finite Schmidt/modular candidate | Packet 3 source/verifier reproduces 120 classes for modular-spectrum and entropy readouts, with 60 pairs and 60 singletons each; both give `log₂(180) − 2/3 = 6.8251864297` bits | `REPRODUCED_FOR_DECLARED_CONSTRUCTED_SOURCE`; model selection `UNSELECTED`; R bridge open |
| Qubit Gibbs “second completion” | Standard qubit entropy and unordered modular spectrum both depend on absolute log-odds; they do not automatically yield different partitions | Candidate needs a more specific oriented readout/source |
| Local modular-data convergence | Chen v2 record reports a theorem under specified quasi-free CAR/wavelet hypotheses; full PDF proof was not read in this edition | External conditional benchmark; transfer to R open |
| State-norm/cocycle continuity | Edalat arXiv v2 Appendix B, Lemma B.1 supplies fixed-algebra, fixed-time strong convergence under predual-norm convergence of faithful states | Source-checked conditional theorem; R varying-regulator bridge open |
| Cocycle operator norm | State-level bound does not imply operator-norm closeness; packaged counterexample is consistent with the distinction | Stronger implication rejected |
| P5′ fixed-μ cutoff behavior | Raw Wilson sequence and independent staggered fixed-x sweep are reproduced; Wilson adjacent slopes 0.185555, 0.177262, 0.172821, 0.170247 | Finite trend only; asymptotic/continuum claim open |
| P5 small-μ relative entropy | For the specified free massive/massless Dirac interval comparison and fixed cutoff order, `D = (1/6)μ² log²(1/μ) + O(μ²|log μ|)` follows from the entropy c-function and first-law terms | Model-specific conditional asymptotic; not a universal GMA or continuum theorem |
| Quantized noisy identifiability sweep | Finite σ grid peaks at 0.9238227270 bit near σ=0.00400 for the declared source and quantizer | Reproduced finite-grid result; no continuous-max or R-detector claim |
| Modular KMS sign | For `σ_t=Δ^{it}(·)Δ^{-it}`, the specified boundary relation has β=−1; β=+1 for the reversed flow | Convention recorded; physical temperature not inferred |
| T–D dependency ledger | D0–D4 requirements, limits, and the noncompact-simple-group correction recorded in Section 4 | Typed dependency record; not a derivation from T-level names |
| D3/HSMI for R | Local modular convergence alone is not an HSMI proof; exact finite-N standard HSMI is obstructed | `OPEN` / blocked in finite-dimensional exact formulation |
| Site/spatial structure | Capacity/dimension does not choose tensor factors, local graph, or local net | Bridge open |
| Physical origin state, gravity bridge, independent \(\Lambda\) prediction | Need state prescription, independent N, and explicit bridge assumptions | `OPEN` |

### 12.2 Prioritized research queue

1. **Fill the R model-selection contract only from independent premises.** Declare the state/source space, uncertainty model, task, admissible readout class, resource assumptions, selection criterion, falsifier, physical interpretation, and derivation to R. A candidate can be mathematically complete without being an R model.
2. **Specify the physical meaning of the verified T2 candidate without changing its selection status.** The supplied 180-state construction is reproduced; what remains missing is an independently justified R source/task/readout mapping. The qubit Gibbs “second completion” remains rejected for the ordinary unordered qubit because the two verified partitions coincide.
3. **Make P5′ continuum-meaningful.** The supplied Wilson raw sequence and staggered sweep reproduce their finite trends. Next test norm convergence of the massive and massless restrictions under explicitly matched embeddings, boundaries, precision, and cutoff order. Do not upgrade fixed-μ growth to continuum divergence without a proof or controlled asymptotic argument.
4. **Review Chen v2 at proof level.** The official record and correction notes were inspected, but the PDF could not be retrieved for full proof review. Obtain the full preprint, record exact theorem hypotheses, and test R's Chern-edge/Wilson embeddings, covariance convergence, endpoint faithfulness, completion, and local algebra compatibility.
5. **Keep local modular flow, Connes cocycle, and HSMI separate.** State which algebra, which state pair, which embedding, which time window, and which topology. The fixed-algebra theorem in Edalat v2 does not settle changing regulator algebras.
6. **Finish site-structure choice or keep it open.** If using a tensor-product site model, state and justify factors, graph, and local interactions. If using a local net, state isotony/locality and the hypotheses for split/nuclearity. Do not infer the Standard Model representation merely from capacity or a dimension factorization.
7. **Specify the Chern-edge embedding package.** Record one-particle spaces, embedding maps, exhaustion projections, covariances, local algebras, endpoint faithfulness, acceptance topology, and failure criteria.
8. **Make the finite-N approximation criterion non-vacuous.** Predeclare ε(N), the norm, observable class, time window, precision/floor, and failure threshold. A one-particle diagnostic is not the full algebraic inclusion property.
8. **Independent prediction and physical origin remain later dependencies.** Do not use observed \(\Lambda\) to infer N and then call the relation a prediction of \(\Lambda\). Compare origin-state prescriptions only after the wave function, contour, normalizability, and perturbation state are specified.

Do not prioritize further finite-source enumeration unless it addresses an explicit unresolved source/task/readout model or a counterexample to the current retention contracts. The finite-source theorem is settled; R's missing model is not.

## 13. Alphabetical glossary index

The definitions in Sections 5-9 are authoritative. This index provides short lookup entries and directs the reader to the relevant section.

| Term | Compact definition | See |
|---|---|---|
| Admissibility | Declared restrictions on the allowed state, measurement, resource, or map class | §2, §12 |
| Araki relative entropy | Relative-entropy functional for states on a von Neumann algebra | §6.1 |
| Audit | Review of named artifacts and claims with a declared verification level | §1.5, §3.6, §10, §11 |
| AWGN | Additive white Gaussian noise channel model | §7.3 |
| Bargmann invariant | Relational phase invariant formed from overlaps around a specified loop | §4.3 |
| Baseline | Preserved earlier source/package used for comparison | §1 |
| Capacity | Resource-dependent information/state limit with a declared unit and model | §5.2, §9.1 |
| Channel | Stochastic map with a declared input/output and transition law | §5.3, §7.3 |
| Chiral edge | Boundary-localized degrees of freedom in a specified lattice/model setting | Legacy source notes, claim-specific record required |
| Claim ID | Stable identifier for one claim across edits | §2.3 |
| Cocycle, Connes | Unitary cocycle comparing modular flows of faithful normal states | §6.1-6.2 |
| Common standard form | Fixed representation framework used for comparing states and modular operators | §6.1-6.2 |
| Conditional result | Statement true only when specified assumptions hold | §2.2 |
| Contrast | For endpoint pair, difference \(m_1-m_2\) | §7.1 |
| D0-D4 | Proposed conjugation/spectral/Tomita/HSMI/geometric pairing ladder | §4.5 |
| Data-processing inequality | Mutual information cannot increase under downstream processing in a Markov chain | §5.3 |
| Deterministic readout | Output y is a fixed function of input x | §8.1 |
| Document edition | Revision of an editorial reference document; distinct from a research release | §0, §1, §1.1 |
| Endpoint identifiability | Whether endpoint constraints uniquely determine a target profile or object | §7.4-7.5 |
| Evidence level | Label describing the verification supporting a claim | §2.1 |
| Evidence mapping | Argument that a formal object or theorem corresponds to a specified R object | §2.1, §8, §12 |
| Faithful state | State with no nonzero positive element in its kernel | §5.2, §6 |
| Fiber | Set of inputs merged by a readout into the same output | §5.3, §8.3 |
| Finite source | Random variable with finite support | §8.1 |
| Glossary edition | Revision of the Methodology & Glossary document series | §0, §1.1 |
| GMA | Geometric modular action, a property of a specified net/state/region | §6, §9.4 |
| HSMI | Half-sided modular inclusion | §6 |
| Identifiability | Ability to distinguish model/source identities from available readouts | §7.4, §8 |
| Information loss | Loss of a named source or task distinction under a specified map/channel | §7.2, §8 |
| Manifest | Hash inventory whose path root and exclusions are declared | §1.6, §11 |
| Model-selection contract | Required specification of source, task, readout, admissibility, criterion, falsifier, physical map, evidence | §8, §12 |
| Modular generator | Logarithmic generator associated with modular operator/flow | §6 |
| Modular spectrum | Spectrum of Δ or log Δ, with multiplicity and convention explicitly specified | §8.4 |
| Mutual information | Shared information between a source and a readout | §5.3 |
| Normal state | State normal in the relevant von Neumann algebra topology | §5.2, §6 |
| Nuclearity | A phase-space compactness condition with theorem-specific implications | §6, §9.2 |
| Observable | Element/effect of a declared observable algebra or operational measurement set | §5, §12 |
| Operator-norm convergence | Uniform convergence over unit vectors | §6.1-6.2 |
| Origin | Underdefined project primitive/boundary/explanatory source | §7.1 |
| Package | Distribution bundle; not the same as a release or run | §1, §1.1-1.6 |
| Predual norm | Norm on the normal functionals of a von Neumann algebra | §6.2 |
| Profile | Function M over a declared domain, with values/regularity/boundary conditions | §7.4-7.5 |
| Readout | Output representation retained after measurement/map | §5.3, §7.2 |
| Reported, not reproduced | Claim/results described in a note but not reconstructed from available artifacts | §2.1, §10.4 |
| Research release | Scoped set of scientific artifacts, claims, code, data, and status | §1, §1.1, §1.3 |
| Research run | Immutable execution record with inputs, code, environment, commands, outputs | §1.4, Appendix B |
| Schmidt spectrum | Multiset of nonzero Schmidt weights/probabilities, convention declared | §8.4 |
| Selection status | Decision state for whether a candidate has been chosen | §2.2 |
| Shannon-Hartley | AWGN channel capacity formula under stated bandwidth/power/noise assumptions | §7.3 |
| Signed sum | Sum of signed endpoint/components; may cancel while contrast remains | §7.1 |
| Source support | Values with positive probability under the declared source distribution | §5.3 |
| Strong operator convergence | Pointwise action convergence on each fixed vector | §6 |
| Strong-resolvent convergence | Convergence of resolvents of self-adjoint operators | §6 |
| T0/T1/T2 | Proposed structural levels introducing total state, conjugation/phase, subsystem/modular data | §4 |
| Task | Target function/distinction t(X) to be recovered | §5.3, §8 |
| Tensor factorization | Decomposition of a Hilbert space into subsystem factors | §9.2 |
| Test run | Execution of a test suite; separate from the suite as a code artifact | §1.1, §1.4 |
| Total variation | Nonnegative measure of absolute signed mass, distinct from signed total | §7.1 |
| Under-determined | More than one inequivalent outcome remains compatible with current assumptions | §2.2 |
| Unit of information | Bits or nats, dependent on logarithm base | §5.2-5.3 |
| Version/release | Identifier scoped to one artifact series; never global by default | §1 |
| Wilson regulator | A specific lattice regularization with model/parameter-dependent artifacts | §9.3 |
---

## 14. Reference list and source handling

1. **Legacy reference source:** *Foundations of R v1.5: Glossary and Methodology*, final local Markdown snapshot preserved under `legacy_sources/`. Historical status labels in that snapshot are not a current release ledger.
2. **Jiaxuan Chen**, *Convergence of local modular data for half-line free fermions and a locality/passband obstruction to raw fixed-cutoff global quasi-equivalence*, Zenodo record 21717255, v2, published 31 July 2026. Official record and correction notes: https://zenodo.org/records/21717255. The PDF could not be fetched in this edition; proof details are not marked as fully reviewed.
3. **Abbas Edalat**, *Finite-Precision Algebraic Quantum Field Theory: Quantum Parcels, Locality, Modular Structure and Factors*, arXiv:2607.24445v2, submitted 27 July 2026, revised 29 August 2026. Official HTML: https://arxiv.org/html/2607.24445. Appendix B, Lemma B.1 was inspected for fixed-algebra relative modular continuity.
4. **Vincenzo Morinelli, Gerardo Morsella, Alexander Stottmeister, Yoh Tanimoto**, “Scaling Limits of Lattice Quantum Fields by Wavelets,” *Communications in Mathematical Physics* 387, 299-360 (2021), DOI: https://doi.org/10.1007/s00220-021-04152-5.
5. **Tobias J. Osborne and Alexander Stottmeister**, “Conformal Field Theory from Lattice Fermions,” *Communications in Mathematical Physics* 398, 219-289 (2023), DOI: https://doi.org/10.1007/s00220-022-04521-8.
6. **H. Casini, C. D. Fosco, and M. Huerta**, “Entanglement and alpha-entropies for a massive Dirac field in two dimensions,” arXiv:cond-mat/0505563v2 (2005), https://arxiv.org/html/cond-mat/0505563v2, especially Eq. (48) for the short-distance entropic c-function.
7. **H. Araki**, “Relative Entropy of States of von Neumann Algebras,” *Publications of the Research Institute for Mathematical Sciences* 11(3), 809–833 (1976), DOI: https://doi.org/10.2977/PRIMS/1195191148.
8. **H.-J. Borchers**, “The CPT-theorem in two-dimensional theories of local observables,” *Communications in Mathematical Physics* 143(2), 315–332 (1992), DOI: https://doi.org/10.1007/BF02099011. The 1992 CMP citation belongs to this title; use its stated hypotheses for modular covariance and positive-energy consequences.
9. **H.-W. Wiesbrock**, “Half-sided modular inclusions of von Neumann algebras,” *Communications in Mathematical Physics* 157 (1993), 83-92. Foundational HSMI reference.
10. **H. Araki and L. Zsidó**, “Extension of the structure theorem of Borchers and its application to half-sided modular inclusions,” *Reviews in Mathematical Physics* 17 (2005), 491-543; preprint https://arxiv.org/abs/math/0412061.
11. **C. J. Fewster**, “The split property for quantum field theories in flat and curved spacetimes,” arXiv:1601.06936, https://arxiv.org/abs/1601.06936.
12. **M. Takesaki**, *Theory of Operator Algebras I* and *II*. Standard reference for modular theory and von Neumann algebras.
13. **Claude Cross-check Packet 2**, cited by the supplied report as `Foundations_of_R_Claude_Crosscheck_Packet_2.zip`. This artifact was not located in the available files for the current edition. No result attributed solely to that packet is certified by this document.
14. **MIT OpenCourseWare**, *6.441 Information Theory (Spring 2016): Lecture Notes*, especially the chapters on mutual information/data processing and Gaussian-channel capacity. https://ocw.mit.edu/courses/6-441-information-theory-spring-2016/resources/lecture-notes/

The existence of a citation means that a source is relevant, not that its theorem proves a claim about R. Every load-bearing citation needs a sentence connecting its hypotheses to the R model and noting any missing bridge.

---

## Appendix A. Model-selection contract template

The following nine fields are mandatory before an R-specific source/task/readout claim can be evaluated. Empty fields are an explicit stop condition, not invitations to invent a default.

```json
{
  "contract_id": "FR-MSC-<stable-id>",
  "state_space": "UNSPECIFIED_FOR_R",
  "source_distribution_or_uncertainty_model": "UNSPECIFIED_FOR_R",
  "target_task": "UNSPECIFIED_FOR_R",
  "candidate_readouts_or_channels": "UNSPECIFIED_FOR_R",
  "admissibility_and_resource_constraints": "UNSPECIFIED_FOR_R",
  "selection_criterion": "UNSPECIFIED_FOR_R",
  "falsification_conditions": "UNSPECIFIED_FOR_R",
  "physical_interpretation": "UNSPECIFIED_FOR_R",
  "evidence_mapping_formal_objects_to_R": "UNSPECIFIED_FOR_R",
  "selection_status": "UNSELECTED"
}
```

The mathematical retention contracts can be applied after these fields are populated. They do not populate them by themselves.

## Appendix B. Research run record template

```yaml
run_id: FR-RUN-YYYYMMDD-AREA-NNN
research_release_id: FR-RR-vX.Y
purpose: <predeclared decision the run informs>
inputs:
  - path: <relative path>
    sha256: <hash>
code:
  - path: <relative path>
    sha256: <hash>
environment:
  python: <version>
  platform: <OS/architecture>
  packages: <lockfile or explicit versions>
parameters: {}
random_seed: <value or not-applicable>
commands: []
exit_codes: []
outputs: []
checks_and_thresholds: []
known_limitations: []
status: <passed|failed|partial|timed-out>
```

## Appendix C. Correction record template

| Field | Required content |
|---|---|
| Correction ID | Stable identifier |
| Former claim | Exact former wording and artifact reference |
| Corrected claim | Narrowest supported replacement |
| Reason | Mathematical error, scope overreach, source mismatch, data/control error, or naming ambiguity |
| Evidence | Proof, source section, test, or counterexample |
| Downstream impact | Claims, plots, abstract statements, and release statuses affected |
| State | Corrected, withdrawn, pending, or reinstated after new verification |

## Appendix D. Contributor and correction register

### D.1 Persistent contributor records

| Contributor ID | Contribution record | Evidence and boundary |
|---|---|---|
| `FR-CONTRIB-KIRTUS-JUSTUS` | **Kirtus Justus**: Foundations of R programme materials, source artifacts, terms, hypotheses, and project-level decisions represented by the supplied research files | Attribution applies to the project materials and decisions recorded here. It does not assign authorship of external scholarship or settle the scientific status of open claims. |
| `FR-CONTRIB-CLAUDE-CC3` | Packet 3 cross-check; T2 finite-source CSV, generation/verifier scripts, qubit partition verifier, model-selection contract and run record; P5′ raw Wilson and staggered datasets, supporting scripts, logs and run record; correction proposal CSV | The source ZIP is preserved byte-for-byte. This entry attributes the packet and artifacts as labelled; it does not authenticate the real-world identity of an individual or imply endorsement of R’s physical interpretation. |
| `FR-CONTRIB-LEGACY-V42` | v4.2 reconciliation audit, small-μ free-Dirac first-law derivation, modular/cocycle scope notes, and typed T–D dependency table | Source artifact preserved under `legacy_sources/`; historical code/run caveats remain active where listed. |
| `FR-CONTRIB-CHATGPT-ED12` | External-source checks, numerical recalculation, correction integration, test and release-chain execution, writing integration, and publication validation for `FR-MG-ED-1.2` | AI-assisted verification/editorial work. Not originator of the underlying R research programme or cited publications, and not an endorsement of open physical claims. |
| `FR-CONTRIB-LITERATURE` | Cited external papers and books | Each named work is attributed to its published author(s). Citation indicates relevance only, not participation in this project or endorsement. |

### D.2 Applied correction records

The source correction file is preserved unmodified at `contributions/packet3_correction_records_as_received.csv`. The current disposition is recorded in `correction_registry.csv`. The corrections below are applied to this edition where they concern citation labels, explicit conventions, missing ledger entries, and scope statements.

| Correction ID | Subject | Disposition in Edition 1.2 |
|---|---|---|
| `FR-CORR-MG-001` | Edalat Appendix B label and part (iv) scope | Applied: all load-bearing references say **Lemma B.1**; fixed-algebra and fixed-time strong convergence is distinguished from operator-norm, uniform-time, and varying-algebra claims. |
| `FR-CORR-MG-002` | Borchers 1992 CMP title | Applied: corrected to “The CPT-theorem in two-dimensional theories of local observables,” CMP 143(2), 315–332 (1992), DOI recorded. |
| `FR-CORR-MG-003` | Osborne–Stottmeister bibliography | Resolved from publisher metadata: *Communications in Mathematical Physics* 398, 219–289 (2023), DOI 10.1007/s00220-022-04521-8. |
| `FR-CORR-MG-004` | Small-μ free-Dirac relative-entropy coefficient | Applied with conditional scope: coefficient `+1/6` for the declared same-interval free-Dirac comparison and fixed-cutoff ordering; not a universal GMA theorem. |
| `FR-CORR-MG-005` | Modular KMS sign convention | Applied: convention and reversed-flow sign are written in Sections 4.4 and 5 glossary. |
| `FR-CORR-MG-006` | Finite-dimensional unitary representation statement | Applied: restrict the obstruction to connected noncompact simple Lie groups; noncompact abelian counterexample noted. |
| `FR-CORR-MG-007` | Typed T–D dependencies | Applied as a typed dependency ledger in Section 4.6; does not identify a physical model or derive the scheme from T labels. |
| `FR-CORR-CL-001` | No-scale function and Completion A | Retained correctly: exact scale invariance with oddness and endpoint limits gives the discontinuous sign function; in the continuous class the candidate set is empty. It is not the smooth `{tanh}` singleton from v6.1. |
| `FR-CORR-CL-002` | Qubit Gibbs “second completion” | Retained as rejected for the ordinary unordered qubit: the supplied verifier finds identical entropy/modular-spectrum partitions (13 classes). |
| `FR-CORR-CL-003` | Edalat source identification | Applied: Abbas Edalat and the official HTML source are identified; Chen and Edalat are kept separate. |

### D.3 Run and data records

| Run ID | Artifact | Reproduced observation | Boundary |
|---|---|---|---|
| `FR-RUN-20261018-T2-001` | `evidence/packet3/t2_source/` | 180 equiprobable states; both modular-spectrum and entropy readouts induce 120 classes, with 60 pairs and 60 singleton fibers; `I = log₂(180) − 2/3` bits | Constructed finite source only; `selection_status = UNSELECTED`; no mapping to R established. |
| `FR-RUN-20261018-P5P-001` | `evidence/packet3/p5prime/` | Raw Wilson values and adjacent slopes reproduce; independent staggered fixed-x sweep shows declining slopes | Finite sequences only. `L=48` attempted point excluded by negative spectral margin at the reported precision/quadrature; no continuum-divergence proof. |
| `FR-AUD-20261018-MG-ED12-001` | Edition-level QA outputs under `audit/outputs/` | Manifests, finite-model verifiers, source citations, tests, document renditions and packet construction checked | Verification applies to listed artifacts and commands only; it does not certify the full R physical theory. |

### D.4 Current scientific gate

Origin remains open/under-typed. The R-specific source/task/observable model remains `UNDERDETERMINED`. Observable selection remains `UNSELECTED`. The T2 candidate stays a declared finite construction. The P5 fixed-μ asymptotic/continuum question and P5′ norm-convergence/continuum question remain open. The Chern-edge embedding package is not specified, and Chen’s PDF proof-level review remains open because the hosted PDF could not be retrieved during this audit.
