import Mathlib

open Finset

namespace FPHPM.CharacterIndependence

/-- Generic form: a linearly independent family of functions containing the constant `1`. -/
theorem generic {C ι : Type*} (F : ι → C → ℂ) (hF : LinearIndependent ℂ F)
    (one : ι) (hone : ∀ g, F one g = 1) (s : Finset ι) (a : ι → ℂ) (k : ℂ)
    (h : ∀ g, ∑ i in s, a i * F i g = k) : ∀ i ∈ s, i ≠ one → a i = 0 := by
  classical
  intro i hi hne
  rw [linearIndependent_iff'] at hF
  have key := hF (insert one s)
    (fun j => (if j ∈ s then a j else 0) - (if j = one then k else 0)) ?_ i
    (mem_insert_of_mem hi)
  · simpa [hi, hne] using key
  · funext g
    have e1 : ∑ j in insert one s, (if j ∈ s then a j else 0) * F j g = k := by
      rw [← h g]
      symm
      apply Finset.sum_subset_zero_on_sdiff (subset_insert _ _)
      · intro x hx
        simp only [mem_sdiff] at hx
        simp [hx.2]
      · intro x hx
        simp [hx]
    have e2 : ∑ j in insert one s, (if j = one then k else 0) * F j g = k := by
      simp [ite_mul, Finset.sum_ite_eq', hone]
    simp only [Finset.sum_apply, Pi.smul_apply, smul_eq_mul, sub_mul, Finset.sum_sub_distrib,
      Pi.zero_apply, e1, e2, sub_self]

/-- If a finite combination of distinct characters `C →* ℂ` is constant, then all
coefficients of nontrivial characters vanish. -/
theorem char_coeff_eq_zero {C : Type*} [Monoid C] (s : Finset (C →* ℂ))
    (a : (C →* ℂ) → ℂ) (k : ℂ) (h : ∀ g, ∑ χ in s, a χ * χ g = k) :
    ∀ χ ∈ s, χ ≠ 1 → a χ = 0 :=
  generic (fun (χ : C →* ℂ) => (χ : C → ℂ)) (linearIndependent_monoidHom C ℂ) 1
    (fun _ => rfl) s a k h

/-- The same for unit-valued characters `C →* ℂˣ`. -/
theorem unitChar_coeff_eq_zero {C : Type*} [Monoid C] (s : Finset (C →* ℂˣ))
    (a : (C →* ℂˣ) → ℂ) (k : ℂ) (h : ∀ g, ∑ χ in s, a χ * (χ g : ℂ) = k) :
    ∀ χ ∈ s, χ ≠ 1 → a χ = 0 := by
  have hinj : Function.Injective (fun χ : C →* ℂˣ => (Units.coeHom ℂ).comp χ) := by
    intro χ ψ hχψ
    exact MonoidHom.ext fun g => Units.ext (DFunLike.congr_fun hχψ g)
  have hli : LinearIndependent ℂ (fun (χ : C →* ℂˣ) (g : C) => (χ g : ℂ)) :=
    (linearIndependent_monoidHom C ℂ).comp (fun χ : C →* ℂˣ => (Units.coeHom ℂ).comp χ) hinj
  have hone : ∀ g : C, ((1 : C →* ℂˣ) g : ℂ) = 1 := fun g => by simp
  exact generic _ hli 1 hone s a k h

/-- Full-sum version for a finite commutative group. -/
theorem char_sum_const {C : Type*} [CommGroup C] [Fintype C] [Fintype (C →* ℂˣ)]
    (a : (C →* ℂˣ) → ℂ) (k : ℂ) (h : ∀ g, ∑ χ, a χ * (χ g : ℂ) = k) :
    ∀ χ, χ ≠ 1 → a χ = 0 :=
  fun χ => unitChar_coeff_eq_zero univ a k h χ (mem_univ χ)

end FPHPM.CharacterIndependence

#print axioms FPHPM.CharacterIndependence.char_coeff_eq_zero
#print axioms FPHPM.CharacterIndependence.unitChar_coeff_eq_zero
#print axioms FPHPM.CharacterIndependence.char_sum_const
