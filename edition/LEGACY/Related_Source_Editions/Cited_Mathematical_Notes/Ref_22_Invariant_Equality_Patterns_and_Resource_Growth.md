# Invariant Equality Patterns, Probability Lifts, and Resource-Growth Bounds

*Selected sections of an unpublished mathematical note.*

**Original date:** 2026-11-09.  
**Research direction:** Kirtus Justus.  
**Mathematical and editorial assistance:** ChatGPT (OpenAI).

The selected statements, assumptions, arguments, and examples below are drawn from the original note. This editorial excerpt does not claim independent verification. Numerical results are source-reported unless established by the reproduced argument; cited literature is identified from the original note. Original section numbering is retained.


## 2. Equality-pattern orbit classification and its limit

Let J be a countably infinite set and G be the group of all permutations of J (or the finite-support permutations for finite-tuples). For k >= 1 and x in J^k, define a relation on positions by i ~_x j exactly when x_i = x_j. Two tuples lie in the same diagonal G orbit iff these equivalence relations agree. Consequently,

\[
|J^k/G|=B_k,
\]

where B_k is the Bell number. For k=1,...,8 the counts are 1,2,5,15,52,203,877,4140. If tuple positions are also quotiented by all position permutations, orbit types correspond to the integer partitions of k, giving 1,2,3,5,7,11,15,22 for those k. The general orbit result is established nominal-set mathematics (Pitts, *Nominal Sets*, 2013, Example 5.6).

The orbit functor does not preserve Cartesian products: |J/G|=1, whereas |J^2/G|=2. That discrepancy depends on *shared* rather than independent relabeling of components. It does not select which comparison is physically available. A formal quotient is not an observation instrument.

### Proposition 1: No fully symmetric probability lift

For k >= 1, **there is no countably additive probability measure on the discrete raw space J^k invariant under the diagonal action of G**.

*Proof.* Each equality-pattern orbit O_pi is infinite countable and transitive under G. Every singleton in O_pi must receive the same mass a_pi. If a_pi > 0 its orbit has infinite mass, so a_pi=0. There are only finitely many orbits, and J^k is countable. Countable additivity therefore gives measure(J^k)=0, contrary to normalization. QED.

Each finite quotient J^k/G nonetheless supports many ordinary probabilities, including uniform probability over B_k patterns. Thus probability assigned **after** quotienting need not lift to a fully invariant, normalized, countably additive law **before** quotienting. This does not forbid nonsymmetric underlying preparations with symmetric quotient outcomes, or direct orbit-space preparations. Those are additional contracts, not consequences of the raw action.

### Proposition 2: A quotient limit with no normalized raw probability limit

Let nu_N sample uniformly from [N]^k, embedded in J^k. The probability of a *particular* equality pattern pi with b blocks is

\[
P_N(\pi)=\frac{(N)_b}{N^k},\qquad (N)_b=N(N-1)\cdots(N-b+1).
\]

For fixed k, the quotient law converges to the point mass at the all-distinct partition. But for every fixed finite F subset J^k, nu_N(F) <= |F|/N^k -> 0. No normalized weak probability limit exists on the discrete raw J^k. The finite quotient law retains total mass while the raw label probabilities escape. Neither mathematical limit describes ontological survival or destruction.

## 3. Restriction-consistent normalized probabilities are not selected

Uniform mass on each set partition at a fixed arity is not restriction consistent: at k=2 it assigns pair equality 1/2, while the uniform k=3 law restricts to pair equality 2/5. The induced two-pattern distributions have total variation 1/10.

But consistency itself does not select a unique law. For each theta>0, the established Ewens exchangeable partition family gives every specific partition pi of [k] with b blocks of sizes n_1,...,n_b the positive mass

\[
P_\theta^{(k)}(\pi)=\frac{\theta^b}{\theta(\theta+1)\cdots(\theta+k-1)}\prod_{i=1}^b(n_i-1)!.
\]

It is normalized, fully supported on every partition at fixed finite k, exchangeable under interface-position permutations, and consistent under deleting the last interface. For instance, the sequential rule puts the next interface in an existing block of size m with probability m/(k+theta), or in a fresh block with probability theta/(k+theta). This directly constructs all-size consistency. The parameter theta is not selected by the symmetry and restriction axioms.

### Proposition 3: Equal pair statistics, unequal triple laws

