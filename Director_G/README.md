# Director G research supplements

**Kirtus Justus**, Theoretical Physicist  
Port Coquitlam, British Columbia, Canada

The signed walk gives two conditional links in this research program. On a chosen amplitude plane, independence of a distant record under a balanced local coin can constrain its probability rule. In a selected band, a uniform force gives a controlled Schrödinger envelope and, for a shrinking packet, a Newtonian position trajectory. The primitives, admissible instruments, physical clock and empirical identification remain open. [Working gate map](ontology_gate_map.json)

| Development | What can be checked |
|---|---|
| [Signed walk and weak field](Signed_walk_and_weak_field.md) | Real sheet transport, classical displacement bound, free envelope |
| [Records and complex structure](Records_and_complex_structure.md) | Plane preparation, parity restriction, composition, entangling contact |
| [Probability from record composition](Probability_from_record_composition.md) | Conditional quadratic law, exact field-embedding classification, five-sheet discriminator |
| [Forced envelope and classical motion](Forced_envelope_and_classical_motion.md) | Uniform spinor error estimate and convergence of the position law |
| [Native preparations and probability embeddings](Native_preparations_and_probability_embeddings.md) | Identical transcript laws, finite-preparation obstruction and a measurable limiting frequency |
| [Base preparation and two rays](Base_preparation_and_two_rays.md) | Full-readout obstruction, coherent direction filter and a two-point classical position limit |
| [Relative sheet transport](Relative_sheet_transport.md) | An exact dark output, finite relative-character preparation and conditional transfer of an external tag |
| [Sequential position records](Sequential_position_records.md) | A measured path limit through a field reversal and the joint preparation yield |
| [Fixed transport and record weights](Fixed_transport_and_record_weights.md) | Relative holonomy tests on a fixed graph and the all-integer squared response from persistent corridor records |
| [Lean proofs](lean/README.md) | Universal response recurrence, physical corridor counts, shared-sheet character reduction and integer rounding |
| [Field reversal during preparation](Field_reversal_during_preparation.md) | Exact signed-schedule amplitudes, optimal yield and adverse finite flight data |
| [Periodic interaction and two limits](Periodic_interaction_and_two_limits.md) | A shared integer gain gives two-body Schrödinger dynamics and interacting Newton trajectories; a folded preparation yields four classical branches |
| [Preparing and measuring a coin qubit](Operational_coin_qubit.md) | Three tomographic settings, all-outcome radial feedback and an exact finite CHSH prediction including timeout records |
| [Sector control and the probability embedding](Sector_control_and_probability_embedding.md) | Separate control of all conjugate character pairs, a rare five-sheet record, and the reversible metric condition on compatible odd cyclotomic embeddings |
| [A phase reference prepared by the walk](Internal_phase_reference.md) | Native records select and compare relative phase units, recover cyclotomic squared moduli and bound errors in a later flight. Absolute embedding labels give identical native records. |
| [Local mediation and the force clock](Local_mediation_and_the_force_clock.md) | A reversible nearest-neighbor signal implements the two-body gain. Two initial packets test finite-speed realizations on the continuum clock. |
| [Cross-review with Director Z](Director_exchange.md) | Hypothesis checks for G10 and a counterexample to the broader prose summary |

Run each checker with Python and an output directory. The walk, record, envelope and position-simulation checks require NumPy. The exact embedding and joint-transport checks use the standard library. The commands assume the current directory contains this file.

```text
python -B check_walk.py rerun
python -B check_record_selection.py rerun
python -B check_probability_selection.py rerun
python -B check_forced_envelope.py rerun
python -B check_native_embedding.py rerun
python -B check_band_preparation.py rerun
python -B check_relative_transport.py rerun
python -B check_position_records.py rerun
python -B check_fixed_transport.py rerun
python -B check_field_echo.py rerun
python -B check_periodic_force.py rerun
python -B check_cycle_interaction.py rerun
python -B check_folded_pair.py rerun
python -B check_coin_qubit.py rerun
python -B check_radial_records.py rerun
python -B check_radial_bell.py rerun
python -B check_simultaneous_sectors.py rerun
python -B check_refinement_geometry.py rerun
python -B check_internal_reference.py rerun
python -B check_reference_comparison.py rerun
python -B check_local_mediator.py rerun
python -B check_three_tick_signal.py rerun
python -B check_moving_source_records.py rerun
```

The previous twenty checkers reproduced thirty-four result files on the recorded Windows runtime. Three further checkers cover the mediator, an exact three-tick signal and a finite two-source quantum read, bringing the total to 23 programs and 37 generated outputs. The results retain first-run comparisons, seeded trajectories with missed targets, short caps below the Bell threshold and zero-gain controls. One single-thread BLAS rerun changed a norm from 1.0000000000000002 to 1.0, with all thirteen affected predicates passing in both runs. The original runtime configuration reproduced the stored bytes. [Verification record](results/verification.json)
