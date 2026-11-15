import Std

/-! Three eight-tick flights on the 16-ring, starting at (site 0, rail R).
Every tick moves. A true coin applies an unnormalized H before the shift;
a false coin applies I. Divide state vectors by √2 per H. Only the sites at
ticks 1 and 9 are written. Their outcomes determine the source's private
basis and sign. This verifies finite instrumental amplitudes; sampling and
privacy of the two records are separate physical assumptions. -/

namespace FourLocalPreparations

abbrev Spin := Int × Int
abbrev Field := List Spin

def atSite (x : Nat) (s : Spin) : Field :=
  (List.range 16).map fun y => if x = y then s else (0,0)

def tick (f : Field) (h : Bool) : Field :=
  let g := f.map fun s => if h then (s.1+s.2, s.1-s.2) else s
  (List.range 16).map fun y => ((g[(y+15)%16]!).1, (g[(y+1)%16]!).2)

def coast (f : Field) : Field := (List.range 7).foldl (fun g _ => tick g false) f
def written (f : Field) (x : Nat) : Field := atSite x f[x]!
def launch := atSite 0 (1,0)

/-- False/true mean that the H tick was followed by a right/left displacement. -/
def firstWrite (firstLeft : Bool) : Field :=
  written (tick launch true) (if firstLeft then 15 else 1)

def secondWrite (firstLeft secondLeft : Bool) : Field :=
  written (tick (coast (firstWrite firstLeft)) true) (if secondLeft then 7 else 9)

/-- First sign picks the basis; the second selects its member. -/
def beforeRead (firstLeft secondLeft : Bool) : Field := coast (secondWrite firstLeft secondLeft)
def final (firstLeft secondLeft : Bool) : Field :=
  coast (tick (beforeRead firstLeft secondLeft) firstLeft)

def norm2 (f : Field) : Int := (f.map fun s => s.1*s.1 + s.2*s.2).sum
def axes : List Bool := [false,true]
def pairs : List (Bool × Bool) := axes.flatMap fun b => axes.map fun c => (b,c)

set_option maxRecDepth 8192

/-- Before each private write every occupied site is in the two named bins.
The H ticks contribute common squared denominators 2 then 4. -/
theorem private_records :
    norm2 (tick launch true) = 2 ∧
    axes.map (fun b => norm2 (firstWrite b)) = [1,1] ∧
    axes.map (fun b => norm2 (tick (coast (firstWrite b)) true)) = [2,2] ∧
    pairs.map (fun p => norm2 (secondWrite p.1 p.2)) = [1,1,1,1] ∧
    coast (firstWrite false) = atSite 8 (1,0) ∧
    coast (firstWrite true) = atSite 8 (0,1) := by decide

/-- Matrices act on unnormalized paths. With two total H ticks in the first
two cases and three in the last two, each output has squared weight 1/4. -/
theorem four_at_one_site :
    beforeRead false false = atSite 0 (1,0) ∧
    beforeRead false true = atSite 0 (0,1) ∧
    beforeRead true false = atSite 0 (1,0) ∧
    beforeRead true true = atSite 0 (0,-1) ∧
    final false false = atSite 8 (1,0) ∧
    final false true = atSite 8 (0,1) ∧
    final true false = atSite 8 (1,1) ∧
    final true true = atSite 8 (-1,1) := by decide

/-- Unread projective record immediately after tick 17, in the X basis
preparation. Its orthogonal classical branches are subsequently added as
density matrices. For real amplitudes store (RR, RL, LL) of the density. -/
abbrev Density := Int × Int × Int
def outer (s : Spin) : Density := (s.1*s.1, s.1*s.2, s.2*s.2)

def extraWriteEffects (secondLeft : Bool) : List Density :=
  let f := tick (beforeRead true secondLeft) true
  [1,15].map fun x => outer ((coast (written f x))[8]!)

theorem extra_position_copy :
    pairs.map (fun p => norm2 (final p.1 p.2)) = [1,1,2,2] ∧
    axes.map (fun c => outer ((final true c)[8]!)) = [(1,1,1),(1,-1,1)] ∧
    axes.map extraWriteEffects = [[(1,0,0),(0,0,1)],[(1,0,0),(0,0,1)]] := by decide

end FourLocalPreparations

#print axioms FourLocalPreparations.private_records
#print axioms FourLocalPreparations.four_at_one_site
#print axioms FourLocalPreparations.extra_position_copy
