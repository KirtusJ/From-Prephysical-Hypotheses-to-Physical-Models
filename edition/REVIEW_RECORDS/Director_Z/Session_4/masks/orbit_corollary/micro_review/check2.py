"""Follow-up (predicates fixed before run): Q1 which (zeta,g,lam,conj) with all phases in quarter turns connect u=1 coin (1,1,1,-1) to u=-1 coin (1,1,-1,1) on N=4; is g outside {+-1} required. Q2 rail phase lam=e^(2pi i/8) with beta!=0 changes P (sharpness needed)."""
exec(open("check.py").read().split("# P0")[0])
exec("\n".join(l for l in open("check.py").read().split("\n") if l.startswith("def ") or l.startswith("    ") or l.startswith("  ") or l.startswith("      ")) if False else "")
