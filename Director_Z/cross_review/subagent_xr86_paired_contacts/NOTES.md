# xr86 notes
## CONTROL (answered first)
chi_{j,k} is a function of a-b alone iff it is trivial on the diagonal {(a,a)}, i.e. j+k = 0 mod 4:
(j,k) in {(0,0),(1,3),(2,2),(3,1)} -- 4 characters, chi = i^(j(a-b)).
Restriction to diagonal: chi_{j,k}(a,a)=i^((j+k)a); 16 characters -> 4 restrictions, so exactly 4 distinct characters share each restriction.
## step: checker + lean
checker copy needs transitive imports (check_joint_phase_records -> check_equal_clock_lags); copied all check_*.py. Lean 4.19.0 exit 0, axioms [propext, Quot.sound] for both theorems.
## step: own program written (predicates in docstring), first run
## step: own program run1 exit 0 (9m27s; no second run for byte comparison, budget)
P1 16/16, P1x 16/16, P2 3 qualifying (n=2,4,6) pass, n=3,5 not qualifying; P3 48 of 2560 settings distinguish, all two-pair all-odd lags;
P4 M=3,4,6,8 qualify, M=2 not; P5 9/9; P6 23/23; P7 81/81 with 24 infeasible cells kept; P8 6/6; P9 1/1.
Checker rerun: byte-identical (python3 -B and -O), sha 68a14cca...; Lean exit 0, axioms propext, Quot.sound.
