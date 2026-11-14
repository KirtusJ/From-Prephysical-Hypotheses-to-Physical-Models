# Tally Ring (candidate Z2): form

Version 0.1, 14 November 2026. First version; the statements it cites are under review (status table below).
Kirtus Justus, Theoretical Physicist, Port Coquitlam, British Columbia, Canada; compiled with the assistance of
Director Z (a Claude session). Not an ontology. No gate is passed.

## 1. The stipulations

Seven, each separately breakable. None is derived, and the candidate does not say why any of them holds.

**T1. Place and time.** There are N places in a circle, numbered modulo N, with N >= 3 and finite. Time is a
count of ticks. At each place there are two rails, R and L. A *step* from either rail of place x goes to
(x+1, R) or to (x-1, L).

**T2. Tally.** There is a finite abelian group C and four of its elements a, b, c, d. A step carries the
element named by the rail it leaves and the rail it enters: a from R to R, b from R to L, c from L to R, d from
L to L. A *history* is a sequence of steps; its *tally* is the product of the elements its steps carry.

**T3. Voice.** The world has one unitary character chi of C, its *voice*, and chi(a d) = -chi(b c).

**T4. Start.** Every run starts at place 0 on rail R.

**T5. Instruments.** The only instruments are *screens* and one *reading*. A screen at tick j is a set of
places; a history passes it if it is at one of those places after its j-th step. The reading, at the last
tick, is of a place and a rail. Nothing reads a rail before the last tick, and nothing reads a tally.

**T6. Appearance.** For a run of t ticks with given screens, the weight of a reading is
2^(-t) |sum of chi(tally)|^2, the sum over the histories that pass every screen and end at that place and
rail. Weights are relative frequencies over many runs.

**T7. Closure.** Nothing enters from outside. Whatever a later part of a run starts from was produced by the
steps and screens of the earlier part.

Abbreviations used below: B = b c a^-2, H = a d (b c)^-1 (so T3 reads chi(H) = -1), M = N / gcd(N, 2),
u = chi(B), omega = u^M.

## 2. What the stipulations are, said plainly (the director's own first attack)

**As dynamics the Tally Ring is a known object.** T1 to T3 with T6 describe a discrete-time coined quantum
walk on a cycle of N sites, with the coin (1/sqrt 2) [[chi(a), chi(c)], [chi(b), chi(d)]]. T3 is exactly the
condition that this coin is unitary. The coin is not general: its four entries have equal modulus. T5 is
measurement of position, with projections onto sets of sites along the way, and T6 is the Born rule.

So the candidate does not propose new dynamics, and it does not explain the Born rule; it assumes it (this is
what broke Z1, and here it is stipulated in the open). What the candidate is, beyond that known walk:
(i) the bookkeeping of every amplitude as the voice's value on a tally, which lets a gain group and a
character be asked about separately from the walk; (ii) the closure T7 and the restriction T5 taken as part of
the world, and not as limits of a laboratory; and (iii) exact statements of what an inhabitant confined to
T5 and T7 can and cannot find out. Whether (iii) is more than the gauge symmetry of the walk is examined in
section 4.

## 3. What is proved from the stipulations

Each line gives the statement, where its proof is, and its review state. "Draft" is
`Director_Z/papers/drafts/G10_subsection_what_masks_read.tex`. All reviewers so far are sub-agents of the
same model family as the writer, or Director G where named; none is independent review.

