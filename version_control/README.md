# Recovering a research revision

GitHub’s default branch is `master`. The [master ruleset](https://github.com/KirtusJ/From-Prephysical-Hypotheses-to-Physical-Models/rules/27277204) blocks deletion and non-fast-forward updates. Normal merges and direct fast-forward updates remain available. The [recovery tag ruleset](https://github.com/KirtusJ/From-Prephysical-Hypotheses-to-Physical-Models/rules/27277206) blocks moving or deleting existing `recovery-*` tags. Both have empty bypass lists. An administrator can change the rules.

## Recovery points

The [14 November 2026 branch inventory](2026-11-14.tsv) records each GitHub branch name, its exact commit and a recovery tag from which that commit is reachable. Of 248 advertised branch tips at the snapshot, 244 were ancestors of `master` at `4c822d242f0171d5799fe79365e2e0cc40ada2fb`, counting that commit itself. Four branch tips lay outside that history. Each has its own recovery tag. This preserves the candidate G1 submission, the standing review queue and the exact original histories of two changes integrated under different commits. The main recovery tag includes the inventory. The tags mark a Git preservation checkpoint and convey no scientific disposition.

| Recovery tag | Material |
|---|---|
| `recovery-2026-11-14` | Mainline, inventory and all listed mainline ancestors |
| `recovery-2026-11-14-review-queue` | Standing review queue at the snapshot |
| `recovery-2026-11-14-candidate-g1` | Open G1 submission branch at the snapshot |
| `recovery-2026-11-14-forward-probability` | Original forward-probability-transfer branch tip |
| `recovery-2026-11-14-fixed-ring-calibration` | Original fixed-ring challenger branch tip |

## Restore through a new branch

For an old branch, take its full commit and recovery tag from the inventory. In a fresh Git checkout, the example below restores the former G1 submission. Confirm the tag's ancestry and inspect the tree before rebuilding from it.

```sh
git fetch origin tag recovery-2026-11-14-candidate-g1
git merge-base --is-ancestor 041735102c19d77a7641b39b4b6f5d378255c372 recovery-2026-11-14-candidate-g1
git switch -c restore/g1-snapshot 041735102c19d77a7641b39b4b6f5d378255c372
git diff --exit-code 041735102c19d77a7641b39b4b6f5d378255c372 HEAD
```

To undo a specific change already merged on `master`, branch from the current mainline and publish a reviewed revert. Inspect the parents first. For a normal two-parent PR merge whose first parent is the preceding mainline, `git revert -m 1 <merge-commit>` creates the inverse change and preserves later history. A tag or restore branch also permits reading an older paper or checking its digest without changing the mainline.

Before retiring a topic branch, check the exact live head, all open PR heads and bases, ongoing shared work, the merged PR record and reachability from its checkpoint. A ref that moved since the check needs a new review. New material outside the existing checkpoint needs a new tag. The standing review queue and the open candidate branches retain their separate purposes.

These controls preserve Git objects in this repository. GitHub issues, PR discussions, uncommitted work and the loss of the entire GitHub repository are outside their coverage.
