# Restriction-Compatible Stochastic Operations and Information Accounting

*Selected sections of an unpublished mathematical note.*

**Original date:** 2026-11-09.  
**Research direction:** Kirtus Justus.  
**Mathematical and editorial assistance:** ChatGPT (OpenAI).

The selected statements, assumptions, arguments, and examples below are drawn from the original note. This editorial excerpt does not claim independent verification. Numerical results are source-reported unless established by the reproduced argument; cited literature is identified from the original note. Original section numbering is retained.


## 2. Deterministic naturality extends to more than two inputs

For a fixed positive integer r, suppose

\[
F_S:\mathrm{Eq}(S)^r\longrightarrow\mathrm{Eq}(S)
\]

is a total deterministic operation for every finite S and commutes with all injection-induced restrictions. Then there are exactly \(2^r+1\) possibilities: the constant discrete relation, together with intersections of a fixed subset of the r input relations. Intersection of the empty subset is the universal relation.

**Proof.** Pair restriction and relabeling reduce the off-diagonal output to a single Boolean function \(f:\{0,1\}^r\to\{0,1\}\). Identify an input vector with its coalition A of coordinates equal to one, and write \(\mathcal W=\{A:f(A)=1\}\).

For A contained in B, realize on three positions the input coalitions A for edges 12 and 23, and B for edge 13. This is possible coordinate by coordinate: coordinates in A identify all three, coordinates in B minus A identify only 13, and all others identify none. Transitivity therefore implies that \(\mathcal W\) is upward closed.

Similarly, realize coalitions A, B, and \(A\cap B\) on edges 12, 23, and 13. Transitivity gives closure of \(\mathcal W\) under intersection. If \(\mathcal W\) is empty, f is constantly zero off the diagonal. Otherwise, because the number of input coordinates is finite, let \(D=\bigcap\mathcal W\). Then \(\mathcal W=\{A:D\subseteq A\}\), and the output is the intersection of the relations indexed by D. Conversely every listed operation is an equivalence relation and respects restrictions. QED.

For r=2 this recovers exactly the five submitted operations. For r=3 there are nine. Full symmetry under input permutation, together with pointwise idempotence, retains only intersection of all r inputs. This is an elementary conditional classification, closely related in method to coalition/filter arguments in relational aggregation. No priority claim is made. It does not classify arbitrary stochastic operations or disjoint-carrier amalgamation.

## 3. Randomization defeats the unextended uniqueness claim

A stochastic operation assigns a probability distribution over output equivalence relations:

\[
\mathsf K_S(R,Q)\in\operatorname{Prob}(\mathrm{Eq}(S)).
\]

Restriction naturality now means equality of pushforward probability laws under every injection. Commutativity means \(\mathsf K_S(R,Q)=\mathsf K_S(Q,R)\). Pointwise idempotence means \(\mathsf K_S(R,R)=\delta_R\), not invariance of a random input law under independently sampled copies.

The kernel

\[
\mathsf K_S(R,Q)=\tfrac12\delta_R+\tfrac12\delta_Q
\]

is restriction-natural, commutative, and pointwise idempotent. Whenever R and Q differ, its output need not equal their intersection. Thus removing determinism without replacing it by another condition destroys the uniqueness conclusion. The deterministic theorem retains its explicitly stated scope.

The distinction between a map of structures and a Markov kernel is substantive. Standard categorical treatments of probability explicitly track stochastic maps, conditioning, and independence; they do not derive an apparatus or foundational source from these choices (Fritz, 2020).

## 4. Associativity of fresh Markov-kernel composition restores uniqueness

**Conditional theorem.** Suppose \(\mathsf K_S\) is natural under all finite injections, commutative, and pointwise idempotent. Suppose also that it is associative under ordinary Markov-kernel composition: the intermediate relation is the complete state passed to the next application, and the second draw has the specified conditional kernel, with no additional hidden shared randomness. Then

\[
\boxed{\mathsf K_S(R,Q)=\delta_{R\cap Q}.}
\]

**Proof.** On a two-element carrier there are only two equivalence relations, encoded by 0 for distinct and 1 for equal. Idempotence fixes the output on (0,0) and (1,1). Naturality and commutativity provide one number

\[
a=\Pr(\text{output equal}\mid\text{input statuses }(1,0))
 =\Pr(\text{output equal}\mid(0,1)).
\]

Take three positions and inputs identifying only 12 and only 23, respectively. Output equality of 13 has probability zero, because both inputs separate that pair. The events that the output identifies 12 and that it identifies 23 are therefore disjoint: their simultaneous occurrence would violate transitivity. Each has probability a, so \(2a\le1\).

On a two-element carrier compare the two parenthesizations of inputs (1,0,0). The left parenthesization returns equality with probability \(a^2\); the right returns it with probability a. Markov-kernel associativity gives \(a^2=a\). Together with \(0\le a\le1/2\), this forces a=0.

Every pair is consequently equal in the output with probability one exactly when it is equal in both inputs. A finite union of zero-probability discrepancies shows that the complete output relation is almost surely \(R\cap Q\). QED.

This strengthens the deterministic selection theorem only after a further hypothesis has been supplied. It is not a derivation of that hypothesis. In particular, no physical independence, absence of memory, or universal deletion compatibility follows from the theorem.

### 4.1 Exact countercontrol and a stability estimate

More generally, for \(0\le a\le1/2\), let

\[
\mathsf K^{(a)}_S(R,Q)
 =a\delta_R+a\delta_Q+(1-2a)\delta_{R\cap Q}.
\]

