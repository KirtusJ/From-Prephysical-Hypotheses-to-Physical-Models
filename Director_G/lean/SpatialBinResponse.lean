import Std

/-! An event-specific response and its two preparation comparisons in
common integer units. Physical control of the aperture is a separate premise. -/

namespace SpatialBinResponse

/-- Sign variation, mixture defect and calibration defect bound the original
flight error. The doubled scale avoids assumptions on divisibility by two. -/
theorem eventError (f fSign target reference signError mixtureError calibrationError : Int)
    (s1 : f - fSign ≤ signError) (s2 : fSign - f ≤ signError)
    (m1 : f + fSign - 2 * reference ≤ 2 * mixtureError)
    (m2 : 2 * reference - (f + fSign) ≤ 2 * mixtureError)
    (c1 : reference - target ≤ calibrationError)
    (c2 : target - reference ≤ calibrationError) :
    2 * (f - target) ≤ signError + 2 * mixtureError + 2 * calibrationError ∧
    2 * (target - f) ≤ signError + 2 * mixtureError + 2 * calibrationError := by
  constructor <;> omega

end SpatialBinResponse
