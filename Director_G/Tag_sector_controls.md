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

Use the fair value \(1/2\) at any zero denominator. The left fraction is the complement. Both are legitimate local stochastic mechanisms since \(2|u_bv_b|\leq s_b\). Each uses the same undisturbed signed walk, copies the tag by the specified permutation, conserves the marker, and preserves its tag between copies. The spectator rule is continuous on the joint unit sphere, depends only on the tallies at the current site, and is invariant under global rescaling. It is equivariant under exchange of the two bit names and under independent common sign flips of each sector. Its response equals the sector rule for every occupied pure input. In a globally pure-tag flight the two markers consequently agree at all depths by induction. The same induction works while the two signed sectors occupy disjoint sites.

Choosing the complementary initial bit and repeating the same XOR schedule swaps the labels in every panel of both models. A spacetime-dependent change of names also preserves their decoded answers when carried through the links. For a frame \(g_t(x)\in\{0,1\}\) write the new name of a tag as \(b'=b\oplus g_t(x)\). A preserving edge \(x\to y\) must then apply \(g_t(x)\oplus g_{t+1}(y)\); a physical XOR on arrival composes with this change. A flip at a single site followed by unmodified links instead changes which physical inputs can interfere. Relabeling symmetry by itself therefore supplies no protection against the spectator rule.

## Two settings at the same splitter

Use the integer line, or identify the sites \(-4,\ldots,4\) on a periodic ring of at least nine sites and apply the same mask on the initial light cone. In setting \(O\), launch \((0,R,0)\). Immediately after tick one apply \(b\leftarrow b\oplus\mathbf 1_{x>0}\) to both rails, then keep the bit. At tick two the two signed pairs at \(x=0\) are \((1,0)\) in tag zero and \((0,1)\) in tag one. Both rules split both sectors equally there. Their full panels coincide through tick three. At \(t=3,x=1\), the pairs are now \((1,0)\) and \((1,1)\), respectively. The tag-one parent has marker mass \(1/4\). Its right fraction is 1 under sector autonomy and \(5/6\) with the spectator. At \(t=4\) the tagged left daughter \((0,L,1)\) has mass 0 or \(1/24\).

In setting \(S\), prepare the sharp selected port \((+1,R,1)\) at absolute tick one. This is the complete surviving tag-one field of \(O\) at that clock, up to common amplitude normalization. Carry out the same remaining ticks at the same sites. At tick three the selected splitter again has raw pair \((1,1)\); its parent probability is \(1/2\). Both rules give zero on its left daughter. The left daughter-to-parent ratio is thus \(0\) in \(S\), versus \(0\) or \(1/6\) in \(O\). Both kernels here are independent of overall scale, past controls and marker history. Operational comparison requires characterizing a sharp restart or a physical early arm removal, including any disturbance to the surviving port, clock, intensity and marker preparation. A late selection of tag one from \(O\) leaves the spectator active during the split.

There is also an all-positive contrast. At tick four take \(A=(-2,L,1)\), \(B=(2,R,1)\). Every cell is a fraction of all launches for its setting.

| Model | \(O_A\) | \(O_B\) | \(S_A\) | \(S_B\) | \(O_A S_B/(O_B S_A)\) |
|---|---:|---:|---:|---:|---:|
| Sector autonomy | \(1/16\) | \(1/4\) | \(1/8\) | \(1/2\) | 1 |
| Local spectator dependence | \(1/16\) | \(5/24\) | \(1/8\) | \(1/2\) | \(6/5\) |

If the expected counts factor as \(C_{ij}=L_i\eta_j P_{ij}\) with positive setting brightness \(L_i\) and stable per-port efficiency \(\eta_j\), both factors cancel in this ratio of expected counts. Comparing sampled counts requires an uncertainty treatment, including possible empty measured bins. Additive background, port crosstalk and changes in relative efficiency across settings require separate characterization.

Absolute universality of the splitting law is stronger than these tests require. For a particular instrument one can require equality to the shielded fraction only at each occupied local context that occurs during its specified operations, with a verified reference for each compared selected input. Together with the initial marker and correct tag transport, those equalities suffice to replay its joint terminal masses step by step. Alternatively, fresh adjacent panels identify each tested mixed fraction directly. Extension to a different set of operations needs new data or a physical reason for that transfer. This finite example shows that even continuous local rules with the same pure-label responses can differ on this extension.

The checker enumerates signed words independently of the marker update, includes zero and inaccessible bins, compares both initial labels, and repeats every calculation in a varying spacetime label frame. It retains 464 joint cells across five settings and 24 time panels. [Standard-library checker](check_tag_sector_controls.py) · [Exact panels](results/tag_sector_controls.json)
