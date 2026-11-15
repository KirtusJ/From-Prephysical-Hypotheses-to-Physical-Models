# Two position echoes compare addressed coin phases

A single walker can compare the relative phases of two addressed coin invocations $A$ and $B$. One five-tick sequence measures the cosine of their phase sum. An eleven-tick sequence measures the cosine of their difference with full ideal visibility. Both use the same two calls on every launch, a sharp initial rail, and exact position records. The result provides an internal test of phase alignment or drift. The absolute sign assigned to both addressed Hadamards remains unobservable through these echoes. This is a proposed circuit with exact path calculations. [Addressed-coin phase ambiguity](addressed_embedding.md) · [Earlier rational reference and controlled bypass](../../../Director_G/Rational_references_and_optical_bypass.md)

## Ring and pulse conventions

Start on R at physical site 0 of a **four-site** ring. Let $y$ be the parity of the cumulative number of left steps. At tick $t$ the physical position is $x=t-2y\pmod4$. Thus $y=0,1$ name the two sites reachable at that clock. Both rails remain present at a site. A stream keeps $(y,R)$ fixed and sends $(y,L)$ to $(1-y,L)$ in the clock-dependent encoding. Two consecutive pure streams restore both encoded labels. A physical controller must select the odd **encoded** address using the clock; selecting the odd physical sites would act on both reachable sites or neither.

Each tick applies the listed coin and then streams. The rail matrices are $H=(X+Z)/\sqrt2$, the rail swap $X$, and the identity $I$. Each addressed call $C_j$ applies $X$ at $y=0$ and $\eta_j H$ at $y=1$, with $\eta_j=e^{i\phi_j}$. The coherent relative phase includes any propagation difference attributed to that call. The other specified operations and routing phases must be characterized. In particular, an unmodeled differential phase from transport around the ring would enter the measured loop contrast.

## Five ticks for the sum

Use $H,C_A,I,C_B,H$. The only site write is at tick 5. Just after tick 1 the rail branches are $(|0,R\rangle+|1,L\rangle)/\sqrt2$. The stream in the addressed tick and the identity tick following it cancel in the encoded basis. The two successive addressed coins therefore act on the same two addresses. The coin products are $X^2=I$ and $(\eta_B H)(\eta_A H)=\eta_A\eta_B I$. After the stream of tick 4 the walker is entirely at $y=0$, with incident coin $(|R\rangle+\eta_A\eta_B|L\rangle)/\sqrt2$. The last Hadamard and stream give

$$
P(y_5=0)=|1+\eta_A\eta_B|^2/4
       =[1+\cos(\phi_A+\phi_B)]/2.
$$

The other encoded site has the complementary probability. No which-route record may be made while the two amplitudes are separated.

## Eleven ticks for the difference

Use $H,C_A,I,X,X,C_B,I,H,H,H,I$, with writes at ticks 10 and 11. Ticks 2–3 and 6–7 implement the respective addressed coin with no net encoded stream. The $X,X$ pair switches the address of **both** branches and restores the input rail: either rail undergoes exactly one left step. Thus each branch receives one addressed Hadamard, at different invocations. Following the branch initially at $(0,R)$, its two addressed coins compose as $\eta_B HX|R\rangle=\eta_B|-\rangle$. The branch initially at $(1,L)$ undergoes $\eta_A XH|L\rangle=-\eta_A|-\rangle$, where $|-\rangle=(|R\rangle-|L\rangle)/\sqrt2$. After tick 7 the two amplitudes are

$$
(\eta_B|1,-\rangle-\eta_A|0,-\rangle)/\sqrt2.
$$

Tick 8 maps $|-\rangle$ to L and streams, leaving $a|0,L\rangle+b|1,L\rangle$ with $a=\eta_B/\sqrt2$ and $b=-\eta_A/\sqrt2$. At tick 10, after two more $H$ ticks, the R amplitudes are $(a-b)/2$ and $(b-a)/2$ at the two sites. The L amplitudes are both $(a+b)/2$. A site write there preserves this rail distinction. The last $I$ tick streams L and holds R in the encoded coordinates. Hence equal successive **address codes** select R, giving

$$
P(y_{10}=y_{11})=|a-b|^2/2
  =[1+\cos(\phi_A-\phi_B)]/2 .
$$

At each of the two possible tick-10 sites, the equal-code word has mass $(1+\cos(\phi_A-\phi_B))/4$ and the changed-code word has mass $(1-\cos(\phi_A-\phi_B))/4$. In physical positions an equal-code word is **one right step** modulo four; the two physical site labels at consecutive clocks are never identical. This displacement read uses no additional addressed coin, phase standard, or rail detector.

## Which aspects of the phase transfer

With ordinary squared scoring, stable detection, and fixed phases, let $C_+=2P(y_5=0)-1$ and $C_-=2P(y_{10}=y_{11})-1$. The two measured combinations determine

$$
\cos\phi_A\cos\phi_B=(C_-+C_+)/2,\qquad
\sin\phi_A\sin\phi_B=(C_--C_+)/2 .
$$

With random phases and matched **joint** phase distributions across the two runs, these are the corresponding expectations of products. They need not factor into products of means. The second addressed call is at tick 4 in the sum sequence and tick 6 in the difference sequence. Changing the inter-call delay can change its phase statistics. Measure or justify that transfer before combining the two contrasts. Each contrast separately still measures its own sequence's average under the stated model.

For example, if $\phi_A=\phi_B$ on every launch but that common phase fluctuates, the difference port stays bright while the sum contrast is $E[\cos(2\phi_A)]$. Independent, equally likely $0$ or $\pi$ errors on the two calls give zero in both contrasts. A common equally likely $0$ or $\pi$ gives one in both: either common sign works perfectly in the echo. If the candidates are known to have phases restricted to 0 or $\pi$, bright versus dark ports test their *relative* sign even under positive power scoring which preserves zero support, for otherwise ideal gates and writes. Intermediate visibility or mixtures require a model of scoring and background reports to infer the cosine numerically.

For any phases, simultaneously replacing $(\eta_A,\eta_B)$ by $(-\eta_A,-\eta_B)$ preserves both echoes. Complex conjugating all their phases does too. In particular the algebraic map $\sqrt2\mapsto-\sqrt2$ changes the sign of every Hadamard, including both addressed ones. Uniform H ticks gain a single global sign. Each echo leaves this simultaneous transformation undetected. What is tested internally is a relation between the two physical invocations. Assigning an absolute phase sign to either invocation in an embedding comparison still needs a separately fixed reference and a transfer check to the experiment.

The [path checker](check_two_address_echoes.py) enumerates the signed rail histories on the four physical sites and accumulates amplitudes separately for each saved position word and terminal rail. It verifies every coefficient of the resulting Laurent polynomials in $\eta_A,\eta_B$, including the four separate two-write words. No random-phase sampling or fitted visibility enters the calculation. Run `python -I -B check_two_address_echoes.py` from this folder.
