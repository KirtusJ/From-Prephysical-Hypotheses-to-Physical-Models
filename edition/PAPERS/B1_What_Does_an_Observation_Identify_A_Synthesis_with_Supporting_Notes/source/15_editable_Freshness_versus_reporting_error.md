# Freshness versus reporting error

## 1. Observation contract

Let `Z=(Z_1,Z_2,Z_3,Z_4)` denote ideal binary match outcomes from four sequential uses of a known gate-or-reset selector, and `Y` the reported record. The independent reference selector has gate probability `t=37/100`; a complete reset produces an ideal match with probability `r=1/16`. Under the memoryless selector, ideal outputs are independent Bernoulli variables with

\[
 s=t+(1-t)r=\frac{131}{320}.
\]

For the comparison process, each reported ideal bit independently flips with probability `e=1/100`. Define

\[
 m=s+(1-2s)e=\frac{6579}{16000},\qquad
 A=\frac{t^4}{4}\big[(1-r)(1-2e)\big]^4.
\]

The target four-bit law is

\[
 Q(y)=\prod_{i=1}^4m^{y_i}(1-m)^{1-y_i}
       -A\prod_{i=1}^4(2y_i-1),\qquad y\in\{0,1\}^4.
\]

All 16 entries of `Q` are strictly positive and sum to one. Its proper marginals are independent Bernoulli(`m`). These equations are mathematical and dimensionless. A genuine experiment must separately justify ideal-state preparation, gate/controller independence, reporting calibration, trial initialization, and the meaning of observation time.

## 2. Total-variation freshness theorem

**Theorem 1 (error-freshness tradeoff).** For any joint law of reported prefix `W=(Y_1,Y_2,Y_3)`, final reported bit `Y_4`, and final ideal bit `Z_4`, fix a reference `s in [0,1]`. Put

\[
 \begin{aligned}
 L_s(Q)&=\sum_{w\in\{0,1\}^3}|Q(w,1)-sQ_W(w)|,\\
 \epsilon_4&=\Pr(Y_4\ne Z_4),\\
 \eta&=\operatorname{TV}\!\left(\mathcal L(W,Z_4),
                           Q_W\otimes\operatorname{Bern}(s)\right).
 \end{aligned}
\]

Then

\[
 \boxed{L_s(Q)\le\epsilon_4+\eta.}
\]

*Proof.* Since `Z_4` and `Y_4` are coupled on the same probability space, replacing one with the other changes the joint distribution with the prefix by at most `Pr(Y_4 != Z_4)` in total variation. Applying the triangle inequality with the reference product law gives the claim. Because the last variable is binary, `L_s(Q)` is precisely the total variation between `Q_{W,Y_4}` and `Q_W x Bern(s)`. The definition of `eta` also equals `sum_w |Pr(W=w,Z_4=1)-sQ_W(w)|`. No detector-Markov assumption is required. QED.

*Interpretation.* Exact conditional freshness `Pr(Z_4=1 | W=w)=s` gives `eta=0` and forces reporting error `epsilon_4 >= L_s(Q)`. If an independent experiment establishes `epsilon_4 <= e_max`, then any model reproducing the reported target must satisfy `eta >= (L_s(Q)-e_max)_+`. Dependence can arise because early reports were buffered until after `Z_4`, or because the supposedly independent ideal final outcome is actually statistically predictable. The inequality by itself cannot distinguish those mechanisms.

**Theorem 2 (closed form).** Suppose a length-`k` target has law `Q(y)=prod_i Bern_m(y_i)-A prod_i(2y_i-1)` with `A>0`, and put `p_m(w)=prod_{i=1}^{k-1}Bern_m(w_i)`. If `A>|m-s| max_w p_m(w)`, then

\[
 \boxed{L_s(Q)=2^{k-1}A-(m-s)(2m-1)^{k-1}.}
\]

