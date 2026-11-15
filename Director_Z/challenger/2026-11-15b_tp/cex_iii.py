"""Counterexample to the 'Equivalently' of cor:tp(iii) as worded (predicate fixed: W has a root with Re>0
while u/g, v/g satisfy the interlacing form vacuously). u=v=X^2+X+1 (nonnegative coefficients)."""
import sympy as sp
X,Y=sp.symbols('X Y'); u=v=X**2+X+1
g=sp.gcd(u,v); print('u/g',sp.cancel(u/g),'v/g',sp.cancel(v/g))
W=sp.expand(v.subs(X,Y**2)+Y*u.subs(X,Y**2)); print('W',sp.factor(W))
print('max Re root', max(sp.re(r) for r in sp.Poly(W,Y).nroots()))
