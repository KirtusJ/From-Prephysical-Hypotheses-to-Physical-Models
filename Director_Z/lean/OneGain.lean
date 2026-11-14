import Mathlib

/-! One-site equation on multisets of gains in a cyclic group: Steps 4, 5, 6 and the converse.
General forms first, then the forms on `ZMod q → ℤ` with the shift. -/

namespace OneGain

/-- The shift on functions on `ZMod q`. -/
def T {q : ℕ} {A : Type*} (W : ZMod q → A) : ZMod q → A := fun g => W (g - 1)

/-! ### Statement A (Step 4) -/

/-- General form: `M` any additive commutative monoid, `T` any additive map, `R` any additive
commutative monoid with cancellation.  No subtraction, no 2-torsion hypothesis, no inverse
of `T`. -/
theorem A_general {M R : Type*} [AddCommMonoid M] [AddCancelCommMonoid R]
    (T : M → M) (hT : ∀ U V, T (U + V) = T U + T V) (G : M → R)
    (h : ∀ U V, G (U + V) + G (U + T V) = 2 • G U + 2 • G V)
    (inv : ∀ W, G (T W) = G W) (U V : M) :
    G (U + T (T V)) = G (U + V) := by
  have sym : ∀ U V, G (U + T V) = G (V + T U) := by
    intro U V
    have a := h U V
    have b := h V U
    rw [add_comm V U, add_comm (2 • G V)] at b
    exact add_left_cancel (a.trans b.symm)
  rw [sym U (T V), ← hT, inv, add_comm]

/-- Consequence in a group: `G` is unchanged by adding `T (T V) - V`. -/
theorem A_general_sub {M R : Type*} [AddCommGroup M] [AddCancelCommMonoid R]
    (T : M → M) (hT : ∀ U V, T (U + V) = T U + T V) (G : M → R)
    (h : ∀ U V, G (U + V) + G (U + T V) = 2 • G U + 2 • G V)
    (inv : ∀ W, G (T W) = G W) (U V : M) :
    G (U + (T (T V) - V)) = G U := by
  have := A_general T hT G h inv (U - V) V
  rw [sub_add_cancel] at this
  rw [← this]; congr 1; abel

/-- Statement A as asked: `ZMod q → ℤ`, any `q`, `R` a commutative ring (no hypothesis on
2-torsion is used). -/
theorem A {q : ℕ} {R : Type*} [CommRing R] (G : (ZMod q → ℤ) → R)
    (h : ∀ U V, G (U + V) + G (U + T V) = 2 * G U + 2 * G V)
    (inv : ∀ W, G (T W) = G W) (U V : ZMod q → ℤ) :
    G (U + T (T V)) = G (U + V) ∧ G (U + (T (T V) - V)) = G U := by
  have h' : ∀ U V, G (U + V) + G (U + T V) = 2 • G U + 2 • G V := by
    intro U V; rw [h]; simp [two_mul, two_nsmul]
  exact ⟨A_general T (fun _ _ => rfl) G h' inv U V, A_general_sub T (fun _ _ => rfl) G h' inv U V⟩

/-- The same on multisets themselves (`ℕ`-valued), before any extension step. -/
theorem A_nat {q : ℕ} {R : Type*} [CommRing R] (G : (ZMod q → ℕ) → R)
    (h : ∀ U V, G (U + V) + G (U + T V) = 2 * G U + 2 * G V)
    (inv : ∀ W, G (T W) = G W) (U V : ZMod q → ℕ) :
    G (U + T (T V)) = G (U + V) := by
  have h' : ∀ U V, G (U + V) + G (U + T V) = 2 • G U + 2 • G V := by
    intro U V; rw [h]; simp [two_mul, two_nsmul]
  exact A_general T (fun _ _ => rfl) G h' inv U V

/-! ### Statement B (end of Step 6) -/

