# Spin fluctuation and microscopic ambiguity

## I. Standard spin-fluctuation contraction: exact finite-size identities

For each positive integer `N` let the microscopic algebra be `M_2(C)^{⊗N}` with conventional Pauli matrices. Choose the **declared physical spin product state**

\[
\rho_{m,N}=\rho_m^{\otimes N},\qquad \rho_m=(I+m\sigma_z)/2,\quad 0<m\le1.
\]

Define collective, centered transverse fluctuations

\[
Q_N=(2mN)^{-1/2}\sum_{j=1}^{N}\sigma_x^{(j)},\qquad
P_N=(2mN)^{-1/2}\sum_{j=1}^{N}\sigma_y^{(j)}.
\]

Then precisely, **at every finite N**,

\[
[Q_N,P_N]=\frac{i}{mN}\sum_{j=1}^N\sigma_z^{(j)},\qquad
\langle[Q_N,P_N]\rangle=i.
\]

Because independent `sigma_z` variables have variance `1-m²` in the product state,

\[
\left\langle([Q_N,P_N]-iI)^\dagger([Q_N,P_N]-iI)\right\rangle
=\frac{1-m^2}{Nm^2}.
\]

**Convergence qualification:** this is mean-square convergence *relative to the chosen sequence of states*, not operator-norm convergence. In fact
`||[Q_N,P_N]-iI|| = 1+1/m` for every `N` (the all-down eigenvector realizes the maximum), so the operator-norm claim is false even for `m=1`.

For real `u,v` let `a=u/sqrt(2mN)`, `b=v/sqrt(2mN)`. Different sites commute and the single-site spin expectation is obtained by multiplying the two Pauli exponentials. Thus the **exact** finite-N ordered characteristic function is

\[
C_N(u,v)=\langle e^{iuQ_N}e^{ivP_N}\rangle
=\left(\cos a\cos b-im\sin a\sin b\right)^N.
\]

For every fixed `m>0`, `u,v`, taking the logarithm and using the uniform small-angle expansion gives

\[
\lim_{N\to\infty}C_N(u,v)
=\exp\left[-\frac{u^2+v^2}{4m}-\frac{iuv}{2}\right].
\]

The reversed product has the opposite imaginary Weyl phase. More generally, the analogous single-site expansion for any **finite word** in transverse Weyl exponentials yields the standard Gaussian Weyl algebra, with limiting `[Q,P]=iI` in the regular quasi-free fluctuation representation. This reproduces known quantum central-limit results; it is not a new theorem. Its limiting covariance is `V=(1/(2m)) I_2`, with symplectic matrix `Omega=[[0,1],[-1,0]]`, and `V+iOmega/2 >=0` because `0<m<=1`. The corresponding effective oscillator thermal occupancy is `nbar=(1-m)/(2m)`. This does not mean the original spins were thermal harmonic oscillators.

**Numerical controls.** The accompanying fluctuation calculation builds full `2^N × 2^N` tensor-product spin matrices for `N=2,3,4,6`; their traces of the ordered exponential products agree with the factorized exact formula to `<2e-13`. High-precision direct formula checks at `N=2,4,16,64,256,1024,4096` approach the displayed limit. For `m=.8,u=v=.7`, the limit is approximately `0.7142175684315161 -0.17857058381200364 i` and the absolute errors are `0.0024151` at `N=16`, `0.00014976` at `N=256`, and `9.36e-6` at `N=4096`. No numerical evidence is being used as a substitute for the elementary limit proof.

### The unpolarized/tracial negative control

At `m=0`, the preceding `Q_N,P_N` scaling is undefined. The appropriate unrescaled-variance fluctuations are `F_x=N^-1/2 sum sigma_x`, `F_y=N^-1/2 sum sigma_y` in the maximally mixed state `rho_0=I/2`. They obey

\[
\langle e^{iuF_x}e^{ivF_y}\rangle
=\left[\cos(u/\sqrt N)\cos(v/\sqrt N)\right]^N
\longrightarrow e^{-(u^2+v^2)/2},
\]

and `E([F_x,F_y])=0`, `E([F_x,F_y]†[F_x,F_y])=4/N`. The limit is the characteristic function of **two commuting, independent classical Gaussians**, even though the microscopic operators do not commute. This is a statement about this specific Gaussian fluctuation sector, not a no-go for quantum behavior in all unpolarized systems or other scaling limits.

For a state sequence with `m_N→0`, the normalized CCR commutator variance is `(1-m_N²)/(N m_N²)`, so it is **not** uniform in polarization. Its decay would require `N m_N²→∞`, and the oscillator covariance `1/(2m_N)` diverges regardless. One cannot extrapolate the fixed-`m` regular oscillator limit all the way to `m=0` using the same normalization.

## II. Exact microscopic non-identification under complete collective controls

Compare two distinct microscopic systems initialized in their maximally polarized product states:

* Model A: `n` spin-1 sites, full space dimension `3^n`.
* Model B: `2n` spin-1/2 sites, full space dimension `2^(2n)`.

The initial state in both models is the highest-weight state of **total spin `J=n`**. Under the total-spin generators `J_x,J_y,J_z`, both cyclic subspaces carry the unique spin-`J=n` irreducible representation, of dimension `2n+1`. The SU(2) raising/lowering relations on a highest-weight vector uniquely determine all matrix elements within this irrep:

