import Std

/-! A final localized rail switch. Positive integer panel scales have been
cross-multiplied. The underlying trajectory and reference-port assertions
are physical premises; the signed recurrence below needs no sign symmetry. -/
namespace Crosswire

theorem matched_scale {reference Zheld Zswap : Int} (not_dark : reference ≠ 0)
    (fixed_probability : reference*Zswap = reference*Zheld) : Zswap = Zheld :=
  Int.eq_of_mul_eq_mul_left not_dark fixed_probability

/-- The physical switch permutes only the two tested terminal rails. An
untouched, positive reference transports its marker mass to itself. Equality
of the *sum* of the two tested port probabilities suffices. -/
theorem local_comparison (F G : Int → Int) (a b reference Zheld Zswap : Int)
    (not_dark : reference ≠ 0) (nonempty : Zheld ≠ 0)
    (fixed_probability : reference*Zswap = reference*Zheld)
    (conserved_pair : Zswap*(F a+G b) = Zheld*(F b+G a)) : F a-G a = F b-G b := by
  rw [matched_scale not_dark fixed_probability] at conserved_pair
  have compare := Int.eq_of_mul_eq_mul_left nonempty conserved_pair
  omega

/-- To avoid natural subtraction at n=0 the positive comparison is written
with a shifted index: D(n+2)=D(n). The two left-edge constraints have their
odd/even index explicit; their arguments are signed integers. -/
theorem all_signed {α : Type} (D : Int → α) (z : α)
    (zero : D 0 = z) (one : D 1 = z) (opposite_unit : D 1 = D (-1))
    (positive_strip : ∀ n : Nat, D ((n:Int)+2) = D (n:Int))
    (odd_strip : ∀ m : Nat, m % 2 = 1 → D (1-(m:Int)) = D (1+(m:Int)))
    (even_strip : ∀ m : Nat, m % 2 = 0 → D ((m:Int)-1) = D (-(m:Int)-1)) :
    ∀ k : Int, D k = z := by
  have pos_pair (m : Nat) : D (m:Int) = z ∧ D ((m:Int)+1) = z := by
    induction m with
    | zero => exact ⟨zero, one⟩
    | succ n ih =>
      have nxt : D ((n:Int)+2) = z := (positive_strip n).trans ih.1
      exact ⟨ih.2, nxt⟩
  intro k
  by_cases hk : 0 ≤ k
  · have e : (k.toNat:Int) = k := by omega
    exact e ▸ (pos_pair k.toNat).1
  by_cases hu : k = -1
  · exact hu ▸ opposite_unit.symm.trans one
  by_cases par : k % 2 = 0
  · let m := (1-k).toNat
    have ident : (m:Int) = 1-k := by dsimp [m]; omega
    have edge := odd_strip m (by omega)
    have arg : 1-(m:Int) = k := by omega
    rw [arg, Int.add_comm] at edge
    exact edge.trans (pos_pair m).2
  · let m := (-1-k).toNat
    have ident : (m:Int) = -1-k := by dsimp [m]; omega
    have edge := even_strip m (by omega)
    have arg : -(m:Int)-1 = k := by omega
    rw [arg] at edge
    have prev : (m:Int)-1 = ((m-1:Nat):Int) := by omega
    exact edge.symm.trans (prev ▸ (pos_pair (m-1)).1)

end Crosswire
