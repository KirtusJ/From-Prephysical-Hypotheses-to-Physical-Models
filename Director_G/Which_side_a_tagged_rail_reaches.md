# Which side a tagged rail reaches

Kirtus Justus, Theoretical Physicist, Port Coquitlam, British Columbia, Canada. Mathematical development and signed-path checks by OpenAI Codex.

Prepare a rail at a known site with the [four-route selector](Reading_a_rail_axis_with_four_coherent_routes.md). Release that same rail into a free one-dimensional Hadamard walk. Its eventual velocity has a distribution; the probability of being on the right already has its limiting value at every odd release time. At clocks 3, 7, 11 and so on, the left-side measurement has exactly the same effect on any input rail as a particular selector outcome.

## A finite side measurement

Use $(R,L)$ rail order, $Z=+1$ on R and $H=(X+Z)/\sqrt2$. A tick applies $H$ and moves R one site right, L one site left. Start at site zero on the integer line; a finite device suffices for a given clock if it reproduces the unwrapped paths. Write only the terminal position in each flight. Let $K_t(x)$ be its two-column amplitude matrix, with $K_0(0)=I$. At odd clocks no path ends at zero. The measured signed-side observable is

$$
S_t=\sum_x \operatorname{sgn}(x)\,K_t(x)^\dagger K_t(x).
$$

For $j\ge0$, set $c_j=(-1)^j\binom{2j}{j}/(2\cdot4^j)$. Then

$$
 S_{4j+3}=(X+Z)/2,\qquad
 S_{4j+1}=(X+Z)/2+2c_j^2(X-Z).
$$

This is an operator identity, including for mixed inputs or a local measurement on a rail entangled with a spectator. The distinct clocks are alternative experiments. The program previously computed $S_3$ for two successive measured flights. The extension here concerns a single uninterrupted flight at every odd clock. [Earlier three-tick computation](What_two_velocity_records_can_identify.md)

**Proof.** Between odd clocks $t$ and $t+2$, only the amplitude at the intervening even-clock origin can transfer population between half-lines. If that spinor is $(r,l)$, the share entering from the positive half-line is $|l|^2$. The share leaving for the positive half-line is $|r+l|^2/2$. Taking twice the difference and using polarization gives

$$
 S_{t+2}-S_t=K_{t+1}(0)^\dagger(X+Z)K_{t+1}(0).
$$

To compute the return matrices let $T(y)=\operatorname{diag}(y,y^{-1})H$ and let $\mathrm{CT}$ take the constant Laurent coefficient in $y$. Put $C=1/\sqrt{1+z^4}$, interpreted as a power series with constant term one, and $J=\left(\begin{smallmatrix}0&-1\\1&0\end{smallmatrix}\right)$. The return generating function is

$$
 \sum_{t\ge0}K_t(0)z^t=\mathrm{CT}(I-zT(y))^{-1}
 =\tfrac12[1+(1+z^2)C]I+\tfrac12[1-(1-z^2)C]J.
$$

Indeed the determinant in the inverse is $D=1-z^2-z(y-y^{-1})/\sqrt2$. The central-binomial series gives $\mathrm{CT}(1/D)=C$ since $\mathrm{CT}(y-y^{-1})^{2k}=(-1)^k\binom{2k}{k}$. The substitution $y\mapsto-y^{-1}$ changes the sign between $\mathrm{CT}(y/D)$ and $\mathrm{CT}(y^{-1}/D)$. Taking the constant term in $D/D$ gives $(z/\sqrt2)\mathrm{CT}(y/D)=((1-z^2)C-1)/2$, which supplies the entries of the inverse.

