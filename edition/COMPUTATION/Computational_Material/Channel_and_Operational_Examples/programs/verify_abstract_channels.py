#!/usr/bin/env python3
"""Small finite checks of abstract-channel formulas and an adverse witness.
No physical measurements. Finite checks do not prove the general theorems.
"""
from fractions import Fraction as F
from math import log2, sqrt, log, pi
import json
import numpy as np
from numpy.polynomial.hermite import hermgauss

checks=[]
def check(name, ok):
    if not ok: raise RuntimeError(name)
    checks.append(name)

# Direct expectation of the Gaussian information density by 2D Gauss-Hermite
# quadrature, independently of entropy subtraction. Natural-log density ratio
# is divided by log(2). Quadrature inputs are standard-normal transforms.
nodes,weights=hermgauss(24)
results=[]
for P,N in [(F(1,4),F(1)),(F(3),F(1)),(F(2),F(5)),(F(7,3),F(2,5))]:
    p,n=float(P),float(N)
    val=0.0
    for u,wu in zip(nodes,weights):
        x=sqrt(2*p)*u
        for v,wv in zip(nodes,weights):
            z=sqrt(2*n)*v
            y=x+z
            # log p(y|x) - log p(y), with Y~Normal(0,P+N)
            density_ratio=(0.5*log((p+n)/n)-z*z/(2*n)+y*y/(2*(p+n)))/log(2)
            val += wu*wv*density_ratio/pi
    target=0.5*log2(1+p/n)
    check(f'gaussian_quadrature_{P}_{N}',abs(val-target)<2e-12)
    # Complex-channel convention: real/imag noise each N/2 and budget each P/2.
    complex_val=2*(0.5*log2(1+(p/2)/(n/2)))
    check(f'complex_factor_{P}_{N}',abs(complex_val-log2(1+p/n))<1e-14)
    results.append({'P':str(P),'noise_variance':str(N),'quadrature_bits_per_real_coordinate':val,'analytic_bits':target})

# Ideal additive Rademacher channel at fixed budget P=1/4 and Var(Z)=1.
# All constellation points are strictly between -1/2 and 1/2.
constellations=[]
a=F(1,2); P=F(1,4)
for M in [2,3,5,17,64,257]:
    xs=[a*F(2*j-M-1,M+1) for j in range(1,M+1)]
    check(f'constellation_distinct_{M}',len(set(xs))==M)
    check(f'constellation_open_interval_{M}',all(-a<x<a for x in xs))
    cost=sum(x*x for x in xs)/M
    check(f'cost_bound_{M}',cost<P)
    mapping={}
    for j,x in enumerate(xs):
        for z in [F(-1),F(1)]:
            y=x+z
            decoded_z=F(1) if y>0 else F(-1)
            decoded_x=y-decoded_z
            check(f'exact_decode_{M}_{j}_{z}',decoded_z==z and decoded_x==x)
            if y in mapping and mapping[y]!=j:
                raise RuntimeError('Confusable distinct messages')
            mapping[y]=j
    check(f'output_disjointness_{M}',len(mapping)==2*M)
    constellations.append({'M':M,'cost':str(cost),'zero_error_bits':log2(M)})

# Same total noise variance, different Gaussian allocation geometry.
# Two real coordinates, total second-moment budget 2.
# Noise variances 1/2,3/2; optimum costs 3/2,1/2.
noise=(F(1,2),F(3,2)); signal=(F(3,2),F(1,2))
check('equal_total_noise',sum(noise)==2)
check('equal_total_cost',sum(signal)==2)
check('equal_waterline',noise[0]+signal[0]==noise[1]+signal[1]==2)
ratio=(1+signal[0]/noise[0])*(1+signal[1]/noise[1])
check('anisotropic_determinant_ratio',ratio==F(16,3))
isotropic=log2(2)
anisotropic=0.5*log2(float(ratio))
check('same_trace_different_capacity',anisotropic>isotropic)

out={
 'status':'PASS','finite_checks':len(checks),
 'gaussian_quadrature':results,
 'rademacher_constellations':constellations,
 'two_coordinate_equal_trace_control':{'isotropic_bits':isotropic,'anisotropic_bits':anisotropic,'anisotropic_ratio':'16/3'},
 'limitations':[
  'The Gaussian supremum and unbounded family of zero-error constellations require the accompanying proofs.',
  'The Rademacher witness assumes exact real-valued output and non-Gaussian discrete noise.',
  'Coordinate counts and second moments carry no physical time or energy interpretation in these checks.',
  'No finite-block zero-error claim is made for nondegenerate Gaussian noise.'
 ]
}
print(json.dumps(out,indent=2,sort_keys=True))
