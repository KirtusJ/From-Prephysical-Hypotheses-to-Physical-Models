import Std

theorem dark_port_parameter (p q r s : Nat) :
    p * (2 * s + 3 * r) = r * (2 * q + 3 * p) ↔
      p * s = r * q := by
  have hp : p * (2 * s + 3 * r) =
      2 * (p * s) + 3 * (p * r) := by
    simp only [Nat.mul_add]
    ac_rfl
  have hr : r * (2 * q + 3 * p) =
      2 * (r * q) + 3 * (p * r) := by
    simp only [Nat.mul_add]
    ac_rfl
  rw [hp, hr]
  omega
