# Formal checks of the persistent-record argument

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
