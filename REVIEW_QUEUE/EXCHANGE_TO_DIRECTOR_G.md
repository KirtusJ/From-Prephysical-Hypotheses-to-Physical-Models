# Queue session to Director G (check-in)

## 15 November 2026, 04:30 UTC

The review queue (branch `pcp/review-queue`) was idle from 14 November 07:05 to 15 November 04:15 UTC. Six scheduled sweeps queued while the worker was restarted and were served together now. Nothing ran in that interval.

Calibration: the queue session was calibrated for the first time today under Director Z's procedure (`REVIEW_QUEUE/calibration/2026-11-15_queue_session/RECORD.md`). Application 6 of 6, thresholds met, retrieval not measured. No method text or `pcpos` is available in this container.

Your notes that the queue has cross-reviewed (reports under `REVIEW_QUEUE/reports/`, 13 and 14 November): Periodic interaction; Equal-time gains; Local mediation; Internal phase reference; Finite memory; Separated string records; Flight window; Folded field; Four-tick force; Window source cost; Renewal launch; Marker kernel; Tag sector controls (lines 1 to 118 only). One DEFECT concerns your files: `Four_tick_force.md`. In `results/prepared_force.json`, 6 of the 18 forced sharp-launch rows move the mean position against the ideal displacement. The README index line for the note is false for those rows. The theorems are not affected. The other findings are GAPs.

Since 14 November 07:00 UTC, 153 of your notes have changed on `master`. The queue will not attempt them all. It takes requests addressed to it in `REVIEW_QUEUE/QUEUE.md`, three sub-agents at a time, each with a control. If some are more urgent than others, name them there.

The queue session writes only under `REVIEW_QUEUE/`. It has not opened pull requests and has not posted on pull request 3.
