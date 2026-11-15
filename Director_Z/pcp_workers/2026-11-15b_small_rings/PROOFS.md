# PROOFS — small rings worker, 2026-11-15b

Worker one level below Director Z. Author's model family; not independent review. No gate is passed.
Notation of `G10_body_Z31_candidate.tex`, subsection "Four arc gains on rings": the carrier
$D_\delta$ on $\mathbb Z_N$ has gains $a=b=c=1$, $d=\delta$, $\delta$ of finite order $q\ge1$;
$M=N/\gcd(N,2)$; a walk starts at $(0,R)$; after a right step it is on rail $R$, after a left step on $L$;
its gain is $\delta^{g}$ with $g$ = number of left steps that follow a left step. $\lambda(w)$ = number of
left steps ("deficit" $e$). Position product events as in the body (masks $A_1,\dots,A_T$).

## Lemma R (residues)

*Statement.* Let $N\ge1$. After $t$ steps a walk with $e$ left steps is at the site $t-2e \bmod N$, and two
walks after $t$ steps are at the same site iff their deficits are congruent mod $M$. For every mask
$A_t$ there is a set $E_t$ of residues mod $M$ such that a walk survives tick $t$ iff its deficit after
the step lies in $E_t$ mod $M$; conversely every set $E_t$ of residues arises from the mask
$\{t-2e \bmod N: e\in E_t\}$.

