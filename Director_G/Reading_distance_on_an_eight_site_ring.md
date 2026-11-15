# Reading distance on an eight-site ring

Six free Hadamard steps on an eight-site ring put fractions \(1/8,2/8,5/8\) of the kinematic mass at graph distances \(0,2,4\) from the source. The fractions hold for every rail state localized at the launch site. A detector that physically writes one of these three distances can test the ordinary probability exponent on a single clock, even when the exponent changes on every launch. A detector that first writes a precise site admits a rival that gives exactly the ordinary records at **every** flight duration under an allowed rail reset. Both claims concern proposed measurements.

## One distance write

Launch at a known site. At every tick apply the real Hadamard to the two rails, then shift the outgoing R and L amplitudes by one site clockwise and counterclockwise. After six ticks a position pointer reports the graph distance from the launch well. The two wells at distance two feed one physical output. The kinematic mass in this output sums both wells and their rails before the instrument applies its probability law. No intermediate site write, rail measurement, controllable coin or independent selector occurs. A hidden site or rail detector upstream of the distance pointer changes this assumption.

Let \(J=\left(\begin{smallmatrix}0&-1\\1&0\end{smallmatrix}\right)\). The table gives the site-transfer matrix multiplied by four, its scalar squared mass, and the number of microscopic direction words when every path has equal positive weight. The two clocks have the same four site effects. The path counts use the full launch denominator at each clock. [Derivation of the two flight matrices](Restoring_a_rail_with_position_records.md)

| Displacement mod 8 | \(4K_6\) | \(4K_{18}\) | Kinematic mass | Fair paths at 6, of 64 | Fair paths at 18, of 262144 |
|---|---|---|---:|---:|---:|
| 0 | \(-(I+J)\) | \(-(I-J)\) | 1/8 | 20 | 65792 |
| 2 | \(I+J\) | \(I-J\) | 1/8 | 16 | 65536 |
| 4 | \(3I-J\) | \(3I+J\) | 5/8 | 12 | 65280 |
| 6 | \(I+J\) | \(I-J\) | 1/8 | 16 | 65536 |

Each \(K_d^\dagger K_d\) equals its listed mass times identity, including on a rail correlated with an idle spectator. Thus even a hidden power correlated with the rail encounters the same three distance masses. Assume that a conditional reader scores the three physically written bins with one common power \(q\) on their squared masses and normalizes on their support. Use the original launch ensemble. Put \(\theta=\log 2/\log 5\) and record the per-launch score whose population mean is

\[
 S=(1-\theta)P_0-\tfrac12 P_2+\tfrac{\theta}{5}P_4 ,
\]

where subscripts here label **distance**. For every finite real power,

\[
 S(q)=\frac{(1-\theta)+\theta5^{q-1}-2^{q-1}}{1+2^q+5^q}\ge0 .
\]

The weighted arithmetic–geometric mean inequality gives equality exactly at \(q=1\). The maximum and minimum selectors score \(\theta/5\) and \(1-\theta\), respectively. A zero **population** mean therefore selects the ordinary power almost surely. For \(h>0\), the fraction with \(|q-1|\ge h\) is at most \(E[S]/v_h\), where

\[
 v_h=\tfrac18\min\{(1-\theta)5^{-h}+\theta-(2/5)^h,\quad
 1-\theta+\theta5^{-h}-2^{-h}\}>0 .
\]

For \(t=q-1\), the denominator is at most \(8\max(1,5^t)\). Dividing the numerator by this upper bound gives two functions increasing with distance from one, as follows by differentiation using \(\theta\log5=\log2\). An incident fraction \(\ell\) of missing distances widens a mean computed with zero assigned to misses by \([-\ell/2,(1-\theta)\ell]\), before sampling uncertainty.

**A control for full path counting.** At six ticks fair counting gives \((5/16,1/2,3/16)\) in increasing distance order and scores \((5-22\theta)/80<0\). In fact the ordinary three-bin distribution is reproduced exactly by mixing uniform-bin scoring, square-power scoring and fair counting with probabilities \((1,35,16)/52\). The same radial experiment at eighteen ticks separates this rival under matching of the type populations across the two clocks. Every powered type keeps the same antipodal rate while fair counting changes from \(3/16\) to \(255/1024\). The eighteen-minus-six antipodal difference is exactly \(63/1024\) times the counting fraction. Equality of those rates excludes counting, after which the six-tick score applies to the powers. This second comparison requires comparable incident populations and losses at the two durations.

## What a full site write can hide

Suppose the detector physically scores each whole well, writes its address, and the analyst computes distance later. At six ticks the four raw masses are \((1,1,5,1)/8\) in displacement order \(0,2,4,6\). At power two the three derived distance rates are \((1,2,25)/28\); a direct distance write gives \((1,4,25)/30\). At ordinary power these operations agree on all distance frequencies.

