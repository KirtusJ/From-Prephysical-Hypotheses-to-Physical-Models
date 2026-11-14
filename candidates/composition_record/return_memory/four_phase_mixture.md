# Four survivor phases test a mixture of binary power responses

Four choices of the phase on site 2 give a return-count comparison in which exponents above and below one contribute with the same sign. Within the model below, equality with the ordinary prediction forces exponent one on almost every responsive survivor. The comparison uses one detector and needs no separate dark, bright or balanced reference. Only the π/2 **phase shift** is shared with the preceding three-phase test. All four arms use the same π/4 **link rotation**. This is a proposed extension of the monitored three-spin experiment. [Three-phase preparation, controls and a mixture passing the midpoint test](phase_cycle.md) · [Liu et al., original experiment](https://arxiv.org/html/2401.09810v2#S8)

## Settings and denominator

Start the walker at site 0. Retain the survivors with recorded misses at the first two measurements. Randomly assign a phase after that common record, then count returns at the third measurement. With the stipulated coherent survivor and final gate order, the squared site-0 coordinate is $x(\phi)=1/4-(\sqrt 2/6)\cos\phi$. Use $A=\sqrt3$, $x_n=(1+A^n)^{-1}$ and $\phi_n=\arccos[6(1/4-x_n)/\sqrt2]$. Each setting lies inside the available interval.

| $n$ | Squared coordinate $x_n$ | Applied phase $\phi_n$ (radians) |
| --- | ---: | ---: |
| 1 | 0.3660254 | 2.0854738 |
| 2 | 0.2500000 | 1.5707963 |
| 3 | 0.1613905 | 1.1853871 |
| 4 | 0.1000000 | 0.8809792 |

Let $Y_n$ be reported returns divided by **all assigned survivors** in arm $n$, interpreted below as the population rate. Record launch, selection, assignment and no-report counts separately. The proposed binary response scores site 0 and its entire complement. Routing that complement through several separately scored cells changes the model. The phase control and common survivor need independent physical checks. A distorted interference curve changes the four $x_n$ themselves.

Each survivor may have its own finite $q>0$, offset $a$, and gain $b$. The model for its reported click chance at setting $n$ is

$$
a+b\,g_q(x_n),\qquad g_q(x)=\frac{x^q}{x^q+(1-x)^q}.
$$

The joint distribution of $(q,a,b)$ is common to the randomized arms, $0\le a,a+b\le1$, and every nonzero gain has the same sign. Dependence among $q,a,b$ within a shot is allowed. We write the proof for positive gain. A consistently inverted reporter uses the complementary report category. Nonzero contrast $Y_1-Y_2$ is required.

## A linear contrast with a fixed sign

Set $T=\tanh(q\log A/2)$ and $F_n=1-2g_q(x_n)=\tanh(nq\log A/2)$. Define $D=F_2-F_1=T(1-T^2)/(1+T^2)>0$. The distribution $\nu$ weights each survivor in proportion to $bD$. Since $Y_1-Y_n=E[b(F_n-F_1)]/2$, ratios of differences are expectations under the **same** distribution:

$$
\frac{Y_1-Y_3}{Y_1-Y_2}=2+E_\nu z,\qquad
\frac{Y_1-Y_4}{Y_1-Y_2}=E_\nu H(z),\qquad
z=\frac{-4T^2}{1+3T^2},\quad H(z)=\frac{(z+2)(2z+3)}{2-z^2}.
$$

For a direct algebra check, $F_1=T$, $F_2=2T/(1+T^2)$, $F_3=T(3+T^2)/(1+3T^2)$ and $F_4=4T(1+T^2)/(1+6T^2+T^4)$. Dividing $F_3-F_1$ and $F_4-F_1$ by $D$ gives $2+z$ and $H(z)$ respectively. On $-1<z<0$,

$$
H''(z)=\frac{2(z+2)(7z^2+16z+10)}{(2-z^2)^3}\geq\tfrac14 .
$$

Indeed $7z^2+16z+10$ is increasing there and equals one at $-1$. Also $z$ decreases strictly with $q$. Write $z_*=(4\sqrt3-10)/13$ for its value at $q=1$, $h'=H'(z_*)$, and $c=H(z_*)-h'(2+z_*)$. An observable which avoids dividing by small gaps is

$$
L=(Y_1-Y_4)-h'(Y_1-Y_3)-c(Y_1-Y_2).
$$

Its coefficients, in setting order, are approximately $(0.660000,-2.217025,2.557025,-1)$. Use the exact derivative and $c$ for calculations. Subtracting the tangent to $H$ gives

$$
L=(Y_1-Y_2) E_\nu[H(z)-H(z_*)-h'(z-z_*)]
\ \geq\ \frac{Y_1-Y_2}{8}\,E_\nu[(z-z_*)^2].
$$

Thus the ordinary exponent gives $L=0$. Conversely, $L=0$ and $Y_1>Y_2$ imply $q=1$ almost surely under $\nu$. This includes the entire survivor population if $b>0$ almost surely. The inequality also separates a single nonordinary exponent from mixtures giving the same signed midpoint residual in the three-phase panel. At ordinary response the two ratios above are approximately 1.763708 and 2.292820.

## What finite counts can resolve

Let $w=(1-h'-c,c,h',-1)$ and $\widehat L=\sum_nw_n\widehat Y_n$. For independent binary reports within each arm with a common rate there, conditional on the assigned sample sizes $N_n>0$, define $e_n=\sqrt{\log(8/\alpha)/(2N_n)}$. With probability at least $1-\alpha$, all four rates are within $e_n$ of their estimates. The ordinary equality $L=0$ is rejected in the positive direction if $\widehat L>\sum_n|w_n|e_n$. If $d=\widehat Y_1-\widehat Y_2-e_1-e_2>0$, the same event bounds $E_\nu[(z-z_*)^2]$ by $8(\widehat L+\sum_n|w_n|e_n)/d$ under the stipulated family. A negative upper bound is inconsistent with the model on that confidence event. Retained serial dependence needs its own uncertainty analysis. [Hoeffding's bounded-sum inequality](https://doi.org/10.1080/01621459.1963.10500830)

For any exponent range $B$ separated from one, put $\delta=\inf_{q\in B}|z(q)-z_*|>0$. The weighted fraction $\nu(B)$ is at most $E_\nu[(z-z_*)^2]/\delta^2$. Converting that into a fraction of original survivors requires a lower bound on $bD$ over $B$. For nearly blind detectors or powers approaching zero or infinity, $bD$ can be arbitrarily small. If half the shots have zero gain, replacing their exponents arbitrarily leaves all four rates unchanged. Opposite signs can likewise mask a nonordinary component: two equally likely reporters at the same $q\ne1$ with responses $g_q$ and $1-g_q$ add a constant offset to a responsive ordinary component. Each boundary case explains why pooled equality can constrain only the modes to which the detector is sensitive.

The earlier four-phase rail experiment compares opposite pairs on squares of coherent rail preparations. Its result for arbitrary bounded Borel responses uses many such squares, and sharp calibration sets the detector orientation. Here the four prepared phases belong to one survivor orbit and constrain mixtures in a specified family of binary scoring laws. An unrestricted response can agree at these four coordinates and differ elsewhere. [Four phase settings and the probability of a rail record](../../../Director_G/Four_phase_rail_probability.md)
