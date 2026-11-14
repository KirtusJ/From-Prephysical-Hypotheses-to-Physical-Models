# Can a detector mark expose a hidden response on a single walk?

**Kirtus Justus**, Theoretical Physicist, Port Coquitlam, British Columbia, Canada. Mathematical derivation and verification with OpenAI Codex.

One science read per launch suffices to test a heavy cell separately for each of $M$ detector modes if the apparatus supplies $M-1$ independent binary diagnostic marks with distinct hit probabilities across modes. One fewer mark can hide a smooth nonordinary response on every terminal table. The marks concern the detector's physical state before the experimenter chooses the read. They differ from the walk's own record of the minor wells.

## Two choices after the marks

On an eight-well ring launch a sharp right rail at 0. Three free signed Hadamard-and-shift ticks give $(R,L)=(0,1),(-1,0),(2,1),(1,0)$ over $\sqrt8$ at wells $-3,-1,+1,+3$. Alice keeps a coherent tag for the three minor wells, of total mass $r=3/8$. Bob's direct setting pools the rails at every well. For a common terminal scalar response $f_j$ in mode $j$ with $f_j(x)=c_jx$ through half mass, Alice's direct tag probability is

$$
q_j=\frac{r}{r+f_j(5/8)/c_j}, \qquad D_j=q_j-r .
$$

Bob's other setting splits the large cell before scoring, so Alice's probability is $r$ in every calibrated mode. To match clocks, tick four coasts everywhere and tick five swaps rails before shifting everywhere in the direct setting. In the split setting only the coin at $+2$ on tick five changes from swap to coast. The heavy rails then contribute $1/8$ at $+1$ and $4/8$ at $+3$. A minor arrival at $+3$ carries the other Alice tag. Both settings score the full joint table of Alice's tag and Bob's well. For a physically padded source, the balanced guarded read provides another possible split with different preparation requirements. [Matched walk and calibration assumptions](held_split_comparison.md) · [Guarded position reads](guarded_position_reads.md)

Draw a mode with probability $\pi_j>0$, fixed only through this launch's diagnostics and its single science read. Before the remote choice, obtain $n$ new binary marks from that mode. Conditional on $j$, these marks are independent Bernoulli draws with propensity $p_j$. The conditional science probability given the mode and the entire mark tape must still equal $q_j$ or $r$ for the chosen setting. A disturbance by a mark, an unread noise source shared by marks and science outcomes, or a new hidden response within $j$ can violate this requirement. The marks are separately available apparatus records. Appending prospective tag amplitudes inside Bob's one jointly normalized score would change its denominator. Copying one observed mark many times gives one diagnostic draw.

Let $K$ count the marked hits and $Y$ denote Alice's minor-tag hit. Compare the direct and split rates with both choices represented in every populated count stratum. Multiply the conditional difference by the frequency of that stratum in the pre-choice population:

$$
b_k=\Pr(K=k)\{\Pr(Y=1\mid K=k,\mathrm{direct})-
                      \Pr(Y=1\mid K=k,\mathrm{split})\}.
$$

Choose the arm independently after the tape is recorded, or randomize using $K$ with both arm probabilities positive at each supported $k$. A zero-probability stratum contributes $b_k=0$. Keep misses and both choices on the assigned exposure denominator. Pooling the marks gives only $\sum_k b_k$. Selection after learning a science outcome does not implement this comparison.

## The number of marks

Write $B_{kn}(p)=\binom nk p^k(1-p)^{n-k}$. Then $b_k=\sum_j B_{kn}(p_j)\pi_jD_j$. The $n+1$ Bernstein polynomials span all polynomials through degree $n$; for example $p^\ell=\sum_k \binom{k}{\ell}B_{kn}(p)/\binom n\ell$ for $0\le\ell\le n$, taking out-of-range binomials as zero. Suppose there are at most $M$ modes, with distinct propensities. At $n\ge M-1$, for each mode the Lagrange interpolation polynomial that is one at its propensity and zero at all the others belongs to this span. If every $b_k=0$, applying that polynomial gives $\pi_jD_j=0$ for each $j$. Thus the direct score has $f_j(5/8)=c_j(5/8)$ throughout the sampled population. The zero test needs an independently justified bound and distinctness. Reconstructing labeled deviations and assigning numerical error bars requires more information about the channel. With coincident propensities only the weighted mean of the deviations in each such group is identified.

