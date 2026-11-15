# Four states are necessary and sufficient through the fifth tick

Director G research note for Kirtus Justus · 15 November 2026 · B.C. Pacific Time (PCT, UTC−07:00)

Prepare the ideal five-site Hadamard walker at site zero on the right rail and count returns to that same port on fresh launches. Direct evolution gives the first six probabilities, in time order, as 1, 0, 1/4, 0, 1/16, 1/32. **Four hidden states are necessary and sufficient to reproduce these six numbers. Every model with at most three states misses at least one by at least one percentage point.** Here the model has a finite row-stochastic matrix P, a fixed initial probability row α, and a fixed readout column b with entries in [0,1]. Its prediction at t is q_t=αP^t b. Preparation, transition and readout are independent of the assigned stopping time.

## A finite rank witness

For h≥1 and a sequence f, let M_h(f) have rows indexed by i=0,…,h, with row i equal to (1,f_i,f_{i+1},…,f_{i+h−1}). A model with ≤h states gives rank M_h(q)≤h. Its left factor has rows αP^i. Its right factor has columns 1,b,Pb,…,P^(h−1)b. The leading column works because each row αP^i sums to one. It needs no additional detector.

For h=3, the four rows of M=M₃(p) are
```
(1,   1,    0,  1/4)
(1,   0,  1/4,    0)
(1, 1/4,    0, 1/16)
(1,   0, 1/16, 1/32).
```
Their determinant is 3/512. Hence three states cannot reproduce the prefix. A four-state countermodel shows exactly where this bound stops. Launch A and read one only in A. From A move to B, from B return to A with probability 1/4 and move to C with probability 3/4, and from C move to D. From D move to B with probability 1/6 and otherwise stay in D. The excursion A→B→A, repeated when needed, produces the returns at ticks two and four. The path A→B→C→D→B→A produces the new return at tick five with probability (3/4)(1/6)(1/4)=1/32.

The same exact rank calculation works at each of h=1,…,25. From signed path counts we computed the determinants of M_h(p) modulo the prime 1009. All 25 are nonzero, so every h-state model fails on the first 2h exact probabilities for those h. For example, 50 exact probabilities force at least 26 states. The h=26 determinant is zero modulo 1009; the earlier proved 26-mode recurrence, with its constant mode, also bounds the augmented rank by 26 over the reals. The earlier 80-probability result against 55 states uses an additional all-horizon argument. [Pinned return study and recurrence](https://github.com/KirtusJ/From-Prephysical-Hypotheses-to-Physical-Models/blob/a1eee36656ab413eac2cfa92c9d2bb62a1bea25e/Director_G/persistent_walk/Return_at_one_port.md)

For horizons ending at ticks 0,1,2,3,4,5, the exact minimum state counts are **1,2,2,3,3,4**. The certificates just given supply the lower bounds at the odd ticks. One state fits the launch alone. Two states fit ticks 0–2 using A→B and B→A with probability 1/4 (otherwise B→B). Three states fit ticks 0–4 using the same A→B and B→A probability but sending the other B output to an absorbing dark state. The four-state construction covers tick five. Exact membership for all prefixes ending beyond tick five is open here.

## Uniform separation of three-state models

Let δ be the largest absolute difference between f=p and f=q on ticks 0–5. For any three-state rival take a nonzero null vector (a,v) of M₃(q), where v has three components. Rescale so that the sum of the absolute entries of v equals one. This is possible because M₃(q) has an all-ones first column and the null vector cannot have v=0. Each entry of w=M(a,v) then has magnitude ≤δ. The last three rows B of M⁻¹ are
```
(−2/3,  2,  20/3, −8)
( 4/3,  4, −16/3,  0)
(   8, −8,   −32, 32).
```
The maximum of the sum of the absolute entries of Bz over vectors z with entries in [−1,1] is 100. By convexity it suffices to check the 16 sign vectors; (1,−1,−1,1) attains the maximum. Since v=Bw, this gives 1≤100δ. The one-point margin is a lower bound. Its optimality over stochastic rivals is open.

## A five-tick experiment against the three-state class

Take independent launches, count every launch, and apply the following six terminal tests in a preassigned schedule whose chosen times cannot affect preparation or the repeated step. Select the ideal model if all counts lie in the inclusive bands.

| Tick | Launches | Accepted port clicks |
|---:|---:|---:|
| 0 | 299 | 299 |
| 1 | 299 | 0 |
| 2 | 31,100 | 7,593–7,958 |
| 3 | 299 | 0 |
| 4 | 10,300 | 586–703 |
| 5 | 5,700 | 147–210 |

At the ideal probabilities the three deterministic tests pass with certainty. Exact binomial tails for the three interior probabilities, summed by the union bound, give a probability below **0.047619** of rejecting the ideal. For any rival there is at least one tick whose detection probability differs by ≥0.01. Binomial monotonicity bounds the probability of passing the corresponding test by its outward one-sided tail at p_t−0.01 or p_t+0.01, whichever is feasible. At deterministic ticks this upper bound is 0.99^299. The largest of the six bounds is below **0.049537**, so the probability of selecting the ideal under any such rival is bounded by the same number.

The 47,997-launch design trades a small memory class and substantial sampling for a maximum depth of five. It assumes a calibrated instrument delivering the ideal unconditional click probabilities and statistical independence between launches. The four-state countermodel fits all six probabilities exactly and gives identical count distributions. There are no data from a physical device in this calculation.

Run `python -I -B check_short_prefix.py` in this directory. The checker forms the probabilities from signed integer path counts, evaluates every stated modular minor, verifies the inverse rows and norm, executes the constructive models and bounds the tails using ratios of exact integers. The accompanying JSON reports the observed output.
