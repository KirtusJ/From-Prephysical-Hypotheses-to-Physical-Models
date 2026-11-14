# How many detector modes can the prechoice marks identify?

**Kirtus Justus**, Theoretical Physicist, Port Coquitlam, British Columbia, Canada. Mathematical and computational assistance by OpenAI Codex.

A repeated binary calibration mark can distinguish several rates even when the apparatus never reports its internal state. The number of marks needed depends on what the experiment must establish. With at most $M$ distinct rates promised, $2M-1$ marks suffice to recover them and their population weights. With no such promise, $2M$ suffice to certify the presence of at most $M$ rates whenever it is true. After that calibration, $K-1$ marks per scientific launch suffice to test for a zero average contrast separately at each of $K$ distinct rates. All three statements concern exact population probabilities.

## What the marks must measure

Let a hidden state $F$ persist through a batch. Conditional on $F$, the $n$ raw binary marks are independent with a common success probability $P=p(F)\in[0,1]$. They precede the scientific setting choice. Retain the count $C$, including $C=0$. Recording every bit additionally permits checks of order effects. The count law alone cannot establish conditional independence: an apparatus could draw a count in advance and randomly distribute its successes over the batch. Disturbance during a longer calibration must be controlled if its mode distribution will be used for shorter scientific runs.

For $j=0,\ldots,n$, the measured count probabilities give

$$
s_j=E[P^j]=\sum_{k=0}^n\Pr(C=k)\frac{\binom{k}{j}}{\binom{n}{j}} .
$$

The ratio counts the fraction of $j$-subsets of mark positions which all succeeded. Conversely $\Pr(C=k)=\binom nk E[P^k(1-P)^{n-k}]$, so the moments through $n$ contain exactly the count-law information. The classical binomial-mixture parameter problem is treated by [Blischke (1964)](https://doi.org/10.1080/01621459.1964.10482176).

## Certifying support with no cardinality assumption

Construct $H_j=(s_{a+b})_{a,b=0}^j$ from the first $2j$ moments. For a coefficient vector $c$ and its polynomial $q(p)=\sum_{a=0}^j c_a p^a$,

$$
c^\mathsf{T}H_jc = E[q(P)^2].
$$

A nonzero kernel vector therefore forces every supported rate to be a zero of its polynomial. Conversely if the rate law has exactly $K$ atoms, its monic product of $K$ linear factors vanishes there. Thus $H_M$ is singular exactly when there are at most $M$ supported rates. At the first singular index $K$, the preceding matrix is positive definite. There must be exactly $K$ distinct positive-weight atoms, each a root of the degree-$K$ kernel polynomial. Solve the first $K$ moment equations for their weights using the invertible Vandermonde matrix. A nonsingular $H_M$ establishes at least $M+1$ support points. It is consistent with a continuum. This one-dimensional calculation is a special case of the [positive moment matrix theory of Curto and Fialkow](https://doi.org/10.1090/memo/0648).

If support size at most $M$ is an independent premise, $2M-1$ marks already suffice. The signed difference between two proposed laws occupies at most $2M$ points. Moments of degrees 0 through $2M-1$ force its masses to vanish by Vandermonde inversion on their union. For reconstruction, take $K=\operatorname{rank} H_{M-1}$ and solve $E[P^j q(P)]=0$ for a monic degree-$K$ polynomial, $j=0,\ldots,K-1$. Its leading coefficient is one, $H_{K-1}$ is invertible, and the actual product over the support solves the equations. The largest moment needed is $s_{2K-1}$. Deterministic rates 0 and 1 are allowed. If roots at endpoints are suspected, a polynomial nonnegative on $[0,1]$ can use $p$ or $1-p$ once there and a squared factor at each interior candidate. A verified zero expectation pins the support to its roots with fewer marks for those special populations.

**Sharp general cutoff.** Take $p_j=j/(2M)$ for $j=0,\ldots,2M$. On odd $j$ put weights $\binom{2M}j/2^{2M-1}$, and form a second probability law on the even $j$ with the same formula. Alternating differences of order $2M$ annihilate every polynomial of degree below $2M$. The $M$ interior modes and the $M+1$ competing modes consequently have identical raw mark laws through $2M-1$ reads. The same construction with an odd grid order $2M-1$ gives two different $M$-atom laws agreeing through $2M-2$ reads, showing the known-cardinality cutoff is sharp too.

For two true modes $1/4,3/4$ of equal weight, the rival modes are $0,1/2,1$ with weights $1/8,3/4,1/8$. Both populations give $(7,9,9,7)/32$ for the count from three marks. The fourth mark changes the comparison:

| Population | 0 successes | 1 | 2 | 3 | 4 |
|---|---:|---:|---:|---:|---:|
| Two rates, probabilities in units of $1/256$ | 41 | 60 | 54 | 60 | 41 |
| Three rates, same units | 44 | 48 | 72 | 48 | 44 |

For $q(p)=16p^2-16p+3$, the first law has $E[q(P)^2]=0$ and the second has $E[q(P)^2]=3$. All entries can be replayed by direct expansion. [Exact Rust example](check_mark_mode_examples.rs)

## A zero scientific contrast without numerical mode estimates

Use $r$ independent prechoice marks, followed by an independently randomized scientific control $Z$ and a bounded read $Y$. Let $\delta(F)$ be the difference in conditional mean read between arms. Conditional on the full type, the mark count must be independent of the response noise in each arm, or at least leave its conditional mean unchanged. Arm assignment and the accepted launches must sample the same prechoice population. Compute each stratum's difference from its **joint** rates per assigned arm,

$$
D_k=E[Y\,{\bf1}_{C=k}\mid Z=1]-E[Y\,{\bf1}_{C=k}\mid Z=0]
=\sum_{i=1}^K w_i\,E[\delta(F)\mid P=p_i]\binom{r}k p_i^k(1-p_i)^{r-k}.
$$

The $r+1$ Bernstein polynomials span all polynomials of degree at most $r$. If $r\ge K-1$ and every $D_k$ is zero, evaluate the corresponding linear functional on each degree-$K-1$ Lagrange indicator of the support. It gives $w_i E[\delta(F)\mid P=p_i]=0$. The implication requires the support bound and distinct rates, but the test of $D_k=0$ does not require numerical guesses for their locations or weights. For $r<K-1$ the evaluation matrix has a nontrivial null space. Scaling any nonzero null vector gives admissible signed changes about an interior science probability which cancel in every observed stratum. In particular, for $K=2$, ignoring the marks lets positive and negative mode changes cancel.

At any $r$, distinct hidden states with the **same** mark probability remain in one stratum of latent rates. Equal amounts of two such states with science changes $+d$ and $-d$ reproduce all marked and unmarked population contrasts of a zero change. To infer the response on each hidden state requires further information, such as a common sign within each mark-rate class, or additional calibrated marks that distinguish its members. The [held-count experiment](held_walk_counts.md) instead investigates what arbitrary dependence among repeated scientific reads can conceal.

In finite samples an estimated Hankel matrix will rarely be exactly singular. For a fixed candidate polynomial $q$, a simultaneous upper confidence bound $\eta$ on $E[q(P)^2]$ gives $\Pr(|q(P)|\ge b)\le\eta/b^2$ for $b>0$. It permits small contamination away from its zero set. Use independent verification data or account for selecting $q$ from the same sample. Near-coincident roots or small mode weights also make numerical inversion sensitive. These limits apply before the mark can be used to calibrate a walk detector. No mark records from a physical detector have been supplied.
