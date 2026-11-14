# Six radial BAO distances and the G1 expansion benchmark

**Kirtus Justus**, Theoretical Physicist, Port Coquitlam, British Columbia, Canada. Retrospective observational check by Director G (OpenAI Codex).

The six radial distances in the DESI DR2 all-tracer baryon acoustic oscillation (BAO) likelihood fit the flat dust-plus-vacuum expansion curve with $\chi^2=3.8115$ for six measurements and two fitted parameters. The largest residual is $+1.32$ marginal standard deviations at $z=0.934$. The dataset was public when Edge Record Walk G1 proposed its cosmology benchmark. G1 stipulated a fresh held-out rejection criterion. This fit supplies a check on its imported expansion history, with no change to the candidate's disposition. [G1 benchmark at the reviewed commit](https://github.com/KirtusJ/From-Prephysical-Hypotheses-to-Physical-Models/blob/09ac880bc51783a8ed04c35a7ab946891d958e7d/Director_G/candidates/edge_record_walk/cosmology.md) · [DESI DR2 Results II, Table IV](https://arxiv.org/html/2503.14738v2#S3.T4)

## The measurements and their likelihood

Radial BAO measures $y=D_H/r_d=c/(H(z)r_d)$ using the common comoving sound horizon at the baryon drag epoch, $r_d$. Use the published compressed Gaussian likelihood in the original $y$ coordinates. The all-tracer mean file has thirteen rows. Selecting every row labeled DH_over_rs gives zero-based indices $2,4,6,8,10,11$. The order of radial and transverse entries reverses for the Lyα forest. The bright galaxy sample at $z=0.295$ has an isotropic distance only. The separately reported LRG3 and ELG1 results at $z=0.922,0.955$ use overlapping data and are superseded in the joint likelihood by LRG3+ELG1 at $z=0.934$. All six radial bins of that likelihood enter. [Official DESI release](https://www.desi.lbl.gov/2025/10/06/desi-dr2-cosmology-chains-and-data-products-released/) · [DESI explanation of the overlapping tracer bins](https://arxiv.org/html/2503.14738v2#S3.T4)

For a joint Gaussian with covariance $C$, marginalizing the omitted observables gives covariance $C_{RR}$ at the retained rows and columns. In this release $C_{RR}$ is diagonal. The full joint covariance contains radial–transverse correlations, so taking the radial block of the *precision* and inverting it would instead give conditional standard deviations, smaller in every bin. The table below uses the actual likelihood files. Some uncertainties differ from the rounded posterior summaries in the paper. The DESI release contact confirmed that the mean and covariance distributed with Cobaya are byte-identical to the inputs used for the public chains. [DESI confirmation](https://help.desi.lbl.gov/index.php?qa=182&qa_1=provenance-external-cobaya-likelihood-public-cosmology-chains) · [Pinned likelihood inputs](https://github.com/CobayaSampler/bao_data/tree/b7b8a36e9bccb063081f811f323cada21ab5fbdd/desi_bao_dr2)

## A fit with one nuisance scale

For flat general relativity with independently conserved pressureless matter, constant positive vacuum density and negligible radiation, put $X=(1+z)^3-1$. G1's prediction in the measured observable is
$$ y(z)=\frac{S}{\sqrt{1+\Omega_m X}}=\frac{1}{\sqrt{A+B X}},\qquad
S=\frac{c}{H_0r_d}>0,\quad A=S^{-2},\quad B=A\Omega_m,\quad 0<B<A. $$
This fit assigns Gaussian errors to the observed distance. Squaring noisy reciprocal distances would change their distribution. The overall scale absorbs the common unknown ruler. These data do not separately determine $r_d$ or $H_0$.

For each matter fraction let $f_i=(1+\Omega_m X_i)^{-1/2}$. The profiled scale is $S=\max(0,f^\top C_{RR}^{-1}y/(f^\top C_{RR}^{-1}f))$. Minimize $(y-Sf)^\top C_{RR}^{-1}(y-Sf)$ over the physical shape. The checker scans the closed limiting interval and refines its grid minima and compares the endpoints. It obtains $\Omega_m=0.269970$, $S=28.46306$, $A=0.00123435$ and $B=0.000333236$. The pure-vacuum and matter-only limits give $\chi^2=3018.82$ and $184.64$ after fitting their scales. The table defines residual as observed minus fitted. Standardized residuals use the released marginal standard deviations.

| Tracer | $z$ | Observed $D_H/r_d$ | Marginal SD | Fitted | Residual | Residual / SD |
|---|---:|---:|---:|---:|---:|---:|
| LRG1 | 0.510 | 21.86295 | 0.42887 | 22.09480 | −0.23185 | −0.541 |
| LRG2 | 0.706 | 19.45535 | 0.33387 | 19.78088 | −0.32553 | −0.975 |
| LRG3+ELG1 | 0.934 | 17.64149 | 0.20104 | 17.37702 | +0.26447 | +1.316 |
| ELG2 | 1.321 | 14.17602 | 0.22455 | 14.04740 | +0.12862 | +0.573 |
| QSO | 1.484 | 12.81700 | 0.51801 | 12.90072 | −0.08372 | −0.162 |
| Lyα | 2.330 | 8.63155 | 0.10106 | 8.70184 | −0.07030 | −0.696 |

The usual asymptotic $\chi^2_4$ reference gives upper-tail probability $0.4321$. Six points and a nonlinear shape fit give no exact $\chi^2_4$ calibration. Its interpretation assumes the released Gaussian compression and covariance, a common ruler, and the two-parameter background family. A different expansion history can reproduce these six distances. The walk presently provides no map from its microscopic records to the three-dimensional metric, measured redshifts, ruler or expansion rate. The published DESI fits using transverse BAO, the CMB or supernovae address other likelihoods. [G1 physical assumptions and prospective test](https://github.com/KirtusJ/From-Prephysical-Hypotheses-to-Physical-Models/blob/09ac880bc51783a8ed04c35a7ab946891d958e7d/Director_G/candidates/edge_record_walk/cosmology.md) · [DESI measurement and inference](https://arxiv.org/abs/2503.14738)

## Sensitivity to the late-time radiation approximation

Add $\Omega_r[(1+z)^4-1]$ inside the square root, imposing $\Omega_m+\Omega_r<1$ and refitting $S,\Omega_m$ at each fixed radiation fraction. The values below are sensitivity settings, with no prior on $\Omega_r$ inferred from the radial data. The last two columns give the largest absolute change in the *predicted radial distances* over the six bins, divided by each bin's marginal SD. One holds the primary best-fit parameters fixed and the other refits them.

| Fixed $\Omega_r$ | Fitted $\Omega_m$ | $S$ | $\chi^2$ | Largest shift at fixed parameters / SD | Largest shift after refit / SD |
|---:|---:|---:|---:|---:|---:|
| 0 | 0.269970 | 28.46306 | 3.81151 | 0 | 0 |
| 0.00005 | 0.269714 | 28.45850 | 3.80166 | 0.02453 | 0.00182 |
| 0.00010 | 0.269459 | 28.45395 | 3.79182 | 0.04904 | 0.00364 |
| 0.00020 | 0.268948 | 28.44484 | 3.77218 | 0.09799 | 0.00728 |

These figures quantify the approximation at the six late effective redshifts and the stated radiation fractions. The extra component scales strictly as $a^{-4}$. Extrapolation to the early Universe, massive-neutrino evolution, sound-horizon physics, peculiar-velocity systematics and additional full-survey likelihood choices require additional modeling. The numerical fit supplies no microscopic mechanism for vacuum or matter.

## Reproduction

Run the following once per new output path with Python and NumPy. The released 472-byte means file and 2,547-byte covariance file are included for offline replay. Their SHA-256 digests are respectively 9ac154ab583ce759c0f7eef3c978c7c70a6ead2d18774caceadf1a350a640585 and 252a143274c8a07c78694c119617d36594f6d7965d00319ca611c6ffb886e509. The checker verifies these bytes, exact row selection, positive-definite covariance, the distinction from conditioning, synthetic noiseless recovery for vacuum, a mixed interior and pure dust, and distance-unit rescaling. Its output retains all residuals for every radiation setting. [Mean vector](results/desi_dr2_radial_source/desi_gaussian_bao_ALL_GCcomb_mean.txt) · [Covariance](results/desi_dr2_radial_source/desi_gaussian_bao_ALL_GCcomb_cov.txt) · [Checker](check_desi_dr2_radial.py) · [Numerical results](results/desi_dr2_radial.json)

~~~console
python -B Director_G/check_desi_dr2_radial.py output.json
~~~
