import Std

namespace UnsignedRailScore

/-- The swap follows each signed Hadamard and directional shift. The common
    amplitude denominator is suppressed. -/
def rails (swaps : List (Nat × Int)) : Nat → Int → Int × Int
  | 0, x => if x = 0 then (1, 0) else (0, 0)
  | t+1, x =>
    let a := rails swaps t (x-1)
    let b := rails swaps t (x+1)
    let r := a.1 + a.2
    let l := b.1 - b.2
    if swaps.contains (t+1, x) then (l, r) else (r, l)

example : let f := rails [(3,3)] 5
    f (-5) = (0,1) ∧ f (-1) = (0,-2) ∧ f 1 = (0,4) := by decide

example : let f := rails [(3,1), (4,4)] 6
    f (-2) = (1,0) ∧ f 0 = (0,-4) ∧ f 2 = (0,5) := by decide

example : let f := rails [(2,2), (3,-3)] 9
    f (-9) = (0,-1) ∧ f (-5) = (0,2) ∧ f (-3) = (0,-16) ∧
    f 3 = (0,2) := by decide

/-- Substituting t = 4^q gives the nine-tick numerator in the paper.
    This is the polynomial identity, valid over the integers. -/
theorem nine_numerator (t : Int) :
    t*t*t*t - 256*t + 768 = (t-4)*(t-4)*(t*t+8*t+48) := by
  simp [Int.add_mul, Int.mul_add, Int.sub_mul, Int.mul_sub, Int.mul_comm,
    Int.mul_left_comm, Int.mul_assoc]
  simp only [← Int.mul_assoc]
  omega

example : (768 : Int) - 512*36 + 84 + 256*84 = 3924 := by decide

end UnsignedRailScore
