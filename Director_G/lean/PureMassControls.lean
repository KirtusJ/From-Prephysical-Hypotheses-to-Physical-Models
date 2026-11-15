import Std

namespace PureMassControls

/-- q=0 with one binary split among three occupied sites.
    Each split site has probability 1/2, and each other site has 1/4. -/
example : (217+46+249 : Nat) = 512 ∧
    2*217+46+249 = 729 ∧ 217+2*46+249 = 558 ∧
    217+46+2*249 = 761 := by decide

/-- Cancelling the two linear constraints on two equal-mass classes.
    The variables denote aggregated, already mass-weighted score coefficients.
    The distinct log-masses in the analytical argument supply unequal weights. -/
theorem two_classes (a b u v : Int) (h : a+b=0) (k : u*a+v*b=0) :
    (u-v)*a=0 := by
  have hb : b = -a := by omega
  rw [hb, Int.mul_neg] at k
  rw [Int.sub_mul]
  omega

end PureMassControls
