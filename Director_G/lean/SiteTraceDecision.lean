import Std

namespace SiteTraceDecision

/-- For the sharp-launch Hadamard walk, the integer arrival matrix has rows
    (d+p,p) and (q,d-q), after removing the common 2^(-t/2) factor.
    This is the signed site weight for the X+Z rail axis. -/
def contrast (d p q : Int) : Int :=
  (d+p)*(d+p) + q*q - p*p - (d-q)*(d-q) + 2*((d+p)*p + q*(d-q))

theorem factor (d p q : Int) :
    contrast d p q = 2*(p+q)*(2*d+p-q) := by
  simp only [contrast, show (2 : Int) = 1+1 by decide, Int.mul_add, Int.add_mul,
    Int.mul_one, Int.one_mul, Int.mul_sub, Int.sub_mul,
    Int.mul_assoc, Int.mul_left_comm, Int.mul_comm]
  omega

/-- Close the finite-site decision identity using the trace-current identity
    proved by cyclic rotation of closed rail words in the accompanying text. -/
theorem site (t x d p q : Int)
    (current : t*(p+q) = x*(2*d+p-q)) :
    t*contrast d p q = 2*x*(2*d+p-q)*(2*d+p-q) := by
  rw [factor]
  calc
    _ = 2*(t*(p+q))*(2*d+p-q) := by ac_rfl
    _ = _ := by rw [current]; ac_rfl

end SiteTraceDecision
