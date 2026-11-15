# Coordinator notes, 2026-11-15b occurrence (appended after every step)

Step 0. Read the two permitted inputs only (draft subsection; body subsections "Four arc gains" and "...winding...").
BLOCK: this agent has no Agent tool (not in its tool list, not among deferred tools; ToolSearch for it returned none).
No child of type pcp-builder / pcp-challenger / pcp-micro-review / pcp-formalizer could be launched. No child controls exist.
Decision: the coordinator does the narrow work itself, in scratch directories, and says so. Everything below is by ONE agent of
the author's model family: not independent review, and without even the reduction of exposure that separate children give.

Coordinator control: Cor. tp(iii): W(Y)=v(Y^2)+Y u(Y^2) has no root with positive real part; for u,v nonzero with non-negative
coefficients, equivalently: g=gcd(u,v) has only real non-positive roots, u/g and v/g have only real, simple, non-positive roots,
and these alternate in decreasing order, the LARGEST root belonging to v/g (the rail L polynomial).

Step 1. Reformulation used by the programs (derived from the proof of thm:tp, unrolled lattice): the state after t masks is
n_t: Z -> N (walk counts by deficit e = number of left steps); a mask is a set E of residues mod M;
n_t(e) = [e mod M in E](n_{t-1}(e)+n_{t-1}(e-1)); profile at a site = (classes c-1, c) of n_{T-1}: v_j=n(c-1+jM), u_j=n(c+jM).
Only M matters, not N.

Step 2 (Q2). Wrote scratch/occ/q2/enum_profiles.cpp (predicates in its header before the first run). Trial runs, all exit 0,
closed (breadth-first search ended with no new state): M=3 B=7 K=4: 210 profiles; M=4 B=7 K=4: 228; M=5 B=7 K=4: 228;
probe dir: M=7 B=7 K=4: 228 (5,324,115 states, 55 s); M=5 B=9 K=4: 550; M=6 B=9 K=4: 550 (3,529,453 states, 21 s).
The numbers 228 and 550 are the draft's allowed counts. Probe M=7 B=9 K=4 was cut off by a usage limit and then killed by me
(no exit code, no result file): kept as a stopped run.
Interruption: stopped by a usage limit after step 2; resumed on the caller's message. No child existed, so none to resume.

Lossless-bounds lemma (mine, hand proof, unchecked by anyone else). Fix a profile at classes (c-1,c) of n_{T-1} with total <= B
and <= K levels. (1) Trim: delete from each mask E_t every residue class from which no open path leads to the two target
classes at time T-1; the target classes are unchanged. (2) In the trimmed event every occupied class at every time has, by
periodicity, the same continuations from each of its levels, so its total is <= the target total <= B. (3) Span: if (t,e1),
(t,e2) are occupied with e2-e1 > (K+1)M, take open continuations P from e1 (adds d1) and Q from e2 (adds d2); both ends lie in
a window of length KM, so d1-d2 > M; the translate of P by iM, i maximal with iM < e2-e1, starts below Q and ends above it,
so they meet; Q then P+iM is an open path from an occupied point ending in a target class above the window: contradiction.
So bounds (a) class totals <= B and (b) span <= (K+1)M lose no such profile, and a closed search is exhaustive over all lengths.

Step 3 (Q2). Wrote compare_profiles.py (predicates in docstring first). First run (dir q2_cmp0), exit 0:
P0 control PASS (550 and 228 reproduced). M=3 B=7 K=4: seen 210 of 228 allowed, 18 not seen (kept in the json), P1 pass.
M=6 B=9 K=4: seen = allowed = 550, P1 and P2 pass.  NOTE: M=6 is the ring of 12 sites (or 6 odd is impossible): the draft's
"6 sites" has M=3.
P3 FAILED as fixed: P3b (a negative minor of order <=4 in rows 0..4) has no witness for 6 resp. 10 root-rejected sequences,
all on ONE rail, e.g. (1,2,2,1), (1,3,3): not real-rooted, but the first negative minor is of higher order. Kept. Follow-up
predicate P3c (added after the first run, said so in the program): for these, a negative Toeplitz minor of order <=6.

Step 4 (Q2). Runs in q2_run1 (each: timeout 600 ../q2/enum_profiles M B K; source sha256 584c5d32...):
 "4 12 6" exit 0, 2 s, closed, 117,480 states, 1644 profiles; "5 11 5" exit 0, 6 s, closed, 1,105,341 states, 1144 profiles;
 "7 8 4" exit 0, 161 s, closed, 14,344,720 states, 368 profiles.
compare_profiles_v2.py (follow-up P3c; pruned candidate generator; P0 regression PASS 550/228), dir q2_cmp1, exit 0:
 M=4 B=12 K=6: allowed 1656, seen 1644, P1 pass, P2 FAIL: 12 allowed profiles NOT SEEN (kept), smallest total 11:
   w=(1,2,3,3,2) i.e. v=1+3z+2z^2, u=2+3z; and its mirror/shifts (0,1,2,3,3,2),(2,3,3,2,1),(0,2,3,3,2,1); total 12: (1,2,8,1),(1,8,2,1),(1,2,3,5,1),(1,5,3,2,1) and shifts.
 M=5 B=11 K=5: allowed 1148, seen 1144, P2 FAIL: the same four of total 11 not seen.
 => the draft's "exactly those allowed" on 5 and 8 sites holds only within its size bounds; first failure at total 11.
 P3c: 6 resp. 4 sequences still without a negative minor in the windows tried, e.g. one rail (1,4,5,1), (1,1,2,2,2,2,1,1)... kept;
 they are rejected by the root criterion (not real-rooted); a larger minor would be needed. Not pursued.
Idea (step 5): in a trimmed event every occupied point has a continuation to the site, so the WHOLE state has total <= profile
total. Stronger lossless bound -> program enum2 with whole-state total <= B; cross-check against enum_profiles on equal bounds.
