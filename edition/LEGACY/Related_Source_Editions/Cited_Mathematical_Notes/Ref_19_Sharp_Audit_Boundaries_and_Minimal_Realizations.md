# Sharp Audit Boundaries and Minimal Stochastic Realizations

*Selected sections of an unpublished mathematical note.*

**Original date:** 2026-11-09.  
**Research direction:** Kirtus Justus.  
**Mathematical and editorial assistance:** ChatGPT (OpenAI).

The selected statements, assumptions, arguments, and examples below are drawn from the original note. This editorial excerpt does not claim independent verification. Numerical results are source-reported unless established by the reproduced argument; cited literature is identified from the original note. Original section numbering is retained.


## 2. A finite-population calibration gate

The report population has

\[
M=\binom{2{,}000{,}000}{2}=1{,}999{,}999{,}000{,}000
\]

binary discrepancy entries. Reports and their comparison reference must be fixed before independent audit and detection query randomizations. A truthful reference, stable sample identity, source independence, and the stated reporting-error class are assumptions, not conclusions.

Consider an audit of 200,000 distinct entries that accepts at most eight discrepancies. For bad populations with error fraction at least \(10^{-4}\), the bound is

\[
P(\mathrm{pass})\le(49997/50000)^{200000}(5/2)^8<47/5000.
\]

For populations whose actual fraction is at most \(10^{-5}\),

\[
P(\mathrm{fail})\le(200007/200000)^{200000}(2/9)^9<29/20000.
\]

The source reports exact integer cross-multiplication for both strict rational bounds. Hoeffding's finite-population convex comparison (1963, Theorem 4) supports the moment bound used in this argument. It does not supply the numerical gate constants or a detector model.

The sparse detector error bounds are

\[
\alpha_s=\frac{25032226015092744528840625}{634998927977903024107964257},\qquad
\beta_s=\frac{27900695463010851341340625}{699384194430517969365104257}.
\]

They imply the retained complete-procedure guarantees

\[
\alpha_{\mathrm{total}}\le\alpha_s+47/5000<1/20,
\qquad
\mathrm{power}_{\mathrm{total}}\ge1-\beta_s-29/20000>19/20
\]

under the stated uniformly good alternative class. Passing the audit does not establish the \(10^{-5}\) premise as a posterior fact, does not validate future records without a transfer assumption, and does not warrant the audit reference itself.

## 3. Sharp-boundary calibration: the precise experiment

Fix an unknown binary vector of length \(M\), with exactly \(E\) discrepancy entries. A truthful query reveals one entry. There are no auxiliary features, direct observations, side channels, or structural restrictions that identify error locations. The vector is fixed independently of the audit randomization.

Set

\[
E_0=M/10000=199{,}999{,}900.
\]

The uniform requirements are:

\[
P_e(\mathrm{accept})\ge19/20 \quad\text{for every } |e|\le E_0,
\]
\[
P_e(\mathrm{accept})\le1/100 \quad\text{for every } |e|\ge E_0+1.
\]

These are demands at adjacent finite populations, not the separated quality levels in Section 2. Private randomized decisions are allowed.

### 3.1 Labelled-pair coupling

For two fixed vectors differing at one specified entry, a uniformly selected set of \(s\) distinct queries sees that entry with probability \(s/M\). Full index-and-answer transcript laws therefore have total variation exactly \(s/M\). The necessary condition \(s/M\ge0.94\) follows.

That comparison allows the two probability laws to refer to one designated changed position. A single rule required to work uniformly over all possible arrangements faces a stronger problem.

### 3.2 Symmetrization and count sufficiency

Average any proposed audit rule over a uniformly random permutation of the population labels. For every fixed error count, the new acceptance probability is the average of the old rule's probabilities over arrangements of that count. Uniform guarantees are preserved.

Under the uniform prior over all arrangements with \(E\) errors, a fixed sample of \(s\) positions yields

