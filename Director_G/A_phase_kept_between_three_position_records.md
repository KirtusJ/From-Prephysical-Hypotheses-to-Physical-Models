# A phase hidden from adjacent position records changes the diffusion coefficient

**Kirtus Justus**, Theoretical Physicist, Port Coquitlam, British Columbia, Canada. Mathematical development and exact replay by OpenAI Codex.

A device that measures the rail after writing a walker's site and a device that instead applies a quarter-turn phase can produce the **same joint distribution for every pair of adjacent flights** from a stationary source. After three flights they disagree even about the signs of the first and last displacements. With rare position writes, they also predict different long-time spreading rates. The preserved phase provides a concrete counterexample to treating a pair of classical-looking velocity records as a complete transition law.

## The three observed displacements

Use the [site-write walk, Fourier conventions and limiting instrument](Velocity_memory_after_a_position_record.md). Every flight starts at a single recorded site, runs freely for many Hadamard ticks, and ends in another exact site record. Start with the completely mixed coin \(I/2\), which can be prepared by an independently randomized sharp R or L launch. In one arm measure R versus L at every written site and discard its rail label. In the other apply the same phase operation \(\operatorname{diag}(1,i)\) after every write. The latter sends a coin Bloch vector \((x,y,z)\) to \((-y,x,z)\). All launch, intermediate and terminal *position* outcomes remain available in either arm. A different phase at random on each flight can change the result.

Let \(a,b,d\) denote three consecutive signed velocities, and \(\nu\) the symmetric free-flight law in the linked note. The following are densities relative to the product \(\nu(da)\nu(db)\nu(dd)\). For the R/L measurement arm the density is

$$
 p_{\rm rail}(a,b,d)=(1+ab)(1+bd).
$$

For the phase arm it is

$$
 p_{\rm phase}(a,b,d)=(1+ab)(1+bd)-ad(1-2b^2).
$$

Indeed after recording \(a\) the coin is \((x,y,z)=(a,0,a)\), and after the phase it is \((0,a,a)\). The second record has density \(1+ab\) in both arms. Before the second phase its unnormalized coin has \(x=z=b(1+ab)\) and \(y=(1-2b^2)a\). The second phase brings the latter component back into \(x\) with a minus sign. The density of the third record equals the incoming trace plus \(d\) times the sum of its unnormalized \(x,z\) components. This gives the formula above. For any real initial coin the triple has the additional first-flight factor \(1+(r_x+r_z)a\). Its first two records are again identical across arms. Stationarity is needed when asserting equality of *all* adjacent pairs without resetting the source.

All terms odd in \(a\) or \(d\) integrate to zero against their respective symmetric laws. Integrating out \(b\), on the other hand, gives \(1+cad\) for the rail arm and \(1+(3c-1)ad\) for the phase arm, where \(c=1-1/\sqrt2\). The first and third flights can therefore reveal the retained phase even when the middle displacement value is suppressed. For chronological displacements one, two, three the respective probabilities of equal signs for displacements **one and three** tend to

$$
 \tfrac12+c/8=0.536612\ldots,\qquad
 \tfrac12+(3c-1)/8=0.484835\ldots .
$$

Their difference in the order rail minus phase is \((1-2c)/8=0.051777\ldots\). Adjacent turn rates converge to \(5/8\) for both. A static calibration of the single-time speed law cannot detect this difference.

The effect can also be tested after **nine ticks**. With three ticks in each of the three flights, both instruments give the same entire adjacent-pair displacement table. This adjacent-pair equality also holds for unequal finite flight lengths. Averaging all earlier positions leaves the initial coin of the pair at \(I/2\) because a free flight summed over position is a unital coin channel (an average of momentum-space unitary conjugations). The first site matrix is real, so a quarter-turn and a rail measurement give the same diagonal and differ only by a purely imaginary off-diagonal. Every final position effect is real symmetric and has zero trace pairing with that difference. The first and third displacements have the same sign in exactly \(9/16\) of the rail-arm law and \(1/2\) of the phase-arm law. At these odd clocks there are no ties. At 256 ticks per flight the corresponding predictions are 0.537454 and 0.485433, including a tie probability of 0.004948 in both denominators. The [integer path replay](check_phase_history.py) obtains the short-clock result both by multiplying the position instruments and by independently enumerating signed paths.

## A classical consequence of the hidden component

The maximally mixed coin is stationary for the unmarked walk, site measurement and either boundary operation. In particular the phase arm has an ordinary joint distribution of the recorded velocities. Its sequence of velocities alone fails the first-order Markov test above. The averaged hidden coin nevertheless gives a short recurrence for all its displacement covariances.

After a phase write keep \(s=x+z\) and \(y\) as **unnormalized** coin components. Integrating over an unobserved flight and applying the next quarter turn maps these components by

$$
 (s,y)\longmapsto \big(c s-(1-2c)y,\;c s\big).
$$

The mean signed velocity from a given input is \(cs\). Equivalently a velocity-weighted first write from the mixed coin produces \((s,y)=(c,c)\). Thus at event lags \(k\), \(C_k=E[V_0V_k]\) has

$$
 C_0=c,\quad C_1=c^2,\quad
 C_{k+2}=c C_{k+1}-c(1-2c)C_k .
$$

The characteristic roots are conjugates of modulus \(\sqrt{c(1-2c)}<1\). For the rail arm \(C_k=c^{k+1}\). Give the two devices the same independent Poisson write clock of rate \(\lambda\), as in the rare-record construction. The integrated velocity \(X(t)\) then has asymptotic variance \(\operatorname{Var}X(t)/(2t)\to D\). Its covariance at elapsed time \(t\) is the Poisson average of \(C_k\) over \(k\) intervening writes, including zero. The integral over \(t\ge0\) is \(\lambda^{-1}\sum_{k\ge0} C_k\) by absolute convergence. Evaluating the generating functions at one yields

$$
 D_{\rm rail}=\frac{c}{\lambda(1-c)},\qquad
 D_{\rm phase}=\frac{c}{\lambda(1-2c^2)} .
$$

The coefficients are approximately \(0.414214/\lambda\) and \(0.353553/\lambda\). This compares second moments after taking the long-flight kinetic limit. The phase arm's second-moment calculation alone provides no functional central limit theorem for its full position record.

The [calibration and identifiability analysis](What_two_velocity_records_can_identify.md) gives a finite three-tick-per-flight test and specifies which third-flight observations can resolve hidden coin components. The [three-flight replay](check_phase_history.py) retains zero displacements. The [Lean algebra check](lean/VelocityPhaseMemory.lean) concerns the specified finite algebra, while the Fourier and kinetic limits are proved separately. These predictions assume an ordinary projective site write, identical free flights, and a phase-preserving local coin. Testing them requires actual multi-time data from a common apparatus.

A [three-qubit circuit and eight matched phase settings](../candidates/composition_record/velocity_experiment/README.md) implement the nine-tick comparison. A [signed phase interaction and two edge controls](../candidates/composition_record/velocity_experiment/phase_comparison.md) can be read from six stored position bits.
