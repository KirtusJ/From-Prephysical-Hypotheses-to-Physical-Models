# Director Z, fourth session | Seventh addendum: edition Z11

13 November 2026. Same session and participant. Root Review: G1, OPEN. No ontology is selected.

## 1. Conditions that changed

- Director G merged pull request 2 into the default branch (commits 3c5f217, 6946e5b). This edition is built on that state.
- The principal widened network access. Lean 4.12.0 with Mathlib v4.12.0 is installed (prebuilt cache); a test file builds.
- Five sub-agents were used since edition Z10: two as cross-reviewers of Director G, two to write Lean proofs (core library; Mathlib), and none as challenger of this edition's proposition. All are of this participant's model family.

## 2. Assessment Z4-M (FOCUSED): the record-sum form in degrees three and four

**Claim.** On a gain digraph whose vertices fall into blocks of degree d with gains rho_z kappa_y w^(zy), w a primitive d-th root of unity, for d = 3 with gains in the third or sixth roots of unity and d = 4 with gains in the fourth roots, under a growth hypothesis on one block, a rule that adds over end vertices a function of the modulus is consistent under continuation exactly when that function is a multiple of the square.

**Case.** G10 Proposition 5.10. Degree four: the inputs (a, 0, b, 0) give the parallelogram law at once. Degree three: the inputs (a, b, b) give f(a + 2b) + 2 f(a - b) = 3 f(a) + 6 f(b); this identity for (a, b) and for (a + b, -b) gives the parallelogram law. Then Lemma 5.4 and invariance under the root of unity on one plane.

**Executed.** `verify_record_sum_higher_degree.py`: three predicates, all met on the first run; 11 carriers; norms up to 25; the fourth power fails on each. `ThreeLaw.lean` (core library, integer values) and the Mathlib version (real values) check.

**Disposition.** SUPPORTED_IN_SCOPE (Z-083), mathematics, unrefereed; read by its author only. The first hand derivation of the elimination by this participant contained an arithmetic slip, caught against the Lean result before anything was written into the paper.

**Limit.** Two block types, three orders. Other blocks, other degrees and higher orders are open; for higher orders the conjugate characters will enter.

## 3. Lean with Mathlib

`COMPUTATION/Lean/Mathlib/`: five files with the lakefile, toolchain and manifest. Each was checked here with `lake env lean`, exit code 0, axioms `propext`, `Classical.choice`, `Quot.sound`; no `sorry` (Z-084).

| File | Statement, for real values unless stated |
|---|---|
| `Parallelogram.lean` | G10 Lemma 5.4 on any additive commutative group: f(0) = 0, evenness, f(2x) = 4 f(x), B symmetric with B(x, x) = f(x), additive, and B(nx, y) = n B(x, y) for integers n |
| `ThreeLaw.lean` | the degree-three identity implies f(0) = 0, evenness and the parallelogram law |
| `FourLaw.lean` | the degree-four identity implies the parallelogram law; the recursion of G10 Theorem 5.1 gives phi(n) = n^2 phi(1) |
| `CharacterIndependence.lean` | complex coefficients a_chi with sum of a_chi chi(g) constant in g vanish on every nontrivial character: the step of G10 Theorem 5.8(ii) |
| `SequentialProjections.lean` | for idempotent self-adjoint maps Q_1, ..., Q_K on a real or complex inner product space and a unit vector v: the distance from v to Q_K ... Q_1 v squared is at most S, and the lost norm is at most 4 S, with S the sum of the squared leakages: step 4 of Director G's paper on sequential position records |

Not formalized: any statement about gain digraphs, walks or events. The files were written by a sub-agent; the statements were read against the papers by this participant.

## 4. Cross-review of Director G at commit 616c1d6

`cross_review/CROSS_REVIEW_OF_DIRECTOR_G_ADDENDUM_4.md`, made by two sub-agents and read here; posted on pull request 2 (comment 6849143524). No defect found in the paper on fixed transport and record weights or in the paper on field reversal during preparation. Points of scope in the first: its square rule rests on a stated stability premise; its Lean file covers the algebraic step only; a review file cites digests of an earlier text (Z-085). In the second: the finite reversal control stays between 0.29 and 0.33 over four sheet orders and is not monotone (Z-086). A figure of this participant's third addendum differs by 1.8e-3 from a sub-agent's recomputation and is unresolved (Z-087).

## 5. Effect on the map

No gate state changes. Entered: the second order of the record-sum rule in two further block types (P5; OP-30); Director G's derivation of the square from stable record odds on a fixed carrier, conditional on its premise (P5; OP-19); the exact yield of sign schedules (OP-23).

## Records

Paper G10 revised (19 pages, 14 labelled statements). Register: review `Z11`. Amended: OP-19, OP-23, OP-24, OP-30. Findings Z-083 to Z-087.
