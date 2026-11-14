# How calibration works for Director Z, and how it adapts

Kept so that it is not lost between sessions (principal, 14 November 2026). Method, not findings. Add to the log at the end; do not rewrite earlier entries.

## What calibration is here

The method text (ACR Core, the section on onboarding) separates three things: retrieval (can the participant produce the words of a clause, scored mechanically by the tool), application (what the participant does on items with known answers, scored by an assessor who is not the participant, against a criterion fixed before the run), and the participant's own account, which is not a score. Application scored by the participant itself is a self-check and counts as not measured.

## Who is calibrated, and by whom

| Tier or form of integration | Calibrated by | Record |
|---|---|---|
| Director (this session, with PCP tools and register) | retrieval by the `pcpos` tool; application not measured (no assessor other than the participant was available) | `CALIBRATION_RECORD_SESSION_4.json`, `retrieval_scores.json`, `answers.json` |
| Plain sub-agent (no role file, no PCP tools) on Haiku, Sonnet, session model | the director as assessor | `stack_2026-11-14/` |
| Role sub-agents (`pcp-challenger` and the rest) | not yet as such; in practice by the director's recheck of every report | open |
| Queue session (unattended child; no method text or `pcpos` in its container) | not yet; it says so in every status file | open |
| Headless nested workers | not yet | open |

## The procedure, as run

1. Write the items from ground truths already established in the session, so that each has an answer nobody has to argue about: an exact count; a correct proof (control: the participant must not invent a defect); the same kind of proof with one planted error; a summary that overstates its record; a statement false as written; a line that must not overclaim (a gate, an ontology).
2. Write the key and the thresholds, hash both files, and print the digests before any participant is launched.
3. Give every participant the same file and the same one-paragraph brief, nothing else.
4. The assessor scores each item FOR, AGAINST or UNCLEAR, no partial credit, and checks any answer that differs from the key's example on its merits.
5. Record model as requested, integration, scores, thresholds MET or NOT_MET, and the limits; say what was not verified (which model actually served; no second reading of the assessor).
6. State the disposition narrowly: what the tier may be tried on, never that tiers are equivalent.

## How I adapt on the results

- A tier that meets the thresholds gets the cheap roles on trial (micro-review, rerun with byte comparison, outlier scan). The director's recheck of every report stays.
- Every brief to a lower-tier agent carries one control with a known answer (a planted error or a clean case), and the control's result is recorded with the report. A failed control voids the report.
- Items at ceiling (every tier 6 of 6) are replaced by harder ones before any wider conclusion: a real proof of some length with one wrong hypothesis, a result file with one outlier in two hundred rows, a note whose lead drops a hypothesis of its body; three repeats per tier.
- When a lower form of integration lacks the method text (the queue session), its reports are treated as claims with a stated lack of calibration, and are rechecked before use, as now.
- What the chaos runs measure (which planted errors the checks miss) is calibration of the checks; what this file describes is calibration of the participants. Both feed the same decision: where the director must look himself.

## Log

- 13 November 2026: director's record written at the start of the fourth session; retrieval scored by the tool; application NOT_MEASURED.
- 14 November 2026: first stack calibration, six items, Haiku, Sonnet and the session model as plain sub-agents: each 6 of 6, thresholds MET, items at ceiling. Trial of cheap roles on lower tiers allowed, with a control in each brief. Not calibrated: role agents as such, the queue session, headless workers, long tasks. The assessor's scoring has had no second reading.
- 14 November 2026, later: the three tier records were rewritten in the method's Calibration Record form (`stack_2026-11-14/CALIBRATION_RECORD_haiku.json`, `_sonnet.json`, `_fable.json`) after the built-in app `pcpos instrument core.calibration` reported the first summary file INCONSISTENT (fields missing, delivery not a Core 15.8 value, application counts not summing to runs). All three now read CONSISTENT AS DECLARED: application 6 of 6, negative controls 1 of 1, positive controls 1 of 1, retrieval NOT_MEASURED; the app's outputs are kept beside them. The app checks that a record's numbers agree; as it says itself, that is not evidence of onboarding. Adaptation: every calibration record is passed through this app before it is filed.
