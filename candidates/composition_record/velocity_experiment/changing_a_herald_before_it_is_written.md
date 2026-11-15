# Changing a herald before it is written

A signed reflection can change the four-path walk gate's success probability from $5/16$ to $245/256$ while preserving its successful action on an arbitrary input. An isolated fair phase tag gives a second binary comparison. The two failure rates $187/512$ and $11/256$ together distinguish ordinary scoring from the competing powers and a prior good/bad copy under the conditions below. Both numbers are predictions for a single measured pointer. No experimental frequencies enter the result. [Original filter and its two Pell paths](a_phase_reference_from_synchronized_walks.md) · [Ambiguity of a separately scored binary herald](records_with_a_heralded_reference.md)

## Four circuits and one terminal read

Let $V$ be the original six-wire unitary. $P_0$ selects its four blank work wires and acts as identity on the logical control and rail. The good projector $\Pi$ selects the two zero path bits and clear rejection bit. The Pell selector is left coherent. The original filter has $P_0 V^\dagger\Pi V P_0=sP_0$ for $s=5/16$. Thus the good and bad maps of a logical input $\psi$, divided by $\sqrt{s}$ and $\sqrt{1-s}$ respectively, are isometries $G$ and $B$ with orthogonal ranges. This holds on coherent inputs and in the presence of a spectator.

