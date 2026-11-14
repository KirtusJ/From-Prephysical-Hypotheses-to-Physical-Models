# Premises attack on G1 v1.0 (Claude sub-agent, same model family as Director Z; in-project review, not independent)
Scope narrowed by coordinator to C, D, E. A, B, F, G not run.

## C. How much stipulation 3 does (computed, exact)
Files: attack_C.py -> run1/attack_C.json ; attack_C2.py -> run2/attack_C2.json.
Setup: sharp launch, unwrapped line, site conservation at every site, every t<T; front forces Z_{t+1}/Z_t=2 (P1 passed, T fronts of T).
- Detector sees only signed total s (G1): solution space projected on inputs seen by tick 6 has dimension 1 (the square), T=8..14. |s| fails from T=3.
- Detector sees only route number n: dimension 1 (the count), T=2..12.
- Detector sees (n+,n-) [= (s,n), a bijection, so one model]: count and square both solve; full dimension 1,2,3,5,7,9,14,18,24,28,37 for T=2..12;
  projected on the 18 responses seen by tick 6 the dimension is 7 and does not shrink for T=8..14 (4 of 12 for tick 5).
  count is strictly positive on all visited inputs, so count + small multiple of any solution is a nonnegative response: a 7-parameter family of
  admissible detector laws obeys marker conservation. Conservation does not select the square; the restriction to s does.
- Detector resolves the last arc, common g of the arc's signed total, g(0)=0: solution space is {0} for T=4..11, i.e. no law with g(1)>0. (square and |.| both fail at T=4.)
  So "one common function of the local signed total" is consistent with marker transport at port resolution and inconsistent one step finer.
FAILED predicates kept: P2 (I predicted PM dim == 2; false, it is 7..37), P3 false at T=12 (dim 2) and P5 false at T=12 (dim 1): both are
boundary artefacts (totals first seen at the last tick only as outputs); projected dimension for S stays 1; ARC equations at T=11 are a subset of those at T=12, so g=0 on all tick<=11 values still holds. Not rerun at larger T (budget).
Verdict C: WOUND. Ledger row 3 already concedes sufficiency is a separate stipulation, but README/overview/P5 wording ("together select", "force") hides that the selection is by the choice of detector variable: n -> count, s -> square, both -> 7+ parameters, arcs -> nothing.

## D. Derived versus assumed (argued, with C's numbers)
Advertised (README): "Those two physical stipulations together select the square of that total"; map P4 "Opposite path signs cancel"; P5 "force the square".
- Assumed in stip 3: the response depends on the net signed total only; f(0)=0 "also at exact cancellations" (destructive interference); f(1)>0; same f on all ports, times, rings.
- Assumed in stip 2: one conserved marker, launch law independent of read time; marker does not disturb tallies.
- Derived: f(k)=k^2 given the above; Z_t=2^t; existence of a coupling (transition (u+v)^2/[2(u^2+v^2)], which makes the marker steered by the tallies; stated as derived after selection).
- Strict criterion "demonstrated assumption of the advertised conclusion": the square is NOT contained in stip 3 alone (|s| satisfies 3, fails 2; computed) nor in 2 alone (count satisfies 2). HELD on the letter.
- But interference (darkness at cancellation, dependence on s only) is assumed, not explained; any reader taking G1 to explain cancellation is taking an input for an output. Map row P4 must say "stipulated".
Verdict D: WOUND (wording), not KILL.

## E. Difference from textbook quantum walk; map classification
run_E_check.txt: p_t = D^2/2^t is exactly the Born distribution of the Hadamard walk with amplitude D/2^(t/2) (sum D^2 = 2^t). For terminal reads G1 predicts nothing different from the textbook walk.
The two "physical checks" (t=3 port (-1,L): 0 vs 1/4; t=4 ports (0,L),(2,L): 1/16,1/16 vs 3/16,1/16) distinguish G1 from the fair marker / route counting, i.e. from a classical random walk, not from quantum mechanics. Numbers reproduced.
Map rows: P0 FOLLOWS (restates stip 1-2; nothing explained). P1 FOLLOWS. P2 tallies FOLLOWS; real arrays ADDED (stip 4). P3 FOLLOWS (restates stip 1).
P4 cancellation is stip 3 itself (assumed); Fourier bands: mathematics of stip 1, physical use ADDED. P5 FOLLOWS for the sharp launch only. P6 SILENT.
P7 norm preservation FOLLOWS; Schroedinger limit ADDED (stip 4, known result of de Valcarcel et al.). P8 lattice/tick restated; rest SILENT. P9 ADDED. P10 ADDED.
P11 tick-four test FOLLOWS (identical to QM, unmeasured); cosmology ADDED (imported GR + flat LCDM, no link to the walk; yet attacks.md lets its failure retire G1). P12 SILENT beyond sharing the carrier.
Verdict E: WOUND: 4.5 of 13 rows follow from 1-3, and those coincide with the standard Hadamard walk plus Born rule.
