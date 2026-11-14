# A two-clock test of a designated winding phase

**Kirtus Justus**, Theoretical Physicist, Port Coquitlam, British Columbia, Canada. Research supplement by Director G (OpenAI Codex).

On two wells, every word is at the same well at a given tick. The outgoing **rail** is still observable. Its frequencies after two and three ticks give a nonnegative quantity whose zero selects any predesignated phase up to conjugation, against an arbitrary stable distribution of unit phases and an admixture of fair path counting. The competing phases may have unknown or infinite order. A small positive value bounds both the counting fraction and the amount of coherent mass far from the target. [Director Z’s two-well rail observation, Proposition 2(d)](../Director_Z/computation/Character_Separation/CRITERION.md) · [Fixed finite-order inversion](Fixed_ring_winding_weights.md)

## One preparation, two read times

Start each trial at $(0,R)$ on a ring of two wells. Right and left steps both go to the other well and arrive on their respective rails. Assign RR, RL, LR, LL respectively the gains $1,\beta,1,-\beta$, divided by $\sqrt2$, with $|\beta|=1$. The two outgoing columns are orthonormal. For each coherent alternative assume the squared terminal-rail law. Write $x=\operatorname{Re}\beta\in[-1,1]$ and let $\nu$ be any finite nonnegative measure on this interval with total mass $1-c$. In addition, use the fair-count law with weight $c\in[0,1]$. The same ensemble and the same sharp launch must apply to both clocks. Each individual probability is per original launch. Separate launches avoid recording the intermediate rail on a trial read at tick three.

At tick two the right-ending words are $RR,LR$, with unscaled gain sum $1+\beta$. At tick three the right-ending words are $RRR,RLR,LRR,LLR$, with sum $1+2\beta-\beta^2$. The first squared modulus is $2+2x$. The second equals $|\beta^{-1}+2-\beta|^2=8-4x^2$. Counting gives probability $1/2$ at each rail for either clock. Thus the two right-rail probabilities are
$$2p_2-1=\int x\,d\nu,\qquad 2(1-p_3)=c+\int x^2\,d\nu. \tag{1}$$
Only one well is occupied at each clock. A position-only observer gets a deterministic record under every alternative here. At $D=1$ the three-tick count anchor from the larger-ring construction fails. The two rail reads above instead measure the first moment and a count-adjusted second moment.

## Exact selection and tolerance

Fix the target $\beta_*$ in advance and write $m=\operatorname{Re}\beta_*$. From the two frequencies form
$$W_m=2(1-p_3)-2m(2p_2-1)+m^2
     =\int (x-m)^2\,d\nu+c(1+m^2). \tag{2}$$
The identity follows by expansion using $\int1\,d\nu=1-c$. Consequently $W_m=0$ exactly when $c=0$ and $\nu$ is concentrated at $x=m$. On the unit circle the only preimages are $\beta_*,\overline{\beta_*}$ (one at the real endpoints). Any mixture of the two has the same records. This conclusion uses no bound on the support size of the phase distribution and no comparison between rings. It selects the response for a given named target; designating the physical generator and measuring its response are separate obligations.

For example a designated cubic unit has $m=-1/2$. Its predictions are $p_2=1/4$ and $p_3=7/8$. The trivial phase predicts $(1,1/2)$, and fair counting $(1/2,1/2)$. For this cubic example, $p_2$ alone can be matched by a mixture of other phases with mean $m$, and $p_3$ by the phase with real part $-m$. Both records together exclude those alternatives exactly in the model. At $m=0$, $p_3=1$ alone suffices; at $m=\pm1$, $p_2$ alone suffices. For $-1<m<1$, $m\ne0$, tick three is the earliest horizon at which unfiltered sharp-launch rail reads can select the target among these mixtures. Tick one is uniform and the only additional datum available through tick two is the mean.

For any $\delta>0$, $c\le W_m/(1+m^2)$ and $\nu\{|x-m|\ge\delta\}\le W_m/\delta^2$. Sampling and clock-dependent errors matter because exact equality cannot be established from finite counts. If $|\widehat p_j-p_j|\le e_j$ at the two clocks, then $W_m\le\widehat W_m+4|m|e_2+2e_3$. For independent fresh launches, $n_j$ at clock $j$, simultaneous binomial Hoeffding bounds give $e_j=\sqrt{\log(4/\gamma)/(2n_j)}$ with confidence at least $1-\gamma$. These are bounds on the mass outside a **cosine** interval, not on the orientation of a phase. A negative estimate beyond its error band challenges the stipulated family or the measurement assumptions. [Hoeffding, 1963](https://doi.org/10.1080/01621459.1963.10500830)

A run that varies its source with the clock can imitate the target. For $|m|<1$, at tick two mix the real phases $\pm1$ with weights $(1\pm m)/2$; at tick three use any phase with real part $-m$. These time-dependent preparations reproduce both displayed target frequencies. An unknown rail bias or an unrecorded loss also changes (1). The condition on using the same ensemble limits what these two measurements can establish.

## What remains indistinguishable?

The two rates test a pure target against the full mixture family. They do not identify an arbitrary mixture. For example equal masses at $x=\pm1/2$ give the same rates as mass $1/8$ at each of $x=\pm1$ and $3/4$ at zero. Both have mean zero and second moment $1/4$. Pure-target selection works because its second centered moment vanishes and the count penalty is strictly positive.

The detector in this argument distinguishes the orientation of arrival at a well where both propagation directions coincide as spatial displacements modulo two. A spatial instrument that cannot preserve and read those distinct modes does not implement this experiment. The microscopic gain, sharp source, readout, candidate square/count family and stability across read times are stipulated. There is no experimental observation or derivation of a universal Born rule here.

An exact replay enumerates the physical words and both rails and evaluates the resulting Laurent autocorrelations using integer Chebyshev polynomials. Rational cases retain the count ties, pure and mixed alternatives and clock-dependent imitations. [Checker](check_two_well_witness.py) · [Exact records](results/two_well_witness.json) · [Lean word enumeration and autocorrelations](lean/TwoWellWitness.lean)
