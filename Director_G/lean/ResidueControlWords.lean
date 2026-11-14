import Std

/-! Whole-position masks for five ticks on three wires. In the occupied
parity of a ring of circumference `4*M`, equality of physical wells is
equality of deficits modulo `2*M`. We keep deficits on the integer lift
and reduce them only for the mask. `true` means L and `false` means R. -/
namespace ResidueControlWords

abbrev Word := List Bool
def stock : Word := [true,false,false,true,false]
def flip : Word := [false,true,true,false,false]
def shift : Word := [false,true,false,true,false]

/-- Destination deficits of one word from the specified input site. -/
def arrivals (start : Nat) : Word → List Nat
  | [] => []
  | c :: cs => let d := start+c.toNat; d :: arrivals d cs

def masks (w : Word) : List (List Nat) :=
  List.zipWith (fun d ss => d :: ss) (arrivals 0 w)
    (List.zipWith (fun d e => [d,e]) (arrivals 2 stock) (arrivals 4 stock))

/-- Test the same new position for either arrival rail; branch in both
directions before filtering. Each survivor keeps the actual oriented word.
The outputs use the lifted deficit so wrap at `M=3` is visible to the test. -/
def accepted (period : Nat) : List (List Nat) → Nat → List Word
  | [], _ => [[]]
  | allowed :: rest, d => [false,true].flatMap fun c =>
    let next := d+c.toNat
    if (allowed.map (· % period)).contains (next % period) then
      (accepted period rest next).map (c :: ·)
    else []

/-- Check every prefix: at each named source the opposite child's well is
absent from that tick's mask. This also detects cross-arcs that die later. -/
def wrongBlocked (period : Nat) : Nat → Word → List (List Nat) → Bool
  | _, [], [] => true
  | d, c :: cs, allowed :: rest =>
    !(allowed.map (· % period)).contains ((d+(!c).toNat) % period) &&
      wrongBlocked period (d+c.toNat) cs rest
  | _, _, _ => false

def isolated (period : Nat) (w : Word) : Prop :=
  accepted period (masks w) 0 = [w] ∧
  accepted period (masks w) 2 = [stock] ∧
  accepted period (masks w) 4 = [stock] ∧
  wrongBlocked period 0 w (masks w) = true ∧
  wrongBlocked period 2 stock (masks w) = true ∧
  wrongBlocked period 4 stock (masks w) = true

private theorem all_isolated (period : Nat) (ring : period = 6 ∨ 8 ≤ period) :
    isolated period stock ∧ isolated period flip ∧ isolated period shift := by
  rcases ring with rfl | large
  · unfold isolated
    decide
  · have h0 : 0 % period = 0 := Nat.mod_eq_of_lt (by omega)
    have h1 : 1 % period = 1 := Nat.mod_eq_of_lt (by omega)
    have h2 : 2 % period = 2 := Nat.mod_eq_of_lt (by omega)
    have h3 : 3 % period = 3 := Nat.mod_eq_of_lt (by omega)
    have h4 : 4 % period = 4 := Nat.mod_eq_of_lt (by omega)
    have h5 : 5 % period = 5 := Nat.mod_eq_of_lt (by omega)
    have h6 : 6 % period = 6 := Nat.mod_eq_of_lt (by omega)
    have h7 : 7 % period = 7 := Nat.mod_eq_of_lt (by omega)
    simp [isolated, accepted, wrongBlocked, masks, arrivals, stock, flip, shift, List.zipWith,
      h0,h1,h2,h3,h4,h5,h6,h7, Nat.reduceAdd, Bool.toNat, List.flatMap,
      List.contains, List.elem, List.map]

theorem all_rings (M : Nat) (three : 3 ≤ M) :
    isolated (2*M) stock ∧ isolated (2*M) flip ∧ isolated (2*M) shift :=
  all_isolated _ (by omega)

/-- The period in deficits is N/gcd(N,2), including odd periods. -/
theorem all_periods (p : Nat) (width : 6 ≤ p) :
    isolated p stock ∧ isolated p flip := by
  by_cases seven : p = 7
  · subst p; unfold isolated; decide
  · have h := all_isolated p (by omega)
    exact ⟨h.1, h.2.1⟩

/-- Count actual LL arcs as a natural number before reduction at any order. -/
def llCount (previous : Bool) : Word → Nat
  | [] => 0
  | c :: cs => (previous && c).toNat + llCount c cs

theorem one_gain_counts :
    llCount false stock = 0 ∧ llCount false flip = 1 ∧
    llCount false [true,true,false] = 1 ∧
    llCount false [false,true,true] = 1 ∧
    llCount false [true,true,false,false] = 1 := by decide

/-- The common starting clock includes the physical launch position.
Departure deficit d has gain floor((clock-2*d)/2); on moving left the
next deficit increases by one. An LL pair flips the signed history. -/
def physicalGain (clock d : Int) : Word → Int
  | [] => 0
  | c :: cs => (clock-2*d)/2 + physicalGain (clock+1) (d+(c.toNat:Int)) cs

def clockSum (t : Int) : Int := t/2+(t+1)/2+(t+2)/2+(t+3)/2+(t+4)/2

def negative (previous : Bool) : Word → Bool
  | [] => false
  | c :: cs => (previous && c) != negative c cs

theorem signs_and_endpoints :
    negative false stock = false ∧ negative false flip = true ∧
    negative false shift = false ∧
    [stock,flip,shift].all (fun w => w.getLast? == some false &&
      (arrivals 0 w).getLast? == some 2) = true := by decide

theorem gains (t d : Int) :
    physicalGain t d stock = clockSum t - 5*d - 5 ∧
    physicalGain t d flip = clockSum t - 5*d - 5 ∧
    physicalGain t d shift = clockSum t - 5*d - 4 := by
  simp [physicalGain, clockSum, stock, flip, shift, Bool.toNat]
  omega

end ResidueControlWords
