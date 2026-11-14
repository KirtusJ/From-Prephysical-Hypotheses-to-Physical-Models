# From Prephysical Hypotheses to Physical Models

**Kirtus Justus**, Theoretical Physicist  
Port Coquitlam, British Columbia, Canada  
Baseline FPHPM-BASELINE-2026-11-14-Z25, 14 November 2026

This is the baseline edition of the research program. It replaces the two-volume arrangement of 10 November 2026 by 41 papers in seven series (689 assembled pages; one paper is planned and not yet written), with program-level registers held outside the papers.

## Where to start

1. `PROGRAM/CHARTER.md` — aim, structure and responsibility.
2. `PROGRAM/STANDARDS.md` — kinds of statement, proof homes, registry status values, computation and citation.
3. `PROGRAM/PAPER_INDEX.md` — the papers. Paper A1 is the program overview.
4. `PROGRAM/registers/` — theorem registry (416 rows), open problems, readiness, citations, component crosswalk, bridge-candidate map, gate map.

## Layout

| Folder | Content |
|---|---|
| `PROGRAM/` | charter, standards, paper index, contributions, registers, the two program figures |
| `PAPERS/` | one folder per paper: assembled PDF, `parts/`, `source/` |
| `COMPUTATION/` | the computational material of the preceding edition with unchanged relative paths, additions made for this baseline, and the rerun record |
| `NEGATIVE_CONTROLS/` | withdrawn and stipulated constructions kept as counterexamples |
| `CONSTRUCTED_TRIALS/` | models built from stated primitives as test objects, with their assumption ledgers |
| `REVIEW_RECORDS/` | records of AI-assisted reviews directed by the author |
| `LEGACY/` | material of the preceding edition that the papers do not carry |
| `tools/` | the programs that built this edition |

## Scope

The collection establishes conditional mathematics, obstructions and counterexamples. It establishes neither a prephysical substrate nor a physical ontology, and it contains no experimental observation. No paper has been independently refereed. `PROGRAM/registers/READINESS.csv` and `OPEN_PROBLEMS.csv` state what each paper still lacks.

## Checking this edition

`python3 verify_baseline.py` recomputes the digest of every file against `MANIFEST.json`, checks that every component of the preceding edition is accounted for in the crosswalk, that registry identifiers are unique and point to existing papers, and that every assembled paper names the author, title and location. A pass is a local fact about these files; it authenticates nobody and certifies no proof.
