import Std

namespace TwoColumnTransport

/-- One entry of the Gram of U-Z with both Grams H and both cross-Grams H-d.
    d is zero off the diagonal and the common power of two on it. -/
theorem gram_of_normal_entry (h d : Int) :
    h - (h-d) - (h-d) + h = 2*d := by omega

/-- After multiplying by the common denominator d, each of the two paired
    reflection terms removes exactly its own displacement coordinate. -/
theorem two_reflections_coordinate (d x z other : Int) :
    d*x - (x-z)*d - other*0 = d*z := by
  rw [Int.sub_mul, Int.mul_comm x d, Int.mul_comm z d]
  simp only [Int.mul_zero, Int.sub_zero]
  omega

/-- Each element of the ideal (m) stays in it under an integer left shear.
    This is the numerator-level arithmetic used in the directional obstruction. -/
theorem relation_preserved (a b c d k m p q : Int)
    (rowOne : b = k*a + m*p) (rowTwo : d = k*c + m*q) (u v : Int) :
    u*b + v*d = k*(u*a+v*c) + m*(u*p+v*q) := by
  subst b
  subst d
  simp only [Int.mul_add, Int.add_mul]
  simp only [← Int.mul_assoc]
  rw [Int.mul_comm u k, Int.mul_comm v k, Int.mul_comm u m, Int.mul_comm v m]
  omega

end TwoColumnTransport
