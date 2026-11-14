import Std

namespace SevenTickPositionScore

/-- Integer Hadamard numerator on one named site, with the stream reversed
    to recover the two predecessor sites. -/
def amplitude : Nat → Int → Int × Int
  | 0, x => if x = 0 then (1,0) else (0,0)
  | n+1, x =>
    let left := amplitude n (x-1)
    let right := amplitude n (x+1)
    (left.1 + left.2, right.1 - right.2)

theorem terminal :
    ([-7,-5,-3,-1,1,3,5,7] : List Int).map (amplitude 7) =
      [(0,1),(-1,4),(-2,-1),(3,0),(-4,-1),(5,4),(6,1),(1,0)] := by
  native_decide

/-- In coefficients sharing an arbitrary integer scale, ordinary mass gives
    zero and the unsigned-path score has the stated positive lower bound. -/
theorem scoreChecks (a b c scale : Int) (hw : a = 9*scale-5*b-17*c)
    (hb : -scale < b) (hc : c < scale) :
    a+5*b+17*c-9*scale = 0 ∧
    4*scale < a+21*b+7*c-35*scale+2*(35-7)*scale := by
  omega

end SevenTickPositionScore
