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

The numerical power uses the two **recorded** port probabilities under \(c_2\). A common loss factor for right and left within a setting preserves \(q_s\) and lowers its arrival rate. Unequal right and left efficiencies can change \(q_s\) itself. Applying the stated threshold to physical counts requires the readout to preserve the right fraction, matched sign operations, and independent preparations. A rejection challenges the joint calibration and curvature assumptions. This design supplies no measurement of the curvature, detector efficiencies or classical limit.

### Randomly exchanging the two detectors

Give the two named daughters a switch after tick nine that can send either daughter to either counter. Keep the physical sign fixed through misses as above. On **every launch**, including retries, draw a second, independent fair bit for the switch. Log this bit and the physical counter that fired, then decode the original port. Assume faithful routing with equal transmission, no false counts and stable counter efficiencies \(e_A,e_B\) that depend only on which counter receives the daughter. The switch must preserve the two incoming port probabilities. An optical receiver using a related random assignment has been tested in a different apparatus. [Taylor et al., Phys. Rev. Applied 25, 054029 (2026)](https://doi.org/10.1103/7zhl-5vv1)

Let \(r_s\) now denote the probability that either daughter reaches the switch. Each port has probability \(\bar e=(e_A+e_B)/2\) of being counted, with any common transmission loss absorbed into the efficiencies. At held sign \(s\), the decoded right and left probabilities per launch are \(r_s q_s\bar e\) and \(r_s(1-q_s)\bar e\). If \(r_s\bar e>0\), the first recorded hit is right with probability \(q_s\). The 1,029-right cutoff therefore keeps the previous false-rejection bound even with an unknown counter efficiency ratio. Choosing the switch setting just once per requested hit gives a different result. For \(q_s=3/4,\ e_A=1,\ e_B=1/2\), the two settings separately give conditional right fractions \(6/7\) and \(3/5\). Their equal mean is \(51/70\).

Under \(c_2\) the named-hit probability becomes \((37/256)\bar e\). For example, with efficiencies \(1\) and \(1/2\) and unit upstream transmission it is \(111/1024\). At the same 1,839-hit target and cutoff, unconditional power is 0.950012511323 with 18,089 launches and 0.949999933316 with 18,088. Thus 18,089 is the first budget attaining 95% for that example. Arbitrarily small positive \(\bar e\) makes the completion probability arbitrarily small at any fixed budget. [Exact arithmetic and adjacent budgets](results/tag_shot_budget.json)

**Loss before the switch.** The following two models predict the same switch-tagged counter records, including misses, for these two ports at both signs. Transmission here is a separate nuisance parameter under each model. Missed and other outcomes share one recorded category.

| Model | True (right, left) per 512 launches in expectation | Transmission (right, left) | Arriving at switch per 512 in expectation |
|---|---:|---:|---:|
| Sector autonomy | \((49,25)\) | \((40/49,1)\) | \((40,25)\) |
| Analytic rule \(c_2\) | \((40,34)\) | \((1,25/34)\) | \((40,25)\) |

The pair of switch inputs has the same distribution under either model. The recorded laws consequently agree even if the orientation, the receiving counter and the launch of every hit are retained. Separately observing upstream losses or calibrating either transmission would give additional evidence.

**How accurately must the paths be matched?** Suppose only that each sign's effective right-to-left throughput ratio \(\lambda_s\) lies in \([1/\kappa,\kappa]\), with \(\kappa\ge1\). Its recorded fraction is \(f_\lambda(q)=\lambda q/(1-q+\lambda q)\). This function is nondecreasing in \(\lambda\), and \(f_{1/\kappa}(q)=q/[\kappa-(\kappa-1)q]\) is increasing and convex in \(q\). For the enlarged null \((q_++q_-)/2\ge257/444\), Jensen's inequality gives a recorded equal-sign mean of at least \(257/(257+187\kappa)\). The sign-even rival has recorded mean at most \(20\kappa/(17+20\kappa)\). Equal true fractions at both signs and endpoint throughput ratios attain each bound. The two recorded means are strictly separated exactly when

\[
  \kappa < \sqrt{257/220}\ \simeq\ 1.080825 .
\]

At equality the construction gives identical sign-conditioned right fractions. Larger uncertainty intervals contain the same construction. This boundary concerns the two **mean predictions**, allowing each hypothesis its own admissible nuisance values. A finite test with residual mismatch would have to use the lower null fraction and recompute its power for the specified arrival rates. The 1,029 cutoff and the budgets above use \(\lambda_s=1\). [Proof of counter averaging and the threshold comparison](lean/TagShotBudget.lean)

### A finite test with a residual throughput ratio of 1.05

Suppose a separate calibration bounds each sign's right-to-left throughput ratio between \(20/21\) and \(21/20\). For the power calculation also assume that, under \(c_2\), each sign gives a recorded named hit with probability at least \(a=1/10\) per raw launch. These are prospective design values. The throughput bound gives a recorded equal-sign mean of at least \(L=5140/9067\) under the one-sided null and at most \(U=21/38\) under \(c_2\).

Use the sign and detector-switch rules above. Stop at \(m=13{,}300\) named hits or \(B=136{,}130\) launches. Include a hit on the last launch. Reject the one-sided null when the target is reached with at most \(k=7{,}445\) decoded right hits. A timeout counts as a non-rejection.

| Quantity | Probability (rounded) |
|---|---:|
| Upper bound on false rejection | 0.049787662465 |
| Lower bound on rival power with unlimited launches | 0.952142761658 |
| Upper bound on rival timeout at 136,130 launches | 0.002249666528 |
| Worst-case rival power at 136,130 launches, including timeouts | 0.950000757956 |
| Worst-case rival power at 136,129 launches, including timeouts | 0.949994710825 |

The null bound follows from the unrestricted lower tail \(F_{m,L}(k)\). A deadline alone cannot rescue the earlier cutoff under this mismatch. In the enlarged probability null, take both recorded right fractions equal to \(L\) and both hit rates equal to \(1/10\). The old 1,029-right cutoff at 1,839 hits and 18,089 launches gives false rejection probability 0.062389375014.

**Power when the signs have unequal hit rates.** For the \(i\)-th planned hit with sign \(s\), write \(a_s\) for its recorded hit probability per launch and \(p_s\) for its recorded right fraction. The wait \(G_i\) (in raw launches) and the label are independent conditional on \(s\). Their joint probability for a right hit at launch \(j\) is \((1-a_s)^{j-1}a_sp_s\). The fair sign draws make the unrestricted labels independent Bernoulli draws with mean \(\bar p=(p_++p_-)/2\). A fast sign can favor one label, so the completed sample can have a different distribution.

For each requested hit, use a separate stream of independent uniforms, independent of the signs and labels. The first uniform at most \(a_s\) gives the actual wait in this construction. The first at most \(a\) gives a reference wait \(G_i^*\). Since \(a_s\ge a\), each \(G_i\le G_i^*\). Whenever the reference waits fit the budget, so do the actual waits. Reference completion is independent of all actual labels. For any fixed \(m,k,B\) and \(\bar p\le U\), the rejection probability is therefore at least

\[
  [1-F_{B,a}(m-1)]\, F_{m,U}(k).
\]

Both signs can attain this bound simultaneously. For the rival's incoming probabilities \(40/512\) and \(34/512\), effective right and left detection efficiencies \(336/475\) and \(64/95\) give total recorded rate \(1/10\) and conditional right fraction \(21/38\). Hence 136,130 is the smallest qualifying budget for this hit target and cutoff. The ratio bound alone allows both rates to approach zero. [Exact bounds and controls](results/tag_shot_budget.json) · [Arithmetic checker](check_tag_shot_budget.py) · [Lean proof of the deadline comparison](lean/TagShotBudget.lean)

An arithmetic average of the two hit rates cannot replace the per-sign floor. Take rates \(19/200\) and \(21/200\), right fraction \(21/38\) at both signs, and allow two launches for one hit. Completion has probability \(1-[(181/200)^2+(179/200)^2]/2=7599/40000\). With a left hit required to reject, power is \(129183/1520000\), strictly below the \(17/200\) predicted by substituting the average rate \(1/10\). For an experiment, the throughput and rate bounds would need their own evidence. The table treats them as given.

### Calibrating the paths before the curvature test

The following prospective protocol makes a single decision using separate reference, pilot and science launches. At each physical sign, send a reference through the two named daughter inputs **before** any path loss. For each raw reference launch a trusted fair chooser sends one event into exactly one input. Redraw the chooser and the independent downstream counter switch on every launch, including misses. Record the chosen input, switch, counter and misses. A detected reference's input label must be read faithfully. The reference must see the same right-to-left efficiency ratio as the signal at that sign, including any dependence on mode, timing or routing. A common factor affecting only the reference changes its completion rate. Keep the signal preparation and detection law fixed between pilot and science. All these calculations assume independent fresh launches at the specified setting.

| Stage | Exposure | Requirement to proceed or reject |
|---|---|---|
| Reference, separately for each sign | First 30,000 detections within 41,500 reference launches | Between 14,778 and 15,222 detected inputs were right, inclusive |
| Signal pilot, separately for each sign | 20,000 ordinary signal launches with the sign fixed | At least 2,071 recorded named hits |
| Fresh science sample after all four checks pass | First 13,300 named hits within 136,130 launches | Reject the curvature bound if at most 7,445 hits were right |

Both reference and science deadlines include the last allowed launch. A failed calibration or timeout gives an inconclusive result and counts as a non-rejection. Register all attempts. A new attempt after an inconclusive result would need a rule for repeated testing. The upper exposure for this one experiment, including both signs, is 259,130 launches.

**Why the full decision controls false rejection.** If the reference ratio is \(\lambda\), the fraction of its detections labeled right is \(\theta=\lambda/(1+\lambda)\). The ratio interval \([20/21,21/20]\) corresponds to \([20/41,21/41]\). At the lower boundary the probability of reaching 14,778 or more right labels in an unlimited sample of 30,000 is 0.048888832433. Reflection gives the same tail for the upper boundary. Monotonicity bounds an erroneous pass beyond either edge, and requiring completion before the deadline can only reduce it. In the signal pilot, the chance of reaching 2,071 hits in 20,000 launches at rate \(1/10\) is 0.048833279046. Smaller rates give smaller probabilities.

If either path ratio lies outside the proposed range, declaring a rejection requires that particular reference to pass. A declaration with an incorrectly certified rate similarly requires the corresponding pilot to pass. When the ratios are within range and the physical curvature null holds, a declaration requires the science sample to reject, with probability at most 0.049787662466. Taking the largest applicable bound gives the same 0.049787662466 upper bound on an erroneous declaration. This is an intersection–union test. Its probability bound applies to all attempted experiments, including calibration failures. [Berger and Hsu, Theorem 1](https://www.public.asu.edu/~rlberge1/papers/statsci96.pdf)

**Power including calibration.** At one specified interior point, take \(c_2\) and equal effective efficiencies \(3/4\) on both paths for both signs and sources. The signal hit probability is \(111/1024\) and its conditional right fraction is \(20/37\). Each completed reference has the same fair binomial label law as the unrestricted first 30,000 detections, since the waits and labels are independent within a fixed sign. All four calibration checks pass with probability **0.954581505531**. The fresh science sample rejects with probability **0.999995990230**. Their product gives **0.954577677878** for passing and rejecting in one attempt. If either sign's true hit rate is exactly \(1/10\), that signal pilot limits the overall rejection probability to at most 0.048833279046, even when the rival is true. [Exact enclosures](results/tag_calibration_counts.json) · [Reproduce the counts](check_tag_calibration_counts.py)

**A reference that responds differently to the signal.** Use the two existing, sign-even models and fixed tick-eight prefix. In the \(c_2\) experiment all right and left efficiencies are \(25/34\). In a second experiment the signal obeys sector autonomy, so its spectator curvature is zero and its incoming right and left masses are \(49/512\) and \(25/512\). Give the reference the same efficiencies \(25/34\), but give the autonomous *signal* efficiencies \(500/833\) on the right and \(1\) on the left. The two signals then have identical recorded right and left probabilities, \(125/2176\) and \(25/512\). Both have hit rate \(925/8704\) and recorded right fraction \(20/37\). Place these losses before an ideal downstream switch and counters. All reference, pilot and science logs then agree in law in the two experiments, including the chosen reference inputs, switches, misses and stopping times. The probability of passing all checks and rejecting is **0.787711458514** in both. This is a false rejection in the zero-curvature experiment. The source-dependent right loss violates precisely the transfer premise.

## Bounding the right fraction from signal records alone

An instrument that identifies some of the **other** tick-nine endpoints can bound the true right fraction using only signal launches. It must record every launch and distinguish a verified outside endpoint from a miss. Name the four possible records certified right \((7,R,1)\), certified left \((5,L,1)\), certified outside the named pair, and unresolved. Each certificate must be correct. Any genuine endpoint may go unresolved, with probabilities that can depend on the endpoint and sign. The outside record requires positive evidence of another endpoint. Silence at the two named detectors belongs in the unresolved category.

At one sign let \(a,b,c,u\) be the probabilities of these four records in order. If the true pair mass is positive, \(1-c>0\). The sharp interval for the true right fraction given the pair is

\[
 \frac{a}{1-c}\ \le\ q\ \le\ \frac{a+u}{1-c}
      =1-\frac{b}{1-c}.
\]

The lower endpoint assigns every unresolved launch to true left. The upper endpoint assigns every one to true right. Each assignment is realizable with faithful reporting and suitable efficiencies. Dividing the unresolved mass between the two named ports attains every intermediate fraction. Allowing some of that mass to be outside cannot enlarge the interval, since the true pair mass is at most \(1-c\) and the true right and left masses are at least \(a\) and \(b\). Averaging the two sign intervals gives the sharp interval for their equal-weighted mean when each sign's reporting law is unrestricted. This uses the usual missing-data principle of considering all completions consistent with the observed law. [Manski (2005)](https://doi.org/10.1016/j.ijar.2004.10.006)

**A finite test that keeps unresolved launches.** Draw a fresh fair sign. Hold it while an outside endpoint is certified. At the first other record, score a certified left as 0 and either a certified right or an unresolved launch as 1. Draw the next sign only after a score. Log all launches and their original categories. Require fresh resets such that the next launch has the specified sign's law conditional on the entire preceding history.

At sign \(s\), a launch produces a score with probability \(d_s=1-c_s>0\). An unrestricted score equals 1 with probability \(p_s=1-b_s/d_s\), the upper endpoint above. Thus the first \(m\) scores in the unlimited experiment are independent Bernoulli draws with parameter \(\bar p=(p_++p_-)/2\). Under the curvature null, \(\bar p\ge(q_++q_-)/2\ge257/444\). A rejection by a fixed deadline is also a rejection in the unlimited experiment. Its lower-tail probability is therefore bounded without specifying certification efficiencies, even when the score and the time it takes to obtain it are dependent.

Retain \(m=4{,}000\) scores and reject if at most 2,263 are ones. Allow at most 28,122 raw launches, including a score on the last launch. A timeout is a non-rejection. The upper bound on false rejection is 0.048670116842. For a power calculation, take \(c_2\) with true masses \((40,34,438)/512\) and certification probabilities \(255/256\) for both left and outside at both signs. Right certification can take any value. Then \(d=9691/65536\) and \(p=5356/9691\) for either sign. The wait and score are independent here. Unconditional power is \([1-F_{B,d}(3999)]F_{4000,p}(2263)\). It is **0.950019928679** at \(B=28{,}122\) and **0.949994230736** one launch earlier. This is the first qualifying deadline for the specified target, cutoff and reporting law. [Exact calculations](results/tag_endpoint_bounds.json) · [Reproduce the bounds](check_tag_endpoint_bounds.py) · [Formal inequalities](lean/TagEndpointBounds.lean)

**How many outside endpoints must be resolved?** If left and outside have a common certification probability \(e\) under \(c_2\), the upper right fraction is \((512-472e)/(512-438e)\). It falls strictly below \(257/444\) exactly when \(e>2816/2853\), about 98.7031%. This is a separation threshold for the observed probabilities. The finite example uses \(e=255/256\). If the instrument certifies no outside endpoints, even perfect reporting at both named detectors leaves an upper right fraction of \(239/256\) under \(c_2\).

**What can remain hidden even at known pair mass?** The following logs are identical across the indicated models at each sign. Masses are in units of \(1/512\). All have true named-pair mass \(74/512\).

| Models | Common log (right, left, outside, unresolved) | Fraction of all launches certified |
|---|---|---:|
| \(c_2\) and \(c_1\) | \((40,31,438,3)\) | \(509/512\) |
| \(c_2\) and zero-curvature sector autonomy | \((40,25,438,9)\) | \(503/512\) |

In each row the rival hides left outcomes and the other model hides right outcomes. The first row crosses the necessary probability threshold since \(40/74<257/444<43/74\). The second row includes a model with exactly zero spectator curvature. At known pair mass \(37/256\), the smallest unresolved mass per sign that can hide a shift from \(c_2\) to the same threshold fraction at both signs is \(17/3072\). In units of \(1/3072\), the two true triples are \((240,204,2628)\) and \((257,187,2628)\), and both can report \((240,187,2628,17)\). The true right masses differ by 17, so any common log must leave at least that much unresolved. These witnesses explain why an overall certification percentage by itself cannot justify the power calculation.