/-- General form: any commutative ring; only the shift invariance and the one family
`(P', Q') = (1, 0)`, `Q = 0` of the equation are used.  Symmetry is not used, nor
2-torsion-freeness. -/
theorem B_general {R : Type*} [CommRing R] (Γ : ℤ × ℤ → R) (hz : Γ (0, 0) = 0)
    (shift : ∀ P Q : ℤ, Γ (P + 1, Q + 1) = Γ (P, Q))
    (h1 : ∀ n : ℤ, Γ (n + 1, 0) + Γ (n, 1) = 2 * Γ (n, 0) + 2 * Γ (1, 0)) (P Q : ℤ) :
    Γ (P, Q) = Γ (1, 0) * (((P - Q : ℤ) : R)) ^ 2 := by
  have shiftn : ∀ n : ℕ, ∀ P Q : ℤ, Γ (P + n, Q + n) = Γ (P, Q) := by
    intro n
    induction n with
    | zero => intro P Q; simp
    | succ n ih =>
      intro P Q
      have := shift (P + n) (Q + n)
      push_cast
      rw [← add_assoc, ← add_assoc, this, ih]
  have red : ∀ P Q : ℤ, Γ (P, Q) = Γ (P - Q, 0) := by
    intro P Q
    rcases le_total 0 Q with hQ | hQ
    · obtain ⟨n, rfl⟩ := Int.eq_ofNat_of_zero_le hQ
      have := shiftn n (P - n) 0
      rw [sub_add_cancel, zero_add] at this
      exact this
    · obtain ⟨n, hn⟩ := Int.eq_ofNat_of_zero_le (neg_nonneg.mpr hQ)
      have := shiftn n P Q
      rw [← this]; congr 1
      ext <;> simp <;> omega
  have rec : ∀ n : ℤ, Γ (n + 1, 0) + Γ (n - 1, 0) = 2 * Γ (n, 0) + 2 * Γ (1, 0) := by
    intro n
    have a := h1 n
    have b := shift (n - 1) 0
    rw [sub_add_cancel, zero_add] at b
    rw [← b]; exact a
  have pos : ∀ n : ℕ, Γ ((n : ℤ), 0) = Γ (1, 0) * (n : R) ^ 2 ∧
      Γ ((n : ℤ) + 1, 0) = Γ (1, 0) * ((n : R) + 1) ^ 2 := by
    intro n
    induction n with
    | zero => exact ⟨by simpa using hz, by simp⟩
    | succ n ih =>
      refine ⟨by push_cast; exact ih.2, ?_⟩
      have a := rec ((n : ℤ) + 1)
      rw [add_sub_cancel_right] at a
      push_cast
      linear_combination a + 2 * ih.2 - ih.1
  have neg : ∀ n : ℕ, Γ (-(n : ℤ), 0) = Γ (1, 0) * (n : R) ^ 2 ∧
      Γ (-(n : ℤ) - 1, 0) = Γ (1, 0) * ((n : R) + 1) ^ 2 := by
    intro n
    induction n with
    | zero =>
      have a := rec 0
      simp only [zero_add, zero_sub, hz] at a
      simp only [Nat.cast_zero, neg_zero, zero_sub, hz]
      constructor
      · ring
      · linear_combination a
    | succ n ih =>
      have e : -((n + 1 : ℕ) : ℤ) = -(n : ℤ) - 1 := by push_cast; ring
      rw [e]
      refine ⟨by push_cast; exact ih.2, ?_⟩
      have a := rec (-(n : ℤ) - 1)
      rw [sub_add_cancel] at a
      push_cast
      linear_combination a + 2 * ih.2 - ih.1
  rw [red]
  rcases le_total 0 (P - Q) with hn | hn
  · obtain ⟨n, hn⟩ := Int.eq_ofNat_of_zero_le hn
    rw [hn]; simpa using (pos n).1
  · obtain ⟨n, hn⟩ := Int.eq_ofNat_of_zero_le (neg_nonneg.mpr hn)
    have e : P - Q = -(n : ℤ) := by omega
    rw [e]; simpa using (neg n).1

/-- Statement B as asked (the symmetry hypothesis `_sym` is not used). -/
theorem B {R : Type*} [CommRing R] (Γ : ℤ × ℤ → R) (hz : Γ (0, 0) = 0)
    (_sym : ∀ P Q : ℤ, Γ (Q, P) = Γ (P, Q))
    (shift : ∀ P Q : ℤ, Γ (P + 1, Q + 1) = Γ (P, Q))
    (h : ∀ P Q P' Q' : ℤ,
      Γ (P + P', Q + Q') + Γ (P + Q', Q + P') = 2 * Γ (P, Q) + 2 * Γ (P', Q'))
    (P Q : ℤ) : Γ (P, Q) = Γ (1, 0) * ((P : R) - (Q : R)) ^ 2 := by
  have := B_general Γ hz shift (fun n => by simpa using h n 0 1 0) P Q
  rw [this]; push_cast; ring

/-! ### Statement C (Step 5) -/

