# Director B | Bell Memory, Sequential Testing and Reciprocal QA Adversarial Audit

**Research program:** From Prephysical Hypotheses to Physical Models  
**Research direction:** Kirtus Justus  
**Reviewing participant:** LLM Director B  
**Date:** 11 November 2026, B.C. Pacific Time  
**Parent Unary PCP:** Initial External Grounding, OPEN  
**Disposition:** Scoped continuation only. No parent transition, formal integration or ontology selection.

## 1. Evidence order and independent source intake

The sources were read in this order: the newly uploaded Director C report and its source ZIP; its release manifest, native checker, mathematics code and local review records; the previous Director B parity/time/QA ZIP and technical disposition (internal research provenance/self-citation); the updated PCP 1.0 packet nested in the B archive; independent fresh mathematical analysis; published CHSH and sequential-testing antecedents.

- Director C new archive: full ZIP CRC PASS; **13/13** listed payloads match SHA-256 and exact size. Its native release validator returns PASS. Its independent Bell checker reports the expected fixed-horizon figures.
- Previous Director B archive: full ZIP CRC PASS; exact SHA-256 recorded in SOURCE_RECEIPTS.json. Its source manifest and previous calculations remain internal research provenance, not external evidence.
- Frozen baseline nested in B: SHA-256 `fde41b3789930b0848cffd80b0ced68b052645808c393525266b1457d6d669cf`, ZIP CRC PASS, unchanged. No renewed claim of whole proof certification follows.
- Updated PCP packet nested in B: SHA-256 `30ea3cdb839ec0e09038a26268a116e4cdb90fb857035d27080193feb9f37a24`, ZIP CRC PASS. Governing relevant texts: Core R13, Mathematics R5, Science R11, Statistics White R2, Quality Assurance Lime R3. The packet's own 58-payload validation was previously run; this audit inspected the actual selected module specifications, not merely their labels.

**Evidence classes:** Original finite model definitions (input); source manifest verification (byte-level); execution of supplied code (same-input reproduction); separately written exact arithmetic and proofs (fresh internal checking); published source (mathematical precedent, not endorsement); physical replication (none).

## 2. Director C claims retained

Write the conditional single-round quantum CHSH win bound as

\[q_Q=\frac{2+\sqrt2}{4}=\cos^2(\pi/8)\approx0.853553390593274.\]

Let `W_i` be the win indicator in each *complete* trial, `S_n=ΣW_i`, and assume the settings are independently, uniformly and freshly chosen, inaccessible to the other party before its own output. Assume the conditional within-round behavior remains an ordinary quantum CHSH strategy. Then

\[\Pr(W_i=1\mid\mathcal F_{i-1})\le q_Q.\]

Director C correctly removes the need for iid output trials from the quantum null. The all-wins event is bounded by `q_Q^n`, giving 18-round size ≈0.057829901576 and 19-round size ≈0.049360908568. The ideal PR alternative wins every round; 19 is minimal among fixed-horizon randomized complete-transcript tests at size 5%, power 95%, using the least-favorable isotropic quantum endpoint.

For the specifically defined noisy isotropic `v=0.99` PR-family alternative, `p=(1+v)/2=199/200`, the 19-round all-win test has power `p^19≈0.90915626` and fails the 95% target. Director C's optimal randomized 28-round count test has power ≈0.950814579 at size 0.05. At 27 rounds the optimum is ≈0.939812381. Among deterministic *upper-threshold tests using win count only*, the first qualifying round count is 31. These figures were reproduced from fresh exact rational enclosures of √2, rather than importing C's mathematical verifier. They are not physical apparatus statements.

### Statistical scope

These theorems condition on a classical account of complete input/output records, valid sampling and quantum-versus-PR model classes, not on prephysical emergent dynamics. Average correlation constraints, setting bias, postselection or an observed win rate by themselves do not establish the full conditional assumptions.

## 3. New theorem: memory-robust fixed-horizon size **and** power

Director C's conditional quantum null is correct. A symmetric extension also removes iid *alternative* records. Suppose in two respective model classes, for all rounds and histories:

