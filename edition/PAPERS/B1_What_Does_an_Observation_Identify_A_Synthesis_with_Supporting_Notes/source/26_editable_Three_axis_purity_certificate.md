# Three-axis purity certificate

## 2. Model and population constraints

Use output-first vectorization on \(\mathcal H=\mathbb C^4\otimes\mathbb C^4\), with normalized Choi vectors \(|M\rangle=\operatorname{vec}(M)/2\). Let

\[
 p=|I_4\rangle,\quad u=|i(Z\otimes I_2)\rangle,\quad v=|i(X\otimes I_2)\rangle,
\]

where \(X,Y,Z\) are the Pauli matrices. Put

\[
 a=sh,\quad k=\frac{(a-\sqrt{a q_0})^2}{s h(1-h)},\quad d=s+k,\quad r=1-d,
\]
\[
 \eta=\frac{\sqrt{s}\,p-\sqrt{k}\,u}{\sqrt d},\qquad
 \theta=\frac{\sqrt{k}\,p+\sqrt{s}\,u}{\sqrt d},\qquad
 F=|v\rangle\langle v|,
\]

and \(D=I-|p\rangle\langle p|-|u\rangle\langle u|-F\), of rank 13. The **exact complete lower-endpoint phase curve** with its fixed effect forces the orthogonal vector \(\theta\) into the kernel of each compatible positive Choi state. For the additional-outcome probability \(f=\operatorname{Tr}(F\rho)\), the fixed populations are \(d,f,r-f\). The normalized CPTP condition is \(\operatorname{Tr}_{\mathrm{out}}\rho=I_4/4\).

The minimum-purity state in this compatible class is

\[
 \rho_\star(f)=d|\eta\rangle\langle\eta|+fF+\frac{r-f}{13}D,
 \qquad J(f)=d^2+f^2+\frac{(r-f)^2}{13}.
\]

All vectors spanning the three sectors can be chosen as maximally entangled Choi vectors; hence \(\operatorname{Tr}_{\rm out}\rho_\star=I_4/4\). For any compatible \(\rho\), the populations give the exact identity

\[
\operatorname{Tr}\rho^2=J(f)+\|\rho-\rho_\star(f)\|_2^2.
\]

This setup is restricted to that exact phase curve and detector. Ordinary readout probability alone does not fix \(\theta\) as a null direction.

## 3. Joint first-qubit X/Y/Z measurement theorem

**Theorem (three-axis locally sharp purity certificate).** Fix the model of section 2, with exact \(s,h,q_0\), the full specified phase curve, and the extra-outcome population \(0\le f\le r\). Assume a normalized CPTP Choi state \(\rho\) transfers unchanged to a fresh product input \(|00\rangle\). For each \(Q\in\{X,Y,Z\}\), denote by \(p_Q\) the probability that a projective measurement of the **first output qubit** in the corresponding Pauli basis returns the positive eigenvalue. Set

\[
 p_Z^{\star}(f)=d+\frac{6(r-f)}{13},\qquad
 p_X^\star=p_Y^\star=\tfrac12.
\]

Then

\[
\boxed{
 \operatorname{Tr}(\rho^2)\;\ge\;J(f)
 +\frac{91}{1230}\bigl[p_Z-p_Z^\star(f)\bigr]^2
 +\frac{7}{97}\Bigl[(p_X-\tfrac12)^2+(p_Y-\tfrac12)^2\Bigr].}
\]

The inequality holds globally over all compatible normalized CPTP Choi states. At every **interior** \(0<f<r\), equality is attainable for every sufficiently small triple of deviations from the indicated reference probabilities, using an explicitly positive normalized CPTP Choi matrix. This is *local* simultaneous sharpness; it does not assert attainability of arbitrary triples far from the reference probabilities, nor impose unital or mixed-unitary constraints.

**Proof.** Define the actual output-probability observables

\[
M_Q=4\,[((I_2+Q)/2)\otimes I_2]_{\rm out}\otimes[|00\rangle\langle00|]_{\rm in}.
\]

Let \(B=I-|\theta\rangle\langle\theta|\). For any Hermitian \(M\), first remove the three fixed population directions:

\[
M_1=BMB
 -\operatorname{Tr}(BMB|\eta\rangle\langle\eta|)|\eta\rangle\langle\eta|
 -\operatorname{Tr}(BMBF)F
 -\frac{\operatorname{Tr}(BMB D)}{13}D.
\]

This operator is supported on \(B\), orthogonal to the three fixed populations, and traceless. Put \(L=\operatorname{Tr}_{\rm out}M_1\), a traceless Hermitian reference operator. Since \(\theta\) is maximally entangled, for traceless Hermitian \(H,G\),

\[
\operatorname{Tr}[B(I\otimes H)B(I\otimes G)]
 =\frac72\operatorname{Tr}(HG).
\]