The amplifier acts with the signed reflection $D=I-2VP_0V^\dagger$ after $V$. Its optional phase $F=I-2\Pi$ precedes $D$. Neither reflection measures its controls. In the basis $(G\psi,B\psi)$, $D=I-2vv^{\mathsf T}$ for $v=(\sqrt{s},\sqrt{1-s})^{\mathsf T}$. Applying $D$ to $v$ gives $-v$. Applying $DF$ to $v$ multiplies its good part by $-(3-4s)=-7/4$ and its bad part by $4s-1=1/4$. This is one step of oblivious amplitude amplification with a known clean-input subspace. [Berry, Childs, Cleve, Kothari and Somma](https://arxiv.org/abs/1312.1414)

| Arm | Operation after $V$ | Ideal success |
|---|---|---:|
| Direct | Read $\Pi$ | $5/16$ |
| Matched phase zero | $D$, then read | $5/16$ |
| Matched phase $\pi$ | $F$, then $D$, then read | $245/256$ |
| Fair unresolved phase | Apply $F$ controlled by a fresh $\lvert+\rangle$ tag, then $D$, then read | $325/512$ |

In each arm every good Kraus operator is proportional to its original value. On the fair arm the unread orthogonal tag supplies the two scalar multiples. Normalizing the successful maps therefore gives the same channel in all four arms. The reference retains its original small dephasing of the addressed operation. Its success probability changes without improving the conditional gate fidelity.

A fresh pointer copies only the predicate $\Pi$ by a reversible three-control operation. Its one read reports success or failure per attempted launch. The direct and signed arms need six circuit wires plus that pointer. For the matched comparison both exports add the same fair unread wire. In the `matched-pi` arm the full phase flip is independent of its value. In the `twirled` arm it controls that flip. The implementation uses the inverse of the signed routing circuit and reflections about its specified register patterns. A forward walk without those controls would need a separate implementation.

## If the flag has already left a record

Suppose the good and bad amplitudes at the cut after $V$ become correlated with normalized marker states $e_G,e_B$. Define $c=\operatorname{Re}\langle e_G|e_B\rangle$. This scalar-marker model leaves the two sectors internally intact and allows any logical input. At the final good port, the component from an initially good branch alone has conditional squared norm $(1-2s)^2=9/64$. The component from an initially bad branch has $4s(1-s)=55/64$. The good/bad interference term before the phase flip is $-165c/512$. The resulting success masses are

$$
p_0(c)=\frac{325-165c}{512},\qquad
p_\pi(c)=\frac{325+165c}{512},\qquad
p_{\rm fair}=\frac{325}{512}.
$$

With a complete copy the ordinary phase contrast vanishes. Even if the subsequently scored probability is unknown, a fully recorded good/bad branch acquires at most a global sign on the deterministic phase arm. On the fair arm it can change the unread tag. With the tag isolated, the rest of the apparatus sees the same within-branch states. A scorer blind to the phase choice thus gives an identical failure probability in both arms. It may use an arbitrary response and the prior record.

Matching the recombiner matters. Consider comparing the **direct** arm, which omits $D$, with the amplified arm. An earlier good/bad writer and the final binary writer may share an exponent $q$ on that launch. Give $q=1$ weight $2/17$. Give the other $15/17$ to minus and plus infinity in the proportions $5:11$. For the direct read the first extremum always selects good, the second always selects bad. On amplification, a previously selected good branch has final success mass $9/64$, so its minimum selector chooses success. The bad branch has final success mass $55/64$, so its maximum selector also chooses success. The ordinary type succeeds on $325/512$. This mixture therefore gives exactly $5/16$ and $245/256$ respectively with an intermediate record. Using the same recombiner on the matched arms removes this way of distinguishing the settings from inside the scorer.

## Two matched binary rates select the ordinary response

For a positive mass $z$ with positive complement let $R_q(z)=z^q/[z^q+(1-z)^q]$. Zero is uniform and the two infinite powers select an extreme. Randomly assign the phase after the release cut, using the same distribution of latent modes on both arms. A mode applies its common $q$ to the terminal binary effects. It may correlate $q$ with the marker overlap. Allow $c\in[0,1]$ for arbitrary signed $q$, and $c\in[-1,1]$ when $q\ge0$. Also allow fully recorded modes with any phase-blind failure rate $d$ on both arms.

Put $x=187/512$, $t=11/256$, and $y_c=(187-165c)/512$. The observed failure pair for a power mode is $(X,Y)=(R_q(x),R_q(y_c))$. For the ideal source and ordinary reader it is $(x,t)$. Define

$$
r=\frac{\log(245/11)}{\log(325/187)},\qquad
g(z)=R_r(z),\qquad
L(z)=t+\frac{r\,t(1-t)}{x(1-x)}(z-x).
$$

Here $g(x)=t$ and $L$ is its tangent. The integer comparison $325/187<245/11<(325/187)^6$ gives $1<r<6<x/t=17/2$. Thus $L(0)<0$ and $L(1)<1$, so $L(z)<z$ on the entire unit interval. On $(0,1/2)$, $g$ is strictly convex. Indeed $g'=rg(1-g)/[z(1-z)]$, and the sign of $g''$ there is that of $r(1-2g)-(1-2z)>0$ because $g(z)<z$.

* For finite $q>0$, $y_c\ge t$ and $X<1/2$, so $Y\ge R_q(t)=g(X)\ge L(X)$. Equality requires $c=1$ and $X=x$, hence $q=1$.
* For finite $q<0$ the allowed overlap gives $y_c\le x$, so $Y\ge X>L(X)$. Zero power and fully recorded phase-blind modes also lie on the identity line. At positive infinity $X=0$ and $Y\ge0>L(0)$. At negative infinity $X=1$ and $y_c\le x<1/2$ gives $Y=1>L(1)$.

Averages preserve this inequality. Exact ordinary population rates imply $E[Y-L(X)]=0$, forcing an intact marker ($c=1$) and ordinary power almost surely among the power modes, with zero incidence of the separate fully recorded class. No single launch is observed in two settings. A setting-dependent population, a phase-aware scorer, or access to the supposedly isolated tag changes the experiment.

The same tangent also tests **coherent** direct and amplified arms with $x$ replaced by $s=5/16$. Independent dilution of the original success by a fair two-bit $00$ tag gives $t'=5/64$ and works for a single coarse binary read. In these two versions $1<\log[(1-u)/u]/\log(11/5)<4\le s/u$ for $u=11/256$ or $5/64$. For negative powers $g(X)\ge X$ on the upper half. If the original herald is separately scored, however, the previous mixture of zero and two powers in proportions $55:73$ already gives its ordinary mean. Two separately scored balanced bits remain fair under either power. Their classical conjunction then gives $5/64$ as well.

## A signed phase can defeat all three matched arms

Dropping the overlap condition for negative powers admits the following exact distribution. The entries are the reported failure bits of each type. Every extremum is unique.

| Weight over 512 | Exponent | $c$ | Fair phase | Phase $\pi$ | Phase zero |
|---:|---:|---:|---:|---:|---:|
| 165 | $-\infty$ | $-1$ | 1 | 0 | 1 |
| 22 | $-\infty$ | $+1$ | 1 | 1 | 0 |
| 187 | $+\infty$ | $+1$ | 0 | 0 | 1 |
| 138 | $+\infty$ | 0 | 0 | 0 | 0 |

The three means are $(187,22,352)/512$, the ordinary predictions. A relative phase $\pi$ gives $c=-1$ even without leaking any information to a further system. This example identifies the needed phase convention for inverse powers. The [five-outcome read with three references](reading_a_herald_with_three_references.md) uses a different comparison and lets the exponent vary across settings.

The [exact replay and circuit exporter](check_amplified_herald.py) reconstructs all four input columns from the original gate's signed paths, checks the full good and bad maps and propagates explicit marker states. The optional Qiskit calculation checks the emitted QASM and the final pointer for all four logical basis inputs and a complex superposition.

    python -I -B check_amplified_herald.py
    python -I -B check_amplified_herald.py --qiskit
    python -I -B check_amplified_herald.py --qasm twirled fresh_twirled.qasm
    python -I -B check_amplified_herald.py --qasm matched-pi fresh_pi.qasm

Kirtus Justus, Theoretical Physicist, Port Coquitlam, British Columbia, Canada, retains scholarly responsibility. OpenAI Codex developed the matched herald comparison, counterexamples and circuit replay.
