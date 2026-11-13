import Mathlib

open MvPolynomial Finset

/-- Newton step: equal power sums of orders `1..k` give equal elementary symmetric
functions of order `k`, in a commutative ring where positive naturals are not zero divisors. -/
theorem esymm_eq_of_psum_eq {R σ : Type*} [CommRing R] [CharZero R] [NoZeroDivisors R]
    [Fintype σ] (f g : σ → R) (n : ℕ)
    (h : ∀ k, 1 ≤ k → k ≤ n → ∑ i, f i ^ k = ∑ i, g i ^ k) :
    ∀ k, k ≤ n → (univ.val.map f).esymm k = (univ.val.map g).esymm k := by
  intro k
  induction k using Nat.strong_induction_on with
  | _ k ih =>
    intro hk
    rcases Nat.eq_zero_or_pos k with rfl | hpos
    · simp [Multiset.esymm]
    · have hps : ∀ (u : σ → R) (j : ℕ), aeval u (psum σ R j) = ∑ i, u i ^ j := by
        intro u j; simp [psum]
      have hN := mul_esymm_eq_sum σ R k
      have hf := congrArg (aeval f) hN
      have hg := congrArg (aeval g) hN
      simp only [map_mul, map_natCast, map_pow, map_neg, map_one, map_sum,
        aeval_esymm_eq_multiset_esymm, hps] at hf hg
      have hsum : ∑ a ∈ (antidiagonal k).filter (fun a ↦ a.fst < k),
            (-1 : R) ^ a.fst * (univ.val.map f).esymm a.fst * ∑ i, f i ^ a.snd =
          ∑ a ∈ (antidiagonal k).filter (fun a ↦ a.fst < k),
            (-1 : R) ^ a.fst * (univ.val.map g).esymm a.fst * ∑ i, g i ^ a.snd := by
        apply Finset.sum_congr rfl
        intro a ha
        rw [Finset.mem_filter, mem_antidiagonal] at ha
        rw [ih a.1 ha.2 (by omega), h a.2 (by omega) (by omega)]
      rw [hsum, ← hg] at hf
      exact mul_left_cancel₀ (Nat.cast_ne_zero.mpr (by omega)) hf

/-- General form: two finite families in an integral domain of characteristic zero,
indexed by the same finite type, with equal power sums of orders `1..card`, are equal
as multisets. -/
theorem multiset_eq_of_psum_eq {R σ : Type*} [CommRing R] [IsDomain R] [CharZero R]
    [Fintype σ] (f g : σ → R)
    (h : ∀ k, 1 ≤ k → k ≤ Fintype.card σ → ∑ i, f i ^ k = ∑ i, g i ^ k) :
    (univ : Finset σ).val.map f = (univ : Finset σ).val.map g := by
  have he := esymm_eq_of_psum_eq f g (Fintype.card σ) h
  have hc : ∀ u : σ → R, Multiset.card ((univ : Finset σ).val.map u) = Fintype.card σ := by
    intro u; simp [Finset.card_univ]
  have hp : (((univ : Finset σ).val.map f).map fun t => Polynomial.X - Polynomial.C t).prod =
      (((univ : Finset σ).val.map g).map fun t => Polynomial.X - Polynomial.C t).prod := by
    rw [Multiset.prod_X_sub_X_eq_sum_esymm, Multiset.prod_X_sub_X_eq_sum_esymm, hc, hc]
    apply Finset.sum_congr rfl
    intro j hj
    rw [he j (by simpa [Nat.lt_succ_iff] using hj)]
  have := congrArg Polynomial.roots hp
  rwa [Polynomial.roots_multiset_prod_X_sub_C, Polynomial.roots_multiset_prod_X_sub_C] at this

/-- The Newton step of Step 1 of thm:vsl: if the power sums of orders `1..m` of `m`
elements all equal `m`, then every element is `1`. No hypothesis `m ≥ 1` is needed. -/
theorem eq_one_of_psum_eq_card {R σ : Type*} [CommRing R] [IsDomain R] [CharZero R]
    [Fintype σ] (z : σ → R)
    (h : ∀ k, 1 ≤ k → k ≤ Fintype.card σ → ∑ i, z i ^ k = (Fintype.card σ : R)) :
    ∀ i, z i = 1 := by
  have hm := multiset_eq_of_psum_eq z (fun _ => (1 : R)) (by
    intro k h1 h2
    rw [h k h1 h2]; simp [Finset.card_univ])
  intro i
  have hi : z i ∈ (univ : Finset σ).val.map z := Multiset.mem_map_of_mem z (Finset.mem_univ i)
  rw [hm] at hi
  obtain ⟨_, _, h1⟩ := Multiset.mem_map.mp hi
  exact h1.symm

/-- As stated in the task: `m` complex numbers. -/
theorem vsl_newton (m : ℕ) (z : Fin m → ℂ)
    (h : ∀ k, 1 ≤ k → k ≤ m → ∑ i, z i ^ k = (m : ℂ)) : ∀ i, z i = 1 :=
  eq_one_of_psum_eq_card z (by simpa using h)

#print axioms multiset_eq_of_psum_eq
#print axioms eq_one_of_psum_eq_card
#print axioms vsl_newton
