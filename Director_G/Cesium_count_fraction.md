# A count fraction from two wells in a four-step cesium walk

**Kirtus Justus**, Theoretical Physicist, Port Coquitlam, British Columbia, Canada. Research supplement by Director G (OpenAI Codex).

Robens, Alt, Meschede, Emary and Alberti prepared cesium atoms at imaged lattice sites in one spin state and applied four fair-coin ticks. Two of their Figure 3 histograms constrain a mixture of signed-path squares and path counting. Under the walk, filtering, detection and sampling assumptions below, the two named wells give a one-sided 95% upper bound of **0.488** on the count fraction. A conservative correction covering choices among the three rows, five wells and either contrast direction gives **0.680**. These are reanalyses of the same atom records. [Original experiment, Fig. 3 and Appendices A–E](https://doi.org/10.1103/PhysRevX.5.011003) · [Prior reconstruction of the full histograms](Cesium_negative_read.md)

## The launches and reads

Let $\alpha$ be the incident weight on the path-count law and $1-\alpha$ the weight on the squared signed tally, with $0\leq\alpha\leq1$. Each word of four directions contributes one count. For squared tallies its sign flips on each $L\to L$ transition, starting with rail $R$. Sum signs only within the same terminal spin and position, then add the two spin probabilities. In the reflected physical coordinates the terminal well is $j=(\#L-\#R)/2$. The sharp spin and calibrated fair rotation implement these endpoint probabilities up to signs common to each final mode. [Walk convention and experimental mapping](Cesium_negative_read.md) · [Position-mask continuation law](Position_mask_preparation.md)

| Setting | Included direction words | Count numerators across $j=-2,-1,0,1,2$ | Square numerators | Denominator |
|---|---|---|---|---:|
| (a) No probe | All 16 | 1, 4, 6, 4, 1 | 1, 10, 2, 2, 1 | 16 |
| (b) Retain negative arm | First letter $R$ | 1, 3, 3, 1, 0 | 1, 5, 1, 1, 0 | 8 |
| (c) Retain positive arm | First letter $L$ | 0, 1, 3, 3, 1 | 0, 1, 1, 5, 1 | 8 |

The last two rows are conditional on the retained arm. The ideal first split has probability $1/2$ under both laws, so the retained ensemble has the same $\alpha$ as the launch. Transfer to the experiment requires arm selection and survival to preserve that composition and the subsequent spin dynamics. Arm retention and per-setting brightness may change the number of observations in each row. The comparison uses no fitted arm weights and never pools the two retained samples.

The following counts were reconstructed from the published vector bars. The two columns were chosen for the opposite ideal peaks. The selection is retrospective. The full seventeen-bin data in the checker include all 203 and 208 displaced atoms in (b) and (c). Two blank-run atoms were assigned to $j=-3$, outside the ideal support. The complete ideal five-bin walk assigns this observation zero probability. Restriction to the two named wells allows a conditional comparison only insofar as errors leave their relative odds as modeled. Trial times and sequence-by-sequence outcomes are unavailable in the figure. [Published vector figure](https://quantum-technologies.iap.uni-bonn.de/assets/pdf/SDT/physrevx-alberti.pdf) · [Archived counts and bar geometry](results/cesium_negative_read.json)

| Run | $j=-1$ | $j=+1$ | Included in two-well comparison | All Figure 3 atoms |
|---|---:|---:|---:|---:|
| Blank (a) | 131 | 35 | 166 | 230 |
| Retain positive arm (c) | 27 | 115 | 142 | 404 |

## Inverting the observed odds

Assume expected counts at the named wells factor as a positive row brightness times a positive well efficiency times the model probability. Each well efficiency must be shared across settings, unresolved final spin and the two response components. The four expected counts then give the odds ratio

$$
\Theta(\alpha)=\frac{P_a(-1)P_c(+1)}{P_a(+1)P_c(-1)}
 =\frac{(10-6\alpha)(5-2\alpha)}{2+2\alpha}.
$$

The numerator factors decrease and the positive denominator increases, so $\Theta$ decreases from 25 to 3. The sample ratio is $131\cdot115/(35\cdot27)=3013/189$. Solving $12\alpha^2-(50+2\Theta)\alpha+50-2\Theta=0$ with the smaller root gives $\alpha=0.228926\ldots$ for that sample ratio. This is an odds-matching point estimate. The confidence bound instead uses the sampling distribution.

Take independent samples with fixed category probabilities within each row. Conditional on the two pair-row totals $(166,142)$ and on 158 observations in the $-1$ column, the top-left cell $X$ has probabilities proportional to

$$
\binom{166}{x}\binom{142}{158-x}\Theta^x,\qquad 16\le x\le158.
$$

This follows by multiplying the row-binomial probabilities and conditioning on their common column total. The upper tail $\Pr_\Theta(X\ge131)$ is increasing in $\Theta$. Its value at pure count is $4.0049312\times10^{-10}$. Invert this inclusive tail at $0.05$ to obtain the lower odds bound $9.5646647\ldots$. Equivalently, test each $\alpha$ directly. The largest retained $\alpha$ is bounded above by $0.487884$, rounded outward. The checker performs the comparisons with integers on a millionth grid.

| Family of possible contrasts | One-sided tests covered | Upper count fraction, rounded outward |
|---|---:|---:|
| Named table and direction fixed for inference | 1 | 0.487884 |
| Blank versus one specified retained arm, four shared-support wells, one specified direction per pair | 6 | 0.585974 |
| Either retained arm versus blank with the same ordering convention | 12 | 0.616924 |
| All three row pairs, five ideal wells and either direction | 60 | 0.679303 |

The last three rows use a Bonferroni tail size $0.05/m$. For one specified arm there are $\binom42=6$ well pairs with positive model probabilities in both rows. The 12-test family counts both choices of arm. The broader family counts $3\binom52\cdot2=60$ slots and safely includes comparisons with an uninformative zero-support cell. The unconditional size of each valid conditional test is at most its nominal size by averaging over its own margins, so the union bound applies despite the shared atoms. The 60 slots cover these choices within Figure 3. Searches across other experiments, models or figures would require their own accounting.

## Sensitivity to position errors

As one specified readout model, let a true terminal well be reported correctly with probability $1-\rho$ and at either immediate neighbor with probability $\rho/2$ each. Apply this translation-invariant channel **before** the stable efficiencies of the reported wells, equally in both settings and for both final spins. The relocated arm in (c) ends far enough away to stay outside the selected wells after one such error. Before row scaling, the four read probabilities have numerators, in table order,

$$
 (1-\rho)(10-6\alpha)+\rho(3+4\alpha)/2,\quad
 (1-\rho)(2+2\alpha)+\rho(3+4\alpha)/2,\quad
 1-\rho+\rho(1+2\alpha)/2,\quad
 (1-\rho)(5-2\alpha)+\rho(2+2\alpha)/2 .
$$

The two numerator factors of the odds ratio decrease and its denominator factors are nondecreasing for the tested $\rho=0,0.02,0.04$. Repeating the one-table inversion gives upper bounds $0.487884,0.476894,0.465733$, respectively. This symmetric error model happens to strengthen the bound. The paper reports 98% well identification per image, adjacent-site errors, and imaging at both initialization and readout. It does not supply a joint error channel for the measured displacement. Neither $0.02$ nor $0.04$ is established as the effective rate in this calculation. Unknown asymmetric crosstalk, different efficiencies on the true spins before imaging, or setting-dependent loss can change the odds.

The authors report 1.2 separated atoms per sequence on average, greater than 99% spin initialization and a fit giving about 6% loss of spin coherence per fair step. Cluster dependence, slow drifts and imperfect arm transport require their own model. The source's bootstrap uncertainty concerns its Leggett–Garg statistic. This result uses conditional atom counts under a specified family of endpoint probabilities. It gives no independent measurement of an apparatus-wide or universal count fraction. [Original experimental and statistical controls](https://quantum-technologies.iap.uni-bonn.de/assets/pdf/SDT/physrevx-alberti.pdf)

The [standard-library checker](check_cesium_count_fraction.py) verifies all 51 source cells against the archived Figure 3 extraction, enumerates the walk, and inverts the finite conditional law. From this directory run `python -B check_cesium_count_fraction.py NEW_DIRECTORY` and compare the result with the [archived output](results/cesium_count_fraction.json).
