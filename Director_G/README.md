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
| [Cross-review with Director Z](Director_exchange.md) | Hypothesis checks for G10 and a counterexample to the broader prose summary |

Run each checker with Python and an output directory. The walk, record and forced-envelope checks require NumPy. The two embedding checkers use the standard library. The commands assume the current directory contains this file.

```text
python -B check_walk.py rerun
python -B check_record_selection.py rerun
python -B check_probability_selection.py rerun
python -B check_forced_envelope.py rerun
python -B check_native_embedding.py rerun
```

The results directory contains all trial rows and the retained first-run adverse phase comparison. The numerical residuals describe the model under the specified inputs. The five checkers reproduced eleven generated files byte for byte on the recorded Windows runtime. On other platforms text line endings, math libraries and binary64 reductions may affect byte identity. [Verification record](results/verification.json)
