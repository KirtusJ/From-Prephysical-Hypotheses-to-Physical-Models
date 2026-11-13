# Incomplete detector calibration

## 2. Independent result: exact detector partial-identification interval

Let trusted density matrices rho_i (i=1,...,m) have exact measured response rates p_i for an otherwise unknown but stable binary measurement effect 0 <= E <= I on a finite-dimensional Hilbert space. For a target state rho_T define

```
L(p) = min Tr(E rho_T),   U(p) = max Tr(E rho_T),
subject to Tr(E rho_i)=p_i for every i and 0 <= E <= I.
```

These are finite semidefinite programs, and by definition are the sharp possible target-response bounds for the entire admissible effect class. Both extrema are attained when the calibration vector is feasible because the effect set is compact. The image is a closed interval by convexity. **They are data dependent**: a target outside the real reference span does not imply ambiguity for every possible calibration dataset.

For any real vector lambda, put A=lambda-weighted subtraction `A=rho_T-sum_i lambda_i rho_i`. Then

```
Tr(E rho_T) = sum_i lambda_i p_i + Tr(E A)
            <= sum_i lambda_i p_i + Tr(A_+),
```

where `A_+` is the positive part of A and the inequality is sharp when E is its positive spectral projector if no other constraints are imposed. Consequently,

```
U(p) <= inf_lambda [sum_i lambda_i p_i + Tr((rho_T-sum_i lambda_i rho_i)_+)].
```

The inequality is equality under the usual finite-dimensional Slater condition: at least one compatible effect satisfies 0 < E < I. At boundary response vectors, rely on the primal SDP or limiting dual, not an unqualified interior-strong-duality assertion. For normalized densities, `L(p)=1-U(1-p)` follows by exchanging E and I-E.

### Elementary complete proof for a qubit

Use two trusted reference states |0><0| and |1><1|. Suppose their calibrated click probabilities are p0,p1. A possible effect has the form

```
E = [[p0, z], [conjugate(z), p1]].
```

Positivity of E and I-E is equivalent to

```
|z| <= R := min(sqrt(p0*p1), sqrt((1-p0)*(1-p1))).
```

For the held-out target |+>=(|0>+|1>)/sqrt(2), `q=(p0+p1)/2+Re(z)`. Choosing z=+/-R proves the *exact* interval

```
(p0+p1)/2-R <= q <= (p0+p1)/2+R.
```

In particular, if p0=p1=p, the range is `[max(0,2p-1),min(1,2p)]`. At p=0 the calibration forces E=0 and q=0, despite |+><+| lying outside the real reference span. At p=1/2 the same two reference probabilities are compatible with every target rate from zero to one. These are extreme physical effects, not a numerical fitting artifact.

This is an instance of established quantum partial tomography and set-identification SDPs (e.g. *Physical Review A* 98, 042318, 2018), not a claim of mathematical originality. Its application to the present measurement contract is useful because it avoids inferring universal ignorance from mere failure of reference informational completeness.

### Uncertain reference data

When independently justified intervals `[l_i,u_i]` replace exact p_i, use the same primal with inequalities. Its Lagrangian bound reads

```
U <= inf_{beta_i,gamma_i>=0} [sum_i (beta_i u_i-gamma_i l_i)
      + Tr((rho_T - sum_i (beta_i-gamma_i)rho_i)_+)].
```

Equality follows under appropriate strict feasibility. This is how uncertainty and physicality should jointly enter, rather than treating a noisy point estimate as exact.

## 3. Cross-check: tetrahedral source-response bound

For four trusted tetrahedral qubit states rho_i=(I+r_i dot sigma)/2, define D_i=(3rho_i-I)/2. They form a dual frame and satisfy sum D_i^2=(5/2)I. The sixteen probabilities `p_ij=Tr(E rho_i tensor rho_j)` determine E exactly. Under entrywise errors |delta p_ij| <= delta, the *maximum response over separable states*, b_sep(E), changes by at most 4 delta, which is sharp. The proof uses the dual weights

```
w_i(x) = Tr(D_i rho_x)=(1+3r_i dot x)/4.
```

The exact maximum of sum_i |w_i(x)| is two for Bloch vectors |x|<=1, attained at a tetrahedral antipode, with weights (-1/2,1/2,1/2,1/2). Product response weights therefore have absolute sum at most four. Direct construction of a sign-perturbation near E=I/2 attains the bound without leaving the effect set for sufficiently small delta.

Using alpha=.05, Delta=13/1280, and seventeen independent settings of n trials each, the sufficient requirement n > 50 log(34/alpha)/Delta^2 gives n=3,161,479, total 53,745,143. This is a *conservative sufficient* shot budget with trusted preparations, stable effect, and independent Bernoulli trials, not a necessary hardware cost.
