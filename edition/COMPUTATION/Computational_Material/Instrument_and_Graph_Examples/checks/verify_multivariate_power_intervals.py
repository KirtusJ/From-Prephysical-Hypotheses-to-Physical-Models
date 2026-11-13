"""Interval-arithmetic verification of two-simple-law symmetric Bayes error crossings.
Uses all attempts; M counts successes on assigned informative input arms.
Total omitted binomial mass bounded by a geometric series.
"""
import mpmath as mp
mp.iv.dps=70
I=mp.iv

def lower(x):return mp.mpf(str(x.a).split(',')[0].lstrip('['))
def upper(x):return mp.mpf(str(x.b).split(',')[-1].rstrip(']'))

def certify(N:int,h:str,eta:str,Lstr:str,stop:int):
    p=I.mpf(h)*I.mpf(eta); L=I.mpf(Lstr)
    pm=I.exp(N*I.log1p(-p))
    e=I.mpf('0.5'); t=I.mpf(1)
    z=pm*e
    for m in range(1,stop+1):
        pm=pm*(N-m+1)/m*p/(1-p)
        if m%2:
            e=e-(1-2*L)*t/2
        else:
            k=m//2
            t=t*(2*k)*(2*k-1)/(k*k)*L*(1-L)
        z=z+pm*e
    ratio=I.mpf(N-stop)/(stop+1)*p/(1-p)
    remainder=pm*ratio/(1-ratio)
    bound_upper=z.b+remainder.b/2
    bound_lower=z.a  # e >= 0
    target=I.mpf(1)/20
    if bool(bound_lower>target):dec='FAIL: strictly >.05'
    elif bool(bound_upper<target):dec='PASS: strictly <.05'
    else:raise AssertionError('Not certified')
    return z, remainder,dec

for lbl,eta,L,cutoff,pairs in [
    ('wide uniformly randomized','0.5','0.2',220,(14130,14131)),
    ('narrow uniformly randomized','0.5','0.45',760,(540253,540254)),
    ('wide always informative','1','0.2',220,(7064,7065))]:
 print('\n',lbl)
 for N in pairs:
    z,rem,dec=certify(N,'0.001',eta,L,cutoff)
    print(N,dec,'partial-risk',z,'tail-prob<=',rem)
