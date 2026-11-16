# Can three different detector gains explain the optical circle figure?

Three separate, time-independent detector gains cannot reproduce the displayed intensities at sites 5, 7 and 9 in rounds 11 and 13 of the ten-site walk in Fig. 7(c) of Lorz et al., under the effective walk and color reading specified below. The calculation allows the overall recorded intensity and the localized input rail state to change freely between rounds. This removes the equal-gain assumption for the two reference sites in the [earlier antipodal comparison](A_return_independent_of_the_launch_rail.md). [Lorz et al., §IV C, Eq. (13) and Fig. 7](https://doi.org/10.1103/PhysRevResearch.1.033036)

Kirtus Justus, research direction. OpenAI ChatGPT (Director G), derivation and source-figure calculation. 15 November 2026, B.C. Pacific Time (PCT, UTC−07:00).

## A ratio fixed by the walk

The launch is at site 2. Site 7 is the antipode and sites 5 and 9 form a reflection pair. Let $p_{t,m}$ be the ideal probability at site $m$ after round $t$, summed over its two rails. For the homogeneous coin $(I-iX)/\sqrt2$ followed by the cyclic shift, $p_{t,7}$ and $p_{t,5}+p_{t,9}$ are individually independent of the rail state at the launch. Their ratio $r_t=(p_{t,5}+p_{t,9})/p_{t,7}$ is 451/281 at round 11 and 1398/941 at round 13. This holds for mixed and pure rail inputs. [Reflection proof](A_return_independent_of_the_launch_rail.md)

Model the displayed intensity as $q_{t,m}=k_t g_m p_{t,m}$. Each $g_m>0$ may differ by site and weights both of that site's rails equally. Each $k_t>0$ is an arbitrary common factor at that round. Put $x=g_7/g_5$ and $y=g_7/g_9$. Then a necessary equality, with the common factor canceled, is

$$xq_{t,5}+yq_{t,9}=r_t q_{t,7}.$$

The following experimental bands use the eight-level RGB tolerance of the earlier comparison. Each interval gives the outermost compatible rows of the authors’ color legend. A black cell permits a range of positive intensities. [Authors’ figure PNG](https://arxiv.org/html/1809.00591v2/Fig7_asymmetricwalk_circle.png) · [Exact reading record](unequal_circle_gains_output.json)

| Round | Site 5 | Site 7 | Site 9 |
|---:|---:|---:|---:|
| 11 | [181/732, 97/366] | [89/366, 47/183] | [115/732, 125/732] |
| 13 | [167/732, 44/183] | [0, 22/183] | [31/183, 133/732] |

Write $A=(97/366,125/732)$ for the upper endpoints at sites 5 and 9 in round 11 and $C=(167/732,31/183)$ for their lower endpoints in round 13. The first row requires $A\cdot(x,y)\ge 40139/102846$. The second requires $C\cdot(x,y)\le 10252/57401$. Since the two gains are positive and $A_j/C_j\le 194/167$ for each site, the largest permitted value of $A\cdot(x,y)$ is at most $(194/167)(10252/57401)$. It falls short of its required lower bound by **0.18280**. This gap is in the weighted equation and has no interpretation as a detector error bar.

The inequality remains strict through 37 levels of added RGB tolerance and changes sign at 38. Round 7 in place of round 11 also gives a contradiction with round 13, through tolerance 29. Once a bound changes sign, this particular argument ceases to exclude the model. The tests share the same figure and do not supply independent observations.

## The closer case at rounds 9 and 13

At tolerance eight, the pair-sum inequalities alone admit $x=1/10$, $y=9/10$ at both rounds 9 and 13. A single-site constraint from the ideal walk closes this gap. The two-round bands require

$$
(22/183)x+(32/183)y\ge 6615/40016,\qquad
(167/732)x+(31/183)y\le 10252/57401.
$$

Eliminating $y$ gives $x\le 22243819/134570528$, about 0.165295. From the walk amplitudes, the probability operator for site 5 at round 9, in the launch basis R, L, is

$$
E_5=\frac{1}{512}\begin{pmatrix}13&-9i\\9i&85\end{pmatrix}.
$$

Its least eigenvalue is $(49-\sqrt{1377})/512$. The checker uses the rational lower bound $1189/51200$ and verifies positive definiteness after subtracting that bound. The round-nine bands require $q_{9,7}\ge135/244$, $q_{9,5}\le22/183$. With $p_{9,7}=41/64$ these imply $x>2349/14080$, about 0.166832, by $xq_{9,5}=q_{9,7}p_{9,5}/p_{9,7}$. The lower bound exceeds the allowed upper bound by more than 0.00153. This narrower discrepancy illustrates why the larger round-11 separation is preferable for a prospective measurement.

## What the displayed intensities leave open

The conclusion depends on fixed multiplicative gains, equal response to both rails at each site, a localized launch and the ideal homogeneous evolution. An additive background, a rail-dependent response, transfer to other sites, or time-dependent site gains can change the equation. The authors include intensity that leaves the displayed circle in the normalization. A common change of denominator cancels exactly. The plot gives no sampling distribution for these three-site readings. The sites and rounds were selected after viewing it. [Article and Fig. 8 caption](https://arxiv.org/html/1809.00591v2#S4.SS3)

A prospective test would preselect sites 5, 7 and 9 and rounds 11 and 13, measure each rail’s response, and save the pre-normalization intensities, background and off-circle channels. Repeating with detectors interchanged would show whether a discrepancy tracks the detector assignment. The present result concerns a published comparison with an effective model. Stage 1 Initial External Grounding and physical identification remain open.

Run `python -I -B Director_G/persistent_walk/check_unequal_circle_gains.py Fig7_asymmetricwalk_circle.png` from the repository root with Pillow and PyMuPDF available. The [checker](check_unequal_circle_gains.py) verifies the supplied PNG, the gain inequalities, the round-nine probability operator and the adverse pair-sum witness.
