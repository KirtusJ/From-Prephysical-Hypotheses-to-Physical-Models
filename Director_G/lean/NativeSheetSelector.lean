import Std

/-! Word-level covariance of a signed Hadamard flight from a sharp port.
True denotes L. Gains are on departure sites on the integer covering
line. The staircase is well-defined modulo M on the 4M-site ring. -/
namespace NativeSheetSelector

def delta : Bool → Int | false => 1 | true => -1

def displacement (w : List Bool) : Int := (w.map delta).sum

def sign (source : Bool) : List Bool → Int
  | [] => 1
  | b :: bs => (if source && b then -1 else 1) * sign b bs

def finalRail (source : Bool) : List Bool → Bool
  | [] => source
  | b :: bs => finalRail b bs

def railGauge : Bool → Int | false => 1 | true => -1

theorem reflect_displacement (w : List Bool) :
    displacement (w.map (! ·)) = -displacement w := by
  induction w with
  | nil => rfl
  | cons b bs ih =>
    simp only [displacement,List.map_cons,List.sum_cons] at ih ⊢
    rw [ih]; cases b <;> simp [delta] <;> omega

theorem reflect_final (w : List Bool) (s : Bool) :
    finalRail (!s) (w.map (! ·)) = !(finalRail s w) := by
  induction w generalizing s with
  | nil => rfl
  | cons b bs ih => exact ih b

/-- All histories with the same time and endpoint rail pick up the
same sign when both the initial rail and all subsequent rails flip. -/
theorem reflect_sign (w : List Bool) (s : Bool) :
    sign (!s) (w.map (! ·)) =
    ((-1:Int)^w.length)*railGauge s*railGauge (finalRail s w)*sign s w := by
  induction w generalizing s with
  | nil => cases s <;> decide
  | cons b bs ih =>
    simp only [List.map_cons,sign,List.length_cons,finalRail,ih,Int.pow_succ]
    cases s <;> cases b <;> simp [railGauge,Int.mul_assoc,Int.neg_mul,Int.mul_neg]

/-- A departure trajectory in the lift, started at zero; its parity
at each time j agrees with the clock. -/
def alternating (y : Nat → Int) := ∀ j, y j % 2 = (j:Int)%2

def gain (x : Nat → Int) : Nat → Int
  | 0 => 0
  | t+1 => gain x t+x t/2

def translateOffset (a : Int) : Nat → Int
  | 0 => 0
  | t+1 => translateOffset a t+(a+(t:Int)%2)/2
def reflectOffset (a : Int) : Nat → Int
  | 0 => 0
  | t+1 => reflectOffset a t+(a-(t:Int)%2)/2

theorem translate_gain (a : Int) (y : Nat → Int) (parity : alternating y) (t : Nat) :
    gain (fun j => a+y j) t = translateOffset a t+gain y t := by
  induction t with
  | zero => rfl
  | succ j ih =>
    have p := parity j
    simp only [gain,translateOffset,ih]
    omega

theorem reflect_gain (a : Int) (y : Nat → Int) (parity : alternating y) (t : Nat) :
    gain (fun j => a-y j) t + gain y t = reflectOffset a t := by
  induction t with
  | zero => rfl
  | succ j ih =>
    have p := parity j
    simp only [gain,reflectOffset]
    omega

def track (x : Int) : List Bool → Int
  | [] => x
  | b :: bs => track (x+delta b) bs

/-- Both native steps switch site parity. -/
theorem track_parity (x : Int) (w : List Bool) :
    track x w % 2 = (x+(w.length:Int)) % 2 := by
  induction w generalizing x with
  | nil => simp [track]
  | cons b bs ih =>
    simp only [track,ih,List.length_cons,Int.natCast_succ]
    cases b <;> simp only [delta] <;> omega

/-- A base winding changes only the choice of sheet representative. -/
theorem ring_gain (x M q : Int) :
    (x+4*M*q)/2 = x/2 + 2*M*q := by
  have h : 4*M*q = 2*(2*M*q) := by
    simp only [←Int.mul_assoc]
    rfl
  rw [h]
  omega

end NativeSheetSelector
