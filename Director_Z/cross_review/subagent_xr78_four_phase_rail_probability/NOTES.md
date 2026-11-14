# NOTES xr78
## CONTROL (answered first)
NO. The second condition is implied by the first (both sides equal 1). Counterexample: f = 1/2 + cos(3 theta): cos(3(theta+pi)) = -cos(3 theta), so f(theta)+f(theta+pi)=1, and f is not 1/2 + A cos + B sin. Any odd harmonic works.
## Step 1 read note/checker/Lean (done)
Hand check of proof: square coords b,u,2u-b,u OK; (1),(2) OK; functional (1+3u)/2 OK; mean|1+3u|=5/3 OK; (3) follows; calibration algebra OK; tilted sqrt(eta) OK.
Premise: square condition == equal 50/50 mixtures with same Bloch centroid give same rate == mixture equivalence (prep noncontextuality) for square mixtures. Not Gleason (measurement side); it is the state-side convex-linearity argument.
Harmonic analysis: in frame of square axis, defect picks m = 2 mod 4 components; invariant subspace => only l=0,1 survive.
Stability: point perturbation F=affine+c*1_p gives dev c, eps c/2 => ratio 2; so best constant in [2,10/3]; 10/3 not shown attained.
## Step 8/9 done
Checker copy: python3 exit 0, python3 -O exit 0, both JSON sha 0923aa7f...bf10 == filed (cmp identical). Second run into same dir refuses (FileExistsError, exit 1).
Lean 4.19.0: exit 0, axioms [propext, Quot.sound]. Formalizes only the integer telescoping identity 2^k e(start) = e(start+k) + tailWeight. Nothing about sphere, squares, averaging, (3).
README line 21 of Director_G: "forces ... affine", "Sharp calibration selects squared amplitude" (summary wording).
## Step 7 program written: xr78_check.py (predicates in docstring before first run)
First run crashed in P2 (my number type: probabilities in Q(sqrt2)); no result written; v0 kept; predicates unchanged.
## Own program run: run1 exit 0, run2 exit 0, bytes identical; all predicates pass, none failed. Third run into existing file refused.
