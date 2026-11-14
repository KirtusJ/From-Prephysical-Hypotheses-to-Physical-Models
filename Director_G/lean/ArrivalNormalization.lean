import Std

namespace ArrivalNormalization

/- Each pair gives original and reweighted nonnegative numerators on one
   common scale. Cross multiplication keeps the proof in integer arithmetic. -/

def original : List (Nat × Nat) → Nat
  | [] => 0
  | (w, _) :: rest => w + original rest

def reweighted : List (Nat × Nat) → Nat
  | [] => 0
  | (_, b) :: rest => b + reweighted rest

def discrepancy : List (Nat × Nat) → Nat
  | [] => 0
  | (w, b) :: rest => ((b : Int) - w).natAbs + discrepancy rest

def normalizedNumerator (W B : Nat) : List (Nat × Nat) → Nat
  | [] => 0
  | (w, b) :: rest =>
      ((b : Int) * W - (w : Int) * B).natAbs + normalizedNumerator W B rest

theorem total_discrepancy (cells : List (Nat × Nat)) :
    ((reweighted cells : Int) - original cells).natAbs ≤ discrepancy cells := by
  induction cells with
  | nil => decide
  | cons entry rest ih =>
    rcases entry with ⟨w, b⟩
    simp only [original, reweighted, discrepancy, Int.natCast_add]
    rw [show (b : Int) + reweighted rest - ((w : Int) + original rest)
        = ((b : Int) - w) + ((reweighted rest : Int) - original rest) by omega]
    exact Nat.le_trans (Int.natAbs_add_le _ _) (Nat.add_le_add_left ih _)

theorem cross_bound (W B : Nat) (cells : List (Nat × Nat)) :
    normalizedNumerator W B cells ≤
      discrepancy cells * B + reweighted cells * ((W : Int) - B).natAbs := by
  induction cells with
  | nil => simp [normalizedNumerator, discrepancy, reweighted]
  | cons entry rest ih =>
    rcases entry with ⟨w, b⟩
    have split : (b : Int) * W - (w : Int) * B =
        ((b : Int) - w) * B + (b : Int) * ((W : Int) - B) := by
      rw [Int.sub_mul, Int.mul_sub]
      omega
    have one := Int.natAbs_add_le (((b : Int) - w) * B) ((b : Int) * ((W : Int) - B))
    rw [Int.natAbs_mul, Int.natAbs_mul] at one
    simp only [Int.natAbs_ofNat] at one
    simp only [normalizedNumerator, discrepancy, reweighted, Nat.add_mul, split]
    omega

/-- For positive totals W,B, divide this bound by 2WB.
    The total variation of the two normalized laws is at most D/W,
    where D is the raw L1 discrepancy in their common numerator units. -/
theorem normalized_tv_bound (cells : List (Nat × Nat)) :
    normalizedNumerator (original cells) (reweighted cells) cells ≤
      2 * (discrepancy cells * reweighted cells) := by
  have raw := total_discrepancy cells
  have swapped : ((original cells : Int) - reweighted cells).natAbs =
      ((reweighted cells : Int) - original cells).natAbs := by
    rw [show (original cells : Int) - reweighted cells =
        -((reweighted cells : Int) - original cells) by omega, Int.natAbs_neg]
  have cross := cross_bound (original cells) (reweighted cells) cells
  rw [swapped] at cross
  have scaled := Nat.mul_le_mul_left (reweighted cells) raw
  rw [Nat.mul_comm (reweighted cells) (discrepancy cells)] at scaled
  omega

end ArrivalNormalization
