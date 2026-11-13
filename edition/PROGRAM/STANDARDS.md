# From Prephysical Hypotheses to Physical Models: standards for statements, proofs, computation and citation

**Kirtus Justus**, Theoretical Physicist  
Port Coquitlam, British Columbia, Canada  
Baseline FPHPM-BASELINE-2026-11-13-Z9, 13 November 2026

## 1. Kinds of statement

| Kind | What it establishes |
|---|---|
| Mathematical premise | a state space, relation, probability rule, composition or observation menu chosen for a model; not established by a theorem that assumes it |
| Derived result | a statement following from displayed assumptions and a proof; its scope includes the dimension, topology, normalization and measurement access used |
| Computed instance | an exact finite enumeration, a rational certificate or a numerical evaluation; numerical precision is distinct from an error enclosure |
| Physical correspondence | a warranted relation between a mathematical experiment and physical preparations, controls and records, with units and uncertainty |

## 2. Statements and proof homes

Each labelled statement has one identifier in `THEOREM_REGISTRY.csv`, of the form *paper*-*part*-*sequence*, and one proof home: the part in which it is stated with its proof. A displayed copy elsewhere is a restatement and names its source. Cite a result by registry identifier, or by paper, part title and label. The registry column `legacy_locator` resolves citations written against the 10 November 2026 edition.

Registry status values:

| Status | Meaning |
|---|---|
| `PROOF_IN_MANUSCRIPT` | a proof paragraph follows the statement in its part; the proof has not been independently refereed |
| `PROOF_NOT_ADJACENT` | no proof paragraph lies between the statement and the next labelled statement; the proof may be assembled in later sections or lie in another paper, and its location is to be confirmed |
| `CONDITIONAL_ON_NAMED_INPUTS` | the statement names estimates of other papers as hypotheses |
| `RESTATEMENT` | a displayed copy of a result whose proof home is elsewhere |
| `RESULT_NOTE_WITHOUT_LABELLED_STATEMENT` | the part states its results in prose or tables without a labelled theorem |

The status values were assigned mechanically from the typeset text. They describe the manuscripts; they are not verdicts on correctness. No statement in this baseline has an independent referee report.

## 3. Conditional statements and limits

A conditional statement lists each premise as a mathematical assertion that can be checked. An exact finite identity, an identity of formal expansion coefficients, a finite-order uniform estimate and an empirical inference are different claims. A bounded remainder does not identify its limit; uniformity at fixed interior cutoff does not give a moving-edge theorem; an additive error tending to zero need not be small relative to a leading term that also vanishes.

## 4. Computation

A program is cited for the conclusion it establishes. Exact symbolic or rational results are identities on their stated domains. A numerical value is a certificate only with outward rounding or rational bounds covering all truncation errors. Counts of successful predicates are not theorem counts. `COMPUTATION/RERUN_RECORD_2026-11-12.csv` states which programs were executed for this baseline and how their output compared with the stored output.

## 5. Front matter

Every paper names Kirtus Justus, Theoretical Physicist, Port Coquitlam, British Columbia, Canada, and carries the contributions statement. Papers do not contain editorial history; changes between editions are recorded in `COMPONENT_CROSSWALK.csv` and `TEX_SOURCE_EDITS.json`.

## 6. Review

A review record states its subject, its question, what was inspected or executed, and a scoped finding. Review records are kept in `REVIEW_RECORDS/`, apart from the papers. A finding made by the party that drafted the work, or by an AI system at the author's direction, is not an independent review.
