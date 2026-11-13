# Director Z, fourth session | Eighth addendum: edition Z12

13 November 2026. Same session and participant. Root Review: G1, OPEN. No ontology is selected.

## 1. A defect of edition Z11

Proposition 5.10 as issued in edition Z11 did not require that the successor sets of different blocks be disjoint. Without it the direction "the square is consistent" is false: on four vertices with the blocks {0, 1} -> {0, 2} and {2, 3} -> {1, 2} and signs of the required form, A*A is not 2, an event of measure 2 continues to measure 6, and only the zero rule is consistent. Found by a challenger sub-agent working from the paper text; the matrix and the two measures were recomputed here. The same omission had been found by the earlier challenger in Corollary 5.9 before issue; it was not carried over to the next statement. The condition is now in Proposition 5.10 and in Theorem 5.11 (Z-088). REFUTED_IN_SCOPE for the statement as issued; corrected.

## 2. Assessment Z4-N (FOCUSED): Fourier blocks of any degree

**Claim.** Let d >= 2 divide q. On a gain digraph whose vertices fall into blocks with gains rho_z kappa_y w^(zy), w a primitive d-th root of unity, with disjoint successor sets and a growth hypothesis on one block, the consistent rules of the record-sum form are exactly the real combinations of the squared moduli in the conjugate characters: dimension phi(q)/2 for q > 2, one for q = 2. The degree plays no part.

**Case.** G10 Theorem 5.11. Even d: two inputs at columns 0 and d/2 give the parallelogram law. Odd d: the inputs (a, b, ..., b) give one identity; two instances of it give a law M_k with k = d - 2; three instances of M_k give the parallelogram law. Then Lemma 5.4 and the invariant forms as in Theorem 5.5.

**Executed.**

| Check | Outcome |
|---|---|
| `verify_fourier_blocks_any_degree.py`, 22 carriers, d = 3 to 6, q up to 12 | 1 of 3 predicates met; two carriers whose gains generate a proper subgroup lay outside the hypothesis, and the predicates did not test it; kept |
| follow-up with the hypothesis tested per carrier, 33 carriers | 4 of 4 met; dimension phi(q)/2 on all 33 |
| Lean with Mathlib, `MkGeneral.lean` | M_k implies the parallelogram law for every k >= 1, for real values on any commutative group, without assuming evenness; exit code 0, standard axioms |
| challenger sub-agent | the "only if" direction survived every check, on 28 further carriers including d = 7; the defect of section 1 in the "if" direction |
| micro-review of boundary cases | seven cases pass; two wording gaps (dimension for q = 2; odd q) corrected |

The proof first written here used a coprimality argument for two recurrences. The formalizer found that three instances suffice; the paper now gives that argument. The challenger had checked the earlier argument and found it correct as well.

**Disposition.** SUPPORTED_IN_SCOPE (Z-089), mathematics, unrefereed; examined by a challenger and a micro-reviewer of the participant's model family.

**What it changes.** Within the record-sum form the second order no longer depends on the degree for this family of carriers, and Theorem 5.5 is its case d = 2. What stays free is the same in every degree: the combination of conjugate characters.

## 3. Micro-reviews

At the principal's suggestion a lower tier of short, narrow reviews was added (three runs of one to two minutes each).

- *Corollary 5.7, edge cases.* Every case passes exactly (orders 2 to 12, loops, disconnected lifts, complete cancellation on a sheet). Three points of wording corrected: part (d) holds for every odd character; on a disconnected lift the factor is fixed per component; part (c) is stated from one sheet (Z-090).
- *Theorem 5.11, boundary cases.* Above.
- *Outlier scan* of 26 result files, 164 numeric columns. No predicate marked met contradicts its own numbers. Two values without an explanation are entered among the retained outliers: the band flatness at order 2 in the confinement run (2.5e-4 against a median of 3.3e-7), and one residual of the even characters (0.86 against 0.03 to 0.13) in the first kernel run (Z-091).

## 4. A figure resolved

Finding Z-087 (a difference of 1.8e-3 in a mean of the third cross-review) is resolved: the mean over sites x > 0 is 1.996575 and over x >= 0 is 1.994766; the site of the origin carries mass 4.5e-4. The addendum's figure used x > 0 (Z-092).

## 5. Method

`CLAUDE.md` at the root of the repository records the review stack (director, cross-director, challenger, formalizer, micro-review), the rule that a new statement gets all of them before issue, and the lessons of the session.

## Records

Paper G10 revised (20 pages, 15 labelled statements). Register: review `Z12`. Amended: OP-19, OP-24, OP-30. Findings Z-088 to Z-092.
