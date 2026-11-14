# Is my PCP OS work clean? (14 November 2026)

The principal overrode the research focus: "ensure your pcp os work is clean". This file says what "clean" was
taken to mean, what was checked, what was found, and what is still not clean.

## What "clean" was taken to mean

1. The mainline builds, passes its tests and boots its kernel, from a fresh clone, with nothing left behind.
2. Nothing I wrote carries a known fault that is still open.
3. The documents say what the source does.
4. No loose ends of mine: issues answered, branches accounted for, local checkouts in step, pull requests in a
   stated condition.
5. Nothing is claimed that was not run.

## 1. The mainline, `KirtusJ/pcp-os` `master` at `6254a71`, fresh clone

Linux x86_64, rustc 1.97.0, QEMU 8.2.2 without hardware virtualisation. One background run; exit codes read
after it ended.

| Check | Result |
|---|---|
| `cargo build --release` | exit 0, 0 warnings |
| vectors regenerated | exit 0; tracked vector files byte-identical |
| `cargo test --release`, workspace | 68 pass, 0 fail |
| kernel with `test=frame-cutoffs` | 72 self-tests pass, 0 fail, exit status 33 |
| `cargo clippy`, workspace, all targets | 0 errors, 16 warnings of six kinds; one was in my code and is fixed in pull request 57 |
| `cargo fmt --check` | fails in 604 places. The source keeps long lines by design and has no `rustfmt.toml`. Not touched: reformatting would rewrite every file under about thirty open pull requests |
| tree after the run | one untracked file, the 6 MB generated `vectors/guard_cases.jsonl`; now ignored (pull request 58) |

## 2. A fault of mine that was open: fixed, awaiting review

Issue 36 (filed by Director G's side) was right: my instrument `mathematics.statement` returned "holds" when no
pin was given, so a check could be recorded as passed although the statement had been compared with nothing.
Pull request 57: it holds only against a pin; without one it returns the digest to pin and does not hold; a
pin that is not 64 hexadecimal digits is refused. Same unpinned input: exit 0 on `master`, exit 1 on the fix.
Workspace tests 69 pass, 0 fail; 0 build warnings. Lesson, the same as with the kernel test earlier today: a
result that says "passed" must have compared something.

## 3. Documents that had fallen behind the source: pull request 58

The specification and the audit harness said eight instruments (nine since my pull request 22); the workspace
README said 22 host tests (25); `ASYNC.md` named an old commit and promised links to work that is now merged;
`RECONCILIATION.md` still said the source and the binary in use are the same build and that the tests had not
been run. All brought into step; the old reconciliation text is left as written and a dated section added.

Raised and not done: `master` and the packaged binary both report version 1.0.22 and behave differently. That
is a release decision (issue 41).

## 4. Loose ends

| Item | State |
|---|---|
| Issue 31 (stop key leaves the task RUNNING) | closed earlier, fixed by pull request 33 |
| Issue 32 (refused program's memory) | closed today, fixed by pull request 33; rechecked on `master` |
| Issue 36 (my instrument) | open until pull request 57 is merged |
| Pull requests 22, 33, 34, 37 (mine) | merged, each after Director G's reading |
| Pull requests 57, 58 (mine) | open, awaiting Director G; I do not merge without their answer |
| Local checkout `/home/user/pcp-os` | was two commits "ahead" of a stale session branch; brought to `master` and pushed; nothing uncommitted |
| My four merged branches (`pcp/director-z-admission-oracle`, `-async-note`, `-kernel-async`, `-mathematics-statement`) | **still on the remote.** I tried to delete them; the remote refused ("the remote end hung up") all four times. They are contained in `master` and harmless. Deleting them needs someone with the right to delete branches |
| `KirtusJ/pcp` pull request 29 (marketplace file on a branch) | open as a draft; installs both plugins, but the `pcp-os` plugin then cannot run a hook until `pcp-os-claude` pull request 3 is merged |
| `KirtusJ/pcp-os-claude` pull request 3 (executable bits; not mine) | evidence posted; awaiting Director G's answer |
| The binary in use | unchanged all day: build 22, digest beginning `c2c6795d`. It has the two hook faults that pull request 40 fixes in source |

## 5. Not clean, and said so

- The plugin installed from the branch route does nothing until the executable-bit fix is merged.
- The source on `master` is ahead of every shipped binary, under the same version number.
- The Python implementation and the `audit/sim` scenarios were not run against a build from `master` by me.
- Nothing of mine was run on Windows, macOS, OpenBSD or FreeBSD, or on real hardware.
- A mistake of mine in this audit, kept: my deletion loop printed "deleted" after each refused deletion. I read
  the remote afterwards and the branches are there. Nothing was reported as deleted.
