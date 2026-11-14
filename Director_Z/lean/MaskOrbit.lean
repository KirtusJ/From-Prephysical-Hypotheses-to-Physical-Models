import Mathlib

open Complex ComplexConjugate

/-! L1 -/
theorem L1_roots (N : ℕ) (w : ℂ) (hw : w ^ (N / Nat.gcd N 2) = 1) :
    ∃ ζ : ℂ, ζ ^ N = 1 ∧ (ζ⁻¹) ^ 2 = w := by
  rcases Nat.eq_zero_or_pos N with rfl | hN
  · -- junk case N = 0: M = 0, every w
    by_cases h0 : w = 0
    · exact ⟨0, by simp, by simp [h0]⟩
    · obtain ⟨s, hs⟩ := IsAlgClosed.exists_pow_nat_eq w (by norm_num : 0 < 2)
      exact ⟨s⁻¹, by simp, by simp [hs]⟩
  · have hω := Complex.isPrimitiveRoot_exp N hN.ne'
    set ω := Complex.exp (2 * Real.pi * Complex.I / N)
    have hord : orderOf (ω ^ 2) = N / Nat.gcd N 2 := by
      rw [orderOf_pow' _ (by norm_num), hω.eq_orderOf]
    have hprim : IsPrimitiveRoot (ω ^ 2) (N / Nat.gcd N 2) := by
      rw [← hord]; exact IsPrimitiveRoot.orderOf (ω ^ 2)
    have hMpos : 0 < N / Nat.gcd N 2 :=
      Nat.div_pos (Nat.le_of_dvd hN (Nat.gcd_dvd_left N 2)) (Nat.gcd_pos_of_pos_left 2 hN)
    obtain ⟨k, -, hk⟩ := hprim.eq_pow_of_pow_eq_one hw hMpos
    refine ⟨(ω ^ k)⁻¹, ?_, ?_⟩
    · rw [inv_pow, ← pow_mul, mul_comm, pow_mul, hω.pow_eq_one, one_pow, inv_one]
    · rw [inv_inv, ← hk, ← pow_mul, ← pow_mul, mul_comm]

/-! L2: identities without hypotheses, then the unit-modulus forms. -/
theorem L2_common_det (g a b c d : ℂ) (h : a * d = -(b * c)) :
    (g * a) * (g * d) = -((g * b) * (g * c)) := by
  linear_combination g ^ 2 * h

theorem L2_common_u (g a b c : ℂ) (hg : g ≠ 0) :
    (g * b) * (g * c) / (g * a) ^ 2 = b * c / a ^ 2 := by
  rw [mul_pow, show (g * b) * (g * c) = g ^ 2 * (b * c) by ring, mul_div_mul_left _ _ (pow_ne_zero 2 hg)]

theorem L2_rail_u_general (l a b c : ℂ) :
    (conj l * b) * (l * c) / a ^ 2 = (conj l * l) * (b * c / a ^ 2) := by
  ring

theorem L2_rail_det (l a b c d : ℂ) (hl : Complex.abs l = 1) (h : a * d = -(b * c)) :
    a * d = -((conj l * b) * (l * c)) := by
  have : conj l * l = 1 := by
    rw [mul_comm, Complex.mul_conj, Complex.normSq_eq_abs, hl]; norm_num
  linear_combination h + b * c * this

theorem L2_rail_u (l a b c : ℂ) (hl : Complex.abs l = 1) :
    (conj l * b) * (l * c) / a ^ 2 = b * c / a ^ 2 := by
  have : conj l * l = 1 := by
    rw [mul_comm, Complex.mul_conj, Complex.normSq_eq_abs, hl]; norm_num
  rw [L2_rail_u_general, this, one_mul]

theorem L2_site_det (z a b c d : ℂ) (h : a * d = -(b * c)) :
    (z * a) * (conj z * d) = -((conj z * b) * (z * c)) := by
  linear_combination z * conj z * h

theorem L2_site_u_general (z a b c : ℂ) :
    (conj z * b) * (z * c) / (z * a) ^ 2 = (conj z * z / z ^ 2) * (b * c / a ^ 2) := by
  rw [mul_pow, div_mul_div_comm]; ring

theorem L2_site_u (z a b c : ℂ) (hz : Complex.abs z = 1) :
    (conj z * b) * (z * c) / (z * a) ^ 2 = (z⁻¹) ^ 2 * (b * c / a ^ 2) := by
  have : conj z * z = 1 := by
    rw [mul_comm, Complex.mul_conj, Complex.normSq_eq_abs, hz]; norm_num
  rw [L2_site_u_general, this, one_div, inv_pow]

theorem L2_conj_det (a b c d : ℂ) (h : a * d = -(b * c)) :
    conj a * conj d = -(conj b * conj c) := by
  rw [← map_mul, ← map_mul, h, map_neg]

theorem L2_conj_u (a b c : ℂ) :
    conj b * conj c / conj a ^ 2 = conj (b * c / a ^ 2) := by
  simp [map_div₀, map_mul, map_pow]

/-! L3: converse. Only a ≠ 0, c ≠ 0, |a| = |a'|, |c| = |c'| are used. -/
theorem L3_converse (a b c d a' b' c' d' : ℂ)
    (ha : a ≠ 0) (hc : c ≠ 0)
    (haa : Complex.abs a' = Complex.abs a) (hcc : Complex.abs c' = Complex.abs c)
    (h : a * d = -(b * c)) (h' : a' * d' = -(b' * c'))
    (hu : b * c / a ^ 2 = b' * c' / a' ^ 2) :
    ∃ g l : ℂ, Complex.abs g = 1 ∧ Complex.abs l = 1 ∧
      g * a = a' ∧ g * conj l * b = b' ∧ g * l * c = c' ∧ g * d = d' := by
  have hA : Complex.abs a ≠ 0 := by simpa using ha
  have hC : Complex.abs c ≠ 0 := by simpa using hc
  have ha' : a' ≠ 0 := by
    intro h0; rw [h0, map_zero] at haa; exact hA haa.symm
  have hc' : c' ≠ 0 := by
    intro h0; rw [h0, map_zero] at hcc; exact hC hcc.symm
  set g := a' / a with hgdef
  set l := c' * a / (a' * c) with hldef
  have hg : Complex.abs g = 1 := by
    rw [hgdef, map_div₀, haa, div_self hA]
  have hl : Complex.abs l = 1 := by
    rw [hldef, map_div₀, map_mul, map_mul, haa, hcc, mul_comm, div_self (mul_ne_zero hA hC)]
  have hcl : conj l = l⁻¹ := by
    rw [Complex.inv_def, Complex.normSq_eq_abs, hl]; simp
  refine ⟨g, l, hg, hl, ?_, ?_, ?_, ?_⟩
  · rw [hgdef]; field_simp
  · rw [hcl, hldef, hgdef]
    field_simp at hu ⊢
    linear_combination hu
  · rw [hldef, hgdef]; field_simp; ring
  · rw [hgdef]
    have hd : d = -(b * c) / a := by field_simp; linear_combination h
    have hd' : d' = -(b' * c') / a' := by field_simp; linear_combination h'
    rw [hd, hd']
    field_simp at hu ⊢
    linear_combination hu

#print axioms L1_roots
#print axioms L2_common_det
#print axioms L2_common_u
#print axioms L2_rail_u_general
#print axioms L2_rail_det
#print axioms L2_rail_u
#print axioms L2_site_det
#print axioms L2_site_u_general
#print axioms L2_site_u
#print axioms L2_conj_det
#print axioms L2_conj_u
#print axioms L3_converse
