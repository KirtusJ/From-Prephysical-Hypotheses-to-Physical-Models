import Std

/- A raw launch records true at (7,R,1), false at (5,L,1), and none elsewhere.
   The stopping rule uses the first n named hits. -/
namespace TagShotBudget

abbrev Launch := Option Bool

def hits (raw : List Launch) : List Bool := raw.filterMap id

def rejects (n k : Nat) (raw : List Launch) : Prop :=
  n ≤ (hits raw).length ∧ ((hits raw).take n).count true ≤ k

/-- A timeout is a non-rejection, including a log with no named hits. -/
theorem timeout {raw : List Launch} {n k : Nat} (h : (hits raw).length < n) :
    ¬rejects n k raw := fun rejected => (Nat.not_le_of_lt h) rejected.1

/-- Any rejection by the deadline is also a rejection on every continuation.
    This event inclusion needs no assumption on the signs or their arrival rates. -/
theorem reject_extension {raw : List Launch} {n k : Nat} (rest : List Launch)
    (h : rejects n k raw) : rejects n k (raw ++ rest) := by
  obtain ⟨enough, cutoff⟩ := h
  have append_hits : hits (raw ++ rest) = hits raw ++ hits rest := by
    simp [hits]
  unfold rejects
  rw [append_hits, List.length_append, List.take_append_of_le_length enough]
  exact ⟨by omega, cutoff⟩

theorem capped_implies_full {raw : List Launch} {n k : Nat} (budget : Nat)
    (h : rejects n k (raw.take budget)) : rejects n k raw := by
  simpa using reject_extension (raw.drop budget) h

/-- At integer common denominators, combine the two equally likely switch settings.
    R has weight x, L has weight y, and the physical counters have responses a,b.
    The crossed setting decodes counter B as R and counter A as L. -/
theorem decoded_exchange (x y a b : Nat) :
    (x * a + x * b, y * b + y * a) = (x * (a + b), y * (a + b)) := by
  simp [Nat.mul_add, Nat.add_comm]

/-- After clearing positive denominators for a rational residual ratio kappa = n/d,
    compare the lower null fraction with the upper rival fraction. -/
theorem residual_separation (n d : Nat) :
    20 * n * (257 * d + 187 * n) < 257 * d * (17 * d + 20 * n) ↔
    220 * (n*n) < 257 * (d*d) := by
  simp only [Nat.mul_add]
  have hm : 20 * n * (257 * d) = 257 * d * (20 * n) := by ac_rfl
  have hn : 20 * n * (187 * n) = 17 * (220 * (n*n)) := by
    calc
      _ = (20 * 187) * (n*n) := by ac_rfl
      _ = (17 * 220) * (n*n) := rfl
      _ = _ := by ac_rfl
  have hd : 257 * d * (17 * d) = 17 * (257 * (d*d)) := by ac_rfl
  rw [hm, hn, hd]
  omega

/-- Given the coupled waits for all requested hits, any reference completion also
    completes the actual run. Mark uniforms and fair signs are shared by both runs. -/
theorem coupled_deadline (waits : List (Nat × Nat)) {budget : Nat}
    (h : ∀ w ∈ waits, w.1 ≤ w.2) (done : (waits.map Prod.snd).sum ≤ budget) :
    (waits.map Prod.fst).sum ≤ budget := by
  apply Nat.le_trans _ done
  clear done
  induction waits with
  | nil => exact Nat.le_refl 0
  | cons w tail ih =>
    simp only [List.map_cons, List.sum_cons]
    exact Nat.add_le_add (h w (by simp)) (ih (fun x hx => h x (by simp [hx])))

/-- A fair source sends the same weight to either arm. After clearing the positive
    binomial denominators, the inclusive 20/41 and 21/41 reference bounds are
    equivalent to the 20/21 and 21/20 bounds on the right-to-left response ratio. -/
theorem fair_reference_bounds (right left : Nat) :
    (20 * (right + left) ≤ 41 * right ∧ 41 * right ≤ 21 * (right + left)) ↔
    (20 * left ≤ 21 * right ∧ 20 * right ≤ 21 * left) := by omega

/-- Finite acceptance sets with a common denominator. A release that requires
    every component to pass has at most the weight of any one limiting component. -/
theorem intersection_bound {Ω : Type} (weight : (Ω → Prop) → Nat)
    (mono : ∀ (s t : Ω → Prop), (∀ x, s x → t x) → weight s ≤ weight t)
    {release component : Ω → Prop} {cap : Nat} (included : ∀ x, release x → component x)
    (limit : weight component ≤ cap) : weight release ≤ cap :=
  Nat.le_trans (mono release component included) limit

end TagShotBudget
