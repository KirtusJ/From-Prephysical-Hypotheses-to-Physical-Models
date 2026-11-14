import Mathlib

/-- The statement `∀ x : ℝ, x ≤ x ^ 2` is false; witness `x = 1/2`. -/
theorem control_witness : ¬ ((1 / 2 : ℝ) ≤ (1 / 2 : ℝ) ^ 2) := by norm_num

theorem control_refuted : ¬ ∀ x : ℝ, x ≤ x ^ 2 := fun h => control_witness (h (1 / 2))

#print axioms control_witness
#print axioms control_refuted
