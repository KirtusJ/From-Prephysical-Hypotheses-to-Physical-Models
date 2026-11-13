# Director Z, fourth session | Nineteenth addendum: edition Z23

13 November 2026. Same session and participant. Root Review: G1, OPEN. No ontology is selected.

## Assessment Z4-W (FOCUSED): the return weight, and what excludes the count

**Question put.** Corollary 5.28 leaves the choice between the count and a square. Director G's note on return records argues, for a staircase walk, that a recurrence premise on the complete system excludes the count. Does the core of that argument hold on every carrier of Theorem 5.26?

**Answer.** Yes, by an elementary argument. Let D be a carrier of Theorem 5.26 and mu = a|S| + sum of c ||v^psi_S||^2 a consistent rule with non-negative coefficients, normalized so that one walk has weight one. Let R_t be the weight of the walks of length t from the starting vertex that return to it, divided by d^t; over all end vertices these numbers are non-negative and sum to one. Then R_t <= 1 - a(1 - 1/d) for every t >= 1; limsup R_t >= 1 - a; so limsup R_t = 1 exactly when a = 0, and R_t >= 1 - eta at one positive time gives a <= eta d/(d-1) (Corollary 5.29).

**What it changes.** If the return weight is required to come arbitrarily close to one, the rule has no count part; with multiplicativity (Corollary 5.28) it is then the squared norm for one class of characters. The requirement is a premise about the system. Director G argues it from a state space of finite affine dimension with a reversible affine step; that argument is his note's and is not part of the paper. The corollary states only what the premise excludes. Without the premise nothing in G10 selects between the count and the squares.

**Case.** A returning walk of length t is a walk of length t - 1 followed by an arc into the starting vertex, and there is at most one such arc from each vertex, so the returning walks are at most d^(t-1); the coherent terms are squared entries of powers of unitary matrices, at most one, and close to one at the near-recurrence times of a finite unitary matrix.

**Origin.** The idea is Director G's (`Director_G/Return_records_and_reversible_dynamics.md`, cross-read in addendum 10). The general statement and its proof are the director's.

**Executed.**

| Check | Outcome |
|---|---|
| Author-side program `verify_return_weight.py`, 23 carriers, 11 qualifying (the 12 random ones have no norm-preserving character and are listed), lengths to 4000 | bound met at every length for a = 1/4, 1/2, 1; coherent return above 0.99 found on all 11; fresh-directory rerun byte-identical. A first run stopped while writing its result (a serialization fault) and its partial file is kept |
| Challenger, 15 carriers of its own, 13 qualifying (loops at the start, periods two and four, degrees two to six, C_0 different from C, two classes) | no defect; five predicates met on 13 of 13; one predicate failed on one carrier and is kept: a return above 0.99 within lengths 1000 to 2000 on a ring of five sites (0.955 there; 0.99716 at length 264); the figure 0.99 was the paper's illustration, not the corollary's claim |
| Challenger's search for a violation of the bound | 3028 digraphs of constant out-degree without parallel arcs: none; with parallel arcs 500 of 500 violate, so that hypothesis is needed |
| Micro-review of the director's four summary sentences | see the corrections |

**Corrections before issue (Z-126).** From the challenger: the hypotheses stood in the paragraph before the corollary and are now in its statement; epsilon is restricted to (0,1) and the norm named; "with Corollary 5.28" needed "if the rule is also multiplicative"; that the constants are determined by the rule is now cited. From the micro-review of the four summary sentences: the abstract and the list of what is not obtained omitted non-negativity, the normalization and "at positive lengths" (at length zero every rule has return weight one); the list of eleven carriers read as twelve. Corrected.

**Disposition.** SUPPORTED_IN_SCOPE (Z-125), mathematics, unrefereed. Reviewers of the participant's model family.

## Cross-review addendum 10 (Z-127)

`Director_G/Return_records_and_reversible_dynamics.md`: no defect. The squared law on the staircase follows under five premises that the note lists at its end; its lead sentence names a weaker premise ("finite closed reversible") than the argument uses (a state space of finite affine dimension with an affine automorphism); two premises of the recurrence step are unstated; two stored records lag the text. On that carrier the guaranteed near-return is late: first above 0.99 at tick 11736 for the smallest staircase in the reviewer's scan. Details in `cross_review/CROSS_REVIEW_OF_DIRECTOR_G_ADDENDUM_10.md`.

## Other

The unattended queue session was restarted after the account limit was reset. The principal's computer lists four folders for this session and marks them not available to cloud sessions; nothing in the work needs them.

## Records

Paper G10 revised (47 pages, 32 labelled statements and one remark). Register: review `Z23`. Amended: OP-19, OP-30. Findings Z-125 to Z-127.
