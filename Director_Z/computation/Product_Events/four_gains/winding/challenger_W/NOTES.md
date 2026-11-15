# challenger_W notes (appended per step)
- Step 1: read STATEMENTS.md and body.tex 778-800, 868-890, 1052-1146 only.
- Step 2: chal_w.py written, predicates in docstring before first run. Run 1:
  `python3 chal_w.py --seed 20261115 --out results_1.txt --tlim 25` (cwd = this folder), exit 0, no failed predicate (FAIL {}).
- Step 3: chal_w2.py = chal_w.py plus per-N counters of hybrid pairs (one line changed, see diff). Run 2:
  `python3 chal_w2.py --seed 20261115 --out results_2.txt --tlim 25`.
- Failed predicates: none in either run. Kept non-qualifying cases: prefixes for N=1,2 are not single walks (lines "P N=1", "P N=2"); 407 (event,site) cases without common lambda in section A; 15 big random events with hybrid test skipped; 13 empty random events.
- Text findings (no computation needed) are in the hand-back report.
