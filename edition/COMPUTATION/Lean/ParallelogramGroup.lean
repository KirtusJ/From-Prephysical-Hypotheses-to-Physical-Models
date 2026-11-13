/-! Result C: the parallelogram law on an abelian group, with values in `Int`. -/

/-- A minimal additive abelian group: zero, addition, negation and the usual axioms. -/
class AbGroup (G : Type) where
  zero : G
  add : G → G → G
  neg : G → G
  add_assoc : ∀ x y z : G, add (add x y) z = add x (add y z)
  add_comm : ∀ x y : G, add x y = add y x
  add_zero : ∀ x : G, add x zero = x
  add_neg : ∀ x : G, add x (neg x) = zero

namespace AbGroup

variable {G : Type} [AbGroup G]

instance : Add G := ⟨AbGroup.add⟩
instance : Neg G := ⟨AbGroup.neg⟩
instance : OfNat G 0 := ⟨AbGroup.zero⟩

theorem add_assoc' (x y z : G) : (x + y) + z = x + (y + z) := AbGroup.add_assoc x y z
theorem add_comm' (x y : G) : x + y = y + x := AbGroup.add_comm x y
theorem add_zero' (x : G) : x + 0 = x := AbGroup.add_zero x
theorem add_neg' (x : G) : x + -x = 0 := AbGroup.add_neg x

theorem zero_add' (x : G) : 0 + x = x := by rw [add_comm', add_zero']
theorem neg_add_self (x : G) : -x + x = 0 := by rw [add_comm', add_neg']

theorem neg_unique (a b : G) (h : a + b = 0) : b = -a := by
  calc b = 0 + b := (zero_add' b).symm
    _ = (-a + a) + b := by rw [neg_add_self]
    _ = -a + (a + b) := add_assoc' _ _ _
    _ = -a + 0 := by rw [h]
    _ = -a := add_zero' _

theorem neg_neg' (x : G) : -(-x) = x := (neg_unique (-x) x (neg_add_self x)).symm

theorem add_right_comm' (a b c : G) : (a + b) + c = (a + c) + b := by
  rw [add_assoc', add_comm' b c, ← add_assoc']

theorem add_add_add_comm' (a b c d : G) : (a + b) + (c + d) = (a + c) + (b + d) := by
  calc (a + b) + (c + d) = a + (b + (c + d)) := add_assoc' _ _ _
    _ = a + ((b + c) + d) := by rw [add_assoc' b c d]
    _ = a + ((c + b) + d) := by rw [add_comm' b c]
    _ = a + (c + (b + d)) := by rw [add_assoc' c b d]
    _ = (a + c) + (b + d) := (add_assoc' _ _ _).symm

theorem neg_add' (x y : G) : -(x + y) = -x + -y := by
  apply Eq.symm
  apply neg_unique
  rw [add_add_add_comm', add_neg', add_neg', add_zero']

theorem neg_zero' : -(0 : G) = 0 := by
  have h := add_neg' (0 : G)
  rw [zero_add'] at h
  exact h

/-- `B x y = f (x + y) - f (x - y)`, four times the associated bilinear form. -/
def B (f : G → Int) (x y : G) : Int := f (x + y) - f (x + -y)

section Parallelogram

variable (f : G → Int)
  (h : ∀ x y : G, f (x + y) + f (x + -y) = 2 * f x + 2 * f y)
include h

/-- (1) -/
theorem f_zero : f 0 = 0 := by
  have h00 := h 0 0
  rw [neg_zero', add_zero'] at h00
  omega

/-- (2) -/
theorem f_neg (y : G) : f (-y) = f y := by
  have h0 := f_zero f h
  have h1 := h 0 y
  rw [zero_add', zero_add'] at h1
  omega

/-- (3) -/
theorem f_double (x : G) : f (x + x) = 4 * f x := by
  have h0 := f_zero f h
  have h1 := h x x
  rw [add_neg'] at h1
  omega

/-- (4) -/
theorem B_symm (x y : G) : B f x y = B f y x := by
  have e : y + -x = -(x + -y) := by rw [neg_add', neg_neg', add_comm']
  unfold B
  rw [e, f_neg f h, add_comm' y x]

/-- (5) -/
theorem B_self (x : G) : B f x x = 4 * f x := by
  unfold B
  rw [add_neg', f_zero f h, f_double f h]
  omega

/-- Key identity: `B (x + z) y + B (x - z) y = 2 * B x y`. -/
theorem B_key (x y z : G) : B f (x + z) y + B f (x + -z) y = 2 * B f x y := by
  have h1 := h (x + y) z
  have h2 := h (x + -y) z
  rw [add_right_comm' x y z, add_right_comm' x y (-z)] at h1
  rw [add_right_comm' x (-y) z, add_right_comm' x (-y) (-z)] at h2
  unfold B
  omega

theorem B_zero_left (y : G) : B f 0 y = 0 := by
  unfold B
  rw [zero_add', zero_add', f_neg f h]
  omega

theorem B_double_left (x y : G) : B f (x + x) y = 2 * B f x y := by
  have k := B_key f h x y x
  rw [add_neg', B_zero_left f h] at k
  omega

/-- (6) additivity in the first argument. -/
theorem B_add_left (u v y : G) : B f (u + v) y = B f u y + B f v y := by
  have k := B_key f h (u + v) y (u + -v)
  have e1 : (u + v) + (u + -v) = u + u := by
    rw [add_add_add_comm', add_neg', add_zero']
  have e2 : (u + v) + -(u + -v) = v + v := by
    rw [neg_add', neg_neg', add_add_add_comm', add_neg', zero_add']
  rw [e1, e2, B_double_left f h, B_double_left f h] at k
  omega

end Parallelogram

end AbGroup

/-- Result C, all six claims together (`x - y` is written `x + -y`). -/
theorem parallelogram_group {G : Type} [AbGroup G] (f : G → Int)
    (h : ∀ x y : G, f (x + y) + f (x + -y) = 2 * f x + 2 * f y) :
    f 0 = 0 ∧
    (∀ y : G, f (-y) = f y) ∧
    (∀ x : G, f (x + x) = 4 * f x) ∧
    (∀ x y : G, AbGroup.B f x y = AbGroup.B f y x) ∧
    (∀ x : G, AbGroup.B f x x = 4 * f x) ∧
    (∀ u v y : G, AbGroup.B f (u + v) y = AbGroup.B f u y + AbGroup.B f v y) :=
  ⟨AbGroup.f_zero f h, AbGroup.f_neg f h, AbGroup.f_double f h, AbGroup.B_symm f h,
   AbGroup.B_self f h, AbGroup.B_add_left f h⟩

#print axioms parallelogram_group
