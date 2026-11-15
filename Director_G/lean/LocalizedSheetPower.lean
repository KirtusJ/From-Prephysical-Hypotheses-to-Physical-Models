import Std

namespace LocalizedSheetPower

/-- Rail numerators after a balanced split, shift and addressed sheet swap. -/
def railsWith (switch : Nat → Int → Bool) : Nat → Int → Bool → Int × Int
  | 0, x, s => if x == 0 && !s then (1,0) else (0,0)
  | t+1, x, s =>
    let p := if switch (t+1) x then !s else s
    let fromLeft := railsWith switch t (x-1) p
    let fromRight := railsWith switch t (x+1) p
    (fromLeft.1 + fromLeft.2, fromRight.1 - fromRight.2)

def rails := railsWith (fun t x => (t == 3 && x == -3) || (t == 4 && x == 2))

theorem terminal :
    ([-5,-3,-1,1,3,5] : List Int).map (fun x => (rails 5 x false, rails 5 x true)) =
    [((0,0),(0,1)),((0,1),(-1,1)),((-1,-2),(1,0)),
     ((0,0),(0,2)),((0,1),(4,0)),((1,0),(0,0))] := by native_decide

theorem scoreNumerator (u : Int) : 16-8*u+u*u = (u-4)*(u-4) := by
  simp only [Int.sub_mul, Int.mul_sub, Int.mul_comm u 4]
  omega

example : (16 : Int)*3-8*4+4 = 20 := by decide

def originRails := railsWith (fun _ x => x == 0)

theorem stationaryTerminal :
    ([-6,-4,-2,0,2,4,6] : List Int).map (fun x => (originRails 6 x false, originRails 6 x true)) =
    [((0,-1),(0,0)),((1,-3),(0,0)),((1,2),(0,0)),((0,-4),(-2,2)),
     ((2,1),(0,2)),((3,1),(2,0)),((1,0),(0,0))] := by native_decide

example : (16 : Int)*1-8*6+8+5*6 = 6 := by decide

end LocalizedSheetPower
