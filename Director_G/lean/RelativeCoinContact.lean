import Std

namespace RelativeCoinContact

/-- Real input populations a,b,c,d in RR,RL,LR,LL order. u and v are the
    real parts of (RR,LL) and (RL,LR) coherences. Rates have a common full
    unit a+b+c+d, so rational density matrices are covered by scaling. -/
theorem nearAgreement (a b c d u v full : Int) (traceOne : a+b+c+d = full) :
    4*a + 4*b + 4*c + 4*d + 2*u - 2*v = 4*full - (-2*u+2*v) := by
  omega

/-- If a column is transformed by the coordinate phase minus on RL, its
    X-tensor-X expectation changes into minus its Y-tensor-Y expectation.
    These are polynomial identities for all real (and rational-scaled)
    components, applied separately to real and imaginary parts. -/
theorem oneContact (rr rl lr ll : Int) :
    2*(rr*ll + (-rl)*lr) = -(2*(rl*lr - rr*ll)) := by
  simp only [Int.neg_mul]
  omega

/-- The event indicator is the maximal binary distinguisher when each cell
    with a positive probability difference is selected and the negative
    ones are omitted. Here the four affected cells have equal absolute mass. -/
theorem fourCellBound (p q r s : Int) (hp : 0 ≤ p ∧ p ≤ 1)
    (hq : 0 ≤ q ∧ q ≤ 1) (hr : 0 ≤ r ∧ r ≤ 1) (hs : 0 ≤ s ∧ s ≤ 1) :
    -2 ≤ p + q - r - s ∧ p + q - r - s ≤ 2 := by
  omega

end RelativeCoinContact
