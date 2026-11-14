# NOTES challenger chal_rails (same model family as authors; not independent review)
step 0: read FINDINGS.md, RAIL_WEIGHT.md, CRITERION.md lines 1-80 (Setting, Control header, Props 1,2 with proofs - read slightly more than the statements; disclosed).
R RLR (Fraction(0, 1), Fraction(3, 5))
R LRR (Fraction(0, 1), Fraction(3, 5))
L RLR (Fraction(-4, 5), Fraction(0, 1))
L LRR (Fraction(4, 5), Fraction(0, 1))
P = 9/50
step 1: CONTROL = 9/50 (brute words, control.py)
  L0 qualify=254 pass=254 fail=0  []
  X0 qualify=2438 pass=2438 fail=0  []
  RW1 qualify=47520 pass=47520 fail=0 N=3..12 and line; chi values all 12th roots, chi(a) in {1,z,z^4} []
  RW12L_equals_beta2_over_2 qualify=8640 pass=528 fail=8112  []
  RW12_equals_alpha2_over_2 qualify=8640 pass=528 fail=8112  [(1, (0, 0, 0, 6), (0, 0, 0, 0), (1, 0, 0, 0), '8P=', (4, 0, 0, 0), '4|a|^2=', (0, 0, 0, 0)), (1, (0, 0, 0, 6), (1, 0, 0, 0), (1, 0, 0, 0), '8P=', (16, 0, 0, 0), '4|a|^2=', (4, 0, 0, 0))]
  RW12_formula qualify=8640 pass=8640 fail=0  []
  RW1_N3 qualify=4320 pass=4320 fail=0  []
  RW1_N4 qualify=4320 pass=4320 fail=0  []
  RW1_NNone qualify=4320 pass=4320 fail=0  []
  RW1c qualify=47520 pass=8712 fail=38808  [(3, (0, 0, 0, 0), (0, 0, 0, 0), (1, 0, 0, 0)), (3, (0, 0, 0, 0), (1, 0, 0, 0), (1, 0, 0, 0))]
  RW2 qualify=47520 pass=47520 fail=0 N=3..12 and line; chi values all 12th roots, chi(a) in {1,z,z^4} []
  RW2_N3 qualify=4320 pass=4320 fail=0  []
  RW2_N4 qualify=4320 pass=4320 fail=0  []
  RW2_NNone qualify=4320 pass=4320 fail=0  []
  RW2c qualify=47520 pass=8712 fail=38808  [(3, (0, 0, 0, 0), (1, 0, 0, 0), (0, 0, 0, 0)), (3, (0, 0, 0, 0), (1, 0, 0, 0), (1, 0, 0, 0))]
 N=3 data=4194 eta-1=3060 eta+1=1134
 N=4 data=4140 eta-1=3024 eta+1=1116
 N=5 data=3312 eta-1=2160 eta+1=1152