The operators \(B(I\otimes H)B\) are already orthogonal to the three fixed populations. Therefore

\[
\widehat M=M_1-\frac27 B(I\otimes L)B
\]

is the Hilbert–Schmidt projection onto the additional tangent condition \(\operatorname{Tr}_{\rm out}\Delta=0\). It is also orthogonal to \(\theta\), and to the three population constraints.

Direct Pauli-matrix multiplication in the specified 16-dimensional vectorization gives the following **exact** Gram matrices for the ordered observables \((Z,X,Y)\):

\[
G^{(1)}_{PQ}=\operatorname{Tr}(M_{P,1}M_{Q,1})=
\begin{pmatrix}
276/13&9&9\\9&49/2&21/2\\9&21/2&49/2
\end{pmatrix},
\]
\[
G^{(L)}_{PQ}=\operatorname{Tr}(L_PL_Q)=
\begin{pmatrix}
27&63/2&63/2\\63/2&149/4&147/4\\63/2&147/4&149/4
\end{pmatrix}.
\]

For example, the X/Y population subtraction is \(M_{Q,1}=BM_QB-B/2\); \(M_Q^2=4M_Q\) and \(\operatorname{Tr}M_Q=8\) give \(\operatorname{Tr}M_{Q,1}^2=49/2\). Their partial traces have diagonal \(7(|00\rangle\langle00|-I_4/4)\) and an off-diagonal magnitude 1/2 with X and Y in orthogonal quadratures, giving \(\operatorname{Tr}L_Q^2=149/4\) and \(\operatorname{Tr}L_XL_Y=147/4\). The entries involving Z follow by the same rank-one contractions, with \(L_Z=6(|00\rangle\langle00|-I_4/4)\).

Subtracting the trace-preservation projection gives

\[
G_{PQ}=\operatorname{Tr}(\widehat M_P\widehat M_Q)
=G^{(1)}-\frac27G^{(L)}
=\operatorname{diag}\!\left(\frac{1230}{91},\frac{97}{7},\frac{97}{7}\right).
\]

For \(\Delta=\rho-\rho_\star(f)\), all imposed constraints are homogeneous and \(\operatorname{Tr}(M_Q\Delta)=\operatorname{Tr}(\widehat M_Q\Delta)\). Orthogonal Bessel inequality in Hilbert–Schmidt space yields

\[
\|\Delta\|_2^2\ge
\frac{[p_Z-p_Z^\star(f)]^2}{1230/91}
+\frac{[p_X-1/2]^2+[p_Y-1/2]^2}{97/7}.
\]

Together with the purity-excess identity, this proves the inequality. For a sufficiently small deviation vector \((\delta_Z,\delta_X,\delta_Y)\), define

\[
\rho=\rho_\star(f)+\frac{91\delta_Z}{1230}\widehat M_Z+
\frac{7\delta_X}{97}\widehat M_X+
\frac{7\delta_Y}{97}\widehat M_Y.
\]

It preserves every linear phase, population and trace-preservation constraint, reproduces the desired three deviations, and achieves equality. For interior \(f\), the base state is strictly positive on the allowed fifteen-dimensional support, so every sufficiently small Hermitian perturbation on that support remains positive. This completes the constructive local-sharpness proof. □

**Restriction to the longitudinal reading.** Setting \(p_X=p_Y=1/2\) reduces exactly to the coefficient \(91/1230\). Measuring additional X/Y axes need not make purity identifiable: if all probabilities equal their reference values, compatible states can still have a wide range of purities.

## 4. Numerical witness and finite-data limits

At \(f=r/2\), the verifier constructs the positive channel state with deviations \((\delta_Z,\delta_X,\delta_Y)=(0.005,0.007,-0.004)\). It checks the full Choi marginal, positivity, phase response at six settings, exact extra-outcome probability, and equality in the three-axis bound within floating-point tolerance. It prints an attained purity of approximately 0.336263620116203. 

The theorem assumes exact population parameters. For a simultaneous confidence region on \((f,p_X,p_Y,p_Z)\), a valid conservative lower purity certificate is obtained by **minimizing the right-hand side of the theorem over that entire region**, together with any independently justified region for \((s,h,q_0)\). For known \(f\) and marginal probability intervals, this is achieved by substituting each interval's distance from its corresponding reference probability. For uncertain \(f\), minimize over its allowed range; the objective is convex quadratic in \(f\) when the other inputs are fixed. An empirical claim requires calibration transfer, finite-sample uncertainty allocation, and an independently supported full-phase compatibility premise. Merely inserting observed frequencies into exact equations provides no coverage guarantee.

The mutually noncommuting X, Y, Z output observables would generally be measured on different preparations. The normalized Choi marginal applies to a **trace-preserving channel**. A history-selected trace-nonincreasing instrument branch need not have that marginal, and applying the same process to product input \(|00\rangle\) is an additional physical transfer claim. Nothing here verifies those premises experimentally.
