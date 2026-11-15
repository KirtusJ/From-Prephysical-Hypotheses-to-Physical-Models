# Certifying a coherent half-interval measurement with short walk returns

**Kirtus Justus**, Theoretical Physicist, Port Coquitlam, British Columbia, Canada. Research supplement by Director G (OpenAI Codex).

The [reflected trajectory theorem](Reflected_position_histories.md) requires a measurement of a region that preserves the relative amplitudes of all occupied wells and rails inside it. A detector can display the right region on every localized input and still destroy that coherence. Here **zero-flight and two-tick return experiments determine the entire visible measurement operation** for a cut dividing the interval into two contiguous end regions. The input menu has \(3L\) preparations on \(L\) wells. The result covers arbitrary stationary completely positive instruments on the stated input space, including incorrect labels, disturbance and visible leakage. It assumes ordinary probabilities, trusted source preparation, a reversible walk and a separate measurement of return to one full directed source mode.

## The experiments

Use \(L\ge4\) wells and the real Hadamard step \(U\) of the [reflecting interval](Reflecting_wells_and_the_classical_limits_of_a_walk.md). An outward shift holds one tick and reverses the rail with positive sign. Choose any cut between neighboring wells, and write \(b(i)\) for the side of directed mode \(i=(x,r)\). The target measurement reports \(b\) and outputs the unnormalized walk state \(P_b\rho P_b\), with \(P_b\) the projector onto that side. The record is classical. An extra failure label or orthogonal leakage space is allowed and included in the incident exposure.

1. For each of the \(2L\) modes \(i\), prepare it sharply, use the instrument once and read the output mode independently. Measure \(a_i\), the joint probability of label \(b(i)\) and return to \(i\). The ideal value is one.
2. For each well \(s\), launch rightward there, apply two ticks, use the instrument once, isolate its classical label, apply the trusted inverse two ticks and test return to \((s,R)\). Let \(h_{sb}\) be the *joint* probability of label \(b\) and that return. Put \(u_s=U^2|s,R\rangle\), \(p_{si}=|\langle i|u_s\rangle|^2\) and \(p_{sb}=\sum_{i\in b}p_{si}\). The ideal value is \(p_{sb}^2\). Both sides are read on the same setting. A zero return on an empty arm needs no division.

Different choices of source and flight length must expose the same instrument in the same state of readiness. Its output label alone cannot serve as the independent directed-mode check in step 1. A loss or wrong mode contributes zero to the joint pass; discarding these outcomes would change the tests. The inverse acts on the visible walk, with an independently specified extension on any extra visible output modes.

## Identification on all inputs

Represent the instrument by an isometry \(W\) to the visible output and an environment. Use orthogonal outcome sectors \(E_b\) in that environment, read the sector as the classical label and trace out its private coordinates. This is the Kraus representation with a private index for each outcome. When \(a_i=1\), the output must be \(W|i\rangle=|i\rangle e_i\) for a unit vector \(e_i\in E_{b(i)}\). Here tensor products with the environment are implicit. Thus perfect basis tests establish the diagonal-tag form. No such form was imposed on the untested instrument.

In this form the joint return is \(h_{sb}=\|\sum_{i\in b}p_{si}e_i\|^2\). Consequently
\[
 p_{sb}^2-h_{sb}=\sum_{i<j,\ i,j\in b}p_{si}p_{sj}\|e_i-e_j\|^2 .
\]
The right-hand side retains relative phases as well as distinguishable private records. Draw an edge between modes in one bin when some two-tick source populates both. An ideal return makes their environment vectors equal. Connectedness inside each bin then leaves a single environment vector \(e_b\) there. Linearity gives \(P_b\rho P_b\) at that label for every density matrix, including inputs entangled with an external spectator.

