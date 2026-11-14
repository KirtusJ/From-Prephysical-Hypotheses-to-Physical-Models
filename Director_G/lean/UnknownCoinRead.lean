import Std

/-! Original-incident flag frequencies for the tick-three site +1. Rates,
including the full-rate unit and tolerances, use common integer units. Thus
these lemmas cover exact finite rational comparisons by clearing denominators.
All mixing equalities are explicit premises about experimentally assigned arms. -/

namespace UnknownCoinRead

/-- Analyzer denominator 8: two sharp, three dark, one X+, two Z+.
    The direct mixture has two sharp, two dark, and four science arms.
    Sharing even imperfect endpoints cancels the entire sharp response. -/
theorem eliminateShared (direct reference native x z sharp dark : Int)
    (hD : 8 * direct = 2 * sharp + 2 * dark + 4 * native)
    (hR : 8 * reference = 2 * sharp + 3 * dark + x + 2 * z) :
    4 * native - x - 2 * z = 8 * (direct - reference) + dark := by
  omega

/-- If only the discrepancy bound and a dark false-positive bound are known,
    the resulting interval has different upper and lower endpoints. -/
theorem sharedBounds (direct reference native x z sharp dark eps darkMax : Int)
    (hD : 8 * direct = 2 * sharp + 2 * dark + 4 * native)
    (hR : 8 * reference = 2 * sharp + 3 * dark + x + 2 * z)
    (hi : direct - reference ≤ eps) (lo : reference - direct ≤ eps)
    (d0 : 0 ≤ dark) (d1 : dark ≤ darkMax) :
    -(8 * eps) ≤ 4 * native - x - 2 * z ∧
    4 * native - x - 2 * z ≤ 8 * eps + darkMax := by
  have h := eliminateShared direct reference native x z sharp dark hD hR
  omega

/-- For independently measured end arms, signs differ for sharp failures
    and dark false positives, and the sharp cancellation cannot be used. -/
theorem distinctBounds
    (full direct reference native x z sharpD sharpR darkD darkR : Int)
    (eps esD esR edD edR : Int)
    (hD : 8 * direct = 2 * sharpD + 2 * darkD + 4 * native)
    (hR : 8 * reference = 2 * sharpR + 3 * darkR + x + 2 * z)
    (hi : direct - reference ≤ eps) (lo : reference - direct ≤ eps)
    (s0 : sharpD ≤ full) (s1 : full - sharpD ≤ esD)
    (s2 : sharpR ≤ full) (s3 : full - sharpR ≤ esR)
    (d0 : 0 ≤ darkD) (d1 : darkD ≤ edD)
    (d2 : 0 ≤ darkR) (d3 : darkR ≤ edR) :
    -(8 * eps + 2 * esR + 2 * edD) ≤ 4 * native - x - 2 * z ∧
    4 * native - x - 2 * z ≤ 8 * eps + 2 * esD + 3 * edR := by
  omega

/-- Endpoint-sharp wrong reader on a maximally mixed coin: use scale 272.
    Both bases report 136/272, but the squared-score native read is 72/272.
    The two independently randomized original-incident mixtures disagree. -/
theorem mixedWitness :
    8 * (104 : Int) = 2 * 272 + 4 * 72 ∧
    8 * (119 : Int) = 2 * 272 + 136 + 2 * 136 ∧
    (104 : Int) - 119 = -15 ∧
    4 * (72 : Int) - 136 - 2 * 136 = -120 := by decide

end UnknownCoinRead
