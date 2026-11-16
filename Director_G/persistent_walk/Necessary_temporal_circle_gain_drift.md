# Necessary temporal gain drift in the ten-site optical-circle figure

For the displayed intervals of Lorz et al.'s Fig. 7(c), **at least one detector gain relative to the antipodal reference must change by a factor strictly greater than 1.88106 between rounds 13 and 11**, if a time-dependent multiplicative-gain model is to evade the previous fixed-gain contradiction while the ideal homogeneous circle walk remains in force. This is a *necessary* condition for that class of explanations, not an inferred drift of the actual apparatus.

Kirtus Justus, research direction. OpenAI ChatGPT (Director G), derivation and exact-rational check. 15 November 2026, B.C. Pacific Time (PCT, UTC−07:00).

## Source and assumptions

The scientific source is Lorz et al., *Photonic quantum walks with four-dimensional coins* (2019), Fig. 7 and Eq. (13), [DOI](https://doi.org/10.1103/PhysRevResearch.1.033036), [original color figure](https://arxiv.org/html/1809.00591v2/Fig7_asymmetricwalk_circle.png). The pinned model and source-figure reading are [PR #301, merge 8bffdb4020a2bfa3d2b399bda11a49f9671ceedb](https://github.com/KirtusJ/From-Prephysical-Hypotheses-to-Physical-Models/pull/301), especially [Testing three unequal circle detectors](Testing_three_unequal_circle_detectors.md) and its [saved readout](unequal_circle_gains_output.json). Saved source-figure interval data have Git blob SHA-1 772ed8386297f93e5564f06b7f0c835523b1b9b7, which identifies provenance only, not independent physical validation.

Let p(t,m) denote the ideal summed-rail site probability; q(t,m) the plotted positive intensity. Generalize the earlier model to q(t,m)=k(t)g(t,m)p(t,m), permitting a different arbitrary overall normalization k(t)>0 in each round and a different positive site gain g(t,m)>0 in the two rounds. The gains weight both internal rails equally. The launched rail state may differ arbitrarily between the rounds. Under the homogeneous coin and cyclic shift, the ideal sum p(t,5)+p(t,9) and p(t,7) are each independent of that launched rail state. Their ratio r(t) is 451/281 at t=11 and 1398/941 at t=13.

Put x(t)=g(t,7)/g(t,5), y(t)=g(t,7)/g(t,9). The necessary equation in every measured round is

$$
x(t)q(t,5)+y(t)q(t,9)=r(t)q(t,7).
$$

At the previously declared eight-level RGB interval allowance, the most favorable endpoints for an explanation with arbitrary positive gains yield

$$
A\cdot(x(11),y(11))\geq L,\qquad
C\cdot(x(13),y(13))\leq U,
$$

where A=(97/366,125/732), C=(167/732,31/183), L=40139/102846, U=10252/57401. These are necessary relaxations of the full preparation model, not an exact representation of detector measurements.

## Growth bound

Set K=max{x(11)/x(13), y(11)/y(13)}. Since all gains are positive, both components at round 11 are bounded by K times their round-13 counterparts. Set M=max{A_1/C_1,A_2/C_2}=194/167. Combining the two necessary inequalities,

$$
L\leq A\cdot(x(11),y(11))
\leq K M C\cdot(x(13),y(13))
\leq K M U.
$$

Consequently

$$
K>\frac{L}{MU}
=\frac{573429403}{304842288}
\approx1.8810690825.
$$

The inequality is strict for positive y(13), because A_2/C_2 is strictly smaller than M. The rational threshold is the **infimum for these two relaxed half-space constraints**, approached by letting y(13) tend to zero. It is not claimed sharp for a complete physical model. If every individual site's gain changes between the two rounds within the symmetric multiplicative interval [1/D,D], then both relative ratios are bounded by D². Thus such a gain explanation requires D>sqrt(573429403/304842288), approximately 1.371520719. This does not imply an observed 37% detector drift: the model class has not been calibrated experimentally.

## Adversarial controls and interpretation

The same endpoint argument with round 7 instead of 11 requires a weaker relative change exceeding 9585967/6811056 (~1.40741). For rounds 9 and 13 the relaxation gives a threshold of 192966165/215209984 (~0.89664), **below one**; it does not exclude fixed gains. The stronger single-site constraint used in PR #301 for rounds 9 and 13 is separate. Widening the RGB allowance enough can also destroy the earlier contradiction. These adverse cases must not be reported as independent replications or as positive physical evidence.

The local exact-rational checker, [check_temporal_gain_drift.py](check_temporal_gain_drift.py), reads the saved PR #301 intervals, verifies its main logged constraints and recomputes all three thresholds. The new checker was run with standard and optimized isolated Python on an explicitly transcribed subset of those JSON fields; both runs exited 0 and returned the exact thresholds above. The relevant fields were separately read back from the pinned GitHub blob. The full original PNG was **not** re-digitized for this calculation, and no hardware experiment, new data acquisition or detector calibration was performed. A direct checked-out repository run and a source-figure re-read remain separate possible audits.

A prospective falsification needs preselected rounds and sites, actual raw counts before plotted normalization, source and detector stability measurements, both internal-rail efficiencies, backgrounds, losses into other sites, and independent detector swaps. A rail-sensitive, additive-background, time-dependent coin, or state-transfer model is not excluded by this bound. Physical identification and Stage 1 Initial External Grounding, including root G1, remain open.
