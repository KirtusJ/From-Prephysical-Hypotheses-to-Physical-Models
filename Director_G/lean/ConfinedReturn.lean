import Std

/-!
# Exact signed area of an always-moving, radius-confined return

Positions are integer offsets from the launch site. A tick consumes its
departure position and then moves by +1 or -1. The radius is a bound at every
physical vertex. A field setting can independently change sign at every tick.
-/
namespace ConfinedReturn

def unit (c : Int) := c = 1 ∨ c = -1

def moves (p : Nat → Int) (ticks : Nat) :=
  ∀ t, t < ticks → p (t+1) = p t + 1 ∨ p (t+1) = p t - 1

def sumAt (v : Nat → Int) (off : Nat) : Nat → Int
  | 0 => 0
  | n+1 => sumAt v off n + v (off+n)

theorem sum_append (v : Nat → Int) (off m n : Nat) :
    sumAt v off (m+n) = sumAt v off m + sumAt v (off+m) n := by
  induction n with
  | zero => simp [sumAt]
  | succ n ih => simp [sumAt,ih,Nat.add_assoc,Int.add_assoc]

theorem reach (p : Nat → Int) (ticks : Nat) (walk : moves p ticks)
    (i n : Nat) (inside : i+n ≤ ticks) :
    p i - (n:Int) ≤ p (i+n) ∧ p (i+n) ≤ p i + (n:Int) := by
  induction n with
  | zero => simp
  | succ n ih =>
    have prev := ih (by omega)
    have edge := walk (i+n) (by omega)
    rw [show i+(n+1)=i+n+1 by omega,Int.natCast_succ]
    omega

theorem endpoint_bounds (p : Nat → Int) (ticks : Nat) (walk : moves p ticks)
    (start : p 0 = 0) (stop : p ticks = 0) (t : Nat) (inside : t ≤ ticks) :
    -(t:Int) ≤ p t ∧ p t ≤ (t:Int) ∧
    -((ticks-t:Nat):Int) ≤ p t ∧ p t ≤ ((ticks-t:Nat):Int) := by
  have left := reach p ticks walk 0 t (by omega)
  have right := reach p ticks walk t (ticks-t) (by omega)
  rw [Nat.zero_add,start] at left
  rw [show t+(ticks-t)=ticks by omega,stop] at right
  omega

theorem clip_radius (p : Nat → Int) (a r : Nat) (walk : moves p (2*a))
    (start : p 0 = 0) (stop : p (2*a) = 0)
    (confined : ∀ t, t ≤ 2*a → -(r:Int) ≤ p t ∧ p t ≤ (r:Int))
    (t : Nat) (inside : t ≤ 2*a) :
    -((min r a:Nat):Int) ≤ p t ∧ p t ≤ ((min r a:Nat):Int) := by
  have h := endpoint_bounds p (2*a) walk start stop t inside
  have c := confined t inside
  simp only [Nat.min_def]
  split <;> omega

theorem weighted_le (c x b : Int) (sign : unit c) (box : -b ≤ x ∧ x ≤ b) :
    c*x ≤ b := by
  rcases sign with h | h <;> rw [h] <;> simp <;> omega

/-- Two adjacent samples cannot both have maximum absolute radius. -/
theorem pair_le (s x y u v : Int) (hx : -s ≤ x ∧ x ≤ s)
    (hy : -s ≤ y ∧ y ≤ s) (edge : y=x+1 ∨ y=x-1)
    (hu : unit u) (hv : unit v) : u*x + v*y ≤ 2*s-1 := by
  rcases hu with h | h <;> rw [h] <;>
    rcases hv with g | g <;> rw [g] <;> simp <;> omega

