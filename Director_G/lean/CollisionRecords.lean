import Std

/-!
# Contact of two labelled particles on a one-dimensional half-cell mesh

At natural microtime t each particle moves one half-cell. A and B denote
the incoming coarse coordinates as integers; multiply by two for micro-sites.
The particles have opposite unit velocities. A contact changes the outgoing
directions and occurs before the next microstream, with no waiting tick.
-/
namespace CollisionRecords

abbrev Pair := Int × Int

def meetingTime (a b : Int) : Nat := (b-a).toNat

def free (a b : Int) (t : Nat) : Pair := (2*a+(t:Int),2*b-(t:Int))

/-- A reflected branch follows the free paths up to their coincidence and
then exchanges the free labels. The other branch transmits. -/
def trajectory (a b : Int) (reflect : Bool) (t : Nat) : Pair :=
  let f := free a b t
  if reflect && decide (meetingTime a b < t) then (f.2,f.1) else f

theorem meet_cast (a b : Int) (order : a<b) :
    (meetingTime a b : Int) = b-a := by
  unfold meetingTime
  omega

theorem free_contact (a b : Int) (order : a<b) (t : Nat) :
    (free a b t).1 = (free a b t).2 ↔ t=meetingTime a b := by
  have h := meet_cast a b order
  simp only [free]
  omega

theorem before (a b : Int) (reflect : Bool) (t : Nat) (early : t ≤ meetingTime a b) :
    trajectory a b reflect t = free a b t := by
  simp [trajectory,show ¬ meetingTime a b < t by omega]

theorem strictly_ordered_before (a b : Int) (order : a<b) (reflect : Bool)
    (t : Nat) (early : t < meetingTime a b) :
    (trajectory a b reflect t).1 < (trajectory a b reflect t).2 := by
  rw [before a b reflect t (by omega)]
  have h := meet_cast a b order
  simp only [free]
  omega

theorem unique_contact (a b : Int) (order : a<b) (reflect : Bool) (t : Nat) :
    (trajectory a b reflect t).1 = (trajectory a b reflect t).2 ↔
    t = meetingTime a b := by
  have h := free_contact a b order t
  unfold trajectory
  split
  · exact (eq_comm).trans h
  · exact h

theorem outgoing (a b : Int) (order : a<b) (reflect : Bool) (j : Nat) :
    trajectory a b reflect (meetingTime a b+j) =
    if reflect then (a+b-(j:Int),a+b+(j:Int)) else (a+b+(j:Int),a+b-(j:Int)) := by
  have h := meet_cast a b order
  cases reflect <;> simp [trajectory,free,Int.natCast_add,h]
  all_goals (try split) <;> (try simp only [Prod.mk.injEq]) <;> omega

theorem branches_separate (a b : Int) (order : a<b) (j : Nat) (positive : 0<j) :
    trajectory a b true (meetingTime a b+j) ≠ trajectory a b false (meetingTime a b+j) := by
  rw [outgoing a b order true,outgoing a b order false]
  intro equality
  have x := congrArg Prod.fst equality
  simp at x
  omega

/-- Incoming tick ends at contact if t+1 equals the meeting time. -/
theorem incoming_step (a b : Int) (reflect : Bool) (t : Nat) (early : t < meetingTime a b) :
    trajectory a b reflect (t+1) =
    ((trajectory a b reflect t).1+1,(trajectory a b reflect t).2-1) := by
  rw [before a b reflect (t+1) (by omega), before a b reflect t (by omega)]
  simp only [free,Int.natCast_succ]
  congr 1 <;> omega

/-- The very first post-contact tick already has the chosen outgoing directions. -/
theorem outgoing_step (a b : Int) (order : a<b) (reflect : Bool) (j : Nat) :
    let t := meetingTime a b+j
    let p := trajectory a b reflect t
    trajectory a b reflect (t+1) =
    if reflect then (p.1-1,p.2+1) else (p.1+1,p.2-1) := by
  dsimp only
  rw [show meetingTime a b+j+1=meetingTime a b+(j+1) by omega,
    outgoing a b order reflect (j+1),outgoing a b order reflect j]
  cases reflect <;> simp only [Bool.false_eq_true,if_false,if_true,Int.natCast_succ]
  all_goals congr 1 <;> omega

theorem separation_after (a b : Int) (order : a<b) (reflect : Bool) (j : Nat) :
    let p := trajectory a b reflect (meetingTime a b+j)
    max p.1 p.2 - min p.1 p.2 = 2*(j:Int) := by
  dsimp only
  rw [outgoing a b order reflect j]
  cases reflect <;> simp only [Bool.false_eq_true,if_false,if_true]
  all_goals omega

