/-
FourGain.lean  --  Lean 4.12.0, Mathlib v4.12.0.

Q1  parallelogram law  ==>  quadratic form, no regularity assumption
Q2  the symmetry step on an additive commutative monoid
Q3  the converse of Q1
Q4  rail relation: maximizers are closed under alpha and beta

Three levels for Q1:
  * `Core`   : values in an additive commutative group `V` (2-torsion-free where needed),
               undivided polar form `P g s t = g (s + t) - g (s - t)`  (= 2 B);
  * `Mod`    : values in a module over a ring in which 2 is invertible,
               `Bm R g s t = ⅟2 • (g (s + t) - g (s - t))`;
  * `Real`   : values in `ℝ`, `B g s t = (g (s + t) - g (s - t)) / 2`, the statements as asked.
No `sorry`, no new axiom, no `native_decide`.
-/
import Mathlib

namespace FourGain

/-! ## Q1, core level: values in an additive commutative group -/

section Core

variable {D V : Type*} [AddCommGroup D] [AddCommGroup V]

/-- Undivided polar form, `P = 2 B`. -/
def P (g : D → V) (s t : D) : V := g (s + t) - g (s - t)

/-- Cancellation of a factor 2 in a 2-torsion-free group. -/
theorem two_cancel (hV : ∀ v : V, v + v = 0 → v = 0) {a b : V} (h : a + a = b + b) : a = b := by
  have h0 : (a - b) + (a - b) = 0 := by
    rw [show a - b + (a - b) = (a + a) - (b + b) by abel, h, sub_self]
  exact sub_eq_zero.mp (hV _ h0)

/-- Q1(a), first half. Needs 2-torsion-freeness (see `Q1a_needs_torsion_free`). -/
theorem core_g_zero (hV : ∀ v : V, v + v = 0 → v = 0) (g : D → V)
    (h : ∀ s t : D, g (s + t) + g (s - t) = 2 • g s + 2 • g t) : g 0 = 0 := by
  have h0 := h 0 0
  simp only [add_zero, sub_zero, two_nsmul] at h0
  exact hV _ (self_eq_add_right.mp h0)

/-- Q1(a), second half. NO hypothesis on `V` is used: evenness holds in every additive
commutative group of values. -/
theorem core_g_neg (g : D → V)
    (h : ∀ s t : D, g (s + t) + g (s - t) = 2 • g s + 2 • g t) (s : D) : g (-s) = g s := by
  have h1 := h s 0
  have h2 := h 0 s
  rw [add_zero, sub_zero] at h1
  rw [zero_add, zero_sub, add_comm (2 • g 0)] at h2
  exact (add_left_cancel (h1.trans h2.symm)).symm

/-- Q1(b), undivided. No hypothesis on `V`. -/
theorem core_P_symm (g : D → V)
    (h : ∀ s t : D, g (s + t) + g (s - t) = 2 • g s + 2 • g t) (s t : D) :
    P g s t = P g t s := by
  unfold P
  rw [add_comm t s, ← neg_sub s t, core_g_neg g h]

/-- Q1(c), undivided: `P(s,s) = 4 g(s)`. -/
theorem core_P_self (hV : ∀ v : V, v + v = 0 → v = 0) (g : D → V)
    (h : ∀ s t : D, g (s + t) + g (s - t) = 2 • g s + 2 • g t) (s : D) :
    P g s s = 4 • g s := by
  have h1 := h s s
  rw [sub_self, core_g_zero hV g h, add_zero] at h1
  unfold P
  rw [sub_self, core_g_zero hV g h, sub_zero, h1]
  abel

/-- The linear algebra behind Q1(d): four instances of the law give the doubled identity. -/
theorem lin4 {A Bm C E x y p q r w z : V}
    (e1 : A + C = 2 • p + 2 • q) (e2 : Bm + C = 2 • r + 2 • w)
    (e3 : A + E = 2 • x + 2 • z) (e4 : E + Bm = 2 • y + 2 • z) :
    (x - y) + (x - y) = (p - r + (q - w)) + (p - r + (q - w)) := by
  have k : ((x - y) + (x - y)) - ((p - r + (q - w)) + (p - r + (q - w)))
      = ((A + C) - (2 • p + 2 • q)) - ((Bm + C) - (2 • r + 2 • w))
        - ((A + E) - (2 • x + 2 • z)) + ((E + Bm) - (2 • y + 2 • z)) := by abel
  rw [sub_eq_zero.mpr e1, sub_eq_zero.mpr e2, sub_eq_zero.mpr e3, sub_eq_zero.mpr e4] at k
  exact sub_eq_zero.mp (k.trans (by simp))

