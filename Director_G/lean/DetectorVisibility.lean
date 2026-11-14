import Std

/-! Finite physical controls for the two-well detector calibration.
    Bloch vector coordinates follow X,Y,Z. For the two phases used here
    the vectors lie on the signed coordinate axes. No floating point,
    angular sampling or assumed rail-conditional formula enters the POVM replay. -/

namespace DetectorVisibility

structure Bloch where
  x : Int
  y : Int
  z : Int
deriving DecidableEq, Repr

inductive Phase
  | negativeOne
  | imaginaryUnit
deriving DecidableEq

def step (b : Phase) (s : Bloch) : Bloch :=
  -- H maps (x,y,z) to (z,-y,x). The left-rail phase rotates about Z.
  match b with
  | .negativeOne => ⟨-s.z, s.y, s.x⟩
  | .imaginaryUnit => ⟨s.y, s.z, s.x⟩

def evolved (b : Phase) : Nat → Bloch
  | 0 => ⟨0,0,1⟩
  | t+1 => step b (evolved b t)

/-- The meter chooses +Y with probability 1/5 and +Z with probability 4/5;
    its probability on a normalized Bloch vector is this numerator over 10. -/
def meter (s : Bloch) : Int := 5 + s.y + 4*s.z

/-- Source uses beta = -1 with probability 1/5 and beta = i with 4/5. -/
def click50 (t : Nat) : Int :=
  meter (evolved .negativeOne t) + 4*meter (evolved .imaginaryUnit t)

theorem coherentMeter : (List.range 4).map click50 = [45,29,21,41] := by decide

/-- For R polarization p=1 and balanced p=1/2 controls, the apparent
    second and third biases are -1/2 and 3/4. Their classical L column
    reconstructed from the two controls is a valid probability 13/50. -/
theorem coherentFalsePass :
    2*(click50 2-click50 1) = -(click50 0-click50 1) ∧
    4*(click50 3-click50 1) = 3*(click50 0-click50 1) ∧
    2*click50 1-click50 0 = 13 ∧ click50 0-click50 1 > 0 := by decide

/-- Terminal phase flip Z on the L component, contributing with probability
    1/2 in front of the same detector, including on the calibration shots. -/
def flip (s : Bloch) : Bloch := ⟨-s.x,-s.y,s.z⟩

def twirledMeter20 (s : Bloch) : Int := meter s + meter (flip s)

theorem twirledOnlyRail (s : Bloch) : twirledMeter20 s = 10 + 8*s.z := by
  simp [twirledMeter20, meter, flip]
  omega

def twirled100 (t : Nat) : Int :=
  twirledMeter20 (evolved .negativeOne t) + 4*twirledMeter20 (evolved .imaginaryUnit t)

theorem falsePassRemoved :
    (List.range 4).map twirled100 = [90,50,42,82] ∧
    5*(twirled100 2-twirled100 1) = -(twirled100 0-twirled100 1) ∧
    5*(twirled100 3-twirled100 1) = 4*(twirled100 0-twirled100 1) := by decide

/-- In a stable, positive-contrast weighted law, a zero sum of
    nonnegative integer-scaled penalties forces each penalty to vanish. -/
theorem allZeroOfSum (penalties : List Nat) (h : penalties.sum = 0) :
    ∀ p ∈ penalties, p = 0 := by
  induction penalties with
  | nil => simp
  | cons a tail ih =>
    simp only [List.sum_cons] at h
    have ha : a = 0 := by omega
    have ht : tail.sum = 0 := by omega
    intro p hp
    rcases List.mem_cons.mp hp with heq | htail
    · exact heq.trans ha
    · exact ih ht p htail

/-- The normalized apparent clock biases at a fixed well for sign-changing
    unit contrast and source masses 3,6,1 on real parts -1,0,1.
    Common factor 10 in the weights cancels. -/
theorem signedFalsePass :
    let weights : List (Int × Int × Int) := [(-1,3,1),(0,6,1),(1,1,-1)]
    let mean := fun (f : Int → Int) => (weights.map (fun (x,w,d) => w*d*f x)).sum
    0 < mean (fun _ => 1) ∧
    2*mean (fun x => x) = -mean (fun _ => 1) ∧
    4*mean (fun x => 1-x*x) = 3*mean (fun _ => 1) := by decide

/-- If everyone reports a click with the same color independent of rail
    when detected, unequal rail-dependent erasures are the only signal.
    For true R probability 1/4, detection probabilities on R,L = 1,1/3;
    at balanced input the overall click probability is 2/3. -/
theorem missesCarrySignal :
    let click12 := fun (rightQuarters : Int) => 3*rightQuarters + (4-rightQuarters)
    click12 1 = 6 ∧ click12 2 = 8 ∧ click12 4 = 12 ∧
      2*(click12 1-click12 2) = -(click12 4-click12 2) := by decide

end DetectorVisibility
