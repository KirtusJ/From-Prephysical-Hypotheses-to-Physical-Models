# How often can a direction detector copy the site?

**Kirtus Justus**, Theoretical Physicist, Port Coquitlam, British Columbia, Canada. Research supplement by Director G (OpenAI Codex).

The field-on source requires $m$ consecutive direction switches. Suppose the passing rail is always correctly identified, but after each pass the detector independently makes a permanent, unreported, fully distinguishing site record with probability $p$. This is one specified noisy instrument. Its tolerance depends on what is measured. The conditional state can approach the ideal Gaussian even while almost no initial walkers release before a polynomial clock deadline. Models distinguishing spatial and spin decoherence have been tested in atom walks. The independent hidden-copy law here is a model to test on this detector. [Alberti et al., experimental decoherence comparison](https://doi.org/10.1088/1367-2630/16/12/123052) · [Ideal field-on source](Field_on_source_and_release.md)

## A renewal equation within a single attempt

Fix a persistent sheet character. At each two-tick block, the passing operation is the ideal rail projection followed by $(1-p)I+p\mathcal D_X$ on density matrices, where $\mathcal D_X$ discards the off-diagonal matrix elements between different sites. The discarded outcome can be retained by the environment; summing over it gives this channel. On a failed rail, record the well and restart as before. This model assumes no loss, fresh independent copy decisions conditional on each pass, and a site record that retains the sheet. A static mixture of perfect and permanently faulty instruments has different multi-block statistics even at the same single-use copy rate.

Write $q=1-p$ and $a_j(h)$ for the one-attempt probability of $j$ consecutive ideal switches at field slope $h$, from a sharp well and rail. Let $S_j(h,p)$ be that probability with hidden records. A site copy at a pass leaves a sharp well and rail. Conditional on a fixed sector, the next ideal segment has the same success law at every such well, either rail and either parity. Thus, with $a_0=S_0=1$,

$$
S_m=\sum_{k=1}^m p^{k-1}q^{m-k}
       \sum_{\substack{l_1+\cdots+l_k=m\\l_i\ge1}}\prod_i a_{l_i}.
$$

Only the first $m-1$ copy decisions change the survival probability. The last decision does matter to the released state. The exact conditional probability that **no** copy occurred, including the last, is $q^m a_m/S_m$. The mean number of moving ticks to a release with retries at recorded failure wells is $2\sum_{j=0}^{m-1}S_j/S_m$ in this character. On a finite deadline, attempts that never produce a packet still consume time. Norm or distribution errors quoted on successful releases use a different denominator.

At zero field on the line $a_j=4^{-j}\binom{2j}{j}$. The same formula applies to the tested prefixes of a finite ring when $2m<4M$. For $0<p<1$ set $B(z)=(1-qz)^{-1/2}-1$. Summing the positive-length segments gives

$$
\sum_{m\ge0}S_m z^m
=1+\frac{B(z)}{q-pB(z)}
=\frac{q}{\sqrt{1-qz}-p}.
$$

In particular $S_1=1/2$, $S_2=(3-p)/8$, and $\sum_{j\ge0}S_j=1+1/\sqrt p$. The simple pole at $z=1+p$ comes before the square-root singularity $1/q$. Its coefficient in the form $(1-z/(1+p))^{-1}$ is $2p/(1+p)$. Removing that pole leaves an analytic function in the open disk of radius $1/q$. Consequently for fixed $0<p<1$,

$$S_m\sim \frac{2p}{1+p}(1+p)^{-m}.$$

For $p=1$, $S_m=2^{-m}$ exactly. For $p=0$, $S_m=a_m$ and the mean is $4m$. These asymptotic statements about arbitrarily large $m$ use the line or rings growing before wraparound. The checker compares the composition sum with a literal two-rail density matrix in two signs of the elementary real character, including the endpoints $p=0,1$. [Independent propagation and rational controls](check_hidden_site_records.py)

## Conditional purity and elapsed time under refinement

Consider the unit sectors of the fixed-action field-on scaling $m\delta^2\to\lambda>0$, $h=\pm F\delta^3$. The ideal comparison gives $a_j(h)\le a_j(0)$ for $j\le m$ and $a_m(h)/a_m(0)\to e^{-F^2\lambda^3/3}>0$. The same hypotheses hold in the shrinking-action regime $m^3h^2\to0$ and for zero field. They permit a uniform bound on the contributions of records containing hidden copies.

Put $A(z)=(1-z)^{-1/2}$. The sum over $k$ segment lengths is at most $[z^m]A(z)^k=\Gamma(m+k/2)/[\Gamma(k/2)\Gamma(m+1)]$. For $2\le k\le m$ the gamma quotient in the numerator divided by $\Gamma(m+1)$ is bounded by $(m+k/2)^{k/2-1}$. One way to see this for half-integers is to peel off the integer factors and use $\Gamma(x+1/2)/\Gamma(x)\le\sqrt x$ by Cauchy–Schwarz. Since $a_m(h)\ge c/\sqrt m$ for large $m$, the sum of all $k\ge2$ terms relative to $q^{m-1}a_m(h)$ is $O(p\sqrt m)$ when $p\sqrt m\to0$. Indeed the term for each $k$ is bounded by a constant times $(C p\sqrt m/q)^{k-1}/\Gamma(k/2)$. Hence

$$
S_m(h,p)=q^{m-1}a_m(h)[1+O(p\sqrt m)],\qquad
\Pr(\text{at least one copy}\mid\text{release in this attempt})=O(p\sqrt m).
$$

The released density matrix contains the ideal state with at least the clean conditional weight. Its trace distance from the ideal is therefore at most the unwanted fraction. Subsequent measurements, including the Gaussian flight, inherit this bound when referred to the latest successful home and correct flight clock. This is a sufficient purity condition. A hidden copy near an endpoint can have a small effect on particular measured probabilities.

For $mp\to\alpha<\infty$, the successful fraction relative to the ideal tends to $e^{-\alpha}$. In finite action put $K=F^2\lambda^3/3$. At relative prefix length $j/m\to x>0$ the survival factor relative to $1/\sqrt{\pi j}$ tends to $\exp(-\alpha x-Kx^3)$. The segment bound is uniform at every $j\le m$ after dividing by $a_j(0)$, and gives $S_j\le C/\sqrt{j+1}$. A Riemann sum in the retry expression yields mean moving time in flight units

$$
2\lambda e^{\alpha+K}\int_0^1 x^{-1/2}e^{-\alpha x-Kx^3}\,dx .
$$

At zero defect it recovers the field-on mean. In contrast take $p=m^{-3/4}$. The conditional copy fraction still tends to zero, while the release probability in one attempt is $O(m^{-1/2}e^{-m^{1/4}})$. Under any polynomial tick deadline the number of attempts that can start is at most polynomial. A union bound over these starts makes the unconditional release probability tend to zero. A flight histogram on the rare successes could therefore converge to its ideal prediction while the apparatus fails its preparation clock on almost every walker.

## The scale $p\sqrt m$ in zero field

At $p\sqrt m\to\theta\ge0$, the ratio of $S_m$ to $q^{m-1}a_m(0)$ has the limiting value

$$
L(\theta)=\sqrt\pi\sum_{k=1}^{\infty}\frac{\theta^{k-1}}{\Gamma(k/2)}
=1+\sqrt\pi\,\theta e^{\theta^2}\operatorname{erfc}(-\theta).
$$

For fixed $k$ the coefficient of $(A-1)^k$ is asymptotic to $m^{k/2-1}/\Gamma(k/2)$, by the binomial formula and the lower powers of $A$. The preceding gamma bound dominates the series when $\theta$ is bounded, so the limit can be taken term by term. Splitting the sum into odd and even powers, or differentiating $e^{x^2}\operatorname{erfc}(-x)$, gives the last expression. The clean conditional fraction tends to $1/L(\theta)$. This crossover is for zero field. At finite action the product of field-dependent survival factors for the segment lengths remains inside the sum.

At $m=1024$ and zero field the full-record calculation gives clean fraction 0.72489 for $p=m^{-3/4}$, with mean time 84.30 times the ideal $4m$ ticks. At $p=1/\sqrt m$ the fraction is 0.10434, compared with the limiting 0.10123. The finite values, including slow approach to the rare-release regime, are retained. [All numerical rows](results/hidden_site_records.json)

## What a detector calibration must establish

On the matched two-output witness with a localized sheet, an independent full site copy gives the two-path marker overlap $\gamma=1-p$. A measured short-word contrast could constrain $p$ if the same instrument applies at each use. A fixed nonzero tolerance on one use does not settle either scaling limit. A detector with memory can reproduce the single-use contrast and have a different survival curve. Comparing joint switch records and timeouts at multiple depths tests that extension. Published measurements of coherence within an atomic parity outcome establish such preservation on that apparatus; they do not supply a per-block copy rate for a cyclic sheet walker. [Localized witness, count nuisance and primary-source comparison](Checking_a_direction_record.md)
