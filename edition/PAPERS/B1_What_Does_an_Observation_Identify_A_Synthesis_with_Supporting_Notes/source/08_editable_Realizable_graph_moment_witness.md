# Realizable graph moment witness

## 1. A graph witness with fixed inverse moments

Let the test input be `u=(e0-e1)/sqrt(2)`. On the 16-vertex rook graph, its positive-Laplacian spectral measure consists of weights `1/4` at `lambda=4` and `3/4` at `lambda=8`, hence transformed inverse-eigenvalue moments

`m0=1, m1=5/32, m2=7/256, m3=11/2048, m4=19/16384`.

Construct a connected four-vertex complete weighted graph with fixed weights `w01=w03=w23=1/50`, and unknown `(w02,w12,w13)`. With `S=[e0-e3,e1-e3,e2-e3]`, `B=(S^T S)^{-1}S^T L S`, `G=S^TS`, `h=(1,-1,0)^T`, and `d=det B`, define three integer/rational polynomial equations

`P_j=0.5 h^T G adj(B)^j h - m_j^(rook) d^j=0`, `j=1,2,3`.

Use the full exact rational centre recorded with the certificate and the radius $r=10^{-34}$. Let $C$ be the inverse Jacobian at that centre. Exact rational polynomial-coefficient bounds for the Hessians on this box give a contraction factor $q$ and centre displacement $\rho$ satisfying $0\le q<1$ and $\rho+qr<r$. Their displayed numerical values are approximately $q=4.479010085739296\times10^{-27}$ and $\rho=3.689057310400891\times10^{-63}$; the proof uses the exact inequalities, not those rounded renderings. Banach's fixed-point theorem therefore gives a unique root in the box. Exact characteristic-polynomial sign changes at the rational centre locate its three positive eigenvalues in $(0.084,0.086)$, $(5.58,5.59)$, and $(33.81,33.82)$. Perturbing the three conductances by at most $r$ changes the Laplacian operator norm by at most $6r$, so the root has spectral gap greater than $0.08$. A direct polynomial numerator-and-determinant derivative bound, with a strictly positive determinant lower bound on the box, proves exactly $0.006804564875115<m_4<0.006804564875116$.

The computed root is approximately:

\[
\begin{pmatrix}
15.6899984582831346064112477306\\
3.9688719037812073827601821080\\
0.0235628563734151668852330800
\end{pmatrix}.
\]

Its positive eigenvalues are approximately `(0.084748449338,5.585135434187,33.814982553350)`, with pair weights `(3.060828e-7,0.84746316616,0.15253652775)`. The slow mode dominates m4 despite tiny weight: its m4 contribution is approximately `0.005933513`.

**Sixteen-site lift.** Add 12 new vertices; reduce every old four-site edge weight by `3epsilon` with `epsilon=3/500`, connect every old vertex to every new vertex with weight `epsilon`, and connect all new pairs with weight `1/100`. Every edge stays positive (the smallest old adjusted weight is `0.002`). The cross block annihilates original four-site zero-sum vectors. On those vectors, the old-site block agrees with the original L. Hence the selected pair's entire spectral measure is preserved. The additional eigenvalues are `16epsilon=0.096` (one copy) and `0.12+4epsilon=0.144` (eleven copies), so the original low eigenvalue remains the 16-graph spectral gap. Both candidate graphs have 16 vertices, matching m0..m3 for the one specified pair but differing at m4.

This is **exact conditional nonidentifiability** from four transformed moments of one pair, not complete-data indistinguishability, a new physical law, or a first-in-literature claim.

## 2. A threshold measurement for the graph witness

Let `g_lambda(s)=4lambda^2 s exp(-2lambda s)` be the calibrated scale density for a positive eigenmode. Rook-edge density:

`p_R(s)=(1/4)g_4(s)+(3/4)g_8(s)`.

Alternative density:

`p_A(s)=sum_{j=1}^3 w_j g_(lambda_j)(s)` with the certified eigenvalue and weight intervals.

Numerical evaluation of the full distributions gives numerical total-variation distance `0.104957402798` (four detected density crossings) and Bhattacharyya coefficient `0.990246324123`. These latter integrals are high-accuracy numerical calculations, not outward-certified integral bounds.

A separate **fully certified** binary experiment requires much less: record the bit `Y=1{s>3/100}`. The exact rational graph eigenvalue/weight enclosures together with rational Taylor bounds for exponentials prove

`P_R(Y=1)>930704/1000000`, `P_A(Y=1)<870032/1000000`.

