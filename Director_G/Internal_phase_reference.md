# A phase reference prepared by the signed walk

**Kirtus Justus**, Theoretical Physicist

Port Coquitlam, British Columbia, Canada

Mathematical development and computational review by Director G (OpenAI Codex).

The walk can choose a physical sheet translation whose limiting interference profile gives the ordinary squared modulus of every rational polynomial in a primitive root of unity. It can do this on one initially localized register, retain that register for a subsequent experiment, and compare references of different odd orders. What remains undetermined is whether an *independently named* algebraic root denotes the translation so obtained. Every candidate probability embedding gives the same distribution of the chosen translation and of the subsequent native records.

## A reference on one fixed graph

Use a ring of $2K$ sites with $K\ge3$ and two directions and a sheet $y\in Y=(\mathbb Z/M)^d$, where $M\ge3$ is odd and $d\ge1$. Start at a specified site, direction and sheet. On departure from $x$, add $g(x)$ to the sheet, apply the real signed Hadamard coin (the minus entry is $L\to L$), then move by the outgoing direction. Measure site and direction together and leave the sheet unread. All probabilities below use the basis-record law established conditionally in the program. [Persistent-record assumptions](Fixed_transport_and_record_weights.md)

From site $x$ with incoming direction $c=\pm1$, read the output after three ticks. The two histories at port $(x-c,-c)$ have opposite signs; those at $(x+c,c)$ have equal signs. The two histories at either port differ in sheet translation by $h=g(x+1)-g(x-1)$, up to orientation. The other four paths reach distinct site-direction ports, including when $2K=6$. On character $k\in Y$, the probability of the destructive port is

$$
 p_k(h)=\frac{|1-\exp(2\pi i\, k\cdot h/M)|^2}{8}
       =\frac{1-\cos(2\pi k\cdot h/M)}4. \tag{1}
$$

The constructive probability is $(1+\cos(2\pi k\cdot h/M))/4$. Each single path has probability $1/8$. Throughout, the setting $h$ denotes the *difference of the paths’ translations*. A linear departure rule with slope $v$ has $h=2v$. These conventions assign different names to the lower five-sheet mode. [Exact physical-coordinate paths](results/internal_reference.json)

Fix a list $h_0,\ldots,h_{K-1}$ with sum zero in $Y$. Set $g(2j)=0$ and $g(2j+1)=\sum_{\ell=0}^j h_\ell$. Then site $2j$ supplies exactly $h_j$, including across the periodic boundary. A full list of all $M^d$ settings has sum zero by pairing with negatives. It uses one fixed assignment of departure gains for the entire calibration.

After a block, read site and direction after each individual tick until the next designated centre is reached. Each such step has conditional probability $1/2$ in either direction and acts on the sheet by a single common translation and sign. Routing preserves the relative weights of the characters. From distance $j$ around a ring of length $2K$, the fair-walk mean time to one specified site is $j(2K-j)\le K^2$, by the discrete hitting-time recurrence with endpoints 0 and $2K$. Routing succeeds almost surely. A deadline gives a separate recorded outcome. No timeout is silently reassigned.

