# Following one velocity with successive position records on a reflecting walk

**Kirtus Justus**, Theoretical Physicist, Port Coquitlam, British Columbia, Canada. Research supplement by Director G (OpenAI Codex).

Launch a walker at one well. At several times, record which part of the interval it occupies while preserving coherence among the wells in that part. The joint records converge to the positions of a classical particle with **one velocity drawn at launch** and elastic wall reflections. The velocity varies continuously across the ensemble even when every launch starts at the same site on the same rail. Each marginal alone is compatible with a new velocity drawn for every observation. Three binary records on the same walker distinguish these predictions. The calculation assumes ordinary probabilities and a specified coherent measurement of each region.

## The instrument and the joint law

Use wells \(0,\ldots,L-1\), the uniform real Hadamard coin and opposite directed shifts. An outward step at a wall stays there for one tick and reverses rail with amplitude \(+1\). The physical coordinate is \(z_x=(x+1/2)/L\). Start at \(x_0/L\to y\in[0,1]\) with fixed unit rail vector \(u\). At increasing ticks \(t_j/L\to\tau_j\) on a bounded time interval, divide position into finitely many bins. Reading bin \(B_j\) applies the projector onto **all** wells and both rails in that bin. The probability of a word is the squared norm after the successive projections and intervening walk steps. Each individual read has this update even when its bin label is only one bit. [Step, signed unfolding and one-time limit](Reflecting_wells_and_the_classical_limits_of_a_walk.md)

