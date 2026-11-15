# Candidate Z8, "Two Books": form

**Label: STIPULATED CANDIDATE FOR DISPROOF.** Not a claim about the world, not an ontology; no gate of the program is passed by it. Kirtus Justus, Theoretical Physicist, Port Coquitlam, British Columbia, Canada; compiled with the assistance of Director Z (a Claude session). Governed by [the candidate process](../CANDIDATE_PROCESS.md). Final candidate of the sprint of 15 November 2026.

Every numbered stipulation is separately breakable.

## 1. Stipulations

| # | Stipulation | Kind |
|---|---|---|
| S1 | **Space and histories.** Histories are walks from (0,R) on the two-rail digraph of the line or of a ring of N ≥ 1 sites: a right step from either rail of x leads to (x+1,R), a left step to (x−1,L). A left step that follows a left step carries the sign −1; every other step carries +1. | carrier |
| S2 | **Events and running free.** An event is a position product event: all walks of one length whose site after each step lies in a prescribed set (a mask). A world *runs free* when every site is admitted at the next step. | instruments |
| S3 | **The book of chance.** At an end vertex v let ε(v) be the sum of the signs of the walks ending there. For an event with Σ ε² > 0, the chance of the record v is p(v) = ε(v)² / Σ_u ε(u)². | rule, stipulated |
| S4 | **The book of heat.** With n(v) the number of walks of the event ending at v, the entropy of the record v is S(v) = log n(v). | rule, stipulated |
| S5 | **The join.** The entropy of the world, given the event, is the mean H = Σ_v p(v)·S(v), taken over the records of non-zero chance. | identification |
| S6 | **The arrow.** The direction of time is the direction in which a world runs free. | identification |

## 2. What is proved from them

**T-1 (second law).** Let an event have Σ ε² > 0 and let it run free for one step. Then H does not decrease. It is unchanged exactly when every site that carries chance has all its walks on one rail; otherwise it increases.

*Proof.* Fix a site x with signed sums ε_R, ε_L and counts n_R, n_L on its two rails. After a free step every walk at x continues once to (x+1,R) and once to (x−1,L), and these two vertices receive walks from no other site. So both have the count n_R + n_L. Their signed sums are ε_R + ε_L and ε_R − ε_L (only the step from rail L to rail L changes a sign), so their weights add to 2(ε_R² + ε_L²). The total weight therefore doubles, and the two children of x together have chance p(x,R) + p(x,L). Hence
H(after) = Σ_x (p(x,R) + p(x,L))·log(n_R + n_L) ≥ Σ_x p(x,R)·log n_R + p(x,L)·log n_L = H(before),
because n_R + n_L ≥ n_R and ≥ n_L. Equality at x needs n_L = 0 if p(x,R) > 0 and n_R = 0 if p(x,L) > 0. ∎

**T-2 (additivity).** For the product of two events, n and ε² multiply over pairs of end vertices, so p is the product distribution and H is the sum of the two entropies. ∎

**T-3 (a mask can lower H).** On the ring of 3 sites there is an event of length 5 and a further mask {2} after which H falls from 0.462… to 0 (`function/result_instances_run1.json`, G4). ∎

**T-4 (bounds).** 0 ≤ H ≤ T·log 2 for an event of length T, since 1 ≤ n(v) ≤ 2^T; and H = 0 for the sharp start. ∎

| Statement | Status |
|---|---|
| T-1 to T-4 | PROVED above; T-1 also checked exactly on 45,218 events (all mask sequences on rings of 3, 4, 5 sites to lengths 5, 4, 3), no failure, with the equality case as stated in all 30,896 equality cases |
| On the line, T·log 2 − H(T) = 2.908 at T = 8, 7.381 at T = 32, 12.791 at T = 64 | COMPUTED (60-digit decimals); no statement is made about its growth |
| S1 to S6 | STIPULATED |

## 3. Where it is most likely to break (named in advance)

1. **The law is not about the two books at all.** T-1 holds with the count in the book of chance as well (p = n/Σn), and for any rule whose weight is conserved site by site. If the brand's one line ("a theorem that joins the two") is judged to claim a link special to the squared rule, the first commitment is empty: a KILL of the brand. The candidate claims only that the law holds for the squared rule, and says in the brand that it is not special to it.
2. **S4 and S5 are unobservable.** An inhabitant sees chances. If n(v) cannot be obtained from anything an inhabitant can do or know, the book of heat is a book nobody can read, and S4 to S6 are empty.
3. **H is not an entropy.** If H violates a property that any entropy must have and that the candidate's own identifications (S5) commit it to, the identification is refuted. Candidates: for a correlated event of a pair of worlds (not a product), is the entropy of the pair at most the sum of the entropies of the parts? Does H fall when records are merged (coarse-grained)? Neither was tested.
4. **S6 against reversibility.** The step is reversible on signed sums. If "running free backwards" can be defined inside the candidate, T-1 may hold in both directions or fail in one; either way S6 would need a reason the candidate does not have.
5. **T-1's equality case and the sharp start.** If some natural world (one that runs free from a sharp start) reaches a state where H stops growing for ever, the arrow stops. From a sharp start on a ring this was not examined beyond 80 steps.

## 4. Director's own attacks before release

| Attack | Result |
|---|---|
| KZ8(a): H along the line and rings of 16, 18 sites, T = 1 to 80 | HELD |
| KZ8(b): 132 random masked events on the ring of 16 sites, each run free for 12 steps | HELD (68 of the 200 draws had no walks or no weight and were not counted) |
| G1, G2: every event on rings of 3, 4, 5 sites to lengths 5, 4, 3, one free step, exact integer inequality | HELD, 45,218 events |
| Does T-1 need the squared rule? | It does not. Recorded as weak point 1 and in the brand. |
| Weak points 2 to 5 | NOT ATTACKED by the director |
