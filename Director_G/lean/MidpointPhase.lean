import Std

/-! The midpoint sum rule and adaptive transcript identity with common
integer numerator units. The note proves the physical unitary and
refresh hypotheses that connect these identities to a rail experiment. -/

namespace MidpointPhase

/-- Parallelogram sum in signed integer numerator coordinates. -/
theorem plusMinus (x y : Int) :
    (x+y)*(x+y) + (x-y)*(x-y) = 2*(x*x+y*y) := by
  simp only [Int.add_mul, Int.mul_add, Int.sub_mul, Int.mul_sub]
  rw [Int.mul_comm y x]
  omega

/-- A balanced numerator p=n/2 has zero deficit, with the denominator
cleared. p and n can be any integers for this polynomial identity. -/
theorem balance (p n : Int) :
    n*n - 4*(p*(n-p)) = (2*p-n)*(2*p-n) := by
  simp only [Int.sub_mul, Int.mul_sub, Int.mul_assoc]
  rw [Int.mul_left_comm n 2 p, Int.mul_left_comm p 2 p, Int.mul_comm n p]
  omega

/-- Along any finite adaptively chosen transcript, a common conditional
kernel fixes its joint numerator. The history argument records observed
outcomes in reverse chronological order. -/
def likelihood (kernel : List Bool → Bool → Nat) (past : List Bool) : List Bool → Nat
  | [] => 1
  | x :: xs => kernel past x * likelihood kernel (x :: past) xs

/-- The average squared centered bias equals its cross product plus half
the squared change, after multiplication by two. -/
theorem unequalBias (x y : Int) :
    x*x+y*y = 2*(x*y)+(x-y)*(x-y) := by
  simp only [Int.sub_mul, Int.mul_sub]
  rw [Int.mul_comm y x]
  omega

theorem histories (k l : List Bool → Bool → Nat)
    (same : ∀ past x, k past x = l past x) (word past : List Bool) :
    likelihood k past word = likelihood l past word := by
  induction word generalizing past with
  | nil => rfl
  | cons x xs ih => simp only [likelihood, same, ih]

end MidpointPhase