\[
P_E(K=k)=\frac{\binom Ek\binom{M-E}{s-k}}{\binom Ms}.
\]

Conditional on the count \(K\), the queried indices and ordering of the observed bits have the same distribution for all error counts. They add no information for the adjacent-count comparison under those uniform priors. This is a minimax argument, not a prior assigned to nature: every uniformly successful rule must also succeed on these averages.

More generally, any adaptive rule choosing an unqueried index using only its previous answers and private randomness has, under the uniform-arrangement prior, conditional discrepancy probability \((E-k)/(M-t)\) after \(t\) queries and \(k\) discrepancies. Index selection cannot change the status law. A rule stopping after at most \(s\) queries can be padded to \(s\) distinct queries without losing information. Hence the same count experiment bounds every such adaptive rule with worst-case query cap \(s\). This is not a bound on expected stopping time.

### 3.3 Exact distance between adjacent count laws

For \(1\le s\le M\), let \(h(k)\) denote the mass function of \(\operatorname{Hypergeom}(M-1,E,s-1)\), extended by zero. Coupling the inclusion of the one additional marked position gives

\[
P_{E+1}(K=k)-P_E(K=k)=\frac{s}{M}[h(k-1)-h(k)].
\]

Hypergeometric masses are unimodal, so telescoping the absolute differences yields

\[
\boxed{\operatorname{TV}(P_E,P_{E+1})=\frac{s}{M}\max_k h(k).}
\]

This is no larger than \(s/M\), and can be much smaller. The proof above controls unrestricted sizes.

## 4. An exact minimum: all but 105 entries

Write \(r=M-s\) for the number of unqueried entries. Let \(U_E\) be the number of errors in that omitted set. Then

\[
P(U_E=u)=\frac{\binom Eu\binom{M-E}{r-u}}{\binom Mr},\qquad K=E-U_E.
\]

Working with \(r\) avoids evaluating enormous \(\binom Ms\) expressions with trillions of factors. At the two boundary populations, put

\[
g_r=P(U_{E_0}=0),\quad b_{r,0}=P(U_{E_0+1}=0),\quad b_{r,1}=P(U_{E_0+1}=1).
\]

The likelihood ratio of bad to good is increasing in \(K\). For \(K=E_0-u\) on the common support it equals

\[
\frac{P_{E_0+1}(K)}{P_{E_0}(K)}
=\frac{(E_0+1)(r-u)}{(M-E_0)(u+1)}.
\]

Thus accepting smaller counts first minimizes bad acceptance at a given good-acceptance constraint. This is the finite Neyman-Pearson ordering principle (Neyman and Pearson, 1933). It is also proved by exchanging acceptance mass from a lower good/bad likelihood ratio to a higher one.

At the relevant \(r\), accepting all \(K<E_0\) gives less than 95% good acceptance. The exact optimizing rule must additionally accept at \(K=E_0\) with probability

\[
\gamma_r=1-\frac{1}{20g_r}.
\]

Its minimum bad acceptance is

\[
B_r=1-b_{r,0}-b_{r,1}+\gamma_r b_{r,1}.
\]

The source reports the following exact rational evaluations (shown as decimals):

| Omitted \(r\) | Minimum bad acceptance at 95% boundary-good acceptance |
|---:|---:|
| 100 | 0.00945061135088093769... |
| 105 | 0.00992053452729221435... |
| 106 | 0.01001448946901366265... |
| 110 | 0.01039021029035270353... |

The source reports agreement between the closed expression and an exact likelihood-ratio optimization. Its boundary comparisons use rationals, rather than rounding or normal approximations; they are not recomputed in this excerpt.

At \(r=105\), a simpler rule suffices: accept if \(K<E_0\); accept with probability \(19/20\) if \(K=E_0\); otherwise reject. Its boundary probabilities are

