# NOTES (formalizer, Lemma R / Prop P steps 1,5 / ring factor)

## Control (answered before any Lean)
Commutative group, a = d = 1, b = c = h.
- delta = ad/(bc) = 1/(h*h) = h^(-2).
- Walk L,R from (0,R): step L from rail R has gain b = h (now on L); step R from rail L has gain c = h.
  Gain = h^2. Check against Lemma 0: rho=1, lam=1, n=1 (one L->R change), ends on R:
  a^1 d^1 delta^(-1) = h^2. Agrees.

## Log
- attempt1 (rw of ih into unfactored goal) failed; attempt2 (group tactic, noncommutative) failed; attempt3 (simp split on if lastRail) failed; attempt4: generalize E(last) + Additive/abel macro: lemma0_gen passes.
- attempt5 (lastRail_eq, closure_induction elaboration, ring_fixed with nested smul) failed; kept as attempt5_partial.lean.
- Final: PrepReduction.lean, exit 0, sha256 1c8057d47b98fb2cc2666bfec7e7505192451adb64b280b9b657b7cd81ee1aa6.
  Axioms: subsets of {propext, Quot.sound, Classical.choice}. Output in run_output.txt.
- No statement in the brief turned out false. Step 1 proved without finiteness of G: only a and bc of finite order.
  Step 5 proved in any monoid for any element (orderOf 0 case included).
- Control checked in Lean too (example at end of namespace).
