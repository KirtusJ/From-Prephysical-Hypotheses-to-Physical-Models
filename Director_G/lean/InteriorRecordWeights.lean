import Std

namespace InteriorRecordWeights

/-- One word of left/right proposals and its signed amplitude. -/
def paths : Nat → List (List Bool)
  | 0 => [[]]
  | n+1 => (paths n).flatMap fun w => [false :: w,true :: w]

def follow (x : Int) (rail : Bool) (amp : Int) : List Bool → List Int × Int
  | [] => ([],amp)
  | d :: rest =>
    let y := if d then x-1 else x+1
    let (tail,sign) := follow y d (if d && rail then -amp else amp) rest
    (y :: tail,sign)

abbrev Word := Int × Int × Int × Int

def signedPaths (fine : Bool) : List (Word × Int) :=
  (paths 7).map fun w =>
    let (xs, a) := follow 0 false 1 w
    ((xs[1]!, if fine then xs[3]! else 0, xs[5]!, xs[6]!), a)

def g (x : Int) : Int :=
  match x with
  | -7 => -8 | -5 => 48 | -3 => -8 | -1 => 1 | 1 => 15 | 5 => -48 | _ => 0

def h (w : Word) : Int :=
  match (w.1,w.2.2.1,w.2.2.2) with
  | (0,0,-1) | (0,2,3) => 1
  | (-2,-4,-5) | (2,4,5) => -8
  | (-2,-2,-3) | (2,2,3) => 8
  | (-2,-4,-3) => -2
  | _ => 0

/-- Consecutive last sites fix the ending rail, so the amplitude may be
    summed over the matching complete words before it is squared. -/
def cellTable (fine : Bool) : List (Word × Int) := Id.run do
  let data := signedPaths fine
  let keys := (data.map Prod.fst).eraseDups
  return keys.map fun x =>
    (x, ((data.filterMap fun e => if e.1 == x then some e.2 else none).sum)^2)

def row (t : List (Word × Int)) (m : Int) : Int × Int × Int :=
  let keys := (t.filter fun e => e.2 == m).map Prod.fst
  ((keys.length : Int), (keys.map fun x => g x.2.2.2).sum, (keys.map h).sum)

theorem seven_tick_rows :
    ([1,4,16,36] : List Int).map (fun m => (row (cellTable false) m).2.1) = [0,0,0,0] ∧
    ([1,4,16] : List Int).map (row (cellTable true)) =
      [(16,16,32), (20,-8,-16), (2,1,2)] := by native_decide

theorem max_score :
    ((cellTable true).filter (fun e => e.2 == 16)).all (fun e => h e.1 == 1) ∧
    ((signedPaths true).map (fun e => h e.1)).sum = 44 := by native_decide

/-- After replacing 4^q by y, both score numerators
    are positive multiples of the same square. -/
theorem square_polynomials (y : Int) :
    16-8*y+y*y = (y-4)*(y-4) ∧
    32-16*y+2*(y*y) = 2*((y-4)*(y-4)) := by
  simp only [Int.sub_mul, Int.mul_sub, Int.mul_comm y (4 : Int)]
  simp only [Int.reduceMul]
  generalize y * y = z
  constructor
  · omega
  · simp only [Int.mul_add, Int.mul_sub, ← Int.mul_assoc, Int.reduceMul]
    omega

end InteriorRecordWeights