/-- General form: `R` any additive group (not necessarily commutative) in which `q • x = 0`
forces `x = 0`.  All `q`, including `q = 0`, where the hypothesis makes `R` trivial. -/
theorem C_general {q : ℕ} {R : Type*} [AddGroup R] (tf : ∀ x : R, q • x = 0 → x = 0)
    (γ : ZMod q → R) (add : ∀ s t, γ (s + t) = γ s + γ t) (s : ZMod q) : γ s = 0 := by
  apply tf
  have := map_nsmul (AddMonoidHom.mk' γ add) q s
  simp only [AddMonoidHom.mk'_apply] at this
  rw [← this]
  have z : q • s = 0 := by rw [nsmul_eq_mul, ZMod.natCast_self, zero_mul]
  rw [z]
  have := add 0 0
  rw [add_zero] at this
  exact (self_eq_add_right.mp this)

/-- Statement C as asked: `q ≥ 1`, `R` a field of characteristic zero. -/
theorem C {q : ℕ} [NeZero q] {R : Type*} [Field R] [CharZero R]
    (γ : ZMod q → R) (add : ∀ s t, γ (s + t) = γ s + γ t) : γ = 0 := by
  funext s
  refine C_general (fun x hx => ?_) γ add s
  rw [nsmul_eq_mul] at hx
  rcases mul_eq_zero.mp hx with h | h
  · exact absurd (Nat.cast_eq_zero.mp h) (NeZero.ne q)
  · exact h

/-! ### Statement D (converse) -/

/-- Total size is unchanged by the shift. -/
theorem sum_T {q : ℕ} [NeZero q] {A : Type*} [AddCommMonoid A] (W : ZMod q → A) :
    ∑ g, T W g = ∑ g, W g :=
  Fintype.sum_equiv (Equiv.subRight 1) _ _ (fun _ => rfl)

/-- `|U + V| + |U + T V| = 2 |U| + 2 |V|`. -/
theorem D_size {q : ℕ} [NeZero q] (U V : ZMod q → ℤ) :
    ∑ g, (U + V) g + ∑ g, (U + T V) g = 2 * ∑ g, U g + 2 * ∑ g, V g := by
  simp only [Pi.add_apply, Finset.sum_add_distrib, sum_T]; ring

/-- General form of the alternating-sum identity: any weight `χ` with `χ (g - 1) = - χ g`. -/
theorem D_alt_general {q : ℕ} [NeZero q] (χ : ZMod q → ℤ) (hχ : ∀ g, χ (g - 1) = - χ g)
    (U V : ZMod q → ℤ) :
    (∑ g, χ g * (U + V) g) ^ 2 + (∑ g, χ g * (U + T V) g) ^ 2
      = 2 * (∑ g, χ g * U g) ^ 2 + 2 * (∑ g, χ g * V g) ^ 2 := by
  have e : ∑ g, χ g * T V g = - ∑ g, χ g * V g := by
    rw [← Finset.sum_neg_distrib]
    refine Fintype.sum_equiv (Equiv.subRight 1) _ _ (fun g => ?_)
    simp only [T, Equiv.subRight_apply, hχ]; ring
  simp only [Pi.add_apply, mul_add, Finset.sum_add_distrib, e]; ring

/-- The sign of the parity class, defined when `q` is even. -/
noncomputable def sign {q : ℕ} (hq : 2 ∣ q) (g : ZMod q) : ℤ :=
  if ZMod.castHom hq (ZMod 2) g = 0 then 1 else -1

theorem sign_sub_one {q : ℕ} (hq : 2 ∣ q) (g : ZMod q) : sign hq (g - 1) = - sign hq g := by
  unfold sign
  rw [map_sub, map_one]
  generalize ZMod.castHom hq (ZMod 2) g = x
  revert x; decide

/-- Parallelogram identity for the alternating sum, `q` even. -/
theorem D_alt {q : ℕ} [NeZero q] (hq : 2 ∣ q) (U V : ZMod q → ℤ) :
    (∑ g, sign hq g * (U + V) g) ^ 2 + (∑ g, sign hq g * (U + T V) g) ^ 2
      = 2 * (∑ g, sign hq g * U g) ^ 2 + 2 * (∑ g, sign hq g * V g) ^ 2 :=
  D_alt_general (sign hq) (sign_sub_one hq) U V

end OneGain

#print axioms OneGain.A_general
#print axioms OneGain.A_general_sub
#print axioms OneGain.A
#print axioms OneGain.A_nat
#print axioms OneGain.B_general
#print axioms OneGain.B
#print axioms OneGain.C_general
#print axioms OneGain.C
#print axioms OneGain.D_size
#print axioms OneGain.D_alt_general
#print axioms OneGain.D_alt
