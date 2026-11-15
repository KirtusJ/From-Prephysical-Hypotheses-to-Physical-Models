# What two velocity records can identify

**Kirtus Justus**, Theoretical Physicist, Port Coquitlam, British Columbia, Canada. Mathematical development and checks by OpenAI Codex.

Two three-tick flights measure exactly the coefficient \(\kappa\) that multiplies the velocity correlation for the simple scattering kernels of the signed walk. This works even if the intervening coin operation mixes complex phases into real components. For a general coin channel the same measurement gives one matrix element. Additional histories determine whether it predicts a full classical scattering law. All probabilities below use ordinary squared amplitudes and a whole-site projective write at each flight boundary. [Velocity limit and write instrument](Velocity_memory_after_a_position_record.md)

## Six ticks with a balanced source

Start at a known well with coin \(I/2\), which can be prepared by an independent fair choice of sharp R or L. Take three free Hadamard-and-shift ticks, write the site, apply the same trace-preserving completely positive coin map \(E\) at every written site, take three more free ticks, and write the final site. Use a line or a ring on which the signed displacement in each segment is unambiguous. Let \(\sigma_1,\sigma_2\) be the signs of the two segment displacements. Three ticks give no ties. With \(Z=+1\) on R, the real amplitude matrices from the incident coin to the two output rails are

$$
\sqrt8\,(A_{-3},A_{-1},A_{1},A_{3})
=\left(\begin{pmatrix}0&0\\1&-1\end{pmatrix},
\begin{pmatrix}-1&1\\0&-2\end{pmatrix},
\begin{pmatrix}2&0\\1&1\end{pmatrix},
\begin{pmatrix}1&1\\0&0\end{pmatrix}\right).
$$

Multiplication gives \(\sum_j\operatorname{sgn}(j)A_j(I/2)A_j^\dagger=(X+Z)/4\) and \(\sum_j\operatorname{sgn}(j)A_j^\dagger A_j=(X+Z)/2\). Write \(R\) for the real linear part of the channel's Bloch-vector map and \(\mathbf e=(\hat x+\hat z)/\sqrt2\). Define \(a=\mathbf e^\mathsf{T}R\mathbf e,\ \kappa=2a\). The first signed sum is traceless, so the affine offset cancels. The second sum reads its projection onto \(\mathbf e\). Thus

$$
E[\sigma_1\sigma_2]=\kappa/4,\qquad
P(\sigma_1=\sigma_2)=1/2+\kappa/8 .
$$

Equal initial weights, a channel independent of the chosen initial rail, and one common post-write operation across the sites are necessary for this calibration. The channel can contain an unobserved environment that is freshly initialized at each use. Memory in that environment across flight boundaries requires a larger state model. Contractivity on two antipodal input states gives \(|a|\le1\).

