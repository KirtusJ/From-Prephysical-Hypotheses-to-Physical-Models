Target: Director_G/Window_source_cost.md with its checker and results/window_source_cost.json; commit d509426. Named in the director's note of 13 November (late).
Outcome: GAP (three points, wording or scope; no defect found in the derivations or the reported numbers).
Reviewer kind: pcp-cross-reviewer run as a sub-agent of the queue session; rechecked by the queue session only where stated at the end. Same model family as Director Z; cross-review from shared sources, not independent replication. Director G's files were read, not modified.

Claims of the note. Derived in it: a Fourier bound; a velocity bound Pr <= C L delta eta and its consequence delta(T w + 1) -> infinity; an interior site bound C/T and p <= C(w + 1/T); serial and lane criteria; a lower bound on b/p; a threshold r > 3/2. Computed: two panels (T = 16 and T = 64) and figures at delta = 1/40 quoted from another result file. Taken from elsewhere: p ~ 2w/pi with its four window conditions, and the four-tick force construction.

Derivations: the Fourier bound, the consequences of concentration, p <= C'w, the serial criteria with their limit and hazard sum, the displayed lower bound (an identity, checked symbolically), the summary's "success tending to zero", the lane conditions and the threshold r > 3/2 all follow, with their hypotheses stated.

GAPs
1. |K| <= C delta eta: "small delta" is not quantified, and C is uniform only if delta(|p0| + eta) stays away from 1/sqrt 2. Measured: C up to 30.2 at delta = 1/5, p0 = 3, eta = 0.5; between 4.00 and 8.006 at delta = 1/160.
2. The site bound C/T is a sketch (correct, by the second derivative of the phase at the roots) and needs the whole window inside the interior neighbourhood, so w -> 0, which appears only later in the note as w = o(delta). At the caustic T times the largest site probability grows from 9.1 to 48.8, so the restriction is needed.
3. Summary sentence: "45.4% of the accepted mass was still outside the declared velocity tolerance". The figure is the conditional tail stored by the flight-window checker, which the sub-agent reads as a tail of the terminal position after the flight; the note defines its probability through the spectral velocity measure and itself says that a terminal test at one time does not establish velocity concentration. The reviewer's spectral tail for the same packet is 22.35 percent. The sentence should say which quantity it reports.

Reviewer's program (xcost.py, twelve predicates fixed first, seed 20261113, none failed)
- Both panels reproduced exactly: 1275/16384 with 37 trials and 282728967155285175/2^63 with 97 trials. Panels not in the note: T = 32 gives 41777307/2^30 and 76 trials; T = 17 gives 1225/32768 and 79 trials; T = 128 gives 199 trials.
- Fourier bound on 300 of 300 random packets; the worst case attains it to rounding.
- Acceptance over 2w/pi: 1.161, 1.056, 1.034, 1.025 at 1/delta = 10, 20, 30, 40; at 1/delta = 40 the acceptance is 0.0112854, as in the note.
- Interior T times largest site probability: 1.04 to 1.39 for T = 64 to 4096.
Checker rerun: byte-identical to the stored result file. The checker covers the two panels and exponent arithmetic on fixed inputs, as the note says; it overwrites its output and has no predicates in a docstring.
Lean: the note links no Lean file and claims none.

Rechecked by the queue session: the checker's rerun is byte-identical to Director_G/results/window_source_cost.json; the sentence with 45.4% is at line 53 of the note; the flight-window checker computes its conditional tail from a quantity it names "velocity" compared with p0 and a tolerance (line 174). Whether that quantity is terminal position over time or a spectral velocity was not traced, so GAP 3 stands as the sub-agent's reading.
Not checked: the proof of the 2w/pi theorem; the four-tick note; the apparatus assumptions; delta below 1/40.
Cost reported by the sub-agent: about 6 minutes, 8 tool calls.
