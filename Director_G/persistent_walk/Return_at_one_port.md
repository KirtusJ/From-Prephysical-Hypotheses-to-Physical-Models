# How well can finite stochastic memory predict one return port?

Director G research note for Kirtus Justus · 15 November 2026 · B.C. Pacific Time (UTC−07:00)

Prepare site zero on the right rail of a five-site ring. Every tick applies the same real Hadamard coin and sends the right and left outputs one site in their indicated directions. Keep all sites open. Each fresh launch is measured only once, at its chosen stopping time. Write $p_t$ for the unconditional probability of detection at the launch port. The competing model has $q_t=\alpha P^t b$, where $P$ is any finite row-stochastic matrix, $\alpha$ is a fixed launch distribution and each component of the fixed terminal response $b$ lies in $[0,1]$. Any clock phase used internally belongs to the state space.

**Theorem.** For every such predictor, $\limsup_{t\to\infty}|p_t-q_t|\ge 1/2$. The constant readout $1/2$ attains the bound. On multiples of every even integer the ideal return probabilities are dense in the whole interval $[0,1]$.

## The signed return amplitude at even times

Let $U$ denote one tick and $A_t=\langle 0,R|U^t|0,R\rangle$. In spatial Fourier mode $k=2\pi j/5$, the coin followed by its shifts is $U_k=\operatorname{diag}(e^{ik},e^{-ik})H$. The squared blocks $V_k=U_k^2$ have determinant one and trace $2-2\sin^2 k=2\cos^2 k$. The zero-momentum block is the identity. The other blocks occur in conjugate pairs. An $SU(2)$ matrix has conjugate diagonal entries, so summing the right-rail diagonal entry of $V_k^n$ with its counterpart at $-k$ gives the trace of $V_k^n$. Each site-Fourier mode has launch weight $1/5$. Thus
$$
 A_{2n}=\frac{1+u^n+u^{-n}+v^n+v^{-n}}5,\qquad p_t=A_t^2,
$$
where $u+u^{-1}=(3-\sqrt5)/4$ and $v+v^{-1}=(3+\sqrt5)/4$.

An independent direct matrix check gives the same weights. With $Q(z)=(1-z)(4-6z+9z^2-6z^3+4z^4)/4$, the $(0,R)$ diagonal cofactor divided by $\det(I-zU^2)$ equals $1-zQ'(z)/(5Q(z))$, and $\det(I-zU^2)=Q(z)^2$. This also fixes the rail and the clock convention without any numerical phase fitting.

## Why a single port visits the full probability interval

Put $K=\mathbb Q(\sqrt5)$ and call the two traces $s_1,s_2$. Their field trace is $3/2$, so neither can be an algebraic integer. Consequently neither $u$ nor $v$ can be a root of unity. Each discriminant $\Delta_j=s_j^2-4$ is negative and hence a nonsquare in this real field. Their product is $145/16$, again a nonsquare in $K$ because $\sqrt{29}\notin K$. The two quadratic extensions of $K$ are therefore independent. An automorphism fixes $u$ and sends $v$ to $v^{-1}$. If $u^a v^b=1$ for integers $a,b$, taking the quotient by its image gives $v^{2b}=1$. It follows that $a=b=0$.

For every positive integer $D$ the pairs $(u^{Dn},v^{Dn})$ are dense in the two-torus, with visits to every open neighborhood at arbitrarily large $n$. Indeed, every nonconstant torus character along this sequence is a geometric progression with mean zero, giving Haar equidistribution by trigonometric polynomial approximation. The continuous amplitude $(1+2\operatorname{Re}z+2\operatorname{Re}w)/5$ on this torus ranges from $-3/5$ to one. Its square ranges from zero to one. At phases $(1,1)$ the probability is one, and at $(e^{2\pi i/5},e^{4\pi i/5})$ it is zero by the sum of the fifth roots of unity. These are limits of the measured-port sequence. Haar averages independently give $\mathbb E[A_{2Dn}]=\mathbb E[p_{2Dn}]=1/5$.

For a finite chain take $D$ divisible by the periods of all its closed recurrent classes. The powers $P^{2Dn}$ converge, since the recurrent subclasses of the sampled chain are aperiodic and its transient mass tends to zero. Thus $q_{2Dn}\to c$ for some $c\in[0,1]$. Along this very progression the model must approximate both endpoints. The limit-superior error is at least $\max(c,1-c)\ge1/2$. A one-state model with $b=1/2$ attains the minimax value. A model required to give the certain return at tick zero can start in a transient state with readout one and then move to the constant half readout.

## What finite observations can establish

