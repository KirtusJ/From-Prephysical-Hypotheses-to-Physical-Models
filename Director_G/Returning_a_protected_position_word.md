# Returning a protected position word to its source

**Kirtus Justus**, Theoretical Physicist, Port Coquitlam, British Columbia, Canada. Research supplement by Director G (OpenAI Codex).

Two position comparisons in a six-tick walk produce three occupied words. Each word contains several terminal modes, so a detector that partitions these modes before powering can imitate the ordinary word histogram. A second experiment copies the two comparison bits to a spare register and reverses the flight. Three clean returns are then individually identifiable, even if the detector groups all other modes in unknown ways. Their measured frequencies would test the common power on each launch. [Three-pure-mass criterion](When_a_position_histogram_identifies_its_probability_power.md)

## Which amplitudes return

Let \(V\) be the complete reversible preparation of a flight and its original word register from one known basis state \(e\). Include each microscopic walk and workspace coordinate in this state. The word projector \(\Pi_w\) accepts every state carrying label \(w\). Write \(p_w=\|\Pi_w V e\|^2\), a computable squared norm. XOR the word bits into a separate blank register in their computational basis. Apply \(V^\dagger\) to the original registers, keeping the spare isolated. The resulting state and its clean-return matrix element at spare label \(w\) are
\[
 \sum_w (V^\dagger\Pi_w Ve)\otimes|w\rangle,\qquad
 \langle e|V^\dagger\Pi_w Ve\rangle=p_w .
\]
Thus the return cell \((e,w)\) has squared mass \(p_w^2\). The original forward word need not be one mode. The complete output at spare label \(w\) still has total squared mass \(p_w\) by unitarity. It generally includes failed returns. The final measurement distinguishes the protected word and checks whether the source site, rail and original blank flags are all correct. A single failure label can absorb every other output. No conditional normalization or dropped failure is used. The copy duplicates orthogonal register labels and preserves coherence within each forward word. The compute–copy–reverse ordering has an earlier classical reversible use. [Bennett, *Logical Reversibility of Computation*](https://doi.org/10.1147/rd.176.0525)

The [two-rail flight-bin comparison](Two_rail_comparison_for_a_flight_bin.md) uses a reversible flag-writing flight and a phase addressing the source to synthesize comparison states. The [stored-track membership test](Reading_a_classical_track_at_the_end_of_flight.md) reads membership in selected histories. Here the only turnaround gate is the spare copy, and its output is read in coincidence with the complete returned state. This converts several actual histories into distinct pure masses in the same experiment.

## A finite two-comparison flight

Use the [reflecting interval](Reflecting_wells_and_the_classical_limits_of_a_walk.md), with 16 wells, a sharp source at well 8 on rail \(R\), and blank original and spare two-bit registers. Each tick applies \(H(r,l)=(r+l,r-l)/\sqrt2\) and shifts \(R\) right and \(L\) left. Outward shifts hold and reverse the rail with amplitude \(+1\). After the third shift, XOR \([x\le5]\) into the high original bit. After the sixth shift, XOR \([x\ge12]\) into the low original bit. These are coherent predicates on the entire bin. At the turnaround copy the word, undo the second comparator, and run the complete step and flag schedule in reverse. Equivalently the two cuts on \(z=(x+1/2)/16\) are \(z<3/8\) and \(z>3/4\). The source cannot reach either wall on the outward flight. The exact test consequently also applies when those outward paths evolve on the line.

| Word | Forward positive mode masses, in units of \(1/64\) | Forward fair paths | Signed clean return, in units of \(1/64\) | Ordinary clean mass, in units of \(1/4096\) | Fair echo paths ending at the clean return |
|---|---|---:|---:|---:|---:|
| 00 | 1, 1, 1, 4, 4, 9, 9 | 49 | 29 | 841 | 405 |
| 01 | 1, 1, 25 | 7 | 27 | 729 | 27 |
| 10 | 1, 1, 1, 1, 4 | 8 | 8 | 64 | 12 |
| 11 | empty | 0 | 0 | 0 | 0 |
| All failed returns | | | | 2,462 | 3,652 |

Every counted echo history makes 12 binary Hadamard choices, with one global set of 4,096 words. Let \(n_{w,d}\) count forward paths ending at microscopic site and rail \(d\) with original flags \(w\). Every forward path to \((d,w)\) and every reversal of any path to that same state give a distinct clean-return history. Thus the fair return count is \(\sum_d n_{w,d}^2\). Requiring that the return retrace its own outward choices would miss legal paths. For example the five paths to the right rail of well 12 at word 01 contribute 25 fair pairs. The ordinary failed-return mass is \(2462/4096\), more than half the input. Distinguishing several failure labels instead produces the same three clean statistics, provided each normalization still includes every output.

## What the terminal frequencies determine

The two bits also have a macroscopic interpretation in the [joint position histories](Reflected_position_histories.md). Keep the same fractional cuts, launch at the center on the right rail, and use clocks \(t_1=\lfloor L\sqrt3/8\rfloor\), \(t_2=\lfloor L\sqrt3/4\rfloor\). They give 3 and 6 at 16 wells. In the ballistic limit no ray reaches a wall by the second clock. The two comparisons test \(V<-1/\sqrt3\) and \(V>1/\sqrt3\) for the one shared velocity. Its density is \((1+v)/(\pi(1-v^2)\sqrt{1-2v^2})\) on \(|v|<1/\sqrt2\). Integrating gives limiting forward masses \((1/2,5/12,1/12,0)\) in binary order. Indeed the distribution function at the two cuts is \(1/12\) and \(7/12\), as follows from the primitive \((\arctan(v/\sqrt{1-2v^2})-\arctan\sqrt{1-2v^2})/\pi+1/2\). The corresponding clean echo masses are the squares of these limits. The finite table uses the actual 16-well masses.

A finite detector type uses a common exponent \(q\ge0\) on all occupied cells of that launch. Within each reported bin it can partition the microscopic modes arbitrarily, add their squared masses within each group, apply the power, and finally normalize across all cells. At zero power empty cells remain dark. Exponent and partition may be freshly correlated each launch. The three reported clean labels contain one occupied cell apiece. Write \(a=64,b=729,c=841\) in the mass units of the table. With \(\lambda=\log(c/b)/\log(c/a)\), define the mean score on the original exposure by
\[
 S=\lambda P_{10,\mathrm{clean}}/a-P_{01,\mathrm{clean}}/b
       +(1-\lambda)P_{00,\mathrm{clean}}/c .
\]
After multiplying by the common positive normalizer, the finite powered score is \(\lambda a^{q-1}+(1-\lambda)c^{q-1}-b^{q-1}\). It is nonnegative by weighted arithmetic–geometric mean, with equality precisely at one. Fair counting has strictly positive score because both \(12/64\) and \(405/841\) exceed \(27/729\). For a rule choosing any maximal cell, the pure masses \(a,b\) cannot win against \(c\), so the score is nonnegative even if a pooled failure dominates. If \(S=0\), only ordinary powers and maximal types with zero score can remain in a mixed population. All maximal types have \(P_{10,\mathrm{clean}}=0\). Its ordinary value \(64/4096\) then excludes them. The same argument works for three distinct positive forward word norms under arbitrary finite powers, whereas the signs of the fair-path contrast require their own check for each flight.

The forward-only read of these same flags has no pure occupied word and admits nonordinary mixtures by the single-histogram necessity theorem. The protected-return result dispenses with assumed indivisibility of the forward words or of the failure bin. It requires a calibrated powered law on the full echo, coherent access to the original flags for the inverse, an isolated spare, one sharp return mode, and known incident yields. An inaccessible spectator or unobserved source degeneracy can leave several live modes in a nominally clean return. A separate transport assumption would be needed to attribute the selected echo law to a different direct word read, to a sequence of live nonlinear measurements, or to a physical apparatus. [Word-read assumptions on a heralded flight](Checking_a_heralded_flight_word.md) · [Selective loss](Terminal_erasure_in_a_powered_walk_read.md)

## Controls on the return operation

The [Lean 4.19 certificate](lean/ProtectedWordEcho.lean) uses a separate enumeration of pairs of outbound paths to prove the clean numerators and both integer inequalities for fair counting.

* Adding a minus sign only at well 12 between copy and reversal changes the signed return numerators to \((29,-25,8,0)\) in binary word order. The clean mass at 01 becomes \(625/4096\). Both end rails at well 12 receive the phase. The operation preserves norm.
* Initializing the spare to 01 moves the three clean numerators to \((27,29,0,8)\). Initializing the original flags to 01 while testing return to the specified original 00 gives zero clean returns at every protected label. The same run returns to its actual initial state with numerators \((27,29,0,8)\).
* Checking the source well alone accepts squared masses \((922,1018,128,0)/4096\). Omitting the protected copy returns the pure input and blank spare with certainty in the ordinary model. These two controls test the source predicate and the holding register separately.

The [integer replay](check_protected_word_echo.py) follows all 4,096 paths forward and backward to their final modes. It separately constructs the complete forward matrix and calculates a restricted inner product of columns for each word and every endpoint. The signed vectors and unsigned fair counts agree, also for the deliberately changed phase. The [result file](results/protected_word_echo.json) retains all reachable ideal endpoints including cancellations, failed returns, and controls. No experimental frequencies enter the table.
