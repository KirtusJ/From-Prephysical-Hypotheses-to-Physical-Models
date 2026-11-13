import Std

/-!
# Signed path counts on the moving corridor of a physical position ring

The step enumerates both signed Hadamard successors at their actual residue
coordinates, then applies the all-yes mask to each successor. Repeated list
entries represent distinct histories, even when their endpoints coincide.
-/
namespace CorridorCounts

structure Cell where
  site : Int
  left : Bool
  negative : Bool
  deriving DecidableEq

def advance (N : Nat) (c : Cell) (left : Bool) : Cell :=
  ⟨(c.site + (if left then -1 else 1)) % (N:Int), left,
   xor c.negative (c.left && left)⟩

def leading (N t : Nat) : Cell := ⟨(t:Int) % N,false,false⟩
def trailing (N t : Nat) (left : Bool) : Cell := ⟨((t:Int)-2) % N,left,false⟩

def keep (N t : Nat) (c : Cell) : Bool :=
  (c.site == (leading N t).site && !c.left) ||
  (c.site == (trailing N t false).site && (!c.left || t % N == 1))

def children (N t : Nat) (c : Cell) : List Cell :=
  [advance N c false, advance N c true].filter (keep N (t+1))

def paths (N : Nat) : Nat → List Cell
  | 0 => [leading N 0]
  | t+1 => (paths N t).flatMap (children N t)

private theorem distinct_lags (N : Nat) (size : 6 ≤ N) (base : Int) :
    base % (N:Int) ≠ (base-2) % N ∧ base % (N:Int) ≠ (base-4) % N := by
  have pos₂ : (2:Int) % N = 2 := Int.emod_eq_of_lt (by decide) (by omega)
  have pos₄ : (4:Int) % N = 4 := Int.emod_eq_of_lt (by decide) (by omega)
  constructor
  · intro eq
    have h := Int.sub_emod base (base-2) (N:Int)
    rw [eq, Int.sub_self, Int.zero_emod] at h
    have dif : base - (base-2) = 2 := by omega
    rw [dif,pos₂] at h
    contradiction
  · intro eq
    have h := Int.sub_emod base (base-4) (N:Int)
    rw [eq, Int.sub_self, Int.zero_emod] at h
    have dif : base - (base-4) = 4 := by omega
    rw [dif,pos₄] at h
    contradiction

private theorem leading_children (N t : Nat) (size : 6 ≤ N) :
    children N t (leading N t) =
      leading N (t+1) :: (if (t+1)%N = 1 then [trailing N (t+1) true] else []) := by
  have p := (distinct_lags N size ((t:Int)+1)).1
  have h : (t:Int)+1-2 = t+(-1:Int) := by omega
  rw [h] at p
  by_cases window : (t+1)%N = 1 <;>
    simp [children, advance, keep, leading, trailing, Int.natCast_succ, h, p, Ne.symm p, window]

private theorem trailing_children (N t : Nat) (size : 6 ≤ N) (left : Bool) :
    children N t (trailing N t left) = [trailing N (t+1) false] := by
  have h₁ : (t:Int)-2+1 = (t+1)-2 := by omega
  have h₂ : (t:Int)-2+(-1) = (t+1)-4 := by omega
  have h₃ : (t:Int)+1-2-2 = (t+1)-4 := by omega
  have p := distinct_lags N size ((t:Int)+1)
  have q := (distinct_lags N size ((t:Int)+1-2)).1
  rw [h₃] at q
  cases left <;> simp [children, advance, keep, leading, trailing, Int.natCast_succ,
                       h₁, h₂, Ne.symm p.2, Ne.symm q]

private def openings (N : Nat) : Nat → Nat
  | 0 => 0
  | t+1 => openings N t + (if (t+1)%N = 1 then 1 else 0)

private def shape (N t : Nat) (openNow : Bool) (oldTurns : Nat) : List Cell :=
  leading N t :: ((if openNow then [trailing N t true] else []) ++
                  List.replicate oldTurns (trailing N t false))

