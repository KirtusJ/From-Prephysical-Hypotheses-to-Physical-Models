# A cosmological benchmark for the edge-record walk

**Kirtus Justus**, Theoretical Physicist, Port Coquitlam, British Columbia, Canada. Research supplement by Director G (OpenAI Codex).

**Status.** The walk gives signed records on a one-dimensional lattice. A cosmological interpretation still needs a map from those records to three spatial dimensions, proper time, a metric, measured photon frequencies, gravitating matter and their physical units. The following benchmark imports those ingredients. Its observational success or failure tests the imported physical model. Deriving them from the walk is an open obligation.

## Added physical hypothesis

Assume general relativity in \(3+1\) dimensions and an expanding, homogeneous, isotropic, spatially flat FLRW background. Normalize the scale factor to \(a_0=1\). At late times take the source to be independently conserved pressureless matter (baryons and collisionless cold dark matter in the homogeneous average) and constant positive vacuum density, with \(0<\Omega_m<1\). Treat photons in geometric optics as null geodesics and assume comoving sources and observers after peculiar-velocity corrections. Then \(1+z=1/a\). Photons used as tracers still propagate when the radiation contribution to the background expansion is neglected. The chosen redshift interval and precision must justify neglecting radiation and pressure.

Write \(H=\dot a/a\), \(E(z)=H(z)/H_0\), and \(X=(1+z)^3\). Conservation gives \(\rho_m=\rho_{m0}X\), and the flat Friedmann equation gives \(E^2=1+\Omega_m(X-1)\). Thus all pairs of redshifts with \(z_i\ne z_j\) have the same dimensionless slope

\[
K_{ij}=\frac{E^2(z_i)-E^2(z_j)}{X_i-X_j}=\Omega_m .
\]

This is the two-redshift form of the \(Om\) diagnostic. With three distinct redshifts, the prediction \(K_{12}-K_{23}=0\) tests the expansion shape. A common \(H_0\) cancels from the zero test when using \(H^2\); obtaining the numerical dimensionless slope still needs \(H_0\). A zero is compatible with other models that share this expansion history. When radiation matters the added term is \(\Omega_r[(1+z)^4-1]\), which changes the slope even under a constant vacuum term. [Sahni, Shafieloo and Starobinsky](https://doi.org/10.1103/PhysRevD.78.103502)

## Held-out attack and existing observations

For a prospective attack, freeze the redshift interval, bins, radiation treatment, estimator, covariance, nuisance calibrations and rejection criterion before examining fresh expansion data. Two bins fix the line in \(H^2\) against \(X\); a held-out third bin predicts a residual with its full covariance, including correlations with the first two. Radial baryon acoustic oscillations measure \(D_H/r_d=c/[H(z)r_d]\). An unknown common sound horizon \(r_d\) cancels from the collinearity test when inverse distances are used consistently. Fit the measured distances with their reported likelihood to avoid bias from squaring noisy reciprocals. Supernovae provide relative luminosity distances, which require a distance model or reconstruction to constrain \(H(z)\). A reproducible held-out rejection within the specified approximations would refute the added cosmological commitment and retire G1 v1.0. No held-out test has been run here. [DESI DR2 measurements and likelihood](https://arxiv.org/abs/2503.14738)

DESI DR2 reported a good fit of flat \(\Lambda\)CDM to its BAO measurements alone. When the collaboration included CMB and supernova data, its comparison with a time-dependent equation of state favored the latter at \(2.8\)–\(4.2\sigma\), depending on the supernova sample. The 2026 DES multiprobe analysis reported \(2.3\sigma\) for its low-redshift combination with DESI BAO. These published fits use different data combinations and inference procedures from the proposed held-out diagnostic. [DESI DR2](https://arxiv.org/abs/2503.14738) · [DES multiprobe analysis](https://arxiv.org/abs/2605.27221)

## Coverage and open obligations

| Question | What this benchmark commits to |
|---|---|
| Dark energy and dark matter | Vacuum has constant density and pressure \(p_\Lambda=-\rho_\Lambda c^2\) for mass-density units. Cold dark matter contributes to the conserved dust. The microscopic origin and magnitudes of both components, and a particle or field corresponding to the dark matter, remain open. Expansion measures the combined matter density. |
| Inflation, initial singularity and baryogenesis | The late-time approximation has no validated early-time continuation. Inflation, generation of primordial fluctuations, the physical status of an initial singularity and the origin of the baryon asymmetry each require additional dynamics and observables. |
| Perturbations and structure | The background supplies \(H(z)\). Growth, lensing, and CMB spectra require perturbation dynamics, primordial statistics and matter transfer functions. DES Y6 obtained \(S_8=0.789\pm0.012\) in flat \(\Lambda\)CDM and found a \(2.6\sigma\) difference along \(S_8\), versus \(1.8\sigma\) across the full parameter space, from its specified CMB comparison. The walk supplies no prediction for that amplitude. [DES Y6 clustering and lensing](https://arxiv.org/abs/2601.14559) |
| Hubble tension | \(H_0\) is an input scale. Planck inferred \(67.4\pm0.5\) km/s/Mpc under its base cosmology; the 2022 SH0ES distance ladder reported \(73.04\pm1.04\) km/s/Mpc. Reconciling early- and late-time calibrations requires an independent ruler or luminosity calibration and its systematics. The slope null alone cannot determine \(H_0\). [Planck](https://arxiv.org/abs/1807.06209) · [SH0ES](https://arxiv.org/abs/2112.04510) |
| Future expansion | If the positive constant vacuum term persists indefinitely on the expanding branch, \(H\to H_0\sqrt{1-\Omega_m}\) as \(a\to\infty\), giving asymptotically de Sitter expansion. Vacuum evolution or decay would require a new dynamical assumption. The walk determines neither the persistence of the vacuum nor the fate of the observed Universe. |
