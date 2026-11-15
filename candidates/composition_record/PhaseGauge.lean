import Std

namespace PhaseGauge

/- The group stores digits 0,...,4. A phase is represented by its integer
   numerator in units of 1/25, with multiples of 25 identified. -/
def carry (x y : Int) : Int := (x+y)/5
def digitSum (x y : Int) : Int := (x+y)%5

theorem digit_formula (x y : Int) :
    digitSum x y = x+y-5*carry x y := by
  unfold digitSum carry
  omega

theorem carry_assoc (x y z : Int) :
    carry x y + carry (digitSum x y) z = carry y z + carry x (digitSum y z) := by
  unfold carry digitSum
  omega

theorem digit_assoc (x y z : Int) :
    digitSum (digitSum x y) z = digitSum x (digitSum y z) := by
  unfold digitSum
  omega

/-- 25 f_ij(a,b). The four entries are the two chosen coordinates of a and b. -/
def primitive (ai aj bi bj : Int) : Int :=
  -ai*bj + 5*(carry ai bi * digitSum aj bj)

/-- Numerator of the inhomogeneous group coboundary:
    f(b,c) - f(a+b,c) + f(a,b+c) - f(a,b). -/
def coboundary (ai aj bi bj ci cj : Int) : Int :=
  primitive bi bj ci cj -
  primitive (digitSum ai bi) (digitSum aj bj) ci cj +
  primitive ai aj (digitSum bi ci) (digitSum bj cj) -
  primitive ai aj bi bj

theorem bilinear_part (ai bi bj cj : Int) :
    -bi*cj - (-(digitSum ai bi)*cj) + (-ai)*(digitSum bj cj) - (-ai)*bj =
      5*(ai*carry bj cj - carry ai bi*cj) := by
  simp only [digit_formula,Int.neg_mul,Int.mul_sub,Int.mul_add,Int.sub_mul,Int.add_mul]
  rw [Int.mul_assoc 5 (carry ai bi) cj, ← Int.mul_assoc ai 5, Int.mul_comm ai 5,
      Int.mul_assoc 5 ai]
  omega

/-- The quotient left by the two reductions of the j-coordinate. -/
def quotient (ai aj bi bj ci cj : Int) : Int :=
  carry bi ci * (carry aj bj + carry (digitSum aj bj) cj - carry bj cj) -
  carry ai bi * carry (digitSum aj bj) cj

theorem seam_part (ai aj bi bj ci cj : Int) :
    carry bi ci * digitSum bj cj -
      carry (digitSum ai bi) ci * digitSum (digitSum aj bj) cj +
      carry ai (digitSum bi ci) * digitSum aj (digitSum bj cj) -
      carry ai bi * digitSum aj bj =
    carry ai bi*cj - aj*carry bi ci + 5*quotient ai aj bi bj ci cj := by
  rw [← digit_assoc aj bj cj]
  have hc := carry_assoc ai bi ci
  have ht : carry ai (digitSum bi ci) =
      carry ai bi + carry (digitSum ai bi) ci - carry bi ci := by omega
  rw [ht]
  unfold quotient
  rw [digit_formula (digitSum aj bj) cj]
  generalize carry (digitSum aj bj) cj = K
  rw [digit_formula aj bj, digit_formula bj cj]
  generalize carry ai bi = A
  generalize carry bi ci = B
  generalize carry (digitSum ai bi) ci = H
  generalize carry aj bj = U
  generalize carry bj cj = V
  have scale (a k : Int) : a*(5*k) = 5*(a*k) := by
    rw [← Int.mul_assoc, Int.mul_comm a 5, Int.mul_assoc]
  simp only [Int.mul_add,Int.add_mul,Int.mul_sub,Int.sub_mul,scale,Int.mul_comm aj B]
  omega

/-- Exact integer lift. In R/Z the final term vanishes after division by 25. -/
theorem exact_coboundary (ai aj bi bj ci cj : Int) :
    coboundary ai aj bi bj ci cj =
      5*(ai*carry bj cj - aj*carry bi ci) + 25*quotient ai aj bi bj ci cj := by
  have hb := bilinear_part ai bi bj cj
  have hs := seam_part ai aj bi bj ci cj
  unfold coboundary primitive
  omega

theorem skew_phase (ai aj bi bj ci cj : Int) :
    (coboundary ai aj bi bj ci cj) % 25 =
      (5*(ai*carry bj cj - aj*carry bi ci)) % 25 := by
  rw [exact_coboundary]
  omega

end PhaseGauge
