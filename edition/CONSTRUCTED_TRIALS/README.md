# Constructed trials

**Kirtus Justus**, Theoretical Physicist  
Port Coquitlam, British Columbia, Canada  
Baseline FPHPM-BASELINE-2026-11-13-Z20, 13 November 2026

A constructed trial is a model built from stated primitives in order to test which parts of the target structure follow from them and which have to be supplied. It is a test object. It is not a candidate ontology and is not evidence for or against any physical claim. Withdrawn and wholly stipulated constructions are in `NEGATIVE_CONTROLS/`.

## GH-1: holonomy counts on a finite gain graph

**Primitive.** A finite connected graph with an element of a finite group on each oriented edge (inverse on the reversed edge), up to switching by a group element at each vertex. For the group of order two this is a signed graph (paper G3). The invariant content is the holonomy of closed walks.

**Rule under test.** A set function on walks of fixed length from a fixed vertex, additive in pairs of walks, vanishing on pairs with different end vertices, given by one rule for all graphs, invariant under switching, strongly positive.

**Proof home.** Paper G8. **Program.** `COMPUTATION/Baseline_Additions/verify_gain_graph_pair_measures.py` (15 predicates) and `verify_gain_graph_covers_and_growth.py` (5 predicates), with their result files.

### Ledger

| Item | Standing in GH-1 | Locator |
|---|---|---|
| dependence of an additive measure on the transport | excluded for one weight function applied to all walks; allowed for returning walks, through a class function of their gain, without interference (derived; Directors A, B, G); excluded altogether when events are sets of histories (derived) | G8 Lemma 3.1; G10 Proposition 4.1 |
| representation-free measure | derived: the count of coincidences on the covering graph is the dimension-weighted mean of the irreducible measures; the choice of one representation is supplied | G8 Proposition 4.4 |
| complex, real or quaternionic amplitudes | derived as representation matrices of gains, conditional on the rule; the group and the representation are supplied | G8 Theorem 4.1, Corollary 4.2 |
| squared-norm probability rule | derived, conditional on second order and strong positivity | G8 Corollary 4.2 |
| absence of third-order interference | follows from second order, which is assumed | G8 Corollary 4.3 |
| Hilbert space, transition probability | derived by the construction of Dowker, Johnston and Sorkin; dense subset of a projective space under a growth condition, which holds exactly when the closed walks of even length realize every group element | G8 Propositions 5.1, 5.2 |
| tensor product for composite systems | derived at each walk length from the product of gain graphs with a common step count, which is assumed; over all lengths the product can reach fewer end-vertex pairs (Director G) | G8 Proposition 6.1, Section 6 |
| classical counting measure | derived for walks that leave distinct records | G8 Proposition 7.1 |
| second order of the rule | derived, conditional on events being sets of histories, on the record-sum form of the rule and on a norm-preserving carrier in which walks merge (on a tree every such rule is the count: Director G); otherwise supplied. With trivial gains the count is consistent on the same carrier | G8 Section 9 (1); G10 Theorems 5.1, 5.2, 5.3 (every connected signed carrier of degree two) |
| end vertices as records | supplied | G8 Section 9 (2) |
| group, representation, ordering of values | supplied; for cyclic orders other than 1, 2, 3, 4, 6 the values depend on the character; consistency on histories admits every conjugate character and every combination of them, and is unique exactly for the orders 2, 4, 6 (derived); multiplicativity on products leaves one conjugate character (derived; Director G); if the gain of a walk is itself a record (signed lift) the rule is unique for every order and no character is chosen (derived; whether the gain is a record is supplied); among pair rules with a kernel the consistent ones are the mixtures of the characters in which -1 acts as -1, and faithfulness is supplied (derived); for any finite abelian group and any degree the consistent pair rules are the mixtures over the characters for which the step is norm-preserving (derived) | G8 Proposition 8.1; G10 Theorem 5.5, Proposition 5.6, Corollary 5.7, Theorem 5.8, Corollary 5.9 |
| relation between the measures at successive lengths | absent in general (Directors A and B); it is the statement that events are sets of histories; see GH-2 | G8 Section 9 (5); G10 Lemma 3.1 |
| reversible dynamics, clock | absent; walk length is not unitary; on an undirected gain graph a norm-preserving step is an involution | G8 Section 9 (5); G9 Proposition 4.2 |
| classical Hamiltonian mechanics | absent | G8 Section 9 (6) |
| operational meaning of the transition probability | absent | G8 Section 9 (7) |
| physical correspondence | absent | |

