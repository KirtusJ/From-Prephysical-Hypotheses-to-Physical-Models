# Does a site detector normalize each stored label separately?

**Kirtus Justus**, Theoretical Physicist, Port Coquitlam, British Columbia, Canada. Research supplement by Director G (OpenAI Codex).

An unread local copy can constrain a detector that totals the amplitudes' squared moduli across its internal labels before scoring each well. A detector might instead calculate a normalized position law inside each label, then combine those laws. We give a forward preparation in which a reversible change of one stored bit at two wells leaves all four spatial populations exactly unchanged. Under the label-conditioned power law every exponent except one produces a remote contrast of one sign. A single finite setting pair consequently tests arbitrary mixtures of positive exponents and controls both extreme tails. [Dyadic site-score comparison](Local_writes_and_dyadic_site_scores.md) · [Remote-position contrasts for a globally normalized power](Remote_position_counts_and_the_spatial_probability_law.md)

## A preparation from one sharp source

Use a flat line or twenty-well ring. All walkers start at zero on R with three blank routing bits $a$ and a distinct blank branch bit $\ell$. Balanced real Hadamards on the four bits give sixteen equal kinematic amplitudes, each $1/4$. Route by $a$ using reversible rail permutations and the ordinary rail-directed nearest-neighbor stream. The six-tick schedules, independent of $\ell$, are

| Routing number | Directions | Final site |
|---|---|---:|
| 0, 1 | RRLLLL | $-2$ |
| 2, 3 | RRRLLL | $0$ |
| 4, 5, 6 | RRRRRL | $4$ |
| 7 | RRRRRR | $6$ |

Each step chooses straight or exchange for the known incoming rail of each route. At site zero apply a fixed sign to $\ell=1$. Thus at each route the local branch vector is proportional to $(1,1)$ at $-2,4,6$ and $(1,-1)$ at zero. Choose whether to apply the real Hadamard on the branch bit at **both** $-2$ and zero, holding all other systems and clock fixed. No route is postselected. Read one of the remote wells, $4$ or $6$, at the matched terminal surface. The alternative settings must leave those two regions causally isolated from the two local pulses and any common control feed before readout. The two pulses can be scheduled from one independent random setting after the source has been launched. The construction requires coherent control of the branch bit and label-dependent routing, beyond an unmodified walk with a fixed coin.

In units of $1/16$, the site masses, obtained by adding over rail and routing number within a specified value of $\ell$, are as follows. Branch and total masses are preserved separately.

| Setting and branch | $-2$ | $0$ | $4$ | $6$ | Total |
|---|---:|---:|---:|---:|---:|
| Idle, either branch | 2 | 2 | 3 | 1 | 8 |
| Mixed, branch 0 | 4 | 0 | 3 | 1 | 8 |
| Mixed, branch 1 | 0 | 4 | 3 | 1 | 8 |
| Both branches combined, either setting | 4 | 4 | 6 | 2 | 16 |

The late Hadamard is a reversible rotation of the bit. A permutation of the names of two resolved outcomes cannot implement it. If an inaccessible copy of $\ell$ has already distinguished the two amplitudes, the rotation cannot produce the local interference. At $-2$, for example, an incoherent equal mixture of the two input branches gives nonzero mass in both output branches, whereas the coherent preparation has zero mass in branch 1. A separate local resolved check on identically prepared launches can probe that distinction.

## A comparison independent of the branch weights

Take as the rival a rule that first groups the full terminal coordinates by $\ell$. Inside each group it raises the group's site masses to the same positive power $q$, normalizes by their sum of powers, then combines the resulting position laws with nonnegative branch weights summing to one. Dividing each nonzero row by its own kinematic total before powering gives exactly the same conditional law. The two branches can be mixed in different proportions in the two settings and the proportions can depend on $q$. What matters is that for each $q$ the two rows have identical **remote** conditional rates within each setting. Equivalently, the fraction assigned to each $(q,\ell)$ may be arbitrary provided the marginal exponent law on launched trials is common to the two settings. An exponent distribution chosen differently for different interventions or monitored wells changes the test.

