# Finite detector memory and coherent returns on the electric string

**Kirtus Justus**, Theoretical Physicist  
Port Coquitlam, British Columbia, Canada

Research supplement by Director G (OpenAI Codex).

Repeatedly tilt one bond of the localized two-occupant string and read the launch port only at the end. A time-homogeneous classical detector with at most \(m\) internal states must differ from the ordinary return probabilities at one of the first \(m+2\) read times. The states in this bound include every classical degree of freedom that can carry information from one tilt to the next. If their number is unrestricted, a single globally normalized finite model can match any prescribed finite tree of the rational gates and ideal sharp coordinate reads defined below, including adaptive decisions. Whether a physical comparison with a separate pointer is equivalent to such terminal reads requires its own instrument premise. [Separated preparations and records](Separated_string_records.md)

## Any given finite panel has a finite realization

Fix the array size, sharp sources and a finite tree of experiments with terminal coordinate reads. A branch may continue with a new word selected by its outcome, taking the post-read state to be the corresponding sharp coordinate. Use the addressed rational controls, inverse controls when available, and the uniform rational electric pulse. All pure projectors then have entries in \(B=\mathbb Z[i,1/5]\).

Collect the exact projectors reached at every read, including every coordinate projector. A sufficiently large integer \(h\) has two properties. First, reducing entrywise modulo \(3^h\) separates all distinct projectors on this list. Second, every nonzero row of every listed projector survives. To see both, take one nonzero numerator component from each distinct matrix difference and from each nonzero row. The denominators are powers of 5 and only finitely many integers need to survive. Reduction commutes with complex conjugation. The ring \(B/3^hB\) is finite and admits unitary inverses for the reduced gates.

Use the full reduced projector as a classical state. Each addressed gate \(G\) acts deterministically by \(P\mapsto \bar G P\bar G^*\), where the bar in this expression denotes reduction. At a coordinate read, give each stored panel state the ordinary vector of diagonal probabilities of its exact representative. For an unlisted key, distribute the unit mass equally among its nonzero rows. At least one row is nonzero because the trace is one in the quotient. Reset to the reduced sharp coordinate for the port observed. This gives one normalized detector and one fixed gate action for every word, with exact agreement on the finite tree by conditional multiplication. It never assigns a click to an exactly zero coordinate. A zero exact coordinate has an all-zero projector row; if the resulting key is pinned, the row-survival test prevents a positive table entry there. True nonzero probabilities can disappear outside the tested panel.

In the four-site example, 39 input rows contain 33 distinct exact projectors. Modulo \(3,9,27,81\) the respective counts of distinct keys are \(6,25,32,33\). The numbers of distinct colliding pairs with different read distributions are \(90,10,1,0\). Positive coordinates disappear at \(66,25,6,0\) entry–port pairs, distributed over \(28,18,6,0\) of the 39 input entries, respectively. The resulting modulus-81 detector agrees on all 36 bins of an adaptive two-read experiment. On an unlisted preparation with a phase pulse it gives \(1/3\) at each of three surviving coordinates; the ordinary probabilities there are \(9/25,256/625,144/625\). After 54 tilts it returns the reduced sharp source with certainty, while the ordinary probability is approximately \(0.96375864\). The checker retains the lower-modulus collisions, all zero bins and the exact return fractions. [Checker](check_finite_record_memory.py) · [Stored projectors, collisions and branch records](results/finite_record_memory.json)

The response is a function of the state reaching the coordinate detector. Two completions of the same backward rank-one effect can produce different full terminal states. The construction imposes no global equality across such completions. The result applies to ideal sharp resets; an unresolved coarse click requires its own instrument. It gives no upper bound on the size of the state space needed by a physical apparatus.

## A detector with a bounded number of states

Launch \(01\), apply \(k\) copies of \(R_{12}\) with \(\cos\theta=3/5,\ \sin\theta=4/5\), and read \(01\). The predicted ordinary return is

\[
 q_k=\cos^2(k\theta)=\tfrac12+\tfrac14(z^k+\overline z^{\,k}),\qquad z=e^{2i\theta}=(-7+24i)/25 .
\]

