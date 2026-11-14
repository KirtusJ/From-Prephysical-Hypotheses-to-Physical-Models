# NOTES (challenger, draft subsection "What position masks read of a character")
Same model family as the author: not independent review.

## Step 0, CONTROL (by hand enumeration of all 8 words of length 3 on Z/4; program repeats it)
Words ending at site 3 on rail L: only RLL (sites 1,0,3) and LRL (3,0,3). (RRR ends at 3 on rail R; others end elsewhere.)
From (0,R): RLL = a,b,d -> chi = 1*1*(-i) = -i ; LRL = b,c,b -> 1*i*1 = i ; sum 0.
From (0,L): RLL = c,b,d -> i*1*(-i) = 1 ; LRL = d,c,b -> (-i)*i*1 = 1 ; sum 2.
P = 2^-3 * |(1/sqrt2)*0 + (1/sqrt2)*2|^2 = (1/8)*2 = 1/4.   CONTROL ANSWER: 1/4 exactly.

## Step 1, read the draft once (only the named .tex). Hand check of proofs in progress; program being written.

## Step 2 (resumed after cut-off): re-read corrected draft as instructed by parent; digest recorded above in shell output.

## Step 3: chal.py written, predicates in docstring before first run. Smoke run next (ncar=3).

## Step 4: smoke run (ncar=3) exit 0, 2m10s, file smoke1.txt. No failure inside hypotheses. Outside-hypothesis failures kept: I1n2/I2n2/IVn2/IVmn2 (N<=2, also for SHARP starts), N2b, *_etaNot-1, PREP2f (factor 2^-t). ETA passes (port (3,-1,L) reads Re eta). Final run ncar=6 next -> results_final.txt

## Step 5: final run exit 0, 4m10s. chal.py sha256 7654e0cf...f009a ; results_final.txt b9017ee5...62fb. Draft digest rechecked. Report being handed back.
