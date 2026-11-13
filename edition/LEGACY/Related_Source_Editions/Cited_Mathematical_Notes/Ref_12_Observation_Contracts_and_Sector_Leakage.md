# Observation Contracts, Repetition Resources, and Sharp Sector-Leakage Bounds

*Selected sections of an unpublished mathematical note.*

**Original date:** 2026-11-09.  
**Research direction:** Kirtus Justus.  
**Mathematical and editorial assistance:** ChatGPT (OpenAI).

The selected statements, assumptions, arguments, and examples below are drawn from the original note. This editorial excerpt does not claim independent verification. Numerical results are source-reported unless established by the reproduced argument; cited literature is identified from the original note. Original section numbering is retained.


## 2. Compact-observation escape and its quantifiers

For `H = ell^2(Z) tensor C^2`, `rho_n = |e_n><e_n| tensor I_2/2`, and `J = I tensor Z`, the exact facts are

- `Tr rho_n=1`, `Tr rho_n J=0`, and `||rho_n||_1=1` for every `n`;
- `Tr(rho_n K) -> 0` for every **fixed** compact `K`;
- `sup_{0<=E<=I, E compact} Tr(rho_n E)=1` for **every** `n`, attained by `E_n=|e_n><e_n| tensor I_2`;
- if a family of compact effects is relatively compact in operator norm, the pointwise vanishing is **uniform** over that family.

The epsilon-net proof of the last statement is correct because all `rho_n` have trace norm one. No converse is claimed. Compactness is a restriction on a mathematical effect class; no physical detector-cost or source-selection mechanism follows.

**Observation-algebra qualification.** `K(H)` is nonunital in infinite dimension. For a binary compact click effect `E`, the complement `I-E` is not compact. The countable projectors `{E_m}` are each compact, but their infinite sum converges to `I` only strongly in `B(H)`, not in `K(H)` in operator norm. Thus the countably infinite-outcome PVM is a valid ideal `B(H)`-valued PVM **if this measurement completion is admitted**. It is not evidence that all its outcomes and normalization arise as a finite internal operation on `K(H)` alone. Similarly a three-outcome example of this form has two compact informative effects and a noncompact residual effect.

The identity effect measures normalization for all normalized states; it does **not** distinguish `rho_n` from a different normalized state. Comparison with the zero operator establishes nonvanishing of a mathematical functional, not a quantum discrimination experiment against another valid density operator.

## 3. Sharp approximate sector preservation

Let `P` be a nontrivial orthogonal projection, `Q=I-P`, and `Phi` any CPTP map. Put `E=Phi^dagger(P)`, a positive contraction, and define

`alpha = ||P(I-E)P||`, `beta = ||Q E Q||`.

**Theorem (optimal two-error universal bound).** For `0<=alpha,beta<=1`,

`||Phi^dagger(P)-P|| <= F(alpha,beta)`, where

`F(a,b)=[|a-b| + sqrt((a-b)^2+4 min(a,b))]/2`.

The bound is **attainable for each pair** `(alpha,beta)` in a two-dimensional CPTP construction. It improves the supplied conservative estimate `max(alpha,beta)+sqrt(min(alpha,beta))` and implies the simpler nonoptimal estimate `sqrt(max(alpha,beta))`.

*Proof.* For any unit vector with nonzero `P` and `Q` components, normalize those components to orthogonal vectors and compress `E` to their two-dimensional span. The compressed effect has matrix

`[[1-a,z],[conj(z),c]]`, with `0<=a<=alpha` and `0<=c<=beta`.

Positivity of this matrix and its complement forces

`|z|^2 <= min((1-a)c, a(1-c))`.

The difference from the compressed projection `diag(1,0)` is the Hermitian matrix `[[-a,z],[conj(z),c]]`. Its spectral norm is at most

`[|a-c|+sqrt((a+c)^2+4 min((1-a)c,a(1-c)))]/2 = F(a,c)`.

The function `F` is nondecreasing in each argument on `[0,1]^2`. For `a>=c`, writing `u=a-c`, it equals `[u+sqrt(u^2+4c)]/2`; its derivative with respect to `a` is positive, and its derivative with respect to `c` is nonnegative because `(2-u)^2-(u^2+4c)=4(1-a)>=0`. The other branch is symmetric. Therefore `F(a,c)<=F(alpha,beta)`. The cases of a vanishing component follow directly. Taking the supremum over unit vectors proves the claim.

For equality take the qubit effect

`E_*=[[1-alpha,z],[z,beta]]`, `z=sqrt(min((1-alpha) beta,alpha(1-beta)))`.

This is a positive contraction and its difference from `diag(1,0)` attains `F(alpha,beta)`. The measure-and-prepare channel

`Phi(rho)=Tr(E_* rho)|0><0|+Tr((I-E_*)rho)|1><1|`

is CPTP and has `Phi^dagger(|0><0|)=E_*`. Hence the bound is sharp even in the CPTP class. QED.

Special cases: if `alpha=beta=epsilon`, the exact maximum is `sqrt(epsilon)`, attained by a qubit rotation. If `beta=0`, the maximum is `alpha`. For block-diagonal input states the change is instead bounded linearly by `max(alpha,beta)`. Consequently, a claim of uniform `O(epsilon)` control of coherent preparations from `alpha,beta<=epsilon` is false.

## 4. Copy counts, optimal testing and resource thresholds

