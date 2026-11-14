import Std

namespace LabelRateContrast

/-- After multiplying by the two positive denominators, the witness
at all integer exponents has the sign of the product of these factors. -/
theorem commonDenominator (monitor big small : Int) :
    (monitor * big - monitor * small) - 3 * (big - small) =
    (monitor - 3) * (big - small) := by
  simp only [Int.sub_mul, Int.mul_sub]
  omega

example : ((9 : Int) - 3) * (26 - 18) * 39 = 4 * 18 * 26 := by decide

end LabelRateContrast
