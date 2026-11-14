# Four binary odds at one site of a signed walk

One excitation starts on the right rail of site 0. Four coin schedules return it to the same two detector ports after ten ticks, with squared rail odds of 1:2, 1:4, 1:8 and 1:16. Other paths reach separately named outputs. The total squared amplitude at the two probe ports is at least 17/32 for every schedule. These are prospective preparations on the program's coined walk. The [monitored three-site phase experiment](phase_cycle.md) uses a different circuit.

## One source, one ring, one read clock

Use a ring of 23 sites. A tick applies the chosen real coin at each site, then shifts R one site right and L one site left. The balanced coin is $H(R,L)=(R+L,R-L)/\sqrt{2}$, $X$ interchanges the rails, and $I$ transmits them. The controls assume independent access to the specified positions and ticks. Time $t$ names the **departure** before a shift. All other coins are $I$.

| Departure | Coin |
| --- | --- |
| $t=0$ | $H$ at the origin |
| $t=1,\ldots,j$ | $H$ at $-t$, where $j=1,2,3,4$ specifies the preparation |
| $t=5$ | $X$ at both $+5$ and $-5$ |

After the initial split the reference moves right with amplitude $1/\sqrt{2}$. It reverses at $+5$ and arrives at the origin on L. The left-moving path takes $j$ balanced splits. Each continuation on L contributes $-1/\sqrt{2}$. The path reverses at $-5$ and arrives at the origin on R with amplitude $(-1)^j2^{-(j+1)/2}$. A path leaving the $t$-th splitter on R stays on R. At tick 5 its position is $5-2t$, strictly between the mirrors, and at tick 10 it reaches $10-2t$, a nonzero site. These exit sites are distinct modulo 23. Hence the two named paths account for the entire probe amplitude, including its sign.

| $j$ | R amplitude at 0 | L amplitude at 0 | Squared mass at 0 | Squared mass at other sites | R fraction within the two ports |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | $-1/2$ | $1/\sqrt{2}$ | $3/4$ | $1/4$ | $1/3$ |
| 2 | $1/(2\sqrt{2})$ | $1/\sqrt{2}$ | $5/8$ | $3/8$ | $1/5$ |
| 3 | $-1/4$ | $1/\sqrt{2}$ | $9/16$ | $7/16$ | $1/9$ |
| 4 | $1/(4\sqrt{2})$ | $1/\sqrt{2}$ | $17/32$ | $15/32$ | $1/17$ |

Thus $x_j=(1+2^j)^{-1}$ is the normalized squared coordinate. It supplies the input to the [four-setting mixture test](four_phase_mixture.md) with odds base $A=2$. The tangent coefficients must be evaluated at that base. A rail sorter can route the two central modes by a common calibrated permutation to a remote pair of named detector cells. Record the other exits, incident counts and missing reports separately. The permutation preserves both central amplitudes. The detector's scoring rule and the population of detector modes among port reports require independent checks. Beam-displacer experiments have implemented polarization-dependent shifts and local wave-plate coins for other measurement networks. This schedule requires its own characterization. [Zhao et al., experimental walk-based measurement](https://doi.org/10.1103/PhysRevA.91.042101)

## Selection can conceal a nonordinary detector

The mixture test needs the same distribution of detector exponent, offset and gain at each accepted binary read, up to any specific common reweighting allowed by its proof. One implementation assumption that suffices is a separate, mode-independent port selector followed by a binary detector whose mode is drawn independently of its accepted input. More generally the distribution among port reports is preserved if acceptance given a preassigned mode factorizes into a setting factor times a mode factor. The measured port fractions alone cannot establish this factorization.

For a counterexample, let half of all launches carry exponent $q=1/2$ and half $q=2$, with zero offset and unit gain. Put $g_q(x)=x^q/[x^q+(1-x)^q]$. For every $x_j$ above,

$$
  t_j=\frac{x_j-g_2(x_j)}{g_{1/2}(x_j)-g_2(x_j)}
$$

lies strictly between zero and one. The rival can also reproduce every ordinary port mass in the table. Write $s=2^{j/2}$ and $m_j=(s^2+1)/(2s^2)$. Give a launch of type $1/2$ port acceptance probability $2m_j t_j$, and a launch of type $2$ acceptance probability $2m_j(1-t_j)$. Substitution into the expression for $t_j$ gives acceptance probabilities $(s+1)^2/[s(s^2+s+1)]$ and $(s^4+1)/[s^2(s^2+s+1)]$, respectively. Their denominators exceed their numerators by $s^3-s-1$ and $s^3+s^2-1$, both positive because $s\ge\sqrt{2}$ and $s^3\ge2s$.

The accepted fraction is $m_j$, and the fraction of type $1/2$ among those accepted is $t_j$. Consequently the incident law for R, L and rejected is exactly $(m_jx_j,m_j(1-x_j),1-m_j)$ under both populations. Even reporting each rejected exit can leave this ambiguity if a rival apparatus may assign its reject label with the ordinary conditional exit proportions in that setting. This construction specifies conditional reporting laws. A calibrated physical selector that enforces a common detector population would rule out that choice.

If instead every terminal well and rail is scored once with a common power and a single global normalization, dividing the R and L counts **within one fixed type** cancels that normalization. Combining types after that selection generally changes their weights at each setting. Keeping the rejected shots makes the acceptance information available for a separate model and calibration.

## Exact replay

The [Rust checker](check_native_odds.rs) evolves all 46 real rail amplitudes in the ring, checks norm conservation at every tick and compares every final rail to the path calculation, including every exit. It also checks an eight-tick alternative. In that version put the mirrors at $\pm4$ on departure 4. Only in schedule $j=4$, replace the left mirror by the fourth $H$. Its R daughter goes to the probe and its L daughter continues outward. All four squared coordinates and port masses agree with the ten-tick schedule. The sign of the weak amplitude in the fourth schedule reverses. The minimum number of ticks remains open.

```sh
rustc --edition 2021 -D warnings check_native_odds.rs -o check_native_odds
./check_native_odds
```
