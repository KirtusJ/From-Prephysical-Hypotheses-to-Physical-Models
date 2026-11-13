import Mathlib

/-! Algebraic steps for the block law.
1. A bounded function with f (g x) = c * f x and |c| > 1 vanishes.
2. Same with 0 < |c| < 1 when g is surjective.
3. For U with Uᵀ U = 1 (square): Uᵀ D U = D iff D U = U D.
-/

theorem bounded_scaling_zero {X : Type*} (f : X → ℝ) (g : X → X) (c M : ℝ)
    (hc : 1 < |c|) (hb : ∀ x, |f x| ≤ M) (h : ∀ x, f (g x) = c * f x) :
    ∀ x, f x = 0 := by
  intro x
  by_contra hx
  have key : ∀ m : ℕ, |f (g^[m] x)| = |c| ^ m * |f x| := by
    intro m
    induction m with
    | zero => simp
    | succ m ih =>
      rw [Function.iterate_succ_apply', h, abs_mul, ih, pow_succ]; ring
  have hpos : 0 < |f x| := abs_pos.mpr hx
  obtain ⟨m, hm⟩ := pow_unbounded_of_one_lt (M / |f x|) hc
  have h1 : M < |c| ^ m * |f x| := (div_lt_iff hpos).mp hm
  have h2 := hb (g^[m] x)
  rw [key m] at h2
  linarith

theorem bounded_scaling_zero' {X : Type*} (f : X → ℝ) (g : X → X) (c M : ℝ)
    (hc0 : c ≠ 0) (hc : |c| < 1) (hg : Function.Surjective g)
    (hb : ∀ x, |f x| ≤ M) (h : ∀ x, f (g x) = c * f x) :
    ∀ x, f x = 0 := by
  apply bounded_scaling_zero f (Function.surjInv hg) c⁻¹ M _ hb
  · intro x
    have := h (Function.surjInv hg x)
    rw [Function.surjInv_eq hg x] at this
    rw [this, ← mul_assoc, inv_mul_cancel₀ hc0, one_mul]
  · rw [abs_inv]
    exact one_lt_inv (abs_pos.mpr hc0) hc

open Matrix in
theorem conj_fixed_iff_commute {n : Type*} [Fintype n] [DecidableEq n] {K : Type*} [CommRing K]
    (U D : Matrix n n K) (hU : Uᵀ * U = 1) :
    Uᵀ * D * U = D ↔ D * U = U * D := by
  have hU' : U * Uᵀ = 1 := mul_eq_one_comm.mp hU
  constructor
  · intro h
    have : U * (Uᵀ * D * U) = U * D := by rw [h]
    rw [← Matrix.mul_assoc, ← Matrix.mul_assoc, hU', Matrix.one_mul] at this
    exact this
  · intro h
    rw [Matrix.mul_assoc, h, ← Matrix.mul_assoc, hU, Matrix.one_mul]

#print axioms bounded_scaling_zero
#print axioms bounded_scaling_zero'
#print axioms conj_fixed_iff_commute