\[
P_{E_0}(\mathrm{accept})=0.9505222793491606\ldots,
\]
\[
P_{E_0+1}(\mathrm{accept})=0.00992601900893398\ldots.
\]

For smaller true error counts, acceptance is at least this large; for larger error counts, acceptance is no larger. This follows by coupling nested populations and the monotonicity of the acceptance rule.

At \(r=106\), even the optimal randomized boundary rule has bad acceptance greater than 1%. Less inspection cannot improve the attainable testing region, since a larger sample can simulate a smaller sample by discarding observations.

Therefore

\[
\boxed{s_{\min}=M-105=1{,}999{,}998{,}999{,}895.}
\]

This is the exact minimum in the stated uniform fixed-size audit problem. It also is the minimum worst-case query cap for the adaptive class described above. It is not a minimum expected sample size, a statement about constrained error patterns, or a prohibition on calibration with a quality gap. No physical inspection of the full population was performed.

## 5. Reference and hypothesis boundaries

The deterministic reference bound is:

\[
d_H(z,t)\le d_H(z,r)+d_H(r,t).
\]

A small disagreement rate between a tested readout and a reference bounds true error only after the reference's own error has been warranted. The common-coarsening example has zero implementation disagreement while both true pair-error probabilities equal \(23/324\). All-size consistency of the recorded equality partitions does not distinguish that common error from truth.

The strengthened audit optimum concerns this audit-only observation experiment. An independently validated structural model, a more informative reference, or a different separation requirement changes the experiment and can change its sample requirements.

The proposed prephysical hypothesis is not either of the two paintboxes. Rejecting one source in the mathematical detector experiment therefore does not directly reject or confirm that hypothesis. Its unspecified internal-selection requirement remains unresolved. An observable response law chosen after inspecting desired observations cannot be counted as a derived prediction.

## 6. Controlled hidden lifts

