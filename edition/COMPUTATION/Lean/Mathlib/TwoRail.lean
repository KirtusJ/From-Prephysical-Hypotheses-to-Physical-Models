import Mathlib

open Complex

namespace TwoRail

local notation "conj" => starRingEnd ℂ

/-- R1, most general form: no unit-modulus hypothesis at all. -/
theorem R1_general (α β xa xb xc xd : ℂ) (h : xa * xd = -(xb * xc)) :
    Complex.normSq (α * (xa*xb*xc) + α * (xb*xc*xa) + β * (xc*xb*xc) + β * (xd*xc*xa))
      = 4 * Complex.normSq α * Complex.normSq (xa*xb*xc) := by
  have e : α * (xa*xb*xc) + α * (xb*xc*xa) + β * (xc*xb*xc) + β * (xd*xc*xa)
      = 2 * (α * (xa*xb*xc)) := by linear_combination (β * xc) * h
  rw [e, Complex.normSq_mul, Complex.normSq_mul]
  have h2 : Complex.normSq (2 : ℂ) = 4 := by simp [Complex.normSq_apply]; norm_num
  rw [h2]; ring

/-- R1 (rail weight): only xa, xb, xc need unit modulus; xd does not. -/
theorem R1 (α β xa xb xc xd : ℂ) (ha : Complex.normSq xa = 1) (hb : Complex.normSq xb = 1)
    (hc : Complex.normSq xc = 1) (h : xa * xd = -(xb * xc)) :
    Complex.normSq (α * (xa*xb*xc) + α * (xb*xc*xa) + β * (xc*xb*xc) + β * (xd*xc*xa))
      = 4 * Complex.normSq α := by
  rw [R1_general α β xa xb xc xd h, Complex.normSq_mul, Complex.normSq_mul, ha, hb, hc]; ring

/-- R2, most general form: no unit-modulus hypothesis at all. -/
theorem R2_general (α β xa xb xc xd : ℂ) (h : xa * xd = -(xb * xc)) :
    Complex.normSq (α * (xa*xb*xd) + α * (xb*xc*xb) + β * (xc*xb*xd) + β * (xd*xc*xb))
      = 4 * Complex.normSq β * Complex.normSq (xb*xc*xd) := by
  have e : α * (xa*xb*xd) + α * (xb*xc*xb) + β * (xc*xb*xd) + β * (xd*xc*xb)
      = 2 * (β * (xb*xc*xd)) := by linear_combination (α * xb) * h
  rw [e, Complex.normSq_mul, Complex.normSq_mul]
  have h2 : Complex.normSq (2 : ℂ) = 4 := by simp [Complex.normSq_apply]; norm_num
  rw [h2]; ring

/-- R2 (mirror): only xb, xc, xd need unit modulus; xa does not. -/
theorem R2 (α β xa xb xc xd : ℂ) (hb : Complex.normSq xb = 1)
    (hc : Complex.normSq xc = 1) (hd : Complex.normSq xd = 1) (h : xa * xd = -(xb * xc)) :
    Complex.normSq (α * (xa*xb*xd) + α * (xb*xc*xb) + β * (xc*xb*xd) + β * (xd*xc*xb))
      = 4 * Complex.normSq β := by
  rw [R2_general α β xa xb xc xd h, Complex.normSq_mul, Complex.normSq_mul, hb, hc, hd]; ring

/-- R3, most general form: xa arbitrary. -/
theorem R3_general (α β γ xa : ℂ) :
    Complex.normSq (xa * (α + β * γ))
      = Complex.normSq xa * (Complex.normSq α + Complex.normSq β * Complex.normSq γ
          + 2 * (conj α * β * γ).re) := by
  simp only [Complex.normSq_apply, Complex.mul_re, Complex.mul_im, Complex.add_re,
    Complex.add_im, Complex.conj_re, Complex.conj_im]
  ring

/-- R3 (first tick), first part. -/
theorem R3 (α β γ xa : ℂ) (ha : Complex.normSq xa = 1) :
    Complex.normSq (xa * (α + β * γ))
      = Complex.normSq α + Complex.normSq β * Complex.normSq γ + 2 * (conj α * β * γ).re := by
  rw [R3_general, ha, one_mul]

/-- R3, second part. -/
theorem R3_unit (α β γ xa : ℂ) (ha : Complex.normSq xa = 1) (hg : Complex.normSq γ = 1)
    (hn : Complex.normSq α + Complex.normSq β = 1) :
    Complex.normSq (xa * (α + β * γ)) = 1 + 2 * (conj α * β * γ).re := by
  rw [R3 α β γ xa ha, hg, mul_one, hn]

/-- R4 (fork cross term), general form: s any real with s^2 = 1. -/
theorem R4_general (w : ℂ) (s : ℝ) (hw : Complex.normSq w = 1) (hs : s ^ 2 = 1) :
    conj (1 + (s : ℂ) * w) * (1 - (s : ℂ) * w) = -2 * (s : ℂ) * (w.im : ℂ) * Complex.I := by
  rw [Complex.normSq_apply] at hw
  apply Complex.ext
  · simp
    linear_combination (-1 : ℝ) * hs - s ^ 2 * hw
  · simp
    ring

/-- R4 as asked. -/
theorem R4 (w : ℂ) (s : ℝ) (hw : Complex.normSq w = 1) (hs : s = 1 ∨ s = -1) :
    conj (1 + (s : ℂ) * w) * (1 - (s : ℂ) * w) = -2 * (s : ℂ) * (w.im : ℂ) * Complex.I := by
  apply R4_general w s hw
  rcases hs with rfl | rfl <;> norm_num

