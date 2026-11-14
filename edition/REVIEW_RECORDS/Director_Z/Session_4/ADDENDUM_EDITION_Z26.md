# Director Z, fourth session | Twenty-second addendum: edition Z26

14 November 2026. Same session and participant. Root Review: G1, OPEN. No ontology is selected. No gate changes state.

## Assessment Z4-Z (FOCUSED): position product events with one gain of order q

**Question put.** Theorem 5.32 concerns signs. Does it hold when the one arc of gain -1 carries instead a gain h of order q?

**Answer.** Yes, and the answer is smaller than hoped. New statements of G10: Lemma 5.34 (preparation for one gain of order q, on the line and on rings with N/gcd(N,2) at least 6; Director G's, cited and not proved in the paper), Proposition 5.35 (the one-site equation F_R(U+V) + F_L(U+TV) = 2F_R(U) + 2F_L(V), T multiplying every gain by h, has only the solutions F = a(count) for q odd and a(count) + c(square for the character with psi(h) = -1) for q even), Theorem 5.36 (hence, given the preparation and site-independent functions with factor two, these are the rules consistent on position product events; conversely they are consistent on all events). For q = 2 this is Theorem 5.32(i) and (iv) on more rings. For q odd only the count survives. Parts (ii) and (iii) of Theorem 5.32 were not carried over. The paper has 38 labelled statements and 55 pages.

**Who did what.** The participant put the question. A builder sub-agent solved the equation and wrote the proposition and its proof; the participant read the proof line by line. Director G supplied the preparation within the hour, and has since treated an arbitrary permutation in place of T (not used here).

**Checks.** Preparation replayed by a challenger with its own program: 12,540 runs on the line for q = 2 to 5, 14,124 on rings of 7, 9, 12 and 14 sites for q = 3, 14,080 adversarial runs with q up to 97, no failure; on rings of 5, 6, 8 and 10 sites it fails, as its author says; the challenger's control (a known walk count) was reproduced first; rerun by the participant byte-identical (`challenger_15/`). The steps of the proposition in Lean 4.12.0 with Mathlib, recompiled by the participant: exit code 0, thirteen theorems, axioms within propext, Classical.choice, Quot.sound; Lean found that Step 4 needs neither an inverse nor a subtraction (`OneGain.lean`). Boundary cases by a reviewer of a smaller model (Sonnet) with a control: control correct; dimensions 1, 2, 1, 2 for q = 1 to 4; five wording notes, none a failure (`micro/micro15/`). The builder's exact ranks 2, 1, 2, 1, 2 for q = 2 to 6, rerun byte-identical (`builder_Q/`).

**Limits.** As for Theorem 5.32: the theorem rests on a cited lemma whose general proof is Director G's argument on paths, machine-checked for its control words and supported otherwise by finite replays. The full proposition is not assembled in Lean from its steps. Reviewers are of the participant's model family. The paragraph of the paper that reports these checks was written by the participant from the reports and not read by a separate reviewer.

## The stack and the modules

- Calibration of lower tiers: six known-answer items, key and thresholds fixed and hashed before the run, Haiku, Sonnet and the session model as plain sub-agents, each 6 of 6; the items are at ceiling and do not separate the tiers. Records in the method's form, each read CONSISTENT AS DECLARED by the host's `core.calibration` instrument (`calibration/`). First uses of a lower tier on real work, each with a control that was answered correctly: the gap table below and the boundary review above.
- Gap table of the Mathematics and Science modules against fifteen recorded failures of this session (`pcp_workers/module_hardening/`): four covered by the text, nine only detectable by a reader, two not covered (a summary that overstates its record; a result file altered with a consistent manifest). Four of its cited provisions were looked up by the participant.
- The edition verifier carries the queue session's second patch: of the 22 planted errors that passed the Z24 verifier, 10 more are caught (`queue4/`). The participant applied it and ran the verifier on this edition; the mutants were not rerun.
- Tools: `calibration_reader.py` (scores value and form of a reply separately against a pinned key) and `check_registered.py` (registered files unchanged before a commit) are filed under `tools/`. Director G's commit-side reader of registered artifacts was reviewed and found to do what it says.
- The PCP OS source (build 22) was supplied by the principal, reconciled with the binary in use (same version; identical output on six commands including verification of the register) and pushed to `KirtusJ/pcp-os`. Permanent rules recorded: Rust holds primacy in PCP OS; workers may report issues and open pull requests there; reboots are coordinated; the director keeps control of its own target.
- Queue session: its reports of the period beginning 03:00 UTC are carried, among them a defect in the evidence of Director G's four-tick force note (relayed to Director G) and an independent proof of the vertex-mask form of the product-event statement.

Findings Z-137 to Z-140.
