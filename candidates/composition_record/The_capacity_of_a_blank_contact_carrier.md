# How much classical memory must the blank contact carrier already have?

**Kirtus Justus**, Theoretical Physicist, Port Coquitlam, British Columbia, Canada. Research supplement by Director G (OpenAI Codex).

The candidate can write 125 covectors through closed contact sequences. If the same isolated classical device also implements every individual contact and its inverse as a reversible action of the proposed group, **a single blank requires at least 3,125 reachable states** to answer every late binary probe correctly after a closed write. Below that threshold, a blinded test has an unavoidable mean error of at least \(5/31\), even for a device with 3,124 available states. This is a prediction about the memory capacity the primitive actions presuppose. A system with the necessary capacity can start in one completely known state. Capacity alone does not establish that any earlier event was recorded there. [Candidate and earlier bounds for completed writes](README.md)

## Two stages of a blinded test

Write \(V=\mathbb F_5^3\) and \(Z=V^*\). In a fixed unit-volume basis the determinant sends \(a,b\) to the covector \(a\times b\). Primitive contacts obey

\[
 (a,u)(b,v)=(a+b,u+v+\tfrac12 a\times b),\qquad (a,u)^{-1}=(-a,-u).
\]

The group \(G\) has \(5^6\) elements and center \(0\times Z\). The group commutator of \((a,0),(b,0)\) writes \(a\times b\). The three pairs of coordinate generators write a basis of the center. Any requested \(u\in Z\) can therefore be realized by a finite word in the same three ordinary generators and their inverses.

1. Begin each trial in one blank state. An independent verifier draws \(u\) uniformly from the 125 covectors and applies its compiled central word. Isolate the carrier and disconnect the preparation controls. Shorter words can be padded with identities to use a common schedule. The readout has no access to the settings, source labels, timing differences, or a second prepared memory carrying \(u\).
2. Choose \(q\) independently and uniformly from one fixed representative of each of the 31 projective lines in \(V\). The decoder receives this freely chosen probe and the carrier. Score whether it returns the prescribed bit \(1_{u(q)\ne0}\). Retain every assigned trial; a missing answer is an error. Repeat preparations to estimate the population rate.

The device class here is explicit. The isolated classical carrier admits a right group action: each primitive acts by a permutation, and every relation of \(G\) holds on its reachable states. The decoder may use arbitrary functions and fresh randomness. Shared randomness independent of the two inputs may select an action, blank, and decoder before a trial, provided each resulting carrier obeys the stated size cap. A history-dependent controller or an actuator that recognizes entire requested words can implement a larger effective state space. Agreement on the 125 compiled central writes alone cannot validate the group-action assumption. Relations involving primitive words and their continuations require independent control or characterization. No counting of optical or quantum modes is implied by a bound on classical distinguishable states.

## The sharp error at each capacity

| Maximum states available | Least possible mean binary error |
|---:|---:|
| 1–24 | \(1/5\) |
| 25–124 | \(6/31\) |
| 125–3,124 | \(5/31\) |
| At least 3,125 | \(0\) |

**Proof.** Let \(H\) be the stabilizer of the blank. The reachable states are the cosets \(Hg\), so the orbit has \(|G|/|H|\) elements. Write \(K=H\cap Z\), identifying \(Z\) with the central subgroup, and let \(A\) be the image of \(H\) in the ordinary label space \(V\). These are linear subspaces with \(c=\dim K\) and \(t=\dim A\). The projection homomorphism gives \(|H|=5^{t+c}\). For \(a,b\in A\), take any lifts in \(H\). Their commutator belongs to \(H\cap Z\), giving \(a\times b\in K\). The span of these products has dimension \(t(t-1)/2\), because the determinant identifies the exterior square of \(V\) with \(Z\). Thus \(t\le1,2,2,3\) at \(c=0,1,2,3\), respectively. The minimum orbit sizes in the four cases are \(3125,125,25,1\). This argument concerns the orbit of one common blank. It imposes no lower bound of 3,125 on an arbitrary permutation representation spread over many disjoint orbits. Coset actions and their point stabilizers are standard in the study of finite permutation representations. [Elias, Silberman and Takloo-Bighash, permutation representations of nilpotent groups](https://www.math.uic.edu/~rtakloo/papers/group-paper/delta.12.pdf)

Two central writes give the same state exactly when their difference lies in \(K\). For any fixed probe that annihilates \(K\), its correct bit is constant on each coset \(u+K\). For any other probe the scalar \(u(q)\) is uniform on the five residues in each coset. The best decoder then raises the flag and errs on one fifth of those cases. There are \((5^{3-c}-1)/4\) projective probes annihilating \(K\). Substitution gives the four errors in the table. The same lower bound holds with input-independent shared randomness by fixing its value before averaging.

All bounds are attained. Choose a stabilizer of the form \(H=A\times K\) with \(a\times b\in K\) for every \(a,b\in A\), and let the primitive contacts act by right multiplication on \(Hg\). For \(c=0\), take \(A=\langle e_1\rangle\). For \(c=1,2\), take \(A=\langle e_1,e_2\rangle\) and \(K\) containing the third dual basis vector. For \(c=3\), take the whole group. The blank coset stores precisely \(u+K\) on central words, for which the preceding decoder is optimal. The [integer replay](check_blank_action.py) enumerates all 64 subspaces of each factor and checks the primitive transition of every group element in all four attaining actions. The [exact data](blank_action_results.json) give the full 3,875-assignment error denominators.

The 125-state tier is particularly discriminating. A register that accepts a complete command “add this covector” can store \(u\) itself and answer every probe correctly. An equally large classical register that implements the required *primitive* group action must make at least 625 errors per 3,875 assignments under the uniform test. Perfect central readout with a 125-state cap therefore contradicts at least one of the primitive-action, isolation and capacity premises. It does not determine which one failed.

## Reading between primitive contacts

A stronger operational requirement gives a different bound. Suppose a read after **any** prefix \((x,v)\) must report \(1_{v(q)\ne0}\) for every probe \(q\), with the same decoder. Appending \(g=(x,v)\) after any \(h=(a,u)\in H\) leaves the blank in the same state as appending \(g\) alone. Choose \(v=0\). The two ideal central values are \(u+\tfrac12a\times x\) and zero. Perfect answers for all \(q\) imply \(u+\tfrac12a\times x=0\) for all \(x\). Set \(x=0\) to get \(u=0\), then vary \(x\) to get \(a=0\). Thus \(H\) is trivial and all **15,625** states are reachable. The regular action on \(G\) attains this bound. The requirement calibrates a read of the central coordinate on an unfinished word, beyond the original closed-write test.

For a concrete challenge, the 3,125-state device above has \(H=\langle(e_1,0)\rangle\). It gives identical states after the single prefix \((e_2,0)\) and the chronological prefix \((e_1,0)(e_2,0)\). The candidate's central scalars at \(q=e_3\) are respectively zero and three. This independently chosen late probe distinguishes the candidate from that minimal closed-write implementation. The full associative simulator on the group reproduces both answers and all central trials. Absolute identification of a first physical record remains open.
