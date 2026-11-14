import Std

/-! A character label is represented by the smaller unsigned representative
of its conjugate pair. Orders start at three; different covers may choose
different conjugations. Only a divisibility-cofinal family is bounded. -/
namespace SheetRefinement

def fold (m k : Nat) := min (k%m) (m-k%m)

/-- Raw unsigned congruence up to sign, using natural arithmetic. -/
def signedAgreement (m a b : Nat) : Prop := b%m=a%m ∨ m ∣ a+b

/-- For a folded a, the two possible congruences both give a=fold(m,b).
This includes a=0 and an even-order half turn. -/
theorem fold_of_agreement {m a b : Nat} (pos : 0<m) (half : 2*a≤m)
    (h : signedAgreement m a b) : fold m b = a := by
  have am : a<m := by omega
  have bm := Nat.mod_lt b pos
  rcases h with equal | opposite
  · rw [Nat.mod_eq_of_lt am] at equal
    simp [fold,equal,Nat.min_eq_left (show a≤m-a by omega)]
  · have zero := Nat.mod_eq_zero_of_dvd opposite
    rw [Nat.add_mod, Nat.mod_eq_of_lt am] at zero
    by_cases small : a+b%m<m
    · rw [Nat.mod_eq_of_lt small] at zero
      have az : a=0 := by omega
      have bz : b%m=0 := by omega
      simp [fold,az,bz]
    · have sum_dvd : m ∣ a+b%m := Nat.dvd_iff_mod_eq_zero.mpr zero
      have le : a+b%m<2*m := by omega
      obtain ⟨q,hq⟩ := sum_dvd
      have qone : q=1 := by
        by_cases q0 : q=0
        · simp [q0] at hq; omega
        by_cases q2 : 2≤q
        · have more := Nat.mul_le_mul_left m q2
          omega
        · omega
      rw [qone, Nat.mul_one] at hq
      have eq : m-b%m=a := by omega
      have lo : a≤b%m := by omega
      simp [fold,eq,Nat.min_eq_right lo]

/-- For period m≥2B, two labels in [0,B] cannot alias at the fold.
At equality, the only possible nonzero minus alias is a=b=B. -/
theorem bounded_lock {m a b B : Nat} (positive : 0<m) (large : 2*B≤m)
    (left : a≤B) (right : b≤B) (agree : signedAgreement m a b) : a=b := by
  have val := fold_of_agreement positive (show 2*a≤m by omega) agree
  rw [fold,Nat.mod_eq_of_lt (show b<m by omega),
      Nat.min_eq_left (show b≤m-b by omega)] at val
  exact val.symm

def Compatible (d : Nat → Nat) : Prop :=
  ∀ m n, 3≤m → m∣n → 0<n → signedAgreement m (d m) (d n)

/-- For every prescribed order q≥3 there is a positive multiple with the
uniform bound. It is unnecessary to choose orientations for the covers. -/
def CofinalBound (d : Nat → Nat) (B : Nat) : Prop :=
  ∀ q, 3≤q → ∃ n, 0<n ∧ q∣n ∧ d n≤B

theorem cofinal_lock (d : Nat → Nat) (B : Nat)
    (folded : ∀ m, 3≤m → 2*d m≤m) (cover : Compatible d)
    (bounded : CofinalBound d B) :
    ∃ k, k≤B ∧ ∀ m, 3≤m → d m=fold m k := by
  obtain ⟨a,pa,diva,wa⟩ := bounded (2*B+3) (by omega)
  have large := Nat.le_of_dvd pa diva
  refine ⟨d a, wa, ?_⟩
  intro m hm
  have product := Nat.le_mul_of_pos_right a (show 0<m by omega)
  obtain ⟨n,pn,dn,wn⟩ := bounded (a*m) (by omega)
  have da : a∣n := Nat.dvd_trans (Nat.dvd_mul_right a m) dn
  have dm : m∣n := Nat.dvd_trans (Nat.dvd_mul_left m a) dn
  have same := bounded_lock pa (show 2*B≤a by omega) wa wn (cover a n (by omega) da pn)
  have localEq := fold_of_agreement (show 0<m by omega) (folded m hm) (cover m n hm dm pn)
  rw [← same] at localEq
  exact localEq.symm

