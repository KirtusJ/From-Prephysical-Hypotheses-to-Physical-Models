# Three sites and four rounds suffice for the optical-circle test

Kirtus Justus, research direction. OpenAI ChatGPT (Director G), derivation, source reading and computation. 15 November 2026, B.C. Pacific Time (PCT, UTC−07:00).

At sites **3, 5 and 9** in rounds **7, 13, 17 and 19**, twelve cells of the experimental panel in Lorz et al. exclude a single localized launch state with fixed, rail-dependent detector gains. Every one of the four rounds and every one of the three sites matters for this choice. With any round removed, a launch and positive gains fit even the five occupied sites. With any site removed, a launch and positive gains fit the two retained sites through all four rounds. The fits may use different parameters for different deletions. The earlier [five-site calculation](Testing_one_launch_state_across_four_circle_rounds.md) left the deletion of round 19 open. [Lorz et al., Eq. (13) and Fig. 7(c)](https://doi.org/10.1103/PhysRevResearch.1.033036) · [Authors’ PNG](https://arxiv.org/html/1809.00591v2/Fig7_asymmetricwalk_circle.png)

The scope is the balanced ideal ten-site walk from site 2 with one common pure or mixed two-rail preparation. At each site two positive gains weight the outgoing rail intensities incoherently. They remain fixed from round to round. The intensity scale may be any positive number in each round. These assumptions let us test the joint pattern even when individual gains and round normalizations are unknown.

## How the twelve cells constrain ten unknowns

Write the input state in the R,L basis using $z=\rho_{RR}-\rho_{LL}$ and $y=2\operatorname{Im}\rho_{LR}$. The individual rail probabilities are affine in $(z,y)$ on the closed unit disk. Real coherence drops out and every disk point is attainable. On each rectangle covering possible launches the four corners give bounds $p^-_{tmr}\le p_{tmr}\le p^+_{tmr}$, with the lower endpoint clipped at zero. Let $L_{tm},U_{tm}$ be the displayed color band's endpoints, $g_{mr}$ the time-independent rail gains and $h_t$ the reciprocal of the round scale. Any fit must obey both inequalities at each retained cell,

$$
\sum_r p^-_{tmr}g_{mr}-U_{tm}h_t\le0,
\qquad L_{tm}h_t-\sum_r p^+_{tmr}g_{mr}\le0.
$$

There are six gain variables and four reciprocal scales. For each rectangle a list of 24 nonnegative integers weights the inequalities. Their sum would have to stay at or below zero. The checker verifies that the coefficient of **each of the ten variables is strictly positive**. Thus the weighted sum is strictly positive for every fit, a contradiction. Generating candidate weights used numerical linear programming. Checking them requires only exact arithmetic and the source image.

At 15 added RGB levels the certificate excludes 496 rectangles, and 12 lie wholly outside the disk. The smallest width is $1/256$. Replay starts from the four unit squares and checks every subdivision. Its leaves have total area four, and the disk boundary is included. The earlier eight-level bands lie inside the fifteen-level bands. The numerical panel admits the ideal equal mixture at all twelve cells at eight levels. [Certificate](three_circle_site_certificate.json) · [Checker](check_three_circle_sites.py)

## Constructive controls

The following exact launches and gains use the site order shown, with R then L at each site. Gains and reciprocal scales can be multiplied by the same positive constant. The checker verifies every retained cell and the total on-circle intensity in each retained round. Sites omitted from a control receive small positive gains on both rails.

| Retained sites | Retained rounds | Added RGB levels | Launch $(z,y)$ | Gain pairs in site order | Reciprocal scales in round order |
|---|---|---:|---|---|---|
| 1, 3, 5, 7, 9 | 7, 13, 17 | 8 | $(11/12,-1/3)$ | (644,2164), (814,7161), (4,4776), (1069,4), (1588,554) | 1000, 1811, 2276 |
| 3, 5 | 7, 13, 17, 19 | 8 | $(0,1)$ | (264,2), (96,1577) | 1000, 281, 253, 1158 |
| 3, 9 | 7, 13, 17, 19 | 8 | $(0,1)$ | (501,3), (189,1075) | 1000, 521, 480, 2074 |
| 5, 9 | 7, 13, 17, 19 | 8 | $(-1/2,1/2)$ | (6407,28), (7,877) | 1000, 219, 5819, 2694 |
| 3, 5, 9 | 7, 13, 17, 19 | 16 | $(21/32,1/2)$ | (7166,1), (3688,17513), (1,23171) | 10000, 2624, 6554, 14262 |

The checker also replays the three [previous round-deletion witnesses](common_circle_launch_output.json). For the full twelve-cell selection **16 is the first integer tolerance that admits a fit** under this color-reading rule. The legend reader accepts colors within the nearest legend distance plus the tolerance, so widening it can only enlarge the bands. These RGB levels quantify uncertainty in reading a raster. They supply no physical error bars. The last construction predicts only the three retained sites within their color bands, and the deletion tests establish minimality only under removal of whole rounds or sites from this selection.

A prospective replication can specify these three sites and four rounds before collecting counts, retain the other positions for independent checks, and record launch repeatability, unnormalized intensity, rail-resolved response and background. The published figure alone cannot determine which experimental assumption accounts for the discrepancy. Stage 1 Initial External Grounding and physical identification remain open.

Run `python -I -B Director_G/persistent_walk/check_three_circle_sites.py Fig7_asymmetricwalk_circle.png` with Pillow and PyMuPDF installed. The checker verifies the image digest, the full disk cover, deletion fits and the positive fit at the next tolerance. The certificate lists 24 row weights per vector, ordered by round, site and upper then lower inequality. Each box is stored as the two lower coordinate numerators, their common denominator and a zero-based index into the weights.
