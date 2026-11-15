import Std

namespace SpectatorRefinement

/-! Lean 4.19.0, standard library. Let A and B be the transformed totals
of two alternative partitions of the same original branch weight, and C
the positive weight on a spectator. Apply the two partition choices to
two other branches. On the settings PP, PQ and QQ the spectator has
probabilities C/(2A+C), C/(A+B+C) and C/(2B+C), respectively.

Here A, B, C are integers on one common scale, which includes arbitrary
rational triples by clearing denominators. Their normalization cancels
from all three probabilities. The formal result concerns these finite
fractions; the choice of partitions or inference from repeated trials
is a separate premise. -/

def denominator (a b c : Int) : Int :=
  (2*a+c)*(2*b+c)*(a+b+c)

/-- Cross-multiplied numerator for PP + QQ − 2 PQ. -/
def numerator (a b c : Int) : Int :=
  c*(2*b+c)*(a+b+c) + c*(2*a+c)*(a+b+c) - 2*c*(2*a+c)*(2*b+c)

theorem square_identity (a b c : Int) :
    numerator a b c = 2*c*((a-b)*(a-b)) := by
  have twice (z : Int) : 2*z=z+z := by omega
  simp only [numerator, twice, Int.mul_add, Int.add_mul, Int.sub_mul, Int.mul_sub,
    Int.mul_comm, Int.mul_assoc, Int.mul_left_comm]
  omega

/-- Empty partition totals are allowed. A positive spectator still makes
all normalizations strictly positive. -/
theorem denominator_positive (a b c : Int) (ha : 0 ≤ a) (hb : 0 ≤ b) (hc : 0 < c) :
    0 < 2*a+c ∧ 0 < 2*b+c ∧ 0 < a+b+c ∧ 0 < denominator a b c := by
  have hp : 0 < 2*a+c := by omega
  have hq : 0 < 2*b+c := by omega
  have hm : 0 < a+b+c := by omega
  exact ⟨hp, hq, hm, Int.mul_pos (Int.mul_pos hp hq) hm⟩

theorem gap_sign_and_equality (a b c : Int) (hc : 0 < c) :
    0 ≤ numerator a b c ∧ (numerator a b c = 0 ↔ a = b) ∧
    (0 < numerator a b c ↔ a ≠ b) := by
  rw [square_identity]
  have h : 0 ≤ (a-b)*(a-b) := by
    by_cases hs : 0 ≤ a-b
    · exact Int.mul_nonneg hs hs
    · exact Int.mul_nonneg_of_nonpos_of_nonpos (by omega) (by omega)
  have hn : 0 ≤ 2*c*((a-b)*(a-b)) := Int.mul_nonneg (by omega) h
  have hz : 2*c*((a-b)*(a-b)) = 0 ↔ a=b := by
    simp only [Int.mul_eq_zero]
    omega
  exact ⟨hn,hz,by omega⟩

end SpectatorRefinement
