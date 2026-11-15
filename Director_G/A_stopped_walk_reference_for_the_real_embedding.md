# A stopped walk reference for the real probability embedding

Can a sequence of the walk's own binary records make an exact reference for an irrational position probability? A counter driven only by balanced recorded steps produces the complete first-address distribution of the specified real coin. The same counter runs independently of the sign chosen for the coherent addressed gate. Comparing the two outputs can therefore test their operational agreement. Their shared numerical label alone cannot fix the gate's sign.

## One counter and three finite records per round

Start a classical counter at one. Obtain three fresh fair bits in each round. For example, from a known site and sharp incoming rail a balanced Hadamard, shift and full position read yield a fair direction and a sharp outgoing rail. Repetition supplies the bits if the next direction is conditionally fair on the entire reached history. Reading the actual shifts and keeping an integer counter and branch controller are required resources. The stopped counter below is distinct from the physical position of the qubit walk generating the bits.

Assign one of eight words to down, one to up, two to hold and four to stop with failure. A down step reaching zero stops with success. Let $u_j$ be the hit probability from $j$. An unresolved run after $N$ rounds must have avoided every kill so far, giving probability at most $2^{-N}$. Thus $u_0=1$, $0\le u_j\le1$, and first-step conditioning gives

$$
 6u_j=u_{j-1}+u_{j+1}\qquad(j\ge1).
$$

The characteristic roots are $3-2\sqrt2$ and $3+2\sqrt2$. Boundedness removes the second root and $u_j=(3-2\sqrt2)^j$. At each reached round the probability of a kill is $1/2$. Consequently $E[T]=2(1-u_1)=4(\sqrt2-1)$ rounds from one; individual runs can be arbitrarily long. The same root arises from the first-passage generating function of a simple symmetric walk after deleting holds and counting the independent kill hazard. [Lalley, *One-dimensional random walks*, first-passage generating function](https://www.stat.uchicago.edu/~lalley/Courses/312/RW.pdf)

## The public address reference

Draw a separate fair three-bit mask. Five mask cells report code 1, one reports code 2, one reports code 3, and the last runs the counter. In that last cell a hit reports 2 and a kill reports 1. No cell reports 0. Code probabilities in order are

$$
 \left(0,\frac{6-u_1}{8},\frac{1+u_1}{8},\frac18\right)
 =
 \left(0,\frac{3+2\sqrt2}{8},\frac{2-\sqrt2}{4},\frac18\right).
$$

These are the three-tick specified-matrix rates in the [addressed rail-coin experiment](../candidates/composition_record/velocity_experiment/addressed_embedding.md). Fixed conjugate matrices with ordinary squared weights on the same port labels have total variation distance $\sqrt2/2$ from this reference. Interleaving reference and science launches and comparing the reported distributions tests a relation between two preparations. The reporter must preserve corresponding codes across arms. Count all incidents on the assigned arm. The mask can be run first, reducing the expected reference cost to $3+3E[T]/8$ fair bits.

At a finite deadline retain “unresolved” as its own outcome. If $h_N$ is the probability of hitting by round $N$ and $v_N$ the probability of still being live in the counter arm, the completed code-one rate lies in $[(6-h_N-v_N)/8,(6-h_N)/8]$. The width is at most $2^{-N}/8$. At eight rounds the [two exact counts](check_stopped_radical_reference.py) give width $12155/67108864$, about $0.000181$. The fixed-deadline counts use dyadic probabilities throughout. Exact matching of the algebraic number uses the infinite union of the stopped hits. Monotonicity on nested events already squeezes any assigned completion probability between the finite bounds as the unresolved mass vanishes.

Two controls clarify the inference.

* A source can make every prescheduled symbol marginally uniform while correlating successive rounds. Draw each odd symbol uniformly and on the even round exchange up and down, leaving holds and kills fixed. At pair boundaries the only surviving launches are back at one. First-round down hits, first-round kill fails, and up or hold survives the pair. The eventual hit rate becomes $1/5$, despite almost-sure termination. The joint conditional prefix law matters.
* The reference itself never applies a coherent addressed gate. Conjugate every $\sqrt2$ in the coherent program while reversing the relative sign of its odd-address Hadamard. The real addressed operation and every branch distribution then agree with the original description. The stopped reference is unchanged too. A physical comparison can establish that the two output laws match at these labeled ports. Inferring an absolute gate phase or a single algebraic embedding for every experiment requires a further transfer assumption. [Coherent comparison and its scope](../candidates/composition_record/velocity_experiment/a_phase_reference_from_synchronized_walks.md)

## Why finite clocks and finite memory matter

Consider any fixed finite-dimensional, time-homogeneous device with a rational initial vector $x$, a rational unnormalized continuation map $C$ and a rational hit row $h$ in a common coordinate system. The probability of first recorded hit at tick $t\ge1$ is $p_t=hC^{t-1}x$. This includes classical finite-state instruments and finite quantum instruments when their density-operator maps have rational matrices. For example, conjugation by a uniform $H$ has rational coefficients in matrix-unit coordinates because each entry uses two Hadamard factors. Finite classical control can be included as direct-sum sectors. The hypothesis concerns the unnormalized maps, so conditional normalization inside a reported branch introduces no new resource by itself.

The generating function $F(z)=\sum_{t\ge1}p_tz^t$ is the rational function $z h(I-zC)^{-1}x$ near zero. Nonnegative first-hit masses sum to at most one. The scalar power series therefore converges for $0\le z<1$ and has finite limit $\sum_t p_t$ at one. After cancelling common factors, a rational function over $\mathbb Q$ with a finite limit there has a rational value. This works even if modes of $C$ survive forever; no inverse at $z=1$ is required. Thus unlimited *time* alone cannot give this irrational reference to a device in the stated finite rational class. The half-line counter supplies unbounded state. A coherent bypass with an irrational density map or an irrational input need not obey this obstruction.

## Other positive square roots

For a positive nonsquare integer $d$, choose an integer $n>\sqrt d$. Take a power-of-two alphabet $D\ge2(n^2+d)$. Allocate $n^2-d$ cells to each direction, $4d$ to kill, and the remaining cells to hold. The same first-step equation has reciprocal roots $(n-\sqrt d)/(n+\sqrt d)$ and $(n+\sqrt d)/(n-\sqrt d)$. Exactly the former is a bounded probability from one. The unresolved probability at $N$ rounds is at most $(1-4d/D)^N$. Inverting the measured scalar relation gives $\sqrt d=n(1-u_1)/(1+u_1)$ as an ordinary real number. No gate rotation by that angle or externally stored digit expansion of the root is used.

If one embedding of a real multiquadratic field is required to act on these *completed event probabilities* by their displayed field expressions, it must preserve each positive generator tested in this way. Changing its sign would assign a probability greater than one. An alternative that scores rational finite transcripts and takes their bounded limit will predict exactly the same stopped records under either algebraic label. Requiring substitution in the closed-form field expression to commute with that limit is precisely where the two statements differ. Nothing here derives conditional fairness for the native records or an unrestricted Born rule from prephysical primitives.

Kirtus Justus, Theoretical Physicist, Port Coquitlam, British Columbia, Canada, holds scholarly responsibility. OpenAI Codex developed the stopped reference, the finite-memory obstruction and the exact replays.
