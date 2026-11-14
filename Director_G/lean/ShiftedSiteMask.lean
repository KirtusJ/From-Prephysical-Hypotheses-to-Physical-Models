import Std

namespace ShiftedSiteMask

/-- Given two successor errors, the mass of the arc-selected sites is the
    programmed width plus their difference, including coincident endpoints. -/
theorem successor_discrepancy
    (origin width nextBefore nextAfter limit : Int)
    (a : 0 ≤ nextBefore - origin) (b : nextBefore - origin ≤ limit)
    (c : 0 ≤ nextAfter - (origin + width))
    (d : nextAfter - (origin + width) ≤ limit) :
    -limit ≤ nextAfter - nextBefore - width ∧
      nextAfter - nextBefore - width ≤ limit := by omega

/-- On the seed subgrid with stride s, a membership window of k strides
    contains precisely k eligible origins. This handles either circle seam
    by using lifted integer coordinates, including negative residues. -/
theorem eligible_grid_origins (a k s : Int) (hs : 0 < s) :
    a / s - (a - k*s) / s = k := by
  have h := Int.add_mul_ediv_left a (-k) (show s ≠ 0 by omega)
  have h' : a + (-k)*s = a - k*s := by
    rw [Int.neg_mul, Int.sub_eq_add_neg]
  rw [Int.mul_comm s (-k), h'] at h
  omega

/-- The plotted scalar can differ from the programmed value by an additional
    profile tolerance, when the actual event mass is uniformly controlled. -/
theorem mismatch
    (actual programmed width instrumentError profileError : Int)
    (a : -instrumentError ≤ programmed - width)
    (b : programmed - width ≤ instrumentError)
    (c : -profileError ≤ actual - programmed)
    (d : actual - programmed ≤ profileError) :
    -(instrumentError + profileError) ≤ actual - width ∧
      actual - width ≤ instrumentError + profileError := by omega

/-- A monotone bracketing experiment inherits the observed rate error and
    the two programmed distances, here in a common integer rate unit. -/
theorem recorded_bracket (x g lower upper readLow readHigh error spacing : Int)
    (a : readLow ≤ g) (b : g ≤ readHigh)
    (c : lower - error ≤ readLow) (d : readHigh ≤ upper + error)
    (e : x - lower ≤ spacing) (f : upper - x ≤ spacing) :
    x - (spacing + error) ≤ g ∧ g ≤ x + (spacing + error) := by omega

end ShiftedSiteMask
