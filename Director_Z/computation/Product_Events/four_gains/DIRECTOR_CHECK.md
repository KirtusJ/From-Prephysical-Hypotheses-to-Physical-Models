# Director's check of the four-gain theorem (14 November 2026)

Rerun by the director in a fresh directory: `four_gain.py`, exit code and duration as recorded below, result
byte-identical to the builder's (sha256 5657f0a5...2b2428af).

Steps checked by hand so far:
- Lemma 0: n_RR + n_LR = rho, n_RL + n_LL = lam; ending on R, n_RL = n_LR = n and the gain is
  a^(rho-n) c^n b^n d^(lam-n) = a^rho d^lam delta^(-n). Ending on L likewise with one more RL arc. Holds.
- Theorem 2(1): the maximum argument on the finite set Omega; closure of Omega under the four maps; F_L(m) =
  F_R(T_c m) because bc is in H. Holds.
- Theorem 2(3) Step 3: the symmetry of (Q), and G0(u + T_delta^2 v) = G0(u + v), which uses invariance under
  T_delta; delta lies in K = H cap Delta, so the invariance is available. Holds.
- The paper's case: a = b = c = 1, d = h gives K = A, |Delta/K| = 1, and one real character with chi(h) = -1 for
  q even: dimension 1 + [q even]. Agrees with the paper.

Not yet checked by the director: Steps 5 to 7 of Theorem 2(3) line by line, and the argument that C_0 = Delta_N
(the builder itself asks for a challenger on it). Both go to a challenger and to Lean (Steps 3 and 6) before
any of this enters the paper. PREP for four gains is a hypothesis; nothing is known about it.

Same model family as the builder; not independent review. No gate is claimed.
exit 0 seconds 145
5657f0a54814ecdd8345ede657d7c2d906a27efc2434178d1b55cdfa2b2428af  result.txt
