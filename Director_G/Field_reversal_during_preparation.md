# Reversing the field during preparation of the signed walk

**Kirtus Justus**, Theoretical Physicist

Port Coquitlam, British Columbia, Canada

Director Z proposed reversing the field during the middle half of the direction-switch preparation. In Z’s two finite simulations this centred the two position distributions more closely on their limiting rays. We derive the full complex amplitude for any signed block schedule, including the phase that a momentum-density comparison loses. If each block reverses the previous block’s field, the preparation attains the maximum possible yield at every field strength. Even then, at the finest of four simulated resolutions, only 29.23% of the subsequent measured histories follow the two sign words predicted in the limit. [Z’s proposal and calculations, §4](https://github.com/KirtusJ/From-Prephysical-Hypotheses-to-Physical-Models/blob/48e0df01a3bf5a385b4faccdf23429412ca7e00e/Director_Z_cross_review/CROSS_REVIEW_OF_DIRECTOR_G_ADDENDUM_3.md) · [Numerical record](results/field_echo.json)

## The retained amplitude for any signed schedule

On the line, write \(\widehat\psi(k)=\sum_x e^{-ikx}\psi(x)\), and take the direction order \(R,L\). A single step multiplies the departure amplitude at \(x\) by \(\exp(-is h x)\), applies the signed Hadamard coin \(H\), and shifts each outgoing direction one site. Thus its Fourier update at the **output** momentum is \(U(k)\widehat\psi(k+sh)\), where \(U(k)=\operatorname{diag}(e^{-ik},e^{ik})H\). The same sign \(s_j\in\{-1,1\}\) is used for both steps of block \(j\). Start at the origin in direction \(d_0=+1\) (right) or \(-1\) (left). After every two steps, measure only the direction, coherently across sites, and retain the switch \(d_j=(-1)^j d_0\). The amplitudes below are unnormalized, so their squared norms include the cost of that entire retained word. [Base preparation and instrument](Base_preparation_and_two_rays.md)

Number the \(m\ge1\) blocks in chronological order. If \(k\) labels the final output, define
\[
 S_j=\sum_{\ell=j+1}^m s_\ell,\qquad a_j=2S_j+s_j,\qquad
 D=\sum_{j=1}^m d_j,\qquad C=2\sum_{j=1}^m d_j S_j.
\]
The momentum immediately after the second step of block \(j\) is \(q_j=k+2hS_j\). Multiplying its two \(2\times2\) matrices gives the opposite-direction entry of \(U(q_j)U(q_j+s_jh)\) as \(-i e^{-id_j q_j}\sin(q_j+s_jh)\). Only that entry survives the specified projection. The initial Fourier amplitude of a localized site at zero is one. Consequently the entire retained scalar in the final direction \(d_m\) is
\[
 \widehat\psi_s(k)=(-i)^m e^{-ikD-ihC}\prod_{j=1}^m\sin(k+h a_j). \tag{1}
\]
The opposite output channel is zero. Here \(D=0\) for even \(m\), and \(D=-d_0\) for odd \(m\). The phase coefficient simplifies to \(C=-2d_0\sum_{\ell\ {\rm even}}s_\ell\), since \(\sum_{j<\ell}d_j\) is \(-d_0\) for even \(\ell\) and zero for odd \(\ell\). Equation (1) specifies both the global phase and the one-site displacement in odd words. Its use of an origin at \(x=0\) matters when comparing complex amplitudes.

## Offset moments and yield

These moments are of the **arguments of the sine factors**, with each block weighted equally. Write \(\bar a=m^{-1}\sum_j a_j\) and \(v=m^{-1}\sum_j(a_j-\bar a)^2\). Swapping the suffix sums gives \(m\bar a=\sum_{\ell=1}^m(2\ell-1)s_\ell\); also \(m^2v=\sum_{j<\ell}(a_j-a_\ell)^2\). The three preparations below all start with field sign \(+\).

| Preparation | Signs through the blocks | \(\bar a\) | \(v\) | \(C\) |
|---|---|---:|---:|---:|
| Constant | Every block \(+\) | \(m\) | \((m^2-1)/3\) | \(-2d_0\lfloor m/2\rfloor\) |
| Quartered, \(m=4q\) | \(q\) plus, \(2q\) minus, \(q\) plus | \(0\) | \((m^2/4-1)/3\) | \(0\) |
| Alternating | \(+,-,+,-,\ldots\) | \(s_m=(-1)^{m-1}\) | \(0\) | \(2d_0\lfloor m/2\rfloor\) |

For a constant sign, the offsets are the odd numbers \(2m-1,2m-3,\dots,1\). In the quartered schedule each of \(+(2r-1)\) and \(-(2r-1)\) occurs exactly twice for every \(1\le r\le q\). Squaring and summing gives the stated variance; counting even positions gives an equal number of plus and minus signs there. For alternating signs, \(a_j-a_{j+1}=s_j+s_{j+1}=0\), so all the offsets equal \(a_m=s_m\). Reversing every applied sign negates the offsets and \(C\).

Let \(\widehat\psi_0\) denote the preparation with zero field, the same length, origin, and initial direction. Under alternation \(C-Ds_m=d_0m\), and (1) gives the exact identity
\[
 \widehat\psi_{\rm alt}(k)=e^{-id_0mh}\widehat\psi_0(k+s_mh),\qquad
 \psi_{\rm alt}(x)=e^{-ih(d_0m+s_mx)}\psi_0(x). \tag{2}
\]
The site probabilities, their complete distribution, and the success probability \(p_0=\binom{2m}{m}4^{-m}\) agree with zero field for all \(h\). Its momentum peaks sit at \(\pm\pi/2-s_m h\), so the finite momentum shift remaining in the even alternating schedule is \(+h\). The quartered schedule has zero mean offset, although it has nonzero spread. In the weak regime its centred profile is symmetric at either edge.

There is a sharp bound for *every* sign word. Parseval turns its success probability into the integral of \(\prod_j|\sin(k+ha_j)|^2\) over one period with normalized measure. Hölder’s inequality with \(m\) exponents equal to \(m\) bounds this by the product of the \(m\) translated \(L^m\) norms of \(\sin^2\), hence by \(p_0\). For \(m\ge2\), equality requires the translated \(\sin^2\) factors to be proportional almost everywhere. Their integrals agree, so their shifts agree modulo \(\pi\). As \(a_j-a_{j+1}=s_j+s_{j+1}\), for \(2h\notin\pi\mathbb Z\) this forces alternation up to the first sign. At \(2h\in\pi\mathbb Z\) every sign word attains the bound, and for \(m=1\) it is automatic. The checker retains the finite example of two equal signs at \(h=\pi/2\).

For a varying schedule set \(t_j=h(a_j-\bar a)\), \(E=\sum_jt_j^2=mh^2v\). If \(m\to\infty\) and \(E\to0\), the success-probability ratio \(p_s/p_0\) tends to one. The normalized output also approaches the translated \(\sin^m(k+h\bar a)\) profile with the phase in (1). To see this, take \(u\) from the nearest translated edge. On \(|u|\le1/2\), expand \(\log\cos(u+t_j)\) at \(u\). The linear terms sum to zero, and the second derivative stays bounded since \(\max_j|t_j|\le\sqrt E\). The absolute log ratio to \(\cos^m u\) is \(O(E)\). Off the two central intervals each factor is eventually bounded in magnitude by a common number below one, while the reference squared norm is of order \(m^{-1/2}\). This transfers the comparison to the full normalized state. Alternation has \(E=0\) exactly. The constant and quartered schedules give \(E=m(m^2-1)h^2/3\) and \(m(m^2/4-1)h^2/3\), respectively. [Earlier constant-field comparison](Base_preparation_and_two_rays.md)

For \(\delta=(\pi/M)^{1/4}\), \(h=\delta^4\), \(m\sim\delta^{-5/2}\), the constant schedule’s shift in the scaled momentum \((k-k_*)/\delta\) has magnitude \(mh/\delta=O(\delta^{1/2})\). Quartering centres the mean offset, and alternation leaves only \(|h|/\delta=\delta^3\). The comparison packets still have width of order \(m^{-1/2}/\delta=O(\delta^{1/4})\) in scaled momentum. The instrument, clock, chosen weak sheet sector, selective preparation and subsequent reversal remain assumptions of the measured-path analysis. A change in the sign schedule supplies a change in the departure gain, or a layer of the carrier that encodes that sign. [Measured-path assumptions and proof](Sequential_position_records.md) · [Z’s treatment of scheduled carrier gains](https://github.com/KirtusJ/From-Prephysical-Hypotheses-to-Physical-Models/blob/48e0df01a3bf5a385b4faccdf23429412ca7e00e/Director_Z_cross_review/CROSS_REVIEW_OF_DIRECTOR_G_ADDENDUM_3.md)

## Finite measured reversals

In these runs the clock starts after a successful preparation. Take \(d_0=+1\), field \(+\pi/M\) until scaled flight time 0.75 and \(-\pi/M\) afterwards. Round the switch and the three reads at \(1.4,2.3,3.0\) to the nearest step of duration \(\delta^3\). The measurement at each read distinguishes \(L:x<0\) from \(R:x\ge0\) and preserves coherence within each side. In the limiting trajectories \(\pm[t^2/2-(t-0.75)_+^2]\), the sign changes between the second and third reads. The table gives the preparation success divided by \(p_0\), followed by the conditional joint probability of those two side histories. Every schedule at the same \(M\) uses the same multiple of four nearest \(\delta^{-5/2}\).

| \(M\) | \(m\) | Yield ratio, constant | Quartered | Alternating | \(P(LLR)+P(RRL)\), constant | Quartered | Alternating |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 127 | 12 | 0.69167 | 0.91431 | 1.00000 | 0.05567 | 0.14111 | 0.14013 |
| 509 | 24 | 0.83580 | 0.95644 | 1.00000 | 0.11245 | 0.18177 | 0.18153 |
| 2039 | 56 | 0.86912 | 0.96559 | 1.00000 | 0.15933 | 0.23105 | 0.23094 |
| 8191 | 136 | 0.88353 | 0.96953 | 1.00000 | 0.20916 | 0.29231 | 0.29227 |

In all 12 rows the other six words together carry a majority. At \(M=8191\), for example, the alternating preparation has \(P(LLR)=0.14412\), \(P(RRL)=0.14815\), and \(0.70773\) on the remaining words. The quartered schedule gives slightly more central switching mass than alternation at each of the four orders. A preparation that attains maximum yield therefore need not maximize the finite tracking metric. Finite values are conditioned on the successful base word in the simulated sector. Whole-ensemble probabilities would also include sheet and base preparation costs. [All eight histories, yield and attained times](results/field_echo.json)

## Credit, adverse checks and reproduction

Director Z introduced the quartered schedule, diagnosed the finite constant-preparation offset, and computed one-time half-line means at \(t=2\) in an unreversed flight. For \(\delta=0.1,0.05\), Z reported quartered conditional half-line means \((-1.94994,1.99657)\) and \((-1.98345,2.00262)\), respectively, with side widths approximately \(0.77,0.67\). The three-read reversal table above is a separate calculation. This supplement adds the sign-word amplitude, its phases, the alternating-state identity, the all-schedule yield bound and the measured comparison. The mathematical cross-reading had access to Z’s derivation and numerical results. [Z’s original finite data](https://github.com/KirtusJ/From-Prephysical-Hypotheses-to-Physical-Models/blob/48e0df01a3bf5a385b4faccdf23429412ca7e00e/Director_Z_cross_review/Crosscheck_Director_G_Offset_Free_Preparation_Results.json)

Run `python -B check_field_echo.py results` from this directory with NumPy installed. The checker uses the literal two-channel position update on a padded causal cone and compares its Fourier sum with (1) at 127 momenta. It also compares the complex position amplitudes directly with (2). The run used Python 3.12.14 and NumPy 2.3.5. The 160 named-schedule profiles include both initial directions, even and odd admissible lengths and four phase slopes. An additional 252 profiles cover every sign word of lengths one through six from both directions at \(h=0.37\). The largest unfitted complex residual was \(7.49\times10^{-15}\) or less, the largest alternating-state residual was below \(2.31\times10^{-16}\), and the largest single flight partition error was below \(9.80\times10^{-14}\). The algebra supplies the result for other schedules, lengths and fields. [Checker](check_field_echo.py) · [Run and adverse controls](results/field_echo.json)

All four original interrupted-checker predicates passed on their 36 even-block profiles and 12 flights. Its fitted global phase could hide an incorrect constant phase. On the additional input \(m=5,h=0.017\), constant sign and initial \(R\), its projection onto the empty \(R\) output gave both fitted modulus zero and fitted residual zero. The unit-modulus check fails on that extension. Reading the occupied \(L\) output and using (1) gives an unfitted residual of \(8.90\times10^{-16}\) or less. The JSON retains the earlier observations and the failed finite-majority benchmark alongside the corrected results. These are facts about the specified walk and conditional instruments. The program’s original emergence claim remains unresolved.
