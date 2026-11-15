# A measured phase reference for a controlled Hadamard

Wang, Xu, Zhu and Ma measured a system photon after a polarization interferometer whose last operation was a controlled Hadamard. The two optical branches applied the identity and the Hadamard to the same target. A separate trigger photon $T$ heralded the system source. The control $C$ belonged to an entangled pair with ancilla $A$. The interferometer phase $\varphi$ set the system preparation, the pair-source phase $\delta$ set the relative phase of the two branches, and $\alpha$ set the polarization basis at the ancilla detector. Shifting $\delta$ by $\pi$ reverses the acted branch in their circuit with the other settings held fixed. [Primary paper, Eqs. 1–6 and Appendix A](https://arxiv.org/pdf/1907.04159#page=2)

## The measured comparison

The authors kept the ancilla outcome $\alpha^\perp$. For those four-photon coincidences, $P_Q$ is the horizontal-system fraction with the anti-diagonal control outcome $C=-$, and $P_C$ is the horizontal-system fraction after pooling both diagonal control outcomes. In counts $n_{s,c}$ at that trigger and ancilla selection, these are $n_{H,-}/(n_{H,-}+n_{V,-})$ and $(n_{H,-}+n_{H,+})/\sum_{s,c}n_{s,c}$. Both denominators require detected coincidences. Their comparison uses some of the same counts. [Appendix D, Eqs. D6 and D8](https://arxiv.org/pdf/1907.04159#page=9)

At $\varphi=\delta=0$, the published figure gives the following conditional fractions and error-bar half-widths. The nine rows span the entire panel, including both negative differences. The last column uses the plotted values before rounding. [Figure 15B, last page](https://arxiv.org/pdf/1907.04159#page=16)

| $\alpha$ | $P_Q$ | bar | $P_C$ | bar | $P_Q-P_C$ |
|---:|---:|---:|---:|---:|---:|
| 0 | 0.465201 | 0.042666 | 0.523810 | 0.031587 | −0.058608 |
| $\pi/16$ | 0.612245 | 0.056469 | 0.465686 | 0.033784 | +0.146559 |
| $\pi/8$ | 0.655405 | 0.054557 | 0.475054 | 0.032101 | +0.180351 |
| $3\pi/16$ | 0.654676 | 0.056330 | 0.393548 | 0.029092 | +0.261128 |
| $\pi/4$ | 0.511905 | 0.054535 | 0.305317 | 0.022885 | +0.206587 |
| $5\pi/16$ | 0.324841 | 0.052013 | 0.247113 | 0.023889 | +0.077728 |
| $3\pi/8$ | 0.242915 | 0.037191 | 0.199405 | 0.017226 | +0.043510 |
| $7\pi/16$ | 0.170833 | 0.032163 | 0.152305 | 0.017471 | +0.018529 |
| $\pi/2$ | 0.123431 | 0.019372 | 0.133011 | 0.012682 | −0.009580 |

For the balanced setting $\alpha=\pi/4$, the observed difference is $+0.206587$. Taking the displayed errors as marginal standard errors, the triangle inequality bounds its standard error by $0.054535+0.022885=0.077420$ for any covariance, to the precision shown. The source derives statistical errors from counting statistics. The table supplies neither the covariance nor a systematic-error estimate. With $w$ the observed fraction of control-minus coincidences in the pooled table, $P_Q-P_C=(1-w)(P_{H\mid-}-P_{H\mid+})$. Thus the direction of the measured difference also orders the two control outcomes whenever both occurred. The magnitude for the complementary control outcome requires its population.

## Which sign is being read?

At $\varphi=0$, the bypass delivers $(|H\rangle-|V\rangle)/\sqrt2$ and the acted branch delivers $|V\rangle$. The $C=-$ projection adds those amplitudes with coefficients $\cos\alpha$ and $e^{i\delta}\sin\alpha$ in the authors' convention. At $\alpha=\pi/4$ the **ideal** probabilities are

$$
P_C=\tfrac14,\qquad P_Q(\delta)=\frac{1}{4(1-\cos\delta/\sqrt2)},\qquad
P_Q(0)=\frac{2+\sqrt2}{4},\quad P_Q(\pi)=\frac{2-\sqrt2}{4}.
$$

Only the bypass contributes to the horizontal numerator. Interference in the vertical channel changes the conditioning denominator. With these target states and a balanced control analyzer, dephasing the two branches gives $P_Q=P_C$. Positive horizontal and vertical detection efficiencies common to both control ports preserve the ordering of the fractions under the two signs when the control ports have balanced acceptance. An imperfect acted branch with a horizontal component or joint port-dependent loss requires its own calibration. The observed balanced fractions differ from both ideal values at $\delta=0$. Their ordering is the more limited comparison supported here.

The authors also scanned $\delta$ at fixed $\alpha=\pi/4$ and reported phase dependence in the control-selected distribution. Figure 4 used nine equally spaced phase settings from $-0.05\pi$ to $-1.95\pi$, with twelve interferometer settings. Its caption gives error-bar ranges of 0.020–0.043 for the pooled distribution and 0.020–0.074 for the selected one. The scan includes $-\pi$ and omits zero. Its interpolated surface supplies no exact measured $0,\pi$ pair in that acquisition. [Figure 4 and caption](https://arxiv.org/pdf/1907.04159#page=6)

The optical record establishes how the arm sign can enter a counted event when the phase of the source and the analyzer settings are held fixed. Assigning that sign to a position-controlled gate in the walk needs a phase reference calibrated on that gate and its bypass. An independent phase shift on the control can compensate a change $H\mapsto-H$. The optical predictions use ordinary quantum probabilities, and the reported fractions describe accepted coincidences. The all-launch distribution of the walk remains unmeasured here. [Complementary optical-gate calibration](../../../Director_G/Rational_references_and_optical_bypass.md) · [Scope of eraser records](../../../Director_G/What_two_eraser_experiments_measure.md)

## Replay

Run `python check_photonic_phase_data.py --fetch` from this directory, or pass `--figure PATH` for the published `Fig/SI/compare.pdf`. The standard-library reader verifies figure SHA-256 `aba9cf3838e6b03b63a4ae6a626a37a997b860a806d51792d26695ab002e3c22`, then reads the two halves of each colored vector error bar. In its drawing coordinates, $y=446$ is probability zero and $y=43$ is one. Panel B has nine abscissas $941+69j$, $\alpha=j\pi/16$. The printed digits describe the vector coordinates. The source archive supplies the plots and article rather than the underlying coincidence counts or covariance matrix. The publisher gives author request as the route to the underlying data. [Replay](check_photonic_phase_data.py) · [Authors' source archive](https://arxiv.org/src/1907.04159) · [Published data availability](https://doi.org/10.1038/s41566-019-0509-0)
