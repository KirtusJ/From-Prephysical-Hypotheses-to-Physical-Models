# A remote coin pulse tests probability weighting with one near bit

**Kirtus Justus**, Theoretical Physicist, Port Coquitlam, British Columbia, Canada. Mathematical and computational assistance by OpenAI Codex.

Alice always reads the same binary tag. Bob changes one coin pulse before he records a walker's position. With ordinary weights, Bob's choice leaves Alice's tag frequency unchanged. When a common finite exponent is applied to the joint terminal cells on each launch, the change in one Alice frequency has the same sign for every exponent other than one. On balanced tags the squared-cell rival predicts $5/9$ in the test arm and $1/2$ in the baseline. These are proposed frequencies. No observations of this apparatus are reported.

## Two matched tags and five ticks

Distribute tags to Alice and Bob with support on $00,11$. Write their kinematic masses as $a,b>0$, $a+b=1$. An equal superposition of the two matched tags supplies the balanced example. Each station requires one **shared tag bit** and Bob also needs a local walker initialized on the right rail at $x=0$. In the contact program the herald must precede the setting choice. Its modeled $a=1/3,b=2/3$ already suffice if its two routes serve as tags and Bob can supply the independent walker. A balancer is optional for the signed comparison.

Every tick streams the right and left rails in opposite directions. A letter $H$ first sends $(r,l)$ to $(r+l,r-l)/\sqrt2$, and $I$ streams without mixing. Words below are in chronological order. In the baseline Bob uses $HHIII$ for both tags. In the test he changes the third coin to $H$ only on tag 0, giving $HHHII$ there. All sites in a selected tag sector receive the same pulse. The remaining ticks, read time, and whole-well detector stay the same. No arm waits. Use a line on which five ticks do not encounter a reflecting boundary, or a ring of at least eleven wells.

| Bob's word | $x=-5$ | $-3$ | $-1$ | $+1$ | $+3$ | $+5$ | Denominator |
|---|---:|---:|---:|---:|---:|---:|---:|
| $HHIII$ ($Q$) | 1 | 1 | 0 | 0 | 1 | 1 | 4 |
| $HHHII$ ($P$) | 1 | 0 | 1 | 1 | 4 | 1 | 8 |