Given a controlled visible transition law \(Q_a(z,z')\), define

\[
P_a((z,h),(z',h'))=Q_a(z,z')R_{a,z,z'}(h,h'),
\]

where each \(R\) is stochastic. Summing over \(h'\) recovers \(Q_a\) for every \(h\). Consequently every visible-history policy and every initial hidden distribution with the same visible marginal give the same visible process. Appending audits and reference outputs that are functions or common kernels of that same history cannot resolve the hidden coordinate.

This is an application of strong lumpability, not a new general reduction theorem. Theorem 3.1 of Wolfer and Watanabe (2024) supplies the relevant row-sum characterization. Such extensions need not be inert: hidden transitions can depend on visible moves and actions. Their physical existence is neither assumed nor proved.

One might attempt to remove this ambiguity by demanding the smallest hidden representation. The next example shows a distinct, narrower failure of that repair.

## 7. Strictly positive, minimal two-state realizations need not be unique

The comparison class now consists of **transition-emitting hidden Markov models**, also called Mealy HMMs. A nonnegative matrix \(T_y\) has entry \(T_y(i,j)=P(Y_t=y,S_{t+1}=j\mid S_t=i)\). The sum over outputs is row-stochastic. Starting from row distribution \(\pi\), a word has probability

\[
P(y_1\ldots y_n)=\pi T_{y_1}\cdots T_{y_n}\mathbf1.
\]

Outputs are emitted on transitions; the output and next latent state need not be conditionally independent given the current state. This is broader than a state-emitting HMM. Its simulation index is not a derived physical clock.

Consider

\[
T_0=\frac1{20}\begin{pmatrix}6&2\\1&3\end{pmatrix},\quad
T_1=\frac1{20}\begin{pmatrix}4&8\\7&9\end{pmatrix},\quad
\pi=(4/9,5/9).
\]

Every entry is positive, and \(\pi\) is stationary for \(T=T_0+T_1\).

Set

\[
S=\begin{pmatrix}9/10&1/10\\1/5&4/5\end{pmatrix},
\quad \widetilde T_y=S^{-1}T_yS,
\quad \widetilde\pi=\pi S.
\]

Then

\[
\widetilde T_0=\frac1{1400}\begin{pmatrix}449&151\\19&181\end{pmatrix},
\]
\[
\widetilde T_1=\frac1{280}\begin{pmatrix}67&93\\125&115\end{pmatrix},
\qquad \widetilde\pi=(23/45,22/45).
\]

These entries are also strictly positive, the total transition matrix is row-stochastic, and the new initial distribution is stationary. Because \(S\mathbf1=\mathbf1\), telescoping proves for every finite word

\[
\widetilde\pi\widetilde T_{y_1}\cdots\widetilde T_{y_n}\mathbf1
=\pi T_{y_1}\cdots T_{y_n}\mathbf1.
\]

The complete finite output laws coincide by the displayed all-word identity.

### 7.1 Both models are minimal

Their common two-output block matrix is

\[
H=\begin{pmatrix}9/100&179/900\\179/900&461/900\end{pmatrix},
\qquad \det H=53/8100>0.
\]

A one-latent-state transition-emitting HMM has iid outputs, so its two-output block matrix has rank one. Both present models have two states and rank-two block data. Each is therefore minimal in the declared class.

### 7.2 They are not state relabelings

Their total transition matrices are

\[
T=\begin{pmatrix}1/2&1/2\\2/5&3/5\end{pmatrix},\qquad
\widetilde T=\begin{pmatrix}14/25&11/25\\23/50&27/50\end{pmatrix}.
\]

The diagonal multisets differ, so no hidden-state permutation relates them. The stationary distributions also differ beyond permutation. Even the sum of their squared stationary probabilities differs by \(4/675\).

The mechanism is established realization theory, not a new discovery of HMM nonuniqueness. Theorem 2 of Vanluyten, De Cock, Willems and De Moor (*Equivalence of State Representations for Hidden Markov Models*) gives sufficient positivity-preserving similarity conditions, while their treatment explicitly distinguishes Mealy from Moore realizations. The rational example above is a separately constructed application.

### 7.3 What additional preparation access would change

Under arbitrary hidden-state preparations, the first model's attainable one-step zero-output probabilities span \([1/5,2/5]\). The second model spans \([1/7,3/7]\). Therefore the equivalence does not extend to unrestricted, physically aligned latent preparation controls.

The hidden-lift result holds for every hidden start with a fixed visible marginal. The present minimal-realization result instead fixes stationary preparations. These quantifiers are not interchangeable.

Minimality, strict positivity, stationarity, and complete passive output laws thus do not guarantee uniqueness up to state relabeling **in the transition-emitting class**. This does not invalidate identifiability theorems for more restricted state-emitting families. It also does not prove that the two representations are physically distinct: a theory might explicitly identify them under an admissible representation change. What the data fail to select is a unique interpretation of the latent categories without further structure.


## Mathematical sources identified in the original note


- W. Hoeffding, *Probability Inequalities for Sums of Bounded Random Variables*, Journal of the American Statistical Association 58 (1963), 13–30, Theorem 4. General finite-population convex-order background, not the exact numerical audit optimum.

- J. Neyman and E. S. Pearson, *On the Problem of the Most Efficient Tests of Statistical Hypotheses*, Philosophical Transactions of the Royal Society A 231 (1933), 289–337. The likelihood-ratio ordering is also justified directly above.

- G. Wolfer and S. Watanabe, *Geometric Aspects of Data-Processing of Markov Chains*, Transactions of Mathematics and Its Applications 8 (2024), tnae001; Theorem 3.1. https://arxiv.org/abs/2203.04575 . Strong-lumpability background.

- B. Vanluyten, K. De Cock, J. C. Willems and B. De Moor, *Equivalence of State Representations for Hidden Markov Models*, technical report 06-157, Theorem 2. Primary background for positive similarity-equivalent Mealy models; the rational example above is not attributed to that report.
