# Predictions written before any edition mutant was run (seed 20261113)

| id | mutant | check that ought to catch it | prediction |
|---|---|---|---|
| E01 | changed digit in a result JSON under COMPUTATION | verify_baseline.py: manifest digest | CAUGHT (digest) |
| E02 | changed word in a paper's .tex | verify_baseline.py: manifest digest | CAUGHT (digest) |
| E03 | one byte replaced in a paper PDF | verify_baseline.py: manifest digest (and crosswalk digest if it is a part) | CAUGHT (digest) |
| E04 | deleted file | verify_baseline.py: missing file | CAUGHT (missing) |
| E05 | added stray file | verify_baseline.py: unlisted file | CAUGHT (unlisted) |
| E06 | added stray file under a directory named __pycache__ | verify_baseline.py: unlisted file | SURVIVES: the unlisted test skips every path containing '__pycache__' |
| E07 | registry CSV: a statement number changed | verify_baseline.py: manifest digest | CAUGHT (digest) |
| E08 | registry CSV: a status word changed | verify_baseline.py: manifest digest | CAUGHT (digest) |
| E09 | a digest changed in the manifest | verify_baseline.py: manifest digest | CAUGHT (digest) |
| E10 | a line changed in the register copy inside the edition | verify_baseline.py: manifest digest | CAUGHT (digest) |
| E11 | README count '413 rows' changed | verify_baseline.py: manifest digest | CAUGHT (digest) |
| E12 | a pair of file names swapped | verify_baseline.py: manifest digest of both | CAUGHT (digest, two files) |
| E13 | result-JSON digit, manifest consistent | rerun of the program and byte comparison (not the verifier) | SURVIVES the verifier; only a rerun catches it |
| E14 | README count, manifest consistent | nothing mechanical ties the README sentence to the registry; a reviewer of the summary | SURVIVES the verifier (it prints 413 but does not compare) |
| E15 | registry status word, manifest consistent | a reviewer comparing the registry row with the paper | SURVIVES the verifier |
| E16 | registry row removed, manifest consistent | verify_baseline.py ought to compare PAPER_INDEX.statements and the README count with the registry | SURVIVES the verifier |
| E17 | addendum '32 labelled statements' -> 33, manifest consistent | summary-sentence review (a reviewer) | SURVIVES the verifier |
| E18 | manifest: predecessor digest changed | verify_baseline.py ought to, but has no predecessor to compare with; git history of MANIFEST.json | SURVIVES the verifier |
| E19 | manifest: a file size changed | verify_baseline.py ought to compare sizes | SURVIVES: the verifier never reads 'size' |
| E20 | register copy line (interior), manifest consistent | the register's own prev-hash chain; comparison with .pcp/register.jsonl | SURVIVES the verifier; a chain check would catch it |
| E21 | PAPER_INDEX pages of G10 47 -> 48, manifest consistent | verify_baseline.py ought to compare with the PDF page count (it already opens each PDF) | SURVIVES the verifier |
| E22 | the verifier itself weakened, plus a wrong README count | nothing inside the edition can; git diff of verify_baseline.py or a trusted copy of the verifier | SURVIVES |
| E23 | register copy LAST line changed, manifest consistent | comparison with the live .pcp/register.jsonl digest | SURVIVES the verifier and a prev-hash chain check (no successor line) |
