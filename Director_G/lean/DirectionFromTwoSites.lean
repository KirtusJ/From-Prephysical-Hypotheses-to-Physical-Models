import Std

/-! Two position-controlled toggles of the same moving bit. Sites are
integer lifts of the cyclic base. The bit is initially false. -/
namespace DirectionFromTwoSites

def periodic (N : Nat) (v : Int → Bool) : Prop :=
  ∀ x, v (x+(N:Int)) = v x

/-- Conditions for XORing u(x) before the tick and v(y) after:
the toggle values agree for R and differ for L. -/
def writesRail (u v : Int → Bool) : Prop :=
  ∀ x, u x = v (x+1) ∧ u x ≠ v (x-1)

theorem characterise (u v : Int → Bool) :
    writesRail u v ↔ (∀ x, u x = v (x+1)) ∧ (∀ x, v (x+2) = !(v x)) := by
  constructor
  · intro h
    refine ⟨fun x => (h x).1,?_⟩
    intro x
    obtain ⟨a,b⟩ := h (x+1)
    have xy : v (x+2)≠v x := by simpa [a,Int.add_assoc] using b
    cases hx : v x <;> cases hy : v (x+2) <;> simp_all
  · rintro ⟨h,g⟩ x
    refine ⟨h x,?_⟩
    have e := g (x-1)
    rw [show x-1+2=x+1 by omega] at e
    rw [h x,e]
    cases v (x-1) <;> decide

/-- Any N-periodic readout with the two-step complement law forces 4|N.
Applying a displacement of 2N is simultaneously N complement steps
and two periods, forcing N even. A displacement of N then forces N/2 even. -/
theorem period_divisible {N : Nat} (v : Int → Bool)
    (cycle : periodic N v) (step : ∀ x, v (x+2) = !(v x)) : 4 ∣ N := by
  have twice (j : Nat) : v (2*(j:Int)) = ((j%2==1) != v 0) := by
    induction j with
    | zero => simp
    | succ j ih =>
      rw [show 2*((j.succ:Int))=2*(j:Int)+2 by omega, step,ih]
      rcases (show j%2=0 ∨ j%2=1 by omega) with p|p
      · have q : (j+1)%2=1 := by omega
        simp [p,q]
      · have q : (j+1)%2=0 := by omega
        simp [p,q]
  have nperiod : v (N:Int) = v 0 := by simpa using cycle 0
  have double : v (2*(N:Int)) = v 0 := by
    rw [show 2*(N:Int)=(N:Int)+(N:Int) by omega, cycle, nperiod]
  have even_at (j : Nat) (same : v (2*(j:Int))=v 0) : j%2=0 := by
    have h := twice j
    rw [same] at h
    by_cases odd : j%2=1
    · cases q : v 0 <;> simp [odd,q] at h
    · omega
  have even := even_at N double
  have half_period : v (2*((N/2:Nat):Int))=v 0 := by
    rw [show 2*((N/2:Nat):Int)=(N:Int) by omega,nperiod]
  have half := even_at (N/2) half_period
  exact ⟨N/4, by omega⟩

def after (x : Int) := ((x/2)%2 == 1)
def before (x : Int) := after (x+1)

theorem explicit_step (x : Int) : after (x+2) = !(after x) := by
  unfold after
  rcases (show (x/2)%2=0 ∨ (x/2)%2=1 by omega) with p|p
  · have q : ((x+2)/2)%2=1 := by omega
    simp [p,q]
  · have q : ((x+2)/2)%2=0 := by omega
    simp [p,q]

theorem explicit_before (x : Int) : before x = (after x != (x%2==1)) := by
  unfold before after
  rcases (show x%4=0 ∨ x%4=1 ∨ x%4=2 ∨ x%4=3 by omega) with p|p|p|p
  all_goals
    first | have a : (x/2)%2=0 := by omega | have a : (x/2)%2=1 := by omega
    first | have b : ((x+1)/2)%2=0 := by omega | have b : ((x+1)/2)%2=1 := by omega
    first | have c : x%2=0 := by omega | have c : x%2=1 := by omega
    simp [a,b,c]

theorem period_four_iff (N : Nat) :
    (∃ u v : Int → Bool, periodic N u ∧ periodic N v ∧ writesRail u v) ↔ 4∣N := by
  constructor
  · rintro ⟨u,v,_,pv,write⟩
    exact period_divisible v pv ((characterise u v).mp write).2
  · rintro ⟨j,eq⟩
    have pv : periodic N after := by
      intro x
      unfold after
      have same : ((x+(N:Int))/2)%2=(x/2)%2 := by omega
      rw [same]
    refine ⟨before,after,?_,pv,(characterise _ _).mpr ⟨fun _ => rfl, explicit_step⟩⟩
    intro x
    unfold before
    rw [show x+(N:Int)+1=x+1+(N:Int) by omega, pv]

end DirectionFromTwoSites
