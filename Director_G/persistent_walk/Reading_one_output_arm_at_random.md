# Reading one output arm at random

Kirtus Justus, research direction. OpenAI ChatGPT (Director G), detector comparison and counting bounds. 15 November 2026, B.C. Pacific Time (PCT, UTC−07:00).

The [two-setting attenuation test](What_a_measured_source_can_test.md) can lose all distinguishing power at low terminal efficiency when the two hypotheses may use different allowed attenuations. Opening one of two complementary optical paths at random changes that conclusion. A single excitation then has exactly half its full click probability in the one-open condition, even if the paths have unequal transmission. A conditionally Poisson field gives a strictly larger fraction whenever both paths carry detectable intensity. The difference can be inferred using only an empty-or-occupied record. The number of independent preparations needed to resolve it grows as the inverse cube of the efficiency.

## Which gate is measured?

Independently of the incident signal, open both paths with probability one half. Otherwise open exactly one, chosen with a second fair coin. Keep every preparation, both coin settings and a single bit that records whether any admitted path produced a detection. The statistic below uses the first coin and the occupancy bit. It can tolerate electronics that discard all but the first hit in a nonempty gate. It requires that selecting a path preserves that path's full-setting sensitivity. Blocking one path must not increase the signal in the other. Recombination that permits interference at a common detector can violate this premise. Two distinguishable paths with a common first-hit register are one possible realization.

For a single excitation at full-setting efficiency $\eta$, the two mutually exclusive path click probabilities add to $\eta$. They become $\eta/2$ on averaging the single-open gate, regardless of their division. The finite-sample prediction assumes independent clean preparations, a constant total efficiency and negligible background. The full setting could retain a rail label separately. The results here use only optical occupancy.

Fiurášek gives tight classical bounds for an unbalanced two-detector Hanbury Brown–Twiss arrangement using the two marginal empty probabilities and their joint empty probability. Kovtoniuk, Bohmann and Semenov derive classical inequalities for one on-off detector at several efficiencies. The construction below uses complementary path choices and addresses their statistical cost under a conditional rate bound. No acquisition on the proposed walk is claimed. [Fiurášek, Phys. Rev. A 109, 033713 (2024)](https://doi.org/10.1103/PhysRevA.109.033713) · [Kovtoniuk, Bohmann and Semenov, Phys. Rev. A 113, 063726 (2026)](https://doi.org/10.1103/pknl-24xd)

## A uniform field bound without recording coincidences

Condition on the incident field and the preceding records. Let $u,v$ be the empty probabilities in the two paths. Conditional independence of Poisson counts gives full occupancy $t=1-uv$ and average single-path occupancy $z=1-(u+v)/2$. Thus
$$2z-t=(1-u)(1-v).$$
The right side is the conditional probability of a coincidence that an ideal two-bank readout would retain. It need never be registered by these electronics.

Assume each path receives a fraction between $c$ and $1-c$ of the full detected conditional rate for every admitted field, with $0<c\le1/2$. Write the rate shares as $g,1-g$. Then $u=(1-t)^g$ and $v=(1-t)^{1-g}$. Concavity gives $1-u\ge gt$ and $1-v\ge(1-g)t$. With $h=c(1-c)$ this yields
$$ z\ge \tfrac12(t+h t^2). $$
The inequality survives mixing fields because the square of the mean does not exceed the mean square. At the measured full mean $\eta>0$ it leaves a gap of at least $h\eta^2/2$ above the single-excitation prediction. The bound works for every positive efficiency. With a completely dark path, a finite coherent intensity in the other instead gives $t=\eta$, $z=\eta/2$ exactly for $\eta<1$. If even the selected-arm label is retained, an equal mixture of left-only and right-only pulses matches the balanced single-excitation law in each labeled arm. A path-dependent change in detector gain also invalidates the identity.

## A finite optical decision

For the calculations set $c=0.49$. Choose the trial count and target efficiency before looking at the outcomes. Put $b=h\eta/3$ and $a=b(1/2+h\eta)$. Multiply a running product by $1+a$ for a full-setting click, by $1-b$ for a single-open click, and by one for any empty gate. Call the final product $W$. Set $A=1+bh\eta^2/4$ and reject the field when $W\ge20A^n$.

The field's expected factor conditional on history is at most
$$1+\tfrac12(a-b/2)t-\tfrac14 bh t^2=A-\tfrac14 bh(t-\eta)^2.$$
Iteration and Markov's inequality bound false rejection by 0.05, including for fields that vary with the previous records. For the single excitation the expected reciprocal factor is
$$B=1+\frac{\eta}{2}\left[-\frac{a}{1+a}+\frac{b}{2(1-b)}\right].$$
The miss probability is at most $20(AB)^n$. Thus $(AB)^n\le1/400$ suffices for at least 95% power. Operating the apparatus only after seeing which setting was drawn can defeat the field premise.

| Full-setting efficiency | Necessary preparations for any fixed-size optical test¹ | Sufficient for the product test |
|---:|---:|---:|
| 5% | 3,171,029 | 18,775,529 |
| 10% | 368,528 | 2,393,857 |
| 15% | 101,213 | 723,990 |
| 42% | 2,858 | 37,334 |
| 62% | 555 | 12,927 |
| 98% | 20 | 4,149 |

¹Both columns use the same fair full-versus-single selection and require field false rejection and single-excitation misses each at most 5%. The lower bound concerns tests of the settings and occupancy, including randomized decisions. The selected-arm label cannot help against the balanced pair used below. Independent rail or timing records would define a different experiment. The sufficient sample sizes come from the stated inequality and leave a substantial gap for more efficient tests.

For necessity, compare a balanced excitation with a balanced coherent field adjusted to have the exact same full-setting occupancy $\eta$. Their single-open click probabilities are $p=\eta/2$ and $v=1-\sqrt{1-\eta}$. The per-preparation Hellinger affinity (sum of square roots of products of corresponding probabilities) is
$$\rho=\tfrac12[1+\sqrt{pv}+\sqrt{(1-p)(1-v)}].$$
After $n$ independent preparations the affinity is $\rho^n$. Total variation is at most $\sqrt{1-\rho^{2n}}$ by Cauchy–Schwarz, while 5% size and 95% power require total variation at least 0.90. Hence $\rho^{2n}\le0.19$ is necessary. The integer checker encloses the square roots and powers from both sides and verifies adjacent integers for each endpoint in the table.

As $\eta$ approaches zero, $v=p+\eta^2/8+O(\eta^3)$, so $1-\rho=\eta^3/512+O(\eta^4)$. For the product test, $1-AB=h^2\eta^3/24+O(\eta^4)$. These two expansions establish the inverse-cube order at fixed positive $c$. They do not give an optimal constant or fast discrimination at low efficiency. The earlier 2,500-preparation design at 62% uses another gate allocation and another statistic. The timing test and the physical origin of the probability rule require their own evidence. A model that first chooses one corpuscular output with the stipulated probabilities also has $z=\eta/2$.

Run `python -I -B Director_G/persistent_walk/check_complementary_shutters.py` from the repository root. [Executable](check_complementary_shutters.py) · [Numerical bounds and decision weights](complementary_shutters_output.json)

[Retaining coincidences on random gates](Retaining_coincidences_on_random_gates.md) gives the sample cost when both bank bits are available on a fraction of full gates, including a decision rule for occasional doubles.