theorem ends_le (v : Nat → Int) (s : Int) (off k : Nat)
    (bound : ∀ j, j < k → v j + v (off+j) ≤ s) :
    sumAt v 0 k + sumAt v off k ≤ (k:Int)*s := by
  induction k with
  | zero => simp [sumAt]
  | succ k ih =>
    have prev := ih (fun j hj => bound j (by omega))
    have last := bound k (by omega)
    simp only [sumAt,Nat.zero_add,Int.natCast_succ,Int.add_mul,Int.one_mul]
    omega

theorem middle_le (v : Nat → Int) (off k : Nat) (b : Int)
    (bound : ∀ j, j < k → v (off+2*j) + v (off+2*j+1) ≤ b) :
    sumAt v off (2*k) ≤ (k:Int)*b := by
  induction k with
  | zero => simp [sumAt]
  | succ k ih =>
    have prev := ih (fun j hj => bound j (by omega))
    have last := bound k (by omega)
    rw [show 2*(k+1) = 2*k+1+1 by omega]
    simp only [sumAt,Int.natCast_succ,Int.add_mul,Int.one_mul]
    rw [← Nat.add_assoc off (2*k) 1]
    omega

def cap (s h : Nat) : Int := (s:Int)*s + (h:Int)*(2*(s:Int)-1)

theorem signed_upper (p w : Nat → Int) (s h : Nat)
    (walk : moves p (s+2*h+s)) (start : p 0=0) (stop : p (s+2*h+s)=0)
    (box : ∀ t, t ≤ s+2*h+s → -(s:Int) ≤ p t ∧ p t ≤ (s:Int))
    (sign : ∀ t, t < s+2*h+s → unit (w t)) :
    sumAt (fun t => w t*p t) 0 (s+2*h+s) ≤ cap s h := by
  let v := fun t => w t*p t
  have ends := ends_le v s (s+2*h) s (by
    intro j hj
    have left := endpoint_bounds p _ walk start stop j (by omega)
    have right := endpoint_bounds p _ walk start stop (s+2*h+j) (by omega)
    have u := weighted_le _ _ _ (sign j (by omega)) ⟨left.1,left.2.1⟩
    have z := weighted_le _ _ _ (sign (s+2*h+j) (by omega)) right.2.2
    dsimp [v]
    omega)
  have mid := middle_le v s h (2*(s:Int)-1) (by
    intro j hj
    exact pair_le _ _ _ _ _ (box _ (by omega)) (box _ (by omega))
      (walk (s+2*j) (by omega)) (sign _ (by omega)) (sign _ (by omega)))
  change sumAt v 0 (s+2*h+s) ≤ _
  rw [sum_append v 0 (s+2*h) s,sum_append v 0 s (2*h)]
  simp only [Nat.zero_add,cap]
  omega

/-- Saturating positive walk. The central samples are s,s−1,s,s−1,... -/
def lobe (s h t : Nat) : Int :=
  if t < s then (t:Int)
  else if t < s+2*h then if (t-s)%2 = 0 then (s:Int) else (s:Int)-1
  else ((s+2*h+s-t:Nat):Int)

theorem lobe_moves (s h : Nat) (positive : 0 < s) : moves (lobe s h) (s+2*h+s) := by
  intro t ht
  unfold lobe
  repeat' split
  all_goals omega

theorem lobe_box (s h : Nat) (positive : 0 < s) (t : Nat) (ht : t ≤ s+2*h+s) :
    0 ≤ lobe s h t ∧ lobe s h t ≤ (s:Int) := by
  unfold lobe
  repeat' split
  all_goals omega

theorem lobe_ends (s h : Nat) (positive : 0 < s) :
    lobe s h 0 = 0 ∧ lobe s h (s+2*h+s)=0 := by
  simp [lobe,positive]
  omega

theorem sum_neg (v : Nat → Int) (off k : Nat) :
    sumAt (fun t => -(v t)) off k = -(sumAt v off k) := by
  induction k with
  | zero => simp [sumAt]
  | succ k ih => simp only [sumAt,ih]; omega

