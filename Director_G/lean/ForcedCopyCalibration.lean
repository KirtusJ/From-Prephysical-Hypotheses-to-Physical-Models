import Std

/-! Finite Boolean forced-copy panels. A bit is true if that boundary
stores a copy. Outside the queried coordinates the experimenter has
already forced all copies, so a single kernel K on the selected bits
includes that fixed outside setting. Raw weights and scores can be
integer-scaled; no independence across copies is used. -/
namespace ForcedCopyCalibration

def Bits : Nat → Type
  | 0 => Unit
  | n+1 => Bool × Bits n

def unionBits : (n : Nat) → Bits n → Bits n → Bits n
  | 0, _, _ => ()
  | n+1, (a,x), (b,y) => (a || b, unionBits n x y)

def clear : (n : Nat) → Bits n → Bool
  | 0, _ => true
  | n+1, (a,x) => !a && clear n x

/-- Alternating sum over forced masks, with the unforced setting positive. -/
def contrast : (n : Nat) → (Bits n → Int) → Int
  | 0, f => f ()
  | n+1, f =>
    contrast n (fun y => f (false,y)) - contrast n (fun y => f (true,y))

/-- A latent copy on any queried bit pairs equal observations with opposite signs. -/
theorem fixed_latent (n : Nat) (x : Bits n) (K : Bits n → Int) :
    contrast n (fun f => K (unionBits n x f)) =
      if clear n x then contrast n K else 0 := by
  induction n with
  | zero => rfl
  | succ n ih =>
    rcases x with ⟨a,x⟩
    cases a with
    | false =>
      change contrast n (fun y => K (false,unionBits n x y)) -
        contrast n (fun y => K (true,unionBits n x y)) =
        if clear n x then _ else _
      rw [ih x (fun y => K (false,y)), ih x (fun y => K (true,y))]
      cases clear n x <;> simp [contrast]
    | true => simp [contrast, unionBits, clear]

private theorem linear (n : Nat) (w : Int) (f g : Bits n → Int) :
    contrast n (fun y => w * f y + g y) = w * contrast n f + contrast n g := by
  induction n with
  | zero => rfl
  | succ n ih =>
    simp only [contrast]
    rw [ih (fun y => f (false,y)) (fun y => g (false,y)),
        ih (fun y => f (true,y)) (fun y => g (true,y)), Int.mul_sub]
    omega

private theorem zero_contrast (n : Nat) :
    contrast n (fun _ => 0) = 0 := by
  induction n with
  | zero => rfl
  | succ n ih => simp [contrast, ih]

def observed (n : Nat) (K : Bits n → Int) :
    List (Bits n × Nat) → Bits n → Int
  | [], _ => 0
  | (x,w)::xs, f => (w : Int) * K (unionBits n x f) + observed n K xs f

def clearWeight (n : Nat) : List (Bits n × Nat) → Int
  | [] => 0
  | (x,w)::xs => (if clear n x then (w : Int) else 0) + clearWeight n xs

/-- Measured contrast = raw mass of rows clear on the queried subset
times the same clean apparatus contrast. Other coordinates and latent
correlations can be summed into the list, including repeated bit masks. -/
theorem measured_contrast (n : Nat) (K : Bits n → Int) (xs : List (Bits n × Nat)) :
    contrast n (observed n K xs) = clearWeight n xs * contrast n K := by
  induction xs with
  | nil => simp [observed, clearWeight, zero_contrast]
  | cons row rest ih =>
    rcases row with ⟨x,w⟩
    change contrast n (fun f => (w : Int)*K (unionBits n x f) + observed n K rest f) = _
    rw [linear n (w : Int) (fun f => K (unionBits n x f)) (observed n K rest),
        fixed_latent, ih]
    cases eq : clear n x <;> simp [clearWeight, eq, Int.add_mul]

/-- A bounded reading on at least one queried bit has absolute contrast
at most 2^(number of bits − 1) times its full score range. -/
theorem bounded_contrast (n : Nat) (D : Int) (K : Bits (n+1) → Int)
    (range : ∀ f, 0 ≤ K f ∧ K f ≤ D) :
    -(2^n * D) ≤ contrast (n+1) K ∧ contrast (n+1) K ≤ 2^n * D := by
  induction n with
  | zero =>
    have h0 := range (false, ())
    have h1 := range (true, ())
    simp [contrast]
    omega
  | succ n ih =>
    have lo := ih (fun y => K (false,y)) (fun y => range (false,y))
    have hi := ih (fun y => K (true,y)) (fun y => range (true,y))
    change -(2^(n+1) * D) ≤ contrast (n+1) (fun y => K (false,y)) -
      contrast (n+1) (fun y => K (true,y)) ∧
      contrast (n+1) (fun y => K (false,y)) -
      contrast (n+1) (fun y => K (true,y)) ≤ 2^(n+1) * D
    rw [Int.pow_succ, Int.mul_comm (2^n) 2, Int.mul_assoc]
    omega

/-- The full Boolean difference of the values on submasks of x. -/
def inverse : (n : Nat) → Bits n → (Bits n → Int) → Int
  | 0, _, f => f ()
  | n+1, (false,x), f => inverse n x (fun y => f (false,y))
  | n+1, (true,x), f =>
    inverse n x (fun y => f (true,y)) - inverse n x (fun y => f (false,y))

/-- Summing the recovered single-mask coefficients on all submasks. -/
def subtotal : (n : Nat) → Bits n → (Bits n → Int) → Int
  | 0, _, f => f ()
  | n+1, (false,x), f => subtotal n x (fun y => f (false,y))
  | n+1, (true,x), f =>
    subtotal n x (fun y => f (false,y)) + subtotal n x (fun y => f (true,y))

/-- Cumulative probabilities P(X ⊆ S), obtained by querying clear bits
outside S, recover every atom P(X = S) by the Boolean inverse. -/
theorem recover_atoms (n : Nat) (x : Bits n) (p : Bits n → Int) :
    inverse n x (fun s => subtotal n s p) = p x := by
  induction n with
  | zero => cases x; rfl
  | succ n ih =>
    rcases x with ⟨b,x⟩
    cases b with
    | false => exact ih x (fun y => p (false,y))
    | true =>
      simp only [inverse, subtotal]
      have additivity (f g : Bits n → Int) :
          inverse n x (fun y => f y + g y) = inverse n x f + inverse n x g := by
        clear ih p
        induction n with
        | zero => rfl
        | succ n rec =>
          rcases x with ⟨a,x⟩
          cases a with
          | false => exact rec x _ _
          | true =>
            simp only [inverse]
            rw [rec x (fun y => f (true,y)) (fun y => g (true,y)),
                rec x (fun y => f (false,y)) (fun y => g (false,y))]
            omega
      rw [additivity, ih x (fun y => p (false,y)), ih x (fun y => p (true,y))]
      omega

end ForcedCopyCalibration
