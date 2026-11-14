# When one reversible circuit transports two input columns

**Kirtus Justus**, Theoretical Physicist, Port Coquitlam, British Columbia, Canada. Research supplement by Director G (OpenAI Codex).

At tick 37, the two input rails of the signed walk give a small example of a simultaneous transport obstruction. At the two mirror sites \(+25,-25\), either input rail separately admits a reversible conversion to a prescribed reference. One circuit working for both rails cannot make those two conversions. The obstruction remembers a direction of the input coin modulo 5. The squared masses of the two inputs and the gcd for each individual column miss it. This section gives a criterion for when a common circuit exists and a construction using four reflections.

## The criterion

Let \(D=\mathbb Z[1/2]\). Let \(X\) and \(Y\) have two columns, entries in \(D\), finite row counts \(n_X,n_Y\) and rank two. The two columns refer to the same ordered input basis. A common overall scale, such as \(2^{-t/2}\) for an integer walk table, can be removed from both. The **row module** \(L_X\subset D^2\) is the set of all dyadic linear combinations of the rows in those input coordinates. The Gram matrix \(X^{\mathsf T}X\) includes the cross term.

**Theorem.** After adjoining zero output coordinates there is a dyadic orthogonal matrix transporting \(X\) to \(Y\) precisely when
\[
             X^{\mathsf T}X=Y^{\mathsf T}Y,\qquad L_X=L_Y.
\]
It suffices to use disjoint source and destination slots and at most \(n_X+n_Y+12\) coordinates before binary-address padding. Four Householder reflections implement the conversion on both full columns. The dimension bound counts named data coordinates, and assumes gates addressed across them. It gives no bound on nearest-neighbor time or on the coefficient sizes found by the search below.

For necessity, orthogonality preserves the Gram matrix. Left multiplication by a dyadic matrix makes each output row a dyadic combination of input rows. Applying the inverse gives the other inclusion. The latter reasoning also applies to circuits over \(D[\sqrt2]\) with dyadic endpoints. Taking the rational component of \(Y=UX\) and of its inverse relation gives dyadic row combinations in each direction. This does not require the rational component of \(U\) to be unitary.

To test equality constructively, test membership of every generating row in the other row module and reverse roles. For a full-rank list of dyadic rows, clear a common power-of-two denominator and compute ordinary row Hermite normal form over the integers. Its two nonzero rows are a \(D\)-basis of the original module since that denominator is a unit. Multiplying a test row by the inverse of this two-by-two basis gives its unique coefficients. Membership means that both are dyadic. Equal Smith invariants on their own can describe distinct submodules of the fixed input plane.

## Construct a common intermediate frame

Choose one row basis \(B\) of the common module, arranged as a \(2\times2\) matrix. Write \(X=F B,\ Y=G B\). Each of \(F,G\) has rows generating all of \(D^2\). In particular there are dyadic right inverses for \(F^{\mathsf T}\) and \(G^{\mathsf T}\). Equivalently the \(2\times2\) minors generate the unit ideal: multiply a Bézout combination of determinants by the corresponding embedded adjugates to get a right inverse. The converse follows by taking the determinant of a right-inverse product and expanding in minors. The matrices \(F,G\) have the same positive-definite Gram \(M\) because \(B\) is invertible over the rationals.

First change both input coordinate charts by the same \(S\in{\rm SL}_2(D)\). This is algebra on the two known columns. It need not be implemented on an unknown input coin. Write \(U=FS,V=GS\) and \(H=S^{\mathsf T}MS\). We want a power of two \(\Delta>0\) for which, with \(C=H-\Delta I\),
\[
                    K_0=H-2CH^{-1}C
\]
has \(K_{0,11}>|K_{0,12}|\) and \(K_{0,22}>|K_{0,12}|\).

