import Std

/-! Integer certificate for the randomized source-revival audit.

Use a common positive denominator d for revival p/d and survival a/d.
The flat branch has p/d ≤ 1/2 and a/d ≤ 1. On the upper branch, survival
is at most 3/4 + √((p/d)(1-p/d))/2. When 4a > 3d, this is equivalent to
the squared inequality below. The formalization starts at these scalar
branch bounds; the quantum instrument and experimental sampling are separate.
-/

namespace SourceRevivalTangent

private theorem square_nonnegative (x : Int) : 0 ≤ x * x := by
  by_cases h : 0 ≤ x
  · exact Int.mul_nonneg h h
  · exact Int.mul_nonneg_of_nonpos_of_nonpos (by omega) (by omega)

/-- Clearing the square root leaves an exact square at p/d = 49/50. -/
theorem gap_identity (d p : Int) :
    (49*d - 48*p) * (49*d - 48*p) - 196*p*(d-p) =
      (50*p - 49*d) * (50*p - 49*d) := by
  simp +arith [Int.sub_mul, Int.mul_sub, Int.mul_assoc, Int.mul_comm, Int.mul_left_comm]
  simp only [← Int.mul_assoc]
  omega

/-- With p=u²/(u²+v²), this is twice the denominator times the tangent
slack on the upper boundary. It also checks the amplitude equality u=7v. -/
theorem amplitude_gap (u v : Int) :
    70*(u*u+v*v) - 7*(3*(u*u+v*v)+2*u*v) - 48*u*u =
      (u-7*v)*(u-7*v) := by
  simp +arith [Int.sub_mul, Int.mul_sub, Int.mul_assoc, Int.mul_comm, Int.mul_left_comm]
  simp only [← Int.mul_assoc]
  omega

/-- The entire flat branch has slack at least 9 before denominator scaling. -/
theorem flat_slack (d p a : Int) (hp : 2*p ≤ d) (ha : a ≤ d) :
    9*d ≤ 35*d - 14*a - 24*p := by omega

private theorem upper_slope (d p q : Int) (hd : 0 ≤ d) (hp : p ≤ d)
    (hcurve : q*q ≤ 4*p*(d-p)) :
    7*q ≤ 49*d - 48*p ∧ (7*q = 49*d - 48*p → 50*p = 49*d) := by
  have hscaled : (7*q)*(7*q) ≤ 196*p*(d-p) := calc
    _ = 49*(q*q) := by simp +arith [Int.mul_assoc, Int.mul_comm, Int.mul_left_comm]
    _ ≤ 49*(4*p*(d-p)) := Int.mul_le_mul_of_nonneg_left hcurve (by decide)
    _ = _ := by simp +arith [Int.mul_assoc, Int.mul_comm, Int.mul_left_comm]
  have hnonneg : 0 ≤ 49*d - 48*p := by omega
  have hgap := gap_identity d p
  have hsq := square_nonnegative (50*p - 49*d)
  constructor
  · by_cases h : 49*d - 48*p < 7*q
    · have hstrict := Int.mul_self_lt_mul_self hnonneg h
      omega
    · omega
  · intro h
    rw [h] at hscaled
    have hz : (50*p - 49*d) * (50*p - 49*d) = 0 := by omega
    rcases Int.mul_eq_zero.mp hz with hzero | hzero <;> omega

/-- Both branches, including p=0, p=d/2 and p=d. -/
theorem tangent_bound (d p a : Int) (hd : 0 < d) (hp : 0 ≤ p ∧ p ≤ d)
    (hbranch : (2*p ≤ d ∧ a ≤ d) ∨ 4*a ≤ 3*d ∨
      (4*a - 3*d) * (4*a - 3*d) ≤ 4*p*(d-p)) :
    14*a + 24*p ≤ 35*d ∧
      (14*a + 24*p = 35*d ↔ 50*p = 49*d ∧ 50*a = 41*d) := by
  rcases hbranch with hflat | hlow | hcurve
  · omega
  · omega
  · have h := upper_slope d p (4*a - 3*d) (by omega) hp.2 hcurve
    constructor
    · omega
    · constructor
      · intro heq
        have atContact := h.2 (by omega)
        omega
      · omega

/-- Choosing the science test with probability 7/19 and the revival test
with probability 12/19 gives a success ceiling of 35/38 on these branches. -/
theorem randomized_bound (d p a : Int) (h : 14*a + 24*p ≤ 35*d) :
    2 * (7*a + 12*p) ≤ 35*d := by omega

theorem contact_attains :
    (4*41 - 3*50 : Int) * (4*41 - 3*50) = 4*49*(50-49) ∧
    (14*41 + 24*49 : Int) = 35*50 := by decide

end SourceRevivalTangent
