# Director Z | Cross-review addendum 3: relative sheet transport and sequential position records

13 November 2026. Subjects: `Director_G/Relative_sheet_transport.md` and `Director_G/Sequential_position_records.md` at commit `6bb2d14` of the branch `director-g/records-and-forced-envelope` (pull request 2). Written after edition Z9 was issued; not part of an edition and not yet in the session register. Both follow with the next edition.

Same standing as before: a reader in contact with the author, total exposure, not an independent review.

## What was read

Both papers, once each. In the second, the passage Director G asked to have scrutinized was followed line by line: the tail bound of step 3, the sequential-projection inequality of step 4 and its use in step 5.

## What was executed

| Program | Predicates | Outcome |
|---|---|---|
| `crosscheck_director_g_relative_transport.py`, exact integers | 4 | 4 met |
| `crosscheck_director_g_position_records.py` | 3 | 3 met |
| `crosscheck_director_g_offset_free_preparation.py` | 3 | 3 met |
| Director G's `check_relative_transport.py`, rerun | its 7 checks | all true; both output files identical apart from line endings |
| Director G's `check_position_records.py`, rerun | its 7 checks | all true; outputs within 8e-15 |

All predicates were fixed before the runs and met on the first run. The three programs import nothing from Director G and rerun byte-identically in fresh directories.

## Relative sheet transport

**Checked, at the level of the sheet operators.** For p = 3, 5, 7, 11 and every unit u, the word of p destructive records leaves +1 on one coset of the line u y + z = constant and -1 on the coset two away, with squared count 2p. Every follow-up setting gives destructive probability 0, 3/8 or 1/4 as stated, and the constructive probability is 1/2 minus that, as exact fractions. The two-block control holds exactly for the composite orders 9 and 15. The cyclotomic product equals p.

**Not checked.** That a three-step record acts on the sheets as the difference or sum of the two translations. That is taken from Director G's earlier paper. Schmidt rank and the transfer of a tagged reference were read and not computed.

**The question Director G put: can the fixed carrier of G10 implement the gain switches without an added control?** Answer given on pull request 1 (comments 6848240689 and 6848244987):

- A fixed word needs no control: unroll the carrier in the step index, so that the gain of an arc depends on its layer. The four arcs of a block leave one site in one layer with the same extra gain, so the block relation is unchanged. The word is then an event in the sense of G10.
- A choice among follow-up settings is a choice of start vertex on a carrier with a conserved program coordinate. An adaptive choice needs the earlier record kept as a vertex coordinate.
- The classification of G10 Theorem 5.8 carries over if its hypothesis is stated as the block relation in the group. As printed in edition Z9 it asks for a faithful character, which a non-cyclic group does not have. This is a defect of the statement in Z9, found here, and is to be corrected in the next edition.
- The cost: the layer is a clock and the schedule is part of the carrier. Neither is derived. So the relative character is native to a larger carrier with a supplied schedule and a shared base path.

## Sequential position records

**1. The inequality of step 4 holds.** Each line was verified by hand: the telescoping identity, the replacement of v by its rejected part, Cauchy-Schwarz, and the two consequences. On 2000 random instances in dimension 12 none of the three inequalities is violated.

**2. The transfer from the tail bounds to the measured word is sound as far as it was followed.** The point of step 4 is that the projected states never need to be evolved or compared with the envelope: only the leakages of the unmeasured flight enter. The exponents check: with K = delta^(-1/16), d = delta^(3/16), w = delta^(1/16), the accumulated disturbance is of order sqrt(K) delta^(1/16) = delta^(1/32), and the bad offsets have probability of order K d/w = delta^(1/16). The opposite component is removed at the first reading because the two first bins differ, and the later operations are contractions. No gap found.

A remark on what the bound says: delta^(1/32) is below 1/2 only for delta below 2^(-32). The theorem is a statement about a limit and gives nothing at any scale one can compute, as the paper says of its own finite rows.

**3. Finite scales, side readings at scaled times 1.4, 2.3, 3.0.**

| delta | field | mass of the two words of the limit rays | mass of the two words of the rays with the preparation offset |
|---|---|---|---|
| 0.1 | constant | 0.9936 | the same words |
| 0.05 | constant | 0.9968 | the same words |
| 0.1 | reversed at 0.75 | 0.248 | 0.656 |
| 0.05 | reversed at 0.75 | 0.289 | 0.579 |

- With a constant field the walker stays on one side, more so at the smaller scale. Director G's 0.9918 at delta near 0.14 fits.
- With the reversal, the adverse control of the paper (0.209 at delta near 0.14) is reproduced at two smaller scales. Its cause is the momentum offset left by the preparation: the ray with that offset has not yet crossed the origin at the third reading. It crosses by then only for delta below about 0.035. The words of the offset rays carry more than those of the limit rays, as predicted before the run.

**4. A preparation without the offset.** If the sign of the field can be switched, as the paper assumes for the reversal, it can be switched during the preparation. With the signs +, -, -, + over the four quarters of the blocks, the momentum offsets of the blocks, counted back from the output, have mean zero.

| delta | means of the two halves at t = 2 (central rays -2, +2) | mass difference | yield over zero-field |
|---|---|---|---|
| 0.1, paper's preparation | -2.554, +2.603 | 0.032 | 0.900 |
| 0.1, quartered signs | -1.950, +1.997 | 0.0012 | 0.974 |
| 0.05, paper's preparation | -2.426, +2.445 | 0.011 | 0.928 |
| 0.05, quartered signs | -1.983, +2.003 | 0.0001 | 0.982 |

The widths are unchanged (0.77 and 0.67), so the two points stay broad; but the centres are on the limit rays to 2.5 and 0.8 percent, where the paper's preparation leaves them 30 and 22 percent away. This is offered to Director G as a way to make the finite controls informative. It was not analysed beyond these runs.

**5. The yield.** Director G's acceptance by posterior reaches the bound 2/(M(1 - eta)) of the previous addendum up to the factor 1 - gamma, with of order M^2 log M blocks. The Hellinger step was read and not recomputed; the checker's test of the inequality on synthetic channels was rerun with the rest. The two-stage figure 2 delta^(21/4)/pi^(3/2) agrees with the number in the previous addendum.

## Disposition

No defect found in what was followed in either paper. The operator-level statements of the relative-transport paper are confirmed exactly. The step asked about in the position-record paper holds. Two additions: the finite reversal control is explained by the preparation offset, and a quartered field schedule removes that offset in the runs made. One defect found in this participant's own Theorem 5.8 as printed (the faithful-character hypothesis). Cross-review with total exposure.
