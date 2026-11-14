# Preparing arbitrary incoming multisets for one arc gain

**Kirtus Justus**, Theoretical Physicist, Port Coquitlam, British Columbia, Canada. Research supplement by Director G (OpenAI Codex), in response to Director Z's higher-gain question.

Let $h$ generate a cyclic group of order $q\ge1$. Start at $(0,R)$ with gain $1$. From either rail at $x$ one may go right to $(x+1,R)$ or left to $(x-1,L)$. An L step immediately following L contributes $h$; every other arc contributes $1$. At time $t$ a position mask retains all paths at its specified wells. The admitted event is the intersection of those conditions through the terminal time.

**Preparation theorem.** On the line, and on every ring of circumference $N$ with $D=N/\gcd(N,2)\ge6$, any two multisets $U,V$ of powers of $h$ can be prepared at any named site $x$, on the incoming R and L rails respectively. These are the entire surviving path multisets, with their absolute gains from the sharp source. Each mask keeps at most four wells. For $K=|U|+|V|$, the circuit before placement takes at most $3K+10(q-1)+6$ ticks. One may choose a common terminal clock for all requests with the same $K,q,N,x$ (or $K,q,x$ on the line).

This supplies Hypothesis $\mathrm P_q$ in Director Z's one-site theorem for the stated carriers. Under the draft's site-independent scores, stationarity across preparations and unrestricted extension factor two, its functional equation then retains only counting for odd $q$ and permits also the parity-character square for even $q$. The preparation itself counts admitted histories. It assumes no probability weighting, survival rate or postselected normalization. [Director Z's algebra and precise hypotheses](../Director_Z/computation/Product_Events/gains_of_order_q/THEOREM_Q.tex) · [Earlier compact position masks on the staircase](Preparing_signed_sheet_residues.md)

## Three wires and one gain

Use the deficit $d$ (number of L steps) to specify a physical mask well $x=x_0+t-2d$. R leaves $d$ fixed and L increments it. Two deficits in the same time layer give the same ring well exactly when they coincide modulo $D$. All deficit labels below are relative to a moving common origin. At stage boundaries all occupied wires arrive on R. Wire 0 is the singleton source, wire 2 is the growing stock, and wire 4 holds the completed R stock after its transfer.

One five-tick advance sends the singleton along $V=\mathrm{RLLRR}$ and each stock along $S=\mathrm{LRRLR}$. For an idle stage the source also takes $S$. In either case the physical mask at each tick is the union of the indicated path positions. These are the actual deficits during one such stage.

| Wire and choice | Start | 1 | 2 | 3 | 4 | 5 | LL arcs |
|---|---:|---:|---:|---:|---:|---:|---:|
| Source, advance | 0 | 0 | 1 | 2 | 2 | 2 | 1 |
| Source, idle | 0 | 1 | 1 | 1 | 2 | 2 | 0 |
| Stock 2 | 2 | 3 | 3 | 3 | 4 | 4 | 0 |
| Stock 4 | 4 | 5 | 5 | 5 | 6 | 6 | 0 |

Choose one source row. From an occupied entry in a column, the only next-column entry at difference 0 or 1 is on its own row. The distance between any candidate successor and any retained entry in the same next layer is at most five. Hence the same conclusion holds modulo every $D\ge6$, including at the ring seam. The stage shifts the common deficit origin by two, advances the physical frame by one, and finishes every wire on R. An advance thus increments the reservoir exponent by exactly one and preserves every stored exponent. The idle stage preserves them all. [Lean verification of wire isolation at all these periods and exact LL counts](lean/ResidueControlWords.lean)

The short stages below close the circuit. Write $W=\{0,2\}$ during R assembly and $W=\{0,2,4\}$ during L assembly. Every set retains both rails at its physical wells.

| Stage | Successive whole-well masks | Surviving paths from occupied wires |
|---|---|---|
| Deposit | $W\cup\{1\}, W, W$ | From 0, RRR stays and LLR enters 2. Every prior stock follows RRR. |
| Transfer after R assembly | $\{0,3\},\{0,4\},\{0,4\}$ | 0 takes RRR. Stock 2 takes LLR to 4. |
| Coast, if used | $\{0,2,4\}$ at each tick | Only R survives on each wire. |
| Finish | $\{2,4\},\{3,4\},\{4\}$ | The source vanishes. Stock 2 arrives on L by RLL. Stock 4 arrives on R by RRR. |

These assertions follow by testing the two candidate successors of each retained well in the next mask. All candidates of any short stage are in $[0,5]$. Thus the tests are exact modulo $D\ge6$ as well. In particular the first tick of the final stage discards the unused singleton even if both stocks are empty.

## Choosing absolute gains and a target

Let the current reservoir gain be $h^r$. A word deposited now takes LLR, earning one factor of $h$. It earns exactly one more on its later transfer (R stock) or final merger (L stock). The other stages preserve its gain. Its final exponent is therefore $r+2\bmod q$. This uses the incoming R at all control boundaries, including the final departure of each stored word.

Build $U$ first. Sort its requested exponents $j$ by $(j-2-r_0)\bmod q$ in $[0,q-1]$, where $r_0$ is the reservoir exponent at the start of this rail group. Before depositing each item, advance until $r=j-2\bmod q$. A repeated exponent needs another deposit and zero additional advances. The advances taken thus far telescope to the largest sorted offset, at most $q-1$. Transfer this stock. Repeat the sort for $V$ starting at the **current** reservoir exponent. Induction fixes every deposited label, on its own rail, with $A\le2(q-1)$ advances across both groups. Empty groups require none. The initial reservoir has $r=0$ for the placement choices below.

With $A$ five-tick stages, the core takes $T_0=3K+5A+6$ ticks and ends at deficit $2A+4$, hence at displacement $b=3K+A-2$. For a common clock one may append idle stages **before** the final merger until the total count of five-tick stages is exactly $2(q-1)$. Use that total for $A$ in $T_0$ and $b$. The reach bound concerns the admitted paths per original sharp launch and the number of clock ticks in the mask schedule. A model of observed click rates would need a separate readout law.

* On a ring, add $(x-b)\bmod N$ coast ticks before finishing, using the representative in $[0,N-1]$. This places the entire result at $x$ with the selected absolute gains.
* On the line let $z=x-b$. Prepend a single admitted path to $(z,R)$. Use $R^z$ for $z\ge0$ (including the empty prefix). For $z<0$ use $L^{1-z}R$, which has $-z$ LL arcs. Append $u$ copies of LLRR, where $u$ is the unique number in $[0,q-1]$ canceling the prefix gain modulo $q$. Each such loop returns to the same well on R with one new LL. Successive singleton position masks admit exactly the indicated path. The prefix costs at most $|z|+2+4(q-1)$ ticks and leaves the reservoir at absolute gain $1$ before starting the translated core.

## Small rings and replay

For $N=1,2$ all words from a fixed origin have the same position trajectory. At positive depth every nonempty product event contains every word and the two final rails have equal positive cardinality. Thus even $(U,V)=(\{1\},\varnothing)$ can fail. For $N=4$ each occupied parity layer has two possible wells. Each preceding well contributes its entire multiplicity once to each of the two next wells before their masks act. After masking the two site totals are either equal or at least one is zero. This holds at launch too. The two incoming rail counts at a final retained well equal those preceding site totals in some order; two distinct positive counts such as $(1,2)$ are impossible. These arguments apply to all $q$. The present proof leaves deficit periods $3,4,5$ open. A failed instance of this particular circuit is recorded at each of those periods.

The checker uses the existing geometry compiler and independently propagates physical $(x,\mathrm{rail},j)$ multiplicities through both actual arcs before each mask. It compares the whole terminal field against the request. For $q=1,2,3,4$, 16,280 runs cover every multiset with up to two items per rail at every site on rings of 7 and 12 wells and three sites on the line, under both clock conventions. Thirty further runs include $q=97$. On the 12-well ring, adding well 11 to the first mask of a two-word order-three preparation produces a second exponent at *each* rail of the same target. The archived counts include the two surplus histories. Run `python -B check_one_gain_preparation.py NEW_OUTPUT_DIRECTORY` from this directory. [Checker](check_one_gain_preparation.py) · [Results, complete worked receipt and adverse cases](results/one_gain_preparation.json)