Write \(F(s)=\operatorname{dist}(s,2\mathbb Z)\). On the unfolded cycle let \(U(k)=\operatorname{diag}(e^{ik},e^{-ik})H\), \(e^{i\omega_b(k)}\) its eigenvalues, \(P_b(k)\) their orthogonal projectors and \(v_b(k)=\omega'_b(k)\). Draw \(k\) uniformly from \([0,2\pi)\) and then band \(b\) with probability \(\|P_b(k)u\|^2\). Put \(V=v_b(k)\), which lies in \([-1/\sqrt2,1/\sqrt2]\).

**Joint limit.** For each fixed finite word of bins whose boundaries have zero probability at the corresponding limiting clocks,
\[
 \lim_{L\to\infty}\Pr_L(B_1,\ldots,B_d)
 = \int_0^{2\pi}\sum_b\|P_b(k)u\|^2
       \prod_{j=1}^d {\bf1}_{B_j}\!\left(F(y+\tau_j v_b(k))\right)\frac{dk}{2\pi}.
\]
Thus a first record updates the distribution of the velocity used at the later reads by ordinary conditioning, for any prefix of positive limiting probability. Paths can meet at the same well, retain different velocities and separate later. The statement includes paths that reflect one or more times. For positive \(\tau_j\), every finite list of interval endpoints qualifies. Each band velocity is a nonconstant analytic function, and the preimages of a specified folded coordinate have zero momentum measure. At time zero the launch position can be entered as known.

### Why the same velocity survives each record

Unfold to \(2L\) sites using the [signed rail permutation](Reflecting_wells_and_the_classical_limits_of_a_walk.md#unfolding-the-interval-and-its-reflection-phase). At each clock the two lifts of a physical well have opposite parity, and a sharp launch occupies just one parity of the cycle. Multiplication by a physical function \(f(z)\) lifts to \(f(F((J+1/2)/L))\). For odd \(L\) a negative wrap changes the momentum grid from \(k_n=\pi n/L\) to \(k_n=\pi(n+1/2)/L\); the argument below works on both grids.

Use the positive-sign Fourier transform with grid-mean norm. In the frame of the source a test state has momentum profile \(e^{ikx_0}a(k)\), with \(a(k)=u\) initially. A cycle position mode \(e^{i\delta(J+1/2)}\), \(\delta=\pi m/L\) for fixed integer \(m\), in the Heisenberg picture at tick \(t\) takes \(a\) to
\[
 e^{i\delta(x_0+1/2)} U(k)^{*t} U(k+\delta)^t a(k+\delta).
\]
Both momentum grids are closed under this shift. On any continuous periodic profile and for \(t/L\to\tau\), this differs uniformly on the grid by \(o(1)\) from applying the matrix
\[
 A_{m,\tau}(k)=\sum_b e^{i\pi m(y+\tau v_b(k))} P_b(k).
\]
Indeed the two eigenphases are \(\arcsin(\sin k/\sqrt2)\) and its supplement. Their spectral gap bounds the projector derivatives. Cross terms contain \(P_b(k)P_c(k+\delta)=O(|\delta|)\) for \(b\ne c\), independently of their oscillatory phases. The diagonal phase remainder after taking the first derivative is \(O(t\delta^2)\). Continuity handles the shift of \(a\).

By uniform trigonometric approximation on the cycle the corresponding assertion holds in grid-mean norm for every continuous folded multiplier \(f\). Its limiting matrix is \(\sum_b f(F(y+\tau v_b(k)))P_b(k)\). A fixed product converges on the initial vector by telescoping. At each step apply the just-proved approximation to the continuous product of the preceding limiting matrices acting on \(u\); the exact operators have norm bounded by the suprema of the multipliers. The limiting matrices share the same two projectors for every time. Their product acts on each band by the product of the scalar functions, so its squared norm integrated over \(k\) gives the joint rule with squared continuous amplitudes.

For a hard bin, choose multipliers \(0\le f_\epsilon\le1\) agreeing with its indicator off an \(\epsilon\)-neighborhood of its boundary. Bound their squared discrepancy by a continuous function \(0\le g_\epsilon\le1\) supported in a slightly larger neighborhood and equal to one on the transition region. In the product error keep the exact projectors on the left and the earlier continuous multipliers on the right. In each term the squared norm of replacing a projector is bounded by the expectation of \(g_\epsilon\) at that clock on the preceding smoothed branch. The continuous calculation bounds its limiting value by the original marginal mass of the enlarged neighborhood, since earlier factors have squared modulus at most one on each band. For finitely many clocks the sum of the square roots of these bounds tends to zero. This proves the indicator formula, including zero-probability words. The same approximation for inner products shows that two different words in the same fixed partitions have vanishing limiting branch overlap, even if their final bins agree.

The Fourier method for the single-clock velocity distribution goes back to Grimmett, Janson and Scudo. Borns-Weil and Oltman proved convergence of repeated indirect records for quantized torus maps with Hamiltonian or metaplectic evolution. Here the signed wall unfolding, two band projectors and discontinuous physical bins enter explicitly. An earlier program result gives [records of two prepared rays in a reversing field](Sequential_position_records.md); the sharp launch here supplies an entire velocity distribution. [Single-time walk theorem](https://arxiv.org/abs/quant-ph/0309135) · [Quantum trajectories for torus maps](https://arxiv.org/abs/2210.03224)

## Which source information appears in the track?

Let the sharp-source rail state have Bloch vector \((s_X,s_Y,s_Z)\), allowing a mixed state by linearity. Its velocity density on \(|v|<1/\sqrt2\) is
\[
 \frac{1+(s_X+s_Z)v}{\pi(1-v^2)\sqrt{1-2v^2}} .
\]
In our convention the positive branch (eigenphase \(\omega=\arcsin(\sin k/\sqrt2)\)) has projector \((U+e^{-i\omega}I)/(2\cos\omega)\). Its Bloch components along \(X,Z\) are both \(v(k)\); its \(Y\) component is odd in \(k\). Momentum reflection cancels the latter in the velocity measure. Shifting momentum by \(\pi\) exchanges the bands with identical velocity and projector, giving the stated tilt after the change of variable \(k\mapsto v(k)\). This recovers the one-dimensional Hadamard density with the present orientation of the rails. In consequence *every* limiting coarse word above depends on the unknown source coin only through \(s_X+s_Z\). Conversely, for an interior launch choose a positive clock so early that neither velocity edge can reach a wall. Recording on which side of \(y\) the walk arrives gives right probability \(1/2+(s_X+s_Z)/4\), since the positive-velocity integral of \(v/[\pi(1-v^2)\sqrt{1-2v^2}]\) is \(1/4\). This single limiting frequency identifies exactly the tilt. [Konno, one-dimensional quantum random walk](https://arxiv.org/abs/quant-ph/0206103)

For example a sharp right rail and the equal in-phase rail superposition have the same tilt, hence the same limiting family of track records. A microscopic one-tick measurement to the right of an interior source gives \(1/2\) and \(1\) respectively. This supplies a finite control for information lost on the ballistic scale. Complex-conjugate input coins pose a different obstruction: every finite record amplitude in a real walk with real projectors is conjugated when the input is conjugated, leaving its norm unchanged. This also holds for a choice of real gates made conditionally on the observed prefix. Detecting the sign of the imaginary rail coherence would require a relative phase reference. [Program result on real position effects](Two_coin_position_read_at_one_contact.md)

There is an exact measurement of the source’s real coin coordinates on the same family. At the left endpoint launch the unknown coin and take three free ticks on \(L\ge4\) wells. In well order \(0,1,2,3\) the effects have triples \((E_{RR},E_{LL},E_{RL})\), in eighths, of \((1,5,-1),(5,1,1),(1,1,-1),(1,1,1)\). These follow by evolving each source rail and taking the two returned columns’ Gram matrix at each well. In particular \(8P_3=1+s_X\) and \(8P_1=3+s_X+2s_Z\). Thus one microscopic position histogram recovers both real coordinates, including for mixed inputs. Conversely, any one-copy transcript built only from real controls and measurements depends on these two coordinates through a real symmetric effect. A relative \(+i\) phase placed on the left rail before \(H\) would give the right-going probability \((1-s_Y)/2\). Such a phase operation introduces the reference missing from the real carrier. The [finite Lean check](lean/ReflectedHistories.lean) verifies the four effect triples and the four-well three-clock word table.

## From a word to a track

Fix a duration \(T\). At resolution level \(n\), choose finitely many times across \([0,T]\) with spacing at most \(1/n\) and finite interval bins of diameter at most \(1/n\). At time zero use the known source. Round each positive observation time to the nearest tick. For fixed \(n\) the full word law converges in total variation, because the alphabet is finite and every word converges. Choose lengths \(L_n\) increasing so that, at that level, every \(L\ge L_n\) has distinct attained ticks and word-law error below \(1/n\). These thresholds exist for both parities. Use level \(n\) until the next threshold.

Join the reported bin centers linearly and enter the known start. Couple this word to the ideal word from one draw of \(V\) by a maximal coupling. On a matching word the uniform interpolation error relative to the ideal reflected curve is at most the bin diameter plus the maximum time gap times \(1/\sqrt2\), with \(O(1/L)\) for clock rounding and the vanishing source-coordinate error at the initial endpoint. Thus the interpolated record laws converge weakly on continuous paths with the uniform metric. This is an existence result for increasingly fine schedules. It does not assign an error rate to an arbitrary growing schedule. In particular a complete site read at each microscopic tick instead gives the [reflected Markov chain](Reflecting_wells_and_the_classical_limits_of_a_walk.md#recording-the-well-after-every-tick).

## An observable requiring three records

Take \(y=1/4\), sharp right rail, and left/right half-interval reads at \(t/L=1/2,1,2\). Use 0 for the left half and 1 for the right. Give the middle boundary to the right. To compute the limiting table split velocity space wherever \(y+\tau_j v\) is a half-integer and intersect with the allowed velocity support. For a right-rail launch, writing \(v(k)=\cos k/\sqrt{1+\cos^2 k}\), the two-band velocity measure is the pushforward of \((1+v(k))\,dk/(2\pi)\) by \(v(k)\). This follows from the band weights \((1\pm v(k))/2\) and the change \(k\mapsto k+\pi\). For \(|v|<1/\sqrt2\), put \(a=\arccos(v/\sqrt{1-v^2})\). Integration over the monotone half of the momentum circle yields the CDF \(1-[a+\arcsin(\sin a/\sqrt2)]/\pi\). The endpoints have zero mass.

| Recorded halves | One shared velocity | Independent draws at the same absolute times |
|---|---:|---:|
| 000 | 0.149137 | 0.084714 |
| 001 | 0.194610 | 0.087160 |
| 010 | 0 | 0.161728 |
| 011 | 0.156253 | 0.166398 |
| 100 | 0 | 0.084714 |
| 101 | 0 | 0.087160 |
| 110 | 0.343747 | 0.161728 |
| 111 | 0.156253 | 0.166398 |

The independent-draw column preserves all three one-time marginals by drawing a fresh velocity for the displacement from the same origin at each absolute time. At 1,024 wells the microscopic three-read distribution lies 0.002475 in total variation from the shared-velocity column and 0.354729 from the independent column. The combined finite probability of 010, 100 and 101 is 0.000894; the limit gives those words zero mass. The [checker](check_reflected_histories.py) uses integer amplitude numerators, sums all retained branch norms, and cross-checks the four-well case against every one of the 256 microscopic direction words. The [numerical record](results/reflected_histories.json) keeps every observed word at all six lengths and the uninterrupted final marginal.

The same first bin probability can come from two instruments with different effects on the next observation. In a two-clock interior control, a near-launch first record followed by a distant second record has limiting probability zero under a coherent bin read. Measuring and then discarding the exact well at the first clock raises its limiting inferior probability to at least 0.06576027. This comparison keeps both rails within each exact well and retains all incident outcomes. [Operations, proof and exact integer replay](One_exact_site_record_changes_a_ballistic_history.md)

Loss, phases written inside a bin, or partial which-site information require an independently specified instrument. The clocks, coherent coin and boundary phases are supplied in the model. No experimental trajectory data enter this theorem. Explaining the preparation, ordinary readout and physical correspondence remains open.
