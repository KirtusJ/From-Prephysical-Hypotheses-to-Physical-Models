# Calibrating the collision phase with a real launch

**Kirtus Justus**, Theoretical Physicist, Port Coquitlam, British Columbia, Canada. Research supplement by Director G (OpenAI Codex).

The [three-tick position experiment](Two_coin_position_read_at_one_contact.md) predicts agreement rates of 3/8 and 5/8 on two circular-coin panels when a collision changes the sign. Can the walk measure how much of that contrast its own collision actually supplies? A pair launched on sharp rails gives a calibration of the cosine of the phase. Swapping the order of the two starting sites cancels the sine term even on an unknown joint input. These are predictions for calibrated whole-site reads under the ordinary probability embedding. These rates have yet to be measured in this program.

## Three settings for an unknown joint coin

Keep the walk order, labels and position score of the three-tick experiment. At a coincidence, multiply **all four** joint rail amplitudes by the same factor $e^{i\phi}$. For a reproducibly prepared joint density matrix write $C_{UV}=\mathrm{tr}(\rho\, U\otimes V)$ for Pauli matrices $U,V$. Let $p_d$ be the probability of agreement for signed launch separation $d$, the initial position of B minus that of A. Write $c=\cos\phi$ and $s=\sin\phi$. Then

$$
16(p_{\pm2}-1/2)=(1+c)C_{ZZ}-(1-c)C_{YY}\ \pm\ s(C_{ZY}-C_{YZ}),\qquad
8(p_4-1/2)=C_{ZZ}.
$$

After the first split, the two-walker signed score pulls back to $X\otimes X/4$ before the collision phase. Only the inward route $RL$ meets for $d=+2$ ($LR$ for $d=-2$). Conjugation of $X\otimes X$ by the first contact leaves the $RR,LL$ exchange unchanged and phases the $RL,LR$ exchange. Conjugating back through both initial Hadamards gives the three Pauli terms above. At the second contact, fixed terminal positions and rails determine the preceding positions, so each output amplitude acquires one common phase. The final contact also contributes only a common phase to that output. Pooling the terminal rails preserves both cancellations for a scalar contact.

Use $RR$ as a known real calibration launch. Its $C_{ZZ}=1$ and all three correlations involving $Y$ in the formula vanish. Define $v=1-c$. The contrast against the far panel is $p_4^{RR}-p_{+2}^{RR}=v/16$. For the science panels, put $\bar p=(p_{+2}+p_{-2})/2$. When $v>0$, the read is

$$
C_{YY}=\frac{(2-v)\,8(p_4-1/2)-16(\bar p-1/2)}{v}.
$$

At $v=0$ the settings coincide and leave $C_{YY}$ unidentified. At $v=2$ the two near settings each read $1/2-C_{YY}/8$. A quarter-turn ($v=1$) retains half the circular contrast of the sign contact. Sharp rails determine $v$ without requiring a circular calibration input or an absolute sign for $s$. Dividing by a poorly resolved $v$ makes the inference unstable. Use the full interval of admissible calibration values when propagating uncertainties.

The mirrored settings require the same ensemble-averaged science input and the same contact law in both orientations. The mean cosine measured on the sharp-rail calibration must also carry over to the unknown science ensemble. A fluctuating phase independently drawn from the same distribution for each panel replaces $c,s$ by their means if it is independent of the input. Correlated preparation and phase can change the joint averages. Other premises include unchanged local Hadamards, labeled positions, and incident-pair accounting for loss. An ensemble of phases can share the calibrated cosine with a single phase. A near/far difference alone cannot certify a coherent collision mechanism or the probability embedding.

## What rail selectivity can hide

At positive separation a sign on only $RL$ at each coincidence gives the **same agreement effect** as the scalar sign. At negative separation that same selective sign yields the free agreement effect. A sign on $LR$ exchanges these two outcomes. These results come from propagating the full selective contact at each of the three ticks. The cancellation argument for a scalar phase does not automatically extend to a rail-dependent phase. [Exact propagation](check_contact_phase_calibration.py)

Schreiber and colleagues used a time-multiplexed optical lattice to encode two virtual walker positions. In their interacting run the diagonal coin was a controlled phase on one coin component followed by two Hadamards. Figure 3 reports a seven-step distribution. Appendix 1, Eq. (A2) gives the addressed component. Appendix 3 reports that the other polarization also acquired a phase, 1/3.5 of the intended shift. Their experiment demonstrates programmable position-conditioned interference. Testing the three-tick calibration above would also require the separated and reversed launches, the specified input panels, measured efficiencies and the corresponding agreement rates. [Experiment, Fig. 3 and appendices](https://arxiv.org/pdf/1204.3555) · [Published article](https://doi.org/10.1126/science.1218448)

Run `python -B Director_G/check_contact_phase_calibration.py` from the repository root. It propagates all four input columns as Gaussian integers, keeps both output rails, and checks every matrix entry of the signed read and normalization for eight phases at five signed spacings. It also contrasts each of the four single-rail sign contacts with the scalar and free controls in both near orientations.
