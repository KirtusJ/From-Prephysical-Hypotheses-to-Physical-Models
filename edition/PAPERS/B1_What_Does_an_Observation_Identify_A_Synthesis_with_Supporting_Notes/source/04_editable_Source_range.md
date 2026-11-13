# Source range

## Proposition 1: exact range recovery

Let B be a d-by-n isometry, B* B = I_n. Let Sigma >= 0 have rank r and support Q_s. Define C = B Sigma B*. Then C C^+ = B Q_s B*. If the experiment combines several source preparations with sum of covariances Sigma supported on the entire desired observable subspace Q, then C C^+ = B Q B*. This follows immediately from the range of B Sigma B*. In the specified three-port passive quantum Ricker isometry B=(W_s,W_t,sqrt(I-W_s^2-W_t^2))^T, the first and second diagonal blocks of the latter projection are W_s^2 and W_t^2. Positive square roots recover W_s and W_t. This proof assumes full access to all three output groups, vacuum-floor subtraction, and sufficiently excited source modes.

## Theorem 2: quantitative range-projector stability

Let C=B Sigma B* be positive semidefinite and of rank r. Let mu>0 denote its smallest nonzero eigenvalue. If a Hermitian observed matrix Chat=C+E satisfies ||E||_op <= delta < mu/2, and Phat projects onto the r largest eigenvalues of Chat, then, for P=CC^+,

    ||Phat-P||_op <= delta/(mu-delta).

Proof: Weyl's theorem places the r signal eigenvalues of Chat above mu-delta and the remainder in [-delta,delta]. Thus Phat is correctly ranked and Chat is invertible on Ran Phat with inverse norm <=1/(mu-delta). Since (I-P)C=0, (I-P)Chat Phat=(I-P)E Phat. Postmultiply by the restricted inverse and take norms. Equal-rank orthogonal-projector geometry gives ||P-Phat||=||(I-P)Phat||. QED.

Interpretation: for an isometric B, mu equals the smallest strictly positive eigenvalue of Sigma. The previously reported rank jump as epsilon approaches zero is therefore compatible with strong instability at finite noise. The proof is a specific Davis-Kahan/Wedin-type estimate, not a claimed novel matrix perturbation theorem.

## Theorem 3: exact Gaussian information loss from subspace rotation

Let P_1 and P_2 be real orthogonal projections of equal rank r in dimension d, and let S_i=v I+epsilon P_i for v,epsilon>0. Write G_i=N(0,S_i). Then

    D_KL(G_1 || G_2) = D_KL(G_2 || G_1)
                       = epsilon^2 ||P_1-P_2||_F^2 / [4 v (v+epsilon)]
                       = epsilon^2 sum_j sin^2(theta_j) / [2 v (v+epsilon)].

Proof: det S_1=det S_2=v^(d-r)(v+epsilon)^r and S_i^(-1)=v^(-1)I-epsilon P_i/[v(v+epsilon)]. Substitute into Gaussian KL and use ||P_1-P_2||_F^2 = 2(r-tr(P_1P_2)). QED.

Corollary (fixed dimension and fixed known candidate projectors): M independent preparations yield KL equal to M times the single-preparation expression. If M epsilon^2 -> 0 for fixed v, Pinsker gives asymptotically zero total-variation separation. If M epsilon^2 -> infinity, a likelihood-ratio test distinguishes the two fixed alternatives consistently. The epsilon^-2 statistical threshold pertains to this homodyne Gaussian observation contract, not all quantum probes.
