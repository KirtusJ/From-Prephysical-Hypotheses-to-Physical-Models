# Can changing detector mass overcome pair contamination?

**Kirtus Justus**, Theoretical Physicist, Port Coquitlam, British Columbia, Canada. Research supplement prepared by OpenAI Codex for Director G.

At a hard cap of four quadrillion pairs, switching masses using the full observation history cannot restore 5% error when each pair independently has a 1.3% chance of coming from the opposite model. On the full allowed routed mass menu, every test has equal-prior error above **5.013928%**. A single repeated mass attains conditional error below **5.013950% under both laws**. The bounds apply even when the tester knows the contamination rate and the exact contaminated tables.

### Locating the critical common contamination rate

At **1.25996%**, a fixed-mass likelihood test meets the 5% target under each model. At **1.26003%**, even equal-prior error exceeds 5% for every randomized adaptive design. This bracket concerns a common, known, symmetric cross-mixture at every mass. It does not quantify tolerance to arbitrary changes of the same size.

To see why the endpoints bracket a transition, write Mₛ = (Pₛ+Qₛ)/2. The two contaminated tables at rate f have midpoint Mₛ and their differences from it scale by 1−2f. For 0 ≤ f₁ < f₂ ≤ 1/2, a tester observing a pair at rate f₁ can simulate rate f₂: keep the pair with probability (1−2f₂)/(1−2f₁), otherwise replace it with an independent draw from Mₛ. This same randomized transformation works under either hypothesis at the selected mass. Feeding only transformed observations to the next mass choice reproduces any rate-f₂ policy. Thus attainable conditional error targets become weakly harder as f increases on this range.

### A uniform displacement counterexample

At each mass let gₛ = TV(Pₛ,Qₛ). Use the smaller of 0.013 and (1.4534 × 10⁻¹⁰)/gₛ as the cross-mixture fraction; use no shift at identical-law controls. Both possible tables move by at most **1.4534 × 10⁻¹⁰ in total variation at every allowed mass**. Both retain the nominal one-detector marginals. For this explicitly defined perturbation the adaptive equal-prior error exceeds 5.000011%. Consequently no policy can guarantee both conditional errors at or below 5% over that entire TV uncertainty class. Smaller displacements may also suffice. The [earlier protected radius](Perturbing_the_paired_detector_laws.md) remains a sufficient bound for its specified rule.

### Verification

The [checker](check_adaptive_contamination.py) forms all mixtures with exact rational arithmetic before computing interval enclosures for log likelihoods. For the adaptive lower bound it applies the [bounded Brownian clock proof](Adaptive_exposure_for_two_paired_detector_laws.md) to the perturbed four-cell tables, recomputing the maximum one-pair clock across masses and both laws, and checking the jump bound. Identical-law controls add zero information. For the achievable upper bound it evaluates the [iid finite-sample likelihood bounds](check_fixed_exposure.py) under both shifted laws at every informative mass and takes the best common mass. Early decisions and adaptive randomization are covered by the lower bound; the upper bound uses all pairs at one mass. These results assume independent fresh draws conditional on the chosen mass. No detector data were acquired.
