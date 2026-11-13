import Std

/-!
# Equal-depth abundance from a closed pair of labelled graph histories

Each edge has an integer gain and a source and destination. Histories are
lists of actual edges. A multiplicative inverse for the loop-gain difference
modulo q witnesses that this difference generates the cyclic group.
-/
namespace GainAbundance

structure Graph (V E : Type) where
  src : E → V
  dst : E → V
  gain : E → Int

variable {V E : Type} (G : Graph V E)

def Walk : V → List E → V → Prop
  | x, [], y => x = y
  | x, e::es, y => G.src e = x ∧ Walk (G.dst e) es y

def gain (w : List E) : Int := (w.map G.gain).sum

private theorem walk_append {a b c : V} {u v : List E}
    (hu : Walk G a u b) (hv : Walk G b v c) : Walk G a (u++v) c := by
  induction u generalizing a with
  | nil => exact (show a = b from hu) ▸ hv
  | cons e es ih => exact ⟨hu.1, ih hu.2⟩

private theorem gain_append (u v : List E) :
    gain G (u++v) = gain G u + gain G v := by
  induction u with
  | nil => simp [gain]
  | cons e es ih =>
    change G.gain e + gain G (es++v) = (G.gain e + gain G es) + gain G v
    rw [ih, Int.add_assoc]

private def copies (w : List E) : Nat → List E
  | 0 => []
  | k+1 => w ++ copies w k

private theorem copies_facts {hub : V} {w : List E} (h : Walk G hub w hub) (k : Nat) :
    Walk G hub (copies w k) hub ∧ (copies w k).length = k*w.length ∧
    gain G (copies w k) = (k:Int)*gain G w := by
  induction k with
  | zero => simp [copies, Walk, gain]
  | succ k ih =>
    refine ⟨walk_append G h ih.1, ?_, ?_⟩
    · simp [copies, ih.2.1, Nat.succ_mul, Nat.add_comm]
    · simp [copies, gain_append, ih.2.2, Int.add_mul, Int.add_comm]

/-- Order the same two loops either way to encode one binary choice at fixed
gain. Low bits first; the index is bounded in the injection theorem. -/
private def code (u v : List E) : Nat → Nat → List E
  | 0, _ => []
  | k+1, i => (if i%2=0 then u++v else v++u) ++ code u v k (i/2)

private theorem code_facts {hub : V} {u v : List E} (hu : Walk G hub u hub)
    (hv : Walk G hub v hub) (hlen : u.length = v.length) (k i : Nat) :
    Walk G hub (code u v k i) hub ∧ (code u v k i).length = (2*k)*u.length ∧
    gain G (code u v k i) = (k:Int)*(gain G u + gain G v) := by
  induction k generalizing i with
  | zero => simp [code, Walk, gain]
  | succ k ih =>
    obtain ⟨hc, hl, hg⟩ := ih (i/2)
    simp only [code]
    split
    · refine ⟨walk_append G (walk_append G hu hv) hc, ?_, ?_⟩
      · simp [List.length_append, ← hlen, hl, Nat.mul_add, Nat.add_mul]; omega
      · simp [gain_append, hg, Int.add_mul]; omega
    · refine ⟨walk_append G (walk_append G hv hu) hc, ?_, ?_⟩
      · simp [List.length_append, ← hlen, hl, Nat.mul_add, Nat.add_mul]; omega
      · simp [gain_append, hg, Int.add_mul]; omega

private theorem code_injective {u v : List E} (hlen : u.length = v.length)
    (hne : u ≠ v) (k : Nat) {i j : Nat} (hi : i < 2^k) (hj : j < 2^k)
    (eq : code u v k i = code u v k j) : i = j := by
  induction k generalizing i j with
  | zero => simp at hi hj; omega
  | succ k ih =>
    have bound_i : i/2 < 2^k := by rw [Nat.pow_succ] at hi; omega
    have bound_j : j/2 < 2^k := by rw [Nat.pow_succ] at hj; omega
    have diff : u++v ≠ v++u := fun h => hne (List.append_inj_left h hlen)
    unfold code at eq
    split at eq <;> split at eq
    · have tails := ih bound_i bound_j (List.append_cancel_left eq)
      omega
    · exact False.elim (diff (List.append_inj_left eq (by simp [hlen])))
    · exact False.elim (diff (List.append_inj_left eq (by simp [hlen])).symm)
    · have tails := ih bound_i bound_j (List.append_cancel_left eq)
      omega