These kernels are natural, commutative, and pointwise idempotent. On (1,0,0), the two parenthesized output laws differ in total variation by exactly \(a(1-a)\). For a=1/2 this is 1/4.

For any kernel satisfying the three exact structural assumptions above, let epsilon bound the associativity defect in total variation for every triple of inputs. The same two-point argument yields

\[
 a(1-a)\le\varepsilon,
 \qquad a\le2\varepsilon.
\]

If \(d(R,Q)\) is the number of unordered pairs on which R and Q disagree, a union bound gives

\[
\boxed{\operatorname{TV}(\mathsf K_S(R,Q),\delta_{R\cap Q})
 \le\min\{1,2d(R,Q)\varepsilon\}.}
\]

This is a dimension-dependent stability bound, not a sharp dimension-free estimate.

### 4.2 A persistent hidden coin changes the contract

Let a single fair bit B be drawn once. At every subsequent binary combination choose the first argument if B=0 and the second if B=1. Reusing this same bit makes either parenthesization of three arguments return the first original argument when B=0 and the third when B=1. The parenthesizations agree.

By contrast, drawing a fresh fair bit independently at each node gives different laws: the left grouping selects the three original arguments with weights (1/4,1/4,1/2), and the right with weights (1/2,1/4,1/4). If the first relation is universal and the other two discrete, their total variation is 1/4.

The persistent-bit implementation is not a counterexample to the theorem. Once past outputs convey information about B, the next conditional operation is not the original fair mixture on the relation alone. B is omitted memory. Retaining it changes the state space and typing of the operation. Single-use equality of response laws does not establish equality of their process composition.

## 5. Coherent output entropy is not automatically controllable information

Consider a coherent family \(Q_k\) on integer-partition types, together with an arity distribution \(\pi_k\). Its output entropy is

\[
H(K,\Lambda)=H(K)+\sum_k\pi_kH(Q_k).
\]

This is a valid entropy of a sampled record. A communication interpretation additionally needs a message M and a specification of which source choices depend on M. Shannon's capacity definition maximizes transmitted information, not output randomness alone (Shannon, 1948).

**Explicit narrower observation/preparation contract.** Fix one family \(Q_k\), independent of M. Let the sender control only the arity K. Conditional on K=k, the apparatus generates \(\Lambda\sim Q_k\), independently of M. The output reveals K, either explicitly or through the size of \(\Lambda\). Then

\[
M\longrightarrow K\longrightarrow (K,\Lambda),
\qquad
I(M;K,\Lambda)=I(M;K)\le H(K).
\]

If neither K nor the pattern preparation depends on the message, the mutual information is zero. Even when order control is granted, the conditional entropy \(H(\Lambda\mid K)\) is uncontrollable randomness in this contract. It can matter for lossless compression of an already sampled record without communicating an independently chosen message.

With K ranging over nonnegative integers, the empty comparison admitted, and \(\mathbb E K\le1\), comparison to the geometric reference \(g_k=2^{-(k+1)}\) gives

\[
H(K)\le-\sum_k\pi_k\log_2g_k=\mathbb E[K]+1\le2.
\]

The usual Gibbs/relative-entropy argument makes this valid even before entropy finiteness is assumed. Equality is attained with \(\pi_k=g_k\) and M=K. Therefore

\[
\boxed{\sup_{\mathbb E K\le1}I(M;K,\Lambda)=2\text{ bits}}
\]

for this order-only control contract. This is a one-use information maximum per attempted preparation, not a physical rate or a universal bound on every allowed encoding. Message-dependent family choice, control of the actual partition, access to shared randomness, or a different observer changes the problem.

### 5.1 Numerical entropy witness

For the Ewens(4/3) family and its finite arity law with beta=1.047262, the source reports the following numerical values:

| Quantity | Value in bits, except the mean |
|---|---:|
| Mean arity | 0.9999962394430055540044 |
| Output entropy \(H(K,\Lambda)\) | 2.3953358338290520666421 |
| Arity entropy \(H(K)\) | 1.9849786487467719689106 |
| Conditional entropy \(H(\Lambda\mid K)\) | 0.4103571850822800977316 |

The probabilities at each arity are exact rationals; the arity weights, logarithms, and displayed decimals are high-precision numerical evaluations, not formal interval enclosures.

The 2.3953 lower entropy witness and 2.419881 relaxed upper entropy bound concern output-entropy optimization. A communication-capacity interpretation additionally requires an encoding contract. The sharp unrestricted 2.420267... entropy can describe an ideal channel only under the separately admitted ability to prepare its outcomes as message symbols.


## Mathematical sources identified in the original note


- T. Fritz, *A synthetic approach to Markov kernels, conditional independence and theorems on sufficient statistics*, Advances in Mathematics 370 (2020), 107239. DOI: 10.1016/j.aim.2020.107239. https://arxiv.org/abs/1908.07021 . Background for stochastic composition, not a claimed proof source for the partition-specific theorem.

- C. E. Shannon, *A Mathematical Theory of Communication*, Bell System Technical Journal 27 (1948), 379–423 and 623–656, sections 11–13. https://academicweb.nd.edu/~powers/ame.20231/shannon1948a.pdf

- Kirtus Justus, with ChatGPT assistance, *Finite-Order Observation, Compositional Typing, and Coherent Entropy in Exchangeable Partitions* (9 November 2026). Unpublished companion mathematical note; internal research provenance and self-citation, not independent corroboration.
