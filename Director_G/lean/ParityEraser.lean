import Std

/-! Raw, unnormalized signed rails on the integer line. One common
normalizing factor per Hadamard tick can be restored after these identities. -/
namespace ParityEraser

abbrev Rails := Int × Int
abbrev Field := Int → Rails

def flight (v : Field) (x : Int) : Rails :=
  ((v (x - 1)).1 + (v (x - 1)).2, (v (x + 1)).1 - (v (x + 1)).2)

/-- Reflection about the launch site zero combined with J(r,l)=(-l,r). -/
def reflect (v : Field) (x : Int) : Rails := (-(v (-x)).2, (v (-x)).1)

def scale (a : Int) (v : Field) (x : Int) : Rails := (a * (v x).1, a * (v x).2)

theorem flight_scale (a : Int) (v : Field) : flight (scale a v) = scale a (flight v) := by
  funext x
  simp [flight, scale, Int.mul_add, Int.mul_sub]

theorem reflect_one (v : Field) : flight (reflect v) = scale (-1) (reflect (flight v)) := by
  funext x
  have h₁ : -(x-1) = -x+1 := by omega
  have h₂ : -(x+1) = -x-1 := by omega
  apply Prod.ext <;> simp [flight, reflect, scale, h₁, h₂] <;> omega

def walk : Nat → Field → Field
  | 0, v => v
  | n+1, v => flight (walk n v)

theorem reflect_all (n : Nat) (v : Field) :
    walk n (reflect v) = scale ((-1 : Int)^n) (reflect (walk n v)) := by
  induction n with
  | zero => funext x; simp [walk, scale]
  | succ n ih =>
    rw [walk, ih, flight_scale, reflect_one, walk, Int.pow_succ]
    funext x
    simp [scale, Int.mul_neg, Int.neg_mul]

/-- Left and right cells respectively contain the two old rails of tag 0
and of tag 1. Exchange (left,L) and (right,R). -/
def transposeDimer (d : Rails × Rails) : Rails × Rails :=
  ((d.1.1, d.2.1), (d.1.2, d.2.2))

theorem transpose_twice (d : Rails × Rails) : transposeDimer (transposeDimer d) = d := rfl

def had (v : Rails) : Rails := (v.1 + v.2, v.1 - v.2)

/-- Read back the two sites after locally mixing and undoing the stream
and the transposition. Left output has the two sums, right the differences. -/
theorem dimer_all (a b c d : Int) :
    let paired := transposeDimer ((a,b),(c,d))
    transposeDimer (had paired.1, had paired.2) = ((a+c,b+d),(a-c,b-d)) := rfl

/-- It suffices to know the two local pairs after transposition. Values
outside the dimer are arbitrary and cannot influence these four ports. -/
theorem terminal_ports (v : Field) (x a b c d : Int)
    (left : v x = (a,c)) (right : v (x+1) = (b,d)) :
    (flight v (x+1)).1 = a+c ∧ (flight v (x-1)).2 = a-c ∧
    (flight v (x+2)).1 = b+d ∧ (flight v x).2 = b-d := by
  have h₁ : x+1-1 = x := by omega
  have h₂ : x-1+1 = x := by omega
  have h₃ : x+2-1 = x+1 := by omega
  simp [flight, h₁, h₂, h₃, left, right]

/-- Flipping the first right arm after the first coin gives the negative
of interchanging the initial rails before it. Streaming preserves this equality. -/
theorem first_arm_sign (r l : Int) :
    (-((had (r,l)).1), (had (r,l)).2) = (-((had (l,r)).1), -((had (l,r)).2)) := by
  apply Prod.ext <;> simp [had] <;> omega

end ParityEraser
