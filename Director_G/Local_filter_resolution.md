# How many local ticks can resolve a sheet character?

**Kirtus Justus**, Theoretical Physicist
Port Coquitlam, British Columbia, Canada. Research supplement by Director G (OpenAI Codex).

On the staircase walk, two nearby characters accumulate almost the same phase during a short flight from one well. This limits both the absolute difference of their record probabilities and the yield of a filter that rejects one character exactly. Rejecting many specified characters exactly also imposes a time limit at arbitrarily small positive yield.

## Model and gain range

Let the physical ring have circumference $4M$. On character $s$, each tick includes exactly one operation multiplying the state at departure well $x$ by $e^{2\pi i s g(x)/M}$, with $g(x)=\lfloor x/2\rfloor$. All live alternatives undergo this operation together, including any coherently controlled idle rail. The other controls and initial internal state must be the same in the two trials. They may use the position, coin, masks, ancillary memory or earlier outcomes. Each clock advances the queried carrier by at most one well in the covering line. Reversals, local holds and deterministic local swaps respect this premise when their physical clock costs are included. There is one queried carrier. A coherent switch that can bypass the sheet operation, a second charged walker, a separately prepared sheet reference or a gain-dependent control would change the model. Classical stopping can be represented by a permanently recorded halt followed by padding. Its branch can be kept at a fixed accessible well and queried on later ticks, since its scalar phase is never recombined with a live branch.

Start at a known $x_0$. At clock $j$ the lifted departure position belongs to $[x_0-j,x_0+j]$. The possible values of $g$ span exactly $j$ on the full interval, since its endpoints differ by the even integer $2j$. Lifts that differ by a ring winding give the same character multiplier. Consequently all accumulated gain exponents after $t$ queries lie in an interval of integer width

$$
W_t=\sum_{j=0}^{t-1}j=t(t-1)/2.
$$

This holds separately for every history, for either launch parity and before any postselection. The two straight rays attain the two endpoints among unrestricted paths. A filter may need further time to interfere those endpoints. The Lean proof checks the cone, integer floor arithmetic, accumulated interval and pairwise bound. [FilterPhaseWidth.lean](lean/FilterPhaseWidth.lean)

## Nearby sectors and a rare herald