### Comparison with FAR-1

FAR-1 imports complex amplitudes, tensor products, the trace probability rule, the update index and the expansion law. GH-1 replaces the first three imports by conditional derivations from a transport on a finite graph and four named assumptions, and keeps the import of a step count. It derives no dynamics and no classical mechanics, and it does not select complex over real or quaternionic amplitudes.

### Disposition

As a claim that a gain graph yields quantum mechanics: NOT_IDENTIFIED_IN_SCOPE. As the conditional statements of paper G8: SUPPORTED_IN_SCOPE (mathematics; proofs unrefereed; one participant). The trial was assessed by the participant that built it.


## GH-2: a norm-preserving step on a gain digraph; the signed arc digraph of a ring

**Primitive.** A finite directed graph with an element of a finite group on each arc, up to switching, and a character of modulus one. For the group of order two this is a signed digraph.

**Rule under test.** The squared-amplitude measure of GH-1 for sets of directed walks, with the requirement that the measure of an event and of the event of all its continuations by one arc agree up to a fixed factor (consistency under continuation).

**Proof home.** Paper G9. **Programs.** `COMPUTATION/Baseline_Additions/verify_reversible_gain_digraphs.py` (21 predicates) and `verify_reversible_walk_rays.py` (7 predicates, one of them failed and kept), with `reversible_walk_lib.py` and the result files.

### Ledger

| Item | Standing in GH-2 | Locator |
|---|---|---|
| consistency under continuation | supplied, in the form: events are sets of histories; equivalent to the step matrix being a multiple of a unitary matrix on the vectors concerned | G9 Lemma 3.1; G10 Lemma 3.1 |
| determinism without transport | derived: with trivial gains the step is a permutation | G9 Proposition 4.1 |
| period two on an undirected gain graph | derived | G9 Proposition 4.2 |
| internal alternative (which of two incoming arcs), sign -1, opposite interference of the two continuations | derived for out-degree two and gains of modulus one | G9 Theorem 4.3 |
| complex structure of a real reversible step, its orientation | derived (positive generator; reversed with the step); not respected by the records | G9 Propositions 5.1, 5.3 |
| complex amplitudes | not selected: real gains satisfy the theorem | G9 Section 8 (8) |
| the ring, its order and translation symmetry | supplied | G9 Section 8 (4) |
| dispersion, group velocity | derived for the signed ring | G9 Lemma 6.1 |
| distribution of position over steps | quoted (Grimmett, Janson, Scudo); instances computed | G9 Theorem 6.2 |
| momentum equation of a ray under a linear gain | derived, exact | G9 Proposition 6.3 |
| position equation of a ray | observed in instances over one period (deviation 0.61 to 0.65 site); with the ray and the eigenvector connection averaged over the packet the remainder is 0.0735 to 0.0016 site over the periods 64 to 2048; no error bound | G9 Table 4; G10 Section 7 |
| velocity as response to the holonomy round the ring | derived | G9 Proposition 6.4 |
| weak force with gains of order 2, 3, 4 or 6 | not obtained: an exact force of size 2 pi / n needs gains of order at least n (derived); winding gains of order 3 or more have no common local quasi-energy apart from four band edges for order 4 (derived); staircases of order 3, 4, 6 confine, leak or are strong fields (instances) | G9 Section 6.2; G10 Propositions 6.1, 6.2, Table 1 |
| clock | absent; step count without unit | G9 Section 8 (6) |
| generator | a choice of logarithm | G9 Section 8 (7) |
| composition, interaction, more than one dimension | not treated | G9 Section 8 (10) |
| uniqueness | absent: the base digraph and the switching class are free; two inequivalent signings on the ring | G9 Section 8 (11) |
| physical correspondence | absent | |

### Disposition

As a claim that a norm-preserving gain digraph yields quantum mechanics and classical Hamiltonian mechanics: NOT_IDENTIFIED_IN_SCOPE. As the conditional statements of paper G9: SUPPORTED_IN_SCOPE, the position equation of the rays CONDITIONAL (mathematics; proofs unrefereed; one participant). A ray limit with a force for gains of bounded order: UNRESOLVED, narrowed by two propositions of paper G10, with five adverse instances. With events taken as sets of histories, as a claim that the trials yield quantum and classical mechanics: NOT_IDENTIFIED_IN_SCOPE (the count is consistent with trivial gains). The trial was assessed by the participant that built it.
