import Std

namespace CrossingImpulse

/-- Four displacement errors in units of a common positive secant width.
    The resulting numerator error is bounded by four endpoint errors. -/
theorem endpointError (a b c d e : Int)
    (aL : -e ≤ a) (aU : a ≤ e) (bL : -e ≤ b) (bU : b ≤ e)
    (cL : -e ≤ c) (cU : c ≤ e) (dL : -e ≤ d) (dU : d ≤ e) :
    -(4*e) ≤ (d-c)-(b-a) ∧ (d-c)-(b-a) ≤ 4*e := by omega

/-- In a quadratic flight the two secant numerators, divided by the common
    width and doubled, are 2v−3Fh and 2v+3Fh. On the ordered upper path
    the left interval is reflected when v is positive. -/
theorem crossingContrast (v fh : Int) :
    (2*v+3*fh)-(2*v-3*fh) = 6*fh ∧
    (2*v+3*fh)+(2*v-3*fh) = 4*v := by omega

end CrossingImpulse