Let $h=\min_{k\in\mathbb Z}|s-r+kM|$. Purify all common channels by retaining their environments, including classical measurement records used for feedback. At clock $j$, center the integer interval of departure gains at its midpoint. Removing the corresponding global phase between the two queries bounds their operator-norm difference on the reachable subspace by $\pi h j/M$, using $|e^{iu}-1|\le |u|$. A common isometry after the query preserves the state-vector distance. Induction gives final unit purifications at distance at most $\epsilon=\pi hW_t/M$ after a choice of relative global phase. This compares the complete normalized trials, with adaptive common controls allowed. [Bennett, Bernstein, Brassard and Vazirani, hybrid arguments](https://arxiv.org/abs/quant-ph/9701001)

For any common herald effect $0\le E\le I$, let $p_s,p_r$ be its probabilities per original launch. The norm of $E^{1/2}\Psi_s$ is $\sqrt{p_s}$. The reverse triangle inequality and contraction give

$$
|\sqrt{p_s}-\sqrt{p_r}|\le\epsilon .
$$

The total variation distance of any complete readout is also at most $\min(1,\epsilon)$, by trace-distance contraction. If $p_s>0$ and the filter promises $p_r\le\lambda p_s$, with $0\le\lambda<1$, it follows that

$$
 p_s\le\frac{\epsilon^2}{(1-\sqrt{\lambda})^2}.
$$

For perfect rejection this bounds the true-sector yield by $\epsilon^2$. Requiring $p_s\ge q>0$ implies $t(t-1)\ge 2M\sqrt q(1-\sqrt\lambda)/(\pi h)$ for $h>0$. With equal prior weights on just $s,r$, posterior fidelity at least $1-\eta$ implies $p_r/p_s\le\eta/(1-\eta)$ for $\eta<1/2$. The prior and per-launch yield therefore matter when interpreting conditional purity.

## Exact rejection, even on a rare branch

For a finite circuit with $t$ ticks, the purified amplitude vector is a Laurent polynomial in $z=e^{2\pi i s/M}$. Each monomial's exponent is the sum of the departure gains of an admitted history. Common masks, record-conditioned linear maps and final application of $E^{1/2}$ preserve this representation. Remove the same monomial from all terms so their degrees lie in $[0,W_t]$. If the herald has positive probability on one character, a component of this accepted vector is a nonzero polynomial. Every rejected character gives a distinct root of that polynomial, because zero probability forces the entire accepted vector to vanish. Thus rejection on $L$ distinct characters requires $W_t\ge L$, irrespective of the positive yield. In particular exact selection of a non-self-conjugate pair from all $M$ sectors requires $W_t\ge M-2$. This constrains sector responses. Preservation of an arbitrary post-herald data state would require a separate argument. The polynomial argument is the walk's gain-range version of degree bounds for query algorithms. [Beals, Buhrman, Cleve, Mosca and de Wolf](https://arxiv.org/abs/quant-ph/9802049)

For the narrower instrument made solely of synchronized signed Hadamards, common permutations and whole-well filters, each fixed oriented transcript has integer matrix coefficients up to a common normalization scalar. With a sharp real input and coordinate records, an accepted component that vanishes at one primitive root vanishes at every cyclotomic conjugate. In particular exact selection of $\{\pm1\}$ is impossible when $\varphi(M)>2$ under that rational-amplitude restriction, regardless of the number of ticks. This older obstruction is stronger for those instruments. The degree and yield bounds above also apply to sector-independent controls whose complex coefficients need not be rational. [Finite clock purity and its control assumptions](Finite_clock_purity.md)

## A uniform incident sheet and any positive yield

Write the accepted vector at sector $s$ as $\sum_{u=0}^{W}v_u e^{2\pi isu/M}$, up to a scalar of modulus one, with $W=W_t<M$. This representation includes every recorded branch in an orthogonal output space. For uniform incident character weights, the conditional probability of a set $S$ is $\sum_{s\in S}p_s/\sum_s p_s$ whenever the denominator is positive. Finite Fourier orthogonality gives $\sum_s p_s=M\sum_u\|v_u\|^2$. The squared norm at each individual sector is at most $(W+1)\sum_u\|v_u\|^2$ by Cauchy–Schwarz. Consequently

$$
\Pr(S\mid\mathrm{herald})\le\min\{1,\ |S|(W+1)/M\}.
$$

For a two-character target, even 90% conditional mass requires $W_t\ge 0.45M-1$, however rare the herald is. If $W_t\ge M$ the same necessary inequality is automatic. The proof needs uniform incident weights and a sector-preserving apparatus with a common record effect. A localized sheet state gives the same summed probabilities if every operation preserves character sectors and the terminal effect ignores their coherences.

For $S=\{a,b\}$, the two Fourier rows restricted to $u=0,\dots,W$ give a sharper envelope. Their $2\times2$ Gram matrix has diagonal $W+1$ and off-diagonal $\sum_{u=0}^{W}e^{2\pi i(a-b)u/M}$. Its largest eigenvalue gives

$$
\Pr(\{a,b\}\mid\mathrm{herald})\le
\frac{W+1+\left|\sum_{u=0}^{W}e^{2\pi i(a-b)u/M}\right|}{M}.
$$

An unrestricted polynomial of that degree attains the eigenvalue by choosing its coefficients along the leading singular vector. The asserted bound for the native walk only uses containment of its actual coefficient vectors in that polynomial space. A particular native pulse sequence need not attain it.

## Dependence on the spatial preparation

An address-dependent rail permutation or sign can change the character. A related width bound still holds for preparing a sheet from a single sheet address $y_0$, even with those controls. Suppose every additional operation preserves each sheet-address subspace and the staircase remains the sole operation that moves its address. Every history is then at a residue in $y_0+[g_{\min},g_{\max}]\bmod M$, where the interval has width $W_t$. For $W_t<M$ this is a cyclic interval of at most $W_t+1$ addresses. Conditional or unconditioned mixtures retain this support when the herald instrument itself preserves these subspaces. A final nonlocal sheet projection must be included among the operations if it is used to create the output.

For a positive-probability output, purify its normalized conditional state and expand it as a sum of vectors on these addresses tensored with their remaining modes. Their discrete Fourier sums give the character probabilities. The single-label and two-label Gram estimates of the preceding section apply directly to this output, with no character-preservation assumption and no output-yield denominator to bound. Here the conclusion limits concentration of the **prepared sheet state**. It does not describe a posterior about an unchanged incident character. The support statement also applies when the common initial site or sheet address lies at a seam.

For an initial support of diameter $D$ in a chosen lift, the departure exponent width at clock $j$ is at most $j+\lceil D/2\rceil$. The guaranteed cumulative width becomes $W_t+t\lceil D/2\rceil$. For even $M$, prepare equal coherent amplitudes at wells $0,M$ with the same internal state. Their one-query sheet gains are $0,M/2$, so sectors 1 and 2 yield orthogonal spatial superpositions after the gain operation. Any common subsequent unitary preserves orthogonality. This example uses the same extended input and violates the sharp-launch estimate at $t=1$. Reading the relative phase through a spatially local recombiner has its own time cost. A camera that only distinguishes the two separated packets records identical site probabilities on this trial.
