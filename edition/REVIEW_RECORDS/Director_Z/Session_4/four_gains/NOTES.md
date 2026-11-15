# NOTES (build_multi) — appended after each step

## Step 0. CONTROL (answered first)
C = Z/4, generator h. Unitary characters psi with 1 + psi(h) = 0: exactly ONE, psi(h^j) = (-1)^j
(the four characters have psi(h) in {1, i, -1, -i}).
sigma_psi(m) for m = (2,1,0,1): 2 - 1 + 0 - 1 = 0.

## Step 1. Read body.tex lines 770-935 (eq:ppcons ... thm:posprodq). Next: thm:periodic.

## Step 2. Derivation on paper (before any run)
Carrier: vertices (x,R),(x,L); arcs (x,R)->(x+1,R) gain a [RR], (x,R)->(x-1,L) gain b [RL],
(x,L)->(x+1,R) gain c [LR], (x,L)->(x-1,L) gain d [LL]. One-site equation (as Lemma onesite):
  F_R(T_a U + T_c V) + F_L(T_b U + T_d V) = 2 F_R(U) + 2 F_L(V).   (E4)
Rail dependence is forced in general: V=0 gives F_R(T_aU)+F_L(T_bU)=2F_R(U), not F_L=F_R.
Plan found by hand: (i) V=0 and U=0 make (F_R,F_L) harmonic for a doubly stochastic chain on finite
orbits => F_R invariant under T_h, h in H=<a,d,bc>, and F_L = F_R o T_c. (ii) then (E4) becomes the
paper's (Eq0) with h := delta = ad/(bc). (iii) quotient argument + parallelogram law => degree <= 2.
Expected dimension (full equation on N^A): |A/H| + #{unordered {chi,chi'}: chi(delta)=chi'(delta)=-1,
chi chi' trivial on H}.  The brief's conjecture (1 + classes {chi, conj chi}) is expected to hold iff H = A.
OBSTACLE found by hand: at one vertex and one length on the line all gains lie in ONE coset of <delta>
(n_RL = n_LR or n_LR+1), so "all pairs (U,V) in N^A x N^A realizable" is impossible unless <delta>=A.
=> must also solve the coset-restricted equation. Expected dim there: 1 (ord delta odd) or 2 (even).
Program next; predicates fixed in docstring.

## Step 3. four_gain.py written (predicates P1..P9 in docstring before first run). First run started.

## Step 4. FINDINGS.md written (theorems and proofs) while run 1 is in progress.
CORRECTION to Step 4: FINDINGS.md was NOT written. The Write tool refused it ("Subagents should return
findings as text, not write report files"). I did not go around the refusal; the full statement and
proofs are delivered in the hand-back report instead.

## Step 5. Run 1 finished: exit code 0, 2m25s, FAILED PREDICATES: 0 (result_run1.txt, 140 lines).
P1..P9 all pass on first run; no predicate was changed after the first run. Rerun in fresh directory next.

## Step 6. Rerun in fresh directory rerun/: exit 0, result byte-identical to run 1.
sha256 four_gain.py      65cf09618ccd6bbb934c20a1fb18caf00431f9beb0607e0d30e05ebae049823a
sha256 result_run1.txt   5657f0a54814ecdd8345ede657d7c2d906a27efc2434178d1b55cdfa2b2428af (= rerun/result_run2.txt)
Cases: Z2 16/16, Z3 81/81, Z4 256/256, Z2xZ2 256/256 (all quadruples); Z6 120 sampled; Z2xZ4 60 sampled.
H = A in 14, 78, 224, 168, 101, 48 cases; brief's conjecture equals the found dimension exactly in those
and in no other (P1c). Failed predicates: none. Failed ATTEMPTS kept: (1) brief's conjecture false for H != A
(Z2, a=d=1, b=c=h: dim 2 not 1; Z4, a=h^2, b=c=d=1: dim 5 not 2); (2) full preparation on N^A x N^A
impossible unless <delta> = A (coset lemma); (3) FINDINGS.md refused by the Write tool; (4) no Lean file.
Limits of the computation: boxes n <= 3 for |A| >= 6 (n = 4 on 12 sampled Z6 cases), n <= 4 line, so for
r = 6 the box does not contain a full <delta>-orbit multiset; ring-like Delta only k = 1, 3.
