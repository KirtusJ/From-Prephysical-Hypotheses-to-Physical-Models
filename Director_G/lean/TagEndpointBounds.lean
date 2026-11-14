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

end TagEndpointBounds
