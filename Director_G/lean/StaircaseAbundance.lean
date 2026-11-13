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

def stride : Rail → Int | R => 1 | L => -1
def drift (w : Word) : Int := (w.map stride).sum

private theorem position (w : Word) (u : State) : (run w u).1=u.1+drift w := by
  induction w generalizing u with
  | nil => simp [run,drift]
  | cons d w ih =>
    change (run w (step u d)).1=_
    rw [ih]
    rcases u with ⟨x,c,z,s⟩
    cases d <;> simp [step,drift,stride] <;> omega

/-- Every lift of a ring site has the same parity. A word from the origin
can reach only its own clock parity, even after any number of windings. -/
theorem clock_parity (w : Word) (M x winding : Int)
    (endpoint : (run w (hub 0 0)).1 = x+4*M*winding) :
    x%2=(w.length:Int)%2 := by
  have hp : drift w%2=(w.length:Int)%2 := by
    clear endpoint
    induction w with
    | nil => rfl
    | cons d w ih =>
      change (stride d+drift w)%2=(↑(w.length+1):Int)%2
      cases d <;> simp only [stride,Int.natCast_succ] <;> omega
  rw [position] at endpoint
  change 0+drift w=x+4*M*winding at endpoint
  have factor : 4*M*winding=4*(M*winding) := Int.mul_assoc _ _ _
  rw [factor] at endpoint
  omega

private theorem run_offset (w : Word) (x : Int) (d : Rail) (z s a b : Int) :
    let u := run w (x,d,z,s)
    run w (x,d,z+a,s+b)=(u.1,u.2.1,u.2.2.1+a,u.2.2.2+b) := by
  induction w generalizing x d z s with
  | nil => rfl
  | cons c w ih =>
    change run w (step (x,d,z+a,s+b) c)=_
    have rearr : step (x,d,z+a,s+b) c =
        ((step (x,d,z,s) c).1,c,(step (x,d,z,s) c).2.2.1+a,(step (x,d,z,s) c).2.2.2+b) := by
      dsimp [step]
      congr 1 <;> congr 1 <;> congr 1 <;> omega
    rw [rearr,ih]
    rfl

private def routeBody (M x : Nat) (d : Rail) : Word :=
  let rs := 2*M+x/2+x%2
  let ls := 2*M+2-x/2
  List.replicate (rs-(if d=R then 1 else 0)) R ++
    List.replicate (ls-(if d=L then 1 else 0)) L

def route (M x : Nat) (d : Rail) : Word := routeBody M x d ++ [d]

private theorem drift_repeat (n : Nat) (d : Rail) :
    drift (List.replicate n d)=(n:Int)*stride d := by
  induction n with
  | zero => simp [drift]
  | succ n ih =>
    rw [List.replicate_succ]
    change stride d+drift (List.replicate n d)=_
    rw [ih,Int.natCast_succ,Int.add_mul,Int.one_mul,Int.add_comm]

private theorem drift_join (w v : Word) : drift (w++v)=drift w+drift v := by
  induction w with
  | nil => simp [drift]
  | cons d w ih =>
    change stride d+drift (w++v)=(stride d+drift w)+drift v
    rw [ih,Int.add_assoc]

theorem route_geometry (M x : Nat) (hx : x<4*M) (d : Rail) :
    (route M x d).length=4*M+2+x%2 ∧ 2+drift (route M x d)=x := by
  cases d <;> simp [route,routeBody,drift_join,drift_repeat,stride]
    <;> constructor <;> (try simp [drift,stride]) <;> omega

private theorem fin_preimage (M : Nat) (hM : 0<M) (r : Fin M) (g : Int) :
    ∃ u : Fin M, ∀ z : Int, z%(M:Int)=u.val → (g+z)%(M:Int)=r.val := by
  let v := ((r.val:Int)-g)%(M:Int)
  have h0 : 0≤v := Int.emod_nonneg _ (by omega)
  have h1 : v<(M:Int) := Int.emod_lt_of_pos _ (by omega)
  refine ⟨⟨v.toNat,by omega⟩,?_⟩
  intro z hz
  have eq : z%(M:Int)=v := hz.trans (Int.toNat_of_nonneg h0)
  rw [← Int.add_emod_emod,eq]
  change (g+(((r.val:Int)-g)%(M:Int)))%(M:Int)=_
  rw [Int.add_emod_emod]
  have undo : g+((r.val:Int)-g)=r.val := by omega
  rw [undo,Int.emod_eq_of_lt (by omega) (by have := r.isLt; omega)]

/-- One-clock abundance for an entire parity. The terminal position is the
chosen lift x itself, so the same result holds for its physical ring port. -/
theorem abundant_parity (M k : Nat) (hM : 0<M) (x : Fin (4*M)) (d : Rail)
    (r : Fin M) (f : Bool) :
    ∃ w : List Bool → Word, (∀ u v, w u=w v → u=v) ∧
      ∀ bs, bs.length=k → (w bs).length=12*k+10*M+10+x.val%2 ∧
        ∃ z s : Int, run (w bs) (hub 0 0)=((x.val:Int),d,z,s) ∧
          z%(M:Int)=r.val ∧ s%2=bit f := by
  let tail := route M x.val d
  obtain ⟨hlen,hx⟩ := route_geometry M x.val x.isLt d
  generalize he : run tail (2,R,0,0) = q
  rcases q with ⟨y,c,g,h⟩
  have xpos := position tail (2,R,0,0)
  rw [he] at xpos
  have ypos : y=x.val := xpos.trans hx
  have rail : c=d := by
    have eq := congrArg (fun u : State => u.2.1) he
    change (run (routeBody M x.val d++[d]) _).2.1=c at eq
    rw [append_run] at eq
    exact eq.symm
  subst y; subst c
  obtain ⟨r',hr⟩ := fin_preimage M hM r g
  let b := decide (h%2≠bit f)
  have hb : ∀ s : Int, s%2=bit b → (h+s)%2=bit f := by
    intro s hs; cases f <;> simp only [b,bit] at * <;> split at hs <;> simp_all [bit] <;> omega
  obtain ⟨u,hinj,hu⟩ := abundant_exits M k hM R r' b
  refine ⟨fun bs => u bs++tail,fun _ _ eq => hinj _ _ (List.append_cancel_right eq),?_⟩
  intro bs hbs
  obtain ⟨len,z,s,hrun,hz,hs⟩ := hu bs hbs
  refine ⟨by rw [List.length_append,len]; change _ + (route M x.val d).length=_; rw [hlen]; omega,
    g+z,h+s,?_,hr z hz,hb s hs⟩
  rw [append_run,hrun]
  have ho := run_offset tail 2 R 0 0 z s
  simpa only [he,Int.zero_add] using ho

end StaircaseAbundance
