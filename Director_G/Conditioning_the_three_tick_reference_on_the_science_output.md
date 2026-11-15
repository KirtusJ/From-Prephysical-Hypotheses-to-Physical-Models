# Three ticks test the readout when the science output is retained

**Kirtus Justus**, Theoretical Physicist, Port Coquitlam, British Columbia, Canada. Research supplement by Director G (OpenAI Codex).

The [four-tick reference](Four_ticks_after_a_recorded_walk_output.md) tests an exponent on the same launch as the science measurement by counting the appended positions across all old outcomes. A detector that secretly resolves the two arrival rails can defeat that comparison. Keeping the *joint* table permits a shorter test. After three ticks, count one outer arrival separately at every saved science label. If its rate is one eighth of each row total, then a fixed nonuniform science spectrum selects the ordinary power, even when the detector secretly chooses whether to resolve the final rails. This selection uses a common way of grouping the rails across old labels **within each launch**.

## The three-tick position table

Retain an orthogonal pointer to the completed science outcome \(i\), including the final position and rail. Advance the same reflecting Hadamard walker three ticks, leaving the pointer and any private environment on the old branch isolated. The final read resolves the pointer and the new site. For at least four wells, each old directed mode supplies the following four positions; displacements are measured on the unfolded line along its old rail. Physical wells follow by folding as in the four-tick construction. Eight physical direction words suffice to check the table. A power acting on the complete joint table means a terminal sampling law and supplies no nonlinear update rule at earlier times.

| Displacement \(j\) | −3 | −1 | +1 | +3 |
|---|---:|---:|---:|---:|
| Positive rail masses at each site, in eighths | 1 | 1 | 1, 4 | 1 |
| Number of unsigned suffix words | 1 | 3 | 3 | 1 |

The site \(-1\) contains one live rail and one exact cancellation. At \(+1\) a powered type can read one pooled cell of mass five or two cells of masses four and one. This one choice \(R\) can fluctuate and correlate with the launch exponent \(q\ge0\), but it applies the same way to the relative table of each old label on that launch. Empty cells remain dark at \(q=0\). Conditional on that type the old-label probabilities are \(T_q(h)_i=h_i^q/\sum_{h_k>0}h_k^q\), for a normalized fixed squared spectrum \(h\). Both \(i\) and the still-unknown grouping enter the same joint normalization. The conditional rate of \(j=-3\) is
\[
 c_R(q)=1/Z_R(q),\qquad Z_{\rm pooled}(q)=3+5^q,\qquad Z_{\rm split}(q)=4+4^q .
\]
For either choice, \(Z_R\) strictly increases and equals 8 at \(q=1\). Thus \(d_R(q)=c_R(q)-1/8\) has the sign of \(1-q\). The sign does not require knowing the partition.

## A comparison inside each old label

Measure the residual \(r_i=\Pr(i,j=-3)-\Pr(i)/8\) from the full joint table, keeping all incident exposures. These are population equalities. Empty science outcomes need no conditioning. If fair path counting is present, with arbitrary old outcomes but an independent uniform choice at each new direction, it contributes zero to every \(r_i\). Its fraction is \(4[\Pr(j=-1)-\Pr(j=-3)]\). Both sites have one occupied unit cell for every powered type, whereas a fair suffix assigns probabilities \(3/8\) and \(1/8\). A maximal joint-cell type can only have \(j=+1\), since the top cell inside each row has strictly greater mass than one for either grouping. Among the old labels only those of maximum \(h\) can receive a maximal output when the grouping is common.

