import Std

/-!
For an oriented monomial in the formal Laurent expansion, x is +1 for a
positive power and -1 for a negative power. The two components below sum
products over the even and odd subsets. Including the next angle changes
the subset parity. The proof works for arbitrary integer coefficients.
-/
namespace PairedCharacterExpansion

def paritySums : List Int → Int × Int
  | [] => (1, 0)
  | x :: xs =>
    let (e, o) := paritySums xs
    (e + x * o, o + x * e)

def productOf (f : Int → Int) : List Int → Int
  | [] => 1
  | x :: xs => f x * productOf f xs

theorem signedProducts (xs : List Int) :
    (paritySums xs).1 + (paritySums xs).2 = productOf (fun x => 1 + x) xs ∧
    (paritySums xs).1 - (paritySums xs).2 = productOf (fun x => 1 - x) xs := by
  induction xs with
  | nil => decide
  | cons x xs ih =>
    obtain ⟨hp, hm⟩ := ih
    simp only [productOf, paritySums, ← hp, ← hm]
    generalize paritySums xs = p
    obtain ⟨e, o⟩ := p
    simp only [Int.add_mul, Int.sub_mul, Int.one_mul, Int.mul_add, Int.mul_sub]
    constructor <;> omega

theorem evenMonomialCoefficient (xs : List Int) :
    2 * (paritySums xs).1 = productOf (fun x => 1 + x) xs +
      productOf (fun x => 1 - x) xs := by
  obtain ⟨hp, hm⟩ := signedProducts xs
  omega

end PairedCharacterExpansion
