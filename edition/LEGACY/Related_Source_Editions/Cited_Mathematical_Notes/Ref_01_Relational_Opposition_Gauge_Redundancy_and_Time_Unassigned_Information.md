# Relational Opposition, Gauge Redundancy, and Time-Unassigned Information

**8 November 2026**

Research direction: Kirtus Justus. Mathematical analysis and drafting assistance: ChatGPT (OpenAI).

## Selected scientific sections

Sections 2–8 are reproduced below in an edited scientific edition, with their original numbering. The stipulated group actions, observation laws, quantum operations, and physical limitations are retained.

## 2. Representation-independent observation quotient

Let $X$ be a *stipulated* mathematical set of candidate descriptions and $G$ a *stipulated* group acting on $X$. Suppose admissible scalar descriptions must be invariant under $G$. Then

$$f(gx)=f(x)\quad\forall g\in G$$

holds **if and only if** there is a function $\widetilde f:X/G\to Y$ with $f=\widetilde f\circ\pi$, where $\pi$ maps a description to its orbit. The proof is by defining $\widetilde f([x])=f(x)$, which is well defined exactly when $f$ is invariant. This is elementary quotient mathematics, not a physical measurement or selection theorem.

If $X/G$ contains only one orbit, all invariant scalar descriptions are constant. If it has several orbits, nontrivial invariants **can** be defined, but no measurement, probability or accessible information follows without an additional operational rule. This statement does not depend on a signal metaphor or on fundamental binary signs.

## 3. Binary opposition as a deliberately weak comparison model

Let $X_n=\{\pm1\}^n$, with **formal labels** $1,\ldots,n$. Consider two different hypotheses about changing reference conventions.

**Global convention change.** The group $G_\mathrm{diag}=\{\pm1\}$ acts by multiplying *every* label by the same sign. For $s=(s_1,\ldots,s_n)$, the invariants

$$r_i=s_1s_i,\qquad 2\le i\le n,$$

are complete: any two sign vectors have the same $r_i$ if and only if one is the global inversion of the other. Hence

$$\boxed{|X_n/G_\mathrm{diag}|=2^{n-1}.} \tag{1}$$

For two labels, the surviving invariant is $r=s_1s_2$. The $r=+1$ class represents *same*, while $r=-1$ represents *opposite*, solely in the formal comparison model.

**Independent convention changes.** If each of the $n$ labels can be flipped separately, the full $\{\pm1\}^n$ acts transitively on $X_n$. The quotient has **one** orbit and there are no nonconstant invariants of the bare vertex-sign descriptions.

**Orientation obstruction.** The ordered contrast $J(s,t)=(s-t)/2$ satisfies

$$J(t,s)=-J(s,t),\qquad J(-s,-t)=-J(s,t).$$

It is not an invariant scalar on unordered or globally-inverted descriptions. The magnitude $|J|$ and the relation $st$ do survive. A nonzero *signed orientation* therefore requires a retained order, reference, or different covariant object. In particular, this simple binary opposition is not physical chirality.

All of these conclusions are conditional on the chosen group actions. A foundational hypothesis must still select one of these group actions.

## 4. Multi-context opposition and exact compatibility

Use a finite combinatorial graph $\Gamma=(V,E)$ **only as a bookkeeping register of comparisons**, with no physical adjacency or spatial meaning. Assign each formal pair $e=\{i,j\}$ a sign $r_{ij}=\pm1$.

**Theorem (compatibility).** There exist vertex signs $s_i\in\{\pm1\}$ such that

$$r_{ij}=s_is_j\quad\text{for every }\{i,j\}\in E$$

if and only if the product of $r_e$ around **every** graph cycle is $+1$.

*Proof.* If $r_{ij}=s_is_j$, each vertex sign occurs twice around a cycle and cancels, so the product is $1$. Conversely, choose a spanning forest and fix one sign in each component. Propagate signs along tree edges; cycle-product constraints ensure that the result is independent of the chosen path and satisfies every remaining edge. QED.

