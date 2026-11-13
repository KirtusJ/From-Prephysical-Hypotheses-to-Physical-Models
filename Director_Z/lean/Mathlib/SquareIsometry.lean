import Mathlib

open Matrix ComplexOrder

/-- General form: over a field, a one-sided inverse up to a nonzero scalar is two-sided. -/
theorem mul_eq_smul_one_comm {K n : Type*} [Field K] [Fintype n] [DecidableEq n]
    (A B : Matrix n n K) (d : K) (hd : d ≠ 0) (h : B * A = d • (1 : Matrix n n K)) :
    A * B = d • (1 : Matrix n n K) := by
  have h1 : (d⁻¹ • B) * A = 1 := by
    rw [Matrix.smul_mul, h, smul_smul, inv_mul_cancel₀ hd, one_smul]
  have h2 : A * (d⁻¹ • B) = 1 := Matrix.mul_eq_one_comm.mp h1
  rw [Matrix.mul_smul] at h2
  rw [← h2, smul_smul, mul_inv_cancel₀ hd, one_smul]

/-- The lemma as asked, complex `d ≠ 0`. -/
theorem mul_conjTranspose_eq_smul_one {n : Type*} [Fintype n] [DecidableEq n]
    (A : Matrix n n ℂ) (d : ℂ) (hd : d ≠ 0) (h : Aᴴ * A = d • (1 : Matrix n n ℂ)) :
    A * Aᴴ = d • (1 : Matrix n n ℂ) :=
  mul_eq_smul_one_comm A Aᴴ d hd h

/-- Real `d ≠ 0`. -/
theorem mul_conjTranspose_eq_real_smul_one {n : Type*} [Fintype n] [DecidableEq n]
    (A : Matrix n n ℂ) (d : ℝ) (hd : d ≠ 0) (h : Aᴴ * A = d • (1 : Matrix n n ℂ)) :
    A * Aᴴ = d • (1 : Matrix n n ℂ) := by
  have h' : Aᴴ * A = (d : ℂ) • (1 : Matrix n n ℂ) := by
    rw [h]; ext i j; simp
  have := mul_conjTranspose_eq_smul_one A (d : ℂ) (by exact_mod_cast hd) h'
  rw [this]; ext i j; simp

/-- Over `ℂ` the hypothesis `d ≠ 0` is not needed: `Aᴴ * A = 0` forces `A = 0`. -/
theorem mul_conjTranspose_eq_smul_one' {n : Type*} [Fintype n] [DecidableEq n]
    (A : Matrix n n ℂ) (d : ℂ) (h : Aᴴ * A = d • (1 : Matrix n n ℂ)) :
    A * Aᴴ = d • (1 : Matrix n n ℂ) := by
  by_cases hd : d = 0
  · subst hd
    rw [zero_smul] at h
    have hA : A = 0 := Matrix.conjTranspose_mul_self_eq_zero.mp h
    simp [hA]
  · exact mul_conjTranspose_eq_smul_one A d hd h

#print axioms mul_eq_smul_one_comm
#print axioms mul_conjTranspose_eq_smul_one
#print axioms mul_conjTranspose_eq_real_smul_one
#print axioms mul_conjTranspose_eq_smul_one'
