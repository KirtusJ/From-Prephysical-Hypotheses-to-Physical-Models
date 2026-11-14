import Mathlib

/-! Product events: the swap-parallelogram equation on ℕ × ℕ forces
`F (p,q) = a (p+q) + c (p-q)^2`.  Division-free general form first. -/

namespace ProductEvents

/-- Weak version, division-free: commutative ring without 2-torsion, hypothesis only for
the three families (U = 0), (V = (1,1)), (U = (j,0), V = (1,0)). -/
theorem two_mul_eq_of_three_families {R : Type*} [CommRing R]
    (tf : ∀ x : R, 2 * x = 0 → x = 0) (F : ℕ × ℕ → R) (hz : F (0, 0) = 0)
    (h0 : ∀ V : ℕ × ℕ, F ((0, 0) + V) + F ((0, 0) + V.swap) = 2 * F (0, 0) + 2 * F V)
    (h1 : ∀ U : ℕ × ℕ, F (U + (1, 1)) + F (U + (1, 1)) = 2 * F U + 2 * F (1, 1))
    (h2 : ∀ j : ℕ, F ((j, 0) + (1, 0)) + F ((j, 0) + (0, 1)) = 2 * F (j, 0) + 2 * F (1, 0))
    (p q : ℕ) :
    2 * F (p, q) = F (1, 1) * ((p : R) + (q : R))
      + (2 * F (1, 0) - F (1, 1)) * ((((p : ℤ) - (q : ℤ) : ℤ) : R)) ^ 2 := by
  have sym : ∀ p q : ℕ, F (q, p) = F (p, q) := by
    intro p q
    have := h0 (p, q)
    rw [hz] at this
    simp only [Prod.mk_add_mk, zero_add, Prod.swap_prod_mk, mul_zero] at this
    linear_combination this
  have shift : ∀ p q : ℕ, F (p + 1, q + 1) = F (p, q) + F (1, 1) := by
    intro p q
    have := h1 (p, q)
    simp only [Prod.mk_add_mk] at this
    have := tf (F (p + 1, q + 1) - F (p, q) - F (1, 1)) (by linear_combination this)
    linear_combination this
  have g : ∀ j : ℕ,
      2 * F (j, 0) = F (1, 1) * (j : R) + (2 * F (1, 0) - F (1, 1)) * (j : R) ^ 2 ∧
      2 * F (j + 1, 0) = F (1, 1) * ((j : R) + 1)
        + (2 * F (1, 0) - F (1, 1)) * ((j : R) + 1) ^ 2 := by
    intro j
    induction j with
    | zero => constructor
              · rw [hz]; simp
              · simp only [Nat.cast_zero, zero_add]; ring
    | succ j ih =>
      refine ⟨by push_cast; exact ih.2, ?_⟩
      have a := h2 (j + 1)
      simp only [Prod.mk_add_mk, add_zero, zero_add] at a
      have b := shift j 0
      simp only [zero_add] at b
      push_cast
      linear_combination 2 * a - 2 * b + 2 * ih.2 - ih.1
  have m : ∀ m j : ℕ, 2 * F (j + m, m) = F (1, 1) * ((j : R) + 2 * (m : R))
      + (2 * F (1, 0) - F (1, 1)) * (j : R) ^ 2 := by
    intro m
    induction m with
    | zero => intro j; simpa using (g j).1
    | succ m ih =>
      intro j
      show 2 * F (j + m + 1, m + 1) = _
      rw [shift]
      push_cast
      linear_combination ih j
  rcases le_total q p with h | h
  · obtain ⟨j, rfl⟩ := Nat.exists_eq_add_of_le h
    have := m q j
    rw [add_comm j q] at this
    push_cast
    linear_combination this
  · obtain ⟨j, rfl⟩ := Nat.exists_eq_add_of_le h
    have := m p j
    rw [add_comm j p] at this
    rw [sym]
    push_cast
    linear_combination this

/-- Full hypothesis, division-free, commutative ring without 2-torsion. -/
theorem two_mul_eq {R : Type*} [CommRing R]
    (tf : ∀ x : R, 2 * x = 0 → x = 0) (F : ℕ × ℕ → R) (hz : F (0, 0) = 0)
    (h : ∀ U V : ℕ × ℕ, F (U + V) + F (U + V.swap) = 2 * F U + 2 * F V) (p q : ℕ) :
    2 * F (p, q) = F (1, 1) * ((p : R) + (q : R))
      + (2 * F (1, 0) - F (1, 1)) * ((((p : ℤ) - (q : ℤ) : ℤ) : R)) ^ 2 :=
  two_mul_eq_of_three_families tf F hz (fun V => h (0, 0) V) (fun U => h U (1, 1))
    (fun j => h (j, 0) (1, 0)) p q