*Proof.* Each difference `Q(w,1)-sQ_W(w)` equals `(m-s)p_m(w)-A prod_i(2w_i-1)`. Under the stipulated inequality its sign is the negative of the parity product. Summing absolute values yields the formula, since the mean parity product under independent Bernoulli(`m`) variables is `(2m-1)^{k-1}`. QED.

For the supplied four-use law, exact rational arithmetic yields

\[
 \boxed{L_s(Q)=\frac{875470225373317}{32768000000000000}
        =0.026717230998941559\ldots .}
\]

Hence if the final bit is misreported at most 1% of the time, every reproducing detector/controller model must have

\[
 \boxed{\eta\ge\frac{547790225373317}{32768000000000000}
         =0.016717230998941558\ldots .}
\]

### A physically stronger, history-by-history calibration

For the reported prefix `W=111`, its target probability is approximately `0.06952159242` and the final click probability conditional on that prefix is approximately `0.36316811406`. Its distance from the fresh probability `s` is approximately `0.04620688594`. If a laboratory can certify an error cap of 1% **conditional on that particular prefix**, it must also permit at least `0.03620688594` conditional freshness deviation on this prefix to reproduce the target. This stronger statement uses a stronger calibration contract than an average 1% last-bit error rate.

## 3. Exact sharpness certificate with a buffered detector

The accompanying exact rational transport certificate specifies 36 strictly positive rational joint masses `T(z,y)` on the 16 ideal and 16 reported words. The accompanying verifier checks all of the following with exact rational arithmetic:

1. `sum_y T(z,y)=prod_i Bern_s(z_i)` for every ideal word `z`;
2. `sum_z T(z,y)=Q(y)` for every reported word `y`;
3. for each of the four bits `i` and both true values `b`, `Pr(Y_i != Z_i, Z_i=b)=e Pr(Z_i=b)`;
4. `epsilon_4=e=1/100`;
5. the measured history-future total variation is **exactly** `eta=L_s(Q)-e`.

Thus Theorem 1 is sharp even under all eight calibrated per-bit conditional flip constraints and an independent Bernoulli ideal input process. The joint law defines a valid classical buffered reporting kernel `T(y|z)`, because its ideal-word marginals are positive. It is a mathematical countermodel, not an assertion that any physical device implements the kernel.

The accompanying executable check also evaluates two exponential tail expressions at 75-digit working precision. For the specified 8,982-record test it returns approximately 0.04999520376305833929 and 0.049985875128356778308. These are numerical evaluations, not outward-rounded interval certificates. They are separate from, and are not needed for, the exact rational transport identities and saturation proof above.

**Information-theoretic corollary.** With the certified ideal marginal `Z_4 ~ Bern(s)`, `eta` measures dependence between the reported prefix and the ideal final bit. Pinsker's inequality gives

\[
 I(Z_4;W)\ge 2\eta^2\ge 0.0005589316245439451\ \text{nats}
     \approx 0.0008063678829256\ \text{bits}.
\]

This is a *minimum predictive information requirement* for any 1%-accurate reproducing apparatus under the model. It is not evidence of backwards-in-time physical causation: a buffered detector can record earlier labels only after seeing the final outcome.

## 4. Direct signed-predictability witness

Define `f(w)=sgn[Q(w,1)-sQ_W(w)]`. For the stipulated target, `f(w)=-prod_i(2w_i-1)` and

\[
 \mathbb E_Q\big[f(W)(Y_4-s)\big]=L_s(Q).
\]

For any joint implementation, replacing `Y_4` by `Z_4` changes this expectation by at most `epsilon_4`. Therefore

\[
 \boxed{\mathbb E[f(W)(Z_4-s)]\ge L_s(Q)-\epsilon_4.}
\]

The rational transport certificate saturates the bound at `epsilon_4=0.01`. This single signed statistic is an informative calibration target if a trusted independent path can observe or challenge the final ideal bit. It does not estimate the entire correlation law and is not justified if the reference path changes the detector's behavior.
