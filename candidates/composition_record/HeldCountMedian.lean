import Std

namespace HeldCountMedian

/-! Use integer hit counts and clear the common denominator of all rational
histogram and sign-allocation weights. An atom carries the weight assigned
to each sign. The signed count sum divided by total weight and block length
is E[sign * K/n]; for equiprobable signs it is half the difference of the
conditional mean hit fractions. No stochastic model of the reads is used. -/

structure Atom where
  hits : Int
  plus : Int
  minus : Int

def Valid (rows : List Atom) : Prop :=
  ∀ a ∈ rows, 0 ≤ a.plus ∧ 0 ≤ a.minus

def total (f : Atom → Int) : List Atom → Int
  | [] => 0
  | a :: rows => f a + total f rows

def bias (a : Atom) : Int := a.plus - a.minus
def Fair (rows : List Atom) : Prop := total bias rows = 0
def signed (rows : List Atom) : Int := total (fun a => bias a * a.hits) rows

def distance (a : Atom) (t : Int) : Int :=
  if a.hits < t then t - a.hits else a.hits - t

def radius (rows : List Atom) (t : Int) : Int :=
  total (fun a => (a.plus + a.minus) * distance a t) rows

-- Weight assigned on the wrong side, multiplied by the distance from the cut.
-- Any division of mass on the cut contributes zero.
def missed (a : Atom) (t : Int) : Int :=
  (if a.hits < t then a.plus else a.minus) * distance a t

private theorem atom_identity (a : Atom) (t : Int) :
    (a.plus + a.minus) * distance a t =
    bias a * a.hits - t * bias a + 2 * missed a t := by
  have twice (v : Int) : 2 * v = v + v := by omega
  unfold missed distance bias
  split <;> simp_all [twice, Int.mul_sub, Int.sub_mul, Int.add_mul, Int.mul_add,
    Int.mul_comm, Int.mul_assoc, Int.mul_left_comm] <;> omega

theorem gap_identity (rows : List Atom) (t : Int) :
    radius rows t =
    signed rows - t * total bias rows + 2 * total (fun a => missed a t) rows := by
  induction rows with
  | nil => simp [total, signed, radius]
  | cons a rows ih =>
    have ha := atom_identity a t
    simp only [total, radius, signed, Int.mul_add] at ih ⊢
    omega

private theorem missed_nonneg (a : Atom) (t : Int) (hp : 0 ≤ a.plus) (hm : 0 ≤ a.minus) :
    0 ≤ missed a t := by
  by_cases h : a.hits < t
  · simpa only [missed, distance, if_pos h] using Int.mul_nonneg hp (show 0 ≤ t - a.hits by omega)
  · simpa only [missed, distance, if_neg h] using Int.mul_nonneg hm (show 0 ≤ a.hits - t by omega)

private theorem total_missed_nonneg (rows : List Atom) (t : Int) (h : Valid rows) :
    0 ≤ total (fun a => missed a t) rows := by
  induction rows with
  | nil => simp [total]
  | cons a rows ih =>
    have ha := h a (by simp)
    have ht : Valid rows := fun b hb => h b (by simp [hb])
    exact Int.add_nonneg (missed_nonneg a t ha.1 ha.2) (ih ht)

theorem fair_upper (rows : List Atom) (t : Int) (h : Valid rows) (fair : Fair rows) :
    signed rows ≤ radius rows t := by
  have hg := gap_identity rows t
  have hm := total_missed_nonneg rows t h
  unfold Fair at fair
  rw [fair, Int.mul_zero, Int.sub_zero] at hg
  omega

def swap (a : Atom) : Atom := ⟨a.hits, a.minus, a.plus⟩

private theorem swap_totals (rows : List Atom) (t : Int) :
    total bias (rows.map swap) = -(total bias rows) ∧
    signed (rows.map swap) = -(signed rows) ∧
    radius (rows.map swap) t = radius rows t := by
  induction rows with
  | nil => simp [total, signed, radius]
  | cons a rows ih =>
    obtain ⟨hb, hs, hr⟩ := ih
    simp only [List.map_cons, signed, radius, total] at hb hs hr ⊢
    have hw : bias (swap a) = -bias a := by simp only [bias, swap]; omega
    have hd : distance (swap a) t = distance a t := rfl
    rw [hb, hs, hr, hw, hd]
    simp only [swap, Int.neg_mul, Int.add_comm a.minus a.plus]
    exact ⟨by omega, by omega, trivial⟩

