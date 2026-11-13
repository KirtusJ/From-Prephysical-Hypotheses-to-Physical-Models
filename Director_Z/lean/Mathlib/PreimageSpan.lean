import Mathlib

/-!
Preimage-span lemma (Remark rem:multisetna, "Step 3 without characters").

Finite dimension of `V` is NOT needed: finite codimension of the target subspace suffices.
Some finiteness is needed.  Counterexample without it: `V = ℕ →₀ K`, `T` the right shift
(`single n 1 ↦ single (n+1) 1`), `W = ⊥`.  Then `W.comap T = ker T = ⊥ ≤ W`, but
`range T ⊔ W = range T ≠ ⊤` (`single 0 1` is not in it).  (Not proved here.)
-/

open Submodule FiniteDimensional

variable {K V V' M : Type*} [DivisionRing K] [AddCommGroup V] [Module K V]
  [AddCommGroup V'] [Module K V'] [AddCommGroup M] [Module K M]

/-- Lemma C (general form): two spaces, only the quotient `V' ⧸ W'` finite-dimensional. -/
theorem range_sup_eq_top_of_comap_le' (T : V →ₗ[K] V') (W : Submodule K V)
    (W' : Submodule K V') [FiniteDimensional K (V' ⧸ W')]
    (h : W'.comap T ≤ W)
    (hd : FiniteDimensional.finrank K (V' ⧸ W') ≤ FiniteDimensional.finrank K (V ⧸ W)) :
    LinearMap.range T ⊔ W' = ⊤ := by
  set q : V →ₗ[K] V' ⧸ W' := W'.mkQ.comp T with hq
  have hker : LinearMap.ker q = W'.comap T := by
    rw [hq, LinearMap.ker_comp, ker_mkQ]
  -- injection V ⧸ ker q → V' ⧸ W'
  set i : (V ⧸ LinearMap.ker q) →ₗ[K] V' ⧸ W' := (LinearMap.ker q).liftQ q le_rfl with hi
  have hinj : Function.Injective i := by
    rw [← LinearMap.ker_eq_bot]; exact ker_liftQ_eq_bot _ _ _ le_rfl
  haveI : FiniteDimensional K (V ⧸ LinearMap.ker q) := FiniteDimensional.of_injective i hinj
  -- surjection V ⧸ ker q → V ⧸ W
  have hle : LinearMap.ker q ≤ W := hker ▸ h
  have hsurj : Function.Surjective ((LinearMap.ker q).liftQ W.mkQ (by rwa [ker_mkQ])) := by
    rw [← LinearMap.range_eq_top, range_liftQ, range_mkQ]
  have h1 := LinearMap.finrank_le_finrank_of_injective hinj
  have h2 := LinearMap.finrank_range_le ((LinearMap.ker q).liftQ W.mkQ (by rwa [ker_mkQ]))
  rw [LinearMap.range_eq_top.2 hsurj, finrank_top] at h2
  have hi_surj : Function.Surjective i :=
    (LinearMap.injective_iff_surjective_of_finrank_eq_finrank (by omega)).1 hinj
  have hrange : LinearMap.range q = ⊤ := by
    rw [← range_liftQ (LinearMap.ker q) q le_rfl]; exact LinearMap.range_eq_top.2 hi_surj
  rw [hq, LinearMap.range_comp] at hrange
  have := congrArg (Submodule.comap W'.mkQ) hrange
  rwa [comap_map_mkQ, comap_top, sup_comm] at this

/-- Lemma A: `W` of finite codimension (in particular `V` finite-dimensional). -/
theorem range_sup_eq_top_of_comap_le (T : V →ₗ[K] V) (W : Submodule K V)
    [FiniteDimensional K (V ⧸ W)] (h : W.comap T ≤ W) :
    LinearMap.range T ⊔ W = ⊤ :=
  range_sup_eq_top_of_comap_le' T W W h le_rfl

/-- Lemma A exactly as asked (finite-dimensional `V`, field or division ring). -/
theorem range_sup_eq_top_of_comap_le_fd [FiniteDimensional K V] (T : V →ₗ[K] V)
    (W : Submodule K V) (h : W.comap T ≤ W) : LinearMap.range T ⊔ W = ⊤ :=
  range_sup_eq_top_of_comap_le T W h

/-- Lemma B: a linear map (to any module) vanishing on `range T` and on `W` is zero. -/
theorem eq_zero_of_vanish_range_of_comap_le (T : V →ₗ[K] V) (W : Submodule K V)
    [FiniteDimensional K (V ⧸ W)] (h : W.comap T ≤ W) (f : V →ₗ[K] M)
    (hT : ∀ v, f (T v) = 0) (hW : ∀ w ∈ W, f w = 0) : f = 0 := by
  have hle : LinearMap.range T ⊔ W ≤ LinearMap.ker f := by
    refine sup_le ?_ (fun w hw => hW w hw)
    rintro _ ⟨v, rfl⟩; exact hT v
  rw [range_sup_eq_top_of_comap_le T W h, top_le_iff] at hle
  exact LinearMap.ker_eq_top.1 hle

/-- Lemma B as asked: functional `f : V →ₗ[K] K`, `V` finite-dimensional. -/
theorem functional_eq_zero_of_comap_le {K V : Type*} [Field K] [AddCommGroup V] [Module K V]
    [FiniteDimensional K V] (T : V →ₗ[K] V) (W : Submodule K V) (h : W.comap T ≤ W)
    (f : V →ₗ[K] K) (hT : ∀ v, f (T v) = 0) (hW : ∀ w ∈ W, f w = 0) : f = 0 :=
  eq_zero_of_vanish_range_of_comap_le T W h f hT hW

#print axioms range_sup_eq_top_of_comap_le'
#print axioms range_sup_eq_top_of_comap_le
#print axioms range_sup_eq_top_of_comap_le_fd
#print axioms eq_zero_of_vanish_range_of_comap_le
#print axioms functional_eq_zero_of_comap_le