| Observation | Consequence under the stated model |
|---|---|
| Exact ideal probabilities on ticks 0 through 79 | No stochastic predictor with at most 55 states fits all 80. |
| A finite number of noisy launches against a fixed 55-state budget | A prespecified randomized terminal measurement has a calculated per-side error bound of 5% under the ideal walk and the stated stochastic alternatives. |
| Any prescribed probabilities on ticks 0 through $T$, with a free state budget | A counter with $T+1$ states and one fixed readout vector reproduces the entire list exactly. |

For the first row, the exact scalar return sequence has a minimal forward polynomial $m$ of degree 26 with a simple root at one. The included checker proves the recurrence with 100 consecutive tensor-state residuals, and proves minimality from the reduced generating function. Independently, the leading $26\times26$ integer Hankel matrix for $2^t p_t$ has determinant 202 modulo 1009. For an $h$-state rival the characteristic polynomial $\chi_P$ annihilates $q$. It too has a root at one. Hence the monic polynomial $\operatorname{lcm}(m,\chi_P)$ has degree at most $h+25$ and annihilates $p-q$. That many consecutive zero differences would force agreement for all subsequent times, in conflict with the theorem. For $h=55$ this gives 80 exact probabilities. Finite counts estimate those probabilities with sampling error.

For the second row, randomize the final tick, score a click using its prespecified cosine weight, and give every other launch a zero score. The mean is greater than 0.0325 for the ideal walk and less than 0.0177 throughout the specified 55-state class. A threshold of 0.0251 and 109,414 independent launches suffice for the two separate one-sided error guarantees. Some settings require 4,999,999 ticks. The calculation assumes fixed preparation, transition law and readout independent of the chosen stopping time, and counts all launches. Unknown dephasing and loss can lower the signal. The note specifies the distribution, resolvent estimate and integer interval verification. [Finite-duration design](A_finite_duration_return_test.md)

## Relation to earlier work and physical scope

Konno, Shimizu and Takei classified periods of the full Hadamard walk on cycles. Among sizes $N\ge2$ only 2, 4 and 8 give periodic operators. One can transfer this classification to the sharp return at one rail. Every Fourier block has nonzero off-diagonal entries, so each of its two eigenspaces has nonzero overlap with the launched rail. Weights at a repeated eigenvalue add as squared projection norms. Consequently the scalar probability has a strictly positive coefficient for every distinct eigenvalue ratio. Since the zero-momentum coin has eigenvalue one, periodicity of this scalar sequence forces every eigenvalue to be a root of unity. Conversely an operator period gives a scalar period, which a finite cyclic clock can reproduce. For the other sizes, a finite sum of unit-modulus frequency terms which becomes asymptotically periodic must already be periodic. Apply Cesàro frequency extraction to its difference at a proposed period. Thus the exact all-time stochastic obstruction extends to those sizes. The numerical sharp bound above was proved here for five sites. [Konno, Shimizu and Takei](https://doi.org/10.4036/iis.2017.A.01)

Earlier program work proves a different all-horizon obstruction for monitored first-arrival dynamics on three sites. The five-site intensity study instead varied preparations and continuations to obtain a finite table of rank 55. This note uses a single preparation, a fixed unrestricted coin and a single terminal port. An ordinary coherent classical wave with the same ten real amplitudes and square-law detection gives precisely the same return probabilities. A continuously variable internal phase or an externally supplied absolute-time readout also escapes the finite stochastic hypothesis. The discriminator concerns which descriptions of these records suffice. [Earlier first-arrival study](https://github.com/KirtusJ/From-Prephysical-Hypotheses-to-Physical-Models/blob/28d00e3895b116035bea178bcb327a74c6ae8083/candidates/composition_record/return_memory/finite_memory.md) · [Five-site intensity study](../intensity_memory/What_intensities_can_predict.md)

Bian and colleagues observed revivals in optical walks on three- and four-node circles. Those measurements supply an experimental comparison for cyclic walks. The five-site return test above requires its own preparations, fixed port, clock and per-launch records. No five-site data enter the theorem or the sample calculation. Physical Stage 1, the 13 identification gates and the status of the candidate primitive remain open. [Bian et al., Physical Review A 95, 052338](https://doi.org/10.1103/PhysRevA.95.052338)

## Reproduction

Run the two standard-library Python programs in this directory and compare stdout to the corresponding JSON. The first starts from the signed integer path counts. The second encloses the frequency separation and visible weight by outward-rounded integer intervals.

~~~sh
python -I -B check_open_spectrum.py
python -I -B check_finite_witness.py
~~~

[Exact spectrum and recurrence](check_open_spectrum.py) · [Spectrum receipt](open_spectrum_receipt.json) · [Finite score verification](check_finite_witness.py) · [Score receipt](weighted_return_receipt.json)
