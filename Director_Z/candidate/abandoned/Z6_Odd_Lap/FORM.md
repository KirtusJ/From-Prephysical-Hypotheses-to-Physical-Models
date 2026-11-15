# Candidate Z6, "Odd Lap": form

**Label: STIPULATED CANDIDATE FOR DISPROOF.** Not a claim about the world, not an ontology; no gate of the program is passed by it. Kirtus Justus, Theoretical Physicist, Port Coquitlam, British Columbia, Canada; compiled with the assistance of Director Z (a Claude session). Governed by [the candidate process](../CANDIDATE_PROCESS.md).

Notation and cited statements are those of paper G10 as issued in edition Z31 (subsections "Four arc gains" and "Four arc gains on rings: the winding of the walks at one vertex"). Every numbered stipulation is separately breakable.

## 1. Stipulations

| # | Stipulation | Kind |
|---|---|---|
| O1 | **Space.** Histories are walks from (0,R) on the two-rail digraph of a ring of N sites with M = N/gcd(N,2) ≥ 8: a right step from either rail of x leads to (x+1,R), a left step to (x−1,L). | carrier |
| O2 | **Tallies.** Each arc carries a gain in a finite abelian group: a (R to R), b (R to L), c (L to R), d (L to L). With δ = ad/(bc), B = bc/a², β = B^M: δ has even order; β is not in ⟨δ⟩ and β² is an even power of δ. So there are exactly two classes of winding (s = 2) and k is even. | carrier |
| O3 | **Events.** Events are position product events: all walks of one length whose site after each step lies in a prescribed set. | instruments |
| O4 | **Shape of the rule.** The weight of an event is the sum, over end vertices, of one function (the same at every site) of the multiset of gains of the walks ending there; it is zero on no walks; and the weight of the continuation of an event by one free step is twice its weight. | rule |
| O5 | **Darkness.** The rule is non-negative, a single walk has weight one, and a vertex whose two class sums are both zero has weight zero. | rule |
| O6 | **Composition.** For two events of one length, the weight given to the product event by the same formula (each square taken on the product of the gains) is the product of the weights. | rule |
| O7 | **The odd lap.** The character χ of the rule has χ(β) = −1. Equivalently: with ε₀, ε₁ the signed sums of the two winding classes at a vertex, the weight is (ε₀ − ε₁)². | the choice |

## 2. What is proved from them, and from what

| Statement | From | Status |
|---|---|---|
| D1. Under O1 to O4 the weight at a vertex is α·(number of walks) + q(ε₀² + ε₁²) + c·ε₀ε₁, for real α, q, c. | G10 Theorem 5.61 (two classes, k even) | PROVED in G10, edition Z31 |
| D2. With O5, α = 0. | A vertex with class sums (0,0) and two walks exists (two walks of opposite sign in one class: G10 Proposition 5.60 with one group of two items). Its weight is 2α, and O5 says zero. | PROVED here, three lines |
| D3. With O5, the rule is c₊(ε₀+ε₁)² + c₋(ε₀−ε₁)² with c₊, c₋ ≥ 0 and c₊ + c₋ = 1. | D1, D2: q(ε₀²+ε₁²) + cε₀ε₁ = c₊(ε₀+ε₁)² + c₋(ε₀−ε₁)² with c₊ = (2q+c)/4, c₋ = (2q−c)/4; vertices with class sums (1,1) and (1,−1) exist (Proposition 5.60) and give 4c₊ ≥ 0, 4c₋ ≥ 0; a single walk gives c₊ + c₋ = 1. | PROVED here |
| D4. With O6, (c₊, c₋) is (1,0) or (0,1). | Take S₁ = S₂ with class sums (1,1) at one vertex: the product formula gives 16c₊, the product of the weights 16c₊². With (1,−1): c₋ ∈ {0,1}. | PROVED here |
| D5. With O7 the rule is (ε₀ − ε₁)², and it satisfies O4, O5, O6. | G10 Theorem 5.51(ii) (every such square is consistent on every event); non-negativity and multiplicativity are immediate. | PROVED |
| D6. The value χ(β) is not a convention: β is the quotient of the gains of two closed walks from (0,R), "left, right" M times and "right" 2M times, and such a quotient is unchanged by switching. | definition of β; the two walks are closed | PROVED here |
| D7. Odd lap and even lap give equal weights to every position product event of length at most M, and the fork separates them at length M + 1. | G10 (subsection "What position masks read"); recomputed in `function/` | PROVED in G10; COMPUTED here for five rings |

So the stipulations leave exactly one rule. Nothing in O1 to O6 chooses between odd and even; O7 is a bare choice and is labelled as one.

## 3. Where it is most likely to break (named in advance)

1. **O7 against O6 on a pair.** Two odd-lap worlds side by side: a joint lap of both multiplies the pair's gain by (−1)(−1) = +1. If "a closed world returns with a sign" is read as a law for every closed system, the composite breaks it. FORM states O7 for the single ring only. An attacker who shows that O6 forces O7 on the product carrier, or that the candidate's own brand sentence needs it there, has a KILL.
2. **O5 as a hidden assumption of the conclusion.** If "a vertex with zero class sums is dark" can be shown to be equivalent, under O1 to O4, to "the rule is a combination of squares", the candidate assumes what it says it derives (the kill that ended Z1). The candidate claims less: it says O5 removes the count and labels that as stipulated. Whether that label is honest is attackable.
3. **O2's two classes.** If, for every choice of gains allowed by O2 on a ring with M ≥ 8, some further symmetry identifies χ(β) = −1 with χ(β) = +1 (as phase symmetries did for Z2's open quantity), O7 says nothing. D6 and D7 are the defence; a symmetry that changes β while fixing every event weight is a KILL.
4. **The parity claim.** "The world can tell whether M is even or odd" rests on the fork. If inhabitants cannot prepare the fork without already knowing M, the claim is empty (a WOUND to the brand, a KILL if the brand's second commitment is judged essential).
5. **Empirical reach.** The candidate maps its ring to no laboratory system. If its stipulations nevertheless imply a statement about measured rings (for example through O6 applied to subsystems), the integer rotational spectra of molecules would kill it at once.

## 4. Director's own attacks before release

| Attack | Result |
|---|---|
| Consistency of (ε₀−ε₁)² on 208 random position product events, rings of 4 and 12 sites | HELD, 0 failures (`../SPRINT_2026-11-15/result_kill_run1.json`) |
| Multiplicativity on 32 pairs | HELD |
| Fork, even M (4, 12, 20 sites) and odd M (6, 10, 14, 7, 9, 11 sites) | HELD; the first run could not reach odd M with its carrier and a follow-up with predicate fixed first was run |
| Is χ(β) a convention? | HELD by D6 |
| Does the brand need O7 on composites? | NOT DECIDED; listed as weak point 1 |
