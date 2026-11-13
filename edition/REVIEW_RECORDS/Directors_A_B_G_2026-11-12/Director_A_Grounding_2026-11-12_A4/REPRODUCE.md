# Reproduction instructions

Use the extracted packet root as your current working directory. The following work on Linux, macOS or Windows provided Python and the dependencies are present.

```sh
python verify_packet.py
python -m pip install numpy sympy
python verification/verify_A4_independent.py
```

The exact verifier writes `verification/A4_INDEPENDENT_RESULTS.json` and deliberately keeps all 26 finite trial rows (7 cyclic orders and 19 consecutive powers). Rerunning it will change only that derived results file, not any source baseline. A semantically identical JSON reproduction is expected, but platform-dependent float representation in secondary diagnostic fields is not ruled out.

To rerun the G8 source comparison, separately extract the original Z2 archive and locate its `COMPUTATION/Baseline_Additions/Gain_Graph_Pair_Measures_Results.json`. Do **not** infer the original file by matching names alone; use the SHA-256 pinned in `records/INPUT_HASH_RECEIPTS.json`. Then:

```sh
python verification/compare_Z2_G8_outputs.py --original /ABSOLUTE/Z2/Gain_Graph_Pair_Measures_Results.json --rerun verification/Gain_Graph_Pair_Measures_Results.json --out /TMP/G8_COMPARE.json
python verification/qa_comparator_controls.py --original /ABSOLUTE/Z2/Gain_Graph_Pair_Measures_Results.json
```

The included `Z2_G8_DIFF.json` records all seven exact floating-point mismatches (max absolute difference `1.1102230246251565e-16`) from the source rerun in this session. These seven entries are not labeled byte-identical and are not discarded.

The proof erratum is a proposed textual correction only; no Z2/G7 source bytes were overwritten. The full Z2, B3 and G3 scripts remain in the user-supplied originals rather than copied into this overlay. There are no experimental measurements, independently commissioned referees or autonomous sub-agents.
