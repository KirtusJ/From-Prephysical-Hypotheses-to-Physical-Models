import Std

/-!
# A counter carried by a nearest-neighbour probe

The two particle positions are parked during a tour of the ring. The probe
starts at the second position. At each tick it compares its present site
with the first position, conditionally translates its cyclic sheet by a
function of its on-board counter, then advances one site and one counter tick.
All claims are about this finite rule on basis coordinates.
-/
namespace LocalMediator

variable {n m : Nat}

/-- Physical rings have orders n+1 and m+1, including order one. -/
def residue (n k : Nat) : Fin (n+1) := ⟨k % (n+1), Nat.mod_lt _ (by omega)⟩

def siteAt (b : Fin (n+1)) (t : Nat) := residue n (b.val+t)

def offset (a b : Fin (n+1)) : Fin (n+1) :=
  if h : b.val ≤ a.val then ⟨a.val-b.val, by omega⟩
  else ⟨n+1+a.val-b.val, by omega⟩

private theorem wrap_once {x : Nat} (hx : x < 2*(n+1)) :
    x % (n+1) = if x < n+1 then x else x-(n+1) := by
  split
  · exact Nat.mod_eq_of_lt (by omega)
  · rw [Nat.mod_eq_sub_mod (by omega : n+1 ≤ x), Nat.mod_eq_of_lt (by omega)]

/-- Within one period, the comparison fires exactly at the oriented distance. -/
theorem encounter_iff (a b : Fin (n+1)) {t : Nat} (ht : t < n+1) :
    siteAt b t = a ↔ t = (offset a b).val := by
  have hb := b.isLt
  have ha := a.isLt
  rw [Fin.ext_iff]
  change (b.val+t)%(n+1) = a.val ↔ _
  rw [wrap_once (by omega)]
  unfold offset
  split <;> split <;> simp only <;> omega

structure Probe (n m : Nat) where
  site : Fin (n+1)
  clock : Fin (n+1)
  sheet : Fin (m+1)
  deriving DecidableEq

def tick (a : Fin (n+1)) (g : Fin (n+1) → Fin (m+1)) (p : Probe n m) : Probe n m :=
  ⟨siteAt p.site 1, siteAt p.clock 1,
   if p.site = a then p.sheet + g p.clock else p.sheet⟩

def run (a : Fin (n+1)) (g : Fin (n+1) → Fin (m+1)) (p : Probe n m) :
    Nat → Probe n m
  | 0 => p
  | t+1 => tick a g (run a g p t)

private theorem site_period (b : Fin (n+1)) : siteAt b (n+1) = b := by
  apply Fin.ext
  simp [siteAt, residue, Nat.mod_eq_of_lt b.isLt]

private theorem next_site (b : Fin (n+1)) (t : Nat) :
    siteAt (siteAt b t) 1 = siteAt b (t+1) := by
  apply Fin.ext
  change ((b.val+t)%(n+1)+1)%(n+1) = (b.val+(t+1))%(n+1)
  simp [Nat.add_assoc]

theorem partial_tour (a b : Fin (n+1)) (g : Fin (n+1) → Fin (m+1))
    (s : Fin (m+1)) (t : Nat) (ht : t ≤ n+1) :
    run a g ⟨b,0,s⟩ t =
      ⟨siteAt b t, siteAt 0 t,
        if (offset a b).val < t then s + g (offset a b) else s⟩ := by
  induction t with
  | zero =>
    have hb := b.isLt
    simp [run, siteAt, residue, Nat.mod_eq_of_lt hb]
  | succ t ih =>
    change tick a g (run a g _ t) = _
    rw [ih (by omega)]
    unfold tick
    simp only [next_site, encounter_iff a b (by omega : t < n+1)]
    by_cases hit : t = (offset a b).val
    · have clock : siteAt (0 : Fin (n+1)) t = offset a b := by
        apply Fin.ext
        change (0+t)%(n+1) = _
        simpa [Nat.mod_eq_of_lt (by omega : t < n+1)] using hit
      have before : ¬ (offset a b).val < t := by omega
      have after : (offset a b).val < t+1 := by omega
      simp only [hit.symm, before, after, clock, if_true, if_false, Nat.lt_irrefl,
        Nat.lt_succ_self]
    · have unchanged : ((offset a b).val < t+1) ↔ (offset a b).val < t := by omega
      simp [hit, unchanged]

/-- A complete tour restores the position and counter and applies exactly the
desired two-position sheet translation, with its signed residue represented in Fin. -/
theorem full_tour (a b : Fin (n+1)) (g : Fin (n+1) → Fin (m+1)) (s : Fin (m+1)) :
    run a g ⟨b,0,s⟩ (n+1) = ⟨b,0,s + g (offset a b)⟩ := by
  rw [partial_tour a b g s _ (by omega), if_pos (offset a b).isLt]
  rw [site_period b, site_period 0]

private theorem site_compose (b : Fin (n+1)) (u v : Nat) :
    siteAt (siteAt b u) v = siteAt b (u+v) := by
  apply Fin.ext
  change ((b.val+u)%(n+1)+v)%(n+1) = (b.val+(u+v))%(n+1)
  simp [Nat.add_assoc]

private theorem fin_add_comm (x y : Fin (n+1)) : x+y = y+x := by
  apply Fin.ext
  change (x.val+y.val)%(n+1) = (y.val+x.val)%(n+1)
  rw [Nat.add_comm]

