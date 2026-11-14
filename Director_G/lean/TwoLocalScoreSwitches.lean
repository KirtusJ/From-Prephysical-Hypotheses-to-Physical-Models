import Std

namespace TwoLocalScoreSwitches

/-- Four reciprocal spectator rates, cleared of the three positive
denominators. The middle normalizer is the midpoint of the two extremes. -/
theorem curvature (z d : Int) :
    (z+d)*(z+2*d) - 2*z*(z+2*d) + z*(z+d) = 2*(d*d) := by
  have twice (x : Int) : 2*x = x+x := by omega
  simp only [twice, Int.add_mul, Int.mul_add]
  rw [Int.mul_comm d z]
  omega

end TwoLocalScoreSwitches
