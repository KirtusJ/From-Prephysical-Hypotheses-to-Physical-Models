# Reading an electric string through local occupation gates

**Kirtus Justus**, Theoretical Physicist

Port Coquitlam, British Columbia, Canada

Research supplement by Director G (OpenAI Codex).

Two occupied sites on an open binary chain can carry an interaction phase proportional to their separation. A physical implementation uses one electric bit per edge. Each hop flips the edge it crosses. Each excited edge accumulates the same local phase. On six sites an initially adjacent pair returns to its starting sites with probability \(3845521/244140625\) after two periods without a field kick, and \(36452881/244140625\) with one quarter-turn kick per period. Both probabilities include every history reaching the port. The continuum scaling and the resulting position law are treated in the [quantum and classical motion analysis](Electric_string_quantum_and_classical_motion.md).

One-dimensional \(\mathbb Z_2\) gauge models with dynamical matter and electric strings have an established literature. The calculation here specifies the staggered gates, the preparation and the finite measurement that detects the string phase. Its assumptions include local coherent control of the matter and link coordinates, a common convention for the phase kicks, and squared-coordinate readout. [Borla et al., *Confined Phases of One-Dimensional Spinless Fermions Coupled to \(\mathbb Z_2\) Gauge Theory*](https://doi.org/10.1103/PhysRevLett.124.120503) · [Kebrič et al., *Confinement and Mott transitions of dynamical charges in 1D lattice gauge theories*](https://arxiv.org/abs/2102.08375)

## Local gates and the effective separation phase

Write \(n_j\in\{0,1\}\) for the occupation of site \(j\), and \(E_j\in\{0,1\}\) for the electric bit on the edge from \(j\) to \(j+1\). Fix the two exterior bits to zero. On each active bond with a single occupant use the following operator, in left-occupied, right-occupied order:

$$
G_j=\begin{pmatrix}cI&-hX_j\\ hX_j&cI\end{pmatrix},
\qquad X_j|E_j\rangle=|1-E_j\rangle,\qquad c^2+h^2=1.
$$

The vacuum and doubly occupied local configurations retain amplitude one. Even bonds use \((c,h)=(3,4)/5\) and odd bonds use \((4,3)/5\), in the same left-to-right convention. A full period applies the disjoint even bonds and then the disjoint odd bonds. The field operation multiplies each edge state by \(w^{E_j}\), where \(|w|=1\). Throughout the continuum comparison it fires once, after the odd layer. The table below also tests a second setting that fires after each layer.

For \(D_j=n_j\mathbin{\oplus}E_{j-1}\mathbin{\oplus}E_j\), every gate preserves each defect bit \(D_j\). A hop flips its two endpoint occupations and their common link, so the two changes cancel at each endpoint. If all \(D_j=0\), solving from the left boundary gives \(E_j=\bigoplus_{r\le j}n_r\). The right boundary admits an even number of occupied sites. For two sites \(x<y\), precisely the edges \(x\le j<y\) are excited, including one edge when both occupations lie in the same two-mode cell.

Map each occupation basis vector to the joint vector of those occupations and their prescribed string. This is an isometry onto the two-occupation defect-free sector. In this basis the kinetic update is the exterior square of the adjacent one-mode layer. The terms with one occupant are its rotation entries, and a doubly occupied bond has the determinant \(c^2+h^2=1\). The kick multiplies by \(w^{y-x}\). A direct evolution of the link coordinates and an independent calculation with two-by-two minors agree exactly on the tested amplitudes. The comparison assumes the stated doubly occupied rule; the data also retain a run with the opposite contact sign. [Occupation contact rule](Occupation_contact_from_composition.md) · [Exact circuit and contraction](check_gauss_string.py)

## Three layers suffice to detect the field

Start at \(x=1,y=2\) on six sites, with \(E_1=1\) and all other edges empty. The complete-cycle read tests whether exactly these two sites are occupied.

| Field convention | Return probability after two full periods |
|---|---:|
| \(w=1\) | \(3845521/244140625\) |
| \(w=i\), once per period | \(36452881/244140625\) |
| \(w=i\), after each half-layer | \(152004241/244140625\) |

For this port the same three values are already reached at half-layer three. Its final bond in layer four is doubly occupied and cannot hop. An exhaustive comparison of all 80 localized two-occupation launches on chains of four through eight sites found that \(w=i\) and \(w=1\) have identical terminal position probabilities through the second layer under both clocks. Some launches differ at the third layer and every tested launch differs in at least one port by the fourth. For the real localized sources and real kinetic gates, replacing \(w\) by \(\bar w\) conjugates the whole state and preserves its sharp-coordinate probabilities. Thus sensitivity to a kick and sensitivity to its orientation are distinct experimental requirements. [Complete amplitudes, schedules and null results](results/gauss_string.json)

## Preparing the links and comparing local records

A neutral pair can be prepared from vacuum by a local source that exchanges the \(00\) and \(11\) occupations of one bond and flips its link in that exchange. This reversible extension leaves single occupations fixed and preserves both endpoint Gauss constraints. The source supplies a number-changing operation in addition to the number-preserving walk. Once a pair occupies adjacent sites, sending one member through \(d\) further edges with deterministic dressed swaps extends the string in \(d\) local steps. Reversing the swaps and applying the source again restores the vacuum.

Disjoint packets can be prepared coherently. On eight sites create the pair at \(3,4\). Two successive layers of outward rotations produce amplitudes \(3/5,12/25,16/25\) for each orbital in order from the innermost to the outermost site. Each of the nine resulting position pairs carries its own electric string. The circuit succeeds with probability one and its inverse restores the original pair. On disjoint intervals of lengths \(L,R\), splitting off one prescribed coefficient at a time gives a real packet source of depth \(\max(L-1,R-1)\) after creation, provided the required addressed rotation angles are available. The finite example uses only the stated rational rotations and their sign reversals.

The links are part of the causal preparation. Compare sources at \((1,4)\) and \((1,6)\) on eight sites. Their occupations differ at 4 and 6 and their electric bits differ on edges 4 and 5. With a quarter-turn kick after each layer the probability of finding an occupant at site zero agrees through layer four, when neither changed input lies in the detector's backward cone. At layer five the probabilities are \(5756224/9765625\) and \(222784/390625\). Their difference is \(186624/9765625\). Each elementary gate touches only two neighboring sites and their shared edge; a diagonal electric kick has no spreading action. An independently assigned field at all sites would change the initial data used by this comparison. [Backward cones and both complete receiver marginals](results/gauss_string.json)

## What an unread link preserves

Distinct two-occupation configurations in this sector have orthogonal strings. Tracing over the links makes the bare two-occupation density matrix diagonal in position. The effective amplitude on the ordered pair coordinates describes the joint dressed state. A local gate that uses both an occupation and its incident link can still measure relative phase.

On four sites take the normalized sum or difference of the dressed \((0,2)\) and \((1,2)\) configurations. Apply a single \((3,4)/5\) dressed rotation on bond \(0,1\), then read \((0,2)\). The probabilities are \(1/50\) for the sum and \(49/50\) for the difference. If the electric bit \(E_0\) is copied into a separate pointer and the pointer remains unread, its orthogonal states distinguish the two incoming components. The same analyzer then gives \(1/2\) for either preparation. The copy is nondemolition for a sharp electric configuration, and applying its inverse before the analyzer restores the original two probabilities. A repeatable read can therefore disturb the later interference of a superposition. Discarding the links entirely also discards their role in the analyzer. A classical mixture of the two dressed configurations gives the \(1/2\) control. [Joint electric-flag and occupation records](results/gauss_string.json)

With both exterior fields held at zero, complementing every *internal* link changes the defects at the first and last sites. In that sector an \(N\)-site string has \(N-1-(y-x)\) excited links. Its kick is \(w^{N-1}\bar w^{\,y-x}\); the separation slope is reversed and the first factor is common to the state. The six-site check compared full amplitudes through two periods after complementing the labels. Launching separated occupations with every link blank instead introduces defects at those occupied sites. The vacuum, the complemented empty-occupation state and the empty-occupation state with a single excited link are also included. These boundary and preparation choices determine which interaction the reduced position coordinates represent. [Exact background controls](results/gauss_string.json)
