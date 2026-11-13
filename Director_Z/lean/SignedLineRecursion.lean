/-! Result A: signed line recursion. -/

/-- Polynomial identity `(k+2)^2 c = 2 (k+1)^2 c + 2 c - k^2 c` over `Int`. -/
theorem sq_step (k c : Int) :
    (k + 1 + 1) * (k + 1 + 1) * c = 2 * ((k + 1) * (k + 1) * c) + 2 * c - k * k * c := by
  have e1 : (k + 1) * (k + 1) * c = k * k * c + 2 * (k * c) + c := by
    simp only [Int.add_mul, Int.mul_add, Int.mul_one, Int.one_mul]; omega
  have e2 : (k + 1 + 1) * (k + 1 + 1) * c = k * k * c + 4 * (k * c) + 4 * c := by
    simp only [Int.add_mul, Int.mul_add, Int.mul_one, Int.one_mul]; omega
  omega

theorem signed_line_recursion (phi : Nat → Int)
    (h0 : phi 0 = 0)
    (hrec : ∀ a : Nat, a ≥ 1 → phi (a + 1) + phi (a - 1) = 2 * phi a + 2 * phi 1) :
    ∀ n : Nat, phi n = (n : Int) * n * phi 1 := by
  have key : ∀ n : Nat, phi n = (n : Int) * n * phi 1 ∧
      phi (n + 1) = ((n + 1 : Nat) : Int) * ((n + 1 : Nat) : Int) * phi 1 := by
    intro n
    induction n with
    | zero => simp [h0]
    | succ n ih =>
      refine ⟨ih.2, ?_⟩
      have h := hrec (n + 1) (by omega)
      rw [Nat.add_sub_cancel, ih.1, ih.2] at h
      have s := sq_step (n : Int) (phi 1)
      simp only [Int.ofNat_succ] at h ⊢
      omega
  exact fun n => (key n).1
#print axioms signed_line_recursion
