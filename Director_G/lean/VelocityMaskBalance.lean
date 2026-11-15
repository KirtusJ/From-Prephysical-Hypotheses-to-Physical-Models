import Std

namespace VelocityMaskBalance

/-- Seven disjoint-mask differences, then the normalization row. -/
def contrasts : List (List Int) := [
    [1, 0, 0, 0, 0, 0, 0, -1],
    [0, 1, 0, 0, -1, 0, 0, 0],
    [1, 0, -1, 0, 0, 1, -1, 0],
    [0, 0, 1, -1, 0, 1, -1, 0],
    [1, -1, -1, 0, -1, 0, 1, 1],
    [1, 1, -1, -1, 0, -1, 1, 0],
    [1, 1, 1, 0, 1, -1, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1]]

/-- Integer inverse certificate, scaled by 128. -/
def correction : List (List Int) := [
    [59, 3, 16, 7, 28, -6, 30, 1],
    [-21, 51, 16, -9, -36, 26, -2, 17],
    [39, 15, -48, 35, 12, -30, 22, 5],
    [19, 27, 16, -65, -4, -54, 14, 9],
    [-21, -77, 16, -9, -36, 26, -2, 17],
    [-13, -5, 16, 31, -4, 10, -50, 41],
    [7, -17, -48, 3, 12, 34, -42, 37],
    [-69, 3, 16, 7, 28, -6, 30, 1]]

def entry (row column : Nat) : Int :=
  ((List.range 8).map (fun k =>
    (correction[row]!)[k]! * (contrasts[k]!)[column]!)).sum

theorem scaled_left_inverse :
    (List.range 8).all (fun i => (List.range 8).all (fun j =>
      entry i j == (if i == j then (128 : Int) else 0))) = true := by native_decide

theorem normalized_weights :
    correction.map (fun row => row[7]!) = [1,17,5,9,17,41,37,1] := by native_decide

end VelocityMaskBalance