/-- Weak version over a field of characteristic not 2, with the stated constants. -/
theorem eq_of_three_families {K : Type*} [Field K] (two_ne : (2 : K) ≠ 0)
    (F : ℕ × ℕ → K) (hz : F (0, 0) = 0)
    (h0 : ∀ V : ℕ × ℕ, F ((0, 0) + V) + F ((0, 0) + V.swap) = 2 * F (0, 0) + 2 * F V)
    (h1 : ∀ U : ℕ × ℕ, F (U + (1, 1)) + F (U + (1, 1)) = 2 * F U + 2 * F (1, 1))
    (h2 : ∀ j : ℕ, F ((j, 0) + (1, 0)) + F ((j, 0) + (0, 1)) = 2 * F (j, 0) + 2 * F (1, 0))
    (p q : ℕ) :
    F (p, q) = F (1, 1) / 2 * ((p : K) + (q : K))
      + (F (1, 0) - F (1, 1) / 2) * ((((p : ℤ) - (q : ℤ) : ℤ) : K)) ^ 2 := by
  have M := two_mul_eq_of_three_families
    (fun x hx => (mul_eq_zero.mp hx).resolve_left two_ne) F hz h0 h1 h2 p q
  have e : F (1, 1) / 2 * 2 = F (1, 1) := div_mul_cancel₀ _ two_ne
  apply mul_left_cancel₀ two_ne
  linear_combination M
    - ((p : K) + (q : K) - ((((p : ℤ) - (q : ℤ) : ℤ) : K)) ^ 2) * e

/-- Full hypothesis over a field of characteristic not 2. -/
theorem eq_of_swap_parallelogram {K : Type*} [Field K] (two_ne : (2 : K) ≠ 0)
    (F : ℕ × ℕ → K) (hz : F (0, 0) = 0)
    (h : ∀ U V : ℕ × ℕ, F (U + V) + F (U + V.swap) = 2 * F U + 2 * F V) (p q : ℕ) :
    F (p, q) = F (1, 1) / 2 * ((p : K) + (q : K))
      + (F (1, 0) - F (1, 1) / 2) * ((((p : ℤ) - (q : ℤ) : ℤ) : K)) ^ 2 :=
  eq_of_three_families two_ne F hz (fun V => h (0, 0) V) (fun U => h U (1, 1))
    (fun j => h (j, 0) (1, 0)) p q

/-- Converse, any commutative ring. -/
theorem swap_parallelogram_of_form {R : Type*} [CommRing R] (a c : R) (F : ℕ × ℕ → R)
    (hF : ∀ p q : ℕ, F (p, q) = a * ((p : R) + (q : R))
      + c * ((((p : ℤ) - (q : ℤ) : ℤ) : R)) ^ 2) :
    F (0, 0) = 0 ∧
    ∀ U V : ℕ × ℕ, F (U + V) + F (U + V.swap) = 2 * F U + 2 * F V := by
  refine ⟨by simp [hF], ?_⟩
  rintro ⟨p, q⟩ ⟨r, s⟩
  simp only [Prod.mk_add_mk, Prod.swap_prod_mk, hF]
  push_cast
  ring

/-- Main theorem over ℝ: characterization. -/
theorem main (F : ℕ × ℕ → ℝ) :
    (F (0, 0) = 0 ∧ ∀ U V : ℕ × ℕ, F (U + V) + F (U + V.swap) = 2 * F U + 2 * F V) ↔
    ∀ p q : ℕ, F (p, q) = F (1, 1) / 2 * ((p : ℝ) + (q : ℝ))
      + (F (1, 0) - F (1, 1) / 2) * ((((p : ℤ) - (q : ℤ) : ℤ) : ℝ)) ^ 2 :=
  ⟨fun ⟨hz, h⟩ => eq_of_swap_parallelogram two_ne_zero F hz h,
   fun hF => swap_parallelogram_of_form _ _ F hF⟩

end ProductEvents

#print axioms ProductEvents.two_mul_eq_of_three_families
#print axioms ProductEvents.two_mul_eq
#print axioms ProductEvents.eq_of_three_families
#print axioms ProductEvents.eq_of_swap_parallelogram
#print axioms ProductEvents.swap_parallelogram_of_form
#print axioms ProductEvents.main
