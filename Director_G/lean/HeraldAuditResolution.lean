import Std

/-! Scalar arithmetic for the five-cell return test and the alternative
random-resolution test. In the five-cell test the three reference masses
are 4/8, 2/8, and 1/8. The two remaining masses sum to 1/8.
The finite-power gap is certified as a polynomial identity over integers,
hence by denominator clearing for rational x = 2^q. Its real extension
uses the same polynomial identity and nonnegativity of a square.

In the alternative test, for defect d = p/t the pass probability is
1 - 3d/4. Under a common
denominator 16mt the m equal pass cells each have mass 4(4t-3p).
The two failure masses are 3p and (4m-1)3p. The random menu gives the
m-cell setting probability 2/m. This file treats rational defects and
compares masses and reported weights. It assumes no quantum dynamics.
-/

namespace HeraldAuditResolution

/-- At x=a/b the normalized reference weights are proportional to
    a², ab, b². Their signed contrast factors exactly. -/
theorem anchor_identity (a b : Int) :
    a*a - 4*(a*b) + 4*(b*b) = (a-2*b)*(a-2*b) := by
  simp +arith [Int.sub_mul, Int.mul_sub, Int.mul_assoc, Int.mul_comm, Int.mul_left_comm]
  simp only [← Int.mul_assoc]
  omega

theorem anchor_gap (a b : Int) :
    0 ≤ a*a - 4*(a*b) + 4*(b*b) ∧
    (a*a - 4*(a*b) + 4*(b*b) = 0 ↔ a = 2*b) := by
  rw [anchor_identity]
  constructor
  · by_cases h : 0 ≤ a-2*b
    · exact Int.mul_nonneg h h
    · exact Int.mul_nonneg_of_nonpos_of_nonpos (by omega) (by omega)
  · constructor
    · intro h
      rcases Int.mul_eq_zero.mp h with h | h <;> omega
    · intro h
      simp [h]

/-- At q=1 the science-pass and science-failure weights sum to the
    low reference weight. The largest reference takes half the total. -/
theorem ordinary_normalization (low pass fail : Nat) (h : pass+fail=low) :
    4*low+2*low+low+pass+fail = 8*low ∧
    2*(4*low) = 4*low+2*low+low+pass+fail := by omega

/-- The maximum power selects the unique largest reference. At the
    minimum power the high and middle references are unavailable, and
    any allowed probability of breaking a tie at low costs +4 per unit. -/
theorem endpoint_scores (total low : Int) (ht : 0 < total) (hl : 0 ≤ low) :
    0 < total - 4*0 + 4*0 ∧ 0 ≤ 0 - 4*0 + 4*low := by omega

/-- Once only ordinary and minimum-selecting modes remain, a half-rate
    at the high anchor forces minimum-mode incidence zero, after clearing
    any common denominator. Monotonicity handles a finite high-rate deficit. -/
theorem residual_minimum (ordinary minimum high : Int)
    (h : 2*high = ordinary) :
    ordinary+minimum-2*high = minimum ∧
    (2*high = ordinary+minimum ↔ minimum = 0) := by omega

/-- Polynomial factor in the upper-tail bound on 2H-1 for x ≥ 2,
    using convexity's lower bound 2/x on the sum of science weights. -/
theorem upper_tail_factor (a b : Int) :
    a*a*a-a*a*b-a*b*b-2*b*b*b = (a-2*b)*(a*a+a*b+b*b) := by
  simp +arith [Int.sub_mul, Int.mul_sub, Int.mul_add, Int.add_mul,
    Int.mul_assoc, Int.mul_comm, Int.mul_left_comm]
  simp only [← Int.mul_assoc]
  omega

/-- The high failure cell crosses all pass cells at exactly this threshold. -/
theorem crossing (m p t : Nat) (hm : 1 ≤ m) (hp : p ≤ t) :
    4*(4*t-3*p) < (4*m-1)*(3*p) ↔ 16*t < (4*m+3)*(3*p) := by
  have h : (4*m-1)*(3*p) + 3*p = 4*m*(3*p) := by
    rw [← Nat.succ_mul]
    congr 1
    omega
  rw [Nat.add_mul]
  omega

/-- At a sufficient resolution, the smaller and larger failures strictly
bracket each pass cell. All nonconstant monotone powers order the three
levels by these masses or by the reverse ordering. -/
theorem bracket (m p t : Nat) (hp : 0 < p) (ht : p ≤ t)
    (hm : 4 ≤ m) (hc : 2*t ≤ m*p) :
    3*p < 4*(4*t-3*p) ∧ 4*(4*t-3*p) < (4*m-1)*(3*p) := by
  refine ⟨by omega, (crossing m p t (by omega) ht).2 ?_⟩
  simp only [Nat.add_mul]
  have h : 4*m*(3*p) = 12*(m*p) := by
    simp +arith [Nat.mul_assoc, Nat.mul_comm, Nat.mul_left_comm]
  omega

/-- The least dyadic with k ≥ 2 and 2t ≤ 2^k p satisfies 2^k p ≤ 4t.
The previous dyadic fails this sufficient condition whenever k > 2. -/
theorem dyadic_cover (p : Nat) (hp : 0 < p) :
    ∀ t : Nat, p ≤ t → ∃ k : Nat, 2 ≤ k ∧
      2*t ≤ 2^k*p ∧ 2^k*p ≤ 4*t ∧ (k = 2 ∨ 2^(k-1)*p < 2*t) := by
  intro t
  induction t with
  | zero => intro h; omega
  | succ t ih =>
    intro ht
    by_cases hprev : p ≤ t
    · obtain ⟨k,hk,hlo,hhi,hmin⟩ := ih hprev
      by_cases hstay : 2*(t+1) ≤ 2^k*p
      · exact ⟨k,hk,hstay,by omega,hmin.imp id (by omega)⟩
      · have hdouble : 2^(k+1)*p = 2*(2^k*p) := by
          rw [Nat.pow_succ]
          ac_rfl
        refine ⟨k+1,by omega,by rw [hdouble]; omega,by rw [hdouble]; omega,
          Or.inr ?_⟩
        simpa using (Nat.lt_of_not_ge hstay)
    · exact ⟨2,by decide,by simp; omega,by simp; omega,Or.inl rfl⟩

/-- If failure has at least the reported weight g of one pass cell, its
fraction of total reported weight is at least 1/(m+1). -/
theorem failure_floor (m f g : Nat) (h : g ≤ f) :
    m*g + f ≤ (m+1)*f := by
  rw [Nat.add_mul]
  have := Nat.mul_le_mul_left m h
  omega

/-- For the selected resolution, (2/m)/(m+1) ≥ (p/t)^2/10 after
clearing positive denominators. -/
theorem incident_floor (m p t : Nat) (h : m*p ≤ 4*t) (hp : p ≤ t) :
    (m*p)*((m+1)*p) ≤ 20*(t*t) := by
  have hnext : (m+1)*p ≤ 5*t := by rw [Nat.add_mul]; omega
  calc
    _ ≤ (4*t)*(5*t) := Nat.mul_le_mul h hnext
    _ = _ := by simp +arith [Nat.mul_assoc, Nat.mul_comm, Nat.mul_left_comm]

end HeraldAuditResolution
