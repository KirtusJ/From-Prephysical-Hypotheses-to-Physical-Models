# Implementing the fixed-point echo on three signed memory addresses

**Kirtus Justus**, Theoretical Physicist, Port Coquitlam, British Columbia, Canada. Research supplement by Director G (OpenAI Codex).

The [binary echo audit](A_binary_read_of_amplified_echoes.md) uses a selective phase of sixty degrees to cube the blank mass on each recursion. A three-address memory realizes that transformation exactly using a balanced signed preparation and an addressed signed cycle. The initial memory has real amplitudes. Either orientation of the cycle gives the same final blank mass. There is no Fourier-sector herald or choice of primitive complex character in the preparation.

## The physical memory operation

Let \(C|s\rangle=|s+1\bmod 3\rangle\) and \(A=-C\). Prepare the product of the data blank and \(\chi=(|0\rangle-|1\rangle)/\sqrt2\) on the memory, using one balanced signed splitter and an unused dark address. In physical coordinates,

\[
 (A^2-A+I)(a,b,c)=(a+b+c)(1,1,1).
\]

Consequently the zero-sum plane containing \(\chi\) is invariant and satisfies \(A^2-A+I=0\). This integer identity remains valid for complex coefficients or vector-valued spectator coefficients. The [Lean file](lean/SignedSheetEcho.lean) checks it before any change of basis.

Let \(P_0\) select the complete data blank, \(P_1=I-P_0\), and \(A_j=P_j\otimes A+(I-P_j)\otimes I\). Every data echo \(W\) and its matched inverse act identically at the three addresses. Set \(V_0=W\otimes I\) and \(V_{k+1}=V_k A_0 V_k^\dagger A_1 V_k\). Pool all three memory addresses in each final data outcome. For initial blank mass \(b=|\langle 0|W|0\rangle|^2\), the mass in the complete data blank at depth \(k\) is **exactly \(b^{3^k}\)**.

To see this, diagonalize \(A\) on the invariant plane for the calculation. Its two eigenvalues are the roots \(z,\bar z\) of \(t^2-t+1=0\). Each sector is preserved by every gate. In a sector with eigenvalue \(u\), suppose the current blank amplitude is \(a\), of mass \(B=|a|^2\). As in the scalar echo, the next blank amplitude is
\[
 a\{1+(u-1)[B+u(1-B)]\}=a uB .
\]
The squared modulus is \(B^3\) in **both** sectors, even for complex \(W\). The sectors are orthogonal in the kinematic norm, so pooling their blank blocks gives the same mass for any normalized initial memory on the plane in product with the data blank. This is an algebraic use of complex coordinates. No probability rule has been used to treat the sector weights as observed frequencies. The scalar recursion is Grover's fixed-point construction. [Grover (2005)](https://doi.org/10.1103/PhysRevLett.95.150501)

Only the data-blank address need control a memory gate. Write \(A_1=(I\otimes A)A_0^\dagger\). The unconditional memory rotation \(I\otimes A\) commutes with every gate and with the final blank projector. Omitting it and using \(A_0^\dagger\) in place of \(A_1\) changes \(V_k\) by \(k\) unconditional memory strokes: at each recursive substitution the preceding powers on \(V_k,V_k^\dagger,V_k\) cancel to one copy and the complement contributes one further stroke. All blank and nonblank **pooled** masses are unchanged. Individual memory-port populations can move. Inverse addressing uses the reverse signed cycle, or five forward applications since \(A^6=I\).

## What fails on a localized sheet

Let \(\eta\) be the initial memory's squared norm on the uniform vector. On this direction \(A=-I\). At the first recursion its blank mass is \(b(4b-3)^2\), by the same amplitude expression with \(u=-1\). Thus a product input with any memory vector has first-step blank mass
\[
 (1-\eta)b^3+\eta b(4b-3)^2 .
\]
The localized launch \(|0\rangle\) has \(\eta=1/3\). For a balanced data echo, it gives blank mass \(1/4\), while the zero-sum input gives \(1/8\). At every depth the absolute error from a contaminating uniform component is at most \(\eta\), since the gates preserve the sectors and the blank mass of either sector lies in \([0,1]\). A bright read on the two individual memory addresses generally measures a different quantity.

Three coordinates matter when the available real matrices have entries in \(\mathbb Q(\sqrt 2)\), as for signed permutations and normalized balanced Hadamards. A two-dimensional real orthogonal matrix satisfying \(A^2-A+I=0\) has determinant one and trace one, hence diagonal elements \(1/2\) and off-diagonal elements \(\pm\sqrt3/2\). These are outside that field: squaring \(r+s\sqrt2=\sqrt3\) with rational \(r,s\) forces \(rs=0\), while neither 3 nor \(3/2\) is a rational square. This rules out a standalone two-coordinate orthogonal implementation in this gate field. A nonorthogonal rational basis of the three-address plane has a different Gram matrix. The argument gives no lower bound on protocols that couple the data directly to other systems.

The signed controls use the register and coherent routing available in earlier [rational reference circuits](Rational_references_and_optical_bypass.md). This construction needs no orientation comparison with a stored reference and no approximation to the rotation angle. The exact addressed cycle remains an additional control for an autonomous walk whose only operation is its fixed tick. The experiment also requires the signed preparation, a product data blank, memory-independent data echoes and inverses, and a detector that pools the memory *before* applying its response. Under the [randomized two-port read](A_binary_read_of_amplified_echoes.md), the same original-launch leakage bound then follows. The construction furnishes a kinematic circuit and supplies no measured audit rate or unconditional selection of the ordinary probability embedding.

The [physical-coordinate checker](check_signed_sheet_echo.py) propagates all six data and memory coordinates, checks both addressed circuits, keeps all ports in the [result record](results/signed_sheet_echo.json), and tests the localized control. For data column \((12/13,5/13)\), the clean and localized blank masses after one step are respectively \(2985984/4826809\) and \(2219184/4826809\). Reproduce with `python -B Director_G/check_signed_sheet_echo.py NEW_OUTPUT_FILE.json`.
