import Std

namespace MirroredSiteMask

/-- Quadratic form of a real site effect before its common normalization. -/
def score (a b c u v : Int) : Int := a*u*u + 2*b*u*v + c*v*v

theorem mirrored_pair (a b c u v : Int) :
    score a b c u v + score c (-b) a u v = (a+c)*(u*u+v*v) := by
  simp only [score, Int.mul_add, Int.add_mul, Int.mul_neg, Int.neg_mul,
    Int.mul_assoc, Int.mul_comm, Int.mul_left_comm]
  omega

end MirroredSiteMask
