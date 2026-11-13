# Director B | Parity, Held-Out Bell Testing, and Reciprocal Quality Assurance

**Research program:** From Prephysical Hypotheses to Physical Models  
**Research direction:** Kirtus Justus  
**Reviewing participant:** LLM Director B  
**Date:** 11 November 2026, B.C. Pacific Time  
**Parent Unary PCP:** Initial External Grounding, OPEN  
**Scope:** A bounded local continuation, not a parent phase transition or independent peer review.

## I. Source, governance, and evidence calibration

I inspected Director C's latest post-withdrawal archive and its accompanying pasted submission; I additionally reexamined my preceding Director B TO-0 Bell/QA release, the supplied PCP 1.0 packet's governing Markdown and checker, and the original local-review reports. The original current C ZIP has 16 manifest-listed payloads. Independent byte-size and SHA-256 recomputation matches all 16. Its normal and deep native validators pass. The prior B ZIP has 17 manifest-listed payloads, with the source archive intact. The supplied PCP verifier accepts all 58 release payloads. The outer original files remain untouched.

**Evidence classes:** Matching a self-issued hash manifest confirms content consistency relative to that manifest, not authenticated origin. Reexecuting code verifies its behavior on the stipulated inputs, not all consequences of a proof. Independently rewriting a calculation improves assurance about a scoped finite statement, but does not provide independent physical replication. Claims of PCP gate performance remain human and procedural evidence questions, not cryptographic hash equalities.

Applicable modules: Core R13, Mathematics R5, Science R11, Statistics White R2, QA Lime R3. In this report, three bounded FOCUSED local examinations contain G1 grounding, G5 checking and G6 scoped release. They are documented locally; no authoritative Parent State Token or formal parent admission is asserted.

### Source accounting

The previous B release has 1,531 inherited identifiers and ten new `DB-TO0QA` findings. The current C release contains a 1,531-ID inherited crosswalk and 14 distinct `C-BPW` findings. The two 1,531-ID sets coincide, but the index rows package different provenance layers, so their JSON/hash fields should not automatically be described as byte-identical. The union is 1,531 + 10 + 14 = **1,555** attributable source/audit entries. This continuation appends ten distinct `DB-PTQA` scoped findings, giving **1,565** entries. These are not independently proved mathematical propositions or completed PCP reviews. File-specific historical provenance is preserved rather than replaced.

## II. Director C parity and locality results

For any Boolean truth table `g=(g00,g01,g10,g11)` on two binary settings, write uniquely

\[
 g(x,y)=c\oplus\alpha x\oplus\beta y\oplus dxy,\quad
 d=g_{00}\oplus g_{01}\oplus g_{10}\oplus g_{11}.
\]

Define a fair-marginal perfect-parity conditional distribution by

\[
 P_g(a,b\mid x,y)=\tfrac12\mathbf1\{a\oplus b=g(x,y)\}.
\]

For a deterministic Bell-local strategy, the same four bits \(A_0,A_1,B_0,B_1\) must satisfy all four equations. XOR of those equations forces \(d=0\). Conversely, if \(d=0\), the shared independent fair bit \(U\) realizes \(a=U\oplus\alpha x\) and \(b=U\oplus\beta y\oplus c\). Thus exactly eight of the 16 fair-marginal perfect-parity tables are Bell-local, and eight are relabeled PR-type tables. The eight *local fair-marginal parity tables* are different mathematical objects from the 16 local deterministic vertices of the full no-signalling polytope.

For fixed standard \(S=E_{00}+E_{01}+E_{10}-E_{11}\), all 16 parity rules have histogram `{-4:1,-2:4,0:6,2:4,4:1}`. All six `S=0` cases have \(d=1\), and each saturates an appropriately relabeled CHSH facet at absolute value four. Thus using one fixed orientation misses six of eight PR variants in this narrow deterministic family. It does *not* imply a 75% empirical false-negative rate.

The unrestricted sampler \(a=U,b=U\oplus g(x,y)\) consumes one fair bit for every perfect-parity table but accesses both inputs. Under Bell-local separation, the eight PR variants require an additional cross-input resource; a one-bit one-way message \(x\) from Alice to Bob is sufficient with shared \(U\), whereas no shared-randomness-only Bell-local simulation can realize exact nonaffine parity. This establishes two distinct model classes, not a physical communication experiment.

**External precedent:** Peter Bierhorst, *Geometric Decompositions of Bell Polytopes with Practical Applications*, NIST (2016), https://www.nist.gov/publications/geometric-decompositions-bell-polytopes-practical-applications; published treatments of CHSH games such as IBM Quantum Learning, https://quantum.cloud.ibm.com/learning/en/courses/basics-of-quantum-information/entanglement-in-action/chsh-game.

