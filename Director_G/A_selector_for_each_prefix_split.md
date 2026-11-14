# A selector for each split of a walk reference

**Kirtus Justus**, Theoretical Physicist, Port Coquitlam, British Columbia, Canada. Research supplement by Director G (OpenAI Codex).

A four-digit reference can be prepared with a marked squared mass of $9/16$. Its observed detector rate can be tested at each digit. At each digit the walk splits one occupied mode against a blank. Two settings include either both children or neither. Two more include one child apiece. A fresh coherent selector and one controlled flip give a physical comparison of these choices on the same pointer. Measuring a midpoint relation at each split suffices for any specified finite threshold. The proposed experiments have no reported data. The earlier reference compares a random-phase preparation with a mixture of all sharp stopping histories. [Preceding construction at its issued revision](https://github.com/KirtusJ/From-Prephysical-Hypotheses-to-Physical-Models/blob/b4dc33e7028b7f9f8f9869a792826088f4bb9e6a/Director_G/A_compact_reference_for_a_written_position.md)

## A single split and one passive flip

Let $O$ collect the previously marked, parked modes, and $N$ the previously unmarked modes. The live prefix splits into children $A,C$ by a Hadamard on an occupied first input and a blank second input. The two outgoing amplitude vectors are equal, including their phases and any spectator. Each trial uses one complete binary pointer $F$. The following four predicates specify which modes write 1.

| Selector value | Endpoint predicate $E_l$ | One-child predicate $D_l$ |
|---|---|---|
| 0 | $O$ | $O\cup C$ |
| 1 | $O\cup A\cup C$ | $O\cup A$ |

Prepare a separate ordered selector $L=(|0\rangle+|1\rangle)/\sqrt2$. In the coherent $E$ program both active children write $F=L$. In the coherent $D$ program they write $F=L\mathbin{\mathrm{XOR}}1_C$. Parked modes write their fixed mark in both programs. After completing the $E$ write, flip $L$ only on $C$, leaving the pointer and spatial mode untouched. For every output address $x,l,f$, the incoming selector coefficient on this path is the coefficient of $l\mathbin{\mathrm{XOR}}1_C(x)$, which equals that of $l$. The required flag is consequently the one in the $D$ program. This proves equality of the **complete** outgoing columns with inert spectators, as long as no extra record distinguishes the selector alternatives. The controlled flip does not even require the two child amplitudes to be equal. Separately, their equality does make exchanging $A,C$ after a standalone $D_0$ write give precisely the standalone $D_1$ column. Both exchanges leave $F$ untouched. This is a finite instance of the idea of compensating an operation on a correlated register by acting on its partner. [Zurek on environmental exchanges](https://arxiv.org/abs/quant-ph/0405161)

The gates require fresh selector preparation, coherent control on $C$, an addressed child exchange, and clock-matched clean paths. A controlled flip itself is an involution. Geometrically distant wires still need time to reach the gate. These are additional controls on the signed walk. A selector with a random sign has fair marginal squared amplitudes but its two coefficients may differ. One residual sign can break the comparison on a superposition with both $C$ and other modes occupied.

If the raw selector was copied earlier to an inaccessible orthogonal tag, after the flip the tag still records $l\mathbin{\mathrm{XOR}}1_C(x)$, while in the target it records $l$. On $C$ the two columns have orthogonal tag support. Their squared distance is exactly $2w_C$, where $w_C$ is the original normalized squared mass of $C$. Even a single occupied $C$ already gives a counterexample to the bare complete-column identity with a retained tag. Entangling the selector with a real classical setting in advance can therefore change this experiment.

## What must agree in the detector

Write $a,b$ for the original-launch rates on the standalone endpoint predicates $E_0,E_1$, and $u,v$ for those on $D_0,D_1$. Independent, fair *classical assignment* between either pair has rates $(a+b)/2$ and $(u+v)/2$. That is an identity of assignment frequencies. Let $R_E,R_D$ denote the rates in the two coherent programs. On the representative incident population, test or bound

$$
 |R_E-(a+b)/2|\le e_E,\qquad |R_D-(u+v)/2|\le e_D,
 \qquad |R_E-R_D|\le e_X,\qquad |u-v|\le e_S.
$$

The first two comparisons tie an unread selector to the chosen branches on the actual device. They can be made by interleaved coherent and classically assigned trials. Another route is evidence that reading the selector leaves the $F$ marginal unchanged, gives equal branch frequencies, and reproduces the respective standalone conditional pointer rates. Such evidence belongs to **each** coherent program. Marginal fairness of $L$ alone says nothing about the conditional $F$ responses. Branch-dependent selection, inaccessible meters or controller tags require their own checks. For the third comparison the passive flip motivates separate tests of pointer isolation during the flip and equivalence to the matched $D$ preparation. The child swap motivates the fourth. Equal kinematic columns do not themselves establish either measured equality. If the four standalone rates are measured, the midpoint and child contrasts can of course be computed directly.

Either one-child rate then differs from $(a+b)/2$ by at most $e_E+e_X+e_D+e_S/2$. This follows from the triangle inequality on the two branch means and the half-difference of the one-child rates. No shared scalar response function is assumed across the four predicates. Keep all incident assignments, misses and unread outputs. Missing binary completions can be bounded by their incident fraction. Simultaneous uncertainty intervals must account for any reused trials or drift.

## Following one requested threshold

Use the fixed binary digits $b_1\ldots b_t$ of $P/2^t<1$. At each split $A$ is parked and $C$ continues. When $b_k=0$ the retained endpoints are $E_0,D_0$. When $b_k=1$ they are $D_1,E_1$. This follows from marking the first unequal digit only when the comparison address is smaller. Equality at depth $t$ remains unmarked. After $t$ steps the lower endpoint is the requested predicate. At a new clock the parent endpoints must transfer to the new $E_0,E_1$ reads. Writing an earlier protected $F$ and preserving it across the next splitter gives a physical probe of this transfer. Equating the actual earlier read with the later written pointer needs the matched preparations and observed marginals. Idle padding and any terminal parity split used to put the numerator in a specified scale also require pointer preservation. No trial must expose a sequence of recorded splitter decisions.

With sharp start rates $0,1$, exact transfers and exact midpoint tests give $P/2^t$ by binary bisection. There is a threshold-specific finite-error bound. At step $k$, let $\Delta_k$ be the signed error of the selected one-child rate about the current midpoint, and $h^-_k,h^+_k$ the signed discrepancies in carrying the two selected endpoints to their next realizations (or the terminal read). Let $z_k=0.b_{k+1}\ldots b_t$, with the empty suffix zero, and $p=P/2^t$. Then

$$
 r-p=(1-p)\delta_0+p\delta_1+
 \sum_{k=1}^t\left[c_k\Delta_k+(1-z_k)h^-_k+z_k h^+_k\right],
 \quad c_k=\begin{cases}z_k&b_k=0,\\1-z_k&b_k=1.\end{cases}
$$

Here the initial endpoint errors $\delta_0,\delta_1$ include deviations of the first split's endpoint reads from 0 and 1. To verify the identity, interpolate the final target at fraction $z_k$ inside the chosen subinterval. In a zero step the midpoint is its upper endpoint; in a one step it is its lower endpoint. Substituting the interpolation at each step gives the indicated coefficients. All weights are nonnegative, so simultaneous absolute error limits may be substituted directly. At $1001_2$ the midpoint-error coefficients are $7/8,1/4,1/2,1$. The number of different local comparisons grows linearly in the digit count. Their exposure and the cost of routing the signed carrier are separate resources.

Consider the binary law $g(s)=s^2/[s^2+(1-s)^2]$ on a pooled squared mass $s$. It is complementary, faithful at both endpoints and fair at every isolated balanced split. A swap of equal children cannot distinguish it. At the second digit of $1001_2$, the endpoint masses are $1/2,1$ and each one-child mass is $3/4$. Its one-child rate $9/10$ exceeds the endpoint mean $3/4$ by $3/20$ per incident launch. Both coherent programs have the same binary mass there, so their coherent comparison passes. The discrepancy appears when the coherent endpoint selector is compared with its standalone branch mixture. At the final threshold this rival gives $81/130$, a discrepancy of $63/1040$ from $9/16$.

This calibrates the specified compact reference under the supplied operations and measured bounds. To use it for the actual flight bin still requires the protected-state conversion and transfer between the flight and reference writes. [Flight transfer and its premises](A_compact_reference_for_a_written_position.md) · [Exact checker](check_midpoint_selector.py) · [Inputs and results](results/midpoint_selector.json)
