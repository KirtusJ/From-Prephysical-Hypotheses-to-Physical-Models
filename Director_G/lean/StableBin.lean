import Std

namespace StableBin

/-- The sum of squares of two same-parity inputs equals that of the four
    integral outputs u,v,u,v in the normalized four-mode Walsh gate. -/
theorem pair_split (a b : Int) (parity : a % 2 = b % 2) :
    let u := (a+b)/2
    let v := (a-b)/2
    u+v=a ∧ u-v=b ∧ 2*(u*u+v*v)=a*a+b*b := by
  dsimp only
  have h (x y : Int) :
      (x+y)*(x+y)+(x-y)*(x-y) = 2*(x*x+y*y) := by
    simp only [Int.add_mul, Int.mul_add, Int.sub_mul, Int.mul_sub]
    omega
  have plus : (a+b)/2+(a-b)/2=a := by omega
  have minus : (a+b)/2-(a-b)/2=b := by omega
  exact ⟨plus, minus, by rw [← h, plus, minus]⟩

/-- Fourth-power descent. The inputs are (u+v,u-v), the outputs (u,v,u,v).
    Their fourth powers differ by the positive integer 12 u² v² when u,v>0. -/
theorem fourth_drop (u v : Int) :
    let fourth := fun x : Int => (x*x)*(x*x)
    fourth (u+v) + fourth (u-v) - 2*(fourth u+fourth v) =
      12*((u*u)*(v*v)) := by
  dsimp
  have scale2 (x : Int) : 2*x = x+x := by omega
  have scale12 (x : Int) : 12*x = x+x+x+x+x+x+x+x+x+x+x+x := by omega
  rw [scale2, scale12]
  simp only [Int.add_mul, Int.mul_add, Int.sub_mul, Int.mul_sub, Int.mul_assoc,
    Int.mul_comm, Int.mul_left_comm]
  omega

theorem positive_drop (u v : Int) (hu : 0 < u) (hv : 0 < v) :
    0 < 12*((u*u)*(v*v)) :=
  Int.mul_pos (by decide) (Int.mul_pos (Int.mul_pos hu hu) (Int.mul_pos hv hv))

end StableBin
