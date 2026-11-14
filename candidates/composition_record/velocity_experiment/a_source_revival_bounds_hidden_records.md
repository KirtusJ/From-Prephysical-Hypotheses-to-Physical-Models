# Testing how much a hidden source record can help a classical memory

A memory that secretly receives the basis of a prepared rail can measure in that basis, discard the rail and return a replacement that always gives the right answer. We propose giving a random fraction of launches a different destination at the moment of release. Reverse the source on six protected qubits and count how often all six return to zero. In ordinary quantum mechanics that frequency limits what any measure-and-prepare memory can score on the other launches, even if its input includes hidden records of arbitrary dimension. At the ideal seven-write walk score of **82.4222%**, the return probability must exceed **97.74563%** to rule out that explanation. Both numbers are predictions or design targets. No physical source has passed this test. [Seven-write walk and position readout](four_preparations_at_one_site.md)

## What the two arms measure

Start a sixteen-site ring at site zero, moving clockwise. The source uses one rail qubit, three address qubits and two private record qubits. At ticks 1 and 9 apply H, shift, and copy the low address bit into the first and second private records respectively. At tick 17 use the first record to control H. On each other tick coast in the current direction. The address stores the count $y$ of left shifts modulo eight. Physical site at tick $t$ is $(t-2y)\bmod16$. At tick 24 every component reaches site 8 with $y=0$. The ideal state on the trusted six qubits $T=CQ$, the two record bits $C$ and the four rail/address qubits $Q$, is

$$
|\Omega\rangle=U|0^6\rangle=\tfrac12\sum_{b,s=0}^1(-1)^{bs}|b,s\rangle_C
 |\psi_{bs},y=0\rangle_Q .
$$

Here $b=0,1$ selects $Z,X$, and $\psi_{bs}=H^b|s\rangle$ has sign $(-1)^s$ on that axis. The branch phase comes from the second balanced coin. The signs matter when the circuit is reversed. Keeping the two copies coherent gives the same ideal data-arm probabilities as reading the two bits when written and controlling the later coin on the first result. The audit requires the coherent implementation. A classical log of the two early reads discards the relative phases needed for the inverse. [Forward gates, inverse and signed path checks](coherent_source_revival.py)

Choose the arm privately **at tick 24**, from the same incident population. Write $\rho_{CQE}$ for the actual state immediately before routing. $E$ includes every extra system accessible to the device, including a correlated quantum memory. The source state can have wrong rail states, biased labels, sign leaks and correlations among them.

- **Data.** Release $Q,E$ to a device. It must commit one output rail, including its position-dependent correction, before learning the two private bits. A trusted tester measures $C$ in the computational basis and measures the output along its indicated $X$ or $Z$ axis. Its success probability $A$ counts every incident launch whose sign agrees. The walk implementation realizes this last read by a trusted basis coin, shift and relative-position probe.
- **Revival.** The tester applies $U^\dagger$ on $C,Q$ only and measures all six qubits. Its success probability is $p=\mathrm{tr}[(|\Omega\rangle\langle\Omega|\otimes I_E)\rho]$. Reverse the gate order, including each address shift, and keep all outgoing copies out of reach. The input address and both private records are part of the test.

