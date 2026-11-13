# Candidate Z1: abandoned on 13 November 2026

Abandoned the same day it was formulated, under the candidate process (`Director_Z/candidate/CANDIDATE_PROCESS.md`). The file `CANDIDATE_MODEL_Z1.md` beside this one is version 0.1, unchanged.

## What broke it

**Attack:** `attacks/2026-11-13_subagent_whole_and_S5/ATTACK_whole.md` and `ATTACK_S5.md`, by an attack sub-agent of the director (same model family as the author; not independent review). The attacker's own verdict was WOUND on both targets. The director read the argument, found it correct, and counts it as a kill under the process, because it shows that the candidate assumes its headline conclusion.

**The headline claim of Z1** was: "the squared norm is not assumed but follows from S1 to S6".

**Why that is false.**

1. **S5 is the conclusion in other words.** S5 says that the return weight comes close to one. The return weight is defined with the rule's own weights. Given D1 and S4, G10 Corollary 5.29(3) is an equivalence: near-return holds exactly when the count coefficient is zero. So S5 does not add a fact about the system from which a = 0 follows; it states a = 0. It cannot be checked before the rule is known. The director wrote Corollary 5.29 and then used it as if the premise were independent; it is not, as stated in Z1.
2. **Unitarity is in the carrier.** S1 to S5 can hold together only on a carrier where some character has A* A = d. Where none has, the only consistent rule is the count, S5 fails and the model has no rule. So the stipulations assert a norm-preserving step; they do not derive one.
3. **Only S5 separated classical from quantum.** The count satisfies S1 to S4 and S6. With S5 circular, nothing in Z1 excludes it.
4. **Diagonality is in S3.** A rule v^T G v with G = (4/5)(I + (U^2 + U^-2)/4) is not a sum over end vertices, satisfies the rest on the ring, and gives the same end-vertex probabilities as the model (computed by the attacker).

The attacker also showed that each of S2 to S5 is needed on the ring, by an explicit other rule for each one dropped, and that the literal S5 is met by a single equality at one length, so that it should have said limsup.

## What the director checked before accepting

The argument of points 1 to 3 against G10 Corollary 5.29 and Theorem 5.26 (they follow from the director's own statements); the attacker's result file `alt_rules_result.json` (seven of eight predicates met; the failed one, P6, is the attacker's and is kept); the table of alternative rules as reported. The alternative rules were not recomputed by the director.

## What survives, as mathematics and not as a model

- G10 Theorem 5.26 (D1): rules that add over end vertices a function of the gain multiset and are consistent under continuation have degree at most two: a count plus squares, the same at every vertex and length. This was not broken.
- G10 Corollary 5.28 (D3): multiplicativity on product events excludes mixtures.
- G10 Corollary 5.29 as a bound: for a normalized non-negative rule the return weight is at most 1 - a(1 - 1/d). It is a true inequality. It is not a derivation of a = 0 from an independent premise, and the sentences in G10 that present near-return as a premise "about the system" need the qualification that, as stated there, it is a condition on the rule. To be corrected in the next edition.
- The honest small statement, in the attacker's words: "branching plus recurrence excludes the random walk".

## Other findings of the same attack, kept for the next candidate

- Return is late or never exact: on rings of 3 to 12 sites the return weight equals one only for 4 sites (t = 8) and 8 sites (t = 24); it first exceeds 0.99 at t = 38, 8, 264, 38, 504, 24, 95946, 264 for 3 to 10 sites, not by t = 100000 for 11 sites, and at 6416 for 12.
- S3 and S5 have no formal conflict, because intermediate vertices are not records in the model; but the end-vertex distributions at two different lengths are not marginals of one distribution over histories.

## What a successor would need

A premise that separates the count from the squares and is not stated in the rule's own weights. The one on record is Director G's: the complete predictive state of the closed system lies in a compact convex set of finite affine dimension and its time step is an affine automorphism, with the rule's probabilities given by effects on that state. That is a stipulation about the state space, checkable without knowing the rule; it carries reversibility as an assumption, openly. Whether a candidate built on it survives attack is not known. Two further attacks on Z1 (events and records; composition and character) were still running when Z1 was abandoned; their findings will be read before any successor is written.
