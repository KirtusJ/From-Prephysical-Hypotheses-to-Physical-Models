import Mathlib

namespace FPHPM.ThreeLaw

variable {G : Type*} [AddCommGroup G]

section
variable {f : G → ℝ} (hf : ∀ a b, f (a + 2 • b) + 2 * f (a - b) = 3 * f a + 6 * f b)
include hf

theorem f_zero : f 0 = 0 := by
  have h := hf 0 0
  rw [smul_zero, add_zero, sub_zero] at h
  linarith

theorem f_neg (b : G) : f (-b) = f b := by
  have h1 := hf 0 b
  have h2 := hf b (-b)
  rw [zero_add, zero_sub, f_zero hf] at h1
  have e1 : b + 2 • (-b) = -b := by abel
  have e2 : b - -b = 2 • b := by abel
  rw [e1, e2] at h2
  linarith

theorem parallelogram (a b : G) : f (a + b) + f (a - b) = 2 * f a + 2 * f b := by
  have h1 := hf a b
  have h2 := hf (a + b) (-b)
  have e1 : a + b + 2 • (-b) = a - b := by abel
  have e2 : a + b - -b = a + 2 • b := by abel
  rw [e1, e2, f_neg hf] at h2
  linarith

/-- Main theorem. -/
theorem threeLaw_main :
    f 0 = 0 ∧ (∀ b, f (-b) = f b) ∧
    (∀ a b, f (a + b) + f (a - b) = 2 * f a + 2 * f b) :=
  ⟨f_zero hf, f_neg hf, parallelogram hf⟩

end

end FPHPM.ThreeLaw

#print axioms FPHPM.ThreeLaw.threeLaw_main
