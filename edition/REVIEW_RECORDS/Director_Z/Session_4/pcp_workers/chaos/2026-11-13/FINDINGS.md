# FINDINGS (chaos1)

Test 1 (edition verifier), 23 mutants: 11 CAUGHT, 12 SURVIVED.
- Every change made AFTER the manifest is computed and inside a listed file is caught by the digest (E01-E05, E07-E12).
- The verifier is a file-identity check only. Any error made BEFORE the manifest is computed passes: result digit (E13), README count (E14), registry status (E15), registry row removed (E16; the verifier even printed '412 registry rows' and passed), addendum count (E17), PAPER_INDEX pages (E21), register copy line (E20, E23).
- Holes in the identity check itself: any path containing '__pycache__' is ignored (E06); 'size' is never read (E19); predecessor digest is never compared (E18); the verifier cannot guard itself (E22).
- Checks that hold on the unmodified baseline and would catch E06, E14, E16, E19, E20, E21: see the patch file.

Baseline reruns of programs (fresh directories): verify_periodic.py, verify_return_weight.py and check_edge_records.py each reproduce the stored result file byte for byte.
Note: verify_return_weight.py uses seed 20261123, not 20261113, and its docstring does not state the value; all 12 of its random carriers fail hypothesis H (11 of 23 qualify), so the random part tests nothing.
