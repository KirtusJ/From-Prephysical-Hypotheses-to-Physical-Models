# Director's recheck of the Lean worker, 15 November 2026

The worker was briefed as a coordinator. It reported that a sub-agent has no tool for launching sub-agents in this host, so it wrote the four files itself; there was no second reader below it. Control answered correctly.

Recheck: each of SymQuad, Transfer, ThreeStep, AxisQuad copied to a scratch Mathlib project and run by the director with `lake env lean`: exit 0 each, no `sorry`, axioms propext, Quot.sound, Classical.choice only. Copies are kept as `Director_Z/lean/Winding*.lean` with the worker's outputs.

What they cover: lem:symquad for k = 2 (with uniqueness) and k = 3 (existence, explicit coefficients); the scalar-transfer step of thm:fgprod in a finite formulation; the induction of thm:fgthree for every degree and both signs, with the polynomial identity behind e_beta * A = B and the shift-invariance of the periodic form; the two-axis step of lem:twolevelabs, in the form with the two families of pairs, where evenness is derived and not assumed.
What they do not cover: lem:symquad for general k (the dimension count); that g is a sum of products; the identity of multisets e_beta * A = B itself; Steps 1 to 5 of the two-level argument; anything about events.
