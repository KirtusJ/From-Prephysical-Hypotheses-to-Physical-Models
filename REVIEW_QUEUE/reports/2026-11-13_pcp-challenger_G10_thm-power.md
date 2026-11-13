Target: edition/PAPERS/G10_*/source/body.tex, Theorem 5.2 (label thm:power), at commit e53742c.
Outcome: NONE FOUND (two wording remarks).
Reviewer kind: pcp-challenger + pcp-micro-review, served by the queue session; same model family as the author, read the paper text only. Not independent review.

Proof, step by step
- "Single walks give c = d": follows. The diagonal of A*A is the out-degree because the values of chi have modulus one.
- The 2(d-m) other successors carry modulus one; the component at a common successor has modulus |1+u_z|: follows.
- sum over Z of u_z = 0 from orthogonality of columns y1, y2: follows (checked exactly in Z[zeta] on 528 instances).
- h(2) = 2m: follows.
- Convexity bounds for 0<p<2 and p>2, strictness from h0 <= m < 2m: follow. The limit at 0 is used on (0,2] by continuity; fine.
- "if" direction (p = 2): Lemma 3.1 of G9; follows.
- Hypotheses used and present in the statement: modulus-one gains, A*A = d, two walks of equal length from a common vertex, distinct ends, a common successor. d >= 2 is redundant: m >= 1 and sum u_z = 0 force m >= 2.

Wording remarks (not defects)
- "gains of modulus one": the gains are group elements; the values of chi are meant.
- The proof uses the unit modulus of u_z and sum u_z = 0 only through sum |1+u_z|^2 = 2m. A termwise argument (weighted arithmetic-geometric mean against the point 1) gives the result without the limit h0; see the formalizer report of the same date.

Computed (challenge_thm_power.py, seed 20261113, predicates fixed first, result file beside it)
- 100 carriers built, 88 satisfy A*A = d exactly (the 12 failing are a deliberately bad matrix and its variants, excluded); all 88 have a merging pair; 528 (carrier, pair) instances. Families: Fourier blocks d = 2..6, W(4,3), conference matrix C6, circulant W(7,4), switched and permuted copies, four tensor products, signed arc digraphs of rings of 4 and 5 sites.
- mu_2(Ext S) = d mu_2(S) exactly on all 528.
- gap(p) = mu_p(Ext S) - d mu_p(S) is negative at p in {1e-6, .25, .5, 1, 1.5, 1.9, 1.99} and positive at p in {2.01, 2.1, 3, 4, 6, 8} on all 528; smallest |gap| 0.0138 (measured separation, not a threshold).
- The two bounds of the proof hold on all instances.
- 20000 random configurations of unit u_z with sum zero (all qualify): same signs, smallest |gap| 0.0138.
- No p on a grid 0.05..8 (step 0.05, p = 2 excluded) with |gap| < 1e-9.
- Binary tree, gains +1: every p consistent on 200 events (the paper's remark that the hypothesis cannot be dropped).

Micro-review boundary cases
- d = 2 block: PASS (6 instances). Some u_z = -1 (h0 < m): PASS (303). m < d: PASS (231). All |1+u_z| = sqrt 2: PASS (21). p = 1e-6: PASS. p = 8: PASS.

Failed predicates: none. (One run aborted on a Python syntax error in a result-key name before any computation; the predicates were not changed.)

Not checked: carriers with non-abelian gain groups; countable carriers other than the tree; the attribution to Li and So; Lemma 3.1 of G9 beyond its use.
