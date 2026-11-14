import Std

namespace TagEndpointBounds

/-- If a certified class count a is at most its true count x, and the positive
    true pair denominator d is at most the retained denominator D, then a/D ≤ x/d
    after clearing the denominators. -/
theorem certified_fraction_le {a x d D : Nat} (ha : a ≤ x) (hd : d ≤ D) :
    a * d ≤ x * D :=
  Nat.le_trans (Nat.mul_le_mul_right d ha) (Nat.mul_le_mul_left x hd)

/-- r,l are the named certificates. x,y,z are unresolved weights of true R,L,outside.
    The first cross product bounds the true right fraction below. The second bounds
    the true left fraction below and hence the true right fraction above. -/
theorem completion_sandwich (r l x y z : Nat) :
    r * ((r+x) + (l+y)) ≤ (r+x) * (r+l+x+y+z) ∧
    l * ((r+x) + (l+y)) ≤ (l+y) * (r+l+x+y+z) := by
  constructor <;> apply certified_fraction_le <;> omega

/-- For c2, common certification n/d on L and outside gives one probability
    (512*d-472*n)/(512*d-438*n). Compare to the curvature threshold using
    integer numerators with positive denominators (d>0, 0≤n≤d). -/
theorem common_certification (n d : Int) :
    444 * (512*d - 472*n) < 257 * (512*d - 438*n) ↔ 2816*d < 2853*n := by
  omega

/-- Across repetitions of the two-sign test, passing both is a subset of either
    pass event, and the two marginal pass counts together exceed the total by
    at most the both-pass count. The four cells allow arbitrary dependence. -/
theorem two_sign_pass_bounds (both plusOnly minusOnly neither : Nat) :
    (both + plusOnly) + (both + minusOnly) ≤ (both + plusOnly + minusOnly + neither) + both ∧
    both ≤ both + plusOnly ∧ both ≤ both + minusOnly := by
  omega

/-- Clearing a common denominator gives the arithmetic–geometric mean step
    for the two nonnegative Bernoulli moment factors. -/
theorem two_moment_factors (a b : Int) :
    4 * (a*b) ≤ (a+b)*(a+b) := by
  have h : 0 ≤ (a-b)*(a-b) := by
    by_cases hab : 0 ≤ a-b
    · exact Int.mul_nonneg hab hab
    · exact Int.mul_nonneg_of_nonpos_of_nonpos (by omega) (by omega)
  simp only [Int.sub_mul, Int.mul_sub] at h
  simp only [Int.add_mul, Int.mul_add]
  rw [Int.mul_comm b a] at h ⊢
  omega

end TagEndpointBounds