After the third $H$, the signed $(R,L)$ numerators in rising well order are $(0,1),(-1,0),(2,1),(1,0)$ over $\sqrt8$. The final two coasts move the rails at $+1$ to different wells. Alice's tag and Bob's well specify distinct joint cells even at wells common to both tag sectors. The calculation can also be read at **three** synchronized ticks by resolving site and rail at Bob after $HHI$ and $HHH$. The five-tick implementation obtains the same masses with a site-only detector. Experiments have realized discrete photonic walks with adjustable coins and conditional shifts. Implementing the matched-tag pulse and verifying these particular counts are separate experimental tasks. [Adjustable photonic walk](https://arxiv.org/abs/0910.2197)

## A sign that survives mixing

Let $q>0$ be finite and common to all occupied joint cells on this launch. Apply $m\mapsto m^q$ to each kinematic mass, normalize once, then pool Bob's outcomes to get Alice's tag. The baseline odds for Alice tag 0 are $t=(a/b)^q$. In the test those odds become $tk$, where

$$
k=\frac{\sum_x P_x^q}{\sum_x Q_x^q}
=\frac{2^{q-1}+2^{1-q}}2
=\cosh((q-1)\log 2).
$$

The arithmetic–geometric mean inequality gives $k\ge1$ with equality exactly at $q=1$. Thus the test-arm frequency minus the baseline frequency is

$$
\Delta(q,a)=\frac{t(k-1)}{(1+tk)(1+t)}.
$$

Independent remote assignment must sample the same launch population in both arms. The source masses and $q$ can vary together in any way. If both routes have positive mass on each scored launch, equality of the population frequencies forces $q=1$ almost surely in this family. Additional signal cells with an arbitrary spectrum can be carried through either arm if their masses factor from the tag and walk within each launch and their resolution is unchanged. Their common power sum cancels.

When $a=b$, each baseline launch gives $1/2$ at every $q$. The test excess becomes $\Delta(q,1/2)=\tfrac12\tanh^2((q-1)\log 2/2)$. For any $\delta>0$ a simultaneous upper bound $\epsilon$ on the excess gives

$$
\Pr_{\rm test}(|q-1|\ge\delta)\le
\min\!\left(1,\frac{2\epsilon}{\tanh^2(\delta\log2/2)}\right).
$$

The balanced baseline remains fair even if its exponent population changes. The bound then concerns the test arm itself. At unequal masses independent assignment is needed for the subtraction, and launches close to one-tag support can make its sensitivity arbitrarily small.

## What the terminal detector must resolve

* A compulsory three-$H$ clock with immediate **whole-well** readout instead gives masses $(1,1,5,1)/8$. The two-$H$ whole-well law is $(1,2,1)/4$. Their different Shannon entropies preclude a sign of one kind on both sides of $q=1$: the derivative of the ratio of the power sums at one is the difference of the sums $\sum p\log p$. For the exact $P,Q$ above both entropies are two bits. On the line, five ticks are minimal for this **particular site-only** spectrum from a sharp rail with a spatially uniform choice of $H$ or $I$ at each tick. Before four ticks fewer than five wells are reachable. At four ticks three $H$ pulses give sorted positive numerators $(1,1,1,5),(1,1,2,2,2),(1,1,2,2,2),(1,1,2,4)$ over 8, as the $I$ moves from the first slot to the fourth. Four $H$ pulses give $(1,1,2,2,10)/16$. At most two $H$ pulses cannot produce mass $1/8$. This finite minimum concerns the specified $P$ and gates.
* All controls and measured projectors preserve the matched-tag sectors. The terminal diagonals therefore also follow from a separable state $a|00\rangle\langle00|+b|11\rangle\langle11|$ **if its complete density operator is the input whose cells the power law scores on each launch**. Exactly the same caveat applies to four equal, classically correlated tags. If a classical source first selects a single tag per launch, the chosen $a$ is 0 or 1. Then Alice's tag cannot change with Bob's pulse. A fair classical source followed by ordinary local sampling within the selected row reproduces the entire ordinary tag-and-well table in both arms. Inter-tag coherence is unused, while interference between Bob's walk histories within a tag is needed for the five-tick construction.
* Calibrate the two Bob spectra on tagged sharp-rail inputs, including the dark wells. Retain every launch counted after the agreed herald, expose misses and bound losses. Pooling Bob's wells before powering or attaching random child labels after a parent outcome was selected removes the effect. A comparison between remote choices also requires isolation from setting-dependent changes in Alice's registration. These two diagonal settings cannot certify entanglement, rule out arbitrary detector laws, or establish an ontology.

The four-equal-tag construction realizes the same $\cosh$ factor by giving two tags in Alice's first bin relative splitting depths 0 and 2, and two in the other bin depth 1. Here the additional tag is replaced by the walk's own five-site spectrum. The [one-split contact comparison](remote_split_read.md) uses the original two-route flight, allows genuinely unequal splitting fractions, and scores two near wells. The present sign uses a single near event and specified ideal Bob spectra. [Earlier branch-normalized walk contrast](../../Director_G/A_branch_basis_switch_after_a_bare_walk.md) · [Single-histogram three-mass criterion](../../Director_G/When_a_position_histogram_identifies_its_probability_power.md)

The [Rust replay](check_remote_refinements.rs) reconstructs the finite walk spectra. The [Lean certificate](RemoteSplitWeights.lean) checks the algebra of the signed comparisons with denominators cleared. The [spectator comparison](spectator_refinements.md) treats fluctuating responses beyond the power family.
