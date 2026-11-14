import Std

/-! One position-only pulse on an unwrapped sharp walk. Coordinates are the
deficit (time - position)/2 relative to the left wall, from 0 to 4. A right
step leaves the deficit unchanged; a left step increments it. A mask tests
only the new deficit, equally for both arrival rails. Counts record positive
and negative words separately, including when their difference vanishes. -/
namespace PositionMaskPulse

abbrev Counts := Nat × Nat
abbrev Rails := Counts × Counts
structure Field where
  wall0 : Rails
  at1 : Rails
  at2 : Rails
  at3 : Rails
  wall4 : Rails

def zero : Counts := (0,0)
def add (a b : Counts) : Counts := (a.1+b.1, a.2+b.2)
def swap (a : Counts) : Counts := (a.2,a.1)
def empty : Rails := (zero,zero)

def landing (d : Nat) (allowed : List Nat) (here west : Rails) : Rails :=
  if d ∈ allowed then (add here.1 here.2, add west.1 (swap west.2))
  else empty

def tick (allowed : List Nat) (s : Field) : Field :=
  ⟨landing 0 allowed s.wall0 empty, landing 1 allowed s.at1 s.wall0,
   landing 2 allowed s.at2 s.at1, landing 3 allowed s.at3 s.at2,
   landing 4 allowed s.wall4 s.at3⟩

def walls (reservoir accumulator : Counts) : Field :=
  ⟨(reservoir,zero),empty,empty,empty,(accumulator,zero)⟩

/-- Each list element enables one interior position for that tick. Two
wall-only ticks then land the pulse on the L rail and merge it into R. -/
def pulse (interior : List Nat) (f : Field) : Field :=
  let moving := interior.foldl (fun state d => tick [0,4,d] state) f
  tick [0,4] (tick [0,4] moving)

theorem negative_pulse (p q a b : Nat) :
    pulse [1,2,3] (walls (p,q) (a,b)) = walls (p,q) (a+q,b+p) := by
  simp [pulse, List.foldl, tick, landing, walls, empty, add, swap, zero]

theorem positive_pulse (p q a b : Nat) :
    pulse [1,2,2,3] (walls (p,q) (a,b)) = walls (p,q) (a+p,b+q) := by
  simp [pulse, List.foldl, tick, landing, walls, empty, add, swap, zero]

end PositionMaskPulse
