import Std

namespace ForwardMaskAudit

private theorem four (a : Int) : a*4 = a+a+a+a := by omega

/-- Numerator from four separately tagged signed rows of the six-tick return.
    Complex source coefficients use this identity on both real components. -/
theorem tagged_norm (a b : Int) :
    (a-b)*(a-b) + (b-a)*(b-a) + (a+b)*(a+b) + (-a-b)*(-a-b)
      = 4*(a*a+b*b) := by
  simp only [Int.mul_add, Int.add_mul, Int.mul_sub, Int.sub_mul, Int.mul_neg,
    Int.neg_mul, Int.neg_neg, Int.mul_assoc, Int.mul_comm, Int.mul_left_comm]
  simp only [four, Int.mul_add]
  omega

end ForwardMaskAudit
