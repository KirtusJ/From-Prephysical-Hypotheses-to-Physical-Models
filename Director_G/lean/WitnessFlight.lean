import Std

/-! A finite comparison behind the survival estimate in Phase_witness_and_flight.
All probabilities are in common integer numerator units. The analytic estimate
on the actual folded-cosine gap and the Holder inequality are separate hypotheses. -/

namespace WitnessFlight

/-- A pointwise upper bound on accepted competitors bounds their total mass. -/
theorem sumEnvelope (pairs : List (Nat × Nat)) (cap : Nat)
    (bound : ∀ p ∈ pairs, p.2 ≤ cap) :
    (pairs.map (fun p => p.1 * p.2)).sum ≤ (pairs.map Prod.fst).sum * cap := by
  induction pairs with
  | nil => simp
  | cons p tail ih =>
    have hp : p.2 ≤ cap := bound p (by simp)
    have ht := ih (fun q hq => bound q (List.mem_cons_of_mem p hq))
    simpa [Nat.add_mul] using Nat.add_le_add (Nat.mul_le_mul_left p.1 hp) ht

/-- Cleared-denominator version of l/(a+l) ≤ b/(a+b) for l ≤ b.
When used for conditional probabilities their two denominators are positive. -/
theorem posteriorBound (good actual cap : Nat) (h : actual ≤ cap) :
    actual*(good+cap) ≤ cap*(good+actual) := by
  simp only [Nat.mul_add]
  rw [Nat.mul_comm cap actual]
  exact Nat.add_le_add_right (Nat.mul_le_mul_right good h) _

end WitnessFlight
