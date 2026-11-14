import Std

/-! A closed position record for the twelve-tick H/I walk on the 16-site ring.
Enumerate signed paths independently for both input rails. At a written
displacement both output rails are kept. Integer amplitudes omit the common
factor (1/√2)^7 in each block. See ScalarPositionBlock.lean for all effects. -/

namespace ClosedPositionTransport

inductive Coin | H | I deriving DecidableEq
open Coin

def schedule : List Coin := [H,H,H,I,I,H,I,H,H,I,I,H]

/-- L is true. The signed contribution of each path has magnitude one. -/
structure Path where
  x : Nat
  left : Bool
  sign : Int

def move (p : Path) (left : Bool) (sign : Int) : Path :=
  ⟨(p.x + (if left then 15 else 1)) % 16, left, sign⟩

def extend (op : Coin) (p : Path) : List Path :=
  match op with
  | I => [move p p.left p.sign]
  | H => [move p false p.sign, move p true (if p.left then -p.sign else p.sign)]

def paths (inLeft : Bool) : List Path :=
  schedule.foldl (fun ps op => ps.flatMap (extend op)) [⟨0, inLeft, 1⟩]

def entry (x : Nat) (outLeft inLeft : Bool) : Int :=
  (paths inLeft).foldl
    (fun total p => if p.x == x && p.left == outLeft then total + p.sign else total) 0

abbrev Column := Int × Int
abbrev Matrix := (Int × Int) × (Int × Int)

def block (x : Nat) : Matrix :=
  ((entry x false false, entry x false true), (entry x true false, entry x true true))

def applyMatrix (m : Matrix) (u : Column) : Column :=
  (m.1.1*u.1 + m.1.2*u.2, m.2.1*u.1 + m.2.2*u.2)

def multiply (a b : Matrix) : Matrix :=
  let c := applyMatrix a (b.1.1, b.2.1)
  let d := applyMatrix a (b.1.2, b.2.2)
  ((c.1, d.1), (c.2, d.2))

/-- Displacements in time order; every position is relative to the preceding write. -/
def word : List Nat := [2,8,14,8]

def positions (x : Nat) : List Nat → List Nat
  | [] => [x]
  | d::ds => x :: positions ((x+d)%16) ds

def rawTransport : Matrix :=
  word.foldl (fun m x => multiply (block x) m) ((1,0),(0,1))

def rotor : Matrix := ((63,-16),(16,63))

def gram (m : Matrix) : Matrix :=
  multiply ((m.1.1, m.2.1), (m.1.2, m.2.2)) m

set_option maxRecDepth 8000 in
set_option maxHeartbeats 2000000 in
theorem native_closed_word :
    positions 0 word = [0,2,10,8,0] ∧
    block 2 = ((-1,-3),(-3,1)) ∧ block 14 = block 2 ∧
    block 8 = ((1,5),(5,-1)) ∧
    rawTransport = multiply ((4,0),(0,4)) rotor := by decide

theorem positive_normalization :
    gram rotor = ((65^2, 0), (0, 65^2)) ∧
    (4*65 : Int)^2 = 10*26*10*26 := by decide

/-- First column numerator of the nth power of rotor / 65. The positive
denominator is 65^n and does not affect which entries vanish. -/
def powerColumn : Nat → Column
  | 0 => (1,0)
  | n+1 => applyMatrix rotor (powerColumn n)

/-- The Gaussian pair (3,1) is idempotent modulo 5. -/
theorem power_residues (n : Nat) :
    (powerColumn (n+1)).1 % 5 = 3 ∧ (powerColumn (n+1)).2 % 5 = 1 := by
  induction n with
  | zero => decide
  | succ n ih =>
    change (63 * (powerColumn (n+1)).1 + (-16) * (powerColumn (n+1)).2) % 5 = 3 ∧
      (16 * (powerColumn (n+1)).1 + 63 * (powerColumn (n+1)).2) % 5 = 1
    rcases ih with ⟨ha,hb⟩
    constructor
    · rw [Int.add_emod, Int.mul_emod 63, Int.mul_emod (-16), ha, hb]
      decide
    · rw [Int.add_emod, Int.mul_emod 16, Int.mul_emod 63, ha, hb]
      decide

/-- No positive repetition sends the first basis rail back to its ray.
Consequently no such power can be a scalar (and in particular not ±I). -/
theorem every_repeat_mixes (n : Nat) : (powerColumn (n+1)).2 ≠ 0 := by
  have h := (power_residues n).2
  intro eq
  rw [eq] at h
  contradiction

end ClosedPositionTransport
