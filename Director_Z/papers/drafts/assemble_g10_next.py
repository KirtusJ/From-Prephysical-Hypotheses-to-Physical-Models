#!/usr/bin/env python3
"""Assemble the G10 body for the next edition: insert the draft subsection on total positivity and products after
the winding subsection.  Usage: assemble.py <draft subsection> <build dir with body.tex and G10_manuscript.tex>."""
import sys, re
draft, B = sys.argv[1], sys.argv[2]
d = open(draft).read()
i = d.index(r"\subsection{Four arc gains on rings: total positivity"); j = d.index("% Bibliography entries needed:")
sub = d[i:j].rstrip() + "\n\n"
p = B + "/body.tex"; s = open(p).read()
k = r"\section{Gains of bounded order and a force}\label{sec:force}"
assert s.count(k) == 1 and r"\label{thm:tp}" not in s
s = s.replace(k, sub + k); open(p, "w").write(s)
m = B + "/G10_manuscript.tex"; t = open(m).read()
bib = r"""\bibitem{lgv} B. Lindstr\"om. On the vector representations of induced matroids. \emph{Bull. London Math. Soc.} \textbf{5} (1973), 85--90; I. Gessel and G. Viennot. Binomial determinants, paths, and hook length formulae. \emph{Adv. Math.} \textbf{58} (1985), 300--321.
\bibitem{aswe} M. Aissen, I. J. Schoenberg and A. M. Whitney. On the generating functions of totally positive sequences I. \emph{J. Analyse Math.} \textbf{2} (1952), 93--103; A. Edrei. On the generating functions of totally positive sequences II. \emph{Ibid.}, 104--109.
\bibitem{holtztyaglov} O. Holtz and M. Tyaglov. Structured matrices, continued fractions, and root localization of polynomials. \emph{SIAM Review} \textbf{54} (2012), 421--509. The theorem cited was read by the author through the account of it in M. Adm, J. Garloff and M. Tyaglov, Total nonnegativity of finite Hurwitz matrices and root location of polynomials, arXiv:1711.04651.
\bibitem{comptp} K. Justus. Programs \texttt{tp\_profiles.py}, \texttt{tp\_profiles\_v2.py}, \texttt{product\_checks.py} and \texttt{coincidence\_pairs.py}, with their result files, and the Lean files \texttt{WindingCoincidence}, \texttt{WindingSymQuad}, \texttt{WindingTransfer}, \texttt{WindingThreeStep}, \texttt{WindingAxisQuad}, in the computation folder of this edition.
"""
e = r"\end{thebibliography}"; assert t.count(e) == 1
open(m, "w").write(t.replace(e, bib + e)); print("assembled")
