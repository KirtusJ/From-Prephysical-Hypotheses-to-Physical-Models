# What real calibration probes can certify about the contact-loop readout

**Kirtus Justus**, Theoretical Physicist, Port Coquitlam, British Columbia, Canada. Mathematical and computational assistance from OpenAI Codex.

The [two-walker contact loop](unread_contact_loop.md) predicts sixteen incident position probabilities. The [separable-distance certificate](contact_distance/README.md) assumes four known qubit effects per station. If the actual effects are complex, even perfect local calibration on *every real preparation* permits a separable reproduction of the predicted table. A randomized, signed exchange of the two routes at **one** station suffices to exclude this rival family if the relabeled science table agrees with the ordinary prediction. These are tests on stipulated probabilities in the two-qubit code. They assume trusted preparations, fixed complete local detectors, tensor-product measurements, and a setting choice independent of the source and detector behavior.

## The undetermined local coordinate

In order of sites $-3,-1,1,3$, call the ideal effects $E_0,E_1,E_2,E_3$. Their upper triangles in units of $1/4$ are $(0,0,1),(1,-1,2),(2,1,1),(1,0,0)$. Use $X,Y,Z$ in the usual qubit convention, with $Y_{01}=-i$. The states $|0\rangle,|1\rangle,|+\rangle$ fix both diagonal entries and the real off-diagonal entry of each effect. Positivity sets the entire off-diagonal of each endpoint effect to zero because one diagonal entry vanishes. Completeness then leaves one real parameter per station:

$$
 (E_0,\ E_1-tY/4,\ E_2+tY/4,\ E_3),\qquad -1\le t\le1.
$$

The determinants of the inner effects in units of $1/16$ are $1-t^2$. All matrices in this interval are physical. The expectation of $Y$ vanishes on every real density matrix, including the minus preparation, so adding further real calibration probes cannot narrow the interval.

## All asymmetric separable rivals

Let $u,v$ be the two station parameters, $a=(1+u^2)^{-1/2}$ and $b=(1+v^2)^{-1/2}$. At either station the position scores of the [distance calculation](contact_distance/README.md) now measure $X+tY$ and $Z$. Set $U_t=\operatorname{diag}(1,e^{i\arctan t})$. Then $U_t XU_t^\dagger=(X+tY)/\sqrt{1+t^2}$ and $U_t ZU_t^\dagger=Z$. In the corresponding local frames, the scored $X$ direction has gains $1/a$ and $1/b$. Rotations are local and preserve separability.

Reconstruct the real symmetric projection $S$ of the state in these frames. Multiplying each local $X$ coefficient by the reciprocal gain while leaving $I,Z$ coefficients unchanged gives

$$
8S=M(a,b)=
\begin{pmatrix}
2&2b&2a&ab\\
2b&2&ab&0\\
2a&ab&2&0\\
ab&0&0&2
\end{pmatrix}.
$$

