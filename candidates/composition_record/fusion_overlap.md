# What a measured comparison of two fusion orders identifies

**Kirtus Justus**, Theoretical Physicist, Port Coquitlam, British Columbia, Canada. Experimental comparison and calculations by Director G (OpenAI Codex).

Hai and colleagues used a four-spin NMR quantum simulator to compare two ways of fusing the excitations \(e,e,m\) in a toric-code plaquette. Three spins encode the plaquette. The fourth controls the comparison and provides two measured quadratures. The experiment supplies a physical example of reading a relative fusion phase. It also exposes a concrete test that a proposed physical realization of *Composition as a Record* would have to pass. [Hai et al., Fig. 4](https://doi.org/10.1093/nsr/nwac264) · [Authors’ supplement, Fig. S9 and p. 20](https://www.ebi.ac.uk/europepmc/webservices/rest/PMC10007699/supplementaryFiles)

## What the instrument reads

The supplement specifies the two Pauli strings \(A_1=X_3Z_3\) and \(A_2=Z_2X_3Z_1\). For plaquette input \(\rho\), the ideal complex overlap is \(\operatorname{tr}(\rho A_1^\dagger A_2)\). Direct multiplication gives

\[
 A_1^\dagger A_2=Z_3X_3 Z_2X_3Z_1=Z_1Z_2Z_3 .
\]

Thus a direct product-basis measurement of the three spins' parity gives the same ideal real mean on **every input**, including mixed states. The ideal imaginary mean vanishes on every input. The encoded ground state has equal amplitudes on \(000,011,101,110\), so its overlap is \(+1\). This equivalence concerns this particular comparison. The authors also studied half braiding in separate circuits.

There is an order convention to check directly against the figure. The detailed circuit, Fig. S9(b), applies controlled \(Z_3,X_3,Z_1,X_3,Z_2\) in chronological order. Its action on the activated branch is \(+Z_1Z_2Z_3\), agreeing with the target overlap. In Fig. S9(a), however, both boxes use the same filled control. Read literally left to right, they apply \(A_1^\dagger\) and then \(A_2\), yielding \(A_2 A_1^\dagger=-Z_1Z_2Z_3\). This minus sign would be observable relative to the inactive control branch. The detailed circuit and the paper's stated target support the plus sign. Either circuit predicts a real mean for every input. No pulse-level calibration is inferred here. [Supplement, Fig. S9(a,b)](https://www.ebi.ac.uk/europepmc/webservices/rest/PMC10007699/supplementaryFiles)

Before rescaling the radius to unity, the authors report \(\langle Z_4\rangle=0.712\pm0.006\) and \(\langle Y_4\rangle=0.177\pm0.004\). The two central estimates give a radius of \(0.733671\) and a polar angle of \(0.077558\pi\) in their convention. They report \((0.077\pm0.002)\pi\) and identify the toric-code value \(+1\). The measured point is \(0.338043\) from the ideal ground-state point and \(0.177\) from the entire interval of possible ideal complex means. Accordingly, changing the input state alone cannot reproduce the central estimates with the specified ideal operations and readout. A common readout contrast \(v=0.733671\) and phase offset \(\delta=0.077558\pi\), acting as multiplication by \(v e^{i\delta}\) on an ideal \(+1\) overlap, would reproduce both means. This is an identifiability example. The experiment does not establish that these two instrumental effects caused the deviations. These calculations use the published ensemble means. [Supplement, p. 20](https://www.ebi.ac.uk/europepmc/webservices/rest/PMC10007699/supplementaryFiles) · [Reproduce the circuit identity and numerical comparisons](check_fusion_overlap.py)

The distance to the schematic's even-parity point, \(-1\), is \(1.721126\). For a general complex branch overlap \(w=\operatorname{tr}(\rho U)\) acquired on control value one, a final Hadamard sends \(X\) to \(Z\) and \(Y\) to \(-Y\). Reading \(Z+iY\) after that Hadamard gives \(\bar w\) with standard Pauli signs. The sign convention has no effect on the zero-imaginary ideal prediction here. It matters for any experiment trying to orient a fifth root.

## A six-setting test for the candidate

Suppose a future carrier realizes a unit relative phase \(u(a,b,c)=\zeta^{\omega(a,b,c)}\), where \(\zeta=e^{2\pi i/5}\) and \(a,b,c\) are the candidate's labels. The five-valued phase encoding is an additional physical premise. Even a perfect read of one ordered triple cannot establish its cohomology class. For example, begin with the zero cocycle and give only the ordered pair \((e_2,e_3)\) a calibration \(f=1\). Its coboundary changes the exponent at \((e_1,e_2,e_3)\) from zero to one, within the same class.

Measure the six permutations of the three basis labels. Write \(m_\pi=K u_\pi\) for a common nonzero complex instrument response \(K\) over that panel. Form

\[
 P=\prod_{\pi\ {\rm even}}m_\pi\prod_{\pi\ {\rm odd}}\overline{m_\pi}
   =|K|^6\zeta^{\operatorname{Alt}(\omega)} .
\]

The three factors of \(K\) and three conjugates remove a fixed instrument phase. The coboundary of any pair calibration has zero alternation on this abelian label group, so it disappears as well. For \(\omega=s\det\), the exponent is \(6s=s\bmod 5\). The direction of \(P\) therefore identifies the determinant coefficient with an oriented quadrature convention. If the apparatus instead gives \(m_\pi=K\bar u_\pi\), the decoded coefficient becomes \(-s\). A known nonreal phase relative to a zero-phase reference can resolve this ambiguity. Other cohomology coefficients remain accessible to different tests in the candidate review. Positive setting-dependent contrasts also preserve the direction whenever all six are nonzero.

If setting \(\pi\) has residual phase error bounded in magnitude by \(d_\pi\) after removing a common offset, the phase error of \(P\), modulo a full turn, is at most \(\sum_\pi d_\pi\). A sum strictly below \(\pi/5\) suffices to decode the nearest fifth root. A common offset can be arbitrarily large. Independent setting offsets can instead produce any of the five answers even for a zero seed. Establishing comparable readout across settings needs independent controls. The toric-code experiment measured one fusion-order comparison and supplies no such bound for the proposed carrier. A reader given the six settings and the target table can reproduce even a perfectly calibrated panel. Physically distinguishing that reader from one coupled to the source still requires an independent change of the source and a bound on information about that change reaching the reader by other channels. [Candidate and proposed isolation test](README.md#the-test-that-separates-the-claims)
