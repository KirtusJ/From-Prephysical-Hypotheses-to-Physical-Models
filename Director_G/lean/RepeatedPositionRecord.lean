import Std

/-! A three-tick product of position masks, with integer counts of positive
and negative words at each arrival rail. Translation is performed on the
integer line. No rail or first-direction observation is made within the
admitted positions. -/
namespace RepeatedPositionRecord

abbrev Counts := Nat × Nat
abbrev Rails := Counts × Counts
abbrev Field := Int → Rails

def zero : Counts := (0, 0)
def empty : Rails := (zero, zero)
def add (u v : Counts) : Counts := (u.1 + v.1, u.2 + v.2)
def flip (u : Counts) : Counts := (u.2, u.1)

def tick (f : Field) (x : Int) : Rails :=
  (add (f (x-1)).1 (f (x-1)).2, add (f (x+1)).1 (flip (f (x+1)).2))

def keep (site : Int) (f : Field) (x : Int) : Rails :=
  if x = site then f x else empty

def source (site : Int) (p q : Nat) (x : Int) : Rails :=
  if x = site then ((p, q), zero) else empty

def block (site : Int) (f : Field) : Field :=
  keep (site+1) (tick (keep site (tick (tick f))))

theorem one_block (site : Int) (p q : Nat) :
    block site (source site p q) = source (site+1) (2*p) (2*q) := by
  funext x
  by_cases hx : x = site + 1
  · subst x
    have left : site-1-1 ≠ site := by omega
    have right : site+1+1 ≠ site := by omega
    simp [block, keep, tick, source, empty, zero, add, flip, left, right,
      Nat.two_mul]
  · simp [block, keep, source, hx]

def repeatBlocks (site : Int) (f : Field) : Nat → Field
  | 0 => f
  | k+1 => block (site+(k:Int)) (repeatBlocks site f k)

theorem repeated (site : Int) (p q k : Nat) :
    repeatBlocks site (source site p q) k =
      source (site+(k:Int)) (2^k*p) (2^k*q) := by
  induction k with
  | zero => simp [repeatBlocks]
  | succ k ih =>
    rw [repeatBlocks, ih, one_block]
    simp [Nat.pow_succ, Int.natCast_succ, Int.add_assoc, Nat.mul_assoc,
      Nat.mul_left_comm, Nat.mul_comm]

theorem total_and_signed (p q k : Nat) :
    2^k*p + 2^k*q = 2^k*(p+q) ∧
    (2:Int)^k*p - (2:Int)^k*q = (2:Int)^k*((p:Int)-q) := by
  exact ⟨(Nat.mul_add ..).symm, (Int.mul_sub ..).symm⟩

/-- For unnormalized mixture weights a and c and one-block retention
scores u and v, the cross-multiplied second moment excess is a*c*(u-v)^2.
Dividing by (a+c)^2 is valid when total weight is nonzero. -/
theorem mixture_excess (a c u v : Int) :
    (a+c)*(a*u*u+c*v*v) - (a*u+c*v)*(a*u+c*v) = a*c*((u-v)*(u-v)) := by
  simp only [Int.add_mul, Int.mul_add, Int.sub_mul, Int.mul_sub]
  simp only [Int.mul_assoc, Int.mul_left_comm, Int.mul_comm]
  omega

end RepeatedPositionRecord
