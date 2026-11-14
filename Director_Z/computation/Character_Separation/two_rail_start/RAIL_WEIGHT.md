# The rail weight of a two-rail start is readable (14 November 2026)

This closes the first open point of the builder's FINDINGS.md ("whether |alpha|^2 itself is readable"). By the
director, by hand, then by exact enumeration. Same model family as the builder; not independent review. A
statement about the model; no gate is claimed, and nothing here is in the paper yet.

## Statement

Setting as in CRITERION.md, with start alpha|0,R> + beta|0,L>, any abelian gains a, b, c, d, a unitary character
chi with chi(H) = -1 (H = ad/(bc)), and a ring of N >= 3 sites or the line. With no mask at all:

    P(tick 3, site 1, rail R)  = |alpha|^2 / 2,
    P(tick 3, site -1, rail L) = |beta|^2 / 2.

No normalization of (alpha, beta) is used.

## Proof

Port (3, 1, R). A word of three steps ends on rail R at site 1 mod N only with exactly one left step that is
not the last: RLR or LRR. (Left counts 1 and 3 are the only ones in the class of site 1 for N = 4, and three
left steps end on rail L; for the other N >= 3 only one left step reaches site 1.) From rail R the two words
have gains (RR, RL, LR) = abc and (RL, LR, RR) = abc. From rail L they have gains (LR, RL, LR) = bc^2 and
(LL, LR, RR) = acd. So the amplitude is

    2^(-3/2) [ 2 alpha chi(abc) + beta ( chi(bc^2) + chi(acd) ) ]
  = 2^(-3/2) chi(abc) [ 2 alpha + beta chi(c/a) ( 1 + chi(H) ) ],

because acd / (abc) = (c/a) H. With chi(H) = -1 the second term vanishes and P = |alpha|^2 / 2.
Port (3, -1, L): the words are RLL and LRL; from rail L their gains are (LR, RL, LL) = bcd and (LL, LR, RL) =
bcd, and from rail R they are (RR, RL, LL) = abd and (RL, LR, RL) = b^2 c, whose ratio to each other is
(a d)/(b c) = H. So the amplitude is 2^(-3/2) [ alpha chi(b^2 c)(1 + chi(H)) + 2 beta chi(bcd) ] and
P = |beta|^2 / 2. QED.

The reason in words: the two words that meet at the port differ by exchanging an R and an L step. From the
rail on which their arcs differ by the plaquette gain H they cancel when chi(H) = -1; from the other rail
their gains are equal and they add.

## Computed

`rail_weight/alpha_read.py`, exact arithmetic in Gaussian rationals, seed 20261114, predicates fixed in the
docstring before the first run. 4000 cases drawn (N = 3..9, gains with character values in the fourth roots of
unity, five starts including sharp ones and one with a complex ratio). Hypothesis tested per case:
983 qualify with chi(H) = -1.

| Predicate | qualify | pass | fail |
|---|---|---|---|
| P1: P(3, 1, R) = |alpha|^2/2 | 983 | 983 | 0 |
| P2: P(3, -1, L) = |beta|^2/2 | 983 | 983 | 0 |
| C1 (control, chi(H) = +1, expected to fail as a universal statement) | 977 | 199 | 778 |

Exit 0; rerun in a fresh directory byte-identical (sha256 36ade4e4...71450318); overwrite refused.

## Consequence for the builder's Theorem B

"For known |alpha|^2" can be dropped: for N >= 3 and chi(H) = -1, two data (start, carrier, character) have
identical statistics on all position-mask events if and only if they share
(|alpha|^2, |beta|^2, Re omega, Re kappa, Im omega Im kappa). Each of the five is read by a named event.

Still open: chi(H) not real; N = 1, 2; Lean.