**Why two ticks work at a boundary.** Each sharp \(R\) source \(x\) returns to \((x,R)\) and \((x,L')\) with amplitude of magnitude \(1/2\) at time two, including endpoint launches. Here \(L'\) denotes the left rail. The \(RR\) departure word also reaches \((x+2,R)\) wherever \(x+2<L\), with magnitude \(1/2\). Thus both rails at each well and every pair of wells separated by two inside the bin are linked. The launch at 0 additionally populates \((1,R)\) together with the rails at 0, since an initial left proposal reflects on the spot. At the opposite end the launch at \(L-1\) populates \((L-2,L')\) together with the rails at \(L-1\). Each bin touches one end. If it has at least two sites, this link joins its odd and even site chains. A one-site bin already has its rails joined. The cut location and the odd or even parity of the total number of wells are unrestricted. Every argument uses actual nonzero signed amplitudes. At two ticks each of the four direction words ends at a different mode.

Conversely, a disconnected co-occupation graph permits different scalar phases on different components of a bin. Such a phase operation passes every sharp-mode and supplied return test, while rotating a balanced superposition on two components to an orthogonal state. With only one free tick and one sharp directed source per preparation, even allowing both launch rails, the two outgoing modes from each site form a disjoint pair after the shift. Restricting those pairs to two spatial bins cannot connect the larger bin’s more than two modes. Thus a two-tick maximum flight length is necessary within this particular family of sharp launches and clean return tests. More general source or reference operations can give a different resource count.

This is an application of channel identification from pure-state tests to a classical-label instrument. Spanning and a connected nonorthogonality graph are established criteria for identification of a unitary channel. The present tests use projected return amplitudes on a nonunitary target and exploit the boundary walk to connect the modes with a short, explicit menu. [Mayer and Knill, *Quantum Process Fidelity Bounds from Sets of Input States*](https://arxiv.org/abs/1805.04491)

## A finite-error bound

Let \(e_i\) be the normalized projection of \(W|i\rangle\) on the joint subspace “output \(i\), label \(b(i)\),” retaining the environment part. When \(a_i=0\) choose any unit vector in that sector, enlarging an unused environment if needed. Define
\[
 W_0|i\rangle=|i\rangle e_i,\qquad
 r_i=\sqrt{2-2\sqrt{a_i}},\qquad r=\left(\sum_i r_i^2\right)^{1/2}.
\]
The phase choice in this definition gives \(\|(W-W_0)|i\rangle\|=r_i\). Cauchy–Schwarz bounds the operator norm \(\|W-W_0\|\) by \(r\). For a particular \(u_s\) use the smaller bound \(r_s=\min(r,\sum_i\sqrt{p_{si}}r_i)\). The second sum uses at most four modes. Projecting the output in label \(b\) onto the source-return amplitude is a contraction. Hence for the diagonal comparison \(W_0\) the norm of its returning environment amplitude is at least \(\max(0,\sqrt{h_{sb}}-r_s)\). Define
\[
 \Delta_{sb}=p_{sb}^2-\max(0,\sqrt{h_{sb}}-r_s)^2 .
\]
For probabilities from a channel satisfying the assumptions, \(\Delta_{sb}\ge0\). For an edge \(i,j\) in bin \(b\) each source populating that edge gives the upper bound
\[
 \|e_i-e_j\|\le
 \min\!\left(2,\sqrt{\Delta_{sb}/(p_{si}p_{sj})}\right).
\]
Use the smallest bound over those sources as the edge length. In each bin take a root minimizing the largest shortest-path distance to another vertex, and let \(D\) be the maximum of the resulting radii. Replacing every \(e_i\) by its bin root tag changes \(W_0\) in operator norm by at most \(D\): its output differences at different directed modes are orthogonal. The resulting isometry \(W_*\) implements the ideal classical-label instrument. Its environment tags on distinct bins are in orthogonal labeled sectors.

For any input with any spectator, the trace distance between the actual and ideal classical-label-and-walk outputs is therefore at most
\[
 \epsilon=\min(1,r+D).
\]
Indeed one can purify the input, bound the distance between the two pure outputs by their vector norm difference, and then read the sector and discard the environment. Tensoring the identity on the spectator leaves the isometry norm bound unchanged. This bounds half the diamond norm of the channel difference. It is sufficient and can be loose; the [stationary diagonal-tag estimate](Calibrating_hidden_tags_with_a_source_return.md) gives a sharper bound when diagonality itself is known. These formulas use population probabilities. Simultaneous lower bounds on \(a_i,h_{sb}\) from data can be used in the same monotone inequalities. Inconsistent estimates require checking the preparation, instrument model and uncertainty.

For a fixed schedule of \(k\) measurements with a reset private apparatus on each use, replace one actual read at a time by its ideal read. Contractivity of every intervening channel, including subsequent processing of recorded labels, bounds the total error by \(\min(1,\sum_{j=1}^k\epsilon_j)\). For adaptive settings use a uniform bound over the possible matched settings at each step. This transfers the [reflected-history law](Reflected_position_histories.md) at fixed clocks if the sum tends to zero. For growing schedules one also needs the ideal schedule’s own convergence and a vanishing total instrument error. The quantitative bound contains the number of modes and a graph radius; an error bar fixed across growing systems need not suffice. An apparatus that writes a private bit during validation and reads it on the next science use is a different process. A [whole-sequence return test](Testing_the_state_left_by_a_position_word.md) covers the visible state and word produced by a particular such sequence.

## Finite controls and the role of the wall

At eight wells with bins \(0{:}3\) and \(4{:}7\) (both endpoints included), put a minus sign only on \((1,R)\) inside the first bin. All sixteen basis returns remain one. The two-tick rightward launch from 0 puts mass \(1/4\) on that mode, so its joint left-label return falls from 1 to \(1/4\). A rotation exchanging amplitude between two modes of one bin, with cosine \(3/5\) and sine \(4/5\), instead leaves its label intact but lowers the sharp-mode return at either mode to \(9/25\).

For the interior bin \(2,\ldots,5\) on the same carrier, put phase \((-1)^x\) inside the bin and phase \(+1\) elsewhere. Every zero-, one- and two-tick sharp-source return passes, yet a balanced test between wells 2 and 3 inside that bin returns an orthogonal state. More generally if every allowed flight is too short for a wall hold followed by arrival in the bin, all its occupied modes from a sharp launch have one site parity at that clock. The phase is then constant on that branch. This control identifies the hypothesis that a bin reaches the wall; it makes no all-time claim for interior bins.

The [integer replay](check_two_tick_instrument.py) checks the two-tick columns against explicit physical words for every launch at all lengths 4 through 40, tests every boundary cut, and retains the disconnected and wrong-phase controls. A separate [Lean 4.19 calculation](lean/TwoTickInstrument.lean) checks the port-level links and parity control at eight wells. The [result record](results/two_tick_instrument.json) is model output. Performing these measurements and bounding acceptance, source and gate errors on a physical walk remain open. The certificate tests a measurement within the ordinary operational theory; it does not derive that probability theory from prephysical primitives.
