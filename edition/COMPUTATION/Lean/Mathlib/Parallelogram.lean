import Mathlib

namespace FPHPM.Parallelogram

variable {G : Type*} [AddCommGroup G]

/-- The polar form attached to `f`. -/
noncomputable def B (f : G → ℝ) (x y : G) : ℝ := (f (x + y) - f (x - y)) / 4

section
variable {f : G → ℝ} (hf : ∀ x y, f (x + y) + f (x - y) = 2 * f x + 2 * f y)
include hf

theorem f_zero : f 0 = 0 := by
  have h := hf 0 0
  rw [add_zero, sub_zero] at h
  linarith

theorem f_neg (y : G) : f (-y) = f y := by
  have h := hf 0 y
  rw [zero_add, zero_sub, f_zero hf] at h
  linarith

theorem f_add_self (x : G) : f (x + x) = 4 * f x := by
  have h := hf x x
  rw [sub_self, f_zero hf] at h
  linarith

theorem f_two_nsmul (x : G) : f (2 • x) = 4 * f x := by
  rw [two_nsmul]; exact f_add_self hf x

theorem B_symm (x y : G) : B f x y = B f y x := by
  unfold B
  have h : f (y - x) = f (x - y) := by rw [← neg_sub, f_neg hf]
  rw [add_comm y x, h]

theorem B_self (x : G) : B f x x = f x := by
  unfold B
  rw [sub_self, f_zero hf, f_add_self hf]
  ring

theorem B_zero_left (y : G) : B f 0 y = 0 := by
  unfold B
  rw [zero_add, zero_sub, f_neg hf]
  ring

theorem B_add_sub (x z y : G) : B f (x + z) y + B f (x - z) y = 2 * B f x y := by
  unfold B
  have h1 := hf (x + y) z
  have h2 := hf (x - y) z
  have e1 : x + z + y = x + y + z := by abel
  have e2 : x + z - y = x - y + z := by abel
  have e3 : x - z + y = x + y - z := by abel
  have e4 : x - z - y = x - y - z := by abel
  rw [e1, e2, e3, e4]
  linarith

theorem B_add_self_left (x y : G) : B f (x + x) y = 2 * B f x y := by
  have h := B_add_sub hf x x y
  rw [sub_self, B_zero_left hf] at h
  linarith

theorem B_add_left (u v y : G) : B f (u + v) y = B f u y + B f v y := by
  have h := B_add_sub hf (u + v) (u - v) y
  have e1 : u + v + (u - v) = u + u := by abel
  have e2 : u + v - (u - v) = v + v := by abel
  rw [e1, e2, B_add_self_left hf, B_add_self_left hf] at h
  linarith

theorem B_zsmul_left (n : ℤ) (x y : G) : B f (n • x) y = n * B f x y := by
  let φ : G →+ ℝ := AddMonoidHom.mk' (fun x => B f x y) (fun u v => B_add_left hf u v y)
  have h := map_zsmul φ n x
  simpa [φ, zsmul_eq_mul] using h

theorem B_add_right (x u v : G) : B f x (u + v) = B f x u + B f x v := by
  rw [B_symm hf x (u + v), B_add_left hf, B_symm hf u x, B_symm hf v x]

theorem B_zsmul_right (n : ℤ) (x y : G) : B f x (n • y) = n * B f x y := by
  rw [B_symm hf x (n • y), B_zsmul_left hf, B_symm hf y x]

/-- Main theorem: all the listed properties of `f` and its polar form `B`. -/
theorem parallelogram_main :
    f 0 = 0 ∧ (∀ y, f (-y) = f y) ∧ (∀ x, f (2 • x) = 4 * f x) ∧
    (∀ x y, B f x y = B f y x) ∧ (∀ x, B f x x = f x) ∧
    (∀ u v y, B f (u + v) y = B f u y + B f v y) ∧
    (∀ (n : ℤ) x y, B f (n • x) y = n * B f x y) :=
  ⟨f_zero hf, f_neg hf, f_two_nsmul hf, B_symm hf, B_self hf, B_add_left hf, B_zsmul_left hf⟩

end

end FPHPM.Parallelogram

#print axioms FPHPM.Parallelogram.parallelogram_main
