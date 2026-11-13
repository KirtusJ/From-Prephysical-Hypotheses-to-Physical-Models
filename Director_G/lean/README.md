# Formal checks of the signed walk and its records

Kirtus Justus, Theoretical Physicist, Port Coquitlam, British Columbia, Canada.

Director G’s formal verification participant checked [RecordWeights.lean](RecordWeights.lean) with Lean 4.19.0, commit 6caaee842e94, on Windows x86-64. The command completed with exit code 0. The file imports only the bundled standard library. The directory’s [toolchain pin](lean-toolchain) works with elan. From this directory, run

```text
lean --version
lean RecordWeights.lean
```

The local run used the official Windows release from a separate tool cache. An existing Lean 4.19.0 executable can also check the file directly. [Official release](https://github.com/leanprover/lean4/releases/tag/v4.19.0)

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
