# How pure can a finite signed clock preparation be?

**Kirtus Justus**, Theoretical Physicist  
Port Coquitlam, British Columbia, Canada

Research supplement by Director G (OpenAI Codex).

A repeated interference measurement can identify the ordinary conjugate pair of a calibrated cyclic sheet. A preparation that approaches that pair can nevertheless have unavoidable leakage at every finite stopping time. The earlier native-preparation theorem gives the exact reason: if a finite branch has integer sheet amplitudes up to one common scalar, its nonzero Fourier support contains full cyclotomic orbits. Here a norm of an algebraic integer gives a bound on the leakage for any order and any number of unresolved output modes. A finite eight-sheet construction identifies the control operation that evades the rational-amplitude premise. [Earlier all-orders obstruction and five-sheet bound](Native_preparations_and_probability_embeddings.md) · [High-yield approximate clocks](Preparing_a_phase_clock.md)

## A bound for a whole accepted branch

Use an order-$M$ sheet with output modes $a$ and real integer numerators $v_{ay}$ in a specified successful coordinate transcript. Let $E=\sum_{a,y}v_{ay}^2>0$ and $P_a(z)=\sum_y v_{ay}z^y$. A common scalar in the actual amplitudes cancels in conditional probabilities. Synchronized Hadamards, signed permutations, coordinate projectors and partial traces over retained orthogonal modes meet the premise after keeping those modes explicit. Addressed permutations can change all coefficients and still preserve their integrality. The bound uses an ordinary squared-coordinate read. Pick a target conjugate pair of order $q>2$ dividing $M$, and let $s=\varphi(q)/2$. In the real cyclotomic field form

$$b=\sum_a P_a(\zeta_q)P_a(\zeta_q^{-1}),\qquad U=ME/2.$$

Its $s$ images $b_i$ are nonnegative and the normalized pair weights are $b_i/U$. If any is positive, all are positive, and $N=\prod_i b_i$ is a positive integer. Indeed, roots of unity are algebraic integers, the embeddings permute their primitive powers, and conjugation changes the sign of the exponent. This uses the norm over the real subfield; the norm over the full cyclotomic field is $N^2$. [Cyclotomic automorphisms, Brian Conrad](https://math.stanford.edu/~conrad/121Page/handouts/cyclotomic.pdf)

Write $e$ for the conditional weight outside the target pair, including all other orders. Then $b_*=(1-e)U$ and the other $s-1$ images sum to at most $eU$. Taking their arithmetic and geometric means gives, for $s>1$ and $b_*>0$,

$$(1-e)e^{s-1}\ \ge\ \frac{N(s-1)^{s-1}}{U^s}.$$

If an integer initial branch has squared energy $E_0$, $t$ complete signed-H layers and intervening permutations or coordinate restrictions imply $E\le2^tE_0$ in the natural unnormalized integer representation. This gives a depth-only bound by taking $N\ge1$. In the order-eight difference seed followed by six plus filters, $E=1584$, $N=1024$, and the exact leakage has $e(1-e)=1/39204$. The depth-only lower bound is $1/4294967296$. The difference matters experimentally. The strict support obstruction extends to positive mixtures of finite transcripts and to successful stopping times supported on finite transcripts. A uniform quantitative bound on the mixture requires controlling its resource distribution. At $q=3,4,6$ the primitive orbit is already a single conjugate pair and this bound on competitors does not apply. [Exact cyclotomic remainders and determinant norms](results/clock_galois_support.json)

For a single occupied output mode with a polynomial of degree $D$ after translating its support and coefficient height at most $H$, each image obeys $b_j\le[(D+1)H]^2$ while $E\le(D+1)H^2$. If the target has positive weight, every competing primitive pair therefore has weight at least

$$\frac{2}{M(D+1)H^2[(D+1)H]^{2(s-1)}}.$$

A nonzero rational polynomial of degree less than $\varphi(q)$ cannot vanish at even one primitive root of order $q$, by its minimal polynomial. Numerator rescaling changes a height-only estimate; the norm-sensitive ratio in the preceding bound is invariant. [Degree thresholds and projector entries](check_clock_galois_support.py)

## An eight-sheet preparation with a coherent idle arm

Start in coordinate zero. Across three layers, apply balanced Hadamards on the following pairs of labeled modes while every other mode is coherently idle: $(0,4)$, then $(0,2)$ and $(4,6)$, then $(2,1)$ and $(6,5)$. Finally permute and sign the six occupied outputs so that the two shallower leaves sit on antipodes and the four deeper leaves on odd sites. In natural sheet order the resulting normalized amplitude is

$$\frac1{2\sqrt2}(\sqrt2,1,0,-1,-\sqrt2,-1,0,1).$$

These entries are $\tfrac12\cos(\pi y/4)$, giving precisely the pair $k=\pm1$ at unit yield. Idle and walked modes meet again with a specified relative phase. Two leaves experienced two Hadamards while four experienced three, so dividing out their common scalar leaves coefficients in $\mathbb Q(\sqrt2)$. Its real generator already distinguishes the two primitive real pairs at order eight. Maintaining the coherent phase between these unequal-depth branches is a physical resource. A classical choice between different synchronized runs retains the positive-mixture obstruction. For other orders, the subgroup fixing the admitted coefficient field determines the surviving orbit. This example supplies neither a general exact preparation at arbitrary order nor a selection of an absolute probability law. [Literal circuit and exact Fourier support](results/clock_galois_support.json) · [Connection to the mechanical and ruler records](Finite_speed_mass_and_motion.md)

An actual binary port makes this distinction measurable in the model. Split a clean comparison rail by $H$, translate the second arm by the held physical $T$, recombine by $H$, and count both rails, summing all eight sheet coordinates. For the normalized sheet state $v$, $P_+=(1+\langle v,Tv\rangle)/2$. The one-step overlap is $1/\sqrt2$. Applying the nontrivial automorphism of $\mathbb Q(\sqrt2)$ to the *whole specified algebraic circuit*, with its signed permutations fixed, sends each normalized Hadamard to $-H$. Where every path experiences the same number the sign cancels. The coherent idle branch retains it here: two-H leaves keep their signs and three-H leaves reverse, producing the complementary pair $k=\pm3$. The two Hadamards of the final comparator cause no additional sign difference. The same physical port therefore has two predictions,

$$ P_+^{\rm ord}=(2+\sqrt2)/4,\qquad P_+^{\rm alt}=(2-\sqrt2)/4.$$

Their sum is one and their separation is $1/\sqrt2$. The observable cylinder generates the full real field $\mathbb Q(\sqrt2)$ for this apparatus, in contrast with rational cylinders under synchronized launches. If the stroke is also replaced by $T^3$, the alternate pair again has positive overlap $1/\sqrt2$. Thus a real phase-sensitive controlled bypass and a held, identified unit stroke supply a finite discrimination experiment. No observation of that apparatus is reported here, and the inference reaches only the embeddings distinguished on its probability field. [Both terminal ports and transformed-stroke control](results/clock_galois_support.json) · [Observable-field criterion](Native_preparations_and_probability_embeddings.md)

A [synchronized rational comparator and optical control](Rational_references_and_optical_bypass.md) quantify the resources for holding the acted/idle phase fixed. A [retained real reference plane](A_rational_plane_for_cyclic_phase.md) establishes relative sine and cosine measurements on a cyclic sheet.
