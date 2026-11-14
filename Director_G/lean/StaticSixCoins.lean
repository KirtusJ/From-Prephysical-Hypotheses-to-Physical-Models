import Std

namespace StaticSixCoins

theorem square_mod_four (a : Nat) : a * a % 4 = (a % 2) := by
  have h : a % 4 < 4 := Nat.mod_lt a (by decide)
  have parity : a % 4 % 2 = a % 2 := by omega
  rw [Nat.mul_mod, ← parity]
  have e : a % 4 = 0 ∨ a % 4 = 1 ∨ a % 4 = 2 ∨ a % 4 = 3 := by omega
  rcases e with h | h | h | h <;> rw [h] <;> decide

theorem no_three_squares (h a b c : Nat) (ha : 0 < a) (hb : 0 < b) (hc : 0 < c) :
    a * a + b * b + c * c ≠ 2 ^ h := by
  induction h using Nat.strongRecOn generalizing a b c with
  | ind h ih =>
    intro eqn
    match h with
    | 0 | 1 =>
      simp at eqn
      have h1 := Nat.mul_pos ha ha
      have h2 := Nat.mul_pos hb hb
      have h3 := Nat.mul_pos hc hc
      omega
    | n + 2 =>
      have four : 2 ^ (n+2) = (2 ^ n) * 4 := by rw [Nat.pow_add]
      have mods : (a % 2 + b % 2 + c % 2) % 4 = 0 := by
        have e := congrArg (fun k : Nat => k % 4) eqn
        simp only at e
        rw [Nat.add_mod, Nat.add_mod (a*a), square_mod_four, square_mod_four,
          square_mod_four, four, Nat.mul_mod_left] at e
        omega
      have ea : a = 2 * (a / 2) := by omega
      have eb : b = 2 * (b / 2) := by omega
      have ec : c = 2 * (c / 2) := by omega
      have sq (k : Nat) : (2*k) * (2*k) = (k*k) * 4 := by
        rw [Nat.mul_mul_mul_comm 2 k 2 k, Nat.mul_comm (2*2)]
      rw [ea, eb, ec, sq, sq, sq, four] at eqn
      have smaller : (a/2)*(a/2) + (b/2)*(b/2) + (c/2)*(c/2) = 2^n := by omega
      exact ih n (by omega) (a/2) (b/2) (c/2) (by omega) (by omega) (by omega) smaller

end StaticSixCoins
