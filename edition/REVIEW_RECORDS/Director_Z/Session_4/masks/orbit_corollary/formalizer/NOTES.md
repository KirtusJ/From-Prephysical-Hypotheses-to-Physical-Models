# NOTES (formalizer, z27, orbit corollary)

## Control (answered before any Lean)
N=4: gcd(4,2)=2, so M = 4/2 = 2. zeta = i: i^4 = 1, so i is a 4th root of unity;
i^(-2) = 1/(i^2) = 1/(-1) = -1. Yes.

## Plan
- L1: omega primitive N-th root; orderOf(omega^2) = N/gcd(N,2) = M; w^M=1 => w = (omega^2)^k;
  zeta = (omega^k)^-1. Try dropping N>=1 (Lean junk: N=0 gives M=0, any w; w=0 via zeta=0).
- L2: identities hold with no hypotheses in Lean's field (x/0=0):
  common u'=(g^2/g^2)u, rail u'=(conj l * l)u, site u'=(conj z * z/z^2)u; then specialise to |.|=1.
- L3: g=a'/a, l=c'a/(a'c). Needed only: a!=0, c!=0, |a|=|a'|, |c|=|c'|; b,d,b',d' unconstrained in modulus.
## Attempt 1 (Orbit_v1.lean, kept; output Orbit_v1.out): exit 1
Errors: wrong lemma name IsPrimitiveRoot.iff_orderOf; wrong sign in a linear_combination (rail det);
wrong coefficients in L3 (needed hu, not a'*hu). All mechanical. Attempt 2 = Orbit.lean.
## Attempt 2 (Orbit.lean): exit 0; all 12 theorems use only propext, Classical.choice, Quot.sound (Orbit.out).
Generalisations: L1 needs no N>=1 (N=0 junk case handled); L2 identities need no modulus hypothesis
(common phase needs g != 0 for u; rail det/u need |l|=1; site det needs nothing, site u = (conj z*z/z^2)u always);
L3 needs only a,c != 0, |a'|=|a|, |c'|=|c|; nothing on b,d,b',d'.