The phase \(z\) has infinite order since \(z+\overline z=-14/25\) is rational and is not an integer. A root of unity and its inverse have an algebraic-integer sum. In the finite classical model write \(p_k=\alpha P^k b\), where \(P\) is a fixed \(m\times m\) row-stochastic matrix, \(\alpha\) the launch distribution, and \(b\) a column of terminal click probabilities in \([0,1]\). The same launch and read must be used across all \(k\). Known tilt counts can be used to schedule the terminal measurement externally. Supplying that count to the detector as an additional input changes this model.

**Finite bound.** Let \(m\ge1\) be an integer and suppose that every read probability is \(p_k=\alpha P^k b\) with the same launch distribution \(\alpha\), row-stochastic transition matrix \(P\) on at most \(m\) states and read column \(0\le b_i\le1\). Pad a smaller matrix with unreachable absorbing states, preserving every \(p_k\), to obtain the stated dimension \(m\). With \(\eta_m=(1-\max_{1\le r\le m}q_r)/(2m)>0\),

\[
 \max_{0\le k\le m+1}|p_k-q_k|\ \ge\
 \frac{24}{25\,2^{m+1}}\,\eta_m^{\,m-1}.
\]

**Proof.** Write \(\chi(x)=\sum_{j=0}^{m}c_j x^j=\det(xI-P)\). Cayley–Hamilton gives \(\sum_j c_jp_{k+j}=0\) for each \(k\). Because \(\chi(1)=0\), the corresponding ordinary residual is \(\frac12\operatorname{Re}[z^k\chi(z)]\). At \(k=0,1\), its maximum absolute value is at least \(\tfrac12|\chi(z)|\sqrt{(1-|\operatorname{Re}z|)/2}\). Indeed the two real projections along axes at angle \(\arg z\) have squared sum at least \((1-|\operatorname{Re}z|)|\chi(z)|^2\). All eigenvalues of \(P\) have modulus at most one, so \(\sum_j|c_j|\le2^m\). It remains to bound \(|\chi(z)|\).

Let \(d=\min_{1\le r\le m}|1-z^r|\). For an eigenvalue \(\lambda\), scale a right eigenvector \(v\) so that \(v_i=1\) and \(|v_j|\le1\). A Markov chain starting at \(i\) has \(\mathbb E_i v(X_k)=\lambda^k\). Therefore

\[
 \mathbb E_i|v(X_k)-z^k|^2
 \le 2\bigl(1-\operatorname{Re}(\overline z^{\,k}\lambda^k)\bigr)
 \le 2|z^k-\lambda^k|\le 2k|z-\lambda|.
\]

