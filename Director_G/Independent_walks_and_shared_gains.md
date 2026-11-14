# Can independent walks share a single sheet record?

**Kirtus Justus**, Theoretical Physicist, Port Coquitlam, British Columbia, Canada. Research supplement by Director G (OpenAI Codex).

Two distinguishable walkers can be prepared separately and read at two named ports. Suppose their probabilities multiply and the joint detector retains only the product of their two signs and the **sum** of their two cyclic residues for each pair of paths. Under the single-walk continuation assumptions, both walkers must then use the same pure probability rule. It may be counting or any one folded character. The test takes six ticks for sheet orders indivisible by four. For orders divisible by four, a second test taking eight ticks separates counting from the quarter-frequency character. A detector retaining **both** residues has a different set of possible laws. [Single-walk preparation theorem](Preparing_signed_sheet_residues.md) · [Separate residue registers](Joint_residue_masks.md) · [Local contact records](Local_contact_and_joint_sheet_records.md)

## Apparatus and assumptions

Each walk starts at well 0 on rail R with positive sign and residue zero on a ring of $4M$ wells, $M\ge3$. Both daughters of a departure at $x$ gain $\lfloor x/2\rfloor\bmod M$. R moves right, L moves left, and only L after L changes sign. A time-dependent filter keeps a set of whole wells. Record the probability per original pair of launches. In the comparisons below all filters finish at the same time and port, and the same fixed readout is used across settings.

For walker $X=A,B$, the single-walk theorem starts with additive nonnegative stationary endpoint scores depending on the signed multiset, and common unrestricted one-tick continuation. For a multiset $U$ at one port, the normalized probability after $T$ steps is $2^{-T}F_X(U)$, where

$$
F_X(U)=\sum_i\lambda_i^X f_i(U),\qquad
f_*(U)=|U|,\qquad
f_s(U)=\left|\sum_{(\epsilon,j)\in U}\epsilon\,e^{2\pi i sj/M}\right|^2 .
$$

Here $\lambda_i^X\ge0$ sum to one. The labels $s=0,\ldots,\lfloor M/2\rfloor$ fold the two conjugate characters together. We permit the two sources to have different weights. Form the multiset $U*V$ of products $(\epsilon\eta,j+k\bmod M)$ over every ordered pair from $U,V$, with multiplicity. Each pure score satisfies $f_i(U*V)=f_i(U)f_i(V)$. **Product independence** requires $4^{-T}F_A(U)F_B(V)$ on separate preparations. **Sufficiency of the summed residue** requires equal joint probabilities whenever the two preparations have the same $U*V$ at the same time and ports. This second assumption restricts what information the apparatus can retain. No polynomial form for its joint detector is assumed. [Derivation and preparation costs](Preparing_signed_sheet_residues.md)

## Three settings with one joint record

Let $e=(+,0)$. Put $B=5e$ and let $H$ contain three copies of $e$, one $(-,0)$ and one $(+,1)$. Write $b_i=f_i(B)$, $h_i=f_i(H)$. The count has $b_*=h_*=5$. For each character, $b_s=25$ and

$$h_s=|2+e^{2\pi i s/M}|^2=5+4\cos(2\pi s/M).$$

All $b_i,h_i$ are positive. The ratios $r_i=h_i/b_i$ separate every folded label. The character ratios decrease strictly with $s$ from $9/25$ to a value at least $1/25$, and the count ratio is one. The local inputs $B*B,B*H,H*H$ each consist of 25 words. The preparation theorem realizes all three at the same clock on R at well 0 from a single sharp launch. Denote them by $BB,BH,HH$. Products below refer to one port on each copy.

| Preparations with identical joint input | Equality required of the local laws |
|---|---|
| $(BB,HH)$, $(HH,BB)$ and $(BH,BH)$ | $F_A(BB)F_B(HH)=F_A(HH)F_B(BB)=F_A(BH)F_B(BH)$ |
| Additional calibration, $(BB,BH)$ and $(BH,BB)$ | $F_A(BB)F_B(BH)=F_A(BH)F_B(BB)$ |

