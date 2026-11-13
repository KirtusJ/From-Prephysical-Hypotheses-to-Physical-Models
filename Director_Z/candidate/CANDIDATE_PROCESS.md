# The candidate process

Set by the principal on 13 November 2026. It governs every stipulated candidate model in `Director_Z/candidate/`.

## The two rules

1. **Steelman the best candidate.** While a candidate stands it is given everything a serious proposal has, so that an attack meets the strongest form and not a sketch.
2. **If it breaks, abandon it at once.** No repair in place, no defence, no narrowing to save the name. What survives the break may seed the next candidate, which gets a new name.

## What steelmanning means here

A standing candidate has, each in its own file under `Director_Z/candidate/<name>/`:

| Part | Content |
|---|---|
| Form | the stipulations, numbered, each separately breakable, and what is proved from them |
| Function | what the model computes: exact instances with programs, and predictions that could fail |
| Brand | a name, a one-line statement, and what the model is not |
| Plain-English overview | one page a reader without the mathematics can follow |
| Specification | a peer-review standard specification: definitions, statements with proofs or references, hypotheses in the form the proofs use, programs, limits, and a status table |
| Stipulated map | where each stipulation sits on the program's gate map and which open problems it would close if true |
| Stipulated answers | what the candidate, taken as true, says about the open problems of cosmology and about the Millennium Prize problems |

**On stipulated answers.** They are positions the candidate commits to, written so that they can be attacked. Each is marked as one of: FOLLOWS (a consequence of the stipulations, with the argument), ADDED (a further stipulation made only to give an answer, with what would refute it), or SILENT (the candidate says nothing, and why). None is a solution, a proof or a claim about the world. A Millennium Prize problem is a mathematical statement and no physical model settles it; the entry records only what the candidate would lead one to expect and what it would need. A stipulated answer that is refuted breaks the candidate like any other part.

## What counts as a break

- **KILL**: a stipulation is shown false, empty or contradictory with another; or a derived statement is refuted; or the candidate is shown to assume its conclusion; or a stipulated answer of kind FOLLOWS or ADDED is refuted. The director checks the attack's files before accepting it. A verified kill ends the candidate.
- **WOUND**: a hypothesis is missing or a statement needs narrowing. Recorded in the ledger. Three unanswered wounds to one stipulation, or any wound that changes what the model claims, are treated as a kill.
- **HELD**: the attack was carried out and failed. Kept, with what was tried.

Anyone may attack: sub-agents, the review queue, Director G, the director. The director attacks too and reports his own kills first.

## On abandonment

- The candidate's folder is moved to `Director_Z/candidate/abandoned/<name>/` unchanged, with a file `WHY_ABANDONED.md`: the attack, its verdict, the files, and what survived.
- Nothing is deleted. The ledger stays.
- The exchange file tells Director G the same day.
- The next candidate is the best that the surviving statements support. If nothing better exists, there is no standing candidate, and that is said.

## Standing limits

No candidate is an ontology. No gate is passed by stipulation. The authorship line and the limits of `CLAUDE.md` apply to every file.