private theorem shape_step (N t : Nat) (size : 6 ≤ N) (now : Bool) (old : Nat) :
    (shape N t now old).flatMap (children N t) =
      shape N (t+1) (decide ((t+1)%N=1)) (old + if now then 1 else 0) := by
  cases now <;> by_cases w : (t+1)%N=1 <;>
    simp [shape, List.flatMap_cons, List.flatMap_replicate, leading_children N t size,
          trailing_children N t size, w, List.replicate_succ]

theorem physical_paths (N t : Nat) (size : 6 ≤ N) :
    paths N (t+1) = shape N (t+1) (decide ((t+1)%N=1)) (openings N t) := by
  induction t with
  | zero =>
    change (shape N 0 false 0).flatMap (children N 0) = _
    exact shape_step N 0 size false 0
  | succ t ih =>
    change (paths N (t+1)).flatMap (children N (t+1)) = _
    rw [ih, shape_step N (t+1) size]
    simp [openings]

private theorem window_iff (N t : Nat) (size : 6 ≤ N) :
    (t+2)%N = 1 ↔ N ∣ t+1 := by
  rw [Nat.dvd_iff_mod_eq_zero]
  have add := Nat.add_mod (t+1) 1 N
  have one : 1 % N = 1 := Nat.mod_eq_of_lt (by omega)
  rw [one] at add
  change (t+2)%N = ((t+1)%N+1)%N at add
  rw [add]
  have lt := Nat.mod_lt (t+1) (show 0 < N by omega)
  by_cases small : (t+1)%N+1 < N
  · rw [Nat.mod_eq_of_lt small]
    omega
  · have edge : (t+1)%N+1=N := by omega
    rw [edge, Nat.mod_self]
    omega

private theorem openings_succ (N t : Nat) (size : 6 ≤ N) :
    openings N (t+1) = 1+t/N := by
  induction t with
  | zero => simp [openings, Nat.mod_eq_of_lt (show 1 < N by omega)]
  | succ t ih =>
    change openings N (t+1) + (if (t+2)%N=1 then 1 else 0) = _
    simp only [ih, window_iff N t size, Nat.succ_div, Nat.add_assoc]

private theorem openings_periods (N n : Nat) (size : 6 ≤ N) :
    openings N (n*N) = n := by
  cases n with
  | zero => simp [openings]
  | succ n =>
    have cut : (n+1)*N = ((N-1)+n*N)+1 := by rw [Nat.succ_mul]; omega
    rw [cut, openings_succ N _ size, Nat.add_mul_div_right _ _ (by omega),
        Nat.div_eq_of_lt (show N-1 < N by omega)]
    omega

/-- At every stopping horizon there are precisely one straight path, one fresh
left path, and n older single-left paths. Every surviving count is positive.
The coordinates below are actual residues modulo N. -/
theorem stopping_histogram (N n : Nat) (size : 6 ≤ N) :
    paths N (n*N+1) =
      leading N (n*N+1) :: trailing N (n*N+1) true ::
        List.replicate n (trailing N (n*N+1) false) := by
  rw [physical_paths N _ size, openings_periods N n size]
  have window : (n*N+1)%N = 1 := by
    rw [Nat.add_comm, Nat.add_mul_mod_self_right, Nat.mod_eq_of_lt (by omega)]
  simp [shape, window]

private def signedSum (cells : List Cell) : Int :=
  (cells.map (fun c => if c.negative then (-1 : Int) else 1)).sum

/-- Copy the coarse trailing-site flag, then propagate one step with a chosen
output direction. Within a flag and direction the successor site is fixed. -/
def portCount (N t : Nat) (trailingFlag left : Bool) : Int :=
  signedSum (((paths N t).filter
      (fun c => (c.site == (trailing N t false).site) == trailingFlag)).map
    (fun c => advance N c left))

private theorem signed_replicates (n : Nat) (z : Int) :
    (List.replicate n z).sum = (n:Int)*z := by
  induction n with
  | zero => simp
  | succ n ih => simp [List.replicate_succ, ih, Int.natCast_succ, Int.add_mul, Int.add_comm]

