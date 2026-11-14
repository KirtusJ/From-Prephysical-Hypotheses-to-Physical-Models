import Std

namespace EraserRowScores

-- Arbitrary already-scored nonnegative rational cells a/d and b/d.
-- Duplicating a common denominator leaves the comparison in natural numbers.
def pairs (a b : Nat) : Bool → Bool → Nat
  | false, false => a
  | false, true  => b
  | true,  false => b
  | true,  true  => a

def normalizer (v : Bool → Bool → Nat) (r : Bool) := v r false + v r true

theorem equalRowScores (a b : Nat) (r : Bool) :
    normalizer (pairs a b) r = a + b := by
  cases r <;> simp [normalizer, pairs, Nat.add_comm]

-- The denominator for a global cell equals two copies of its row normalizer.
-- If a+b is positive this proves equality of the two normalized cell fractions.
theorem equalCellDenominators (a b : Nat) (r : Bool) :
    normalizer (pairs a b) false + normalizer (pairs a b) true =
      2 * normalizer (pairs a b) r := by
  simp only [equalRowScores]
  omega

end EraserRowScores
