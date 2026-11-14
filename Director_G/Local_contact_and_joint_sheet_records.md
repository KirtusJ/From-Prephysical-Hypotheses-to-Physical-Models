# A local contact reads the relative orientation of two cyclic sheets

**Kirtus Justus**, Theoretical Physicist, Port Coquitlam, British Columbia, Canada. Research supplement by Director G (OpenAI Codex).

Two distinguishable walkers leave the same well, each with its own signed cyclic sheet. Measurements made separately on them cannot tell whether one walker's character has been conjugated. After two ticks, both walkers can return to the launch well with their branch information still present in their arrival rails. One local comparison, followed by one ordinary tick, distinguishes matching and opposite orientations. At sheet order four, the same named detector is dark in one case and has probability $1/16$ per double launch in the other. A family of such contacts recovers every orientation contrast allowed by simultaneous conjugation. These are predictions for a coherent detector with a specified score law. [Single-sheet masks and detector laws](Preparing_signed_sheet_residues.md) · [Independent preparation and shared gains](Independent_walks_and_shared_gains.md)

## What separate records can identify

The two walkers A and B begin on R and advance synchronously. Each has a $4M$-site ring and gains $g(x)=\lfloor x/2\rfloor\bmod M$ on departure, with a minus sign only for L following L. A joint history retains its two residues $(j,k)$ and the product of its signs. Suppose a double-launch endpoint score is a normalized mixture of one global count term of weight $c$ and coherent squares evaluated at characters $(s,t)\in\mathbb Z_M^2$. Their weights sum to $1-c$. A coherent component evaluates a signed history as $\epsilon\exp[2\pi i(sj+tk)/M]$. The score of a two-walker history event at depth $T$ is divided by $4^T$. The companion construction specifies its preparation and continuation premises. Here the observable consequences use this family as a premise. [Preparation on two separate residues](Joint_residue_masks.md)

Write $[s,t]$ for the orbit $\{(s,t),(-s,-t)\}$ and $b_{[s,t]}$ for its total weight, counted once also when the orbit is a singleton. Joint squared scores have this symmetry because all history multiplicities and signs are real. A Cartesian event selects one set of paths on A and one on B independently. Its coherent probabilities factor as $|A_s|^2|B_t|^2$. Each factor is separately even in its own frequency. Consequently Cartesian data combine $[s,t]$ with $[s,-t]$. If either frequency is self-conjugate (zero, or $M/2$ at even order), these are already the same orbit. When neither is self-conjugate they are two different orbits, even if the two frequency magnitudes happen to be equal. The distinction between the A and B apparatuses fixes the order of the two coordinates.

Let $f=\lfloor M/2\rfloor+1$ count folded frequencies and $u=\lfloor(M-1)/2\rfloor$ count positive representatives of non-self-conjugate pairs. The coherent Cartesian rank is $f^2$ and the full joint coherent rank is $f^2+u^2$. Each of the $u^2$ pairs of non-self-conjugate magnitudes loses exactly one difference of weights. Local two-word preparations generate the cosine basis on each axis, so the stated Cartesian rank is attained. A cancelling signed pair and a singleton separate the count from the coherent basis, giving ranks $1+f^2$ and $1+f^2+u^2$ in the global-count model before imposing normalization. At $M=4$ the coherent ranks are 9 and 10. At $M=5$ they are 9 and 13. For differing sheet orders the same Fourier algebra gives $f_A f_B$ and $f_A f_B+u_A u_B$; the physical census here uses equal orders. [Exact rank calculations and local input basis](check_joint_phase_records.py)

## The three-tick record

Launch both walkers from $(0,R)$. At tick two retain their joint return to zero. For each walker the possible words are RL and LR. They both have positive sign. They arrive on L and R respectively, with residues $0$ and $-1$. Thus equality of the incoming rails at this single physical site is exactly equality of the first directions on the return branch.

A blank three-state pointer at zero can record failure, equal or different. At joint contact add 1 modulo 3 to its value for equal incoming rails and 2 for different rails. Elsewhere leave it alone. This reversible controlled permutation needs access to both distinguishable local residents and their rail states. Read or retain the pointer as an orthogonal record, keeping each pair of histories within a recorded value coherent. The probability calculation assumes that this writer merely labels the admitted histories and that the same endpoint score applies separately to each terminal pointer value. An instrument with a new mixed-pointer response would need a separate calibration. Compare the incoming rails **before** the next Hadamards. A register recording which of LL and RR occurred would retain more information and spoil their interference. Reading both first directions and later comparing the classical answers would implement that more resolving instrument. The position and pointer operations require time. A separate contact microstep must be included if the apparatus cannot act during the tick boundary. [Local contact controls](Phase_contact_and_shared_walks.md) · [Mixed-pointer calibration limits](Tag_sector_controls.md)

At tick three take the named terminal port $(+1,R;+1,R)$. For either pointer record it receives two histories out of 64. In the equal record the residue pairs are $(0,0),(-1,-1)$; in the different record they are $(0,-1),(-1,0)$. Every contribution to this port has positive sign. A pure character $(s,t)$ gives

