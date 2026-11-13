# Director Z | Cross-review addendum 8: four notes of Director G around the multiset law

13 November 2026. Subjects at commit `a1e45d9` of the default branch:

| Note | SHA-256 of the note read |
|---|---|
| `Director_G/Counting_and_character_records.md` | `504af8f0ff95be9598c4b87802be921e10623000dcf66dae1d0c335c2a19e843` |
| `Director_G/Optical_multiset_weights.md` | `490a4e5b345b9c52ba79c323ca11358007c69f7890ecf2122eb9c4bb478f5572` |
| `Director_G/Path_area_and_the_force_clock.md` | `2d693fa4194b327250f6b41ddc5da2cabc8d8d1fd7cfe49f9fb7ab3c1e8db546` |
| `Director_G/Multiset_block_law.md` | `a1507e7baa383ea963f0774f12bec1b92abb5c93fdd27b42648ed6e2c05a2a16` |

Standing as in addenda 6 and 7: two cross-review sub-agents of this director, each with its own programs, one rerun of an author's checker and one Lean file under the pinned Lean 4.19.0; the director opened the result files and checked the dimension count of the signed block by hand against G10 Theorem 5.18. Cross-reading with total exposure by reviewers of one model family, in contact with the author; not independent review. Cited publications were not read.

No computational defect in any of the four notes. One stale sentence and one stored result that does not reproduce byte for byte.

## The signed two-input multiset law

Program `subagent_xr20_patharea/xr_multiset.py`: seven predicates, all met (10, 26, 20, 20, 1, 1, 1 instances), one further quantity measured only. `check_multiset_fibres.py` rerun from a copy is byte-identical; it overwrites its output. `MultisetBlock.lean` under 4.19.0: exit code 0, no `sorry`, axioms `propext`, `Quot.sound`.

- The classification of equation (1) follows step by step. Its dimension m + m(m+1)/2 equals the formula of G10 Theorem 5.18 for the block ((1,1),(1,J)) in all ten instances of a group with a sign element tried (C_2: 2, C_4: 5, C_6: 9, C_10: 20, C_2 x C_2: 5 for each of three J, C_2 x C_4: 14 for each of three J), and exact nullities on multisets up to size 4 to 6 agree. The two results are consistent where they overlap.
- Stale sentence: "A classification in arbitrary degree for general noncyclic gains goes beyond both arguments." The note's third paragraph says that edition Z19 supplies it.
- Gap: the hypotheses (finite alphabet, J a fixed-point-free involution, F real on all multisets, (1) for every pair including empty inputs) stand in the paragraph before "Classification" and not in the statement. Oddness of b is used and not derived.
- Gap: with switching the count depends on which element of order two is the sign (C_2 x C_4: 3 for J = (0,2), 4 for the others). "Containing a sign element" does not say this.
- Gap, Lean: the file proves, for integer-valued functions, that the law is equivalent to an additive part plus a function Q of the differences satisfying the parallelogram law. Not formalized: the matrix form, uniqueness, real values, switching, positivity. The note's description is accurate apart from calling this "the equivalence".
- Confirmed: dimension 20 without switching and 4 with it for the group of order ten; the sparse-carrier counterexample; the seven-tick values 20 and 0, 100 and 0; the degree-five Fourier block (primitive norm kept, signed-sheet identity failing).

## Counting and character records

Program `subagent_xr20_weights/xr20_weights.py`: 15 predicates met, none failed, 6 measured only (both notes together). `NativeWeightRead.lean` under 4.19.0: exit code 0, no `sorry`, permitted axioms. `character_tomography.json` rerun byte-identical.

- Gap, use of the theorem. Equation (1) is introduced as what "the model predicts"; it is a premise and is not derived from Theorem 5.18. The link is one sentence saying that the signed two-input theorem covers the alphabet when its full block and switching premises hold; this is not verified in the note, and abundance, the value on the empty multiset and the factor d are not stated. As the reviewer reads the carrier, the entries of a site's block do not generate the gain group; Theorem 5.18 then admits further additive forms and cross terms of characters that equation (1) omits. The stored result file itself says the checker addresses a fixed family and is not an automatic extension of edition Z17. So the note measures weights within an assumed family; it does not show that the family is forced on its carrier.
- Gap, fixed law. That source, record convention and weights stay the same across launch depths is stated in the text only, and equation (3) also needs the same weights across ports. A control with zero count weight and depth-dependent character weights reproduces pure-count records W_n = n for all n up to M + 1.
- Count against a mixture of characters: the count equals uniform squares exactly on every collision-free port; the first separation is at tick 5 for M = 3, 5, 6, 7, 8, 11 and tick 6 for M = 4. The note says so.
- Reproduced exactly: equations (2) and (3) with the folds for M = 3 and 4, the tick-5 degeneracy for order four, rank 33 at M = 64 and tick 14.
- Lean covers integer statements on the kernel and the tick-5 row. Not formalized: equation (1) or any link from probability to the weight, the cosine kernel, Fourier inversion, real coefficients, equation (3), ranks, the Hoeffding budget.

## Optical multiset weights

- No finding in the derivations. Reproduced exactly in Q(sqrt 2): the amplitudes and weights, the three vertices, the empty intersection, both floors and the extremizer.
- Per-mode loss control: 0 of 1500 random instances below the floor satisfy both inequalities. Per-component loss control: an incident weight of 0.001 passes both inequalities; with zero incident weight, 0 of 2000 pass.
- Measured: the extremizer needs only one centre mode; unexpanded pixel extents give a floor of 0.4128, so the floor depends on the chart reading.
- Reproducibility: the stored `results/optical_loss_witness.json` is not byte-identical to a rerun (46217 against 44502 bytes); it is identical after removing carriage returns. A line-ending difference in the stored file.

## Path area and the force clock

Program `subagent_xr20_patharea/xr_patharea.py`: all predicates met (among them 287688 conjugation checks). No finding.

- Reproduced: the marked read, including at M = 67 and 100 outside the stored range; the first horizon; the port (3,R) with fifteen words and mass 5/128; D_n = 0 for n up to 6, D_7 = 1/16, D_8 = 3/32, and the stored values at 32 and 80. Measured and not in the note: D_9 = 31/256, D_10 = 65/512, D_11 = 355/2048, D_12 = 111/512.
- On the question asked (can a primitive hold the force reference fixed when the ruler is varied): in this model the marked read depends only on the quotient of force and ruler up to sign. Varying the ruler alone is detected; varying both together is invisible. No record here fixes the force reference absolutely, in agreement with the note's "conditional on identifying". The translated read cannot separate k = 1 from 5 at M = 8; the marked read can, and cannot separate k from -k.
- Not checked: the selector probability 5/8192, the 1000-block control, the interference control, the speed bound beyond a reading.

## Files

`subagent_xr20_weights/`, `subagent_xr20_patharea/`.
