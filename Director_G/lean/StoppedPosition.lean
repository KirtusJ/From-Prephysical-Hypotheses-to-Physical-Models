import Std

namespace StoppedPosition

/-- Integer numerator identity for one monitored digit. All probability
quantities z,d use the same scale, and z+d is twice the previous suffix.
The unobserved incident term uses that previous suffix as a reference value. -/
theorem oneDigit (stop cont unread z d : Int) :
    2 * (stop*d + cont*z) + unread*(z+d) - (stop+cont+unread)*(z+d)
      = (cont-stop)*(z-d) := by
  simp only [Int.add_mul, Int.mul_add, Int.sub_mul, Int.mul_sub]
  omega

/-- Unknown outcomes can each add at most one hit, including at a truncated horizon. -/
theorem completion (hits missing live fromMissing fromLive : Int)
    (hm : 0 ≤ fromMissing) (hm' : fromMissing ≤ missing)
    (hc : 0 ≤ fromLive) (hc' : fromLive ≤ live) :
    hits ≤ hits+fromMissing+fromLive ∧ hits+fromMissing+fromLive ≤ hits+missing+live := by
  omega

end StoppedPosition