Every local effect is a linear combination of $I,X+tY,Z$, with the same coefficients for those observables as in the ideal frame. Agreement of the reconstructed coefficients is therefore equivalent to agreement of all sixteen probabilities, including both marginals. On a product state, projection to the local real planes preserves positivity on both factors. Consequently $S$ must be positive for every separable explanation. Conversely a positive $S$ has unit trace and equals its own partial transpose. It is separable by the two-qubit positive-partial-transpose criterion. Rotating it back by $U_u\otimes U_v$ gives a separable physical state for the original detectors. [Horodecki, Horodecki and Horodecki](https://arxiv.org/abs/quant-ph/9605038)

Writing $x=a^2,y=b^2$, the lower three-by-three block of $M$ has eigenvalues $2,2+ab,2-ab$, all positive. Its scalar Schur complement has the sign of

$$
D(x,y)=\det M=(4-xy)^2-16(x+y-xy),\qquad 1/2\le x,y\le1 .
$$

Thus the exact table has a separable explanation **if and only if $D(x,y)\ge0$**. At $u=v=1$, $a=b=1/\sqrt2$, and the leading principal minors are $2,2,3/2,33/16$. This yields an explicit strictly positive separable rival. Substituting the rotated-back state into its four local effects gives the integer table with rows $(1,3,3,1),(3,7,5,1),(3,5,19,5),(1,1,5,1)$ divided by 64.

At equal gains $x=y$, $D=(x-2)(x^3+2x^2+12x-8)$. The unique cubic root in the physical interval is $x=0.59119548\ldots$, corresponding to $|u|=|v|=0.83155750\ldots$. Larger absolute tilts permit a separable explanation, as does the boundary. With only one contaminated station, $D(1,y)=y^2-8y<0$ for the whole allowed interval. The second station can therefore remain entirely uncalibrated in its imaginary coordinate once the first is known to have zero tilt.

## One randomized signed exchange

At one station, independently of the prepared state, select one of two operations after formation and before the free readout. With probability $1-q$ keep the routes and count the actual site. With probability $q$ apply the trusted signed exchange $F=-iY$, then count site $i$ under the label $3-i$. All trials enter the relabeled table. Conjugation by $F$ changes the signs of $X,Z$ and preserves $Y$; mirroring the outcome interchanges the two inner effects. Hence $F^\dagger E_{3-i}(t)F=E_i(-t)$. Averaging the branches gives exactly $E_i((1-2q)t)$. The target table is unchanged for the ideal measurement.

At $q=1/2$ the treated station has effective tilt zero, so the previous one-contaminated-station result excludes every separable rival if the table is observed. Independent fair choices on both stations recover both ideal POVMs and hence the [fixed-detector distance](contact_distance/README.md). A shared fair choice applied simultaneously on both stations can retain a $Y\otimes Y$ term and does not prove the product-averaging identity. A route exchange $X$ without the relative minus sign is a different operation. Stability across selector choices, calibrated sign and coherent implementation of $F$ are physical assumptions.

For a biased switch the exact worst case also follows. The partial derivatives of $D$ are strictly negative on the physical square since $\partial_xD=-2y(4-xy)-16(1-y)<0$, and likewise for $y$. If Bob's tilt is unknown and Alice's residual tilt magnitude is at most $h$, the largest attainable $D$ is $D(1/(1+h^2),1/2)$. This is strictly negative exactly when

$$
h<\sqrt{1/(24-4\sqrt{34})-1}=0.69200360\ldots .
$$

The endpoint gives a separable explanation with Bob at maximal tilt. Thus the two settings with arbitrary original tilts guarantee exclusion for the exact target precisely when $|1-2q|$ is strictly below that bound, or $0.15399820\ldots<q<0.84600180\ldots$. The bias bound concerns the selector probabilities. Finite calibration error, finite incident counts, code leakage, and conditioning on the selector require separate analysis.


## A finite margin with one fair switch

Choose the conservative factor $c=2/3$ on the unswitched station B. Its unknown score axis has length $1/b$ between 1 and $\sqrt 2$, so $c/b\le 1$. In the rotated local frame, reconstruct each real one-party matrix from the usual scores, multiplying B's $X$ score by $c$. This projects each local Bloch ball onto a disk and contracts its $X$ coordinate. It sends every local density matrix to a positive matrix. Applied to a separable state, its tensor product with the switched station's real projection therefore gives a positive matrix, even if the local states have unmeasured $Y$ coordinates.

Score the reconstructed matrix against $v=(3,-1,-3,-1)^T$ by $v^T S v$. In the original site order, the signed scores for a single pair of observations are the entries of

$$
\begin{pmatrix}
37&-19&13&-43\\
-43&13&13&69\\
21&-3&-3&-27\\
-59&29&-3&85
\end{pmatrix}.
$$

These entries follow by taking $v^T(D_i(1)\otimes D_j(c))v$, where $D_i(c)=(I+c x_i X+z_i Z)/2$. All separable laws in the specified calibration family have nonnegative mean. The target table gives $-1/2$. The range of the score is 144, so any incident law within total variation strictly less than **$1/288$** of the target still excludes every separable rival in this family. This is a sufficient radius for one switched station. The exact distance for two ideal detectors is given in the [separate certificate](contact_distance/README.md). Sampling uncertainty applies to the measured score or distribution. The bound assumes the real probe probabilities and the fair signed exchange are exact.


For the stipulated blank-loop state the expected table after a fair exchange at A is the ideal one even when B has an unknown imaginary tilt. Its density matrix is real in the parked route basis, so the expectation of any real symmetric effect at A tensored with $Y$ at B vanishes. This argument does not assume that every rival prepares a real state.

There is a direct counterexample if the code dimension and absence of source labels are dropped. Give each detector a direct sum of the calibrated route qubit and four mutually distinguishable extra states. On the qubit block implement the ideal effects. On the extra block deterministically output its site label. The joint source can then send the two labels with the sixteen stipulated probabilities as a mixture of product states. All preparations confined to the calibration qubit still pass. Extend the signed exchange on the extra block by the site-mirror permutation and the counterexample also passes the randomized, relabeled test. Physically excluding or quantifying such leakage is a separate task.

For a native implementation, the program's [signed local routing construction](../../Director_G/Protected_records_and_coordinate_weights.md) realizes a route exchange and a relative minus sign using controlled routing and Hadamard ticks. Apply these on the parked route code and undo the routing before the read. The common timing and extra rail modes must not record the selected branch. The experiment continues to assume the two-dimensional encoding, ordinary measurement probabilities, and the action of the controls on complex amplitudes. It tests detector dependence within that model; it does not select a probability embedding from unlabeled records.

Compile [the exact checker](check_real_probe.rs) with `rustc --edition=2021 check_real_probe.rs` and run the resulting executable to reproduce the polynomial determinant identity, detector counts and integer trial scores.
