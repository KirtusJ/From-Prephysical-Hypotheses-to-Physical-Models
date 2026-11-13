# Reproduction and scope

Requires Python 3.10+, NumPy and SciPy (tested here with the execution environment's installed packages). Optionally use a PDF reader; the mathematical paper's TeX requires standard pdflatex packages.

Run from the root of the extracted B2 packet:

```bash
python verification/verify_packet.py
python verification/verify_B2.py
python verification/verify_packet.py
```

The first command checks the delivered manifest before execution. The second reruns new independent B2 calculations and rewrites `verification/RESULTS_B2.json` and every `verification/raw_trials/*.csv` output deterministically; the third checks they are byte-for-byte equal to the delivered values. The verifier reports only local consistency. If executed in a different NumPy/SciPy version, floating-point CSV bytes may differ while the stated bounds still hold; treat that as a distinct machine-reproduction result rather than suppressing it. Run on a copy to preserve the source archive.

Checks and interpretation:

1. **Fixed Gram probability trial family:** 257 evenly spaced phases plus two additional off-grid phase witnesses = **259 distinct trials**. Every trial included. At `±pi`, Gram rank drops to two but remains positive semidefinite; that is not an excluded outlier.
2. **Complex tangent holonomy:** eight independently integrated CP2 rays/geodesics; the two extremal `±pi` cases require rotating the *coordinate chart* (not the physical rays) to avoid affine denominator zero. A maximum error about `5e-12` is numerical, not a proof.
3. **Adaptive instrument conjugation:** 32 seeds at each of dimensions 2,3,4 = 96 finite three-stage adaptive tests, each with eight outcome words. Uniform conjugation is an exact algebraic identity; the zero reported probability residual reflects the array operations, not measured physical precision.
4. **Finite approximate homogeneity:** 12 relations for explicit CP1 latitude-longitude nets `N=4,8,16`, each checking 12,000 randomly indexed pair comparisons; the analytic proof covers every pair, not only these samples. Unequal nearest-neighbor multiplicities detect nonhomogeneity of the finite nets.
5. **Negative controls:** wrong phase exponent 2 at CP2 witness is rejected; conjugating one state with a fixed projective effect changes probability 1 to 0; finite grids are not mistakenly reported as exactly homogeneous.

Original Director A/G computations are contained in their own supplied ZIPs and were rerun in isolated working copies during the B2 assessment; they are not silently vendored into this packet. To reproduce those, run their respective `validate_overlay.py` / `verify_packet.py` and first-principles numerical checkers inside copies of their archives. Director Z's G7 and Z1 code were not available to run. For original baseline and PCP/ACR mechanical checks, use each original archive's included verifier, not this packet verifier.

Neither the statement `PASS` nor a small floating-point residual warrants a claim of quantum emergence, prephysical ontology, experimental validation or peer review.

A clean ZIP extraction was actually verified in this assessment: running the included checker reproduced byte-identical outputs and a second manifest check passed. On a separate disposable copy, appending one byte to `RESULTS_B2.json` caused the manifest verifier to fail. This is a **local integrity control**, not a proof check.
