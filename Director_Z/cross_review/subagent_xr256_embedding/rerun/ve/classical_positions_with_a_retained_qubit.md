# Classical position records with a retained qubit

On a ring of 16 sites, one walker with two internal rails can make **independent position increments while retaining an arbitrary qubit**. Each increment has the same eight-outcome distribution for every localized input coin. Given the position record, the change to the ideal coin is a known unitary and can be undone. A device that resets the coin after every position read gives precisely the same position records. A separate rail read can distinguish the two devices.

## What the terminal site detects

Start at site 0. On each of twelve ticks apply the same coin at every site, then shift R one site clockwise and L one site anticlockwise. In time order the coins are **H H H I I H I H H I I H**, with $H(R,L)=(R+L,R-L)/\sqrt2$ and $I$ the identity. Read the exact terminal site, leaving the two rails there coherent. There are seven balanced coins. Writing the output at displacement $x$ as $K_x\psi=M_x\psi/\sqrt{128}$, the integer matrix $M_x$ sums the signed paths from **both** input rails to the two output rails. Winding paths reaching the same site and rail add before the position is written. On this clock all odd displacements are dark.

Two examples are

$$
M_0=\begin{pmatrix}7&3\\3&-7\end{pmatrix},\qquad
M_4=\begin{pmatrix}-1&-1\\1&-1\end{pmatrix}.
$$

They obey $M_0^\top M_0=58I$ and $M_4^\top M_4=2I$. In fact $K_x^\dagger K_x=p_x I$ for every $x$. The table compares the complete terminal distribution with the result of writing every intermediate site using the very same controls on a sharp R launch.

| Displacement modulo 16 | Only terminal site written, numerator / 128 | Every site written, numerator / 128 |
| ---: | ---: | ---: |
| 0 | 58 | 18 |
| 2 | 10 | 18 |
| 4 | 2 | 16 |
| 6 | 10 | 14 |
| 8 | 26 | 14 |
| 10 | 10 | 14 |
| 12 | 2 | 16 |
| 14 | 10 | 18 |
| Each of 1, 3, 5, 7, 9, 11, 13, 15 | 0 | 0 |

For the second column, a sharp R or L launch, a complex superposition, a mixed coin, and a coin entangled with an external system all give $\Pr(x)=p_x$. For the third column, writing position every tick resolves each new direction given the preceding position. An H tick then supplies a fair new sign; an I tick repeats the preceding sign. Thus 128 equally likely direction choices contribute to the ring endpoints, including motion on every I tick. Counting them without phases gives the third column. It is a weighted sum over seven fair choices; a twelve-step simple binomial model would assign the wrong movement law. The total variation distance between the two recorded endpoint laws is $13/32$. A [signed-path and output-circuit checker](check_scalar_walk.py) verifies every effect and checks the measured-every-tick histogram by two independent counts.

## Position histories

Repeat the same block and record each endpoint. At the start of a block, let the recorded site be $s$ and let the local rail state depend arbitrarily on all preceding records. It can also be correlated with a retained external memory. For an ordinary site read the probability of $s+x$ conditioned on the whole past is

$$
\operatorname{tr}[(p_x I\otimes I)\rho_{\rm rail,memory}]=p_x.
$$

Translation invariance and localization at each recorded site give independent, identically distributed **increments**. Positions themselves form a translation-invariant Markov chain on the eight parity-allowed sites, and generally remain correlated across records. The conditional argument still holds if the apparatus changes the coin after each read, even in a history-dependent way, provided the next input remains on the recorded site and the controls and readout effects remain the ones above.

In the coordinate $j=x/2\bmod8$, the eight Fourier modes diagonalize the transition matrix. Using the symmetry of the eight numerators, the eigenvalue at mode $k$ is

$$
\frac{58+20\cos(\pi k/4)+4\cos(\pi k/2)+20\cos(3\pi k/4)+26(-1)^k}{128}.
$$

Its values for $k=0,\ldots,7$ are $1,1/4,5/8,1/4,3/8,1/4,5/8,1/4$. Starting at the origin, the return probability after $m$ recorded blocks is therefore

$$
\Pr(X_m=0)=\frac{1+4(1/4)^m+2(5/8)^m+(3/8)^m}{8}.
$$

For $m=1$ this gives $58/128$; at long times it tends to $1/8$. This is an exact finite-ring chain under the specified position instrument, with no diffusion scaling or inferred force law.

## A rail read distinguishes retention from erasure

In the ideal coherent device $O_x=K_x/\sqrt{p_x}$ is a real orthogonal matrix on each allowed displacement, because $K_x^\dagger K_x=p_x I$ and the local rail spaces have dimension two. Conditioned on the known record, the coin evolves by $O_x$. Applying the rail correction $O_x^\top$ restores the full input state, including its correlations with an untouched reference qubit. After several blocks reverse the recorded product of these orthogonal maps. This recovery requires calibrated local rail controls beyond the position measurements. [Environment-assisted correction from reversible conditional channels, Gregoratti and Werner](https://arxiv.org/abs/quant-ph/0209025)

For a direct test requiring just one conditional H and a rail read, launch sharp R and condition on $x=4$, an event of probability $2/128$. Its ideal output is $(-1,1)/\sqrt2$. Apply H and measure the two rails: the L outcome occurs with certainty. A detector that instead prepares R after recording the same $x$ gives an L outcome with probability $1/2$. Counting per incident launch, the joint frequency of this displacement and the L outcome is $1/64$ in the ideal device and $1/128$ for the reset. One selected input and test can exclude that specified reset; a deliberately programmed device can imitate its statistics for one preparation. Retention of arbitrary inputs or entanglement is a consequence of the specified Kraus operators and requires correspondingly wider calibration on a physical device.

The position chain uses ordinary quantum record probabilities as a premise. Classical increments alone determine neither the action on the unobserved coin nor a fundamental probability law. These calculations are prospective. Kirtus Justus, Theoretical Physicist, Port Coquitlam, British Columbia, Canada, retains scholarly responsibility for the research program. OpenAI Codex developed the schedules, calculations and checks.
