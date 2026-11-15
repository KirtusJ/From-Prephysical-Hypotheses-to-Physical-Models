# Wildcard, seed "unrolled", 15 November 2026 (same model family as the director; not independent review)

CONTROL: CLAUDE.md "Lessons paid for" has 8 items; the first is "Test the hypothesis in the predicate."

## Step 1: looked around
Read in full: papers/drafts/G10_subsection_winding_products.tex; total_positivity/NOTES.md, product_checks.py and its
result; pcp_workers/STATE_2026-11-15.md; listing of winding/, challenger/2026-11-15b_products (exists: the products
were already given to a challenger), wildcard/2026-11-13_hinge.
Checked by hand and set aside (found nothing wrong): the unrolled-lattice proof of thm:tp (sinks strictly increasing
needs M>=2, true for N>=3; u_j=n(l0+jM), v_j=n(l0-1+jM)); the Hurwitz transposition/reversal in cor:tp(iii) and
"beginning with a root of v/g" (tested on (1+Y)^2, (1+Y)^3); e_beta*A=B expanded by hand; the Toeplitz step of
thm:fgprod(ii) (restrictions pi_k=0 and pi_0=0 via P=e_1 and P=e_beta); 4*sigma+1 != 4+2*sigma for both signs.

## Step 2: choice
Chosen: Remark rem:tpprod(b), "No such pair is known to the author for s>=5" (line 131 of the draft), because the
question is finite and can be closed rather than sampled, and NOTES.md records only an unkept exploration.

## Step 3: lemma (written proof)
Pair: multisets a, b of n=s-1 positive integers with e_j(b)=e_{s-j}(a), 1<=j<=n. Symmetric in a, b.
(1) For positive integers prod >= sum-(n-1) (from xy >= x+y-1, induction), equality iff at most one entry > 1.
(2) j=1 and j=n: sum(b)=prod(a), prod(b)=sum(a). With D(c)=prod(c)-sum(c): D(b)=-D(a), so by (1) |D(a)|<=n-1.
(3) If a has at most one entry >1 then D(a)=-(n-1), D(b)=n-1 > -(n-1), so b has two entries >=2. Hence every pair
    has a member in F_n={c: two or more entries >=2, D(c)<=n-1}.
(4) F_n is finite: with k>=2 entries y_i>=2, prod(y)-sum(y) is strictly increasing in each y_i.
(5) For c in F_n the partner has product sum(c): finitely many candidates. So the full list for each s is computable.

## Step 4: program coincidence_pairs.py (predicates P1-P4 in the docstring before the first run)
Command 1 (in scratch dir): python3 -B coincidence_pairs.py r_coincidence_S12.json 12   exit 0; P1-P4 hold.
Command 2: python3 -B coincidence_pairs.py r_coincidence_S80.json 80   exit 0, 46.5 s; P1-P4 hold.
Result: s=3: {(1,5),(2,3)} and the self-pair {(2,2),(2,2)}. s=4: {(1,1,7),(1,3,3)}, {(1,1,8),(1,2,5)} and the
self-pair (1,2,3). s=5..80: NO pair. Self-pairs have D=0 (a=b), so they give no relation.
New relative to the draft: the second pair for s=4, and non-existence for 5<=s<=80 in the stated form.
FAILED, kept: first rerun for byte comparison was launched as "python3 -B ../coincidence_pairs.py ..." and the
result differed from the original at line 2 (the recorded command string). Not a difference of content; rerun again
with the identical command line in step 5.

## Step 5: rerun and close
Rerun in fresh dir rerun2 with the program copied in and the identical command line
"python3 -B coincidence_pairs.py r_coincidence_S12.json 12": exit 0, bytes equal to the first result (cmp).
The S80 run was not rerun (46 s; one run, exit 0, result read back: P1-P4 hold, 0 pairs for s=5..80).
Not done / limits: no proof of non-existence for all s>=5 (tried Maclaurin and the j=2, j=n-1 equations briefly; no
contradiction found by hand). Scope is the draft's stated form only: factors a_i+X and 1+b_jX, trivial twist. Factors
p_0+p_1X with both coefficients >1, a shift X^j with j>1, or a non-trivial twist are NOT covered.
Files here: coincidence_pairs.py (program; three-line description is its docstring head), r_coincidence_S12.json,
r_coincidence_S80.json. No repository file was changed; no patch is needed (a wording suggestion only).
e529f91572879d279a6b43e524d2b70b6ea65ae5adec719b12b2b982e7bcfb58  coincidence_pairs.py
bac71ef53197ecf3fec2e81b9ce36cd3bdb6ae8d367800b45bb0411c55485663  r_coincidence_S12.json
9f98f18899307c70b763c717b1fbcea50595021e382492f16223fe4f83bb0b40  r_coincidence_S80.json
