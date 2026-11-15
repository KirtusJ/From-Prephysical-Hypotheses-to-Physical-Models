# NOTES (reviewer sub-agent, same model family as the author), 15 Nov 2026
Tools: python-flint 0.9.0 and numpy installed with `pip install --user` (exact ranks over Q; nothing in the repository changed).
CONTROL: Z_4=<beta>, delta=beta^2: chi(delta)=-1 iff chi(beta)^2=-1, so 2 characters, chi(beta)=+i and -i, one pair {chi,chi^-1}; k=1 odd, r=2 even: theorem predicts ONE square, eps0^2+eps1^2 (c=0).
## Items 4, 6(b) first sentence: `python3 item46_walks.py 20261115 item46_run1.jsonl 6000` exit 0
6682 position product events (3848 nonempty), rings N=1..9, T<=11 (exhaustive masks N<=3,T<=3). W1..W8: 0 failures. 2003 vertices with >=3 levels.
X1: second rail inequality fails at l'-l=M in 2603 sites (not claimed). X2: mirror pattern (R at l, L at l+M, nothing else) occurs 225 times: only one of the two patterns is excluded, as the text says.
X3: for ARBITRARY events 24 of 3232 have a vertex with exactly 3 walks on 3 levels -> cor:nowind sentence 1 needs "position product event" in the statement.
B1/B2/B3 (HYP psi(delta)=-1 qualifying 1018/803/873): Laurent identity mu(Ext S)=2mu(S) exact, 0 failures, incl. arbitrary and mixed-length events.
B4 (no HYP): identity fails 6147 of 7892 (holds 1745: events with no site occupied on both rails etc.). B5 u=2: fails 2649 of 2694 (45 hold; kept).
## Item 6(b) second sentence: `python3 item6b_z2z9.py 20261115 item6b_run1.jsonl 400 11` exit 0
104976 carriers in Z_2xZ_9 on N=3; 3888 qualify (s=3, r even); 400 sampled. Criterion: generic u, two-walk events pooled over lengths <= T0.
First failing length, variant A (F_R, F_L separate): 7 in 278, 8 in 41, 10 in 81; 9 in NONE. Variant B (one table): 7 in 342, 8 in 22, 9 in 18, 10 in 18.
Predicate Z1 (first failure at 9) FAILED for all 400 in variant A; holds for 18/400 in variant B (e.g. a=(0,8),b=(1,1),c=(0,7),d=(0,0)).
Typical clash: level differences +3 and -6 for one ordered pair of gains: equal values iff u^9=1. So the sentence needs the gains, u, and the reading named.
## Item 1 run 1: `python3 item1_fgtwo.py 20261115 item1_run1.jsonl 3000000` KILLED after ~3 min (stalled on a Z_12 class with large r, 1.1 GB). Partial file kept: 20 cases, all P1-P6 true. v2 skips classes over cap (recorded).
## Item 1/2 run 2: `python3 item1_fgtwo_v2.py 20261115 item1_run2.jsonl 3000000` exit 0 (stdout in item1_run2.stdout)
152608 carriers enumerated (9 groups, N in {9,16}); 25652 qualify s=2; 54 classes (group, r, k parity, |H/Delta_N|); one carrier per class; 51 run, 3 SKIPPED (r=6, over cap).
All 51 sampled carriers have N=9 (M=9). r odd: 33 (r=1: 26, r=3: 7); r even k odd: 10; r even k even: 8; r=4: 2 cases (n=4 only).
P1..P4 true in 51/51; P5 (eps0*eps1 is NOT a solution for k odd) true 10/10; P6 (sign formulas, sigma_chi, 2 characters) true 18/18. No failed predicate.
dimproj(adm)=dimproj(all)=E in every case and every n' in {n-1,n-2}; at n'=1 for r=4 the dimension is 1 (squares are not separated at size 1: expected).
Not covered: r=6 and larger; n>4 for r>=3; N=16 never drawn.
Reruns in a fresh directory: item46_run1.jsonl and item6b_run1.jsonl byte-identical (sha256 c2c64784..., f346fd94...). item1 not rerun (contains timings, so bytes would differ anyway).
## Reading findings (items 3-6): see final report. Main: cor:nowind sentence 1 lacks "position product event"; rem (a) "one square" false for r odd; rem (b) Z_2xZ_9 sentence not reproduced; thm:fgtwo statement omits its dependence on prop:threegroups (COMPUTED); intro sentence overclaims.
