# NOTES (reviewer of T1/T2, same model family as author)
Step 0. Control: after arriving by R, steps L,R,L,L: left steps +3; gain times delta^1 (only the last L follows an L).
Step 1. Read draft lines 1-90, Director_G note, body.tex 778-800, 868-890. Nothing else.
Ambiguities resolved (T1): (a) origin of relative deficits = absolute deficit of source, moves +2 per advance only; after removal fixed at sigma.
(b) "each with the stocks" in Deposit = union with all stock entries. (c) Merge masks {1},{2} read as residues of M+1, M+2.
(d) coast placed immediately before End. (e) empty C: merge of A still performed (A must reach M+2). (f) all empty: source still removed, End run with p.
(g) Merge idle tick and Coast have no refused list in the text; encoded as "j+1 for the others" (merge idle) and empty (coast).
Step 2. Run 1: `python3 threegroups.py result_main_1.json main`. P1,P2,P5,P6,P7: 0 failures. P3: millions of failures -- KEPT, cause is the reviewer's
checker: `isint` evaluated to None (not False) when the spawn argument was None, and None != False counted as a mismatch (first record: removal, admitted False, intended None).
P8 failed as fixed (max relative deficit 12..24 > 9). P4: omissions at coast and merge idle tick.
Step 3. Fixed isint with bool(); program copied to threegroups_v2.py (v1 kept). Rerun to result_main_2.json and result_small_1.json.
Step 4. Run 2: `python3 threegroups_v2.py result_main_2.json main` : 54,352 cases, all qualify (M>=8); P1,P2,P3,P5,P6,P7 0 failures; P4 omissions: coast (no list), merge idle tick; P8 fails (max relative deficit M+4).
`python3 threegroups_v2.py result_small_1.json small` (M=7,7,6,3; 0 qualify): first break at M=7 and M=6 is run A 2->6, tick 2 (k=5 resp. 4..5), candidate k+2 = M = source.
Step 5. T2: inline check of the note's five-tick table (not saved as a file; code in report): admitted iff own row for D=6..12, max distance 5.
