# xr41 cross-review notes: Director_G/Preparing_signed_sheet_residues.md
(in-project cross-review, different model family from author; not independent replication)

## Step 1 hypotheses (read of note)
Preparation part: N multiple of 2M (stated, body); sharp launch on R, sign +, residue 0 (body); H>=4 coprime to M (body);
 first wiring needs N/2 > H+3 (body) -> fails on 4M for M=3,4 (stated, kept by author); compact wiring N=4M, M>=3 (body).
Endpoint law: F_v function of multiset at port only (body); F_v(0)=0 (body, NOT in lead); nonneg finite (lead+body);
 some positive score (body only); scores add across terminal ports (body only, NOT in lead); stationarity = F_v independent of
 horizon (lead says 'stationary'; body never restates it but uses it: construction horizon varies, 'common response law across
 horizons is essential'); common k over every finite position product event (lead+body).
Lead 'forces that constant to be two and the score to be a mixture...' omits additivity across ports and F(0)=0 -> lead states
 the result with fewer premises than the body uses.

## Step 2 rerun of author's checkers (copy in ./copy, output ./run1)
residue_mask_preparation.json: bytes identical, sha256 bb392300...; second run FileExistsError (refuses overwrite)
compact_residue_preparation.json: bytes identical, sha256 f8919024...; second run FileExistsError
Observation: first checker's 'verified' families for M=3,4 run on 8M rings (24, 32), consistent with note.

## Step 4 Lean (4.19.0 already installed; copies in ./lean with #print axioms appended)
ResiduePulseDelay.lean exit 0; reduce_gain/delayed/tune/fixed_slot: [propext, Quot.sound]
ResidueControlWords.lean exit 0; all_rings [propext, Quot.sound]; signs_and_endpoints none; gains [propext, Classical.choice, Quot.sound]
No sorry. Formalized: departure formula on integer lift, delay adds width*wait, tuning for width M-1 only (H=4 at M=3, H=5 at M=4 not covered,
 note's link text says so), five-tick isolation of S/V/W at period 2M for all M>=3, signs, gains.
Not formalized: reduction of physical wells mod N to deficits mod N/2 (comment only), deposit/transfer/finish stages, induction over items,
 padding/terminal site, and the whole endpoint-law section (k=2, irreducibility, harmonic constancy, block identity, classification, line).

## Step 3 own program xr41_check.py -> own1/xr41_result.json (rerun own2 byte-identical; second write refused)
One syntax slip in a dict key was fixed before any output existed; predicates unchanged.
A1 timing map, N%2M==0: 343896 qualify, all met. A1n (N not multiple of 2M, outside hypothesis): 72396 of 335708 disagree -> hypothesis is needed and is stated.
A2 loops LR (+,-1), RLLR (-,-1): 10/10. A3 pulse reversals H-1/H-2: 12/12. A4 table + V/W relative effect: 437/437.
B1 compact wiring N=4M: 1248 qualify (M=3:396, 4:528, 5:132, 10:96, 13:96), all met; M=10,13 not in author's checker.
B2 outside hypothesis (measured): N=2M M=3: 0/108 match; M=4: 0/144; M=5 N=10: 60/180; M=2 N=8: 0/144; M=2 N=4: 0/72. FAILED, kept.
B3 stationary-wall wiring with N/2>H+3: 512 qualify, all met (unique delay each item, incl. H=4 at M=3 and H=5 at M=4, which Lean does not cover).
B4 stationary-wall on 4M (outside hypothesis): M=3 empty 0/144, M=3 all 0/144, M=4 empty 256/256, M=4 all 0/256. Agrees with the note's sentence. FAILED, kept.
B5 naive independent tuning: wrong in 23 of 33 requests (note: 'can give the wrong residue').
C lifted walk: M=3 N=12 (144 states), M=4 N=16 (256): in/out degree 2, strongly connected, exact nullity of A-2I is 1 and the vector is constant;
  for k in {1,3/2,5/2,3,17/4,0,-2} all null vectors have coordinate sum 0 (nullity 2 at k=1 for M=3, 1 at k=-2, 36/64 at k=0) -> no nonnegative solution.
  Same on N=2M and M=2,5 (measured). Numeric spectrum: only modulus-2 eigenvalues are +2 and -2.
C4 z^x with k=z+1/z and h=x with k=2 exist on the line; z^x not single-valued on a ring unless z=1; h=x negative.
D1 block-identity solution space (rank mod 2^61-1, truncated at size n): M=3 n=4,5 -> 3; M=4 n=4,5 -> 4; M=5 n=4 -> 4; M=6 n=4 -> 5; equals 2+floor(M/2) each time.
D2 count and character squares satisfy block identity exactly: 2100/2100.

## Derivation check (endpoint law)
k=2 by summation: follows (in-degree 2 verified). Irreducibility by loops: follows. Harmonic constant: follows. Block identity: follows.
Pair increment, descent to D, parallelogram -> quadratic form, circulant, PSD, normal form: follows. Converse: follows (each well feeds two ports no other well feeds).
Line: follows given k=2; counterexample z^x|U| correct.
GAP 1 (lead): second lead paragraph lists only nonnegativity, stationarity, common k; body also needs additivity across terminal ports,
  score a function of the port multiset only, F_v(0)=0, some positive score.
GAP 2: 'stationary' is never defined in the body although the varying horizon makes it load-bearing.
GAP 3 (Lean): only five-tick macro isolation, signs, gains, departure formula, delay shift and width M-1 tuning are formal; nothing of the endpoint law.
No DEFECT found. No repository change needed; no patch written.
