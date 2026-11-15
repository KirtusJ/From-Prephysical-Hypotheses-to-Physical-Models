# An event-ready Bell test for the unread contact loop

**Kirtus Justus**, Theoretical Physicist, Port Coquitlam, British Columbia, Canada. Mathematical and computational assistance from OpenAI Codex.

The stipulated blank-register contact prepares an entangled pair of two-route walkers. With a single copy, arbitrary unfiltered local binary measurements satisfy the CHSH bound. A setting-independent local filter on each walker succeeds jointly on $3/64$ of launches. On this heralded ensemble, each station can choose an immediate position read or three free walk ticks. The two settings predict $|S|=49/24$ with every terminal position counted. These are ordinary-probability predictions conditional on coherent contacts, the stated local instruments and freely chosen settings. [Contact state and fixed position detectors](unread_contact_loop.md) · [Distance of the fixed position law from separable laws](contact_distance/README.md)

## The blank pair before filtering

Use route order $00,01,10,11$, Pauli order $X,Y,Z$, and normalized input $\lvert+\rangle\lvert+\rangle$. After the four contacts and disconnection of the unobserved register, the first three routes have a common memory endpoint and $11$ has an orthogonal endpoint. With $u=(1,1,1,0)^T$ the pair has density matrix
\[
 \rho=(uu^T+\lvert11\rangle\langle11\rvert)/4 .
\]
The $3\times3$ correlation matrix and the eigenvalues of its square are
\[
 T_{ij}=\operatorname{tr}(\rho\,\sigma_i\otimes\sigma_j)
  =\tfrac12\begin{pmatrix}1&0&1\\0&1&0\\1&0&0\end{pmatrix},
 \qquad
 \operatorname{spec}(T^TT)=
 \left\{\tfrac{3+\sqrt5}{8},\,\tfrac14,\,\tfrac{3-\sqrt5}{8}\right\}.
\]
For $S=E_{00}+E_{01}+E_{10}-E_{11}$, the largest absolute value with nondegenerate binary projective qubit measurements is twice the square root of the sum of the two largest eigenvalues. This gives $\sqrt{(5+\sqrt5)/2}=1.902113\ldots$. Allowing arbitrary binary POVMs gives exactly 2: the extreme qubit observables are projective, and if any one is constant its two local observables commute and admit a common outcome distribution, which obeys CHSH. Constant outputs attain 2. Assigning different numerical scores to a single fixed four-position detector likewise supplies joint local data for every postprocessing. Scores outside $[-1,1]$ fall outside the CHSH bound used here. [Horodecki, Horodecki and Horodecki](https://doi.org/10.1016/0375-9601(95)00214-N)

## A local preparation with a recorded success flag

Give each station a clean flag and apply the same real contraction
\[
 K=\tfrac12\begin{pmatrix}1&0\\-1&1\end{pmatrix}.
\]
The eigenvalues of $K^TK$ are $(3\pm\sqrt5)/8$, both below one. On a local input $(a,b)$ the two accepted modes must carry $(a/2,(-a+b)/2)$ coherently. This can be realized as an addressed path circuit. Split each input against an empty mode by a balanced Hadamard. At a second layer mix one $a$ arm with an empty mode, taking its $a/2$ port; mix the other $a$ arm with one $b$ arm using a signed Hadamard, taking the $(-a+b)/2$ port. Route the two accepted outputs to the same flag value while preserving the two route labels. The remaining outputs, including the unused $b$ arm, carry failure. Equal-depth padding of rejected arms is possible by pairing them with other unused modes. The flag measures membership in the two-mode success subspace without distinguishing the accepted paths. This construction requires local spare modes, coherent routing, signed permutations, balanced coins and a coarse nondestructive flag. It extends the free two-tick position apparatus.

Writing $K_2=K\otimes K$, its unnormalized successful output has the following two-dimensional block on $00,11$, and all entries on $01,10$ vanish:
\[
  (K_2\rho K_2^T)_{\{00,11\}}=\tfrac1{64}
     \begin{pmatrix}1&-1\\-1&2\end{pmatrix}.
\]
The two local flag effects are $Q=K^TK$ and $I-Q$. Multiplying each pair of effects against $\rho$ gives probabilities $(35,13,13,3)/64$ in flag order (failure/failure, failure/success, success/failure, success/success). Each local flag succeeds with probability $1/4$, and $P(H)=3/64$ for the joint success signal $H$. The instrument must retain the output coherently on a successful flag. Flag probabilities alone do not establish its state update. The normalized conditional law has $T_{zz}=1$, $T_{xx}=-2/3$, $T_{yy}=2/3$ and vanishing mixed correlations. Its optimum over binary qubit measurements is $2\sqrt{13}/3=2.403700\ldots$, attained by real projective settings. This figure concerns this particular filter. [Popescu, hidden nonlocality under sequential local measurements](https://doi.org/10.1103/PhysRevLett.74.2619) · [Single-copy local filtering and CHSH](https://arxiv.org/abs/quant-ph/0112012)

## A shared setting switch and three free ticks

Return each successful output to the local route code $\lvert0\rangle=\lvert+1,R\rangle$, $\lvert1\rangle=\lvert-1,L\rangle$. Both stations use the same two settings. For setting zero, read the sign immediately, giving $Z$ (right positive). For setting one, take three homogeneous Hadamard-and-shift ticks and retain every terminal site, summing both rails. Report $+1$ when $x>0$, and $-1$ when $x\le0$. The origin belongs to the negative bin. The local walk must have no wall within the reachable sites from $-4$ through $4$.

For clarity, the two positive sites after three ticks are $x=2,4$. The route-code-to-outgoing-rail matrices there, in row order $R,L$, are $\left(\begin{smallmatrix}2&1\\1&0\end{smallmatrix}\right)/\sqrt8$ and $\left(\begin{smallmatrix}1&0\\0&0\end{smallmatrix}\right)/\sqrt8$. Summing their squared matrices gives
\[
 E_+=\tfrac18\begin{pmatrix}6&2\\2&1\end{pmatrix},
 \qquad O=2E_+-I=-I/8+X/2+5Z/8 .
\]
The filtered state has local $Z$ means $-1/3$. Its correlators for the two settings are $E_{00}=1$, $E_{01}=E_{10}=2/3$, and $E_{11}=7/24$. Thus $S=49/24=2.041666\ldots$ with identical analyzers and complete position counts on every heralded trial. The setting choice changes the actual free evolution before detection. Pad the immediate read locally to the same reporting deadline if needed for the spacetime design.

If the detector resolves the rail at the origin, also put $(0,R)$ in the positive bin, leaving $(0,L)$ negative and all other assignments fixed. This changes $O$ to $X/2+3Z/4$, and the correlators become $1,3/4,3/4,19/48$. They give $S=101/48$. Independent fair replacement of a whole pair's correlations with retention $\eta$ gives $|S|=\eta|S_{\rm ideal}|$. The strict thresholds for these two respective protocols are $\eta>48/49$ and $\eta>96/101$, with equality at the local bound. This error model is separate from optical efficiency or setting-dependent losses.

For an explicit detector-loss convention on the heralded sample, assign $-1$ to every missing local result. With independent, outcome- and setting-independent detection of common efficiency $\eta$ on both sides, the ideal double-positive probabilities in settings $00,01,10,11$ are $1/3,1/4,1/4,5/32$; both local positive probabilities on setting zero are $1/3$. The Clauser-Horne expression, double positives in $00,01,10$ minus those in $11$ and the two setting-zero singles, is therefore $65\eta^2/96-2\eta/3$. It is positive precisely at $\eta>64/65$, with equality at $64/65$. All missing results remain in the counts. This efficiency threshold is specific to the three-tick position bins, the stated erasure channel and the fixed fallback outcome. [Terminal-position readout checks](terminal_bell_read.md)

## Trial accounting and interpretation

The [exact Rust replay](check_heralded_bell.rs) enumerates all possible binary position bins, with independent local read times and bins for each setting. On this filtered source their maximum through two free ticks is 2 (23 distinct observables). Through three ticks it is $49/24$ (45 observables). The clock bound applies to forward homogeneous evolution from the re-encoded routes, with both rails pooled.

1. Record a launch ID, initialize the walkers and registered blank, complete the contacts and disconnect the mediator. At both stations run the fixed local filter, time-stamp each flag, and bring the two flag values together. Log all four flag pairs.
2. On a joint herald, communicate the ready signal to both stations. Keep the local quantum outputs coherent until both settings are selected. Choose each binary setting independently of the source, the flags and the other setting. The settings and local outcomes must meet the spacetime separation required for a Bell experiment.
3. Record both outcomes by fixed local deadlines on every heralded trial. Each $(x,y)$ correlator is the mean over all joint-herald trials receiving $(x,y)$, including any missed detections assigned the specified local response. Preparatory failures stay in the separate, setting-independent launch and yield record. Trials with lost outputs after setting choice require a prespecified local binary response included in the data.

Under these conditions the hidden-variable distribution given the herald is common to all four settings, so the CHSH bound remains 2 on that conditional ensemble. The joint herald rate is part of the preparation record; the conditional correlators use the heralded trial count. One can instead choose settings on every launch and have both stations output $+1$ on every previously announced joint-preparation failure. The resulting all-launch score is $2+(3/64)(S-2)$. For the three-tick position read this is $1025/512$, a smaller positive excess. Both procedures require the common herald to arrive before the choices. Conditioning on a setting-dependent coincidence would change the sample used for each correlator. An actual event-ready spin experiment supplies precedent for the timing and detection controls. This candidate supplies a mathematical prediction for a different apparatus. [Hensen et al., event-ready Bell experiment](https://doi.org/10.1038/nature15759)

The preparation and measurement circuits assume quantum composition, ordinary probabilities, memory coherence and calibrated route controls. A positive experimental score under Bell’s operational conditions would test the correlations of the whole preparation. Identifying the particular memory mechanism would also require independent checks on the contacts, initial independence and isolation of the stations.
