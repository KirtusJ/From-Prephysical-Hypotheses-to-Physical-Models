# A forward staircase test of spatial probability

**Kirtus Justus**, Theoretical Physicist, Port Coquitlam, British Columbia, Canada. Research supplement by Director G (OpenAI Codex).

Eight nine-tick programs compare the probability of seeing one position on a ring. Each uses the same source, the same Hadamard walk and one fixed staircase of signs that can be switched on or off. Two groups of four programs predict the same ordinary site frequency, $1/4$. A detector that samples sites in proportion to the **squares of the site weights** instead predicts $1/6$ and $1/3$. Their measured equality would select the ordinary exponent among all fixed positive powers. A fluctuating exponent can counterfeit this comparison at every site. One more site frequency separates that mixture as well.

## Controls and the eight preparations

On the eight-site ring the source is $(0,R)$. The normalized Hadamard coin maps $(r,l)$ to $(r+l,r-l)/\sqrt2$ and the walk sends R one well clockwise and L one well counterclockwise. Before departure, bit 0 leaves both rails alone and bit 1 multiplies both by $(-1)^{\lfloor x/2\rfloor}$ at site $x=0,\ldots,7$. Thus the only actuator switches the signs of wells $2,3,6,7$ **together**. The circuit applies no phase to an individually addressed source or output bin. A separate forward ring design controls those two phases and uses a cubic character. [Two-switch cubic comparison](https://github.com/KirtusJ/From-Prephysical-Hypotheses-to-Physical-Models/pull/89)

This profile is the order-two character of the program's staircase gain on the $4M$ ring at $M=2$. The permanent-gain walk supplies the profile. Its switching, a sharp reproducible source and a detector stable across switch words require physical control. An implementation with an unresolved internal sheet needs evidence that it prepares or realizes this signed sector. Xue et al. implemented position-dependent, polarization-independent phase shifts in a ten-step optical walk. Their apparatus provides a precedent for the control, while the eight-well periodic boundary and these eight switch programs would need their own test. [Staircase and signed sectors](Preparing_signed_sheet_residues.md) · [Position-dependent optical phase shifters](https://doi.org/10.1088/1367-2630/16/5/053009)

Choose three bits $a,b,c$ before launch and apply $0000\,a\,1\,b\,c\,c$ from left to right. Group by the parity of $a+b+c$. Use four equally weighted preparations per group. All arms take nine ordinary forward ticks. There is one terminal position read and every launch is counted. In an experiment with missing outputs, include a miss on the original denominator and establish the detector response before interpreting a frequency as an ideal site probability. The source and switch log must allow the two groups to be compared with the same position detector.

Let $w_x$ denote the sum of squared **kinematic coordinates** on the two rails at $x$, with $\sum w_x=1$. It is a number computed from the signed walk. The competing normalized-site-power laws predict
$$P_q(x\mid\psi)=w_x^q/\sum_yw_y^q,\qquad q>0.$$
Calling $w_x$ the observed frequency would already assume $q=1$. The competing law also permits ordinary conditional rail proportions inside a site, so an isolated rail test need not distinguish it. [Spatial bin law and reversible controls](Two_rail_comparison_for_a_flight_bin.md)

| $abc$ | parity | $(w_1,w_3,w_5,w_7)$ in quarters | $P_2(1)$ |
|---|---|---|---:|
| 000 | even | $(0,1,2,1)$ | 0 |
| 001 | odd  | $(1,2,1,0)$ | $1/6$ |
| 010 | odd  | $(1,0,1,2)$ | $1/6$ |
| 011 | even | $(0,1,2,1)$ | 0 |
| 100 | odd  | $(1,0,1,2)$ | $1/6$ |
| 101 | even | $(2,1,0,1)$ | $2/3$ |
| 110 | even | $(2,1,0,1)$ | $2/3$ |
| 111 | odd  | $(1,2,1,0)$ | $1/6$ |

The full real coordinate matrices agree. If $u_{abc}$ is the normalized column in the eight occupied site-rail modes, then
$$\tfrac14\sum_{\rm odd}u_{abc}u_{abc}^{T}=\tfrac14\sum_{\rm even}u_{abc}u_{abc}^{T}.$$
There are 64 entries including the inter-site coherences. The checker calculates each column twice, first by propagating the rails, then by enumerating all 512 complete direction histories. The independent Lean recurrence indexes a site by its rank inside the current spatial parity. It checks every entry and every named site numerator from the actual words. Equality of matrices is a kinematic prediction. Equality of measured frequencies for the named bin is the empirical comparison. A single passing bin establishes only that comparison. [Signed-history enumeration and projective orbit](check_forward_staircase_power.py) · [Exact matrix and output columns](results/forward_staircase_power.json) · [Lean 4.19.0 proof](lean/ForwardStaircasePower.lean) · [Operational equivalence of preparations](https://doi.org/10.1103/PhysRevA.71.052108)

At site 1 the odd and even group means are
$$A(q)=\frac1{2+2^q},\qquad B(q)=\frac{2^q}{2(2+2^q)}.$$
Every fixed $q>0$ gives $B/A=2^{q-1}$. Thus measured equality forces $q=1$ **within this family**. Every control setting uses one independently prepared launch. A classical mixture of words must therefore be scored by averaging their individual frequencies.

## A fluctuating exponent and all forward clocks

Let $q$ vary between launches independently of the chosen word. Give $q=\log_2(3/2)$ weight $7/10$ and $q=2$ weight $3/10$. Its mean odd rate is $(7/10)(2/7)+(3/10)(1/6)=1/4$. Its high-population-site rate is $1-2(1/4)=1/2$. The missing site is dark. Consequently every site probability of every nine-tick word agrees with the ordinary rule.

This law also passes **every equal-matrix site comparison at a single common clock** for this source, actuator and final position read, at arbitrarily long clocks. To verify the scope, propagate all projective integer columns. At each step divide by the gcd and identify an overall minus sign. The two successor rays depend only on the preceding ray. Exact equality of the reachable sets at clocks 7 and 19 therefore repeats them with period 12 from clock 7. The census gives the following complete set of site profiles, up to permutation and zero entries:

- Profiles uniform on their support occur at clocks 0, 1 and later in the cycle. All powers agree there.
- The profile proportional to $(1,1,2)$ occurs at clock 2 and later. The stated mixture gives exactly the ordinary weights there.
- At each remaining clock the profile is a permutation of $(1,1,1,5)/8$. Four sites can be occupied on that parity. On them even the response of an arbitrary stable mixture of exponents is affine in the individual $w_x$, because it takes only two values. The other parity has zero weight. Equal matrices at that clock have equal mean $w_x$ and hence equal mean site rates.

No new nine-tick word can resolve this particular ambiguity by adding more equal-matrix comparisons at the same clock. The census also gives a minimality result for fixed powers. At clocks 0 and 1 there is one profile at the named sites. At clock 2 both words give the same site distribution. At clocks 3 through 8 every fixed-power response is affine on the two available kinematic site weights on the occupied parity. Hence **clock 9 is the first** at which this class of same-clock equal-matrix comparisons, allowing arbitrary positive mixture weights and arbitrary site bins, can discriminate a fixed power. This statement is specific to the specified source and switch. [All reachable ray counts and site profiles](results/forward_staircase_power.json)

## One absolute site rate identifies a mixture

Keep the stable launch distribution of positive exponents. Also run three forward ticks with the staircase off. Read site $-3=5$, reached by a unique LLL path. Its site weight is $1/8$ and the other three occupied sites have weights $1/8,1/8,5/8$. Its probability for a given exponent is $y=(3+5^q)^{-1}$. An observed rate of $1/8$ would be a substantive calibration. Neither sharpness at launch nor uniqueness of the LLL history implies this frequency for the family being tested.

Write $t=2^q>1$, $k=\log_2 5$, $x=(2+t)^{-1}$. An equal nine-tick comparison means $E[x]=1/4$, since $B=1/2-x$. An early rate of $1/8$ means $E[y]=1/8$. For every $t\ge1$,
$$ y-\tfrac18 - \frac{5k}{8}\bigl(x-\tfrac14\bigr)\ge0, $$
with equality only at $t=2$. These two comparisons therefore force $q=1$ with probability one.

Here is the strictness argument. The slope of $y$ with respect to $x$ is $h(t)=kt^{k-1}(t+2)^2/(3+t^k)^2$, with $h(2)=5k/8$. Its derivative has the sign of
$$N(t)=3(k+1)t+6(k-1)-t^k[(k-1)t+2(k+1)].$$
Since $k>1$, $N'$ is strictly decreasing. Also $N(1)=6k-4>0$ and $N(2)=-8k<0$. Thus $h$ rises to one maximum between 1 and 2 and decreases thereafter. Since $x$ decreases, the displayed difference rises for $t>2$. On $[1,2]$ it takes its minimum at an endpoint because $h(1)=9k/16<h(2)$ and $h$ crosses the level $h(2)$ once before the maximum. The difference vanishes at 2 and equals $(12-5k)/96>0$ at 1, since $5^5<2^{12}$. This proves strictness throughout.

Finite data give an error bound. If $|E[B-A]|\le e_9$ and $|E[y]-1/8|\le e_3$, the expected nonnegative difference is at most $e_3+5k e_9/16$. Its minimum for $q$ outside any fixed neighborhood of 1 is strictly positive, including the limits at zero and infinity. Dividing by that minimum bounds the fraction of launches outside the neighborhood. This inference assumes the same distribution of exponents across the two clocks. A detector with other dependence on the word or clock still needs independent constraints. The result is a finite test of spatial readout on a ring. Transfer to a moving flight, a joint record or an unrestricted response requires further measurements.