\[H_Q:\quad \theta_i:=\Pr(W_i=1\mid\mathcal F_{i-1})\le q_Q,\qquad
H_A:\quad \theta_i\ge p=199/200.\]

The two inequalities are separate model contracts. The alternative lower bound is not inferred from a global average.

**Proof:** Use independent uniforms `U_i` to sample `W_i=1{U_i≤θ_i(history)}`. Coupling to `B_i(q)=1{U_i≤q}` and `B_i(p)=1{U_i≤p}` proves pathwise domination by `B_i(q)` under the null and domination of `B_i(p)` under the alternative. Hence for every nondecreasing function `h:{0,...,n}→[0,1]`:

\[\mathbb E_Qh(S_n)\le\mathbb E h(\mathrm{Bin}(n,q_Q)),\qquad
\mathbb E_Ah(S_n)\ge\mathbb E h(\mathrm{Bin}(n,p)).\]

This covers a randomized upper-threshold rule with an *independent* final randomizer. Accordingly, C's 28-round rule retains ≤5% size and ≥95% power against these two **memory-allowing conditional classes**. The iid endpoint null and alternative are included, so C's 27-round Neyman–Pearson impossibility remains a lower bound for the enlarged classes. **This is not a claim that generic noisy PR behavior fulfills the conditional alternative inequality.**

## 4. New positive control: deterministic implementation of the randomized decision using seven independently fair bits

For `n=28`, reject for 28 wins and reject for 27 wins with probability `γ`. With `p=199/200` and `q=q_Q`, the necessary and sufficient gamma interval within this count-rule family is

\[\frac{0.95-p^{28}}{28p^{27}(1-p)}\le\gamma\le\frac{0.05-q^{28}}{28q^{27}(1-q)}.\]

The endpoints are respectively ≈0.661987160123256 and 0.668648815209585. Choose the dyadic fraction

\[\boxed{\gamma=85/128=0.6640625}.\]

Use seven independent fair bits drawn *after* all 28 outputs; interpret them as an integer from 0 through 127 and reject on values 0 through 84 when exactly 27 wins. The resulting quantum size is ≈0.049738464931 and conditional-alternative power is ≥0.950253770098. Independent rational calculations using a certified enclosure of √2 prove the inequalities. Exhausting dyadic fractions of denominator `2^k` for `k≤6` proves seven fixed fair bits is the least within this **specific implementation family**, not minimum entropy for arbitrary randomized tests. The seed is an additional operational resource; it is not generated by the speculative ontology.

## 5. New negative control: indefinite repetition of the fixed 19-round test invalidates size

Under the admissible iid quantum endpoint with winning probability `q_Q`, disjoint 19-round blocks independently have all-wins probability `r=q_Q^19≈0.049360908568`. Repeating the one-block decision on every disjoint block without a multiple-testing correction yields

\[\Pr_Q(\text{at least one false rejection in m blocks})=1-(1-r)^m.\]

This is ≈0.397223 for `m=10`, ≈0.636660 for `m=20`, and ≈0.993668 for `m=100`; it converges to one. The fixed-horizon theorem was never authorization for repeated window scanning. This is a valid adverse procedure control, not a refutation of Director B's original 19-round theorem.

## 6. Anytime-valid positive alternative

Fix `p=199/200>q_Q` *before* observing the sequence and define

\[M_n=\left(\frac p{q_Q}\right)^{S_n}
\left(\frac{1-p}{1-q_Q}\right)^{n-S_n},\quad M_0=1.\]

Under `H_Q`, each factor has conditional expectation at most one: the expectation is affine increasing in `θ_i≤q_Q`, and equals one at `θ_i=q_Q`. Thus `(M_n)` is a nonnegative supermartingale. Ville's inequality proves

\[\boxed{\Pr_Q(\sup_{n\ge0}M_n\ge20)\le0.05}.\]

This supports prespecified sequential monitoring and arbitrary data-dependent stopping **without false-rejection inflation** under the quantum conditional bound. It does not inherit C's 28-round power certificate. Under iid `p` alternatives, `log M_n/n→D_KL(Bern(p)||Bern(q_Q))≈0.1356818537434>0`, so threshold crossing eventually occurs with probability one; this is not a finite-horizon guarantee. Sequential test supermartingales and Ville validity are established statistical methods.

