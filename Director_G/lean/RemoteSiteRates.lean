import Std

/-! Enumerate signed histories without a floating-point amplitude or probability. -/
namespace RemoteSiteRates

structure Path where
  x : Int
  left : Bool
  sign : Int

def children (marked : Bool) (clock : Nat) (address : Int)
    (now : Nat) (p : Path) : List Path :=
  let s := if marked && (clock == now) && (p.x == address) then -p.sign else p.sign
  [⟨p.x + 1, false, s⟩, ⟨p.x - 1, true, if p.left then -s else s⟩]

def paths (marked : Bool) (clock : Nat) (site : Int) : Nat → List Path
  | 0 => [⟨0, false, 1⟩]
  | t+1 => (paths marked clock site t).flatMap (children marked clock site t)

def total (ps : List Path) (x : Int) (left : Bool) : Int :=
  ((ps.filter (fun p => p.x == x && p.left == left)).map Path.sign).sum

def panel (ps : List Path) (sites : List Int) : List Int :=
  sites.map fun x => (total ps x true)^2 + (total ps x false)^2

theorem firstChoice :
    panel (paths false 2 (-2) 5) [-5,-3,-1,1,3,5] = [1,5,4,4,17,1] ∧
    panel (paths true 2 (-2) 5) [-5,-3,-1,1,3,5] = [1,5,0,8,17,1] ∧
    ((paths true 2 (-2) 5).filter (fun p => p.x == -1)).length = 10 := by decide

theorem secondChoice :
    panel (paths false 5 1 7) [-7,-5,-3,-1,1,3,5,7] = [1,17,5,9,17,41,37,1] ∧
    panel (paths true 5 1 7) [-7,-5,-3,-1,1,3,5,7] = [1,17,5,25,25,17,37,1] := by
  set_option maxRecDepth 20000 in decide

end RemoteSiteRates
