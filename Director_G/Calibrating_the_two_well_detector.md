# Reading a winding phase with an uncalibrated terminal detector

**Kirtus Justus**, Theoretical Physicist, Port Coquitlam, British Columbia, Canada. Research supplement by Director G (OpenAI Codex).

On two wells, sharp launches and two native controls can calibrate an unknown terminal rail detector. Its reports can include missed detections, dark clicks, rail confusion and an ambiguous output. An instrument that measures a coherent combination of the rails can pass those controls and falsely select a phase absent from the source. Randomly reversing the sign of the final left-rail amplitude removes this ambiguity for a fixed quantum measurement. The protocol still needs a stable response and enough visibility to observe the source. [Ideal-detector phase witness](Two_well_phase_witness.md)

## Calibrate the channel at the well that receives the walk

Launch on rail $R$ and evolve with the coherent coin $U_\beta=\mathrm{diag}(1,\beta)H$ for $|\beta|=1$. The competing model counts each word of length $t$ with weight $2^{-t}$. Suppose a stable fraction $c$ follows fair counting and the coherent subprobability $\nu$ is distributed over $x=\operatorname{Re}\beta$. The physical readout is the complete distribution of report symbols per attempted launch. Assign an explicit outcome to missing, double or ambiguous detections whenever these can occur. If the launch itself is unheralded, the known exposure per setting is an additional requirement.

First assume a detector at well $w$ where every report is produced by a fixed stochastic channel with arbitrary columns $K_w(\cdot|R),K_w(\cdot|L)$. These can be different at the two wells. Read a sharp $R$ at tick zero and, on a fresh launch from the adjacent well, read the same detector at tick one. Both the coherent and counted walks have right-rail probability $1/2$ after the first step. Write $U_w$ and $B_w$ for the observed zero- and one-tick report distributions. Then
$$K_w(\cdot|R)=U_w,\qquad K_w(\cdot|L)=2B_w-U_w.$$
In particular $2B_w-U_w$ must be a probability distribution. A test distribution must lie on the line segment with these two columns as endpoints. With more than two report symbols these are checkable restrictions on the data.

For a predetermined event $A$ among the report symbols, write $d_w=U_w(A)-B_w(A)$. If $d_w\ne0$ the raw test frequency $Y_t(A)$ at $w$ gives the ideal right-rail bias
$$b_t=2p_t(R)-1=\frac{Y_t(A)-B_w(A)}{d_w}. \tag{1}$$
All assignments must use the same detector response at that well. With a common sharp launch, tick two and tick three end on different wells. Each can use its own controls and its own event. If the controls at both wells are informative on the same fixed rail-only channel within each well, a translation of the **test** source is unnecessary. If one terminal well is blind, the missing frequency can instead be measured by translating the initial well so both readouts arrive at the informative detector. That use of translation additionally requires transporting the same phase ensemble and arc law. A blind channel at both wells supplies no rail information.

Set the target cosine $m=\operatorname{Re}\beta_*$ in advance. In the mixture, $b_2=\int x\,d\nu$ and $1-b_3=c+\int x^2\,d\nu$. The affine channel thus yields the same nonnegative witness as an ideal detector:
$$W_m=1-b_3-2m b_2+m^2=\int(x-m)^2\,d\nu+c(1+m^2). \tag{2}$$
Its exact zero requires $c=0$ and support on the designated conjugate pair. The pure cubic target has $m=-1/2$, $b_2=-1/2$, $b_3=3/4$. The two native controls supply operational endpoints of (1); they presuppose the sharp launch and the balanced step. They give no empirical reason by themselves to choose a phase or probability law.

## A coherent detector that imitates a cubic phase

The linear channel above only uses the rail populations. A quantum detector can also respond to rail coherence. Take the binary effect
$$E=\frac{I+(Y+4Z)/5}{2},$$
where $Y,Z$ are Pauli matrices with $Z|R\rangle=|R\rangle$. This is a mixture of the positive $Y$ and positive $Z$ projectors with weights $1/5,4/5$. Use one detector and the *same* ensemble in all four settings, with phase $-1$ on $1/5$ of launches and $i$ on $4/5$. Both are outside the designated cubic pair. For a direct derivation write $(X,Y,Z)$ for Bloch coordinates, $a=\operatorname{Re}\beta$ and $s=\operatorname{Im}\beta$. One step, first $H$ then the relative phase, sends
$$(X,Y,Z)\longmapsto (aZ+sY,\ sZ-aY,\ X).$$
Starting from $(0,0,1)$ gives
$$ (U,B,Y_2,Y_3)=(45,29,21,41)/50. $$
Equation (1) returns the two cubic biases exactly. The inferred left column $2B-U=13/50$ is legitimate. A binary report lies on the inferred segment at both test times, despite the false conclusion from (2).