The localized sheet has equal squared Fourier coefficients $M^{-d}$. Each sheet-blind instrument in this protocol preserves character subspaces. At a full base read, the state in each subspace has just one base coordinate. Consequently its next dark indicator has law (1) regardless of the previous outcomes, once the setting and the same $k$ are fixed. The entire transcript can be computed by first drawing a uniform $k$ and then sampling these conditional records. This is a representation of this measurement law. It requires no physical postulate that a character existed as a hidden classical state. Character decomposition of lifts and repeated nondemolition readout supply related mathematical results. [Dalfó, Fiol and Širáň](https://arxiv.org/abs/1707.04463) · [Bauer and Bernard](https://arxiv.org/abs/1106.4953)

## Which translation does the walk select?

Let $f(u)=\min(u\bmod M,(-u)\bmod M)$. Equation (1) increases strictly with $f(k\cdot h)$. The image of $h\mapsto k\cdot h$ has order $H=M/\gcd(M,k_1,\ldots,k_d)$, and its profile contains $(H+1)/2$ distinct levels. Accept when the full menu has $(M+1)/2$ levels. Report the first setting $h_*$, in a fixed ordering, in the lowest positive level. Thus a correctly accepted register satisfies

$$
 k\cdot h_*=\epsilon=\pm1\bmod M,\qquad
 D(t):=p_k(th_*)=(1-\cos(2\pi t/M))/4. \tag{2}
$$

The probability of a surjective character in the localized input is

$$
 P_{M,d}=\prod_{p\mid M,\;p\ {\rm prime}}(1-p^{-d}). \tag{3}
$$

For each prime dividing $M$, the only forbidden case has all coordinates zero modulo that prime. The Chinese remainder theorem makes these restrictions independent. Surjectivity is onto the cyclic phase group; a multidimensional sheet generally has a nontrivial kernel. The ideal identification yield on five sheets is $4/5$ for one register, $24/25$ for two and $124/125$ for three. A protocol that insists on one preassigned conjugate pair on one localized register has prior mass only $2/5$. The higher yield in (3) comes from reporting and reusing a *measured choice of translation*. On two registers the yield is $8/9$ at order nine and $64/75$ at order fifteen.

Two registers also suffice for a yield bounded away from zero along *every* sequence of odd orders. In (3), enlarge the product from the prime divisors of $M$ to all integers $j=3,\ldots,M$. Each added factor is below one. The enlarged product at $d=2$ telescopes to $2(M+1)/(3M)$, giving a uniform lower bound of $2/3$ for every $d\ge2$. Thus the accepted wrong fraction tends to zero whenever the finite error bound below tends to zero, even if new prime divisors continue to appear. The number of calibration blocks can still grow rapidly.

The full menu also fixes signed *relative* exponents. For a new $h$, write $u=(k\cdot h)/\epsilon\bmod M$. Its folded rank and the folded rank of $h+h_*$ give $f(u)$ and $f(u+1)$. The first leaves at most $u,-u$. If both candidates give the same second value, then $u+1\equiv -u+1$ or $u+1\equiv-(-u+1)$; the first identifies the candidates and the second would imply $2\equiv0\bmod M$. Either orientation of the reference works. [General Lean statement](lean/InternalReference.lean)

### Fewer physical settings for large registers

Write $M=\prod_p p^{a_p}$. For each assignment of one coordinate $i(p)\in\{1,\dots,d\}$ to each prime, form a vector $v$ that equals the basis vector $e_{i(p)}$ modulo $p^{a_p}$. Include the entire list $tv,\ 0\le t<M$, for every one of the $J=d^{\omega(M)}$ assignments. The $K=MJ$ listed settings sum to zero, so the same fixed-graph construction works, including repeated settings. If $k$ is surjective, choose $i(p)$ with $p\nmid k_{i(p)}$. Then $k\cdot v$ is a unit. Conversely, a line attaining all $(M+1)/2$ levels implies surjectivity. Test each line separately, choose the first complete line, and report the first rank-one multiple on it. This smaller menu supplies all multiples of the selected reference. Arbitrary off-line signed decoding additionally needs sites for $h,h+h_*$.

Composite orders require this qualification. For instance $k=(3,5)\bmod15$ is surjective even though neither coordinate is a unit. The exhaustive checks include such tuples and verify the signed path differences on the physical graphs through $M=105,d=2$. [Construction and exhaustive checks](check_reference_comparison.py) · [Results](results/reference_comparison.json)

## Accuracy at finite cost

At each of $K$ settings, use $n$ three-tick blocks, keeping every outcome. Adjacent possible rates are separated by at least $\tfrac12\sin^2(\pi/M)\ge 2/M^2$. This follows by subtracting consecutive cosines in (1) and applying $\sin x\ge2x/\pi$ for $0\le x\le\pi/2$. If all empirical rates have error below $1/(3M^2)$, sorting them and separating consecutive values at gaps exceeding $1/M^2$ recovers the true ordered clusters. The controller uses only counts and rational comparisons. Conditional independence and the union bound give a probability of any inaccurate rate of at most

$$
 \eta=\min(1,2K\exp[-2n/(9M^4)]).
$$

Thus the correct accept mass is at least $P_{M,d}-\eta$, the wrong accept mass at most $\eta$, and the total accept mass lies within $\eta$ of (3). When $\eta<P_{M,d}$, the wrong fraction among accepts is at most $\eta/(P_{M,d}-\eta)$. These are joint-sample guarantees, averaged over all accepted transcripts. For a global budget of $B$ ticks, the timeout probability is at most $nK(3+K^2)/B$ by the mean routing bound. Add it to the error budget when timeout rejects. These bounds are sufficient and can be loose. [Hoeffding’s bounded-variable inequality](https://doi.org/10.1080/01621459.1963.10500830)

An exact short test at $M=5,d=1$ uses 16 blocks at $h=1$ and 16 at $h=2$. Select the setting with fewer dark outcomes and reject every tie, including the trivial sector. All 289 count pairs sum to one. Acceptance is **0.7738719426**, the wrong gain fraction among accepts is **0.0251790845**, and the next observed dark probability at the selected setting is **0.1797835195**. The ideal low rate is $(5-\sqrt5)/16$. The finite next-record probability is rational. The posterior error refers to the character decomposition and the subsequent dark rate can be measured directly. An independent eight-path evaluation fixes the named $h=1$ lower rate at $k=\pm1$, and checks the likelihoods of both conjugate pairs at every count pair. The first run used the doubled departure-slope index. Its aggregate record probabilities agreed while its named sectors were interchanged. [Corrected finite table and port oracle](results/internal_reference.json) · [Retained first run](results/internal_reference_first_index.json)

## What can be measured with the reference?

For any rational polynomial $A(z)=\sum_j a_j z^j$, measure the profile on retained registers and form

$$
 \sum_{ij}a_i a_j[1-4D(i-j)] = |A(e^{2\pi i/M})|^2. \tag{4}
$$

The identity holds on correctly calibrated components by pairing the conjugate terms in the squared modulus. Replacing the second factor $a_j$ by $b_j$ recovers the real part of $A\overline B$. Estimation uses finitely many settings for each polynomial. If a finite accepted ensemble has wrong weight $\lambda$, its mean dark rate at any multiple differs from (2) by at most $\lambda/2$, since every rate is between zero and $1/2$. Sample that ensemble on independently calibrated accepted registers. A uniform sampling error $e$ around the ensemble means gives error at most $4(e+\lambda/2)(\sum_j|a_j|)^2$ for (4). A long follow-up on just one retained register instead estimates its own conditional profile. Rational coefficients permit a common denominator. Since $\mathbb Q[\zeta_M]$ is already a field, (4) covers the entire cyclotomic field in the variable defined by the experiment. Preparing an arbitrary amplitude $A$ coherently is a separate operational claim.

The reference must persist. On a localized five-by-five sheet the marginal dark probability at every nonzero $h$ is $1/4$. Two dark outcomes at the same setting have joint mass $3/32$ on the retained sheet, versus $1/16$ with fresh sheets. For settings $e_1,e_2,e_1+e_2$ the three pairs each have zero covariance, yet all three dark outcomes have probability $3/256$ on one sheet and $1/64$ on three fresh sheets. Character orthogonality and signed integer sheet counts agree on these fractions. They directly distinguish preservation of the register from resetting it. [Record controls](results/reference_comparison.json)

For two odd orders $M\mid N$, calibrate their initially localized registers on the same path with the other register a spectator. Allow joint diamond settings on their product. Put all required settings for every possible reported reference and their negatives into the fixed graph before the run. Given correct calibrations $h_M,h_N$, the two joint settings $(h_M,\pm(N/M)h_N)$ have dark probabilities $0$ and $q=(1-\cos(4\pi/M))/4>0$ in some order. A null at $(h_M,-s(N/M)h_N)$ gives $\epsilon_M=s\epsilon_N$. It identifies which orientation of the order-$N$ reference, raised to $N/M$, agrees with the order-$M$ reference. With $L$ repetitions per sign, the probability of seeing neither sign fire is $(1-q)^L$ conditional on correct calibration. Keep that inconclusive outcome. This gives a relative refinement comparison at every specified finite pair. Each comparison requires a coherent common path and access to both product gains. [Signed comparisons for four refinement pairs](results/reference_comparison.json)

### Transfer to an interaction

Suppose the record controller can freeze its reported $h_*$ as a gain for a subsequent experiment on the retained sheet. A departure previously assigned the integer $b$ now translates the sheet by $b h_*$. On every correctly selected component the induced phase is $\exp(\pm2\pi i b/M)$. Launch the *same* base preparation on every good branch, up to conjugation, and use character-preserving instruments depending on $k$ only through $k\cdot h_*$, with conjugate operations in the two orientations. These hypotheses hold for a common real-coordinate preparation, real base coins, this integer transport and sheet-blind base readout. A separate fresh base coupled to the retained sheet is one way to standardize the launch. A different real direction for each accepted transcript alone would violate the common-input condition.

Let $\lambda$ be the wrong mass conditional on calibration acceptance, and $Q$ the future transcript law of the standardized fixed-character experiment. Orthogonality under the sheet trace and equality of the conjugate branches give the accepted future law $(1-\lambda)Q+\lambda R$ for some probability law $R$. Its total-variation distance from $Q$ is at most $\lambda$ for the full subsequent record at any flight time. A further herald $E$ can increase the wrong weight to $\lambda R(E)/[(1-\lambda)Q(E)+\lambda R(E)]$. A rare band herald must therefore enter the joint error budget.

This gives a way to supply the effective unit gain in the program’s two-body quantum and classical comparison. It requires a programmable flight after the fixed-graph calibration, the original shared-sheet interaction, and its specified base packet or conjugate pair. Along a sequence of orders the calibration error must tend to zero and the training time lies outside the flight. A folded input retains its own mixture of rays. Spatial locality of the two-position gain, single-band preparation, the clock and empirical correspondence remain physical obligations. [Two-body model and its two limits](Periodic_interaction_and_two_limits.md)

## Which embeddings survive?

Write $\zeta=e^{2\pi i/M}$ for the mathematical Fourier convention. For any unit $a\bmod M$, replace $\zeta$ with $\zeta^a$ and $k$ with $a^{-1}k$. Every phase at every fixed physical translation is preserved. This includes $h_*$, since the controller computes it solely from the same record. Even protocols with actual named-sheet reads, which can mix Fourier sectors, retain the more general physical-coordinate proof. On each synchronized finite branch the state has integer signed counts times a common $2^{-t/2}$, and its mass is $2^{-t}\sum_y m_y^2$ with the sum over complete output cells. The sign change of $\sqrt2$ is global there. Cylinder equality determines the law on the sigma-algebra of complete countably long transcripts, including adaptive stopping records. The native finite record field for deterministic protocols is $\mathbb Q$; identical external classical randomization preserves equality. Ordered irrational limiting profiles in (2) coexist with that invariant. [Full protocol theorem](Native_preparations_and_probability_embeddings.md) · [Relational information without a shared reference](https://arxiv.org/abs/quant-ph/0302111)

Two controls locate the missing resource. On three real modes, admit a balanced Hadamard on a chosen pair and a *phase-fixed coherent identity* on its complement. For an input $e_0$, the sequence $H_{01},H_{12},H_{01}$ yields probabilities $(3+2s\sqrt2)/8,(3-2s\sqrt2)/8,1/4$, with $s=\pm1$ the embedding sign. Alternatively, on a three-site, three-sheet walk of departure gain $g(x)=x$, only the right-right-right path returns to $(1,R,0)$ in three ticks. Coherently interfering the identity arm with those three ticks gives one control port probability $1/2+s\sqrt2/8$. Keeping a distinguishing record of the arms gives $1/2$. Both circuits require a specified relative phase between acted-on and bypassed amplitudes. A synchronized native walk supplies a common number of coin factors. Even these enlarged circuits have physical-coordinate entries in $\mathbb Q(\sqrt2)$, so their data leave the independent cyclotomic relabeling intact. [Lean clock calculation](lean/InternalReference.lean) · [Physical implementation of controlled unitaries](https://arxiv.org/abs/1309.7976)

If an independent source also prepares the *specified* tagged vector $(e_0+\zeta_5e_1)/\sqrt2$, a real balanced mixer gives port-zero probabilities $(3+\sqrt5)/8$ and $(3-\sqrt5)/8$ under the two real cyclotomic choices. Combined with the bypass test, this distinguishes four real-field embeddings at order five. Tagging the source using (2) applies the same relabeling to the tag, restoring equality. Simultaneous complex conjugation of the whole apparatus preserves squared moduli in either case.

Two PCP parent models ran overlapping jobs and each called a local child model. Their named-port and bypass proposals were checked with signed path counts and exact algebra. One child gave a correct port probability with an unsupported interpretation; another gave incorrect numbers. The worker record includes the original rejected delegation and its rerun. The finite algebra, scoped Lean theorems and numerical checks concern the specified mathematical instruments. Physical selection of their preparation and readout, and an identification of the probability embedding for an independently named field, remain open. [Worker trials and dispositions](results/embedding_worker_reviews.json) · [Program gate map](ontology_gate_map.json)

A [synchronized rational rotation](A_rational_plane_for_cyclic_phase.md) supplies a two-coordinate comparison plane with a declared orientation. Repeated records establish a relative phase and subsequent reads resolve its signed sine as well as its cosine.

On a four-site base ($K=2$), the other four histories can collide in pairs even though the stated dark and bright laws survive for the reviewed lists. At five sheets the opposite stroke gives the same retained two-dark probability $3/32$ as the named stroke. These boundary checks were made by the review queue on the earlier text. [Cross-review, including failed boundary predicate](https://github.com/KirtusJ/From-Prephysical-Hypotheses-to-Physical-Models/blob/e37e86fa1ec9e424c8cd8d98a8000d717852f6f3/REVIEW_QUEUE/reports/2026-11-13_pcp-cross-reviewer_Director_G_Internal_phase_reference.md)
