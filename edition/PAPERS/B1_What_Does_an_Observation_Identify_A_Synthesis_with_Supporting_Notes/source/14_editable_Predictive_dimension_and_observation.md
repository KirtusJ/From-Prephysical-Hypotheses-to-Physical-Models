# Predictive dimension and observation

## 1. Operational and mathematical assumptions

Fix a block length `k >= 2` and an independent reference selector with `P(X=1)=t` and `P(X=0)=q=1-t`, where `0<t<1`. Define `h(1)=1`, `h(0)=-1` and `epsilon_k=min(t,q)^k`. On an aligned k-word x define

\[
P_k(x)=\prod_{i=1}^k p(x_i)-\epsilon_k\prod_{i=1}^k h(x_i).
\]

The correction has zero total mass and vanishes when any coordinate is marginalized. It is small enough to preserve nonnegativity. Concatenate independent k-blocks and draw the initial block offset uniformly from `0,...,k-1`, retaining that offset during a continuous run. This yields a stationary selector process. Every marginal with fewer than k sites is exactly the independent Bernoulli law.

Under the quantum-instrument comparison, a selector value 1 implements a known unitary gate; value 0 implements complete depolarization. A calibrated independent probe produces a match bit `Z`. It has `P(Z=1|X=1)=1` and `P(Z=1|X=0)=r`, with `r=1/16` for the ideal generalized Bell measurement. An additional classical detector may flip match bits.

We keep distinct the following experimental contracts: (i) a single continuous stationary controller run; (ii) independently reinitialized fixed-length records; (iii) direct access to the controller versus accessible probe records. Transition-emitting hidden-state counts refer to a model class, not to the microscopic state count of physical hardware.

## 2. Exact predictive dimension and its positive realization

### Proposition 1: zero-run Hankel lower bound

Let `z_m=P(X_1=...=X_m=0)`. Put

\[
 r_k=1-\frac{(-1)^k\epsilon_k}{q^k}.
\]

For `m=nk+j`, `n>=1` and `0<=j<k`, phase averaging gives

\[
\frac{z_m}{q^m}=\frac{(j+1)r_k^n+(k-j-1)r_k^{n-1}}{k},
\]

while `z_m=q^m` for `m<k`. These coefficients have rational generating function

\[
\sum_{m\ge0}\frac{z_m}{q^m}u^m=
\frac{\sum_{j=0}^{k-1}u^j+\frac{1-r_k}{k}u^k\sum_{j=0}^{k-2}(k-1-j)u^j}{1-r_k u^k}.
\]

The reduced sequence has Hankel rank `2k-1`, including the special case `r_k=0`. Consequently every linear predictive representation of the full stationary word process has dimension at least `2k-1`.

### Proposition 2: positive upper realization

For each proper prefix `u` of an aligned block, define

\[
 b(u)=\prod_{i=1}^{|u|}\frac{h(u_i)}{p(u_i)}.
\]

For each prefix length `j=1,...,k-1`, let `l_j` and `u_j` be its minimum and maximum over possible j-symbol prefixes. The conditional suffix law is affine in `b(u)`:

\[
P(v\mid u)=\prod_i p(v_i)-\epsilon_k b(u)\prod_i h(v_i).
\]

Therefore each intermediate conditional law is a convex mixture of the two endpoint laws at that position. Construct one fresh-block hidden state and two endpoint states at each interior position. At interior positions emit x with probability p(x), update b to `b h(x)/p(x)`, and randomly encode the updated b as the convex combination of the two endpoint states at the next position. At the final position emit x with probability `p(x)-epsilon_k b h(x)` and return to the fresh state. The output probabilities are nonnegative and normalized. Initialize phases uniformly; conditional endpoint weights have mean b zero at each interior position, which makes the initialization stationary.

This is a transition-emitting positive hidden-state model with `1+2(k-1)=2k-1` states. Proposition 1 proves that no smaller model of this class reproduces the complete word law. The equality of minimum positive and linear dimension is **specific to this construction**, not a generic consequence of finite Hankel rank.

### Verification

The accompanying verifier constructs exact rational transition probabilities and checks every output word up to lengths 7,8,10,8,7 for k=2,3,4,5,6, respectively. The resulting 2,047 word tests at k=4 agree exactly. The zero-run Hankel ranks are 3,5,7,9,11. Additional checks at t=1/10,1/2,4/5 preserve the claimed positive realization and Hankel ranks. No approximate numerical tolerance is used for these results.

## 3. Observation channels and predictive rank

### Proposition 3: injective per-use readout preserves linear predictive dimension

