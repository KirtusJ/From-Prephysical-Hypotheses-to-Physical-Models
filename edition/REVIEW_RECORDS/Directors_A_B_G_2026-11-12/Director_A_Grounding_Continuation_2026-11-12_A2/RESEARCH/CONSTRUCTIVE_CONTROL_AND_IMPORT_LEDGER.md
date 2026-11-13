# Finite-cycle structural control and assumption ledger

## Finite input and exact output

Initial finite relational datum: oriented edges `1 -> 2 -> 3 -> 1`, with no duration, spatial embedding, frequency, wave, clock, preferred update, probability, field of amplitudes, or physical interpretation. To analyze it, choose its action on the free integer module `Z^3`, restrict to the zero-sum lattice, and rationalize. The permutation `P`, its transpose, and skew difference `C=P-P^T` satisfy `C^2=-3 Q`, where `Q=I-11^T/3`; on the two-dimensional contrast plane `Q=I`. This is an exact computation in a supplied linearization, not a derivation of that functor from experiment. It creates a rational endomorphism algebra `Q[sqrt(-3)]` and a nonzero alternating bilinear form on the contrast lattice.

A label-reflection reverses `P` to `P^2`, maps `C` to `-C`, and conjugates the complex representation after real completion. The full unoriented permutation group has only real scalars in its real commutant on the contrast plane. The two orientations of the unlabelled 3-cycle are graph-isomorphic. Thus covariance under relabelling and physical chirality selection must not be confused.

## Additional mathematical choices, each separately labelled

| Stage | Chosen input | Exact mathematical output | Status for physical emergence |
|---|---|---|---|
| directed 3-cycle | orientation is an initial relational datum, not a physical clock | cyclic permutation on 3 labels | stipulated primitive for trial, no observation |
| linearization | free `Z^3`, sum-zero restriction, rational scalars | contrast `V_Q`, `C^2=-3 I` | selected representation functor, not physically derived |
| Euclidean extension | tensor with R, counting inner product, positive square root of 3 | orthogonal `J=C/sqrt(3)` with `J^2=-I` | imported continuum / metric |
| multiplicity | take **two copies** `V_R ⊕ V_R` | complex dimension 2 as real structure | multiplicity choice not forced |
| phase geometry | unit sphere in the doubled module, continuous `exp(tJ)` action, its quotient | projective `CP^1`, standard Hopf/Fubini-Study structures | continuous group and quotient imported |
| measurement | postulate squared modulus of Hermitian overlaps | pairwise transition probabilities and Bargmann phase | Born-style rule stipulated, not emergent |
| dynamics | no generator specified | none | no time/clock or Hamiltonian |
| composition | no joint-system rule specified | none | quantum tensor product and instrument structure not derived |
| classical limit | no controlled `hbar -> 0` family or phase-space map supplied | none | classical mechanics not derived |

## Competing completion of exactly the same finite input

The ordinary 3-state probability simplex `Delta_2` carries preparations `p_i>=0`, `sum p_i=1`, effects `E_p(f)=sum_i p_i f_i`, pure states given by the three vertices and the reversible relabeling `p -> Pp`. Its contrast-space action still has `C^2=-3I`, yet its operational state space and probabilistic predictions are classical. Therefore a nontrivial internal complex representation does *not* select quantum probability, quantum superposition, entangled composition or classical phase-space mechanics. No additional proposed observation discriminates these completions here.

## Independent future discriminators, not achieved

The smallest next primitive-to-operational contract would name observable preparation distinctions, measurable effects and a calibration mapping that can rule out classical simplex and conjugate complex presentations without smuggling in interference or a reference phase. Further independent problems: justify the linearization, two-copy multiplicity, continuum completion, projective quotient, strong symmetry and spectrality postulates, Born probability calculus, tensor composition and instruments, calibrated physical time and dynamical generator, and a Hamiltonian classical limit with quantified uncertainty.

## Reproducibility scope

`VERIFICATION/verify_cycle_and_phase.py` tests symbolic identities with SymPy and carries forward every sampled floating-point trial. All machine outputs are internal researcher-assistant provenance. The numerical minimum Gram eigenvalue of `-2.0816681711746057e-17` in 271 trials is retained: it is a floating point artifact at a rank-deficient matrix, not a discovered physical negative probability or a disproval of positive semidefiniteness. Exact Gram inequalities provide the proof.
