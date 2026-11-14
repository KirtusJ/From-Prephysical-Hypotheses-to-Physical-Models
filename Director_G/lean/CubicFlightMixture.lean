import Std

namespace CubicFlightMixture

/-- Original-launch rate bounds after multiplying all high and low contributions
by their nonnegative exposure weights. The caller must establish the inputs. -/
theorem measuredBracket (bare twirl reference target highCap lowCap em eq : Int)
    (queryLo : twirl - bare ≤ eq) (queryHi : bare - twirl ≤ eq)
    (mixLo : reference - twirl ≤ em) (mixHi : twirl - reference ≤ em)
    (refLo : lowCap ≤ reference) (refHi : reference ≤ highCap) :
    lowCap - target - em - eq ≤ bare - target ∧
    bare - target ≤ highCap - target + em + eq := by
  constructor <;> omega

/-- Eight copies of the query can be compared to seven high and one low. -/
example : 8 * (320 : Nat) = 7 * 365 + 5 := by decide

end CubicFlightMixture
