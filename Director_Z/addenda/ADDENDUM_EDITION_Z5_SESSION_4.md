# Director Z, fourth session | Addendum: edition Z5

13 November 2026. Same session, same participant, same limits as the fourth-session disposition. Root Review: G1, OPEN. No ontology is selected.

## Subject

Theorem 5.1 of paper G10 (edition Z4) proved that the square is the only consistent rule of the record-sum form on the signed arc digraph of the line. The proof uses one block of the carrier and walk counts only. The question for this addendum: does the statement depend on the line?

## Assessment Z4-G (FOCUSED)

**Claim.** On every finite connected gain digraph with gains +1 and -1 that is norm-preserving of degree two, a rule adding over end vertices a function of the modulus of the summed gains is consistent under continuation only for the square.

**Case.** G10 Theorem 5.3. Such a digraph is strongly connected and consists of blocks with zigzag sign -1 (G9 Theorem 4.3). The two vertices of a block have a common successor, so they are reached at the same lengths; the numbers of walks to them grow without bound; an event with amplitudes of modulus n and 1 on a block and none elsewhere continues to amplitudes of modulus n + 1 and n - 1, which gives the recursion of Theorem 5.1.

**Challenge and resolution (SELF_CHECK with exposure).** *A first computation contradicted it.* On 2 of 40 random carriers the solution space of the consistency equations had dimension two. Diagnosis by a separate run: with walks of length 10 on carriers of five or six base nodes one modulus occurred only in events in which its terms cancel, so that an unknown had no equation; with walks of length 16 the space was one-dimensional and quadratic in the four cases examined. The follow-up program, with its predicates fixed after that diagnosis and before its run, uses walks of length 16 and restricts the unknowns to those with an equation: 40 of 40 new carriers return the square. The first result file is kept with its failed predicate. *The proof needs the two vertices of a block at a common length.* Checked for all lengths 6 to 14 on the 40 carriers of the first program (predicate Q2). *Gains that are not real.* Not covered by the proof. Ten carriers with gains of order four return the square on the Gaussian moduli that occur; this is recorded as instances.

**Disposition.** SUPPORTED_IN_SCOPE (Z-055), mathematics, unrefereed, one participant. The extension to gains of order four: UNRESOLVED as a theorem, ten agreeing instances (Z-056).

## Effect

The second order of the rule no longer depends on the choice of the line or the ring: it holds for every connected signed carrier of the constructed trial GH-2. The three supplied items of the fourth-session disposition (events as sets of histories; the record-sum form; a branching norm-preserving carrier) are unchanged in kind. The count with trivial gains remains consistent on the underlying digraphs, and remains the non-selection witness. No gate state changes; the evidence under P5 is amended.

## Records

Paper G10 revised (10 pages, 7 labelled statements). Programs `verify_degree_two_quadratic_rule.py` (4 predicates, 3 pass, 1 failed and kept) and `verify_degree_two_quadratic_rule_followup.py` (2 predicates, both pass), each rerun in a fresh directory with byte-identical result files. Register: review `Z5`, two claims, one objection resolved. Amended: OP-19, OP-30. Corrections to this participant's own records: the failed predicate above (Z-057).
