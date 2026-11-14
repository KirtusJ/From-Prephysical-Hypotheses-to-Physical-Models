import Std

namespace CountReference

/-- Each physical word of weight k passes exactly k of the m positive
    count thresholds. No distribution on the words is required. -/
def passed (thresholds k : Nat) : Nat :=
  match thresholds with
  | 0 => 0
  | m+1 => passed m k + (if m+1 ≤ k then 1 else 0)

theorem passed_eq_min (m k : Nat) : passed m k = min m k := by
  induction m with
  | zero => simp [passed]
  | succ n ih =>
    simp only [passed, ih]
    split <;> omega

theorem word_tail_sum (m k : Nat) (within : k ≤ m) : passed m k = k := by
  rw [passed_eq_min, Nat.min_eq_right within]

/-- For counts k ≤ l, the number of threshold answers on which they
    differ is exactly l-k. Averaging over independent draws yields the
    absolute-count-difference identity. -/
theorem separated_thresholds (m k l : Nat) (order : k ≤ l) (within : l ≤ m) :
    passed m l - passed m k = l-k := by
  rw [word_tail_sum m l within, word_tail_sum m k (Nat.le_trans order within)]

/-- The eight-copy counterexample, in cleared units. -/
theorem certain_or_midpoint : 2*2 + 6*1 = (10 : Nat) ∧
    2*4 + 6*1 = (14 : Nat) ∧ 4*5 - 14 = (6 : Nat) := by decide

/-- A common monotone complementary response has g(125) ≤ g(162)
    and g(162)+g(350)=d in arbitrary integer rate units out of d.
    The mean of the three rates is thus at most 2/3. -/
theorem three_copy_upper (r125 r162 r350 r485 d : Nat)
    (ordered : r125 ≤ r162) (complementary : r162+r350=d)
    (ceiling : r485 ≤ d) : r125+r350+r485 ≤ 2*d := by omega

/-- Site x=1 under the stated tick-three probe has kinematic odds 5:3.
    Powers of these counts give the three threshold numerators. -/
theorem three_threshold_counts :
    8^3 - 3^3 = (485 : Nat) ∧ 3*5^2*3 + 5^3 = (350 : Nat) ∧
    5^3 = (125 : Nat) ∧ 125 ≤ (512 : Nat)-350 := by decide

theorem square_gap : 3*(25 : Nat) = 2*34+7 := by decide

end CountReference
