import Mathlib

open Finset

namespace FPHPM

/-- Lemma A, elementary form of independence (the form the proof uses). -/
theorem idempotent_coeffs_of_indep {K ι X : Type*} [CommRing K] [Fintype ι] [DecidableEq ι]
    (f : ι → X → K)
    (hf : ∀ g : ι → K, (∀ x, ∑ i, g i * f i x = 0) → ∀ i, g i = 0)
    (e : ι → K)
    (h : ∀ x y, ∑ i, e i * f i x * f i y = (∑ i, e i * f i x) * (∑ j, e j * f j y)) :
    ∀ i j, e i * e j = if i = j then e i else 0 := by
  have h1 : ∀ y i, e i * f i y - e i * (∑ j, e j * f j y) = 0 := by
    intro y
    apply hf
    intro x
    have : ∑ i, (e i * f i y - e i * (∑ j, e j * f j y)) * f i x
        = ∑ i, e i * f i x * f i y - (∑ i, e i * f i x) * (∑ j, e j * f j y) := by
      rw [Finset.sum_mul, ← Finset.sum_sub_distrib]
      apply Finset.sum_congr rfl
      intros; ring
    rw [this, h x y, sub_self]
  intro i j
  have h2 : ∀ j, (if i = j then e i else 0) - e i * e j = 0 := by
    apply hf
    intro y
    have : ∑ j, ((if i = j then e i else 0) - e i * e j) * f j y
        = e i * f i y - e i * (∑ j, e j * f j y) := by
      simp only [sub_mul, Finset.sum_sub_distrib, ite_mul, zero_mul, Finset.mul_sum,
        Finset.sum_ite_eq, Finset.mem_univ, if_true, mul_assoc]
    rw [this, h1 y i]
  exact (sub_eq_zero.mp (h2 j)).symm

/-- The two formulations of independence agree. -/
theorem linearIndependent_iff_elementary {K ι X : Type*} [CommRing K] [Fintype ι]
    (f : ι → X → K) :
    LinearIndependent K f ↔
      ∀ g : ι → K, (∀ x, ∑ i, g i * f i x = 0) → ∀ i, g i = 0 := by
  rw [Fintype.linearIndependent_iff]
  constructor
  · intro H g hg
    apply H
    funext x
    simpa using hg x
  · intro H g hg
    apply H
    intro x
    simpa using congrFun hg x

/-- Lemma A under `LinearIndependent K f`. -/
theorem idempotent_coeffs {K ι X : Type*} [CommRing K] [Fintype ι] [DecidableEq ι]
    (f : ι → X → K) (hf : LinearIndependent K f) (e : ι → K)
    (h : ∀ x y, ∑ i, e i * f i x * f i y = (∑ i, e i * f i x) * (∑ j, e j * f j y)) :
    ∀ i j, e i * e j = if i = j then e i else 0 :=
  idempotent_coeffs_of_indep f ((linearIndependent_iff_elementary f).mp hf) e h

/-- Lemma B. -/
theorem zero_or_one_at_most_one {K ι : Type*} [CommRing K] [IsDomain K] [DecidableEq ι]
    (e : ι → K) (h : ∀ i j, e i * e j = if i = j then e i else 0) :
    (∀ i, e i = 0 ∨ e i = 1) ∧ (∀ i j, i ≠ j → ¬ (e i = 1 ∧ e j = 1)) := by
  constructor
  · intro i
    have := h i i
    simp only [if_true] at this
    have h' : e i * (e i - 1) = 0 := by rw [mul_sub, this, mul_one, sub_self]
    rcases mul_eq_zero.mp h' with h0 | h0
    · exact Or.inl h0
    · exact Or.inr (sub_eq_zero.mp h0)
  · rintro i j hij ⟨hi, hj⟩
    have := h i j
    rw [if_neg hij, hi, hj] at this
    rw [mul_one] at this
    exact one_ne_zero this

end FPHPM

#print axioms FPHPM.idempotent_coeffs_of_indep
#print axioms FPHPM.linearIndependent_iff_elementary
#print axioms FPHPM.idempotent_coeffs
#print axioms FPHPM.zero_or_one_at_most_one
