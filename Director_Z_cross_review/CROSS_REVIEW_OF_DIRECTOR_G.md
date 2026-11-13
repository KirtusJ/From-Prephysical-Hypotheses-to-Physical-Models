# Director Z | Cross-review of two results of Director G

13 November 2026. Research direction: Kirtus Justus. Reviewing participant: LLM Director Z, Claude (Anthropic). Subject: research supplements of Director G (Codex) in pull request 2 of the program repository, branch `director-g/records-and-forced-envelope`, commit `b626c0d30348eba5f1640bcbc19dd6169167d3f4`. Digests of the files read are in `DIRECTOR_G_FILES_READ_SHA256.txt`. Director G named the two targets on the review thread (pull request 1, comment 6847254453).

This is a cross-review by a participant of another model family working from the same baseline and in contact with the author during the work. It is not an independent review, and agreement is not replication.

## 1. Reproduction of Director G's programs (executed)

The four checkers were run on Linux (Python 3.13.18, numpy 2.5.3) into fresh directories; the stored results were produced on Windows (Python 3.12.14, numpy 2.3.5).

| Output | Comparison with the stored file |
|---|---|
| `probability_selection.json` | identical apart from line endings |
| `probability_walk_trials.csv` (2920 rows) | byte-identical |
| `checks.json`, `filter_trials.csv`, `ray_trials.csv` | numeric differences at most 2.4e-8 relative; no other difference |
| `record_selection.json`, `record_branch_trials.csv` | at most 3.2e-12 |
| `forced_envelope.json`, `forced_envelope_trials.csv` (54774 rows) | at most 1.5e-6 relative, in residuals; no predicate changed |

A same-input rerun: it shows the programs run and return the stored values on another platform. Two of the checkers import a sibling module and do not run under Python's isolated mode; that is a property of how they were invoked here, not a defect.

## 2. Target 1: classification of weights by field embeddings

**Claim (Director G, `Probability_from_record_composition.md`).** On K = Q(zeta_M, sqrt 2), M odd, a weight W that passes the marginal test with one balanced coin, is invariant under multiplication by zeta, factorizes on product tables and has W(1) = 1 is W(a) = lambda(a conj a) for a field embedding lambda of the real subfield F; conversely each such W qualifies.

**Reading of the proof (REASONED).** Each step was followed.
- The flag comparison gives W((a+b)/sqrt2) + W((a-b)/sqrt2) = k [W(a) + W(b)], and b = 0 gives 2 W(a/sqrt2) = k W(a); together they give the parallelogram law. Checked.
- The parallelogram law on a Q-vector space gives a symmetric Q-bilinear B with W(a) = B(a, a). Here halving is available; the same lemma without halving is G10 Lemma 5.4.
- Product tables give W(xy) = W(x) W(y); with W(2) = 4 this gives W(sqrt2) = 2, hence sqrt2 is self-adjoint for B; invariance under zeta gives the adjoint conj(zeta). Since K is generated as a ring by zeta and sqrt2, B(sx, y) = B(x, conj(s) y) for every s, so W(x) = lambda(conj(x) x) with lambda(t) = B(1, t) on F. Checked; inversion is not needed.
- lambda is multiplicative on norms; norms span F because t = ((t+1)^2 - (t-1)^2)/4; so lambda is a unital ring homomorphism, hence an embedding. Checked.
- Converse: K lies in an abelian cyclotomic field, so every embedding commutes with conjugation and |sigma(a)|^2 = lambda(a conj a) passes all three conditions. Checked; F is totally real, so all its embeddings are real.

No gap was found. Two remarks. (i) The number of solutions is [F : Q] = phi(M): for M = 5 the four choices of a root of q^2 + q - 1 and a sign of sqrt2. (ii) The claim uses every element of K as a preparation, which the paper states as a hypothesis stronger than what the walk supplies.

**Check by another route (EXECUTED; `crosscheck_director_g.py`, predicates fixed before the run).**
- X1: for M = 3, 5, 7, 9 the symmetric Q-bilinear forms on K with adjoint conj(zeta) for zeta and self-adjoint sqrt2 form a space of dimension 2, 4, 6, 6 = phi(M), by an exact rational nullspace computation; the forms of the phi(M) embeddings lie in it (residual below 5e-15) and are independent. This is the linear core of the claim obtained without the proof: every admissible W is a real combination of the embedding weights.
- X2: for M = 5, on 300 sampled pairs, such a combination is multiplicative for each single embedding (defect below 2e-14) and for none of five other weight vectors (defect 0.50 to 0.94). Together with X1 this gives the claim by the idempotent argument of G10 Proposition 5.6.
- X3: the five-sheet values are 0.3272542485937368 = (3 + sqrt5)/16 and 0.0477457514062631 = (3 - sqrt5)/16; the control entry s = q + sqrt2 - 2 is 0.0322 in the ordinary embedding and -2.796, -2.204, -5.032 in the other three.

**Disposition.** The claim as stated: no defect found on reading; its linear core and its instances confirmed by a route that imports nothing from the author (Z-061). The operational premises (that the flag preparations, the independently timed coin and product tables are available) are the author's stated assumptions and were not assessed.

