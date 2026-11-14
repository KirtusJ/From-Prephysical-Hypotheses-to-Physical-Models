import Std

namespace UnequalLocalSwitches

/-- The four spectator probabilities after clearing positive denominators
and omitting their common spectator numerator. -/
theorem mixedDifference (z a b : Int) :
    (z+a)*(z+b)*(z+a+b) - z*(z+b)*(z+a+b) -
    z*(z+a)*(z+a+b) + z*(z+a)*(z+b) = a*b*(z+z+a+b) := by
  simp only [Int.add_mul, Int.mul_add, Int.mul_assoc, Int.mul_comm, Int.mul_left_comm]
  omega

end UnequalLocalSwitches
