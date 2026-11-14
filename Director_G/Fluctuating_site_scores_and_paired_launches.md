# What repeated launches can tell us about a fluctuating site detector

**Kirtus Justus**, Theoretical Physicist, Port Coquitlam, British Columbia, Canada. Research supplement by Director G (OpenAI Codex).

Can a position detector agree with the usual rule on **every** prepared distribution while using a different rule on each launch? Yes, even for continuous strictly increasing score functions that assign nothing to an empty well. A second read can distinguish these models if it samples the same detector state with independent outcome noise. Three forward walk ticks give an exact example. All rates below are predictions per original launch or pair. No paired records have been acquired.

## All single-launch position records

Let a preparation give a finite normalized table of nonnegative kinematic masses $w_i$, for example the squared rail amplitudes summed within each site. A latent detector type $t$ returns site $i$ with probability $f_t(w_i)/\sum_j f_t(w_j)$. The type distribution is independent of the setting. This is a model of the detector. The calculation begins after the walk and its terminal bins have been specified.

Choose two types with equal weights. Let $h$ vanish for $w\le1/2$ and satisfy $|h(w)|<1$. For $w>1/2$ put
$$
 f_\pm(w)=\frac1{1\pm h(w)}-(1-w).
$$
Use $f_\pm(w)=w$ everywhere else. The scores are positive at every occupied site because $1/(1\pm h)>1/2$ and $1-w<1/2$. With no site above half occupancy every score is ordinary. Otherwise there is exactly one such site. Its score plus all other scores is $1/(1\pm h(w))$. A minor bin of mass $p$ therefore has probabilities $p(1\pm h(w))$. Their mean is $p$. The dominant bin follows by complement. This proves equality of the marginal rule for **every finite table**, irrespective of its size, zeros, binning or how the walk prepared it. At a sharp table even repeats cannot identify the response at mass one from normalized outcomes.

The two functions may be continuous and strictly increasing. Take $z=2w-1$ and $h=z(1-z)/4$ on $[1/2,1]$. It joins continuously to zero at half occupancy. Here $|h|\le1/16$, $|h'|\le1/2$, so each right-hand score has derivative at least $1-(1/2)/(1-1/16)^2>0$ and joins the identity at both ends. Both functions give the ordinary dark and sharp controls.

If the detector draws the type independently afresh at every read, and subsequent preparations or state updates depend on the recorded history by the same conditional kinematics in both models, induction gives the ordinary probability for **every finite adaptive sequence** of such reads. A detector that scores a whole two-walk terminal table once can equally apply this construction to that table. Independent preparations alone therefore do not test persistence of a detector type. The [earlier joint-residue study](Independent_walks_and_shared_gains.md) imposes a different composition rule on the two registers.

## Repeating a three-tick walk

Launch at $(0,R)$, apply the balanced real coin and stream three times. On the eight-site ring the four occupied position masses are $5/8,1/8,1/8,1/8$. Choose the bin of the three minor sites, with total mass $p=3/8$. It is read by pooling the three position outcomes **after** the full position read. For a large exact illustration set $h(5/8)=1/2$ and $h=0$ elsewhere. This example has discontinuous scores. The continuous example above gives the same effect at smaller magnitude with $h(5/8)=3/64$. [Independent walk and path recurrences](Forward_staircase_and_spatial_probability.md)

Let the two preparations be fresh and take the same detector type for both acquisitions, with independent outcome draws *given that type*. The single-bin probability is $p$. The probability of reading the bin twice exceeds $p^2$ by $p^2h^2$. In the discontinuous example the two conditional rates are $9/16$ and $3/16$. They give $45/256$ double hits compared with $36/256$ under independent ordinary reads. If the detector retains the type with probability $\rho$ and otherwise redraws independently, independently of settings and types, the excess is $\rho p^2h^2$. Positive correlation alone does not attribute its cause to the score. A common preparation fluctuation, lost launch pairs, memory or electronic cross-talk requires separate control.

