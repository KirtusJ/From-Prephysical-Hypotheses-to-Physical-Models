# NOTES (formalizer, char separation)
CONTROL: w = exp(2 pi i/3) has Re(w) = -1/2, so 2 + 2*Re(w) = 1.
Step 1: wrote first draft CharSeparation.lean (abs form; L3 via Chebyshev real-part polynomials, stronger L3_re: b.re = b'.re)
Step 2: first run exit 1: line 49 'ring' had no goals (simp closed re_pow2 expansion); sorryAx appeared in L3 as a consequence. Fix: drop that ring.
Step 3: second run EXIT 0, no warnings; all six #print axioms show only propext, Classical.choice, Quot.sound. sha256 3ebdad49d6ce3bb441f93858f2546eb3e2ad546cb9d6384f78136cc0d4e97a4a. L1-L4 all proved; copy in this folder. Done.
