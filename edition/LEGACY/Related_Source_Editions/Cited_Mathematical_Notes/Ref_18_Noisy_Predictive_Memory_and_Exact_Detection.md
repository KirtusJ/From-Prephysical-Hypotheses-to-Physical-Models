# Noisy Predictive Memory and Exact Detection

*Selected sections of an unpublished mathematical note.*

**Original date:** 2026-11-09.  
**Research direction:** Kirtus Justus.  
**Mathematical and editorial assistance:** ChatGPT (OpenAI).

The selected statements, assumptions, arguments, and examples below are drawn from the original note. This editorial excerpt does not claim independent verification. Numerical results are source-reported unless established by the reproduced argument; cited literature is identified from the original note. Original section numbering is retained.


## 2. Mathematical and observation contract

For known integer L >= 1 and -1 < eta < 1, start with a uniformly distributed L-bit block. Given state x=(x_1,...,x_L), append b with probability

\[
 P_\eta(x,(x_2,\ldots,x_L,b))
 =\frac{1+\eta(-1)^{x_1+\cdots+x_L+b}}2.
\]

Let E_t be the modulo-two sum of Y_t,...,Y_(t+L). There is a bijection between the raw output record and its initial block plus these innovations. The innovations are iid, independent of the initial block, with Pr(E_t=0)=(1+eta)/2.

The readout model in this note is deliberately specific:

\[
 \widetilde Y_t=Y_t\oplus N_t,
 \qquad N_t\stackrel{\rm iid}{\sim}\operatorname{Bernoulli}(\epsilon),
 \qquad N\perp Y,
 \quad 0\le\epsilon<1/2.
\]

Write a=1-2 epsilon, W_t=(-1)^(E_t), V_j=(-1)^(N_j), and Z_t=(-1)^(tilde E_t). Then

\[
 Z_t=W_t\prod_{j=t}^{t+L}V_j.
\]

All W variables are independent with mean eta; all V variables are independent with mean a; the two complete families are independent. No physical detector is supplied by these definitions.

The observed initial L-bit block remains uniform and independent of the entire observed innovation sequence: conditional on all noise and innovation variables, it is the original uniform initial block XOR a fixed noise block. Consequently the observed innovation *sequence* is sufficient for the two-parameter law within this family. Its *count* is not generally sufficient.

## 3. Full noisy covariance and finite dependence

Direct cancellation of repeated detector factors gives

\[
 \mu:=\mathbb E Z_t=\eta a^{L+1}.
\]

For a lag h>=1, the exact covariance is

\[
 \Gamma_h=
 \begin{cases}
 \eta^2(a^{2h}-a^{2L+2}),&1\le h\le L,\\
 0,&h\ge L+1.
 \end{cases}
\]

Also Gamma_0=1-mu^2. For h<=L, the two detector windows have exactly 2h factors that occur only once; shared factors square to one. For h>=L+1, both W and detector factors are disjoint. More generally, groups of Z variables separated by more than L indices are independent, not merely uncorrelated.

If C_m counts the observed even innovations,

\[
 \operatorname{Var}(C_m)
 =\frac14\left[m\Gamma_0+
 2\sum_{h=1}^{\min(L,m-1)}(m-h)\Gamma_h\right].
\]

For L=2, eta=1/2, epsilon=1/10, the mean sign is 32/125, Gamma_1=1476/15625 and Gamma_2=576/15625. At m=40, E C_m=628/25 and Var(C_m)=185736/15625=11.887104. The binomial variance obtained by substituting the attenuated mean is 9.34464, so it omits a positive covariance contribution.

A concrete sufficiency failure is visible at just three observed innovations:

\[
 P(001)=681/5000,\qquad P(010)=609/5000.
\]

Both strings contain two even innovations. They have the same probability under the fair-iid null, but different alternative likelihoods. Thus count-only tests discard information available in the ordered record.

## 4. Exact finite count distributions and testing

### 4.1 Dynamic-programming recurrence

For a detector-history state h of L bits, let A_t(h,k) denote the joint probability that t observed innovations have been formed, the current detector history is h, and k innovations were even. Initially,

\[
 A_0(h,0)=\epsilon^{|h|}(1-\epsilon)^{L-|h|}.
\]

