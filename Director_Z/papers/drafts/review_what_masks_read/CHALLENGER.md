# Challenger on the draft subsection "What position masks read of a character" (14 November 2026)

A challenger working from the draft text alone, with its own program in exact arithmetic. It was stopped twice
by the account's rate limit and resumed each time with its context, not relaunched. Same model family as the
author; not independent review. The director's rerun of its program in a fresh directory is at the end.

Outcome: no theorem and no proof step failed, in its range (rings of 3 to 10 sites for the named formulas;
exhaustive masks on rings of 3, 4 and 5 sites to lengths 5, 4 and 3; cyclic and non-cyclic groups; starts
normalized and not). Its control (port (3, 3, L) on a ring of 4 for a stated start) gave 1/4.

Corrections, all made in the draft, which compiles after them:

1. WOUND, Remark (a). "That eta = -1 is an input here and is not measured by these events" was false. From a
   sharp start, with no mask, the port (3, -1, L) has P = (1 + Re eta)/4 for any eta: zero exactly when
   eta = -1 (193 of 193 qualifying sharp-start evaluations across 192 carrier–ring draws; checked by hand by the director: the two words RLL and LRL have gains whose
   quotient is H). The remark now says that eta = -1 is assumed in the statements and can be tested.
2. WOUND, Remark (c). On rings of 1 or 2 sites, parts (i) and (iv) fail already for sharp starts, not only for
   starts in both rails; parts (ii) and (iii) hold there. Stated now, with the value at N = 2.
3. Wording, last proposition: the later statistics are 2^(-t) times those of the stated start, since the two
   sums are not normalized.
4. Wording, the paragraph after it: "it grows only if ..." is proved among position-mask events only.
5. Minor: on the line M is not defined and omega does not enter. 6. Minor: the lemma is for t >= 1.

Kept: its predicates that fail outside the stated hypotheses (eta not -1; rings of 1 or 2 sites), and the
check that the fair-count sentence needs a sharp start.

Not checked by it: the Remark's counts and Lean claims; eta not real; rings above 10 sites for the named
formulas; the complete list on rings of 6 or more.

Director's rerun:
exit 1 seconds 6
26034dda3d1414ec53bc62cc8a6d3fdb02b05e4cf477e2fafcce964f7f8a953d  results_final.txt
cmp: EOF on results_final.txt after byte 340, line 6

### Director G's replay of the filed program

The original six-second rerun listed above preserves neither the invocation nor stderr. Omitting the
carrier-count argument in a fresh directory reproduced its six-line output through `DP check done`,
including the reported SHA-256 after normalizing line endings. Python raised `IndexError` at the first
access to `sys.argv[2]` on line 467. This matches the recorded failure and does not establish the original
command. The archived final run used six carriers for its main exhaustive configurations.

To reproduce that run, with NumPy and SymPy installed, use a fresh output path:

```text
python challenger_chal.py results-new.txt 6
```

At source commit `e4f8b728e659d7a8eee1e99bb7f9ace171883e0d`, the Windows rerun exited 0 in 568 seconds
with empty stderr. After converting CRLF to LF its entire 96-line, 10,445-byte output matches the archived
Git blob content, SHA-256 `b9017ee5c99c08ddd73fd5506dddc81c2841a6754f304b3f25e1e0a8d8de62fb`.
Both the 70 predicate rows with no failures and the 13 rows containing expected failures are present.
The ETA row counts 193 evaluations on 24 carrier draws at each of eight ring sizes. On one draw at N=5,
the random sharp-start phase equals the fixed one. The two records count as two evaluations of that draw.
[Cross-review and reproduction](https://github.com/KirtusJ/From-Prephysical-Hypotheses-to-Physical-Models/pull/3#issuecomment-6874051571)
