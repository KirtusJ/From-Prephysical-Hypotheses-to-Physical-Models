# What a randomized omission can reveal about a detector mark

**Kirtus Justus**, Theoretical Physicist, Port Coquitlam, British Columbia, Canada. OpenAI Codex developed the bounds and compared them with deposited counts.

The proposed walk experiment uses a mark taken before a remote choice to distinguish responses at a well of mass $5/8$. A mark can also alter the later read. To test that possibility, randomize each launch between acquiring the mark and omitting it. A duration-matched sham substitutes a specified pulse for the acquisition. It defines another comparison, and any claimed equivalence between omission and sham requires its own test. Keep the preparation, subsequent science operations, normalization, clock and outcome definition fixed. This note asks how much a successful randomization would identify when the omitted mark is unobserved. [Prechoice walk experiment](detector_marks.md) · [Why read order matters](mark_read_order.md)

## Bounds on the two groups

Use $Z$ for the binary mark a launch would give **if assigned the marked protocol**. Let $Y_1,Y_0$ be the final bits under the marked and comparison protocols. A coupling of these variables is a way to compare possible explanations of the arm distributions. It supplies no physical simultaneous read of incompatible instruments. This use of a potential post-assignment label is related to principal stratification. [Frangakis and Rubin](https://pubmed.ncbi.nlm.nih.gov/11890317/)

Under random assignment and comparable retention, the marked arm supplies $w=\Pr(Z=0)$, $a=\Pr(Z=0,Y_1=1)$ and $b=\Pr(Z=1,Y_1=1)$. The other arm supplies $u=\Pr(Y_0=1)$. Put $x=\Pr(Z=0,Y_0=1)$. The entire remaining uncertainty in the *two average effects* is determined by a single interval.
$$
 \max(0,u+w-1)\le x\le\min(w,u),\qquad
 \Delta_0=(a-x)/w,\qquad \Delta_1=(b-u+x)/(1-w).
$$
Here $\Delta_j=E[Y_1-Y_0\mid Z=j]$ when the group has positive probability. Omit empty groups, retaining their zero weighted effects. The pair moves along a line with $w\Delta_0+(1-w)\Delta_1=a+b-u$. Its two component bounds cannot be chosen independently.

Necessity is the nonnegativity of the four $(Z,Y_0)$ probabilities. For any $x$ in this interval, assign comparison hit probabilities $x/w$ and $(u-x)/(1-w)$ to the two groups. Within each group retain the observed marked hit probability, coupling the two possible final bits independently if desired. This attains both proposed effects and preserves the full observed $(Z,Y_1)$ table. One can also make $Y_0$ and $Y_1$ dependent within a group. Individual changes on a given launch remain unmeasured even where a group effect is identified.

## A small common record improves the comparison

Latch a discrete baseline label $C$ in *both* protocols **before** randomizing whether to acquire $Z$. For each value $c$, use unconditional masses $s_c=\Pr(C=c)$, $w_c=\Pr(C=c,Z=0)$ and $u_c=\Pr(C=c,Y_0=1)$. The sharp interval for $x$ becomes
$$
 \sum_c \max(0,w_c+u_c-s_c)\le x\le\sum_c\min(w_c,u_c).
$$
Apply the same four-cell construction inside each stratum and sum it. The interval can only shrink. It collapses if $C$ predicts $Z$ perfectly, and it may remain wide for an uninformative reference. This controls the additional effect of the marked operation in the apparatus with the baseline label already present. Any effect of acquiring $C$ itself is a separate question.

For a binary reference using $C$ itself as the prediction of $Z$, let $\epsilon=\Pr(C\ne Z)$, estimable in the marked arm. The width of the interval for $x$ is at most $\epsilon$. Within any stratum its width is at most $\min(w_c,s_c-w_c)$, which in turn is bounded by that stratum's probability of the chosen predictor making an error. Thus the widths of the two conditional mean-effect intervals are at most $\epsilon/w$ and $\epsilon/(1-w)$. The width bound is sharp. For equally common reference bits, let each conditional mismatch rate be $\epsilon\le1/2$ and the comparison hit rate within each reference group be $1/2$. Each stratum then contributes width $\epsilon/2$. A rare detector group can remain unresolved even if the common reference is usually correct. No conditional independence between the common reference and the science output is used for these bounds.

A copied register bit is a perfectly predicting $C$ only if the subsequent $Z$ is genuinely a copy of that already available bit in the marked protocol. Repeating a stochastic meter operation can give a different mark. Copying also changes the scientific question when acquiring the original bit has already perturbed the apparatus.

## Illustration from published counts

The superconducting-qubit archive supplies a circuit with the measurement inserted before two X rotations, and a corresponding unmarked circuit. Treat the recorded proportions temporarily as exact arm masses to calculate the *empirical compatibility intervals*. The archive lacks randomized omission with a duration-matched sham and individual trial chronology. These intervals are neither confidence intervals nor causal measurements of the proposed walk. [Source data and full delay replay](observed_mark_disturbance.md) · [Rudinger et al. dataset](https://zenodo.org/records/5146074)

| Delay | Marked counts $(Z,Y_1)=00,01,10,11$ | Unmarked hits / shots | $1024x$ | $\Delta_0$ | $\Delta_1$ |
|---|---|---:|---:|---:|---:|
| 500 ns | $795,200,18,11$ | $988/1024$ | $[959,988]$ | $[-788,-759]/995$ | $[-18,11]/29$ |
| 2,020 ns | $35,961,8,20$ | $995/1024$ | $[967,995]$ | $[-34,-6]/996$ | $[-8,20]/28$ |

At 500 ns even the allocation of unmarked hits most favorable to mark group zero leaves a large negative group difference. Both signs remain compatible for group one. At 2,020 ns the group-zero empirical upper bound is just $-6/996$. Sampling uncertainty matters particularly at that endpoint. Without the two X rotations, the corresponding zero-group bounds are positive at both endpoints, $[8,28]/1004$ and $[13,33]/1004$. The [exact count replay](check_observed_mark_disturbance.rs) emits the two gated group intervals at all 39 delays.

For a prospective walk run, record the common baseline on every trial, randomize the marked/sham assignment, then independently randomize the remote direct/split choice. Record both the near tag and all resolved terminal cells, with explicit failure outcomes and fixed exposure denominators. Compute the group-effect bounds within each remote arm, accounting for sampling uncertainty and the common baseline. This would test how much a diagnostic operation can change the measured response. Establishing that the baseline label distinguishes physically different detector responses, and that the implemented walk produces the stipulated joint cells, remains necessary for a claim about the ordinary probability rule.
