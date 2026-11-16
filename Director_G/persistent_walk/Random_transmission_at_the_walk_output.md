# A five-site return test that survives suppression of coincident clicks

Kirtus Justus, research direction. OpenAI ChatGPT (Director G), mathematical design and checks. 15 November 2026, B.C. Pacific Time (PCT, UTC−07:00).

A counter that retains only the first detector hit in a gate can make a classical pulse appear to occupy exactly one output bank. It still distinguishes an empty gate from an occupied gate if it preserves the first hit. Randomizing the transmission immediately before detection makes that distinction informative. In the design below, 158 prepared walks give calculated joint power above 0.95054 under the stated single-excitation model. Both count tests use the same preparations and include every empty gate. [Split-bank readout and its failure case](Split_readout_at_the_walk_output.md)

## Records and physical assumptions

Use the five-site walk and three-cosine stopping-time sampler of the long single-port experiment. After the light incident on the attenuator is fixed, choose full transmission with probability $\pi=78/125$ independently on every trial. On the other trials use an attenuator with relative **intensity** transmission between 0.49 and 0.51 across the admitted modes. The choice can also be made earlier if it is isolated from the source and evolution. Record the setting, the stopping-time sign, whether any rail clicked, and whether the launch rail clicked. Retain the preparation count even if the whole gate is empty. [Timing sampler and stochastic bound](Longer_single_port_timing.md)

An attenuation success is either a full-transmission trial with a click anywhere or an attenuated trial with no click anywhere. An electronic lock that suppresses later hits during the gate leaves this score intact if each nonempty gate still records a hit. Full-transmission launch-rail labels supply the existing timing test. Its null assumes a fixed terminal response for independent preparations; a fixed first-hit rule can be included in that response. Under the ideal alternative each preparation contains one excitation, so there are no competing simultaneous signal hits. The power calculation assumes no background, a fresh reset, and uniform full-setting detection efficiency 0.98 across all durations and rails.

## A bound for an arbitrary mixture of classical intensities

Conditional on the field and past records, suppose the total detected photoelectron number is Poisson before first-hit processing. The field may fluctuate arbitrarily between gates. Let $x=e^{-\lambda}$ be the full-setting probability of an empty gate. If the effective relative transmission is $g$, the attenuated empty probability is $x^g$. An independent, unchanged Poisson background only decreases the latter relative to this upper bound when its contribution has already been counted in the full rate. The bound requires the transmission and empty-gate model throughout the admitted optical inputs, together with isolation of the setting.

The attenuation-success probability is at most $f(x)=\pi(1-x)+(1-\pi)x^{0.49}$. The exponent 0.49 gives the largest value in the permitted transmission range. For $g=0.49$ this concave function has its maximum at $x=[(1-\pi)g/\pi]^{1/(1-g)}$. Its maximum lies between 0.683392807 and 0.683392808. The checker proves that bracket by integer powers. A fixed classical intensity at the indicated extremum and a transmission of 0.49 attain the analytic maximum. Since the bound applies conditional on history, the upper tail of the observed count is bounded by a binomial tail even if the intensities are chosen adaptively.

Kovtoniuk, Bohmann and Semenov derived nonclassicality tests using a single on-off detector with switchable efficiency. The calculation here uses that established measurement principle and derives a finite decision for this five-site timing experiment, including an interval for the transmission. The published study supplies methodological grounding. The actual transmission, first-hit behavior and timing isolation in the proposed apparatus require measurement. [Physical Review A 113, 063726 (2026)](https://doi.org/10.1103/pknl-24xd)

## Both decisions must pass

Let $M$ denote the number of full-transmission trials. At those trials score launch-rail clicks or misses according to the original timing sign. Use the smallest integer $k(M)$ for which $\Pr[\mathrm{Bin}(M,0.557844796873)\ge k(M)]\le0.05$. If the sample is too small even for all successes, set $k(M)=M+1$. The random subset is independent of the timing sampler. Conditional on the setting sequence, the original finite-state bound controls the full-setting count. The complete cutoff table is in the recorded output.

| Prepared walks | Attenuation count needed | Field false rejection at most | Stochastic timing false rejection at most | Joint ideal power at least |
|---:|---:|---:|---:|---:|
| 158 | 118 | 0.049590043 | 0.039523787 | 0.950541513 |
| 180 | 135 | 0.037669611 | 0.042009671 | 0.954791147 |

The 180-launch row permits a specific additional fault under the field rival. Before drawing the transmission on each trial, conditional on every prior record, a fault gate opens with probability at most 0.01. On a faulty trial the attenuation score may be arbitrary. On all other trials the conditional model above holds, including independence of the setting. Thus that row charges $0.01+0.99\max f$ per trial. The timing null retains its own acquisition assumptions. The stated power for both rows concerns the clean single-excitation alternative. A retrospective one-percent average across a run does not establish the fault premise.

For the alternative, the probability of attenuation success is at least $\pi(0.98)+(1-\pi)(1-0.51\times0.98)=0.7995952$. On a full trial the timing success probability is at least $0.98p_1+0.02p_-$, where $p_1$ is the ideal full-efficiency lower endpoint and $p_-$ the exact negative-sign probability. The checker averages timing power over the binomial law of $M$. Adding the two marginal powers and subtracting one gives the stated joint lower bound regardless of dependence between the scores. Under either rival, joint rejection requires rejection by the test valid for that rival.

At 62% efficiency the same 158-shot optical count has power below 0.003728 at relative transmission 0.51. Changing the allocation and thresholds gives a 2,500-preparation design with joint power above 0.97324 under uniform loss. Published two-bank observations also permit a separate check of the optical field prediction. [Measured bank statistics and lower-efficiency decision](What_a_measured_source_can_test.md)

## What can still imitate the record?

A source that learns the setting can emit a bright pulse with full-setting miss probability 0.01 and vacuum on every attenuated trial. Its attenuation-success probability is 0.99376. Multihit suppression alone preserves the occupied-gate observation; a setting-dependent missed-first-hit rate, saturation that blanks a whole gate, or a reset failure can change it. A broader classical rule that first samples one rail from the propagated intensities and then independently thins that single event at the selected transmission reproduces the ideal record. These comparisons leave the underlying probability rule and physical identification open.

From the repository root, run `python -I -B Director_G/persistent_walk/check_random_transmission.py`. The computation uses exact binomial sums. Each conditional timing result is rounded outwards before the average over settings. [Executable](check_random_transmission.py) · [Decisions and cutoff tables](random_transmission_output.json)
