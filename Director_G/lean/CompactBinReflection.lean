import Std

namespace CompactBinReflection

/-- Integer form of the hyperplane correction after clearing denominators.
    The scalar product of the provisional point is dot; the repair vector has
    scalar product one. -/
theorem correct_dot (dot goal : Int) : dot+(goal-dot)*1=goal := by omega

/-- Each coordinate of the unnormalized first Householder action, after
    clearing its common nonzero denominator d, once dot(x,x-z)=d. -/
theorem hit_coordinate (d x z : Int) : d*x-(x-z)*d=d*z := by
  rw [Int.sub_mul, Int.mul_comm x d, Int.mul_comm z d]
  omega

/-- With equal squared norms P and common scalar product b, the displacement
    has the squared length 2*(P-b) required by the reflection. -/
theorem normal_length (p b : Int) : p+p-2*b=2*(p-b) := by omega

/-- The sum of a Gaussian factor and its conjugate is the scalar 2a.
    The same identity holds componentwise for a quaternion multiple. -/
theorem conjugate_sum (u v a h : Int) :
    (u*a+v*h)+(u*a-v*h)=2*(u*a) := by omega

end CompactBinReflection