Suppose the measured residuals all vanish. Take \(i\) of largest \(h_i\) and any \(k\) with \(0<h_k<h_i\), and write \(a=h_i/h_k>1\). On finite-powered launches the contribution to
\[
 r_i-a r_k
 = \int T_q(h)_k (a^q-a)d_R(q)\,d\nu(q,R)
   -\tfrac18\Pr(\text{maximal type reports }i)
\]
is strictly negative unless \(q=1\). Here \(\nu\) includes only the finite-powered part with its original total mass. The second term allows arbitrary tie-breaking in a maximal rule. Classical fair paths contribute zero. The measured zero forces \(q=1\) almost surely on finite-powered launches. Repeating with every maximal \(i\) eliminates all maximal-rule launches as well. The unsigned contrast fixes its fraction; only a zero fraction or a separately characterized unsigned science law removes the ambiguity in its old outputs. If the positive old masses are all equal, each finite power has uniform old marginals and supplies the same residual in every occupied row. At zero residual in every row the maximal component must also report each of these labels with the same probability, since its contribution there is minus one eighth of its incident row rate. Thus a flat spectrum can leave the exponent unidentified, yet the old marginal of the powered and maximal population is ordinary even in that case.

The experiment uses observed joint frequencies and the nominal constant \(1/8\). Checking equality in each row does not require plugging in \(h\); the inequality proof requires a **single** fixed old spectrum. If \(a\) and \(h\) are independently specified, near-zero residuals also give a bound. For \(0<\epsilon<1\) and finite powers outside \((1-\epsilon,1+\epsilon)\), set
\[
 B_\epsilon=\inf_{q,R}T_q(h)_k\,|a^q-a|\,|d_R(q)| .
\]
It is positive on that closed range. At infinity \(T_q(h)_k(a^q-a)=T_q(h)_i-aT_q(h)_k\) tends to the reciprocal of the number of largest old cells, and \(d_R\to-1/8\). The finite-powered outlying fraction is at most \((a r_k-r_i)/B_\epsilon\). Each separate maximal contribution reporting \(i\) is at most \(8(a r_k-r_i)\). A nearly flat science spectrum, rare old labels and uncharacterized losses can make this bound uninformative. Every label and position used in the score must have a calibrated meaning, including the response to failures.

## How the comparison can fail

* **Averaging over old outcomes too soon.** With all final rails resolved, mix \(q=0\) and \(q=2\) in equal proportions. A single heavy rail of mass four then occurs with probability \((1/5+4/5)/2=1/2\), its ordinary weight. The other four unit rails agree by symmetry. The entire relative-position marginal passes. At \(h=(1/4,3/4)\) the old-label law is \((3/10,7/10)\). The two measured row residuals are \(3/200,-3/200\); averaging them loses the signal.
* **Science changes with the power.** Retain this half mixture but use \(h=(1/4,3/4)\) on the zero-power launches and \((1/2,1/2)\) on the square-power launches. Both types then report each old label with probability \(1/2\). Every row has the ordinary conditional reference law and the two \(r_i\) vanish. The average kinematic science table is \((3/8,5/8)\). A fixed science field, including its hidden type dependence, is a substantive premise here.
* **One less tick.** A fully rail-resolved two-tick suffix from a sharp source has four occupied equal-mass rails. Every \(q\) predicts the same reference even after conditioning on the science output. A detector that chooses its old labels by \(T_2(h)\) passes all such conditional suffix comparisons. The old spectrum can change the two-label marginal while the suffix remains exact. Three ticks are minimal for the stated conditional-position test with unknown pooled or rail-resolved terminal scoring.
* **Independent response rules.** A device that weights old labels by \(T_2(h)\) and separately supplies an ordinary conditional reference in every row also passes. A grouping that varies with the old label gives row-specific \(Z_{R_i}\) and defeats the sign argument. The theorem tests the readout within its specified joint family. It supplies no independent origin for that family.

The [replay](check_conditional_position_reference.py) compares every starting rail and well at lengths 4 through 48 and retains all joint cells of the two explicit counterexamples. The [result](results/conditional_position_reference.json) gives the signed residuals. Applying the selection on a physical flight would require the coherent pointer copy, a matched read of the joint cells and measured row frequencies.
