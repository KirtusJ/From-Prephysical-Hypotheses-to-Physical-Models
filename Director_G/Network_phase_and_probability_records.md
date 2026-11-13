# What a two-source network measures about the walk's phase standard

**Kirtus Justus**, Theoretical Physicist

Port Coquitlam, British Columbia, Canada

Mathematical development and checks by Director G (OpenAI Codex).

A network can distinguish phase planes which were prepared independently from planes which met and retained a common orientation. A finite signed circuit can make this distinction even when every probability it produces is rational. This gives the walk an operational phase standard across sites. The construction uses the squared coordinate rule to predict its records. The same finite transcripts occur under the alternative embeddings of the signed walk.

## How much alignment can independent preparations supply?

Give site \(i\) a two-coordinate real plane and the signed quarter-turn \(J_i|0\rangle=|1\rangle,\ J_i|1\rangle=-|0\rangle\). Operators on different sites commute. The observable \(K_{ij}=-J_iJ_j\) is a real symmetric involution. In the complexification write \(s_i=\pm1\) for the label of the eigenvalue \(s_i\,\mathrm i\). A comparison gives \(s_i s_j\). Let \(P\) be the projector onto all labels equal on a connected graph with \(n\ge1\) vertices. Its real rank is two. The mixed plane state \(\tau=P/2\) is the distributed phase standard used in real simulations of complex experiments. It is established in the literature, including the case of many sources reusing one initial resource. The walk supplies an explicit finite circuit for preparing it before use. For example, after preparing a pure real vector in the common plane, averaging identity and a local \(J_i\) with a fair bit gives \(\tau\). [McKague, Mosca and Gisin](https://doi.org/10.1103/PhysRevLett.102.020505) · [Weilenmann, Gisin and Sekatski, Eq. 8](https://arxiv.org/html/2502.20102v2) · [Local preparation and its timing](Phase_contact_and_shared_walks.md)

Partition the vertices into \(m\) nonempty source blocks, allowing arbitrary real states within each. Call \(\mathcal S\) the convex hull of tensor products across the blocks. This also allows the sources shared classical randomness. Write \(D(\rho,\sigma)=\|\rho-\sigma\|_1/2\). Then

\[
 \max_{\sigma\in\mathcal S}\operatorname{tr}(P\sigma)=2^{1-m},
 \qquad
 \min_{\sigma\in\mathcal S}D(\tau,\sigma)=1-2^{1-m}.
\]

For a block \(B\), its two complex product vectors with every \(s_i=+\) and every \(s_i=-\) are conjugates and orthogonal. A real density matrix gives them equal diagonal weights \(x_B\le1/2\). On a product of blocks, the total all-aligned probability is \(2\prod_B x_B\). Convex mixing preserves the bound. The product of the normalized internal projectors \(P_B/2\) attains it, including when \(B\) is a singleton. Measuring \(P\) bounds the trace distance from below. The attaining product is diagonal with mass \(2^{-m}\) on each of the \(2^m\) internal-block sign strings, whereas \(\tau\) gives \(1/2\) to each of the two common signs. Their classical total variation equals \(1-2^{1-m}\). A source within distance \(\delta\) of \(\mathcal S\) can pass with probability at most \(\min(1,2^{1-m}+\delta)\). This bound concerns a specified real tensor product and a joint read. Its application to the physical independence of sources requires that representation premise.

For \(m=2\) define \(\omega_\nu=(I+\nu K_{AC})/4\), \(-1\le\nu\le1\). Both one-site states are \(I/2\). Each real-separable state has \(\langle K\rangle=0\), since the trace of a real symmetric density times a real skew operator vanishes. The \(K\) read gives \(D(\omega_\nu,\mathcal S)\ge|\nu|/2\), with equality for the comparison to \(I/4\). For \(\nu\ne0\) the extra resource crosses the real source cut. All \(\omega_\nu\) are separable over the *complex* numbers, as their diagonal chirality decomposition shows. The previous theorem uses real local preparations. A joint contact, followed by local feedback, can leave the set \(\mathcal S\) because the contact itself acts across its partition.

## A network score from all trial outcomes

Use two real \(\Phi^+\) data pairs on \(AB_1,B_2C\). Bob projects \(B_1B_2\) onto the four real Bell vectors. Each result \(b=(p,s)\) has probability \(1/4\). The corresponding \(AC\) data state has signed \(Z,X,Y\) correlations \(t_Z=(-1)^p,\ t_X=(-1)^s,\ t_Y=-t_Z t_X\). At each endpoint give the data a real reference plane, independent of the data and jointly in state \(\omega_\nu\). Use the physical symmetric matrices \(Z\otimes I, X\otimes I, J_{\mathrm{data}}\otimes J_{\mathrm{ref}}\) as the three analyzers. The first two Bell correlations retain their signs and magnitudes. The \(Y\) correlation becomes \(\nu t_Y\). All cross-axis correlations and one-site means vanish.

For each ordered pair \((j,k)=(Z,X),(Z,Y),(X,Y)\), Charlie measures \((j\pm k)/\sqrt2\). For Alice's setting \(i\), let \(d_i\) be its signed coefficient in the numerator of Charlie's observable, hence \(0,+1\) or \(-1\). For a fixed setting pair the full model law is

\[
 p(a,b,c\mid i,j{\pm}k)
 =\tfrac1{16}\left[1+
    ac\,t_i(b)d_i\,v_i/\sqrt2\right],
 \qquad (v_Z,v_X,v_Y)=(1,1,\nu).
\]

Summing the four signed correlations of each CHSH expression with Bob's indicated signs gives the total \(W(\nu)=2\sqrt2(2+\nu)\). The isolated negative-grade state yields \(2\sqrt2\), the independent mixed planes yield \(4\sqrt2\), and aligned planes yield \(6\sqrt2\). For independent planes an extra grade measurement with half the trials kept gives the last value *conditionally*. Summing both grades restores \(4\sqrt2\). All four Bob labels remain in each calculation. An acquired plane can give \(6\sqrt2\) on all subsequent trials, with the initial cross-source contact included in the physical history. The numerical check contracts the real tensor projectors and separately reconstructs every probability algebraically. [Raw settings, signs and outcomes](results/independent_source_phase.json) · [Checker](check_independent_source_phase.py)

The mixed aligned reference can also be used on fresh data in later trials. Its two diagonal chirality sectors carry conjugate gates, conjugate input data and conjugate states on every real readout branch. They give equal likelihood for the entire recorded history. All the stated instruments commute with the endpoint quarter turns, so they preserve the sector labels. After tracing out the old data the posterior reference on any nonzero record is again the equal mixture of the two aligned sectors. This gives the same per-trial outcome distribution for fresh independent Bell pairs. An instrument that measures an individual reference coordinate can consume this property. A source-independence test that assumes a product source conditional on the past excludes the retained shared reference from the outset.

Renou et al. give a numerical upper bound of \(7.6605\) in their supplementary Theorem 3 for their real independent-source network including shared classical randomness. The complex quantum value is \(6\sqrt2\). Wu et al. report \(7.83(3)\), a 5.30-standard-deviation excess against the rounded bound, using four-photon coincidences, fair sampling and space-like separation of specified events. Their six-setting endpoint and three-setting endpoint are exchanged relative to the convention above. Our four synthetic visibility settings are apparatus predictions. The experiment did not measure \(\nu\) or perform the walk contact. For the real tensor-product model, Weilenmann et al. bound distance to real-separable sources from the score alone. Their Eq. 7 uses the Bell operator range, while their numerical optimization yields sharper bounds. Neither calculation measures this apparatus-specific visibility. The inference from operational source independence to product states is itself subject to a published challenge. [Renou et al.](https://doi.org/10.1038/s41586-021-04160-4) · [Renou et al., Eq. E4](https://arxiv.org/pdf/2101.10873#page=12) · [Wu et al., Fig. 4](https://harvest.aps.org/v2/journals/articles/10.1103/PhysRevLett.129.140401/fulltext) · [Weilenmann et al., Table 1](https://arxiv.org/html/2502.20102v2) · [Hoffreumon and Woods, discussion of the independence premise](https://arxiv.org/abs/2610.03644)

## A finite signed walk can cross the same bound

Charlie can replace the irrational bisectors with the rational observables \(V=(3j\pm4k)/5\) for the same ordered pairs. The anticommuting signed involutions give \(V^2=I\). A controlled \(V\) in an \(H\)–control–\(H\) meter reads this observable. Its numerator on the acted arm uses three copies of \(j\), four of \(\pm k\) and one orthogonal junk label. The idle arm uses five identities and three junk labels. A Walsh transform over eight labels, signed selection, and inverse Walsh give successful amplitude \(5/8\) on *both* arms. The uniformity also holds for a data input entangled with Bob or the other endpoint. Alice's individual signed-axis read and Bob's real Bell measurement require only deterministic signed gates and balanced coins. [Signed rational gates and coarse failure recovery](Rational_references_and_optical_bypass.md)

If the first attempt fails, apply the inverse, read only whether the ancilla reset, apply the forward operation and recheck success. Keep every result. With \(p=25/64\), the probability still undelivered after \(1+2l\) gate calls is \(f_l=(1-p)[1-2p(1-p)]^l\). On a timeout Charlie returns a fresh fair sign. This yields zero contribution to the correlation on those trials and keeps the full trial denominator. The three delivered scores are \(2(3+4)/5,\ 2(3+4\nu)/5,\ 2(3+4\nu)/5\), so

\[
 W_l(\nu)=(1-f_l)(26+16\nu)/5 .
\]

For aligned planes the delivered score is \(42/5\). At deadlines of five, seven and nine calls the all-trial scores are approximately \(6.994912,\ 7.663838,\ 8.014306\). The seven-call value exceeds the supplementary upper bound \(7.6605\) by \(0.003338\). Nine calls give a margin of \(0.353806\). These calls count the compiled controlled-analyzer and its inverse. The initial contact, spatial delivery, local Walsh layers and physical reset/read times also cost resources. None of the settings requires an external complex phase to encode its analyzer after the planes meet. [All successes, timeouts and reversed-plane controls](results/rational_network_ports.json) · [Signed-coordinate checker](check_rational_network_ports.py)

With localized coordinate inputs, signed permutations, equal-depth balanced coins and coarse coordinate reads, each fine branch has an integer vector times a single power of \(1/\sqrt2\). Every normalized finite record probability is consequently rational. This remains true after retaining the contact transcript, Bob's two bits, the recovery transcript and the fair timeout output. It explains how a large network score can identify a cross-source resource without choosing the ordinary cyclotomic embedding. Literal comparison to an independent laboratory standard for gain labels adds an operational premise. The net result also assumes the squared coordinate readout, the availability of these controlled contacts, and their causal schedule. A microscopic origin for those assumptions and a connection to a common interacting quantum and classical limit remain open. [Native transcript theorem](Native_preparations_and_probability_embeddings.md) · [Current gate map](ontology_gate_map.json)
