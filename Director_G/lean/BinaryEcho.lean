import Std

namespace BinaryEcho

/- An integer pair (a,b) represents a+b*z, with z²=z-1. Let d>0 be
   the mass denominator, and n/d the initial blank squared mass. -/
def phaseMul (x y : Int × Int) : Int × Int :=
  (x.1*y.1 - x.2*y.2, x.1*y.2 + x.2*y.1 + x.2*y.2)

/-- After clearing d, the blank amplitude is multiplied by
    d + (z-1)(n+z(d-n)) = z*n. -/
theorem blank_factor (d n : Int) :
    (d + (phaseMul (-1, 1) (n, d-n)).1, (phaseMul (-1, 1) (n, d-n)).2) =
      (0, n) := by
  apply Prod.ext <;> simp [phaseMul] <;> omega

/-- With a common integer probability denominator d, the two routing
    assignments together collect at least d nonblank records in expectation
    per 2d original blocks whenever the physical response is ordered. -/
theorem fair_routing (low high d : Nat) (ordered : low ≤ high) (within : high ≤ d) :
    d ≤ high + (d-low) := by omega

theorem equal_responses_attain_half (v d : Nat) (h : v ≤ d) :
    v + (d-v) = d := by omega

/-- If each high-leakage case contributes at least one half, its mass
    is bounded by twice the total recorded nonblank probability. -/
theorem high_tail (high brightHigh brightOther : Nat)
    (h : high ≤ 2 * brightHigh) : high ≤ 2 * (brightHigh + brightOther) := by omega

/-- Exact cleared denominators for depth five, rate 1/200:
    (299/300)^243 < 1/2 and 1/300+(299/300)(2/200) < 1/75. -/
theorem depth_five_example :
    3^5 = (243 : Nat) ∧ 2 * (299 : Nat)^243 < 300^243 ∧
    75 * (100+299) < (300 : Nat) * 100 := by decide

end BinaryEcho
