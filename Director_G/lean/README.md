# Formal checks of the signed walk and its records

Kirtus Justus, Theoretical Physicist, Port Coquitlam, British Columbia, Canada.

Director G’s formal verification participant checked [RecordWeights.lean](RecordWeights.lean) with Lean 4.19.0, commit 6caaee842e94, on Windows x86-64. The command completed with exit code 0. The file imports only the bundled standard library. The directory’s [toolchain pin](lean-toolchain) works with elan. From this directory, run

```text
lean --version
lean RecordWeights.lean
```

Director G’s supplements in this directory use Lean 4.19.0. Director Z’s edition proofs use their own Lean 4.12.0 toolchain. The local run used the official Windows release from a separate tool cache. An existing Lean 4.19.0 executable can also check the file directly. [Official release](https://github.com/leanprover/lean4/releases/tag/v4.19.0)

| Lean statement | Scope of the check |
|---|---|
| `five_step_histograms` | Enumerates the four and thirty-two signed paths on the specified ten-site, two-register, five-sheet-per-register walk. It sums signs at common endpoints before taking magnitudes. The four histograms reproduce the persistent-flag witness by kernel evaluation. |
| `double_from_five_step_odds` | The cross-multiplied odds equation fixes the response to a count of two at four copies of the unit response. |
| `at_most_one_left`, `admitted_left_time`, `each_left_time_survives` | On rings of size 2m, m ≥ 3, the reduced lag-and-direction masks exclude a second left turn. A permitted left time has residue one. Each positive time in that residue class admits a surviving one-turn path for any number of further right steps. |
| `one_turn_sheet_identity` | Moving a single left turn by whole periods preserves the sheet sum on the intervening departures for every integer-valued periodic gain. This applies separately to each coordinate before modular reduction. |
| `square_from_corridor_odds` | Given all the persistent-flag equations, an arbitrary spectator weight depending on the corridor length cancels. The resulting recurrence forces f(n) to be n² copies of f(1) on every natural count. The code quantifies over a commutative cancellative additive response space. |

RecordWeights.lean covers the reduced masks and conditional recurrence. The separate CorridorCounts.lean file below supplies the physical position enumeration. The experimental justification of stable joint-record odds remains open. The formalization covers the pieces listed above. It declares no new axioms and uses no proof placeholders. Lean’s axiom report for the finite flag enumeration is empty. Some general theorems use Lean’s standard logical foundations through its library tactics.

[SharedSheet.lean](SharedSheet.lean) checks the two-walker character reduction with arbitrary joint departure gains and sheet-unresolved coordinate masks, four-way signed norm scaling, periodic integer gains and nearest-integer accuracy. Use the same compiler and run `lean SharedSheet.lean`. The analytic torus limits are in the [two-body paper](../Periodic_interaction_and_two_limits.md).

[CorridorCounts.lean](CorridorCounts.lean) enumerates signed steps with the actual modular site-and-direction mask for every ring length of at least six. It proves the general physical histogram, signed output ports and the common integer sheet coordinate both at the stop and on each flagged outgoing port. Run `lean CorridorCounts.lean` with the same toolchain. Persistent joint-odds consistency remains an operational premise.

The coin experiment adds three Lean 4.19.0 files. Run `lean` on each file from this directory.

| File | Scope |
|---|---|
| [CoinInterferometer.lean](CoinInterferometer.lean) | Two signed mirror histories on the line, their winding increments and return directions, and the common norm attenuation under the stated phase and coin norm laws. |
| [RadialRecords.lean](RadialRecords.lean) | Both adjacent radius outcomes on a ring of length at least eight, equal branch norms, boundary coordinates and uniqueness of the rational first-step tables. |
| [RadialBell.lean](RadialBell.lean) | Finite source correlations in Eisenstein arithmetic, observer table, mass conservation at every cap and exact four correlations at cap 24. Kernel evaluation gives the strict CHSH inequality. |

The manuscript proves projective density and adaptive hitting. The physical origin of the measured radius, shared sheet, locality and probability interpretation remains open. [Model and proof](../Operational_coin_qubit.md)

[RefinementLocality.lean](RefinementLocality.lean) proves the signed-integer locality certificate for any modulus exceeding the product of the forward and inverse displacement bounds plus one. An explicit family at equality proves sharpness for every even common budget. The identification of a reference encoder and access to its inverse are premises. [Physical interpretation](../Sector_control_and_probability_embedding.md)

[InternalReference.lean](InternalReference.lean) proves that folded distances to two adjacent references determine a residue for every modulus greater than two. It checks simultaneous root and character relabeling on signed counts, the held-label counterexample at order five, and the complete three-site clock control with its recorded-arm comparison. The relative phase of a coherent bypass is a separate apparatus premise. Run `lean InternalReference.lean` with the same toolchain. [Reference protocol](../Internal_phase_reference.md)

[LocalMediator.lean](LocalMediator.lean) proves the unique encounter time on a ring, the pre-contact sheet value, cyclic counter reset and exact branch equality under arbitrarily many common release operations. An explicit inverse covers every counter value. Use the same pinned Lean compiler. The site-register detector, time calibration and packet argument are described in the [local mediation paper](../Local_mediation_and_the_force_clock.md).

[GainAbundance.lean](GainAbundance.lean) proves common-length multiplicity for actual graph edge lists with prescribed cyclic gain, conditional on a primitive equal-length loop difference and equal-length exits. The bound is exponential in the number of repeated two-block choices, independent of their interference. [Graph criterion and readout](../Equal_time_gains_and_history_records.md)

[CoherentComparison.lean](CoherentComparison.lean) proves the cross-table normalization for signed integer entries at a common depth and the exact parity-fold identities. [HeraldedWeights.lean](HeraldedWeights.lean) proves the finite equalizer column counts, common failure factor and conditional cancellation for an arbitrary integer-norm branch. The proofs expose the operational assumptions; local routing, the eight-mode reduction and measurement interpretation are treated in the [comparison paper](../Protected_records_and_coordinate_weights.md).

[AutonomousRecords.lean](AutonomousRecords.lean) checks calibration on one directed orbit, preservation of moving masks by finite edge-supported couplings, and the two local fairness implications for a bright/dark pair. Alternating probes propagate equality over a finite list of signed entries. The theorem distinguishes a reverse coupling of the same marginal record from a fresh reverse experiment. [Physical hypotheses and tests](../Autonomous_records_and_local_echoes.md)

[OpticalPhaseRead.lean](OpticalPhaseRead.lean) computes the ten-step origin numerator and the total norm over all sites under the four eighth-root embeddings. It also checks the four phase settings whose return probabilities coincide. The empirical comparison uses independently reported optical records and the stated phase-plate convention. [Optical phase labels](../Optical_walk_records_and_phase_labels.md)

[ClockPhasePreparation.lean](ClockPhasePreparation.lean) verifies the ten-tick detector mass for every odd integer seed on the physical eight-sheet clock, the preparation recurrence and the total walked norm. [Model and cost](../Preparing_a_phase_clock.md)

[MovingPhaseClock.lean](MovingPhaseClock.lean) checks the moving clock on the doubled cycle and bounds cyclic path-area transport under time-, site- and rail-dependent gauge translations and bounded edge errors. [HolonomyRead.lean](HolonomyRead.lean) verifies the three-tick ordered-pair reads, the even-order alias and the anchored two-plus-one comparator. [Clock model](../Moving_phase_clocks_and_reuse.md) · [Physical record model](../Path_area_and_the_force_clock.md)

[MultisetBlock.lean](MultisetBlock.lean) proves the signed two-input multiset equivalence and its integer polarization at arbitrary finite rank. The real-valued result and switching spectrum are established in the [paper](../Multiset_block_law.md). The proofs in this directory use Lean 4.19 with Std. Director Z’s edition proofs use a separate Lean 4.12 toolchain and Mathlib. [Director Z, cross-review addendum 6](https://github.com/KirtusJ/From-Prephysical-Hypotheses-to-Physical-Models/blob/ad79f263c4791e9ea7ff91800e3940a8cebae2d8/Director_Z_cross_review/CROSS_REVIEW_OF_DIRECTOR_G_ADDENDUM_6.md)

[NativeWeightRead.lean](NativeWeightRead.lean) proves the one-left signed path interval on a staircase-gain ring, its integer-scaled ordered-pair second difference, and the five-tick cancellation. The physical model, real weights, inverse Fourier map, finite-sample costs and detector tests are in the [native measurement paper](../Counting_and_character_records.md).

[LoopCoinPreparation.lean](LoopCoinPreparation.lean) verifies physical coin pulses, equal-time base return, both signed sheet shifts, ring wrap and the action on an entire R packet. [ForceAliasRefinement.lean](ForceAliasRefinement.lean) verifies the odd-order unit classification from bounded doubled representatives and the independent unit-scale criterion. The continuum and apparatus arguments are in the [loop preparation](../Returning_loops_and_one_classical_ray.md) and [calibration](../Force_calibration_across_scales.md) papers.

[ConfinedReturn.lean](ConfinedReturn.lean) proves the parity-compatible signed-area bound on a confined always-moving path, its saturation, and the exact cancellation of the common force kick for a reflected double lobe. The arbitrary even-duration optimum with balanced signs and the ancillary herald bound have separate analytic proofs. [Physical conventions and scope](../Confined_returns_and_quadrature.md)

[MassGauge.lean](MassGauge.lean) checks the bare and quarter-sheet mass frames on complete signed histories with input preparation, arbitrary scalar kicks, variable stride, masks, and a sheet-unresolved squared read. The [bounded-speed replacement and real sheet source](../Local_mass_clock_and_common_ray.md) use additional analytic estimates.

[PhaseContact.lean](PhaseContact.lean) checks both signed contact ports, their squared norms on real integer inputs, the correction at a blank child, and tree-transcript reconstruction up to global reversal. The chain-depth bound and source-independence test have separate proofs in the [contact supplement](../Phase_contact_and_shared_walks.md) and [network supplement](../Network_phase_and_probability_records.md).

[CollisionRecords.lean](CollisionRecords.lean) proves first encounter and reflected versus transmitted labelled positions for the always-moving half-cell walk. [LocalOccupation.lean](LocalOccupation.lean) checks the adjacent-gate action on every two-orbital minor and the rational hopping determinants. The band approximations and hard-point limits are proved separately in the [occupation supplement](../Interacting_occupation_walk.md).

[ContactComposition.lean](ContactComposition.lean) checks the one-particle identity and the two-particle path coefficients for the two rational rotations on four sites, including distinct double-occupation phases on the outer bonds. The general unit-phase selection and robustness estimates use these amplitudes and the [analytic port identities](../Occupation_contact_from_composition.md).

[GaussString.lean](GaussString.lean) proves the ordered two-charge flux law, support size, and adjacent-hop update. The endpoint result extends over finite histories with spectator registers. The [electric-string paper](../Electric_string_quantum_and_classical_motion.md) gives the separate continuum and collision arguments.

[StaircaseAbundance.lean](StaircaseAbundance.lean) constructs at least 2^k physical histories of a common length for every signed residue at both merging inputs of the staircase carrier. The [weight classification](../Counting_and_character_records.md) also assumes a single endpoint function and consistent continuation of arbitrary selected histories.

The extended [staircase proof](StaircaseAbundance.lean) reaches every site and either rail of one parity with every signed gain, at a common time for that parity. It proves clock parity on arbitrary physical words as well. The [Z20 application](../Return_records_and_reversible_dynamics.md) combines the two parity equations analytically.

[StringControl.lean](StringControl.lean) checks the two site-layout responses of the uniform separation energy, their difference for every occupied pair, and the diagonal contrast on each hopping edge. The [control and detector proof](../Electric_string_controls_and_probability.md) gives the Lie closure and the operational premises for probabilities.

[ResidueFrames.lean](ResidueFrames.lean) constructs four-site detector frames from permutations of the sites and proves the sharp and singly calibrated zero entries for integral-scaled weights. [PeriodicReadout.lean](PeriodicReadout.lean) bounds the return at common multiples of component periods with an arbitrary bounded tail and imperfect launch. The [two papers](../Separated_string_records.md) give the physical controls and the [real-valued and stochastic arguments](../Finite_memory_and_coherent_returns.md).

[FlightWindow.lean](FlightWindow.lean) proves the reversible bit operation, the conditional signed tally, and an accepted two-path example distinguishing the bit from a separate record of each port. The later free-flight and continuum estimates are given in the [flight-window paper](../Flight_window_preparation.md).

[ThreeWellPhase.lean](ThreeWellPhase.lean) derives the signed masses of three terminal wells and the determinant factors for independent row brightnesses and fixed well gains. Their normalized contrast measures the real first-arm coherence in the [proposed cesium sign reversal](../Cesium_negative_read.md#comparing-three-wells-with-unknown-detector-efficiencies).

[TagShotBudget.lean](TagShotBudget.lean) proves that a timeout cannot reject and that every rejection within a raw launch budget survives any continuation of the same tick-nine port log. It also verifies the common gain after a fair detector exchange at integer common denominators and the comparison of the two residual throughput bounds at every positive rational ratio. The [sampling calculation](../Tag_sector_controls.md#testing-a-curvature-cap-with-a-finite-number-of-launches) gives the independence assumptions and the resulting binomial probabilities.

Its deadline comparison proves that when each actual wait is at most its paired reference wait, any budget that accommodates the reference waits accommodates the actual waits. The [finite test with residual mismatch](../Tag_sector_controls.md#a-finite-test-with-a-residual-throughput-ratio-of-105) uses independent reference waits to bound power even when actual wait times and right counts are dependent.

The same file verifies the reference ratio endpoints after clearing denominators and the event inclusion for a finite measure with monotone event weights. The [calibration protocol](../Tag_sector_controls.md#calibrating-the-paths-before-the-curvature-test) supplies the binomial component bounds and the source-transfer assumption.

[TagEndpointBounds.lean](TagEndpointBounds.lean) bounds the true conditional right fraction for every allocation of integer unresolved weights among the right, left and outside outcomes. It checks the common certification threshold at rational efficiencies. The [signal-only test](../Tag_sector_controls.md#bounding-the-right-fraction-from-signal-records-alone) supplies the endpoint instrument and the finite-sample calculation.

The same file proves the marginal upper and joint lower count inequalities for arbitrary two-sign pass tables. The [separate-sample design](../Tag_sector_controls.md#when-the-two-sign-streams-can-be-dependent) constructs a raw-stream coupling attaining the probability bound and evaluates the binomial tails. For the [combined-count test](../Tag_sector_controls.md#testing-the-mean-with-unequal-sign-responses), `two_moment_factors` proves the arithmetic–geometric mean step at integer common denominators.

[ThreeTickRing.lean](ThreeTickRing.lean) checks the four-well cubic port counts and integer weight inversion. It also proves that adding an odd circumference changes parity and that the first full left-count span forces the two extreme counts on each rail. The [fixed-ring paper](../Fixed_ring_winding_weights.md#launch-cost-at-the-earliest-clock) derives the signs, probability differences and decision bounds.

[LaterWinding.lean](LaterWinding.lean) propagates signed line amplitudes, folds them onto the 16 physical wells and 21 gain residues, and checks both integer numerators at the four right-rail detectors at tick 144. It also checks the prefix-length implications for the [later-clock bound](../Later_winding_clocks.md#how-far-the-first-clock-obstruction-extends).

[RelativeCoinContact.lean](RelativeCoinContact.lean) checks the sign on the one coincident rail pair, the scaled input agreement identity and the maximum difference for a binary subset of four affected sites. The [three-tick position calculation](../Two_coin_position_read_at_one_contact.md) connects these identities to the full site effects.

[CrossedCoinPairs.lean](CrossedCoinPairs.lean) checks the table partition and the covariance rearrangement used in the [contact partner comparison](../Reassigning_the_two_coin_partners.md).

[PositionRecordBlocks.lean](PositionRecordBlocks.lean) checks the four-tick calibration identities and the norm identity conditional on the single-predecessor premise for [three position records between coherent flights](../Diffusion_from_three_position_records.md).

[FiveTickRecordPowers.lean](FiveTickRecordPowers.lean) checks the three integer rate equations, the centered product and the old-word numerator in the [five-tick position read](../Two_five_tick_records_and_the_probability_power.md).

[SevenTickPositionScore.lean](SevenTickPositionScore.lean) checks the eight terminal rail pairs and the scaled ordinary and counting numerators for the [single position survey](../Seven_free_ticks_and_one_position_read.md).
