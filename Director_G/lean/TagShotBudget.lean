import Std

/- A raw launch records true at (7,R,1), false at (5,L,1), and none elsewhere.
   The stopping rule uses the first n named hits. -/
namespace TagShotBudget

abbrev Launch := Option Bool

def hits (raw : List Launch) : List Bool := raw.filterMap id

def rejects (n k : Nat) (raw : List Launch) : Prop :=
  n ≤ (hits raw).length ∧ ((hits raw).take n).count true ≤ k

/-- A timeout is a non-rejection, including a log with no named hits. -/
theorem timeout {raw : List Launch} {n k : Nat} (h : (hits raw).length < n) :
    ¬rejects n k raw := fun rejected => (Nat.not_le_of_lt h) rejected.1

/-- Any rejection by the deadline is also a rejection on every continuation.
    This event inclusion needs no assumption on the signs or their arrival rates. -/
theorem reject_extension {raw : List Launch} {n k : Nat} (rest : List Launch)
    (h : rejects n k raw) : rejects n k (raw ++ rest) := by
  obtain ⟨enough, cutoff⟩ := h
  have append_hits : hits (raw ++ rest) = hits raw ++ hits rest := by
    simp [hits]
  unfold rejects
  rw [append_hits, List.length_append, List.take_append_of_le_length enough]
  exact ⟨by omega, cutoff⟩

theorem capped_implies_full {raw : List Launch} {n k : Nat} (budget : Nat)
    (h : rejects n k (raw.take budget)) : rejects n k raw := by
  simpa using reject_extension (raw.drop budget) h

end TagShotBudget
