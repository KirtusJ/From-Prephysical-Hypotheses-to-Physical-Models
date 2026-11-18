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


/-! ## Assembly of Proposition 5.35 (`prop:solveq`) -/

namespace OneGain
open Finset

variable {q : ℕ} [NeZero q]

/-- `|m|`, as a real number. -/
def size (m : ZMod q → ℕ) : ℝ := ((∑ g, m g : ℕ) : ℝ)

/-- `ε(m) = ∑_{j=0}^{q-1} (-1)^j m(h^j)`. -/
def eps (m : ZMod q → ℕ) : ℤ := ∑ g : ZMod q, (-1 : ℤ) ^ g.val * (m g : ℤ)

theorem T_single (g : ZMod q) (n : ℕ) :
    T (Pi.single g n : ZMod q → ℕ) = Pi.single (g + 1) n := by
  funext x
  have : (x - 1 = g) ↔ (x = g + 1) := by
    constructor <;> intro h <;> linear_combination h
  simp [T, Pi.single_apply, this]

theorem T_T_single (g : ZMod q) (n : ℕ) :
    T (T (Pi.single g n : ZMod q → ℕ)) = Pi.single (g + 2) n := by
  have e : g + 1 + 1 = g + 2 := by ring
  rw [T_single, T_single, e]

theorem single_sum (a : ZMod q) (f : ZMod q → ℕ) :
    ∑ g, (Pi.single a (f g) : ZMod q → ℕ) = Pi.single a (∑ g, f g) := by
  funext x
  by_cases hx : x = a <;> simp [Pi.single_apply, hx]

/-- From Step 4 (`A_nat`): a single gain may be moved by any multiple of `2`. -/
theorem swap (F : (ZMod q → ℕ) → ℝ)
    (h : ∀ U V, F (U + V) + F (U + T V) = 2 * F U + 2 * F V)
    (inv : ∀ W, F (T W) = F W) (U : ZMod q → ℕ) (g t : ZMod q) (n : ℕ) :
    F (U + Pi.single g n) = F (U + Pi.single (g + 2 * t) n) := by
  have step : ∀ (k : ℕ) (g : ZMod q),
      F (U + Pi.single g n) = F (U + Pi.single (g + 2 * (k : ZMod q)) n) := by
    intro k
    induction k with
    | zero => intro g; simp
    | succ k ih =>
      intro g
      have a := A_nat F h inv U (Pi.single (g + 2 * (k : ZMod q)) n)
      rw [T_T_single] at a
      have e : g + 2 * (k : ZMod q) + 2 = g + 2 * ((k + 1 : ℕ) : ZMod q) := by push_cast; ring
      rw [ih g, ← a, e]
  have := step t.val g
  rwa [ZMod.natCast_zmod_val] at this

/-- Normal form: every gain replaced by its representative. -/
theorem normal (F : (ZMod q → ℕ) → ℝ) (r : ZMod q → ZMod q)
    (hs : ∀ (U : ZMod q → ℕ) (g : ZMod q) (n : ℕ),
      F (U + Pi.single g n) = F (U + Pi.single (r g) n)) (m : ZMod q → ℕ) :
    F m = F (∑ g, Pi.single (r g) (m g)) := by
  have key : ∀ (s : Finset (ZMod q)) (U : ZMod q → ℕ),
      F (U + ∑ g in s, Pi.single g (m g)) = F (U + ∑ g in s, Pi.single (r g) (m g)) := by
    intro s
    induction s using Finset.induction_on with
    | empty => intro U; simp
    | @insert a s hg ih =>
      intro U
      rw [Finset.sum_insert hg, Finset.sum_insert hg]
      calc F (U + (Pi.single a (m a) + ∑ g in s, Pi.single g (m g)))
          = F ((U + Pi.single a (m a)) + ∑ g in s, Pi.single g (m g)) := by rw [add_assoc]
        _ = F ((U + Pi.single a (m a)) + ∑ g in s, Pi.single (r g) (m g)) := ih _
        _ = F ((U + ∑ g in s, Pi.single (r g) (m g)) + Pi.single a (m a)) := by
            rw [add_right_comm]
        _ = F ((U + ∑ g in s, Pi.single (r g) (m g)) + Pi.single (r a) (m a)) := hs _ _ _
        _ = F (U + (Pi.single (r a) (m a) + ∑ g in s, Pi.single (r g) (m g))) := by
            rw [add_right_comm, add_assoc]
  have := key Finset.univ 0
  rwa [zero_add, zero_add, Finset.univ_sum_single] at this

