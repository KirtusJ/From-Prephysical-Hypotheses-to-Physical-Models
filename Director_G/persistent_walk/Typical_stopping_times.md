# Prediction error at typical stopping times

Director G research note for Kirtus Justus · 15 November 2026 · B.C. Pacific Time (PCT, UTC−07:00)

Prepare site zero on the right rail of the five-site Hadamard walk. Keep all sites open, apply the same coin and shift at every tick, and observe the launch port only at the terminal time. Let p_t be its ideal unconditional return probability. A finite stochastic rival has prediction q_t = αP^t b, with fixed initial distribution α, finite row-stochastic P, and fixed response b with components in [0,1].

**Theorem.** Under equal weighting of the first T ticks, every such rival has a limiting mean-square error. The smallest possible value is 3264/105125. Its square root is approximately **0.1762065591**, or **17.62 percentage points** of RMS error in the predicted probability. A deterministic two-state clock attains it by predicting 1/5 on even ticks and 17/290 on odd ticks. These quantities concern the error between probabilities. Physical launch counts add sampling variation.

A separate, conservative bound gives a frequency of large mistakes. For every finite rival, the lower asymptotic density of times with |p_t−q_t| > 3/8 is at least **1/72** among all ticks. These results complement the limit-superior error of 1/2 in the [pinned one-port proof](https://github.com/KirtusJ/From-Prephysical-Hypotheses-to-Physical-Models/blob/a1eee36656ab413eac2cfa92c9d2bb62a1bea25e/Director_G/persistent_walk/Return_at_one_port.md). Neither proof assigns a deadline common to all finite rivals.

## The signed amplitude on each parity

Write k_j = 2πj/5 for j=1,2 and ω_j = arcsin(sin(k_j)/√2), taking the principal branch. In the spatial Fourier block at k the eigenvalues are exp(iω) and −exp(−iω). Their launch-rail weights within that block are (1+d)/2 and (1−d)/2, respectively, where d = cos(k)/√(1+cos²(k)). The projector onto the first eigenvalue is (U_k + exp(−iω)I)/(2cos ω), giving these weights directly. Blocks k and −k have complex-conjugate return amplitudes, and each site mode has weight 1/5. The zero block gives 1 on even ticks and 1/√2 on odd ticks. Adding the five blocks gives

- A_{2n} = [1 + 2 cos(2nω₁) + 2 cos(2nω₂)]/5.
- A_{2n+1} = 1/(5√2) + (2/5) Σⱼ dⱼ cos((2n+1)ωⱼ).
- p_t = A_t².

The two even-tick phases exp(2iω₁), exp(2iω₂) have no nontrivial multiplicative relation, by the discriminant argument in the pinned proof. Consequently (2nω₁,2nω₂) is uniformly distributed on the two-torus modulo 2π, including when n runs along any infinite arithmetic progression. Translation by (ω₁,ω₂) preserves uniformity for odd ticks. This last observation matters because the rival can keep a clock of any finite period.

## The optimal mean-square prediction

On either parity write the corresponding Haar-distributed signed amplitude as A=C+a₁cos x+a₂cos y with x,y independent uniform angles. Set S=a₁²+a₂² and B=a₁²a₂². The mean of A² is C²+S/2. Using E[cos² x]=1/2, E[cos⁴ x]=3/8 and zero odd moments gives

Var(A²) = 2C²S + S²/8 + 3B/4.

For example, on odd ticks aⱼ² = (4/25)cos²(kⱼ)/(1+cos²(kⱼ)), with cos²(k₁)=(3−√5)/8 and cos²(k₂)=(3+√5)/8. Substitution gives the rational moments in the table.

| Ticks | C² | S | B | Mean return | Variance of return |
|---|---:|---:|---:|---:|---:|
| Even | 1/25 | 8/25 | 16/625 | 1/5 | 36/625 |
| Odd | 1/50 | 56/725 | 16/18125 | 17/290 | 2364/525625 |

For a fixed rival take an even integer L divisible by every recurrent-class period of P. On each residue class r modulo L, q_t converges to a constant c_r. Its squared-error sequence has the same limiting average as (p_t−c_r)² because p_t,q_t,c_r are bounded. Equidistribution on this residue class gives the parity variance in the table plus (mean−c_r)². Each residue has weight 1/L. The two variances therefore contribute exactly (36/625 + 2364/525625)/2 = 3264/105125 and any additional term is nonnegative. The two-state clock starts in its even state and switches states at every step. With the two readouts in the table it realizes equality. A third transient state can enforce the certain launch-port return at tick zero if that extra condition is imposed.

## How frequently a large error must occur

Consider even ticks. On the phase rectangle |x|,|y| ≤ π/6, with angles represented in [−π,π], the return probability is at least (1+2√3)²/25. On the separate region where cos x and cos y both lie in [−1/2,0], the absolute amplitude is at most 1/5 and the probability is at most 1/25. Each region has Haar probability 1/36 and boundary of measure zero.

The two bounds differ by (12+4√3)/25 > 3/4. For any limiting prediction c_r, at least one region is uniformly farther than 3/8 from c_r. Its strict surplus over 3/8 ensures the same inequality for q_t at sufficiently late visits in that residue. Equidistribution gives lower density at least 1/36 on every even residue. Even ticks comprise half the clock, giving 1/72 overall. Optimality of this frequency bound is open here.

## Reproduction and scope

Run `python -I -B check_typical_times.py` from the folder containing this note. The standard-library checker independently evolves integer signed path counts on all ten ports. It compares both parity formulas at ticks 0 through 201 using arithmetic in ℚ(√5) after scaling odd amplitudes by √2. It integrates the second and fourth torus moments by a multinomial expansion as a check on the variance formula. The observed output included 202 matched ticks, means 1/5 and 17/290, variances 36/625 and 2364/525625, and the exact minimax mean-square error 3264/105125. Equidistribution and the all-model bound follow from the arguments above.

The model assumes ideal coherent evolution and square-law terminal readout. A coherent classical wave gives the same probabilities. The calculation supplies no experimental count or physical identification of the primitive.
