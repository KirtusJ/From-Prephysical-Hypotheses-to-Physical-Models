import Mathlib

namespace FPHPM.FourLaw

/-- The "four law" is the parallelogram law multiplied by two. -/
theorem parallelogram {G : Type*} [AddCommGroup G] {f : G → ℝ}
    (hf : ∀ a b, 2 * f (a + b) + 2 * f (a - b) = 4 * f a + 4 * f b) :
    ∀ a b, f (a + b) + f (a - b) = 2 * f a + 2 * f b := by
  intro a b
  have h := hf a b
  linarith

/-- The line recursion forces a quadratic. -/
theorem line_recursion (φ : ℕ → ℝ) (h0 : φ 0 = 0)
    (h : ∀ a, 1 ≤ a → φ (a + 1) + φ (a - 1) = 2 * φ a + 2 * φ 1) :
    ∀ n : ℕ, φ n = (n : ℝ) ^ 2 * φ 1 := by
  have key : ∀ n : ℕ, φ n = (n : ℝ) ^ 2 * φ 1 ∧ φ (n + 1) = ((n + 1 : ℕ) : ℝ) ^ 2 * φ 1 := by
    intro n
    induction n with
    | zero => constructor <;> simp [h0]
    | succ n ih =>
      refine ⟨ih.2, ?_⟩
      have h1 := h (n + 1) (Nat.le_add_left 1 n)
      rw [Nat.add_sub_cancel, ih.1, ih.2] at h1
      push_cast at h1 ⊢
      linarith
  exact fun n => (key n).1

/-- Main theorem: both statements together. -/
theorem fourLaw_main :
    (∀ (G : Type) [AddCommGroup G] (f : G → ℝ),
      (∀ a b, 2 * f (a + b) + 2 * f (a - b) = 4 * f a + 4 * f b) →
      ∀ a b, f (a + b) + f (a - b) = 2 * f a + 2 * f b) ∧
    (∀ φ : ℕ → ℝ, φ 0 = 0 →
      (∀ a, 1 ≤ a → φ (a + 1) + φ (a - 1) = 2 * φ a + 2 * φ 1) →
      ∀ n : ℕ, φ n = (n : ℝ) ^ 2 * φ 1) :=
  ⟨fun _ _ _ hf => parallelogram hf, line_recursion⟩

end FPHPM.FourLaw

#print axioms FPHPM.FourLaw.fourLaw_main
