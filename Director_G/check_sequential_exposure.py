"""Interval bounds on prior-averaged expected pair count under sequential stopping."""
from fractions import Fraction as Q
from mpmath import iv
from check_paired_exposure import cells, rates


def dec(x):
    return iv.mpf(x.numerator)/x.denominator


def main():
    iv.dps=60
    rows=[]
    for s,g,l in rates():
        p,q=cells(s,Q(1,10**8)*g),cells(s,Q(1,10**8)*l)
        z=[iv.ln(dec(a/b)) for a,b in zip(p,q)]
        dp=sum(dec(a)*v for a,v in zip(p,z))
        dq=-sum(dec(a)*v for a,v in zip(q,z))
        rows.append((s,dp,dq,max(abs(v).b for v in z)))
    best=max(rows,key=lambda row: row[1].a)
    s,dp,dq,b=best
    D=max(max(row[1].b,row[2].b) for row in rows)
    lo=iv.mpf('0.90')*iv.ln(19)/D
    a=iv.ln(19)+b
    # Any stopped path overshoots by at most b. Compare its likelihood under both laws.
    upper_error=(1-iv.exp(-a-b))/(iv.exp(a)-iv.exp(-a-b))
    lower_error=(1-iv.exp(-a))/(iv.exp(a+b)-iv.exp(-a))
    assert upper_error < iv.mpf('0.05')
    mean_log_cap=a+b-(2*a+b)*lower_error
    upper_P,upper_Q=mean_log_cap/dp,mean_log_cap/dq
    upper=(upper_P+upper_Q)/2
    print('node',float(s),'b',float(b),'max KL',float(D))
    print('error interval',float(lower_error.a),float(upper_error.b))
    print('lower',float(lo.a),'upper',float(upper.b),'by law',float(upper_P.b),float(upper_Q.b))
    assert lo > 1861452480000000 and upper < 1861453214000000


if __name__=='__main__':
    main()
