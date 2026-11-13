import Mathlib

/-- General form: a nonempty multiplicatively closed subset of a group, all of whose
elements have finite order, contains `1` and is closed under inverses. -/
theorem one_mem_and_inv_mem_of_mul_closed_of_torsion {G : Type*} [Group G] (S : Set G)
    (hne : S.Nonempty) (hmul : ∀ x ∈ S, ∀ y ∈ S, x * y ∈ S)
    (htors : ∀ x ∈ S, IsOfFinOrder x) :
    (1 : G) ∈ S ∧ ∀ x ∈ S, x⁻¹ ∈ S := by
  have hpow : ∀ x ∈ S, ∀ n : ℕ, x ^ (n + 1) ∈ S := by
    intro x hx n
    induction n with
    | zero => simpa using hx
    | succ n ih => rw [pow_succ]; exact hmul _ ih _ hx
  have key : ∀ x ∈ S, (1 : G) ∈ S ∧ x⁻¹ ∈ S := by
    intro x hx
    have hpos : 0 < orderOf x := (htors x hx).orderOf_pos
    obtain ⟨n, hn⟩ : ∃ n, orderOf x = n + 1 := ⟨orderOf x - 1, by omega⟩
    have h1 : (1 : G) ∈ S := by
      have := hpow x hx n
      rwa [← hn, pow_orderOf_eq_one] at this
    refine ⟨h1, ?_⟩
    have hinv : x⁻¹ = x ^ n := by
      apply inv_eq_of_mul_eq_one_right
      rw [← pow_succ', ← hn, pow_orderOf_eq_one]
    rw [hinv]
    rcases n with _ | n
    · simpa using h1
    · exact hpow x hx n
  obtain ⟨x, hx⟩ := hne
  exact ⟨(key x hx).1, fun y hy => (key y hy).2⟩

/-- The lemma as used: finite group. -/
theorem one_mem_and_inv_mem_of_mul_closed_of_finite {G : Type*} [Group G] [Finite G] (S : Set G)
    (hne : S.Nonempty) (hmul : ∀ x ∈ S, ∀ y ∈ S, x * y ∈ S) :
    (1 : G) ∈ S ∧ ∀ x ∈ S, x⁻¹ ∈ S :=
  one_mem_and_inv_mem_of_mul_closed_of_torsion S hne hmul (fun x _ => isOfFinOrder_of_finite x)

/-- Packaged as a subgroup with carrier `S`. -/
theorem exists_subgroup_of_mul_closed_of_finite {G : Type*} [Group G] [Finite G] (S : Set G)
    (hne : S.Nonempty) (hmul : ∀ x ∈ S, ∀ y ∈ S, x * y ∈ S) :
    ∃ H : Subgroup G, (H : Set G) = S :=
  let h := one_mem_and_inv_mem_of_mul_closed_of_finite S hne hmul
  ⟨{ carrier := S, mul_mem' := fun {a b} ha hb => hmul a ha b hb, one_mem' := h.1,
     inv_mem' := fun {a} ha => h.2 a ha }, rfl⟩

#print axioms one_mem_and_inv_mem_of_mul_closed_of_torsion
#print axioms one_mem_and_inv_mem_of_mul_closed_of_finite
#print axioms exists_subgroup_of_mul_closed_of_finite
