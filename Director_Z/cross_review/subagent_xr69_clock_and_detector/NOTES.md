# NOTES xr69
CONTROL: p(phi)=(1+0.8cos phi)/2: max 0.9 (phi=0), min 0.1 (phi=pi). Mixture w of phi=0 vs phi=pi: w*0.9+(1-w)*0.1=0.5 -> w=1/2 (independent of V when V>0).
Step 1 done: read both notes, Lean, checker heads.
Step 2: checker reruns from copies: both exit 0, output byte-identical to filed JSON (sha 976f23e8... common_clock, b9dee935... detector).
Step 3: Lean 4.19.0 present locally; both files exit 0, no output. Axioms still to print.
Hand derivations: A (1),(2),V_m,(4),example 10/21, tick-2/3 formulas all re-derived OK. B (1),(2),Bloch map,45/29/21/41,twirl 45/25/21/41,W=1/4,(3),two alias examples,error identity,dW identity all re-derived OK.
Step 4: own program xr69_check.py run; result xr69_result.json (mode x, rerun in rerun/ byte-identical). Exit 1 = 129 kept failures of the non-claim predicate B8_mixedsign (sign-changing visibility gives W<0 or false zero; agrees with the note's warning). All claim predicates 0 fail.
Step 5: Lean 4.19.0 axioms: A none; B twirledOnlyRail and allZeroOfSum propext+Quot.sound, others none. No sorry/native_decide.
Findings: no arithmetic defect. GAPs: Lean coverage (A: R start, R port only, 4 of 16 four-tick schedules, no cosine/measure/detector/minimality step; B: twirl only for one meter, Bloch step hard-coded for two phases). A13: within-flight varying gain passes {1},{1,3}; {3} catches. B6/B7: rail-blind coherent detectors: fair bit -> blind, any biased bit -> false pass intact.
ez0 helper rerun with segment check; see output in report
