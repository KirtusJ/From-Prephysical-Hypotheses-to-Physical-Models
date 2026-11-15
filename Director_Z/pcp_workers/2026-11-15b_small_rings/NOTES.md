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
- step 6: PROOFS.md written: Lemmas R, S, T, E and Theorem A (three groups, modes (i),(ii), for M >= 6, hand proof
  by the pairwise-distance rule of Lemma E), Corollary A1 (thm:fgtwo, thm:fgadj, cor:pplus8, thm:fgprod, thm:fgthree
  carry over to M >= 6 given the body's proofs as written).  Challenger on Theorem A launched (folder
  challenger_theoremA/, statement extract STATEMENT_theoremA.md sha256 002d8ae8...).
- step 7: exhaustive search batch /tmp/claude-0/w_bfs_b2 (run.sh: `bfs_small.py OUT M q 2 60 2000000`, ulimit -v 4 GB):
  M=3 q=2 W=2: exit 0, CLOSED at t=13 (1,396 states): P^+ 19/19 met; modes 84/126 met (42 not met).
  M=3 q=3 W=2: exit 0, CLOSED at t=15 (2,262 states): P^+ 24/33 met; NOT met (any length, relaxation sound):
  ({0},{1}), ({0},{1,1}), ({0,0},{0,1}), ({0,0},{1}), ({0,0},{1,1}), ({0,0},{1,2}), ({0,1},{1,1}), ({0,1},{1,2}),
  ({0,1},{2,2}) [U' on R, V' on L, exponents of delta, up to a common translation]; modes 144/486.
  M=5 q=2 W=2 running: at t=10 all 19 P^+ and all 126 mode requests met in the relaxed search (replay pending).
- step 8: M=5 exhaustive search `bfs_small.py /tmp/claude-0/w_bfs_b2/r_M5_q2_W2_T60.json 5 2 2 60 2000000` exit 0, 453 s,
  CLOSED (646,602 states): all 19 P^+ and all 126 mode requests (G1,G2,G3 non-empty) met, every witness replayed on
  Z_5 and Z_10. So M=5 is not obstructed at q=2, sizes <= 2.  Hand argument (PROOFS remark) that S + two packets
  with S isolated cannot split on Z_5 is true but does not cover dynamic configurations.
- step 9: M=5 construction by search: worker/m5_schedule.py. Configuration ALPHA (S 0, X +1, Y -2), rails
  RHO=(S:L, X:R, Y:R); gadgets adv (7 ticks, dS=1, dX=dY=0), depX (3 ticks), depY (3 ticks) found by bounded BFS
  (depth 8; good RHO: LRR, LRL of 8 tried).  Phase P uses the old gadgets with P at +3 (two packets), then a
  2-tick transition into ALPHA with B as X and P as Y.  Runs: w_m5_g1 (gadget search only, `m5_schedule.py
  OUT 3 3 8`, exit 0); w_m5_g2 exit 0 but 78/216 replays FAILED only because my comparator allowed level
  shifts {0,-1} and not +1 (one-group requests in mode (ii)); fixed (shifts {-1,0,1}), w_m5_g3
  `m5_schedule.py /tmp/claude-0/w_m5_g3/m5_q2_s2.json 2 2 8` exit 0: 216/216 (q<=2, total size <=2, modes (i),(ii),
  prefix z in {0,1,3}, N=5 and 10, exact gains).  Tick tables: worker/m5_table.py ->
  results/m5/m5_tables.txt, ALL_OK=True (exit 0).  Predicate C (M=4 control) of m5_schedule.py was NOT implemented.
  Large replay q<=3, size<=3 running in /tmp/claude-0/w_m5_g4.
- step 10: w_m5_g4 `m5_schedule.py /tmp/claude-0/w_m5_g4/m5_q3_s3.json 3 3 8` exit 0, 88 s: G3 1926/1926 replays
  (q<=3, total size <=3, modes (i),(ii), z in {0,1,3}, N=5 and 10, exact gains). PROOFS.md: Theorem B (M=5),
  Corollary B1 (prop:threegroups and its consequences for M >= 5), Statement C (M=3, q=3: P^+ false; COMPUTED).