A single fixed compact binary effect is `E= sum_{j>=1} (j+1)^(-1) E_j`. Comparing `rho_n` with `rho_{2n}` gives `p_n=1/(n+1)` and `q_n=1/(2n+1)`; the one-use total variation tends to zero.

For `m` **independently prepared copies**, separately measured with this same effect, the click count `K` has laws `Bin(m,p_n)` and `Bin(m,q_n)`. For the choice `m=n`, the likelihood ratio increases with the click count `K`, obeys `L(0)<1`, and obeys `L(1)=2 [1-1/(2n+2)]^n>1` by Bernoulli's inequality. The optimal equal-prior decision therefore uses `K>=1`, with **exact** total variation

`TV(Bin(n,p_n),Bin(n,q_n))=(1-q_n)^n-(1-p_n)^n -> exp(-1/2)-exp(-1)`.

The asymptotic value `0.238651218541191...` is therefore optimal for **this restricted product detector**, not an optimum over arbitrary quantum effects.

For any copy count `m_n`, coupling gives `TV<=m_n |p_n-q_n|`. Hence `m_n=o(n)` guarantees vanishing discrimination. If `m_n/n -> infinity`, a threshold halfway between the two binomial means and Chebyshev's inequality yields error tending to zero because its squared signal-to-noise ratio grows proportional to `m_n/n`. For `m_n` of order `n`, a nonzero and generally nonunit limiting discrimination is possible. None of these expressions supplies a physical clock, rate, freely replicating source, or experimental cost.

**General adaptive restriction.** Suppose at each of `m_n` independently supplied copies an experimenter may choose adaptively from a fixed norm-precompact family `F` of compact **binary click effects**, with no collective processing before measurement. Set `epsilon_n = sup_{E in F} max{Tr(rho_n E),Tr(rho_{2n} E)}`. Then `epsilon_n ->0`, and maximal coupling of two experimental histories gives

`TV(full adaptive records under rho_n versus rho_{2n}) <= min(1,m_n epsilon_n)`.

Thus if `m_n epsilon_n ->0`, even adaptive measurement choice cannot rescue distinguishability **within that particular contract**. This does not handle collective quantum effects, unconstrained noncompact tests, unbounded outcome resolution, or a physically warranted rate for `epsilon_n`.

## 5. One fixed binary noncompact countercontrol

For a positive integer `n`, let `v_2(n)` be its 2-adic valuation. Define one fixed infinite-rank projector on the positive-label subspace,

`F_even = sum_{j>=1: v_2(j) is even} E_j`.

It is a bounded **noncompact** projection. For every `n>=1`, `v_2(2n)=v_2(n)+1`; therefore its two outcome distributions for `rho_n` and `rho_{2n}` are opposite deterministic bits. A **fixed two-outcome PVM** thus perfectly distinguishes **each specified pair** in one use, without infinite outcome resolution or an `n`-dependent detector.

The decision decoder still needs to know which `n` is being compared; the two source families overlap when `n` is an unspecified nuisance parameter, so no single uniform source-label decoder follows. This deliberately separates detector fixity, decision-rule side information, outcome resolution and physical availability.

The example shows why an assertion that repetition is *necessary* would be too strong once noncompact effects are admitted. It does not contradict the valid pointwise compact-observation limit.

## 6. Common reference entropy and the proposed capacity budget

For classical `f_i` with a fixed normalized reference `mu`, if every admissible preparation satisfies `D(f_i||mu)<=K`, then an ensemble satisfies

`I(source;Y) <= I(source;underlying outcome) <= K` nats,

by the relative-entropy decomposition and data processing. The corresponding quantum statement uses a common normal reference state, support conditions, Donald's identity, Holevo information, and measurement data processing. The resulting per-use information cap is `K/ln 2` bits, but only after a reference and an admissible preparation set have been independently selected.

**Direct quantum orthogonal-state test.** Let `sigma` be a fixed normal state on an infinite-dimensional Hilbert space, and `{P_j}` be countably many nonzero pairwise orthogonal projections, with `rho_j` supported in `P_j`. Set `q_j=Tr(sigma P_j)`. Data processing by `{P_j,I-P_j}` gives

`D(rho_j||sigma) >= -ln q_j`.

Because `sum_j q_j<=1`, `q_j->0` along an enumeration, so the divergence necessarily grows unbounded (or is already infinite when `q_j=0`). If all the first `N` orthogonal preparations satisfied `D(rho_j||sigma)<=K`, then `q_j>=exp(-K)` for those labels; summing yields `N<=exp(K)`. This is exact and conditional.

For the supplied bilateral-shift states, a concrete faithful reference is `sigma=sum_{j in Z} q_j rho_j`, with `q_j=2^{-|j|}/3`. Then `D(rho_n||sigma)=ln 3+|n| ln 2`. The “escape” states necessarily become arbitrarily expensive under this **chosen** reference, but nothing from signed balance or relational cores derives this reference or the cost rule.

A per-use budget also composes additively for product preparations and product references; allowing arbitrarily many independent uses may grow total information without a bound. To infer a global cosmological capacity requires an independently derived **global** resource budget, not a re-labeling of entropy.


## Mathematical sources identified in the original note


- D. Bakić, *Compact operators, the essential spectrum and the essential numerical range*, Mathematical Communications 3 (1998), 103–108. https://hrcak.srce.hr/en/file/2826

- B. Schumacher and M. Westmoreland, *Relative entropy in quantum information theory* (2000). https://arxiv.org/abs/quant-ph/0004045 . Background for relative-entropy identities and information bounds; the operational premises remain those stated above.