To repair this failure for an arbitrary fixed terminal effect, draw an independent fair bit per trial. Apply $I$ or $Z=\mathrm{diag}(1,-1)$ **after** the last coherent step. Equivalently at a positive clock multiply the gains on both arcs *arriving on L* by the chosen sign at the final tick. The zero-tick sharp control is already diagonal. For each report effect $E_j$, averaging its two toggled responses gives $(E_j+ZE_jZ)/2$, which consists precisely of its diagonal entries. Thus the original populations and all fair-count probabilities survive while every off-diagonal readout term cancels. This is the standard complete dephasing channel applied only at the terminal surface. Randomizing signs in the interior would change propagation. The sign switch, independent setting choice, both exposures and a detector whose effects are stable across them are physical inputs. A source with an inaccessible sign arc does not acquire this capability from the calculation. [Quantum channels, complete dephasing](https://learning.quantum.ibm.com/course/general-formulation-of-quantum-information/quantum-channels)

The same false-pass example then gives $(45,25,21,41)/50$. Its recovered biases are $-1/5$ and $4/5$, hence $W_{-1/2}=1/4$. The two subensembles' distances from $-1/2$ both equal $1/2$. Their mean square gives the same result. A pure cubic source sent through this same instrument and the sign switch has $W_{-1/2}=0$. Stable losses and coherent detection can coexist (add a missing-output effect); the symmetrization applies to every report.

## Hidden phase dependence of detector visibility

Suppose even the diagonal channel depends on a latent label $\lambda$, which may include the choice of count or coherent dynamics. For one fixed well and report event, put $v(\lambda)=K_\lambda(A|R)-K_\lambda(A|L)$. Use the **same ensemble** for every clock and control, for example by translating homogeneous launches to end at this well. Conditional on $\lambda$, the control at tick one is balanced and the one at tick zero is sharp. Therefore the normalized bias (1) is exactly
$$\frac{\mathbb{E}[v(\lambda)b_t(\lambda)]}{\mathbb{E}v(\lambda)}. \tag{3}$$
If $v$ has strictly one sign almost everywhere, (2) holds for the reweighted distribution $|v|\,dP/\mathbb{E}|v|$. Its zero set still selects the true pure response. Strict visibility supplies equivalence of these measures. A completely invisible off-target subpopulation can evade this test. If $0<v_{\min}\le |v|\le v_{\max}$ on the full source, the observed witness bounds the original count fraction by $(v_{\max}/v_{\min})W_m/(1+m^2)$ and original coherent mass with $|x-m|\ge\delta$ by $(v_{\max}/v_{\min})W_m/\delta^2$. Without a quantitative lower visibility bound the corresponding original-mass limits need not be small.

Two examples show why the common weighting matters. First, mix $x=-1,0,1$ with weights $(3,6,1)/10$. Use fixed midpoint $1/2$ and contrasts $v=(1,1,-1)$ on the three labels. The signed reweighted masses are $(3/8,3/4,-1/8)$. Their first two moments imitate $-1/2,1/4$ with no cubic phase present. Second, take $x=-1,0$ with equal weights, all contrasts positive, and rail midpoint $1/2$. Use visibilities $(1,1)$ at the tick-two well and $(1/3,1)$ at the tick-three well. Local controls infer $b_2=-1/2$ and $b_3=3/4$ again. Each well sees a different reweighted population. Routing both clocks and both calibrations to either one of these wells removes this particular alias. Globally proportional contrast functions on the support would also suffice. These are specific exact failures of the inference under changed observation hypotheses.

## Keeping uncertainty in the denominator

Suppose an independent calibration or simultaneous confidence intervals give absolute errors $e_Y,e_U,e_B$ on the three raw frequencies at a clock. Let $\widehat d=\widehat U-\widehat B$, and compute $\widehat b=(\widehat Y-\widehat B)/\widehat d$ only for $\widehat d\ne0$. For an actual stochastic rail read, $|b|\le1$. From $\widehat d(\widehat b-b)=(\widehat Y-Y)-(1-b)(\widehat B-B)-b(\widehat U-U)$ it follows that
$$|\widehat b-b|\le(e_Y+2e_B+e_U)/|\widehat d|.$$
To certify nonzero true contrast from the same intervals, require $|\widehat d|>e_U+e_B$ or retain a one-sided interval excluding zero. A denominator near zero yields a poor bound. If the bias errors are bounded by $e_2',e_3'$, use $W_m\le\widehat W_m+2|m|e_2'+e_3'$. Joint coverage can be obtained by a union bound over the raw frequencies used, including calibrations shared across clocks. At one common well with a common event, the same data also give the score without dividing any raw measurement:
$$dW_m=(1+m^2)U+(2m-m^2)B-2mY_2-Y_3.$$
Its raw-error bound is $(1+m^2)e_U+|2m-m^2|e_B+2|m|e_{Y_2}+e_{Y_3}$. Keep the estimated denominator and its sign interval with the raw score. Dividing to infer a quantitative phase or count fraction again needs resolved contrast. These bounds apply under the stated response assumptions.

Run the checker with a fresh output directory. It retains the raw channels and distributions, blind and sign-changing settings, the coherent counterexample, the sign repair and the finite error calculation. [Checker](check_detector_visibility.py) · [Exact results](results/detector_visibility.json) · [Lean checks](lean/DetectorVisibility.lean)
