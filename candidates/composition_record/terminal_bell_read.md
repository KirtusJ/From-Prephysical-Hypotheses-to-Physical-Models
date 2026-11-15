# What the two terminal position readings should count

**Kirtus Justus**, Theoretical Physicist, Port Coquitlam, British Columbia, Canada. Mathematical and computational assistance from OpenAI Codex.

The [event-ready contact experiment](heralded_bell.md) predicts a Bell violation using two identical local instruments. This supplement gives their full binary outcome table, a finite comparison of other pooled position bins, and tests of what the successful filters must preserve. The conditioned state on $00,11$ has block $\tfrac13\left(\begin{smallmatrix}1&-1\\-1&2\end{smallmatrix}\right)$.

## A table with every output assigned

At either station, setting 0 reads the initial separated routes $|+1,R\rangle$ and $|-1,L\rangle$ as $+,-$. Setting 1 applies three homogeneous free Hadamard-and-shift ticks. Assign $+$ to $x=2,4$ and $-$ to $x=-4,-2,0$, pooling both rails at every well. These assignments are fixed before sampling. The two settings measure $Z$ and $O=-I/8+X/2+5Z/8$. Both have marginal $P(+)=1/3$ on successful pairs.

| Setting pair | $96P(++)$ | $96P(+-)$ | $96P(-+)$ | $96P(--)$ |
|---|---:|---:|---:|---:|
| 00 | 32 | 0 | 0 | 64 |
| 01 | 24 | 8 | 8 | 56 |
| 10 | 24 | 8 | 8 | 56 |
| 11 | 15 | 17 | 17 | 47 |

Each row is conditional on the joint preparation herald and that setting pair. Thus $S=E_{00}+E_{01}+E_{10}-E_{11}=49/24$. For a fixed setting choice on every launch, multiply the table by $3/64$ and send the other $61/64$ of the probability to the common predeclared failure output. The three other flag combinations have probabilities $13/64,13/64,35/64$ for a success at A alone, B alone, or neither, respectively.

## Which pooled read clocks can violate?

For each station keep the immediate $Z$ read and vary the clock of the other setting from zero to five free ticks after release. At each clock enumerate **all** maps from its reachable wells to two signs, independently at the two stations. Optimize the absolute CHSH value over both bins. Complementing either bin and taking the absolute value covers the CHSH sign conventions. The largest value is 2 for every clock pair except:

| Free ticks at A and B | Maximum $|S|$ | One pair of positive bins |
|---|---:|---|
| $(3,3)$ | $49/24$ | $\{2,4\}$ at each station |
| $(3,4)$ or $(4,3)$ | $65/32$ | $\{0,2,4\}$ at tick 3 and $\{3,5\}$ at tick 4 |
| $(4,4)$ | $129/64$ | $\{3,5\}$ at A and $\{-1,1,3,5\}$ at B |

An integer enumeration follows from the amplitude transfer $M_x$. Initially $M_{+1}=\operatorname{diag}(1,0)$ and $M_{-1}=\operatorname{diag}(0,1)$. Multiply each matrix on the left by the unnormalized Hadamard; send its first row to the first row at $x+1$ and its second row to the second row at $x-1$. At tick $n$ a signed bin has observable $\sum_x s_x M_x^T M_x/2^n=aI+bX+cZ$. For the other station use coefficients $d,e,f$. The exact score is

$$
S=1+(c-a/3)+(f-d/3)-ad-cf+(af+cd+2be)/3.
$$

The maximum can therefore be checked using integer scores for at most $128^2$ sign-vector pairs at any one clock pair. The search concerns the stated finite horizons, direct route read, and position bins. It allows neither new control gates nor rail resolution.

## What can spoil the test?

The flags are measured *before* either setting choice. A coarse success bit may still have an unobserved copy of which successful route occurred. If local records on success have net overlap $r$ between the branches $00$ and $11$, tracing them multiplies the $00,11$ coherence by $r$ (up to complex conjugation). The reported flag yields and the one-party marginals stay the same, while $S=15/8+\mathrm{Re}(r)/6$. This read requires $\mathrm{Re}(r)>3/4$. Copying both accepted alternatives perfectly gives $S=15/8$ despite the intended $3/64$ joint success rate. Source isolation, erasure of path labels, stable real phase conventions, and choice-independent heralding all matter. The filter requires addressed local splitting and coherent routing. Only the post-herald setting-1 walk uses three homogeneous ticks.

For independently missed local detections assign $-$ on each miss. If station efficiencies $\eta_A,\eta_B$ are constant and independent of settings, true outcomes and each other, the Clauser–Horne score is $65\eta_A\eta_B/96-(\eta_A+\eta_B)/3$. The equal-efficiency threshold is $64/65$. A different perturbation replaces the *heralded state* by $I/4$ with probability $1-V$. The maximally mixed state gives $S=-1/64$ because the position bin has nonzero trace. The mixture violates for $V>387/395$. These cutoffs describe distinct models and do not bound arbitrary setting-dependent loss or drift. [Clauser and Horne](https://doi.org/10.1103/PhysRevD.10.526)

The source and read probabilities here use the ordinary quantum probability rule. A measured violation with the stated locality and timing conditions could exclude local hidden-variable explanations of the resulting correlations. The calculation alone does not select the ordinary probability embedding or identify the contact memory as the mechanism.
