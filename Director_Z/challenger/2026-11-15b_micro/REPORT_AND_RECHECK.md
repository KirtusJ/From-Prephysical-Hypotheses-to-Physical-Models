# Micro-review of boundary cases of thm:fgprod, thm:fgthree, cor:pplus8 (draft), 15 November 2026

Sub-agent `pcp-micro-review`, of the author's model family; by hand, no program. Control answered correctly (three parts; for r odd the value is alpha_m times the product of the counts).

1. k = 1 and factors in one coset: TRUE AS WORDED.
2. s = 2: true, but the proof of thm:fgprod(ii) cites pairs from thm:fgadj, which is stated for s >= 3, and part (iii) used the letter k of thm:fgtwo in another sense. Closed: thm:fgprod is now stated for s >= 3 (two classes are settled by thm:fgtwo).
3. r = 2, k_0 odd: A has signed sums (3, 2, -1), B has (1, 3, 2); count 12, squares 14, cross term 7 at both with the sign sigma = -1 on eps_2 eps_0, and 1 against 11 without it. TRUE AS WORDED. The director recomputed these six numbers by hand: 3*2 + 2*(-1) - (-1)*3 = 7 and 1*3 + 3*2 - 2*1 = 7.
4. General m in one coset: true; the letter m was used for two things in thm:fgthree. Closed.
5. cor:pplus8 with an empty side and at M = 8: TRUE AS WORDED.
6. Remark (a): "removes this dimension" said more than the theorem (which acts for M >= 8, not on the small rings where the dimension was seen). Closed by rewording.
