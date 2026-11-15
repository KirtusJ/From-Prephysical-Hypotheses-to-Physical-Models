# Corollary "the list is an orbit": director's check (14 November 2026)

- **Micro-review.** No failure on items 1, 2, 3 and 5. Item 4 was false as worded, and the director checked its counterexample by hand. The sentence was replaced, then replaced again after the challenger's enumeration. Its program, rerun, gave output byte-identical to `run1.txt`.
- **Formalizer.** `MaskOrbit.lean` (Lean 4.12.0, Mathlib). The director recompiled it: exit 0, twelve theorems, axioms `propext`, `Classical.choice` and `Quot.sound`. The converse needs less than the corollary assumes: |a''| = |a'| ≠ 0 and |c''| = |c'| ≠ 0. The proof was tightened to its explicit g and λ.
- **Challenger.** No defect in the corollary or its proof. Changes made:
  - a gap on realizing a coin as a character, closed with one clause;
  - a sentence false as worded about changes of description from starts in both rails, replaced; the director checked the counterexample by hand (P = 2 against P = 1);
  - a gap in an inference, made explicit;
  - the four-site sentence corrected;
  - "the corollary" named.

  The challenger also found that η = −1 is needed (with η = i, coins with equal Re(u^M) are separated), and this was added. Its program, rerun in a fresh folder, gave output byte-identical to its own runs (`21904e92…`).
- All three reviewers are of the director's model family, so this is not independent review.