For three formal contexts, **all three pairs cannot be mutually opposite** if "opposite" means $s_is_j=-1$ for one globally assigned collection of binary signs, since the triangular product would be $(-1)^3=-1$. Two negative pairs and one positive pair are compatible.

If edge relations are instead *independently supplied*, an odd cycle product may be permitted; then it is extra relational data, not a reconstruction from local vertex polarities. Under independent vertex-frame changes $g_i=\pm1$, edge signs transform as $r_{ij}\mapsto g_ir_{ij}g_j$. Cycle products are invariant. For a graph with $n$ vertices, $m$ edges, and $c$ connected components, the number of distinct gauge classes of unrestricted edge-sign configurations is

$$\boxed{2^{m-n+c}.} \tag{2}$$

A spanning forest removes $n-c$ independent edge signs, leaving $m-n+c$ cycle signs. A connected tree consequently has one gauge class for its transport-only edges; one triangle has two. These are standard signed-graph/structural-balance and finite-$\mathbb Z_2$ gauge facts, not a new physical effect (Harary and Kabell, 1981; modern accounts of signed-graph switching).

**Adversarial meaning.** One must choose between globally realized binary pair relations, independently specified pair relations, or a richer structure. That choice determines possible consistency tests. Nothing establishes which is fundamental, or even that a binary comparison domain exists.

## 5. A relational distinction does not select its own informational capacity

Under the global two-sign quotient, the relational variable $r\in\{+1,-1\}$ has two mathematical possibilities. It does **not** follow that a physical signal carries a bit or that there is any transmission channel.

If an extra statistical observation contract is stipulated, for example a binary symmetric readout $Y$ of $r$ with error probability $p\in[0,1/2]$, then its Shannon capacity is

$$\boxed{C_{\rm use}(p)=1-h_2(p),\quad h_2(p)=-p\log_2 p-(1-p)\log_2(1-p).} \tag{3}$$

The **same** relational quotient permits $p=1/2$, yielding zero bits per use, or $p=0$, yielding one bit per use, and a continuum of intermediate capacities. For example, $p=3/8$ yields $C_{\rm use}\approx0.0455659971$ bits per admitted use. These are standard discrete-channel calculations (Shannon 1948). The *use* is a specified procedural operation, not a physical second, a temporal cycle, or an intrinsic clock.

This is an exact underdetermination result for the proposed interpretation: invariance and relational opposition by themselves do **not** determine a channel law or information capacity. An allowed effect family, source statistics, and operational repeatability must be selected or independently derived.

## 6. Tensor-copy comparison and the surviving sign ambiguity

Consider the two-event Hermitian comparator

$$D_t=\begin{pmatrix}1/2&it\\-it&1/2\end{pmatrix},\quad |t|\le1/2,$$

assigns identical **single-copy Boolean event scores** for all $t$. Under separately *stipulated* tensor-product source composition, the nonproduct two-copy event $\{(0,1),(1,0)\}$ has score

$$\mu_{t,s}=\frac12+2ts.$$

For $|t|=|s|=1/4$, this gives $5/8$ for matching relative signs and $3/8$ for opposing signs. With identical copies, only $t^2$ is seen, and $t\leftrightarrow-t$ remains unidentifiable. With several nonzero sources whose pair comparisons are admitted, the signs of the measured deviations $\mu_{ij}-1/2$ obey the same positive-cycle constraints as the binary proxy in Section 4, **provided** they factor as $2t_it_j$.

This is a mathematical structural parallel between a signed gauge quotient and tensor-copy orientation ambiguity. It is **not** a proof that the two mathematical models share one ontological root. A fixed oriented reference can identify a sign *relative to that reference*; it does not derive an absolute physical orientation or a fundamental clock.

## 7. A finite obstruction to deterministic quantum-channel aggregation

Let $d(\rho,\sigma)=\tfrac12\|\rho-\sigma\|_1$ denote trace distance. The two normalized positive comparison matrices are

$$D_\pm=I_4/4\pm\tfrac18(|a\rangle\langle a|-|b\rangle\langle b|),\quad
 a=(1,1,0,0)^T/\sqrt2,\ b=(0,0,1,1)^T/\sqrt2.$$