The first row has exactly 625 path pairs in each setting. For residues $0,1,2$ its positive multiplicities are $250,150,25$ and its negative multiplicities are $150,50,0$. Thus equality holds for the entire signed histogram before taking a character sum.

**Purity proof.** Write $a_X=F_X(BB)>0$, and reweight the local distribution by $\rho_i^X=\lambda_i^X b_i^2/a_X$. It is still a probability distribution, with mean $m_X=F_X(BH)/a_X$ and second moment $n_X=F_X(HH)/a_X$ for the scalar $r_i$. Dividing just the first row by $a_Aa_B$ yields $n_A=n_B=m_A m_B$. Thus

$$\sum_{i,j}\rho_i^A\rho_j^B(r_i-r_j)^2=n_A+n_B-2m_A m_B=0.$$

Each term is nonnegative. Every supported pair must have the same ratio and hence the same label. Since each marginal has positive total mass, each concentrates on that one common label. The second row gives an independent calibration of the mean equality. For identical marginals the two exchanged settings in the first row are equivalent, leaving just two distinct comparisons. Conversely the common label's multiplicative score fits **every** product preparation. Pure counting, the trivial character, nonfaithful characters when present, and the ordinary folded character all pass. Testing which label the apparatus uses requires additional calibrated records. [Single-walk equal-lag comparisons](Repeating_a_position_record.md)

For different marginal weights, a single *oriented* equality may pass spuriously. At $M=4$ take A on character 1 and B with character weights $1/10$ on 0 and $9/10$ on 2. The ratios for $0,1,2$ are $9/25,5/25,1/25$. Then $n_B=m_A m_B$ but $n_A\ne m_A m_B$. Including the reversed setting prevents this error. A fair random choice between the two exchanged settings yields one operational comparison with $(BH,BH)$, provided the same readout applies after randomization and the conditional source laws remain fixed. Its exact excess in units of $4^{-T}a_Aa_B$ is half the sum of squares above. For $g_M=\min_{i\ne j}|r_i-r_j|$, the excess in these units is at least

$$\frac{g_M^2}{2}\left(1-\sum_i\rho_i^A\rho_i^B\right).$$

This bounds the probability that independent draws from the two **reweighted** distributions have different labels. The bound uses the actual frequency separation and source normalization. For equal marginal weights, the unnormalized contrast is the Gram determinant

$$
F(BB)F(HH)-F(BH)^2
=\sum_{i<j}\lambda_i\lambda_j(b_i h_j-b_j h_i)^2 .
$$

Dividing by $a^2$ gives $\operatorname{Var}_\rho(r)$. The lower bound also gives $\operatorname{Var}_\rho(r)\ge g_M^2(1-\max_i\rho_i)/2$. At $M=4$ the general compiler takes 584 ticks. These preparations have strictly positive component scores at every setting and give one common histogram for every order. The following shorter preparations allow dark outputs. The one-fiber support argument on integer-scaled weights and responses, covering finite rational panels after denominator clearing, is checked in Lean. The trigonometric separation and the proof for arbitrary real weights are given above. [Lean proof](lean/SharedGainPurity.lean)

## Six- and eight-tick tests for every sheet order

At home $x$ block C opens $\{x-1,x+1\},\{x\},\{x+1\}$ on its three successive ticks. Block I opens $\{x+1\},\{x\},\{x+1\}$. C admits RLR and LRR, I admits RLR, and each finishes on R. The signed multisets at the endpoint have the form $\delta_g * K$ and $\delta_g$, where $K$ contains one positive history at each of residues $0,-1$. Translating the home changes only $g$. At each common tick the two histories' departures have the same parity, so a two-site separation always contributes one unit of gain difference, including across the ring seam.

Concatenate the blocks at homes 0 and 1. Compare $(CC,II)$, $(II,CC)$ and $(CI,IC)$. All yield the same shifted $K*K$ at the shared detector. For a pure rule write $q_i=f_i(K)$, so $q_*=2$ and $q_s=2+2\cos(2\pi s/M)$. The three independent joint numerators are respectively $\mathbb E_A q^2$, $\mathbb E_B q^2$ and $\mathbb E_A q\,\mathbb E_B q$. Half the first two minus the third equals $\tfrac12\sum_{ij}\lambda_i^A\lambda_j^B(q_i-q_j)^2$. Thus equality forces agreement of $q_i$ for every pair of supported labels even at a dark port. All folded characters have distinct $q_s$. Counting collides with a character precisely when $4\mid M$, at $s=M/4$.

