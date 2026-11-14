# How much independence can a change of coin partners test?

**Kirtus Justus**, Theoretical Physicist, Port Coquitlam, British Columbia, Canada. Research supplement by Director G (OpenAI Codex) and the Codex workers.

Two independent sources of entangled Bell pairs make a concrete prediction for the walk. When the two coins from one pair enter the three-tick contact, the probability of agreement between their terminal position signs is \(3/8\). Exchange partners between the pairs and that probability becomes \(1/2\). This comparison needs neither a circular phase reference nor a measurement of an individual coin's imaginary coherence. A sign shared across the whole bank, however, survives any partner change. Here is what the difference measures and when it can recover the magnitude of one coin's coherence.

## The two assignments

Herald a bank of \(n\ge2\) labeled pairs \((A_i,B_i)\) and preserve their coin states. In one arm use the original partners. In the other choose a uniform shift \(k\in\{1,\ldots,n-1\}\) after the bank is ready and pair \(A_i\) with \(B_{i+k\bmod n}\). Read every \(i\) with equal weight, or choose one \(i\) uniformly and read only that pair. Both choices sample each ordered off-diagonal pair with probability \(1/[n(n-1)]\). Randomizing uniformly over all permutations without fixed points also works. A single fixed nonzero shift need not work. Draw the arm and assignment independently of the heralded state and all unread data. Conditioning on the bank size is allowed.

At the contact reader launch the selected, distinguishable coins two wells apart. Use a real Hadamard coin, conditional shift and minus sign at coincident positions, in that order at each tick. Give final displacements \(-3,+1\) one sign and \(-1,+3\) the other. Write \(s_i=+1\) for agreement and \(s_i=-1\) otherwise. For any joint state of the bank, the calibrated binary effects on the selected pair are \(E_s=(I-sY_A Y_B/4)/2\), with \(Y\) the usual Pauli matrix. All expressions below use ordinary quantum probabilities on this specified readout. [Signed path derivation and full position table](Two_coin_position_read_at_one_contact.md)

Let \(\langle\cdot\rangle\) denote the expectation in the entire heralded density operator \(\Omega\), allowing entanglement among all \(2n\) coins. Define

\[
q_{ij}=\langle Y_{A_i}Y_{B_j}\rangle,\quad
D={1\over n}\sum_i q_{ii},\qquad
O={1\over n(n-1)}\sum_{i\ne j}q_{ij}.
\]

The two agreement probabilities are \(1/2-D/8\) and \(1/2-O/8\). Linearity of the effect gives these identities even for entangled banks. Every nonzero cyclic offset occurs once for each first label when averaging the shifts. If both arms use independently randomized assignments over a varying population of heralded banks, the formulas hold for its ensemble-averaged \(\Omega\).

## What excluding the original partner changes

Put \(a_i=\langle Y_{A_i}\rangle\), \(b_i=\langle Y_{B_i}\rangle\), and \(c_{ij}=q_{ij}-a_i b_j\). Bars on \(a,b\) denote label averages. Set \(V_{ab}=n^{-1}\sum_i(a_i-\bar a)(b_i-\bar b)\) and let \(\bar c_{\rm off},\bar c_{\rm diag}\) average the corresponding entries. These are reduced-state expectations, defined even when the original pairs have no product decomposition. Removing the diagonal from \((\sum_i a_i)(\sum_j b_j)\) gives

\[
O=\bar a\bar b-{V_{ab}\over n-1}+\bar c_{\rm off},\qquad
D-O={n\over n-1}V_{ab}+\bar c_{\rm diag}-\bar c_{\rm off}.
\]

If the bank factors **across original pairs**, each pair may itself be entangled, and every off-diagonal \(c_{ij}\) vanishes. Identically prepared original pairs then give \(O=ab\) exactly and \(D-O\) tests their connected \(YY\) correlation. Equal \(Y\)-means on the two inputs further give \(O=y^2\). This can replace independence *within* each measured original pair by independence *between* bank members. Only the average off-diagonal covariance needs to vanish for this particular observable. Agreement of the two arms tests one moment and cannot establish full product preparation.

For independent but heterogeneous original pairs the error in replacing \(O\) by \(\bar a\bar b\) is bounded sharply by

\[
\frac{4\lfloor n^2/4\rfloor}{n^2(n-1)} .
\]

