# How many launches can loss force?

Research for Kirtus Justus · 15 November 2026 · B.C. Pacific Time (PCT, UTC−07:00)

Consider the five-site Hadamard walk, launched sharply at site zero on the right rail. At one chosen integer time a binary detector reads the launch port. Write $p_t$ for its ideal probability, and suppose the launch survives independently at each tick with probability $r$. A lost walker gives zero signal. A true return triggers the detector with fixed probability $\eta$. An independent background click has probability $d$ on each terminal read. The observed probability is $d+(1-d)\eta r^tp_t$. Each launch starts afresh.

A competing predictor gives the observed click probability as $\alpha P^t b$ with at most 55 states, a fixed launch, a row-stochastic matrix, and a fixed response in $[0,1]$. The observer may choose the time for each fresh launch using every previous outcome and private randomness. The only data returned by a launch are its chosen time and one terminal click or miss. Separate loss heralds, measurements in both rails, additional preparations and access to a coherent device between launches define different experiments.

**A 55-state counter can match the first 54 click probabilities exactly.** Its states are numbered 0 through 54. It starts at zero and moves up by one until it reaches the last state, where it stays. Assign each of the first 54 states the target click probability at its tick. The last state's response may be chosen freely. Thus the raw probabilities on ticks 0 through 53 carry no information against this particular rival. The construction also puts all 19 rounds of the optical comparison inside a horizon that a finite clock can fit exactly for one such binary record.

Define $\Delta(r)=\max_{t\ge54}r^tp_t$. The following are *necessary* launch counts for any experiment with a fixed maximum budget and with false rejection and false acceptance each at most 5%. The examples assume perfect true detection. The columns use different absorbing-state responses tailored to the stated background.

| Per-tick survival $r$ | Tick attaining $\Delta$ | $\Delta$ | Necessary launches, zero background | Necessary launches, 1% independent background |
|---:|---:|---:|---:|---:|
| 0.63 | 58 | $1.22314\times10^{-12}$ | 2,407,270,941,225 | 143,134,620,284,670,307,032,015 |
| 0.80 | 60 | $1.29341\times10^{-6}$ | 2,276,494 | 128,005,398,692 |
| 0.90 | 60 | $1.51666\times10^{-3}$ | 1,940 | 93,095 |

For a separate set of sufficient conditions at much higher survival, see [the calibrated finite test](Calibrated_loss_and_background.md). The sharp minimum number of launches for the full 55-state class is open. The lower bounds here apply to pure permanent loss. The known reset examples have a separate signal law.

## Zero background

Let $d=0$ and choose zero for the final state. Before tick 54 the outcome law is identical under both hypotheses. At every later tick the stochastic counter always reports a miss, and the lossy walk reports a miss with probability at least $1-\eta\Delta$. Thus at every chosen tick the law of the walk dominates $1-\eta\Delta$ times the rival's law as a measure on the two outcomes. Apply this pointwise along a transcript, conditional on the same previous outcomes. The time selection kernels are common to both models. After at most $n$ launches the walk's transcript law dominates $(1-\eta\Delta)^n$ times the counter's. An early-stopping protocol can be padded with ignored measurements up to its hard launch budget.

Any decision that correctly accepts the counter with probability at least $0.95$ must then accept it under the walk with probability at least $0.95(1-\eta\Delta)^n$. Requiring this to be at most $0.05$ gives

$$ n\;\ge\;\left\lceil\frac{\log 19}{-\log(1-\eta\Delta)}\right\rceil. $$

## Positive background

Let $0<d<1$ and $e=(1-d)\eta\Delta$. Choose the final state's fixed response $q=d+e/2$. The walk's late probability lies in $[d,d+e]$. Write $m=\min\{d(1-d),(d+e)(1-d-e)\}>0$. For Bernoulli laws the divergence $D(p\|q)$ as a function of $p$ has value and first derivative zero at $q$, and second derivative $1/[p(1-p)]$. Taylor's formula bounds it by $e^2/(8m)$ throughout this interval.

The chain rule for relative entropy sums the conditional divergences of successive launches along the adaptive design. Early ticks contribute zero. The total divergence is at most $ne^2/(8m)$. Coarsening the transcript to a binary decision cannot increase divergence. If the two decision errors are at most 5%, the decision divergence is at least $D(0.95\|0.05)=0.9\log 19$ by monotonicity for separated Bernoulli probabilities. It follows that $n\ge\lceil8m(0.9\log19)/e^2\rceil$. Fixed interior background can therefore force a lower bound proportional to $\Delta^{-2}$ at small tail signals.

## Reproduction and physical scope

The [checker](check_loss_floor.py) evolves integer signed path counts on all ten ports. The probability at tick $t$ is the squared numerator divided by $2^t$. It searches the tail with rational arithmetic until $r^t$ bounds every later value below the best one found. It encloses the logarithms by a rational series with a geometric remainder and checks that both endpoints yield the same integer ceiling. No fitted frequencies, simulated counts or measured count rates enter the bounds.

For an experimental scale, Lorz and colleagues report $63\pm3\%$ transmission per roundtrip in a different optical walk. The 0.63 row evaluates a hypothetical five-site experiment with independent homogeneous survival exactly 0.63. Transferring a nominal transmission between instruments, counting a roundtrip as a tick, and identifying optical loss with independent Bernoulli survival each require their own experimental justification. The other two rows examine hypothetical improvements to survival. [Lorz et al., section II](https://doi.org/10.1103/PhysRevResearch.1.033036) · [What the optical circle measures](Optical_circle_comparison.md)
