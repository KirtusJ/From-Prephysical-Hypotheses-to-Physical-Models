# Worker notes: small rings (M = 3, 5, 6, 7) — 2026-11-15b

Worker session one level below Director Z. Branch `pcp/worker-small-rings-opus-2026-11-15`.
Author's model family throughout; nothing here is independent review; no gate is passed.

Input: `Director_Z/papers/drafts/G10_body_Z31_candidate.tex` (subsections "Four arc gains", "... winding ..."),
`Director_Z/papers/drafts/G10_subsection_winding_products.tex` (draft, not issued).

## Log (appended after each step)

- step 0: read CLAUDE.md, the two subsections and the draft. Branch created. Previous worker left nothing.
- step 1: launched builder (three-group schedules, M=5,6,7; folder builder_threegroups/) and challenger
  (exact ranks for thm:fgtwo on M=3,5,6,7; folder challenger_fgtwo_ranks/), both opus, paper text only
  (PAPER_TEXT_*.tex are verbatim extracts: body lines 1055-1290 and 775-800, and the draft), each with a control.
- step 2: own idea, independent of the paper's construction: a packet with TWO levels. With the source S alive,
  a packet P at residue a receives deposits from the + side (copy runs up from S) at deficit e_S+a and from the
  - side (S moves up, copy stays) at e_S+a-M. So S, P, B (three packets, pairwise distance >= 2) suffice for
  modes (i) and (ii); this needs M >= 6 (S@0, B@2, P@4).  Program worker/spb_schedule.py.
  First runs (/tmp/claude-0/w_spb_run1, run2) exposed two bugs of mine (phantom removal; split tick of the
  - deposit shifted P by one); kept in the log, not in results. run3:
  `python3 worker/spb_schedule.py /tmp/claude-0/w_spb_run3/result.json 5 9 2 2` exit 0:
  P1 (finite stage check) True for M=6..9, False for M=5 (control P3 as predicted: S,B,P cannot be pairwise
  >=2 apart on Z_5); P2 replays 76/76 for each M=6..9 (q<=2, total size <=2, both modes, N=M and 2M).
- step 3: larger replay started: `spb_schedule.py .../w_spb_run4/result_M5-14_q3_s3.json 5 14 3 3` (background).
- step 4: run4 `python3 worker/spb_schedule.py /tmp/claude-0/w_spb_run4/result_M5-14_q3_s3.json 5 14 3 3` exit 0 (~3 min):
  P1 True for every M = 6..14, False for M = 5 (control); P2 648/648 replays for each M = 6..14
  (q = 1..3, |G1|+|G2|+|G3| <= 3, modes (i) and (ii), N = 2M and N = M for odd M).
- step 5: worker/bfs_small.py (exhaustive relaxed search; contents recorded before the relaxation; witnesses
  replayed on the real ring). Two trial bugs of mine, fixed before any kept result: (a) dropping classes at W
  removed the final site itself; (b) dedup before recording lost witnesses.  Control C1
  `bfs_small.py /tmp/claude-0/w_bfs_t2/r_M5_q1_W3_T40.json 5 1 3 40 2000000` exit 0: all 15 P^+ count
  profiles and all 54 mode profiles met; the search CLOSED (empty layer at t=17, 86,177 states), so the
  relaxed reachable set is complete for all lengths.  Batch M in {3,5,6,7}, q in {2,3}, W=2 started in
  /tmp/claude-0/w_bfs_b1 (run.sh, summary.txt).