/-- Q1(d) doubled; no hypothesis on `V`, no use of (a). -/
theorem core_P_add_left_two (g : D → V)
    (h : ∀ s t : D, g (s + t) + g (s - t) = 2 • g s + 2 • g t) (s s' t : D) :
    P g (s + s') t + P g (s + s') t = (P g s t + P g s' t) + (P g s t + P g s' t) := by
  have e1 : g (s + s' + t + t) + g (s - s') = 2 • g (s + t) + 2 • g (s' + t) := by
    have := h (s + t) (s' + t)
    rwa [show s + t + (s' + t) = s + s' + t + t by abel,
      show s + t - (s' + t) = s - s' by abel] at this
  have e2 : g (s + s' - t - t) + g (s - s') = 2 • g (s - t) + 2 • g (s' - t) := by
    have := h (s - t) (s' - t)
    rwa [show s - t + (s' - t) = s + s' - t - t by abel,
      show s - t - (s' - t) = s - s' by abel] at this
  have e3 : g (s + s' + t + t) + g (s + s') = 2 • g (s + s' + t) + 2 • g t := by
    have := h (s + s' + t) t
    rwa [show s + s' + t - t = s + s' by abel] at this
  have e4 : g (s + s') + g (s + s' - t - t) = 2 • g (s + s' - t) + 2 • g t := by
    have := h (s + s' - t) t
    rwa [show s + s' - t + t = s + s' by abel] at this
  exact lin4 e1 e2 e3 e4

/-- Q1(d), undivided: additivity in the first argument. -/
theorem core_P_add_left (hV : ∀ v : V, v + v = 0 → v = 0) (g : D → V)
    (h : ∀ s t : D, g (s + t) + g (s - t) = 2 • g s + 2 • g t) (s s' t : D) :
    P g (s + s') t = P g s t + P g s' t :=
  two_cancel hV (core_P_add_left_two g h s s' t)

/-- Additivity in the second argument, by symmetry. -/
theorem core_P_add_right (hV : ∀ v : V, v + v = 0 → v = 0) (g : D → V)
    (h : ∀ s t : D, g (s + t) + g (s - t) = 2 • g s + 2 • g t) (s t t' : D) :
    P g s (t + t') = P g s t + P g s t' := by
  rw [core_P_symm g h s (t + t'), core_P_add_left hV g h, core_P_symm g h t s,
    core_P_symm g h t' s]

theorem core_P_zsmul_left (hV : ∀ v : V, v + v = 0 → v = 0) (g : D → V)
    (h : ∀ s t : D, g (s + t) + g (s - t) = 2 • g s + 2 • g t) (n : ℤ) (s t : D) :
    P g (n • s) t = n • P g s t :=
  (AddMonoidHom.mk' (fun s => P g s t) (fun a b => core_P_add_left hV g h a b t)).map_zsmul s n

theorem core_P_zsmul_right (hV : ∀ v : V, v + v = 0 → v = 0) (g : D → V)
    (h : ∀ s t : D, g (s + t) + g (s - t) = 2 • g s + 2 • g t) (n : ℤ) (s t : D) :
    P g s (n • t) = n • P g s t := by
  rw [core_P_symm g h s (n • t), core_P_zsmul_left hV g h, core_P_symm g h t s]

/-- Q1(e), core: `g (n • s) = n^2 • g s` for every integer `n`. -/
theorem core_g_zsmul (hV : ∀ v : V, v + v = 0 → v = 0) (g : D → V)
    (h : ∀ s t : D, g (s + t) + g (s - t) = 2 • g s + 2 • g t) (n : ℤ) (s : D) :
    g (n • s) = (n ^ 2) • g s := by
  have h4 : 4 • g (n • s) = 4 • ((n ^ 2) • g s) := by
    rw [← core_P_self hV g h (n • s), core_P_zsmul_left hV g h, core_P_zsmul_right hV g h,
      core_P_self hV g h s]
    module
  apply two_cancel hV
  apply two_cancel hV
  have e : ∀ a : V, a + a + (a + a) = 4 • a := fun a => by abel
  rw [e, e, h4]

/-- 2-torsion-freeness cannot be dropped from Q1(a): the constant map `1 : ℤ → ZMod 2`
satisfies the law and `g 0 ≠ 0`. -/
theorem Q1a_needs_torsion_free :
    ∃ g : ℤ → ZMod 2, (∀ s t : ℤ, g (s + t) + g (s - t) = 2 • g s + 2 • g t) ∧ g 0 ≠ 0 :=
  ⟨fun _ => 1, fun _ _ => by
    show (1 : ZMod 2) + 1 = 2 • (1 : ZMod 2) + 2 • (1 : ZMod 2)
    decide, by
    show (1 : ZMod 2) ≠ 0
    decide⟩

end Core

/-! ## Q1, module level: 2 invertible in the ring of scalars -/

section Mod

/-- A module over a ring in which 2 is invertible is 2-torsion-free. -/
theorem torsion_free_of_invertible_two (R : Type*) {V : Type*} [Ring R] [Invertible (2 : R)]
    [AddCommGroup V] [Module R V] : ∀ v : V, v + v = 0 → v = 0 := by
  intro v hv
  have h2 : (2 : R) • v = 0 := by rw [two_smul]; exact hv
  rw [← invOf_smul_smul (2 : R) v, h2, smul_zero]

/-- `B(s,t) = (g(s+t) - g(s-t)) / 2` with values in an `R`-module. -/
def Bm (R : Type*) {D V : Type*} [AddCommGroup D] [Ring R] [Invertible (2 : R)]
    [AddCommGroup V] [Module R V] (g : D → V) (s t : D) : V :=
  (⅟ (2 : R)) • (g (s + t) - g (s - t))

theorem mod_g_zero (R : Type*) {D V : Type*} [AddCommGroup D] [Ring R] [Invertible (2 : R)]
    [AddCommGroup V] [Module R V] (g : D → V)
    (h : ∀ s t : D, g (s + t) + g (s - t) = 2 • g s + 2 • g t) : g 0 = 0 :=
  core_g_zero (torsion_free_of_invertible_two R) g h

theorem mod_B_symm (R : Type*) {D V : Type*} [AddCommGroup D] [Ring R] [Invertible (2 : R)]
    [AddCommGroup V] [Module R V] (g : D → V)
    (h : ∀ s t : D, g (s + t) + g (s - t) = 2 • g s + 2 • g t) (s t : D) :
    Bm R g s t = Bm R g t s :=
  congrArg (fun v => (⅟ (2 : R)) • v) (core_P_symm g h s t)

theorem mod_B_self (R : Type*) {D V : Type*} [AddCommGroup D] [Ring R] [Invertible (2 : R)]
    [AddCommGroup V] [Module R V] (g : D → V)
    (h : ∀ s t : D, g (s + t) + g (s - t) = 2 • g s + 2 • g t) (s : D) :
    Bm R g s s = 2 • g s := by
  have hP : g (s + s) - g (s - s) = 4 • g s :=
    core_P_self (torsion_free_of_invertible_two R) g h s
  unfold Bm
  rw [hP, show (4 : ℕ) • g s = 2 • g s + 2 • g s by abel, ← two_smul R (2 • g s),
    invOf_smul_smul]

theorem mod_B_add_left (R : Type*) {D V : Type*} [AddCommGroup D] [Ring R] [Invertible (2 : R)]
    [AddCommGroup V] [Module R V] (g : D → V)
    (h : ∀ s t : D, g (s + t) + g (s - t) = 2 • g s + 2 • g t) (s s' t : D) :
    Bm R g (s + s') t = Bm R g s t + Bm R g s' t := by
  have hP : g (s + s' + t) - g (s + s' - t)
      = (g (s + t) - g (s - t)) + (g (s' + t) - g (s' - t)) :=
    core_P_add_left (torsion_free_of_invertible_two R) g h s s' t
  unfold Bm
  rw [hP, smul_add]

theorem mod_B_add_right (R : Type*) {D V : Type*} [AddCommGroup D] [Ring R] [Invertible (2 : R)]
    [AddCommGroup V] [Module R V] (g : D → V)
    (h : ∀ s t : D, g (s + t) + g (s - t) = 2 • g s + 2 • g t) (s t t' : D) :
    Bm R g s (t + t') = Bm R g s t + Bm R g s t' := by
  rw [mod_B_symm R g h s (t + t'), mod_B_add_left R g h, mod_B_symm R g h t s,
    mod_B_symm R g h t' s]

theorem mod_g_zsmul (R : Type*) {D V : Type*} [AddCommGroup D] [Ring R] [Invertible (2 : R)]
    [AddCommGroup V] [Module R V] (g : D → V)
    (h : ∀ s t : D, g (s + t) + g (s - t) = 2 • g s + 2 • g t) (n : ℤ) (s : D) :
    g (n • s) = (n ^ 2) • g s :=
  core_g_zsmul (torsion_free_of_invertible_two R) g h n s

end Mod

/-! ## Q1, real level: the statements as asked -/

section Real

variable {D : Type*} [AddCommGroup D]

/-- `B(s,t) = (g(s+t) - g(s-t)) / 2`. -/
noncomputable def B (g : D → ℝ) (s t : D) : ℝ := (g (s + t) - g (s - t)) / 2

/-- Q1(a). -/
theorem Q1a (g : D → ℝ) (h : ∀ s t : D, g (s + t) + g (s - t) = 2 * g s + 2 * g t) :
    g 0 = 0 ∧ ∀ s : D, g (-s) = g s := by
  have h0 : g 0 = 0 := by
    have := h 0 0
    simp only [add_zero, sub_zero] at this
    linarith
  refine ⟨h0, fun s => ?_⟩
  have := h 0 s
  simp only [zero_add, zero_sub] at this
  linarith

/-- Q1(b). -/
theorem Q1b (g : D → ℝ) (h : ∀ s t : D, g (s + t) + g (s - t) = 2 * g s + 2 * g t)
    (s t : D) : B g s t = B g t s := by
  unfold B
  rw [add_comm t s, ← neg_sub s t, (Q1a g h).2]

/-- Q1(c). -/
theorem Q1c (g : D → ℝ) (h : ∀ s t : D, g (s + t) + g (s - t) = 2 * g s + 2 * g t)
    (s : D) : B g s s = 2 * g s := by
  have h1 := h s s
  have h0 := (Q1a g h).1
  unfold B
  rw [sub_self] at h1 ⊢
  linarith

/-- Q1(d), the shortest route found: four instances of the law and linear arithmetic.
Neither `g 0 = 0` nor `g (-s) = g s` is used. -/
theorem Q1d (g : D → ℝ) (h : ∀ s t : D, g (s + t) + g (s - t) = 2 * g s + 2 * g t)
    (s s' t : D) : B g (s + s') t = B g s t + B g s' t := by
  have e1 := h (s + t) (s' + t)
  have e2 := h (s - t) (s' - t)
  have e3 := h (s + s' + t) t
  have e4 := h (s + s' - t) t
  rw [show s + t + (s' + t) = s + s' + t + t by abel,
    show s + t - (s' + t) = s - s' by abel] at e1
  rw [show s - t + (s' - t) = s + s' - t - t by abel,
    show s - t - (s' - t) = s - s' by abel] at e2
  rw [show s + s' + t - t = s + s' by abel] at e3
  rw [show s + s' - t + t = s + s' by abel] at e4
  unfold B
  linarith

/-- Additivity in the second argument, by symmetry. -/
theorem Q1d_right (g : D → ℝ) (h : ∀ s t : D, g (s + t) + g (s - t) = 2 * g s + 2 * g t)
    (s t t' : D) : B g s (t + t') = B g s t + B g s t' := by
  rw [Q1b g h s (t + t'), Q1d g h, Q1b g h t s, Q1b g h t' s]

/-! ### The hand route for Q1(d), as written in the paper -/

/-- Hand identity 1: `2 B(s,t) + 2 B(s',t) = B(s + s', 2t)`. -/
theorem hand_H1 (g : D → ℝ) (h : ∀ s t : D, g (s + t) + g (s - t) = 2 * g s + 2 * g t)
    (s s' t : D) : 2 * B g s t + 2 * B g s' t = B g (s + s') (t + t) := by
  have e1 := h (s + t) (s' + t)
  have e2 := h (s - t) (s' - t)
  rw [show s + t + (s' + t) = s + s' + (t + t) by abel,
    show s + t - (s' + t) = s - s' by abel] at e1
  rw [show s - t + (s' - t) = s + s' - (t + t) by abel,
    show s - t - (s' - t) = s - s' by abel] at e2
  unfold B
  linarith

/-- Hand identity 2, obtained exactly as the paper says: identity 1 at `s' = 0`.
This step uses `B(0,t) = 0`, i.e. evenness of `g` (Q1(a)). -/
theorem hand_H2 (g : D → ℝ) (h : ∀ s t : D, g (s + t) + g (s - t) = 2 * g s + 2 * g t)
    (s t : D) : 2 * B g s t = B g s (t + t) := by
  have h1 := hand_H1 g h s 0 t
  have hB0 : B g 0 t = 0 := by
    unfold B
    rw [zero_add, zero_sub, (Q1a g h).2, sub_self, zero_div]
  rw [add_zero, hB0] at h1
  linarith

/-- Q1(d) by the hand route: identity 1, and identity 2 applied at `s + s'`. -/
theorem hand_Q1d (g : D → ℝ) (h : ∀ s t : D, g (s + t) + g (s - t) = 2 * g s + 2 * g t)
    (s s' t : D) : B g (s + s') t = B g s t + B g s' t := by
  have h1 := hand_H1 g h s s' t
  have h2 := hand_H2 g h (s + s') t
  linarith

/-- Q1(e), second half: `g (n • s) = n^2 * g s` for every integer `n`. -/
theorem Q1e_zsmul (g : D → ℝ) (h : ∀ s t : D, g (s + t) + g (s - t) = 2 * g s + 2 * g t)
    (n : ℤ) (s : D) : g (n • s) = (n : ℝ) ^ 2 * g s := by
  have hc : ∀ s t : D, g (s + t) + g (s - t) = 2 • g s + 2 • g t := fun s t => by
    rw [h s t]; simp [nsmul_eq_mul]
  have hV : ∀ v : ℝ, v + v = 0 → v = 0 := fun v hv => by linarith
  have := core_g_zsmul hV g hc n s
  rw [this]
  simp [zsmul_eq_mul]

/-- Q1 (a)-(e) in one statement: `B` is a symmetric biadditive map (bundled as `D →+ D →+ ℝ`),
`g s = B s s / 2`, and `g (n • s) = n^2 * g s`.  MAIN THEOREM. -/
theorem Q1_main (g : D → ℝ) (h : ∀ s t : D, g (s + t) + g (s - t) = 2 * g s + 2 * g t) :
    g 0 = 0 ∧ (∀ s : D, g (-s) = g s) ∧
    ∃ β : D →+ D →+ ℝ,
      (∀ s t : D, β s t = (g (s + t) - g (s - t)) / 2) ∧
      (∀ s t : D, β s t = β t s) ∧
      (∀ s : D, β s s = 2 * g s) ∧
      (∀ s : D, g s = β s s / 2) ∧
      (∀ (n : ℤ) (s : D), g (n • s) = (n : ℝ) ^ 2 * g s) := by
  refine ⟨(Q1a g h).1, (Q1a g h).2, ?_⟩
  refine ⟨AddMonoidHom.mk' (fun s => AddMonoidHom.mk' (fun t => B g s t) (Q1d_right g h s))
    (fun s s' => AddMonoidHom.ext fun t => Q1d g h s s' t), fun _ _ => rfl, ?_, ?_, ?_,
    Q1e_zsmul g h⟩
  · intro s t; exact Q1b g h s t
  · intro s; exact Q1c g h s
  · intro s
    have : B g s s = 2 * g s := Q1c g h s
    show g s = B g s s / 2
    linarith

end Real

/-! ## Q2: the symmetry step -/

section Q2

variable {M V : Type*} [AddCommMonoid M]

/-- Q2(a), general: values in an additive cancellative commutative monoid, `T` ANY function.
Uses (Q) at `(u,v)` and `(v,u)` only; no additivity of `T`, no invariance. -/
theorem Q2a [AddCancelCommMonoid V] (T : M → M) (f : M → V)
    (hQ : ∀ u v : M, f (u + v) + f (u + T v) = 2 • f u + 2 • f v) (u v : M) :
    f (u + T v) = f (v + T u) := by
  have h1 := hQ u v
  have h2 := hQ v u
  rw [add_comm v u, add_comm (2 • f v)] at h2
  exact add_left_cancel (h1.trans h2.symm)

/-- Key step for Q2(b): `f (T u + T v) = f (u + v)` from (Q) and invariance, `T` ANY function. -/
theorem Q2_TT [AddCancelCommMonoid V] (T : M → M) (f : M → V)
    (hQ : ∀ u v : M, f (u + v) + f (u + T v) = 2 • f u + 2 • f v)
    (hinv : ∀ u : M, f (T u) = f u) (u v : M) :
    f (T u + T v) = f (u + v) := by
  have h1 := hQ (T u) v
  rw [hinv, ← hQ u v, add_comm (T u) v, ← Q2a T f hQ u v, add_comm (f (u + v))] at h1
  exact add_left_cancel h1

/-- Q2(b), general: uses (Q) and the invariance only.  ADDITIVITY OF `T` IS NOT USED. -/
theorem Q2b [AddCancelCommMonoid V] (T : M → M) (f : M → V)
    (hQ : ∀ u v : M, f (u + v) + f (u + T v) = 2 • f u + 2 • f v)
    (hinv : ∀ u : M, f (T u) = f u) (u v : M) :
    f (u + T (T v)) = f (u + v) := by
  rw [Q2a T f hQ u (T v), add_comm (T v) (T u), Q2_TT T f hQ hinv]

/-- Q2(b) by the route of the task (additivity, then invariance), for comparison. -/
theorem Q2b_hand [AddCancelCommMonoid V] (T : M → M) (f : M → V)
    (hT : ∀ u v : M, T (u + v) = T u + T v)
    (hQ : ∀ u v : M, f (u + v) + f (u + T v) = 2 • f u + 2 • f v)
    (hinv : ∀ u : M, f (T u) = f u) (u v : M) :
    f (u + T (T v)) = f (u + v) := by
  rw [Q2a T f hQ u (T v), ← hT, hinv, add_comm]

/-- `f 0 = 0` follows from (Q) and `T (0 + 0) = T 0 + T 0`, when the values are 2-torsion-free. -/
theorem Q2_f_zero [AddCancelCommMonoid V] (hV : ∀ c : V, c + c = 0 → c = 0) (T : M → M)
    (f : M → V) (hT0 : T (0 + 0) = T 0 + T 0)
    (hQ : ∀ u v : M, f (u + v) + f (u + T v) = 2 • f u + 2 • f v) : f 0 = 0 := by
  have he : T 0 + T 0 = T 0 := by rw [← hT0, add_zero]
  have h1 := hQ (T 0) 0
  rw [add_zero, he, two_nsmul, two_nsmul] at h1
  exact hV _ (self_eq_add_right.mp h1)

/-- The invariance `f (T u) = f u` is NOT an independent hypothesis: it follows from (Q)
and `T (0 + 0) = T 0 + T 0`, when the values are 2-torsion-free. -/
theorem Q2_inv [AddCancelCommMonoid V] (hV : ∀ c : V, c + c = 0 → c = 0) (T : M → M)
    (f : M → V) (hT0 : T (0 + 0) = T 0 + T 0)
    (hQ : ∀ u v : M, f (u + v) + f (u + T v) = 2 • f u + 2 • f v) (u : M) :
    f (T u) = f u := by
  have h1 := hQ 0 u
  rw [zero_add, zero_add, Q2_f_zero hV T f hT0 hQ, smul_zero, zero_add, two_nsmul] at h1
  exact add_left_cancel h1

/-- Q2(b) without the invariance hypothesis: (Q) and `T (0 + 0) = T 0 + T 0` suffice. -/
theorem Q2b' [AddCancelCommMonoid V] (hV : ∀ c : V, c + c = 0 → c = 0) (T : M → M)
    (f : M → V) (hT0 : T (0 + 0) = T 0 + T 0)
    (hQ : ∀ u v : M, f (u + v) + f (u + T v) = 2 • f u + 2 • f v) (u v : M) :
    f (u + T (T v)) = f (u + v) :=
  Q2b T f hQ (Q2_inv hV T f hT0 hQ) u v

/-- Q2 as asked, real values; the additivity hypothesis on `T` is dropped (not used). -/
theorem Q2_real (T : M → M) (f : M → ℝ)
    (hQ : ∀ u v : M, f (u + v) + f (u + T v) = 2 * f u + 2 * f v)
    (hinv : ∀ u : M, f (T u) = f u) :
    (∀ u v : M, f (u + T v) = f (v + T u)) ∧ (∀ u v : M, f (u + T (T v)) = f (u + v)) := by
  have hQ' : ∀ u v : M, f (u + v) + f (u + T v) = 2 • f u + 2 • f v := fun u v => by
    rw [hQ u v]; simp [nsmul_eq_mul]
  exact ⟨Q2a T f hQ', Q2b T f hQ' hinv⟩

/-- Q2, real values, with the invariance hypothesis dropped and derived instead. -/
theorem Q2_real' (T : M → M) (f : M → ℝ)
    (hT : ∀ u v : M, T (u + v) = T u + T v)
    (hQ : ∀ u v : M, f (u + v) + f (u + T v) = 2 * f u + 2 * f v) :
    f 0 = 0 ∧ (∀ u : M, f (T u) = f u) ∧
    (∀ u v : M, f (u + T v) = f (v + T u)) ∧ (∀ u v : M, f (u + T (T v)) = f (u + v)) := by
  have hQ' : ∀ u v : M, f (u + v) + f (u + T v) = 2 • f u + 2 • f v := fun u v => by
    rw [hQ u v]; simp [nsmul_eq_mul]
  have hV : ∀ v : ℝ, v + v = 0 → v = 0 := fun v hv => by linarith
  exact ⟨Q2_f_zero hV T f (hT 0 0) hQ', Q2_inv hV T f (hT 0 0) hQ', Q2a T f hQ',
    Q2b' hV T f (hT 0 0) hQ'⟩

/-- Q2(b) is FALSE from (Q) alone: on `ℕ` with `T v = v + 1` and `f n = 2 n + 1`, (Q) holds
(so does (a)), `f` is not `T`-invariant, `T` is not additive, and (b) fails at `u = v = 0`. -/
theorem Q2b_false_from_Q_alone :
    ∃ (T : ℕ → ℕ) (f : ℕ → ℝ),
      (∀ u v : ℕ, f (u + v) + f (u + T v) = 2 * f u + 2 * f v) ∧
      ¬ (∀ u v : ℕ, f (u + T (T v)) = f (u + v)) := by
  refine ⟨fun n => n + 1, fun n => 2 * (n : ℝ) + 1, fun u v => ?_, fun hb => ?_⟩
  · push_cast; ring
  · have := hb 0 0
    norm_num at this

end Q2

/-! ## Q3: the converse -/

section Q3

/-- Q3, general: `D` any additive group (commutativity not used), values in any additive
commutative group, `B` biadditive.  SYMMETRY OF `B` IS NOT USED. -/
theorem Q3 {D V : Type*} [AddGroup D] [AddCommGroup V] (B : D → D → V)
    (hl : ∀ s s' t : D, B (s + s') t = B s t + B s' t)
    (hr : ∀ s t t' : D, B s (t + t') = B s t + B s t') (s t : D) :
    B (s + t) (s + t) + B (s - t) (s - t) = 2 • B s s + 2 • B t t := by
  have hnl : ∀ a x : D, B (-a) x = -B a x := fun a x =>
    (AddMonoidHom.mk' (fun s => B s x) (fun a b => hl a b x)).map_neg a
  have hnr : ∀ x a : D, B x (-a) = -B x a := fun x a =>
    (AddMonoidHom.mk' (fun t => B x t) (fun a b => hr x a b)).map_neg a
  simp only [sub_eq_add_neg, hl, hr, hnl, hnr]
  abel

/-- Q3 as asked: symmetric, additive in the first argument, real values. -/
theorem Q3_real {D : Type*} [AddCommGroup D] (B : D → D → ℝ)
    (hsymm : ∀ s t : D, B s t = B t s)
    (hl : ∀ s s' t : D, B (s + s') t = B s t + B s' t) (s t : D) :
    B (s + t) (s + t) + B (s - t) (s - t) = 2 * B s s + 2 * B t t := by
  have hr : ∀ s t t' : D, B s (t + t') = B s t + B s t' := fun s t t' => by
    rw [hsymm s (t + t'), hl, hsymm t s, hsymm t' s]
  have := Q3 B hl hr s t
  rw [this]
  simp [nsmul_eq_mul]

end Q3

/-! ## Q4: rail relation -/

section Q4

/-- Q4, general: `Ω` any type (finiteness not used), values in any linear ordered field,
the relation needed only at the point `x`. -/
theorem Q4 {Ω K : Type*} [LinearOrderedField K] (φ : Ω → K) (α β : Ω → Ω) (x : Ω)
    (h : φ x = (φ (α x) + φ (β x)) / 2) (hx : ∀ y : Ω, φ y ≤ φ x) :
    φ (α x) = φ x ∧ φ (β x) = φ x := by
  have h1 := hx (α x)
  have h2 := hx (β x)
  constructor <;> linarith

/-- Q4: the set of maximizers is closed under `α` and `β`. -/
theorem Q4_closed {Ω K : Type*} [LinearOrderedField K] (φ : Ω → K) (α β : Ω → Ω)
    (h : ∀ x : Ω, φ x = (φ (α x) + φ (β x)) / 2) (x : Ω) (hx : ∀ y : Ω, φ y ≤ φ x) :
    (∀ y : Ω, φ y ≤ φ (α x)) ∧ (∀ y : Ω, φ y ≤ φ (β x)) := by
  obtain ⟨ha, hb⟩ := Q4 φ α β x (h x) hx
  exact ⟨fun y => ha ▸ hx y, fun y => hb ▸ hx y⟩

/-- Q4 as asked: finite type, real values, "maximum" as `Finset.sup'` over the whole type. -/
theorem Q4_fintype {Ω : Type*} [Fintype Ω] [Nonempty Ω] (φ : Ω → ℝ) (α β : Ω → Ω)
    (h : ∀ x : Ω, φ x = (φ (α x) + φ (β x)) / 2) (x : Ω)
    (hx : φ x = Finset.univ.sup' Finset.univ_nonempty φ) :
    φ (α x) = φ x ∧ φ (β x) = φ x :=
  Q4 φ α β x (h x) (fun y => hx ▸ Finset.le_sup' φ (Finset.mem_univ y))

end Q4

end FourGain

#print axioms FourGain.core_g_zero
#print axioms FourGain.core_g_neg
#print axioms FourGain.core_P_symm
#print axioms FourGain.core_P_self
#print axioms FourGain.core_P_add_left_two
#print axioms FourGain.core_P_add_left
#print axioms FourGain.core_P_add_right
#print axioms FourGain.core_g_zsmul
#print axioms FourGain.Q1a_needs_torsion_free
#print axioms FourGain.mod_g_zero
#print axioms FourGain.mod_B_symm
#print axioms FourGain.mod_B_self
#print axioms FourGain.mod_B_add_left
#print axioms FourGain.mod_B_add_right
#print axioms FourGain.mod_g_zsmul
#print axioms FourGain.Q1a
#print axioms FourGain.Q1b
#print axioms FourGain.Q1c
#print axioms FourGain.Q1d
#print axioms FourGain.Q1d_right
#print axioms FourGain.hand_H1
#print axioms FourGain.hand_H2
#print axioms FourGain.hand_Q1d
#print axioms FourGain.Q1e_zsmul
#print axioms FourGain.Q2a
#print axioms FourGain.Q2_TT
#print axioms FourGain.Q2b
#print axioms FourGain.Q2b_hand
#print axioms FourGain.Q2_f_zero
#print axioms FourGain.Q2_inv
#print axioms FourGain.Q2b'
#print axioms FourGain.Q2_real
#print axioms FourGain.Q2_real'
#print axioms FourGain.Q2b_false_from_Q_alone
#print axioms FourGain.Q3
#print axioms FourGain.Q3_real
#print axioms FourGain.Q4
#print axioms FourGain.Q4_closed
#print axioms FourGain.Q4_fintype
#print axioms FourGain.Q1_main
