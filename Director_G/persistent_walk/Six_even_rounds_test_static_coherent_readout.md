# Six even rounds test static coherent readout on the optical circle

Kirtus Justus, research direction. OpenAI ChatGPT (Director G), derivation, figure reading and exact computation. 16 November 2026, B.C. Pacific Time (PCT, UTC−07:00).

A fixed coherent analyzer can fit the twenty selected **odd-round** cells of the ten-site walk. The **even-round** data distinguish that explanation. At sites 0, 2 and 4 in rounds 2, 4, 10, 14, 16 and 18, no common localized rail preparation fits the experimental figure with time-independent positive detector responses. Each site may have its own arbitrary coherent analyzer and efficiencies, and every round may have its own positive normalization. The discrepancy holds at the original eight-level RGB tolerance and persists at nine levels. All eighteen cells of the numerical panel accept the ideal equal-mixture control. [Odd-round construction and phase test](Testing_coherent_readout_with_a_terminal_phase.md) · [Lorz et al., Eq. (13) and Fig. 7(c)](https://doi.org/10.1103/PhysRevResearch.1.033036) · [Authors’ source image](https://arxiv.org/html/1809.00591v2/Fig7_asymmetricwalk_circle.png)

## A test on displayed intensities

Use the following coefficients to combine intensities at three sites in each round. At least one of the six weighted sums must be nonnegative in the model. In the experimental panel, even the largest allowed value of each sum is negative. The row of upper bounds uses the high endpoint of a cell band for a positive coefficient and the low endpoint for a negative coefficient.

| Site or bound | Round 2 | Round 4 | Round 10 | Round 14 | Round 16 | Round 18 |
|---|---:|---:|---:|---:|---:|---:|
| 0 | 137 | −559 | −156 | 1 | 1026 | 135 |
| 2 | −49 | 49 | 155 | −81 | 132 | 1 |
| 4 | −24 | 285 | 104 | 97 | −552 | −54 |
| Experimental upper bound, nine added RGB levels | −121/732 | −51/244 | −35/183 | −37/366 | −2/61 | −32/183 |

Each column can be evaluated on a position histogram multiplied by any positive round-specific factor. This permits a prospective test without transferring an absolute intensity calibration from one round to the next.

## Why coherent mixing cannot reverse all six signs

Launch at site 2 and evolve with the homogeneous balanced coin $(I-iX)/\sqrt{2}$ followed by opposite rail shifts. Let $B_{tm}$ map the input rails to the output rails at site $m$ after round $t$. With a fixed input density matrix $\rho$, a fixed positive semidefinite detector response $H_m$, and a positive round scale $k_t$, the displayed intensity has the form

$$
q_{tm}=k_t\operatorname{tr}\!\left(H_m B_{tm}\rho B_{tm}^{\dagger}\right).
$$

This includes a detector that resolves any fixed local rail basis and adds the two outputs with different nonnegative efficiencies. The unscaled expression equals the squared Frobenius norm of $H_m^{1/2}B_{tm}\rho^{1/2}$. Every entry inside that norm is linear in the entries of $B_{tm}$.

Write $B_{tm}=2^{-t/2}\begin{pmatrix}a&ib\\ic&d\end{pmatrix}$ with real integer numerators. For the six rounds in the table, the exact walk gives $d=a+b-c$ at sites 0 and 4. At site 2 it gives $d=a$ and $c=b$. Thus at each retained site we can write the transfer matrix as a fixed real-linear function of a vector $v_{tm}$, divided by $2^{t/2}$. Use $v=(a,b,c)$ at sites 0 and 4 and $v=(a,b)$ at site 2. Substitution in the squared norm gives a real symmetric positive semidefinite matrix $G_m$ with

$$
q_{tm}/k_t=2^{-t}v_{tm}^{\mathsf T}G_m v_{tm}.
$$

The matrix $G_m$ is fixed across all six rounds. The test allows *every* such positive matrix separately at each site, including those with no factorization into the specified physical launch and detector. A stationary mixture of launch and detector settings also has this form if its mixing law stays fixed across rounds.

For the weights $w_{mt}$ in the table, form one symmetric matrix per site,

$$
S_m=\sum_t w_{mt}\,2^{-t}v_{tm}v_{tm}^{\mathsf T}.
$$

All three matrices are positive definite. The [checker](check_even_circle_readout.py) constructs them from the two independent input columns of the walk and verifies all eight leading principal minors in rational arithmetic. Therefore

$$
\sum_t \frac{1}{k_t}\sum_m w_{mt}q_{tm}=\sum_m\operatorname{tr}(S_mG_m)\geq 0.
$$

Six negative sums on the left contradict that inequality for every choice of positive round scales. The integer weights were chosen after reading the figure. Their verification requires no numerical optimizer. [Exact minors and band endpoints combined by round](even_circle_readout_output.json)

## Where the exclusion ends

At nine added RGB levels the strict sign test survives a further uniform enlargement of every endpoint by any amount less than $1/52155$ in displayed intensity. This is the smallest of the six column margins divided by the respective sums of absolute weights. At ten added RGB levels all six upper bounds for these weights become positive. The calculation leaves the feasibility of the intervening tolerances 10 through 23 open.

At **24** added RGB levels an explicit fixed physical model fits the eighteen experimental bands. Use the pure launch $(1,-1-i)/\sqrt 3$. For each response write $H_m=\begin{pmatrix}p&q+ir\\q-ir&s\end{pmatrix}$. The tuples $(p,q,r,s)$ for sites 0, 2 and 4 are respectively $(22380,4043,-5931,5630)$, $(19896,11363,-4006,14192)$ and $(30446,-3310,-19655,14553)$. Sites 6 and 8 use the identity. Divide by 10000, 9004, 6604, 9618, 7400 and 19751 in round order. The responses are positive definite, and changing their common unit together with all six divisors leaves the predictions invariant. The predicted totals over **all five** occupied sites range from 0.433 to 0.990, rounded. The omitted cells are constrained only through those totals. The witness demonstrates feasibility for the selected cells at that wider tolerance. Neither its gains nor the figure-reading tolerances are measured apparatus uncertainties.

A replication could prespecify these six columns, record the counts, background and exposure at each site, check a stable launch and detector response, and place simultaneous upper bounds on the six weighted sums. Observing all six bounds below zero would exclude the stated model at the confidence level of that procedure. The published raster does not supply that statistical test or identify the failing apparatus assumption. Stage 1 Initial External Grounding and physical identification remain open.

With Pillow and PyMuPDF installed, run `python -I -B Director_G/persistent_walk/check_even_circle_readout.py Fig7_asymmetricwalk_circle.png`. The checker verifies the image digest, transfer identities, matrix signs, both figure panels and the wider-tolerance construction.
