# Attack on Z8 "Two Books": wildcard, seed word "ledger", 15 November 2026

Stipulated candidate for disproof; nothing here is a claim about the world. Attacker is a sub-agent of the same model family as the candidate's author.

Chosen line: (a), sharpened. Reason: FORM T-1 lets the signed sums evolve without ever consulting the counts, so the count is a ledger entry of the preparation and not of the world's condition; that is testable exactly.

Program `ledger_attack.py` (SHA-256 4dc9cc1d...ad333), predicates A1 to A8 fixed in the docstring before the first run.
Command: `python3 ledger_attack.py result_ledger_run1.json ../../function/plot_mean_entropy.json` (run in this folder; exit 0).
Result `result_ledger_run1.json` (SHA-256 00670bbc...92ccb, mode 'x'). Rerun in a fresh scratch folder: identical apart from the recorded argv.
Predicates: A1 True, A2 True, A3 FALSE (kept), A4 True, A5 True, A5b True, A6 True, A7 True, A8 True.

## Control
T-4: H = 0 for the sharp start. Ceiling for length 3 by T-4: 3 log 2 = 2.0794. It is not attained: the last step of a walk is fixed by the rail of its end vertex, so n(v) <= 2^(T-1), and the largest H at length 3 is 2 log 2 = 1.3863 (A6: max n = 4 over every event on rings 1..7; attained by 9 events, first the free run on the ring of 1 site).

## Finding 1 (lead): H is not a function of the world's state. Verdict offered: KILL of S4/S5 on the candidate's own criterion
Argument. In the proof of T-1 the signed sums go to (eR+eL, eR-eL); n appears nowhere. So every chance, now and after every continuation (free or masked), is fixed by the vector eps up to scale; n is inert.
A1 (no masks at all). Ring of 1 site, free run from the sharp start: at T = 2, eps = 2 at (0,R) and 0 at (0,L), the sharp start's vector times 2, with n(0,R) = 2. H = log 2 > 0 = H(start). Same on the ring of 2 at every even T (H = (T-1) log 2), ring of 4 at T = 8, 16, ... (H = log 64 at T = 8), ring of 8 at T = 24, 48 (H = log 2098176). The world has returned exactly to its beginning in every chance it will ever show, and its "entropy" is higher. H there is log of a number fixed by T: a tick counter.
A2 (equal length). Ring of 3, length 3: masks {1},{0},{1} and {1,2},{0},{1} both leave all signed weight at (1,R); H = 0 and H = log 2. 121 such groups on rings 3 and 4.
A8. n(v) from counts propagated through the masks alone equals n(v) from enumerating walks (300 events, 0 mismatches): so n is knowable to an inhabitant who kept the list of masks (weak point 2 as worded, "beyond anything an inhabitant can know": HELD), and is a function of that list and of nothing else.
Why this bites. SPECIFICATION section 1 fixed in advance, as counting against, "a property that any entropy must have and that H lacks". That a thermodynamic entropy is a function of state is such a property (RECALLED from general knowledge, NOT INSPECTED). BRAND commitment 4 calls log n(v) "that record's thermodynamic entropy". The only escape is to say H is the entropy of the preparation record ("given the event", S5) and not of the world; that narrows the brand, changes what the model claims, and makes ANSWERS "the beginning was a state behind which there was one history" (ADDED) about the length of the ledger and not about a state: A1 shows a state identical to the beginning with H as large as one likes.
What the director must judge: whether "function of state" is accepted as a property any entropy must have. The instances themselves are exact.

## Finding 2: S6 and T-1 give an arrow already put in by S1. WOUND (the SPEC lists "S6 is circular" as counting against)
S2 defines free running by "the next step"; S1 anchors every history at (0,R) and orders its steps. S6 then identifies time's direction with the direction in which steps are appended. There is no state of the toy in which S6 could fail, and by Finding 1 the rise of H under free running tracks walk length, not the state (the state is periodic on rings 1, 2, 4, 8 while H rises). Argument only; no program beyond A1.

## Finding 3: BRAND last paragraph, "has nothing to do with ignorance or coarse-graining". WOUND, false as worded
A record "ended at v" lumps n(v) histories; S(v) = log n(v) is the log size of the lump and H its mean. If records were whole histories every lump has size 1 and H = 0 for every event, with T-1 trivial. The step in T-1's proof (n_R + n_L >= n_R) is the merging of two lumps into one. Argument from S4/S5 and the proof; "histories merge" in ANSWERS is what the proof uses (HELD), and it is a coarse-graining.

## Finding 4: FUNCTION Q5, "the mean entropy rises at every step". WOUND (wording)
A5b: on the line H = 0 at T = 0, 1, 2; steps 1 and 2 do not rise. T-1 (non-decreasing) is right; Q5's wording is not.

## Finding 5: FORM T-4 ceiling is never attained for T >= 1 (see Control). Can be made stronger: 0 <= H <= (T-1) log 2, attained on the ring of 1 site at odd T.

## HELD (kept)
- A3 FAILED as a predicate: I predicted an equality case of T-1 in which an occupied site of zero chance has walks on both rails (which would falsify BRAND commitment 1 and OVERVIEW "every occupied room"). None among 45,218 events, 30,896 equality cases. The brand wording HELD on that range; not proved in general.
- T-1 and its equality case as worded in FORM: 45,218 events, 0 failures, 0 mismatches (own program).
- Q4: ring 3, masks {1},{0},{1,2},{0,1},{0,2} then {2}: H from exactly (2/3) log 2 = 0.46209812 to 0.
- Q5 numbers: 2.637, 14.799, 31.571; gaps 2.908, 7.381, 12.791 (80 digits).
- Plot: 64 intervals, each of width 1e-6 and containing the 80-digit value; `pcpos plot < plot_mean_entropy.json | sha256sum` = 93c11082...8ecb, equal to the receipt and to the SVG.
- MAP gate titles equal those of ONTOLOGY_GATE_MAP.json. Note only: MAP says P6 (Composition) is not touched, yet T-2 is a statement about composition.
- T-1 proof read on rings of 1 and 2 sites (x+1 = x-1): the two children differ by rail, the proof stands.

## Not attacked
Weak point 3's subadditivity for correlated pairs (the candidate defines no marginal for a non-product pair event).
