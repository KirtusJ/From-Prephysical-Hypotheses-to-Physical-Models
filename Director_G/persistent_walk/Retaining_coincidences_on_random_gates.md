# How often must both detector banks be read?

Kirtus Justus, research direction. OpenAI ChatGPT (Director G), optical decision rules and sample bounds. 15 November 2026, B.C. Pacific Time (PCT, UTC−07:00).

Consider a two-path readout whose electronics usually retain only whether a gate was occupied. At 10% full-setting efficiency, the [occupancy-only experiment](Reading_one_output_arm_at_random.md) needs at least 368,528 preparations to distinguish a clean single excitation from the specified conditional Poisson fields with both errors at most 5%. If each full gate independently has a 10% chance of retaining both bank outputs, 48,067 preparations suffice. Genuine coincidences carry information that the common occupancy register loses. The fraction of full gates that retain them determines how the sample cost grows with loss.

## What the electronics must record

Keep every preparation, including empty gates. Choose the full setting with probability one half. Otherwise open a single uniformly chosen path. On a fresh independent fraction $f$ of the full gates, retain both independently live bank bits. On the other full gates, keep only occupancy. The incident field cannot know the setting or bank selection in advance. Switching the readout must preserve both sensitivities, and the single-path shutter must preserve the sensitivity of the open path. The total number of occupied full gates is $K$, including the audited ones. The number of audited full gates with both bits set is $D$.

For the field hypothesis, condition on incident intensity and prior records. Each path takes a fraction in $[c,1-c]$ of the total detected Poisson rate. Conditional counts in the paths are independent. Write $t$ for full occupancy, $d$ for a full-setting double, and $h=c(1-c)$. If one rate share is $g$, the two path click probabilities are $1-(1-t)^g$ and $1-(1-t)^{1-g}$. Their product gives $d\ge h t^2$ by concavity. All numerical examples use $c=0.49$. The ideal alternative has independent single excitations with full efficiency $\eta$, no background and $d=0$.

## A test that uses confirmed doubles

For $f>0$ choose $w=(1-2fh\eta)^{-1}$, $A=1+(w-1)\eta/4$ and $k=\lceil3n\eta/8\rceil$ in advance. Reject the field when $D=0$ and $K\ge k$. Give each occupied full gate weight $w$, each audited double weight zero instead, and other records weight one. The field's expected weight at each preparation, conditional on history, satisfies
$$
1+(w-1)t/2-fw d/2
\;\le\; A-fw h(t-\eta)^2/2.
$$
Iteration and Markov's inequality bound false rejection by $A^n/w^k$. On independent clean excitations $K$ has law $\mathrm{Bin}(n,\eta/2)$ and $D=0$ surely. The miss probability is at most $\exp(-n\eta/64)$ by the lower-tail Chernoff bound. The checker uses the exact binomial lower tail when this estimate is loose.

| Full efficiency $\eta$ | Fraction $f$ of full gates retaining both banks | Necessary preparations | Sufficient preparations | Minimum occupied full gates $k$ |
|---:|---:|---:|---:|---:|
| 5% | 1% | 444,079 | 1,918,270 | 35,968 |
| 5% | 10% | 50,812 | 192,039 | 3,601 |
| 5% | 100% | 5,156 | 19,430 | 365 |
| 10% | 1% | 93,503 | 479,623 | 17,986 |
| 10% | 10% | 12,117 | 48,067 | 1,803 |
| 10% | 100% | 1,249 | 4,925 | 185 |
| 62% | 1% | 440 | 12,488 | 2,904 |
| 62% | 10% | 153 | 1,262 | 294 |
| 62% | 100% | 20 | 159 | 37 |

The lower bound applies to any fixed-sample optical decision using these settings and records. The upper column gives feasible designs for the stated rule. Each targets field false rejection at most 5% and clean-excitation acceptance of the field at most 5%. The fraction is conditional on a full gate, so $f=10\%$ reads both banks on 5% of all preparations on average.

## Why the sample cost changes