Append detector bit b with probability r_b, where r_1=epsilon. Let d(h,b) be the parity of all L+1 detector bits. Conditional on this window, the next observed innovation is even with probability

\[
 q(h,b)=\frac{1+\eta(-1)^{d(h,b)}}2.
\]

The recurrence adds A_t(h,k) r_b q(h,b) to A_(t+1)(shift(h,b),k+1), and A_t(h,k) r_b (1-q(h,b)) to the count-k entry. Summing over h gives the complete C_m law. For rational eta and epsilon, a common-denominator integer implementation avoids rounding entirely.


### 4.2 Power of the 40-innovation rule under noise

Fix L=2, eta=0 as null, eta=1/2 as alternative, epsilon=1/10, the uniform initial law, and a fixed horizon. The null remains iid fair observed bits. Its parity innovations, although overlapping as functions, are again iid fair under this null. Thus the rejection rule below still has size exactly 1/20.

The rule rejects for C_40>=26 and at C_40=25 with probability 4423136507/16760560440. Its alternative power is now

\[
 \frac{180356317471162013175783697521909827575795938288925685989}
 {366140029665280000000000000000000000000000000000000000000}
 =0.4925883619882841\ldots.
\]

The ideal-readout power 0.9530027582141789... does not transfer. A binomial alternative with the attenuated mean would give another incorrect value, approximately 0.4902866; neither substitution recovers the actual dependent count law.

### 4.3 A noise-aware repair, with sharply limited optimality

At each m, form the exact count likelihood ratio Pr_1(C_m=k)/Pr_0(C_m=k). Allocate rejection probability in decreasing ratio order, randomizing at a boundary. This is the finite Neyman–Pearson optimum over all randomized tests using C_m only (Neyman and Pearson, 1933). Ordering uses the exact ratios, without assuming monotonicity in the count.

The source reports that every m=1,...,182 fails to reach power 19/20 at size 1/20. At m=183 the count-optimal power is 0.9504796564538425... . In particular:

| m | Optimal count-test power at size 1/20 |
|---:|---:|
|40|0.4925883619882841...|
|182|0.9492033175217136...|
|183|0.9504796564538425...|

The exact boundary is C_m=103. A convenient slightly conservative rational rule is:

- Reject for C_183 >= 104.
- At C_183=103, reject with probability 43/50.
- Otherwise do not reject.

It has exact rational error comparisons with decimal summaries

\[
 \text{size}=0.04986347138568466\ldots,
 \qquad \text{power}=0.9503356923994559\ldots.
\]

The record contains L+m=185 consecutive outputs. Thus 183 innovations are necessary and sufficient **among randomized count-only fixed-horizon tests of these two specified noisy laws**. This is not an optimum over all ordered-record tests: the 001/010 example proves that the count is no longer sufficient. No monotonicity assumption across count-only horizons is used; the source reports exact evaluation of every smaller horizon.

A nonrandom sufficient rule uses 188 innovations, rejects for C_188>=106, and has size 0.04659560696121274... and power 0.9520313511286134... . No general deterministic-test minimality is claimed.

### 4.4 An alternative independent subexperiment

Selecting parity windows with starts spaced L+1 apart gives independent observed parity signs, since both the underlying innovation variables and detector windows are disjoint. Their even probability is (1+eta a^(L+1))/2. A binomial law is valid for this thinned experiment, but its sample count and raw span differ from the overlapping experiment. Merely replacing eta in the original overlapping-count formula is not equivalent to this change of design.

## 5. Conditional identification of source bias and detector noise

Let nu=E[Z_t Z_(t+1)]. Within the stipulated model,

\[
 \mu=\eta a^{L+1},\qquad \nu=\eta^2 a^2.
\]

For known L, eta nonzero, and a>0,

\[
 a=\left(\frac{\mu^2}{\nu}\right)^{1/(2L)},
 \qquad \epsilon=\frac{1-a}{2},
 \qquad \eta=\frac{\mu}{a^{L+1}}.
\]

Thus population knowledge of these two moments identifies both parameters within the declared independent symmetric-flip family. For the example mu=32/125 and nu=4/25 give a=4/5 and eta=1/2 exactly.

