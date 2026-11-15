# NOTES (reviewer, same model family as the author), 2026-11-15
Control: (ii) excludes none of (1,2,2),(1,3,3),(2,3,2); (iii) excludes (1,2,2) only ((2,3,2) does not meet its hypothesis; (1,3,3) is equality).
Item 3 (first): `python3 s3_adjacent.py s3_results.jsonl` exit 0, 35 s. 66 runs, 15 (group,delta,beta) cases, ranks mod p=2^31-1 (argument for equality over Q in docstring). All H0 true. No failed predicate. P1c control fails exactly for k odd, r even (as fixed beforehand).
Item 2/1: `python3 s1s2_walks.py s1s2_results.jsonl 1500` exit 0, 7.5 s, seed 20261115. 16229 events. No failed predicate Q1,Q2,Q4-Q9. Q3 (stronger, no hypothesis) violated 112 times, all on N=1,2; smallest N=1,T=5, all walks, vertex (0,R), l=1, profile (4,6,4): 16 > 15.
Weak coverage kept: Q5 qualifies only N=1,2 (572 each) and N=4 random (51); Q2 qualifies N=7: 6, N=5: 263; exhaustive N=3,5,6 reach no three levels (length too short); 2046 (y,l) levels skipped in Q4 by PAIRCAP; N=1 and N=2 give identical numbers (positions forced).
Item 4, 5: by hand, see report.
Plot: plot_input.json -> plot_output.svg (sha256 9016b030...9fc6), receipt plot_receipt.json, exit 0, digest matches.
Three-line description: s3_adjacent.py = exact ranks of the restricted equation on two adjacent cosets; s1s2_walks.py = explicit walks/exchange test for lem:winding(iii), cor:threetwo, lem:windingrails; results in *.jsonl (mode x).
