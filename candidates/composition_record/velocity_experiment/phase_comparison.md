# What the phase comparison tests

At each of two intermediate position writes in a nine-tick walk, choose \(S=\operatorname{diag}(1,i)\) or \(S^\dagger=\operatorname{diag}(1,-i)\). Let \(s_1,s_2=+1,-1\) denote the respective choices. A written site can leave local rail coherence even if the recording device forgets which site it saw. A phase choice can then alter a later position. The matched design changes only the signs of the two quarter turns. Its primary observable is the fraction of launches on which the first and third displacements have the same sign. [Circuit, bit order and replay](README.md) · [Classical flight law and the three-record phase prediction](../../../Director_G/A_phase_kept_between_three_position_records.md)

## A finite prediction independent of the incoming coin

With equal weights on all four phase assignments the ideal walk gives

$$
 E[s_1s_2\,\mathrm{sgn}(d_1)\mathrm{sgn}(d_3)]=-1/8,\qquad
 E[s_1s_2\,{\bf1}_{d_1d_3>0}]=-1/16.
$$

Equivalently the same-direction rate in the opposite-phase arms minus that in the equal-phase arms is **\(1/8\)**. Inserting a complete R/L measurement at either intermediate write gives zero. These are incident-launch predictions under ordinary probabilities and an exact site write. The identity holds for every localized trace-one source coin, including a complex superposition, provided the distribution of that coin is common to the phase choices.

Here is a short check using the real three-tick matrices \(M_d=\sqrt8\,T_d\) for \(d=-3,-1,1,3\). They are printed in the [six-tick calibration](../../../Director_G/What_two_velocity_records_can_identify.md). For unnormalized input \(\rho_1=M_{d_1}\rho M_{d_1}^\dagger/8\), the signed average of the first phase removes the diagonal and sends its upper off-diagonal \(z\) to \(-iz\). If the middle displacement is an edge \(\pm3\), the output has a single rail and the second phase has no effect. For either interior displacement the middle matrix has off-diagonal product \(M_{01}M_{10}=0\) and diagonal product \(M_{00}M_{11}=2\). After the second signed phase average the upper off-diagonal is \(-2z/8\) in each of the two interior branches. The final sign effect is \((X+Z)/2\); on a purely off-diagonal state it reads the real part of the upper entry. Finally the sign-weighted first-flight sum of real upper entries equals \(\mathrm{tr}(\rho)/4\), by the same four matrices. These factors give \(-1/8\). For a first displacement of \(\pm3\) the state reaching the first phase has one rail, so that phase also has no effect. The ideal phase interaction therefore vanishes separately on the events with \(|d_1|=3\) and with \(|d_2|=3\). Both are useful control strata with all launches retained in the denominator.

Independent, uniform \(S/S^\dagger\) draws at the two boundaries also realize a physical rail-dephasing **channel on average** because the single-boundary average removes every off-diagonal. Combining the four phase arms with equal weights therefore reproduces the dephased position law. This equality of the pooled law is built into the protocol. The discriminating measurement is the difference between the two phase-product groups. A separate arm that physically measures the rail can test how well the intended dephasing channel is realized.

## What the result can survive

Randomize the two signs independently of the source and apparatus. Balance within each prepared source and interleave jobs or blocks to address drift. For an input with one common spatial origin, recovering displacements from successive site readings removes a common translation of all positions, including the origin. Errors in a measured site affect *two* reconstructed displacements. Replacing missing outcomes with a favorable sign can create a contrast.

For a simple calibration model let \(m_{\sigma\tau}\) be the conditional mean reported outcome for true first and last signs \(\sigma,\tau\). It can include correlated sign errors. Assume these four numbers are independent of phase assignment, and that no other aspect of the true word changes the reporter. Their product-sign coefficient is \(\gamma=(m_{++}-m_{+-}-m_{-+}+m_{--})/4\). The other three basis functions of the two signs are \(1,\sigma,\tau\). The constant and first sign have zero phase interaction because a subsequent phase choice is still independently random. The last sign alone can carry an interaction for a polarized input. For example a sharp R source gives unconditioned real upper off-diagonal 1/4 after the first position write. Averaging over a balanced R/L source removes that term. The simple formula

$$
 E[s_1s_2\,m_{\sigma\tau}]=-\gamma/8
$$

therefore holds for a balanced \(I/2\) launch, for which the unconditioned first-flight coin is \(I/2\), or for a reporter with no term proportional to \(\tau\). The physical ideal sign product and equality observables satisfy the latter condition. When applying a general four-cell readout calibration, retain the source label and verify the balancing and common population assumptions. A phase-insensitive rival that generates the *entire* underlying word independently of both phase signs and uses a common reporting channel gives zero for any fixed function of the word. Control-dependent reporting can violate that null.

Likewise, rail phase drift is consequential. If the actual two phases are \(s_1\pi/2+\theta_1\) and \(s_2\pi/2+\theta_2\), the ideal sign-product interaction becomes \(-E[\cos(\theta_1+\theta_2)]/8\) for phase offsets set independently of the randomized signs and the subsequent displacement outcomes. This follows by multiplying the two off-diagonal factors in the preceding calculation, with the sign-weighted first-flight sum real. A second run with one pulse shifted by \(\pi/2\) measures the complementary quadrature. Perfectly coherent individual shots can have zero average interaction when their accumulated phase drifts.

As physical controls, prepare deterministic paths using identity and rail-exchange coins. All 64 displacement words can be constructed by selecting the three directions in each block to contain zero, one, two or three left moves. Quarter turns then add only a global phase on each trajectory. The same register and site-read clocks can test endianness, sign errors, losses, and control-dependent reporting. The [reporter calibration analysis](reporter_calibration.md) bounds the full-null and single-erasure contrasts separately and exhibits a hidden apparatus state that passes every forced-path control. Transfer of the resulting error estimates to coherent preparations remains an experimental premise.

## Analyzing incident counts

The [count analyzer](analyze_counts.py) weights the four strata in each phase-product group equally (two phase orders and two source rails). This remains correct for unequal attempted shot counts. It reports the primary difference and two edge controls. Under independent binary trials the three comparisons have simultaneous confidence coverage by Hoeffding's inequality and a union bound. From each arm it uses all recorded counts and the stated total attempts. It allows every missing outcome to take either event value and propagates the resulting interval. An ideal enumerated table receives no sampling interval. See the [histogram schema and commands](README.md). [Hoeffding's bounded-sum inequality](https://doi.org/10.1080/01621459.1963.10500830)

OpenAI Codex developed the circuit, discrimination test and checks in the research program of Kirtus Justus, Theoretical Physicist, Port Coquitlam, British Columbia, Canada. No hardware execution is reported.
