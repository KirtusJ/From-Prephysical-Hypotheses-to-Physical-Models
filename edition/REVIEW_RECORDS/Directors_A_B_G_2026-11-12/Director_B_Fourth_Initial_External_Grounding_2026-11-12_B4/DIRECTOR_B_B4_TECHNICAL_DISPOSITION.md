# Director B | Fourth Initial External Grounding disposition

**Research program:** *From Prephysical Hypotheses to Physical Models*  
**Research direction:** Kirtus Justus, Theoretical Physicist, Port Coquitlam, British Columbia, Canada  
**Mathematical and computational assistance:** ChatGPT (GPT-6), Director B  
**Date:** 12 November 2026, B.C. Pacific Time  
**Parent state:** Initial External Grounding OPEN; root G1 OPEN. **No total ontology established or selected.**

## 1. Basis and calibration

The actual uploaded Z2 bundle, Director A3 packet and Director G3 packet were extracted and inspected rather than adopting the relayed summaries. The independently supplied PCP 1.0 Enterprise Edition and its ACR Implementation archive were re-opened in read-only mode. Their bundled edition and release verification programs were executed, and precise provisions were fetched using the supplied **reference lookup** utility. These are artifact checks and local text retrieval, not installation or host enforcement. No independent sub-agent was available; every focused examination was performed by one model participant. Reports from other Directors are distinct submissions with substantially shared sources, **not multiple independent replications**.

### Source-first results

| Input | Direct check | Result and limitation |
|---|---|---|
| Z2 baseline | `verify_baseline.py` on extracted 791-file tree | PASS: 791 files, 39 papers, 367 registry rows; internal structural and hash consistency only |
| Director A3 | Manifest validator; own mathematics checker rerun in working copy | PASS: 19 payloads; 22 claims, 13 open problems; 217 high-precision, 249 finite matrix, 480 GHZ, 240 pure-seed trials retained |
| Director G3 | Manifest validator; three separate mathematics checkers rerun in working copy | PASS: 36 payloads; Veronese, projective-instrument and cycle findings pass their programmed tests |
| Z2 gain graph verification | Supplied independent predicate program rerun | 15/15 predicates pass; 7 numeric JSON values differ in last-place rounding, maximum absolute delta 1.11e-16; no nonnumeric mismatch |
| Z2 phase recovery verification | Supplied program rerun | All 11 printed predicates pass; 29 numeric JSON values differ in rounding, max absolute delta 4.44e-16; no nonnumeric mismatch |
| Z2 Galois embeddings verification | Supplied program rerun | 7/7 printed predicates pass, output JSON byte-identical |
| PCP 1.0 Enterprise Edition | `verify_edition.py` | PASS, edition SHA-256 manifest fingerprint `6e0cd24f626c065eb5d00ad976caade59f4da286a4b1203362feb79a98a8d1f6`; no authenticity/behavioral certification |
| ACR Implementation | `verify_release.py`; targeted clause retrieval | PASS, 57 payloads, manifest fingerprint `42341ddf38a21a659d974af7d27c739605dd192b2d16c76ef1ae2dcdbdd41c79`; not host-enforced |

All supplied claims remain subject to the original premises and source limitations. The exact input SHA-256 values are stored in `RECEIPTS/SOURCE_INTAKE.json`. No inherited baseline was modified.

## 2. Director Z, paper G8: what survives

**B4-01 | SUPPORTED_IN_SCOPE, mathematical growth.** The explicit `K_4` voltage graph over `Z_3`, with gain +1 on oriented edge `(0,3)` and identity gains elsewhere, satisfies a stronger quantitative form of G8 Proposition 5.1's growth requirement. For every endpoint `y` and gain `g` and all `k >= 10`,

`N_k(y,g) >= 3^floor((k-10)/2)`.

The theorem is proved constructively, independent of numerical extrapolation. It implies the specified **character-based** finite-event rays are dense in `CP^3` over arbitrarily large walk lengths. This **resolves an explicit existence instance**, not the whole physical-limit gate or a graph classification. The model imports a complex character, amplitude summation, squaring and ray interpretation.

**B4-02 | SUPPORTED_IN_SCOPE, refinement obstruction.** For each finite horizon `k`, G8's `D_k` is strongly positive. But its natural extension by one walk step satisfies `D_{k+1}(Ext S, Ext T) = <v_S,A* A v_T>`. Compatibility with a single growing history functional, even allowing one positive scalar rescaling per horizon, requires the compression `P_R A* A P_R = c_k P_R`. On the *same* `K_4` construction, two distinct one-step histories have cross-term 0 but their complete one-step extensions have cross-term 2. Thus the supplied graph construction is **not** an extension-consistent history measure. On identity-gain `K_3`, the change is 0 to 1 and scalar normalization changes a single-event fraction from 1/2 to 1/3. This is a scope-limited mathematical no-go for unmodified adjacency iteration, **not** a no-go for all quantum measures, graph-based dynamics or the existence of a Hilbert space at a fixed finite horizon.

**B4-03 | SUPPORTED_IN_SCOPE, unitary-adjacency involution.** Reciprocal unit-modulus gains make the adjacency Hermitian. If it can be rescaled to unitary, `A^2=cI`; the normalized adjacency squares to identity and has step period at most two on vectors and rays. A nonempty loop-free example requires an even vertex count by the trace argument. This closes a loophole in the specific attempt to obtain rich, reversible evolution by simply choosing a 'nice' gain adjacency. Unitary directed shifts, coined quantum walks and exponentials `e^{-iAt}` are outside this claim, since they introduce other choices.

