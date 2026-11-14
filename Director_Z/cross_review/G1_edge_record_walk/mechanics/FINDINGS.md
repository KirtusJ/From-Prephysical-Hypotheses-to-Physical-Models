# FINDINGS — challenger on Director_G/candidates/edge_record_walk/mechanics.md
Reviewer: Claude sub-agent, same model family as the commissioning director; in-project review, not external, not independent.
Input read: mechanics.md only. Cited files (EdgeRecords.lean, Signed_walk_and_weak_field.md, Forced_envelope_and_classical_motion.md, Base_preparation_and_two_rays.md, the frontier balance theorem) NOT read, NOT checked.

## Item a (program p1_exact.py, results_p1_run1.txt; exact integers / sympy / 50-digit mpmath)
- A1 met: A^T A = 2I and A A^T = 2I on rings N = 1,2,3,4,5,8,12 (integer matrices).
- A1L met: A^T A = 2I on line windows m = 0,1,5.
- A2 met: on rings N = 4, 8 (exact roots of unity) the real-space step on a plane wave e^{ikx}v equals e^{ikx} sqrt2 U(k) v with U(k) = diag(e^{-ik},e^{ik})H, 24 of 24 instances. A2neg met: U(-k) fails on 16 of 24 (passes only at k = 0, pi). The stated kernel convention e^{-ikx} is the right one.
- A3 met: lambda_+ root, modulus 1, Re >= 1/sqrt2 (worst residual 4.5e-51 at 50 digits); other root is -conj(lambda_+).
- A4 met: U(k*)u = e^{i pi/4}u for u = (1,-i)/sqrt2; omega* = -pi/4, omega' = 0, omega'' = 1; u is not an eigenvector of the other band.
- GAP (minor, hypothesis stated nowhere): "A^T A = 2I, and U = A/sqrt2 is unitary" on the infinite line. A^T A = 2I gives an isometry only; unitarity on l^2(Z) also needs every port to be an output ((x,R) from block x-1, (x,L) from block x+1). True here, not said. On a window with ends it is false (4 output ports never hit in each window tested).

## Item d (p1_exact.py)
- D1 met: (1,1) -> (2,0), (1,-1) -> (0,2); formula probabilities (1,0), (0,1); each sharp rail gives (1/2,1/2).
- NONE FOUND.

## Item e (p1_exact.py, exact integer autocorrelation)
- E1a met: C_t(d) = 2^t C_0(d) for all d, t <= 10, 40 integer sources. Momentum density is preserved for every source.
- E1b met: 20 of 20 single-site sources have uniform density.
- E1c: 20 of 20 sources on two or more sites have NON-uniform density.
- GAP (wording): "Free waiting after a localized launch preserves the uniform total momentum density" is true only when "localized" means one site. A launch on two sites is localized and its density is not uniform (h = delta_0 + delta_1 on one rail gives |1+e^{-ik}|^2). The conclusion (free waiting cannot prepare the narrow band) survives, because the density is preserved whatever it is; the word "uniform" needs "single-site".

## Item h (p1_exact.py)
- H1 met: 48 (W,n,N) cells x 10 integer sources, every even N with W+2n+2 < N <= W+2n+8: ring and line evolutions agree on the cone at every tick <= n. Measured: agreement holds from N = W+2n+1 on (W = max site - min site), fails at N = W+2n in every (W,n). The stated condition is sufficient with slack 2; evenness is not used.
- H2 FAILED as written (kept): double precision gave max ratio |<a,Ma>-<b,Mb>|/(2 eta) = 1.0000000014 > 1 for the optimal M. Cause to be tested in follow-up H2b at 50 digits (cancellation in ||a-b|| at eta ~ 1e-6; exact value is cos(theta/2) <= 1).
- GAP (hypothesis in surrounding text only): the 2 eta bound needs BOTH vectors of norm one. The text says "normalizing" one sentence earlier. Without it: a=(1,0), b=(1.5,0), M=I gives 1.25 > 2 eta = 1.
