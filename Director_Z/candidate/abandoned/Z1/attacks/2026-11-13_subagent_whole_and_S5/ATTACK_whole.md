**Verdict: WOUND.** Target: "The whole". Attacker: sub-agent of the author's model family; not independent review.

The model is not a pure restatement: D1 (degree at most two, no cross terms) is a theorem and was not broken here. But "the squared norm is not assumed but follows from S1 to S6" is false as written. Only the degree is derived; unitarity, diagonality and the exclusion of counting are stipulated.

**1. The unitary is in the carrier.** v_S and v_{Ext S} = A v_S are defined by S1 alone. S1 to S5 are jointly satisfiable only if some character has A*A = d: where none has (G10's three-vertex example) the only consistent rule is the count, S5 fails, and the model has no rule. So S5 also asserts "the step is unitary". That existence clause added to S1 is the smallest sub-collection giving a vector with a preserved quadratic form. S2 does not force it: the count satisfies S2.

**2. S5 is D2.** Given D1 and S4, Corollary 5.29(3) is an equivalence: near-return if and only if a = 0. S5 is written in the rule's own weights and cannot be checked before the rule is known. Any other one-bit selector does the same work, for example "some non-empty event has weight zero", visible at t = 3.

**3. Only S5 separates classical from quantum.** The count satisfies S1 to S4 and S6. What is derived is "branching plus recurrence excludes the random walk": true and small, not a derivation of the Born rule.

**4. Diagonality is in S3.** See GRAM below: without "sum over end vertices" another U-invariant quadratic form passes everything else.

**Each of S2 to S5 is needed on Z1-R.** Ring of 8 sites, x0 = (0,R), all events of length 0 to 4 enumerated exactly; S5 tested as R_t = 1 for some t <= 48. E is the pair of walks of length 3 ending at (1,R); model weight 4.

| Dropped | Rule | Fails only | Values |
|---|---|---|---|
| S5 | count; (count + norm)/2 | S5: max R_t 1/4; 18433/32768 | E: 2; 3 |
| S4 non-negativity | (37/5)norm - (32/5)count | -64/5 on the two walks to (7,L) | E: 84/5; R_10 = 1 |
| S4 normalization | (1/2)count + (30719/32768)norm | single walk 47103/32768 | R_24 = 1 |
| S3 additivity | GRAM: v^T G v, G = (4/5)(I + (U^2 + U^-2)/4) | additivity | walks to (2,R) and (0,R) at length 2: 11/5, model 2; same P_t(y) |
| S3 gains | norm for the signing with the minus sign at site 0 moved to (0,R)->(7,L) | not a function of the gains | E: 0; P_3 mirrored; R_12 = 1 |
| S2 | square at x0, count elsewhere | consistency | E: 2; R_24 = 1 |

Row two shows the literal S5 ("comes arbitrarily close") is met by one equality at one length.

**Computed.** `alt_rules.py`: 7 of 8 predicates; P6 failed and is kept (the uniform re-signing is a switching and equals the model on all events). `alt_rules_followup.py`: 24 single-site re-signings, all norm-preserving, 4 differ from the model, 2 return exactly at t = 12. Caveat: that row is the model's rule on another S1 carrier.

**Not tried.** No strictly weaker set with the same consequences was found. S6 was not tested on the alternative rules (it is idle on Z1-R, as is S7). Whether non-negativity is redundant under a limsup reading of S5 was not examined. D1 and Z1-F were not attacked.
