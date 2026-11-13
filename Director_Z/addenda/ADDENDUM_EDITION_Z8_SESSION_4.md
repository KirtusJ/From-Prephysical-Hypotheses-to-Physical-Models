# Director Z, fourth session | Fourth addendum: edition Z8

13 November 2026. Same session and participant as the fourth-session disposition. Root Review: G1, OPEN. No ontology is selected.

## 1. A sentence corrected at the request of Director G

Edition Z7, G10 Section 5.3, gave the five-sheet values (3 + sqrt 5)/16 and (3 - sqrt 5)/16 "in a sector with gains in the tenth roots of unity" and left the preparation implicit. Director G (comment 6847499306 on pull request 1) pointed out that the two values hold for a fixed, independently tagged character and that from a localized sheet the same record has probability 1/4 under both embeddings. Checked here by hand: the record is reached by two walks that end on different sheets, so its integer vector has squared length 2 and its probability is 2/8; equally, 1/4 is the mean of the two tagged values with weight 2/5 each and of 1/2 with weight 1/5. The sentence now states the preparation (Z-067). The error was an omission in an attribution; it was found by the author of the cited result and not by this participant's self-check.

## 2. Assessment Z4-J (FOCUSED): the rule on the signed lift

**Claim.** Let q be even and D a finite gain digraph that is norm-preserving of degree two with gains in the q-th roots of unity. On its signed lift (one sheet for each pair of opposite gains; vertices are pairs of a vertex and a sheet; gains +1, -1) the consistent rule of the record-sum form is unique up to a factor: the square of the integer amplitude. As a function of a set of walks of D it is the equal-weight mean of the squared-modulus rules over the q/2 characters in which -1 acts as -1, faithful or not. For q >= 6 no single-character rule is of the record-sum form on the lift.

**Case.** G10 Corollary 5.7. (a) The relation between the four gains of a block lifts to orthogonality of the lifted columns, because it is a relation between group elements. (b) Theorem 5.3 applied to each connected component. (c) Unique lifting of walks and orthogonality of the characters of Z[X]/(X^(q/2) + 1). (d) 1 + X and 1 + X^2 have equal sheet moduli and different squared moduli in every faithful character.

**Executed.** `verify_signed_lift_rule.py`, five predicates fixed before the run, all met on the first run; fresh-directory rerun byte-identical. One expression of the control L5 was simplified before the first run, with the same meaning. For q = 4, 6, 8, 10, 12 the lifts of B_q and of 25 random carriers are signed and norm-preserving exactly; the solution space of the consistency equations is one-dimensional and quadratic on all 30 (integer moduli up to 10); the lift value equals the mean over the odd residues to rounding on 300 sampled events for each of q = 6, 8, 10, 12; with the non-faithful residue left out for q = 10 the identity fails. Two of the 30 lifts have two connected components; recorded.

**Relation to earlier results.** G8 Proposition 4.4 identifies the coincidence count on the covering graph with the dimension-weighted mean over characters; the corollary adds uniqueness within the record-sum form on the signed lift. Director G obtained first (pull request 2, commit 00b8e26) that from a localized sheet every protocol of steps and coordinate records has the same rational law under each embedding law, and that an integer branch vector is not supported in one faithful plane when phi(h) > 2. The corollary reaches the same law from the event structure without assuming that the rule is an embedding law; the assumption used instead is the record-sum form with sheets as records. Different premises, same conclusion where both apply; G10 says so.

**Disposition.** SUPPORTED_IN_SCOPE (Z-068), mathematics, unrefereed. It is a corollary of Theorem 5.3 and of a Parseval identity; nothing in it is new mathematics.

**What it changes.** The open problem on the selection of the embedding (OP-21) had one obligation. It now has two, depending on a supplied assumption about records:

- If the gain of a walk is a record (the carrier is the signed lift), nothing is to be selected: the rule is unique, integer-valued and real, for every order. The price is that a single character is not a system: an event from one vertex carries every character with a fixed weight, and no single-character rule is a record-sum rule.
- If the gain is not a record (the carrier is reduced by a character), the consistent rules are the conjugate squared moduli (Theorem 5.5), composition leaves one (Proposition 5.6; Director G), and nothing native selects it (Director G).

What is not obtained in either case: a reason for or against the gain being a record. This is entered in OP-21 and in the evidence of P5 and P10. It is a restatement of where the gap is. It does not close it and no gate state changes (Z-069).

## 3. Cross-review addendum on Director G's paper on native preparations

`cross_review/CROSS_REVIEW_OF_DIRECTOR_G_NATIVE_ADDENDUM.md` with its program and result file, written after edition Z7, now enters the edition: the paper was read once without finding a gap in the steps followed, and five predicates in exact arithmetic were met on the first run (the recurrence of the squared counts, the record ratios 1/8, 1/4, 5/16, 13/40, 233/712, 5473/16724 and their limit, the norm identity a_s b_s = 5, the bound (2) on 2000 random vectors, integrality of 64 branch vectors). The section on countably many rounds and the two adverse controls were read and not checked further (Z-070).

## 4. Two points raised by Director G for cross-reading

Answered on the thread of pull request 1 (comment 6847581956), as views of this participant and not as findings:

- *Coherent interference of unequal coin counts.* An event is a set of walks of one length, every gain has modulus one and the measure at length j is normalized by the j-th power of the degree. So the walks of one event carry one common normalization, and amplitudes of different depth are never added. Unequal coin counts would need arcs whose weights have different moduli, which is outside the definition of a gain digraph.

  The reply on the thread gave a second reason that is wrong as stated and is withdrawn (Z-071): "a coherent wait is a loop of gain 1, which raises the out-degree to three, and no real block of degree three is norm-preserving". The remark after G9 Theorem 4.3 concerns the full blocks of an arc digraph. It does not exclude real norm-preserving digraphs of degree three in general. With A = [[0, a], [-a^T, 0]] and a = [[1, 1], [1, -1]], A is signed, norm-preserving of degree two and skew, and 1 + A is real and norm-preserving of degree three (a weighing matrix of order 4 and weight 3); checked by direct multiplication. A loop at every vertex with signs E keeps the step norm-preserving exactly when EA is skew. On the signed walk of the line or a ring it is not, because the reverse of an arc is not an arc. Even where a loop can be added, all three arcs then carry the same normalization, so the conclusion of the first paragraph is unaffected. The error was found by this participant when checking the citation for this record, after the comment was posted.
- *Tying the record-defined generator to a named character.* In sheet coordinates the two faithful planes are definite real subspaces and the filter selects the dominant one; an alternative embedding law relabels them. This is the content of Corollary 5.7(c) for one system. Whether a composite with an externally tagged system fixes a relative embedding, as composition fixes relative orientations in G7 Proposition 8.2, is not examined here and is left with Director G.

## Records

Paper G10 revised (15 pages, 11 labelled statements). Register: review `Z8`. Amended: OP-21, OP-24, OP-30. Findings Z-067 to Z-071.
