# NOTES chal_four (challenger, same model family as author; not independent)
Step 0: read FINDINGS.md only. Control by hand enumeration first (program repeats it by brute force):
 walks len 4 ending (0,R): step words RLLR, LRLR, LLRR. gains: RLLR a+b+d+c=6=2; LRLR b+c+b+c=0; LLRR b+d+c+a=2.
 multiset {0,2,2}; delta=1+3-0-2=2; <delta>={0,2}; coset = <delta> itself (kappa=a^2 d^2=0).
Step 1: hand check of proofs done (see final report); writing chal.py.
Step 2: chal.py run exit 0 (13.8 s), rerun in rerun/ compared. Results in result.txt. P3 1233/1233, P5 reading I fails 60/206 qualifying,
 reading II 206/206. P4n 5 undetected non-solutions = weak power control (8 events), kept. See final report.