$$
 P_{\rm eq}=\frac{1+\cos(2\pi(s+t)/M)}{32},\qquad
 P_{\rm diff}=\frac{1+\cos(2\pi(s-t)/M)}{32}.
$$

Both figures are per double launch. On the selected four-history return, either pointer record has unconditional mass $1/8$ summed over its four exits. The other $3/4$ of launches fail the common return under these laws. Each accepted outcome, including a dark terminal port, agrees with the corresponding early first-direction comparison followed by the return masks. An actual sole tick-one equality read would also accept histories that fail to return.

| Component | Order | Equal record, RR exit | Different record, RR exit |
|---|---:|---:|---:|
| $(1,1)$ | 4 | 0 | $1/16$ |
| $(1,-1)$ | 4 | $1/16$ | 0 |
| $(1,1)$ | 5 | $(3-\sqrt5)/128$ | $1/16$ |
| $(1,-1)$ | 5 | $1/16$ | $(3-\sqrt5)/128$ |
| Count, or a permanent first-direction record on either walker | 4 or 5 | $1/32$ | $1/32$ |

Counting is a **zero contrast**, with positive probability in both named bins. At order four the *unflagged* RR port also gives $1/16$ for either coherent orientation and for count. The qutrit's timing is consequential: writing it after the outgoing coin assigns all four histories reaching RR the same equal label. A rail-name reversal on only one incoming discriminator exchanges its two recorded values. A single surviving incoming LR pair goes entirely to the different record; the two herald probabilities need not be equal on other preparations. [Short panels, signed residue bins and pointer controls](results/joint_phase_records.json)

## Contacts at every pair of lags

For each requested residue lag $r$, take the two equal-sign words of the one-walker lag construction. Remove their common last R step. The words now end at the same well on opposite rails, L for the upper word and R for the lower. Removing a shared departure leaves the difference of their staircase gains unchanged. Prepend a forced singleton-position word ending on R so the pair arrives at the contact well at a common depth $T$ for all settings. For a truncated word of length $n$ and displacement $q$, the prefix must move $d=y-x-q$ if the source well is $x$ and the contact is $y$. Choose $T-n\ge |d-1|+1$ with $T-n\equiv d\pmod 2$. A prefix of the required length ending on R then exists. Its sign and gain are common to the two alternatives. Translating the split preserves the gain difference because the two arms at each departure are separated by an even number of wells. The checker returns each pair to its physical source well and also starts at the ring seam. A synchronous joint contact from distinct launch wells requires compatible spatial parity. [Lag words and common-clock construction](Repeating_a_position_record.md) · [Physical paired histories](check_joint_phase_records.py)

Program lag $r$ for A and $v$ for B. Use separate position masks during the flights and the same local pointer at the meeting. Define the coherent moment

$$
 C(r,v)=\sum_{[s,t]} b_{[s,t]}\cos[2\pi(sr+tv)/M].
$$

Put $\chi=+1$ if the two outgoing rails agree and $-1$ if they differ. One more native tick gives the following probabilities for each *specified* outgoing rail pair:

$$
 P_{\rm eq}=\frac{1+\chi C(r,v)}{2\,4^T},\qquad
 P_{\rm diff}=\frac{1+\chi C(r,-v)}{2\,4^T}.
$$

The two alternatives in each pointer class have equal signs on RR. Switching only one outgoing rail changes their relative sign. Summing the four exit probabilities gives $2/4^T$ for each herald and $4/4^T$ for either. Conditioning on a successful herald divides out this cost. In the count-plus-square family $C(0,0)=1-c$, so an absolute zero-lag calibration also fixes $c$. A calibrated rail-parity contrast within each herald gives the same $C$. Uncontrolled relative efficiencies of the four exit detectors or of the two pointer values need their own calibration. The archive contains the complete two-history RR bins for all lag pairs at $M=3,4,5,6,7,8,9,12$, for two source wells, and checks the alternative early filter separately. [Inputs, clocks, denominators and rank checks](results/joint_phase_records.json)

Choose $1\le s,t\le u$ and write $\Delta_{st}=b_{[s,t]}-b_{[s,-t]}$. The measured difference

$$
 D(r,v)=\frac{C(r,-v)-C(r,v)}2
 =\sum_{s,t=1}^u\Delta_{st}\sin(2\pi sr/M)\sin(2\pi tv/M)
$$

has no self-conjugate contribution. Multiplication by the two corresponding sine factors and summation over $r,v=0,\ldots,M-1$ gives each $\Delta_{st}$ with inverse factor $4/M^2$. Together with the Cartesian sums, these $u^2$ numbers give the two orbit weights individually. Equivalently the complete real joint Fourier moments determine the weights on simultaneous-conjugacy orbits. A simultaneous reversal of both orientations leaves every result unchanged. Access to a named physical sheet step, stable control of the signed masks and reproducible preparations are required to transfer inferred labels across experiments. [Single-sheet calibration and its physical scope](Counting_and_character_records.md)