theorem signed_bounds (p w : Nat → Int) (a r : Nat)
    (walk : moves p (2*a)) (start : p 0=0) (stop : p (2*a)=0)
    (box : ∀ t, t ≤ 2*a → -(r:Int) ≤ p t ∧ p t ≤ (r:Int))
    (sign : ∀ t, t < 2*a → unit (w t)) :
    let s := min r a;
    let b := cap s (a-s);
    -b ≤ sumAt (fun t => w t*p t) 0 (2*a) ∧
         sumAt (fun t => w t*p t) 0 (2*a) ≤ b := by
  let s := min r a
  let h := a-s
  have length : s+2*h+s = 2*a := by dsimp [s,h]; omega
  have clipped (t : Nat) (ht : t ≤ 2*a) := clip_radius p a r walk start stop box t ht
  have mag (u : Nat → Int) (hu : ∀ t, t < 2*a → unit (u t)) :=
    signed_upper p u s h (length ▸ walk) start (length ▸ stop)
      (length ▸ clipped) (length ▸ hu)
  have up := mag w sign
  have down := mag (fun t => -(w t)) (by
    intro t ht
    specialize sign t ht
    change -w t = 1 ∨ -w t = -1
    unfold unit at sign
    omega)
  rw [length] at up down
  simp only [Int.neg_mul,sum_neg] at down
  change -(cap s h) ≤ _ ∧ _ ≤ cap s h
  exact ⟨by omega,up⟩

theorem lobe_area (s h : Nat) :
    sumAt (lobe s h) 0 (s+2*h+s) = cap s h := by
  let v := lobe s h
  have ep (j : Nat) (hj : j < s) : v j + v (s+2*h+j) = (s:Int) := by
    dsimp [v,lobe]
    repeat' split
    all_goals omega
  have mp (j : Nat) (hj : j < h) : v (s+2*j) + v (s+2*j+1) = 2*(s:Int)-1 := by
    dsimp [v,lobe]
    repeat' split
    all_goals omega
  have e1 := ends_le v (s:Int) (s+2*h) s (fun j hj => by rw [ep j hj]; omega)
  have e2 := ends_le (fun t => -(v t)) (-(s:Int)) (s+2*h) s
    (fun j hj => by dsimp only; have := ep j hj; omega)
  have m1 := middle_le v s h (2*(s:Int)-1) (fun j hj => by rw [mp j hj]; omega)
  have m2 := middle_le (fun t => -(v t)) s h (-(2*(s:Int)-1))
    (fun j hj => by dsimp only; have := mp j hj; omega)
  simp only [sum_neg,Int.mul_neg] at e2 m2
  change sumAt v 0 (s+2*h+s) = _
  rw [sum_append v 0 (s+2*h) s,sum_append v 0 s (2*h)]
  simp only [Nat.zero_add,cap]
  omega

theorem zero_radius_impossible (p : Nat → Int) (ticks : Nat) (positive : 0 < ticks)
    (walk : moves p ticks) (start : p 0=0)
    (confined : ∀ t, t ≤ ticks → 0 ≤ p t ∧ p t ≤ 0) : False := by
  have h := walk 0 positive
  have c := confined 1 (by omega)
  change p 1 = p 0+1 ∨ p 1 = p 0-1 at h
  omega

theorem tick_parity (p : Nat → Int) (ticks : Nat) (walk : moves p ticks)
    (start : p 0=0) (t : Nat) (inside : t ≤ ticks) : p t % 2 = (t:Int) % 2 := by
  induction t with
  | zero => simp [start]
  | succ t ih =>
    have prev := ih (by omega)
    have edge := walk t (by omega)
    rw [Int.natCast_succ]
    omega

theorem return_even (p : Nat → Int) (ticks : Nat) (walk : moves p ticks)
    (start : p 0=0) (stop : p ticks=0) : ticks % 2 = 0 := by
  have h := tick_parity p ticks walk start ticks (by omega)
  rw [stop] at h
  omega