This argument identifies a zero contrast. The general problem of recovering the unknown components of a finite mixture from observations grouped by component has different data requirements. Vandermeulen and Scott give the grouped-sample identifiability theorem for unknown component measures. [Primary grouped-sample result](https://arxiv.org/abs/1502.06644)

## A mark that hides an error and a second mark that exposes it

Take three equally likely modes with $p=(0,1/3,1)$ and $g=(2,-3,1)$. Let their heavy-cell hit probabilities at $5/8$ be $5/8+\eta g_j$ for sufficiently small $\eta>0$. Then the direct-minus-split spectator deviations are $D_j=-\eta g_j$. A single mark is informative about the apparatus. A hit rules out mode one and a miss rules out mode three. Yet neither conditional science comparison shows an error. The table includes every count stratum with up to two marks.

| Marks | Count $k$ | $\Pr(K=k)$ | $b_k/\eta$ |
|---:|---:|---:|---:|
| 0 | 0 | 1 | 0 |
| 1 | 0 | $5/9$ | 0 |
| 1 | 1 | $4/9$ | 0 |
| 2 | 0 | $13/27$ | $-6/27$ |
| 2 | 1 | $4/27$ | $12/27$ |
| 2 | 2 | $10/27$ | $-6/27$ |

Exactly one hit in two marks singles out mode two and gives a conditional spectator difference $3\eta$. Pooling these strata cancels all three differences. For any deviations in this specific channel, the inverse is $D_1=3(b_0-b_1)$, $D_2=27b_1/4$, $D_3=3b_2-3b_1/4$. Thus simultaneous upper bounds $\lvert b_k\rvert\le\delta$ imply $\max_j\lvert D_j\rvert\le27\delta/4$. These are joint-stratum discrepancies. The numerical constant assumes the displayed propensities and priors. Close propensities or small mode frequencies can worsen conditioning. No finite-sample confidence is implied by the algebra.

## Sharp obstruction at any bounded diagnostic length

For any fixed maximum $n\ge0$, take $d=n+1$ and $d+1$ equally likely modes with $p_j=j/d$, $g_j=(-1)^j\binom dj$, $0\le j\le d$. The $d$th finite difference annihilates every polynomial of degree below $d$, so $\sum_jg_jP(p_j)=0$ for all such polynomials. The likelihood of **every specific ordered mark tape** of length at most $n$ has degree at most $n$. Thus $E[g_j\mid\mathrm{tape}]=0$ whenever that tape can occur. One more mark can expose the fluctuation, since the all-hits tape has $\sum_j g_jp_j^d=(-1)^d d!/d^d\ne0$.

To realize the rival simultaneously on every possible finite table, choose one smooth bump $h$ supported inside $(1/2,1)$ with $h(5/8)=1$. Set $T_j(x)=x+\eta g_jh(x)$ and, on the support, $f_j(x)=(1-x)T_j(x)/(1-T_j(x))$. Elsewhere put $f_j(x)=x$. For sufficiently small $\eta>0$ these responses remain strictly increasing and positive away from zero. In a table with a heavy cell of mass $x>1/2$, that cell's normalized probability is $T_j(x)$; each minor cell of mass $y$ receives $y[1-T_j(x)]/(1-x)$ when $x<1$. A sole occupied cell has probability one. If no cell exceeds half, the read is ordinary in each mode. All perturbations of observable cell probabilities are linear in $g_j$. Given every available tape their mean vanishes. [Smooth response construction and its normalization](spectator_refinements.md#an-explicit-invisible-fluctuation-above-one-half)

Consequently this rival reproduces the entire ordinary science law even for a table chosen after the tape, an adaptively shortened tape within the bound, or any finite panel of such launches with fresh independent modes. Use the same diagnostic population in the ordinary comparison. Conditioning on past transcripts and the current tape proves equality of the joint law. For each maximum $n$ there is a rival with $n+2$ modes; the extra-mark test distinguishes that same rival. No sensor implementing the required link to an actual terminal response has been demonstrated. The walk supplies a heavy cell and a setting pair to use if such a sensor becomes available.

The [standalone Rust replay](check_detector_marks.rs) verifies both independent tag sectors on the ring, all the displayed strata, the inverse and finite-difference obstructions through twelve marks. Compile the file with rustc in the Rust 2021 edition and run the executable.
