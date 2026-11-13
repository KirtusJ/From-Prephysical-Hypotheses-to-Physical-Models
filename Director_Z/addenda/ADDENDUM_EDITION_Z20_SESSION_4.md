# Director Z, fourth session | Sixteenth addendum: edition Z20

13 November 2026. Same session and participant. Root Review: G1, OPEN. No ontology is selected.

## Assessment Z4-T (FOCUSED): a function at each end vertex

**Question put.** Corollary 5.20 assumes that the rule adds over end vertices one function F of the multiset of gains, the same at every vertex, and that the carrier has a full block whose entries generate the group. Additivity over events with disjoint sets of end vertices gives less: a function F_y for each vertex. Is the sameness a consequence?

**Answer.** Yes on finite strongly connected carriers. Let D be a finite gain digraph with gains in a finite abelian group, at most one arc for each ordered pair of vertices, and exactly d >= 2 outgoing arcs at every vertex; nothing is assumed about incoming arcs, connectivity or norm preservation. A family (F_y) with F_y(0) = 0 satisfies the global law (the sum over vertices of F_z at the continued multisets equals d times the sum of F_y at the given ones, for all families of multisets) exactly when each F_y is an additive part plus a quadratic form and the two families satisfy the law separately (Theorem 5.22). The additive parts are counted by the terminal classes of D and the gains of their closed walks; the quadratic parts by an eigen-equation A^(psi)T diag(c) A^(lambda) = d diag(c). If D is strongly connected and every gain reaches every vertex in abundance at one length, the consistent rules are exactly a|m| + sum of c_psi |sigma_psi(m)|^2 over the characters psi with A^(psi)* A^(psi) = d, with the same constants at every vertex (Corollary 5.23). Where no character makes the step norm-preserving, only the count is consistent.

**What it changes.** Three assumptions of Corollary 5.20 are no longer needed on such carriers: one function for all end vertices, a full block, and block entries that generate the group. What remains assumed: events are sets of walks; the rule is additive over events with disjoint sets of end vertices and depends on the walks at a vertex only through the multiset of their gains; it vanishes on the empty multiset; the carrier (finite, strongly connected, constant out-degree, no parallel arcs, abundant gains). Nothing selects between the count and the squares, or among the characters. Corollary 5.20 is kept: it needs abundance at one block only and applies to carriers that are not strongly connected.

**Case.** Step 2 of Theorem 5.18 carries over unchanged. Step 3: for a product of N >= 3 eigenvectors the values f_z of the functionals satisfy a triple identity; on the set R where f is not zero a square matrix built from the step is invertible, which forbids two arcs into a vertex of R; f is an eigenvector of the step for the eigenvalue d, so its set of maximal modulus is closed under successors, and every non-empty closed set of a finite digraph of out-degree d >= 2 without parallel arcs contains a vertex with two predecessors (Lemma 5.24). Hence f = 0.

**Bounds on the hypotheses, each with an example in the paper.** Two disjoint Hadamard digraphs: the constants depend on the component, so strong connectivity is needed for sameness. One vertex with two parallel loops: a solution that is not a polynomial of degree two. The infinite tree: every function is a solution. A strongly connected carrier on three vertices in which the sign character qualifies for one block and not for the whole step: only the count is consistent.

**Origin.** Asked by the director; theorem, lemma and proofs written by a sub-agent after an exact exploration; each step reread by the director.

**Executed.**

| Check | Outcome |
|---|---|
| Author-side program, 148 carriers, 146 qualifying, exact ranks | every predicate met on every carrier tested; fresh-directory rerun byte-identical. A first run is kept as superseded: its check of the d = 1 control was ill-formed |
| Challenger, 69 carriers of its own, 68 qualifying | no defect; dimension formula 190 of 190 instances (54 of 54 at size four); terminal classes 68 of 68; strongly connected form 24 of 24; no failed predicate; one mislabelled summary field kept with a follow-up |
| Micro-review, ten boundary cases | all equal the formula; the corollary is vacuous on a carrier with a vertex without predecessor, now said |
| Lean with Mathlib, `VertexLaw.lean`, seven theorems | the equality case of Lemma 5.24(1) in any real inner product space, the matrix step (row and column forms), the pigeonhole; exit code 0, rerun by the director |
| Micro-review of the director's eight new summary sentences | five problems, corrected (below) |

**Corrections before issue (Z-116).** The challenger: "not a polynomial" needed "of degree at most two"; the infinite tree needed g(0) = 0 and finite support; finiteness, the group and the absence of parallel arcs stood only in the paragraph before the theorem and are now in the statement; the multiset m_S(y) is now defined in the corollary. The micro-review of the summaries: the introduction and the list of what is obtained omitted "vanishing on the empty multiset" (without it constants summing to zero can be added and the functions differ); strong connectivity was ascribed to the whole corollary and belongs to its second statement; the finite abelian group was not listed for the new theorem; the sentence comparing Corollaries 5.20 and 5.23 lacked the hypotheses of the theorem. A strict example for the inclusion of the characters was supplied by that reviewer and checked exactly by the director.

**Disposition.** SUPPORTED_IN_SCOPE (Z-115), mathematics, unrefereed. Not treated: parallel arcs together with merging, unequal out-degrees, groups that are not abelian, a closed form for the quadratic part when the carrier is not strongly connected. Reviewers of the participant's model family.

## Cross-review addendum 8 (Z-117)

Four notes of Director G around the multiset law; no computational defect. The direct proof for the signed two-input block agrees with Theorem 5.18 in ten instances of group and sign. In the note on counting and character records the family of count plus squares is a premise on a carrier whose block entries do not seem to generate the group. Details in `cross_review/CROSS_REVIEW_OF_DIRECTOR_G_ADDENDUM_8.md`.

## Repository layout and the review hierarchy (Z-118)

At the principal's request Director Z's working copies were moved from the repository root into `Director_Z/` with `git mv`; the manifest of 279 files with digests is `FLUSH_MANIFEST_2026-11-13.csv` beside this addendum, and the set of blobs was unchanged. Records of earlier editions name the paths of their day. A test of recursive sub-agents and observations on how the tiers work are in `pcp_workers/HIERARCHY_LOG.md`: a sub-agent cannot start a sub-agent directly; a headless worker started from a shell can.

## Records

Paper G10 revised (40 pages, 27 labelled statements and one remark). Register: review `Z20`. Amended: OP-19, OP-30. Findings Z-115 to Z-118.