**A second read tests which-way information.** Write distance at six ticks, take four more free steps, and read distance from the **original** well again. If the first write preserves coherence between the two sites of radius two, their equal rail amplitudes cancel exactly at both of those sites at tick ten. Indeed \(K_6(2)=K_6(6)\), whereas \(K_4(0)=-K_4(4)\). The joint probability of two radius-two reports is zero for every localized incoming rail. If the first detector records the exact site, an arbitrary normalized rail left at that site encounters the two scalar effects \(I/8\) at four-tick displacements zero and four. Under ordinary scoring the joint probability is then \((1/4)(1/4)=1/16\). In increasing order of the final radius, the entire joint row with the first radius fixed at two is \((1/8,0,1/8)\) for the coherent write and \((3/32,1/16,3/32)\) for a rail-preserving exact-site write. With otherwise ideal routing and two normalized path marks of overlap \(\gamma\), the middle entry is \((1-\operatorname{Re}\gamma)/16\). An untracked relative phase changes the same contrast. This control diagnoses coherence left by the first read. Transferring a result to a probability law still requires the stipulated scoring cells. [Four-tick transfer matrices](A_rail_measurement_from_four_free_steps.md)

For all real powers there is an exact obstruction to distinguishing ordinary and powered whole-site writes using just the flight times, from an initial sharp R or L rail and without assumptions on the rail reset. An admissible writer in each of the two models prepares R at the reported site after every write. An unknown classical choice of sharp launch rails also works here. For the rival draw a fresh power at every write,

\[
 \Pr(q=-2,0,2)=(57,7,140)/204 .
\]

Use only occupied sites for a negative power and keep structural zeros dark. The sharp-rail site histograms over one period, up to site permutation, are as follows.

| Flight duration modulo 24 | Positive masses up to order |
|---|---|
| 2, 9, 14, 21 | \((2,1,1)/4\) |
| 3–8, 15–20 | \((5,1,1,1)/8\) |
| 0, 1, 10, 11, 12, 13, 22, 23 | Uniform on the occupied sites |

Both columns of the free walk return to their starting rail and site at tick 24. Translation extends the period to the full walk. For the first nonuniform row the probability of its unique largest site is \(A(q)=2^q/(2+2^q)\); for the second it is \(B(q)=5^q/(3+5^q)\). The displayed mixture gives \(E A=1/2\) and \(E B=5/8\). The other occupied sites share the remaining probability equally. Thus the two reset instruments agree on **every conditional next-address distribution**, and induction gives identical full site transcripts even when the next duration is chosen from the past. Independence of each fresh power from the prefix ensures those weights survive conditioning. This is an existence result for the allowed updates. A separately certified coherent rail update or a different preparation can add information. At direct distance resolution this very mixture predicts \((2201,1378,5193)/8772\), visibly different from \((1,2,5)/8\).

## Two complete site writes with nonnegative powers

There is still a test using complete sites if powers are nonnegative and the first source is sharp R or L. Write the site after two ticks, then write it again after six further free ticks. Let \(a\) be the first return rate and \(b\) the rate of an antipode **relative to the first reported site**. Allow the first write to leave any rail state localized there. The first clock gives \(A(q)\) and the second gives \(B(q)\) above. The powers at the two writes may be refreshed or correlated with past records. Their *unconditional marginal laws on all original launches* must agree. The unknown rail left by the first write can vary with both powers. For a mixed source the first formula also holds if its kinematic rail density conditional on the first type satisfies \(\operatorname{tr}(X\rho)=0\). A density obtained only after averaging type-correlated X eigenstates does not justify this use of \(A\).

Put \(k=15\log5/(16\log2)\). The contrast \(5/8+k(a-1/2)-b\) is zero only at ordinary power almost surely in this class. For one common argument \(q\), the integrand vanishes at one along with its derivative. Multiplying by \(8(2+2^q)(3+5^q)\) gives

\[
 (4k-3)10^q-(6+8k)5^q+(15+12k)2^q+30-24k .
\]

A nonzero combination of four distinct real exponentials has at most three real zeros counted with multiplicity. Divide by the first exponential, differentiate, and induct by Rolle's theorem. Here the expression is negative at sufficiently negative \(q\), and positive at zero since \(k<9/4\) by \(5^5<2^{12}\). The double zero at one therefore exhausts the other possible zeros. The contrast is positive everywhere else on \([0,\infty)\), including the limiting value \(k/2-3/8\). Averaging only uses the equality of the two marginal laws. Fair counting in both blocks contributes \(7/16\) to this contrast. A global power on complete transcripts with the ideal position write also gives the same \(A,B\), since the two ordinary displacement masses factorize.

Two exact false passes locate the assumptions. First, choose powers zero and two independently at the two writes but use probabilities \(1/2\) and \(7/12\), respectively, of power two. This changes the marginal law and reproduces the entire ordinary two-address distribution. Second, let a reader resolve both rails at each well, select a rail cell and continue from that sharp rail. The first four cells have equal mass. The six-tick antipode then has rate \((9^q+1)/(9^q+7)\). One *persistent* exponent equal to two with probability \(11/20\) and zero otherwise again reproduces every ordinary two-address probability. A fit to the two clocks therefore depends on what actually gets written.

These tables use the signed Hadamard transport and calibrated geometry, localization and detector grouping. They supply probability references for records on this carrier. The microscopic source of those primitives and their correspondence to measured trajectories remain open. [Exact replay](check_ring_distance.py) · [Full clock and control tables](results/ring_distance.json) · [Sixteen-site scalar position instrument using a programmed coin](../candidates/composition_record/velocity_experiment/ordinary_powers_with_a_retained_qubit.md) · [Repeated-word comparison](Two_five_tick_records_and_the_probability_power.md)

Kirtus Justus, Theoretical Physicist, Port Coquitlam, British Columbia, Canada, holds scholarly responsibility. OpenAI Codex derived and checked the comparisons.
