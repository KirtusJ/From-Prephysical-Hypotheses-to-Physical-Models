# Three detector resolutions after five ticks of one walk

One right-going excitation makes five free Hadamard steps on a nine-site ring. A terminal switch changes where its modes meet the same four-site detector mask. Ten switch settings suffice for a conditional test of ordinary probabilities even if the apparatus draws a new exponent **and** a new scoring resolution on every launch. This is a proposed experiment. The terminal routing stage is additional to the five free ticks. An earlier test using only translations and two read clocks admitted a negative contrast from a detector that scores sites. [Earlier experiment and counterexample](mixed_order.md) · [Ten-setting translation test covering all three resolutions](three_grains.md)

## Input, routing and scoring

A tick sends $R+L$ one site right on R and $R-L$ one site left on L, with a common factor $1/\sqrt{2}$. From $(0,R)$, the five-tick squared rail weights, before division by 32, are four 1s, three 4s and one 16. The ten other rails are dark. A switch permutes the 18 modes without loss, followed by the same read clock and fixed target $T$ comprising both rails of sites 0 through 3. Controls are also needed over which two modes share a site at the input to the detector. A permutation of labels on an already scored data file would act too late. The [Rust checker](check_routed_resolutions.rs) specifies a bijection for each setting, including where the dark modes go. General terminal permutations are an assumption about the hardware. No claim of a synthesis in five free ticks is needed.

Randomly assign the switch independently of the common launch and detector population. A mode carries a finite $q>0$, a scoring order, an offset $a$ and a gain $b\ge0$, with $a,a+b\in[0,1]$. Its chance to report the target is $a+bP$. The three orders compute $P$ as follows.

* **Whole.** Sum the squared weights in $T$ and outside $T$. Raise the two masses to $q$ and normalize.
* **Sites.** Sum the two rail weights at each site. Raise the nine site masses to $q$, normalize once, then add the target sites.
* **Rails.** Raise the 18 rail weights to $q$, normalize once, then add the target rails.

All readout probabilities below use every launch assigned to the setting. The experiment must record missing reports and specify how they enter the reported categories. Offsets, gains, orders and exponents may be correlated within a mode. Their joint law must persist **across settings in distribution**. A common inverse convention can be relabeled once. Unmeasured setting-specific gain, coupling or loss requires a different model.

## First isolate scoring at individual sites

At four separate target sites place the 16 and the three 4s, one per site. Outside the target arrange the four unit rails into two designated pairs. Each pair can occupy two separate sites or the two rails of one site. With zero, one or two pairs joined, the ordinary target mass stays 28/32 and every rail remains present in the normalization. Let $Y_0,Y_1,Y_2$ here denote the rates for these three settings and put $J=Y_0-2Y_1+Y_2$.

Whole and rail modes contribute zero at every exponent. In site mode set $z=2^q$ and $K=16^q+3\,4^q$. The three target chances before reporting are $K/(K+4)$, $K/(K+2+z)$ and $K/(K+2z)$. The contribution to $J$ is

$$
b\frac{2K(z-2)^2}{(K+4)(K+2+z)(K+2z)}.
$$

It is nonnegative and vanishes on a site mode of positive gain exactly at $q=1$. Thus population equality $J=0$ forces ordinary scores on all responsive site modes. This applies the [two-pair spectator refinement](../spectator_refinements.md) to the actual rail spectrum.

## Then isolate scoring at individual rails

Use the same switches and mask with the following target assignments. In each setting route selected occupied rails, in increasing input-label order, into successive target rails. Fill successive exterior rails with the unselected occupied inputs, then put the ten dark inputs into the ten vacancies. This defines the site groupings as well as the named target. The final two columns give all positive site masses and allow a numerical test to retain site-mode effects even when $J$ is uncertain.

| Setting | Individual weights directed into $T$ | Target mass / 32 | Site masses inside | Site masses outside |
| --- | --- | ---: | --- | --- |
| A | 1, 1, 1, 1 | 4/32 | 2, 2 | 8, 20 |
| B | one 4 | 4/32 | 4 | 2, 4, 5, 17 |
| C | 16 | 16/32 | 16 | 2, 4, 5, 5 |
| D | all seven nonheavy rails | 16/32 | 2, 4, 5, 5 | 16 |
| E | two 4s | 8/32 | 8 | 2, 5, 17 |
| F | 16 and those two 4s | 24/32 | 4, 20 | 2, 2, 4 |
| O | none | 0 | none | 2, 2, 8, 20 |

