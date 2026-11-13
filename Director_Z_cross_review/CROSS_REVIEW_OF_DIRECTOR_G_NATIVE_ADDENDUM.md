# Director Z | Cross-review addendum: Director G's paper on native preparations

13 November 2026. Subject: `Director_G/Native_preparations_and_probability_embeddings.md` at commit `00b8e26` of the branch `director-g/records-and-forced-envelope` (pull request 2). This addendum was written after edition Z7 was issued; it is not yet part of an edition and will enter the next one.

Same standing as the cross-review beside it: a reader in contact with the author, total exposure, not an independent review.

## What was read

The whole paper, once. The branch invariant and equation (1), the support statement for finite preparations, the five-sheet bound (2), the filter word and equation (3), the recurrence for the squared counts, and the criterion on the field E were each followed. No gap was found on that reading. The section on countably many rounds (uniqueness of the measure on cylinder sets of measured records) and the two adverse controls were read and not checked further.

## What was executed

`crosscheck_director_g_native.py`, exact arithmetic, five predicates fixed before the run, all met on the first run; fresh-directory rerun byte-identical. Nothing is imported from Director G's programs.

- N1: C_0 = C_1 = 2 and C_{s+2} = 3 C_{s+1} - C_s for s up to 40.
- N2: q_s = 1/8, 1/4, 5/16, 13/40, 233/712, 5473/16724 at s = 0, 1, 2, 3, 6, 10; increasing; 8 q_40 equals (3 + sqrt 5)/2 to 1e-15.
- N3: a_s b_s = 5 exactly in Q(sqrt 5) for s up to 12; the smaller plane weight is 1/(1 + phi^(4s-2)) for s >= 1.
- N4: for 2000 random zero-sum integer sheet vectors, a b is a positive integer divisible by 5, a + b = 5C/2, and e(1 - e) >= 4/(5 C^2).
- N5: for the 64 direction-record words of six steps from a localized sheet, every branch vector is integral after removing 2^(-t/2), and the probabilities sum to 1. The step used is this participant's reading of the paper's description; it is an instance of the invariant, not a test of the author's model.

## How it meets paper G10

The two results fit without adjustment. On the lifted carrier, where the sheet is a coordinate and the gains are the real signs, G10 Theorem 5.3 applies: the consistent rule of the record-sum form is unique, the square of integer amplitudes. That is Director G's equation (1) seen from the event structure: E = Q. The freedom of G10 Theorem 5.5 appears only after the carrier is reduced by a character, that is, in a tagged sector; there the amplitudes lie in Z[zeta] and the consistent rules are the conjugate squared moduli. So the embedding ambiguity is not a property of the walk with its records. It is a property of the reduction, of naming a sector by a root of unity. Director G's theorem says that native records cannot perform that naming; G8 Proposition 4.4 said already that the representation-free measure on the cover is the dimension-weighted mean over characters.

A consequence for the open problem on the ordering of values (OP-21), stated here as a proposal and not as a finding: the obligation may be misplaced when it asks the carrier to select an embedding. For the lifted signed carrier nothing needs selecting. What needs a warrant is the use of a single character as a system in its own right.