Persistence by itself gives no square identity. With $p=1/4$, $h=1/2$, the two rates are $1/8$ and $3/8$. Each type admits a two-trial distribution with both marginals equal to its rate $r$, and double-success probability $1/16$. The four probabilities are $1/16,r-1/16,r-1/16,1-2r+1/16$. Their mean is exactly the whole ordinary independent table despite the enduring type. All entries are nonnegative. Recording a fresh pair of launches, timestamps, settings and every miss permits an investigation of common-mode variation. The premise of conditional independence within an unobserved type still needs physical support.

## A pair comparison with no absolute site probability supplied

Take the two blank routings A and B of the [nine-tick dyadic apparatus](Local_writes_and_dyadic_site_scores.md). With $u=1/N$ and $2\le k<N$, their local mass pairs are $(0,ku)$ and $(u,(k-1)u)$, and their common positive spectator mass is $s=(N-k)u$. Denote its two type-specific probabilities by $a_t,b_t$. Use equally prepared, ordered pairs of launches, randomize each source setting independently of the detector type and the other setting, and count the pairs in which both launches hit the spectator, per assigned pair for each combination. With the same type for both launches, the same type law across assignments, and conditional product responses using the same calibrated instrument on each trial,
$$
 C=J_{AA}-J_{AB}-J_{BA}+J_{BB}
   =E[(a_t-b_t)^2].
$$
This is a testable **equality of joint rates**, with no supplied ordinary value for the spectator. Conditional order symmetry gives $J_{AB}=J_{BA}$, so three pair settings suffice when that symmetry is supported. Keeping both orders provides a diagnostic. The A and B source wirings differ before the late copy. This direct test of blank-rate equality is stronger than locality alone. To keep the late-choice formulation, perform the same square comparison on A blank versus A copy, then on B blank versus B copy. For every scalar-score type the two copy spectra are identical and have the same spectator rate. Their equality connects the two local constraints. All comparisons must sample the same population; use a common clock, bank and original-pair denominator.

Exact zero $C$ forces $a_t=b_t$ almost surely. For a scalar-score type with a strictly positive spectator numerator this implies equal normalizers and hence
$$
 f_t(ku)+f_t(0)=f_t((k-1)u)+f_t(u).
$$
The finite intersection over $k$ gives an affine score on that grid below unity for almost every type. A zero rate at a calibrated empty site forces $f_t(0)=0$ almost surely by nonnegativity. All grid tables then give ordinary normalized probabilities type by type. Countably many nested grids can share this conclusion for one common population. Extension to non-dyadic masses requires regularity. An upper confidence bound $C\le e$ on the underlying square implies $\Pr(|a_t-b_t|\ge d)\le e/d^2$ for $d>0$. Translating a rate tolerance to a score tolerance also requires control of spectator rates and the arbitrary score scale. If the type persists with setting- and type-independent probability $\rho$ and otherwise refreshes independently, the same joint cells give $C=\rho E[(a_t-b_t)^2]+(1-\rho)(E[a_t-b_t])^2$. Any $\rho>0$ suffices at exact zero. A calibrated lower bound $\rho_0>0$ gives a finite-error tail bound $e/(\rho_0d^2)$. For $\rho=0$ the contrast can vanish for both nonlinear types together.

These tests concern whether original-launch data identify a latent mechanism under a stated composition rule. The one-launch construction gives ordinary observed probabilities exactly. It supplies neither a physical origin for them nor a counterexample to reconstructions with additional composition and state-estimation postulates. [Masanes, Galley and Müller, 2019](https://doi.org/10.1038/s41467-019-09348-x)

The [exact checker](check_fluctuating_site_scores.py) tests complete tables, including empty sites, reconstructs the three-tick position spectrum by signed history counts and evaluates both paired protocols. Its routed-panel inputs come from the physical propagation in the linked nine-tick checker. The [Lean identity](lean/PairedSiteContrast.lean) checks the four-term cancellation after clearing a common denominator and the finite positive-sum implication. [Stored results](results/fluctuating_site_scores.json)