/-! ### `q` odd -/

theorem odd_case (hq : ¬ 2 ∣ q) (F : (ZMod q → ℕ) → ℝ) (h0 : F 0 = 0)
    (h : ∀ U V, F (U + V) + F (U + T V) = 2 * F U + 2 * F V)
    (inv : ∀ W, F (T W) = F W) (m : ZMod q → ℕ) :
    F m = F (Pi.single 0 1) * size m := by
  have h2 : (2 : ZMod q) * (2 : ZMod q)⁻¹ = 1 := by
    have := ZMod.coe_mul_inv_eq_one 2 ((Nat.prime_two.coprime_iff_not_dvd).mpr hq)
    simpa using this
  have sw : ∀ (U : ZMod q → ℕ) (g g' : ZMod q) (n : ℕ),
      F (U + Pi.single g n) = F (U + Pi.single g' n) := by
    intro U g g' n
    have := swap F h inv U g ((g' - g) * (2 : ZMod q)⁻¹) n
    have e : g + 2 * ((g' - g) * (2 : ZMod q)⁻¹) = g' := by linear_combination (g' - g) * h2
    rwa [e] at this
  have nf := normal F (fun _ => 0) (fun U g n => sw U g 0 n) m
  rw [single_sum] at nf
  have addφ : ∀ s t : ℕ, F (Pi.single 0 (s + t)) = F (Pi.single 0 s) + F (Pi.single 0 t) := by
    intro s t
    have a := h (Pi.single 0 s) (Pi.single 0 t)
    rw [T_single, sw _ (0 + 1) 0, ← Pi.single_add] at a
    linarith
  have lin : ∀ n : ℕ, F (Pi.single 0 n) = F (Pi.single 0 1) * n := by
    intro n
    induction n with
    | zero => simp [h0]
    | succ n ih => rw [addφ, ih]; push_cast; ring
  rw [nf, lin, size]

/-! ### `q` even -/

/-- The equation on `ℕ²` (Step 6, without the extension to `ℤ²`). -/
theorem natSolve (Φ : ℕ → ℕ → ℝ) (h0 : Φ 0 0 = 0)
    (E : ∀ P Q P' Q' : ℕ,
      Φ (P + P') (Q + Q') + Φ (P + Q') (Q + P') = 2 * Φ P Q + 2 * Φ P' Q') (P Q : ℕ) :
    Φ P Q = Φ 1 1 / 2 * ((P : ℝ) + Q) + (Φ 1 0 - Φ 1 1 / 2) * ((P : ℝ) - Q) ^ 2 := by
  have sym : ∀ P Q, Φ Q P = Φ P Q := by
    intro P Q
    have := E 0 0 P Q
    simp only [zero_add, h0] at this
    linarith
  have sh : ∀ P Q, Φ (P + 1) (Q + 1) = Φ P Q + Φ 1 1 := by
    intro P Q
    have := E P Q 1 1
    linarith
  have base : ∀ n : ℕ,
      Φ n 0 = Φ 1 1 / 2 * (n : ℝ) + (Φ 1 0 - Φ 1 1 / 2) * (n : ℝ) ^ 2 ∧
      Φ (n + 1) 0 = Φ 1 1 / 2 * ((n : ℝ) + 1) + (Φ 1 0 - Φ 1 1 / 2) * ((n : ℝ) + 1) ^ 2 := by
    intro n
    induction n with
    | zero =>
      constructor
      · rw [h0]; simp
      · simp
    | succ n ih =>
      refine ⟨by push_cast; exact ih.2, ?_⟩
      have a := E (n + 1) 0 1 0
      have b := sh n 0
      simp only [add_zero, zero_add] at a b
      push_cast
      linear_combination a - b + 2 * ih.2 - ih.1
  induction P generalizing Q with
  | zero =>
    rw [sym Q 0, (base Q).1]; push_cast; ring
  | succ P ih =>
    cases Q with
    | zero => rw [(base P).2]; push_cast; ring
    | succ Q => rw [sh, ih Q]; push_cast; ring

theorem chi_eq (hq : 2 ∣ q) (g : ZMod q) : (-1 : ℤ) ^ g.val = sign hq g := by
  have c := map_natCast (ZMod.castHom hq (ZMod 2)) g.val
  rw [ZMod.natCast_zmod_val] at c
  have key : (ZMod.castHom hq (ZMod 2) g = 0) ↔ 2 ∣ g.val := by
    rw [c, ZMod.natCast_zmod_eq_zero_iff_dvd]
  unfold sign
  by_cases h : 2 ∣ g.val
  · rw [if_pos (key.mpr h)]; exact Even.neg_one_pow (even_iff_two_dvd.mpr h)
  · rw [if_neg (fun x => h (key.mp x))]; exact Odd.neg_one_pow (Nat.not_even_iff_odd.mp (fun e => h (even_iff_two_dvd.mp e)))

theorem chi_sub_one (hq : 2 ∣ q) (g : ZMod q) : (-1 : ℤ) ^ (g - 1).val = - (-1 : ℤ) ^ g.val := by
  rw [chi_eq hq, chi_eq hq, sign_sub_one]

theorem size_add (U V : ZMod q → ℕ) : size (U + V) = size U + size V := by
  simp [size, Finset.sum_add_distrib]

theorem size_T (V : ZMod q → ℕ) : size (T V) = size V := by
  simp [size, sum_T]

theorem eps_add (U V : ZMod q → ℕ) : eps (U + V) = eps U + eps V := by
  simp [eps, mul_add, Finset.sum_add_distrib]

theorem eps_T (hq : 2 ∣ q) (V : ZMod q → ℕ) : eps (T V) = - eps V := by
  unfold eps
  rw [← Finset.sum_neg_distrib]
  refine Fintype.sum_equiv (Equiv.subRight 1) _ _ (fun g => ?_)
  simp only [T, Equiv.subRight_apply, chi_sub_one hq]; ring

theorem size_single : size (Pi.single (0 : ZMod q) 1) = 1 := by
  simp [size, Pi.single_apply]

theorem eps_single : eps (Pi.single (0 : ZMod q) 1) = 1 := by
  simp [eps, Pi.single_apply]

theorem size_one : size (1 : ZMod q → ℕ) = q := by
  simp [size]

theorem eps_one (hq : 2 ∣ q) : eps (1 : ZMod q → ℕ) = 0 := by
  have e : T (1 : ZMod q → ℕ) = 1 := rfl
  have := eps_T hq (1 : ZMod q → ℕ)
  rw [e] at this
  omega

theorem even_case (hq : 2 ∣ q) (F : (ZMod q → ℕ) → ℝ) (h0 : F 0 = 0)
    (h : ∀ U V, F (U + V) + F (U + T V) = 2 * F U + 2 * F V)
    (inv : ∀ W, F (T W) = F W) (m : ZMod q → ℕ) :
    F m = F 1 / q * size m + (F (Pi.single 0 1) - F 1 / q) * (eps m : ℝ) ^ 2 := by
  -- representatives
  have hs : ∀ (U : ZMod q → ℕ) (g : ZMod q) (n : ℕ),
      F (U + Pi.single g n) = F (U + Pi.single (((g.val % 2 : ℕ) : ZMod q)) n) := by
    intro U g n
    have c : (((g.val % 2 + 2 * (g.val / 2) : ℕ)) : ZMod q) = g := by
      rw [Nat.mod_add_div, ZMod.natCast_zmod_val]
    rw [Nat.cast_add, Nat.cast_mul, Nat.cast_ofNat] at c
    have := swap F h inv U g (-((g.val / 2 : ℕ) : ZMod q)) n
    have e : g + 2 * (-((g.val / 2 : ℕ) : ZMod q)) = ((g.val % 2 : ℕ) : ZMod q) := by
      linear_combination (-1 : ZMod q) * c
    rwa [e] at this
  let Φ : ℕ → ℕ → ℝ := fun P Q => F (Pi.single 0 P + Pi.single 1 Q)
  let Pm : ℕ := ∑ g : ZMod q, if g.val % 2 = 0 then m g else 0
  let Qm : ℕ := ∑ g : ZMod q, if g.val % 2 = 0 then 0 else m g
  have nf : F m = Φ Pm Qm := by
    rw [normal F _ hs m]
    show _ = F (Pi.single 0 Pm + Pi.single 1 Qm)
    congr 1
    rw [← single_sum, ← single_sum, ← Finset.sum_add_distrib]
    refine Finset.sum_congr rfl (fun g _ => ?_)
    rcases Nat.mod_two_eq_zero_or_one g.val with hg | hg <;> simp [hg]
  have E : ∀ P Q P' Q' : ℕ,
      Φ (P + P') (Q + Q') + Φ (P + Q') (Q + P') = 2 * Φ P Q + 2 * Φ P' Q' := by
    intro P Q P' Q'
    have a := h (Pi.single 0 P + Pi.single 1 Q) (Pi.single 0 P' + Pi.single 1 Q')
    have t : T (Pi.single 0 P' + Pi.single 1 Q' : ZMod q → ℕ)
        = Pi.single (0 + 1) P' + Pi.single (1 + 1) Q' := by
      rw [← T_single, ← T_single]; rfl
    have s := swap F h inv (Pi.single 0 P + Pi.single 1 Q + Pi.single (0 + 1) P') (1 + 1) (-1) Q'
    have e1 : ((1 : ZMod q) + 1 + 2 * (-1)) = 0 := by ring
    rw [e1, add_assoc _ (Pi.single ((0 : ZMod q) + 1) P' : ZMod q → ℕ) _] at s
    rw [t, s] at a
    have x1 : (Pi.single 0 P + Pi.single 1 Q + (Pi.single 0 P' + Pi.single 1 Q') : ZMod q → ℕ)
        = Pi.single 0 (P + P') + Pi.single 1 (Q + Q') := by
      rw [Pi.single_add, Pi.single_add]; abel
    have x2 : (Pi.single 0 P + Pi.single 1 Q + Pi.single (0 + 1) P' + Pi.single 0 Q' : ZMod q → ℕ)
        = Pi.single 0 (P + Q') + Pi.single 1 (Q + P') := by
      rw [Pi.single_add, Pi.single_add, zero_add]; abel
    rw [x1, x2] at a
    exact a
  have Φ00 : Φ 0 0 = 0 := by simp [Φ, h0]
  have sol := natSolve Φ Φ00 E
  have Φ10 : Φ 1 0 = F (Pi.single 0 1) := by simp [Φ]
  -- sizes and alternating sums
  have hsize : ∀ m' : ZMod q → ℕ,
      ((∑ g : ZMod q, if g.val % 2 = 0 then m' g else 0 : ℕ) : ℝ)
        + ((∑ g : ZMod q, if g.val % 2 = 0 then 0 else m' g : ℕ) : ℝ) = size m' := by
    intro m'
    rw [size, ← Nat.cast_add, ← Finset.sum_add_distrib]
    congr 1
    refine Finset.sum_congr rfl (fun g _ => ?_)
    split <;> simp
  have heps : ∀ m' : ZMod q → ℕ,
      ((∑ g : ZMod q, if g.val % 2 = 0 then m' g else 0 : ℕ) : ℝ)
        - ((∑ g : ZMod q, if g.val % 2 = 0 then 0 else m' g : ℕ) : ℝ) = (eps m' : ℝ) := by
    intro m'
    rw [eps]
    push_cast
    rw [← Finset.sum_sub_distrib]
    refine Finset.sum_congr rfl (fun g _ => ?_)
    rcases Nat.mod_two_eq_zero_or_one g.val with hg | hg
    · rw [Even.neg_one_pow (Nat.even_iff.mpr hg)]; simp [hg]
    · rw [Odd.neg_one_pow (Nat.odd_iff.mpr hg)]; simp [hg]
  have main : F m = Φ 1 1 / 2 * size m + (Φ 1 0 - Φ 1 1 / 2) * (eps m : ℝ) ^ 2 := by
    rw [nf, sol, hsize, heps]
  -- the same at the full multiset identifies the first coefficient
  have hs1 : F (∑ g : ZMod q, Pi.single (((g.val % 2 : ℕ) : ZMod q)) ((1 : ZMod q → ℕ) g))
      = Φ (∑ g : ZMod q, if g.val % 2 = 0 then (1 : ZMod q → ℕ) g else 0)
          (∑ g : ZMod q, if g.val % 2 = 0 then 0 else (1 : ZMod q → ℕ) g) := by
    show _ = F (Pi.single 0 _ + Pi.single 1 _)
    congr 1
    rw [← single_sum, ← single_sum, ← Finset.sum_add_distrib]
    refine Finset.sum_congr rfl (fun g _ => ?_)
    rcases Nat.mod_two_eq_zero_or_one g.val with hg | hg <;> simp [hg]
  have one : F 1 = Φ 1 1 / 2 * q := by
    rw [normal F _ hs 1, hs1, sol, hsize, heps, size_one, eps_one hq]; simp
  have qne : (q : ℝ) ≠ 0 := Nat.cast_ne_zero.mpr (NeZero.ne q)
  have a' : F 1 / q = Φ 1 1 / 2 := by rw [one]; field_simp; ring
  rw [main, a', Φ10]

/-! ### The proposition -/

/-- The one-site equation (5.35, eq. Eq0) with the normalization at the empty multiset. -/
def Solves (FR FL : (ZMod q → ℕ) → ℝ) : Prop :=
  FR 0 = 0 ∧ FL 0 = 0 ∧ ∀ U V, FR (U + V) + FL (U + T V) = 2 * FR U + 2 * FL V

/-- Proposition 5.35 of G10, assembled. -/
theorem prop_solveq {q : ℕ} [NeZero q] :
    -- direct part
    (∀ FR FL : (ZMod q → ℕ) → ℝ, FR 0 = 0 → FL 0 = 0 →
      (∀ U V, FR (U + V) + FL (U + T V) = 2 * FR U + 2 * FL V) →
        FR = FL ∧
        (¬ 2 ∣ q → ∀ m, FR m = FR 1 / q * size m) ∧
        (2 ∣ q → ∀ m, FR m = FR 1 / q * size m
            + (FR (Pi.single 0 1) - FR 1 / q) * (eps m : ℝ) ^ 2)) ∧
    -- converse
    (∀ a : ℝ, Solves (q := q) (fun m => a * size m) (fun m => a * size m)) ∧
    (2 ∣ q → ∀ a c : ℝ, Solves (q := q) (fun m => a * size m + c * (eps m : ℝ) ^ 2)
        (fun m => a * size m + c * (eps m : ℝ) ^ 2)) ∧
    -- dimension: the parameters are determined by the function
    (∀ a a' : ℝ, (∀ m : ZMod q → ℕ, a * size m = a' * size m) → a = a') ∧
    (2 ∣ q → ∀ a c a' c' : ℝ, (∀ m : ZMod q → ℕ, a * size m + c * (eps m : ℝ) ^ 2
        = a' * size m + c' * (eps m : ℝ) ^ 2) → a = a' ∧ c = c') := by
  have qne : (q : ℝ) ≠ 0 := Nat.cast_ne_zero.mpr (NeZero.ne q)
  refine ⟨?_, ?_, ?_, ?_, ?_⟩
  · intro FR FL hR hL h
    have eq : FL = FR := by
      funext U
      have := h U 0
      have t0 : T (0 : ZMod q → ℕ) = 0 := rfl
      rw [t0, add_zero, hL] at this
      linarith
    subst eq
    have inv : ∀ W, FL (T W) = FL W := by
      intro W
      have := h 0 W
      rw [zero_add, zero_add, hR] at this
      linarith
    refine ⟨rfl, ?_, ?_⟩
    · intro hq m
      have f := odd_case hq FL hR h inv
      rw [f m, f 1, size_one]; field_simp
    · intro hq m
      exact even_case hq FL hR h inv m
  · intro a
    refine ⟨by simp [size], by simp [size], ?_⟩
    intro U V
    simp only [size_add, size_T]; ring
  · intro hq a c
    refine ⟨by simp [size, eps], by simp [size, eps], ?_⟩
    intro U V
    simp only [size_add, size_T, eps_add, eps_T hq]; push_cast; ring
  · intro a a' hm
    have := hm (Pi.single 0 1)
    rw [size_single] at this
    linarith
  · intro hq a c a' c' hm
    have h1 := hm 1
    have h2 := hm (Pi.single 0 1)
    rw [size_one, eps_one hq] at h1
    rw [size_single, eps_single] at h2
    have ha : a = a' := by
      have : a * (q : ℝ) = a' * q := by simpa using h1
      exact mul_right_cancel₀ qne this
    subst ha
    refine ⟨rfl, ?_⟩
    simp at h2
    linarith

end OneGain

#print axioms OneGain.prop_solveq
