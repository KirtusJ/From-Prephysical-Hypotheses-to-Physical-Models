# FINDINGS (challenger, same model family as the director)

## Hand check before any program run (13 Nov 2026)
- Orthogonality: sum_h (1+Re rho(h)) rho'(h) = sum_h rho'(h) + (1/2) sum_h rho(h)rho'(h) + (1/2) sum_h rho^{-1}(h)rho'(h).
  rho' nontrivial => first term 0. Second = |H| iff rho'=rho^{-1}; third = |H| iff rho'=rho.
  rho'=rho or rho^{-1}, order>2: |H|/2. Order two: both fire: |H|. Other nontrivial class: 0. HOLDS.
- Rounding: m_T(h) = T(1+Re rho(h)) - f_h, 0<=f_h<1, so |sigma_rho'(m_T) - T*main| <= sum f_h < |H|. "bounded by |H|" HOLDS (strict).
- 1+Re rho(h) >= 0 so m_T is a nonnegative integer vector; count = T|H| - sum f_h <= T|H|. HOLDS.
- Limit W/T^2 -> c_rho |H|^2/4 (|H|^2 for order two) > 0 multiple. HOLDS.
- Predicted: no uniform T. Witness needs T of order 4a/(|c||H|) (a/(|c||H|) for order two).
- Run 1 of chal_signs.py crashed (iv.sqrt of an interval touching 0 in the P2 measurement); no result file written. Fixed by comparing squared deviation with |H|^2; predicate P2 unchanged in meaning.
- Run 2 crashed (iv.floor does not exist); no result file written. Fixed by flooring both interval ends with mp.floor and requiring agreement.

## Run 3 (completed; result chal_signs_result.json, sha256 e87f535a...7546; rerun in rerun/ byte-equal)
Groups: Z_2..Z_12, Z2xZ2, Z2xZ4, Z3xZ3, Z2xZ2xZ3. Index sets: full, empty, one seeded proper subset.
Hypothesis test: all class lists distinct+nontrivial; 506 coefficient vectors with a negative coefficient qualified, 210 controls.
- P1 orthogonality: 424 met / 0 failed.
- P2 rounding < |H| (T=1..200, all nontrivial rho'): 84800 / 0. Measured max deviation 0.321|H| (Z_5, Z_10).
- P3 m_T >= 0 and |m_T| <= T|H|: 11000 / 0.
- P4 proof's witness gives certified W<0 for every negative coefficient (T<=5000): 574 / 0.
  Smallest T: 1-2 for (-1, others +1); 1-15 for normalised; for a=10, c=-1/100: 501 (Z_2), 1333 (Z_3), 1001/251 (Z_4), ... 333-334/84 (order 12).
  Matches T > 4a/(|c||H|) (order>2), a/(|c||H|) (order 2). No uniform T exists: threshold grows without bound as a/|c| grows.
- P5 independent small search (entries 0..3/0..2/0..1): 399 met / 107 FAILED (kept): 84 big-count/small-negative, 14 normalised (-1/10), 9 random normalised.
  In all 107 the witness (P4) did find a negative event at larger T. So: positivity on a bounded box of multiplicities does NOT force the signs.
  NO coefficient vector with a negative coefficient was left without a negative event.
- P6 controls: 210 / 0.
- P7 redundancy: 11 / 0 (Z8 over {0,4}; Z2xZ2 over {00,01}; Z12 over {0,3,6,9}); list (0,-1,2) on identical squares is >= 0. Remark holds.
- P8 edge cases: 11 / 0 (trivial H; Z_2 witness = (2T,0) exactly, threshold T = floor(a/(2|c|))+1; empty index set).
- P9 report table: multiplicities (9,4,4,4,4); weights -5, 6-4sqrt5, 6-4sqrt5 exact (sympy): 4 / 0.
Counterexample attempt to the claim: none possible by the argument - W>=0 on integer points of the orthant forces the quadratic part to be copositive (scale m by T, divide by T^2), and x=1+Re rho is an orthant vector on which the quadratic part equals c_rho*|H|^2/4 (or |H|^2). A large a only delays T.

GAPs (hypotheses not in the claim's own sentence):
- G1 S4 (nonnegativity on EVERY event, at all lengths) and S5 are not defined in the inputs given; the proof needs S4 at unboundedly large lengths (max m_T ~ 2T, Lemma (4) needs d^k >= N|V||C|). Stated only in the report's closing sentences.
- G2 "A singleton gives a+sum c=1" / "a=1 when no classes" uses the singleton normalisation, which is in the text before Cor. return, not in the claim. Not needed for the signs.
- G3 Distinctness of classes as restrictions to C_0 (not as full characters) is essential; stated in the report. With a redundant list the sign claim is false (P7).
Not checked: Cor 5.29(3) (its text is cut off in the input), definition of S4/S5, the 125-vertex reachability and "twenty qualifying characters" of the F_5 example, the report's own checker.
