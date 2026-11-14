# Answers

All counts below come from an enumeration program I wrote (all walks of length 3 and 4; the doubling check in Item 5 over all subsets of walks for lengths 0 to 3 and 2000 seeded random subsets each for lengths 4 and 5; 4278 sets per rule, 0 failures).

## Item 1

- Length 3, port (-1, L): route count 2 (RLL, LRL), signed total 0 (RLL is -, LRL is +).
- Length 4, port (0, L): route count 3 (RRLL, RLRL, LRRL), signed total +1.
- Length 4, port (2, L): route count 1 (RRRL), signed total +1.

## Item 2

The proof is correct. Lines 1 and 2 give two base cases and a two-step induction hypothesis. Line 3 is the recurrence solved for g(n+1) with g(1) = c. Line 4 expands correctly: 2cn^2 + 2c - c(n^2 - 2n + 1) = cn^2 + 2cn + c = c(n+1)^2.

## Item 3

The claim and the conclusion are true, but the proof is not correct as written. The first wrong line is Line 3. Line 2 gives F(V) + F(JV) = 2 F(V), so the step should read F(JV) = 2 F(V) - F(V) = F(V). The written "3 F(V) - 2 F(V)" does not follow from Line 2; it only happens to equal the same value. Lines 1 and 2 are correct.

## Item 4

Not accurate.

- The first part is right: 399 + 107 = 506, and every rule received a negative event (and 57 + 22 + 28 = 107).
- "107 of them only beyond multiplicity three" is wrong. Only 57 of the 107 were searched over entries 0..3. The other 50 were searched only over 0..2 (22 rules) or 0..1 (28 rules), so for them the record excludes events only up to multiplicity two or one; an event at multiplicity three (or two) is not ruled out.
- The supported sentence is: "107 not found by the small search; 57 of these have none with entries 0..3, 22 none with entries 0..2, 28 none with entries 0..1; all 107 found by a larger search."
- Even for the 57, "only beyond three" needs the 0..3 search to have been exhaustive over that box, which the record does not say.

## Item 5

False as written. The hypothesis allows the weight to depend on the port, and the conclusion wrongly says the constant a does not.

Counterexample: F_y(p, q) = x (p + q), where x is the site of port y. More generally (a + b x)(p + q) + c (p - q)^2 with b nonzero works.

- Why it satisfies the hypothesis: the rule is additive over walks, each walk at site x has weight x, and its two continuations have weights (x + 1) + (x - 1) = 2x. So the total doubles for every set of walks.
- Why it is not of the stated form: at port (1, R) with (p, q) = (1, 0) the weight is 1, and at port (-1, L) with (1, 0) it is -1. The form a(p + q) + c(p - q)^2 with a, c independent of y gives a + c at both.
- Check on the two walks of length 1 (R at port (1, R), sign +; L at port (-1, L), sign +):

| Set | Weight | Continuations | Weight after |
|---|---|---|---|
| {R} | 1 | RR at (2, R): 2; RL at (0, L): 0 | 2 |
| {L} | -1 | LR at (0, R): 0; LL at (-2, L), sign -: -2 | -2 |
| {R, L} | 0 | all four | 0 |

Each doubles. The stated form itself (a = 2, c = 3) also passed the same check, so the form is sufficient but not necessary.

The statement becomes plausible only with an added hypothesis, for example that the rule is the same function at every port, or that weights are non-negative (x (p + q) is negative at x < 0). I did not prove either repaired version.

## Item 6

"No gate is passed and the root review remains open; today one new theorem was proved under its stated hypotheses, which is a conditional result and neither passes a gate nor yields an ontology."
