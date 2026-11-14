import Std

namespace AddressedPositionScore

/-- Integer Hadamard rail numerators after the shift and addressed sign. -/
def rails : Nat → Int → Int × Int
  | 0, x => if x = 0 then (1, 0) else (0, 0)
  | t+1, x =>
    let a := rails t (x-1)
    let b := rails t (x+1)
    let flip := ((t+1 == 2) && (x == -2)) || ((t+1 == 7) && (x == 3)) ||
      ((t+1 == 8) && (x == 6))
    let s : Int := if flip then -1 else 1
    (s*(a.1+a.2), s*(b.1-b.2))

example : rails 10 (-2) = (2,0) ∧ rails 10 0 = (0,-6) ∧
    rails 10 4 = (-18,0) := by decide

/-- Multiply through by the positive normalizer and factor out 4^q.
    The real-power substitution u = 9^q and its monotonicity are in the text. -/
theorem numerator (u : Int) : 81 - 18*u + u*u = (u-9)*(u-9) := by
  simp only [Int.sub_mul, Int.mul_sub, Int.mul_comm u 9]
  omega

example : (81 : Int)*210 - 18*252 + 120 = 12594 := by decide

end AddressedPositionScore