## 7. Reciprocal QA of Director C's **current** validator

The current C validator's source was inspected before mutation. In fresh, disposable extracted copies, the following was directly observed:

| Mutation/control, self-rehashed where indicated | Validator result |
|---|---|
| Original release | PASS |
| G5 status explicitly FAILED, rehashed | REJECT |
| G5 success-looking status but basis expressly states no checking happened, rehashed | PASS |
| C-CHSH-005 prose claim changed to "one round suffices", computed reference left correct, rehashed | PASS |
| Independently recomputed numerical reference changed from 28 to 1, rehashed | REJECT |

**Positive assurance controls:** C has improved from earlier validators by checking explicit `G5.status`, excluding an explicit `FAILED` marker, and recomputing numerical references without rewriting their saved input. It detects numeric corruption. **Negative assurance controls:** it cannot authenticate that actual checking happened or bind every prose finding to the mathematical result. It explicitly advertises a narrow file-integrity/math/source-ID contract, so these limits do not constitute a refutation of that advertised contract. A `PASS` is not evidence of formal PCP gate completion or authenticated provenance. Previously documented analogous B validator limitations remain attributable to B.

A stronger validator would require an explicit, type-checked claim-to-computation assertion map and known-invalid mutation controls, plus independent source authentication where the higher claim requires it. Even then, successful software checks cannot prove that real-world evidence was obtained.

## 8. Source provenance and review disposition

C's inherited crosswalk contains 1,555 stable IDs, all of which appear in the preceding B 1,565-entry source register. B has ten additional `DB-PTQA` identifiers not present in C's inherited layer. C's 12 new `C-CHSH` findings are distinct from all prior B identifiers. The current source-preserved union is therefore 1,577 attributed entries before this audit. This is a set-of-identifiers result, not proof of byte identity for every original upstream finding (C's index has metadata rather than the full source-row objects).

Eight new DB-CHSHM scoped findings are released in a separate append-only register. Original source records remain unchanged. Two original ZIPs and source receipts are packaged, with the frozen baseline and updated PCP embedded in the original B archive and identified by exact SHA-256.

**Local review status:** Three locally completed FOCUSED assessments (mathematical memory/optimality, sequential design, reciprocal QA) have documented grounding, faithful-case, adverse checking and release. No parent registry token, formal child closure or admission is claimed; parent Initial External Grounding remains OPEN.

**Scientific hold:** TO-0 remains withdrawn as a candidate physical ontology; mathematical contextuality comparisons stay valid. No derived physical time, Hamiltonian dynamics, quantum-selection rule, measurement apparatus, or calibrated Bell data appear. The Wilson–Dirac `M_s` cross-boundary dependency, exact eight-output quantum-copying optimum, and comparative effectiveness of PCP remain unresolved from earlier records. None is silently resolved by this finite Bell/statistical audit.

## 9. External precedent, not external certification

- IBM Quantum Learning, CHSH game and quantum winning bound: https://qiskit.qotlabs.org/learning/courses/basics-of-quantum-information/entanglement-in-action/chsh-game
- Knill, Zhang and Bierhorst (2020), NIST / *Physical Review Research*, adaptive Bell-test supermartingales: https://www.nist.gov/publications/quantum-randomness-probability-estimation-classical-side-information-0
- Sequential model confidence sets and Ville's inequality: https://doi.org/10.1093/jrsssb/qkag066
- Loophole-free Bell testing with memory-robust p-values, *Nature* (2023): https://www.nature.com/articles/s41586-023-05885-0

Each establishes a relevant general mathematical or experimental-method precedent. None independently referees the finite counts or certifies physical assumptions in the current research program.

**Director B closing disposition:** Retain C's exact finite results; strengthen their conditional power validity to memory-dependent alternatives; add a seven-bit fixed randomizer, an optional-stopping negative control and an anytime-valid positive procedure; document reciprocal validator strengths and limits. No foundational or parent-stage advancement.