For those orders use a second panel. Block D opens the successive well sets $\{-1,1\},\{0,2\},\{1\},\{2\}$ relative to home. Its only words are RRLR, RLRR, LRRR. They all have positive sign and final rail R. Relative to RRLR their residues are $0,-1,-2$. Block J forces RRLR using one well per tick. Translate both blocks by 2 for the second slot. The three settings $(DD,JJ)$, $(JJ,DD)$, $(DJ,JD)$ now have the same shifted joint histogram. The response of D relative to J is 3 for count and $(1+2\cos(2\pi s/M))^2$ for a character. At $s=M/4$ it is 1. The pair of panels therefore separates all folded labels at every order. At fixed $M$, both controls in each comparison share identical clocks and specified ports. Dark records and failed masks count in the per-launch probability.

At $M=4$, $(CC,II)$ and $(CI,IC)$ both have positive residues $0,1,2$ with multiplicities $1,2,1$. With equal weights on count and the trivial square, the local numerators for $CC,II,CI,IC$ are $10,1,3,3$. The two independent probabilities are $10/4096$ and $9/4096$. Any common prediction must miss at least one by $1/8192$. With equal weights instead on count and the quarter-frequency square, all three six-tick numerators are 4. The eight-tick numerators are $5,5,4$ at the same shared eight-tick histogram, giving a per-launch contrast $1/65536$. The exact calculation tested all 144 ordered pairs of marginal laws in the order-four panel. Only the four common pure laws passed both tests. Setting-dependent efficiencies, renormalization on survival or retaining separate local counts change the comparison. No joint flux has been measured here. [Checker](check_product_gain_fibers.py) · [Exact words, histograms and probabilities](results/product_gain_fibers.json)

## Joint records in free classical flight

There is an independent way to probe the distinction between two incident mixtures. Consider the signed **line** walk and the binary central or moving apertures of the free-flight theorem. Write $C_i,Q_i$ for their per-launch counting and square success probabilities, and $\alpha$ for the incident counting fraction. Draw a single count-or-square label for the pair and then prepare the two walkers independently given that label. Against independent label draws with the same marginals, the joint excess is exactly

$$
\alpha C_1 C_2+(1-\alpha)Q_1Q_2-
[\alpha C_1+(1-\alpha)Q_1][\alpha C_2+(1-\alpha)Q_2]
=\alpha(1-\alpha)(C_1-Q_1)(C_2-Q_2).
$$

The shared draw defines a different source. Positive or negative excess compares those two source models, with the local probabilities held fixed. In the scaling $\delta=T^{-5/14},\ w=\delta^{11/10}$, central counting success tends to one, moving counting success is smaller than any fixed power of $w$, and both square success rates are asymptotic to $\kappa w$, $\kappa=2/\pi$. The joint excess tends to $\alpha(1-\alpha)$ for two central windows. For one central and one moving window it is asymptotic to $-\alpha(1-\alpha)\kappa w$, and for two moving windows to $\alpha(1-\alpha)\kappa^2 w^2$ when $0<\alpha<1$. For a central–moving pair, the shared draw gives joint yield of order $w^2$ while independent draws give order $w$. The conditioned individual free rays alone miss this difference. [Free-flight preparation, success rates and scope](Count_weight_in_classical_flight.md)

At $T=1024$, $\alpha=1/2$, the exact saved single-launch numerators give a **positive** excess of about $0.0530001$ for the central window paired with the $p_0=1$ window. Substituting the $p_0=2$ window gives $-0.0117051$. The sign reversal at finite depth is retained. These predictions concern position records under the stated source couplings. They supply neither a force law for the pair nor measurements of a common latent mechanism. [Finite apertures and integer denominators](results/count_flight_windows.json)
