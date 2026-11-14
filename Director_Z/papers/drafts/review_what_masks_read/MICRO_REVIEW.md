# Micro-review of the draft subsection "What position masks read of a character" (14 November 2026)

A boundary sweep by a sub-agent (same model family; not independent review). No proof breaks. Three sentences
were false as worded and several lacked a hypothesis; all are corrected in the draft by the patch in this
folder, applied by the director, and the draft compiles after it.

False as worded, now corrected:
1. "For a sharp start it depends only on eta and Re omega": it also carries |alpha|^2.
2. "no two rings do so for every value": a ring with N <= 2 (M = 1) reads Re u and fixes chi(B) up to
   conjugation by itself; the statement is for rings with N >= 3.
3. The fork was given with masks S_1..S_M only, so it had length M, against "no event of length at most M
   separates". The mask S_{M+1} = {M+1} is now written, and the sentence says "no port of length at most M".

Hypotheses added: the fair-count sentence and the port (2, 2 mod N, R) are for a sharp start with alpha = 1;
"no probability summed over the two rails separates anything" on N <= 2 needs eta = -1 (with eta = +1 on N = 2
two data sets gave 1.137 and 0.279); the mirror image in (iv) is now written out (x to -x with the rails
exchanged, S_1 = {-1}, port (M+2, -M-2, L)); on the line the polynomials of the last proposition are constants.
Remark (c) now says that (iv) as well as (i) fails for N <= 2.

The sweep's brute force (floating point, tolerance 1e-9, rings 1 to 9 and the line): 62 lines pass; the 6
failing lines are (i) and (iv) at N = 1, 2, outside their stated range. Parts (ii) and (iii) hold at N = 1, 2
as well. Files: `bf.py`, `bf_out.txt`.
