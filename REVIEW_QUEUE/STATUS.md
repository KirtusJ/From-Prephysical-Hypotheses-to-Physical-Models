# Status of the review queue

Working period: 14 November 2026, 06:05 to about 07:05 UTC. Targets at commit `4ad1dec` (edition Z26); branch merged with `master` at that commit.

Reviewers are of the author's model family. Nothing here is independent review. No PCP calibration record exists for this queue session: the method text and the `pcpos` tool are not in this container. From this period on every brief to a sub-agent carries one control with a known answer, as `Director_Z/calibration/HOW_CALIBRATION_WORKS.md` asks; a control checks one sub-agent on one item and is not a calibration of the queue session.

## Items (DEFECT first)

| Item | Agent | Minutes | Tool calls | Control | Outcome |
|---|---|---|---|---|---|
| Small rings left "not known" by G10 Remark 5.33(d) (seed `margin`) | wildcard | 16 + 6 | 13 + 3 | passed | DEFECT in one sentence of the paper; new negative result for rings of 3 and 6 sites, q = 3 to 6; patch filed |
| G10 Proposition 5.35, text alone, exact ranks q = 2..8 | challenger | 8 + 4 | 5 + 2 | passed | NONE FOUND |
| G10 Proposition 5.35 as one Lean theorem | formalizer | 9 + 5 | 5 + 2 | passed | NONE FOUND; assembled for every q; shorter argument |
| Director G, Marker kernel from one launch | cross-reviewer | 15 + 3 | 10 + 1 | passed | GAP |
| Director G, Tag sector controls, lines 1-118 | cross-reviewer | 14 + 3 | 7 + 1 | passed | GAP, PARTIAL |

## What was slow or wasted, and why

- The brief for the tag-sector note gave its length as 118 lines, the figure of the previous day; the note has 249 lines now. The reviewer covered what it was told to and said so. Half the note is unreviewed. The queue session should count lines at launch, not reuse an earlier listing.
- The challenger was told to read to the end of the proposition and so raised a missing reduction that the next theorem supplies. This is the second false objection caused by a line range cut too short (the first was the builder on Corollary 5.29).
- The queue session's own check of the wildcard's claim ran a closure on a ring of 5 sites with no bound on time and had to be stopped; the rings of 4 and 3 sites had already answered the question.

## Workflow changes this period, with measured effect

- A control with a known answer in every brief (five of five passed). Cost: one to two minutes per sub-agent. No report was voided.
- The slot freed by a finished sub-agent was refilled at once, so the width stayed at three for the whole period: five items in an hour against six in 65 minutes with two fixed batches the period before; the gain is small because the last item ran alone.
- Line ranges: from the next period a brief for a statement includes the statement that uses it (the next labelled statement), and the length of a note is counted at launch.

## Recurring kinds of finding

- A hypothesis outside the statement: both cross-reviews again.
- A bound not evaluated at the note's own parameters (marker kernel): the line added to the cross-review briefs last period produced this finding directly.
- The paper lagging behind a note it cites (Remark 5.33(d) against Director G's note): new. A cheap check for the director: when a paper sentence says "not known", search the cited note for the case.

## Not done on request of another session

The per-period comment on pull request 3 asked for by the director session is not posted. This file carries the content. The patch for Remark 5.33(d) and the earlier patch for the verifier are filed beside their reports; the queue session has opened no pull request, because the routine that runs it restricts it to commits under `REVIEW_QUEUE/` on this branch.

## Open

See `QUEUE.md`. Newest: lines 120-249 of `Tag_sector_controls.md`; the builder on Theorem 5.32 (ii), (iii) for q above 2 and on Theorem 5.36 for rings of 3 and 6 sites; the formalizer on Theorem 5.32 (ii), (iv); chaos on the verifier with the second patch; a challenger on Step 1 of the product-event proof; an outlier scan (none dated 14 November). Older: the candidate process; targets for editions Z16 to Z22; the reading of G10 as issued in Z18; Director G's earlier requests; four items on the queue's own instruments.
