import Std

namespace FiveSheetSuccessSpectrum

/-- The canonical five-sheet row is (0,u,v,-v,-u). Translating and
    reversing its global sign leave the squared integer count invariant. -/
def row : Nat → Int × Int
  | 0 => (1, 0)
  | k + 1 =>
    let (u, v) := row k
    (v, u - v)

def sheetMass (k : Nat) : Nat :=
  let (u, v) := row k
  (2 * (u*u + v*v)).toNat

theorem six_sheet_masses :
    (List.range 6).map sheetMass = [2, 2, 4, 10, 26, 68] := by native_decide

/-- Coefficients of (1-24x+64x²)², calculated by convolution. -/
def coeff : Nat → Int
  | 0 => 1
  | 1 => -24
  | 2 => 64
  | _ => 0

def squareCoeff (k : Nat) : Int :=
  ((List.range (k + 1)).map fun j => coeff j * coeff (k - j)).sum

theorem square_coefficients :
    (List.range 5).map squareCoeff = [1, -48, 704, -3072, 4096] := by native_decide

theorem zero_conditional_residual :
    ((List.range 5).map fun k =>
      squareCoeff k * (sheetMass k : Int) * (8 : Int)^(4-k)).sum = 0 := by native_decide

/-- An alternate positive law with weights (1517,1728,11)/3256
    at (0,11/48,1). This numerator has denominator 3256*48^k. -/
def altNum (k : Nat) := 1517 * 0^k + 1728 * 11^k + 11 * 48^k

theorem rival_matches_through_three :
    (List.range 4).all (fun k =>
      altNum k * (2 * 8^k) == sheetMass k * (3256 * 48^k)) = true := by native_decide

theorem rival_fourth_excess :
    (altNum 4 * (2 * 8^4) - sheetMass 4 * (3256 * 48^4)) * 24576
    = 41 * (3256 * 48^4) * (2 * 8^4) := by native_decide

end FiveSheetSuccessSpectrum