Write $Y_A,\ldots,Y_O$ for these rates and set $W=5(Y_A-Y_B)+Y_C-Y_D$. Equality of the target masses within each comparison makes this zero for every whole mode. If $J=0$, all responsive site modes are ordinary, so they too contribute zero. On a rail mode let $u=4^q$ and $Z=4+3u+u^2$. Its numerator before gain is $5(4-u)+u^2-(4+3u)=(u-4)^2$. Under $J=0$, equality $W=0$ therefore implies $q=1$ on every responsive rail mode. Individual site-mode contributions to $W$ may have either sign before the first equality has been established.

## Finally test whole-mask scoring

Use O, B, E and F, whose squared fractions are $0,1/8,1/4,3/4$. Write $B_0=Y_E+Y_F-2Y_O$, $m=(7/12)\log(7)/\log(3)$ and $k=m/2-1/4$. The third contrast is

$$
V=kB_0-2m(Y_E-Y_O)+2(Y_B-Y_O).
$$

Under $J=W=0$ the responsive microscopic modes already act ordinarily. They contribute zero to $V$. A whole mode contributes zero precisely at $q=1$ for positive gain, and a strictly positive amount at the other exponents. In detail, let $t=(3^q-1)/(3^q+1)$, $h(t)=\tanh[(\log7/\log3)\operatorname{atanh}t]$. The whole-mode contribution is $b[h(1/2)+h'(1/2)(t-1/2)-h(t)]$. Here $h(1/2)=3/4$, $h'(1/2)=m$, and $h''(t)<0$ for $0<t<1$. [Full concavity calculation](translated_mask.md#what-a-common-binary-instrument-implies)

Consequently, **$J=W=V=0$ with $B_0>0$ identifies $q=1$ almost surely among the modes with positive gain.** Conversely these equalities hold for any mixture of the three orders at $q=1$, when $B_0=E[b]$. In that case no choice of mask can identify how often the detector used each order. Zero-gain modes are invisible throughout. The theorem tests the specified power and reporting families. Independent redraw on every launch is permitted. A persistent mode is also permitted if randomized settings sample the same mode law.

## What finite data can establish

The equalities are sequential population implications. A confidence interval for $J$ containing zero does not set a site's contribution to $W$ to zero. The following simultaneous feasibility formulation uses the unrounded ten rates throughout. For independent Bernoulli shots within each setting $h$ with sample size $n_h$, intersect $[0,1]$ with $\widehat Y_h\pm\sqrt{\log(20/\alpha)/(2n_h)}$. All ten population rates then lie in their intervals together with probability at least $1-\alpha$. Other valid uncertainty sets may be substituted.

For an order $o$ let $p_o(q)$ be its ten-vector of target probabilities, computed from the tables. Let positive measures $\mu_o$ on $(0,\infty)$ represent gain-weighted mode laws and $\bar a$ the common mean offset. Test the common system

$$
Y=\bar a\,\mathbf{1}+\sum_o\int p_o(q)\,d\mu_o(q),\qquad
\bar a\ge0,\quad M=\sum_o\mu_o((0,\infty))\le1-\bar a,\quad
Y_h\ \text{in its interval for every }h .
$$

Every admissible population gives such measures. Conversely, masses $\mu_o$ may be implemented by modes with $a=0,b=1$, with remaining probability allocated to always-report and never-report modes to supply the required offset. To bound the gain-weighted fraction outside a chosen exponent range, maximize the corresponding measure divided by $M$ over the feasible models with $M>0$. A strictly positive lower bound for $M$ is needed for an informative fractional bound. The finite contrast data do not by themselves justify treating a discretized exponent grid as exhaustive. Rigorous continuous-parameter enclosures or an analytic dual certificate are needed before reporting numerical exclusions. No shots have been acquired for these switch settings.

## Check

Compile the adjacent Rust file with edition 2021 and warnings denied. It checks every initial rail weight, the terminal bijections, the routed mass classes in all ten settings, and the denominator-cleared square identities by exact integer polynomial interpolation.
