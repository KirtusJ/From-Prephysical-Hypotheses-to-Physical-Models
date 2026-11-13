# Director Z, fourth session | Eleventh addendum: edition Z15

13 November 2026. Same session and participant. Root Review: G1, OPEN. No ontology is selected.

## Assessment Z4-P (FOCUSED): when the gains are abundant

**Question.** Corollary 5.13 assumes that every gain reaches both vertices of a merging pair in abundance at one length. Does this follow from finiteness and connectedness?

**Answer.** No, and the exact condition is known. For a finite carrier with A*A = d, d >= 2, whose derived digraph on pairs (vertex, gain) is strongly connected with period r, while the carrier has period r_0: the gains that occur at a vertex at one length form a coset of a subgroup C_0 of index r/r_0 (Proposition 5.14). All gains occur at one length exactly when r = r_0. In general the consistent rules of the record-sum form are the combinations of the conjugate squared moduli for the order q_0 of C_0 (Corollary 5.15); q_0 = q exactly when the periods agree.

**Origin and corrections.**

- The director's first version (strong connectedness of the derived digraph suffices) is false; a sub-agent found a four-vertex counterexample for order 4 and the corrected statement with its proof (Z-098).
- A challenger then found part (c) of the draft false for a character that is not faithful (example with the group Z_2 x Z_2), and three omissions: why r_0 divides r; that the coset statement is for one length and one starting vertex; and that carriers whose gains generate a proper subgroup need the subgroup in place of the group. All corrected before issue (Z-099).

**Executed.**

| Check | Outcome |
|---|---|
| `abund_v2.py`, 660 random carriers of degrees two to four | hypotheses hold on 483; the corrected statement holds on all of them; the naive one fails on exactly the 130 with r != r_0 |
| `abund.py`, first version | two predicates failed: the coset at the second vertex was inverted in the program; kept |
| challenger, 721 carriers | 473 with the hypothesis; every structural predicate 473 of 473; dimension phi(q_0)/2 on 472 at first pass and on the last after a larger sample, among them 110 with q_0 smaller than q |

**Disposition.** SUPPORTED_IN_SCOPE (Z-100), mathematics, unrefereed, not formalized.

**What it changes.** On a finite carrier with a strongly connected derived digraph the classification of record-sum rules needs no hypothesis on events. The order that enters is that of the gains that can meet at one length. The earlier observation that some random carriers have fewer consistent rules than the order of their gains suggests is explained, for carriers whose gains generate the whole group.

## Records

Paper G10 revised (24 pages, 19 labelled statements). Register: review `Z15`. Amended: OP-30. Findings Z-098 to Z-100.
