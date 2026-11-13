import Std

/-! A reversible binary position flag on signed integer path amplitudes.
A port label can contain both site and rail; the flag only sees the prescribed
Boolean function on that label. Lists allow distinct histories to arrive with
either sign at the same port. The result concerns the algebra of the proposed
instrument, conditional on coherent recording of this one bit. -/
namespace FlightWindow

def flag {α : Type} (inside : α → Bool) (q : α × Bool) : α × Bool :=
  (q.1, Bool.xor q.2 (inside q.1))

theorem flag_involution {α : Type} (inside : α → Bool) (q : α × Bool) :
    flag inside (flag inside q) = q := by
  obtain ⟨p,b⟩ := q
  cases b <;> cases h : inside p <;> simp [flag,h]

/-- Signed sum at a port, before squaring or normalization. -/
def tally {α : Type} [DecidableEq α] (p : α) : List (α × Int) → Int
  | [] => 0
  | (x,a) :: rest => (if x = p then a else 0) + tally p rest

def flagged {α : Type} (inside : α → Bool) (paths : List (α × Int)) :=
  paths.map fun (x,a) => (flag inside (x,false), a)

theorem conditional_tally {α : Type} [DecidableEq α] (inside : α → Bool)
    (paths : List (α × Int)) (p : α) (b : Bool) :
    tally (p,b) (flagged inside paths) =
      if inside p = b then tally p paths else 0 := by
  induction paths with
  | nil => simp [flagged,tally]
  | cons entry rest ih =>
    obtain ⟨x,a⟩ := entry
    change (if flag inside (x,false) = (p,b) then a else 0) +
        tally (p,b) (flagged inside rest) =
        if inside p = b then (if x = p then a else 0) + tally p rest else 0
    by_cases xp : x = p
    · subst x
      cases b <;> cases h : inside p <;> simp [flag,h,ih]
    · cases b <;> cases h : inside p <;> simp [flag,h,ih,xp]

/-- Reading the shared bit preserves cross terms between accepted inputs
that a later signed joining row sends to the same output. A permanent
port label would keep their contributions in distinct output bins. -/
theorem accepted_join {α : Type} [DecidableEq α] (inside : α → Bool)
    (p q : α) (hp : inside p = true) (hq : inside q = true) (distinct : p ≠ q)
    (a b : Int) :
    let word := flagged inside [(p,a),(q,b)]
    tally (p,true) word + tally (q,true) word = a+b := by
  dsimp only
  rw [conditional_tally,conditional_tally,if_pos hp,if_pos hq]
  simp [tally,distinct,Ne.symm distinct]

/-- An uncut output mapped to one common port, with either a retained
window bit or an orthogonal copy of each source port as its record. -/
theorem flag_versus_port_copy {α : Type} [DecidableEq α] (inside : α → Bool)
    (p q : α) (distinct : p ≠ q) (hp : inside p = true) (hq : inside q = true) :
    let paths : List (α × Int) := [(p,1),(q,1)]
    let common := tally (p,true) (flagged inside paths) +
                  tally (q,true) (flagged inside paths)
    let copied := paths.map fun h => (((),h.1),h.2)
    common*common = 4 ∧
      (tally ((),p) copied)^2 + (tally ((),q) copied)^2 = 2 := by
  dsimp only
  rw [accepted_join inside p q hp hq distinct]
  simp [tally,distinct,Ne.symm distinct]

end FlightWindow