**Relation to G10.** G10 Theorem 5.5 reaches the same family from consistency on history events, without multiplicativity, and therefore stops at combinations; with multiplicativity (G10 Proposition 5.6 (b)) it reaches single embeddings. Director G's classification was issued first. The two derivations use different premises and agree where both apply.

## 3. Target 2: spinor bound and position law under a constant force

**Claim (Director G, `Forced_envelope_and_classical_motion.md`).** For a packet in the plus band near k* = -pi/2 with envelope supported in |p| <= P, the l2 distance between the walk and the constant-force Schroedinger envelope encoded at the final momentum is at most E(t) = 2|F| t delta + t delta^2 L^4/(6 eps) + t |F| L delta^2/2, L = P + |F| t, delta L <= 1; and for a shrinking packet the scaled lattice position law converges weakly to the point mass at Y0 + p0 t - F t^2/2.

**Reading of the proof (REASONED).** Followed term by term.
- First term: replacing the section u(k_{j-1}) by u(k_j) costs |u'| |h| per step and the errors add by unitarity; n |h| = |F| t delta. The stated bound |u'| <= 2 holds; the computed largest value is 0.7071, so the first term has a margin of a factor 2.8.
- Second term: |w(k* + q) - w(k*) - q^2/2| <= q^4/6. The integrand is sin s / sqrt(1 + sin^2 s) = s - (2/3) s^3 + (19/30) s^5 - ..., so the remainder is q^4/6 - (19/180) q^6 + ...; checked in 60-digit arithmetic on 4000 grid points (largest ratio 0.99999984).
- Third term: right-endpoint quadrature of p(s)^2/2 with derivative bounded by |F| L. Checked.
- Phase (2): the integral of (p - F s)^2/2 over [0, t]. Checked.
- Position law: a bounded observable changes by at most twice the state distance; replacing the section by the constant spinor costs 2 delta L in norm; the shift by xi eps in p gives the continuum characteristic function; the envelope deviation is at most sqrt(eps) (|g'| + t |s g|); the continuity theorem gives weak convergence. Checked. The paper's own caveat stands: no statement about variances or about successive outcomes on one path.

No gap was found.

**Check by another route (EXECUTED).** A real-space walk on a ring (the step of G9 with the gain exp(-i h x) on arcs leaving site x), not the fibre recursion of the author; the envelope is encoded in the section built from the band projector; three runs.

| Run | sites | steps | largest distance | bound E over the run | mean scaled position at the end | classical Y |
|---|---|---|---|---|---|---|
| eps = 1, delta = 0.05 | 65536 | 400 | 3.1e-4 | 0.010 to 0.086 | -0.08438 | -0.08350 |
| eps = delta = 0.1 | 65536 | 1000 | 4.0e-4 | 0.020 to 0.302 | -0.17949 | -0.17937 |
| eps = delta = 0.05 | 1048576 | 4000 | 7.4e-5 | 0.006 to 0.053 | 0.030124 | 0.030158 |

- X5: the distance is within the bound at every sampled time in all three runs; the largest ratio of distance to bound is 0.011. The bound holds with a margin of two orders of magnitude in these runs, as expected of a bound built from worst-case terms.
- X6: the characteristic function at xi = 1 is within the paper's chain of bounds; its distance from exp(i Y_c) is 0.137 at eps = 0.1 (t = 1) and 0.071 at eps = 0.05 (t = 0.5). The chain of bounds is loose enough that both orientations of the position axis pass it; the mean scaled position identifies the orientation used by the author (agreement to 1.2e-4 and 3.4e-5).

**A failure of this participant's check, kept.** Predicate X4 of the first program failed: the ratio of the band remainder to q^4/6 came out as 1.000114 at a grid point near q = 0.001, where the remainder is 1.7e-13 and is formed by cancellation in double precision. The follow-up program repeats the test in 60-digit arithmetic and it holds. The failure is in the check, not in the paper.

**Disposition.** The bound and the weak convergence: no defect found on reading; the bound confirmed in three real-space runs (Z-062). What the result is and is not, in the terms of this program: a conditional link from the signed walk to a constant-force Schroedinger equation and to a Newtonian position record, for a packet prepared in one band near a band edge, with the squared-amplitude readout, with lattice variables scaled by hand, and with a field h = F eps delta^3 that tends to zero, hence with gains of unbounded order (G10 Proposition 6.1). It does not address the full-period criterion of OP-26, as its author states.

## 4. What Director G found in G10

Recorded in `ADDENDUM_EDITION_Z7.md`: four proofs read and reported as holding within their hypotheses; one summary sentence false (binary tree); the informal dimension count for order two corrected; the requirement of a common length made explicit.

## 5. Limits

One reader. The reading was done with the author's text open and in contact with the author; exposure is total. The executed checks import nothing from the author's programs but share the author's statement of the problem, the baseline and the conventions of paper G9. Not read: `Signed_walk_and_weak_field.md`, `Records_and_complex_structure.md`, the gate map and metadata files of Director G, and the three other checkers' source beyond what was needed to run them.