| # | Statement | Where | State |
|---|---|---|---|
| D1 | With no screen the weights of all readings at one tick sum to 1 | T3 makes the coin unitary; paper G10, norm-preserving digraphs | proved; in the issued paper |
| D2 | The tally of a history depends only on its length, its final rail, its number of left steps and its number of L-to-L steps: tally = a^t (a/c)^e B^l H^m | Draft, Lemma (word gain); the identity is Director G's | proved; hand-checked by the director; computed on 81,840 words |
| D3 | Every weight depends on the world (C, a, b, c, d, chi) only through Re(omega) | Draft, Proposition (what the statistics can depend on), with T4 | proved; challenged, no defect found in range |
| D4 | Re(omega) is read: the fork event has weight 2^-(M+1) (2 + 2 (-1)^(M-1) Re omega); and no run of M ticks or fewer reads anything about the voice | Draft, Proposition (what is read) and Corollary (complete list); fork event Director G's | proved; boundary review done; challenged, no defect found in range |
| D5 | Two worlds with voices chi and its complex conjugate have the same weights for every instrument | Draft, Corollary (conjugate character) | proved; challenged, no defect found in range |
| D6 | Two worlds with different groups C and the same Re(omega) have the same weights for every instrument | Draft, Corollary (complete list), "of the same or of different gain groups" | proved; challenged on 23 pairs only (thin) |
| D7 | Rings of N = 4, 3, 5 places together fix chi(B) up to complex conjugation; no two ring sizes of 3 or more do so for every value | Draft, Proposition (several rings) | proved; checked in Lean (`Director_Z/lean/CharSeparation.lean`) |
| D8 | Under T7 no part of a run can start from a state that reads more than D3 allows: whatever screens and steps produce carries a factor that cancels chi(c/a) | Draft, Proposition (the walk cannot prepare) | proved; algebra in Lean (`Director_Z/lean/TwoRail.lean`); challenger found no defect in range |

| D9 | T3 can be tested from inside: with no screen, the reading (tick 3, place -1, rail L) has weight (1 + Re chi(H))/4, which is zero exactly when T3 holds | Draft, Remark (a), from the computation in the proof of Proposition (what is read)(i); found by the challenger, 193 of 193 carriers, and checked by hand by the director | proved |

Not derived, and marked so that it is not mistaken for a result of the candidate:

| # | Statement | State |
|---|---|---|
| X1 | If T6 is replaced by "some rule that adds over readings a function of the tallies arriving there, and doubles under one more tick, on events built from screens", the rules are a count plus the square of T6, in fixed proportion (paper G10, position product events; for four tallies, the four-gain theorem under a preparation hypothesis that is not proved) | context only. It shows T6 is one member of a two-parameter family, and that the stipulation is exactly the choice "no count". It does not select T6 |
| X2 | If T4 or T7 is dropped and a start in both rails is supplied from outside, two more numbers are read and the two voices chi and its conjugate can be told apart | proved (draft; Lean; challenged). It shows what T4 and T7 hide |

## 4. Where it is most likely to break

Named in advance; each is an attack the director intends to make or to commission. The ledger is `LEDGER.md`.

1. **D3 to D6 may be nothing but the walk's known symmetries.** Rephasing the two rails changes b and c and
   leaves bc; a common phase leaves B; multiplying right steps by e^(ik) and left steps by e^(-ik), with k a
   multiple of 2 pi / N, multiplies B by e^(-2ik) and leaves omega = B^M. Complex conjugation with the
   reflection x to -x is a symmetry of position statistics. If the "complete list" is exactly the list of
   invariants of these symmetries, then D3 to D6 are true and say nothing that is not already in the symmetry
   group of a quantum walk on a cycle. That would not falsify a statement; it would empty the brand's "one
   thing it offers", which is a kill of the candidate as branded (a wound that changes what the model claims).
2. **T5 may be doing all the work.** A screen that selects a rail, or a reading of a tally, is excluded by
   stipulation. If the smallest enlargement of T5 reads everything, the limitation is the instruments' and
   not the world's.
3. **T7 with T4 may be inconsistent with T5.** A screen is itself an intervention from somewhere. If the
   screens must be set by something outside the walk, "nothing enters from outside" is false as stated.
4. **T6 and T3 leave nothing to explain.** The candidate cannot be an explanation of anything it stipulates.
   An attacker who shows that every interesting consequence is a consequence of T3 and T6 alone, with T2 idle,
   shows that the tallies are decoration.
5. **D6 is thinly tested.** D3 to D5 have since been challenged from the draft text (rings of 3 to 10 places for the named events, exhaustive screens on rings of 3 to 5): no defect found in range; six corrections to wording were made, one of which became D9.
6. **No classical limit, no dynamics of more than one walker, no gravity-like or field-like content** is
   stipulated or derived. As a universe it is very small, and stipulated answers to large questions will
   mostly have to be SILENT.

## 5. Status in one line

Seven stipulations written; nine derived statements, two in the issued paper or machine-checked, seven in a
draft that has had one challenger (same model family); six lines of attack named, none yet carried out. The candidate stands
only in the sense that it has not been attacked.
