# Foundations of R — Physical model-selection gate (A11)

**Outcome in this checkpoint: HOLD / PHYSICAL R UNSELECTED.** This is a falsifiable specification for future candidate submissions, **not** a construction of a physical R theory. All external physical assumptions must carry independent, inspectable evidence.

## What must be supplied together

1. **Physical problem:** target system, source/preparation, physical task, units, controllable variables and experimentally or independently justified interpretation of the letter R. A generic mathematical covariance without this provenance is only a benchmark.
2. **Observable algebra:** define the one-particle Hilbert space \(\mathcal H_R\), CAR algebra \(\mathrm{CAR}(\mathcal H_R)\) (or a rigorously mapped alternative), representation/state and meaning of each mode. Explain and justify gauge invariance if used.
3. **Covariance and state:** give a concrete kernel/symbol/formula for \(C_R\); verify \(C_R^*=C_R\) and \(0\le C_R\le I\); identify its physical derivation and reference state on the **same** CAR algebra. Prohibit comparisons between silently different algebras.
4. **Localization:** prescribe regions \(\mathcal O\), algebra inclusions and local one-particle projections/embeddings, with isotony and compatibility of state restrictions. Differentiate finite intervals, half-lines and global volumes.
5. **Regulator:** specify \(\epsilon\), regularized \(C_{R,\epsilon}\), common-algebra identifications, cutoffs, renormalization (if any), and prove the resulting positive-contraction properties uniformly in needed domains.
6. **P5-prime:** state its quantifiers and topology. If asserting **full CAR-state norm** convergence, use CT14's necessary Hilbert–Schmidt condition and A03's half-line translation-invariant obstruction. Neither is a substitute for proving sufficiency. If asserting weaker local/relative-entropy convergence, do not silently replace it by state-norm convergence.
7. **Relative entropy:** identify faithful supports and the exact localized von Neumann algebra, the relative entropy notion and its domain; make each required finiteness/continuity claim separately.
8. **Modular/HSMI:** specify the relevant von Neumann algebras, cyclic separating vectors/faithfulness, modular groups, inclusions, half-sided invariance direction, and D3 conventions; test each hypothesis and limit.
9. **External validation:** provide a physical reason to select this candidate over alternatives and at least one discriminating prediction or observation, with independently inspectable sources. Algorithmic or Gaussian benchmark convenience is *not* physical selection.

## Fail-closed outcomes

- If items (1) or (9) are absent: `PHYSICAL_R=UNSELECTED` even if every CAR inequality checks out.
- If the covariance is not a bounded positive contraction on the claimed \(\mathcal H_R\): `STATE_INVALID`, all quasi-free state predictions `HOLD`.
- If localization/regulator data or a common observable algebra are missing: `R_EMBEDDING=OPEN`, `REGULATOR=OPEN`.
- If a nonzero translation-invariant difference is proposed with convergence in full half-line **state norm**, A03 + CT14 yield norm distance 2 at each nonidentical regulator point: reject that claimed mode of convergence. This does **not** automatically reject convergence of finite intervals or a different topology.
- If a benchmark Gaussian kernel \(h(p)=\frac14e^{-p^2}\) is submitted with no R-specific physical derivation: classify `MATHEMATICAL_BENCHMARK_ONLY`; never `PHYSICAL_R_SELECTED`.
- Never promote P5-prime, relative entropy, modular dynamics or D3/HSMI based only on the conditional benchmark certificates.

## Worked counterexample to false model selection

The scalar Gaussian family \(C=\frac12I,\ D=\frac12I+\frac14e^{-P^2}\) defines valid positive-contraction Fourier multipliers, has well-defined interval compressions and admits the studied Chernoff bounds. It **does not** identify the physical R source, task, localization prescription, regulator or empirical interpretation. Its algebraic success must therefore leave `PHYSICAL_R=UNSELECTED`.

## Governance rule

Each proposed candidate receives a unique source ID and independently archived hash. Do not reuse CT19/A08, CT20/A09 or CT21/A10 without a branch qualifier. Keep inherited v2.1, CT14–CT21 scientific statuses and source bytes immutable. Apply a new audit and distinct approvals before any master-claim promotion.
