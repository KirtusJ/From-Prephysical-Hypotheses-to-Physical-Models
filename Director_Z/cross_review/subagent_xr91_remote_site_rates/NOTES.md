# NOTES xr91
## CONTROL (note A convention = brief convention: coin then shift; confirmed by reading note A)
After 2 ticks: P(-2)=1/4, P(0)=1/2, P(2)=1/4 (amplitudes/2: site2 R=1; site0 R=1,L=1; site-2 L=-1).
q=2 detector: (1/16,1/4,1/16)/(3/8) = 1/6, 2/3, 1/6. (Agrees with note A "1/6 of its mass at -2".) Brute enumeration is in my program too.
## Step 1: read both notes + Lean file. 
## Step 2: hand check of derivations (before program)
- A: W5=(17^q-17)D, D sign = sign(8^q-2*4^q)=sign(q-1): FOLLOWS, strict. W7 via convexity (9,41)->(25,25): FOLLOWS. limits 8/15, 1, 0: FOLLOW.
- A blank: (4,4)->(2,6); (9,17,41)->(17,21,29): majorization FOLLOWS. Tail bound via Cauchy-Schwarz FOLLOWS (existence constants only).
- B: 89/261*1/356+172/261*1/344 = 1/348 by hand OK. Majorization under splitting standard. 38 e7 and 24(...) bounds FOLLOW.
- Whole content: remote n_x unchanged, so Delta_x = n_x^q * (1/Zb - 1/Zm): signalling through global Z only.
- Rivals planned: unnormalised f(p); site-dependent exponents; block-normalised; setting-dependent mixtures; setting-dependent efficiency eta_b/eta_m = Zb/Zm.
## Step 3: first run of xr91_check.py crashed in R7 (TypeError Decimal*Fraction, my bug, before result file written; no predicate outcome lost). Fix: convert to Decimal in R7 only.
## Step 3 result, run 1 (xr91_result.json, exit 1, KEPT): fails A4 (1), A6 (1), U1 (138), R2 (1).
- A4/A6 fails are MY bug: q->0 limit computed with int/int float division (0.5333.. vs 8/15; 0.0833.. vs 1/12). Not a note defect. Fixed in run 2 (powr returns Fraction 1 at q=0).
- U1 predicate was too strict (demanded sign(q-1), many instances have uniformly reversed sign, some are pure permutations = min sep 0). 25 instances have a sign change at q != 1 => false-pass exponent exists for those designs. Reclassify in run 2, keep run 1.
- R2: rail-resolved power law: five-tick sign test rail-cell multisets IDENTICAL ([1,1,1,1,4,4,4,16]) => that rival passes five-tick sign test for all q.
- R3 found exact setting-dependent mixture passing; R4, R5 rivals pass all four line tests exactly; R6 efficiency ratio 87/95.
## Coordinator addition: author's note 99 (Fluctuating_site_scores_and_paired_launches.md): f_pm(w)=1/(1 pm h(w))-(1-w) for w>1/2, identity else. Will verify exactly (N99) and classify vs family.
## Step 3 run 2: xr91_result_run2.json exit 1 (kept fails: U1b 18 designs with a false-pass exponent; R2 1 and R2b 2 = rail-resolved rival does not signal in sign tests). All note-number predicates pass.
## Step 7: both checkers rerun from copies, python3 and -O, exit 0, byte-identical to filed JSON.
## Step 8: Lean 4.19.0: SpatialFlagPartitions exit 0, axioms propext, Lean.ofReduceBool, Quot.sound (native_decide). RemoteSiteRates exit 0, no axioms.
## Step 9: wording checked (README rows 26, 28; gate map key remote_position_rate_test).