step 2: chal.py run 1 TIMED OUT at 540 s (exit 124) after L0, X0, rail-weight predicates (all printed above in NOTES); no result file written. Kept as chal_v1_timeout.py. Rerun with smaller parameters as chal2.py.
  L0 qualify=254 pass=254 fail=0  []
  X0 qualify=2698 pass=2698 fail=0  []
  RW1 qualify=22176 pass=22176 fail=0 N=3..12 and line; chi values all 12th roots, chi(a) in {1,z} []
  RW12L_equals_beta2_over_2 qualify=4032 pass=320 fail=3712  []
  RW12_equals_alpha2_over_2 qualify=4032 pass=320 fail=3712  [(1, (0, 0, 0, 6), (0, 0, 0, 0), (1, 0, 0, 0), '8P=', (4, 0, 0, 0), '4|a|^2=', (0, 0, 0, 0)), (1, (0, 0, 0, 6), (1, 0, 0, 0), (1, 0, 0, 0), '8P=', (16, 0, 0, 0), '4|a|^2=', (4, 0, 0, 0))]
  RW12_formula qualify=4032 pass=4032 fail=0  []
  RW1_N3 qualify=2016 pass=2016 fail=0  []
  RW1_N4 qualify=2016 pass=2016 fail=0  []
  RW1_NNone qualify=2016 pass=2016 fail=0  []
  RW1c qualify=22176 pass=5280 fail=16896  [(3, (0, 0, 0, 0), (0, 0, 0, 0), (1, 0, 0, 0)), (3, (0, 0, 0, 0), (1, 0, 0, 0), (1, 0, 0, 0))]
  RW2 qualify=22176 pass=22176 fail=0 N=3..12 and line; chi values all 12th roots, chi(a) in {1,z} []
  RW2_N3 qualify=2016 pass=2016 fail=0  []
  RW2_N4 qualify=2016 pass=2016 fail=0  []
  RW2_NNone qualify=2016 pass=2016 fail=0  []
  RW2c qualify=22176 pass=5280 fail=16896  [(3, (0, 0, 0, 0), (1, 0, 0, 0), (0, 0, 0, 0)), (3, (0, 0, 0, 0), (1, 0, 0, 0), (1, 0, 0, 0))]
 N=6 data=2205 eta-1=1605 eta+1=600
 N=8 data=2325 eta-1=1620 eta+1=705
 N=4 data=2580 eta-1=2025 eta+1=555
 N=7 data=2295 eta-1=1665 eta+1=630
 N=1 data=715 eta-1=535 eta+1=180
 N=3 data=2580 eta-1=1995 eta+1=585
 N=2 data=745 eta-1=550 eta+1=195
 N=None data=730 eta-1=555 eta+1=175
 N=5 data=2220 eta-1=1620 eta+1=600
  A1 qualify=113718 pass=113718 fail=0  []
  A1_N12 qualify=3447 pass=3447 fail=0  []
  B1 qualify=10530 pass=0 fail=10530  [(8, (0, 0, 0, 6), 0), (8, (0, 0, 0, 6), 1)]
  B1_well_equals_port qualify=10530 pass=10530 fail=0  []
  B2a qualify=10530 pass=2639 fail=7891  [(8, (0, 0, 1, 7), 0), (8, (0, 0, 1, 7), 1)]
  B2b qualify=10530 pass=2640 fail=7890  [(8, (0, 0, 1, 7), 0), (8, (0, 0, 1, 7), 1)]
  B2c qualify=10530 pass=10530 fail=0  []
  B2c_exactly_one_prefactor_zero (count) qualify=621 pass=621 fail=0  []
  B3 qualify=10530 pass=10530 fail=0  []
  C_boundary(complex ratio, exactly one of gamma, omega real -> readable) qualify=2064 pass=2064 fail=0  []
  C_boundary(complex ratio, gamma=+-1, omega=+-1 -> unreadable) qualify=576 pass=576 fail=0  []
  C_boundary(gamma or omega = +-1) qualify=4950 pass=4950 fail=0  []
  C_readable_side qualify=5040 pass=5040 fail=0  []
  C_unreadable_side qualify=5490 pass=5490 fail=0  []
  D1 qualify=9016 pass=9016 fail=0  []
  D1_N12 qualify=1040 pass=1040 fail=0  []
  D1_N12_pairs_same_omega_different_gamma (count) qualify=995 pass=0 fail=0  []
  D1_line qualify=6700 pass=6700 fail=0  []
  D1_line_pairs_same_omega_different_gamma (count) qualify=6152 pass=0 fail=0  []
  D1_pairs_same_omega_different_gamma (count) qualify=8392 pass=0 fail=0  []
  D2 qualify=78 pass=78 fail=0  []
  D2_N12 qualify=44 pass=44 fail=0  []
  D2_line qualify=2 pass=2 fail=0  []
  D3_N12_nonreal_kappa_prime (count of site-states) qualify=19529 pass=13295 fail=0  []
  D3_line_nonreal_kappa_prime (count of site-states) qualify=234768 pass=0 fail=0  []
  D3_nonreal_kappa_prime (count of site-states) qualify=485472 pass=17351 fail=0  []
  D4 qualify=13761 pass=13761 fail=0  []
  D4_N12 qualify=1848 pass=1848 fail=0  []
  D4_N12_pairs_different_gamma (count) qualify=1735 pass=0 fail=0  []
  D4_line qualify=6700 pass=6700 fail=0  []
  D4_line_pairs_different_gamma (count) qualify=6152 pass=0 fail=0  []
  D4_pairs_different_gamma (count) qualify=12746 pass=0 fail=0  []
  IFF1 qualify=98852 pass=98852 fail=0  []
  IFF2 qualify=9234733 pass=9234733 fail=0  []
  IFF_sub_Im_omega0_Im_kappa_differs_eq qualify=18978 pass=18978 fail=0  []
  IFF_sub_Im_omega0_Im_kappa_differs_ne qualify=506956 pass=506956 fail=0  []
  IFF_sub_alpha0_or_beta0_eq qualify=49112 pass=49112 fail=0  []
  IFF_sub_alpha0_or_beta0_ne qualify=613580 pass=613580 fail=0  []
  IFF_sub_omega_pm1_eq qualify=36496 pass=36496 fail=0  []
  IFF_sub_omega_pm1_ne qualify=1463399 pass=1463399 fail=0  []
  IFF_sub_|2Re k|=n_eq qualify=4573 pass=4573 fail=0  []
  IFF_sub_|2Re k|=n_ne qualify=27727 pass=27727 fail=0  []
  K1 qualify=122912 pass=98852 fail=24060  [[(8, (2, 8, 10, 10), 4), (8, (2, 4, 10, 6), 4)], [(8, (2, 8, 10, 10), 5), (8, (2, 4, 10, 6), 5)]]
  K2 qualify=357570 pass=98852 fail=258718  [[(8, (3, 6, 9, 6), 0), (8, (3, 6, 9, 6), 1)], [(8, (3, 6, 9, 6), 3), (8, (0, 9, 9, 0), 10)]]
  K3 qualify=98852 pass=12325 fail=86527  [[(8, (6, 0, 6, 6), 0), (8, (6, 9, 9, 6), 0)], [(8, (6, 0, 6, 6), 1), (8, (6, 9, 9, 6), 1)]]
  K4 qualify=98852 pass=66312 fail=32540  [[(8, (2, 4, 10, 6), 0), (8, (2, 8, 10, 10), 0)], [(8, (2, 4, 10, 6), 1), (8, (2, 8, 10, 10), 1)]]
  LINE qualify=16859 pass=16859 fail=0  []
  LINE_converse_eta-1 (not claimed; information) qualify=138525 pass=138525 fail=0  []
