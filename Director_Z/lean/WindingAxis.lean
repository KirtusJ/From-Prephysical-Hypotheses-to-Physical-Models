/-
WindingAxis.lean  (Lean 4.12.0, Mathlib v4.12.0)
Axis-restricted parallelogram equation on ℤ and ℤ × ℤ, values in an abelian group M
without 2-torsion (hypothesis `h2`, used only where stated).
Control: (a - b)^2 + (a + b)^2 = 2*a^2 + 2*b^2 over ℤ.
-/
import Mathlib

namespace WindingAxis

/-- Control. -/
example (a b : ℤ) : (a - b)^2 + (a + b)^2 = 2*a^2 + 2*b^2 := by ring

variable {M : Type*} [AddCommGroup M]

/-- Core lemma (no torsion hypothesis): a ℤ-sequence with vanishing second difference
that vanishes at 0 and 1 vanishes everywhere. -/
theorem second_diff_zero (d : ℤ → M)
    (hd : ∀ n : ℤ, d (n + 1) + d (n - 1) = (2 : ℤ) • d n)
    (h0 : d 0 = 0) (h1 : d 1 = 0) : ∀ n : ℤ, d n = 0 := by
  have key : ∀ n : ℤ, d n = 0 ∧ d (n + 1) = 0 := by
    intro n
    induction n using Int.induction_on with
    | hz => exact ⟨h0, by simpa using h1⟩
    | hp i ih =>
      obtain ⟨a, b⟩ := ih
      refine ⟨b, ?_⟩
      have e := hd ((i : ℤ) + 1)
      rw [add_sub_cancel_right, a, b] at e
      simpa using e
    | hn i ih =>
      obtain ⟨a, b⟩ := ih
      have e := hd (-(i : ℤ))
      rw [a, b] at e
      refine ⟨by simpa using e, ?_⟩
      rw [sub_add_cancel]; exact a
  exact fun n => (key n).1

/-- Statement B (affine), general form: only t = 1 is used, no torsion hypothesis. -/
theorem affine_int (h : ℤ → M)
    (hh : ∀ n : ℤ, h (n + 1) + h (n - 1) = (2 : ℤ) • h n) (h0 : h 0 = 0) :
    ∀ n : ℤ, h n = n • h 1 := by
  intro n
  have := second_diff_zero (fun n => h n - n • h 1)
    (by intro n; simp only; rw [show h (n + 1) = (2 : ℤ) • h n - h (n - 1) from
          eq_sub_of_add_eq (hh n)]; module)
    (by simp [h0]) (by simp) n
  exact sub_eq_zero.mp this

/-- Statement B as asked (all t). -/
theorem affine_int' (h : ℤ → M)
    (hh : ∀ n t : ℤ, h (n + t) + h (n - t) = (2 : ℤ) • h n) (h0 : h 0 = 0) :
    ∀ n : ℤ, h n = n • h 1 :=
  affine_int h (fun n => hh n 1) h0

/-- Statement A, part 1: g 0 = 0 (uses s = t = 0 and no 2-torsion). -/
theorem quad_zero (h2 : ∀ x : M, (2 : ℤ) • x = 0 → x = 0) (g : ℤ → M)
    (hg : ∀ s t : ℤ, g (s + t) + g (s - t) = (2 : ℤ) • g s + (2 : ℤ) • g t) :
    g 0 = 0 := by
  apply h2
  have e := hg 0 0
  simp only [add_zero, sub_zero] at e
  have : (2 : ℤ) • g 0 = ((2 : ℤ) • g 0 + (2 : ℤ) • g 0) - (g 0 + g 0) := by module
  rw [this, ← e, sub_self]

/-- Statement A with the hypotheses the proof uses: t = 1 only, plus g 0 = 0. -/
theorem quad_int_of_zero (g : ℤ → M)
    (hg : ∀ s : ℤ, g (s + 1) + g (s - 1) = (2 : ℤ) • g s + (2 : ℤ) • g 1)
    (g0 : g 0 = 0) : ∀ n : ℤ, g n = (n ^ 2) • g 1 := by
  intro n
  have := second_diff_zero (fun n => g n - (n ^ 2) • g 1)
    (by intro n; simp only; rw [show g (n + 1) = (2 : ℤ) • g n + (2 : ℤ) • g 1 - g (n - 1) from
          eq_sub_of_add_eq (hg n)]; module)
    (by simp [g0]) (by simp) n
  exact sub_eq_zero.mp this

