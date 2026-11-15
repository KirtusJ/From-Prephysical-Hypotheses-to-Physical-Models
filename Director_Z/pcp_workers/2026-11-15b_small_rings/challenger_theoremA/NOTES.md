# Challenger notes, Theorem A (M >= 6)

## CONTROL (from PAPER_TEXT_subsections.tex alone)
In the proof of Proposition prop:threegroups the text says that for M = 7 the first of the listed uses of
M >= 8 fails: the run of the first group (A) from relative deficit 2 to 6, whose last refused candidate is 7,
which must not coincide with the source at 0; for M = 7, 7 == 0 mod 7, so the refused candidate lies in the mask.

## Step 1 (read statement)
Read STATEMENT_theoremA.md and the definitions/Proposition in PAPER_TEXT_subsections.tex.
Interpretation for the program: N with N/gcd(N,2)=M, i.e. N=M (M odd) and N=2M (all M).

## Step 2 (program written)
chal_theoremA.py, predicates P1-P6 fixed in docstring before first full run. Dev smoke test in
/tmp/claude-0/chal_A_dev: M=5 fails P1/P2 already (exclusivity), M=6,7,8 pass on one request.
Planted control: advances 0 and coast 0 must give a P3 mismatch for a nonzero target (see next run).

## Step 3 (runs; all exit 0)
cd /tmp/claude-0/chal_A_small && python3 $W/chal_theoremA.py res_small_M6-12.jsonl 6,7,8,9,10,11,12 small   (exit 0, 364 s)
  20 (M,N,variant) blocks x 13770 cases, all qualify H (M>=6); 0 failures of P1-P5.
cd /tmp/claude-0/chal_A_m5 && python3 $W/chal_theoremA.py res_small_M5.jsonl 5 small   (exit 0, 127 s)
  M=5 (labelled, outside H): phantom 13754/13770 fail, omit 13270/13770 fail; first failure always P1
  (packet P's excluded residue required), then P2 (leaked walk) and P3. Non-failing M=5 cases are requests
  with G1=G3=empty (no P packet; in 'omit' all of them pass).
cd /tmp/claude-0/chal_A_large && python3 $W/chal_theoremA.py res_large_M6-14.jsonl 6,...,14 large   (exit 0, 59 s)
  sampled q<=8, |Gi|<=6, seed 20261113: 26 blocks x 600, 0 failures.
Planted control (advances 0, coast 0, target nonzero): walks at site 1, x=0, mismatch visible -> P3 detects.
Kernel reported an OOM kill during the last command (not attributable to this program, Pool(4), small state).

## Step 4 (proof text read)
Bullets of exclusivity, Levels, Gains, depP- merge length M-4: consistent with runs (P1,P3,P4,P5 hold).
GAP (Lemma S): statement is for an arbitrary event; proof covers only the coast in these constructions.
GAP (Lemma T): singleton masks isolate one walk only for N>=3 (N=2: x+1=x-1); statement says every k with N>=1 implicit. Not used for M>=6.
M=5: P-S circular distance min(4,M-4)=1; first failing tick is the first tick with S, P adjacent and moves conflicting.