/-- R5 (fork from a two-rail start), general form: s any real with s^2 = 1. -/
theorem R5_general (α β γ w : ℂ) (s : ℝ) (hg : Complex.normSq γ = 1)
    (hw : Complex.normSq w = 1) (hs : s ^ 2 = 1) :
    Complex.normSq (α * (1 + (s : ℂ) * w) + β * γ * (1 - (s : ℂ) * w))
      = Complex.normSq α * (2 + 2 * s * w.re) + Complex.normSq β * (2 - 2 * s * w.re)
        + 4 * s * w.im * (conj α * β * γ).im := by
  rw [Complex.normSq_apply] at hg hw
  simp only [Complex.normSq_apply, Complex.mul_re, Complex.mul_im, Complex.add_re,
    Complex.add_im, Complex.sub_re, Complex.sub_im, Complex.one_re, Complex.one_im,
    Complex.ofReal_re, Complex.ofReal_im, Complex.conj_re, Complex.conj_im]
  linear_combination
    (β.re ^ 2 + β.im ^ 2) * (1 - 2 * s * w.re + s ^ 2 * (w.re ^ 2 + w.im ^ 2)) * hg
    + (α.re ^ 2 + α.im ^ 2 + β.re ^ 2 + β.im ^ 2 - 2 * (α.re * (β.re * γ.re - β.im * γ.im) + α.im * (β.re * γ.im + β.im * γ.re))) * s ^ 2 * hw
    + (α.re ^ 2 + α.im ^ 2 + β.re ^ 2 + β.im ^ 2 - 2 * (α.re * (β.re * γ.re - β.im * γ.im) + α.im * (β.re * γ.im + β.im * γ.re))) * hs

/-- R5 as asked. -/
theorem R5 (α β γ w : ℂ) (s : ℝ) (hg : Complex.normSq γ = 1)
    (hw : Complex.normSq w = 1) (hs : s = 1 ∨ s = -1) :
    Complex.normSq (α * (1 + (s : ℂ) * w) + β * γ * (1 - (s : ℂ) * w))
      = Complex.normSq α * (2 + 2 * s * w.re) + Complex.normSq β * (2 - 2 * s * w.re)
        + 4 * s * w.im * (conj α * β * γ).im := by
  apply R5_general α β γ w s hg hw
  rcases hs with rfl | rfl <;> norm_num

/-- R6, general form: γ arbitrary. -/
theorem R6_general (p q γ u : ℂ) :
    conj (u * p) * (u * conj γ * q) * γ
      = (Complex.normSq u : ℂ) * (Complex.normSq γ : ℂ) * (conj p * q) := by
  rw [Complex.normSq_eq_conj_mul_self, Complex.normSq_eq_conj_mul_self, map_mul]
  ring

/-- R6 (compensating phase). -/
theorem R6 (p q γ u : ℂ) (hg : Complex.normSq γ = 1) :
    conj (u * p) * (u * conj γ * q) * γ = (Complex.normSq u : ℂ) * (conj p * q) := by
  rw [R6_general, hg, Complex.ofReal_one, mul_one]

/-- All six, as asked, in one statement. -/
theorem main :
    (∀ α β xa xb xc xd : ℂ, Complex.normSq xa = 1 → Complex.normSq xb = 1 →
      Complex.normSq xc = 1 → xa * xd = -(xb * xc) →
      Complex.normSq (α * (xa*xb*xc) + α * (xb*xc*xa) + β * (xc*xb*xc) + β * (xd*xc*xa))
        = 4 * Complex.normSq α) ∧
    (∀ α β xa xb xc xd : ℂ, Complex.normSq xb = 1 → Complex.normSq xc = 1 →
      Complex.normSq xd = 1 → xa * xd = -(xb * xc) →
      Complex.normSq (α * (xa*xb*xd) + α * (xb*xc*xb) + β * (xc*xb*xd) + β * (xd*xc*xb))
        = 4 * Complex.normSq β) ∧
    (∀ α β γ xa : ℂ, Complex.normSq xa = 1 →
      Complex.normSq (xa * (α + β * γ))
        = Complex.normSq α + Complex.normSq β * Complex.normSq γ + 2 * (conj α * β * γ).re) ∧
    (∀ α β γ xa : ℂ, Complex.normSq xa = 1 → Complex.normSq γ = 1 →
      Complex.normSq α + Complex.normSq β = 1 →
      Complex.normSq (xa * (α + β * γ)) = 1 + 2 * (conj α * β * γ).re) ∧
    (∀ (w : ℂ) (s : ℝ), Complex.normSq w = 1 → (s = 1 ∨ s = -1) →
      conj (1 + (s : ℂ) * w) * (1 - (s : ℂ) * w) = -2 * (s : ℂ) * (w.im : ℂ) * Complex.I) ∧
    (∀ (α β γ w : ℂ) (s : ℝ), Complex.normSq γ = 1 → Complex.normSq w = 1 → (s = 1 ∨ s = -1) →
      Complex.normSq (α * (1 + (s : ℂ) * w) + β * γ * (1 - (s : ℂ) * w))
        = Complex.normSq α * (2 + 2 * s * w.re) + Complex.normSq β * (2 - 2 * s * w.re)
          + 4 * s * w.im * (conj α * β * γ).im) ∧
    (∀ p q γ u : ℂ, Complex.normSq γ = 1 →
      conj (u * p) * (u * conj γ * q) * γ = (Complex.normSq u : ℂ) * (conj p * q)) :=
  ⟨R1, R2, R3, R3_unit, R4, R5, R6⟩

end TwoRail

#print axioms TwoRail.R1_general
#print axioms TwoRail.R2_general
#print axioms TwoRail.R3_general
#print axioms TwoRail.R4_general
#print axioms TwoRail.R5_general
#print axioms TwoRail.R6_general
#print axioms TwoRail.main
