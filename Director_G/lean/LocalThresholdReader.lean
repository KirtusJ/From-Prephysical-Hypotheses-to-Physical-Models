import Std

namespace LocalThresholdReader

/-- A matching can enlarge a single site's cone to at most two sites on
    its first layer, and a later interval by at most two more. -/
theorem cone_after_first (width : Nat → Nat) (first : width 0 ≤ 2)
    (step : ∀ t, width (t+1) ≤ width t + 2) (t : Nat) :
    width t ≤ 2*(t+1) := by
  induction t with
  | zero => omega
  | succ i ih => have h := step i; omega

/-- Every input bit is essential to the jth threshold: the other bits can
    contain exactly j-1 hits when 1 ≤ j ≤ m. -/
theorem pivotal (m j : Nat) (positive : 0<j) (within : j ≤ m) :
    j-1 ≤ m-1 ∧ j-1 < j ∧ j ≤ (j-1)+1 := by omega

/-- If a protected, reversible read of a one adds at least one dimension
    to the span of nonzero-prefix states each time, that span and the
    orthogonal zero-prefix ray require m+1 dimensions at the end. -/
theorem head_dimension (rank : Nat → Nat) (grow : ∀ i, rank i + 1 ≤ rank (i+1))
    (m width : Nat) (room : rank m + 1 ≤ width) : m+1 ≤ width := by
  have lower (t : Nat) : t ≤ rank t := by
    induction t with
    | zero => omega
    | succ i ih => have h := grow i; omega
  have h := lower m
  omega

end LocalThresholdReader
