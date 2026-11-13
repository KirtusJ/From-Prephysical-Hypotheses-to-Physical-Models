import Mathlib

open Finset

theorem sum_roots_of_unity_eq_zero (k : ℕ) (hk : 2 ≤ k) :
    ∑ j in Finset.range k, Complex.exp (2 * Real.pi * Complex.I * j / k) = 0 := by
  have h := (Complex.isPrimitiveRoot_exp k (by omega)).geom_sum_eq_zero (by omega)
  rw [← h]
  apply Finset.sum_congr rfl
  intro j _
  rw [← Complex.exp_nat_mul]
  congr 1
  ring

theorem c0_eq_zero_of_forall_roots (k : ℕ) (hk : 2 ≤ k) (c0 : ℝ) (c ω : ℂ)
    (h : ∀ η : ℂ, η ^ k = 1 → (c0 : ℝ) = (c * ω * η).re) : c0 = 0 := by
  have hζ := Complex.isPrimitiveRoot_exp k (by omega)
  have hsum := hζ.geom_sum_eq_zero (by omega)
  have h1 : ∑ _j in Finset.range k, c0
      = ∑ j in Finset.range k, (c * ω * Complex.exp (2 * Real.pi * Complex.I / k) ^ j).re := by
    apply Finset.sum_congr rfl
    intro j _
    apply h
    rw [← pow_mul, mul_comm j k, pow_mul, hζ.pow_eq_one, one_pow]
  rw [← Complex.re_sum, ← Finset.mul_sum, hsum, mul_zero, Complex.zero_re,
    Finset.sum_const, Finset.card_range, nsmul_eq_mul] at h1
  rcases mul_eq_zero.mp h1 with h2 | h2
  · have : k = 0 := by exact_mod_cast h2
    omega
  · exact h2

#print axioms sum_roots_of_unity_eq_zero
#print axioms c0_eq_zero_of_forall_roots