*Proof.* The site is $(\#R)-(\#L)=t-2e$. $t-2e\equiv t-2e' \pmod N$ iff $N\mid 2(e-e')$ iff $M\mid e-e'$
(if $N$ is odd, $M=N$; if $N$ is even, $N\mid 2k$ iff $N/2\mid k$). Take $E_t=\{e \bmod M: t-2e\in A_t\}$;
this is well defined by the first part. The converse is the same computation. $\square$

So everything below depends on $M$ only, and every statement is for all $N$ with the given $M$.

## Lemma S (site) and Lemma T (common gain translation)

*Statement S.* If an event realises a content $C$ (walks with rails, deficits, gains) at a site $y$, then for
every site $x$ some event realises $C$ at $x$ with all deficits increased by one common integer and all
gains multiplied by one common power of $\delta$ that the construction may choose to be $1$.
*Statement T.* For every $k$, some event realises $C$ with all gains multiplied by $\delta^{k}$ (at some
site; with S at any site).

*Proof.* T: prefix the event by a single walk $p$ from $(0,R)$ back to rail $R$ with $k+1$ consecutive left
steps followed by right steps (isolated by singleton masks), ending at $(z,R)$; then use the masks of the
event translated by $z$. The ring is invariant under translation, and both parts of every walk leave from
rail $R$, so gains multiply ($g(p)=k$) and all deficits increase by $\lambda(p)$. S (as used in this file):
in the constructions below, after the last deposit the packets are pairwise at circular distance $\ge2$
and a tick in which every packet steps right ("coast") is exclusive (Lemma E); each coast tick moves every
site by $+1$ and changes no gain and no deficit; $c$ coast ticks reach every $x$ (for even $N$ the parity
of $T$ changes with $c$). $\square$

## Lemma E (exclusive ticks; packets)

*Definitions.* A packet is a non-empty set of walks at one residue at a tick. A move of a packet is R, L,
S (both) or X (none). Its required residues are $u$ (R), $u+1$ (L), both (S), none (X); its excluded
residues are the others of $\{u,u+1\}$. A tick (a set of packets at distinct residues with moves) is
*exclusive* if no excluded residue of any packet lies in the set $E$ of all required residues.

*Statement.* With $E_t=E$, after an exclusive tick the walks of each packet are exactly its walks continued
by its move. If two packets are at circular distance $\ge2$ (i.e. $v-u\notin\{-1,0,1\}$ mod $M$), no
choice of their moves makes a conflict between them; so a tick is exclusive as soon as every pair of
packets at circular distance $\le1$ is free of conflict.

*Proof.* A walk at deficit $e$ has the two candidates $e$ and $e+1$; it survives with a candidate iff the
candidate's residue is in $E$. Required residues are in $E$; excluded ones are not, by exclusivity. A
conflict between packets at $u$ and $v$ needs a residue in $\{u,u+1\}\cap\{v,v+1\}$, empty when
$v-u\notin\{-1,0,1\}$. $\square$

## Theorem A (three groups on two levels for $M\ge6$)

*Statement.* Let $N\ge1$ with $M=N/\gcd(N,2)\ge6$, and $\delta$ of finite order $q\ge1$. For every site
$x$ and all $G_1,G_2,G_3\in\mathcal M(\langle\delta\rangle)$ there are position product events in $D_\delta$
on $\mathbb Z_N$ in which the walks that end at the site $x$ are exactly
(i) on $R$ the multiset $G_2$ at one level $l$; on $L$ the multiset $G_3$ at $l$ and $G_1$ at $l+M$;
(ii) on $R$ the multiset $G_3$ at $l$ and $G_1$ at $l+M$; on $L$ the multiset $G_2$ at $l+M$;
and no walk ends at another site ("at level $l$" = with $\lambda=l$).

This is Proposition prop:threegroups of the body with $M\ge8$ replaced by $M\ge6$. Status: **PROVED** below
(hand proof, all $M\ge6$), and **COMPUTED** (finite stage check and replays on the actual rings,
$M=6,\dots,14$; `worker/spb_schedule.py`).

*Proof.* If $G_1=G_2=G_3=\emptyset$ take $A_1=\emptyset$. Otherwise use packets (Lemma E), positions given
as deficits relative to the source $S$ at a gadget boundary, every walk having arrived by a right step at
every boundary (true at the start: the walk of length $0$ is on $R$). Put $a=4$. Packets: the source $S$
(one walk), $P$ at residue $a$ whose walks have deficit $e_S+a$ ("high", group $A=G_1$) or $e_S+a-M$
("low", group $C=G_3$), and $B$ at deficit $e_S+2$ (group $B=G_2$). Circular distances: $S$–$B$ $=2$,
$B$–$P$ $=2$, $P$–$S$ $=\min(4,M-4)\ge2$ for $M\ge6$.

Gadgets (moves per tick, in order; "others" are the packets present other than those named):
1. adv (4 ticks): $S$: L, L, R, R; others: L, R, L, R.
2. dep$P^{+}$: $S$: S (split; its left part is the copy $c$), others R; then while $c$ has not reached
   residue $a$: $c$: L, all others R (the last such tick merges $c$ into $P$ at residue $a$, or creates
   $P$ there); then one tick all R.
3. dep$P^{-}$: $S$: S, others L; the right part is the copy $c$, the left part is the new source; then
   while $P$ (low level) has not reached $c$: $c$: R, all others L (the last such tick merges; if $P$ does
   not exist, stop when $c$ is at relative position $a-M$, creating $P$); then one tick all R.
4. dep$B$: $S$: S, others R; then $c$: L, others R (merging into $B$ at relative position $2$, or creating
   it); then one tick all R.
5. remove: $S$: X, others R.
6. end (i): $P$: L, $B$: R, repeated until $e_B-e_{P,\rm low}=2$, then two ticks $P$: L, $B$: R.
   end (ii): one tick $B$: L, $P$: R (bringing $e_B-e_{P,\rm low}$ from $M-2$ to $M-1$), then one tick
   $B$: L, $P$: R.

Schedule: all deposits into $P$ ($C$ walks by dep$P^-$, $A$ walks by dep$P^+$, each preceded by some
number of advances), with $B$ absent; then all deposits into $B$ (each preceded by advances); remove; coast
(Lemma S) to bring the final site to $x$; end (i) or (ii). An empty group is replaced by a position without
walks (it only adds residues to masks; Lemma E then still applies, the masks without it are subsets).

*Exclusivity (Lemma E, only pairs at distance $\le1$ need checking; residues mod $M$, $M\ge6$).*
- adv, packets at $S{:}0$, $B{:}2$, $P{:}4$ (any subset): tick 1 candidates $\{0,1\},\{2,3\},\{4,5\}$
  pairwise disjoint; tick 2 ($S$ at 1 L, $B$ at 3 R, $P$ at 5 R): $\{1,2\},\{3,4\},\{5,6\}$ disjoint since
  $6\not\equiv1$; tick 3 ($S$ at 2 R, $B$ at 3 L, $P$ at 5 L): $S$ requires 2 excludes 3, $B$ requires 4
  excludes 3, $P$ requires 6, excludes 5, and $6\not\equiv 2,3,4$; tick 4 all R from $2,4,6$: candidates
  $\{2,3\},\{4,5\},\{6,7\}$ pairwise disjoint mod $M$ for $M\ge6$ ($6,7$ reduce to $\{0,1\}$, $\{6,0\}$
  or $\{6,7\}$ for $M=6$, $7$, $\ge8$). Result: all at $+2$; $S$ gains one factor $\delta$ (one LL), the others none.
- dep$P^+$ ($B$ absent, $P$ at 4 or absent): split: $\{0,1\}$ vs $\{4,5\}$ disjoint ($5\not\equiv0$).
  Copy at $u\in\{1,2,3\}$ steps L, $S$ at 0 and $P$ at 4 step R: only the pairs ($S$, copy at 1) and
  (copy at 3, $P$) are at distance 1: $S$ requires 0 excludes 1, copy requires 2 excludes 1; copy requires
  4 excludes 3, $P$ requires 4 excludes 5 (merge, intended; $5\not\equiv0,2$). Copy at 2 or 3 vs $S$:
  distance $\ge2$ since $u\le M-2$. Idle tick: $S{:}0$, $P{:}4$, distance $\ge2$.
- dep$P^-$: split tick $S$ at 0 S, $P$ at 4 L: $\{0,1\}$ vs $\{4,5\}$ disjoint. Then copy at residue 0
  steps R; new source at $1+j$ and $P$ at $5+j$ step L ($j=0,1,\dots$). Pairs at distance 1: (copy, source)
  for $j=0$: copy requires 0 excludes 1, source requires 2 excludes 1; ($P$, copy) when $P$ is at $M-1$:
  $P$ requires 0 excludes $M-1$, copy requires 0 excludes 1 (merge, intended). Source–$P$ distance stays 4
  / $M-4$; copy–source distance $j+1\le M-4$ forward and $\ge4$ backward. The merge happens after
  $M-4$ ticks (including the split tick); then $P_{\rm low}$ has the copy's deficit and the source is at
  relative position $M-a$ from it: the configuration returns. The copy's deficit is its source's old deficit,
  i.e. the low level.
- dep$B$ ($S{:}0$, $B{:}2$ or absent, $P{:}4$ or absent): split $\{0,1\}$ vs $\{2,3\}$, $\{4,5\}$ disjoint.
  Next tick: ($S$, copy at 1): $S$ requires 0 excludes 1; copy requires 2 excludes 1; $B$ requires 2
  excludes 3 (merge, intended); $P$ requires 4 excludes 5 ($5\not\equiv 0,2$). Idle tick: distances 2,2,$\ge2$.
- remove: $S$ excludes 0,1; $B$ requires 2, $P$ requires 4 ($\not\equiv0,1$); exclusions 3, 5 are not required.
- coast: $B{:}2$, $P{:}4$, distance $\ge2$.
- end (i): $P$ climbs from residue 4 to $M\equiv0$ with $B$ at 2: $P$ at $r\in\{4,\dots,M\}$ has distance
  $r-2\ge2$ and $M+2-r\ge2$ to $B$; then $P{:}0\to1$ ($\{0,1\}$ vs $\{2,3\}$ disjoint), then $P{:}1\to2$ with
  $B$ R: both require 2, exclusions 1 and 3 (merge, intended, on different rails).
- end (ii): $B{:}2\to3$, $P$ R at 4 (distance 2); then $B{:}3\to4$ L, $P$ R at 4: both require 4,
  exclusions 3 and 5 (merge, intended).

*Levels.* dep$P^+$ walks have deficit $e_{P,\rm low}+M$, dep$P^-$ walks $e_{P,\rm low}$; $B$ walks
$e_{P,\rm low}+M-2$ after removal (relative positions $2$ and $4-M$). end (i) makes $e_B=e_{P,\rm low}$, with
$B$ arriving by R and $P$ by L: (i) holds with $l=e_{P,\rm low}$. end (ii) makes $e_B=e_{P,\rm low}+M$, $B$
by L, $P$ by R: (ii) holds.

*Gains.* At a boundary every walk is on $R$. An advance adds $1$ to the exponent of $S$ (one LL) and $0$ to
every other walk (LRLR from $R$). Every other gadget adds to each walk an exponent fixed by the gadget type
and the walk's role in it (the moves and the rails at the start are fixed; in a merge tick the copy and the
packet may arrive on different rails, and the idle tick puts all on $R$ before the next gadget; the end
gadgets are the same for all walks of one packet). Hence, for a fixed order of the gadget types, the final
exponent of the walk deposited $i$-th is $n_i+\kappa_i$, with $n_i$ the number of advances before that
deposit and $\kappa_i$ independent of the $n_j$. Choose $n_1\le n_2\le\dots$ with
$n_i\equiv t_i-\kappa_i \pmod q$, $t_i$ the required exponent. $\square$

