import Std

/-! A finite arithmetic certificate for labels that are mutual inverses in a
cyclic register and have small signed representatives in both directions. -/
namespace RefinementLocality

theorem local_inverses (N u v : Nat) (a b : Int)
    (inverse : (N : Int) ∣ a*b-1)
    (forward : a.natAbs ≤ u) (backward : b.natAbs ≤ v)
    (size : u*v+1 < N) :
    (a=1 ∧ b=1) ∨ (a= -1 ∧ b= -1) := by
  have bound := Int.natAbs_sub_le (a*b) 1
  rw [Int.natAbs_mul, Int.natAbs_one] at bound
  have envelope := Nat.mul_le_mul forward backward
  have zero := Int.eq_zero_of_dvd_of_natAbs_lt_natAbs inverse (by
    rw [Int.natAbs_ofNat]; omega)
  have one : a*b=1 := by omega
  have divisor := Nat.dvd_mul_right a.natAbs b.natAbs
  rw [← Int.natAbs_mul, one, Int.natAbs_one] at divisor
  have unitA := Int.natAbs_eq_iff.mp (Nat.eq_one_of_dvd_one divisor)
  rcases unitA with pos | neg
  · left; change a=1 at pos; simpa [pos] using one
  · right; change a= -1 at neg
    have : -b=1 := by simpa [neg] using one
    exact ⟨neg,by omega⟩

/-- At equality the conclusion fails for every k>0. Here u=v=2k,
N=4k²+1, and a*b-1 is precisely -N. -/
theorem boundary_family (k : Nat) (positive : 0 < k) :
    let N := 4*k^2+1
    let u := 2*k
    let a : Int := u
    let b : Int := -a
    N = u*u+1 ∧ (N:Int) ∣ a*b-1 ∧
      a.natAbs = u ∧ b.natAbs = u ∧
      ¬((a=1 ∧ b=1) ∨ (a= -1 ∧ b= -1)) := by
  dsimp only
  have equality : (2*k)*(2*k) = 4*k^2 := by
    rw [Nat.pow_two]
    calc
      (2*k)*(2*k) = (2*2)*(k*k) := by
        simp only [Nat.mul_assoc, Nat.mul_comm, Nat.mul_left_comm]
      _ = 4*(k*k) := rfl
  refine ⟨by rw [equality],⟨-1,?_⟩,Int.natAbs_ofNat _,by rw [Int.natAbs_neg, Int.natAbs_ofNat],?_⟩
  · rw [← equality]
    simp [Int.natCast_mul, Int.mul_neg, Int.neg_sub, Int.add_comm]
    <;> omega
  · simp only [Int.natCast_mul]
    omega

end RefinementLocality