Extracting coefficients gives $K_{4j}(0)=c_j(I-J)$ for $j\ge1$ and $K_{4j+2}(0)=c_j(I+J)$ for $j\ge0$. Their contributions to the flux are $+2c_j^2(X-Z)$ and $-2c_j^2(X-Z)$ respectively. The matched pair cancels. The first read gives $S_1=X$ and the first flux gives $S_3=(X+Z)/2$. This sign convention also gives right-side probability one for the one-tick $X+$ launch. Published return-probability formulas give an independent check on the norms of the center matrices; here their signed entries determine the flux. [Return probabilities of one-dimensional quantum walks](https://doi.org/10.3390/e24050584)

## The same-carrier comparison

Start the selector on $I/2$. Conditional on reaching signed threshold $\tau m$ with $\tau=\pm1$, it prepares

$$
 \rho_{m,\tau}=(I+\tau\eta_m H)/2,\qquad
 \eta_m=\frac{1-(3-2\sqrt2)^{2m}}{1+(3-2\sqrt2)^{2m}}.
$$

The Bloch components are $s_X=s_Z=\tau\eta_m/\sqrt2$. Thus at **every odd** release clock,

$$
 \Pr(x_t<0\mid \tau)=\tfrac12-\frac{\tau\eta_m}{2\sqrt2}.
$$

A fresh selector probe reports code 2 on raw minus or null 01, with effect $I/2-(X+Z)/4$. For **every localized input rail** this equals the left-half effect $(I-S_t)/2$ at $t=4j+3$. At $t=4j+1$ the two predictions differ by $-c_j^2(s_X-s_Z)$ in left probability minus code-2 probability. For the specified tagged source the difference vanishes. The $m=1$ left probabilities are $1/6$ and $5/6$ for positive and negative tags; at $m=2$ they are $5/34$ and $29/34$.

To test the equality on the incident population, independently assign and log an arm for every launch before preparation. Conceal the choice from the preparation and apply the assigned selector or free flight only after the tag. Compare the fraction with the specified tag and code 2 in the selector arm against the fraction with the same tag and a left arrival in the flight arm. Use all launches assigned to the corresponding arm, including timeouts and missing reads. A confirmed preparation timeout is a nonhit for a by-deadline joint event and unresolved for an eventual outcome. Specify the target before counting. If arms were assigned only to completed preparations, the arm fractions instead refer to that subset. Recovering an incident by-deadline probability also requires the completion fraction among all launches. A cell with $h$ confirmed hits and $u$ unclassified outcomes among $N$ assignments permits the incident rate interval $[h/N,(h+u)/N]$ in that realized sample; sampling uncertainty is additional. The comparison requires a common tagged population, the specified independent arm assignment and matched outcome reporting. Equality of effects predicts equal rates; the probe and position read can leave different states. The signed-amplitude calculation assumes ordinary quantum probabilities. A match would test this pair of preparations and reads; alternative responses can agree on the same two bins. This is a proposed experiment.

## The velocity distribution and the role of the source

Under ordinary quantum probabilities, $x_t/t$ converges weakly on the line to the Konno distribution with the input tilt $\kappa=s_X+s_Z$. In the present convention and on $|v|<1/\sqrt2$ the tagged density is

$$
 f_{m,\tau}(v)=\frac{1+\tau\sqrt2\eta_m v}{\pi(1-v^2)\sqrt{1-2v^2}}.
$$

The even base density has second moment $1-1/\sqrt2$. Bounded speed gives convergence of the first two moments. The conditional mean velocity is $\tau(\sqrt2-1)\eta_m$ and its variance is $1-1/\sqrt2-(\sqrt2-1)^2\eta_m^2$. Both tag populations retain a spread of order $t$ in position. Balanced pooling cancels their signed means. This is the free coherent walk's ballistic limit. The general initial-rail density was already developed for the program's reflected-position analysis. [Konno's weak-limit theorem](https://arxiv.org/abs/quant-ph/0206103) · [Fourier method of Grimmett, Janson and Scudo](https://arxiv.org/abs/quant-ph/0309135) · [Program's rail convention and reflected limit](Reflected_position_histories.md)

An independent coherent selector can act at every site with each operator $I_{\rm pos}\otimes K_{\rm raw}$. Measuring or reusing the occupied position as its selector can instead reveal spatial information. A delocalized product input also changes the velocity law even if the tag acts on a separate register. Consider the two spatial preparations $(|-1\rangle\pm|+1\rangle)/\sqrt2$ with the same tagged rail. Both have the same initial position distribution and center. Their momentum densities relative to uniform are $1\pm\cos 2k$. The two velocity bands have squared slope $v(k)^2=\cos^2k/(1+\cos^2k)$; pairing their weights on this real input gives the mean $\kappa\int v(k)^2(1\pm\cos2k)\,dk/(2\pi)$. The uniform averages of $v(k)^2$ and $v(k)^2\cos2k$ are $1-1/\sqrt2$ and $-2+3/\sqrt2$. Consequently the limiting signed means are $\tau\eta_m(2-\sqrt2)$ and $\tau\eta_m(3\sqrt2-4)$, respectively. Their incoherent mixture gives $\tau\eta_m(\sqrt2-1)$. This provides a source-coherence control for transferring the sharp-launch prediction.

## Replaying the signed paths

Run the [standard-library checker](check_tagged_free_flight.py) from this directory.

~~~sh
python -I -B check_tagged_free_flight.py
~~~

It checks the full half-line operator at all 256 odd clocks through 511 and both input columns of the center matrix at the 256 even clocks through 512. For the positive $m=1$ source, exact integer evolution gives the following values, rounded for display. The fixed velocity window illustrates weak convergence at a continuity point.

| Clock | Mean $x_t/t$ | Second moment | $\Pr(x_t/t\le1/2)$ | Mean, coherent plus | Mean, coherent minus |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 16 | .39447021 | .29455948 | .45923360 | .55257543 | .23636500 |
| 64 | .39103753 | .29301038 | .43821109 | .55229314 | .22978191 |
| 256 | .39058903 | .29290093 | .44126936 | .55228501 | .22889306 |
| 512 | .39054721 | .29289517 | .43746292 | .55228479 | .22880964 |
| Limit | .39052429 | .29289322 | .43469557 | .55228475 | .22876383 |
