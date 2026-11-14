import Mathlib

/-!
Character separation lemmas L1-L4 over ℂ.
Unit modulus is stated as `Complex.abs z = 1`.
-/

open Complex ComplexConjugate

namespace CharSeparation

theorem normSq_of_abs {z : ℂ} (h : Complex.abs z = 1) : Complex.normSq z = 1 := by
  rw [← Complex.sq_abs, h]; norm_num

theorem sq_add_sq_of_abs {z : ℂ} (h : Complex.abs z = 1) : z.re ^ 2 + z.im ^ 2 = 1 := by
  have := normSq_of_abs h
  rw [Complex.normSq_apply] at this
  linarith

/-- L1, general form: no hypothesis on `w` or on the real `s`. -/
theorem L1_general (w : ℂ) (s : ℝ) :
    Complex.normSq (1 + (s : ℂ) * w) = 1 + 2 * s * w.re + s ^ 2 * Complex.normSq w := by
  simp [Complex.normSq_apply]
  ring

/-- L1 as asked. -/
theorem L1 (w : ℂ) (s : ℝ) (hw : Complex.abs w = 1) (hs : s = 1 ∨ s = -1) :
    Complex.normSq (1 + (s : ℂ) * w) = 2 + 2 * s * w.re := by
  rw [L1_general, normSq_of_abs hw]
  rcases hs with rfl | rfl <;> ring

/-- L2. -/
theorem L2 (u v : ℂ) (hu : Complex.abs u = 1) (hv : Complex.abs v = 1)
    (h : u.re = v.re) : v = u ∨ v = conj u := by
  have h1 := sq_add_sq_of_abs hu
  have h2 := sq_add_sq_of_abs hv
  have h3 : (v.im - u.im) * (v.im + u.im) = 0 := by rw [h] at h1; linarith
  rcases mul_eq_zero.mp h3 with h4 | h4
  · left; apply Complex.ext
    · exact h.symm
    · linarith
  · right; apply Complex.ext
    · simpa using h.symm
    · simp; linarith

theorem re_pow2 {b : ℂ} (h : Complex.abs b = 1) : (b ^ 2).re = 2 * b.re ^ 2 - 1 := by
  have h1 := sq_add_sq_of_abs h
  have : (b ^ 2).re = b.re ^ 2 - b.im ^ 2 := by
    simp [pow_succ, Complex.mul_re, Complex.mul_im]
  rw [this]; linarith

theorem re_pow3 {b : ℂ} (h : Complex.abs b = 1) : (b ^ 3).re = 4 * b.re ^ 3 - 3 * b.re := by
  have h1 := sq_add_sq_of_abs h
  have : (b ^ 3).re = b.re ^ 3 - 3 * b.re * b.im ^ 2 := by
    simp [pow_succ, Complex.mul_re, Complex.mul_im]; ring
  rw [this]; linear_combination (-3 * b.re) * h1

theorem re_pow5 {b : ℂ} (h : Complex.abs b = 1) :
    (b ^ 5).re = 16 * b.re ^ 5 - 20 * b.re ^ 3 + 5 * b.re := by
  have h1 := sq_add_sq_of_abs h
  have : (b ^ 5).re = b.re ^ 5 - 10 * b.re ^ 3 * b.im ^ 2 + 5 * b.re * b.im ^ 4 := by
    simp [pow_succ, Complex.mul_re, Complex.mul_im]; ring
  rw [this]
  linear_combination
    (-10 * b.re ^ 3 + 5 * b.re * (b.im ^ 2 + 1 - b.re ^ 2)) * h1