## When each source chooses a response independently

Which products of local laws does the **classified joint family** realize on all Cartesian records? Let $c_A,c_B$ be the local count probabilities. Let $a_i,d_j$ be the weights of the folded coherent frequencies, with $\sum_i a_i=1-c_A$ and $\sum_j d_j=1-c_B$. In the joint family write $B_{ij}$ for the total coherent weight above the ordered folded pair $(i,j)$. The independent local response columns are the count and the folded squares. Their tensor products are linearly independent on independently programmable Cartesian inputs. Indeed both local evaluation matrices have full column rank by the cancelling-pair, singleton and cosine preparations above. Equality of the joint law with the product of the local laws on every such input is therefore equivalent to equality of **each coefficient**:

$$
 c=c_Ac_B,\qquad c_A d_j=0\ (\text{all }j),\qquad a_i c_B=0\ (\text{all }i),\qquad B_{ij}=a_i d_j.
$$

The two sets of zero coefficients follow because the classified family contains only global counting and coherent joint characters. Summing gives $c_A(1-c_B)=(1-c_A)c_B=0$. There are exactly two cases. Both local laws and the joint law are pure counting, or both local count probabilities and the joint count probability vanish and $B$ is the outer product of the two local folded distributions. Conversely either case gives the required product on **every** Cartesian event. In the second case each folded distribution may have several frequencies. For a pair $i,j$ with neither frequency self-conjugate, the aligned weight can take any value in $[0,a_i d_j]$ and the opposite weight takes the remainder. Thus $-a_i d_j\le\Delta_{ij}\le a_i d_j$ is sharp, even when a local distribution has zero entries. A self-conjugate index leaves just one orbit. The local contact can resolve the free split. Pooling the two sheet gains into their sum before readout changes the premise and yields the stronger shared-register purity result. [Comparison with the pooled register](Independent_walks_and_shared_gains.md)

In a different composition model, each source can independently choose counting or a coherent character. A realization of local counting stores that walker's path as a permanent distinguishable record. In either contact class, the two alternatives differ on **both** walkers. An archive on only A or only B therefore kills the cross term at this port, and count–character, character–count and count–count all give the same flat two-word rate. Only the coherent–coherent part contributes to the orientation difference. On Cartesian events the mixed responses can be separated: the count plus folded coherent responses supply $f+1$ independent local columns per side, or $(f+1)^2$ Cartesian columns for unrestricted joint component weights. Strict independence further requires those weights to factor. For example with $c_A=1/3$, $c_B=2/5$, and matching unit orientations whenever both are coherent, coherent–coherent has weight $2/5$. At order four the equal and different RR probabilities become $3/160$ and $7/160$. Unflagged Cartesian agreement alone cannot select an extension to a joint contact. [Independent-product scores and their comparison](Independent_walks_and_shared_gains.md) · [Mixed and archived-path controls](results/joint_phase_records.json)

## An optical network comparison

Renou et al. showed that two independent quantum sources and a joint Bell measurement can test the standard real tensor-product formalism even when shared classical randomness is allowed. A common real quantum reference across the source cut changes that premise. A simultaneous complex conjugation of states, measurements and operations preserves their joint probabilities. The present walk makes the residual *relative* orientation observable with a specified contact and a calibrated sheet label. [Renou et al.](https://doi.org/10.1038/s41586-021-04160-4) · [Real reference planes and the earlier Wu experiment](Network_phase_and_probability_records.md)

Li et al. used two separately pumped, phase-randomized optical sources with a shared classical trigger. Bob chose one of four binary Bell projections and recorded its positive result. Alice measured the $X,Y,Z$ Pauli axes and Charlie the six bisectors of their three axis pairs. The authors combined 72 herald-weighted correlations and subtracted a term proportional to the four herald probabilities. They estimated the latter from singles, twofold and fourfold counts; their sum was $1.0038\pm0.0061$. The measured score was $0.8508\pm0.0218$, 4.70 reported standard deviations above the real-model bound $0.7486$. The four selectable filters have a different normalization constraint from a single complete four-outcome Bell measurement. [Published experiment, Eq. 1 and Fig. 3](https://doi.org/10.1103/PhysRevLett.128.040402) · [Supplement, Appendix C](https://arxiv.org/pdf/2111.15128#page=8)

In an ideal calibration with herald probability $1/4$ for each filter, correct $X,Z$ correlations, and only the $Y$ correlation multiplied by an orientation mean $\nu$, Li's score would be $[2\sqrt2(2+\nu)-4]/5$. Whether those calibration conditions hold matters: their measured source and two-photon interference visibilities already gave an ordinary complex-model prediction of $0.8404$ in their analysis. The optical records constrain the stated network model under its source and detection assumptions. They supply neither a measured mixture of staircase characters nor a demonstration of this walk's local pointer. [Li et al., Fig. 3 and optical imperfections](https://physics.aps.org/featured-article-pdf/10.1103/PhysRevLett.128.040402)
