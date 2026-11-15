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


namespace PosProd
open ProductEvents

/-- CONTROL refuted: witness n = 1. -/
theorem control : ¬ ∀ n : ℕ, n ^ 2 ≥ 2 * n := fun h => absurd (h 1) (by norm_num)

/-- a second-difference-zero sequence on ℤ that is bounded below is constant -/
lemma affine_const (P : ℤ → ℝ) (h : ∀ x, P (x+1) + P (x-1) = 2 * P x)
    (hb : BddBelow (Set.range P)) : ∀ x, P x = P 0 := by
  have hD : ∀ x, P (x+1) - P x = P 1 - P 0 := by
    intro x
    induction x using Int.induction_on with
    | hz => simp
    | hp i ih => have := h (i+1); simp at this; linarith
    | hn i ih => have := h (-i); simp at this ih; ring_nf at this ih ⊢; linarith
  have hlin : ∀ x : ℤ, P x = P 0 + x * (P 1 - P 0) := by
    intro x
    induction x using Int.induction_on with
    | hz => simp
    | hp i ih => have := hD i; push_cast at ih ⊢; linarith
    | hn i ih => have := hD (-(i:ℤ)-1); simp at this; push_cast at ih ⊢; ring_nf at this ih ⊢; linarith
  obtain ⟨b, hb⟩ := hb
  have hge : ∀ x : ℤ, b ≤ P 0 + x * (P 1 - P 0) := fun x => hlin x ▸ hb ⟨x, rfl⟩
  have hd : P 1 - P 0 = 0 := by
    by_contra hne
    obtain ⟨n, hn⟩ := exists_nat_gt ((P 0 - b) / |P 1 - P 0|)
    have hpos : 0 < |P 1 - P 0| := abs_pos.mpr hne
    rw [div_lt_iff hpos] at hn
    have h1 := hge n; have h2 := hge (-n); push_cast at h1 h2
    rcases le_or_lt 0 (P 1 - P 0) with h | h
    · rw [abs_of_nonneg h] at hn; nlinarith
    · rw [abs_of_neg h] at hn; nlinarith
  intro x; rw [hlin x, hd]; ring

/-- a bounded two-sided solution of (α,β) ↦ (α+β, α) vanishes -/
lemma fib_zero (α β : ℤ → ℝ) (B : ℝ) (hα : ∀ x, |α x| ≤ B) (hβ : ∀ x, |β x| ≤ B)
    (h1 : ∀ x, α (x+1) = α x + β x) (h2 : ∀ x, β (x+1) = α x) :
    ∀ x, α x = 0 ∧ β x = 0 := by
  set φ : ℝ := (1 + Real.sqrt 5) / 2
  have s5 : Real.sqrt 5 ^ 2 = 5 := Real.sq_sqrt (by norm_num)
  have s5g : 1 < Real.sqrt 5 := by
    rw [show (1:ℝ) = Real.sqrt 1 by simp]; exact Real.sqrt_lt_sqrt (by norm_num) (by norm_num)
  have hφ : φ ^ 2 = φ + 1 := by simp only [φ]; ring_nf; rw [s5]; ring
  have hφ1 : 1 < φ := by simp only [φ]; linarith
  have unb : ∀ (c C : ℝ), 0 < c → (∀ n : ℕ, φ ^ n * c ≤ C) → False := by
    intro c C hc hn
    obtain ⟨n, hn'⟩ := pow_unbounded_of_one_lt (C / c) hφ1
    have := hn n; rw [div_lt_iff hc] at hn'; linarith
  let s : ℤ → ℝ := fun x => α x + (φ - 1) * β x
  let t : ℤ → ℝ := fun x => α x + (-φ) * β x
  have hs : ∀ x, s (x+1) = φ * s x := by
    intro x; simp only [s, h1, h2]; linear_combination (-(β x)) * hφ
  have ht : ∀ x, t (x-1) = -φ * t x := by
    intro x
    have a := h1 (x-1); have b := h2 (x-1); simp at a b
    simp only [t, a, b]; linear_combination (-α (x-1)) * hφ
  have hsn : ∀ x (n : ℕ), s (x + n) = φ ^ n * s x := by
    intro x n; induction n with
    | zero => simp
    | succ k ih => push_cast; rw [← add_assoc, hs, ih]; ring
  have htn : ∀ x (n : ℕ), t (x - n) = (-φ) ^ n * t x := by
    intro x n; induction n with
    | zero => simp
    | succ k ih => push_cast; rw [show x - (k + 1 : ℤ) = x - k - 1 by ring, ht, ih]; ring
  have bs : ∀ x, |s x| ≤ B + |φ - 1| * B := by
    intro x
    have e : |s x| ≤ |α x| + |φ - 1| * |β x| := by
      simp only [s]; rw [← abs_mul]; exact abs_add _ _
    exact e.trans (add_le_add (hα x) (mul_le_mul_of_nonneg_left (hβ x) (abs_nonneg _)))
  have bt : ∀ x, |t x| ≤ B + |-φ| * B := by
    intro x
    have e : |t x| ≤ |α x| + |-φ| * |β x| := by
      simp only [t]; rw [← abs_mul]; exact abs_add _ _
    exact e.trans (add_le_add (hα x) (mul_le_mul_of_nonneg_left (hβ x) (abs_nonneg _)))
  have s0 : ∀ x, s x = 0 := by
    intro x; by_contra hne
    exact unb |s x| _ (abs_pos.mpr hne) fun n => by
      have := bs (x + n); rw [hsn, abs_mul, abs_pow, abs_of_pos (by linarith : (0:ℝ) < φ)] at this
      exact this
  have t0 : ∀ x, t x = 0 := by
    intro x; by_contra hne
    exact unb |t x| _ (abs_pos.mpr hne) fun n => by
      have := bt (x - n); rw [htn, abs_mul, abs_pow, abs_neg, abs_of_pos (by linarith : (0:ℝ) < φ)] at this
      exact this
  intro x
  have a := s0 x; have b := t0 x; simp only [s, t] at a b
  have hb : β x = 0 := by
    have : (2 * φ - 1) * β x = 0 := by linear_combination a - b
    rcases mul_eq_zero.mp this with h | h
    · simp only [φ] at h; linarith
    · exact h
  exact ⟨by rw [hb] at a; linarith, hb⟩