Suppose the hidden alphabet is `{0,1}` and an observation kernel K has different conditional output distributions `K_0` and `K_1`. Since both are normalized probability vectors, these columns are linearly independent. There exists a real linear left inverse L with `LK=I_2`. For any word length m, the output probability tensor is `K^{\otimes m}` applied to the hidden probability tensor, and the hidden tensor is recovered algebraically by `L^{\otimes m}`. Thus the full predictive Hankel ranks agree.

The left inverse can contain negative coefficients and is **not asserted to be a physical readout operation**. Statistical error may be amplified severely by it, so exact predictive-rank identification does not imply practical finite-sample identification.

At k=4, t=37/100, r=1/16 and an independent readout flip rate 1%, the leading observed 7x7 zero-run Hankel matrix has exact rank seven and a numerical smallest singular value of approximately 2.75841e-6. Rank is exact, whereas conditioning is poor.

## 4. New test separating bounded detector-only memory from controller correlations

A one-step calibration of detector error does not establish conditional independence across gate uses. A stronger null model still permits arbitrary within-record correlations of the bit flips.

**Null assumption H0:** selectors are independent Bernoulli(t), and ideal probe match bits are conditionally independent per use. The detector reports `Y_i=Z_i XOR E_i`, where the four flip variables may have any joint distribution, each has the same Bernoulli(e) marginal, and the entire error vector is independent of the ideal match vector. The distribution may be arbitrary across the four positions, but independent records must be initialized for the statistical guarantee below.

Set `s=t+(1-t)r`, `m=s+(1-2s)e` and the centered four-way statistic

\[
T_4=\prod_{i=1}^4 (Y_i-m).
\]

### Theorem 4: a universal correlated-flip bound within H0

Condition on the error vector. Since the ideal match bits are independent,

\[
\mathbb E(Y_i-m\mid E_i)=(1-2s)(E_i-e).
\]

It follows that

\[
\mathbb E_{H_0}T_4=(1-2s)^4\mathbb E\prod_{i=1}^4(E_i-e).
\]

Holder's inequality gives the exact **universal upper bound on the absolute value**

\[
\boxed{\left|\mathbb E_{H_0}T_4\right|
\le |1-2s|^4\left[e(1-e)^4+(1-e)e^4\right].}
\]

The Holder factor can be attained as a positive fourth moment by perfectly correlated errors `E_1=...=E_4`, though the sharpest negative-side bound could be smaller. The stated symmetric bound is deliberately conservative.

**Alternative H1:** the stationary four-block correlated selector is used with perturbation amplitude `epsilon_4=t^4`, while detector flips are independent Bernoulli(e). Exactly one of four possible phases aligns a full observed four-word with a block. Conditional-output factorization yields

\[
\boxed{\mathbb E_{H_1}T_4=-\frac{t^4}{4}\left[(1-r)(1-2e)\right]^4.}
\]

These are different **physically specified model classes**; the theorem is not a general device-independent memory-location witness.

### Exact numerical separation

At `t=37/100`, `r=1/16`, `e=1/100`:

\[
\begin{aligned}
s&=131/320=0.409375,\\
m&=6579/16000=0.4111875,\\
\mathbb E_{H_1}T_4&=-0.003338384177260746\ldots,\\
|\mathbb E_{H_0}T_4|&\le 0.000010367004497635\ldots.
\end{aligned}
\]

Thus the absolute alternative moment is 322.0201 times the conservative detector-only maximum. The signed separation below the null interval is 0.003328017172763111. An independent exact enumeration of all sixteen possible four-bit output patterns reproduces the H1 expectation and zero expectation for the ideal independent model.

### Theorem 5: a finite-sample test with declared size and power

Define `A=0.003338384177260746...`, `B=0.000010367004497635...`, `Delta=A-B>0`, and `R=max(m,1-m)^4=0.1202010010523694...`. For N independent and identically initialized four-gate records, compute the average of T4 and reject H0 when

\[
\overline T_4<-\frac{A+B}{2}.
\]

Each record satisfies `|T4|<=R`; Hoeffding's inequality gives under **every H0 model**, and under the specified H1,

\[
P(\text{respective decision error})\le\exp\left(-\frac{N\Delta^2}{8R^2}\right).
\]

For `N=31,264`, this upper bound is below 0.05 for both errors. Thus 31,264 independent four-gate records, totaling 125,056 gate uses, are a conservative sufficient design for at most 5% false rejection and at least 95% power against the named H1 alternative. This is **not** a minimum count. It does not include costs of calibration, randomized preparation, or environmental resets.

**Failure conditions:** H0 would have to be redefined if detector errors depend on the ideal flags, the nominal per-use flip rate is unknown or nonstationary, the selectors are correlated with detector errors, or there are dependencies across independent records. The source and detector may also both carry memory; this two-class test cannot establish uniqueness of memory location.