- step 11: cross-check of Statement C without relaxation, worker/m3_brute.py (full states on the actual ring, no
  dropping): `m3_brute.py /tmp/claude-0/w_m3_brute/m3_N3_T14.json 3 14 3000000`: reached length 10 (802,803 states
  in layer 10) with L-R gain differences 0 (first at length 2) and 2 (length 3) seen and difference 1 NOT seen;
  then KILLED by the kernel for lack of memory during layer 11 (shared limit; the challenger's four rank processes
  held ~10 GB at the time). No result file. FAILED RUN, kept here; my CAP was per layer and not a memory bound.
  Evidence kept from the log only: no ({g},{g+1}) one-level pair at lengths <= 10 on Z_3 without relaxation.
- step 12: challenger_theoremA report: NOT BROKEN IN RANGE (M=6..12 all q<=4, |G|<=4, 20 blocks x 13,770 cases;
  M=6..14 sampled q<=8, |Gi|<=6, 26 x 600; 0 failures of P1-P5); M=5 fails as stated (P-S distance 1), as predicted;
  two gaps in proof text: Lemma S stated for arbitrary events but proved only for the constructions; Lemma T needs
  N>=3. Both corrected in PROOFS.md (restrictions stated; neither is used outside M>=5). Control answered correctly.
  RERUN by worker: `cd /tmp/claude-0/w_rerun_chA && python3 challenger_theoremA/chal_theoremA.py res_large_M6-14.jsonl
  6,7,8,9,10,11,12,13,14 large` exit 0, 48 s, result byte-identical (sha256 4a26a1c9...). Small runs (364 s, 127 s)
  not rerun.
- step 13: micro_m3 report: CONFIRMED TO LENGTH 9 on Z_3 (exhaustive, no relaxation, own program) and 7 on Z_6; no
  invariant found; control correct (M=3 for N=6, 5 for N=10). Wording caveat: the extract does not define
  position product events (defined in PAPER_TEXT_ppcons.tex, which it was not given) — its reading matches.
  RERUN by worker: `cd /tmp/claude-0/w_rerun_m3 && python3 micro_m3/enum_pp.py 3 3 8 z3_T8.txt` (ulimit -v 2.5 GB)
  exit 0, byte-identical (47ad6571...). So Statement C has: closed relaxed search (all lengths, my program) and
  unrelaxed exhaustive search to length 9 (micro) / 10 (my killed run, log only).
- step 14: builder_threegroups report (control correct: lambda(G1)-lambda(G2)=M, G1 larger). Claims: T7 (modes (i),(ii)
  for M=7 by a 4-packet certificate with a rotating gap of 1; ticks checked by program, some by hand; replays 432/432 on
  Z_7, Z_14); T3 (M=3: request G1={1},G2={1,1},G3={1} met by no event, every q, both modes; complete search + its Lemma
  L-shrink); E56 (M=5,6: all requests met up to total size 7/6/4 for q=1/2/3, deficit picture only, no construction);
  TP (cor:tp excludes nothing for modes (i),(ii)). Its claim R3 in NOTES ("all stocks lie in (S,S+M) while S lives";
  "G1 one lap above G3 forces S dead before that merge") is FALSE in general: Theorems A/B put a stock on the minus
  side of S and fill one packet at two levels from both sides; it only restricts the builder's own model, and its M=7
  result is subsumed by Theorem A. Its Lemma L-shrink (restrict each mask to the sites occupied by final walks) is a
  cleaner soundness argument than my relaxation; adopted in PROOFS with credit.
  RERUN by worker in /tmp/claude-0/w_rerun_bld (ulimit -v 3 GB): `tg_cert.py cert_M7.jsonl 7` exit 0 and
  `tg_exh.py ex_W12_M3.jsonl 12 40 200 3` exit 0; both identical to the kept files except line 1 (argv records the
  script path as typed). Not rerun: tg_search run4, tg_exhg, tg_certreplay, tg_replay.
- step 15: bfs M=5 q=3 W=2 STOPPED by the worker at t=12 (2,500,908 states, ~29 min; not closed, no result file):
  in the relaxed search all 33 P^+ and all 486 mode requests had been met, but witnesses were NOT replayed, so this
  is only a log (results/bfs_M5/log_M5_q3_W2_STOPPED.txt). The queued M=6,7 controls were not run (constructions of
  Theorems A, B make them unnecessary). The watcher on summary.txt hit its background time limit (killed) first.
