# Four-gain theorem: after a challenger (14 November 2026)

A challenger, working from FINDINGS.md alone with its own program, found no defect in Lemma 0, Lemma 1,
Theorem 2, Corollary 3 with its two counterexamples, or Theorem 6, in its range, and one real fault in a side
claim (G3). Rerun by the director in a fresh directory: exit 0, 14 seconds, result byte-identical (sha256
1acf768b...ced52da96). Same model family as the authors; not independent review. No gate is claimed; nothing
here is in the paper.

## What it confirms (qualifying / pass / fail)

- Lemma 0 on the line, lengths to 10, eight groups including non-cyclic ones: 112 / 112 / 0; and the quotients
  of gains generate exactly <delta>.
- Lemma 0 on rings of 1 to 8 sites, lengths to 14, same kappa on both rails: 896 / 896 / 0; the quotients
  generate exactly Delta_N, so Delta_N is the smallest subgroup that works.
- Theorem 2, dimension against the formula: 1233 / 1233 / 0, stable at box size 3. Z2, Z3, Z4, Z2xZ2
  exhaustive, Z6 in 47 cases; for Delta = <delta>, Delta = A and one intermediate subgroup. Sub-cases all
  pass: delta trivial (463); a = d and b = c (115); H trivial (37); K smaller than Delta (164); r odd with
  Delta larger than <delta> (311); a non-conjugate pair present (66).
- Theorem 6 on arbitrary sets of walks (not product events), line and rings of 1 to 6 sites: 1197 / 1197 / 0,
  including 329 linear solutions and 105 mixed non-conjugate ones.
- The proof, step by step: follows, with the remarks below.

## Corrections accepted (FINDINGS.md stays as filed; these lines amend it)

1. **G3 is wrong as worded, and right once the period is named.** "A closed walk of length divisible by the
   period" must mean the period of the DERIVED digraph (closed walks of gain 1), not of the ring digraph.
   Counterexample, checked by the director by hand: Z2 written additively, (a, b, c, d) = (1, 0, 0, 1), ring
   of 3 sites. delta = 0 and Delta_N is trivial. The ring digraph has closed walks of lengths 2 (L then R,
   gain 0) and 3 (three right steps, gain 1), so its period is 1 and the gains of all its closed walks
   generate Z2, which is not Delta_N. In the derived digraph three right steps do not close (gain 1), the
   period is 2, and the closed walks of even length have gains in the trivial group. With the derived period
   C_0 = Delta_N in all 360 cases computed (206 of them strongly connected); with the ring period it fails in
   60 of 206.
2. Corollaries 4 and 5 use site-independent F_R, F_L and factor 2 (through Lemma 1); the statements must say
   so.
3. G4, third bullet, was headed PROVED: "consistent only as the zero rule" needs PREP(<delta>) and
   F_L = F_R o T_c. Computed without PREP it held in 134 of 134 cases. So: PROVED under PREP, COMPUTED without.
4. G4, second bullet: "does happen when H is smaller" needs r even.
5. Proof, Step 3: the invariance under T_delta is available because delta lies in K = H cap Delta (delta is in
   H and in Delta in every case the theorem covers). The text did not say so. The director had noted this in
   DIRECTOR_CHECK.md.
6. Proof, Step 6: one line is missing, B(s + s', 2t) = 2 B(s + s', t), between "with s' = 0" and "so B is
   additive in s".
7. Proof of part 1: real values are needed for the maximum argument; for complex values apply it to real and
   imaginary parts.

## Kept: a failed predicate of the challenger

Its power control (non-solutions must fail on random events) missed in 5 of 1232 cases, because 8 events per
case are too few in degenerate carriers (Z2 with gains (1,1,0,0) on a ring of 1 site, and others). Not
followed up. It bears on the strength of the test of Theorem 6, not on the theorem.

## Not checked

PREP for four gains (a hypothesis; nothing is known); Z6 beyond 47 cases; the periodic theorem's set U(D);
Lean (Steps 3 and 6 are the natural candidates); G4 with F_L free.
