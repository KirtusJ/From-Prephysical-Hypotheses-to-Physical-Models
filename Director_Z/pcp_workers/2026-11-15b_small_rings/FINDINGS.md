# FINDINGS — small rings (M = 3, 5, 6, 7), worker 2026-11-15b

Reader: Director Z. Author's model family throughout (worker and four children); not independent review. No gate passed.
Statements in full: PROOFS.md. Log: NOTES.md.

## PROVED
- **Theorem A**: prop:threegroups (modes (i), (ii), every x, q, G1, G2, G3; no walk elsewhere) holds for **M ≥ 6**.
  New idea: one packet P holds two levels, because the source deposits into it from both sides: + side at level l+M,
  − side at l. Then three packets suffice: S, P, B at pairwise circular distance ≥ 2. Hand proof by Lemma E (pairs at
  distance ≥ 2 never conflict).
- **Theorem B**: the same for **M = 5**. Gadgets were found by a bounded search; three packets on Z_5 move as a rotating
  configuration. Proof by finite tick tables (`worker/results/m5/m5_tables.txt`) plus gain bookkeeping.
- **Corollary B1** (given the body's proofs as written; only the statement of prop:threegroups is cited there):
  thm:fgtwo, thm:fgadj, cor:pplus8, thm:fgprod and thm:fgthree hold for **M ≥ 5**. P^+_δ holds for M ≥ 5 without
  \cite{dgone}. This answers (1) and (2) for M = 5, 6, 7 positively, and (3) for those rings by proof.
- **TP separation** (also proved independently by the builder): for modes (i)/(ii), W(Y) = n3 + n2 Y + n1 Y², times Y
  in mode (ii); cor:tp excludes nothing. Every failure below is therefore a failure "on this ring".
- **Lemma L-shrink** (builder; read and checked): it makes a closed search decide requests of size ≤ n for all lengths.

## COMPUTED
- `spb_schedule.py OUT 5 14 3 3`, exit 0. Finite stage check true for M = 6..14, false for M = 5 (control). Replays
  648/648 for each M = 6..14 (q ≤ 3, total size ≤ 3, both modes, N = M and 2M).
- `m5_schedule.py OUT 3 3 8`, exit 0: 1926/1926 replays on Z_5 and Z_10 with exact gains. `m5_table.py OUT`, exit 0:
  ALL_OK=True.
- `bfs_small.py OUT M q W 60 2000000` (relaxed, sound for "not met"; witnesses replayed):
  - M=5, q=2, W=2: closed; all P^+ and mode requests met (exit 0, 453 s).
  - M=3, q=2: closed; P^+ 19/19, modes 84/126.
  - M=3, q=3: closed; P^+ 24/33.
- **Statement C** (M = 3, q = 3): P^+ is false. No event leaves exactly ({δ^g} on R, {δ^{g+1}} on L) at one level;
  9 of the 33 requests of size ≤ 2 fail. Closed search, plus an unrelaxed exhaustive check to length 9 (micro-review).
  No invariant found.
- **Statement C′** (builder): M = 3, every q: G1={1}, G2={1,1}, G3={1} fails in both modes (counts (1,2,1)).
- (3) by exact ranks (challenger, `fgtwo_beam.py`, ulimit 3 GB): NOT BROKEN IN RANGE on M = 3, 5, 6, 7 (40 qualifying
  ring/carrier pairs). On N=3 at L=9, L0=6 there are two excesses: Z8_r4_kodd 3 vs 2 and Z4Z2_r4_keven 6 vs 3. Both sit
  only at L0 = L-3; at L0 ≤ 5, and with width cap 2 at L=10, the dimensions equal the prediction. Full enumeration at
  L=10 ran out of memory. **Unsettled; probably a bound artefact.** Coverage of the winding is thin on M = 7 (2
  two-coset keys) and absent on the M = 8 control.
  So (3) on M = 3, where Theorems A/B do not apply, has only this computation.

## Failed or kept
- My bugs, all caught before results were kept (NOTES steps 2, 5, 9): a phantom removal, the split tick of dep−,
  a level comparator, relaxation at W, and dedup before recording.
- m3_brute run killed by the kernel for memory (shared limit). No result file.
- Predicate C (M = 4 control) of m5_schedule.py was not implemented.
- bfs M=5 q=3 and M=6, 7 controls: see NOTES (unfinished or not needed once constructions existed).
- Builder: NOTES claim R3 is false in general (refuted by Theorems A/B); it constrained only its own model.

## Children: controls and reruns
- builder_threegroups: control correct. Result: M=7 (subsumed by Theorem A), Statement C′, deficit-picture evidence
  for M = 5, 6. Rerun: tg_cert M7 and tg_exh W12 M3 identical except the argv line.
- challenger_theoremA: control correct. NOT BROKEN IN RANGE (M = 6..14). Two gaps in the text of Lemmas S and T,
  corrected. Rerun: large run byte-identical.
- micro_m3: control correct. Confirmed to length 9. Rerun: T=8 byte-identical.
- challenger_fgtwo_ranks: control correct. Rerun: both r=4 excess runs give output identical except timing fields.

## Nobody checked
- The body's proofs of thm:fgtwo etc. themselves (Corollary B1 is conditional on them).
- Lean: no step formalized. Lemma E and the tables are finite checks, not algebra.
- Builder runs other than the two reruns.
- Theorem A beyond M = 14 by program (it is proved by hand for all M ≥ 6).
- M = 4 (N = 8).