theorem fair_bounds (rows : List Atom) (t : Int) (h : Valid rows) (fair : Fair rows) :
    -(radius rows t) ≤ signed rows ∧ signed rows ≤ radius rows t := by
  obtain ⟨hb, hs, hr⟩ := swap_totals rows t
  have hv : Valid (rows.map swap) := by
    intro a ha
    obtain ⟨b, hb', rfl⟩ := List.mem_map.mp ha
    exact ⟨(h b hb').2, (h b hb').1⟩
  have hf : Fair (rows.map swap) := by
    unfold Fair at *
    omega
  have hn := fair_upper _ t hv hf
  rw [hs, hr] at hn
  exact ⟨by omega, fair_upper rows t h fair⟩

/-- A fair upper-half assignment with an explicit tie at t. Below and above
contain repeated integer hit counts; their lengths include multiplicities.
After doubling the frequency units, tieWeight permits any rational median
split, including half an original unit. This construction repurposes only
sign labels; the histogram of unconditional hit counts is unchanged. -/
def lowerAtom (k : Int) : Atom := ⟨k, 0, 1⟩
def upperAtom (k : Int) : Atom := ⟨k, 1, 0⟩

def medianRows (below above : List Int) (t half : Int) : List Atom :=
  below.map lowerAtom ++
  (⟨t, half - (above.length : Int), half - (below.length : Int)⟩ :: above.map upperAtom)

private theorem total_append (f : Atom → Int) (xs ys : List Atom) :
    total f (xs ++ ys) = total f xs + total f ys := by
  induction xs with
  | nil => simp [total]
  | cons a xs ih => simp [total, ih, Int.add_assoc]

private theorem map_constant (xs : List Int) (atom : Int → Atom) (f : Atom → Int)
    (z : Int) (h : ∀ k ∈ xs, f (atom k) = z) :
    total f (xs.map atom) = (xs.length : Int) * z := by
  induction xs with
  | nil => simp [total]
  | cons x xs ih =>
    have hx := h x (by simp)
    have ht : ∀ k ∈ xs, f (atom k) = z := fun k hk => h k (by simp [hk])
    simp [total, hx, ih ht, Int.add_mul, Int.add_comm]

theorem median_attains (below above : List Int) (t half tieWeight : Int)
    (hl : (below.length : Int) ≤ half) (hu : (above.length : Int) ≤ half)
    (weight : (below.length : Int) + tieWeight + (above.length : Int) = 2 * half)
    (low : ∀ k ∈ below, k < t) (high : ∀ k ∈ above, t < k) :
    let rows := medianRows below above t half
    Fair rows ∧ Valid rows ∧
    (half - (above.length : Int)) + (half - (below.length : Int)) = tieWeight ∧
    signed rows = radius rows t := by
  dsimp only
  let rows := medianRows below above t half
  have fair : Fair rows := by
    change total bias (_ ++ _) = 0
    rw [total_append, map_constant below lowerAtom bias (-1) (by intro k _; rfl)]
    simp only [total]
    rw [map_constant above upperAtom bias 1 (by intro k _; rfl)]
    simp [bias]
    omega
  have valid : Valid rows := by
    intro a ha
    change a ∈ (_ ++ _) at ha
    rcases List.mem_append.mp ha with h | h
    · obtain ⟨_, _, rfl⟩ := List.mem_map.mp h
      simp [lowerAtom, upperAtom]
    · rcases List.mem_cons.mp h with h | h
      · subst a
        change 0 ≤ half - (above.length : Int) ∧ 0 ≤ half - (below.length : Int)
        exact ⟨by omega, by omega⟩
      · obtain ⟨_, _, rfl⟩ := List.mem_map.mp h
        simp [lowerAtom, upperAtom]
  have noMiss : total (fun a => missed a t) rows = 0 := by
    change total _ (_ ++ _) = 0
    rw [total_append]
    have l : ∀ k ∈ below, missed (lowerAtom k) t = 0 := by
      intro k hk
      simp [missed, lowerAtom, low k hk]
    have u : ∀ k ∈ above, missed (upperAtom k) t = 0 := by
      intro k hk
      have h : ¬ k < t := by have := high k hk; omega
      simp [missed, upperAtom, h]
    rw [map_constant _ _ _ _ l]
    simp only [total]
    rw [map_constant _ _ _ _ u]
    simp [missed, distance]
  have hg := gap_identity rows t
  change total bias rows = 0 at fair
  rw [fair, noMiss] at hg
  exact ⟨fair, valid, by omega, by simpa using hg.symm⟩

end HeldCountMedian
