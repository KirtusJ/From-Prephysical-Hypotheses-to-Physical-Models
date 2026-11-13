import Std

/-! Physical signed Hadamard histories on the staircase lift.
The last two state entries are the integer departure gain and the number
of L-to-L transitions, reduced modulo M and 2 only at the read. -/
namespace StaircaseAbundance

inductive Rail | R | L deriving DecidableEq
open Rail
abbrev Word := List Rail
abbrev State := Int × Rail × Int × Int

def step : State → Rail → State
  | (x,d,z,s), c => (x + (if c = R then 1 else -1), c, z+x/2,
                        s + (if d = L ∧ c = L then 1 else 0))

def run (w : Word) (u : State) := w.foldl step u
def hub (z s : Int) : State := (0,R,z,s)
def A : Word := [R,L,R,L,L,R]
def B : Word := [L,R,R,L,L,R]
def C : Word := [R,L,L,R]
def D : Word := [L,R,L,R]
def exitWord : Rail → Word | R => [R,R,L,R] | L => [R,R,R,L]
def exitGain : Rail → Int | R => 1 | L => 2

theorem loops (z s : Int) :
    run A (hub z s) = hub (z-1) (s+1) ∧
    run B (hub z s) = hub (z-2) (s+1) ∧
    run C (hub z s) = hub (z-1) (s+1) ∧
    run D (hub z s) = hub (z-2) s := by
  simp [run,step,hub,A,B,C,D,List.foldl] <;> omega

theorem exits (d : Rail) (z s : Int) :
    run (exitWord d) (hub z s) = (2,d,z+exitGain d,s) := by
  cases d <;> simp [run,step,hub,exitWord,exitGain,List.foldl] <;> omega

theorem append_run (u v : Word) (p : State) :
    run (u++v) p = run v (run u p) := List.foldl_append

/-- The enclosed integer coordinate is a valid lift of the 4M-site base
ring: translating a departure by one circumference adds exactly 2M. -/
theorem staircase_period (x M : Int) :
    (x+4*M)/2 = x/2+2*M := by omega

def copies (w : Word) : Nat → Word
  | 0 => []
  | n+1 => w ++ copies w n

theorem copies_length (w : Word) (n : Nat) : (copies w n).length=n*w.length := by
  induction n with
  | zero => simp [copies]
  | succ n ih => simp [copies,ih,Nat.succ_mul,Nat.add_comm]

theorem copies_run {w : Word} {g h : Int}
    (hw : ∀ z s, run w (hub z s)=hub (z+g) (s+h)) (n : Nat) (z s : Int) :
    run (copies w n) (hub z s)=hub (z+n*g) (s+n*h) := by
  induction n generalizing z s with
  | zero => simp [copies,run]
  | succ n ih =>
    rw [copies,append_run,hw,ih]
    simp only [Int.natCast_succ,Int.add_mul,Int.one_mul]
    congr 1 <;> omega

def tag : Bool → Word | false => A++B | true => B++A
def historyCode (bs : List Bool) : Word := bs.flatMap tag

theorem tag_run (v : Bool) (z s : Int) :
    run (tag v) (hub z s)=hub (z-3) (s+2) := by
  cases v <;> simp only [tag,append_run,(loops _ _).1,(loops _ _).2.1]
            <;> congr 1 <;> omega

theorem code_run (bs : List Bool) (z s : Int) :
    run (historyCode bs) (hub z s)=hub (z-3*bs.length) (s+2*bs.length) := by
  induction bs generalizing z s with
  | nil => simp [historyCode,run]
  | cons b bs ih =>
    change run (tag b++historyCode bs) _=_
    rw [append_run,tag_run,ih]
    simp only [List.length_cons,Int.natCast_succ]
    congr 1 <;> omega

theorem code_length (bs : List Bool) : (historyCode bs).length = 12*bs.length := by
  induction bs with
  | nil => rfl
  | cons b bs ih =>
    change (tag b++historyCode bs).length=_
    cases b <;> simp [tag,A,B,ih] <;> omega

