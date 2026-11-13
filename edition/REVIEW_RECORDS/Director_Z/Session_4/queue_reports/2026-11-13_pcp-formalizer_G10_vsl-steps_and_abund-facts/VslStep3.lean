import Mathlib

open MvPolynomial

/-- Coefficients of a partial derivative. -/
theorem MvPolynomial.coeff_pderiv' {R σ : Type*} [CommSemiring R] (j : σ)
    (p : MvPolynomial σ R) (m : σ →₀ ℕ) :
    coeff m (pderiv j p) = coeff (m + Finsupp.single j 1) p * ((m j + 1 : ℕ) : R) := by
  classical
  induction p using MvPolynomial.induction_on' with
  | h1 s a =>
    rw [pderiv_monomial, coeff_monomial, coeff_monomial]
    by_cases h : s = m + Finsupp.single j 1
    · subst h
      simp
    · rw [if_neg h, zero_mul]
      split_ifs with h2
      · have hs : s j = 0 := by
          by_contra hne
          apply h
          rw [← h2]
          ext i
          by_cases hij : i = j
          · subst hij; simp; omega
          · simp [Finsupp.single_apply, Ne.symm hij]
        simp [hs]
      · rfl
  | h2 p q hp hq => rw [map_add, coeff_add, coeff_add, hp, hq, add_mul]

/-- The operator `∂_j (t_j ∂_j ·)` multiplies the coefficient of a monomial by the square
of its exponent in `t_j` (and lowers that exponent by one). -/
theorem MvPolynomial.coeff_pderiv_X_mul_pderiv {R σ : Type*} [CommSemiring R] (j : σ)
    (g : MvPolynomial σ R) (m : σ →₀ ℕ) :
    coeff m (pderiv j (X j * pderiv j g)) =
      coeff (m + Finsupp.single j 1) g * ((m j + 1 : ℕ) : R) * ((m j + 1 : ℕ) : R) := by
  rw [coeff_pderiv', add_comm m, coeff_X_mul, coeff_pderiv', add_comm m]

/-- Step 3 of thm:vsl, general form: any index type, any commutative semiring in which
positive natural numbers are not zero divisors (`CharZero` and `NoZeroDivisors`).
If `∂_j (t_j ∂_j g) = 0` for every `j` then `g` is constant. -/
theorem MvPolynomial.eq_C_of_pderiv_X_mul_pderiv_eq_zero {R σ : Type*} [CommSemiring R]
    [CharZero R] [NoZeroDivisors R] (g : MvPolynomial σ R)
    (h : ∀ j, pderiv j (X j * pderiv j g) = 0) : g = C (coeff 0 g) := by
  classical
  ext s
  rw [coeff_C]
  split_ifs with hs
  · rw [← hs]
  · obtain ⟨j, hj⟩ : ∃ j, s j ≠ 0 := by
      by_contra hno
      push_neg at hno
      exact hs (by ext i; simp [hno i])
    have hsm : s - Finsupp.single j 1 + Finsupp.single j 1 = s := by
      ext i
      by_cases hij : i = j
      · subst hij; simp; omega
      · simp [Finsupp.single_apply, Ne.symm hij]
    have key := coeff_pderiv_X_mul_pderiv j g (s - Finsupp.single j 1)
    rw [h j, coeff_zero, hsm] at key
    have hne : (((s - Finsupp.single j 1 : σ →₀ ℕ) j + 1 : ℕ) : R) ≠ 0 :=
      Nat.cast_ne_zero.mpr (Nat.succ_ne_zero _)
    rcases mul_eq_zero.mp key.symm with h1 | h1
    · rcases mul_eq_zero.mp h1 with h2 | h2
      · exact h2
      · exact absurd h2 hne
    · exact absurd h1 hne

/-- The form used in the paper: finitely many variables, real coefficients. -/
theorem vsl_step3_real {k : ℕ} (g : MvPolynomial (Fin k) ℝ)
    (h : ∀ j, pderiv j (X j * pderiv j g) = 0) : ∃ c : ℝ, g = C c :=
  ⟨_, MvPolynomial.eq_C_of_pderiv_X_mul_pderiv_eq_zero g h⟩

/-- Characteristic zero is needed: over `ZMod 2` the polynomial `t²` satisfies the
hypothesis and is not constant. -/
theorem vsl_step3_fails_char_two :
    ∃ g : MvPolynomial Unit (ZMod 2),
      (∀ j, pderiv j (X j * pderiv j g) = 0) ∧ ∀ c, g ≠ C c := by
  refine ⟨X () ^ 2, ?_, ?_⟩
  · intro j
    cases j
    have h2 : (2 : MvPolynomial Unit (ZMod 2)) = 0 := by
      have h0 : ((2 : ℕ) : MvPolynomial Unit (ZMod 2)) = 0 := by
        rw [← map_natCast (C : ZMod 2 →+* MvPolynomial Unit (ZMod 2)) 2,
          CharP.cast_eq_zero (ZMod 2) 2, C_0]
      exact_mod_cast h0
    simp [pderiv_pow, h2]
  · intro c hc
    have := congrArg (coeff (Finsupp.single () 2)) hc
    rw [X_pow_eq_monomial, coeff_monomial, coeff_C] at this
    rw [if_pos rfl, if_neg (by
      intro h0
      exact absurd (Finsupp.single_eq_zero.mp h0.symm) (by norm_num))] at this
    exact one_ne_zero this

#print axioms MvPolynomial.coeff_pderiv_X_mul_pderiv
#print axioms MvPolynomial.eq_C_of_pderiv_X_mul_pderiv_eq_zero
#print axioms vsl_step3_real
#print axioms vsl_step3_fails_char_two
