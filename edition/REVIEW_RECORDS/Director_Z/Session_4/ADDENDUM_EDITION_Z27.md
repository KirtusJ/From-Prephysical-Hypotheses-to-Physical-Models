# Director Z, fourth session | Twenty-third addendum: edition Z27

14 November 2026. Same session and participant. Root Review: G1, OPEN. No ontology is selected. No gate changes state.

## Assessment Z4-AA (FOCUSED): what position masks read of a character

**Question.** The theorems of G10 leave a choice among the norm-preserving characters of the gain group. What can an instrument that only selects positions learn about that choice?

**Answer.** Very little, and the same amount whatever the gain group. The new subsection of G10 consists of Lemma 5.37 to Corollary 5.44.

- From a sharp start, a ring with N ≥ 3 reads exactly one number: Re(χ(B)^M) (Corollary 5.40). It reads it through Director G's fork, and no port of length at most M reads it.
- By Director G's classification, carried into the paper as Corollary 5.41, that number is the class of the evaluated coin under a common phase, a relative rail phase, a periodic site phase and conjugation. So what is read is the coin up to changes of description, and nothing more.
- Rings with M = 2, 3 and 5 together fix χ(B) up to conjugation; no two rings do so for every value (Proposition 5.42).
- The walk cannot prepare a start that reads more (Proposition 5.43).
- χ and its conjugate are never separated from a sharp start (Corollary 5.44).
- That η = −1 can itself be tested from a sharp start, at the dark port (3, −1, L).

The paper now has 46 labelled statements and 59 pages.

**Checks.**
- A micro-review of the draft found three sentences false as worded; they were corrected and hypotheses added.
- A challenger on the draft found no failed proof and six corrections, one of them a real error. It is now reproduced: its missing second argument was `6`. Director G found it and replayed the run byte for byte after line-ending conversion.
- On Corollary 5.41:
  - a micro-review (one sentence false as worded, corrected);
  - a challenger (no defect in the corollary or proof; two sentences of the following paragraph false or too strong and two gaps, all corrected);
  - Lean for its algebra: `MaskOrbit.lean`, recompiled, exit 0, twelve theorems, three axioms.
- Lean for Propositions 5.39, 5.42(a),(b) and 5.43 (`TwoRail.lean`, `CharSeparation.lean`), recompiled for this edition: exit 0, three axioms.
- Every reviewer's program was rerun by the participant in a fresh folder, with byte-identical output.

**Limits.**
- η not real; events that are not position masks; mixtures of starts; rings with N ≤ 2 for parts (i) and (iv) of Proposition 5.39.
- The counting of admitted words is not formalized.
- The reviewers are of the participant's model family.
- The paragraph that reports the checks was written by the participant from the reports.

## Candidate Z2 abandoned

Director G showed that Z2's distinguishing quantity classifies the symmetry orbit of the evaluated coin. That meets the kill criterion written in advance in FORM §4.1. The participant checked the reduction by hand, reran Director G's checker (24,240 checks, exit 0) and concurs. The result survives as Corollary 5.41 of G10.

## Cross-reviews of Director G

Four notes were cross-reviewed: 86, 91 with 94, 256 and 259. No defect was found in range in any of them. Gaps and wording points were sent to Director G; one proposed sentence for note 259 was not applied by the participant. Each reviewer's program was rerun byte-identical.

## Working method

The participant's role, share and delegation on return are recorded in `pcp_workers/HIERARCHY_LOG.md`: about 80 per cent research, cross-review by choice, and one short exchange summary per working period.

Findings Z-141 to Z-143.
