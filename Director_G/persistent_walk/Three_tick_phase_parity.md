# Reading the parity of two local phases in three ticks

Kirtus Justus, research direction. OpenAI Codex, derivation and computational checks. 15 November 2026.

A three-tick Hadamard walk has a terminal port for equal arm bits and another for unequal bits. Half the original launches reach these ports. With ideal independent launches, the complete record distinguishes the walk from a carrier restricted to one arm and its local bit with at most 5% error in each direction after **13 launches**. A second design allows bounded unobserved traffic and erroneous readings. It uses **17 launches** and a same-launch monitor. Both numbers are prospective design guarantees.

## Preparation and readout

Start at site 0 on rail R. Each tick maps the incoming amplitudes $(r,l)$ to $(r+l,r-l)/\sqrt2$, then shifts R one site right and L one left. The apparatus may use the line or any ring with at least three sites. After tick one, apply $x=(-1)^a$ at $+1$ and $y=(-1)^b$ at $-1$. The local bits $a,b$ are independent, fair and fresh. After tick two, keep both rails at site 0 and absorb everything else. After tick three, read $R=(+1,\mathrm R)$ and $L=(-1,\mathrm L)$. Record both settings and one of R, L and loss on every preparation. This uses the sharp source, whole-site mask and terminal-rail convention of the public walk construction. Local phase encoding at two positions and reading the parity by interference also occurs in the single-particle communication protocol of Del Santo and Dakić. [Walk convention](https://github.com/KirtusJ/From-Prephysical-Hypotheses-to-Physical-Models/blob/d6e025a6215185e8e4b51abee3f434c98485452b/Director_G/Four_arc_gains_and_winding_records.md) · [Del Santo and Dakić, Phys. Rev. Lett. 120, 060503](https://doi.org/10.1103/PhysRevLett.120.060503)

At site 0 the surviving rail amplitudes after tick two are $(y,x)/2$. The terminal amplitudes are $(x+y,y-x)/\sqrt8$. Equal bits give R with probability $1/2$, unequal bits give L with probability $1/2$, and the remaining probability is loss for every setting. If the two arms carry unit markers with real inner-product part $g$, the probabilities per preparation are

| Correct port | Wrong port | Loss |
|---:|---:|---:|
| $(1+g)/4$ | $(1-g)/4$ | $1/2$ |

This marker formula assumes balanced amplitudes, the same recombiner, and a detector insensitive to the marker. The ideal 13-launch calculation sets $g=1$.

## What the exclusive-arm model can predict

In the comparison model a carrier commits to one arm before the two current bits are drawn. The local history $H$ includes the committed arm, its bit, shared randomness independent of the new settings, and any earlier trials. The other bit $Y$ is fair given $H$. Conditional on $H$, let $K_y$ be the distribution of all additional information available to the port-and-loss decision given $Y=y$. This includes any information that could change whether a carrier registers. Score $D=+1$ for the correct port, $-1$ for the wrong port and 0 for loss.

Knowing the local bit, a port declaration is a guess for $Y$. Write $f$ for the decoder's mean signed guess, giving a declared 0 weight $+1$, a declared 1 weight $-1$ and loss weight 0. Then $|f|\le1$ and

$$
\left|\mathbb{E}[D\mid H]\right|
=\tfrac12\left|\int f\,d(K_0-K_1)\right|
\le \operatorname{TV}(K_0,K_1).
$$

Thus equal remote-bit laws imply conditional mean zero, including setting-dependent loss permitted by local information. A device that can read both bits can route a correct answer on half the trials and duplicate the complete ideal record. A coherent classical field can also realize the stated amplitudes. The witness constrains remote-bit information available after commitment. An apparatus applying the comparison requires independent justification for its timing and information restrictions.

## A sharp cap with ideal isolation

Start $W=1$. Multiply it by two on each correct port, set it to zero on any wrong port and leave it alone on a loss. After the predetermined cap, reject the comparison model with probability $\min(1,W/20)$ using randomness independent of the data. The conditional null bound $\mathbb{E}[D\mid{\rm past}]\le0$ implies $\mathbb{E}[W_{\rm end}]\le1$, since each factor is $1+D$. The false-rejection probability is at most $1/20$.

Under the ideal independent target, the number $h$ of recorded ports is binomial with parameters $(n,1/2)$, and all are correct. The power is $\mathbb E\min(1,2^h/20)$. To bound every decision on the recorded bits and terminal outcomes, fix a schedule of $h$ hits at arbitrary specified launches. A valid null realizes that schedule and outputs a fresh independent fair port on each hit. With probability $2^{-h}$ all guesses are correct. Conditional on this event the entire transcript has the ideal distribution conditional on that schedule, including both local bits at every launch. A level-$1/20$ rule's conditional ideal rejection probability is therefore at most $\min(1,2^h/20)$. Average over the ideal schedules. A decision that stops early is also a decision on a full record that ignores the unused suffix.

| Launch cap | Maximum ideal rejection probability at level 5% |
|---:|---:|
| 12 | $76009/81920 = 0.92784423828125$ |
| 13 | $156047/163840 = 0.952435302734375$ |

The cap is sharp for this observation record and a null that permits arbitrarily scheduled losses. Under a run-wide shutter that opens for all launches with probability $1/2$ and otherwise closes for all of them, every single-launch marginal has the ideal port law. The 13-launch rule then has power $(1+1/20)/2=0.525$. Independent survival in the target matters.

## A 17-launch test with same-launch monitoring

Designate a physical quiet state of the receiver input. Define its baseline port by holding the decoder's local inputs and random seed fixed and feeding it quiet. Let $B$ be the resulting signed parity score. Under the exclusive-arm null, the baseline decoder has no information about $Y$ and $\mathbb E[B\mid{\rm past}]=0$. An actually quiet receiver must give that baseline output. A same-launch monitor flags suspected nonquiet inputs. On **every** flagged launch assign the final score $S=-1$, including losses. On unflagged launches use $S=D$. Pathwise,

$$
 S\le B+2\,\mathbf 1\{\text{input nonquiet and monitor silent}\}.
$$

The coefficient two allows a wrong baseline answer to become a correct port. If the probability of this missed traffic is at most 1% **conditional on each past history**, the null obeys $\mathbb{E}[S\mid{\rm past}]\le0.02$. The monitor model assumes access to every receiver input through which the remote bit can change the decision. Its missed-traffic specification is an instrument premise.

Set a cap of 17 preparations. Reject if five positive scores arrive before the first negative, by the cap. A zero consumes a launch. Writing $p,q$ for the conditional probabilities of positive and negative, the greatest null crossing probability $V_t(k)$ with $t$ launches remaining and $k$ positives needed obeys

$$
V_t(k)=\max_{p,q}\big[pV_{t-1}(k-1)+(1-p-q)V_{t-1}(k)\big].
$$

Use $V_t(0)=1$, $V_0(k)=0$ for $k>0$. The null polygon $p-q\le0.02$ in the probability simplex has vertices $(0,0),(0,1),(.02,0),(.51,.49)$. For the alternative require $p\ge.498$ and $q\le.002$ conditional on each history. Minimize at its vertices $(.498,0),(.498,.002),(.998,.002),(1,0)$. Affinity makes these two recursions valid for adaptive responses. Exact rational results give null size at most **0.043756845304** and target power greater than **0.956124997057**. Sufficient target premises are half the launches reaching a port, incorrect ports on at most .001 of all launches and alarms on at most .001 of all launches, each conditional on the past.

A pooled monitor calibration can give a different answer. Choose a run-wide leak mode with probability .02. In that mode a decoder always hits, defaults to remote bit 0 and receives an unflagged correction exactly when the remote bit is 1. The decoder is always correct. Outside that mode an independent fair guess always hits and no traffic occurs. At every fixed launch the unconditional missed-traffic probability is .01. The crossing rule nevertheless rejects with probability $.02+.98/32=81/1600=0.050625$. Reporting average errors alone therefore fails to justify the 17-launch size bound.

Run the exact standard-library checker from this directory with the command below. It propagates integer walk amplitudes, computes both finite decisions, and checks the monitored bound and clustered examples. [Companion program](check_three_tick_phase_parity.py)

~~~sh
python -I -B -O check_three_tick_phase_parity.py
~~~

A separate design uses only rail labels and loss with imperfect arm isolation. Its sufficient cap is 41 or 42 launches, depending on the rail-label calibration. [Test with imperfect rail labels](Parity_with_rail_errors.md)
