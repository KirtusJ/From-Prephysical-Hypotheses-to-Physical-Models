import Mathlib

/-! Lemma 0, Lemma R, steps 1 and 5 of Proposition P, ring factor.
Rails and steps are `Bool`: `true` = R (right), `false` = L (left).
The rail after a step is R iff the step is right, so the rail after step `s` is `s`. -/

namespace PrepReduction

/-- normalise an identity in a commutative group by passing to `Additive` and using `abel`. -/
macro "comm_group_tac" : tactic => `(tactic| (
  apply Additive.ofMul.injective
  simp only [ofMul_mul, ofMul_inv, ofMul_zpow, ofMul_one, ofMul_div, ofMul_pow]
  try simp only [smul_add, add_smul, smul_neg, neg_smul, smul_sub, sub_smul, one_smul, mul_smul, smul_zero]
  try push_cast
  abel))

variable {G : Type*} [CommGroup G]

/-- gain of one step from rail `r`: a (R,right), b (R,left), c (L,right), d (L,left). -/
def stepGain (a b c d : G) : Bool → Bool → G
  | true,  true  => a
  | true,  false => b
  | false, true  => c
  | false, false => d

/-- gain of a walk started on rail `r`. -/
def gainFrom (a b c d : G) : Bool → List Bool → G
  | _, []      => 1
  | r, s :: w  => stepGain a b c d r s * gainFrom a b c d s w

/-- number of L→R changes of a walk started on rail `r`. -/
def nLR : Bool → List Bool → ℕ
  | _, []     => 0
  | r, s :: w => (if r = false ∧ s = true then 1 else 0) + nLR s w

/-- final rail. -/
def lastRail : Bool → List Bool → Bool
  | r, []     => r
  | _, s :: w => lastRail s w

/-- rail correction: 1 on R, b d⁻¹ on L. -/
def E (b d : G) (r : Bool) : G := if r then 1 else b * d⁻¹

/-- Lemma 0, general start rail (induction form). -/
theorem lemma0_gen (a b c d : G) (r : Bool) (w : List Bool) :
    E b d r * gainFrom a b c d r w =
      a ^ (w.count true : ℤ) * d ^ (w.count false : ℤ) *
        (a * d * (b * c)⁻¹) ^ (-(nLR r w : ℤ)) * E b d (lastRail r w) := by
  induction w generalizing r with
  | nil => simp [gainFrom, nLR, lastRail]
  | cons s w ih =>
    have key := eq_inv_mul_of_mul_eq (ih s)
    simp only [gainFrom, nLR, lastRail]
    rw [key]
    generalize E b d (lastRail s w) = e
    cases r <;> cases s <;>
      simp only [stepGain, E, List.count_cons, beq_self_eq_true, Bool.true_beq, Bool.false_beq,
        if_true, if_false, Bool.false_eq_true, and_true, and_false, true_and, false_and,
        Nat.cast_add, Nat.cast_one, Nat.cast_zero, add_zero, zero_add, inv_one, one_mul,
        reduceCtorEq, Bool.not_false, Bool.not_true, ite_true, ite_false] <;>
      comm_group_tac

/-! ## (F1) Lemma 0 from rail R -/

/-- the final rail is the last step, or R for the empty walk. -/
theorem lastRail_eq (r : Bool) (w : List Bool) : lastRail r w = w.getLast?.getD r := by
  induction w generalizing r with
  | nil => rfl
  | cons s w ih =>
    rw [lastRail, ih]
    cases w with
    | nil => rfl
    | cons t u =>
      show (t :: u).getLast?.getD s = (s :: t :: u).getLast?.getD r
      rw [List.getLast?_cons_cons]
      cases h : (t :: u).getLast? with
      | none => simp at h
      | some v => rfl

/-- Lemma 0, walk ends on R (last step right, or empty walk). -/
theorem lemma0_R (a b c d : G) (w : List Bool) (h : lastRail true w = true) :
    gainFrom a b c d true w =
      a ^ (w.count true : ℤ) * d ^ (w.count false : ℤ) * (a * d * (b * c)⁻¹) ^ (-(nLR true w : ℤ)) := by
  have := lemma0_gen a b c d true w
  simpa [E, h] using this

/-- Lemma 0, walk ends on L (last step left). -/
theorem lemma0_L (a b c d : G) (w : List Bool) (h : lastRail true w = false) :
    gainFrom a b c d true w =
      a ^ (w.count true : ℤ) * d ^ ((w.count false : ℤ) - 1) * b *
        (a * d * (b * c)⁻¹) ^ (-(nLR true w : ℤ)) := by
  have := lemma0_gen a b c d true w
  simp only [E, h, if_true, Bool.false_eq_true, if_false, one_mul] at this
  rw [this]
  comm_group_tac

/-! ## (F2) Lemma R -/

theorem lemmaR_R (a b c d : G) (w : List Bool) (h : lastRail true w = true) :
    gainFrom a b c d true w =
      a ^ ((w.count true : ℤ) - w.count false) * (b * c) ^ (w.count false : ℤ) *
        gainFrom 1 1 1 (a * d * (b * c)⁻¹) true w := by
  rw [lemma0_R a b c d w h, lemma0_R 1 1 1 _ w h]
  comm_group_tac

theorem lemmaR_L (a b c d : G) (w : List Bool) (h : lastRail true w = false) :
    gainFrom a b c d true w =
      a ^ ((w.count true : ℤ) - w.count false) * (b * c) ^ (w.count false : ℤ) *
        (b * (a * d * (b * c)⁻¹) * d⁻¹) * gainFrom 1 1 1 (a * d * (b * c)⁻¹) true w := by
  rw [lemma0_L a b c d w h, lemma0_L 1 1 1 _ w h]
  comm_group_tac

/-! ## Step 1 of Proposition P: every element of ⟨a, e, δ⟩ has a coset representative
a^x e^μ with x, μ natural, provided a and e have finite order (no finiteness of G needed). -/

theorem closure_three_exp (a e δ κ : G) (hκ : κ ∈ Subgroup.closure ({a, e, δ} : Set G)) :
    ∃ i j k : ℤ, κ = a ^ i * e ^ j * δ ^ k := by
  refine Subgroup.closure_induction (p := fun κ => ∃ i j k : ℤ, κ = a ^ i * e ^ j * δ ^ k) hκ
    ?_ ?_ ?_ ?_
  · intro x hx
    rcases hx with rfl | rfl | rfl
    · exact ⟨1, 0, 0, by simp⟩
    · exact ⟨0, 1, 0, by simp⟩
    · exact ⟨0, 0, 1, by simp⟩
  · exact ⟨0, 0, 0, by simp⟩
  · rintro x y ⟨i, j, k, rfl⟩ ⟨i', j', k', rfl⟩
    exact ⟨i + i', j + j', k + k', by comm_group_tac⟩
  · rintro x ⟨i, j, k, rfl⟩
    exact ⟨-i, -j, -k, by comm_group_tac⟩

theorem exists_nat_pow_eq_zpow (a : G) (ha : IsOfFinOrder a) (i : ℤ) : ∃ x : ℕ, a ^ x = a ^ i := by
  have hpos : (0 : ℤ) < orderOf a := by exact_mod_cast ha.orderOf_pos
  refine ⟨(i % (orderOf a : ℤ)).toNat, ?_⟩
  rw [← zpow_natCast, Int.toNat_of_nonneg (Int.emod_nonneg _ hpos.ne'), zpow_mod_orderOf]

theorem step1 (a e δ κ : G) (ha : IsOfFinOrder a) (he : IsOfFinOrder e)
    (hκ : κ ∈ Subgroup.closure ({a, e, δ} : Set G)) :
    ∃ x μ : ℕ, κ⁻¹ * (a ^ x * e ^ μ) ∈ Subgroup.zpowers δ := by
  obtain ⟨i, j, k, rfl⟩ := closure_three_exp a e δ κ hκ
  obtain ⟨x, hx⟩ := exists_nat_pow_eq_zpow a ha i
  obtain ⟨μ, hμ⟩ := exists_nat_pow_eq_zpow e he j
  refine ⟨x, μ, -k, ?_⟩
  simp only [hx, hμ]
  comm_group_tac

/-! ## (F3) Step 5 (any monoid, any element; orderOf = 0 makes ≡ equality) -/

theorem step5_pow {M : Type*} [Monoid M] (x : M) {n m : ℕ} (h : n ≡ m [MOD orderOf x]) :
    x ^ n = x ^ m := by
  rw [← pow_mod_orderOf x n, h, pow_mod_orderOf]

theorem step5 (b c : G) {lam1 k mu0 : ℕ} (h : lam1 + k ≡ mu0 [MOD orderOf (b * c)]) :
    (b * c) ^ (lam1 + k) = (b * c) ^ mu0 :=
  step5_pow (b * c) h

theorem step5_kappa (a b c : G) (x : ℤ) {lam1 k mu0 : ℕ}
    (h : lam1 + k ≡ mu0 [MOD orderOf (b * c)]) :
    a ^ x * (b * c) ^ (lam1 + k) = a ^ x * (b * c) ^ mu0 := by
  rw [step5 b c h]

/-! ## (F4) Ring factor -/

theorem ring_winding (a d : G) (ρ lam M j : ℤ) :
    a ^ (ρ + M * j) * d ^ (lam - M * j) = a ^ ρ * d ^ lam * (a / d) ^ (M * j) := by
  comm_group_tac

theorem ring_ratio (a b c d : G) : a * (a * d * (b * c)⁻¹) / d = a ^ 2 / (b * c) := by
  comm_group_tac

theorem ring_fixed (a b c d : G) (M : ℤ) (hB : (b * c / a ^ 2) ^ M = 1) :
    (a / d) ^ M = (a * d * (b * c)⁻¹) ^ (-M) := by
  have e : a / d = (b * c / a ^ 2)⁻¹ * (a * d * (b * c)⁻¹)⁻¹ := by
    rw [pow_two]; comm_group_tac
  rw [e, mul_zpow, inv_zpow', inv_zpow', zpow_neg, hB, inv_one, one_mul]

/-- control: a = d = 1, b = c = h; walk L,R from (0,R) has gain h^2, and δ = h^(-2). -/
example (h : G) : gainFrom 1 h h 1 true [false, true] = h ^ 2 ∧ (1 * 1 * (h * h)⁻¹ : G) = h ^ (-2 : ℤ) := by
  constructor
  · simp [gainFrom, stepGain, pow_two]
  · comm_group_tac

end PrepReduction

#print axioms PrepReduction.lemma0_gen
#print axioms PrepReduction.lastRail_eq
#print axioms PrepReduction.lemma0_R
#print axioms PrepReduction.lemma0_L
#print axioms PrepReduction.lemmaR_R
#print axioms PrepReduction.lemmaR_L
#print axioms PrepReduction.step1
#print axioms PrepReduction.step5_pow
#print axioms PrepReduction.step5
#print axioms PrepReduction.step5_kappa
#print axioms PrepReduction.ring_winding
#print axioms PrepReduction.ring_ratio
#print axioms PrepReduction.ring_fixed
