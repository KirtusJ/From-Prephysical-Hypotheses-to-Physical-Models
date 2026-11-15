Target: two steps of the proof of G10 Theorem 5.16 (thm:block): the difference step (vanishing threefold differences give a polynomial of degree at most two on each coset) and the maximum argument for the parts of degree zero and one (director's Z16 request); master a8c9608.
Control: decide in Lean that 2^n >= n + 1 for all natural n. Expected: proved. Delivered a proof. Control passed.
Outcome: NONE FOUND; both steps check in general form; a shorter argument for the first.
Reviewer kind: pcp-formalizer run as a sub-agent of the queue session; the file was rerun by the queue session (exit 0, standard axioms, no sorry / axiom / native_decide). Same model family as the author. Not independent review.

G10Block.lean (Lean 4.12.0, Mathlib v4.12.0):
- third_diff_quadratic: on any abelian group, a real function whose third differences vanish equals f(0) + l(x) + b(x,x)/2 with l additive and b symmetric biadditive. No lattice, divisibility or rank condition is needed (2 is invertible in the reals).
- third_diff_coset: the same with steps in dG, for x -> f(c + dx) on every coset.
- max_arg: on a finite set, m >= 0 with d^2 m(c) <= sum over d values of m, d >= 2, forces m = 0; used for deg_zero (constants) and deg_one (in any normed group, with sum ||l'||^2 = d^2 ||l||^2).
Not formalized: "additive on Z^n means linear" (standard); the derivation in the paper of the degree-one hypothesis from T^t l' = d l and T = sqrt(d) U; Step 1's reduction to the threefold-difference equation.
Shorter argument: the second difference f(h+k) - f(h) - f(k) + f(0) is already symmetric and biadditive, so f - f(0) - b(x,x)/2 is additive; this replaces the paper's chain through constant twofold differences and affine differences and needs no basis. The maximum argument is one lemma used twice, needing only d >= 2 and finitely many cosets.
Rechecked by the queue session: the rerun. Cost: about 6 minutes, 4 tool calls.
