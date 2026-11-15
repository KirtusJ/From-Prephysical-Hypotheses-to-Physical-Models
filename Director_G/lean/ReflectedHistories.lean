import Std

namespace ReflectedHistories

abbrev Rail := Int × Int

/-- The first output rail arrives from the left unless it is reflected at well zero.
Each mask acts on the two rails together. Amplitudes omit the common Hadamard factor. -/
def step (wells : Nat) (state : Nat → Rail) (x : Nat) : Rail :=
  let (a, b) := state (x - 1)
  let (c, d) := state (min (x+1) (wells-1))
  (if x = 0 then a-b else a+b, if x+1 = wells then c+d else c-d)

def fly (wells : Nat) : Nat → (Nat → Rail) → Nat → Rail
  | 0, state => state
  | t+1, state => step wells (fly wells t state)

def mask (wells bit : Nat) (state : Nat → Rail) (x : Nat) : Rail :=
  if (if 2*x+1 < wells then 0 else 1) = bit then state x else (0,0)

def source (x : Nat) : Rail := if x = 1 then (1,0) else (0,0)

def mass (wells : Nat) (state : Nat → Rail) : Int :=
  ((List.range wells).map fun x =>
    let (r,l) := state x
    r*r+l*l).sum

def history (a b c : Nat) : Int :=
  let one := mask 4 a (fly 4 2 source)
  let two := mask 4 b (fly 4 2 one)
  mass 4 (mask 4 c (fly 4 4 two))

theorem four_well_words :
    [history 0 0 0, history 0 0 1, history 0 1 0, history 0 1 1,
     history 1 0 0, history 1 0 1, history 1 1 0, history 1 1 1] =
    [100,12,20,60,12,4,28,20] := by native_decide

def coinEffect (x : Nat) : Int × Int × Int :=
  let r := fly 6 3 (fun j => if j = 0 then (1,0) else (0,0)) x
  let l := fly 6 3 (fun j => if j = 0 then (0,1) else (0,0)) x
  (r.1*r.1+r.2*r.2, l.1*l.1+l.2*l.2, r.1*l.1+r.2*l.2)

theorem endpoint_coin_effects :
    (List.range 6).map coinEffect = [(1,5,-1),(5,1,1),(1,1,-1),(1,1,1),(0,0,0),(0,0,0)] :=
  by native_decide

end ReflectedHistories
