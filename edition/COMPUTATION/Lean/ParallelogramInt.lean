/-! Result B: the parallelogram law on the integers. -/

theorem sq_step (k c : Int) :
    (k + 1 + 1) * (k + 1 + 1) * c = 2 * ((k + 1) * (k + 1) * c) + 2 * c - k * k * c := by
  have e1 : (k + 1) * (k + 1) * c = k * k * c + 2 * (k * c) + c := by
    simp only [Int.add_mul, Int.mul_add, Int.mul_one, Int.one_mul]; omega
  have e2 : (k + 1 + 1) * (k + 1 + 1) * c = k * k * c + 4 * (k * c) + 4 * c := by
    simp only [Int.add_mul, Int.mul_add, Int.mul_one, Int.one_mul]; omega
  omega

theorem parallelogram_int_zero (f : Int → Int)
    (h : ∀ x y : Int, f (x + y) + f (x - y) = 2 * f x + 2 * f y) : f 0 = 0 := by
  have h00 := h 0 0
  simp at h00
  omega

theorem parallelogram_int_even (f : Int → Int)
    (h : ∀ x y : Int, f (x + y) + f (x - y) = 2 * f x + 2 * f y) :
    ∀ x : Int, f (-x) = f x := by
  intro x
  have h0 := parallelogram_int_zero f h
  have h1 := h 0 x
  simp at h1
  omega

theorem parallelogram_int_nat (f : Int → Int)
    (h : ∀ x y : Int, f (x + y) + f (x - y) = 2 * f x + 2 * f y) :
    ∀ n : Nat, f (n : Int) = (n : Int) * n * f 1 := by
  have h0 := parallelogram_int_zero f h
  have key : ∀ n : Nat, f (n : Int) = (n : Int) * n * f 1 ∧
      f ((n : Int) + 1) = ((n : Int) + 1) * ((n : Int) + 1) * f 1 := by
    intro n
    induction n with
    | zero => simp [h0]
    | succ n ih =>
      rw [Int.ofNat_succ]
      refine ⟨ih.2, ?_⟩
      have h1 := h ((n : Int) + 1) 1
      rw [Int.add_sub_cancel, ih.1, ih.2] at h1
      have s := sq_step (n : Int) (f 1)
      omega
  exact fun n => (key n).1

theorem parallelogram_int_quadratic (f : Int → Int)
    (h : ∀ x y : Int, f (x + y) + f (x - y) = 2 * f x + 2 * f y) :
    ∀ n : Int, f n = n * n * f 1 := by
  intro n
  rcases Int.eq_nat_or_neg n with ⟨k, hk | hk⟩
  · rw [hk]; exact parallelogram_int_nat f h k
  · rw [hk, parallelogram_int_even f h, Int.neg_mul_neg]
    exact parallelogram_int_nat f h k

/-- Result B, all three claims together. -/
theorem parallelogram_int (f : Int → Int)
    (h : ∀ x y : Int, f (x + y) + f (x - y) = 2 * f x + 2 * f y) :
    f 0 = 0 ∧ (∀ x : Int, f (-x) = f x) ∧ (∀ n : Int, f n = n * n * f 1) :=
  ⟨parallelogram_int_zero f h, parallelogram_int_even f h, parallelogram_int_quadratic f h⟩
#print axioms parallelogram_int
