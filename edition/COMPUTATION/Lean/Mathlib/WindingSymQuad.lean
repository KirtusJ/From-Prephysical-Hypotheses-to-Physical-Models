import Mathlib
/-!
T1. Algebraic core of lem:symquad for k = 2 and k = 3.
A polynomial that is a quadratic form in each of k vectors of R^2 is
  T = sum_{i,j,..} t i j .. * mon p i * mon p' j * ..,   mon p = (p0^2, p0 p1, p1^2).
Symmetry under exchange of the vectors is taken in the form "the coefficient array t is symmetric".
Existence: T = G(pi) with G an explicit quadratic form in the coefficients pi of prod (p0 + p1 X).
Uniqueness (k = 2 only): a quadratic form G in three variables with G(pi(p,p')) = 0 for all real p, p' is zero.
-/
open Finset

/-- the three monomials of degree 2 in (x, y) -/
def mon (x y : ℝ) : Fin 3 → ℝ := ![x ^ 2, x * y, y ^ 2]

/-- k = 2, existence. -/
theorem symquad_two (t : Fin 3 → Fin 3 → ℝ) (hs : ∀ i j, t i j = t j i)
    (p0 p1 q0 q1 : ℝ) :
    (∑ i, ∑ j, t i j * mon p0 p1 i * mon q0 q1 j)
      = t 0 0 * (p0 * q0) ^ 2 + t 2 2 * (p1 * q1) ^ 2
        + t 0 1 * ((p0 * q0) * (p0 * q1 + p1 * q0))
        + t 1 2 * ((p0 * q1 + p1 * q0) * (p1 * q1))
        + t 0 2 * (p0 * q1 + p1 * q0) ^ 2
        + (t 1 1 - 2 * t 0 2) * ((p0 * q0) * (p1 * q1)) := by
  simp only [Fin.sum_univ_three, mon, Matrix.cons_val_zero, Matrix.cons_val_one,
    Matrix.head_cons, Matrix.cons_val_two, Matrix.tail_cons]
  rw [hs 1 0, hs 2 0, hs 2 1]
  ring

/-- k = 2, existence, for an arbitrary coefficient array whose polynomial is symmetric
    (symmetry of the function, not of the array). -/
theorem symquad_two_fun (t : Fin 3 → Fin 3 → ℝ)
    (hsym : ∀ p0 p1 q0 q1 : ℝ, (∑ i, ∑ j, t i j * mon p0 p1 i * mon q0 q1 j)
        = ∑ i, ∑ j, t i j * mon q0 q1 i * mon p0 p1 j) :
    ∀ i j, t i j = t j i := by
  have E : ∀ p0 p1 q0 q1 : ℝ, _ := fun p0 p1 q0 q1 => by
    have := hsym p0 p1 q0 q1
    simp only [Fin.sum_univ_three, mon, Matrix.cons_val_zero, Matrix.cons_val_one,
      Matrix.head_cons, Matrix.cons_val_two, Matrix.tail_cons] at this
    exact this
  have a1 := E 1 0 0 1
  have a2 := E 1 0 1 1
  have a3 := E 1 0 1 (-1)
  have a4 := E 0 1 1 1
  have a5 := E 0 1 1 (-1)
  have a6 := E 1 1 1 (-1)
  norm_num at a1 a2 a3 a4 a5 a6
  intro i j
  fin_cases i <;> fin_cases j <;> simp <;> linarith

/-- k = 2, uniqueness: a quadratic form in (pi0, pi1, pi2) vanishing on all products is zero. -/
theorem symquad_two_unique (g00 g01 g02 g11 g12 g22 : ℝ)
    (h : ∀ p0 p1 q0 q1 : ℝ,
      g00 * (p0 * q0) ^ 2 + g01 * ((p0 * q0) * (p0 * q1 + p1 * q0))
      + g02 * ((p0 * q0) * (p1 * q1)) + g11 * (p0 * q1 + p1 * q0) ^ 2
      + g12 * ((p0 * q1 + p1 * q0) * (p1 * q1)) + g22 * (p1 * q1) ^ 2 = 0) :
    g00 = 0 ∧ g01 = 0 ∧ g02 = 0 ∧ g11 = 0 ∧ g12 = 0 ∧ g22 = 0 := by
  have a1 := h 1 0 1 0
  have a2 := h 0 1 0 1
  have a3 := h 1 0 0 1
  have a4 := h 1 0 1 1
  have a5 := h 0 1 1 1
  have a6 := h 1 1 1 1
  norm_num at a1 a2 a3 a4 a5 a6
  refine ⟨a1, ?_, ?_, a3, ?_, a2⟩ <;> subst_vars <;> linarith

/-- k = 3, existence. pi0..pi3 are the coefficients of (p0+p1 X)(q0+q1 X)(r0+r1 X). -/
theorem symquad_three (t : Fin 3 → Fin 3 → Fin 3 → ℝ)
    (hs1 : ∀ i j k, t i j k = t j i k) (hs2 : ∀ i j k, t i j k = t i k j)
    (p0 p1 q0 q1 r0 r1 π0 π1 π2 π3 : ℝ)
    (h0 : π0 = p0 * q0 * r0)
    (h1 : π1 = p0 * q0 * r1 + p0 * q1 * r0 + p1 * q0 * r0)
    (h2 : π2 = p0 * q1 * r1 + p1 * q0 * r1 + p1 * q1 * r0)
    (h3 : π3 = p1 * q1 * r1) :
    (∑ i, ∑ j, ∑ k, t i j k * mon p0 p1 i * mon q0 q1 j * mon r0 r1 k)
      = t 0 0 0 * π0 ^ 2 + t 0 0 1 * (π0 * π1)
        + (t 0 1 1 - 2 * t 0 0 2) * (π0 * π2)
        + (t 1 1 1 - 3 * t 0 1 2) * (π0 * π3)
        + t 0 0 2 * π1 ^ 2 + t 0 1 2 * (π1 * π2)
        + (t 1 1 2 - 2 * t 0 2 2) * (π1 * π3)
        + t 0 2 2 * π2 ^ 2 + t 1 2 2 * (π2 * π3) + t 2 2 2 * π3 ^ 2 := by
  simp only [Fin.sum_univ_three, mon, Matrix.cons_val_zero, Matrix.cons_val_one,
    Matrix.head_cons, Matrix.cons_val_two, Matrix.tail_cons]
  have e010 : t 0 1 0 = t 0 0 1 := by rw [hs2 0 1 0]
  have e020 : t 0 2 0 = t 0 0 2 := by rw [hs2 0 2 0]
  have e021 : t 0 2 1 = t 0 1 2 := by rw [hs2 0 2 1]
  have e100 : t 1 0 0 = t 0 0 1 := by rw [hs1 1 0 0, hs2 0 1 0]
  have e101 : t 1 0 1 = t 0 1 1 := by rw [hs1 1 0 1]
  have e102 : t 1 0 2 = t 0 1 2 := by rw [hs1 1 0 2]
  have e110 : t 1 1 0 = t 0 1 1 := by rw [hs2 1 1 0, hs1 1 0 1]
  have e120 : t 1 2 0 = t 0 1 2 := by rw [hs2 1 2 0, hs1 1 0 2]
  have e121 : t 1 2 1 = t 1 1 2 := by rw [hs2 1 2 1]
  have e200 : t 2 0 0 = t 0 0 2 := by rw [hs1 2 0 0, hs2 0 2 0]
  have e201 : t 2 0 1 = t 0 1 2 := by rw [hs1 2 0 1, hs2 0 2 1]
  have e202 : t 2 0 2 = t 0 2 2 := by rw [hs1 2 0 2]
  have e210 : t 2 1 0 = t 0 1 2 := by rw [hs1 2 1 0, hs2 1 2 0, hs1 1 0 2]
  have e211 : t 2 1 1 = t 1 1 2 := by rw [hs1 2 1 1, hs2 1 2 1]
  have e212 : t 2 1 2 = t 1 2 2 := by rw [hs1 2 1 2]
  have e220 : t 2 2 0 = t 0 2 2 := by rw [hs2 2 2 0, hs1 2 0 2]
  have e221 : t 2 2 1 = t 1 2 2 := by rw [hs2 2 2 1, hs1 2 1 2]
  rw [e010, e020, e021, e100, e101, e102, e110, e120, e121, e200, e201, e202, e210, e211, e212, e220, e221]
  subst h0 h1 h2 h3
  ring

#print axioms symquad_two
#print axioms symquad_two_fun
#print axioms symquad_two_unique
#print axioms symquad_three