On \(N\) independent launches let \(n_+,n_-,n_?\) count same signs, opposite signs and missing pairs, with total \(N\). Without a missing-at-random premise, assign a missing pair either value. The ideal sample mean lies between \((n_+-n_--n_?)/N\) and \((n_+-n_-+n_?)/N\) if the reported signs are correct. If at most \(k\) of the reported sign products were misclassified, expand each side by \(2k/N\). For fixed independent launches, expand again by \(\sqrt{2\log(2/\alpha)/N}\) for a two-sided \(1-\alpha\) bound on the population mean, then multiply by four and intersect with \([-2,2]\). Misclassification bounds estimated from another experiment carry their own uncertainty. This is an all-launch comparison; dividing just by the complete reports would require a separately supported loss model. [Hoeffding, Theorem 2](https://doi.org/10.1080/01621459.1963.10500830)

## Which velocity histories test a memoryless kernel?

Now take the long-flight limit of the companion paper, keeping a fixed finite number of boundaries. Write \(r=\sqrt2 v\) and \(\mu\) for the pushforward of the symmetric velocity law \(\nu\). Let \(A=E_\mu[r^2]=2-\sqrt2,\ B=1-A\), and use \(s,t\) for subsequent scaled velocities. Denote by \(x\) the Bloch component along \(\mathbf e\), and by \(y\) the component along the Pauli \(Y\) axis. At a fixed \(r\), the two band polarizations have components \((r,\pm\sqrt{1-r^2})\) with equal reference weight. Averaging their rank-one projections shows that the unnormalized state with trace \(\tau\) and components \((x,y)\) becomes

$$
\big(\tau+rx,\;r(\tau+rx),\;(1-r^2)y\big)
$$

per unit \(\mu(dr)\). Its component along \((\hat x-\hat z)/\sqrt2\) is zero. A component that the boundary channel creates in this last direction disappears at the next limiting site write. On the observable plane write the channel between flights as

$$
(x,y)\ \longmapsto\ (u+a x+b y,\ w+c x+d y)
$$

on normalized inputs. Here \(b\) describes the conversion of \(Y\)-coherence into the velocity-sensitive direction. The coefficients are restricted by complete positivity. The use of one fixed channel here excludes hidden changes driven by the earlier record.

Suppose the pre-flight state is stationary for the unconditional flight and boundary map. The target stationary Markov law has marginal \(\mu\) and transition density \(1+a r s\) relative to \(\mu(ds)\), equivalent to \(1+\kappa v_1v_2\). The actual first marginal is \((1+r x_*)\mu(dr)\). The moment \(E[r]=0\) therefore implies its stationary sensitive component \(x_*=0\). Write \(y_*\) for its other stationary component, so \(u=-bB y_*\). After a first observed \(r\), the actual conditional mean-sensitive component is

$$
x_{\rm next}=a r+b y_*(A-r^2).
$$

Thus \(E[rs]=a A^2\). A second observable tests the entire remaining shape of the adjacent conditional distribution:

$$
E[(A-r^2)s]=b y_* A\,\operatorname{Var}_\mu(r^2).
$$

The factor multiplying \(by_*\) is strictly positive. In the stationary Markov model this moment is zero. If it vanishes, either \(b=0\) or \(y_*=0\). When \(b=0\), stationarity gives \(u=0\) and every previous history leaves \(x_{\rm next}=a r\) after observing its last velocity \(r\); the visible process is already Markov. If \(y_*=0\), both stationary offsets \(u,w\) are zero. Averaging over the intervening flight scales the \(x,y\) components by \(A,B\), respectively. Consequently the two-step-lag product in that case is

$$
E[rt]=A^2\big(Aa^2+Bbc\big).
$$

Comparison with the Markov value \(A^3a^2\) now detects \(bc\). If the comparison agrees, then \(b=0\) or \(c=0\). In the second case an initial \(y_*=0\) stays zero after every history. This proves that **a stationary mean, two adjacent moments and one lag-two moment suffice** within this limiting channel family: \(E[r]=0,\ E[rs]=aA^2,\ E[(A-r^2)s]=0,\ E[rt]=A^3a^2\) imply the entire visible Markov law for all finite histories. With \(a\) independently calibrated by the six-tick experiment the adjacent product checks that calibration. The conclusion concerns the observable law. A \(Y\)-component can persist internally forever with \(b=0\). A physical analyzer sensitive to \(Y\) would be needed to identify that component.

## A channel that defeats every signed pair comparison

There is a sharper limitation if only products of signs, or even arbitrary two-velocity marginals relative to a fitted transition kernel, are checked. Measure the incoming coin's Pauli \(Y\), then prepare a coin with Bloch components \((u+b,w)\) or \((u-b,w)\) according to the two outcomes, in the \((\mathbf e,Y)\) plane. Take \(w=b=1/2\), \(u=-B/4\). Both possible prepared vectors have squared length at most \((1/2+B/4)^2+1/4<1\); measurement followed by these preparations is a valid complex CPTP map. This gives the affine update \(x'=u+b y,\ y'=w\). Take the stationary initial components \(x_*=0,\ y_*=w\). Define the even function \(f(r)=bw(A-r^2)\), of \(\mu\)-mean zero.

The adjacent pair density is exactly \(K(r,s)=1+s f(r)\). Its signed correlation vanishes just as it does for an independent pair, since \(f\) is even. After one unobserved intermediate flight the actual mean state again has \(x'=u+bBw=0,\ y'=w\). Thus every pair at separation two or greater has product law. The stationary first-order Markov chain fitted to the adjacent records also has these complete pair laws at *every* separation: integrating \(K(r,s)K(s,t)\) over \(s\) gives one by symmetry and \(E_\mu f=0\).

The actual three-velocity density differs from this fitted Markov chain's density by

$$
-t s\,f(r)\,bw(1-s^2)
$$

relative to \(\mu(dr)\mu(ds)\mu(dt)\). Indeed, after \(r,s\) the actual \(x'\) is \(u+bw(1-s^2)/(1+s f(r))\); the fitted chain uses \(f(s)\). The difference is nonzero on a set of positive measure. This example passes the signed-pair tests against independence at every lag. Its **full adjacent** density differs from the specific \(1+a r s\) template, as the quadratic moment detects. Comparing full pair laws to an unrestricted fitted kernel therefore answers a different physical question from testing the calibrated walk kernel. These are predictions for specified channels and preparations, without a claim of observed phase memory. [Scope of available joint records](../candidates/composition_record/return_memory/experimental_coverage.md)