/-- Statement A as asked. -/
theorem quad_int (h2 : ∀ x : M, (2 : ℤ) • x = 0 → x = 0) (g : ℤ → M)
    (hg : ∀ s t : ℤ, g (s + t) + g (s - t) = (2 : ℤ) • g s + (2 : ℤ) • g t) :
    g 0 = 0 ∧ ∀ n : ℤ, g n = (n ^ 2) • g 1 :=
  ⟨quad_zero h2 g hg, quad_int_of_zero g (fun s => hg s 1) (quad_zero h2 g hg)⟩

/-- Statement C with the hypotheses the proof uses: t = 1 only, the first equation for all
(s0, s1), the second only on the lines s0 = 0 and s0 = 1, and γ 0 0 = 0. No torsion hypothesis. -/
theorem axis_quad_of_zero (γ : ℤ → ℤ → M)
    (hx : ∀ s0 s1 : ℤ, γ (s0 + 1) s1 + γ (s0 - 1) s1 = (2 : ℤ) • γ s0 s1 + (2 : ℤ) • γ 1 0)
    (hy0 : ∀ s1 : ℤ, γ 0 (s1 + 1) + γ 0 (s1 - 1) = (2 : ℤ) • γ 0 s1 + (2 : ℤ) • γ 0 1)
    (hy1 : ∀ s1 : ℤ, γ 1 (s1 + 1) + γ 1 (s1 - 1) = (2 : ℤ) • γ 1 s1 + (2 : ℤ) • γ 0 1)
    (z : γ 0 0 = 0) (x y : ℤ) :
    γ x y = (x ^ 2) • γ 1 0 + (y ^ 2) • γ 0 1 + (x * y) • (γ 1 1 - γ 1 0 - γ 0 1) := by
  -- the y-axis
  have ay : ∀ y : ℤ, γ 0 y = (y ^ 2) • γ 0 1 := quad_int_of_zero (fun y => γ 0 y) hy0 z
  -- the line x = 1
  have l1 : ∀ y : ℤ, γ 1 y = γ 1 0 + (y ^ 2) • γ 0 1 + y • (γ 1 1 - γ 1 0 - γ 0 1) := by
    intro y
    have := second_diff_zero
      (fun y => γ 1 y - (γ 1 0 + (y ^ 2) • γ 0 1 + y • (γ 1 1 - γ 1 0 - γ 0 1)))
      (by intro n; simp only; rw [show γ 1 (n + 1) = (2 : ℤ) • γ 1 n + (2 : ℤ) • γ 0 1 - γ 1 (n - 1)
            from eq_sub_of_add_eq (hy1 n)]; module)
      (by simp) (by simp only; module) y
    exact sub_eq_zero.mp this
  -- every horizontal line
  have := second_diff_zero
    (fun x => γ x y - ((x ^ 2) • γ 1 0 + γ 0 y + x • (γ 1 y - γ 1 0 - γ 0 y)))
    (by intro n; simp only; rw [show γ (n + 1) y = (2 : ℤ) • γ n y + (2 : ℤ) • γ 1 0 - γ (n - 1) y
          from eq_sub_of_add_eq (hx n y)]; module)
    (by simp) (by simp only; module) x
  rw [sub_eq_zero.mp this, l1 y, ay y]
  module

/-- Statement C as asked (γ : ℤ → ℤ → M, M an abelian group without 2-torsion). -/
theorem axis_quad (h2 : ∀ x : M, (2 : ℤ) • x = 0 → x = 0) (γ : ℤ → ℤ → M)
    (hx : ∀ s0 s1 t : ℤ, γ (s0 + t) s1 + γ (s0 - t) s1 = (2 : ℤ) • γ s0 s1 + (2 : ℤ) • γ t 0)
    (hy : ∀ s0 s1 t : ℤ, γ s0 (s1 + t) + γ s0 (s1 - t) = (2 : ℤ) • γ s0 s1 + (2 : ℤ) • γ 0 t)
    (x y : ℤ) :
    γ x y = (x ^ 2) • γ 1 0 + (y ^ 2) • γ 0 1 + (x * y) • (γ 1 1 - γ 1 0 - γ 0 1) :=
  axis_quad_of_zero γ (fun s0 s1 => hx s0 s1 1) (fun s1 => hy 0 s1 1) (fun s1 => hy 1 s1 1)
    (quad_zero h2 (fun s => γ s 0) (fun s t => hx s 0 t)) x y

