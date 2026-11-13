# Director B | Third Grounding and Reconciliation Packet (B3)

**From Prephysical Hypotheses to Physical Models**  
**Research direction:** Kirtus Justus, Port Coquitlam, B.C., Canada  
**AI-assisted mathematical analysis:** ChatGPT (GPT-6, OpenAI), Director B  
**Research status:** 12 November 2026, B.C. Pacific Time; Initial External Grounding G1 OPEN; total ontology NOT IDENTIFIED.

This is an **additive** mathematical research and adversarial reconciliation package. It does not change, unlock, replace or rewrite the source baseline. The supplied earlier A2/G2 archives are source inputs and are **not embedded** here. The internal analyses are not independent peer review; no claimed mechanism has been experimentally identified as prephysical reality.

## Contents

- `papers/Selective_Local_Filtering_and_Odd_Cycle_Algebra.pdf` (three-page self-contained manuscript), `.tex` source.
- `reports/DIRECTOR_B_B3_TECHNICAL_DISPOSITION.md` complete claim-level reconciliation, assumptions and open obligations.
- `reports/DIRECTOR_B_B3_SHORT_HANDOFF.md` short inter-director transmission artifact.
- `figures/ONTOLOGY_GATE_MAP.pdf`, `.svg`, `.dot`; `records/ONTOLOGY_GATE_MAP.json` explicit **obligation** graph, not a proven ontology.
- `records/CLAIM_RECONCILIATION.csv`, `OPEN_PROBLEMS.csv`, `SOURCE_LEDGER.md`, `PCP_ACR_SESSION_CALIBRATION.md`, `ACR_FIDELITY.json`, verifier receipt.
- `verification/verify_B3.py` new exact symbolic + numerical controls; `ALL_FILTER_TRIALS.csv`, `ALL_CYCLE_TRIALS.csv`, `B3_RESULTS.json` retain all reported rows including boundary anomalies.
- `verification/negative_controls.py`, `NEGATIVE_CONTROL_RESULTS.json` eight expected-failure cases.
- `verify_packet.py` + `MANIFEST.json` local-byte inventory and semantic schema smoke checks.

## Core exact witness

For `0<t<1`, `K_t=(1-t)Sep_2 + t D_2`, `rho_t=(1-t)|00><00|+t|Psi+><Psi+|` and two successful local filters `diag(epsilon,1)`, setting `x=epsilon^2`, the postfiltered Bell fidelity is `t/(t+(1-t)x)` while **all** states in `K_t` obey Bell fidelity `<= (1+t)/2`. Choosing `0<x<t/(1+t)` violates that inequality with positive success probability. At `t=epsilon=1/2`, success `5/32` and the excess is exactly `1/20`.

**Interpretation:** this does not invalidate the pair model's previously proved deterministic local CPTP closure. It proves that adding unrestricted **selective** local filters is a stronger requirement. An even stronger conditional theorem says that closing a complex two-level composite under all successful local filters, all local unitaries, mixing and limits forces the entire ordinary two-party quantum state set. These premises are imported; none is derived from the finite primitive.

## Verify

In a suitable environment with Python, NumPy and SymPy installed, run:

```bash
python3 verify_packet.py
python3 verification/verify_B3.py
python3 verification/negative_controls.py
python3 verify_packet.py
```

Reruns overwrite only this extracted packet's generated JSON/CSV verification records. On the same environment they reproduce the retained records identically; across different floating-point LAPACK implementations, recorded cycle residuals may vary slightly, and should be checked against the proved numerical acceptance bound rather than assumed byte-reproducible. The manifest validator is an internal consistency check, **not** cryptographic source authentication or independent scientific certification.

The scientific target remains emergent and explained quantum mechanics **and** classical mechanics with a full empirically grounded map. Neither has been achieved by this work.
