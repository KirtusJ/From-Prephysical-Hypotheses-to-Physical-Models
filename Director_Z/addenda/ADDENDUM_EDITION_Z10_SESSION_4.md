# Director Z, fourth session | Sixth addendum: edition Z10

13 November 2026. Same session and participant as the fourth-session disposition. Root Review: G1, OPEN. No ontology is selected.

## 1. Conditions that changed

- The principal stated that both directors may update the main repository, asked for Lean to be used where the environment allows, and asked for sub-agents to be used for the review stack.
- Director G merged the branch of this session into the default branch (pull request 1, merge commit 37efa56). This edition is built on that commit.
- Lean 4.12.0 was installed from its release archive (core library; Mathlib is not available here).
- Two sub-agents were used: one as challenger on the new theorem, one to write Lean proofs. Both are of the same model family as this participant, in fresh contexts. Their output was checked here before it was used.

## 2. Assessment Z4-L (FOCUSED): the kernel theorem in general form

**A defect of edition Z9.** Theorem 5.8 as printed assumed a carrier norm-preserving "for the faithful character". A group that is not cyclic has none, so the theorem did not apply to two sheet registers, although its proof did. Found by this participant when answering Director G (Z-077).

**Claim.** Let C be a finite abelian group and D a gain digraph with gains in C in which every vertex has d successors. Let X(D) be the set of characters for which the step matrix satisfies A*A = d. (i) Every real combination of the kernels Re chi, chi in X(D), gives a pair rule consistent with factor d. (ii) If for every two distinct vertices with a common successor the quotients of gains of walks of one length to them take every value of C, a pair rule that is not identically zero and is consistent has factor d and such a kernel. In degree two with a block relation u4/u3 = eps u2/u1, X(D) is the set of characters with chi(eps) = -1.

**Case.** G10 Theorem 5.8 and Corollary 5.9. For two walks ending at vertices with common successors Z and quotient g, the continued event has measure 2d f(1) + 2 sum over Z of f(g r_z); the sum is the entry of A*A for the two vertices, expanded in characters; independence of the characters in g gives c_chi (A*A)_{y1 y2} = 0.

**Executed.** Three programs.

| Program | Predicates | Outcome |
|---|---|---|
| `verify_kernel_rules_general.py`, 40 carriers in four families | 4 | 3 met; the fourth, a minimum of three carriers with the hypothesis in each family, failed for the two-register family (2 of 4) |
| first follow-up, 12 small two-register carriers | 3 | 2 met; the minimum of six with the hypothesis failed (1 of 12) |
| second follow-up, 16 larger two-register carriers | 3 | 3 met (12 with the hypothesis, all with dimension 5) |

On all 47 carriers with the hypothesis the solution space is the span of X(D); on the others it is at least as large. The two failed predicates were coverage requirements set by this participant; small carriers do not generate a group of rank two. Both are kept.

**Challenger.** `challenger/CHALLENGER_REPORT.md`. No counterexample on about 2500 carriers by its own program; four gaps in the wording of the corollary, each checked here and corrected: in-degree two and disjoint successor pairs stated; item (d) restricted to consistent kernel rules; "mu_f not identically zero"; the converse direction and a reused letter (Z-079). The first of these was a real omission: without it the claim about X(D) is false, as the challenger's carriers show.

**Disposition.** SUPPORTED_IN_SCOPE (Z-078), mathematics, unrefereed; read by a sub-agent with reduced exposure, which is not independent review.

**What it changes.**

- The classification of consistent pair rules no longer depends on the degree or on the group being cyclic. The open item "degrees above two" is closed for pair rules and stays open for rules of the record-sum form.
- "-1 acts as -1" is a feature of degree two. In degree three with gains in the sixth roots of unity the consistent characters are those of order three and six, in which the cube root acts faithfully, and the sign character is excluded. What consistency asks is that the step be norm-preserving in the character, nothing more specific.
- The tree, on which every rule is consistent, is the case in which no relation exists.

## 3. Lean

`COMPUTATION/Lean/`: three files, each checked here with Lean 4.12.0, exit code 0, depending only on the axioms `propext` and `Quot.sound`; no `sorry`.

| File | Statement |
|---|---|
| `SignedLineRecursion.lean` | phi(0) = 0 and phi(a+1) + phi(a-1) = 2 phi(a) + 2 phi(1) for a >= 1 imply phi(n) = n^2 phi(1): the recursion of G10 Theorem 5.1 |
| `ParallelogramInt.lean` | the parallelogram law on the integers gives f(0) = 0, f even, f(n) = n^2 f(1) |
| `ParallelogramGroup.lean` | G10 Lemma 5.4 for integer values on any abelian group: f(0) = 0, f(-y) = f(y), f(2x) = 4 f(x), and the form B(x, y) = f(x+y) - f(x-y) is symmetric, has B(x, x) = 4 f(x), and is additive in its first argument |

Limits (Z-080): the values are integers where the paper has real values; the combinatorial part of Theorem 5.1 (which events exist on the signed line) is not formalized; nothing else in the program is formalized. The files were written by a sub-agent and rechecked here; the statements were read against the paper by this participant.

## 4. Cross-review of Director G at commit 6bb2d14

`cross_review/CROSS_REVIEW_OF_DIRECTOR_G_ADDENDUM_3.md` with three programs and result files; posted on pull request 2 (comment 6848430165). Relative sheet transport: the sheet-operator statements hold exactly (Z-081). Sequential position records: the sequential-projection inequality and its use were followed without finding a gap; the adverse finite reversal control is explained by the momentum offset of the preparation; a quartered field schedule removes the offset in the runs made (Z-082).

## 5. Effect on the map

No gate state changes. Entered: the general classification (P5, P6); Director G's relative character on a carrier with a supplied schedule and a joint position-record law with a supplied pointer and clock (P9, P10; OP-21, OP-23).

## Records

Paper G10 revised (18 pages, 13 labelled statements). Register: review `Z10`. Amended: OP-21, OP-23, OP-24, OP-30. Findings Z-077 to Z-082.
