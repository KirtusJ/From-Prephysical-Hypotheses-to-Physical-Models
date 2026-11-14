import Std

namespace ExchangeableWord

/-- All 36 two-rare masks of a nine-bank block carry weight 1/64.
    The empty mask carries the remaining 28/64. -/
def pairs : List (Nat × Nat) :=
  (List.range 9).flatMap fun i =>
    ((List.range 9).filter fun j => i < j).map fun j => (i,j)

def has (bank : Nat) (mask : Nat × Nat) : Bool :=
  bank == mask.1 || bank == mask.2

theorem nine_masks :
    pairs.length = 36 ∧
    ((List.range 9).all (fun i => (pairs.filter (has i)).length == 8)) = true ∧
    (pairs.all (fun ij => (pairs.filter (fun m => has ij.1 m && has ij.2 m)).length == 1)) = true ∧
    (pairs.filter (fun m => has 0 m && has 1 m && has 2 m)).length = 0 := by
  native_decide

theorem rare_count_pointwise (k : Nat) (hk : k ≤ 2) : k * (k-1) ≤ k := by
  have h : k = 0 ∨ k = 1 ∨ k = 2 := by omega
  rcases h with h | h | h <;> subst k <;> decide

/-- With marginal 1/8 and joint 1/64 on distinct banks, the expected
    factorial second moment ≤ expected count implies n(n−1) ≤ 8n. -/
theorem at_most_nine (n : Nat) (hn : 0 < n) (hm : n*(n-1) ≤ n*8) : n ≤ 9 := by
  by_cases h : n ≤ 9
  · exact h
  · have ht : 8 < n - 1 := by omega
    have hs := Nat.mul_lt_mul_of_pos_left ht hn
    omega

end ExchangeableWord
