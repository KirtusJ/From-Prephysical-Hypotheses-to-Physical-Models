import Std

/-! First-click contrasts in two static read settings. Integer units represent
exact rational rates after clearing denominators. Physical calibration of
the exposed minor cells and conditional hazards is a separate premise.
Lean 4.19.0, Std. -/

namespace ExposureContrast

/-! Static direct and split configurations. A clock with two discrete
ticks tests stationary conditional hazards. Rates a/d and b/d are
per-tick event probabilities. The conditional direct minor hazard is
r*b/d. Weighting a tick-two hit by its minor indicator divided by r
minus one gives the marked term below (multiply by two). -/

def staticTwoTick (d a b : Int) : Int :=
  (d-b)*(d-b) - (d-a)*(d-a) + 2*(d-a)*(b-a)

theorem staticSquare (d a b : Int) : staticTwoTick d a b = (a-b)*(a-b) := by
  have twice (z : Int) : 2*z=z+z := by omega
  simp only [staticTwoTick, twice, Int.mul_sub, Int.sub_mul,
    Int.mul_add, Int.add_mul, Int.mul_comm, Int.mul_left_comm, Int.mul_assoc]
  omega

theorem staticEquality (d a b : Int) :
    0 ≤ staticTwoTick d a b ∧ (staticTwoTick d a b = 0 ↔ a = b) := by
  rw [staticSquare]
  constructor
  · by_cases h : 0 ≤ a-b
    · exact Int.mul_nonneg h h
    · exact Int.mul_nonneg_of_nonpos_of_nonpos (by omega) (by omega)
  · simp only [Int.mul_eq_zero]
    omega

/-- Convert the monitored minor-event count to the observable term.
The minor fraction is r/s, and the total/minor tick-two numerators
before multiplying by two are s*(d-a)*a and r*(d-a)*b in units
of 1/(s*d²), respectively. -/
theorem markedTerm (s r d a b : Int) :
    s*(r*(d-a)*b) - r*(s*(d-a)*a) = (s*r)*(d-a)*(b-a) := by
  simp only [Int.mul_sub, Int.sub_mul, Int.mul_comm, Int.mul_left_comm, Int.mul_assoc]
  omega

/-- Deviations from stationary alive-conditional second-slot hazards.
u,v shift the direct, split total hazard. w is the direct minor hazard
shift after division by the positive minor fraction r. Integer units
are shared by the hazards and d. This is the exact residual term. -/
theorem staticDrift (d a b u v w : Int) :
    (d-b)*(d-b-v) - (d-a)*(d-a-u) + 2*(d-a)*(b+w-a-u) =
    staticTwoTick d a b - (d-a)*u - (d-b)*v + 2*(d-a)*w := by
  have twice (z : Int) : 2*z=z+z := by omega
  simp only [staticTwoTick, twice, Int.mul_add, Int.add_mul, Int.mul_sub,
    Int.sub_mul, Int.mul_comm, Int.mul_left_comm, Int.mul_assoc]
  omega

/-- For the named two-mode example scale the raw rates by 1/2 to make
valid per-tick probabilities: (a+,a−,b)=(9/16,9/20,1/2). Its fair mean
two-tick gap is 41/12800. The elapsed time scale is part of the model. -/
theorem twoTickRival :
    staticTwoTick 80 45 40 + staticTwoTick 80 36 40 = 41 ∧
    (2*(80: Int)*80 = 12800) := by decide

/-- Ordinary diagonal loss on the 4:1:3 heavy-R : heavy-L : minor
sectors. The first-tick totals and protected minor rates match. The
split survival factors are 5/8,0,1/2; the direct ones are all 1/2.
After two ticks the marked direct correction vanishes and the survival
difference is 5/128. The sharper square test needs stationary hazards
conditional on survival within each response mode. -/
theorem splitSurvivorBias :
    (4*5 + 1*0 + 3*4 : Int) = 8*4 ∧
    (4*5*5 + 1*0*0 + 3*4*4 : Int) = 148 ∧
    (8*4*4 : Int) = 128 ∧
    ((148-128)*128 : Int) = 5*(8*8*8) := by decide

/-- Clear the positive common denominator (k+b)(k+a)² in the alternative
static exponential-deadline statistic. -/
def deadlineNumerator (k a b : Int) : Int :=
  k*(k+a)*(k+a) - k*(k+b)*(k+a) + k*(b-a)*(k+b)

theorem deadlineSquare (k a b : Int) :
    deadlineNumerator k a b = k*((b-a)*(b-a)) := by
  simp only [deadlineNumerator, Int.mul_add, Int.add_mul, Int.sub_mul, Int.mul_sub,
    Int.mul_comm, Int.mul_assoc, Int.mul_left_comm]
  omega

theorem deadlineDenominator (k a b : Int) (hk : 0 < k) (ha : 0 ≤ a) (hb : 0 ≤ b) :
    0 < (k+b)*(k+a)*(k+a) := by
  exact Int.mul_pos (Int.mul_pos (by omega) (by omega)) (by omega)

/-- k=b=1, a+=9/8 and a−=9/10. The common-unit factors cancel.
325/208658 equals the fair mean of 1/578 and 1/722. -/
theorem deadlineRival :
    deadlineNumerator 8 9 8 * 578 = (8+8)*(8+9)*(8+9) ∧
    deadlineNumerator 10 9 10 * 722 = (10+10)*(10+9)*(10+9) ∧
    ((578+722)*208658 : Int) = 325*(2*578*722) := by decide

end ExposureContrast