For `p>q`, the binary Bhattacharyya coefficient `sqrt(pq)+sqrt((1-p)(1-q))` is maximized by reducing p and increasing q. Exact rational square comparisons then show `B<994759/1000000`. Tensorization and the classical Bhattacharyya bound give

`P_e(M) <= (1/2) B^M < (1/2)(994759/1000000)^307 < 1/10`.

Thus **307 independent photon trials suffice for <=10% equal-prior Bayes error** under this exact scale-threshold measurement contract, for this graph pair, with no detector loss and calibrated known source. This is a conservative sufficient guarantee, not the minimum and not a general physical resource bound.

The submitted `57,291,466` Cantelli guarantee concerns **a different** three-atom positive-measure witness *and* the fourth-moment estimator. Comparing those trial counts as if they were the same alternative/model/estimator would be invalid.

This illustrates a central lesson: matching several moments does not imply closeness of complete distributions. The tiny slow-mode spectral weight makes m4 sensitive to rare long-scale outcomes, while much larger spectral-weight rearrangements cause readily testable differences at short scales.

## 3. Statistical threshold calculations

The simple equal-phase and antisymmetric rook-edge/nonedge scale densities give the following tests:

- For a single identically repeated upper-threshold bit, equal-phase pair: `M=165`, `t=0.22943`, risk `0.099786766829`, whereas the numerically optimized `M=164` risk is ~`0.10046967`.
- Antisymmetric pair: `M=173`, `t=0.23077`, risk `0.099493720411`; numeric optimized `M=172` risk ~`0.10017110`.
- The source's **exact rational sweep certificates** exclude every upper threshold at M=164 and M=172, respectively. The threshold distributions were checked numerically. The claimed global minimum rests on the supplied exact interval-sweep certificate; numerical agreement alone is insufficient.
- Fourier-likelihood inversion reproduces `M=116:0.10022951`, `M=117:0.09926536` for equal phase, and `M=126:0.10028047`, `M=127:0.09939238` for antisymmetric. These full-distribution crossings are **numerical**.
- For the antisymmetric sample-mean Chernoff statistic at threshold `0.1711`, the prescribed positive and negative exponential tilts give `0.0998551584` and `0.0998533841` at M=375. The source supplies stronger rational exponential enclosures; The reported floating values agree with those enclosures.

## 4. Quantum information, phase access and calibration rank

For `a_lambda(s)=2lambda sqrt(s) e^(-lambda s)` in `L^2(ds)`, the pure-state quantum Fisher information for `lambda` equals `2/lambda^2`; classical measurement of s achieves the same FI. Multiplying the amplitude by a *parameter-dependent* phase `exp(i b lambda s)` preserves all scale probabilities but changes the QFI to `2(1+b^2)/lambda^2`. Thus coefficient two is **not** a universal quantum-physical ceiling. This agrees with Braunstein–Caves 1994. The phase dependence is an additional physical instrument assumption, not a free resource.

Maximizing the specified three-port real-amplitude local-FI objective along equal scales gives `0.8279358531658`. For the quoted equal-scale alias parameters, the ideal continuous-register overlap is `0.3429323662853`, one ideal pure photon has optimal error `0.0303199514`, and a coherent known-amplitude input requires mean energy `0.7774323335` to reach 10% error. These apply to distinct measurement contracts. The source report contains an analytic global-optimum proof of the three-port class; the numerical calculation checks its value and does not replace the analytic global-uniqueness proof.

On the rook and Shrikhande graphs, take `k=128L^+=24I+4A-3J`. The exact calculation constructs all 120 contrast-perturbation residual derivatives, collects 120 off-diagonal components per derivative, and eliminates the resulting **integer** `120 x 120` matrix modulo `1,000,003`. Both ranks equal **119**. Both matrices have zero column sums. This proves rank >=119 over rational numbers and rank <=119 from the exact column sum identity, hence **rational rank=119**. It supports the revised distinction between `d-1` constraints for common spectral functions and locally 119 directions for pair-specific contrast perturbations.

For the deterministic power-law readout $S^{\prime}=\kappa S^p$, the transformed inverse-moment relation persists under the stated common coherence contrasts; consequently a zero quadratic residual alone does not identify linear scale calibration. A classification of all measurable readout functions preserving that graph-moment relation requires a separate argument. The controlled density-ratio theorem in *Detector Transfer Ambiguity* instead addresses recovery of the dimensionless incident coordinate under one common standard-Borel subprobability response kernel, known control multipliers and per-preparation normalization. Its zero-conditional-variance criterion does not establish the power-law classification.