private theorem subtract_gain (s c : Fin (m+1)) : offset (s+c) c = s := by
  have h : siteAt c s.val = s+c := fin_add_comm c s
  exact Fin.ext ((encounter_iff (s+c) c s.isLt).mp h).symm

private theorem restore_gain (s c : Fin (m+1)) : offset s c + c = s := by
  rw [fin_add_comm]
  exact (encounter_iff s c (offset s c).isLt).mpr rfl

/-- Undo streaming first; undo the modular translation at the recovered
departure coordinate with the recovered clock. One backward edge is a local
inverse even though its representative as a rightward offset is n. -/
def untick (a : Fin (n+1)) (g : Fin (n+1) → Fin (m+1)) (p : Probe n m) : Probe n m :=
  let oldSite := siteAt p.site n
  let oldClock := siteAt p.clock n
  ⟨oldSite, oldClock, if oldSite = a then offset p.sheet (g oldClock) else p.sheet⟩

/-- The elementary operation is a permutation on the entire probe, clock,
and cyclic sheet state space, including probe states with arbitrary clocks. -/
theorem reversible_tick (a : Fin (n+1)) (g : Fin (n+1) → Fin (m+1)) (p : Probe n m) :
    untick a g (tick a g p) = p ∧ tick a g (untick a g p) = p := by
  cases p with
  | mk x c s =>
    constructor
    · simp only [untick, tick, site_compose, Nat.add_comm 1 n, site_period]
      by_cases h : x = a <;> simp [h, subtract_gain]
    · simp only [untick, tick, site_compose, site_period]
      by_cases h : siteAt x n = a <;> simp [h, restore_gain]

/-- A superposition or signed path list may carry any coefficient type. The
pointwise tour restores each branch's own probe origin, carries its original
coefficient, and produces exactly the departure-dependent joint increment. -/
structure Term (C : Type) (n m : Nat) where
  a : Fin (n+1)
  b : Fin (n+1)
  sheet : Fin (m+1)
  coefficient : C

theorem tour_on_terms {C : Type} (g : Fin (n+1) → Fin (m+1)) (ts : List (Term C n m)) :
    ts.map (fun e => (e.a, e.b, run e.a g ⟨e.b,0,e.sheet⟩ (n+1), e.coefficient)) =
    ts.map (fun e => (e.a, e.b, (⟨e.b,0,e.sheet + g (offset e.a e.b)⟩ : Probe n m),
                     e.coefficient)) := by
  simp only [full_tour]

/-- Before the unique encounter has been processed the carrier has no signal.
Immediately after the encounter it contains the specified translated sheet. -/
theorem signal_time (a b : Fin (n+1)) (g : Fin (n+1) → Fin (m+1))
    (s : Fin (m+1)) :
    (run a g ⟨b,0,s⟩ (offset a b).val).sheet = s ∧
    (run a g ⟨b,0,s⟩ ((offset a b).val+1)).sheet = s + g (offset a b) := by
  have h := (offset a b).isLt
  simp [partial_tour a b g s _ (show (offset a b).val ≤ n+1 by omega),
        partial_tour a b g s _ (show (offset a b).val+1 ≤ n+1 by omega)]

/-- Any parking-then-release rule, including a signed multibranch walk step,
gets the same branch list after the full tour as after a direct sheet gate. -/
def mediatedStep {C : Type} (g : Fin (n+1) → Fin (m+1))
    (release : Term C n m → List (Term C n m)) (ts : List (Term C n m)) :=
  ts.flatMap fun e => release {e with sheet := (run e.a g ⟨e.b,0,e.sheet⟩ (n+1)).sheet}

def directStep {C : Type} (g : Fin (n+1) → Fin (m+1))
    (release : Term C n m → List (Term C n m)) (ts : List (Term C n m)) :=
  ts.flatMap fun e => release {e with sheet := e.sheet + g (offset e.a e.b)}

theorem release_after_tour {C : Type} (g : Fin (n+1) → Fin (m+1))
    (release : Term C n m → List (Term C n m)) (ts : List (Term C n m)) :
    mediatedStep g release ts = directStep g release ts := by
  simp [mediatedStep, directStep, full_tour]

theorem repeated_release {C : Type} (g : Fin (n+1) → Fin (m+1))
    (releases : List (Term C n m → List (Term C n m))) (ts : List (Term C n m)) :
    releases.foldl (fun ps next => mediatedStep g next ps) ts =
    releases.foldl (fun ps next => directStep g next ps) ts := by
  simp only [release_after_tour]

/-- For B=0 and A=n the first n ticks all miss a nonzero unit gain. The
final tick changes the sheet and returns the carrier to its launch cell. -/
theorem last_cell_control (n m : Nat) :
    (run (Fin.last n) (fun _ => (1 : Fin (m+2))) ⟨0,0,0⟩ n).sheet = 0 ∧
    run (Fin.last n) (fun _ => (1 : Fin (m+2))) ⟨0,0,0⟩ (n+1) =
       (⟨0,0,1⟩ : Probe n (m+1)) ∧ (1 : Fin (m+2)) ≠ 0 := by
  have d : (offset (Fin.last n) 0).val = n := by simp [offset]
  have early := (signal_time (Fin.last n) 0 (fun _ => (1 : Fin (m+2))) 0).1
  rw [d] at early
  exact ⟨early, by simp [full_tour], by
    intro h
    have := congrArg Fin.val h
    simp [Fin.val_one, Nat.mod_eq_of_lt (by omega : 1 < m+2)] at this⟩

end LocalMediator