**Remark (why $M\ge6$ and where $M=5$ fails).** Three packets at pairwise circular distance $\ge2$ need
$M\ge6$. On $\mathbb Z_5$ the schedule is not exclusive (program control P3). Moreover: *on $\mathbb Z_5$, a
single walk $S$ and two other packets $X,Y$ with $S$ at circular distance $\ge2$ from both cannot be
followed by a clean split of $S$* — the gaps around $S$ are then $(2,2)$, $X,Y$ are adjacent and must
spread, and in the next tick the pair ($S$, its copy) and the pair ($Y$, $S$) demand opposite moves of $S$
(checked by hand for both choices of which part continues as the source). This does not exclude other
events on $\mathbb Z_5$; see FINDINGS for the exhaustive search.

## Corollary A1 (consequences, conditional only on the body's proofs)

The proofs of Theorem thm:fgtwo, Theorem thm:fgadj, Corollary cor:pplus8 (draft) and Theorems thm:fgprod,
thm:fgthree (draft) use Proposition prop:threegroups only through its statement, together with Lemmas
fgkappa, fgonesite, fginv, Theorem fgsolve (i),(ii) and the prefixes of prop:fgonelevel, which need $N\ge3$.
Hence, by Theorem A, each of them holds with "$M\ge8$" replaced by "$M\ge6$". In particular $P^+_\delta$ holds
for $M\ge6$ without \cite{dgone} (mode (i) with $G_1=\emptyset$), i.e. for $M=6,7$ the condition left open
after cor:pplus8 is removed. Status: **PROVED given the body's proofs as written** (the worker checked that
these proofs cite only the statement of prop:threegroups; it did not re-review those proofs).