/-- Faithfulness on all orders means gcd(d_m,m)=1. An ordinary k≥1 is
tested at order 3k, which makes its fold k and its gcd k. The k=0
case is excluded already by order three. -/
theorem faithful_one (d : Nat → Nat) (k : Nat)
    (ordinary : ∀ m, 3≤m → d m=fold m k)
    (faithful : ∀ m, 3≤m → (d m).gcd m=1) : k=1 := by
  by_cases zero : k=0
  · subst k
    have test := faithful 3 (by decide)
    rw [ordinary 3 (by decide)] at test
    change 3=1 at test
    omega
  · have pos : 3≤3*k := by omega
    have test := faithful (3*k) pos
    rw [ordinary _ pos,fold,Nat.mod_eq_of_lt (show k<3*k by omega),
      Nat.min_eq_left (show k≤3*k-k by omega),
      Nat.gcd_eq_left (Nat.dvd_mul_left k 3)] at test
    exact test

/-- A child on the short quarter of the doubled ring already lies in the
parent's folded interval. The edge shared by both intervals is allowed. -/
theorem double_lock (d : Nat → Nat) (folded : ∀ m, 3≤m → 2*d m≤m)
    (cover : Compatible d) (n : Nat) (hn : 3≤n) (short : 2*d (2*n)≤n) :
    d (2*n)=d n := by
  have h := fold_of_agreement (show 0<n by omega) (folded n hn)
    (cover n (2*n) hn (Nat.dvd_mul_left n 2) (by omega))
  rw [fold,Nat.mod_eq_of_lt (show d (2*n)<n by omega),
    Nat.min_eq_left (show d (2*n)≤n-d (2*n) by omega)] at h
  exact h

def level (m j : Nat) := 2^j*m

private theorem initial_le (m j : Nat) : m≤level m j :=
  Nat.le_mul_of_pos_left m (Nat.pow_pos (by decide))

private theorem clock_lt {m : Nat} (hm : 0<m) (j : Nat) : j<level m j := by
  have h : j<2^j := Nat.lt_two_pow_self
  exact Nat.lt_of_lt_of_le h (Nat.le_mul_of_pos_right _ hm)

private theorem next_level (m j : Nat) : level m (j+1)=2*level m j := by
  simp [level,Nat.pow_succ,Nat.mul_assoc,Nat.mul_comm,Nat.mul_left_comm]

def TailQuarter (d : Nat → Nat) : Prop :=
  ∀ m, 3≤m → ∃ j0, ∀ j, j0≤j → 2*d (2*level m j)≤level m j

private theorem stable_chain (d : Nat → Nat) (folded : ∀ m, 3≤m → 2*d m≤m)
    (cover : Compatible d) (m : Nat) (hm : 3≤m)
    (tail : ∃ j0, ∀ j, j0≤j → 2*d (2*level m j)≤level m j) :
    ∃ start k, ∀ j, start≤j → d (level m j)=k := by
  obtain ⟨s,hs⟩ := tail
  refine ⟨s,d (level m s),?_⟩
  intro j hj
  have iter : ∀ h, d (level m (s+h))=d (level m s) := by
    intro h
    induction h with
    | zero => simp
    | succ h ih =>
      rw [←Nat.add_assoc,next_level,double_lock d folded cover _ (by
        have := initial_le m (s+h); omega) (hs _ (by omega))]
      exact ih
  obtain ⟨h,rfl⟩ := Nat.exists_eq_add_of_le hj
  exact iter h

/-- Choose one common tower for each target, based at A*m. Its stable
value must equal the value in the fixed tower based at A: project to
a late level of the latter exceeding twice both constants. Projecting to
m gives the requested fold. The starts and bounds need not be uniform. -/
private theorem anchored_lock (d : Nat → Nat) (folded : ∀ m, 3≤m → 2*d m≤m)
    (cover : Compatible d) (A : Nat) (hA : 3≤A)
    (stable : ∀ n, 3≤n → A∣n → ∃ s c, ∀ j, s≤j → d (level n j)=c) :
    ∃ k, ∀ m, 3≤m → d m=fold m k := by
  obtain ⟨s,k,anchor⟩ := stable A hA (Nat.dvd_refl _)
  refine ⟨k,?_⟩
  intro m hm
  have large := Nat.le_mul_of_pos_right A (show 0<m by omega)
  obtain ⟨t,c,tower⟩ := stable (A*m) (by omega) (Nat.dvd_mul_right _ _)
  let j := s+t+2*max k c
  have da := anchor j (show s≤j by dsimp [j]; omega)
  have db := tower j (show t≤j by dsimp [j]; omega)
  have ja := clock_lt (m:=A) (by omega) j
  have la := initial_le A j
  have lb := initial_le (A*m) j
  have dvd : level A j ∣ level (A*m) j :=
    Nat.mul_dvd_mul_left (2^j) (Nat.dvd_mul_right A m)
  have agree := cover _ _ (by omega) dvd (by omega)
  rw [da,db] at agree
  have same := bounded_lock (show 0<level A j by omega)
    (show 2*max k c≤level A j by dsimp [j] at ja; dsimp [j]; omega)
    (Nat.le_max_left k c) (Nat.le_max_right k c) agree
  have dm : m ∣ level (A*m) j := Nat.dvd_trans (Nat.dvd_mul_left m A)
    (Nat.dvd_mul_left _ _)
  have localEq := fold_of_agreement (show 0<m by omega) (folded m hm)
    (cover _ _ hm dm (by omega))
  rw [db,←same] at localEq
  exact localEq.symm

