# Director Z, fourth session | Eighteenth addendum: edition Z22

13 November 2026. Same session and participant. Root Review: G1, OPEN. No ontology is selected.

## Assessment Z4-V (FOCUSED): composition, the count or one character

**Question put.** Theorem 5.26 leaves a vector space of consistent rules: the count and the squares for the qualifying characters, with any real coefficients. Proposition 5.6(b) showed, for squares alone, that multiplicativity on products removes the combinations. Does it also remove the mixtures of the count with a square?

**Answer.** Yes. Let D be a carrier of Theorem 5.26 and mu a consistent rule a|S| + sum of c ||v^psi_S||^2. For two events of D of one length the product event has the pairs of walks, with the product of the gains; on it the count and each square are the products of their values on the factors. If mu, given by the same formula on product events, is multiplicative for all pairs of events at every sufficiently large length, then mu is zero, the count, or the squared norm for one class of characters (Corollary 5.28). Each of these is multiplicative.

**What it changes.** Consistency and composition together leave a choice among finitely many rules with fixed normalization: one that ignores the gains, and one for each class of characters in which the step is norm-preserving. Mixtures are excluded. Nothing makes the choice. The corollary assumes the same formula on the product, concerns products of a carrier with itself only, and does not examine consistency on the product carrier.

**Case.** The count and the squares are linearly independent as functions on the events of one large length whose walks end at one vertex (they are polynomials of degree at most two in the counts, independent on multisets, hence on multisets of size at most two). Multiplicativity is then a relation to which independence is applied twice, once in each event, giving e_i e_j = delta_ij e_i for the coefficients.

**Origin.** Statement and proof by the director. This is the first statement of this run not found by a sub-agent, and it was sent to a challenger with that said.

**Executed.**

| Check | Outcome |
|---|---|
| Challenger, four carriers (two vertices over C_2; B_4; the ring of four sites; B_8 with two classes), all pairs of events of length three, up to 65,536 pairs | no failing step; only the rules named are multiplicative; violating pairs exhibited for (1,1), (2,0), (0,2), (1/2,1/2), (1,-1) |
| Same program at length two on B_4 and the ring of four | 4 instances of a predicate failed and are kept: the mixtures (1/2,1/2) and (1,-1) are multiplicative there, because every event of that length has count equal to squared norm; a rank predicate failed on the same instances |
| Lean with Mathlib, `Composition.lean` | the coefficient step over any commutative ring, and the consequence over a domain; exit code 0, rerun by the director; the formal proof applies independence twice and is the one now given in the paper |
| Micro-review of the director's five summary sentences | see the corrections |

**Corrections before issue (Z-123).** From the challenger: the hypothesis "at every length" is replaced by "at every sufficiently large length", with the length-two instances stated; a citation pointed to part (c) of Theorem 5.26 where the fact is in its proof; the existence of the vertex and length used is now derived; two sentences omitted the zero rule. From the micro-review of the five summary sentences: the abstract omitted the zero rule, large lengths and the carrier with itself; the sentence in the list of what is not obtained attached the corollary to Corollary 5.20, whose carriers it does not cover; the Lean step is now named. Corrected.

**Disposition.** SUPPORTED_IN_SCOPE (Z-122), mathematics, unrefereed. Carriers with C_0 different from C were not computed for this corollary. Reviewers of the participant's model family.

## The review hierarchy and tools (Z-124)

Recorded in `pcp_workers/HIERARCHY_LOG.md` with scripts in `pcp_workers/recursion/`: chains of headless workers relay correctly to depth eight at about eleven seconds per level; a task restated at four levels keeps its meaning and changes its terms; a level that adds nothing costs a cold start; the working rule is at most two levels below the director. `tools/pcp_submit.py` refuses to submit a register call file twice; it was written after two duplicate submissions and is tested against a stand-in server only. The principal allows changes to the PCP repositories and a restart of PCP, with care toward Director G; nothing was changed, and the rule for such a change is in `CLAUDE.md`.

## Records

Paper G10 revised (46 pages, 31 labelled statements and one remark). Register: review `Z22`. Amended: OP-30. Findings Z-122 to Z-124.