Here is why a search terminates. Set \(\lambda=\sqrt{\det M}\). The real matrix \(T=\sqrt{\lambda}\,M^{-1/2}\) has determinant one and \(T^{\mathsf T}MT=\lambda I\). The dyadic determinant-one group is dense in the real one. Indeed let \(U(a),L(a)\) denote the upper and lower unit triangular shears of entry \(a\). A real determinant-one matrix with entries \(a,b,c,d\) in row order and \(c\ne0\) is \(U((a-1)/c)L(c)U((d-1)/c)\). A matrix with \(c=0\) is a limit of ones with \(c\ne0\), by a small left lower shear. Rounding the three parameters to dyadics proves density while retaining determinant one exactly. Choose \(\Delta=2^{\lfloor\log_2\lambda\rfloor}\), computable by comparing powers of four to \(\det M\), including negative exponents. At \(T\), \(K_0\) equals \((\lambda-2(\lambda-\Delta)^2/\lambda)I\), with diagonal \(>\lambda/2\). The inequalities persist on a neighborhood. Enumerate dyadic shear triples of increasing numerator and denominator bit bounds until the two rational comparisons hold. No real eigenvector is needed for the executable criterion. [Elementary-matrix background, Chapter 28](https://jvoight.github.io/quat-book.pdf)

Put the source and target on disjoint sets of coordinates. On the source support we seek a dyadic \(A\) with \(U^{\mathsf T}A=C\), and on the destination support a dyadic \(E\) with \(V^{\mathsf T}E=C\). The ideal rational targets are \(U H^{-1}C\) and \(V H^{-1}C\). Round the first entrywise to a dyadic grid obtaining \(R\), and set
\[
                     A=R+J_U(C-U^{\mathsf T}R),
             \qquad U^{\mathsf T}J_U=I .
\]
Use the analogous repair for \(E\). The right inverses exist since the charts remain primitive. Crucially \(C\) is dyadic even if \(H^{-1}\) is not. The repaired matrices are dyadic and approach their ideal targets as the grid is refined. The residual \(K=H-A^{\mathsf T}A-E^{\mathsf T}E\) approaches \(K_0\). Double the grid until the residual is positive definite. In the proof one could continue until both strict dominance inequalities hold as well.

An initially positive-definite residual need not already be diagonally dominant. It still admits the same 12-row bound. Under integral congruence, swap columns and rows together if required to put the smaller diagonal entry $a$ first. If the off-diagonal entry $c$ has $|c|\ge a$, subtract $m=\operatorname{round}(c/a)$ copies of the first basis vector from the second. Its new squared length is the old one minus $2mc-m^2a$, strictly smaller because $|c|\ge a$ and $|c/a-m|\le 1/2$. A swap preserves the trace, every such shear decreases it, and all entries remain integral multiples of the original common dyadic grid. The positive trace therefore gives finite termination with strict diagonal dominance. Fill the resulting form $T^{\mathsf T}KT$ as below and right multiply the new rows by the integral $T^{-1}$. This version lets a caller supply any chart and scale with positive-definite $K_0$. If the chosen chart already gives that property, the density search can be skipped.

For \(h=K_{12}\), write \(K\) as the sum of three nonnegative multiples of dyadic rank-one matrices:
\[
  |h|(1,\operatorname{sgn}h)^{\mathsf T}(1,\operatorname{sgn}h)
       +(K_{11}-|h|)e_1 e_1^{\mathsf T}+(K_{22}-|h|)e_2e_2^{\mathsf T}.
\]
Here \(e_i\) are column vectors and the first term is zero for \(h=0\). Each nonnegative dyadic coefficient is a sum of at most four squared dyadics: multiply by a squared power of two clearing its denominator, use Lagrange's four-square theorem, and rescale. Base-four expansion also supplies a deterministic sum of dyadic squares, with one to three copies of each nonzero power per digit. That choice can use more than 12 rows but avoids the four-square search. The four-square choice yields at most 12 rows \(W\) with \(W^{\mathsf T}W=K\). Together \(Z=[A;E;W]\) has Gram \(H\) and the padded \(U,V\) satisfy \(U^{\mathsf T}Z=V^{\mathsf T}Z=C\). [Four-square construction](https://www.pollack-math.net/finding4squares.pdf)

The two columns \(w_i\) of \(U-Z\) now have Gram \(2\Delta I\), and \(U^{\mathsf T}(U-Z)=\Delta I\). The two orthogonal dyadic maps \(I-w_iw_i^{\mathsf T}/\Delta\) commute, subtracting \(w_i\) from column \(i\) and fixing the other column. Their product sends \(U\) to \(Z\). Apply the same construction with \(Z-V\) to send \(Z\) to \(V\). Right multiplying the identity by \(S^{-1} B\) recovers the original \(X,Y\). Their common conversion is the laboratory operation; the chart changes cancel. The normals have squared norm a power of two, so the existing sign, four-coordinate Walsh and binary-register Hadamard synthesis compiles each reflection after padding the dimension. [Compilation and gate assumptions](Compact_transport_of_a_flight_bin.md) · [Amy, Glaudell, Li and Ross](https://arxiv.org/abs/2305.11305)

For \(X^{\mathsf T}X=Y^{\mathsf T}Y=P I\) with primitive rows in each table, use \(B=S=I\), \(H=P I\), directly. For rank one with equal Gram and equal row modules, choose their common single basis row and apply the [one-column theorem](Stable_flattening_inside_a_recorded_bin.md) to its coefficient columns; the coefficients in both lists generate the unit ideal and their norms agree. Equal zero Gram means all entries vanish.

## A native obstruction and its positive control

The three-tick shell \(|x|=1\) of the localized Hadamard walk gives source rows \((-1,1),(0,-2),(2,0),(1,1)\) in the order \(-1\) then \(+1\), right and left output rails within each site. They have Gram \(6I\). On disjoint supports the target is two copies of \((2,1,1)\), one per input column. In the ordered 4+6+2 slots a midpoint has rows
\[
(0,0),(0,-1),(1,0),(0,0);\quad
(1,0),(0,0),(0,0),(0,1),(0,0),(0,0);\quad (2,0),(0,2).
\]
Its cross Grams with both endpoints are \(2I\), so use \(\Delta=4\). The checker compiles and replays the four reflections on both input columns. It also tests a positive non-scalar Gram after factoring a shared proper row module, transports the original two columns in both directions, and checks Gauss reduction of a non-dominant slack example. The checker accepts an explicit chart or a positive-definite ideal slack, with a choice of four-square or deterministic base-four padding. It does not implement the exhaustive chart search. Lean checks the denominator-cleared normal Gram, the effect on one coordinate and preservation of a linear congruence under two integral row combinations. [Lean identities](lean/TwoColumnTransport.lean) [Checker](check_two_column_transport.py) · [Results](results/two_column_transport.json)

At 37 ticks take the two sites \(+25,-25\), in that order. Removing the common divisor 80 from the four numerator rows gives
\[
(1984,937),\quad(663,384),\quad(-384,663),\quad(937,-1984).
\]
For either column its scalar gcd is one. Their reduced Gram is \(5{,}401{,}250 I\). The reduced second column is three times the first modulo 5, yet the matrix has full real rank. Its two-by-two minor gcd is 25. As reference choose disjoint copies of any primitive integer column of the same squared norm, for example a 1 followed by a base-four square expansion of \(5{,}401{,}249\). The reference has a unit minor formed from its two unit rows. Restoring the common factor 80 on both endpoints preserves both individual transfer comparisons and the failure of a joint transfer. The complement can be left unchanged. This is an obstruction in one protected sector of the actual two-input walk. It does not assert that the mathematical reference has already been prepared physically.

Even the gcd of the minors is too coarse. Take the two matrices with rows \((1,2),(-2,1)\) and \((1,-2),(2,1)\). Both Grams are \(5I\), all scalar column gcds are one, and the determinants agree at 5. Their row spans modulo 5 are the distinct lines through \((1,2)\) and \((1,-2)\). No common left circuit transports them in the named input basis.

A positive transport is complex-linear on the span of the two real input columns, including a spectator tensored with the gate. The construction assumes access to all listed output rows of a protected sector and its clean padding. Measuring before conversion, keeping a controller copy of the input, or changing the input basis independently between source and target describes another instrument. Even a successful two-column transport establishes an equality of kinematic preparations. Transferring a physical flag rate still needs evidence for the record and its read.
