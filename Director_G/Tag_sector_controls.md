# What two pure pointer preparations calibrate

**Kirtus Justus**, Theoretical Physicist, Port Coquitlam, British Columbia, Canada. Research supplement by Director G (OpenAI Codex).

Both pointer values can be calibrated on the same two-rail walk. A marker can nevertheless reproduce every such calibration and give a different result when two pointer values arrive at the same splitter. One joint cell distinguishes two explicit models with probabilities \(0\) and \(1/24\). A separate comparison uses four positive rates. All values below are model predictions. [Dense directions and the conditional marker replay theorem, PR #20](https://github.com/KirtusJ/From-Prephysical-Hypotheses-to-Physical-Models/pull/20)

## The measured fraction

At each tick the integer rail pair \((u,v)\) at \(x\) sends \(u+v\) to \((x+1,R)\) and \(u-v\) to \((x-1,L)\), separately for each surviving tag. A marker travels along one outgoing edge. A faithful coordinate-controlled XOR changes both its pointer and the signed history labels. Prepare a sharp source \((0,R,b)\) in the active tag apparatus. A deterministic source flip selects either \(b=0\) or \(b=1\). Hold the tag through the calibration flight. If the apparatus needs an operation to set one label, match its elapsed time and other controls when setting the other.

Let \(P_t(x,c,b)\) denote a joint terminal frequency. For any fixed preparation and control prefix, compare fresh runs ending at \(t\) with runs continuing through one ordinary tag-preserving tick. Only the named parent site and tag can feed its right daughter. Conservation, consistency of the pre-read dynamics and a faithful joint terminal read therefore give the aggregate right fraction

\[
K_t(x,b)=\frac{P_{t+1}(x+1,R,b)}{P_t(x,R,b)+P_t(x,L,b)}
\]

whenever the denominator is positive. The left fraction uses the other daughter. This identification works even in the presence of another populated tag. It needs no transfer of the blank instrument's response. The quotient averages over the incoming rails, marker memories and other conditions present in that preparation.

Suppose each pure-label experiment separately yields the squared terminal panels of the sharp walk. Each then measures \(h(u,v)=1/2+uv/(u^2+v^2)\) at its actual inputs. One may test the panels directly or justify the score hypotheses separately in the two settings. The mathematical density result for the raw pair along \(t=4n,x=2n\) applies unchanged to either pure tag. A continuous, positive-scale-invariant pure-label response depending only on the local rail direction is thereby determined for that label. Pure calibration samples two planes of a four-component mixed input.

## A marker that passes both pure calibrations

Write \(s_b=u_b^2+v_b^2\). Consider the following right fractions for a marker at \(x\) carrying tag \(b\).

| Rule | Right fraction |
|---|---|
| Sector autonomy | \(1/2+u_bv_b/s_b\) |
| Local spectator dependence | \(1/2+u_bv_b/(s_0+s_1)\) |
| Dependence on the larger sector norm | \(1/2+u_bv_b/\max(s_0,s_1)\) |

Use the fair value \(1/2\) at any zero denominator. The left fraction is the complement. Each denominator is at least \(s_b\), and \(2|u_bv_b|\le s_b\), so all three rules give probabilities. They use the same signed walk, transport one marker with its tag, and depend only on the current site's tallies. Each is invariant under global rescaling and under a common sign flip within either sector. Exchanging the bit names exchanges their predictions. In a pure flight the occupied sector has \(s_b=s_0+s_1=\max(s_0,s_1)\), so induction gives identical panels at every depth. The same holds while the two sectors occupy disjoint sites.

Sector autonomy is continuous where \(s_b>0\). To see the boundary, hold the other sector at \((1,0)\) and take the selected pair to be \((a,a)\) or \((a,-a)\), with \(a\downarrow0\). Normalize each full input to unit length. Both paths approach the same point, but the autonomous right fractions are 1 and 0 along the two paths. No value at the empty sector gives a continuous extension. The sum and maximum denominators are strictly positive everywhere on the joint unit sphere, so these two rules are continuous there, including when the selected sector vanishes. The vacuum with both sectors zero lies outside that sphere.

Choosing the complementary initial bit and repeating the same XOR schedule swaps the labels in every panel for each rule. A spacetime-dependent change of names also preserves their decoded answers when carried through the links. For a frame \(g_t(x)\in\{0,1\}\) write the new name of a tag as \(b'=b\oplus g_t(x)\). A preserving edge \(x\to y\) must then apply \(g_t(x)\oplus g_{t+1}(y)\). A physical XOR on arrival composes with this change. A flip at a single site followed by unmodified links instead changes which physical inputs can interfere. Relabeling symmetry by itself therefore supplies no protection against the spectator rule.

## Two settings at the same splitter

Use the integer line, or identify the sites \(-4,\ldots,4\) on a periodic ring of at least nine sites and apply the same mask on the initial light cone. In setting \(O\), launch \((0,R,0)\). Immediately after tick one apply \(b\leftarrow b\oplus\mathbf 1_{x>0}\) to both rails, then keep the bit. At tick two the two signed pairs at \(x=0\) are \((1,0)\) in tag zero and \((0,1)\) in tag one. All three rules split both sectors equally there. Their full panels coincide through tick three. At \(t=3,x=1\), the pairs are now \((1,0)\) and \((1,1)\), respectively. The tag-one parent has marker mass \(1/4\). Its right fraction is 1 with the autonomous or maximum denominator and \(5/6\) with the sum. At \(t=4\) the tagged left daughter \((0,L,1)\) has mass 0 or \(1/24\).

In setting \(S\), prepare the sharp selected port \((+1,R,1)\) at absolute tick one. This is the complete surviving tag-one field of \(O\) at that clock, up to common amplitude normalization. Carry out the same remaining ticks at the same sites. At tick three the selected splitter again has raw pair \((1,1)\); its parent probability is \(1/2\). All three rules give zero on its left daughter. The left daughter-to-parent ratio is thus \(0\) in \(S\), versus \(0\) or \(1/6\) in \(O\). These kernels are independent of overall scale, past controls and marker history. Operational comparison requires characterizing a sharp restart or a physical early arm removal, including any disturbance to the surviving port, clock, intensity and marker preparation. A late selection of tag one from \(O\) leaves the spectator active during the split.

There is also an all-positive contrast. At tick four take \(A=(-2,L,1)\), \(B=(2,R,1)\). Every cell is a fraction of all launches for its setting.

| Model | \(O_A\) | \(O_B\) | \(S_A\) | \(S_B\) | \(O_A S_B/(O_B S_A)\) |
|---|---:|---:|---:|---:|---:|
| Sector autonomy | \(1/16\) | \(1/4\) | \(1/8\) | \(1/2\) | 1 |
| Local spectator dependence | \(1/16\) | \(5/24\) | \(1/8\) | \(1/2\) | \(6/5\) |
| Larger sector norm | \(1/16\) | \(1/4\) | \(1/8\) | \(1/2\) | 1 |

If the expected counts factor as \(C_{ij}=L_i\eta_j P_{ij}\) with positive setting brightness \(L_i\) and stable per-port efficiency \(\eta_j\), both factors cancel in this ratio of expected counts. Comparing sampled counts requires an uncertainty treatment, including possible empty measured bins. Additive background, port crosstalk and changes in relative efficiency across settings require separate characterization.

Through tick four, the larger-norm rule reproduces every autonomous cell. At each parent that feeds these panels, either \(u_bv_b=0\) or the selected sector has the larger or equal norm. The denominators differ for other mixed inputs. For example, keep running setting \(O\). At tick seven the tag-one parent at \(x=-1\) has selected pair \((1,2)\), other-sector squared norm 8, and marker mass \(5/128\) under both rules. Its unique left daughter \((-2,L,1)\) at tick eight receives \((5/128)(1/2-2/5)=1/256\) under sector autonomy and \((5/128)(1/2-2/8)=5/512\) under the larger-norm rule. This extension uses the line or a ring with the eight-tick cone unwrapped.

For a particular instrument, equality to the shielded fraction at each occupied local context suffices to replay the joint terminal masses, given the initial marker and correct tag transport. Fresh adjacent panels can test those fractions directly. Even within the class of rules continuous on the whole joint unit sphere, the sum and maximum denominators agree on all occupied pure inputs and give different four-tick records. Agreement with the autonomous four-tick records also leaves the later routing underdetermined.

## What a finite calibration can determine

Suppose a set of mixed-tag calibrations visits finitely many local signed fields. This includes finitely many finite-support preparations run to finite depths with specified tag permutations and free ticks. Fix the same field evolution, initial marker distributions and marker transport at those permutations for every rule. Even exact agreement with sector autonomy at every panel in this set, together with all occupied pure-tag responses, leaves distinct **real-analytic** splitting rules on the joint unit sphere. A later measurement on the sharp launch in setting \(O\) distinguishes them. The construction places no uniform bound on derivatives or on the degree of the response.

Write \(S=s_0+s_1>0\) and \(r=s_b/S\). Let \(A\) contain 1 and every value of \(r\) in the calibration for which \(u_bv_b\ne0\), using both choices of \(b\). All members of \(A\) are positive. Define

\[
H(r)=\prod_{a\in A}(r-a)^2,\qquad
K_b^{(c)}=\frac12+\frac{u_bv_b/S}{r+cH(r)},\qquad c>0 .
\]

The denominator is positive for \(r>0\) and equals \(cH(0)>0\) at zero. Thus \(K_b^{(c)}\) is real-analytic everywhere on \(S=1\), including an empty selected sector. Assign a fair split at the separate all-zero field. The numerator satisfies \(2|u_bv_b|/S\le r\), so these are probabilities. They are invariant under common nonzero rescaling, and use the same formula upon exchanging the two bit names. Where \(u_bv_b=0\) every rule is fair. At the other calibration inputs \(H(r)=0\), giving the autonomous fraction. The same holds for every occupied pure-tag direction because \(1\in A\). Starting with the common marker, equality at each visited splitter gives equality of the full calibrated panels by induction.

To find a reachable input outside any such finite \(A\), consider the parent at \(x=t-2\), \(t\ge3\), in setting \(O\). Every history there has exactly one left step. With first step right, the left step in positions 2 through \(t-1\) gives \(t-2\) right-ending words, while a final left step gives one left-ending word. With first step left there is just the right-ending word. All signs are positive. Putting \(n=t-2\), the two pairs are \((n,1)\) in tag one and \((1,0)\) in tag zero. The tagged marker reaches this parent with positive probability under every rule: one route takes \(t-1\) right steps on the pure right frontier, then goes left. Each choice on that route has probability \(1/2\).

The fractions \(r_n=(n^2+1)/(n^2+2)\) are distinct. Infinitely many \(n\ge2\) therefore give \(r_n\notin A\). At each such parent \(H(r_n)>0\) and \(u_bv_b=n>0\), so the right fraction decreases strictly as \(c\) increases. Both daughters have positive mass and each has that unique parent. Their ratio in a single terminal panel is \(K_b^{(c)}/(1-K_b^{(c)})\), even if earlier marker masses have already diverged. This argument uses the integer line or rings large enough to keep each chosen light cone unwrapped.

For a finite example take all panels of \(O\) through tick eight. Its contributing parent ticks are 0 through 7. The checker finds 12 distinct values in \(A\). The next edge parent, \(t=8,x=6,b=1\), has \(r_*=37/38\notin A\) and mass \(37/256\). Choose \(c_1=r_*/H(r_*)\) and \(c_2=3c_1\). The following joint endpoint probabilities count all launches under the indicated rule.

| Rule | Tick 9 at \((7,R,1)\) | Tick 9 at \((5,L,1)\) |
|---|---:|---:|
| Sector autonomy | \(49/512\) | \(25/512\) |
| Analytic rule with \(c_1\) | \(43/512\) | \(31/512\) |
| Analytic rule with \(c_2\) | \(40/512\) | \(34/512\) |

The two analytic rules agree with every autonomous cell up to and including tick eight. Calibrated relative efficiencies at the two named detectors would allow their odds to be tested on fresh terminal reads. Physical implementation and sampling uncertainty remain open.

## Reversing the sign of the other tag

Repeat setting \(O\) with a matched identity plate (\(+\)) and a plate that reverses the entire signed field of tag zero (\(-\)) immediately after the tick-one XOR. Both plates preserve the marker, its bit and all ports. Use the same subsequent ticks and a common local routing law in both settings. At native tick \(n+2\), site \(n\), the tag-one pair is \((n,1)\) and the other pair is \((\pm1,0)\), by the edge count above. For each setting separately let \(q_n^\pm=R_\pm/(R_\pm+L_\pm)\), where \(R_\pm,L_\pm\) are the joint masses of its two tag-one daughters at the next native tick. The pure right frontier supplies a positive parent in each setting. These ratios require faithful reads or independently calibrated relative efficiencies. The sign and identity settings must also match in elapsed time and other apparatus effects.

Write \(g(y,z)=K((1,y),(z,0))\) for the common aggregate **right** fraction. Homogeneity gives \(q_n^\pm=g(1/n,\pm1/n)\). Pure calibration gives \(g(y,0)=1/2+y/(1+y^2)\), hence \(g(0,0)=1/2\) and \(\partial_y g(0,0)=1\). If \(g\) is jointly differentiable at the origin, let \(\gamma=\partial_z g(0,0)\). The first-order expansion on the two rays gives \(q_n^\pm=1/2+(1\pm\gamma)/n+o(1/n)\). Therefore

\[
n\left(\frac{q_n^++q_n^-}{2}-\frac12\right)\longrightarrow1,
\qquad \frac n2(q_n^+-q_n^-)\longrightarrow\gamma .
\]

The mean recovers the pure slope. The contrast measures sensitivity to the other tag's sign. If each sector's sign is a freely changeable convention for the entire apparatus, \(g(y,z)=g(y,-z)\), the contrast is identically zero and either setting suffices. Testing a sign-sensitive rule requires a physical relative-sign reference.

There is also a finite bound for \(n\ge1\). Put \(d=1/n\) and suppose that \(|\partial_z^2g(d,z)|\le M\) throughout \(-d\le z\le d\). Taylor's formula about \(z=0\) cancels the two first-order terms in the mean, giving

\[
\left|\frac{q_n^++q_n^-}{2}-\left(\frac12+\frac{n}{n^2+1}\right)\right|
\le \frac{M}{2n^2}.
\]

The constant concerns this specific coordinate and segment. Establishing it separately is an experimental or model obligation. Equivalently, the measured discrepancy gives a *lower* bound on the supremum of the absolute curvature over the segment. If both fractions have simultaneous absolute error bounds \(e_+,e_-\), their mean has error at most \((e_++e_-)/2\). At \(n=6\) the pure value is \(49/74\). The two analytic rules above are even in the spectator sign and give \(43/74\) and \(40/74\). They therefore require curvature at least \(216/37\) and \(324/37\), respectively. An independently justified cap of 6 in these coordinates excludes the second prediction. The first clears this necessary test only. No physical cap is supplied.

**Why the two settings must be normalized separately.** For selected rails \((u,v)\) and spectator rails \((a,b)\), one possible analytic response sends the marker right with fraction

\[
K=\frac12+\frac{u(v-a)}{u^2+(v-a)^2+a^2+b^2}.
\]

The denominator is positive off the vacuum, and \(2|u(v-a)|\le u^2+(v-a)^2\). The rule is homogeneous, agrees with the occupied pure calibration and uses the same expression for either selected bit. It allows sensitivity to relative sign. It gives \(q_n^+=1/2\) and \(q_n^-=1/2+2n/(n^2+5)\). At \(n=2\) the parent masses are \(3/16\) and \(13/48\). The equal mean of the two right fractions is \(13/18\). Pooling the daughter counts over equal numbers of launches instead gives \(151/198\).

This bias persists at large depth. Let \(m_n^\pm\) be the tag-one parent mass and \(X_n^\pm=2^{n+2}m_n^\pm\). It receives the right daughter of the preceding inner-edge parent and a left daughter from the pure right frontier. Thus \(X_0^\pm=1\) and \(X_{n+1}^\pm=2q_n^\pm X_n^\pm+1\). Here \(X_n^+=n+1\), while \(2q_n^-\ge1+2/n\) for \(n\ge3\), giving \(X_n^-\ge X_3^- n(n+1)/12\). The minus setting consequently dominates the pooled ratio. Its scaled excess tends to 2 while the equal-setting mean has scaled excess 1.

Joint differentiability matters even if independent sector signs are unobservable. For \(S=u^2+v^2+a^2+b^2>0\), take \(K=1/2+\operatorname{clip}((uv-|ua|)/S,-1/2,1/2)\), with ordinary clipping to the indicated interval. This rule is Lipschitz on the normalized field sphere and agrees with every occupied pure-tag response. Its two edge fractions are exactly \(1/2\) at every depth. The absolute value introduces a cusp at the pure right input. All sign-control results here are predictions from the stated instruments and laws.

The checker enumerates signed words independently of the marker update, includes zero and inaccessible bins, and checks the labels in a varying spacetime frame. It verifies the tick-eight and tick-nine differences, the sign and matched-identity panels, and the weighting example. The stored 464 cells across five settings and 24 four-tick panels also give the larger-norm probabilities by checked equality to the autonomous column. [Standard-library checker](check_tag_sector_controls.py) · [Exact four-tick panels](results/tag_sector_controls.json)

## Testing a curvature cap with a finite number of launches

At the tick-eight parent \((6,b=1)\), the pure right fraction is \(h=49/74\). If the spectator curvature is at most six in absolute value on the specified segment, the equal-sign mean \(\mu=(q_++q_-)/2\) must satisfy \(\mu\ge h-1/12=257/444\). This gives a one-sided test against the second analytic rule, \(c_2\). At tick nine that rule assigns \(40/512\) to \((7,R,1)\) and \(34/512\) to \((5,L,1)\) under either sign. Its right fraction among these two ports is \(p_1=20/37\), and the probability of reaching either is \(r=37/256\). The first rule, \(c_1\), lies inside the one-sided null.

Fix the following sampling rule before collecting data. Each launch uses a fresh preparation. Let \(r_s>0\) be the probability of a named hit under sign \(s\), and \(q_s\) the probability of right given that hit. These probabilities must be stable across independent launches at that sign.

1. Draw a fair, independent sign. Use it for successive launches until either named port fires. Record every launch, its setting and its outcome. All other outcomes consume one launch and keep the sign fixed.
2. Count the named hit as right or left. Draw a fresh sign for the next requested hit. Stop upon recording 1,839 hits or using 13,549 launches, including a hit on the last launch.
3. With 1,839 hits, reject \(\mu\ge257/444\) if at most 1,029 went right. With fewer hits, report a timeout and count it as a non-rejection in the full set of runs.

To calculate the null error, extend each possible run beyond the deadline until all requested hits have occurred. Given sign \(s\), the probability that the first hit falls on launch \(j\) and is right equals \((1-r_s)^{j-1}r_s q_s\). Summing over \(j\) and averaging the two signs gives \(\mu\). Independent repetitions make the right count in the extended run binomial with parameters \(m=1839\) and \(\mu\). Every rejection observed by the deadline is also a rejection in its extension. Its probability is therefore at most \(F_{m,p_0}(k)\), where \(F_{m,p}(k)=\Pr\{\mathrm{Bin}(m,p)\le k\}\), \(p_0=257/444\) and \(k=1029\). This lower tail decreases with \(p\). The bound holds even when completion and the right count are dependent. [Binomial probabilities, NIST](https://itl.nist.gov/div898/handbook/eda/section3/eda366i.htm)

Under \(c_2\), both signs give the same arrival rate and the same right fraction. The wait for each hit is then independent of its label. With \(B=13549\) the timeout probability is \(F_{B,r}(m-1)\), and the unconditional rejection probability is \([1-F_{B,r}(m-1)]F_{m,p_1}(k)\).

| Quantity | Probability (rounded) |
|---|---:|
| Upper bound on false rejection over the one-sided null | 0.049532549250 |
| Rejection under \(c_2\) with unlimited launches | 0.951525623912 |
| Timeout under \(c_2\) with 13,549 launches | 0.001597098026 |
| Rejection under \(c_2\) with 13,549 launches, including timeouts | 0.950005944216 |
| Rejection under \(c_2\) with 13,548 launches, including timeouts | 0.949988732445 |

For this hit count and cutoff, 13,549 is the first launch budget to achieve 95% power. Raising the cutoff by one would raise the unrestricted boundary tail to 0.054539198659. The checker evaluates the tails as rational numbers before comparing them with 0.05 and 0.95. [Exact enclosures](results/tag_shot_budget.json) · [Reproduce the calculations](check_tag_shot_budget.py) · [Lean proof of the deadline and timeout rules](lean/TagShotBudget.lean)

**What goes wrong if the sign is redrawn after a miss?** Drawing a fair sign on every raw launch and pooling hits gives the right fraction \((r_+q_+ + r_-q_-)/(r_++r_-)\). For a control within the probability null, take \(q_\pm=h\mp1/6\), the two endpoint values of \(g(1/6,z)=h-z\), and arrival probabilities \(r_+=1/4,\ r_-=1/32\). The equal-sign mean is the pure value \(49/74\), yet the pooled mean is \(532/999\). With the same deadline and cutoff, redrawing on every launch would reject this null with probability 0.942229063259. The example allows the arrival rates to vary as nuisance parameters. Conditioning even the prescribed procedure on prompt completion can also distort the mean. With only two launches to get two hits in this example, the conditional probability that both hits are left is \((1-532/999)^2\). The corresponding unlimited probability is \((1-49/74)^2\).

The numerical power uses the two **recorded** port probabilities under \(c_2\). A common loss factor for right and left within a setting preserves \(q_s\) and lowers its arrival rate. Unequal right and left efficiencies can change \(q_s\) itself. Applying the stated threshold to physical counts therefore requires faithful or efficiency-matched ports, matched sign operations, and independent preparations. A correction based on separately measured efficiency ratios needs its own sampling calculation. A rejection challenges the joint calibration and curvature assumptions. This design supplies no measurement of the curvature, detector efficiencies or classical limit.
