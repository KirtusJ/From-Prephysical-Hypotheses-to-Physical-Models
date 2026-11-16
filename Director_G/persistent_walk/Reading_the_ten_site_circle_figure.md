# Which input is consistent with the published ten-site walk figure?

Kirtus Justus, research direction. OpenAI ChatGPT (Director G), source comparison and independent walk calculation. 15 November 2026, B.C. Pacific Time (PCT, UTC−07:00).

Figure 7(c) of Lorz and colleagues gives a sharper preparation check at round three than at the previously studied round seven. In the authors’ **numeric** panel, the cells immediately either side of the launch site have exactly the same displayed color at round three. Under the homogeneous coin in their Eq. (13), either sharp input rail instead predicts probabilities 1/8 and 5/8, in one order or the other. A diagonal input predicts 3/8 at both sites. The two **experimental** cells have different colors. The figure distinguishes a discrepancy in the numerical comparison but does not identify which state entered the apparatus. [Journal article, §IV C and Fig. 7](https://doi.org/10.1103/PhysRevResearch.1.033036)

## Evidence from the two source versions

The September 2018 caption labels the ten-site input ccD. The journal and October 2019 revision label it ccV. Both give launch position $m=2$ and the same reported similarity of 79.9%. The authors use ccH and ccV as the traveling-line rails. An effective two-rail calculation still requires specifying how the optical network maps the prepared input to the first coin and shift. The caption alone cannot establish that mapping. [2018 version, Fig. 10](https://arxiv.org/html/1809.00591v1#S4.SS3) · [2019 version, Fig. 7](https://arxiv.org/html/1809.00591v2#S4.SS3)

Two independent readings of the published graphics establish the round-three color comparison. In the journal PDF, the numerical cells at $(t,m)=(3,1),(3,3)$ both have palette index 8 in the same indexed image. The experimental cells in their own image have indices 10 and 11. Indices belong to each image’s own palette. In the authors’ version-2 PNG the two numerical cells both have RGB (255, 2, 0), while the experimental cells have RGB (196, 0, 0) and (255, 36, 0). The [journal PDF, page 8](https://physik.uni-paderborn.de/fileadmin-nw/physik/Arbeitsgruppen/integrierte-quantenoptik/publications/2019/PhysRevResearch.1.033036.pdf#page=8) and [version-2 PNG](https://arxiv.org/html/1809.00591v2/Fig7_asymmetricwalk_circle.png) are two renderings of the same published comparison.

| Round and position | Numeric panel, legend range | Experimental panel, legend range | Ideal sharp R | Ideal sharp L | Ideal diagonal |
|---|---:|---:|---:|---:|---:|
| 3, position 1 | 0.337–0.402 | 0.270–0.281 | 1/8 | 5/8 | 3/8 |
| 3, position 3 | 0.337–0.402 | 0.467–0.484 | 5/8 | 1/8 | 3/8 |
| 7, position 7 | 0.446–0.465 | 0.364–0.410 | 29/64 | 29/64 | 29/64 |

The legend ranges quantify ambiguity in reading a rendered color. They give no sampling error or uncertainty for the detector. The checker compares a cell’s RGB with every interior row of the published color bar using the largest absolute difference among the three channels. It keeps all rows within four channel levels of the closest match and takes their outer endpoints. The table rounds outward to 0.001. A band can cover several probabilities, especially near red and black. For example, at round seven the experimental band includes the ordinary Hadamard prediction of 25/64. A single such cell provides no test of that alternative without a model of measurement error. The authors’ 79.9% uses internal-state-resolved probabilities. These five-site comparisons use the displayed position intensities summed over both rails.

## Why round three is informative

Use the cyclic shift following $H'=(I-iX)/\sqrt2$ at each tick. Launch at $m=2$. The [exact integer walk](check_cycle_cover.py) gives the three columns above. Reversing the circle swaps the two sharp predictions at round three and preserves their separation. At round seven the three candidates give exactly the same position return. The earlier [five-to-ten-site correspondence](Optical_circle_comparison.md) remains exact for the same homogeneous shift, coin and input.

There is a further limit to preparation identification from positions. For any fixed final rail, every path from one input rail has an even number of rail changes and every path from the other an odd number, or conversely. Each change contributes $-i$. All amplitudes from one input rail to that final rail are therefore real up to the common normalization, while those from the other are purely imaginary. A real superposition $(R+L)/\sqrt2$ has zero interference term in every terminal rail probability. Its probability agrees exactly, at every round, with the equal incoherent mixture of R and L. A relative input phase with nonzero imaginary coherence can alter these records. To distinguish the real diagonal state from the mixture, an experiment could rotate the relative phase by a quarter turn before the first coin. The diagonal input then exits in a single direction at round one. The equal mixture still splits evenly. This control assumes independently calibrated preparation and phase rotation.

## All displayed rounds and adverse checks

The checker uses all 100 parity-allowed cells in the numeric panel over rounds 0 through 19. It compares each ideal probability directly with the legend band. It retains the original scale and checks the other 100 cells have zero ideal probability. A neighborhood of nine pixels around each sampled center has a uniform color.

| Added RGB tolerance above the closest color | Cells containing sharp R prediction | Cells containing sharp L prediction | Cells containing diagonal or equal-mixture prediction |
|---:|---:|---:|---:|
| 2 | 44/100 | 44/100 | 87/100 |
| 4 | 46/100 | 46/100 | 95/100 |
| 8 | 49/100 | 49/100 | 100/100 |

At tolerance four the five misses are $(6,0),(6,6),(7,5),(7,9),(19,7)$. These are sensitivity checks on a raster, not statistical model-selection scores. The round-three separation between a sharp launch and the displayed numeric pair persists at all three tolerances. The experimental pair shows an asymmetry. The displayed intensities omit the underlying rail-resolved counts. The figure also omits the input file used for the numerical panel. An original preparation log, the simulator's input vector and raw channel counts would resolve different parts of the discrepancy. The material does not establish a caption error, an actual diagonal preparation, a launch-normalized return probability or a physical origin for the walk’s probability rule. Stage 1 Initial External Grounding and physical identification remain open.

Save the linked version-2 PNG and journal PDF locally. With Pillow and PyMuPDF available, run `python -I -B Director_G/persistent_walk/check_circle_figure.py Fig7_asymmetricwalk_circle.png lorz.pdf` from the repository root. The [checker](check_circle_figure.py) verifies the source files, reads the original PDF palette indices and reproduces the [numerical record](circle_figure_output.json). No raw count table is reconstructed from the graphics.