For an individual exponent define
$$
 D(q)=\frac{1}{3^q+1+2\,2^q}-\frac{1}{3^q+1+4^q}.
$$
The idle-minus-mixed remote differences are $\Delta_4(q)=3^qD(q)$ and $\Delta_6(q)=D(q)$. Define $W(q)=\Delta_4(q)-3\Delta_6(q)$. Its two sign-determining factors are $3^q-3$ and $4^q-2\,2^q$, which both have the sign of $q-1$. Therefore $W(q)>0$ for every positive $q\ne1$ and $W(1)=0$. For $q=2$ the remote rates are $(9/18,1/18)$ and $(9/26,1/26)$, giving $W=4/39$ per launch. Compare separately assigned launch samples at the same terminal clock, retaining no-click outcomes. The coefficient three comes from the kinematic weights of the remote wells. Any deterministic common response applied after aggregating the labels gives identical rates in the two settings for each remote well, since its whole spatial input is identical. It need not be a power law. Within the rival class it is precisely the response's dependence on the hidden partition that this experiment tests.

Let $\nu$ be a positive subprobability measure describing the launches subject to the branch-power rule, with the remaining launches following any law contributing zero to both remote differences. The measured witness is $\int W\,d\nu$ under the stated response and sampling assumptions. If it vanishes, $\nu$ is concentrated at one. The two limits are
$$ \lim_{q\downarrow0} W(q)=1/6,\qquad \lim_{q\to\infty} W(q)=1. $$
At small $q$ the two monitors each change from $1/4$ to $1/3$; at large $q$ the idle row concentrates at $4$ and either mixed row concentrates on a local well. Thus for $\delta>0$, $c_\delta=\inf_{q>0,\ |q-1|\ge\delta} W(q)>0$ by continuity on the compactified domain and strict positivity away from one. A simultaneous upper bound $B$ on the absolute-rate combination gives $\nu(|q-1|\ge\delta)\le B/c_\delta$. Two remote equalities separately need only positive common efficiencies within each well across the settings. Using nonzero rate differences quantitatively requires known relative efficiencies, correction or bounds. Conditional click fractions or an unknown setting-dependent loss of whole launches can change the result.

## What the unchanged remote records leave open

- A fair forward marker with fixed route and no response to a local branch rotation keeps its remote rates unchanged. It contributes zero to this contrast, as does the ordinary $q=1$ law. The test bounds the fraction using other exponents on the specified partition and cannot identify the total fraction using that partition.
- A rule may normalize separately on the **finer** label $(a,\ell)$. Each occupied such group in this preparation has a single occupied site, so every exponent gives that site with probability one. Assigning groups their kinematic masses then gives the ordinary remote rates at both settings. The protected routing bits and their operational grouping therefore have to be specified. This construction provides no argument eliminating all hidden refinements or all possible functions inside a branch.
- If the label is genuinely classical before the choice, the stipulated coherent rotation on $(1,\pm1)$ cannot restore the corresponding interference. Conversely a device can have coherent amplitudes while using a branch-indexed rule only at terminal readout. This is the rival addressed here. A common failure in both records, a monitor that sees the controller, or a change in the incident exponents requires a distinct control.

The [integer path checker](check_local_label_mixing.py) reconstructs the four spatial populations and all branch amplitudes, scans extremely biased branch weights, and retains the zero-exponent limit, the large-exponent tail, an asymmetric-monitor mutation and the finer-label escape. [Exact original-launch predictions](results/local_label_mixing.json) · [Lean integer certificate](lean/LabelRateContrast.lean)

The local invariance comparison is related to operational causality tests. The theorem about the particular branch-power family follows from the displayed finite populations and monotonicity, with no general causality theorem imported. [Beckman, Gottesman, Nielsen and Preskill](https://arxiv.org/abs/quant-ph/0102043)