theorem lobe_end_rails (s h : Nat) (positive : 0 < s) :
    lobe s h 1 = 1 ∧ lobe s h (s+2*h+s-1) = 1 := by
  unfold lobe
  repeat' split
  all_goals omega

/-- Both arms pass through the same launch site before entering the mirror
lobe. At that join the same physical direction continues into the second
lobe. A uniform field reversal changes only the gain. -/
def mirrored (p : Nat → Int) (k t : Nat) := if t < k then p t else -(p (t-k))
def reversed (k t : Nat) : Int := if t < k then 1 else -1

theorem mirrored_moves (p : Nat → Int) (k : Nat) (walk : moves p k)
    (start : p 0=0) (stop : p k=0) : moves (mirrored p k) (k+k) := by
  intro t ht
  by_cases h : t+1 < k
  · have ht' : t < k := by omega
    simpa only [mirrored,if_pos h,if_pos ht'] using walk t ht'
  by_cases e : t < k
  · have tk : t+1 = k := by omega
    have z := walk t e
    rw [tk,stop] at z
    simp only [mirrored,if_neg h,if_pos e,tk,Nat.sub_self,start,Int.neg_zero]
    simpa using z
  · have z := walk (t-k) (by omega)
    simp only [mirrored,if_neg e,if_neg h]
    rw [show t+1-k=t-k+1 by omega]
    omega

theorem sum_from_samples (u v : Nat → Int) (i j n : Nat)
    (same : ∀ t, t<n → u (i+t)=v (j+t)) : sumAt u i n = sumAt v j n := by
  induction n with
  | zero => rfl
  | succ n ih =>
    simp only [sumAt, ih (fun t ht => same t (by omega)),same n (by omega)]

theorem shifted_sum (x : Int) (p : Nat → Int) (k : Nat) :
    sumAt (fun t => x+p t) 0 k = (k:Int)*x + sumAt p 0 k := by
  induction k with
  | zero => simp [sumAt]
  | succ k ih =>
    simp only [sumAt,ih,Int.natCast_succ,Int.add_mul,Int.one_mul]
    omega

theorem zero_kick (p : Nat → Int) (k : Nat) (x : Int) :
    sumAt (fun t => reversed k t * (x+mirrored p k t)) 0 (k+k) =
    2*sumAt p 0 k := by
  let u := fun t => reversed k t * (x+mirrored p k t)
  have first := sum_from_samples u (fun t => x+p t) 0 0 k (by
    intro t ht
    simp [u,reversed,mirrored,ht])
  have second := sum_from_samples u (fun t => -x+p t) k 0 k (by
    intro t ht
    have hh : ¬k+t<k := by omega
    simp [u,reversed,mirrored,hh,show k+t-k=t by omega]
    omega)
  change sumAt u 0 (k+k) = _
  rw [sum_append u 0 k k,Nat.zero_add,first,second,shifted_sum,shifted_sum,
    Int.mul_neg]
  omega

theorem saturated_pulse (s h : Nat) (x : Int) :
    let k := s+2*h+s
    sumAt (fun t => reversed k t * (x+mirrored (lobe s h) k t)) 0 (k+k) =
    2*cap s h := by
  simp only [zero_kick,lobe_area]

theorem join_rail (s h : Nat) (positive : 0<s) :
    let k := s+2*h+s
    let path := mirrored (lobe s h) k
    path (k-1) = 1 ∧ path k = 0 ∧ path (k+1) = -1 := by
  have e := lobe_end_rails s h positive
  have z := lobe_ends s h positive
  have pos : 0 < s+2*h+s := by omega
  simp only [mirrored,if_pos (show s+2*h+s-1 < s+2*h+s by omega),
    if_neg (show ¬s+2*h+s < s+2*h+s by omega),Nat.sub_self,z.1,Int.neg_zero,
    if_neg (show ¬s+2*h+s+1 < s+2*h+s by omega),
    show s+2*h+s+1-(s+2*h+s)=1 by omega,e.1,e.2,and_self]

end ConfinedReturn
