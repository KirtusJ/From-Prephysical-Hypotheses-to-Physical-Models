/-! The functional equation `f (a + 2b) + 2 f (a - b) = 3 f a + 6 f b` on an abelian group
(values in `Int`) implies the parallelogram law. -/

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

/-- `b + (-b + c) = c`. -/
theorem add_neg_cancel_left' (b c : G) : b + (-b + c) = c := by
  rw [← add_assoc', add_neg', zero_add']

section ThreeLaw

variable (f : G → Int)
  (H : ∀ a b : G, f (a + (b + b)) + 2 * f (a + -b) = 3 * f a + 6 * f b)
include H

theorem three_f_zero : f 0 = 0 := by
  have h := H 0 0
  rw [add_zero', add_zero', add_neg'] at h
  omega

/-- Evenness, from the instances `H 0 b` and `H b (-b)`. -/
theorem three_f_neg (b : G) : f (-b) = f b := by
  have h0 := three_f_zero f H
  have h1 := H 0 b
  rw [zero_add', zero_add'] at h1
  have h2 := H b (-b)
  rw [add_neg_cancel_left', neg_neg'] at h2
  omega

/-- Parallelogram law, from the instances `H a b` and `H (a + b) (-b)`. -/
theorem three_parallelogram (a b : G) :
    f (a + b) + f (a + -b) = 2 * f a + 2 * f b := by
  have hn := three_f_neg f H b
  have h1 := H a b
  have h2 := H (a + b) (-b)
  rw [add_assoc' a b (-b + -b), add_neg_cancel_left', neg_neg', add_assoc' a b b] at h2
  omega

end ThreeLaw

end AbGroup

/-- Main theorem (no evenness hypothesis needed; `x - y` is written `x + -y`). -/
theorem three_law {G : Type} [AbGroup G] (f : G → Int)
    (H : ∀ a b : G, f (a + (b + b)) + 2 * f (a + -b) = 3 * f a + 6 * f b) :
    ∀ a b : G, f (a + b) + f (a + -b) = 2 * f a + 2 * f b :=
  AbGroup.three_parallelogram f H

#print axioms three_law