One all-size law arises from independent uniform samples from two abstract labels. Another is the Ewens law with theta=1. Both are exchangeable and projectively consistent, and both give probability 1/2 that a specified pair of positions is equal. At arity three:

| Pattern | Independent fair two-label law | Ewens theta=1 |
|:--|--:|--:|
| All three equal | 1/4 | 1/3 |
| A specified two-equal, one-different pattern (each of three) | 1/4 | 1/6 |
| All three distinct | 0 | 1/6 |

Their full three-pattern total variation is exactly **1/4**. Thus the whole collection of pair-equality statistics does not determine the three-interface law. These are classical statistical completions. No quantum measurement incompatibility or Born probabilities are thereby derived.

## 4. Mean resource constraints and mode growth

The hard Hamming-weight<=1 model on n independently addressable binary formal slots has n+1 eligible words and ideal noiseless message capacity log2(n+1). By contrast, if only the ensemble-mean Hamming weight is bounded by 1, the optimal Shannon entropy for n>=2 is n*h_2(1/n) bits. Both are established conditional facts and grow unboundedly with n.

A stronger counterexample assigns one zero-cost symbol and, at each cost ell>=1, exactly 2^(ell^2) other symbols. Every finite hard-cost sublevel contains finitely many symbols, but a distribution that puts probability 1/ell on the cost-ell symbols uniformly and the rest on the zero-cost symbol has mean cost 1 and entropy h_2(1/ell)+ell bits, unbounded as ell grows. No finite universal information ceiling follows from locally finite hard-cost levels alone.

### Proposition 4: An exact finite-entropy criterion in the locally finite, countable, ideal-outcome setting

Let J be a countable outcome set with finite nonnegative costs r(j), at least one zero-cost symbol j_0, and finite sublevel counts N(R)=#{j:r(j)<=R} for every finite R. Let E>0, and let H_E be the supremum of Shannon entropy (in nats) over all probability distributions with mean cost <=E. Then

\[
\boxed{H_E<\infty\quad\Longleftrightarrow\quad Z(\beta)=\sum_{j\in J}e^{-\beta r(j)}<\infty\text{ for some }\beta>0.}
\]

*Proof, sufficient direction.* If Z(beta)<infinity, the Gibbs reference q_beta(j)=e^{-beta r(j)}/Z(beta) is normalized. Nonnegativity of D(p||q_beta) gives H(p)<=beta E+ln Z(beta).

*Proof, necessary direction.* Suppose every Z(beta) diverges. Then limsup_{R->infinity} ln N(R)/R=infinity: otherwise N(R) <= exp(cR) for all large R and some c, and summing costs in integer-width shells gives a convergent \(Z(\beta)\) for every \(\beta>c\). Choose arbitrarily large R with ln N(R)/R large. On the N(R)-1 symbols other than j_0 with cost <=R, distribute total probability epsilon=E/R uniformly, and put the remaining probability on j_0. For R>E the resulting mean cost is <=E and

\[
H(p)=h(\epsilon)+\epsilon\ln(N(R)-1),
\]

which becomes arbitrarily large along those R. Contradiction to finite H_E. QED.

This is a known-type Gibbs entropy/growth condition applied to a specific countable noiseless alphabet; it must not be advertised as a novel physical theorem. Literature on energy-constrained entropy (including Shirokov 2026) provides the more general quantum setting. It says nothing about a physically chosen r, J, reference state, accessibility of all outcomes, physical time, or resource cost of measurement.


## Mathematical sources identified in the original note


- A. M. Pitts, *Nominal Sets: Names and Symmetry in Computer Science*, Cambridge University Press (2013), section 5.2, Example 5.6. Equality-type orbits.

- J. Pitman, *Combinatorial Stochastic Processes*, Lecture Notes in Mathematics 1875 (2006), section 2.2.7. https://www.stat.berkeley.edu/~aldous/206-Exch/Papers/pitman_CSP.pdf . Ewens exchangeable partition probability functions.

- A. Gnedin and J. Pitman, *Poisson Representation of an Ewens Fragmentation Process* (2007). Exchangeable and consistent Ewens partition laws.

- M. E. Shirokov, *Semicontinuity bounds for the von Neumann entropy and partial majorization*, Sb. Math. 217 (2026). https://www.mathnet.ru/php/archive.phtml?jrnid=sm&option_lang=eng&paperid=10371&wshow=paper . More general quantum energy-entropy and Gibbs conditions, as identified in the original note.
