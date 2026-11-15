# Preparing a force with the order of two contacts

**Kirtus Justus**, Theoretical Physicist, Port Coquitlam, British Columbia, Canada. Research supplement by Director G (OpenAI Codex).

The [two-contact walk](contact_flight.md) assumed that someone supplied its weak-force character. Starting from a blank contact register, a real two-route instrument can herald the pair of conjugate characters that produce the weak field. Their force signs are opposite. Encoding the launch phase with the same register also reverses the band curvature and the launch momentum between them. The resulting **position distributions agree at every tick**. This removes the need to prepare one oriented character for this mechanical observable. The growing-prime family, coherent controls, ordinary probabilities and physical clock are still premises. The [original candidate review](README.md) records the counterexample to its proposed origin of a first record.

## A binary interference test of contact order

Use the field of odd prime order \(p\ge5\), the stipulated Heisenberg register \((r,l,z)\), and precisely the generators \(g,h\) of the two-contact walk. A chronological \(gh\) has one more central unit than \(hg\), with identical ordinary coordinates. For a positive word with \(d\) of each generator, relative to \(h^d g^d\), its central increment counts the \(g\)-before-\(h\) pairs. For \(0\le s\le d^2\), write \(s=fd+b\) with \(0\le b<d\). If \(f<d\) use

\[
 w_s=g^f h^{d-b} g h^b g^{d-f-1}.
\]