theorem after_free_step (N n : Nat) (size : 6 ≤ N) :
    portCount N (n*N+1) true false = (n:Int)+1 ∧
    portCount N (n*N+1) true true = (n:Int)-1 ∧
    portCount N (n*N+1) false false = 1 ∧
    portCount N (n*N+1) false true = 1 := by
  have separated := (distinct_lags N size (((n*N+1:Nat):Int))).1
  simp only [Int.natCast_add, Int.natCast_mul, Int.natCast_one] at separated
  simp [portCount, signedSum, stopping_histogram N n size, leading, trailing, advance,
        separated, List.filter_cons, List.filter_replicate, List.map_replicate,
        signed_replicates, Function.comp_def]
  omega

/-! Track the actual sheet displacement as well as the cell. An integer
component suffices before reduction modulo a sheet order; several components
can be selected separately. -/

structure Lifted where
  cell : Cell
  sheet : Int
  deriving DecidableEq

def liftedChildren (N t : Nat) (g : Int → Int) (w : Lifted) : List Lifted :=
  (children N t w.cell).map fun c => ⟨c,w.sheet + g w.cell.site⟩

def liftedPaths (N : Nat) (g : Int → Int) : Nat → List Lifted
  | 0 => [⟨leading N 0,0⟩]
  | t+1 => (liftedPaths N g t).flatMap (liftedChildren N t g)

private def load (N : Nat) (g : Int → Int) : Nat → Int
  | 0 => 0
  | t+1 => load N g t + g ((t:Int)%N)

private def turnLoad (N : Nat) (g : Int → Int) (t : Nat) : Int :=
  load N g t + g ((-1:Int)%N) + g (0%(N:Int)) -
    g (((t:Int)-2)%N) - g (((t:Int)-1)%N)

private theorem turnLoad_step (N t : Nat) (g : Int → Int) :
    turnLoad N g (t+1) = turnLoad N g t + g (((t:Int)-2)%N) := by
  have x : (t:Int)+1-2 = t-1 := by omega
  have y : (t:Int)+1-1 = t := by omega
  simp only [turnLoad, load, Int.natCast_succ, x, y]
  omega

private theorem turnLoad_window (N t : Nat) (g : Int → Int)
    (w : t%N=1) : turnLoad N g t = load N g t := by
  have window : (t:Int) % N = 1 := by exact_mod_cast w
  have h (j : Int) : ((t:Int)-j)%N=(1-j)%N := by
    rw [← Int.emod_sub_emod (t:Int) (N:Int) j, window]
  have a := h 2
  have b := h 1
  change ((t:Int)-2)%N = (-1:Int)%N at a
  change ((t:Int)-1)%N = 0%(N:Int) at b
  simp only [turnLoad, a, b]
  omega

private def decorate (N t : Nat) (g : Int → Int) (c : Cell) : Lifted :=
  ⟨c,if c.site == (leading N t).site then load N g t else turnLoad N g t⟩

private theorem lifted_leading (N t : Nat) (size : 6 ≤ N) (g : Int → Int) :
    liftedChildren N t g (decorate N t g (leading N t)) =
      (children N t (leading N t)).map (decorate N (t+1) g) := by
  have sep := (distinct_lags N size ((t:Int)+1)).1
  change (children N t (leading N t)).map _ = _
  rw [leading_children N t size]
  by_cases w : (t+1)%N = 1
  · have h := turnLoad_window N (t+1) g w
    simp [liftedChildren, leading_children N t size, w, decorate, leading, trailing,
          Int.natCast_succ, Ne.symm sep, h, load]
  · simp [liftedChildren, leading_children N t size, w, decorate, leading, load]

