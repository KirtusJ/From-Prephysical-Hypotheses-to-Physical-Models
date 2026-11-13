# Director C | Unknown-Orientation Bell and Reciprocal Assurance Audit

**Research program:** From Prephysical Hypotheses to Physical Models  
**Research direction:** Kirtus Justus  
**Reviewing participant:** LLM Director C  
**Date:** 11 November 2026, B.C. Pacific Time  
**Parent Unary PCP:** Initial External Grounding, OPEN  
**PCP release:** PCP 1.0, Core R13; Mathematics R5, Science R11, Statistics White R2, Quality Assurance Lime R3 as applicable.

## 1. Commission, source hierarchy, and limits

This is a scoped continuation examining Director B's new `Parity, Time and QA` archive and pasted statement against the preceding Director C CHSH/QA release and the governing updated PCP specifications. The frozen November 10 research baseline remains the unchanged reference. Nothing here changes parent phase, claims a registered child Council, selects an ontology, or certifies physics.

**Source-derived facts:** The newly supplied Director B archive passes ZIP CRC, 18/18 internally declared payload hashes/sizes, its native fast and deep validators, and its mathematical program. Its inherited register contains 1,555 rows and its new scoped findings ten rows. Director C's preceding CHSH/QA archive contains 12 distinct new findings not in B's 1,565-entry ledger; their IDs were checked. Hence the pre-audit union is 1,577 attributed entries, **not** distinct theorems. The 2026 PCP collection nested in B's source archive passes its 58-payload checker, and its original frozen baseline checker has previously passed 445 files and 85 component PDFs. All these are internal/recomputed integrity evidence, not authenticated historical provenance or physical replication.

**Independent mathematics:** The calculations in `verification/independent_math.py` were derived without importing A/B/C mathematical routines. Test assumptions and checks are repeated below.

## 2. Director B's six-round minimax orientation theorem: supported in scope

Let the four input contexts be indexed by `c in {0,1,2,3}`. Exactly eight four-bit PR parity words have XOR of all four entries equal to one. In an ideal fixed PR box, the parity observed on each input context is deterministic; the other output bit is a fair coin and provides no information about the PR orientation.

After observing `K` distinct contexts, there are `4` compatible PR orientations if `K=1`, `2` if `K=2`, and `1` if `K>=3`. Under a uniform prior and an ideal PR source, uniformly guessing among the consistent orientations is minimax by symmetry. For independent uniform context choices, the error for `n>=1` is

\[
 e_n=\tfrac34\Pr(K=1)+\tfrac12\Pr(K=2)
     =\boxed{\frac{3(2^n-1)}{4^n}}.
\]

At `n=5`, success is `931/1024=90.91796875%`. At `n=6`, it is `3907/4096=95.3857421875%`. Thus six is the minimum for 95% identification with **independent, uniformly sampled training contexts and this ideal-source model**. This is not a universal minimum over experimental designs.

### A new exact generalization to nonuniform settings

For any independently sampled context probabilities `p_0,...,p_3`, sum one, define

\[
 e_n(p)=\boxed{\frac12\sum_{i<j}(p_i+p_j)^n
                  -\frac34\sum_i p_i^n}.
\]

This follows from the same context-occupancy count, not by fitting a simulation. For `(3/10,3/10,3/10,1/10)` and six training rounds the exact error becomes `74487/1000000`, so orientation-learning success is **92.5513%**, not 95%.

All formulas were checked independently by enumerating every one of the `4^6` ordered context transcripts with exact rational weights.

## 3. Director B's 25-round test: correct under declared assumptions

After six independent uniform training rounds, predict an ideal fixed PR orientation using a consistent random-tie classifier. Reject the quantum CHSH null only if all 19 fresh independent uniform held-out trials satisfy the predicted parity. The quantum one-round CHSH bound is

\[
q_Q=\cos^2(\pi/8)=\frac{2+\sqrt2}{4}.
\]

Under a quantum null that continues to hold conditional on past transcripts, and **fresh unpredictable held-out settings**, iterated conditioning yields a size bound `q_Q^19 = 0.0493609085679...`. It is an **upper bound**, not automatically an attained maximal false-rejection probability for every narrower null contract.

Under an ideal fixed PR model, training succeeds with probability `3907/4096`. A mistaken consistent PR orientation differs on exactly two of the four contexts (the all-four complement cannot remain training-consistent), so it still passes all nineteen test contexts with probability `2^-19`. Thus

\[
\Pr_{\mathrm{PR}}(\mathrm{reject})
 = \frac{3907}{4096}+\frac{189}{4096\cdot2^{19}}
 =\frac{2048393405}{2147483648}
 \approx0.953857509885.
\]

The 33-round scan of all eight orientations satisfies the Bonferroni size bound `8q_Q^33=0.04302321073...` and power 1 against ideal fixed PR behavior. Neither procedure is declared globally sample-optimal.

## 4. New explicit adverse control: a biased setting distribution breaks the 25-round guarantee

Use contexts `(00,01,10,11)` with probabilities `(0.3,0.3,0.3,0.1)`. Let a completely local, deterministic device always output `a=b=0`. During training, if all three common contexts occur but the rare context does not, the observed first three parity values uniquely select the PR orientation `g(x,y)=xy`. A false rejection occurs when all nineteen test contexts also avoid the rare input.

The number of length-six onto context strings over the three common contexts is `3^6 - 3*2^6 + 3 = 540`; hence

\[
\Pr_{\mathrm{local}}(\mathrm{false\ reject}) \ge
540(3/10)^6(9/10)^{19}
 =\frac{20}{27}(9/10)^{25}
 =0.053177628717915\ldots>0.05.
\]

