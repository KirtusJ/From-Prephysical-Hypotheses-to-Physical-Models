"""Exact checks for attempt selection and a calibrated qubit effect. No simulated observations."""
from fractions import Fraction as Q
from math import comb
from collections import defaultdict

def require(ok, reason):
    if not ok:
        raise ArithmeticError(reason)

def crosses(n,k):
    odds=Q(2)**(2*k-n)
    return odds+1/odds >= 40 * Q(33,25)**n

def crossing_probabilities(n):
    surviving={0:Q(1)}
    for step in range(1,n+1):
        upcoming=defaultdict(Q)
        for k,p in surviving.items():
            for count,weight in ((k,Q(1,10)),(k+1,Q(9,10))):
                if not crosses(step,count):
                    upcoming[count] += p*weight
        surviving=upcoming
    fixed=sum(comb(n,k)*Q(9,10)**k*Q(1,10)**(n-k)
              for k in range(n+1) if crosses(n,k))
    by=1-sum(surviving.values())
    # Independent backward stopping recursion.
    value={k:Q(int(crosses(n,k))) for k in range(n+1)}
    for step in reversed(range(n)):
        value={k:(Q(1) if crosses(step,k) else (value[k]+9*value[k+1])/10)
               for k in range(step+1)}
    require(value[0]==by,'Backward and forward stopping recursions differ.')
    return fixed,by

def check_calibrated_effect():
    low,high=Q(1,8),Q(7,8)
    spectrum=[(Q(1,25),Q(4,25)),(Q(9,100),Q(1,100))]
    for row in spectrum:
        pop_plus,pop_minus=row
        success=pop_plus+pop_minus
        click=high*pop_plus+low*pop_minus
        require((click-low*success)/(high-low)==pop_plus,'Spectral probability inversion')
        for d_plus,d_minus in [(Q(-2),Q(1,3)),(Q(1,2),Q(-1))]:
            scores=[d_minus+(y-low)*(d_plus-d_minus)/(high-low) for y in (0,1)]
            require(scores[0]*(success-click)+scores[1]*click==d_plus*pop_plus+d_minus*pop_minus,
                    'Dual score uses observed outcomes.')
    # With rational square-root weights the spectral discrepancy is exactly 0.10.
    require((Q(1,5)-Q(3,10))**2+(Q(2,5)-Q(1,10))**2==Q(1,10),'Squared discrepancy')
    print('Calibrated-effect inversion and signed-score identity passed.')

if __name__=='__main__':
    fixed,by=crossing_probabilities(20)
    require(fixed==Q(43352333828283669431,50000000000000000000),'Terminal probability')
    require(by>fixed,'Cumulative probability must exceed terminal probability for this case.')
    require([k for k in range(21) if crosses(20,k)]==[0,1,2,3,17,18,19,20],'Boundary')
    print('At 20 successes:',fixed,f'{float(fixed):.12f}')
    print('Ever by 20 successes:',by,f'{float(by):.12f}')
    check_calibrated_effect()
