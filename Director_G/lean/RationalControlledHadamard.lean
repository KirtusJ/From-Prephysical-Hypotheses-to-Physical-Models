import Std

/-!
The bypass entry of a nonzero projective controlled-Hadamard matrix has
twice the squared modulus of each active diagonal entry. If the two real
entries have a common scale and integer numerators, that equality is
impossible. These lemmas concern the two entries after the common scale
has been removed. They do not postulate a physical controlled gate.
-/

namespace RationalControlledHadamard

private theorem even_of_twice_square (a b : Nat)
    (eqn : a*a = 2*(b*b)) : 2 ∣ a := by
  apply Nat.dvd_of_mod_eq_zero
  have zero : a*a % 2 = 0 := by rw [eqn, Nat.mul_mod_right]
  by_cases h : a % 2 = 0
  · exact h
  · have one : a % 2 = 1 := by omega
    rw [Nat.mul_mod, one] at zero
    contradiction

/-- From a positive solution (a,b), evenness of a gives the smaller
solution (b,a/2). The decreasing measure is a+b. -/
theorem nat_square_eq_twice (a b : Nat) (eqn : a*a = 2*(b*b)) :
    a = 0 ∧ b = 0 := by
  by_cases ha : a = 0
  · subst a
    have bb : b*b = 0 := by omega
    exact ⟨rfl, (Nat.mul_eq_zero.mp bb).elim id id⟩
  · obtain ⟨k, hk⟩ := even_of_twice_square a b eqn
    have twice : (2*k)*(2*k) = 2*(2*(k*k)) := by ac_rfl
    rw [hk, twice] at eqn
    have smaller : b*b = 2*(k*k) := by omega
    have descent := nat_square_eq_twice b k smaller
    omega
termination_by a+b
decreasing_by omega

/-- The signed integer version applies even when accessible paths have
different signs or the candidate gate carries a global minus sign. -/
theorem int_square_eq_twice (a b : Int) (eqn : a*a = 2*(b*b)) :
    a = 0 ∧ b = 0 := by
  have absolute := congrArg Int.natAbs eqn
  simp only [Int.natAbs_mul] at absolute
  have zero := nat_square_eq_twice a.natAbs b.natAbs absolute
  exact ⟨Int.natAbs_eq_zero.mp zero.1, Int.natAbs_eq_zero.mp zero.2⟩

/-- For entries a/sqrt(2^t), b/sqrt(2^t) the normalized squared-entry
mismatch is at least 1/2^t. The integer version also applies at any
common positive squared denominator. -/
theorem squared_gap (a b : Int) (live : a ≠ 0 ∨ b ≠ 0) :
    1 ≤ (2*(b*b)-a*a).natAbs := by
  by_cases gap : 1 ≤ (2*(b*b)-a*a).natAbs
  · exact gap
  have h : (2*(b*b)-a*a).natAbs = 0 := by omega
  have eqn := Int.natAbs_eq_zero.mp h
  have zero := int_square_eq_twice a b (by omega)
  rcases live with ha | hb
  · exact False.elim (ha zero.1)
  · exact False.elim (hb zero.2)

/-- Compare the two squared entries with any target whose ratio is 2:1.
In numerator units the target mixed square is k/d. If both errors are
at most e/d, at least one third of a numerator unit is necessary. Dividing
by a common squared denominator 2^t gives error at least 1/(3*2^t). -/
theorem projective_square_precision (a b k : Int) (d e : Nat)
    (live : a ≠ 0 ∨ b ≠ 0)
    (bypass : ((d:Int)*(a*a)-2*k).natAbs ≤ e)
    (active : ((d:Int)*(b*b)-k).natAbs ≤ e) : d ≤ 3*e := by
  let u := (d:Int)*(a*a)-2*k
  let v := (d:Int)*(b*b)-k
  have ident : (d:Int)*(2*(b*b)-a*a) = 2*v + (-u) := by
    dsimp [u, v]
    rw [Int.mul_sub]
    rw [show (d:Int)*(2*(b*b)) = 2*((d:Int)*(b*b)) by ac_rfl]
    omega
  have tri := Int.natAbs_add_le (2*v) (-u)
  rw [← ident] at tri
  simp only [Int.natAbs_mul, Int.natAbs_ofNat, Int.natAbs_neg] at tri
  have hu : u.natAbs ≤ e := bypass
  have hv : v.natAbs ≤ e := active
  have nonzero := squared_gap a b live
  have scaled := Nat.mul_le_mul_left d nonzero
  change d * (2*(b*b)-a*a).natAbs ≤ 2*v.natAbs + u.natAbs at tri
  omega

end RationalControlledHadamard
