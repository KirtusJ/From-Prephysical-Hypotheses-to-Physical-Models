import Mathlib
/-!
The coincidence used for three classes of winding (draft Theorem `thm:fgthree`), as identities in a
commutative ring.  `x` stands for the gain β of one winding and `η` for δ^{-k₀}; the relation β³ = δ^{k₀}
is `η * x^3 = 1`.

* `coincidence`: (1+2x)(1+(2+η)x) = x (4+η+ηx)(1+x) + (1 - η x³), with no hypothesis.
* `coincidence_folded`: under η x³ = 1 the two products differ by the factor x.
* `separation_plus`, `separation_minus`: the two values compared in the induction differ (σ = 1, σ = -1).
-/
theorem coincidence {R : Type*} [CommRing R] (x η : R) :
    (1 + 2 * x) * (1 + (2 + η) * x) = x * ((4 + η + η * x) * (1 + x)) + (1 - η * x ^ 3) := by
  ring

theorem coincidence_folded {R : Type*} [CommRing R] (x η : R) (h : η * x ^ 3 = 1) :
    (1 + 2 * x) * (1 + (2 + η) * x) = x * ((4 + η + η * x) * (1 + x)) := by
  have := coincidence x η
  rw [h] at this
  simpa using this

theorem separation_plus : (1 : ℤ) * (4 + 1) ≠ 2 * (2 + 1) := by decide
theorem separation_minus : (-1 : ℤ) * (4 + (-1)) ≠ 2 * (2 + (-1)) := by decide

#print axioms coincidence
#print axioms coincidence_folded
#print axioms separation_plus
#print axioms separation_minus
