# Director A | Fourth continuation and cross-director disposition

**Research program:** From Prephysical Hypotheses to Physical Models  
**Research direction:** Kirtus Justus, Port Coquitlam, British Columbia, Canada  
**AI research participant:** ChatGPT (GPT-6), Director A, internal mathematical assistance  
**Local date:** 12 November 2026, B.C. Pacific Time  
**Controlling state:** Initial External Grounding OPEN. Root review G1 OPEN. No total ontology selected. No baseline overwrite or phase advancement.

## 1. Intake and provenance boundary

Directly inspected the actual supplied ZIP files, not merely their transmitted dispositions:

- Director Z Session 2 outer ZIP, its revised G7 (18 pages), G8 (9 pages), disposition and cross-adjudication CSV, plus the extracted Z2 baseline with 791 files, 39 papers and 367 registry rows. Ran the Z2 baseline's own SHA-256 structural verifier (PASS).
- Director B3 ZIP, mathematical paper, verifier, exact filter data, cycle data and claim records. Ran the 23-payload integrity verifier, `verify_B3.py` and eight negative controls (PASS under their recorded scope).
- Director G3 ZIP, both mathematical papers, claim delta, the full raw trial data and three mathematical scripts. Ran 36-payload integrity verification, Veronese countermodel, projective instruments and cycle-family scripts in a disposable copy (PASS under their recorded scope).
- PCP Version 1.0 Enterprise Edition and its enclosed ACR Implementation packet. Ran their two offline source/release verifiers and retrieved exact clauses using the packet's own read-only lookup tool. This is **tool-assisted local consultation of supplied material**, not host-enforced PCP/ACR, not activation of a CLI integration for this ChatGPT session, and not proof of runtime behavioral conformity. The governing process is text-absorbed.

All submitted authors' LLM calculations are internal provenance. A/G/B agreement with Z is not independent external replication. A second source or a different model is not enough to confer referee status.

## 2. Scope and review disposition

The review retained the original target: an explanatory, emergent and empirically mapped quantum **and** classical mechanics, not merely mathematical Hilbert structure. No primitive, probability law, measurement protocol, composition, clock, reversible dynamics, classical Hamiltonian limit or calibrated empirical map was established as physically emergent. Constructed claims below are expressly conditional mathematical models.

## 3. New mathematical results (complete proofs in the paper)

### A4-01. Z2/G8 growth premise has a concrete witness

Let `Gamma=K4`, with `Z_n` gains: oriented edge `2 -> 3` has gain `+1`, its reverse `-1`, and all remaining edges carry identity. The associated 4n-cover graph is connected because the cycle `0 -> 2 -> 3 -> 0` has generator gain. It contains a triangle `0 -> 1 -> 2 -> 0` of net-zero gain and therefore an odd cycle. It is three-regular.

The Perron-Frobenius theorem for its symmetric, connected, aperiodic adjacency gives, for every vertex `v` and gain `g`,

`N_k(v,g) = 3^k/(4n) + O(rho_n^k)` for some `rho_n < 3`.

The fixed-graph finite event rays of G8, **after choosing a faithful complex character and the squared-amplitude pair rule**, are dense in `CP^3` for every `n >= 3`. This establishes a specific nonhomogeneous approximant family satisfying G8 Proposition 5.1's growth condition. It leaves unchanged every physical selection and interpretation obligation. No claim of mathematical priority over Perron-Frobenius/voltage-graph theory is made.

The new verification includes every `n=2..8` primitive-cover trial (7 rows), every `k=0..18` gain-count row for `n=3` (19 rows), including zeros, and exact wave-amplitude controls. For `n=3` the least gain/endpoint count at lengths `4`, `8`, `12` is respectively `2`, `348`, `36126`. A zero-gain negative control yields a disconnected cover, defeating the all-gain growth premise as expected.

### A4-02. The fixed-length kernels are not automatically a histories process

Write `omega = exp(2*pi*i/3)` and

```
A = [ 0, 1, 1, 1;
      1, 0, 1, 1;
      1, 1, 0, conj(omega);
      1, 1, omega, 0 ].
```

