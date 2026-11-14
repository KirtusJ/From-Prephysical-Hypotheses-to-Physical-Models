import Std

namespace RecoilPositionFilter

private theorem twice (a : Int) : a * 2 = a + a := by omega

/-- Integer coordinates for the numerator after multiplying the filtered
    velocity difference by 2*h*k. Units on the grid are arbitrary. -/
theorem cancels_launch (x p r₀ r₁ n₀ n₁ f h k : Int) :
    let z₀ := x+n₀
    let twiceX₁ := 2*x+2*h*(p-r₀)-f*h*h
    let twiceZ₁ := twiceX₁+2*n₁
    let twiceY₂ := twiceX₁+2*k*(p-r₀-f*h-r₁)-f*k*k
    h*(twiceY₂-twiceZ₁)-k*(twiceZ₁-2*z₀)+f*(h+k)*h*k =
      2*k*n₀-2*(h+k)*n₁-2*h*k*r₁ := by
  dsimp
  simp only [Int.mul_add, Int.add_mul, Int.mul_sub, Int.sub_mul, Int.mul_assoc,
    Int.mul_comm, Int.mul_left_comm]
  simp only [twice, Int.mul_add]
  omega

end RecoilPositionFilter
