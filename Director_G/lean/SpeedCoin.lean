import Std

namespace SpeedCoin

/-- A symmetric integer matrix acting on the two incoming rails. -/
def applySymmetric (a b d : Int) (v : Int × Int) : Int × Int :=
  (a * v.1 + b * v.2, b * v.1 + d * v.2)

def quarterTurn (v : Int × Int) : Int × Int := (-v.2, v.1)

/-- Commutation on the first basis vector alone forces an integer symmetric
    two-rail matrix to have zero off-diagonals and equal diagonals. -/
theorem scalar_of_quarter_turn (a b d : Int)
    (h : applySymmetric a b d (quarterTurn (1, 0)) =
      quarterTurn (applySymmetric a b d (1, 0))) : b = 0 ∧ d = a := by
  have h₁ := congrArg Prod.fst h
  have h₂ := congrArg Prod.snd h
  simp [applySymmetric, quarterTurn] at h₁ h₂
  omega

/-- All proposed directions. False is right, true is left. -/
def paths : Nat → List (List Bool)
  | 0 => [[]]
  | n+1 => (paths n).flatMap fun w => [false :: w, true :: w]

/-- Signed integer path contribution at its final position and rail. -/
def walk (x : Int) (incoming : Bool) (sign : Int) : List Bool → (Int × Bool) × Int
  | [] => ((x, incoming), sign)
  | left :: rest =>
    walk (if left then x - 1 else x + 1) left
      (if incoming && left then -sign else sign) rest

def amplitude (source : Bool) (x : Int) (rail : Bool) : Int :=
  ((paths 8).map fun w =>
    let dest := walk 0 source 1 w
    if dest.1 == (x, rail) then dest.2 else 0).sum

/-- Count the center once. Away from zero both signed positions contribute. -/
def shell (radius : Nat) : List (Int × Bool) :=
  let x : Int := radius
  let sites := if radius == 0 then [x] else [x, -x]
  sites.flatMap fun site => [(site, false), (site, true)]

/-- Raw radial Gram entry. Division by 256 restores squared normalization. -/
def gram (radius : Nat) (sourceA sourceB : Bool) : Int :=
  ((shell radius).map fun (x, rail) =>
    amplitude sourceA x rail * amplitude sourceB x rail).sum

def radii : List Nat := [0, 2, 4, 6, 8]

def shellGrams : List (Int × Int × Int) := radii.map fun radius =>
  (gram radius false false, gram radius false true, gram radius true true)

/-- Both input columns and their cross term, for every occupied radius. -/
theorem eighth_tick_grams :
    shellGrams = [(18,0,18), (44,0,44), (116,0,116), (76,0,76), (2,0,2)] := by
  native_decide

def fairCounts (source : Bool) : List Nat := radii.map fun radius =>
  ((paths 8).filter (fun w => ((walk 0 source 1 w).1.1).natAbs == radius)).length

theorem eighth_tick_unsigned :
    fairCounts false = [70,112,56,16,2] ∧ fairCounts true = [70,112,56,16,2] := by
  native_decide

theorem all_paths_covered :
    (paths 8).length = 256 ∧
      [false,true].all (fun source => (paths 8).all (fun w =>
        radii.contains ((walk 0 source 1 w).1.1).natAbs)) = true := by
  native_decide

end SpeedCoin