If \(|z-\lambda|<d^2/(8m)\), each of \(1,z,\ldots,z^m\) would have one of the \(m\) eigenvector coordinates strictly within \(d/2\). Their mutual separation is at least \(d\), so the \(m+1\) open disks are disjoint. This is impossible. Since \(d^2/(8m)=\eta_m\) and one eigenvalue equals 1, we have \(|\chi(z)|\ge |z-1|\eta_m^{m-1}\). Substitution and \(|z-1|=8/5,\ \sqrt{(1-|\operatorname{Re}z|)/2}=3/5\) give the claim. This estimate only needs two characteristic residuals. Sharper spectral information is available from the region of eigenvalues of stochastic matrices. [Johnson and Paparella](https://arxiv.org/abs/1611.06970)

For three states the read count is attained. Start in state 0, move deterministically \(0\to1\to2\), and from state 2 go to states 0 and 2 with probabilities \(779/900,121/900\). Give the states read probabilities \(1,9/25,49/625\). The model agrees at \(k=0,1,2,3\), including \(q_3=13689/15625\). At \(k=4\) it gives \(167729/390625\) against \(277729/390625\), a gap of \(176/625\). The bound need not be optimal for other state counts, and its displayed tolerance can be very small. A statistical application requires uncertainty below the relevant gap and evidence for the memory bound and reproducibility of the gate. [Exact finite checks](check_return_memory_bound.py) · [Fractions and controls](results/return_memory_bound.json)

## A sharp three-read test for two-state mixtures

**Two-state mixture interval.** Prepare the same sharp pair and read the same return port after zero, one or two tilts on fresh trials. Each trial draws one type independently of the requested tilt count and retains it throughout the run. Conditional on that type the response is \(\alpha P^k b\) for one launch distribution, one row-stochastic matrix on at most two states and one fixed terminal column \(0\le b_i\le1\). The type distribution is arbitrary and common to all three read times.

Write $t=p_0$, $s=p_1$. Define $L(0,s)=0$ and, for $t>0$,
$$
L(t,s)=\frac{\max(0,t+s-1)^2}{t}.
$$
For every $0\le t,s\le 1$, the attainable third reads form exactly the interval
$$
L(t,s)\le p_2\le 1-L(1-t,1-s).
$$

**Proof.** Split each type into point launches and binary read columns. This preserves all three expectations because the read is terminal and the expectations are linear in the initial distribution and in the read column separately. A type whose launch state clicks has first-step click probability $x$. With one click state and one dark state, its two-step probability is $x^2+(1-x)y$, where $y$ is the probability to move from dark to click in one step. This is at least $x^2$. The constant click column satisfies the same inequality.

The types that click at launch have total mass $t$. Their contribution $m$ to $s$ is at least $\max(0,t+s-1)$ because the remaining mass can contribute at most $1-t$. For $t>0$, Cauchy–Schwarz gives $p_2\ge\int_{\text{click at launch}} x^2\,d\mu\ge m^2/t$ for the probability distribution $\mu$ over types. For $t=0$ the trivial lower bound is attained.

For $s\le1-t$, mix the triples $(1,0,0)$, $(0,1,0)$ and $(0,0,0)$ with masses $t,s,1-t-s$. The first comes from a click state that moves to an absorbing dark state. The second starts dark and swaps the states at every tick. For $s>1-t$, take the first type with a click-state self-loop of probability $x=(s+t-1)/t$ and an absorbing dark state. Mix its triple $(1,x,x^2)$ with the swap triple $(0,1,0)$ using masses $t,1-t$. This attains the lower bound. Complementing the terminal click gives the upper bound, and mixing the two boundary realizations at fixed $t,s$ gives the entire interval.

**Consequence for the string tilt.** Its first three coherent return probabilities are $1,9/25,49/625$. A two-state mixture that matches the first two has $p_2\ge81/625$. If all three entries can vary, their smallest possible maximum absolute error is
$$
r_* = \frac{16}{369+\sqrt{111161}} = 0.0227787787\ldots.
$$
The lower boundary is nondecreasing in both arguments. At fixed $s$, its positive branch is $t-2(1-s)+(1-s)^2/t$ for $t>1-s$. Therefore any model within $r<9/50$ requires $(9/25-2r)^2\le(1-r)(49/625+r)$, or $3125r^2-1476r+32\le0$. The smaller root is $r_*$. The lower-bound construction attains the triple $(1-r_*,9/25-r_*,49/625+r_*)$. This gives a sharp model distance in probability units. A simpler rational check for every such mixture is $625p_2-336p_0-400p_1+400\ge0$. It follows by bounding $x^2$ from below by its tangent at $x=8/25$ in the click-launch argument above. The coherent panel gives $-31$, so this linear check alone guarantees a maximum discrepancy of at least $31/1361$. Using these checks with data requires a joint uncertainty region for the three true probabilities. For instance, simultaneous bounds $p_0\ge t_-,p_1\ge s_-,p_2\le u_+$ contradict the model whenever $u_+<L(t_-,s_-)$.

Every pair of launch and first-step probabilities $(p_0,p_1)$ is possible with two-state mixtures. A homogeneous deterministic three-state chain $0\to1\to2\to2$ with read column $(1,9/25,49/625)$ reproduces this entire three-read comparison. Thus the test addresses a cap of two states per type and a type distribution independent of the requested read time. The accompanying checker evaluates finite rational controls and the polynomial certificate. The analytic interval and distance are derived above. An internal Codex challenger separately recovered the boundary, attainment and distance from the assumptions. This comparison has no empirical counts or Lean proof. [Exact checks](check_return_memory_bound.py) · [Results](results/return_memory_bound.json)

## A single detector over arbitrarily long runs

Suppose each prepared trial draws a fixed type independently of the word that will be requested, and its return response for repeated tilts is periodic with some finite period. Finite reversible classical state models, including reductions modulo any fixed finite ring, have this property. The distribution over periods may be unbounded. Given \(\varepsilon>0\), choose \(M\) so that at most \(\varepsilon\) of the mass lies on periods above \(M\); take \(L=\operatorname{lcm}(1,\ldots,M)\). At every \(Lr\) the averaged return is at least \(p_0-\varepsilon\), because the selected types return to their own launch response. For \(p_0=1\) and irrational \(\theta/\pi\), ordinary returns approach zero at some such multiples, so their supremum discrepancy is one. Stability of just this return near the signed transfer that empties the launch port would already rule out this family: for each \(L\), the powers \(R^{Lr}\) approach that transfer on the active bond. [Lean finite-mass bound](lean/PeriodicReadout.lean)

An irreversible finite classical detector can leave its launch state and stay away forever. Testing only for dark transfers then misses the distinction. For a fixed finite homogeneous stochastic matrix, however, the only peripheral eigenvalues are roots of unity, and the peripheral Jordan blocks have size one since all powers are bounded. The first assertion follows by applying the eigenvector disk argument to any infinite-order unit-modulus eigenvalue, taking that eigenvalue as the target phase. Thus each terminal response is a periodic sequence plus a term tending to zero. At the irrational frequency \(z\) its complex average \(N^{-1}\sum_{k=0}^{N-1}p_k\overline z^{\,k}\) tends to zero by the geometric-series formula. Bounded convergence passes this conclusion through any fixed probability mixture of finite homogeneous classical detectors, even with different matrix sizes and random transition probabilities. Under the ordinary calibration the same average tends to \(1/4\). A persistent nonzero coefficient at this known frequency would already exclude that mixture. A finite truncation supplies no uniform test without a resource or mixing bound. The comparison concerns classical finite-state dynamics; the finite quantum rotation itself retains an irrational phase. [Finite stochastic matrices and periodic components, Paz, chapter II](https://www.ime.usp.br/~jmstern/wp-content/uploads/2020/12/Paz1971.pdf)

If the components of a mixture each have at most \(m\) states, the Fourier test also has a finite, uniform bound. Pad smaller models with unreachable absorbing states and put \(D_m=|z-1|\eta_m^{m-1}\). By Cayley–Hamilton, \(\chi(z)(zI-P)^{-1}=\sum_{j=1}^m c_j\sum_{\ell=0}^{j-1}z^{j-1-\ell}P^\ell\). In row-sum norm its right side is bounded by \(\sum_j j|c_j|\le m2^{m-1}\), using the elementary symmetric polynomial bounds \(|c_j|\le\binom mj\). A finite geometric sum then gives \(\left|\sum_{k<N}p_k\overline z^{\,k}\right|\le m2^m/D_m\), uniformly over components and hence over their mixture. The ordinary sum differs from \(N/4\) by at most \(1/|1-z|+1/(2|1-z^2|)=85/96\). Thus the largest absolute error through \(N-1\) is at least \(1/4-(m2^m/D_m+85/96)/N\). This can require far longer runs than the \(m+2\) reads for one transition matrix; a hidden type retained across a whole run can increase the total classical memory.

These tests isolate consequences of storing coherent preparation information over repeated steps. Infinite memory, program-dependent detectors and continuous response laws that depend on the other ports remain possible. Selecting an ordinary law on all preparations still uses evidence about complete instruments, such as the [protected-program comparisons](Electric_string_controls_and_probability.md). The [mechanical limits](Electric_string_quantum_and_classical_motion.md) also require calibrated sources, clock and field scaling, and rules for recording a trajectory.

Director Z’s cross-review found no error in the five results or reported numbers. It distinguished the two loss counts above and retained its failed predicates B2, D2 and B5 with their follow-up interpretations. The queue session reproduced both stored checker outputs byte for byte. The reviewer read the Lean source without elaborating it. [Cross-review, tests and limits](../REVIEW_QUEUE/reports/2026-11-14_pcp-cross-reviewer_Director_G_Finite_memory_and_coherent_returns.md)
