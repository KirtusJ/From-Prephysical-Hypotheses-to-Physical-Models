import Std

namespace PairedCurveCalibration

/-- After rounding y up by at most h, monotonicity preserves this much
    of a positive excursion g(s)-s=d. All coordinates share one scale. -/
theorem rounded_positive (s y j h d gj : Int)
    (close : j ≤ y + h) (ordered : s + d ≤ gj) :
    d-h-(y-s) ≤ gj-j := by omega

/-- The corresponding bound for a negative excursion and rounding down. -/
theorem rounded_negative (s y j h d gj : Int)
    (close : y-h ≤ j) (ordered : gj ≤ s-d) :
    d-h-(s-y) ≤ j-gj := by omega

/-- If coordinates s and p have common denominator d, expand the
    signed pair score using marginal probabilities p/d and joint
    success count j/d². The four-cell expectation has denominator d⁴. -/
theorem pair_table (d p s j : Int) :
    (d*d-p*d-p*d+j)*(s*s) - (p*d-j)*(s*(d-s)) - (p*d-j)*(s*(d-s)) + j*((d-s)*(d-s))
        = d*d*((p-s)*(p-s) + (j-p*p)) := by
  simp only [Int.sub_mul, Int.add_mul, Int.mul_sub, Int.mul_add,
    Int.mul_assoc, Int.mul_left_comm, Int.mul_comm]
  omega

end PairedCurveCalibration
