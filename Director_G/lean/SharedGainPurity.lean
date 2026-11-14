import Std

/-! The two normalized fiber equalities reduce both marginal variance
tests to the same center. All lists below are finite; zero-weight labels
are allowed. No class-indicator record or product-factorization test on
an indicator is a premise. -/
namespace SharedGainPurity

def total {α K : Type} [Add K] [Zero K] (f : α → K) : List α → K
  | [] => 0
  | a :: rest => f a + total f rest

def deviation {K : Type} [Sub K] [Mul K] (w r c : K) := w*((r-c)*(r-c))

/-- Nonnegative terms cannot cancel. IsZeroHead/IsZeroTail encode just
this fact for the chosen list summands. ZeroAt is strict definiteness of
the squared deviation at a supported label. These properties apply to
nonnegative real weights and are proved concretely for integers below. -/
theorem supported_center {α K : Type} [Zero K] [Add K] [Sub K] [Mul K]
    (labels : List α) (w r : α → K) (c : K)
    (isZeroHead : ∀ i xs, deviation (w i) (r i) c +
       total (fun j => deviation (w j) (r j) c) xs = 0 → deviation (w i) (r i) c = 0)
    (isZeroTail : ∀ i xs, deviation (w i) (r i) c +
       total (fun j => deviation (w j) (r j) c) xs = 0 →
       total (fun j => deviation (w j) (r j) c) xs = 0)
    (zeroAt : ∀ i, w i ≠ 0 → deviation (w i) (r i) c = 0 → r i = c)
    (sum_zero : total (fun i => deviation (w i) (r i) c) labels = 0) :
    ∀ i ∈ labels, w i ≠ 0 → r i = c := by
  induction labels with
  | nil => simp
  | cons x xs ih =>
    intro i h hw
    rcases List.mem_cons.mp h with eq | mem
    · subst i; exact zeroAt x hw (isZeroHead _ _ sum_zero)
    · exact ih (isZeroTail _ _ sum_zero) i mem hw

/-- Availability of a common center plus injectivity of the folded response
makes *all* positive labels of both margins the same. -/
theorem same_label {α K : Type} [Zero K] (r wA wB : α → K)
    (labels : List α) (c : K)
    (injective : ∀ i j, r i = r j → i = j)
    (left : ∀ i ∈ labels, wA i ≠ 0 → r i = c)
    (right : ∀ i ∈ labels, wB i ≠ 0 → r i = c)
    (i j : α) (hi : i ∈ labels) (hj : j ∈ labels)
    (wi : wA i ≠ 0) (wj : wB j ≠ 0) : i = j :=
  injective i j ((left i hi wi).trans (right j hj wj).symm)

/-- Normalized second-moment rows. No positivity or division is required
for this reduction: the second moments equal the product of the two means. -/
theorem two_fiber_centers {K : Type} [Mul K] (mA mB nA nB : K)
    (first : mA=mB) (secondA : nA=mA*mB) (secondB : nB=mA*mB) :
    nA=mA*mA ∧ nB=mA*mA ∧ mB=mA := by
  subst mB; exact ⟨secondA,secondB,rfl⟩

def mass {α : Type} (w : α → Nat) (xs : List α) : Int :=
  total (fun i => (w i : Int)) xs
def first {α : Type} (w : α → Nat) (r : α → Int) (xs : List α) :=
  total (fun i => (w i : Int)*r i) xs
def second {α : Type} (w : α → Nat) (r : α → Int) (xs : List α) :=
  total (fun i => (w i : Int)*(r i*r i)) xs

theorem square_expansion (w r c : Int) :
    deviation w r c = w*(r*r) - w*r*c - w*r*c + w*(c*c) := by
  simp [deviation, Int.sub_mul, Int.mul_sub, Int.mul_assoc, Int.mul_left_comm, Int.mul_comm]
  omega

/-- Exact finite variance expansion, without dividing by the total mass. -/
theorem variance_expansion {α : Type} (w : α → Nat) (r : α → Int) (c : Int)
    (xs : List α) :
    total (fun i => deviation (w i : Int) (r i) c) xs =
    second w r xs - first w r xs*c - first w r xs*c + mass w xs*(c*c) := by
  induction xs with
  | nil => simp [total,second,first,mass]
  | cons i xs ih =>
    simp only [total,second,first,mass,Int.add_mul] at ih ⊢
    rw [ih, square_expansion]
    omega

private theorem dev_nonneg (w : Nat) (r c : Int) : 0 ≤ deviation (w : Int) r c := by
  apply Int.mul_nonneg (by omega)
  by_cases h : 0 ≤ r-c
  · exact Int.mul_nonneg h h
  · exact Int.mul_nonneg_of_nonpos_of_nonpos (by omega) (by omega)

private theorem total_dev_nonneg {α : Type} (w : α → Nat) (r : α → Int)
    (c : Int) (xs : List α) : 0 ≤ total (fun i => deviation (w i : Int) (r i) c) xs := by
  induction xs with
  | nil => simp [total]
  | cons i xs ih => exact Int.add_nonneg (dev_nonneg _ _ _) ih

