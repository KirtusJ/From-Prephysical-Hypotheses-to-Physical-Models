import Std

namespace VelocityMeshParity

/-- Parity of a terminal site's signed path sum. Over F₂ both Hadamard signs
    are +1, so forgetting the final rail gives the ordinary Pascal recurrence.
    k is the number of rightward steps, hence the site displacement is 2k-n. -/
def pathParity : Nat → Nat → Bool
  | 0, k => k == 0
  | n+1, 0 => pathParity n 0
  | n+1, k+1 => xor (pathParity n (k+1)) (pathParity n k)

/-- Two Pascal steps over F₂: the two ways to take one right step cancel. -/
theorem twoSteps (n k : Nat) :
    pathParity (n+2) (k+2) = xor (pathParity n (k+2)) (pathParity n k) := by
  simp only [pathParity]
  cases pathParity n (k+2) <;> cases pathParity n (k+1) <;>
    cases pathParity n k <;> decide

theorem evenZeroOdd (n k : Nat) :
    pathParity (2*n) (2*k+1) = false := by
  induction n generalizing k with
  | zero => simp [pathParity]
  | succ n ih =>
    cases k with
    | zero =>
      rw [Nat.mul_succ]
      simp only [Nat.mul_zero, Nat.zero_add, pathParity]
      have h := ih 0
      simp only [Nat.mul_zero, Nat.zero_add] at h
      cases h0 : pathParity (2*n) 0 <;> simp [h, h0]
    | succ k =>
      rw [Nat.mul_succ, Nat.mul_succ]
      have off := twoSteps (2*n) (2*k+1)
      have atK := ih k
      have atS := ih (k+1)
      rw [Nat.mul_succ] at atS
      rw [show 2*k+2+1 = 2*k+1+2 by omega, off]
      rw [show 2*k+1+2 = 2*k+2+1 by omega, atS, atK]
      decide

theorem evenEven (n k : Nat) :
    pathParity (2*n) (2*k) = pathParity n k := by
  induction n generalizing k with
  | zero =>
    cases k <;> simp [pathParity] <;> omega
  | succ n ih =>
    cases k with
    | zero =>
      rw [Nat.mul_succ]
      simpa [pathParity] using ih 0
    | succ k =>
      rw [Nat.mul_succ, Nat.mul_succ, twoSteps, pathParity]
      rw [show 2*k+2 = 2*(k+1) by omega, ih, ih]

theorem oddRow (n k : Nat) :
    pathParity (2*n+1) (2*k) = pathParity n k ∧
    pathParity (2*n+1) (2*k+1) = pathParity n k := by
  constructor
  · cases k with
    | zero => simpa [pathParity] using evenEven n 0
    | succ k =>
      rw [Nat.mul_succ, pathParity]
      change xor (pathParity (2*n) (2*k+2)) (pathParity (2*n) (2*k+1)) = _
      rw [show 2*k+2 = 2*(k+1) by omega, evenEven, evenZeroOdd]
      simp
  · rw [pathParity, evenZeroOdd, evenEven]
    simp

/-- Every reachable site has odd total signed amplitude numerator. Its two
    directed amplitudes therefore cannot both vanish. -/
theorem fullRow (m k : Nat) (hk : k < 2^m) :
    pathParity (2^m-1) k = true := by
  induction m generalizing k with
  | zero =>
    have : k = 0 := by simpa using hk
    subst k
    decide
  | succ m ih =>
    have hp : 0 < 2^m := Nat.pow_pos (by decide)
    rw [Nat.pow_succ] at hk ⊢
    have hn : 2^m*2-1 = 2*(2^m-1)+1 := by omega
    rw [hn]
    have hl : k/2 < 2^m := by omega
    obtain ⟨he, ho⟩ := oddRow (2^m-1) (k/2)
    by_cases even : k%2=0
    · have ke : k=2*(k/2) := by omega
      exact (congrArg (pathParity (2*(2^m-1)+1)) ke).trans (he.trans (ih _ hl))
    · have ke : k=2*(k/2)+1 := by omega
      exact (congrArg (pathParity (2*(2^m-1)+1)) ke).trans (ho.trans (ih _ hl))

end VelocityMeshParity