theorem hard_core (a b : Int) (order : a<b) (t : Nat) :
    let f := free a b t
    trajectory a b true t = (min f.1 f.2,max f.1 f.2) := by
  have h := meet_cast a b order
  simp only [trajectory,free,Bool.true_and,decide_eq_true_eq]
  split <;> congr 1 <;> omega

theorem coarse_contact (a b : Int) (order : a<b) (reflect : Bool) :
    (∃ j : Nat, (trajectory a b reflect (2*j)).1=(trajectory a b reflect (2*j)).2) ↔
    (b-a)%2=0 := by
  have h := meet_cast a b order
  simp only [unique_contact a b order reflect]
  constructor
  · rintro ⟨j,e⟩
    omega
  · intro hpar
    exact ⟨meetingTime a b/2,by omega⟩

theorem odd_cell_records (a b : Int) (order : a<b) (oddGap : (b-a)%2=1) :
    let t := meetingTime a b
    trajectory a b false (t-1) = (a+b-1,a+b+1) ∧
    trajectory a b true (t-1) = (a+b-1,a+b+1) ∧
    trajectory a b false (t+1) = (a+b+1,a+b-1) ∧
    trajectory a b true (t+1) = (a+b-1,a+b+1) ∧
    (t-1)%2=0 ∧ (t+1)%2=0 := by
  dsimp only
  have h := meet_cast a b order
  rw [before a b false _ (by omega),before a b true _ (by omega),
    outgoing a b order false 1,outgoing a b order true 1]
  simp only [free,Bool.false_eq_true,if_false,if_true]
  exact ⟨by congr 1 <;> omega,by congr 1 <;> omega,rfl,rfl,by omega,by omega⟩

structure Occupied where
  sites : Pair
  approaching : Bool      -- right-moving first label, left-moving second label
  deriving DecidableEq

/-- The sole branch-dependent interaction is a test of coincident sites.
After the chosen velocity update the regular stream moves both particles. -/
def tick (reflect : Bool) (p : Occupied) : Occupied :=
  let nextRail := if reflect && decide (p.sites.1=p.sites.2) then !p.approaching
                  else p.approaching
  if nextRail then ⟨(p.sites.1+1,p.sites.2-1),true⟩
  else ⟨(p.sites.1-1,p.sites.2+1),false⟩

def run (reflect : Bool) (p : Occupied) : Nat → Occupied
  | 0 => p
  | t+1 => tick reflect (run reflect p t)

def carrier (a b : Int) (reflect : Bool) (t : Nat) : Occupied :=
  ⟨trajectory a b reflect t, !(reflect && decide (meetingTime a b < t))⟩

theorem local_update (a b : Int) (order : a<b) (reflect : Bool) (t : Nat) :
    tick reflect (carrier a b reflect t) = carrier a b reflect (t+1) := by
  by_cases early : t < meetingTime a b
  · have separate : (trajectory a b reflect t).1 ≠ (trajectory a b reflect t).2 := by
      intro eq
      have := (unique_contact a b order reflect t).mp eq
      omega
    have direction := incoming_step a b reflect t early
    cases reflect <;> simp [tick,carrier,separate,show ¬meetingTime a b<t by omega,
      show ¬meetingTime a b<t+1 by omega,direction]
  · have h : t=meetingTime a b+(t-meetingTime a b) := by omega
    have direction := outgoing_step a b order reflect (t-meetingTime a b)
    rw [←h] at direction
    by_cases atSite : t=meetingTime a b
    · have same := (unique_contact a b order reflect t).mpr atSite
      cases reflect <;> simp [tick,carrier,same,show ¬meetingTime a b<t by omega,
        show meetingTime a b<t+1 by omega,direction]
    · have separate : (trajectory a b reflect t).1 ≠ (trajectory a b reflect t).2 :=
        fun eq => atSite ((unique_contact a b order reflect t).mp eq)
      cases reflect <;> simp [tick,carrier,separate,show meetingTime a b<t by omega,
        show meetingTime a b<t+1 by omega,direction]

theorem physical_run (a b : Int) (order : a<b) (reflect : Bool) (t : Nat) :
    run reflect ⟨(2*a,2*b),true⟩ t = carrier a b reflect t := by
  induction t with
  | zero => simp [run,carrier,trajectory,free]
  | succ t ih => rw [run,ih,local_update a b order]

end CollisionRecords
