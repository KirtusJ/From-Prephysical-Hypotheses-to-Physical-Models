# Reading one spatial record in two bases constrains fluctuating powers

**Kirtus Justus**, Theoretical Physicist, Port Coquitlam, British Columbia, Canada. Research supplement by Director G (OpenAI Codex).

On an eight-well ring, the first direction can be stored in a bit and read in either of two bases. The same pair of terminal sites has the same predicted probability in both outcomes of either read. Within a family of detectors that apply a fluctuating power to the site weights *inside each pointer outcome*, changing the basis supplies a comparison that the bare staircase lacked. Combined with a nine-tick staircase comparison it forces the ordinary exponent on every launch except a set of probability zero. Neither test requires a prescribed absolute site frequency.

## Three ticks, two bases, one position event

Start at site zero on R, with a blank two-state pointer. Use three free balanced Hadamard walk ticks. After the first tick XOR the predicate $x=+1$ into the pointer. The two possible positions at that clock are $+1$ and $-1$, so the bit retains the first direction. The next two ticks act on position and rail alone. At the common final surface choose to read the pointer in its recorded (Z) basis or to apply a single balanced Hadamard to it and then read (X). Read both outcomes jointly with position, summing over the walker's final rail. Compare the frequency of the event $B=\{3,5\}$ modulo eight across the two settings, on all original launches.

This requires a coherent blank pointer, a selective copy, a calibrated analyzer and a stable site read. A separate routed multi-site construction gives a single basis contrast with a definite sign for every wrong exponent. Its additional label controls and rail routes change the accessible preparations. [Four-site routed label test](https://github.com/KirtusJ/From-Prephysical-Hypotheses-to-Physical-Models/pull/97)

The existing parity-encoded eraser specifies a nearest-neighbor transposition and one coin tick that realize the two-output sum and difference. A separate bit analyzer or a clock-matched decoder must address the same logical outputs. A genuine remote non-signalling interpretation additionally needs separation of the basis choice from the position read. Coherent bit control on one device supplies a test of basis dependence without that inference. Retain both pointer and site outcomes, including losses or their calibrated contribution, for either setting. Polarization eraser experiments supply a physical precedent for basis-selective reading of which-way information and coincidence-resolved outcomes. [Walk eraser and its decoder](Parity_record_eraser.md) · [Walborn et al., optical double-slit eraser](https://doi.org/10.1103/PhysRevA.65.033818)

The integer rows below are kinematic site numerators after adding the two squared final-rail coordinates. The rows of a given basis have a common amplitude scale. A final H gives the sums and differences of the original flagged amplitudes at each rail. All eight signed histories are retained.

| Pointer basis and outcome | Site 1 | Site 3 | Site 5 | Site 7 | Whole-launch denominator |
|---|---:|---:|---:|---:|---:|
| Z, bit 0 | 1 | 0 | 1 | 2 | 8 |
| Z, bit 1 | 2 | 1 | 0 | 1 | 8 |
| X, bit 0 | 5 | 1 | 1 | 1 | 16 |
| X, bit 1 | 1 | 1 | 1 | 5 | 16 |

## A relative comparison replaces an absolute calibration

For a given positive exponent $q$, let the site distribution inside a reported pointer row of weights $v_i$ be $v_i^q/\sum_j v_j^q$. The distribution of $q$ is stable across the basis choice and the staircase settings below. The readout may mix rows with arbitrary weights depending on the basis and $q$. In Z, *each* row gives $P(B)=x(q)=1/(2+2^q)$. In X, each gives $P(B)=2y(q)$, where $y(q)=1/(3+5^q)$. No branch probabilities enter the comparison. A detector normalizing its powered cells jointly across both rows also has these rates because the two row denominators coincide inside each basis. At $q=1$ both settings give $1/4$. At $q=2$ they give $1/6$ and $1/14$.

Use the same source's eight nine-tick words with a switchable staircase sign and no marker. For site 1, the odd and even groups there give $A(q)=x(q)$ and $B_9(q)=1/2-x(q)$. Equality of those two group means implies $E[x]=1/4$. Equality of the three-tick basis rates implies $E[2y-x]=0$, hence $E[y]=1/8$. These are expectations under the common exponent distribution; the analysis does not assign either site's underlying trials an observed Born frequency. The strict supporting-line inequality on $q\ge0$ from the staircase calculation is
$$D(q)=y(q)-\tfrac18-m(x(q)-\tfrac14)\ge0,\qquad m=\tfrac58\log_2 5,$$
with equality only at $q=1$. Thus $E[D]=0$ forces the ordinary exponent almost surely. The nine-tick words, controls and proof of strictness are given in the [staircase supplement](Forward_staircase_and_spatial_probability.md). The two test discrepancies $\delta_3=E[2y-x]$ and $\delta_9=E[B_9-A]$ satisfy the exact identity
$$E[D]=\tfrac12\delta_3+\tfrac12(m-\tfrac12)\delta_9.$$
Consequently simultaneous bounds on the two discrepancies give a bound on the mass outside any specified neighborhood of one by dividing the corresponding upper bound on $E[D]$ by the positive infimum of $D$ there. The infimum remains positive at both endpoints $q=0,\infty$ in the limiting models.

For the known nine-tick false pass, take $q=\log_2(3/2)$ on $7/10$ of launches and $q=2$ on the rest. The recorded-basis rate on $B$ is $1/4$. The X-basis rate is $\tfrac75/(3+5^{\log_2(3/2)})+\tfrac3{140}$, approximately $0.27306$. The comparison distinguishes this mixture even if the two reported flag outcomes have unequal weights. It depends on the score family and one source distribution shared by all settings. It does not identify a hidden sublabel that can independently renormalize arbitrary portions of each row.

## What forgetting the pointer first can conceal

Summing the two kinematic rows in either basis gives exactly $(3,1,1,3)/8$. A rule that combines all cells by site before applying any power is therefore insensitive to this basis choice for every exponent, including a mixture that passes the nine-tick test. Even reporting two pointer labels does not by itself prove the conditional score hypothesis. For example, select the site according to those pooled powered site weights, then attach a bit according to the ordinary proportions of the two kinematic cells at the selected site in the selected basis. This yields a complete joint record with the same marginal for each choice. It can be challenged by checking the measured conditional tables on preparations with independently known responses. Families that may choose the all-pooled convention therefore cannot be ruled out by these two marginal equalities. The seven-tick local marking test gives separate constraints for choices that combine or split **within** sites. [Flag partitions and a false pass](Partial_flag_readout_and_spatial_powers.md)

The exact four-row calculation is verified with a position recurrence, signed word enumeration and Lean 4.19.0 reduction of the walk itself. The checker covers each conditional and globally normalized joint-cell read, integer powers including the zero-power limit and unequal branch-weight controls. These are proposed frequency tests. No spatial data were acquired. [Python checker](check_two_record_bases.py) · [Exact rows](results/two_record_bases.json) · [Lean recurrence](lean/TwoRecordBases.lean)
