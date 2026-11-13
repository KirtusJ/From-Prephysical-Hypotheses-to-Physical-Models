import Std

/-! Sharp four-mode calibrations for a probability kernel on two residue
labels. Weights are natural numbers after a common rescaling, with arbitrary
total mass. Every frame in the proof is induced by a mode permutation.
No hypothesis factors the outcome probabilities of the two bonds. -/
namespace ResidueFrames

inductive Edge
  | ab | ac | ad | bc | bd | cd
  deriving DecidableEq, Repr
open Edge

def ends : Edge → Fin 4 × Fin 4
  | ab => (0,1) | ac => (0,2) | ad => (0,3)
  | bc => (1,2) | bd => (1,3) | cd => (2,3)

def edges : List Edge := [ab, ac, ad, bc, bd, cd]

/-- A fixed first reduction and a second reduction given by the same mode
permutation on every unordered endpoint pair. -/
def ModeFrame (route : Edge → Edge) : Prop :=
  ∃ p : Fin 4 → Fin 4, (∀ i j, p i = p j → i = j) ∧ ∀ e,
    let (i,j) := ends e
    ends (route e) = (p i,p j) ∨ ends (route e) = (p j,p i)

def Normalized (F : Edge → Edge → Nat) (mass : Nat) : Prop :=
  ∀ route, ModeFrame route → (edges.map fun e => F e (route e)).sum = mass

def neighbor : Edge → Bool
  | ac | ad | bc | bd => true
  | _ => false

def relabel (first last : Bool) (i : Fin 4) : Fin 4 :=
  if i = 0 then (if first then 1 else 0)
  else if i = 1 then (if first then 0 else 1)
  else if i = 2 then (if last then 3 else 2)
  else (if last then 2 else 3)

def edgeRoute (first last : Bool) : Edge → Edge
  | ab => ab | cd => cd
  | ac => if first then (if last then bd else bc) else (if last then ad else ac)
  | ad => if first then (if last then bc else bd) else (if last then ac else ad)
  | bc => if first then (if last then ad else ac) else (if last then bd else bc)
  | bd => if first then (if last then ac else ad) else (if last then bc else bd)

theorem native_frame (first last : Bool) : ModeFrame (edgeRoute first last) := by
  refine ⟨relabel first last, ?_, ?_⟩
  · cases first <;> cases last <;> decide
  · intro e
    cases first <;> cases last <;> cases e <;> decide

theorem neighbors_reachable (p q : Edge)
    (hp : neighbor p = true) (hq : neighbor q = true) :
    ∃ a b, edgeRoute a b p = q := by
  cases p <;> cases q <;> first | contradiction | decide

theorem sharp_vanish (F : Edge → Edge → Nat) (mass : Nat)
    (frames : Normalized F mass) (sharp : F ab ab = mass)
    (p q : Edge) (hp : neighbor p = true) (hq : neighbor q = true) :
    F p q = 0 := by
  obtain ⟨a, b, hit⟩ := neighbors_reachable p q hp hq
  have total := frames _ (native_frame a b)
  simp only [edges, List.map_cons, List.map_nil, List.sum_cons, List.sum_nil,
    Nat.add_zero] at total
  rw [show edgeRoute a b ab = ab from rfl, sharp] at total
  have zero : F p (edgeRoute a b p) = 0 := by
    cases p <;> first | contradiction | omega
  simpa only [hit] using zero

def exchangeBonds : Edge → Edge
  | ab => cd | cd => ab | ad => bc | bc => ad | ac => ac | bd => bd

theorem exchange_is_mode_frame : ModeFrame exchangeBonds := by
  refine ⟨fun i => i+2, ?_, ?_⟩
  · decide
  · intro e; cases e <;> decide

theorem other_fixed_pair_zero (F : Edge → Edge → Nat) (mass : Nat)
    (frames : Normalized F mass) (sharp : F ab ab = mass) :
    F cd cd = 0 := by
  have total := frames _ (native_frame false false)
  simp [edges, edgeRoute, sharp] at total
  omega

theorem opposite_outputs (F : Edge → Edge → Nat) (mass : Nat)
    (frames : Normalized F mass) (sharp : F ab ab = mass) :
    F ab cd + F cd ab = mass := by
  have total := frames _ exchange_is_mode_frame
  simp only [edges, List.map_cons, List.map_nil, List.sum_cons, List.sum_nil,
    Nat.add_zero, exchangeBonds] at total
  rw [sharp_vanish F mass frames sharp ac ac rfl rfl,
      sharp_vanish F mass frames sharp ad bc rfl rfl,
      sharp_vanish F mass frames sharp bc ad rfl rfl,
      sharp_vanish F mass frames sharp bd bd rfl rfl] at total
  omega

def secondThird : Edge → Edge
  | ab => ac | ac => ab | ad => ad | bc => bc | bd => cd | cd => bd

