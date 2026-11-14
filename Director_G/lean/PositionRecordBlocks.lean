import Std

namespace PositionRecordBlocks

/-- For fixed final site and outgoing rail, the conditional shift picks only
    one preceding site. All other preceding-site amplitudes for this terminal
    channel vanish. Splitting by the preceding-site record preserves its Gram. -/
theorem selectedPredecessor (fromHere fromElsewhere : Int)
    (uniqueSite : fromElsewhere = 0) :
    (fromHere + fromElsewhere)^2 = fromHere^2 + fromElsewhere^2 := by
  simp [uniqueSite]

/-- Integer numerators for the four-tick table, in sixteenths per block.
    The variance uses tick units. C and W can scale rational choice weights. -/
theorem returnVariance (C W total return16 variance : Int)
    (norm : total = C + W) (hits : return16 = 2*C + 6*W)
    (spread : variance = 5*C + 4*W) :
    4*variance = 22*total - return16 ∧ 4*W = return16 - 2*total := by
  omega

end PositionRecordBlocks