step 3: chal2.py exit 1. B1 (10530/0 pass), B2a, B2b failed: MY predicate code had a factor 2 wrong (values are stored
as 2^t P; I compared 2*value with n+2Re k, and 2*value with (n+2Re k)(2+2s Re w)). Not a defect of the text. chal2.py and
chal2_result.json kept. chal3.py = chal2.py with only those three comparisons corrected.
  L0 qualify=254 pass=254 fail=0  []
  X0 qualify=2698 pass=2698 fail=0  []
  RW1 qualify=22176 pass=22176 fail=0 N=3..12 and line; chi values all 12th roots, chi(a) in {1,z} []
  RW12L_equals_beta2_over_2 qualify=4032 pass=320 fail=3712  []
  RW12_equals_alpha2_over_2 qualify=4032 pass=320 fail=3712  [(1, (0, 0, 0, 6), (0, 0, 0, 0), (1, 0, 0, 0), '8P=', (4, 0, 0, 0), '4|a|^2=', (0, 0, 0, 0)), (1, (0, 0, 0, 6), (1, 0, 0, 0), (1, 0, 0, 0), '8P=', (16, 0, 0, 0), '4|a|^2=', (4, 0, 0, 0))]
  RW12_formula qualify=4032 pass=4032 fail=0  []
  RW1_N3 qualify=2016 pass=2016 fail=0  []
  RW1_N4 qualify=2016 pass=2016 fail=0  []
  RW1_NNone qualify=2016 pass=2016 fail=0  []
  RW1c qualify=22176 pass=5280 fail=16896  [(3, (0, 0, 0, 0), (0, 0, 0, 0), (1, 0, 0, 0)), (3, (0, 0, 0, 0), (1, 0, 0, 0), (1, 0, 0, 0))]
  RW2 qualify=22176 pass=22176 fail=0 N=3..12 and line; chi values all 12th roots, chi(a) in {1,z} []
  RW2_N3 qualify=2016 pass=2016 fail=0  []
  RW2_N4 qualify=2016 pass=2016 fail=0  []
  RW2_NNone qualify=2016 pass=2016 fail=0  []
  RW2c qualify=22176 pass=5280 fail=16896  [(3, (0, 0, 0, 0), (1, 0, 0, 0), (0, 0, 0, 0)), (3, (0, 0, 0, 0), (1, 0, 0, 0), (1, 0, 0, 0))]
 N=6 data=2205 eta-1=1605 eta+1=600
 N=8 data=2325 eta-1=1620 eta+1=705
 N=4 data=2580 eta-1=2025 eta+1=555
 N=1 data=715 eta-1=535 eta+1=180
 N=7 data=2295 eta-1=1665 eta+1=630
 N=2 data=745 eta-1=550 eta+1=195
 N=3 data=2580 eta-1=1995 eta+1=585
 N=None data=730 eta-1=555 eta+1=175
 N=5 data=2220 eta-1=1620 eta+1=600
  A1 qualify=113718 pass=113718 fail=0  []
  A1_N12 qualify=3447 pass=3447 fail=0  []
  B1 qualify=10530 pass=10530 fail=0  []
  B1_well_equals_port qualify=10530 pass=10530 fail=0  []
  B2a qualify=10530 pass=10530 fail=0  []
  B2b qualify=10530 pass=10530 fail=0  []
  B2c qualify=10530 pass=10530 fail=0  []
  B2c_exactly_one_prefactor_zero (count) qualify=621 pass=621 fail=0  []
  B3 qualify=10530 pass=10530 fail=0  []
  C_boundary(complex ratio, exactly one of gamma, omega real -> readable) qualify=2064 pass=2064 fail=0  []
  C_boundary(complex ratio, gamma=+-1, omega=+-1 -> unreadable) qualify=576 pass=576 fail=0  []
  C_boundary(gamma or omega = +-1) qualify=4950 pass=4950 fail=0  []
  C_readable_side qualify=5040 pass=5040 fail=0  []
  C_unreadable_side qualify=5490 pass=5490 fail=0  []
  D1 qualify=9016 pass=9016 fail=0  []
  D1_N12 qualify=1040 pass=1040 fail=0  []
  D1_N12_pairs_same_omega_different_gamma (count) qualify=995 pass=0 fail=0  []
  D1_line qualify=6700 pass=6700 fail=0  []
  D1_line_pairs_same_omega_different_gamma (count) qualify=6152 pass=0 fail=0  []
  D1_pairs_same_omega_different_gamma (count) qualify=8392 pass=0 fail=0  []
  D2 qualify=78 pass=78 fail=0  []
  D2_N12 qualify=44 pass=44 fail=0  []
  D2_line qualify=2 pass=2 fail=0  []
  D3_N12_nonreal_kappa_prime (count of site-states) qualify=19529 pass=13295 fail=0  []
  D3_line_nonreal_kappa_prime (count of site-states) qualify=234768 pass=0 fail=0  []
  D3_nonreal_kappa_prime (count of site-states) qualify=485472 pass=17351 fail=0  []
  D4 qualify=13761 pass=13761 fail=0  []
  D4_N12 qualify=1848 pass=1848 fail=0  []
  D4_N12_pairs_different_gamma (count) qualify=1735 pass=0 fail=0  []
  D4_line qualify=6700 pass=6700 fail=0  []
  D4_line_pairs_different_gamma (count) qualify=6152 pass=0 fail=0  []
  D4_pairs_different_gamma (count) qualify=12746 pass=0 fail=0  []
  IFF1 qualify=98852 pass=98852 fail=0  []
  IFF2 qualify=9234733 pass=9234733 fail=0  []
  IFF_sub_Im_omega0_Im_kappa_differs_eq qualify=18978 pass=18978 fail=0  []
  IFF_sub_Im_omega0_Im_kappa_differs_ne qualify=506956 pass=506956 fail=0  []
  IFF_sub_alpha0_or_beta0_eq qualify=49112 pass=49112 fail=0  []
  IFF_sub_alpha0_or_beta0_ne qualify=613580 pass=613580 fail=0  []
  IFF_sub_omega_pm1_eq qualify=36496 pass=36496 fail=0  []
  IFF_sub_omega_pm1_ne qualify=1463399 pass=1463399 fail=0  []
  IFF_sub_|2Re k|=n_eq qualify=4573 pass=4573 fail=0  []
  IFF_sub_|2Re k|=n_ne qualify=27727 pass=27727 fail=0  []
  K1 qualify=122912 pass=98852 fail=24060  [[(8, (2, 8, 10, 10), 4), (8, (2, 4, 10, 6), 4)], [(8, (2, 8, 10, 10), 5), (8, (2, 4, 10, 6), 5)]]
  K2 qualify=357570 pass=98852 fail=258718  [[(8, (3, 6, 9, 6), 0), (8, (3, 6, 9, 6), 1)], [(8, (3, 6, 9, 6), 3), (8, (0, 9, 9, 0), 10)]]
  K3 qualify=98852 pass=12325 fail=86527  [[(8, (6, 0, 6, 6), 0), (8, (6, 9, 9, 6), 0)], [(8, (6, 0, 6, 6), 1), (8, (6, 9, 9, 6), 1)]]
  K4 qualify=98852 pass=66312 fail=32540  [[(8, (2, 4, 10, 6), 0), (8, (2, 8, 10, 10), 0)], [(8, (2, 4, 10, 6), 1), (8, (2, 8, 10, 10), 1)]]
  LINE qualify=16859 pass=16859 fail=0  []
  LINE_converse_eta-1 (not claimed; information) qualify=138525 pass=138525 fail=0  []
step 4: chal3.py exit 0, no unexpected fails; fresh-directory rerun byte-identical (sha256 c658fd82...c4ee0c). Full log run3.log.
Findings: no KILL/WOUND. GAPs: same N (and eta=-1) for both data not stated in the iff; normalisation silent in RAIL_WEIGHT consequence
(holds unnormalised in my run); RAIL_WEIGHT proof of port (3,-1,L) silent on N=4 word RRR (ends rail R, harmless);
N=1,2 true value 8P=|alpha(1+2u-u^2)+beta gamma(1+u^2)|^2. Wording: "each of the five is read by a named event" (Re w and Im w Im k only after dividing by earlier readings); "exactly" in Reachable set is a definition.