theorem quarter_lock (d : Nat → Nat) (folded : ∀ m, 3≤m → 2*d m≤m)
    (cover : Compatible d) (tail : TailQuarter d) :
    ∃ k, ∀ m, 3≤m → d m=fold m k := by
  apply anchored_lock d folded cover 3 (by decide)
  intro m hm _
  exact stable_chain d folded cover m hm (tail m hm)

/-- Stronger eventual window. If both successive normalized positions
are strictly below one third, the reflected lift would have a+b=n,
which contradicts 3a<n and 3b<2n. -/
theorem third_step (d : Nat → Nat) (folded : ∀ m, 3≤m → 2*d m≤m)
    (cover : Compatible d) (n : Nat) (hn : 3≤n)
    (small : 3*d n<n) (next : 3*d (2*n)<2*n) : d (2*n)=d n := by
  have h := fold_of_agreement (show 0<n by omega) (folded n hn)
    (cover n (2*n) hn (Nat.dvd_mul_left n 2) (by omega))
  rw [fold,Nat.mod_eq_of_lt (show d (2*n)<n by omega)] at h
  by_cases short : d (2*n)≤n-d (2*n)
  · rwa [Nat.min_eq_left short] at h
  · rw [Nat.min_eq_right (by omega)] at h
    omega

theorem third_lock (d : Nat → Nat) (folded : ∀ m, 3≤m → 2*d m≤m)
    (cover : Compatible d)
    (third : ∀ m, 3≤m → ∃ start, ∀ j, start≤j → 3*d (level m j)<level m j) :
    ∃ k, ∀ m, 3≤m → d m=fold m k := by
  apply quarter_lock d folded cover
  intro m hm
  obtain ⟨s,hs⟩ := third m hm
  refine ⟨s,?_⟩
  intro j hj
  have parent := hs j hj
  have child := hs (j+1) (by omega)
  rw [next_level] at child
  have floor := initial_le m j
  rw [third_step d folded cover _ (by omega) parent child]
  omega

/-- At the inclusive one-third boundary an isolated tower could repeatedly
take the reflected lift. On orders divisible by 3*z this boundary projects
to zero at z. Choosing any z with d(z) nonzero removes the obstruction. -/
theorem closed_third_lock (d : Nat → Nat) (folded : ∀ m, 3≤m → 2*d m≤m)
    (cover : Compatible d)
    (third : ∀ m, 3≤m → ∃ s, ∀ j, s≤j → 3*d (level m j)≤level m j) :
    ∃ k, ∀ m, 3≤m → d m=fold m k := by
  classical
  by_cases any : ∃ z, 3≤z ∧ d z≠0
  · obtain ⟨z,hz,nonzero⟩ := any
    apply anchored_lock d folded cover (3*z) (by omega)
    intro n hn div
    apply stable_chain d folded cover n hn
    obtain ⟨s,hs⟩ := third n hn
    have strict : ∀ j, s≤j → 3*d (level n j)<level n j := by
      intro j hj
      have le := hs j hj
      by_cases eq : 3*d (level n j)=level n j
      · have divLevel : 3*z ∣ level n j := Nat.dvd_trans div (Nat.dvd_mul_left _ _)
        obtain ⟨q,hq⟩ := divLevel
        have mult : d (level n j)=z*q := by rw [Nat.mul_assoc] at hq; omega
        have dz : z ∣ level n j := Nat.dvd_trans (Nat.dvd_mul_left z 3)
          (Nat.dvd_trans div (Nat.dvd_mul_left _ _))
        have lo := initial_le n j
        have ordinary := fold_of_agreement (show 0<z by omega) (folded z hz)
          (cover _ _ hz dz (by omega))
        simp [fold,mult] at ordinary
        omega
      · omega
    refine ⟨s,?_⟩
    intro j hj
    have lo := initial_le n j
    have p := strict j hj
    have c := strict (j+1) (by omega)
    rw [next_level] at c
    rw [third_step d folded cover _ (by omega) p c]
    omega
  · refine ⟨0,?_⟩
    intro m hm
    have z : d m=0 := by
      by_cases h : d m=0
      · exact h
      · exact False.elim (any ⟨m,hm,h⟩)
    simp [z,fold]

end SheetRefinement
