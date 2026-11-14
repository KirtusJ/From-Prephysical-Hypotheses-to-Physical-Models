import Std

/-! Signed final-spin amplitudes after three fair steps following arm preparation.
The populations a,b and real off-diagonal entry c share a common integer
denominator. Observed intensity includes unknown row and column factors. -/
namespace ThreeWellPhase

abbrev Field := Int → Int × Int

def flight (v : Field) (x : Int) : Int × Int :=
  ((v (x + 1)).1 + (v (x + 1)).2, (v (x - 1)).1 - (v (x - 1)).2)

def sharpL (x : Int) : Int × Int := if x = -1 then (1, 0) else (0, 0)
def sharpR (x : Int) : Int × Int := if x =  1 then (0, 1) else (0, 0)
def terminal (v : Field) (j : Int) := flight (flight (flight v)) (2*j)

def spinMass (a b c l r : Int) : Int := a*(l*l) + b*(r*r) + c*(2*l*r)

def mass (a b c j : Int) : Int :=
  let l := terminal sharpL j
  let r := terminal sharpR j
  spinMass a b c l.1 r.1 + spinMass a b c l.2 r.2

/-- At (-2,-1,0), masses have a single omitted factor of 1/8. -/
theorem three_wells (a b c : Int) :
    mass a b c (-2) = a ∧ mass a b c (-1) = 5*a+b+4*c ∧ mass a b c 0 = a+b := by
  simp [mass, spinMass, terminal, flight, sharpL, sharpR] <;> omega

/-- A two-row, two-well determinant used in each difference of odds. -/
def minor (u v : Int → Int) (j : Int) := u j * v 0 - v j * u 0
def read (brightness : Int) (gain row : Int → Int) (j : Int) := brightness * gain j * row j

/-- Each determinant gets one factor from each row and from each well. -/
theorem read_minor (s r : Int) (g u v : Int → Int) (j : Int) :
    minor (read s g u) (read r g v) j = s*r*g j*g 0 * minor u v j := by
  simp [minor, read, Int.mul_sub, Int.mul_assoc, Int.mul_comm, Int.mul_left_comm]

/-- The sharp odds spans at the outer and inner wells have ratio 1:4. -/
theorem sharp_spans :
    minor (mass 1 0 0) (mass 0 1 0) (-2) = 1 ∧
    minor (mass 1 0 0) (mass 0 1 0) (-1) = 4 := by decide

/-- The inner minus outer interpolation, before division by 4*(a+b).
It vanishes for every mixture c=0. Positive reference yields and gains
make the corresponding real-valued odds well-defined. -/
theorem contrast_numerator (a b c : Int) :
    minor (mass a b c) (mass 0 1 0) (-1) -
      4 * minor (mass a b c) (mass 0 1 0) (-2) = 4*c := by
  obtain ⟨ho, hi, hz⟩ := three_wells a b c
  obtain ⟨ro, ri, rz⟩ := three_wells 0 1 0
  simp [minor, ho, hi, hz, ro, ri, rz] <;> omega

end ThreeWellPhase