theorem code_injective (u v : List Bool) (h : historyCode u=historyCode v) : u=v := by
  induction u generalizing v with
  | nil =>
    cases v with
    | nil => rfl
    | cons b v => have hlen := congrArg List.length h; simp [code_length] at hlen; omega
  | cons a u ih =>
    cases v with
    | nil => have hlen := congrArg List.length h; simp [code_length] at hlen; omega
    | cons b v =>
      change tag a++historyCode u=tag b++historyCode v at h
      have eq : a=b := by
        cases a <;> cases b <;> simp_all [tag,A,B]
      subst b
      rw [ih v (List.append_cancel_left h)]

def choose : Bool → Word | false => D | true => C
def bit : Bool → Int | false => 0 | true => 1

private theorem choose_run (b : Bool) (z s : Int) :
    run (choose b) (hub z s) = hub (z-2+bit b) (s+bit b) := by
  cases b <;> simp only [choose,bit,(loops _ _).2.2.1,(loops _ _).2.2.2]
          <;> congr 1 <;> omega

def suffix (M a : Nat) (b : Bool) (d : Rail) :=
  copies A a ++ copies B (M-a) ++ choose b ++ exitWord d

theorem suffix_run (M a : Nat) (ha : a≤M) (b : Bool) (d : Rail) (z s : Int) :
    run (suffix M a b d) (hub z s) =
      (2,d,z+a-2*M-2+bit b+exitGain d,s+M+bit b) := by
  have wa : ∀ z s, run A (hub z s) = hub (z+(-1)) (s+1) := (fun z s => (loops z s).1)
  have wb : ∀ z s, run B (hub z s) = hub (z+(-2)) (s+1) := (fun z s => (loops z s).2.1)
  simp only [suffix,append_run,copies_run wa,copies_run wb,choose_run,exits]
  have h : (↑(M-a):Int)=(M:Int)-a := by omega
  rw [h]
  simp only [Prod.mk.injEq,true_and,Int.mul_one]
  constructor <;> omega

theorem suffix_length (M a : Nat) (ha : a≤M) (b : Bool) (d : Rail) :
    (suffix M a b d).length = 6*M+8 := by
  cases b <;> cases d <;> simp [suffix,copies_length,A,B,C,D,choose,exitWord] <;> omega

/-- Both exits admit all gain/sign classes at one common clock for every
positive M. The witness injects all k-bit words by prepending neutral-order
permutations, yielding 2^k distinct physical words for every class. -/
theorem abundant_exits (M k : Nat) (hM : 0<M) (d : Rail) (r : Fin M) (f : Bool) :
    ∃ w : List Bool → Word,
      (∀ u v, w u=w v → u=v) ∧
      ∀ bs, bs.length=k → (w bs).length=12*k+6*M+8 ∧
        ∃ z s : Int, run (w bs) (hub 0 0)=(2,d,z,s) ∧
          z%(M:Int)=r.val ∧ s%2=bit f := by
  let b := decide (((M:Int)%2) ≠ bit f)
  have hbit : ((M:Int)+bit b)%2=bit f := by
    cases f <;> simp only [b,bit] <;> split <;> simp_all [bit] <;> omega
  let base : Int := -3*k-2*M-2+bit b+exitGain d
  let a := (((r.val:Int)-base)%(M:Int)).toNat
  have hp : 0<(M:Int) := by omega
  have hpos := Int.emod_nonneg ((r.val:Int)-base) (show (M:Int)≠0 by omega)
  have hlt := Int.emod_lt_of_pos ((r.val:Int)-base) hp
  have ha : (a:Int)=((r.val:Int)-base)%(M:Int) := Int.toNat_of_nonneg hpos
  have hle : a≤M := by omega
  have hz : ((a:Int)+base)%(M:Int)=r.val := by
    rw [ha,Int.emod_add_emod]
    have t : (r.val:Int)-base+base=r.val := by omega
    rw [t,Int.emod_eq_of_lt (by omega) (by have := r.isLt; omega)]
  refine ⟨fun bs => historyCode bs ++ suffix M a b d, ?_, ?_⟩
  · intro u v eq
    exact code_injective u v (List.append_cancel_right eq)
  · intro bs hk
    refine ⟨by simp [code_length,hk,suffix_length M a hle,Nat.add_assoc], a+base,2*k+M+bit b,?_,hz,by omega⟩
    rw [append_run,code_run,hk,suffix_run M a hle]
    simp only [base,Prod.mk.injEq,true_and]
    constructor <;> omega

end StaircaseAbundance