/-- Theorem 5.32(ii), line form (ℤ sites).  FR x, FL x are F_{(x,R)}, F_{(x,L)}. -/
theorem part_ii (FR FL : ℤ → ℕ × ℕ → ℝ)
    (hz : ∀ x, FR x (0,0) = 0 ∧ FL x (0,0) = 0)
    (hE : ∀ x U V, FR (x+1) (U+V) + FL (x-1) (U+V.swap) = 2 * FR x U + 2 * FL x V)
    (hb : ∀ m, BddBelow (Set.range fun x => FR x m) ∧ BddBelow (Set.range fun x => FL x m)) :
    (∀ x m, FR x m = FR 0 m ∧ FL x m = FR 0 m) ∧
    ∀ p q : ℕ, FR 0 (p, q) = FR 0 (1, 1) / 2 * ((p : ℝ) + (q : ℝ))
      + (FR 0 (1, 0) - FR 0 (1, 1) / 2) * ((((p : ℤ) - (q : ℤ) : ℤ) : ℝ)) ^ 2 := by
  have same : ∀ x m, FR x m = FR 0 m ∧ FL x m = FR 0 m := by
    intro x0 m
    have e1 : ∀ x, FR (x+1) m + FL (x-1) m = 2 * FR x m := fun x => by
      have := hE x m (0,0); have h0 : FL x 0 = 0 := (hz x).2; simpa [h0] using this
    have e3 : ∀ x, FR (x+1) m + FL (x-1) m.swap = 2 * FL x m := fun x => by
      have := hE x (0,0) m; have h0 : FR x 0 = 0 := (hz x).1; simpa [h0] using this
    have e4 : ∀ x, FR (x+1) m.swap + FL (x-1) m = 2 * FL x m.swap := fun x => by
      have := hE x (0,0) m.swap; have h0 : FR x 0 = 0 := (hz x).1; simpa [h0] using this
    have e2' : ∀ x, FR (x+1) m.swap + FL (x-1) m.swap = 2 * FR x m.swap := fun x => by
      have := hE x m.swap (0,0); have h0 : FL x 0 = 0 := (hz x).2; simpa [h0] using this
    let P : ℤ → ℝ := fun x => (FR x m + FR x m.swap) / 2
    have hQ : ∀ x, (FL x m + FL x m.swap) / 2 = P x := fun x => by
      simp only [P]; linarith [e1 x, e2' x, e3 x, e4 x]
    have hP : ∀ x, P (x+1) + P (x-1) = 2 * P x := fun x => by
      have := hQ (x-1); simp only [P] at this ⊢; linarith [e1 x, e2' x]
    obtain ⟨⟨a1, ha1⟩, ⟨b1, hb1⟩⟩ := hb m
    obtain ⟨⟨a2, ha2⟩, ⟨b2, hb2⟩⟩ := hb m.swap
    have A1 : ∀ x, a1 ≤ FR x m := fun x => ha1 ⟨x, rfl⟩
    have A2 : ∀ x, a2 ≤ FR x m.swap := fun x => ha2 ⟨x, rfl⟩
    have B1 : ∀ x, b1 ≤ FL x m := fun x => hb1 ⟨x, rfl⟩
    have B2 : ∀ x, b2 ≤ FL x m.swap := fun x => hb2 ⟨x, rfl⟩
    have hPc := affine_const P hP ⟨(a1 + a2)/2, by
      rintro _ ⟨x, rfl⟩; simp only [P]; linarith [A1 x, A2 x]⟩
    let α : ℤ → ℝ := fun x => (FR x m - FR x m.swap) / 2
    let β : ℤ → ℝ := fun x => (FL x m - FL x m.swap) / 2
    have hPx : ∀ x, FR x m + FR x m.swap = 2 * P 0 := fun x => by
      have := hPc x; simp only [P] at this ⊢; linarith
    have hQx : ∀ x, FL x m + FL x m.swap = 2 * P 0 := fun x => by
      have := hQ x; rw [hPc x] at this; linarith
    set Bd := |a1| + |a2| + |b1| + |b2| + 2 * |P 0|
    have hα : ∀ x, |α x| ≤ Bd := fun x => by
      simp only [α]; rw [abs_le]
      constructor <;> linarith [A1 x, A2 x, hPx x, le_abs_self a1, neg_abs_le a1, le_abs_self a2,
        neg_abs_le a2, abs_nonneg b1, abs_nonneg b2, le_abs_self (P 0), neg_abs_le (P 0)]
    have hβ : ∀ x, |β x| ≤ Bd := fun x => by
      simp only [β]; rw [abs_le]
      constructor <;> linarith [B1 x, B2 x, hQx x, le_abs_self b1, neg_abs_le b1, le_abs_self b2,
        neg_abs_le b2, abs_nonneg a1, abs_nonneg a2, le_abs_self (P 0), neg_abs_le (P 0)]
    have r1 : ∀ x, α (x+1) + β (x-1) = 2 * α x := fun x => by
      simp only [α, β]; linarith [e1 x, e2' x]
    have r2 : ∀ x, α (x+1) - β (x-1) = 2 * β x := fun x => by
      simp only [α, β]; linarith [e3 x, e4 x]
    have f1 : ∀ x, α (x+1) = α x + β x := fun x => by linarith [r1 x, r2 x]
    have f2 : ∀ x, β (x+1) = α x := fun x => by
      have a := r1 (x+1); have b := r2 (x+1); simp at a b; linarith [f1 x]
    have z := fib_zero α β Bd hα hβ f1 f2
    have z0 := z 0; have zx := z x0
    simp only [α, β] at z0 zx
    constructor <;> linarith [hPx x0, hQx x0, hPx 0]
  refine ⟨same, ?_⟩
  apply eq_of_swap_parallelogram two_ne_zero (FR 0) (hz 0).1
  intro U V
  have := hE 0 U V
  simp only [zero_add, zero_sub] at this
  rw [(same 1 _).1, (same (-1) _).2, (same 0 V).2] at this
  exact this

/-- Ring form: sites ℤ with period N ≠ 0 (ZMod N lifted); boundedness is automatic. -/
theorem part_ii_ring (N : ℤ) (hN : 0 < N) (FR FL : ℤ → ℕ × ℕ → ℝ)
    (hper : ∀ x m, FR (x+N) m = FR x m ∧ FL (x+N) m = FL x m)
    (hz : ∀ x, FR x (0,0) = 0 ∧ FL x (0,0) = 0)
    (hE : ∀ x U V, FR (x+1) (U+V) + FL (x-1) (U+V.swap) = 2 * FR x U + 2 * FL x V) :
    (∀ x m, FR x m = FR 0 m ∧ FL x m = FR 0 m) ∧
    ∀ p q : ℕ, FR 0 (p, q) = FR 0 (1, 1) / 2 * ((p : ℝ) + (q : ℝ))
      + (FR 0 (1, 0) - FR 0 (1, 1) / 2) * ((((p : ℤ) - (q : ℤ) : ℤ) : ℝ)) ^ 2 := by
  have bdd : ∀ f : ℤ → ℝ, Function.Periodic f N → BddBelow (Set.range f) := by
    intro f hf
    apply ((Set.finite_Ico (0:ℤ) N).image f).bddBelow.mono
    rintro _ ⟨x, rfl⟩
    obtain ⟨y, hy, e⟩ := hf.exists_mem_Ico₀ hN x
    exact ⟨y, hy, e.symm⟩
  exact part_ii FR FL hz hE fun m =>
    ⟨bdd _ fun x => (hper x m).1, bdd _ fun x => (hper x m).2⟩

/-- Theorem 5.32(iv), after reindexing: Ext puts U_x+V_x at (x+1,R), U_x+JV_x at (x-1,L). -/
theorem part_iv {ι : Type*} (a c : ℝ) (F : ℕ × ℕ → ℝ)
    (hF : ∀ p q : ℕ, F (p, q) = a * ((p : ℝ) + (q : ℝ))
      + c * ((((p : ℤ) - (q : ℤ) : ℤ) : ℝ)) ^ 2)
    (s : Finset ι) (U V : ι → ℕ × ℕ) :
    ∑ x in s, (F (U x + V x) + F (U x + (V x).swap)) = 2 * ∑ x in s, (F (U x) + F (V x)) := by
  rw [Finset.mul_sum]
  refine Finset.sum_congr rfl fun x _ => ?_
  rw [((swap_parallelogram_of_form a c F hF).2 (U x) (V x))]; ring

end PosProd

#print axioms PosProd.control
#print axioms PosProd.part_ii
#print axioms PosProd.part_ii_ring
#print axioms PosProd.part_iv
