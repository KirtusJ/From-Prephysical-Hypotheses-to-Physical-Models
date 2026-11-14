import Std

/-! The scaled affine relations use X, Y=y/sqrt(3), Z and a common
    integer denominator d. They apply before assigning any detector score. -/
namespace CubicRailLaw

theorem tetrahedron (x y z d : Int) :
    let a := 3*d + 6*z
    let b := 2*d - 2*z + 12*y
    let c := 2*d - 2*z - 6*x - 6*y
    let e := 2*d - 2*z + 6*x - 6*y
    a+b+c+e = 9*d ∧
    -3*c+3*e = 36*x ∧
    2*b-c-e = 36*y ∧
    2*a-b-c-e = 18*z := by
  dsimp
  omega

theorem pole_test (red blue green yellow l : Int)
    (operational : 9*l+3*red = 4*blue+4*green+4*yellow) :
    9*l = -3*red+4*blue+4*green+4*yellow := by omega

end CubicRailLaw
