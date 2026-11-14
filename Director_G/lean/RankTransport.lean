import Std

/-! Counts use the same uniform K-slot grid at each time. No divisions or
floating-point comparisons are required. On the line, the two neighboring
parents are consecutive occupied-parity bins and their shared daughter
collects the right block of the first followed by the left block of the
second. Empty blocks are allowed. -/
namespace RankTransport

/-- Entrance at local index z in the right block of the left bin. Its global
index is offset+z. At the daughter the rank starts at zero. -/
theorem enter_right (offset left right fromEast z : Nat) (lo : left ≤ z)
    (hi : z < left + right) :
    z - left < right ∧ z - left < right + fromEast ∧
    offset + z = (offset + left) + (z - left) := by omega

/-- Entrance in the left block of the eastern parent. All rightward
arrivals from its western neighbor precede it at their shared daughter. -/
theorem enter_left (offset left right fromEast z : Nat) (hi : z < fromEast) :
    right ≤ right + z ∧ right + z < right + fromEast ∧
    (offset + left + right) + z = (offset + left) + (right + z) := by omega

/-- Exactly the same global indices belong to the reassembled daughter
as to the union of its two incoming blocks. The intervals are half open. -/
theorem cut_union (offset left right fromEast k : Nat) :
    (offset + left ≤ k ∧ k < offset + left + right + fromEast) ↔
    ((offset + left ≤ k ∧ k < offset + left + right) ∨
     (offset + left + right ≤ k ∧ k < offset + left + right + fromEast)) := by
  omega

/-- A probability mass m/2^t has exactly m*2^(H-t) integer slots out of
2^H whenever t ≤ H. The equality is in cross-multiplied form. -/
theorem common_grid (H t m : Nat) (h : t ≤ H) :
    (m * 2^(H-t)) * 2^t = m * 2^H := by
  rw [Nat.mul_assoc, ← Nat.pow_add, Nat.sub_add_cancel h]

theorem two_pow_strict (b H : Nat) (h : b < H) : 2^b < 2^H := by
  induction H with
  | zero => omega
  | succ n ih =>
    have pos : 0 < 2^n := Nat.pow_pos (by decide)
    rw [Nat.pow_succ]
    by_cases e : b = n
    · subst b
      omega
    · have smaller : b < n := by omega
      have bound := ih smaller
      omega

/-- Counting leaves of a bounded fair-bit decision tree. A sampler using
at most b fair bits can be padded to exactly b, so any event has mass a/2^b.
Matching the sharp frontier event 1/2^H forces b ≥ H. -/
theorem sharp_frontier_bit_bound (a b H : Nat) (mass : a * 2^H = 2^b) :
    H ≤ b := by
  have pos : 0 < 2^b := Nat.pow_pos (by decide)
  have one : 1 ≤ a := by
    by_cases h : a = 0
    · simp [h] at mass
      omega
    · omega
  have lower : 2^H ≤ a * 2^H := by
    simpa using Nat.mul_le_mul_right (2^H) one
  by_cases h : H ≤ b
  · exact h
  · have bad := two_pow_strict b H (by omega)
    omega

/-- The bit appended to a uniform local rank is the low binary digit.
Removing the digit and taking the quotient is the inverse on the whole
doubled support, including the empty parent case. -/
theorem bit_append (size i b : Nat) (hi : i < size) (hb : b < 2) :
    2*i+b < 2*size ∧ (2*i+b)/2 = i ∧ (2*i+b)%2 = b := by omega

theorem bit_unappend (size z : Nat) (hz : z < 2*size) :
    z/2 < size ∧ z%2 < 2 ∧ 2*(z/2)+z%2 = z := by omega

/-- Raw signed source (u,v) splits its doubled grid into consecutive
blocks with the two exact successor sizes. -/
theorem signed_split (u v : Int) :
    (u-v)*(u-v) + (u+v)*(u+v) = 2*(u*u+v*v) := by
  simp only [Int.add_mul, Int.mul_add, Int.sub_mul, Int.mul_sub]
  omega

/-- Appending the same fresh digit at every spatial prefix doubles the
global offset as well as the local index. -/
theorem double_offset (offset i b : Nat) :
    2*(offset+i)+b = 2*offset+(2*i+b) := by omega

end RankTransport