For all-extension of events from length `k` to `k+1`, represented vectors update as `v(Ext S)=A v(S)`. The two one-step events ending at vertices 1 and 2 have `D_1(S,T)=0`; their all-extensions have `D_2(Ext S,Ext T)=1+omega`, with squared modulus exactly `1`. A nonzero scalar per length cannot make these compatible. Total masses for lengths 0,1,2 are exactly `1,3,15`. After normalization by each length's total, the first single-step event has weight `1/3` but all its length-two extensions have weight `1/5`.

This **refutes** the proposition that G8's original `D_k` family automatically supplies a projectively consistent decoherence functional on the cylinder algebra of infinite walks under the natural extension. G8 does **not** assert such a process; it establishes fixed-length positivity and an event Hilbert-space quotient. The distinction is a sharpened open dynamics gate, not a refutation of the fixed-length result. A unitary modification or dilation would be a new, assumption-bearing model and remains unselected.

### A4-03. Endpoint-aware, additive, positive holonomy dependence

Define for each root `x` and finite walk event `S`, with the same `Z_3` gain, the nonnegative finite-additive function

`nu(S) = sum_{w in S, terminal(w)=x} (1 + Re(chi(gain(w))))`.

For closed paths switching changes gain only by conjugation, and for the abelian group this changes nothing. This rule is gauge invariant, gain sensitive, additive, and strongly positive under the diagonal intersection kernel. In `K4` the closed paths `0-1-2-0` and `0-2-3-0` receive respective weights `2` and `1/2`, although both have three steps. All higher interference terms vanish.

**Scope adjudication:** G8 Lemma 3.1 is valid as written for **one universal function of the gain alone** applied to both open and closed paths, without endpoint dependence. The broader unqualified slogan that a gauge-invariant additive walk measure can never depend on transport is false once an endpoint-return predicate is admitted. Endpoint awareness and a record criterion are imported; this counterexample does not establish their physical availability or provide a physical stochastic law.

### A4-04. Source-verified G7 proof erratum

In the proof of revised G7 Proposition 4.3, the horizontal-lift recurrence `alpha_{j+1}=alpha_j - arg <a_j,a_{j+1}>` implies `alpha_k=-arg B`, not `+arg B`. Hence the terminal lift is `exp(-i theta) a0`, `U a0=exp(-i theta)a0`, and the tangent conversion is `T=exp(+i theta) U|a0^perp`. The source instead gives both opposite signs. With both repaired,

`det_C T = exp(i(n+1)theta) = (B/|B|)^(n+1)`.

The theorem's displayed determinant formula survives; only the provided derivation requires a sign correction. The exact triangle with `B=(9+3i)/16` gives terminal lift phase `(3-i)/sqrt(10)` and tangent determinant `(4+3i)/5`. This is internal source scrutiny, not independent refereeing. A proposed erratum is included separately; the governing G7 manuscript is **not** silently modified.

### A4-05. Alternative mathematical completions persist

From the very same `K4` carrier one can choose an ordinary three-way classical Markov walk, with each length-`k` walk weighted by `3^{-k}`. Its cylinder weights are projectively consistent because each prefix has exactly three continuations. This classical completion ignores the gain. The endpoint-sensitive holonomy measure of A4-03 and G8's strongly positive pair measure supply distinct additional completions. Thus carrier-plus-gain data do not select a unique operational probability rule. This is a mathematical nonselection witness, not a claim that any of these models is physical classical Hamiltonian mechanics or quantum mechanics.

## 4. Reconciliation with the other directors

**Z2:** The root-stage and total-ontology dispositions stand. The original revised G7 and G8 have now been inspected rather than inferred from a short handoff. The G7 determinant law is retained with an explicit proof patch; the G8 positive-definite class-function theorem is retained under its exact universal, endpoint-blind pair-rule assumptions. The new `K4` witness advances G8's growth prerequisite from an unverified condition to a proved example, while the histories-consistency check identifies a separate missing process law.

**B3:** The local-filter example is mathematically coherent in the declared complex two-system Hilbert representation; its exact verifier and fault controls reran. Its closure/selectivity theorem does not obtain physical local filters or any non-Hilbert composition law from prephysical relations. The odd-cycle polar-complex structure is a valid linear-algebra control with an imported counting metric.

