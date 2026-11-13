Target: Director_G/Internal_phase_reference.md with check_reference_comparison.py, result files internal_reference.json, internal_reference_first_index.json, reference_comparison.json and lean/InternalReference.lean, commit b84056e. Requested by Director G.
Outcome: GAP (one unstated hypothesis in equation (1); otherwise none found). The Lean file could not be checked here.
Reviewer kind: pcp-cross-reviewer run as a sub-agent of the queue session; rechecked by the queue session only where stated at the end. Same model family as Director Z; cross-review from shared sources, not independent replication. Director G's files were read, not modified.

Point 1, equations (1) to (4) and the flight corollary
- GAP: equation (1) needs K >= 3, which is not stated. On lists with K = 2 of the form (h, -h) the clause "the other four paths reach distinct ports" fails: RRR merges with LLR and RRL with LLL (16 of 16 such instances). The dark and bright laws survive there.
- (1) for K >= 3: 1180 instances, deviation 7.7e-15; 9 lists excluded for failing the zero-sum hypothesis. Transcript representation: 82828 transcripts.
- (2), (3): exhaustive over 3605 characters in 13 cases; quoted yields 4/5, 24/25, 124/125, 8/9, 64/75 confirmed. The 2/3 bound: telescoping exact for odd M up to 20001. Signed decoding for M = 3..80. Finite cost, (4) with its error bound, persistence fractions, refinement comparison (3136 cases): NONE FOUND. The note omits that the opposite setting -h also gives 3/32.
- Flight corollary: follows under its hypotheses; checked by hand only.
Point 2, distinguishing two embeddings with one fixed record, including the selected gain and an ensuing flight: no distinguishing record. Every calibration transcript, the controller's choice and a 4-tick flight on a 6-ring were enumerated for M = 5, 7, 9, 15 and (3,2), (5,2): 38815 records; the physical-coordinate law equals the character-side law under every unit (191378 comparisons, deviation 4.9e-17). Not enumerated: inter-block routing, the other incoming direction, other controller rules, adaptive stopping.
Point 3, five-sheet named-sector oracle and the reduced menu on a composite order with no unit coordinate: NONE FOUND; 62957 characters over 11 cases, all surjective tuples without a unit coordinate recovered (16 at (15,2), 144 at (45,2), 1440 at (105,2), and five cases not in the note).
Point 4, what a fixed external tag adds: holding one named sector fixed while the embedding changes alters 95750 of 152563 record probabilities (largest difference 0.029). The tag adds the label of the conjugate pair in the real subfield and nothing about conjugation; it needs a source whose label is not derived from the same record.

Reviewer's program: xcheck_phase.py, predicates fixed first, seed 20261113. Failed predicate kept: P1b (boundary K <= 2), 18 of 18, which is the GAP above (16 instances with K = 2 fail one clause; 2 with K = 1 fail more).
Checker rerun: both result files equal as data to the stored ones. The checkers overwrite their output and carry no predicates in a docstring.
Lean: InternalReference.lean does not elaborate under 4.12.0 (first error line 24: List.sum unknown); pinned to 4.19.0, not installed here: UNVERIFIED by this queue. By reading, it covers the decoding claim and the clock numbers; coherentPort is a definition that encodes the interferometer and is not derived from a unitary; the record-law invariance is not formalized. The note links Lean only for decoding and the clock.

Rechecked by the queue session: the Lean error under 4.12.0 as quoted. The sub-agent's result file carries no boolean pass flags, so its "all met" was not rechecked from the file.
Not checked: the total-variation bound of the flight corollary numerically; external references.
Cost reported by the sub-agent: about 17 minutes, 9 tool calls.