For a lower bound, take a balanced clean excitation and a balanced coherent field with the same full occupancy $\eta$. Each arm of that field clicks with probability $v=1-\sqrt{1-\eta}$, giving $d=v^2$. On a single-open gate the excitation clicks with probability $p=\eta/2$. The occupancy-only affinity is $\rho_0=(1+\sqrt{pv}+\sqrt{(1-p)(1-v)})/2$. On a full gate with two live bits, the probabilities for empty, left only, right only and both are $(1-\eta,\eta/2,\eta/2,0)$ and $(1-\eta,(\eta-d)/2,(\eta-d)/2,d)$. Summing square roots of products of matching probabilities gives the per-preparation affinity
$$
\rho_f=\rho_0-\frac{f}{2}\frac{d}{1+\sqrt{1-d/\eta}}.
$$
Total variation after $n$ independent preparations is at most $\sqrt{1-\rho_f^{2n}}$. The two error requirements imply total variation at least 0.90. The necessary column gives the first integer for which $\rho_f^{2n}\le0.19$. The path labels on single-open trials also have the same probabilities within each setting of this balanced comparison.

For small $\eta$, the affinity deficit is
$$
1-\rho_f=\eta^3/512+f\eta^2/16+O(\eta^4+f\eta^3).
$$
For sufficiency, the preceding occupancy-only design works with $O(\eta^{-3})$ preparations after discarding the extra bank bits. The present test works with $O(1/(f\eta^2))$. To see the latter bound uniformly, write $x=2fh\eta$. For $x\le1/4$, $\log w\ge x$ and $\log A\le x\eta/[4(1-x)]\le x\eta/3$. Hence $A^n/w^k\le\exp(-nfh\eta^2/12)$. The two tests can be chosen from $f,\eta$ before acquisition. Together with the lower bound they give
$$
n=\Theta\!\left((\eta^3+f\eta^2)^{-1}\right)
$$
at fixed positive $c$ and the stated errors. The two contributions have the same order when $f$ is proportional to $\eta$. A fixed positive fraction gives inverse-square growth as efficiency falls. This establishes the order for these fair settings and ideal preparations. Optimizing the settings or retaining rail and timing information defines another comparison.

## A rule for sources with occasional real doubles

Grangier, Roger and Aspect measured nine coincidences in a triggered cascade run for which their semiclassical calculation gave about fifty. This is a concrete reason to allow some audited doubles when specifying an experiment. Their published run used its own gates, detectors and source. [Experimental Evidence for a Photon Anticorrelation Effect on a Beam Splitter, pp. 175–177 (1986)](https://doi.org/10.1209/0295-5075/1/4/004)

For independent preparations, suppose a measured source has full occupancy at least 0.10 and full double probability at most 0.0002. These are prospective calibration requirements. With $f=0.10$, take 320,000 preparations and reject the field if $K\ge12{,}000$ and $D\le10$. For a field false-rejection bound, multiply by $w$ for each occupied full gate and by an additional $r=1/2$ for each audited double. The same quadratic argument now uses $f(1-r)$ in place of $f$ to calculate $w$ and $A$. The decision implies $w^K r^D\ge w^{12000}r^{10}$, giving field false rejection below 0.047236.

For the source, $\Pr(K<12000)\le e^{-500}$. The probability of an audited double on one preparation is at most $10^{-5}$. A union bound over all 11-element subsets gives $\Pr(D\ge11)\le {320000\choose11}(10^{-5})^{11}<0.0090245$. The combined miss probability is below 1%, without assuming independence between $K$ and $D$ on the same gate. The nine published coincidences supply no calibration of this proposed apparatus.

A shared latch that suppresses the second bank on an audited gate destroys the field bound. For a bright field it can report $K$ near $n/2$ and $D=0$ even with substantial actual coincidences. A simultaneous two-path pulse with known timing and independently measured bank responses can check that failure mode. Applying either rule to the five-site walk still requires source, optical split, switching and readout measurements. Stage 1 Initial External Grounding and physical identification remain open.

Run `python -I -B Director_G/persistent_walk/check_audited_banks.py` from the repository root. The [checker](check_audited_banks.py) uses the adjacent [occupancy arithmetic](check_complementary_shutters.py), checks the two-bank probability table independently and reproduces the [sample bounds and thresholds](audited_banks_output.json).

[Changing the polarization analyzer](Changing_the_polarization_analyzer.md) replaces a positive rate-share floor on each field with independently selected, calibrated analyzer axes and records both banks on every gate.
