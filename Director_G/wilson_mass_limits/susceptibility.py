"""Finite sine-kernel Hessian for the constant two-spin direction (mpmath)."""
from mpmath import mp

def endpoint_hessian(length):
    n = 2*length
    mp.dps = 2*n + 35
    b = mp.matrix(n)
    for i in range(n):
        for j in range(n):
            delta = i-j
            b[i,j] = (mp.mpf('0.5') if not delta else
                      mp.sinpi(mp.mpf(delta)/2)/(mp.pi*delta))
    occ, eigenvectors = mp.eigsy(b)
    # U maps sigma_z in each spin block to -sigma_x. Staggering supplies (-1)^j.
    first = mp.matrix([(-1)**(i//2)/mp.sqrt(length) if i%2==0 else 0 for i in range(n)])
    second = mp.matrix([(-1)**(i//2)/mp.sqrt(length) if i%2==1 else 0 for i in range(n)])
    first = eigenvectors.T * first
    second = eigenvectors.T * second
    logit = [mp.log(x)-mp.log1p(-x) for x in occ]
    hessian = mp.mpf(0)
    for i in range(n):
        for j in range(n):
            dd = (logit[i]-logit[j])/(occ[i]-occ[j]) if i!=j else 1/(occ[i]*(1-occ[i]))
            hessian += (first[i]*second[j]+first[j]*second[i])**2*dd
    return (length, mp.nstr(hessian,18), mp.nstr(hessian/(8*mp.pi**2),18))

if __name__ == '__main__':
    print('L   entropy Hessian(Q,Q)       implied coefficient')
    for length in [1,2,4,8,16,24]:
        print(*endpoint_hessian(length))
    print('limits', mp.nstr(4*mp.pi**2/3,18), mp.nstr(mp.mpf(1)/6,18))
