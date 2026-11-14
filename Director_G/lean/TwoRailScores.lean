import Std

/-! Two independent sign-insensitive detector shapes (integer-scaled
scores). At one shared clock comparison, the right and left fronts have
the respective sole unit input and the same pair of unit successors. -/
namespace RailShape

theorem compare_fronts (a b oldScale newScale : Int)
    (new_nonzero : newScale ≠ 0) (unit_nonzero : a ≠ 0)
    (right : oldScale*(a+b) = newScale*a)
    (left : oldScale*(a+b) = newScale*b) :
    a = b ∧ newScale = 2*oldScale := by
  have eq := Int.eq_of_mul_eq_mul_left new_nonzero (right.symm.trans left)
  refine ⟨eq, ?_⟩
  rw [← eq, Int.mul_add] at right
  apply Int.eq_of_mul_eq_mul_right unit_nonzero
  rw [Int.mul_assoc]
  omega

/-- Each near-front observation reads the respective scalar on the actual
incoming/output rail. At the left inner edge (1,-n) up to overall sign
exchanges the arguments n-1,n+1 of the two score shapes. -/
theorem forced (F G : Nat → Int) (c : Int)
    (zeroF : F 0 = 0) (zeroG : G 0 = 0) (oneF : F 1 = c) (oneG : G 1 = c)
    (right : ∀ n, F (n+2) + G n = 2*(F (n+1) + c))
    (left : ∀ n, F n + G (n+2) = 2*(c + G (n+1))) :
    ∀ n : Nat, F n = c*(n:Int)*(n:Int) ∧ G n = c*(n:Int)*(n:Int) := by
  have evolve (n : Nat) :
      (F n = c*(n:Int)*(n:Int) ∧ G n = c*(n:Int)*(n:Int)) ∧
      (F (n+1) = c*((n+1:Nat):Int)*((n+1:Nat):Int) ∧
       G (n+1) = c*((n+1:Nat):Int)*((n+1:Nat):Int)) := by
    induction n with
    | zero => simp [zeroF, zeroG, oneF, oneG]
    | succ n ih =>
      refine ⟨ih.2, ?_⟩
      have r := right n
      have l := left n
      rw [ih.1.2, ih.2.1] at r
      rw [ih.1.1, ih.2.2] at l
      change F (n+2) = c*((n+2:Nat):Int)*((n+2:Nat):Int) ∧
             G (n+2) = c*((n+2:Nat):Int)*((n+2:Nat):Int)
      rw [show ((n+2:Nat):Int) = ((n+1:Nat):Int)+1 by omega]
      simp only [Int.natCast_succ, Int.add_mul, Int.mul_add, Int.one_mul, Int.mul_one] at r l ⊢
      omega
  exact fun n => (evolve n).1

end RailShape
