"""Model and numerical checks, Kirtus Justus, Vancouver, 7 November 2026."""
import mpmath as m
from fractions import Fraction as F
m.mp.dps=65
s=m.mpf(131)/320; h=m.mpf(99)/100; q=m.mpf(81711338569043)/224995905216000
a=s+(m.sqrt(q)-m.sqrt(s*h))**2/(1-h)+m.mpf('.06')/13
c=m.mpf('.96')
def G(x): return (c*m.sqrt(x)+m.sqrt((1-c*c)*(1-x)))**2
split=m.findroot(lambda b:G(a+b)-G(a)-m.mpf('.04')+b,(0,m.mpf('.04')))
neighbor=G(a+split)
t=(2+a+G(a)+m.mpf('.04'))/4
click=G(1-a)-(1-a); purity=t*t+(1-t)**2
assert click<m.mpf('.272954') and neighbor<m.mpf('.810954608659') and purity<m.mpf('.732104302723')
print('Click contrast, split, neighbor, purity:',*[m.nstr(x,23) for x in [click,split,neighbor,purity]])
g=F(1,25);u=(4-2*g)/2;pstar=F(1,2)
assert (pstar*g,pstar*u,1-(2*g)/8)==(F(1,50),F(49,50),F(99,100))
print('Exact success-only counterexample passed.')
