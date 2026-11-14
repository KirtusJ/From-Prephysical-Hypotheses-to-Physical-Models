import Std

namespace SpatialFlagPartitions

def pairCells (split : Bool) (a b : Nat) : List Nat :=
  if split then [a, b] else [a+b, 0]

def cumulative (xs : List Nat) : List Nat :=
  let sorted := xs.mergeSort (· ≥ ·)
  ((sorted.foldl (fun (s : Nat × List Nat) n =>
    (s.1+n,(s.1+n)::s.2)) (0,[])).2.reverse)

def strictMajor (xs ys : List Nat) : Bool :=
  let x := cumulative xs
  let y := cumulative ys
  xs.sum == ys.sum && x != y && (x.zip y).all (fun p => decide (p.1 ≥ p.2))

def seven (a b c : Bool) : List Nat :=
  [1,17,5,37,1] ++ pairCells a 13 4 ++ pairCells b 13 8 ++ pairCells c 25 4

theorem sevenOrder : ∀ a b c : Bool,
    strictMajor [1,17,5,37,1,9,17,41,0,0,0] (seven a b c) = true ∧
    (seven a b c).count 37 = 1 := by native_decide

def nine (a b c : Bool) : List Nat :=
  [256] ++ pairCells a 32 32 ++ pairCells b 80 16 ++ pairCells c 80 16

theorem nineSupport : ∀ a b c : Bool,
    strictMajor [256,128,128,0,0,0,0] (nine a b c) = true ∧
    4 ≤ ((nine a b c).filter (· > 0)).length := by native_decide

end SpatialFlagPartitions