/-- On a common integer scale for responses and weights, a rational
center can always be made integral by increasing the response scale.
The raw first and second moments at a common center imply the full
positive-support conclusion; the moments are the only record premises. -/
theorem moments_force_center {α : Type} (w : α → Nat) (r : α → Int) (c : Int)
    (xs : List α) (mean : first w r xs = mass w xs*c)
    (moment : second w r xs = mass w xs*(c*c)) :
    ∀ i ∈ xs, (w i:Int) ≠ 0 → r i = c := by
  apply supported_center xs (fun i => (w i:Int)) r c
  · intro i rest h
    have a := dev_nonneg (w i) (r i) c
    have b := total_dev_nonneg w r c rest
    omega
  · intro i rest h
    have a := dev_nonneg (w i) (r i) c
    have b := total_dev_nonneg w r c rest
    omega
  · intro i hw hz
    unfold deviation at hz
    have z := (Int.mul_eq_zero.mp hz).resolve_left hw
    rcases Int.mul_eq_zero.mp z with h | h <;> omega
  · rw [variance_expansion, mean, moment, Int.mul_assoc]
    omega

/-- Common-center purity for both distributions from their two true
moment equations, even when their weights and total masses differ. -/
theorem two_margin_purity {α : Type} (wA wB : α → Nat) (r : α → Int)
    (xs : List α) (c : Int) (inj : ∀ i j, r i = r j → i = j)
    (mA : first wA r xs = mass wA xs*c)
    (nA : second wA r xs = mass wA xs*(c*c))
    (mB : first wB r xs = mass wB xs*c)
    (nB : second wB r xs = mass wB xs*(c*c))
    (i j : α) (hi : i ∈ xs) (hj : j ∈ xs)
    (wi : (wA i:Int)≠0) (wj : (wB j:Int)≠0) : i=j :=
  same_label r (fun k => (wA k:Int)) (fun k => (wB k:Int)) xs c inj
    (moments_force_center _ _ _ _ mA nA) (moments_force_center _ _ _ _ mB nB)
    i j hi hj wi wj

/-- Cross-distance argument for a *single* matched fiber. Here vA,vB
are the (nonnegative) variances of the two normalized margins; the
fiber says both raw second moments equal the product of the means.
Writing normalized moments on a common rational scale gives integers
with these equations after multiplying variances by the squared scale. -/
theorem one_fiber_common_center (a b vA vB : Int)
    (varA : vA = a*b-a*a) (varB : vB = a*b-b*b)
    (positiveA : 0 ≤ vA) (positiveB : 0 ≤ vB) :
    a=b ∧ vA=0 ∧ vB=0 := by
  have sq := square_expansion 1 a b
  simp only [deviation, Int.one_mul, Int.mul_comm b a] at sq
  have nonneg := dev_nonneg 1 a b
  simp only [deviation, Int.ofNat_one, Int.one_mul] at nonneg
  have z : (a-b)*(a-b) = 0 := by omega
  rcases Int.mul_eq_zero.mp z with h | h <;> have eq : a=b := by omega
  all_goals subst b; simp_all

/-- Nonnegativity used by the single-fiber argument comes from an actual
finite weighted sum. This is the mass-scaled variance around its mean. -/
theorem raw_variance_nonneg {α : Type} (w : α → Nat) (r : α → Int) (xs : List α)
    (c n : Int) (mean : first w r xs = mass w xs*c)
    (moment : second w r xs = mass w xs*n) (positive : 0 < mass w xs) :
    0 ≤ n-c*c := by
  have ex := variance_expansion w r c xs
  rw [mean, moment, Int.mul_assoc] at ex
  have lo := total_dev_nonneg w r c xs
  have prod : 0 ≤ mass w xs*(n-c*c) := by rw [Int.mul_sub]; omega
  by_cases good : 0 ≤ n-c*c
  · exact good
  have neg := Int.mul_neg_of_pos_of_neg positive (show n-c*c<0 by omega)
  omega

/-- The equal shared histograms (BB,HH), (HH,BB), (BH,BH) alone give
both second moments equal to a*b. No first-fiber mean equality is needed. -/
theorem one_fiber_purity {α : Type} (wA wB : α → Nat) (r : α → Int)
    (xs : List α) (a b : Int) (inj : ∀ i j, r i = r j → i = j)
    (positiveA : 0 < mass wA xs) (positiveB : 0 < mass wB xs)
    (mA : first wA r xs = mass wA xs*a)
    (mB : first wB r xs = mass wB xs*b)
    (nA : second wA r xs = mass wA xs*(a*b))
    (nB : second wB r xs = mass wB xs*(a*b))
    (i j : α) (hi : i ∈ xs) (hj : j ∈ xs)
    (wi : (wA i:Int)≠0) (wj : (wB j:Int)≠0) : i=j := by
  have loA := raw_variance_nonneg wA r xs a (a*b) mA nA positiveA
  have loB := raw_variance_nonneg wB r xs b (a*b) mB nB positiveB
  obtain ⟨eq,_,_⟩ := one_fiber_common_center a b _ _ rfl rfl loA loB
  subst b
  exact two_margin_purity wA wB r xs a inj mA nA mB nB i j hi hj wi wj

end SharedGainPurity