## III. New finite result: learning an unknown ideal PR orientation

The earlier Director B 19-round theorem assumed the CHSH orientation was specified in advance. If the source is promised to be one of the eight *fixed ideal PR parity tables*, but the truth table is unknown, selecting a game by scanning the same data is a distinct inferential task.

Assume iid uniformly sampled input pairs (four contexts), a constant unknown ideal PR rule, independent fair outcome bits within each context with perfectly known parity, and no observation error. After observing \(n\ge1\) training settings, let \(K\) be the number of distinct contexts observed. Because the rule has odd truth-table XOR, the number of compatible PR rules is \(2^{\max(3-K,0)}\). Output bits supply no additional information about the rule beyond observed parity bits. Randomly select uniformly among the surviving rules.

Its conditional error is \(3/4\) for \(K=1\), \(1/2\) for \(K=2\), and zero for \(K\ge3\). Uniform sampling yields

\[
 \Pr(K=1)=4/4^n,\quad
 \Pr(K=2)=6(2^n-2)/4^n.
\]

Therefore the exact minimax error is

\[
 \boxed{e_n=3(2^n-1)/4^n,\qquad n\ge1.}
\]

A uniform prior over the eight transitive PR alternatives gives this Bayes lower bound to every classifier; uniform randomized selection among compatible alternatives attains the same error for each true rule, establishing minimaxity. I independently enumerated all \(4^5\) and \(4^6\) input transcripts for each of the eight models:

| Training rounds | Minimax misidentification | Correct identification |
|---:|---:|---:|
| 5 | \(93/1024=9.08203125\%\) | \(931/1024\) |
| 6 | \(189/4096=4.6142578125\%\) | \(3907/4096\) |

Six is the sharp minimum for at least 95% success *under this eight-hypothesis, uniform-setting promise*. If only one or two contexts have nonzero sampling probability, there remain distinct PR rules producing exactly the same available records no matter how many repetitions are taken. The uniform, independently generated settings are a genuine prerequisite, not a cosmetic assumption.

## IV. New held-out Bell discrimination guarantees

Let \(q_Q=\cos^2(\pi/8)=(2+\sqrt2)/4\) be the optimal conventional-quantum winning probability in any fixed, relabeled CHSH game under independently uniform inputs and no within-round communication. For iid quantum rounds, \(\Pr(\text{all }n\text{ win})\le q_Q^n\). These statements are about a stipulated quantum null, not arbitrary conditional probability tables.

**Two-stage 25-round test (unknown ideal PR variant).** Use six training rounds to select one of the eight candidate PR rules uniformly among those consistent with the training parity data. Use 19 fresh, independent test rounds with uniform inputs. Reject the quantum null only if all 19 holdout parities match the chosen PR orientation. Since selection and testing are separated, the null size is bounded by \(q_Q^{19}\approx0.049360908568<0.05\). For a fixed ideal PR source, a correctly selected orientation wins every held-out round, so power is at least \(3907/4096\approx95.3857421875\%\). Since any wrong surviving PR rule differs on exactly two unobserved contexts, the exact ideal-PR power in the specified split protocol is

\[
 \boxed{\frac{3907}{4096}+\frac{189}{4096\,2^{19}}
 =\frac{2048393405}{2147483648}\approx0.953857509885.}
\]

This is a sufficient conditional test, not the global minimum number of samples needed to distinguish unknown PR behavior from the quantum set. Within this particular uniform-prior orientation-learner plus fixed-orientation all-win holdout design, five training rounds cannot reach the 95% power target, and 18 holdout all-win rounds cannot achieve both the 5% size and 95% power targets even allowing a randomized all-win rejection. A more powerful experiment using the whole transcript might do better; it has not been optimized here.

**One-stage orientation-free control.** Reject if the complete \(n\)-round transcript is perfectly consistent with at least one of the eight PR truth tables. The event is the union of eight fixed-orientation all-win events, each with quantum probability at most \(q_Q^n\). Hence a Bonferroni bound gives

\[
 \Pr_Q(\mathrm{reject})\le8q_Q^n.
\]

At \(n=33\), the upper bound is \(0.043023210735<0.05\) with 100% power against every ideal fixed PR rule. At \(n=32\), the **bound** is \(0.0504048267>0.05\); this does not establish that the real rejection probability exceeds 5% or that 33 is a sharp sample minimum. In particular, the previous 19-round fixed-orientation guarantee must not be transferred to a posthoc eight-orientation scan without a new calculation.

