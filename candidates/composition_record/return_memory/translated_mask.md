# Four launch sites test the probability rule of a three-tick walk

A nine-site ring, one sharp right-going input, three identical Hadamard steps and a fixed binary detector suffice for a conditional selection theorem. Change only the starting site. Four population rates then identify the ordinary exponent even if the detector draws a different positive exponent on every launch. The essential physical question is **what the detector scores**. Scoring each oriented port first and pooling reports afterward admits an explicit nonordinary mixture that matches every one of the four ordinary rates.

## The preparations

Number sites modulo nine. Each tick takes the signed inputs \((u,v)\) at a site to \(u+v\) at its right neighbor on rail R and \(u-v\) at its left neighbor on rail L. From a sharp unit R source, the integer squared norm after three ticks is eight. Relative to the starting site, the occupied displacements \(-3,-1,1,3\) have rail totals \((0,1),(-1,0),(2,1),(1,0)\) respectively. The terminal device presents two cells, **both rails of wells \(\{0,2\}\)** together and the entire remainder of the ring together. No intermediate measurement or conditional acceptance occurs. For each preparation let \(p\) be the fraction of the conserved squared norm in the target cell. This definition is a calculation on signed paths. The physical sampling law is the unknown. [Signed-walk specification](../../../Director_G/candidates/edge_record_walk/specification.md)

| Starting site, always rail R | Target squared norm out of eight | \(p\) |
| ---: | ---: | ---: |
| 0 | 0 | 0 |
| 5 | 1 | \(1/8\) |
| 3 | 2 | \(1/4\) |
| 1 | 6 | \(3/4\) |

The checker sums signed paths recursively, then compares independent enumeration of all eight histories at each of the nine source translations, including the dark rows. [Exact Rust replay](check_translated_mask.rs)

## What a common binary instrument implies

Suppose the chance of a recorded target report for an individual instrument mode is \(a+b\,g_q(p)\), where \(g_q(p)=p^q/[p^q+(1-p)^q]\), \(0<q<\infty\), and \(a,a+b\in[0,1]\). The joint population of \((a,b,q)\) must be the same under all four random launch choices. Permit arbitrary correlation between gain and exponent. Take \(b\ge0\) and \(E[b]>0\). A common inverted reporting convention can be reversed once. Let \(Y_p\) be the rate per original launch. Then

$$
B=Y_{1/4}+Y_{3/4}-2Y_0=E[b],\qquad
Z_p=(Y_p-Y_0)/B=E_\nu[g_q(p)],\quad d\nu=b\,dP/E[b].
$$

The equality for \(B\) uses the two *physically prepared* weights and the symmetry \(g_q(p)+g_q(1-p)=1\). It requires no bright bypass and no change of readout or clock. A zero-gain mode receives zero weight.

