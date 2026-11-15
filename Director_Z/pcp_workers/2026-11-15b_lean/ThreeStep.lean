import Mathlib
/-!
T3. The induction step of thm:fgthree as algebra.
-/
open Polynomial Finset

/-- L(pi) = sum_{d'} b_{d'} sum_i pi_i pi_{i+d'} (sums truncated at K > deg), with
    b_{d'} = 0 for d' < d and deg pi <= d, is b_d pi_0 pi_d. -/
theorem L_single (b : ℕ → ℝ) (π : ℝ[X]) (d K : ℕ) (hK : d < K)
    (hb : ∀ d', d' < d → b d' = 0) (hdeg : π.natDegree ≤ d) :
    ∑ d' ∈ range K, b d' * ∑ i ∈ range K, π.coeff i * π.coeff (i + d')
      = b d * (π.coeff 0 * π.coeff d) := by
  rw [Finset.sum_eq_single d]
  · congr 1
    rw [Finset.sum_eq_single 0]
    · simp
    · intro i _ hi
      rw [coeff_eq_zero_of_natDegree_lt (n := i + d) (by omega)]
      simp
    · intro h
      exact absurd (mem_range.mpr (by omega)) h
  · intro d' _ hne
    rcases Nat.lt_or_gt_of_ne hne with h | h
    · rw [hb d' h]; simp
    · have : ∑ i ∈ range K, π.coeff i * π.coeff (i + d') = 0 := by
        apply Finset.sum_eq_zero
        intro i _
        rw [coeff_eq_zero_of_natDegree_lt (n := i + d') (by omega)]
        simp
      rw [this]; simp
  · intro h
    exact absurd (mem_range.mpr hK) h

/-- pi_A = (4 + sigma + sigma X)(1+X)^(d-1), d = e + 2 -/
noncomputable def piA (σ : ℝ) (e : ℕ) : ℝ[X] := (C (4 + σ) + C σ * X) * (1 + X) ^ (e + 1)
/-- pi_B = (1+2X)(1+(2+sigma)X)(1+X)^(d-2), d = e + 2 -/
noncomputable def piB (σ : ℝ) (e : ℕ) : ℝ[X] :=
  (1 + C 2 * X) * (1 + C (2 + σ) * X) * (1 + X) ^ e

theorem deg_lin (u v : ℝ) : (C u + C v * X).natDegree ≤ 1 := by
  compute_degree
theorem deg_onex : ((1 : ℝ[X]) + X).natDegree ≤ 1 := by
  compute_degree

theorem piA_deg (σ : ℝ) (e : ℕ) : (piA σ e).natDegree ≤ e + 2 := by
  unfold piA
  have h1 := deg_lin (4 + σ) σ
  have h2 : (((1 : ℝ[X]) + X) ^ (e + 1)).natDegree ≤ e + 1 := by
    simpa using natDegree_pow_le_of_le (e + 1) deg_onex
  have := natDegree_mul_le_of_le h1 h2
  omega

theorem piB_deg (σ : ℝ) (e : ℕ) : (piB σ e).natDegree ≤ e + 2 := by
  unfold piB
  have h1 : ((1 : ℝ[X]) + C 2 * X).natDegree ≤ 1 := by compute_degree
  have h2 : ((1 : ℝ[X]) + C (2 + σ) * X).natDegree ≤ 1 := by compute_degree
  have h3 : (((1 : ℝ[X]) + X) ^ e).natDegree ≤ e := by
    simpa using natDegree_pow_le_of_le e deg_onex
  have := natDegree_mul_le_of_le (natDegree_mul_le_of_le h1 h2) h3
  omega

theorem piA_coeff_zero (σ : ℝ) (e : ℕ) : (piA σ e).coeff 0 = 4 + σ := by
  simp [piA, coeff_zero_eq_eval_zero]

theorem piB_coeff_zero (σ : ℝ) (e : ℕ) : (piB σ e).coeff 0 = 1 := by
  simp [piB, coeff_zero_eq_eval_zero]

theorem piA_coeff_top (σ : ℝ) (e : ℕ) : (piA σ e).coeff (e + 2) = σ := by
  unfold piA
  have h2 : (((1 : ℝ[X]) + X) ^ (e + 1)).natDegree ≤ e + 1 := by
    simpa using natDegree_pow_le_of_le (e + 1) deg_onex
  have := coeff_mul_of_natDegree_le (deg_lin (4 + σ) σ) h2
  rw [show e + 2 = 1 + (e + 1) by ring, this]
  have h3 := coeff_pow_of_natDegree_le (n := 1) (m := e + 1) deg_onex
  rw [mul_one] at h3
  rw [h3]
  simp [coeff_X, coeff_one]

theorem piB_coeff_top (σ : ℝ) (e : ℕ) : (piB σ e).coeff (e + 2) = 2 * (2 + σ) := by
  unfold piB
  have h1 : ((1 : ℝ[X]) + C 2 * X).natDegree ≤ 1 := by compute_degree
  have h2 : ((1 : ℝ[X]) + C (2 + σ) * X).natDegree ≤ 1 := by compute_degree
  have h3 : (((1 : ℝ[X]) + X) ^ e).natDegree ≤ e := by
    simpa using natDegree_pow_le_of_le e deg_onex
  have a := coeff_mul_of_natDegree_le (natDegree_mul_le_of_le h1 h2) h3
  have b := coeff_mul_of_natDegree_le h1 h2
  have c := coeff_pow_of_natDegree_le (n := 1) (m := e) deg_onex
  rw [mul_one] at c
  rw [show e + 2 = (1 + 1) + e by ring, a, b, c]
  simp [coeff_X, coeff_one]

/-- the induction step: L(pi_A) = L(pi_B), b_{d'} = 0 below d = e+2, sigma = ±1  ⟹  b_d = 0 -/
theorem step (b : ℕ → ℝ) (σ : ℝ) (hσ : σ = 1 ∨ σ = -1) (e K : ℕ) (hK : e + 2 < K)
    (hb : ∀ d', d' < e + 2 → b d' = 0)
    (hL : ∑ d' ∈ range K, b d' * ∑ i ∈ range K, (piA σ e).coeff i * (piA σ e).coeff (i + d')
        = ∑ d' ∈ range K, b d' * ∑ i ∈ range K, (piB σ e).coeff i * (piB σ e).coeff (i + d')) :
    b (e + 2) = 0 := by
  rw [L_single b _ (e + 2) K hK hb (piA_deg σ e), L_single b _ (e + 2) K hK hb (piB_deg σ e),
    piA_coeff_zero, piA_coeff_top, piB_coeff_zero, piB_coeff_top] at hL
  rcases hσ with rfl | rfl <;> linarith

/-- all b_d with 2 <= d < K vanish, given b_0 = b_1 = 0 and the coincidences for each d -/
theorem all_zero (b : ℕ → ℝ) (σ : ℝ) (hσ : σ = 1 ∨ σ = -1) (K : ℕ)
    (h0 : b 0 = 0) (h1 : b 1 = 0)
    (hL : ∀ e, e + 2 < K →
      ∑ d' ∈ range K, b d' * ∑ i ∈ range K, (piA σ e).coeff i * (piA σ e).coeff (i + d')
        = ∑ d' ∈ range K, b d' * ∑ i ∈ range K, (piB σ e).coeff i * (piB σ e).coeff (i + d')) :
    ∀ d, d < K → b d = 0 := by
  intro d
  induction d using Nat.strong_induction_on with
  | _ d ih =>
    intro hd
    match d, ih, hd with
    | 0, _, _ => exact h0
    | 1, _, _ => exact h1
    | e + 2, ih, hd =>
      exact step b σ hσ e K hd (fun d' hd' => ih d' hd' (by omega)) (hL e hd)

/-- Qbar(phi(X pi)) = Qbar(phi(pi)): multiplication by X sends (e0,e1,e2) to (sigma e2, e0, e1). -/
theorem Qbar_shift (q c σ e0 e1 e2 : ℝ) (hσ : σ ^ 2 = 1) :
    q * ((σ * e2) ^ 2 + e0 ^ 2 + e1 ^ 2) + c * ((σ * e2) * e0 + e0 * e1 + σ * e1 * (σ * e2))
      = q * (e0 ^ 2 + e1 ^ 2 + e2 ^ 2) + c * (e0 * e1 + e1 * e2 + σ * e2 * e0) := by
  linear_combination (q * e2 ^ 2 + c * e1 * e2) * hσ

/-- the identity e_beta * A = B at the level of polynomials in X with X^3 = sigma (eta -> sigma):
    X (4 + sigma + sigma X)(1 + X) - (1 + 2X)(1 + (2 + sigma) X) = (X^3 - sigma) * sigma, sigma^2 = 1 -/
theorem AB_coincidence (σ x : ℝ) (hσ : σ ^ 2 = 1) :
    x * (4 + σ + σ * x) * (1 + x) - (1 + 2 * x) * (1 + (2 + σ) * x) = σ * (x ^ 3 - σ) := by
  linear_combination hσ

#print axioms L_single
#print axioms piA_deg
#print axioms piB_deg
#print axioms piA_coeff_zero
#print axioms piB_coeff_zero
#print axioms piA_coeff_top
#print axioms piB_coeff_top
#print axioms step
#print axioms all_zero
#print axioms Qbar_shift
#print axioms AB_coincidence
