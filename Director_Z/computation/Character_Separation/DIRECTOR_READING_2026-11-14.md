# Director's line-by-line reading of CRITERION.md (14 November 2026)

The builder's report is left as filed. This is the director's check of its proofs, done by hand; it is the same
model family as the builder and is not independent review. No gate is claimed. Nothing here is in the paper yet.

| Item | Checked how | Outcome |
|---|---|---|
| Word-gain identity (1) | Recounted arcs: n_RL = l - m, n_LR = l - m - e, n_RR = t - 2l + m + e; product of gains | holds |
| Prop 1 | x = t - 2l mod N fixes l mod D; c_k real for eta real; masks do not depend on chi | holds |
| Prop 2(a) | two left counts in [0,t], same class mod D, t <= D: only {0, D}, words R^D and L^D, different rails (also D = 1) | holds; true for every N, the report's "N >= 3" is not needed for (a) |
| Prop 2(b) | redid the enumeration: for j < D the wells +j and -j are distinct (D does not divide j); from +j only R stays in the mask, from -j only L; at tick D both in well D; only R reaches D+1 when N >= 3 | holds; (l,m) = (0,0), (D, D-1) |
| Prop 2(c) | from Prop 1, (a), (b) | holds |
| Prop 2(d) | the step is unitary iff chi(H) = -1 (a conj c + b conj d = 0 iff ad = -bc); words RR, LR at port (2, R) | holds |
| Prop 3(a) | Re beta^3 = 0 and Re beta^5 = 0 give beta^6 = beta^10 = -1, so beta^4 = 1, beta^2 = -1 | holds |
| Prop 3(b) | beta'^D1 = beta^D1; beta'^D2 beta^D2 = 1; beta' beta = tau != 1 | holds; needs D1, D2 >= 2, as stated |
| Prop 3(c) | power map is a bijection of the q-th roots and commutes with conjugation | holds |
| Corollaries | fair count iff Re omega = 0; note's group: 3 divides D iff 3 divides N | hold |
| Control | control.py rerun in a fresh directory, exit 0, result file byte-identical | reproduced |

Not checked by me: table.py was not rerun in this reading (the builder reports a byte-identical rerun; that is a
claim until rerun). P4 is not reached by computation for N = 7, 9, 11, 12; there the least length rests on Prop 2(a).

Sent to a formalizer the same day: Prop 3(a), Prop 3(b) and the modulus identity.

Follow-up, same day: table.py rerun by the director in a fresh directory. A first attempt did not run (exit 127, a missing timing tool; kept as a failed attempt). Second attempt:

```
exit 0 seconds 47
03bcd177b8c48c23079a54309a84b2086dc1aa0143bdd6ae0e4131219adae7b0  table_result.json
```

Filed digest of table_result.json: 03bcd177b8c48c23079a54309a84b2086dc1aa0143bdd6ae0e4131219adae7b0.
