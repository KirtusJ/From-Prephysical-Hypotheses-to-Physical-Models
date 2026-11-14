import Std

/-! Light-cell extrapolation for a signed three-tick walk. The four sites
are ordered -3,-1,+1,+3. Write (z,x)=(R²-L²,2RL) for a normalized real
rail state. All arithmetic here uses integer numerators on a common grid;
the extrapolation certificate is a linear coefficient identity with its
denominators cleared. Checked in Lean 4.19.0 (Std only). -/

namespace LightProbeExtrapolation

/-- For z = Z/d and x = X/d these are masses in units of 1/(8d).
Only |x| ≤ 1 is needed for the two exterior wells. -/
theorem allLight (d Z X : Int) (hd : 0 < d) (hx : -d ≤ X ∧ X ≤ d) :
    (d - X ≤ 4*d ∧ 3*d - 2*Z - X ≤ 4*d ∧
     3*d + 2*Z + X ≤ 4*d ∧ d + X ≤ 4*d) ↔
    (-d ≤ 2*Z + X ∧ 2*Z + X ≤ d) := by omega

/-- A,B,C are the coefficients of the affine form A+Bz+Cx, possibly
scaled together. Each parenthesis on the right equals five probe hits. -/
theorem affineIdentity (A B C : Int) :
    20*(A+B) = 3*(5*A+4*B-3*C) + 3*(5*A+5*C) - 2*(5*A-4*B+3*C) := by
  omega

/-- On the diagonal source line the points z = ±1/2, x = 0 suffice.
The probe values are (2A+B)/2 and (2A-B)/2. -/
theorem diagonalIdentity (A B : Int) :
    4*(A+B) = 3*(2*A+B) - (2*A-B) := by omega

/-- With errors at both diagonal probes bounded by e, the inferred
heavy value has error at most 2e; all terms are scaled by two. -/
theorem diagonalError (e ep em : Int)
    (hp : -e ≤ ep ∧ ep ≤ e) (hm : -e ≤ em ∧ em ≤ e) :
    -4*e ≤ 3*ep-em ∧ 3*ep-em ≤ 4*e := by omega

/-- If an affine fit has error at most e at each of the three data
points, the target's deviation from interpolation cannot exceed 3e.
The minimized maximum fit error, over real coefficients, is therefore
at least the absolute residual divided by three. -/
theorem diagonalFitResidual (e ep em er : Int)
    (hp : -e ≤ ep ∧ ep ≤ e) (hm : -e ≤ em ∧ em ≤ e)
    (hr : -e ≤ er ∧ er ≤ e) :
    -6*e ≤ 2*er-3*ep+em ∧ 2*er-3*ep+em ≤ 6*e := by omega

/-- The error pattern ep=-e, em=e, er=e attains 3e. -/
theorem diagonalResidualAttains (e : Int) :
    2*e - 3*(-e) + e = 6*e := by omega

/-- If e1,e2,e3 are the three probe errors, this is the signed
extrapolation error with the common denominator four left in place. -/
theorem uniformError (e e1 e2 e3 : Int)
    (h1 : -e ≤ e1 ∧ e1 ≤ e) (h2 : -e ≤ e2 ∧ e2 ≤ e)
    (h3 : -e ≤ e3 ∧ e3 ≤ e) :
    -8*e ≤ 3*e1 + 3*e2 - 2*e3 ∧ 3*e1 + 3*e2 - 2*e3 ≤ 8*e := by omega

/-- The witness 2z+x evaluates to 1,1,-1 on these probes and 2 on
sharp R, so the bound also saturates within the class of affine errors. -/
theorem witnessValues :
    (2*4 + (-3) : Int) = 5 ∧ (2*0 + 5 : Int) = 5 ∧
    (2*(-4) + 3 : Int) = -5 ∧ (2*5 + 0 : Int) = 10 := by decide

private theorem oneTerm (w t d : Int) (safe : -d ≤ t ∧ t ≤ d) :
    w*t ≤ (w.natAbs : Int)*d := by
  by_cases hw : 0 ≤ w
  · rw [Int.natAbs_of_nonneg hw]
    exact Int.mul_le_mul_of_nonneg_left safe.2 hw
  · rw [Int.ofNat_natAbs_of_nonpos (show w ≤ 0 by omega)]
    have ht : -t ≤ d := by omega
    have h := Int.mul_le_mul_of_nonneg_left ht (show 0 ≤ -w by omega)
    simpa only [Int.neg_mul, Int.mul_neg, Int.neg_neg] using h

/-- Any finite signed combination representing the sharp-R target must
represent the witness as well. Each pair stores an integer weight and
its probe's scaled witness value. This proves the dual L1 lower bound. -/
theorem dualBound (d : Int) (wt : List (Int × Int))
    (safe : ∀ p ∈ wt, -d ≤ p.2 ∧ p.2 ≤ d) :
    (wt.map (fun p => p.1*p.2)).sum ≤
      (wt.map (fun p => (p.1.natAbs : Int))).sum * d := by
  induction wt with
  | nil => simp
  | cons p wt ih =>
    have hp := oneTerm p.1 p.2 d (safe p (by simp))
    have hs := ih (by intro q hq; exact safe q (by simp [hq]))
    simp only [List.map_cons, List.sum_cons, Int.add_mul]
    omega

/-- Weights are represented over the positive common denominator W.
Reproducing the target witness value 2 forces L1 norm at least 2. -/
theorem optimalLowerBound (d W : Int) (hd : 0 < d) (_hW : 0 < W)
    (wt : List (Int × Int)) (safe : ∀ p ∈ wt, -d ≤ p.2 ∧ p.2 ≤ d)
    (target : (wt.map (fun p => p.1*p.2)).sum = (2*W)*d) :
    2*W ≤ (wt.map (fun p => (p.1.natAbs : Int))).sum := by
  have bound := dualBound d wt safe
  rw [target] at bound
  exact Int.le_of_mul_le_mul_right bound hd

end LightProbeExtrapolation