At \(s=d^2\) use \(g^d h^d\). These are two histories with identical ordinary endpoints and length \(2d\). Taking \(d=\lceil\sqrt{p-1}\rceil\) realizes every central residue, including zero, with a common contact clock. The [Lean proof](ContactOrder.lean) verifies the integer doubling of the group law, contextual adjacent swaps and all areas, including the two endpoints. Reduction modulo an odd prime gives the displayed contact identity. The quadratic area growth is related to the word metric of the discrete Heisenberg group. [Blachère, word distance](https://doi.org/10.4064/cm95-1-2)

Prepare a balanced real path bit. On its two arms apply \(w_0,w_s\), then apply the same inverse \(w_0^{-1}\) to both. Recombine on a second real Hadamard, recording bright as \(B=1\) and dark as \(B=-1\). The two final register actions are identity and translation by \(s\) on the center. This requires controllable ordered calls, inverse calls, erased routing labels and the same unused degrees of freedom on the two arms. A free walk has additional paths and generally different final rails. An unintended copy of the path yields a zero-mean contrast for every \(s\), even \(s=0\). The zero-shift control directly checks that failure. Each query costs \(4d\) sequential generator calls along an arm plus real path control. The preparation is completed at one common origin before a spatial packet is attached. If the common displacement is left uncompensated on a packet, the ordinary coordinates may imprint a phase varying with the launch site.

In the Fourier convention \(T_s\mapsto e^{-2\pi i k s/p}\), the conditional mean of \(B\) is \(\cos(2\pi k s/p)\). Draw \(s\) uniformly and independently on each round. Give its score the sign \(J_s=+1\) for centered \(2s\bmod p\) in \([-\lfloor p/4\rfloor,\lfloor p/4\rfloor]\), and \(-1\) elsewhere. Define \(\mu_k=\mathbb E[J_s B\mid k]\). Multiple-pass interrogation of a phase has a demonstrated optical implementation. Here the phase comes from reordering equal-length words, and the sign uses a fixed arithmetic partition of settings. No measurements of this register are available. [Higgins et al., experiment](https://arxiv.org/abs/0809.3308)

For \(L=2\lfloor p/4\rfloor+1\), let \(n\) be the absolute centered residue of \(k\,2^{-1}\). Summing the Fourier series of that interval gives, at \(n>0\),

\[
 \mu_k=\frac{2\sin(L\pi n/p)}{p\sin(\pi n/p)}.
\]

At \(k=0\) the mean is \((2L-p)/p=\pm1/p\). Since \(L=(p\pm1)/2\), for odd \(n\) the absolute coefficient is \(1/[p\sin(\pi n/(2p))]\); for even \(n\) it is \(1/[p\cos(\pi n/(2p))]\). Both target characters \(k=\pm2\) have positive mean exceeding \(2/\pi\). Odd \(n\ge3\) gives at most \(1/n\) by concavity of sine, and even \(n\) gives less than \(\sqrt2/p\). Thus **every other sector has absolute mean at most \(1/3\)**. The choice of quadratic area and the arithmetic sign mask is specific to this preparation.

## Acceptance, cost and the blank-memory bound

Run \(m\) rounds on the same memory, with a fresh path bit and fresh independent setting. Accept a launch if its average signed score is at least \(1/2\), counting threshold ties. Each complete measurement branch is diagonal in the central Fourier label after resetting the ordinary coordinates. Conditional on \(k\) the scores are independent, with probability \((1+\mu_k)/2\) of \(+1\). A blank supplies prior \(1/p\) per sector. The exact pass likelihood is an upper binomial tail, including all unsuccessful outcomes in the incident denominator. Applying the bounded-variable Hoeffding inequality gives target miss probability at most \(a=\exp[-m(2/\pi-1/2)^2/2]\) and any other sector pass probability at most \(b=\exp(-m/72)\). The incident pass probability is at least \(2(1-a)/p\), and the posterior weight outside the target pair is at most \((p-2)b/[2(1-a)+(p-2)b]\). For target error \(\eta\) and fixed completeness bounded away from zero, \(O(\sqrt p\log(p/\eta))\) calls per launch suffice. The bound is conservative.

| Register order | Rounds | Chance to accept a blank launch | Weight on selected pair after acceptance |
|---:|---:|---:|---:|
| 5 | 64 | 0.382169 | 0.995436 |
| 31 | 64 | 0.060719 | 0.997080 |
| 127 | 64 | 0.014844 | 0.995173 |

The yield has an intrinsic restriction. Right multiplications commute with every central translation. So do walker-only operations, their controlled compositions, and the path measurements here. For the folded projection \(P=P_2+P_{-2}\), if every complete-branch Kraus operator \(A_b\) commutes with \(P\), completeness gives \(\sum_b A_b^\dagger P A_b=P\). This applies also after feedback with all terminal outcomes counted. If the accepted fraction is \(\alpha\) with conditional leakage at most \(\eta\), positivity forces \(\alpha(1-\eta)\le2/p\). Collecting every branch without a herald preserves the original \(2/p\) exactly. An instrument mixing individually addressed central memory cells changes this restriction. A direct example is a Hadamard between the blank and its neighboring central address. The symmetric output has folded target weight \((2/p)[1+\cos(4\pi/p)]\), which differs from \(2/p\) for every odd prime here. This intervention requires addressing the memory coordinates themselves.

Even a successful real transcript assigns equal weights to \(+2,-2\). Furthermore, on any finite positive branch of these real binary Hadamards and permutations, the real-space central coefficients, conditional on a particular setting word, are integers up to a common factor. A nonzero polynomial of degree less than \(p\) on those coefficients that vanishes at any primitive \(p\)th root must vanish at all primitive roots by cyclotomic irreducibility. Thus at \(p\ge5\) such a finite branch with target mass cannot exactly erase all the other nonzero characters. Mixtures of branches cannot cancel positive leakage. Our estimates only claim approximate selection. [Related finite-branch obstruction](../../Director_G/Native_preparations_and_probability_embeddings.md)

## One real packet for both sign choices

Let \(a_{x,b}e^{i\theta_{x,b}}\) be a specified normalized input spinor in real space, \(a_{x,b}\ge0\), with rail \(b\). Supply its **real amplitude profile** \(a\). Coherently conditioned on the site and rail, translate the center by

\[
 c(x,b)=2^{-1}\operatorname{round}[-p\theta_{x,b}/(2\pi)]\pmod p .
\]

For \(+2\) the resulting multiplier differs from the intended complex phase by at most \(\pi/p\) in modulus. The norm error of the whole normalized packet is at most \(\pi/p\), independent of width and propagation time. Round the accumulated angle at each address. Rounding one generator for a linear phase and repeatedly applying it can accumulate an error of order one across a wide packet. A central shift can itself be synthesized from the two ordered words and an inverse. Addressing a whole spatial profile or preparing its real magnitudes requires additional coherent controls. No bound on the cost of constructing that controller is implied by the herald's contact count.

Include the synchronized ordinary labels \((x/2,-x/2)\) and central offset \(x/4\) from the [contact-flight encoding](contact_flight.md). Decode the terminal ordinary coordinates and the known central endpoint offset there. In sector \(+2\) this gives the electric walk with departure factor \(\exp(-2\pi i x/p)\). In sector \(-2\) the prepared packet, the field factor and the entire propagator are their complex conjugates. Hence these two sectors predict the same probability for **every named site and rail at every clock**, including with real coordinate masks in a subsequent sequence. Off-diagonal sector coherences drop out when tracing the memory. With herald leakage \(\eta\), the position law on accepted launches differs from the ideal oriented input's law by at most \(\eta+\pi/p\) in total variation. This bound is for unconditional future reads given the herald. A further rare postselection needs its own denominator.

For the packet in the [uniform-force estimate](../../Director_G/Forced_envelope_and_classical_motion.md), the positive-curvature band is centered at \(k_*=-\pi/2\) with edge spinor \((1,-i)/\sqrt2\). Its conjugate is centered at the opposite band edge with opposite curvature and opposite force. The observed acceleration agrees. At \(2\pi/p=F\varepsilon\delta^3\), select leakage tending to zero and use the same normalized scalar packet as in that estimate. At fixed \(\varepsilon=1\), the \(+2\) component approximates the forced Schrödinger envelope in norm and the \(-2\) component its conjugate. Their common position distribution approaches the envelope's position law. At \(\varepsilon=\delta\to0\) with the specified shrinking packet it concentrates at \(Y_0+p_0t-Ft^2/2\). The unresolved absolute orientation matters for a complex phase observable. The two signs produce the same physical position record already at finite spacing under the real protocol. Experiments have realized an electric quantum walk by imposing an extra phase per step. Its physical carrier differs from this proposed memory. [Genske et al., experiment](https://arxiv.org/abs/1302.2094)

These statements use ordinary squared probabilities and a calibrated supply of coherent controls. A classical choice of one Fourier label per launch followed by its conditional quantum walk reproduces the entire path-bit and position transcript. A measurement of the memory in a different basis would be needed to test that alternative. The contact order supplies a preparation and a common mechanical record within the stipulated model. The physical origin of its control and probability law remains open.

Run the [checker](check_sector_preparation.py) with Python from this directory. It multiplies both actual contact words and their inverses for every setting, compares the mask spectrum with a direct sum, and propagates real-space integer contact flights separately from their two complex field recurrences. The [stored results](sector_preparation.json) include all sector means, pass rates and named packet outputs across the tested clocks. The angular and propagation comparisons use binary64 arithmetic; the word and Lean identities are exact.
