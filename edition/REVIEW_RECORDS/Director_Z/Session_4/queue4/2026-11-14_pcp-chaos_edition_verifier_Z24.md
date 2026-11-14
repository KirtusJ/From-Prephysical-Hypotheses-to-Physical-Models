Target: edition/verify_baseline.py as changed for edition Z24, run on a copy of the edition at commit d509426. Asked for by the director's note for edition Z24.
Outcome: DEFECT in the check (22 of 32 planted errors pass the verifier; one of its six new checks does not run in this container). A patch that catches 10 of the 22 is filed beside this report, not applied.
Reviewer kind: pcp-chaos run as a sub-agent of the queue session; mutants were planted in scratch copies only and the repository was untouched (git status empty). The queue session rechecked what is stated at the end. Same model family as the author.

Baseline: the verifier passes on an untouched copy (exit 0; 1629 files, 41 papers, 413 registry rows). PyMuPDF is not installed in this container, so the page-count and front-matter checks are skipped with a notice. Of the six new checks, five caught their mutants; the page-count check did not run.

Counts: 32 mutants. CAUGHT 9, SURVIVED 22, EQUIVALENT 1 (the registry file converted to other line endings). Every prediction made before a run held; every restore was verified by a digest of the tree.

The ten kinds named by the director: all ten still pass the verifier (programs and Lean were not rerun by it).
- A digit in a result file: caught only by a rerun and byte comparison.
- A status word in the registry: a reader.
- A count in an addendum's summary: a reader of summaries.
- The predecessor digest: patch (compare against git history).
- The verifier itself disabled: patch, when a trusted copy is run from outside the tree.
- The last line of the register copy changed: patch (the copy must be an initial segment of .pcp/register.jsonl).
- Three program changes (a walk stopped early, a weakened predicate, a shortened loop): a digest of the source inside the result file, or a rerun.
- A hypothesis deleted from a Lean theorem: the Lean build.

Other survivors
- Page count in the paper index raised by one: patch (a fallback to pdfinfo).
- Register copy missing its last three lines: not caught by the patch; idea, untested: require the last line to close the review of this edition.
- Register copy with its first line dropped; a line altered and re-chained: patch.
- A result file cut to half: patch (listed .json files must parse; one stored file, a kept partial output of a crashed run, is not valid JSON, so names containing "partial" are exempt).
- A file renamed, removed or added with the manifest made consistent: needs a comparison of the file list with the predecessor manifest and the list of changes; not written.
- Paper G10 marked "planned" (which switches off its tests): patch.
- A registry row removed with both counts lowered to agree: a reader.
- The count sentence of the README reworded so that the pattern never matches: patch.
- A text file with a compiled-file name under a cache folder: patch.

The patch (verify_baseline_z24_chaos2.patch, 73 lines, with a description file): passes on the unmodified copy and, per the sub-agent, catches 10 of the 22 survivors. It is a proposal for the director; the queue does not edit edition/.

Rechecked by the queue session: the unpatched verifier exits 0 on the pristine copy with the notice about PyMuPDF; the patched verifier exits 0 on the same copy; the result file holds 9 CAUGHT, 22 SURVIVED, 1 EQUIVALENT; the repository is unchanged. Not rechecked: the 32 runs and the claim that the patch catches ten.
Cost reported by the sub-agent: about 6 minutes, 13 tool calls.
