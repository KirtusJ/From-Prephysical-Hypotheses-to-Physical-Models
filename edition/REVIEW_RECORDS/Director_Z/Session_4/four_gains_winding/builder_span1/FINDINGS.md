# builder_span1 FINDINGS (appended as work proceeds; same model family as the director)

## Step 0. Control (by hand, then P0 in span1.py)
N=6, masks {1,5},{2,4},{3}: exactly two walks. RRR ends at (3,R), gain 1, lambda=0. LLL ends at (3,L), gain delta^2, lambda=3.
(Step 2 from site 1 to 0 and from 5 to 0 is refused.) Levels differ by M=3; rails differ.

## Step 1. Before any run: the construction AS REQUESTED cannot exist (Lemma X, proof in PROOFS.md)
Hand argument: an L-walk with lambda=l and an R-walk with lambda=l+M at one site force an L-walk with l+M and an R-walk with l.
So (U_0,U_1,V_0,V_1)=(empty,{1},{1},empty) with l'=l is impossible on every ring; with l'=l+M the request
({1},empty,empty,{1}) is impossible.  Plan: test PX by program, build the three-group preparation instead.

## Step 2. Run 1 (first and only run of span1.py; no predicate changed after it)
Command: `python3 -B span1.py results_run1.json` (cwd = this folder). Rerun in a fresh directory: bytes identical.
- P0 control: as in Step 0 for q=1..4.
- PX: 3200 random events, N=3..10. PX1: 2102 non-vacuous instances, 0 fail (124 with equality). PX2: 1232, 0 fail.
- PC at and above the bound, all sites, q=1..4, both modes: N=16 (M=8) 13824/13824; N=9 7776/7776; N=11 9504/9504;
  N=20 (M=10) 17280/17280 qualify. Max length 102, max mask 5 sites.
- PC below the bound (construction fails, kept): qualifying/cases at sites 0,1:
  N=3 56/1728; N=6 (M=3) 56/1728; N=5 128/1728; N=10 128/1728; N=12 (M=6) 344/1728; N=7 400/1728; N=14 400/1728.
  First failures are in results_run1.json (PC.<N>.first_fail). The ones that qualify have enough empty groups.
- PR: 300/300 random cases (q<=7, <=5 items per group, N in {16,9,17,22,40}).
Not covered by any run: four non-empty groups (shown impossible in general by Lemma X; the admissible ones not built).

## Step 3. Proofs written: PROOFS.md (Lemma X, Corollary X.1, Proposition T, Theorem Y).
## Failed / not done
- The requested four-group construction: does not exist (Cor. X.1).
- Whether every request with |V_0||U_1| <= |V_1||U_0| can be prepared: not attempted, open.
- Rings with M in {3,5,6,7}: this construction fails; statement open there. Bound 8 comes from DEP needing
  relative deficits 0..7 distinct and the stock at 6 two away from the source.
- No Lean; Theorem Y's replacement of Step 6 is elementary but hand-checked only once.

## Tool note
span1.py: builder + exact replay of (site, rail, exponent, lambda) counts for the three-group preparation and the
cross-rail inequality test. Python 3 standard library only. Output: results_run1.json (mode 'x').
