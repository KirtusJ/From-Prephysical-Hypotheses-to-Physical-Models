# How much classical memory can a three-site return record require?

At the exchange angle \(\theta=\pi/5\), an ideal three-site circuit produces 20 survival probabilities that require at least **18 states** in any exact, time-homogeneous classical generator. **20 classical states suffice** for the probabilities of *all* 20-bit records. If the same generator must remain exact for arbitrarily many ticks, its number of states must be unbounded. The experimental records give a different result. At six settings the first seven measured arrival bins resolve a lower bound of **four states**, subject to a sampling assumption. The experiment has 40,000 shots at each setting. It does not resolve the ideal 18-state bound at \(\pi/5\). [Experiment](https://arxiv.org/html/2401.09810v2#S8) · [Authors' data](https://doi.org/10.5281/zenodo.18429670)

## What counts as a state

Each clock tick produces a binary readout at site 0. Let \(f_j\) be the **unconditional** probability of first reporting a hit at tick \(j\), and \(S_j=1-\sum_{k=1}^j f_k\) the probability of surviving \(j\) ticks without a hit, with \(S_0=1\). A classical generator starts with distribution \(\alpha\) over \(d\) states. Its fixed nonnegative matrices for the two outputs sum to a row-stochastic matrix. If \(T\) is the no-hit matrix, then

$$
 S_j=\alpha T^j{\bf1},\qquad f_j=\alpha T^{j-1}({\bf1}-T{\bf1}).
$$

This permits hidden states, noisy emissions and state-dependent changes after every output. It charges the launch, any clock, and any memory used by the readout to the same state budget. A different instrument at every tick can encode an entire hazard schedule in its external controller. A continuous classical phase also lies outside a finite-state bound.

## The ideal return law at one archived setting

Use the gate order in the archived OpenQASM, with \(c=\cos\theta,\ s=\sin\theta\). Each round applies \(G_{12}\) and then \(G_{01}\), each active link acting as \(cI-isX\) on a single excitation. The first null from site 0 leaves \(v=(-is,0)^\mathsf{T}\) on sites 1 and 2. From that subspace the next null has matrix \(K\) and a hit has amplitude row \(r\),

$$
 K=\begin{pmatrix}c^2&-ics\\-is&c\end{pmatrix},\qquad
 r=(-ics,-s^2),\qquad f_{m+2}=|rK^m v|^2\quad(m\ge0).
$$

At \(\pi/5\), \(c=(1+\sqrt5)/4\). The determinant of \(K\) is \(c\) and its trace is \(c^2+c\). Its two eigenvalues are \(\sqrt c\,e^{\pm i\phi}\), with \(2\sqrt c\cos\phi=c^2+c\). In the survivor basis \((-i|1\rangle,|2\rangle)\) the input, transfer and output are real. The amplitude is therefore \(c^{m/2}(A\cos m\phi+B\sin m\phi)\), with real coefficients and \(A=-s^2c\ne0\). Squaring gives three nonzero exponential modes with bases \(c,ce^{2i\phi},ce^{-2i\phi}\). The real coefficient of the first is \((A^2+B^2)/2\), and each complex coefficient has modulus \((A^2+B^2)/4\).

The phase has infinite order. The number

$$
 x=2\cos(2\phi)=c(c+1)^2-2=\frac{-6+5\sqrt5}{8}
$$

lies strictly between \(-2\) and \(2\), which also confirms the complex eigenvalue pair above. Its quadratic field trace is \(-3/2\). An algebraic integer has integer field trace, whereas a root of unity and its inverse have an algebraic-integer sum. Thus \(e^{2i\phi}\) cannot be a root of unity. The three bases are distinct. Because the survivor norm tends to zero, \(S_{m+1}=\sum_{j=m}^\infty f_{j+2}\). Summation divides each coefficient by one minus its base, retaining all three modes.

## Why a finite classical generator must eventually depart

Discard states unreachable from \(\alpha\) by null transitions. For each remaining state \(i\), some \((\alpha T^\ell)_i>0\), so \(S_{n+\ell}\ge(\alpha T^\ell)_i(T^n{\bf1})_i\). The ideal tail is \(O(c^n)\). With finitely many reachable rows this bounds the maximum row sum of \(T^n\) by a constant times \(c^n\), so \(\rho(T)\le c\). Conversely Cayley–Hamilton makes the survival sequence satisfy the characteristic recurrence of \(T\). Three distinct modes with nonzero coefficients force each base to be a root of that polynomial, by independence of exponential sequences. In particular \(ce^{2i\phi}\) would be an eigenvalue and \(\rho(T)=c\).

Every eigenvalue on the spectral circle of a finite nonnegative matrix is its spectral radius times a root of unity. For a reducible matrix this follows by looking at the irreducible diagonal block containing the eigenvalue. Here the required phase has infinite order. This is the peripheral-pole obstruction used in positive realization theory. The application here is to the circuit's survival law at a specified gate setting. [Perron–Frobenius notes](https://math.umd.edu/~mboyle/papers/pfnotes.pdf) · [Benvenuti and Farina, Example 4](https://sites.math.rutgers.edu/~sussmann/papers/res-farina-tutorial-positive-realization.pdf)

Now suppose a \(d\)-state classical generator matches \(S_1,\ldots,S_N\) exactly. The difference of the two sequences starting at \(S_1\) satisfies a monic recurrence of order at most \(d+3\), obtained by multiplying the two characteristic polynomials (using the three mode bases for the ideal law). If \(N\ge d+3\), the first \(d+3\) differences vanish and forward recurrence forces all later differences to vanish. The spectral obstruction rules this out. Hence \(d\ge N-2\). The argument uses only survival up to \(N\) and allows arbitrary updates on a hit.

## A classical construction for every finite record

In the ideal one-excitation sector a true hit prepares site 0 again. A word with completed gaps of lengths \(j_1,\ldots,j_k\), including each terminating hit, followed by \(b\) misses, has probability \(\prod_i f_{j_i}\,S_b\). Allocate \(N\) classical states for ages \(a=0,\ldots,N-1\). At age \(a\) emit a hit with probability \(f_{a+1}/S_a\) and reset to zero. On a miss increment the age, capping it at \(N-1\). A zero-survival age can use any transition. Through tick \(N\) this generator gives exactly the word probabilities above, including a record of all misses. An unbounded classical age counter does the same at all times.

Approximation changes the resource question. Using just \(d\) ages and capping the last one can first alter a record only after \(d\) consecutive misses since a fresh start. Couple the generators until that happens. At most \(N\) starts, each followed by a conditional chance \(S_d\) of such a gap, give total variation at most \(\min(1,N S_d)\) through tick \(N\). Here \(S_d=O(c^d)\). At fixed angle, a number of ages of order \(\log(N/\epsilon)\) thus suffices for error at most \(\epsilon\). Conversely, for fixed \(N\) the set of \(d\)-state survival vectors is compact by continuity on a compact parameter space. Exact exclusion implies a positive distance for \(d<N-2\), but its size matters for any experimental use.

Lean 4.19 checks the reset word factorization, a finite-age path telescope, the capped construction through its last tick, and the denominator-cleared polynomial expansion used in the phase calculation. The spectral and finite-prefix lower bounds above are analytic proofs. [Lean source](ReturnRenewal.lean)

## A bound that the shots can resolve

At a fixed setting form the four-by-four matrix \(H_{ij}=f_{1+i+j}\), \(0\le i,j<4\). It factors as rows \(\alpha T^i\) times columns \(T^j({\bf1}-T{\bf1})\), hence has rank at most \(d\). This uses arrivals starting at tick **one**. An exceptional launch response outside the counted state space would change the hypothesis.

Each of seven first-hit bins is the mean of 40,000 binary indicators. With independent, identically distributed shots within each setting, Hoeffding and a union bound over 99 settings and seven bins give simultaneous absolute errors at most \(0.01131\) with probability at least \(1-2(99)(7)\exp[-2(40000)(0.01131)^2]>0.95\). Dependence between bins and across settings is allowed. For the sample matrix \(\widehat H\), an inverse radius \(1/\|\widehat H^{-1}\|_\infty>4(0.01131)=0.04524\) then guarantees that \(H\) is invertible on this event. The norm is the maximum absolute row sum. The checker uses integer determinants and adjugates for the comparison, with singular sample matrices left uncertified. [Hoeffding, Theorem 2](https://doi.org/10.1080/01621459.1963.10500830)

| Sweep index \(j\), angle \(j\pi/50\) | Inverse radius |
| ---: | ---: |
| 15 | 0.049786 |
| 16 | 0.064511 |
| 17 | 0.065821 |
| 18 | 0.049181 |
| 83 | 0.068836 |
| 84 | 0.061282 |

These six settings exclude a homogeneous generator with at most three classical states under the sampling assumptions. The remaining 93 settings are retained, including index 10 (\(\pi/5\)), with radius 0.005589. The test counts the memory of the entire classical generator, including apparatus behavior. A three-site quantum model also propagates off-diagonal terms after a miss. Assigning a physical memory dimension or identifying an underlying probability rule calls for additional measurements and controls.

To reproduce, compile the checker with stable Rust, pass the sibling dataset and compare the full output with the [99-setting panel](rank_panel.csv).

~~~sh
rustc --edition=2021 -D warnings check_rank.rs -o check_rank
./check_rank ../first_return_data/first_returns.csv > rebuilt.csv
cmp rebuilt.csv rank_panel.csv
~~~

The original histograms are credited to the [dataset authors](https://doi.org/10.5281/zenodo.18429670) under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). The panel reports integer tests derived from their arrival counts. OpenAI Codex developed the bounds and replayed the derived tables for the research program. The circuit calculation assumes the one-excitation Hilbert space, the squared-amplitude rule and the specified measurement. The [paired-angle contrasts](angle_pairs/README.md) and [recorded-reset check](README.md) test consequences of that description. Deriving the ordinary probability rule from prephysical records remains open.