**B4-04 | Original broad statement REFUTED_IN_SCOPE; precise lemma SUPPORTED_IN_SCOPE.** G8's abstract and Section 3 say broadly that *no additive* walk measure can depend on gain. Counterexample: `L(S) = sum_{w in S, terminal(w)=start(w)} 1[gain(w)=identity]` is positive, additive, gauge invariant, and transport-sensitive on a gain triangle. This remains true for arbitrary finite gain groups, since identity is conjugacy invariant. It does **not** contradict G8 Lemma 3.1 with its explicit narrower `sum_w F1(gain(w))` independent of endpoint and walk closure. That lemma remains valid, as does Theorem 4.1 within its declared endpoint-conditioned **bi-additive gain-only** pair-rule class. A scope correction, not a wholesale rejection of G8, is required.

## 3. Director Z, paper G7: geometric-phase sign audit

**B4-05 | FORMULA SUPPORTED_IN_SCOPE; INTERMEDIATE PROOF STEP INVALID.** With the antilinear-first inner product, the horizontal phases satisfy `alpha_{j+1}=alpha_j - arg<a_j|a_{j+1}>`. Therefore the final horizontal lift is `exp(-i theta) a_0`, where `theta=arg B`. G7 Proposition 4.3 incorrectly says `exp(+i theta) a_0` and reverses the compensating determinant signs. Correcting both gives `det_C(T) = exp(i(n+1)theta)`, **the same final formula that G7 states**. This is a sign defect in its displayed derivation, not a counterexample to the determinant identity or to the fan recovery. Exact control: a qubit triangle with `B=(1+i)/4` has lift factor `(1-i)/sqrt(2)` and tangent determinant `i`.

**B4-06 | CONDITIONAL mathematical phase recovery retained.** G7's fan argument uses the full `CP^n` transition-probability metric and arbitrarily subdivided nonorthogonal geodesic sides. One complex orientation must be chosen globally to take complex determinants. It does not recover measured complex phases solely from the three pairwise probabilities of an arbitrary `CP^2` triangle, nor select physical orientation. The proof's relevant hypotheses are explicit and the existing numerical predicates were rerun, but the manuscript remains unrefereed.

## 4. Directors A3 and G3: composition and operational nonselection

**B4-07 | CONDITIONAL mathematical composition results retained.** A3's pure-entangled-seed theorem follows from Schmidt decomposition and one-sided contractive local filtering **inside an imported complex Hilbert-space composite**. Its matching-generated hierarchy explicitly survives independent preparation, discarding and unconditioned local channels while excluding genuine GHZ3 states. These results demonstrate the assumption sensitivity of any quantum-composition claim; they do not derive those operations.

**B4-08 | SUPPORTED_IN_SCOPE, nonselection example.** G3's `k=3` odd Veronese convex body has a 10-dimensional affine state space but the full restricted pure Born projector table and pure `CP^1` geometry. The specified mixtures have identical mean Bloch vectors and projective outcomes yet differ by an admissible cubic effect (`1/2` versus `5/8`). This exact `1/8` difference is a theoretical model separator, not experimentally observed. Its extra effects and failure of projective-test tomography remain an independent gate after the gain graph yields dense rays.

## 5. Research control and implications

1. **P3/P10:** G8's concrete finite graph growth existence requirement is now met in one stipulated example; overall transition geometry and quantitative physical-limit gates remain OPEN. No theorem about every class of gain graphs follows.
2. **P5:** A quadratic character measure is mathematical but does not become a probability law by naming it one. G8's general additive impossibility wording must be narrowed. Finite-horizon positivity alone does not supply history-refinement consistency.
3. **P6:** Tensor-vector-space composition without accessible physical instruments, closure at every arity and state/effect selection does not establish emergent entangled quantum systems.
4. **P7:** Adjacency iterates either generally fail refinement-compatible isometry or, when the adjacency is a unitary rescaling, are involutive. Distinct dynamics can be stipulated but not claimed derived.
5. **P8/P9/P11:** No clock, causal metric, Hamiltonian classical limit or experimentally calibrated map has been obtained. The open obligations remain decisive.

The supplement `RESEARCH/G9_Gain_Graph_Growth_and_History_Consistency.pdf` contains proofs; the exact checker retains 492 count rows for all lengths `0..40`, 108 independent brute-force cross-counts for lengths `0..8`, all 64 gauge-switching cases and five negative controls. Computation is not evidence of an observed universe. The main new value is the **paired positive and adverse test on the same graph**, which separates pure-state density from operational and temporal consistency.

### Open obligations (local additions; not silently renumbered into Z2)

- **B4-OP01:** Find physically motivated premises that select an operational probability law and all appropriate instruments from a relational carrier without stipulating amplitudes.
- **B4-OP02:** Characterize all graph/categorical constructions with projectively compatible positive decoherence functionals across the whole history hierarchy, and determine whether a non-imported dynamics can meet them.
- **B4-OP03:** Determine what, if anything, fixes a representation, gain-character embedding, and phase orientation with experimentally testable criteria.
- **B4-OP04:** Relate finite graph growth to a controlled classical Hamiltonian, rather than only a dense pure-state representation or stochastic counting.
- **B4-OP05:** Independently referee G7's corrected sign chain, G8's narrowed additive claim and the new K4 growth proof; reproduce checks in different mathematical software.
- **B4-OP06:** Establish actual instrument-closure, multipartite composition and mixed-state tomography premises without importing the desired outcome.

**Disposition:** `INITIAL_EXTERNAL_GROUNDING=OPEN`, `ROOT_G1=OPEN`, `TOTAL_ONTOLOGY=NOT_IDENTIFIED`, `Z2_SOURCE_BASELINE=UNCHANGED`. No conclusion here licenses physical ontology selection, administrative phase advancement or host-enforced PCP/ACR claims.
