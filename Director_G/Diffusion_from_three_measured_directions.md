# Inferring diffusion from three measured directions

Three position displacements of a nine-tick walk can determine the long-time diffusion coefficient of a different, rarely monitored walk, **if both experiments use the same time-independent coin channel** at every position write. The constituent rail phase can remain unknown. The data needed are the rates of agreement between the signs of displacements 1 and 2, 2 and 3, and 1 and 3. Two explicit alternating channels give identical three-flight word tables but different diffusion coefficients. This makes the time-independence assumption experimentally consequential. The results below are model predictions. [Three-qubit circuit and record order](../candidates/composition_record/velocity_experiment/README.md) · [Velocity-memory limit](Velocity_memory_after_a_position_record.md)

## What the short record identifies

Prepare one walker at site 0 with coin $I/2$ by a fair, logged choice between sharp R and sharp L. Run three blocks of three free Hadamard-and-shift ticks. Write the exact site at each boundary, retaining its local coin. No added calibration pulse is needed. Let the first two writes multiply the **lower** off-diagonal entry of the local coin density matrix by $\gamma_i=x_i+iy_i$, and the upper entry by its conjugate. Populations remain unchanged. This is a trace-preserving positive quantum channel for $|\gamma_i|\le1$. Its pure-phase special case is conjugation by $\operatorname{diag}(1,e^{i\phi_i})$. The specification presumes the same channel across sites and histories at each particular write, and calibrated preparation, evolution and reporting. Each sign-agreement rate $P_{ij}=\Pr(D_iD_j>0)$ uses every incident launch. All three-tick displacements are odd.

The exact rates are

$$
8P_{12}=5+x_1,\qquad 8P_{23}=5+x_2,\qquad
16P_{13}=9+x_2+x_1x_2-y_1y_2.
$$

These identities use ordinary probabilities at the recorded sites. A direct derivation uses the real three-tick signed matrices $M_d=\sqrt{8}\,T_d$ for displacements $d=-3,-1,1,3$. Given a density with upper entry $B+iJ$, the real off-diagonal entry after multiplying by $M_d$ on the left and $M_d^\top$ on the right is $acA+(ad+bc)B+bdC$, for $M_d=\left(\begin{smallmatrix}a&b\\c&d\end{smallmatrix}\right)$ and initial diagonal entries $A,C$. The imaginary part is $(ad-bc)J$. The write rotates and attenuates that pair to $(x_i B+y_i J,\ x_i J-y_i B)$, now using the entries just after the flight. A factor $1/8$ per flight restores normalization.

Summing the corresponding records is affine in $(x_1,y_1)$ and separately affine in $(x_2,y_2)$. To verify all coefficients, evaluate at $(0,0),(1,0),(0,1)$ for each write. The following table gives $16P_{13}$, with rows for the first channel and columns for the second. These nine evaluations determine a separately affine function on the entire product of unit disks. The [exact checker](check_phase_diffusion.py) verifies the same grid for both adjacent rates. Summing a complete flight over positions leaves $I/2$ fixed for a localized $I/2$ launch. The pooled second adjacent pair thus has the same preparation as the first. [Signed three-tick matrices](What_two_velocity_records_can_identify.md)

| First / second | $(0,0)$ | $(1,0)$ | $(0,1)$ |
| --- | ---: | ---: | ---: |
| $(0,0)$ | 9 | 10 | 9 |
| $(1,0)$ | 9 | 11 | 9 |
| $(0,1)$ | 9 | 10 | 8 |