This is **not** a refutation of B's explicitly uniform-setting theorem. It is a constructive failure of an attempted extension to the displayed nonuniform experiment.

Under the same settings, the optimal six-round ideal-PR training success is `0.925513`. Every wrong PR orientation differs from the true orientation on at least two contexts of total probability at least `0.4`, so the probability it passes nineteen held-out trials is at most `(0.6)^19`. Hence the power of **this six-training-plus-all-win protocol** against an ideal fixed PR model is at most `0.92551753894...`, below 95%. Both size and power guarantees are lost under this biased input distribution.

### Even marginally uniform settings do not establish physical independence

A separate mathematical implementation can reproduce a PR table with settings that are uniformly distributed **marginally** but correlated with a hidden source variable `Λ=(x,y,U)`. Taking `a=U` and `b=U XOR xy` produces the PR parity table, with no within-round communication, because `Λ` already contains both settings. This violates **measurement independence**, not Bell locality under the ordinary free-setting contract. Consequently a uniform histogram or even unconditional iid settings is not a substitute for independence from causally relevant device information.

## 5. New positive control: 22 records suffice under a different calibration design

Choose three **distinct, predetermined** training contexts `(00,01,10)`, one each. Under any ideal fixed PR source, their observed parities uniquely determine the fourth by the odd-parity constraint, so orientation learning has success probability one after only three training records.

Then run nineteen fresh, independent, uniformly random CHSH test contexts, chosen unpredictably relative to the apparatus. The selected PR orientation is fixed after training. Conditional on the complete training transcript, the quantum CHSH bound yields size at most `q_Q^19 < 0.05`; the ideal fixed PR model wins all nineteen test rounds, giving power exactly one. Total: **22 records**.

This design is *not* an improvement within B's random-uniform-training contract. It changes that contract to deterministic-context calibration followed by randomized testing. The training data are not counted as Bell evidence. Conditional quantum validity requires correct isolation of test settings and no within-round signalling. Physical feasibility is wholly unverified.

Within the much narrower class of protocols demanding deterministic orientation identification first and using an unrandomized all-win held-out rejection rule, three distinct calibration contexts and nineteen test rounds are necessary. This is not a claim of global sample-size optimality.

## 6. Reciprocal QA and original-source status

Independently reexecuted the new B fast/deep validators, plus two disposable mutation controls against exact original releases. **Positive controls:** B's current validator passes correct data and uses isolated recomputation to detect a self-rehashed corrupted saved mathematical result without rewriting it. **Negative controls:** its manifest rejects a stale-hash injected `G5 FAILED`, but a matching self-rehashed failure record still passes because the validator does not certify gate success.

The older C checker has a distinct orchestration defect: a corrupted/self-rehashed mathematical saved result is overwritten by a verifier before final comparison, allowing the first run to report PASS and the second run to fail due to the now-stale manifest. That is an assurance defect, not an error in the correct original finite result.

The QA controls support **two distinct diagnoses**, neither to be exaggerated:

1. Self-declared successful gate metadata cannot authenticate substantive checking, even when a manifest is internally consistent.
2. The old C mathematical checker must not write into its archived result reference during validation. Independent recomputation should happen in an isolated work directory, comparison should be read-only, and release file hashes must be checked after execution.

Neither mutation proves that the actual original G5 work failed. Neither archive can authenticate its own claimed authorship. No result here demonstrates that PCP improves scientific correctness against a competent baseline.

## 7. Sources and external mathematical grounding

- **New supplied Director B archive:** `Director_B_Parity_Time_QA_PCP_Handoff_2026-11-11(1).zip` and accompanying pasted report, including its original verifier and 18-payload manifest. Original B source is embedded in the portable handoff, byte-for-byte.
- **Prior Director C CHSH/QA release:** original source archive and twelve attributable later C findings, included as a separately hashed ZIP.
- **PCP 1.0:** governing Core R13, Statistics White R2 and Quality Assurance Lime R3 read directly from the B-embedded verified source archive.
- **Quantum CHSH bound:** IBM Quantum Learning, CHSH game: https://quantum.cloud.ibm.com/learning/en/courses/basics-of-quantum-information/entanglement-in-action/chsh-game
- **Bell testing with memory / finite sample:** Elkouss & Wehner (2016), https://doi.org/10.1038/npjqi.2016.26
- **Measurement independence:** Stanford Encyclopedia of Philosophy, Bell's Theorem: https://plato.stanford.edu/entries/bell-theorem/
- **Freedom-of-choice loophole:** Cosmic Bell Test (2017), https://doi.org/10.1103/PhysRevLett.118.060401

These external works establish the relevant known methods and constraints, not historical novelty or independent external certification of the program-specific calculations.

## 8. Final scoped disposition and remaining obligations

**Retain as scoped mathematical results:** B's six-round minimax formula and 25/33 round conditional protocols, the 22-round designed-calibration positive control, the general nonuniform setting formula, and the biased-setting Bell-local counterexample. Keep the quantum-null size bound distinct from exact attainment and empirical application.

**Retain as QA findings:** both normal integrity successes and the two distinct semantic/oracle limitations. Do not conflate file-integrity `PASS` with Council gate success.

**Withdrawn:** TO-0's ontological candidacy remains withdrawn. No new ontology, foundational quantum mechanics, Hamiltonian time, cosmology or mathematical prize solution is asserted.

**Unresolved from frozen baseline:** Wilson–Dirac uniform `M_s` dependency preceding (B9), eight-output fixed copying optimum, physical observation/calibration bridge, and empirical comparison of PCP against competent conventional procedures.

**Parent Unary PCP:** Initial External Grounding, OPEN. The two locally bounded FOCUSED assessments attached to this audit document G1/G5/G6 work; they do not claim registered child authorization, Parent State Token receipt or parent admission.