/-- L3, stronger form: the three hypotheses force equal real parts. -/
theorem L3_re (b b' : ℂ) (hb : Complex.abs b = 1) (hb' : Complex.abs b' = 1)
    (h2 : (b ^ 2).re = (b' ^ 2).re) (h3 : (b ^ 3).re = (b' ^ 3).re)
    (h5 : (b ^ 5).re = (b' ^ 5).re) : b.re = b'.re := by
  rw [re_pow2 hb, re_pow2 hb'] at h2
  rw [re_pow3 hb, re_pow3 hb'] at h3
  rw [re_pow5 hb, re_pow5 hb'] at h5
  generalize b.re = x at *
  generalize b'.re = y at *
  have h : (x - y) * (x + y) = 0 := by linarith
  rcases mul_eq_zero.mp h with h | h
  · linarith
  · have hy : y = -x := by linarith
    subst hy
    by_cases hx : x = 0
    · simp [hx]
    · exfalso
      have e3 : x * (4 * x ^ 2 - 3) = 0 := by linear_combination h3 / 2
      have e3' : 4 * x ^ 2 - 3 = 0 := by
        rcases mul_eq_zero.mp e3 with h | h
        · exact absurd h hx
        · exact h
      have e5 : x * (16 * x ^ 4 - 20 * x ^ 2 + 5) = 0 := by linear_combination h5 / 2
      have e5' : 16 * x ^ 4 - 20 * x ^ 2 + 5 = 0 := by
        rcases mul_eq_zero.mp e5 with h | h
        · exact absurd h hx
        · exact h
      have : (1 : ℝ) = 0 := by
        linear_combination (4 * x ^ 2 - 2) * e3' - e5'
      norm_num at this

/-- L3 (main). -/
theorem L3 (b b' : ℂ) (hb : Complex.abs b = 1) (hb' : Complex.abs b' = 1)
    (h2 : (b ^ 2).re = (b' ^ 2).re) (h3 : (b ^ 3).re = (b' ^ 3).re)
    (h5 : (b ^ 5).re = (b' ^ 5).re) : b' = b ∨ b' = conj b :=
  L2 b b' hb hb' (L3_re b b' hb hb' h2 h3 h5)

/-- L4 (i): no modulus hypothesis needed. -/
theorem L4_pow_D1 (D1 : ℕ) (e b : ℂ) (he : e ^ D1 = 1) : (e * b) ^ D1 = b ^ D1 := by
  rw [mul_pow, he, one_mul]

/-- L4 (ii): no modulus hypothesis needed. -/
theorem L4_pow_D2 (D2 : ℕ) (e t b : ℂ) (ht : t ^ D2 = 1) (hbe : b ^ 2 * e = t) :
    (e * b) ^ D2 * b ^ D2 = 1 := by
  rw [← mul_pow, ← ht, ← hbe]; congr 1; ring

/-- L4 (ii'): the conjugate form; needs `|b| = 1`. -/
theorem L4_pow_D2_conj (D2 : ℕ) (e t b : ℂ) (ht : t ^ D2 = 1) (hbe : b ^ 2 * e = t)
    (hb : Complex.abs b = 1) : (e * b) ^ D2 = conj (b ^ D2) := by
  have h1 := L4_pow_D2 D2 e t b ht hbe
  have h2 : b ^ D2 * conj (b ^ D2) = 1 := by
    rw [Complex.mul_conj, map_pow, normSq_of_abs hb]; simp
  calc (e * b) ^ D2 = (e * b) ^ D2 * (b ^ D2 * conj (b ^ D2)) := by rw [h2, mul_one]
    _ = ((e * b) ^ D2 * b ^ D2) * conj (b ^ D2) := by ring
    _ = conj (b ^ D2) := by rw [h1, one_mul]

/-- L4 (iii): needs only `b ≠ 0`, which `|b| = 1` gives. -/
theorem L4_ne (e b : ℂ) (hb : Complex.abs b = 1) (he : e ≠ 1) : e * b ≠ b := by
  intro h
  have hb0 : b ≠ 0 := by
    intro h0; rw [h0] at hb; simp at hb
  apply he
  have : (e - 1) * b = 0 := by linear_combination h
  rcases mul_eq_zero.mp this with h | h
  · linear_combination h
  · exact absurd h hb0

/-- L4 (iv). -/
theorem L4_ne_conj (e t b : ℂ) (hbe : b ^ 2 * e = t) (hb : Complex.abs b = 1)
    (ht : t ≠ 1) : e * b ≠ conj b := by
  intro h
  apply ht
  have h2 : b * conj b = 1 := by
    rw [Complex.mul_conj, normSq_of_abs hb]; simp
  rw [← hbe, ← h2, ← h]; ring

/-- L4 as asked, all parts together (the hypothesis `|e| = 1` is carried but not used). -/
theorem L4 (D1 D2 : ℕ) (e t b : ℂ) (he : e ^ D1 = 1) (ht : t ^ D2 = 1)
    (hbe : b ^ 2 * e = t) (hb : Complex.abs b = 1) (_he1 : Complex.abs e = 1) :
    (e * b) ^ D1 = b ^ D1 ∧ (e * b) ^ D2 * b ^ D2 = 1 ∧ (e * b) ^ D2 = conj (b ^ D2) ∧
      (e ≠ 1 → e * b ≠ b) ∧ (t ≠ 1 → e * b ≠ conj b) :=
  ⟨L4_pow_D1 D1 e b he, L4_pow_D2 D2 e t b ht hbe, L4_pow_D2_conj D2 e t b ht hbe hb,
    L4_ne e b hb, L4_ne_conj e t b hbe hb⟩

end CharSeparation

#print axioms CharSeparation.L1_general
#print axioms CharSeparation.L1
#print axioms CharSeparation.L2
#print axioms CharSeparation.L3_re
#print axioms CharSeparation.L4
#print axioms CharSeparation.L3
