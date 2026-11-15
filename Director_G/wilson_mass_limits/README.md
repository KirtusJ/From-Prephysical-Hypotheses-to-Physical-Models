# Wilson–Dirac interval entropy as mass and length vary

For the half-filled infinite Wilson–Dirac chain, compare the massive occupied-band state with the massless one on the same interval of $L$ consecutive two-orbital cells. Write $m=\mu/L$ for the bare mass, $D_L(\mu)$ for the massive-first relative entropy, and $h=\log(1/\mu)$. All logarithms are natural. At fixed positive $\mu$, the Z33 expansion has leading term $\mu^2\log L/6$. Taking $\mu$ to zero with $L$ gives different scales. [Model and entropy convention](https://github.com/KirtusJ/From-Prephysical-Hypotheses-to-Physical-Models/blob/0ca75f60c76af1be7f3c25c2ed8914e82243ff5d/edition/PAPERS/D1_Relative_Entropy_of_Finite_Interval_Wilson_Dirac_Quasifree_States/D1_Relative_Entropy_of_Finite_Interval_Wilson_Dirac_Quasifree_States.pdf#page=4) · [Fixed-positive-mass expansion](https://github.com/KirtusJ/From-Prephysical-Hypotheses-to-Physical-Models/blob/0ca75f60c76af1be7f3c25c2ed8914e82243ff5d/edition/PAPERS/D3_Finite_Part_of_Wilson_Dirac_Relative_Entropy/D3_Finite_Part_of_Wilson_Dirac_Relative_Entropy.pdf#page=2)

| Limit | Result for the specified chain |
|---|---|
| Fixed $L$, then $\mu\downarrow0$ | $D_L(\mu)=\kappa_L\mu^2 h^2+O_L(\mu^2h)$. At one cell $\kappa_1=1/(\pi^2-4)$. The coefficients satisfy $\kappa_L\to1/6$ as $L\to\infty$. [Finite coefficient and spectral proof](fixed.md) |
| Every simultaneous $L\to\infty$, $\mu\downarrow0$ | $\displaystyle\liminf D_L(\mu)/(\mu^2h^2)\ge1/6$. For example, $\mu=1/L$ makes the ratio to $\mu^2\log L/6$ diverge. At $\mu=\exp[-a\sqrt{\log L}]$ the same ratio has liminf at least $a^2$. [Joint lower bound](upper.md) |
| $h/[\sqrt L(1+\sqrt2)^{2L}]\to\infty$ | $D_L(\mu)\sim\mu^2 h^2/6$. The proof controls the contribution from reference occupations close to zero or one. [Upper bound and sufficient sector](upper.md) |
| $\mu\log L/\log^3(e/\mu)\to\infty$ with $\mu\downarrow0$ | $D_L(\mu)\sim\mu^2\log L/6$ on the finite modular and nonlinear estimates used in D4/D5. This includes $\mu=(\log L)^{-a}$ for $0<a<1$. The boundary estimate used here holds at finite $L$. [Finite entropy estimate and its inputs](window.md) |

At every integer $L\ge1$ and $0<\mu\le1$, one binary orbital measurement gives $D_L(\mu)\ge\mu^2h^2/(200\pi^2)$. As $\mu\downarrow0$, the lower coefficient $1/\pi^2$ holds uniformly over all lengths, including one cell. [Finite-length bounds and proof](orbital.md)

The matching upper bound for polynomially shrinking $\mu=L^{-b}$, $b>0$, and the transition between the two scales remain open. Casini and Huerta previously calculated the coefficient $-1/6$ of the small-mass double logarithm for continuum **entanglement entropy**. The finite-lattice conclusions above concern **relative entropy** and are derived from the Wilson covariance. Transferring the continuum expansion to the Z33 entropy-difference functional would require a comparison of regulators and control of the remainder. [Continuum comparison](continuum_entropy.md) · [Casini–Huerta, §4.2, Eq. (75)](https://arxiv.org/pdf/0903.5284v3#page=11)

## Reproduce the finite checks

Run these commands in this directory with Python 3 and `mpmath` 1.3.0 installed.

```sh
python3 -I -B fixed.py
python3 -I -B susceptibility.py
```

The first script evaluates the finite coefficient in both the scalar sine-kernel and original orbital bases, tests the one-cell identity, and computes massive nonlinear covariances for $L=1,2,3$ at $\mu=10^{-8},10^{-16},10^{-24}$. The second evaluates the finite trace Hessian directly at lengths through 24. Their common coefficient at $L=16$ is 0.1666829226370926. These are multiprecision numerical checks. The bounds and limits follow from the proofs. [First script](fixed.py) · [First output](fixed.txt) · [Second script](susceptibility.py) · [Second output](susceptibility.txt)

For the explicit finite-length constants, run `python3 -I -B orbital.py` with the standard library. Add `--quadrature` for the SciPy checks. [Orbital checker](orbital.py) · [Orbital output](orbital.txt)

The reference edition is Z33, commit `0ca75f60c76af1be7f3c25c2ed8914e82243ff5d`. Z33 D4 gives the modular and nonlinear estimates used for the slow-mass limit. D5 states the bounded-scaled-mass additive assembly. D8 specifies the restricted projectors, the trace path and its finite-size estimate. [D4, pp. 3–5](https://github.com/KirtusJ/From-Prephysical-Hypotheses-to-Physical-Models/blob/0ca75f60c76af1be7f3c25c2ed8914e82243ff5d/edition/PAPERS/D4_Uniform_Modular_Control_and_Nonlinear_Convergence_for_Wilson_Dirac_Int/D4_Uniform_Modular_Control_and_Nonlinear_Convergence_for_Wilson_Dirac_Int.pdf#page=3) · [D5, pp. 1–4](https://github.com/KirtusJ/From-Prephysical-Hypotheses-to-Physical-Models/blob/0ca75f60c76af1be7f3c25c2ed8914e82243ff5d/edition/PAPERS/D5_Conditional_Uniform_Additive_Limit_of_Wilson_Dirac_Relative_Entropy_on/D5_Conditional_Uniform_Additive_Limit_of_Wilson_Dirac_Relative_Entropy_on.pdf#page=1) · [D8, part 1, pp. 8–10](https://github.com/KirtusJ/From-Prephysical-Hypotheses-to-Physical-Models/blob/0ca75f60c76af1be7f3c25c2ed8914e82243ff5d/edition/PAPERS/D8_Wilson_Dirac_Covariance_Majorant_and_Boundary_Estimates/D8_Wilson_Dirac_Covariance_Majorant_and_Boundary_Estimates.pdf#page=8)

Kirtus Justus directs the research program and holds scholarly responsibility. OpenAI Codex assisted with these mathematical derivations, source comparisons and computational checks. This research supplement is dated 15 November 2026.
