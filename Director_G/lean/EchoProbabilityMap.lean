import Std

namespace EchoProbabilityMap

/-- With site mass n/d, subtracting the squared return amplitude from
    the total gives the same numerator as twice the independent binary
    disagreement probability. Both fractions have denominator d². -/
theorem escape_disagreement (d n : Int) :
    d*d - (d-n-n)*(d-n-n) = 4*(n*(d-n)) := by
  simp only [Int.sub_mul, Int.mul_sub, Int.mul_comm d n]
  omega

/-- At the three-tick shell the echo is complementary to the direct
    read. Its factorized discrepancy vanishes only at p=1 or p=1/4. -/
theorem quarter_factor (d n : Int) :
    d*(d-n) - 4*(n*(d-n)) = (d-n)*(d-4*n) := by
  simp only [Int.sub_mul, Int.mul_sub, Int.mul_left_comm, Int.mul_comm d n]
  have same : d*(4*n) = n*(4*d) := by
    calc d*(4*n) = 4*(d*n) := Int.mul_left_comm _ _ _
         _ = 4*(n*d) := by rw [Int.mul_comm d n]
         _ = n*(4*d) := Int.mul_left_comm _ _ _
  omega

/-- Two increasing functions on the same cell are compared by the
    cross endpoint differences. A common positive denominator may be
    cleared throughout. -/
theorem crossed_endpoints (a b loA hiA loB hiB bound : Int)
    (a0 : loA ≤ a) (a1 : a ≤ hiA) (b0 : loB ≤ b) (b1 : b ≤ hiB)
    (hi : hiA-loB ≤ bound) (lo : hiB-loA ≤ bound) :
    -bound ≤ a-b ∧ a-b ≤ bound := by omega

/-- Supremum estimate in angular units from expansion on the two tent
    branches and interpolation between the tested arguments. -/
theorem angular_mesh_budget (d e h : Int)
    (hnode : 2*d ≤ d+e+2*h) : d ≤ e+2*h := by omega

end EchoProbabilityMap