Indeed, Cauchy–Schwarz bounds \(\lvert V_{ab}\rvert\) by the geometric mean of the two label variances. Variance on \([-1,1]^n\) is convex in each coordinate, so a maximum occurs at a vertex. With \(h\) positive signs its value is \(4h(n-h)/n^2\), maximized by the two most balanced counts. Set \(b=a\) or \(b=-a\) on that vertex to attain both error signs. An independently justified bound \(\lvert\bar c_{\rm off}\rvert\le\epsilon\) adds \(\epsilon\) to the error. For two original product pairs with both coins circular \(+\) in the first and both \(-\) in the second, \(D=1\), \(O=-1\) and \(\bar a=\bar b=0\). A nonzero arm difference can therefore come entirely from label variation. With four such pairs in order \(++--\), the three nonzero cyclic shifts give \(0,-1,0\); the full crossing average is \(-1/3\).

One can instead draw \(A_i\) and \(B_j\) uniformly and independently from **two independently supplied banks**, using all index combinations, including equal indices. Then \(q_{ij}=a_i b_j\) across banks and the mean equals the product of the two bank-averaged marginal means. Entanglement within either bank is unrestricted. Equal bank means again give a square. Shared drift or conditioning on a common herald can spoil bank independence, which must hold for the ensemble actually read.

## Entangled control and the cost of counting independent shots

Take the product of \(n\) original Bell pairs \(\lvert\Phi^-\rangle=(\lvert RR\rangle-\lvert LL\rangle)/\sqrt2\). Each has \(q_{ii}=1\) and zero single-coin means. Thus \(D=1,\ O=0\). The \(n\) observations made after one partner assignment can still be dependent. For a fixed permutation \(\pi\), suppose disjoint contact readers implement their product measurement. For any subset \(S\) of their output labels,

\[
\left\langle\prod_{i\in S}s_i\right\rangle
=\begin{cases}(-1/4)^{|S|},&\pi(S)=S,\\0,&\text{otherwise}.\end{cases}
\]

The moment operator is \((-1/4)^{|S|}\prod_{i\in S}Y_{A_i}Y_{B_{\pi(i)}}\). In each original Bell pair one isolated \(Y\) has expectation zero, two have expectation one, and an untouched pair contributes a factor one. Every label is hit twice or zero times precisely on unions of permutation cycles. For a swap of two pairs the full agreement/disagreement table is \(17/64,15/64,15/64,17/64\) in \(++,+-,-+,--\) order. Both margins are fair. Independent fair outputs would give \(16/64\) per cell. The classically correlated mixture of the two like-handed circular products within each original pair has the same \(Y\) moments, so these records alone do not identify entanglement. Use the bank as the unit for independent-repeat error estimates when independent bank repeats are warranted.

## A correlation preserved by every real read

Let \(P_\pm=(I\pm Y)/2\). Compare \(P_+^{\otimes 2n}\) to \((P_+^{\otimes 2n}+P_-^{\otimes 2n})/2\). The latter is the shared circular-sign construction of Caves, Fuchs and Schack. Its one-coin marginal is \(I/2\); the first state's marginal is pure circular. Any full transcript effect of a real protocol is real symmetric, including with real blanks, real partner routing, adaptive choices and joint measurements. A density operator and its complex conjugate have the same expectation on every such effect. The two banks above therefore agree on **all** those transcript probabilities. Both have \(D=O=1\). No choice of \(n\) or of partners within the bank separates them. Fresh independent banks with signs redrawn separately change the joint input to a cross-bank test. The same obstruction persists across any collection over which one sign remains shared. [Caves, Fuchs and Schack, Section V, Eqs. 5.2–5.3](https://arxiv.org/html/quant-ph/0104088#S5)

Multi-copy quantum networks can estimate nonlinear functions of an input density operator. For this contact walk the recovered quantity is linear in the actual bank state. Its interpretation as a square requires the source conditions above. Each arm also needs trace-preserving delivery of both coins, or explicit treatment of losses, and the same calibrated near effect after routing; uncontrolled holding times or phases can change \(q_{ij}\). Event-ready labels alone cannot move a coin between different release times. Coherent delay or memory and contact routing are additional resources. Selecting just one ordered pair avoids simultaneous readers but still requires the chosen inputs to arrive together. Count the heralded attempts and retain or bound all missing terminal results. No phase reference, independent source, physical contact or probability law has been derived here. [Ekert et al. on direct quantum estimation](https://arxiv.org/abs/quant-ph/0203016) · [Earlier bank test for the walk's count threshold](One_threshold_on_several_walks.md)

The [exact checker](check_crossed_coin_pairs.py) reconstructs the signed position effect from trajectories, evaluates Bell-bank moments in the computational basis and compares complete binary transcripts to the cycle formula. The [result archive](results/crossed_coin_pairs.json) records finite bounds and control probabilities. Run it with Python and a new JSON output path. [Lean 4.19](lean/CrossedCoinPairs.lean) checks the diagonal removal and the scaled covariance rearrangement.