theorem second_third_frame : ModeFrame secondThird := by
  refine ⟨fun i => if i = 1 then 2 else if i = 2 then 1 else i, ?_, ?_⟩
  · decide
  · intro e; cases e <;> decide

theorem composed_frame (r t : Edge → Edge) (hr : ModeFrame r) (ht : ModeFrame t) :
    ModeFrame (fun e => r (t e)) := by
  obtain ⟨p, ip, hp⟩ := hr
  obtain ⟨q, iq, hq⟩ := ht
  refine ⟨fun i => p (q i), fun _ _ h => iq _ _ (ip _ _ h), ?_⟩
  intro e
  have first := hq e
  have last := hp (t e)
  dsimp only at first last ⊢
  rcases first with forward | reverse
  · rw [forward] at last
    exact last
  · rw [reverse] at last
    exact last.elim Or.inr Or.inl

def viaSwap (a b : Bool) (e : Edge) :=
  edgeRoute a b (secondThird (edgeRoute a b e))

/-- After both orientations of the calibrated single hop, the only
undetermined weights are the split between the two opposite labels. -/
theorem calibrated_opposite_neighbor (F : Edge → Edge → Nat) (mass q r : Nat)
    (frames : Normalized F mass) (sharp : F ab ab = mass) (split : q+r=mass)
    (stay : ∀ e, neighbor e = true → F ab e = q)
    (move : ∀ e, neighbor e = true → F e ab = r)
    (e : Edge) (he : neighbor e = true) : F cd e = 0 ∧ F e cd = 0 := by
  have for_each (a b : Bool) :
      F cd (viaSwap a b cd) = 0 ∧ F (viaSwap a b cd) cd = 0 := by
    have total := frames _ (composed_frame _ _ (native_frame a b)
      (composed_frame _ _ second_third_frame (native_frame a b)))
    simp only [edges, List.map_cons, List.map_nil, List.sum_cons, List.sum_nil,
      Nat.add_zero] at total
    have zz (p t : Edge) (hp : neighbor p = true) (ht : neighbor t = true) :
        F p t = 0 := sharp_vanish F mass frames sharp p t hp ht
    cases a <;> cases b <;>
      simp [viaSwap, edgeRoute, secondThird,
        stay ac rfl, stay ad rfl, stay bc rfl, stay bd rfl,
        move ac rfl, move ad rfl, move bc rfl, move bd rfl,
        zz ac ac rfl rfl, zz ad ad rfl rfl, zz bc bc rfl rfl, zz bd bd rfl rfl]
        at total ⊢ <;> omega
  have hits : ∃ a b, viaSwap a b cd = e := by
    cases e <;> first | contradiction | decide
  obtain ⟨a,b,hit⟩ := hits
  simpa only [hit] using for_each a b

/-- Read bonds (a,c) and (b,d) from source ab. First reduction fixes every
mode, second swaps both bonds. This second reduction maps ab↔cd, ad↔bc.
Thus the probabilities for "a stayed" and "b stayed" agree including both
mixed output bins. The cd term is absent from both marginals. -/
theorem equal_stay_marginals (F : Edge → Edge → Nat) (mass : Nat)
    (frames : Normalized F mass) (sharp : F ab ab = mass) :
    F ab cd + F ad bc = F ab cd + F bc ad := by
  rw [sharp_vanish F mass frames sharp ad bc rfl rfl,
      sharp_vanish F mass frames sharp bc ad rfl rfl]

/-- In any finite mode set, after all entries away from the sharp row and
column have vanished, every derangement of the source label gives a
two-entry equation. Applied to a route taking s to a and b to s for two
far labels a,b, this identifies the remaining far split. -/
theorem two_entries {α : Type} [DecidableEq α] (labels : List α)
    (F : α → α → Nat) (s a b : α) (g : α → α) (gs : g s = a)
    (pre : ∀ x, g x = s ↔ x = b) (bs : b ≠ s)
    (one_s : labels.count s = 1) (one_b : labels.count b = 1)
    (zero : ∀ x y, x ≠ s → y ≠ s → F x y = 0) :
    (labels.map fun x => F x (g x)).sum = F s a + F b s := by
  have formula (xs : List α) :
      (xs.map fun x => F x (g x)).sum = xs.count s * F s a + xs.count b * F b s := by
    induction xs with
    | nil => simp
    | cons x xs ih =>
      by_cases ps : x = s
      · subst x
        simp [gs, bs, Ne.symm bs, ih, Nat.add_mul, Nat.add_assoc, Nat.add_comm,
          Nat.add_left_comm]
      · by_cases pb : x = b
        · subst x
          simp [ps, Ne.symm ps, (pre b).mpr rfl, ih, Nat.add_mul, Nat.add_assoc,
            Nat.add_comm, Nat.add_left_comm]
        · have away : g x ≠ s := fun hx => pb ((pre x).mp hx)
          simp [ps, pb, Ne.symm ps, Ne.symm pb, zero x (g x) ps away, ih]
  simpa [one_s, one_b] using formula labels

end ResidueFrames