/-- Statement C in the ℤ × ℤ form. -/
theorem axis_quad_prod (h2 : ∀ x : M, (2 : ℤ) • x = 0 → x = 0) (γ : ℤ × ℤ → M)
    (hx : ∀ s0 s1 t : ℤ,
      γ (s0 + t, s1) + γ (s0 - t, s1) = (2 : ℤ) • γ (s0, s1) + (2 : ℤ) • γ (t, 0))
    (hy : ∀ s0 s1 t : ℤ,
      γ (s0, s1 + t) + γ (s0, s1 - t) = (2 : ℤ) • γ (s0, s1) + (2 : ℤ) • γ (0, t))
    (x y : ℤ) :
    γ (x, y) = (x ^ 2) • γ (1, 0) + (y ^ 2) • γ (0, 1)
      + (x * y) • (γ (1, 1) - γ (1, 0) - γ (0, 1)) :=
  axis_quad h2 (fun a b => γ (a, b)) hx hy x y

/-- The torsion hypothesis cannot be dropped from A (hence from C as asked):
over ZMod 2 the constant 1 satisfies the equation and g 0 ≠ 0. -/
theorem torsion_needed :
    ∃ g : ℤ → ZMod 2, (∀ s t : ℤ, g (s + t) + g (s - t) = (2 : ℤ) • g s + (2 : ℤ) • g t)
      ∧ g 0 ≠ 0 :=
  ⟨fun _ => 1, fun _ _ => by show (1 : ZMod 2) + 1 = (2 : ℤ) • 1 + (2 : ℤ) • 1; decide, by decide⟩

section D
variable {R : Type*} [CommRing R]

/-- D1 (any commutative ring; only (x, y) = (1, 0) is used; c plays no role). -/
theorem swap_invariant (q0 q1 c : R)
    (h : ∀ x y : ℤ, q0 * (x : R) ^ 2 + q1 * (y : R) ^ 2 + c * x * y
        = q0 * (y : R) ^ 2 + q1 * (x : R) ^ 2 + c * y * x) : q0 = q1 := by
  have e := h 1 0
  simpa using e

/-- D2 (commutative ring where 2c = 0 implies c = 0; only (1,0) and (1,1) are used). -/
theorem rot_invariant (h2 : ∀ r : R, 2 * r = 0 → r = 0) (q0 q1 c : R)
    (h : ∀ x y : ℤ, q0 * (x : R) ^ 2 + q1 * (y : R) ^ 2 + c * x * y
        = q0 * ((-y : ℤ) : R) ^ 2 + q1 * (x : R) ^ 2 + c * ((-y : ℤ) : R) * x) :
    q0 = q1 ∧ c = 0 := by
  have e := h 1 0
  have f := h 1 1
  simp at e f
  refine ⟨e, h2 c ?_⟩
  linear_combination f

/-- D1 over ℝ as asked. -/
theorem swap_invariant_real (q0 q1 c : ℝ)
    (h : ∀ x y : ℤ, q0 * (x : ℝ) ^ 2 + q1 * (y : ℝ) ^ 2 + c * x * y
        = q0 * (y : ℝ) ^ 2 + q1 * (x : ℝ) ^ 2 + c * y * x) : q0 = q1 :=
  swap_invariant q0 q1 c h

/-- D2 over ℝ as asked. -/
theorem rot_invariant_real (q0 q1 c : ℝ)
    (h : ∀ x y : ℤ, q0 * (x : ℝ) ^ 2 + q1 * (y : ℝ) ^ 2 + c * x * y
        = q0 * ((-y : ℤ) : ℝ) ^ 2 + q1 * (x : ℝ) ^ 2 + c * ((-y : ℤ) : ℝ) * x) :
    q0 = q1 ∧ c = 0 :=
  rot_invariant (fun r hr => by linarith) q0 q1 c h

end D

end WindingAxis

#print axioms WindingAxis.second_diff_zero
#print axioms WindingAxis.affine_int'
#print axioms WindingAxis.quad_int
#print axioms WindingAxis.axis_quad_of_zero
#print axioms WindingAxis.axis_quad
#print axioms WindingAxis.torsion_needed
#print axioms WindingAxis.swap_invariant_real
#print axioms WindingAxis.rot_invariant_real
#print axioms WindingAxis.axis_quad_prod
