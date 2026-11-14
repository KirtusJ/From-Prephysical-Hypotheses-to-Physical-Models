# Certifying a position measurement by return to the launch well

**Kirtus Justus**, Theoretical Physicist, Port Coquitlam, British Columbia, Canada. Research supplement by Director G (OpenAI Codex).

The [three-tick dark-port test](Certifying_a_position_read_with_three_forward_ticks.md) uses a particular directed output that can differ from the launch well. One additional forward tick allows the interference experiments to use just **the original launch well, with both terminal rails summed**. This replaces both reversible propagation and rail resolution in the interference read. It uses the ordinary probability of a nonempty outcome. Independently checking sharp modes before these experiments still requires a rail-resolving instrument.

## What to measure

Use the same \(L\ge4\) reflecting Hadamard walk, single cut, fixed apparatus, and ordinary probabilities as in the [instrument certificate](Certifying_a_coherent_half_interval_read.md). Require exact correct-label and correct-mode probabilities on all \(2L\) sharp inputs. Thus \(W|i\rangle=|i\rangle e_i\) for unit tags in the correct classical outcome sectors. In each subsequent run prepare \((x,r)\) sharply and let the walk run forward for four ticks. Insert the unknown instrument once, after tick 3 or tick 2. Record its label and whether the walker returns to **site** \(x\) at tick 4. Keep all nonreturns in the original exposure.

Write \(\bar r\) for the other rail and \(S\) for one directed shift with wall holds and rail reversals. Thus \(S^2(x,r)\) follows the stored rail after the first shift, including a wall reversal. We use \(\operatorname{site}(i)\) for the well of a directed mode. Although the detector sums terminal rails, their two contributions add incoherently under the ordinary rule.

**First identify the two rails at every well.** Insert the instrument after tick 3. Set \((y,h)=S(x,r)\) and \(y'=\operatorname{site}(S(x,\bar r))\). In units of \(1/4\), the amplitude vector returning to site \(x\) on rail \(\bar r\), at label \(b(y)\), is
\[
  \pm(2e_{(y,h)}-e_{(y,\bar h)}).
\]
The amplitude on rail \(r\) has a single unit tag at well \(y'\) with coefficient of magnitude \(1/4\). Hence at label \(b(y)\) the joint site-return probability satisfies
\[
  16p_3 = 1+\mathbf 1_{\{b(y')=b(y)\}}
               +2\|e_{(y,h)}-e_{(y,\bar h)}\|^2 .
\]
Every well occurs as \(y\) for some launch because \(S\) is a permutation. Equality to the ideal value fixes the two tags at well \(y\) to one common \(e_y\).

**Then identify the sites within each bin.** Insert the instrument after tick 2. Let \(z=\operatorname{site}(S^2(x,r))\), \(z'=\operatorname{site}(S^2(x,\bar r))\). Given the verified rail equalities, the two terminal return vectors have coefficients \(\pm(2e_x-e_z)/4\) on \(\bar r\) and \(\pm e_{z'}/4\) on \(r\), before projecting on the classical label. If \(x,z\) are in the same bin, the joint site return at their label obeys
\[
  16p_2 = 1+\mathbf 1_{\{b(z')=b(x)\}}+2\|e_x-e_z\|^2 .
\]
All the returns being at their ideal values therefore gives \(e_x=e_z\) for every such pair. Interior pairs include all wells two apart. At \(x=0\) the outward launch gives \(z=1\); at \(x=L-1\) it gives \(z=L-2\). These end links join the even and odd site chains on their respective sides. A one-site bin has no further constraint. The calibrated dilation implements the coherent projection on both bins on every input. A probe split by the cut gives no comparison of its cross-bin tags; the two terms reside in distinct label sectors.

## Where the coefficients come from

Consider a four-step source return on the unfolded reflecting cycle of length \(2L\). At clock four only the lift of the source of its original parity is accessible. The signed [unfolding identity](Reflecting_wells_and_the_classical_limits_of_a_walk.md) relates the cycle and physical rails by a permutation, rail signs and a possible seam sign. For \(L\ge4\), a four-step source return has zero winding, since \(4<2L\). All six histories with two right and two left traveling steps arrive at the starting lift. Changing intermediate gauge multiplies each subpath to a mode by a phase and the subpath away by its inverse. The closed-path coefficients inherit only the common endpoint gauge sign. At tick \(k\) use the physical mode reached by that lifted path, including its reflected rail.

For example take first traveling rail \(R\), translate the source to 0 in lifted coordinates, and measure the amplitudes in units of \(1/4\). Group the six words according to their read port and final rail. The terms below include destructive cancellation. A pair \((a,r)\) is the mode at displacement \(a\) when the instrument acts. In the tick-2 row the two tags at site zero have already been equated by the tick-3 test.

| Intermediate grouping | Terminal rail \(R\) | Terminal rail \(L'\) |
|---|---|---|
| Tick 3, by mode | \(-e_{(-1,R)}\) | \(2e_{(+1,R)}-e_{(+1,L')}\) |
| Tick 2, by site | \(-e_{-2}\) | \(2e_0-e_{+2}\) |

For a left-rail launch reflected directions give the same magnitudes and relative minus sign. Explicitly the tick-3 opposite-rail vector is \(-2e_{(-1,L')}+e_{(-1,R)}\), and the tick-2 one is \(-2e_0+e_{-2}\). Folding the displaced lifts back gives \(S(x,r)\) and \(S^2(x,r)\), also when the first step holds at a wall. At reflected sites the traveling rails exchange their physical names. Squaring the vector with two tags uses \(\|2u-v\|^2=1+2\|u-v\|^2\) for all unit \(u,v\). The same-terminal-rail background is fixed even when its well lies in the target bin.

## A four-tick requirement for source-only experiments

In a sixteen-well walk cut between 7 and 8, attach a minus phase only to mode \((4,R)\) during the read. The phase changes the instrument on a balanced pair in the left bin. Nevertheless all source-site return tests using at most three total ticks pass from every sharp source, with one intermediate bin read, even if the final rail at the source is resolved. Through two ticks each path from a sharp source ends on a distinct mode. A three-tick source return needs a wall hold by parity. It cannot both visit well 4 and return to its launch well: the nearest wall is four edges from that marked well. Thus the phase cannot change any such source event. The probabilities of the labels alone are unchanged by a diagonal phase, so keeping the complementary site-miss outcome also preserves the full observed law at those clocks. A detector recording *which* nonreturn mode is occupied would admit the different [three-tick test](Certifying_a_position_read_with_three_forward_ticks.md). This finite example proves that four ticks are necessary in the worst case for the given source-only menu.

The [checker](check_forward_source_site.py) compares each tagged coefficient from all 16 direction words with a separately masked site recurrence for both launch rails, both terminal rails, and every well at lengths 4 through 32. It checks every contiguous cut, and the sixteen-well phase control at every intermediate clock. The [output](results/forward_source_site.json) gives the eight-well coefficients and all coverage sizes. A [Lean 4.19 calculation](lean/ForwardCut.lean) checks every intermediate coefficient for both final rails at eight wells, including the stored rail after a wall hold. These are exact model probabilities. A finite-precision implementation with imperfect rail equalities would have to propagate the first calibration error into the second test. The robust [directed dark-port protocol](Certifying_a_position_read_with_three_forward_ticks.md) avoids that intermediate approximation. Common detector readiness, calibrated forward dynamics and physical source and read errors remain experimental obligations.
