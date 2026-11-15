# Restoring a rail with position records

The two nulls of the [four-step rail measurement](A_rail_measurement_from_four_free_steps.md) leave the same rail rotation up to sign. On the eight-site ring the fixed walk itself can undo this rotation using only free flights, position writes and feedback on the next flight time. Starting immediately after either null, the correction takes **84 additional walk ticks on average** and succeeds with probability one. The last recorded site can serve as the origin of the next measurement.

## Two clocks with inverse rotations

Use the ordered rails $(R,L)$, the Hadamard coin $H$ and the shift of the outgoing rows by $+1,-1$. A flight begins at one recorded site and ends with a position write preserving both rails. Define

$$
J=\begin{pmatrix}0&-1\\1&0\end{pmatrix},\quad
A=\frac{I+J}{\sqrt2}=HZ,\qquad
B=\frac{3I-J}{\sqrt{10}} .
$$

Both matrices are rotations, so they commute, and $A^4=-I$. The following are the actual rail matrices for all reachable displacements. Each matrix entry in the two central columns has a common denominator of four.

| Displacement from last position | Six ticks, $4K_6$ | Eighteen ticks, $4K_{18}$ | Probability at either clock |
|---|---|---|---|
| $0$ | $-(I+J)$ | $-(I-J)$ | $1/8$ |
| $+2$ | $I+J$ | $I-J$ | $1/8$ |
| $-2$ | $I+J$ | $I-J$ | $1/8$ |
| $4$ | $3I-J$ | $3I+J$ | $5/8$ |

One derivation propagates both sharp input rails. At each site add its two rows and send the sum one site to the right. Send their difference one site to the left, with both rows divided by $\sqrt2$. Six iterations give the second column. Continuing through tick 24 gives identity on both input rails at the origin and zero everywhere else. Translation supplies this identity for all eight launch sites. Consequently the eighteen-step walk is the adjoint of the six-step walk. Its matrix at displacement $d$ is $K_6(-d)^T$, giving the third column. Each squared matrix $K^T K$ is its tabulated probability times identity. The complete position record has the same probabilities on an unknown rail, including a rail entangled with a spectator.

The 24-tick period of the eight-cycle is known. The feedback here uses the individual position-conditioned matrices at two clocks within that period. [Tregenna, Flanagan, Maile and Kendon, table 1](https://doi.org/10.1088/1367-2630/5/1/383)

## The feedback rule and its cost

At the start of each trial keep $n$ modulo four, with the accumulated rotation $A^n$ up to an overall sign. Set $n=0$ on entry. Take six ticks and write position. A displacement $0,+2,-2$ increments $n$ and finishes the trial. On displacement $4$, the rail has acquired $B$. Take eighteen ticks between successive position writes until displacement $4$ occurs. Each intervening displacement $0,+2,-2$ decrements $n$. The final $4$ supplies $B^{-1}$ and finishes the trial. Test $n=1$ only at the end of a trial, when the two $B$ factors have canceled. Stop on that value and continue from the last written site.

Write $q=3/8$ and $p=5/8$. The inverse loop ends almost surely, with mean $1/p$ eighteen-step flights conditional on entering it. Each trial therefore has mean duration $6+p(18/p)=24$ ticks. At the trial boundaries three consecutive direct increments, of probability $q^3$, suffice to visit $1$ from any other exponent. The probability of exceeding $3k$ trials is at most $(1-q^3)^k$. This gives finite mean and shows that $1$ is the only closed class of the stopped process.

For the exact mean, the increment $d$ modulo four has probability

$$
w_d=q\,\mathbf1_{d=1}+\frac{p^2q^{(-d\bmod 4)}}{1-q^4},
\qquad (w_0,w_1,w_2,w_3)=\frac{(320,318,45,120)}{803}.
$$

The second term sums the possibilities of $k\equiv-d\pmod4$ ordinary returns in the inverse loop before its first antipodal return. Let $T_n$ count expected remaining ticks and set $T_1=0$. For $n=0,2,3$, first-step conditioning gives $T_n=24+\sum_d w_d T_{n+d\bmod 4}$. Substitution yields $(T_0,T_1,T_2,T_3)=(84,0,132,128)$. The time within a trial and its increment can be correlated. The first-step equation uses their separate contributions to expected total time.

At the stop the rotation is $A$ up to sign on every recorded word. The four-step null's rotation was $\pm A^{-1}$, so the entire conditional operation restores the initial rail and its correlations with any spectator. A relative position record suffices for each update. Returning to the original physical site would be a further requirement. Counting only free walk ticks, one corrected four-step measurement costs $4+(1/4)84=25$ ticks on average. For the balanced source and threshold $m$ of the four-step measurement this gives $25\sqrt2\,m\eta_m$ expected walk ticks, where $\eta_m=[1-(3-2\sqrt2)^{2m}]/[1+(3-2\sqrt2)^{2m}]$. Durations of position writes and feedback add to these totals. A finite deadline can interrupt the correction before it has restored the rail.

The [exact replay](check_position_pulse.py) propagates all sixteen sharp columns, checks the four effects and inverse pairing at every origin, and reconstructs the stopped process with rational probabilities. The cost is for this particular controller. The physical assumptions include a coherent eight-cycle and a repeatable position write that preserves the arriving rail.

Kirtus Justus, Theoretical Physicist, Port Coquitlam, British Columbia, Canada, holds scholarly responsibility. OpenAI Codex derived the position-feedback construction and checked its cost.
