# Findings, PR 22, First_direction_in_site_parity.md (cross-review sub-agent, Claude family; not independent replication)

## Item 2. Rerun of the note's checker (done first)
- Copied check_parity_direction.py to work/checker_copy/ (only file there), ran `python -B check_parity_direction.py work/rerun1` (Python 3.13.18): exit 0.
- Output byte-identical (cmp) to src/Director_G/results/parity_direction.json; SHA-256 a3822640131bc31acb59a27332cc410cb934758c39eed87c70ee52dd0d264132 = stated digest. MET.
- Second run into the same directory: FileExistsError, exit 1, digest of file unchanged. MET.
