import Mathlib

/-!
# (M k) + evenness ⟹ parallelogram law, for k = 1, 2, 3

Each case is an explicit combination of three instances of (M k):
`(k+1)·(M k)(a, b) − k·(M k)(a + b, b) + (M k)(a + k•b, −b)`.
-/

namespace FPHPM.MkSmall

variable {G : Type*} [AddCommGroup G]

/-- k = 1. -/
theorem parallelogram_of_M1 (f : G → ℝ)
    (h : ∀ a b : G, 1 * f (a - b) + f (a + 1 • b) = (1 + 1) * f a + 1 * (1 + 1) * f b)
    (heven : ∀ x, f (-x) = f x) :
    ∀ a b : G, f (a + b) + f (a - b) = 2 * f a + 2 * f b := by
  intro a b
  have E1 := h a b
  have E2 := h (a + b) b
  have E3 := h (a + 1 • b) (-b)
  have e1 : a + b - b = a := by abel
  have e2 : a + b + 1 • b = a + 1 • b + b := by abel
  have e3 : a + 1 • b - -b = a + 1 • b + b := by abel
  have e4 : a + 1 • b + 1 • (-b) = a := by abel
  have e5 : a + 1 • b = a + b := by abel
  rw [e1, e2] at E2
  rw [e3, e4, heven b] at E3
  rw [e5] at E1
  linarith

/-- k = 2. -/
theorem parallelogram_of_M2 (f : G → ℝ)
    (h : ∀ a b : G, 2 * f (a - b) + f (a + 2 • b) = (2 + 1) * f a + 2 * (2 + 1) * f b)
    (heven : ∀ x, f (-x) = f x) :
    ∀ a b : G, f (a + b) + f (a - b) = 2 * f a + 2 * f b := by
  intro a b
  have E1 := h a b
  have E2 := h (a + b) b
  have E3 := h (a + 2 • b) (-b)
  have e1 : a + b - b = a := by abel
  have e2 : a + b + 2 • b = a + 2 • b + b := by abel
  have e3 : a + 2 • b - -b = a + 2 • b + b := by abel
  have e4 : a + 2 • b + 2 • (-b) = a := by abel
  rw [e1, e2] at E2
  rw [e3, e4, heven b] at E3
  linarith

/-- k = 3 (the degree-five case). -/
theorem parallelogram_of_M3 (f : G → ℝ)
    (h : ∀ a b : G, 3 * f (a - b) + f (a + 3 • b) = (3 + 1) * f a + 3 * (3 + 1) * f b)
    (heven : ∀ x, f (-x) = f x) :
    ∀ a b : G, f (a + b) + f (a - b) = 2 * f a + 2 * f b := by
  intro a b
  have E1 := h a b
  have E2 := h (a + b) b
  have E3 := h (a + 3 • b) (-b)
  have e1 : a + b - b = a := by abel
  have e2 : a + b + 3 • b = a + 3 • b + b := by abel
  have e3 : a + 3 • b - -b = a + 3 • b + b := by abel
  have e4 : a + 3 • b + 3 • (-b) = a := by abel
  rw [e1, e2] at E2
  rw [e3, e4, heven b] at E3
  linarith

end FPHPM.MkSmall

#print axioms FPHPM.MkSmall.parallelogram_of_M1
#print axioms FPHPM.MkSmall.parallelogram_of_M2
#print axioms FPHPM.MkSmall.parallelogram_of_M3