For a common fixed channel $\gamma=x+iy$, the data must have $P_{12}=P_{23}$. Recover $x=8P_{12}-5$ and $y^2=9+x+x^2-16P_{13}$. The physical range requires $-1\le x\le 1$ and $0\le y^2\le 1-x^2$. Complex conjugation changes the sign of $y$ while preserving all position records of the real experiment. The diffusion coefficient below uses only the identifiable pair $(x,y^2)$. For a pure phase, $y^2=1-x^2$, so even one adjacent rate fixes its transport prediction; the other rates test consistency. The earlier [two-reference write calibration](../candidates/composition_record/velocity_experiment/README.md#calibrating-the-two-writes-separately) treated real attenuation. Here the outer pair also recovers the feedback through imaginary coherence.

## Transfer to the rare-write walk

Use the free walk on an unwrapped line, with $n$ ticks per macroscopic unit of time and site spacing $1/n$. Independent control schedules enable exact position writes with probability $p_n$ per microscopic tick, $np_n\to\lambda>0$. At each enabled write apply the same channel $\gamma$ used in the calibration. First take the kinetic limit on fixed macroscopic intervals. The resulting Poisson clock has rate $\lambda$. Then take long time in that limiting process. The coefficient $D$ is the asymptotic ratio $\operatorname{Var}X(t)/(2t)$ for the stationary velocity ensemble. A single inferred coefficient is a statement about second moments of an ensemble of recorded motions. The construction does not establish a functional central limit theorem for every hidden-phase channel. [Rare-write record convergence](Velocity_memory_after_a_position_record.md) · [Quarter-turn hidden-coin recurrence](A_phase_kept_between_three_position_records.md)

Write $c=1-1/\sqrt2$ and $d=1-2c$. Here $c$ is the stationary second velocity moment. On an averaged, possibly unnormalized coin let $s=r_x+r_z$ and $j=r_y$ denote Bloch components. Integrating an unobserved long flight maps $(r_x,r_y,r_z)$ to $(cs,dj,cs)$ by the Hadamard band projectors. Applying the calibrated channel then gives the boundary matrix

$$
B=\begin{pmatrix}c(1+x)&-dy\\cy&dx\end{pmatrix}
$$

on $(s,j)$. A velocity-weighted first record from $I/2$ produces $B(1,0)^\top$. The next signed-velocity read has mean $cs$. Thus the stationary event-lag covariance is $C_k=c(B^k)_{11}$, including $C_0=c$. Between Poisson writes the limiting velocity remains the same. Summing the Poisson weights and integrating the covariance in macroscopic time gives

$$
\lambda D=\sum_{k\ge0}C_k=
\frac{c(1-dx)}
{[1-c(1+x)](1-dx)+cd\,y^2}.
$$

Absolute convergence holds uniformly on the entire channel disk. The unobserved full Bloch flight operator is real symmetric with eigenvalues $2c,d,0$, and the disk channel contracts the Euclidean Bloch norm. Their product therefore has norm at most $\max(2c,d)<1$. The matrix $B$ represents its induced map on the two visible components; the hidden orthogonal component is killed before the next write. In particular event-lag covariances decay geometrically. The denominator also has the explicit uniform lower bound $(1-2c)(1-d)>0$, since $|x|\le1$ and $y^2\ge0$. Thus finite sampling error does not generate an intrinsic pole at a physical channel, including a fully dephased one. With experimental intervals one can intersect the intervals for the three rates with the physical disk constraints and bound the displayed rational expression over that compact set. Testing the unrestrained inversion at noisy central estimates can produce an unphysical negative $y^2$. If the control rate is reported in inverse seconds and physical velocities are a scale $v_0$ times the velocities used here, multiply the dimensionless numerator for $\lambda D$ by $v_0^2$ to recover length squared per second. [Velocity-jump diffusion limit](https://doi.org/10.1137/S0036139999358167)

For a calibrated identity ($x=1,y=0$) the result is $\lambda D=c/(1-2c)$. Complete rail dephasing gives $c/(1-c)$. A pure quarter turn gives $c/(1-2c^2)$ and a fixed sign gate gives $c$. Each case uses the same Poisson rate. The nine-tick measurement supplies the channel parameters; it does not by itself verify the random clock, frequency transfer across flight lengths, or the free long-flight limit.

## Equal short records and unequal alternating transport

For two distinct contacts and a real source, every word in the reference table depends only on $x_1,x_2,y_1y_2$. After the first real flight there is no imaginary component. The first write creates one proportional to $y_1$; the second real flight transports that term only within the imaginary component. Only its conversion back to a real read by $y_2$ contributes to final position. Products of the two real parts and ordinary population terms are already determined by $x_1,x_2$. Consider the two ordered pairs

$$
(\gamma_1,\gamma_2)=(1/2+i/2,\,-1/4+i/2),\qquad
(\gamma'_1,\gamma'_2)=(1/2+3i/8,\,-1/4+2i/3).
$$

Both lie in the unit disks and have $x_1=1/2,\ x_2=-1/4,\ y_1y_2=1/4$. The [exact calculation](check_phase_diffusion.py) compares all 64 words separately for each sharp real source R and L, as well as for $I/2$. Now repeat the respective channels in alternation at successive Poisson events. For the stationary transport coefficient choose the first phase of the alternating schedule uniformly, independently of the coin and clock. Let $B_1,B_2$ be the two boundary matrices. For one parity, summing the even- and odd-length products gives the $(1,1)$ entry of $(I+B_1)(I-B_2B_1)^{-1}$. Average it with the expression with indices reversed and multiply by $c$. This yields $\lambda D=0.4117292182\ldots$ for the first pair and $0.4097829800\ldots$ for the second; the checker distinguishes them in $\mathbb Q(\sqrt2)$ before rounding. Their finite comparisons begin with the first listed contact in each apparatus. Averaging the starting parity of the short circuit also preserves their equality.

Thus even acquiring the complete unshifted histogram leaves alternating transport ambiguous. Real parts and their product statistics measured on one transfer schedule do not establish a common channel that persists under later interventions. Standard-library reproduction from the repository root:

    python -I -O Director_G/check_phase_diffusion.py

Kirtus Justus, Theoretical Physicist, Port Coquitlam, British Columbia, Canada, retains scholarly responsibility for the program. OpenAI Codex developed the finite calibration, transport calculation and checks.
