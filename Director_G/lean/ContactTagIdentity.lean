import Std

namespace ContactTagIdentity

/-- A path contributes to the coefficient of I or of SWAP on the tag register. -/
abbrev Coeff := Int × Int

def sectors (c : Coeff) : Coeff := (c.1 + c.2, c.1 - c.2)

inductive Gate where
  | common (k : Int)
  | contact (k : Int)

def physical : Gate → Coeff → Coeff
  | .common k, (a,b) => (k*a,k*b)
  | .contact k, (a,b) => (k*b,k*a)

def scalarStep : Gate → Coeff → Coeff
  | .common k, (a,b) => (k*a,k*b)
  | .contact k, (a,b) => (k*a,-(k*b))

theorem eachStep (g : Gate) (c : Coeff) :
    sectors (physical g c) = scalarStep g (sectors c) := by
  cases c with
  | mk a b =>
    cases g <;> simp only [sectors, physical, scalarStep, Int.mul_add, Int.mul_sub,
      Prod.mk.injEq] <;> constructor <;> omega

theorem contactWord (word : List Gate) (c : Coeff) :
    sectors (word.foldl (fun a g => physical g a) c) =
      word.foldl (fun a g => scalarStep g a) (sectors c) := by
  induction word generalizing c with
  | nil => rfl
  | cons g rest ih =>
    simp only [List.foldl_cons, ih, eachStep]

theorem addPaths (a b : Coeff) :
    sectors (a.1+b.1,a.2+b.2) =
      ((sectors a).1+(sectors b).1,(sectors a).2+(sectors b).2) := by
  simp only [sectors, Prod.mk.injEq]
  constructor <;> omega

end ContactTagIdentity