The memory under test can make any joint measurement of $Q,E$, keep its classical outcome, and prepare any qubit from that outcome. Seal the final address, correction label and output or timeout before enabling the tester’s basis-controlled probe. This is the entanglement-breaking benchmark across the whole release boundary. If an unaudited quantum path carries the answer around the intended memory, passing a test of this boundary cannot identify the physical path. The construction uses the ordinary tensor product, Born readout and independently characterized measurement effects. It does not derive them. Accessible fidelity and coherent descriptions of basis-dependent source imperfections have precedents in quantum information. [Fuchs and Sasaki](https://arxiv.org/abs/quant-ph/0302092) · [Gottesman, Lo, Lütkenhaus and Preskill](https://arxiv.org/abs/quant-ph/0212066)

## Sharp upper bound

For every such state and measure-and-prepare device,

$$
A\le f(p)=
\begin{cases}
1,&0\le p\le 1/2,\\
3/4+\tfrac12\sqrt{p(1-p)},&1/2\le p\le1 .
\end{cases}
$$

**Proof.** Let $M_k$ be the effects of the device's measurement on $Q,E$ and let $n_k$ be the Bloch vector of its output. The data success effect is $(I+H)/2$. In the $(b,s)$ block on $C$ the centered operator $H$ is $(-1)^s\sum_k n_{kb}M_k$, where $n_{kb}$ is the component along the selected axis. Hence $-I\le H\le I$. Purify $\rho$ to a vector $\Psi$, extending all effects by identity. For $p>0$ its normalized projection onto the trusted target has the form $\Phi=\Omega\otimes e$ and $|\langle\Phi,\Psi\rangle|^2=p$. For $t>1$, Cauchy–Schwarz with the two positive operators $(t-H)^{\pm1/2}$ gives

$$
p\le(t-\mu)\langle\Phi,(t-H)^{-1}\Phi\rangle,\qquad \mu=2A-1 .
$$

For scalars $z_k=(-1)^s n_{kb}$ in each block we have
$(tI-\sum z_kM_k)^{-1}\le\sum M_k/(t-z_k)$. Indeed, the isometry $Vv=(\sqrt{M_k}v)_k$ compresses the diagonal operator $D=\mathrm{diag}(t-z_k)$. The variational formula for $\langle u,(V^\dagger DV)^{-1}u\rangle$ maximizes $2\operatorname{Re}\langle Vu,w\rangle-\langle w,Dw\rangle$ over $w$ in the range of $V$. Maximizing over the full space gives $\langle Vu,D^{-1}Vu\rangle$. Continuous outcomes follow by grouping the bounded output Bloch vectors into cells of vanishing diameter. For fixed $t>1$ the resolvents converge in norm. [Hansen and Pedersen on operator Jensen inequalities](https://arxiv.org/abs/math/0204049)

Compress each effect to address zero and fixed side vector $e$. The resulting rail effect is $w_k(I+r_k\cdot\sigma)$ with $\sum w_k=1$ and $|r_k|\le1$. Average the last bound over the four ideal labels. The expectation of the inverse is at most

$$
\sum_k \frac{w_k}{2}\sum_{b=X,Z}
 \frac{t+r_{kb}n_{kb}}{t^2-n_{kb}^2}
\ \le\ \frac12\left(\frac1{t-1}+\frac1t\right).
$$

For the second inequality let $u_b=n_{kb}^2$. The scalar part is $t\sum_b(t^2-u_b)^{-1}$. Cauchy–Schwarz bounds the vector part by $\sqrt{\sum_b u_b/(t^2-u_b)^2}$. Both sums attain their maxima at $(1,0)$ or $(0,1)$ since the summands are increasing and convex on the simplex $u_X+u_Z\le1$. Substitution gives the displayed value, attained with a measurement and resend on one common axis. Thus for every $v=2t-1>1$,

$$
\mu\le t-\frac{2pt(t-1)}{2t-1}
     =\frac{1+(1-p)v+p/v}{2}.
$$

For $1/2<p<1$, minimize at $v=\sqrt{p/(1-p)}$. The limits $v\downarrow1$ and $v\to\infty$ cover the two endpoints. For $p\le1/2$ use $A\le1$. The proof permits an otherwise unrestricted cut state, including an inaccessible purification.

**Attainment.** On the two bases attach pure flags $e_Z=\sqrt p\,|0\rangle+\sqrt{1-p}\,|1\rangle$ and $e_X=\sqrt p\,|0\rangle-\sqrt{1-p}\,|1\rangle$ to the corresponding branches of $\Omega$. Projecting onto $\Omega$ leaves the flag vector $(e_Z+e_X)/2$, of squared norm $p$. Measuring the flag along X guesses the basis with probability $1/2+\sqrt{p(1-p)}$. A correct guess lets the device measure and resend the rail perfectly. A wrong guess succeeds with probability $1/2$. This attains the upper curve with fair private labels and ideal conditional rails. For $p\le1/2$, use orthogonal basis flags and multiply the branches with $s=1$ by the same phase $e^{i\phi}$. The data score remains one while the revival becomes $(1+\cos\phi)/4$, covering the entire lower interval. [Exact checks, including both endpoints](check_revival_benchmark.py) · [Optimal score for arbitrary basis-only flags](basis_information_at_the_source.md)

## A decision on counted launches

The seven-write walk has $A_7=226560354573/274877906944$. Solving $f(p)=A_7$ on the descending branch gives $p_*=(1+\sqrt{1-(4A_7-3)^2})/2$. The exact checker places $p_*$ strictly between 0.977456297837 and 0.977456297838. Equality permits the explicit counterfeit above. At 98% revival the counterfeit can reach 82% recovery. The previously simulated seven-write counts came from a source with classically read labels and do not measure a six-qubit revival. [Previous source and count record](four_preparations_at_one_site.md)

One preregistered test needs a single tally. The tangent at $p=49/50$ gives $14A+24p\le35$ on the entire classical boundary. Route to data with probability $7/19$ and to revival with probability $12/19$. Count one success for a matched sign or a complete six-zero revival in the selected arm. A lost launch, missing report or failed inverse earns zero. The classical conditional probability of success is at most $35/38$ on every trial, provided the routing is fresh and independent of the common cut state, apparatus and their history. Conditional on any past transcript, the null must still factor through one measurement and an independently prepared output on the data arm. The fixed-size one-sided bound for an observed fraction $h>35/38$ in $N$ trials is $\exp[-2N(h-35/38)^2]$ by conditional Hoeffding. Adaptive drift satisfying those premises is allowed. The ideal leak-free walk gives $(7A_7+12)/19\simeq0.93524$. Keep both arm counts and failed outcomes for diagnosis.

The measurement model requires a trusted inverse and comparator, a protected basis through output commitment, and the absence of any change at the source that anticipates the routing choice. For known worst-case upper errors $\epsilon_R,\epsilon_A$ in the two success effects (operator norm), add $(12\epsilon_R+7\epsilon_A)/19$ to the null success cap. An inverse allowed to erase a leaked flag can show 100% revival alongside a perfectly informed replacement. The circuit checker demonstrates that failure directly. It also gives 1/2 for a complete private basis, sign or parity copy and 1/4 for copying both bits when those records stay beyond the tester's reach. The return therefore constrains the data score without uniquely identifying a leak.

For a fixed horizon use the upper tail of $\mathrm{Binomial}(N,35/38)$. Conditional on earlier sealed outcomes, represent the next binary success by a fresh uniform draw below its conditional success probability. Raising each threshold to $35/38$ couples the tally to a dominating binomial. Independent repetitions of the attaining tag strategy reach that null. At $N=1019$, 953 successes give a one-sided null probability of 0.049505. At $N=3596$, rejecting at 3339 or more successes has size at most 5% and 95.07% power for independent repetitions of the ideal leak-free walk. These are planning examples. Seal each trial's outcome or timeout before drawing the next route. A shuffled batch with a fixed quota makes late routes predictable. This tangent misses some violations of the full curve, such as $p=1,A=0.77$. [Fixed-size scorer](score_revival_routes.py) · [Lean proof of the rational tangent and its contact](../../../Director_G/lean/SourceRevivalTangent.lean)

## Circuit replay of an attaining counterfeit

Prepare the flag in $(7|0\rangle+|1\rangle)/\sqrt{50}$ and reverse its relative sign on the X basis. Measure the flag, measure the input in the guessed basis and prepare a fresh output qubit from the two classical results. The trusted output analyzer reads its own private basis only after that output is committed. A statevector replay agreed with the full analytic outcome distribution to within $10^{-12}$. Three separately seeded Aer arms gave the following counts.

| Simulator arm | Observed successes out of 16,384 | Ideal probability |
|---|---:|---:|
| Measure input, send a fresh qubit | 13,389 | 41/50 |
| Reverse trusted six qubits only | 16,060 | 49/50 |
| Erase the external flag before reversing | 16,384 | 1 |

All histogram cells, including zeros, are retained. The fixed exposure per simulator arm demonstrates the mechanism. The pooled binomial test above requires private random routing on every launch. [Replay program](replay_leaking_source.py) · [Complete histograms, seeds and versions](../../../Director_G/results/coherent_source_leakage_replay.json)

    python -I -B coherent_source_revival.py
    python -I -B check_revival_benchmark.py

Kirtus Justus, Theoretical Physicist, Port Coquitlam, British Columbia, Canada, retains scholarly responsibility. OpenAI Codex developed the bound, source, formal arithmetic and replays. Claude documented the classical bypass’s blindness to a basis label and verified a counterexample. This is a prospective test within ordinary quantum mechanics. [Cross-review of the classical bypass](../../../Director_Z/cross_review/subagent_xr259_four_preparations/REPORT.md)
