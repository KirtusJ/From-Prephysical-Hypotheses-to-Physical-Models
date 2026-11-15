# The minimum period of a deterministic herald target tape

A cyclic tape can supply the targets of the [six-wire walk herald](../candidates/composition_record/velocity_experiment/a_private_controller_for_the_walk_herald.md) without drawing new private target bits during the walk. Suppose the initial phase is uniform over a single tape of period $N$, and each completed block advances the tape by one place. The genuine auxiliary walk and its two sector measurements still run at every block. For these rules, the minimum tape length that matches $K$ consecutive stationary held-mode target records is

$$
 N_K=16\cdot64240^{K-1}.
$$

The same minimum applies if only the block return indicators are compared and the specified target-to-return channel is kept fixed. It is a period bound for this deterministic architecture. The [stochastic register](A_fixed_clock_for_a_private_herald.md) uses a different update rule.

## Count the target words

Let $j$ be the number of ones in a particular $K$-bit word and $\ell=K-j$. The stationary probability per word is the held mixture with weights $(55,73)/128$ and target rates $(467/880,173/1168)$. Putting the two terms over the common denominator $128N_K$ gives numerator

$$
 U=73^{K-1}467^j413^\ell+55^{K-1}173^j995^\ell.
$$

For $K\ge2$, reduction modulo $5,11,73$ shows $U$ is divisible by none of them. At each prime only one summand remains and its factors are units. To count the twos, multiply $U$ by $55\cdot73$. The bases $73\cdot467$ and $55\cdot173$ differ by $24576$, while $73\cdot413$ and $55\cdot995$ differ by $-24576$. The respective bases agree modulo $256$ and are odd. The multiplied sum is therefore congruent to $(55+73)$ times an odd number, or $128$ modulo $256$. Exactly seven factors of two cancel. For $K=1$ the two probabilities are $5/16$ and $11/16$. Every specified word thus has reduced denominator $N_K$, so any uniform-phase period producing it must be a multiple of $N_K$.

To attain the bound, make each $(K-1)$-bit word a vertex. A $K$-bit word is an edge from its prefix to its suffix, with multiplicity $N_K$ times its held probability. Stationarity equates incoming and outgoing counts. All edges have positive multiplicity, and appending a destination's bits eventually reaches it from any vertex. An Euler tour in this balanced connected directed graph uses each copy once. Reading the appended bits cyclically yields the required counts. For $K=1$ the single vertex has two kinds of loop. This is the de Bruijn overlap construction with integer multiplicities supplied by the target law. [De Bruijn, *A combinatorial problem*](https://research.tue.nl/en/publications/a-combinatorial-problem/)

The first three minimum periods are $16$, $1{,}027{,}840$ and $66{,}028{,}441{,}600$. No shortest tape can reproduce the next full target-word law. Every tape frequency is an integer multiple of $1/N_K$, and every held $(K+1)$-word probability has reduced denominator $64240N_K$. With independent auxiliary trials the binary target-to-return channel has probability difference $55/256$ and is invertible. Its tensor power is invertible at every finite length. Exact equality and the first failure of the full word law therefore transfer to reported returns. This argument supplies no lower bound on the ease of inverting a long word channel from noisy counts.

## Consequences for motion and resources

For any phase the long-run target fraction is $5/16$. The ordinary herald responses and position kernel give the same single full-site diffusion rate and the same single right-site velocity as the rotating stochastic register. In the held model the two modes retain separate rates. A direct two-clock control also exists. At lag $N_K$ the tape reuses the identical target, with covariance $m(1-m)$ for $m=5/16$. The held model gives only $\mathrm{Var}(a)=144/4015$. Multiplication by $(55/256)^2$ yields an excess joint-return probability of $10117855/1224736768$ at that lag. The first differing span may be much shorter than this control requires.

At $K\ge2$ the exact uniform phase has a non-dyadic denominator. A bounded number of fair binary draws cannot prepare it. Phase randomization can be completed before the run or the ensemble can enumerate phases in balanced proportions. A single common starting phase does not reproduce the stationary short-window ensemble at a fixed launch clock. [Exact arithmetic for the periods and walk channels](check_clocked_herald_register.py)

Kirtus Justus, Theoretical Physicist, Port Coquitlam, British Columbia, Canada, holds scholarly responsibility. OpenAI Codex derived and independently checked the period and the return-channel obstruction.
