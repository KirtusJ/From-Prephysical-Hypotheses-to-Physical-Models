import Std

/-! On the integer covering line a walker can move at most one site per
clock. All gains are evaluated on departures, including the launch site
and excluding the site reached on the last tick. -/
namespace FilterPhaseWidth

def movesLocally (x : Nat → Int) : Prop :=
  ∀ j, x j-1 ≤ x (j+1) ∧ x (j+1) ≤ x j+1

theorem cone (x : Nat → Int) (localMove : movesLocally x) (j : Nat) :
    x 0-(j:Int) ≤ x j ∧ x j ≤ x 0+(j:Int) := by
  induction j with
  | zero => simp
  | succ j ih =>
    have step := localMove j
    omega

def gain (x : Nat → Int) : Nat → Int
  | 0 => 0
  | n+1 => gain x n + x n/2

def width : Nat → Nat
  | 0 => 0
  | n+1 => width n+n

/-- Width of the common departure interval is exactly j for integer
floor division, even for odd launches and across zero. -/
theorem departure_width (home : Int) (j : Nat) :
    (home+(j:Int))/2 - (home-(j:Int))/2 = j := by omega

theorem gain_interval (x : Nat → Int) (localMove : movesLocally x) (t : Nat) :
    gain (fun j => x 0-(j:Int)) t ≤ gain x t ∧
    gain x t ≤ gain (fun j => x 0+(j:Int)) t := by
  induction t with
  | zero => simp [gain]
  | succ j ih =>
    have contain := cone x localMove j
    simp only [gain]
    omega

theorem interval_width (home : Int) (t : Nat) :
    gain (fun j => home+(j:Int)) t - gain (fun j => home-(j:Int)) t = width t := by
  induction t with
  | zero => simp [gain,width]
  | succ j ih =>
    have span := departure_width home j
    simp only [gain,width,Int.natCast_add]
    omega

theorem pair_bound (x y : Nat → Int) (lx : movesLocally x) (ly : movesLocally y)
    (same : x 0=y 0) (t : Nat) : gain x t-gain y t ≤ width t := by
  obtain ⟨_,hx⟩ := gain_interval x lx t
  obtain ⟨hy,_⟩ := gain_interval y ly t
  rw [←same] at hy
  have span := interval_width (x 0) t
  omega

theorem twice_width (t : Nat) : 2*width t=t*(t-1) := by
  induction t with
  | zero => rfl
  | succ t ih =>
    cases t with
    | zero => rfl
    | succ j =>
      simp only [width, Nat.mul_add, Nat.add_one_sub_one] at *
      simp only [Nat.succ_eq_add_one, Nat.add_mul, Nat.mul_add, Nat.one_mul, Nat.mul_one] at *
      omega

end FilterPhaseWidth
