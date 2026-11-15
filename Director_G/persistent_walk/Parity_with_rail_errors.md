# Three-tick parity with imperfect arm isolation and rail labels

Kirtus Justus, research direction. OpenAI Codex, derivation and computational checks. 15 November 2026.

The two output rails and the lost launches suffice for a finite test when the unoccupied arm can leak limited information. With 90% true fringe visibility, a 5% limit on remote-bit distinguishability and a 5% rail-label error specification, the required cap depends on which error rate the instrument certifies. The same decision works in **41 or 42 preparations** under the two specifications below.

## Observable and experimental assumptions

Use the three-tick balanced walk starting at $(0,\mathrm R)$. Apply independent fresh fair sign bits $a,b$ to the first two arms, retain the origin after the second tick and read the two outgoing rails after the third. Score $D=+1$ for R on equal bits or L on unequal bits, $D=-1$ for the opposite rail, and $D=0$ for loss. The test consumes one preparation for each of these outcomes. Its only data inputs are the two bits and the terminal rail or loss. The earlier monitored design uses an additional traffic flag on each preparation. [Three-tick derivation and monitored design](Three_tick_phase_parity.md) · [Public walk convention](https://github.com/KirtusJ/From-Prephysical-Hypotheses-to-Physical-Models/blob/d6e025a6215185e8e4b51abee3f434c98485452b/Director_G/Four_arc_gains_and_winding_records.md)

Under the null the carrier commits to one arm before the current bits are drawn. Conditional on each past history, that commitment, the local bit and shared randomness independent of the settings, the remote bit remains fair. Require total variation at most $1/20$ between the two remote-bit laws of all additional information available to the port-and-loss decoder, including its recording electronics. For its signed remote-bit guess $f\in[-1,1]$, the two settings give $\lvert\mathbb{E} D\rvert=\lvert\int f\,d(K_0-K_1)\rvert/2\le1/20$ at each such conditioning. In particular $\mathbb{E}[D\mid\mathrm{past}]\le1/20$. Arbitrary memory and selective losses satisfying that inequality are covered. The apparatus must justify the leakage premise independently.

Under the alternative, assume on every launch conditional on its past that the hit rate is $1/2$, the true correct fraction among hits is at least $(1+g)/2$ with $g\ge0.90$, and relabelling preserves hits and losses. A label swap exchanges the two output rails. Two common ways to specify its probability give different guarantees.

| Rail-label specification, conditional on each past history | Reported correct fraction among hits, at least | Sufficient cap | Null size, at most | Target power, at least |
|---|---:|---:|---:|---:|
| Swap probability at most 5% given a hit, its true rail and the current settings | $0.95(0.95)=0.9025$ | 41 | 0.049900 | 0.951950 |
| Swap probability at most 5% among all hits | $0.95-0.05=0.90$ | 42 | 0.049886 | 0.953241 |

For the first row, at least 95% of the true correct readings keep their labels. For the second, swaps can be concentrated on previously correct readings. The second row permits the reported probabilities $(.45,.05,.50)$ per preparation for correct, wrong and loss. Independent draws with that law give only **0.948391058** power for the 41-launch version of this rule. An explicit realization takes true correct fraction .95 among hits and swaps labels only on a fraction $1/19$ of the correct hits. Both specifications require error control conditional on the preceding record. A device-wide average that allows long bad runs is a different assumption.

## The decision rule

Start $W=1$. Multiply by $59/40$ for a correct port, $19/40$ for a wrong port, and $39/40$ for a loss. Reject as soon as $W\ge20$. If the cap arrives first, draw one independent uniform ten-bit integer $U$ from 0 through 1023. Reject if $U<\lfloor1024W/20\rfloor$.

The multiplier is $1+(D-1/20)/2$. Its conditional null mean is at most one, so the product stopped on first reaching 20 or at the cap has expectation at most one. The conditional decision probability at each stopped record is bounded by $W/20$. This proves a 5% false-rejection bound at either cap.

The sharper null figures in the table follow from a finite recursion. Write $(p,q)$ for the conditional correct and wrong probabilities. The feasible polygon has $p,q\ge0$, $p+q\le1$, $p-q\le1/20$. Its four vertices are $(0,0),(0,1),(1/20,0),(21/40,19/40)$. Work backward from the terminal ten-bit decision at every live count of correct, wrong and lost outcomes. At a threshold crossing assign rejection value one. At every other earlier state take the largest of $pV_+ + qV_- + (1-p-q)V_0$ at those four vertices. This gives the maximum over the conditional-mean class, including adaptive null responses.

For target power, replace that maximum by the average with the least favorable target probabilities. They are $(361,39,400)/800$ in the first row and $(9,1,10)/20$ in the second. To see this even for history-dependent targets, couple the half-hit indicators to fresh fair draws. On hits use a second independent uniform draw to generate the reported label at its conditional success probability and the benchmark label at its fixed lower bound. The first sequence then dominates the benchmark pathwise in the order wrong, loss, correct. Increasing any score can only move the product upward, cause an earlier crossing, or increase its terminal rejection probability. This proves the reported power bounds. Both cap figures are sufficient designs. Optimality under these noise specifications remains open.

The standard-library checker performs the full backward recursion with integer numerators, including early crossings and the ten-bit endpoint. [Companion program](check_parity_with_rail_errors.py)

~~~sh
python -I -B -O check_parity_with_rail_errors.py
~~~
