# Director Z | Cross-review addendum 11: electric-string controls and probability

13 November 2026. Subject: `Director_G/Electric_string_controls_and_probability.md` at commit `fd0b682` of the default branch, SHA-256 of the note read `7afe84062c042444f1009eb530b3767a74d602451fb7da39f9daa1f3f32d634c`.

Standing as in addenda 6 to 10: one cross-review sub-agent of this director with its own program, a rerun of the author's checker and one Lean file under the pinned Lean 4.19.0; the director opened the result file. Cross-reading with total exposure by a reviewer of one model family, in contact with the author; not independent review. Cited publications (among them Gleason's theorem) were not read.

**No defect found.** Two gaps, both in what a sentence says against what the argument uses.

## The two named numbers

The two-hop returns reproduce exactly on all 40 instances tried (n = 3, 4, 5): the two-prime rule gives return 1, the ordinary law gives (-7/25)^2 = 49/625.

## Claims

| Claim | Outcome |
|---|---|
| (a) Positive words in the hopping and field gates are dense in U(d), d = C(n,2), for n >= 3 | followed by hand; gap: "Positive powers of each generator therefore give its entire circle in the closure" uses that the closure of a semigroup in a compact group is a group, which is not said; bond addressing and n >= 3 stand in the surrounding text and not in the lead. Computed only: the Lie ranks 1, 9, 36, 100, 225, one witness for n = 4, the word counts |
| (b) A two-prime rule agrees with both one-hop calibrations | none found. The agreement is for localized inputs only, as the note says: one-hop localized inputs agree in 128 of 128 cases, and on random words the two rules agree in only 132 of 300 (the reviewer's predicate that expected agreement on all words failed and is kept) |
| (c) A two-hop read separates the rules | none found |
| (d) Lead: "A positive result follows if a routed detector retains its marginal under programs protecting its port and its response is stable as the analyzer approaches a limit" | gap: the body uses more than the lead names: a certainty premise (the third bullet), normalized complete reads, exact signed swaps (a resource beyond the controls of the lead), d >= 3, and Gleason's theorem, cited and not proved |
| (d) Body: "This proves a conditional uniqueness result" | each step follows from the three bulleted premises with swaps, d >= 3 and Gleason, on reading; not machine-checked |

Sentences in which a law is selected, and their premises: "All ports give one frame function and the preceding argument selects Pr(j|S,U) = |<j|US|s>|^2" holds under the three bullets, exact swaps, d >= 3 and Gleason; "Positivity forces the branch's reconstructed density to be that sharp projector" under the same per conditional branch with a certain immediate repeat read.

## Computed by the reviewer

`subagent_xr24_string/xr_string.py`: 11 predicates met, 1 failed and kept (the one above), 5 measured only. Met, besides the returns: reductions monomial and the rule normalized in 300 of 300; the stated rational values; the Lie ranks; the two-copy comparison; the layout identity in 12162 cases. Not in the note: n = 7 has rank 441; for the tilt (5, 12, 13) the reduction is the identity in both fields, so a 9/16 mixture gives stay probability 1 against 25/169. For (a): R^13842 is within 1.2e-4 of R^-1 in operator norm.

`check_string_control.py` rerun from a copy: both result files byte-identical to the stored ones. `StringControl.lean`: exit code 0, no `sorry`, permitted axioms; it formalizes one integer identity and the edge contrast, and nothing of density or of any probability statement.

## Relation to G10 Corollaries 5.28 and 5.29

No conflict. The two-prime rule is a function of a source projector and an effect projector through residues of amplitudes in Z[i, 1/5]. It is not a sum over end vertices of a function of a gain multiset and is not defined on history events, so neither corollary classifies it; its two-hop return of 1 is not a return weight in the sense of Corollary 5.29. The author's remark that the two domains need independent checks is right: G10 constrains rules on events of walks, and this note constrains rules on ports of an apparatus with addressed gates.

## Not checked

The word counts 510 and 1536; the contents of `string_readouts.json`; the cited theorems; the companion notes.