Both tests assume complete correct records, one fixed ideal PR alternative, uniform independent and unpredictable setting draws, and the stated quantum null. No real physical apparatus or admissible superquantum device has been established. No control over drift, selection errors, imperfect settings or detector detection loopholes is supplied.

## V. Known versus unknown time-scale

Director C's continuous-time Markov result is correct under its assumptions: with

\[ G_\lambda=\lambda\begin{pmatrix}-1&1\\1&-1\end{pmatrix},\quad
 A_\lambda(t)=\frac{1+e^{-2\lambda t}}2,\]

all \(\lambda>0\) share the same stationary distribution \((1/2,1/2)\). The static law does not identify \(\lambda\). If \(t>0\) is independently known and \(1/2<A<1\), the exact model permits \(\lambda=-\log(2A-1)/(2t)\). Without a warranted lag, only the product \(\lambda t\) is identified. Neither the Markov parameter nor continuity is an emergent physical clock. This is conventional probability theory; it is not a new physical result.

## VI. Reciprocal QA findings against the latest C validator

I ran fresh disposable mutant controls against the actual current C release. The following results were reproduced:

| Test | Current C native validator |
|---|---|
| Valid original archive | PASS |
| Inject explicit G5 `FAILED` without changing manifest | Reject |
| Inject `FAILED` and self-rehash changed record | **PASS** |
| Replace saved numeric result `affine_local_models=8` by `0` and self-rehash | **PASS on first execution** |
| Recheck same extracted package immediately afterward | **FAIL** |

The last anomaly has a precise code-level explanation. The current validator checks the manifest first, then calls `verify_independent_math.py`. That routine unconditionally **rewrites** `verification/INDEPENDENT_C_RESULTS.json` with recomputed values. A self-rehashed, deliberately corrupted reference file is therefore silently repaired during a validation run which nonetheless prints `RELEASE_VALIDATION_PASS`. Because the manifest remains pinned to the corrupted bytes, a second run rejects the now-correct file. This is a new *validator orchestration and saved-reference comparison defect*, not a mathematical failure of the original C results.

I also confirmed that the genuine unmodified reference bytes are exactly regenerated by the independent mathematics script. Thus the mathematical data in the actual supplied release survive this specific control. A safe validator would recompute to a **separate temporary output**, compare against the archived result, and reverify release hashes after performing any checking code with side effects.

The same G5 semantic-acceptance limitation was previously shown in B's own checker, so the correct finding is symmetrical. Neither tool describes itself as a complete substantive PCP-gate oracle. The mutation proves a definite coverage gap, not that the real review failed. A self-issued manifest is not an externally authenticated provenance or gate-completion certificate.

## VII. Bounded child work and phase boundaries

Three local FOCUSED assessments were completed against declared, limited targets: (i) parity/communication resources and all orientations; (ii) held-out orientation learning and exact statistical controls; (iii) reciprocal validator false acceptance and reference mutation. Each records grounding, adversarial checking and scoped release corresponding to Core G1/G5/G6. These local examinations are not claimed as formally registered or integrated child Councils because no current authoritative Parent State Token or integration act was supplied. Parent Initial External Grounding remains OPEN.

## VIII. Ontology, baseline, and PCP dispositions

TO-0's candidacy as a total physical ontology remains withdrawn, in agreement with C's own revised decision. Its finite contextual probability tables remain useful mathematical comparators, particularly as **nonselection evidence**, not positive physical identification. The quantum model is imported. The PR model and Bell-local model differ in causal resource requirements, but the shared context notation does not select which model describes nature. No successor ontology is necessary or warranted.

No changes are made to the frozen November 10 baseline. The unresolved Wilson–Dirac \(M_s\) dependency before (B9), exact eight-output quantum-copying optimum, foundational-to-operational bridge, physical clock, selective records, and comparative effectiveness of PCP remain open at prior audited depths. This current handoff does not recertify the old 85-component proof corpus or claim fresh physical data.

## IX. Release checks and source attribution

The release contains the exact user-supplied new C ZIP, previous B ZIP and updated PCP packet, together with this report, an independent standard-library parity checker, saved exact results, a disposable QA mutation verifier, both old and new attributed registers, ten new scoped findings and six numerical/QA watch entries. The current inherited union is 1,555 distinct IDs; the appended view is 1,565 distinct IDs. No historical record is overwritten or semantically deduplicated. CRC and manifest hashes are checked. The release validator itself is listed and hashed; the reference outputs are checked in a temporary copy **without overwriting saved results**.

**Current disposition:** This continuation strengthens operational Bell-model testing under a precisely stated unknown-orientation contract, and independently identifies a reproducibility defect in C's newest saved-output validation. Neither statement selects an ontology, demonstrates physical measurements or advances the parent PCP phase.