private theorem lifted_trailing (N t : Nat) (size : 6 ≤ N) (g : Int → Int) (left : Bool) :
    liftedChildren N t g (decorate N t g (trailing N t left)) =
      (children N t (trailing N t left)).map (decorate N (t+1) g) := by
  have sep := (distinct_lags N size (t:Int)).1
  have sep' := (distinct_lags N size ((t:Int)+1)).1
  change (children N t (trailing N t left)).map _ = _
  rw [trailing_children N t size]
  simp [liftedChildren, trailing_children N t size, decorate, leading, trailing,
        Int.natCast_succ, Ne.symm sep, Ne.symm sep', turnLoad_step]

private theorem flatMap_on_support (xs : List α) (f h : α → List β)
    (agree : ∀ x, x ∈ xs → f x = h x) : xs.flatMap f = xs.flatMap h := by
  induction xs with
  | nil => rfl
  | cons x xs ih =>
    simp only [List.flatMap_cons]
    rw [agree x (by simp), ih (by intro a ha; exact agree a (by simp [ha]))]

/-- The decorated list is equal to literal lifted propagation. Every trailing
history occupies the *same* sheet, including the fresh and returning paths at
the stopping horizon. The gain is arbitrary and evaluated at the departure
residue, hence periodicity is built into the physical lift. -/
theorem common_sheet (N t : Nat) (size : 6 ≤ N) (g : Int → Int) :
    liftedPaths N g t = (paths N t).map (decorate N t g) := by
  induction t with
  | zero => simp [liftedPaths, paths, decorate, load]
  | succ t ih =>
    simp only [liftedPaths, ih, paths, List.flatMap_map, List.map_flatMap, Function.comp_def]
    apply flatMap_on_support
    intro x hx
    cases t with
    | zero =>
      simp [paths] at hx
      subst x
      exact lifted_leading N 0 size g
    | succ t =>
      rw [physical_paths N t size] at hx
      simp only [shape, List.mem_cons, List.mem_append] at hx
      rcases hx with home | (fresh | returning)
      · subst x; exact lifted_leading N _ size g
      · by_cases w : (t+1)%N=1
        · simp [w] at fresh
          subst x; exact lifted_trailing N _ size g true
        · simp [w] at fresh
      · rcases List.mem_replicate.mp returning with ⟨_,rfl⟩
        exact lifted_trailing N _ size g false

theorem lifted_stopping_histogram (N n : Nat) (size : 6 ≤ N) (g : Int → Int) :
    liftedPaths N g (n*N+1) =
      ⟨leading N (n*N+1), load N g (n*N+1)⟩ ::
      ⟨trailing N (n*N+1) true, load N g (n*N+1)⟩ ::
      List.replicate n ⟨trailing N (n*N+1) false, load N g (n*N+1)⟩ := by
  have w : (n*N+1)%N = 1 := by
    rw [Nat.add_comm, Nat.add_mul_mod_self_right, Nat.mod_eq_of_lt (by omega)]
  rw [common_sheet N _ size g, stopping_histogram N n size]
  simp [decorate, turnLoad_window N _ g w]

/-- The old flag separates trailing and leading branches. At a chosen output
direction all paths in a flag reach one output sheet, even after the final
unmasked step. Thus summing signs at each combination of flag, site, direction
and sheet is legitimate without an independently supplied sector. -/
def liftedPort (N t : Nat) (g : Int → Int) (flag left : Bool) : List Lifted :=
  ((liftedPaths N g t).filter (fun w => (w.cell.site == (trailing N t false).site) == flag)).map
    (fun w => ⟨advance N w.cell left, w.sheet + g w.cell.site⟩)

theorem lifted_after_free_step (N n : Nat) (size : 6 ≤ N) (g : Int → Int) (flag left : Bool) :
    let t := n*N+1
    let site := if flag then (trailing N t false).site else (leading N t).site
    let outputSheet := load N g t + g site
    (∀ w ∈ liftedPort N t g flag left, w.sheet = outputSheet) ∧
    signedSum ((liftedPort N t g flag left).map Lifted.cell) =
      if flag then (if left then (n:Int)-1 else n+1) else 1 := by
  have separated := (distinct_lags N size (((n*N+1:Nat):Int))).1
  simp only [Int.natCast_add, Int.natCast_mul, Int.natCast_one] at separated
  cases flag <;> cases left <;>
    simp [liftedPort, signedSum, lifted_stopping_histogram N n size g, leading, trailing,
          advance, separated, List.filter_cons, List.filter_replicate, List.map_replicate,
          signed_replicates, Function.comp_def, List.forall_mem_replicate] <;> omega

end CorridorCounts
