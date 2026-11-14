# Director's check of the two-rail theorem (14 November 2026)

The builder's FINDINGS.md is filed as received. Same model family as the director; not independent review. No
gate is claimed; this is a statement about the model, and nothing here is in the paper yet.

Rerun by the director in a fresh directory: `rails.py`, exit 0, 14 seconds, result byte-identical (sha256
fc71ae35...3327976). A first rerun failed for a missing argument (kept as a failed attempt).

Steps checked by hand:
- Lemma 0: the word Lw from a sharp R start has gain b G_L(w); identity (1) with t+1, l+1, the same m and e;
  a B / b = c / a. Holds.
- B1: tick 1, well 1, amplitude chi(a)(alpha + beta gamma)/sqrt 2, so P = 1/2 + Re kappa. Holds.
- B3: from rail L the admitted words R^(D+1) and L^D R have (k, m) = (0,0) and (1, D), so S_L = 1 - s omega;
  T = conj(S_R) S_L = -2 i s Im omega; the formula follows. Holds.
- Theorem D: from a sharp R start the L component at any site carries chi(a/c) = conj gamma, so gamma cancels in
  kappa' = conj(psi_R) psi_L gamma. Holds.

What it settles, in the model:
1. The follow-up's example is right (probabilities 1 and 1/2; the follow-up's 4 and 2 are the same numbers
   before normalization).
2. A start in both rails reads exactly Re kappa and Im omega Im kappa more, with kappa = conj(alpha) beta
   chi(c/a). It does not read chi(c/a) as a phase, nor more of chi(B) than omega = chi(B)^D.
3. Steps and position masks cannot prepare such a start with a phase free of chi(c/a): every reachable site
   state carries the compensating phase. So Proposition 1's list of what is undetermined stands for everything
   the walk can prepare for itself; it shortens only if a rail superposition is supplied from outside.
4. Conjugation is read only with a start whose relative amplitude is not real, in a rail phase convention fixed
   from outside.

Open: whether |alpha|^2 itself is readable; eta not real; N = 1, 2; Lean for the one identity.

## Lean, same day

`Director_Z/lean/TwoRail.lean` (Lean 4.12.0, Mathlib v4.12.0), sha256 70e27809...131a3296. Rerun by the director:
exit 0, axioms propext, Classical.choice, Quot.sound only, no sorry. Proved, each in a general form: the two
rail-weight identities (R1, R2), the first-tick formula (R3), the fork cross term (R4), the fork from a two-rail
start with the sign of its last term confirmed on a numerical instance (R5), and the cancellation of gamma
(R6). Lean found a shorter argument for the rail weight: by the gain relation alone the four-term sum is
2 alpha chi(abc); no interference computation is needed, and of the unit-modulus hypotheses only
|chi(abc)| = 1 is used. Not formalized: the counting of words (which words are admitted at a port). Same model
family; not independent review.