This result does not independently establish the detector model. Under eta=0 the output is fair iid for every epsilon, so epsilon is not identified. At epsilon=1/2 the source is erased entirely. Near either degeneracy the inversion is unstable. Estimated moments need valid uncertainty bounds for dependent observations. Plugging estimated eta or epsilon into the 183-innovation rule does not inherit its simple-hypothesis size and power guarantee.

## 6. Exact classical state dimension survives invertible readout

Let H_L be the 2^L by 2^L past/future block probability matrix. Let D_epsilon be the binary symmetric readout matrix with diagonal 1-epsilon and off-diagonal epsilon. Independent readout gives

\[
 \widetilde H_L
 =D_\epsilon^{\otimes L}\,H_L\,(D_\epsilon^{\otimes L})^\top.
\]

For epsilon!=1/2, both channel factors are invertible. The rank 2^L therefore survives whenever eta!=0. The original 2^L-state shift process followed by stochastic memoryless emission realizes the noisy output, so the lower and upper bounds match:

\[
 D_{\min}^{\rm classical,noisy}=2^L
 \qquad(0<|\eta|<1,\ 0\le\epsilon<1/2).
\]

Here classical HMM means a finite latent Markov state and state-conditioned independent emissions. The result does not count physical constituents, locate a mechanism, or bound quantum memory dimension. At eta=0 or epsilon=1/2, the observed output is fair iid and one classical state suffices.

### 6.1 Exact noisy singular values

For a binary vector s=(s_1,...,s_L), define

\[
 r_i(s)=\bigoplus_{j=1}^{i}s_j,
 \qquad \ell_i(s)=\bigoplus_{j=i}^{L}s_j.
\]

With |.| denoting Hamming weight, the complete noisy spectrum is

\[
 \boxed{\sigma_s(\widetilde H_L)
 =2^{-L}|\eta|^{|s|}a^{|r(s)|+|\ell(s)|},
 \qquad s\in\{0,1\}^L.}
\]

Proof. The latent block law has the expansion

\[
 H_L(x,y)=2^{-2L}\sum_s\eta^{|s|}
 (-1)^{r(s)\cdot x+\ell(s)\cdot y}.
\]

Each independent bit flip multiplies a Walsh character by a for each bit in its support. In orthonormal Walsh coordinates, the noisy matrix therefore has one nonzero entry per row and column, with the displayed signed weight. Both maps s->r(s) and s->ell(s) are invertible over the binary field. A weighted permutation matrix has singular values equal to its entry magnitudes. QED.

For L=2, eta=1/2, epsilon=1/10, the noisy singular values are exactly

\[
 (1/4,\ 8/125,\ 8/125,\ 1/25),
\]

where the error-free values were (1/4,1/8,1/8,1/16). Rank survives while conditioning worsens. A convenient general lower bound is sigma_min(tilde H_L)>=(|eta|a^2/2)^L, but the exact formula can be sharper.

A rank lower bound is only useful empirically with a justified matrix-error norm. For example, if a D-state candidate has block matrix H' and total-variation distance delta from the true 2L-word law, then ||tilde H_L-H'||_2 <= 2 delta. Since rank(H')<=D, ordinary singular-value rank bounds imply delta >= sigma_(D+1)(tilde H_L)/2. This is a lower bound, not an attained approximation optimum. Sampling uncertainty, readout-model error, and positivity constraints remain separate.


## Mathematical sources identified in the original note


- Kirtus Justus, *Predictive Memory, Innovations, and Realization Bounds* (9 November 2026). Unpublished companion mathematical note; internal research provenance, not independent corroboration.

- B. Ryabko, *Low-Entropy Stochastic Processes for Generating k-Distributed and Normal Sequences, and the Relationship of These Processes with Random Number Generators*, Mathematics 7 (2019), 838. DOI: 10.3390/math7090838. https://boris.ryabko.net/two-f-math.pdf . Background for the model family.

- Y. Ohta, *On the Realization of Hidden Markov Models and Tensor Decomposition* (2020/2021). https://arxiv.org/abs/2008.11487 . General realization and Hankel-rank background; the displayed noisy spectrum is not attributed to that work.

- J. Neyman and E. S. Pearson, *On the Problem of the Most Efficient Tests of Statistical Hypotheses*, Philosophical Transactions of the Royal Society A 231 (1933), 289–337. DOI: 10.1098/rsta.1933.0009. General likelihood-ratio ordering; not the noise-specific count calculation.
