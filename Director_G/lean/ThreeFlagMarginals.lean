import Std

namespace ThreeFlagMarginals

/-- With total d, single weights a,b,c and pairs ab,ac,bc, these eight
    affine cells at triple weight h are nonnegative precisely on this interval. -/
theorem feasible (d a b c ab ac bc h : Int) :
    (0 ≤ d-a-b-c+ab+ac+bc-h ∧ 0 ≤ c-ac-bc+h ∧
     0 ≤ b-ab-bc+h ∧ 0 ≤ bc-h ∧ 0 ≤ a-ab-ac+h ∧
     0 ≤ ac-h ∧ 0 ≤ ab-h ∧ 0 ≤ h) ↔
    (0 ≤ h ∧ ab+ac-a ≤ h ∧ ab+bc-b ≤ h ∧ ac+bc-c ≤ h ∧
     h ≤ ab ∧ h ≤ ac ∧ h ≤ bc ∧ h ≤ d-a-b-c+ab+ac+bc) := by omega

/-- All pair counts include the triple. Its contribution is removed once
    to obtain the sum of the two higher threshold weights. -/
theorem high_tails (ab ac bc h : Int) :
    ((ab-h)+(ac-h)+(bc-h)+h)+h = ab+ac+bc-h := by omega

/-- Pointwise on a nonnegative weight table, the first pair and the third
    marginal bound the combined high thresholds. The excess is cell 001. -/
theorem one_pair_suffices (w001 w011 w101 w110 w111 : Nat) :
    (w011+w101+w110+w111)+w111 ≤
      (w110+w111) + (w001+w011+w101+w111) := by omega

/-- Three fair midpoint identities at attainable masses of the one-bank
    walk, a sharp dark, and a complementary pair give the ordinary values
    after clearing any common rate denominator. -/
theorem one_bank_midpoints (a b c e d : Int)
    (dark_row : 2*a=b) (second : 2*b=a+c) (third : 2*c=a+e)
    (complementary : c+e=d) :
    8*a=d ∧ 8*b=2*d ∧ 8*c=3*d ∧ 8*e=5*d := by omega

/-- Worst-case sign of every residual is allowed. e0 bounds the error of
    the first doubled row (including dark error), e1 and e2 of the others,
    and ec of the complementary-pair identity. -/
theorem fifth_mass_perturbation (a b c e d e0 e1 e2 ec : Int)
    (r0 : -e0 ≤ 2*a-b ∧ 2*a-b ≤ e0)
    (r1 : -e1 ≤ 2*b-a-c ∧ 2*b-a-c ≤ e1)
    (r2 : -e2 ≤ 2*c-a-e ∧ 2*c-a-e ≤ e2)
    (rc : -ec ≤ c+e-d ∧ c+e-d ≤ ec) :
    -(2*e0+e1+3*e2+5*ec) ≤ 8*e-5*d ∧
      8*e-5*d ≤ 2*e0+e1+3*e2+5*ec := by omega

end ThreeFlagMarginals
