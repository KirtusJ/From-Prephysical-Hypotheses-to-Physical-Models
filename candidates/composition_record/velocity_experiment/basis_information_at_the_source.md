# How much basis information can a classical memory exploit?

The four-state walk prepares the two eigenstates of $Z$ and the two eigenstates of $X$, each with probability $1/4$. A classical replacement for the memory can measure the incoming rail together with any accessible auxiliary system, retain the result, and send a new qubit to the trusted matching-basis probe. If the auxiliary system partly identifies the basis, its optimal average probability of reproducing the source sign is

$$
F_{\rm MP}=\frac34+\frac14D(\tau_Z,\tau_X),\qquad
D(A,B)=\tfrac12\|A-B\|_1 .
$$

Here the complete accessible input conditional on basis $b$ and sign $s=\pm1$ is $(I+sP_b)/2\otimes\tau_b$, where $P_Z=Z$ and $P_X=X$. The side state may be mixed or noncommuting and is the same for both signs within each basis. The receiver commits the output qubit before the trusted basis probe, has no later source information, and every launch counts. The expression is an accessible-fidelity benchmark for this ensemble. [Four-state preparation and probe](four_state_circuit.py) · [Fuchs and Sasaki on measuring and resending a state](https://arxiv.org/abs/quant-ph/0302092)

## Attainment and an upper bound for joint measurements

Make the optimal binary measurement of the side system to guess $b$. Measure the rail along the guessed basis and resend the resulting eigenstate. Correct basis guesses score one. A mistaken guess scores one half because the two bases are mutually unbiased. The optimal equal-prior basis guess has success $(1+D)/2$, attained by the positive spectral subspace of $\tau_Z-\tau_X$ and its complement. This gives the stated score. [Helstrom, *Detection theory and quantum mechanics*](https://doi.org/10.1016/S0019-9958%2867%2990302-6)

For the converse, let $(M_j)$ be any measurement of the joint input. Write $c_j,d_j$ for the $Z,X$ Bloch coordinates of the qubit resent on outcome $j$, so $c_j^2+d_j^2\le1$. Summing over the four inputs gives

$$
F=\frac12+\frac18\sum_j\operatorname{tr}M_j
   (c_j Z\otimes\tau_Z+d_j X\otimes\tau_X).
$$

Let $H=(\tau_Z+\tau_X+|\tau_Z-\tau_X|)/2$. Then $H\ge\tau_Z,\tau_X$ and $\operatorname{tr}H=1+D$. For any real $c,d$ with $c^2+d^2\le1$ we claim

$$
c Z\otimes\tau_Z+d X\otimes\tau_X\ \le\ I\otimes H .
$$

To see this, whiten by $H+\epsilon I$ with $\epsilon>0$. The resulting side operators $A=(H+\epsilon I)^{-1/2}\tau_Z(H+\epsilon I)^{-1/2}$ and $B$ defined with $\tau_X$ are positive contractions. In the eigenbasis of the rail's Pauli $Y$, the whitened signed sum has zero diagonal blocks and off-diagonal blocks $cA\pm i dB$. Its norm is $\|cA+i dB\|$.

For each unit side vector $v$, $\operatorname{Im}\langle Av,Bv\rangle=\operatorname{Im}\langle(I-A)v,(I-B)v\rangle$, because the discarded scalar expectations are real. Cauchy–Schwarz bounds the cross term of $\|(cA+i dB)v\|^2$ by $c^2\|(I-A)v\|^2+d^2\|(I-B)v\|^2$. Adding the two diagonal terms gives at most $c^2+d^2$ since $A^2+(I-A)^2\le I$ and likewise for $B$. Undo the whitening and send $\epsilon$ to zero in the operator inequality. This argument also covers trace-class flags in infinite dimension, since the limit is taken before the trace.

There is an independent two-dimensional check. For each matrix element between unit vectors $u,v$, compress both positive contractions to their span. In this space they are convex mixtures of projections. If either of two such projections $P,Q$ is zero or identity, simultaneous diagonalization bounds $\|cP+i dQ\|$ by $\sqrt{c^2+d^2}$. Otherwise both have rank one and the squared Hilbert–Schmidt norm of $cP+i dQ$ is $c^2+d^2$. Taking mixtures and the supremum over $u,v$ gives the same bound.

Sum the inequality over the measurement using $\sum_j M_j=I$. The excess over $1/2$ is at most $\operatorname{tr}(I\otimes H)/8=(1+D)/4$. The same inequality integrates over a continuous outcome space. The joint measurement therefore attains its optimum with the basis-guess procedure above. The endpoints $D=0,1$ give $3/4$ and $1$.

## The threshold at seven writes

The ideal four-Pauli correction gives $A_4(7)=226560354573/274877906944$. Its predicted margin over every measure-and-prepare memory in this model is strictly positive precisely when

$$
D < 4A_4(7)-3
 =\frac{20401924365}{68719476736}
 \simeq 0.296887074 .
$$

At equality the classical strategy matches the predicted score. Equivalently the best basis guess from the flag alone must have success below $89121401101/137438953472\simeq0.648443537$. An experiment compares a lower confidence bound for its own incident score with $3/4+D_{\rm upper}/4$, using jointly valid coverage. These thresholds use the ideal score as a planning calculation. [Exact seven-write calculation](check_four_state_alphabet.py) · [Incident scoring](four_state_records.py)

## Measuring leakage and checking the sign premise

Performance of one attempted basis discriminator gives a lower bound on optimal guessing. An upper bound requires control of the full system accessible to the memory, including timing, position and classical records. For two pure flags with amplitude overlap $r$, $D=\sqrt{1-|r|^2}$. For mixed flags, a lower bound on the root fidelity $f=\|\sqrt{\tau_Z}\sqrt{\tau_X}\|_1$ gives $D\le\sqrt{1-f^2}$. [Fuchs and van de Graaf on distinguishability](https://arxiv.org/abs/quant-ph/9712042)

If the entire flag is known to be a qubit, the traceless difference has eigenvalues $\pm D$. Three overlap measurements yield

$$
D^2=\tfrac12\left[\operatorname{tr}\tau_Z^2+\operatorname{tr}\tau_X^2
                         -2\operatorname{tr}(\tau_Z\tau_X)\right].
$$

The mean of a SWAP read on two independent preparations equals their Hilbert–Schmidt overlap. Simultaneous upper bounds for the two purities and a lower bound for the cross overlap give an upper bound on $D^2$ by substitution. Preparation stability between calibration and the science launches, independence within each calibration pair, calibrated SWAP readout and the assumed flag dimension are physical premises. The source-only bypass checks rail preparation and readout; it cannot by itself bound a side channel. [Ekert et al. on direct estimation by controlled SWAP](https://arxiv.org/abs/quant-ph/0203016)

A sign-only classical flag gives a concrete failure of a basis-averaged audit. Let the flag contain $s$ perfectly for both bases. The two basis-averaged flags are identical. Ignoring the rail and resending the pure state with Bloch direction $s(\hat X+\hat Z)/\sqrt2$ gives $(1+1/\sqrt2)/2\simeq0.853553$, exceeding the seven-write prediction. Testing sign independence within each basis therefore matters.

For calibrated sign dependence, write $\tau_b=(\tau_{b,+}+\tau_{b,-})/2$ and $D_b=D(\tau_{b,+},\tau_{b,-})$. Keeping the same pure rail inputs, replacing the four actual side states by $\tau_b$ changes the mean success of any fixed strategy by at most $(D_Z+D_X)/4$. Indeed each input has trace distance $D_b/2$ from its replacement, and each strategy followed by its matching test defines a success effect between zero and identity. This gives a conservative upper bound of $3/4+[D(\tau_Z,\tau_X)+D_Z+D_X]/4$, capped at one. It accommodates upper calibration bounds on all three distances. The equality formula applies to the sign-independent model.

Kirtus Justus, Theoretical Physicist, Port Coquitlam, British Columbia, Canada, retains scholarly responsibility. OpenAI Codex developed the joint-measurement bound and calibration analysis. No hardware data enter these predictions.
