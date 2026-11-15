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
