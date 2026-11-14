import Std

namespace RemoteSplitWeights

/-! Lean 4.19.0; standard library only. All ratios below are represented by
integer numerators and positive common denominators. Thus the identities
also give exact rational comparisons without constructing a fraction type.
Real-power monotonicity and the integral over a hidden distribution are
separate mathematical steps.

The column odds t are a/b; the remote multiplier d is r/s; and the
inner-well factor u is m/n. These ratios may each be scaled independently.
The five well rows, in common integer units, are
  (a*n,0), (a*m,b*n), (a*n,b*n), (a*n,b*m), (0,b*n).
The two column sums are a*(m+3*n) and b*(m+3*n). The baseline uses
multipliers (s,s) on the two columns, and the split uses (r,s). -/

private theorem four_times (x : Int) : 4*x = x+x+x+x := by omega

private theorem normalizers_pos (a b r s m n : Int)
    (ha : 0 < a) (hb : 0 < b) (hr : 0 < r) (hs : 0 < s)
    (hm : 0 < m) (hn : 0 < n) :
    0 < (m+3*n)*(a*r+b*s) ∧ 0 < (m+3*n)*(a+b) := by
  have hp : 0 < m+3*n := by omega
  have har := Int.mul_pos ha hr
  have hbs := Int.mul_pos hb hs
  exact ⟨Int.mul_pos hp (by omega), Int.mul_pos hp (by omega)⟩

theorem column_totals (a b m n : Int) :
    a*n + a*m + a*n + a*n + 0 = a*(m+3*n) ∧
    0 + b*n + b*n + b*m + b*n = b*(m+3*n) := by
  have h (v : Int) : 3*v=v+v+v := by omega
  rw [h n]
  simp only [Int.mul_add]
  omega

/-- This numerator for the normalized split-minus-baseline change in a
row with baseline weights (x,y) has positive scalar denominator
(m+3*n)*(a*r+b*s)*(a+b). -/
def rowChange (a b r s x y : Int) : Int :=
  (r*x+s*y)*(a+b) - (x+y)*(a*r+b*s)

theorem row_change_factor (a b r s x y : Int) :
    rowChange a b r s x y = (r-s)*(b*x-a*y) := by
  simp only [rowChange, Int.add_mul, Int.mul_add, Int.sub_mul, Int.mul_sub,
    Int.mul_assoc, Int.mul_comm, Int.mul_left_comm]
  omega

def wellScore (a b r s m n : Int) : Int :=
  4*rowChange a b r s (a*n) 0 - rowChange a b r s (a*m) (b*n)

/-- The signed combination 4 Δ(left) − Δ(inner), on the common positive
denominator, is a*b*(r−s)*(5*n−m). -/
theorem native_score_identity (a b r s m n : Int) :
    wellScore a b r s m n = a*b*(r-s)*(5*n-m) := by
  have five (v : Int) : 5*v=v+v+v+v+v := by omega
  rw [wellScore, row_change_factor, row_change_factor, four_times, five]
  simp only [Int.mul_add, Int.mul_sub, Int.sub_mul, Int.mul_zero, Int.sub_zero,
    Int.mul_assoc, Int.mul_comm, Int.mul_left_comm]
  omega

/-- Positive for lower powered inner factor and larger first-column
multiplier, or for higher inner factor and smaller multiplier. -/
theorem native_strict (a b r s m n : Int) (ha : 0 < a) (hb : 0 < b)
    (hr : 0 < r) (hs : 0 < s) (hm : 0 < m) (hn : 0 < n)
    (h : (s < r ∧ m < 5*n) ∨ (r < s ∧ 5*n < m)) :
    0 < (m+3*n)*(a*r+b*s) ∧ 0 < (m+3*n)*(a+b) ∧
      0 < wellScore a b r s m n := by
  obtain ⟨hd1,hd2⟩ := normalizers_pos a b r s m n ha hb hr hs hm hn
  refine ⟨hd1,hd2,?_⟩
  rw [native_score_identity, Int.mul_assoc (a*b)]
  apply Int.mul_pos (Int.mul_pos ha hb)
  rcases h with ⟨h1,h2⟩ | ⟨h1,h2⟩
  · exact Int.mul_pos (by omega) (by omega)
  · exact Int.mul_pos_of_neg_of_neg (by omega) (by omega)

theorem native_zero_iff (a b r s m n : Int) (ha : 0 < a) (hb : 0 < b) :
    wellScore a b r s m n = 0 ↔ r = s ∨ m = 5*n := by
  rw [native_score_identity]
  simp only [Int.mul_eq_zero]
  omega

/-! Two balanced prefix trees on a different remote rail have leaf
probabilities (1/2,1/8,1/8,1/8,1/8) and (1/4,1/4,1/4,1/4,0).
For t=2^q=u/v, removal of the common 8^(−q) factor gives u²+4v²
and 4uv. The fifth zero stays dark. An arbitrary positive branch weight w
and any common positive reference mass b are allowed in the comparison. -/

def treeP (u v : Int) := u*u+4*v*v
def treeQ (u v : Int) := 4*u*v

theorem tree_square (u v : Int) : treeP u v-treeQ u v=(u-2*v)*(u-2*v) := by
  have h4 (a b : Int) : 4*a*b=a*b+a*b+a*b+a*b := by rw [Int.mul_assoc]; omega
  have h2 (a : Int) : 2*a=a+a := by omega
  rw [treeP, treeQ, h4 v v, h4 u v, h2 v]
  simp only [Int.sub_mul, Int.mul_sub, Int.add_mul, Int.mul_add, Int.mul_comm]
  omega

def treeGap (w b u v : Int) : Int :=
  (w*treeP u v)*(w*treeQ u v+b) - (w*treeQ u v)*(w*treeP u v+b)

theorem tree_gap_factor (w b u v : Int) :
    treeGap w b u v=w*b*((u-2*v)*(u-2*v)) := by
  rw [← tree_square]
  simp only [treeGap, Int.mul_add, Int.add_mul, Int.mul_sub, Int.mul_assoc, Int.mul_comm, Int.mul_left_comm]
  omega

theorem tree_nonnegative_and_equality (w b u v : Int) (hw : 0 < w) (hb : 0 < b) :
    0 ≤ treeGap w b u v ∧ (treeGap w b u v = 0 ↔ u = 2*v) := by
  rw [tree_gap_factor]
  constructor
  · apply Int.mul_nonneg (Int.le_of_lt (Int.mul_pos hw hb))
    by_cases h : 0 ≤ u-2*v
    · exact Int.mul_nonneg h h
    · exact Int.mul_nonneg_of_nonpos_of_nonpos (by omega) (by omega)
  · simp only [Int.mul_eq_zero]
    omega

end RemoteSplitWeights
