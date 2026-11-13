# Director B | Bell Memory and QA Continuation

11 November 2026, B.C. Pacific Time. Research direction: Kirtus Justus. Parent Unary PCP: Initial External Grounding, OPEN.

Read `reports/TECHNICAL_DISPOSITION.md` first. The fixed-horizon CHSH results, conditional-memory extension, seven-bit randomized rule, optional-stopping failure mode and anytime-valid supermartingale have separate contracts. `verification/verify_bell_math.py` recomputes exact probability checks without modifying saved references. `verification/verify_qa_controls.py` runs controlled mutations only in disposable copies of the C source ZIP. The original B and C ZIPs are retained in source_archives and identified by SHA-256 in receipts.

The source register contains 1,577 inherited attributed IDs (not distinct theorems), plus eight separately attributable new findings. Original B rows are preserved verbatim in the CSV; the C 12 are appended with JSON and source identity. Only stable-ID union, not universal byte-identical upstream row equality, is claimed.

No physical data, authenticated provenance, parent state token, formal child closure or phase transition is claimed.

To validate the extracted handoff: `python verify_release.py`, optionally `python verify_release.py --deep` for controlled QA mutations.