Set \(T=(3^q-1)/(3^q+1)\), \(k=\log7/\log3>1\), and \(h(T)=\tanh(k\,\mathrm{atanh}\,T)\). The two measured contrasts give \(E_\nu T=1-2Z_{1/4}\) and \(E_\nu h(T)=1-2Z_{1/8}\). On \(0<T<1\), \(h>T\), \(h'>0\), and

$$
h''(T)=\frac{2h'(T)}{1-T^2}\big[T-kh(T)\big]<0 .
$$

At \(q=1\), \(T_*=1/2\) and \(h(T_*)=3/4\). Agreement with the two ordinary readings gives equality in strict Jensen concavity, hence \(q=1\) for almost every responsive launch. This applies even when powers below and above one are mixed.

A single linear comparison can be used without dividing by a noisy \(B\). Write \(m=h'(1/2)=7k/12\) and compute

$$
L=(m/2-1/4)B-2m(Y_{1/4}-Y_0)+2(Y_{1/8}-Y_0).
$$

It equals \(B\,E_\nu[3/4+m(T-1/2)-h(T)]\). The integrand is strictly positive away from \(T=1/2\). Thus \(L=0\) and \(B>0\) suffice for exact selection in this family. For a target exponent range separated from one, minimize that tangent gap on its closure, including the limits at \(q=0,\infty\) if required. Dividing a simultaneous upper bound on \(L\) by a positive lower bound on \(B\) and the positive minimum bounds the **gain-weighted** fraction in that range.

In an experiment randomize and interleave source translations, count every launch and track failures, lost records and the response convention. If the four sample sizes are \(n_i>0\) and shots within each arm are independent with a common rate, simultaneous rate errors are at most \(e_i=\sqrt{\log(8/\alpha)/(2n_i)}\) with confidence at least \(1-\alpha\). Propagate them through the displayed linear forms for \(L\) and \(B\) by summing absolute coefficients times \(e_i\). This allows a negative observed contrast and retains it with uncertainty. Source-dependent losses or drive changes can change the mode population. An arbitrary response outside the power family can pass all four values. [Hoeffding, Theorem 2](https://doi.org/10.1080/01621459.1963.10500830)

## A rival when the apparatus scores rails first

There are four light oriented ports of squared norm one and a single heavy port of squared norm four. Normalize powers over *these five ports* and then pool any reported target ports. Each light port has probability \(\ell_q=1/(4+4^q)\), and the heavy port has \(1-4\ell_q\). In table order these instruments give target rates \(0,\ell_q,2\ell_q,1-2\ell_q\). Draw \(q=1/2\) with probability \(9/14\) and \(q=2\) otherwise. Each light port then has mean probability \((9/14)(1/6)+(5/14)(1/20)=1/8\). The four ordinary rates are reproduced **exactly**, with a perfect reporter and no ordinary exponent anywhere. In fact every grouping of those same resolved ports gives the ordinary population probabilities for this mixture. Changing software labels on fine records cannot settle the physical scoring order.

## Testing the resolved-port rival with the same mask

Run the *same coin, shift, source rail and two-well detector* for **five ticks**. Across the complete ring there are four light oriented ports of squared norm one, three of squared norm four and one of squared norm sixteen. For the fully resolved rival put \(u=4^q\) and \(Z=4+3u+u^2\). Each light, medium and heavy port now scores \(1/Z,u/Z,u^2/Z\), respectively. Changing the starting well places different subsets of these ports inside the physical mask. All other ports remain in the normalization.

| Starting well | Light ports in mask | Medium | Heavy | Ordinary target fraction |
| ---: | ---: | ---: | ---: | ---: |
| 0 | 0 | 0 | 0 | 0 |
| 1 | 0 | 2 | 0 | \(8/32\) |
| 4 | 1 | 0 | 0 | \(1/32\) |
| 6 | 2 | 0 | 1 | \(18/32\) |

Writing \(W_s\) for the incident report rate from source \(s\) at tick five gives

$$
 W_6-4W_1+14W_4-11W_0
 =E\!\left[b\,\frac{u^2-8u+16}{4+3u+u^2}\right]
 =E\!\left[b\,\frac{(4^q-4)^2}{4+3\cdot4^q+16^q}\right].
$$

The dark-source subtraction cancels a common mean additive background. The identity holds with arbitrary correlations of exponent and reporting gain, a shared population across the four settings, fine-port normalization before pooling and the same affine reporting convention as above. Every term is nonnegative for \(b\ge0\). Under this mechanism equality with the ordinary contrast forces \(q=1\) on the responsive population. The exact three-tick impostor with unit gain gives a five-tick contrast of \(27/77\), while the ordinary prediction is zero. This is a directly measurable difference using four binary rates. The checker verifies every port involved and the three integer coefficients. The argument is a translated-mask implementation of a known three-mass criterion. [Earlier theorem for resolved and partially resolved bins](../../../Director_G/When_a_position_histogram_identifies_its_probability_power.md)

Run both panels if it is unknown which of the two specified scoring orders a stable instrument uses. If both contrasts vanish at population level and one of these orders governs the entire apparatus, the corresponding theorem identifies the ordinary exponent on the responsive modes tested at its clock. Transferring the conclusion across clocks requires a common population or separate calibration. If the instrument mixes the two orders across hidden modes, a repeated quarter-weight preparation gives a joint test using only five settings. [Proof for mixed scoring orders and a third resolution that evades it](mixed_order.md) Both tests concern a specified family of probability laws.

Existing single-atom work demonstrates sharp local preparation, state-dependent shifts and site-resolved imaging. A site-resolved image supplies a record at that instrument's resolution. Establishing the physical binary coupling, its stability across the translated input wells, and its relation to that resolution remains experimental work. No new hardware records were acquired. [Karski et al., original experiment](https://arxiv.org/abs/0907.1565) · [Monitored-circuit comparison](four_phase_mixture.md)

OpenAI Codex constructed and checked the launch panel, selection argument and rival in the research program of Kirtus Justus, Theoretical Physicist, Port Coquitlam, British Columbia, Canada.