**G3:** The odd-degree Veronese convex hull exposes the gap between pure Born transition tables and full mixed-state tomography. The `k=3` two-mixture cubic-effect gap `1/8` and restricted projective-instrument equality reran. The minimal-tensor multipartite family is a legitimate alternative completion under its expressly limited effects and operations. Neither G3 nor the explicit G8 density example selects the physical experiment or resolves general composition.

**External grounding:** The published Hilbert-space-from-histories results require a decoherence functional, conventionally normalized on the event algebra; the separate literature on extensions makes consistency a substantive issue. The exact-Gromov-Hausdorff finite-homogeneity obstruction and quantum reconstruction postulates retain their previously checked scope. The cited external authors did not validate these new deductions.

## 5. Numerical and QA ledger

- Z2 baseline: `BASELINE_CHECK_PASS 791 files; 39 papers; 367 registry rows`, local structural scope.
- B3: `PASS_B3_PACKET 23 payloads; 14 claims; 12 open problems`; direct exact/numerical and eight adverse-controls pass.
- G3: `DIRECTOR_G_G3_LOCAL_PACKET_INTEGRITY_PASS 36 payloads`; reproduced 1,536 pure, 384 mixed, 768 adaptive-word and 16 cycle rows, with reported checks passing.
- Z2 G8 code: own pass predicates all pass, but numerical result JSON **is not byte-identical**. Exactly seven scalar values changed, with maximum absolute change `1.1102230246251565e-16`. All seven raw pairs remain in `Z2_G8_DIFF.json`; no rounding, merging or deletion. The results are not rigorous error enclosures.
- New A4: seven primitive-cover cases, 19 full exact-count rows, and exact symbolic identities; no exclusions. False-input controls include a trivial-gain disconnected covering and a nonzero inter-step cross-decoherence witness.
- QA: the first A4 comparison script unintentionally omitted the traversal call, falsely returning zero differences despite mismatched SHA-256 digests. The defect was detected in review and repaired. Three explicit known-outcome QA controls now pass, including an injected numeric mutation. This is a specific process improvement; it is not evidence of general checker reliability.

## 6. ACR lifecycle and calibration

**Commission:** Scope is a focused source-first review and mathematical continuation, with independent source/context checks where possible. **Source method:** PCP 1.0 Enterprise Edition and its ACR packet were checked locally. Relevant Core 5.2, 15.8, Mathematics 4 and 6, Science 5.4 and QA 5 were fetched by exact clause lookup. Actual delivery is text-absorbed with offline reference and verifier assistance; no host-enforced ACR workflow or installed PCP runtime is claimed.

**Review graph:** (1) source intake/identity; (2) formal mathematical statement and missing premise; (3) affirmative construction; (4) adversarial countercompletion; (5) proof/QA checker; (6) reconciliation; (7) ontology gate. These are staged acts by **one** AI participant, not independent sub-agents. No child review gains independent-evidence status by recursion; each carries source lineage and a halting condition tied to a specific theorem or defect.

**Adaptation tested:** The cross-length consistency challenge was added when the K4 positive growth example surfaced, rather than permitting the successful density calculation to increase ontological confidence. The checker itself was subjected to a control after its digest-consistency anomaly. This targeted reallocation improved detection of an actual error. No assertion that the optimization is universally superior is made.

## 7. Gate and task disposition

No ontology gate passes. The explicit density witness resolves a **mathematical existence sub-obligation only**; the probability selector remains open. The projective consistency obstruction is an identified failure of one naturally proposed path kernel, not a proof that alternative histories dynamics are impossible. The next highest-value scientific task is to formulate and test a bridge that jointly supports normalized, projectively consistent histories, empirically identifiable probabilities, nonimported composition, a defensible clock/dynamics notion, and classical Hamiltonian mechanics, while providing comparison models with the same finite relations.

The manuscript is unrefereed. Scientific authorship and project direction remain Kirtus Justus; the present assistant's contribution is labeled internal AI-assisted research. The source baseline is **not** modified or reissued.

**Final controlling disposition:** Initial External Grounding OPEN; G1 OPEN; total ontology NOT IDENTIFIED.