For $M=\left(\begin{smallmatrix}1&1&0&0\\0&0&1&1\end{smallmatrix}\right)$, direct exact calculation verifies

$$d(D_+,D_-)=\tfrac14,\quad d(MD_+M^T,MD_-M^T)=\tfrac12.$$

No **deterministic CPTP channel** can reproduce both proposed outputs because CPTP maps contract trace distance. The minimax two-input deterministic approximation error is exactly $1/8$, attained by conventional measure-and-group processing. The conventional heralded Kraus filter $K=M/\sqrt2$ succeeds with probability $1/2$ on both states, conditional on which the outputs are exact. Its success flag/failure branch is an **additional conventional quantum instrument**. These results do not invalidate generalized event-kernel aggregation, but prohibit conflating that map with a universal deterministic physical quantum channel.

For a normalized Hermitian kernel $D=R+iB$, complete labelled nonproduct two-copy Boolean scores determine $D$ up to $B\mapsto-B$, equivalent to global complex conjugation. All identical-copy Boolean event weights preserve that conjugation ambiguity. This mathematical determination does not select the underlying effect class as physically accessible.

## 8. Bandwidth and the absence of a physical spectral parameter

For this exploratory hypothesis the term *afrequent* must **not** be translated into a limiting value of frequency. It states that physical periodicity, wavelength and temporal frequency are not assumed to be fundamental descriptions. An elementary ambiguity illustrates why a spectral-width assignment does not emerge from a bare abstract sign exchange.

Even if one imports the two-dimensional representation $Q=\left(\begin{smallmatrix}0&1\\1&0\end{smallmatrix}\right)$ with $Q^2=I$ and then separately chooses an operator $A_\alpha=\alpha Q$, its spectral range is $2|\alpha|$. The representation alone does not choose $\alpha$, physical units, a temporal generator, or an experimentally calibrated spectral bandwidth. This is a demonstration of **representation dependence**, not a declaration that physical frequency can never emerge in an effective theory.

Hartley's 1928 transmission analysis explicitly links physical frequency range and transmission duration; Shannon's 1948 model distinguishes discrete communication problems from band-limited continuous channels. Their theorems are useful comparisons, not foundational premises about a putative prephysical structure.

## References

- F. Harary and J. A. Kabell, *Counting Balanced Signed Graphs Using Marked Graphs*, **Proceedings of the Edinburgh Mathematical Society** 24 (1981), 99–104. https://www.cambridge.org/core/journals/proceedings-of-the-edinburgh-mathematical-society/article/counting-balanced-signed-graphs-using-marked-graphs/4FC857BB402340C68D4694FC2D046231.
- S. D. Bartlett, T. Rudolph, and R. W. Spekkens, *Reference frames, superselection rules, and quantum information*, **Reviews of Modern Physics** 79, 555 (2007). https://doi.org/10.1103/RevModPhys.79.555.
- L. Diósi, *Anomalies of Weakened Decoherence Criteria for Quantum Histories*, **Physical Review Letters** 92, 170401 (2004). https://doi.org/10.1103/PhysRevLett.92.170401.
- P. Boës and M. Navascués, *Composing decoherence functionals*, **Physical Review A** 95, 022114 (2017). https://doi.org/10.1103/PhysRevA.95.022114.
- R. V. L. Hartley, *Transmission of Information*, **Bell System Technical Journal** 7, 535–563 (1928). https://doi.org/10.1002/j.1538-7305.1928.tb01236.x.
- C. E. Shannon, *A Mathematical Theory of Communication*, **Bell System Technical Journal** 27, 379–423 and 623–656 (1948). https://www.princeton.edu/~wbialek/rome/refs/shannon_48.pdf.
- Wigner symmetry theorem comparison: *Two Elementary Proofs of the Wigner Theorem on Symmetry in Quantum Mechanics*, **Physics Letters A** 372 (2008), 6847–6852. https://doi.org/10.1016/j.physleta.2008.09.052.
