import Std

/-!
# A spectator-selective difference of uniform electric string energies

The two distinct occupied modes can be listed in either order. A layout gives
each mode a distinct position in the chain. The energy counts bonds between
the two positions. All identities are pointwise on the occupation basis.
-/
namespace StringControl

def energy (x y : Nat) : Int := ((x - y : Nat) : Int) + ((y - x : Nat) : Int)

def boundarySwap : Nat → Nat
  | 0 => 1
  | 1 => 0
  | k + 2 => k + 2

def interiorSwap : Nat → Nat
  | 0 => 0
  | 1 => 2
  | 2 => 1
  | k + 3 => k + 3

def response (s : Nat → Nat) (x y : Nat) : Int :=
  energy x y - energy (s x) (s y)

def occupied {α : Type} [DecidableEq α] (u x y : α) : Int :=
  if u = x ∨ u = y then 1 else 0

def pairLamp {α : Type} [DecidableEq α] (h u x y : α) : Int :=
  occupied h x y * occupied u x y

theorem pairLamp_is_pair {α : Type} [DecidableEq α] (h u x y : α) (hu : h ≠ u) :
    pairLamp h u x y = 1 ↔ (x = h ∧ y = u) ∨ (x = u ∧ y = h) := by
  by_cases hx : h = x <;> by_cases hy : h = y <;>
    by_cases ux : u = x <;> by_cases uy : u = y <;>
    simp_all [pairLamp, occupied, eq_comm]

theorem boundary_response (x y : Nat) (distinct : x ≠ y) :
    response boundarySwap x y = occupied 0 x y - occupied 1 x y := by
  rcases x with _ | (_ | x) <;> rcases y with _ | (_ | y) <;>
    simp_all [response, boundarySwap, energy, occupied] <;> omega

theorem interior_response (x y : Nat) (distinct : x ≠ y) :
    response interiorSwap x y = occupied 1 x y - occupied 2 x y -
      2 * (pairLamp 0 1 x y - pairLamp 0 2 x y) := by
  rcases x with _ | (_ | (_ | x)) <;> rcases y with _ | (_ | (_ | y)) <;>
    simp_all [response, interiorSwap, energy, occupied, pairLamp] <;> omega

def Injective {α β : Type} (f : α → β) := ∀ ⦃x y⦄, f x = f y → x = y

theorem occupied_layout {α : Type} [DecidableEq α] (f : α → Nat)
    (inj : Injective f) (u x y : α) :
    occupied (f u) (f x) (f y) = occupied u x y := by
  have eq_iff (v : α) : f u = f v ↔ u = v := ⟨fun q => inj q, congrArg f⟩
  simp only [occupied, eq_iff]

theorem pair_layout {α : Type} [DecidableEq α] (f : α → Nat) (inj : Injective f)
    (h u x y : α) : pairLamp (f h) (f u) (f x) (f y) = pairLamp h u x y := by
  simp only [pairLamp, occupied_layout f inj]

/-- The layouts jointly address u,v. Only the interior layout needs h on its
left. The right-hand side vanishes on configurations with both or neither of
u,v occupied and on configurations with a spectator other than h. -/
theorem isolate_spectator {α : Type} [DecidableEq α]
    (b i : α → Nat) (binj : Injective b) (iinj : Injective i)
    (h u v x y : α) (distinct : x ≠ y)
    (bu : b u = 0) (bv : b v = 1) (ih : i h = 0) (iu : i u = 1) (iv : i v = 2) :
    response interiorSwap (i x) (i y) - response boundarySwap (b x) (b y) =
      -2 * (pairLamp h u x y - pairLamp h v x y) := by
  rw [interior_response _ _ (fun q => distinct (iinj q)),
      boundary_response _ _ (fun q => distinct (binj q))]
  have interior :
      occupied 1 (i x) (i y) - occupied 2 (i x) (i y) -
          2 * (pairLamp 0 1 (i x) (i y) - pairLamp 0 2 (i x) (i y)) =
        occupied u x y - occupied v x y -
          2 * (pairLamp h u x y - pairLamp h v x y) := by
    rw [← ih, ← iu, ← iv, occupied_layout i iinj, occupied_layout i iinj,
        pair_layout i iinj, pair_layout i iinj]
  have boundary : occupied 0 (b x) (b y) - occupied 1 (b x) (b y) =
      occupied u x y - occupied v x y := by
    rw [← bu, ← bv, occupied_layout b binj, occupied_layout b binj]
  rw [interior, boundary]
  omega

/-- For a mode rotation mixing u and v, each spectator k gives one edge
{u,k} ↔ {v,k}. The diagonal contrast P_hu−P_hv has a nonzero difference
across precisely the edge with spectator h. This is the scalar factor
which multiplies that matrix element in a diagonal commutator. -/
theorem edge_contrast {α : Type} [DecidableEq α] (h u v k : α)
    (hu : h ≠ u) (hv : h ≠ v) (uv : u ≠ v) (ku : k ≠ u) (kv : k ≠ v) :
    (pairLamp h u u k - pairLamp h v u k) -
      (pairLamp h u v k - pairLamp h v v k) = if h = k then 2 else 0 := by
  by_cases q : h = k <;>
    simp [pairLamp, occupied, hu, hv, uv, Ne.symm uv, Ne.symm ku, Ne.symm kv, q]

end StringControl

open StringControl in
#print axioms isolate_spectator
open StringControl in
#print axioms edge_contrast
open StringControl in
#print axioms pairLamp_is_pair
