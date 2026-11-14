import Std

/-! Two equal-label carriers and an already written pointer. The algebra below
does not identify equality of coherent columns with equality of observed rates. -/

namespace FlagExchange

/-- A column after copying a predicate of the first or second carrier. The
spectator argument can include any other retained coordinates. -/
def writeFirst {Label Env Scalar : Type} (mark : Label → Bool)
    (input : Label → Label → Env → Scalar) (zero : Scalar) :
    Label → Label → Bool → Env → Scalar :=
  fun j k flag e => if flag = mark j then input j k e else zero

def writeSecond {Label Env Scalar : Type} (mark : Label → Bool)
    (input : Label → Label → Env → Scalar) (zero : Scalar) :
    Label → Label → Bool → Env → Scalar :=
  fun j k flag e => if flag = mark k then input j k e else zero

/-- Pull back the output column through the self-inverse swap. The written flag
and all other retained coordinates are identical on input and output. -/
def swapCarriers {Label Env Scalar : Type}
    (column : Label → Label → Bool → Env → Scalar) :
    Label → Label → Bool → Env → Scalar :=
  fun j k flag e => column k j flag e

/-- For any marking predicate, symmetric joint amplitudes (including their
phases and spectator coordinates) suffice for equality of the complete columns. -/
theorem passiveSwap {Label Env Scalar : Type} (mark : Label → Bool)
    (input : Label → Label → Env → Scalar) (zero : Scalar)
    (symmetric : ∀ j k e, input k j e = input j k e) :
    swapCarriers (writeFirst mark input zero) = writeSecond mark input zero := by
  funext j k flag e
  simp only [swapCarriers, writeFirst, writeSecond, symmetric j k e]

/-- Full-column matching also requires this symmetry. Read its coefficient on
the reference flag's populated side; this includes any persistent which-path tag. -/
theorem symmetryNecessary {Label Env Scalar : Type} (mark : Label → Bool)
    (input : Label → Label → Env → Scalar) (zero : Scalar)
    (matched : swapCarriers (writeFirst mark input zero) = writeSecond mark input zero) :
    ∀ j k e, input k j e = input j k e := by
  intro j k e
  have h := congrArg (fun c : Label → Label → Bool → Env → Scalar => c j k (mark k) e) matched
  simpa only [swapCarriers, writeFirst, writeSecond, if_pos rfl] using h

/-- All quantities are in common integer units; four times the diluted rate is
one full scale plus twice the original rate. -/
theorem exactDilution (scale reference measured target original : Int)
    (geometry : 4 * reference = scale + 2 * target)
    (randomization : 4 * measured = scale + 2 * original)
    (agreement : measured = reference) : original = target := by omega

/-- Directional sharp/dark errors have opposite signs. Therefore each side
uses just one helper tolerance. Rates and tolerances use the same integer scale. -/
theorem dilutionError (scale target original ref coherent mix sharp dark copy
    refErr mixErr sharpErr darkErr copyErr : Int)
    (geometry : 4 * ref = scale + 2 * target)
    (mixing : 4 * mix = sharp + dark + 2 * copy)
    (refHi : coherent - ref ≤ refErr) (refLo : ref - coherent ≤ refErr)
    (mixHi : mix - coherent ≤ mixErr) (mixLo : coherent - mix ≤ mixErr)
    (sharpHi : sharp ≤ scale) (sharpLo : scale - sharp ≤ sharpErr)
    (darkLo : 0 ≤ dark) (darkHi : dark ≤ darkErr)
    (copyHi : original - copy ≤ copyErr) (copyLo : copy - original ≤ copyErr) :
    2 * (original - target) ≤ 4 * (refErr + mixErr) + sharpErr + 2 * copyErr ∧
    2 * (target - original) ≤ 4 * (refErr + mixErr) + darkErr + 2 * copyErr := by
  constructor <;> omega

end FlagExchange
