import Std

namespace StoredWordParity

/-- Number of binary masks giving an odd dot product with this difference
word. For a zero head both mask-head choices have the same effect. For a
one head exactly one of the two choices works for each remaining mask. -/
def oddMasks : List Bool → Nat
  | [] => 0
  | false :: xs => 2 * oddMasks xs
  | true :: xs => 2 ^ xs.length

theorem oddMasks_zero (xs : List Bool) (h : true ∉ xs) : oddMasks xs = 0 := by
  induction xs with
  | nil => rfl
  | cons x xs ih =>
    cases x with
    | false =>
      have tail : true ∉ xs := by simpa using h
      simp [oddMasks, ih tail]
    | true => simp at h

theorem oddMasks_half (xs : List Bool) (h : true ∈ xs) :
    2 * oddMasks xs = 2 ^ xs.length := by
  induction xs with
  | nil => simp at h
  | cons x xs ih =>
    cases x with
    | false =>
      have tail : true ∈ xs := by simpa using h
      simp only [oddMasks, List.length_cons, Nat.pow_succ]
      rw [ih tail]
      omega
    | true =>
      simp [oddMasks, Nat.pow_succ, Nat.mul_comm]

end StoredWordParity