\[
J_\pm|J,M\rangle=\sqrt{(J\mp M)(J\pm M+1)}\,|J,M\pm1\rangle.
\]

Therefore an intertwining unitary between these *cyclic irreducible subspaces* maps the initial vectors and every polynomial and bounded functional calculus of the **collective** `J_a` to each other. All corresponding collective preparations, collective gates (including nonlinear functions such as `J_z²`), and collective effects give **exactly equal outcome probabilities**, not merely asymptotically equal ones. This is familiar angular-momentum representation theory, not publication novelty.

For `n=3`, the complete microscopic Hilbert spaces have dimensions `27` versus `64`, but all collective experiments restricted to the common seven-dimensional `J=3` irrep agree. A full-matrix implementation checks noncommuting rotation sequences and nonlinear collective evolution for `n=1,2,3`; discrepancies are below `1e-15`.

**Scope of equivalence:** no claim of equality of full observable algebras. A physically calibrated site-resolved intervention, or operations accessing another total-spin sector, can distinguish the models. The comparison demonstrates that knowing the collective bosonic limit, and even far more than that limit, does not identify microscopic constituent number/type without an adequate observation toolbox.

## III. Ricker-filtered emergent bosons do not select geometry

This section deliberately reconnects to the program's *negative controls* only; it does not use a wavelet as a particle ontology. Supply a connected graph with real symmetric positive Laplacian `L`, and define the mathematical scale-response operator

\[
W_s=s L e^{-sL},\quad s>0.
\]

Place `N` independent spins at **each already identified graph vertex** and take the `N→∞` polarized fluctuation limit at fixed `m>0`. It yields an independent canonical pair `Q_i,P_i` at every *assumed* vertex. The filtered fields `Q_s=W_s Q`, `P_t=W_t P` satisfy

\[
[Q_s(i),P_t(j)] = i(W_sW_t)_{ij}
\]

in the limit. The full 4-site spin matrix calculation verifies the same relation for the **finite-N commutator expectation** without invoking the limit. The scale labels remain redundant/noncanonical; the exact Laplacian zero mode is removed.

An aggregate, mode-blind multiscale commutator measures only

\[
\mathcal A(s,t)=\frac1{V}\frac1i\sum_i\langle [Q_s(i),P_t(i)]\rangle
=\frac1V\operatorname{Tr}(W_sW_t),
\]

which depends on the eigenvalues of the supplied `L` alone. In the previous exact graph test, the nonisomorphic 16-vertex rook and Shrikhande graphs have identical Laplacian spectra `0^(1),4^(6),8^(9)`. Both therefore yield

\[
\boxed{\mathcal A(s,t)=st\,[6e^{-4(s+t)}+36e^{-8(s+t)}]}
\]

**for every pair of mathematical scales**, despite different labeled connectivity. At `s=.12,t=.31`, both values are `0.0829085908049164`, with spectral-formula residual `<5e-17`. The full labeled filtered commutator kernels differ in Frobenius norm by `0.0604811368` under the exhibited fixed vertex labeling.

The latter distinction is physically actionable **only if that vertex identification and spatial measurement protocol have independent meaning**. There is no emergent local measurement basis or spatial metric from CCR or the aggregate wavelet result. Thus bosonic algebra plus multi-scale spectral data does not resolve the already identified inverse-geometry ambiguity. This is a synthesis of known quantum-fluctuation and cospectral-graph phenomena, not a novel theorem.

## IV. Microscopic dynamics is a separate ingredient, and bosons do not imply Lorentz invariance

As a controlled physical *example*, supply a one-dimensional periodic spin-1/2 chain with independently calibrated hopping `J>0`, on-site energy `Delta=2J+mu` and an independently specified physical evolution parameter:

\[
H=\Delta\sum_j n_j-J\sum_j(\sigma^-_j\sigma^+_{j+1}+\sigma^+_j\sigma^-_{j+1}),\quad
n_j=(I-\sigma_z^{(j)})/2.
\]

In the **single-down-spin excitation sector**, the exact restricted Hamiltonian is `Delta I-J A_cycle`, giving

\[
E(k)=\mu+2J[1-\cos(ka)]=\mu+Ja^2k^2+O(k^4a^4).
\]

For `J=.75,mu=.2` on a six-site ring, the independent full `2^6` spin matrix has one-excitation energies `[.2,.95,.95,2.45,2.45,3.2]`, matching the formula to `<9e-16`. At `mu=0`, the one-particle band touches zero with **quadratic** long-wavelength dispersion (`z=2`), not the `z=1` linear spectrum of a relativistic massless scalar. Calling this toy band's touching point a Goldstone boson would require a separate symmetry-breaking argument; none is asserted for the tuned XY model.

In actual symmetry-broken nonrelativistic many-body theories, Watanabe and Murayama (2012, 2014) show that pairs of broken generators with nonzero commutator expectation can describe a single low-energy mode, often with nonrelativistic dispersion. This is structurally suggestive of the same spin commutator mechanism, but **our product-state central limit is not by itself a spontaneous-symmetry-breaking theorem**.

Ricker filtering `W_s` on such an already-defined spatial generator only reweights wave numbers; it neither changes `E(k)` nor supplies the physical space, time, sources or causality needed for a field theory.