/-- A constructive bound uniform in the target vertex and residue. There are
at least 2^k distinct walks to each target/gain, each of length
(2k+q)L+D, where L is the common loop length and D the exit-word length.
Both endpoints of a pair can use the same bound by taking equal-length
exit words. Exit-word gains may be unrelated and may have either sign. -/
theorem histories_from_generator {hub target : V} {u v tail : List E}
    (hu : Walk G hub u hub) (hv : Walk G hub v hub) (ht : Walk G hub tail target)
    (hlen : u.length = v.length) (hne : u ≠ v)
    (q : Nat) (hq : 0 < q) (inv : Int)
    (unit : (gain G v-gain G u)*inv % (q:Int) = 1 % (q:Int)) (res : Fin q) (k : Nat) :
    ∃ f : Fin (2^k) → List E,
      (∀ i j, f i = f j → i = j) ∧
      ∀ i, Walk G hub (f i) target ∧
        (f i).length = (2*k+q)*u.length + tail.length ∧
        gain G (f i) % (q:Int) = (res.val:Int) := by
  let base := (k:Int)*(gain G u + gain G v) + (q:Int)*gain G u + gain G tail
  let d := gain G v - gain G u
  let r := (((res.val:Int) - base)*inv) % (q:Int)
  have qr : 0 < (q:Int) := by omega
  have rpos : 0 ≤ r := Int.emod_nonneg _ (by omega)
  have rlt : r < (q:Int) := Int.emod_lt_of_pos _ qr
  let j := r.toNat
  have jcast : (j:Int) = r := Int.toNat_of_nonneg rpos
  have jle : j ≤ q := by omega
  let suffix := copies u (q-j) ++ copies v j ++ tail
  obtain ⟨hu', hlu, hgu⟩ := copies_facts G hu (q-j)
  obtain ⟨hv', hlv, hgv⟩ := copies_facts G hv j
  have hs : Walk G hub suffix target := walk_append G (walk_append G hu' hv') ht
  have ls : suffix.length = q*u.length + tail.length := by
    simp only [suffix, List.length_append, hlu, hlv, ← hlen]
    rw [← Nat.add_mul, Nat.sub_add_cancel jle]
  have gs : gain G suffix = (q:Int)*gain G u + (j:Int)*d + gain G tail := by
    have gain_v : gain G v = gain G u+d := by dsimp [d]; omega
    simp only [suffix, gain_append, hgu, hgv, gain_v, Int.mul_add]
    have jq : (↑(q-j):Int) + (j:Int) = q := by omega
    have prod := congrArg (fun s : Int => s * gain G u) jq
    simp only [Int.add_mul] at prod
    omega
  refine ⟨fun i => code u v k i.val ++ suffix, ?_, ?_⟩
  · intro i j eq
    apply Fin.ext
    exact code_injective hlen hne k i.isLt j.isLt (List.append_cancel_right eq)
  · intro i
    obtain ⟨hc, hl, hg⟩ := code_facts G hu hv hlen k i.val
    refine ⟨walk_append G hc hs, ?_, ?_⟩
    · simp [hl, ls, Nat.add_mul, Nat.add_assoc]
    · simp only [gain_append, hg, gs]
      have regroup : (k:Int)*(gain G u+gain G v) + ((q:Int)*gain G u+(j:Int)*d+gain G tail)
          = (j:Int)*d+base := by unfold base; omega
      have shifted : ((j:Int)*d)%(q:Int) = ((res.val:Int)-base) % (q:Int) := by
        rw [jcast]
        dsimp only [r]
        have undo (a : Int) : (a%(q:Int)*d)%(q:Int) = (a*d)%(q:Int) := by
          rw [Int.mul_emod (a%(q:Int)) d, Int.emod_emod, ← Int.mul_emod]
        rw [undo, Int.mul_assoc, Int.mul_comm inv d, Int.mul_emod _ (d*inv),
            show (d*inv) % (q:Int) = 1 % (q:Int) from unit, ← Int.mul_emod, Int.mul_one]
      rw [regroup, ← Int.emod_add_emod, shifted, Int.emod_add_emod]
      have reduce : ((res.val:Int)-base)+base = res.val := by omega
      rw [reduce, Int.emod_eq_of_lt (by omega) (by have := res.isLt; omega)]

/-- A unit gain difference of exactly +1 needs no modular-inverse witness. -/
theorem histories_at_every_gain {hub target : V} {u v tail : List E}
    (hu : Walk G hub u hub) (hv : Walk G hub v hub) (ht : Walk G hub tail target)
    (hlen : u.length = v.length) (delta : gain G v = gain G u + 1)
    (q : Nat) (hq : 0 < q) (res : Fin q) (k : Nat) :
    ∃ f : Fin (2^k) → List E,
      (∀ i j, f i = f j → i = j) ∧
      ∀ i, Walk G hub (f i) target ∧
        (f i).length = (2*k+q)*u.length + tail.length ∧
        gain G (f i) % (q:Int) = (res.val:Int) := by
  have hne : u ≠ v := by intro eq; rw [eq] at delta; omega
  have one : (gain G v-gain G u)*(1:Int) = 1 := by rw [Int.mul_one]; omega
  exact histories_from_generator G hu hv ht hlen hne q hq 1 (by rw [one]) res k

/-- The same length works for all gains at both target labels. Different
residues cannot share an edge word, and different endpoints cannot share a
word with the same initial vertex. -/
theorem two_target_horizon {hub : V} {u v : List E} (hu : Walk G hub u hub)
    (hv : Walk G hub v hub) (hlen : u.length = v.length) (hne : u ≠ v)
    (q : Nat) (hq : 0 < q) (inv : Int)
    (unit : (gain G v-gain G u)*inv % (q:Int) = 1 % (q:Int))
    (target : Bool → V) (exitWord : Bool → List E)
    (exits : ∀ b, Walk G hub (exitWord b) (target b))
    (common : (exitWord true).length = (exitWord false).length) (k : Nat) :
    ∀ (b : Bool) (res : Fin q), ∃ f : Fin (2^k) → List E,
      (∀ i j, f i = f j → i = j) ∧
      ∀ i, Walk G hub (f i) (target b) ∧
        (f i).length = (2*k+q)*u.length + (exitWord false).length ∧
        gain G (f i) % (q:Int) = (res.val:Int) := by
  intro b res
  have len : (exitWord b).length = (exitWord false).length := by
    cases b
    · rfl
    · exact common
  simpa only [len] using
    histories_from_generator G hu hv (exits b) hlen hne q hq inv unit res k

end GainAbundance
