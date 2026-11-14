# NOTES form_four (formalizer; same model family as the director: not independent review)

## Step 0. CONTROL (answered before any Lean)
g : Z -> R, g(s+t) + g(s-t) = 2 g(s) + 2 g(t) for all s, t.
- s = t = 0: 2 g(0) = 4 g(0), so g(0) = 0.
- s = 0: g(t) + g(-t) = 2 g(0) + 2 g(t) = 2 g(t), so g(-s) = g(s).
- t = s: g(2s) + g(0) = 4 g(s), so g(2s) = 4 g(s).

## Step 1. Environment and Mathlib search
- Lean 4.12.0, Mathlib tag v4.12.0 at mathlib_proj; nothing installed.
- grep "parallelogram" in Mathlib: only Analysis/InnerProductSpace/{Basic,OfNorm,TwoDim,Projection}.
  `InnerProductSpaceable` + `InnerProductSpaceable.add_left` (OfNorm.lean) proves additivity of the
  polarization of a NORM on a normed group over RCLike satisfying the parallelogram identity (and then
  uses continuity for real scalars). It is stated for `‖x‖*‖x‖`, not for an arbitrary g : D -> R on an
  abelian group, so it does not cover Q1 as stated. `QuadraticMap.ofPolar` needs polar additivity as input;
  no constructor from the parallelogram law found.
- `module` tactic exists (Mathlib/Tactic/Module.lean); `linear_combination` is ring-only at this tag.

## Step 2. Plan (written before first compile)
- Core: V any AddCommGroup with hV : forall v, v + v = 0 -> v = 0; P s t := g(s+t) - g(s-t) (= 2B, no division).
- Module version: Ring R, Invertible (2:R), B := (1/2) • P. Real version: exact statements asked.
- Q1(d) route: four instances h (s+t) (s'+t), h (s-t) (s'-t), h (s+s'+t) t, h (s+s'-t) t; no use of (a).
- Q2: (a) needs only (Q) + commutativity (T arbitrary function, no invariance). Hand check suggests
  invariance is derivable from (Q) and T(0+0) = T0 + T0: with e = T0, e+e = e, (Q) at (e,0) gives
  f(e)+f(e) = 2f(e)+2f(0), so f(0)=0; (Q) at (0,v) gives f(v)+f(Tv) = 2f(v). To be checked in Lean.
- Q3: symmetry looks unneeded; D need not be commutative. Q4: finiteness unneeded; relation needed only at x.

## Step 3. First compiles
- run1 (exit 1): two faults of mine, kept: (i) `decide` on a goal with free variables in the ZMod 2
  counterexample; (ii) section `variable (R)` not included in theorems whose statement does not mention R.
  All Q1 real, Q2, Q3, Q4 proofs passed at the first attempt.
- run2 (exit 0): all statements pass, axioms subset of {propext, Quot.sound, Classical.choice}.

## Step 4. Q2 hypotheses re-examined by hand after run2
- From (Q) at (0,v): f(Tv) = f(v) + 2 f(0). So invariance <=> f(0) = 0 (real values).
- (Q) at (Tu, v) with invariance: f(Tu+v) + f(Tu+Tv) = 2f(u)+2f(v) = f(u+v) + f(u+Tv), and
  f(Tu+v) = f(u+Tv) by (a). So f(Tu+Tv) = f(u+v) WITHOUT additivity of T. Hence (b) needs only
  (Q) + invariance, T an arbitrary function. First version of Q2b used hT; replaced.
- With (Q) alone (b) is false: M = N, T v = v+1, f(n) = 2n+1: (Q) holds (4(u+v)+4 both sides),
  f(0) = 1, f(u+TTv) = f(u+v) + 4. To be put in Lean as a counterexample.

## Step 5. run3 (exit 0) after the Q2 change
- Q2b now proved from (Q) + invariance only (T arbitrary); Q2b_hand keeps the route with additivity;
  Q2b' from (Q) + T(0+0)=T0+T0 (invariance derived); Q2b_false_from_Q_alone is the counterexample.

## Step 6. Probe: is 2-torsion-freeness needed for Q1(d) undivided?
- torsion_probe.py (helper, brute force; predicate in docstring). D in Z/2..Z/6, Z/2xZ/2, Z/2xZ/4, V in Z/2, Z/4.
  Every case has qualifying g (2 to 64); none has P non-additive. No counterexample found; NOT decided.
  Lean: the doubled identity core_P_add_left_two needs no hypothesis on V; the cancellation of 2 uses hV.
  Torsion-freeness IS needed for g(0)=0 (Q1a_needs_torsion_free, constant 1 into ZMod 2).

## Step 7. Final run
- command: export PATH=$HOME/.elan/bin:$PATH; cd mathlib_proj; lake env lean FPHPM/FourGain.lean
- exit 0, no warnings, 40 `#print axioms` lines: 18 [propext, Classical.choice, Quot.sound],
  2 [propext, Quot.sound], 15 [propext], 5 no axioms. Last line: Q1_main.
- sha256 FourGain.lean = 09241fa40de14b94e85d92292bf49034a0eecb4de95e467a12c1f9e08c951d90 (both copies identical)
- sha256 final.out = c6d62c1fe11c023608ab8a715bd39865c7b1b35142bb4f78dcfbe9102784443a
- token scan sorry|native_decide|^axiom|admit: only the header comment line 15.
- Hand route Q1(d): works as written (hand_H1, hand_H2, hand_Q1d); H2 from H1 at s'=0 uses evenness of g.
  Shortest route (Q1d): 4 instances + linarith, no use of (a).
- Unused hypotheses: Q2(a) additivity+invariance; Q2(b) additivity; Q3 symmetry and commutativity of D;
  Q4 finiteness and the relation away from x.
