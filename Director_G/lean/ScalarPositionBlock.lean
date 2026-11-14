import Std

/-! Kernel-checked integer amplitudes for twelve H/I ticks on a 16-site ring.
A pair in a row gives the amplitudes from the two sharp-site input rails.
The positive normalization factor 1/√2 for each H is suppressed. -/

namespace ScalarPositionBlock

inductive Coin | H | I deriving DecidableEq
open Coin

def schedule : List Coin := [H, H, H, I, I, H, I, H, H, I, I, H]

abbrev Row := Int × Int
abbrev Matrix := Row × Row
abbrev Ring := List Matrix

def zeroMatrix : Matrix := ((0, 0), (0, 0))
def start : Ring :=
  (List.range 16).map fun x =>
    if x = 0 then ((1, 0), (0, 1)) else zeroMatrix

def scatter : Coin → Matrix → Matrix
  | I, m => m
  | H, ((a, b), (c, d)) => ((a+c, b+d), (a-c, b-d))

/-- Right rail arrives from x−1, left rail from x+1. The ring wraps at every tick. -/
def tick (field : Ring) (coin : Coin) : Ring :=
  let moved := field.map (scatter coin)
  (List.range 16).map fun x =>
    ((moved[(x+15)%16]!).1, (moved[(x+1)%16]!).2)

def lastField : Ring := schedule.foldl tick start

/-- All four entries of the real transfer matrix transpose times the matrix. -/
def gram : Matrix → Matrix
  | ((a, b), (c, d)) => ((a*a+c*c, a*b+c*d), (b*a+d*c, b*b+d*d))

def scalar (n : Int) : Matrix := ((n, 0), (0, n))

/-- Even sites in physical order alternate with the eight dark odd sites. -/
def masses : List Int := [58,0,10,0,2,0,10,0,26,0,10,0,2,0,10,0]

theorem denominator : 2 ^ schedule.count H = 128 := by decide

set_option maxRecDepth 4096 in
set_option maxHeartbeats 2000000 in
theorem all_site_effects : lastField.map gram = masses.map scalar := by
  decide

theorem normalized : masses.length = 16 ∧ masses.sum = 128 := by decide

/-- Arithmetic convolution at the origin for two translation-invariant
blocks whose conditional displacement numerators are the displayed masses.
This statement certifies a finite sum, not the physical read rule. -/
def twoBlockReturn : Int :=
  ((List.range 16).map fun x => masses[x]! * masses[(16-x)%16]!).sum

theorem two_block_return_numerator : twoBlockReturn = 4448 ∧
    twoBlockReturn * 512 = 139 * (128 * 128) := by decide

end ScalarPositionBlock
