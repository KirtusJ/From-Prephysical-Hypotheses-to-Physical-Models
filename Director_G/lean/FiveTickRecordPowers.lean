import Std

namespace FiveTickRecordPowers

/-- Given a positive denominator and equality to 5/8 by cross multiplication,
    each proposed response implies the unpowered base weight. Monotonicity of
    the real power function then gives q=1 in the mathematical argument. -/
theorem globalRoot (u : Int) : 8*(1+u) = 5*(7+u) ↔ u = 9 := by omega
theorem siteRoot (u : Int) : 8*u = 5*(3+u) ↔ u = 5 := by omega
theorem railRoot (u : Int) : 8*(1+u) = 5*(4+u) ↔ u = 4 := by omega

/-- In common mass units, r1,r2 have target 5/8 when 8*r_i=5*unit.
    Their centered product gives the two-block discrepancy after scaling. -/
theorem centeredProduct (r1 r2 unit : Int) :
    (8*r1-5*unit)*(8*r2-5*unit) =
    (8*r1)*(8*r2) - (8*r1)*(5*unit) - (5*unit)*(8*r2) + (5*unit)*(5*unit) := by
  simp only [Int.sub_mul, Int.mul_sub]
  omega

/-- Polynomial numerator of (4-u^2) times the S-word marginal change.
    Positivity of the denominators and real-power monotonicity are supplied
    in the paper. This identity checks the old-word arithmetic on rationals
    after polynomial expansion. -/
theorem oldWordNumerator (u : Int) :
    (4-u*u)*(2*(4+2*u+2*u*u)-(8+6*u*u)) =
    2*u*(2-u)*(2-u)*(2+u) := by
  have outer : 4-u*u = (2-u)*(2+u) := by
    simp only [Int.sub_mul, Int.mul_add, Int.mul_comm u 2]
    omega
  have inner : 2*(4+2*u+2*u*u)-(8+6*u*u) = 2*u*(2-u) := by
    simp only [Int.mul_add, Int.mul_sub, Int.mul_assoc, Int.mul_comm u 2]
    omega
  rw [outer, inner]
  ac_rfl

end FiveTickRecordPowers
