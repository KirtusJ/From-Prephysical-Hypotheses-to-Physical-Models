# Director A additive grounding overlay | 12 November 2026

**Project:** *From Prephysical Hypotheses to Physical Models*  
**Research direction and original project authorship:** Kirtus Justus, Theoretical Physicist, Port Coquitlam, British Columbia, Canada  
**Technical assistance and internal self-review:** ChatGPT, GPT-6 (OpenAI), Director A  
**Stage and disposition:** Initial External Grounding **OPEN**; root G1 **OPEN**; **no total ontology selected**, quantum/classical mechanics and their physical emergence **not derived**.

This is an **additive, standalone overlay**, not a modified or authenticated official baseline. The supplied baseline remains untouched. The quoted Director Z Z1/G7 disposition was considered, but the complete Z1 archive and G7 source documents were not supplied, so this overlay does not pretend to integrate them. The reviewed standard baseline was `FPHPM-BASELINE-2026-11-12`. All paper proofs and countermodels remain explicitly conditional on their stated mathematical structures, and all ACR assessments were performed by one AI actor.

## Where to begin

1. `DIRECTOR_A_TECHNICAL_DISPOSITION.md` for exact scoped mathematical findings and parent/root status.
2. `Transition_Probability_Geometry_Research_Note.pdf` (six pages; source `.tex`) for local holonomy proof, two phase obstructions, local real-vs-complex discriminator, finite-homogeneity theorem, symplectic counterexample and dynamics nonselection.
3. `ONTOLOGY_GATE_MAP.md` for the explicit scientific-method dependency map and the test conditions required before emergent physics could be asserted. `ONTOLOGY_GATE_GRAPH.pdf`, `.svg`, `.dot`, and JSON give different representations of the same **incomplete search map**, not a proposed final ontology.
4. `REGISTERS/CLAIM_DISPOSITION_DELTA.csv` and `REGISTERS/OPEN_PROBLEMS_DELTA.csv` for 16 new scoped claims and 9 additive open questions, with provisional IDs not colliding with quoted Director Z OP-17–19.
5. `COMPUTATION/verify_transition_geometry.py` and its deterministic JSON data; `CHECKS/` contains local verifier receipts; `SOURCE_LEDGER.md` records exact internal/external sources and limitations.
6. `ACR_CALIBRATION_AND_USE_LOG.md` and `REVIEWS/ADVERSARIAL_CASE_RECORDS.md` for what PCP/ACR was actually used for, including single-actor limitations and recursive case-dependencies.

## Top-line results (mathematical, not emergent physics)

- Projective determinant formula holds *after CP^n and its complex structure are supplied*; six independent tangent ODE/phase-product test cases match with maximal observed residual `7.36e-13`.
- Conjugation shows an unoriented transition metric cannot select signed nonreal Bargmann phase; explicit CP² Gram matrices preserve all three pairwise probabilities while varying that phase continuously.
- Standard real three-level (`RP²`) and complex two-level (`CP¹`) transition geometries differ locally by curvatures `1` vs `4`, without any global monodromy experiment.
- Gelander rules out **exact finite homogeneous** GH approximations to CP^n. Explicit **nonhomogeneous** nets converge only because the target sphere metric was already imported.
- Classical symplectic spin with `I3=0` defeats the **unrestricted** symplectic-plus-no-third-order-interference selector; narrower Jordan theorems have additional premises and remain subject to verification.
- The same static quantum state geometry allows distinct unitary generators; rank-one dephasing is not reversible classical Hamiltonian mechanics. Neither a physical clock nor classical emergence follows.

## Reproduction

```bash
python3 validate_overlay.py
python3 COMPUTATION/verify_transition_geometry.py /tmp/transition_geometry_rerun.json
python3 -c "import json;print(json.load(open('/tmp/transition_geometry_rerun.json'))['dynamics_nonselection'])"
```

Dependencies for the mathematical checks: Python 3, NumPy and SciPy. The second command writes a separate output; existing JSON and PDFs remain unmodified. The first command needs only Python stdlib, validates exact packaged digests, required status markers, CSV headers and the finite graph data.

The source PCP and baseline verifiers ran on the **supplied originals**, not on an integrated host. Baseline: PASS 645 files; PCP Enterprise edition: PASS 10 files; ACR release: PASS 57 payloads; toy verifier: PASS after output-path-only relocation. These are **local consistency checks**, not review validation or proofs. The new geometry verifier is likewise floating-point and is secondary to the mathematical arguments.

## File provenance and operational limits

`RUN_MANIFEST.json` lists SHA-256 and lengths for every payload and original input fingerprints. `validate_overlay.py` can recheck it without the original archives. Primary baseline documents and toy verifier are not silently altered or redistributed. Original G7/Z1 are absent, not reconstructed from the quote. PCP is **absorbed text**, not a CLI/MCP/plugin, installed enforcement layer, independently evaluated procedure, or sub-agent system. All reported counterchecks, nested cases and the research paper are **internal AI-assisted provenance** under human research direction, not independent peer review. No planned case, conjecture, mathematical bridge or source citation implies physical correspondence.
