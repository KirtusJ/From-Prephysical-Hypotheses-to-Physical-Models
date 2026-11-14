import Std

/-! Position-only record of the last two wells and concatenation of
retained signed-residue words. On each recording layer a position
aperture includes both incoming rails. -/
namespace TwoWellTranscript

def dx (left : Bool) : Int := if left then -1 else 1

/-- When N>2, the pair of recorded neighboring wells fixes the arrival
rail. Both positions are compared on the actual cyclic base. -/
theorem two_well {N : Int} (large : 2<N) (before target : Int) (move want : Bool) :
    (before+dx move)%N=target%N ∧ move=want ↔
    before%N=(target-dx want)%N ∧ (before+dx move)%N=target%N := by
  constructor
  · rintro ⟨land,rfl⟩
    refine ⟨?_,land⟩
    have h := congrArg (fun x : Int => (x-dx move)%N) land
    simpa [Int.emod_sub_emod] using h
  · rintro ⟨prev,land⟩
    refine ⟨land,?_⟩
    have h := congrArg (fun x : Int => (x+dx want)%N) prev
    simp [Int.emod_add_emod] at h
    have diff := Int.emod_eq_emod_iff_emod_sub_eq_zero.mp (land.trans h.symm)
    by_cases e : move=want
    · exact e
    · have plus : (2:Int)%N=2 := Int.emod_eq_of_lt (by decide) large
      have neg : (-2:Int)%N=N-2 := by
        have k := Int.add_mul_emod_self_left (-2) N 1
        rw [Int.mul_one,Int.emod_eq_of_lt (by omega) (by omega)] at k
        omega
      cases move <;> cases want <;> simp [dx] at e diff <;>
        have norm : ((before + 1 - (before + -1))=2 ∧
                     (before + -1 - (before + 1))= -2) := by omega
      all_goals simp_all [Int.sub_eq_add_neg, Int.add_assoc, Int.add_left_comm, Int.add_comm] <;> omega

abbrev Gain := Int × Int  -- sign, integer sheet representative

def combine (u v : Gain) : Gain := (u.1*v.1,u.2+v.2)

def convolution (U V : List Gain) : List Gain :=
  U.flatMap (fun u => V.map (combine u))

def summed {K : Type} [Zero K] [Add K] (eval : Gain → K) : List Gain → K
  | [] => 0
  | u :: us => eval u + summed eval us

/-- Pure gain sums multiply before any conjugate-square read, including
zero sums, repeated words and empty records. The scalar identities are
just the multiplicative-character and semiring laws. -/
theorem multiply_transcript {K : Type} [Zero K] [Add K] [Mul K]
    (eval : Gain → K) (mul : ∀ u v, eval (combine u v)=eval u*eval v)
    (distL : ∀ a b c : K, a*(b+c)=a*b+a*c)
    (distR : ∀ a b c : K, (a+b)*c=a*c+b*c)
    (zeroL : ∀ a : K, 0*a=0) (zeroR : ∀ a : K, a*0=0)
    (assoc : ∀ a b c : K, (a+b)+c=a+(b+c)) (neutral : ∀ a : K, 0+a=a)
    (U V : List Gain) :
    summed eval (convolution U V)=summed eval U*summed eval V := by
  have append (a b : List Gain) : summed eval (a++b)=summed eval a+summed eval b := by
    induction a with
    | nil => simp [summed,neutral]
    | cons x xs ih => simp [summed,ih,assoc]
  have row (u : Gain) : summed eval (V.map (combine u))=eval u*summed eval V := by
    induction V with
    | nil => simp [summed,zeroR]
    | cons x xs ih => simp [summed,mul,ih,distL]
  induction U with
  | nil => simp [convolution,summed,zeroL]
  | cons u us ih =>
    simp only [convolution,List.flatMap_cons] at ih ⊢
    rw [append,row,ih,summed,distR]

end TwoWellTranscript
