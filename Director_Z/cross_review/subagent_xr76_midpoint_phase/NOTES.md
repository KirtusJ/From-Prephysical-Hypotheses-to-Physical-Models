# NOTES xr76
CONTROL: U=[[1,i],[i,1]]/sqrt2, start 0. UU = [[0,i],[i,0]] -> P(end in 1)=1. UZU = diag(1,-1) -> P(end in 1)=0.
STEP1 read note. Own derivation done before reading proof: (UP_lU)_LR=U_LR(A+lB); |A|=|B|; L2+C_-1=c+int 4q(1-q) dnu; nu mass 1-c => D=int (q-1/2)^2 dnu. True for all U(2), count = independent fair per tick, rates per launch, plate exactly diag(1,-1), same U both sides.
W = c/2((a-1)^2+1)+int q(r-a)^2. Full identity, bounds, beta statements, H(q) false pass, Chebyshev kernel all rederived by hand: follow.
Candidate gaps: inactive plate (lambda=1) false pass for D; post-selected normalisation; non-unitary alternatives.
STEP5 Lean 4.19.0 on copy: exit 0; axioms plusMinus,balance [propext, Quot.sound]; histories [propext]. Lemmas = integer parallelogram, integer balance polynomial, congruence of products under pointwise-equal Nat kernels. Not formalized: complex path sum, unitarity |A|=|B|, integral/mixture, Chebyshev kernel, redraw independence, infinite records.
Helper check_unknown_two_mode_coin.py not in export; taken from repo working copy Director_G/ (sha afdf825d...), head not verifiable.
STEP4 checker rerun python3 and -O: exit 0 both, byte-identical to filed JSON (sha 65f7ec99...); refuses overwrite (exit 1).
STEP3 own program prog/xr76_attack.py -> prog/result_run1.json; exit 0; rerun in rerun/ with -O byte-identical; refuses overwrite. All predicates pass; 0 failed cases; 1 non-unitary case rejected by hypothesis filter.
Findings: identity holds on U(2); false passes P7 (note's), P8 (universal: any U has a setting-dependent V), P9 (inactive plate), P16 (post-selection, rail confusion 1/65) all lie outside stated hypotheses; abstract omits retention/plate-calibration premise.
